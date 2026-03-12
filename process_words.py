#!/usr/bin/env python3
"""
Process the Morph-it! morphological lexicon into a clean word list for ABCx3.

Source: https://docs.sslmit.unibo.it/doku.php?id=resources:morph-it
Authors: Marco Baroni, Eros Zanchetta (Università di Bologna)
License: CC BY-SA 2.0 / LGPL (dual license)

Processing steps:
  1. Read the Morph-it! tab-delimited file (latin-1 encoded)
     Format: inflected_form <TAB> lemma <TAB> morphological_tag
  2. Remove proper nouns (tag contains 'NPR')
  3. Remove entries with non-alphabetic characters (punctuation, symbols,
     emoticons, digits, spaces, apostrophes)
  4. Strip accents: Italian word games (Scarabeo) use unaccented a–z tiles,
     so à→a, è/é→e, ì→i, ò→o, ù→u. This matches traditional Italian
     Scrabble (Scarabeo) rules where only a–z tiles exist.
  5. Remove single-letter words (not valid in word games)
  6. Deduplicate
  7. Sort alphabetically
  8. Write one word per line (no header)

Usage:
  python3 process_words.py <input_file> <output_file>
  python3 process_words.py morph-it_048.txt words_it-IT.txt

where <input_file> is the raw Morph-it! lexicon file
(e.g. morph-it_048.txt from the morph-it.tgz archive).
"""

import os
import sys
import unicodedata


# Two-letter abbreviations to REMOVE.
# These are measurement / political-party / technical abbreviations that have
# no standalone use as an Italian game word:
#   br  – bromuro / Brasile
#   cc  – centimetri cubici / carbon copy
#   ct  – commissario tecnico
#   dc  – Democrazia Cristiana
#   dg  – decagrammo
#   ds  – Democratici di Sinistra
#   dt  – (technical abbrev)
#   gr  – grammo
#   gt  – (technical abbrev)
#
# Words retained because they are used as regular Italian nouns / words:
#   cd  – compact disc ("ho comprato un cd")
#   dj  – disc jockey ("il dj")
#   go  – the board game ("una partita a go")
#   ex  – former partner ("il mio ex")
ABBREVIATIONS_TO_REMOVE: set[str] = {
    'br',   # Bromuro / Brasile abbreviation
    'cc',   # Centimetri cubici / carbon copy
    'ct',   # Commissario tecnico
    'dc',   # Democrazia Cristiana
    'dg',   # Decagrammo
    'ds',   # Democratici di Sinistra
    'dt',   # Technical abbreviation
    'gr',   # Grammo
    'gt',   # Technical abbreviation
}


def strip_accents(s: str) -> str:
    """Normalize accented Italian vowels to their plain ASCII equivalents.

    Covers the accented vowels present in the Morph-it! corpus:
      à → a,  è/é → e,  ì/î/ï → i,  ò/ó/ô → o,  ù/ú → u
    Uses Unicode NFKD decomposition to split base letter from combining
    accent, then drops any remaining non-ASCII combining marks.
    """
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def process(input_path: str, output_path: str) -> None:
    with open(input_path, encoding='latin-1') as f:
        raw_lines = f.readlines()

    seen: set[str] = set()
    kept: list[str] = []
    removed_npr = 0
    removed_non_alpha = 0
    removed_single = 0
    removed_abbrev = 0

    for line in raw_lines:
        line = line.rstrip('\n')
        parts = line.split('\t')
        if len(parts) < 3:
            continue

        word, _lemma, tag = parts[0], parts[1], parts[2]

        # 1. Remove proper nouns (tagged NPR)
        if 'NPR' in tag:
            removed_npr += 1
            continue

        # 2. Lowercase
        lower = word.lower()

        # 3. Strip accents (à→a, è/é→e, ì→i, ò→o, ù→u)
        stripped = strip_accents(lower)

        # 4. Keep only purely alphabetic a–z words
        if not stripped.isalpha() or not stripped.isascii():
            removed_non_alpha += 1
            continue

        # 5. Skip single-letter words (not valid in word games)
        if len(stripped) < 2:
            removed_single += 1
            continue

        # 6. Remove pure abbreviations / acronyms
        if stripped in ABBREVIATIONS_TO_REMOVE:
            removed_abbrev += 1
            continue

        # 7. Deduplicate
        if stripped not in seen:
            seen.add(stripped)
            kept.append(stripped)

    kept.sort()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(kept) + '\n')

    total_input = sum(1 for ln in raw_lines if ln.strip())
    print(f"Input lines (non-blank):  {total_input:>8,}")
    print(f"Removed proper nouns:     {removed_npr:>8,}  (NPR tag)")
    print(f"Removed non-alpha/symbol: {removed_non_alpha:>8,}  (punct, digits, apostrophes, etc.)")
    print(f"Removed single-letter:    {removed_single:>8,}")
    print(f"Removed abbreviations:    {removed_abbrev:>8,}  ({', '.join(sorted(ABBREVIATIONS_TO_REMOVE))})")
    print(f"Unique words after dedup: {len(kept):>8,}")
    print(f"Output written to:        {output_path}")


if __name__ == '__main__':
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _default_input = os.path.join(_script_dir, 'morph-it_048.txt')
    _default_output = os.path.join(_script_dir, 'output', 'italian_it_it_morphit.txt')
    if len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} [input_file [output_file]]")
        sys.exit(1)
    _input = sys.argv[1] if len(sys.argv) > 1 else _default_input
    _output = sys.argv[2] if len(sys.argv) > 2 else _default_output
    os.makedirs(os.path.dirname(_output), exist_ok=True)
    process(_input, _output)
