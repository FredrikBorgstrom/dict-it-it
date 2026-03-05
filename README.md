# dict-it-it

Italian word list for the [ABCx3](https://abcx3.com) crossword game.

## Source

The word list is derived from **Morph-it!**, a free corpus-based morphological
resource for the Italian language, version 0.4.8.

> Baroni, M. and Zanchetta, E. (2008).
> *Morph-it! A free corpus-based morphological resource for the Italian language.*
> In Proceedings of the Ninth Meeting of the ACL Special Interest Group in
> Computational Morphology and Phonology, pages 21–28, Columbus, Ohio.
> Association for Computational Linguistics.

The source lexicon was created by **Marco Baroni** and **Eros Zanchetta** at the
University of Bologna using corpus-based methods, regular-expression-based rules,
and manual checking against the CORIS/CODIS Italian reference corpus.

The lexicon contains 504,906 entries with morphological analyses (inflected form,
lemma, and morphological features).

## License

The source Morph-it! lexicon and this derived work are dual-licensed under:

- [Creative Commons Attribution ShareAlike 2.0 (CC BY-SA 2.0)](https://creativecommons.org/licenses/by-sa/2.0/)
- [GNU Lesser General Public License (LGPL)](https://www.gnu.org/licenses/lgpl.html)

You may choose either license. Both permit commercial use. The CC BY-SA 2.0 option
requires attribution and that derivative works be shared under the same license.
**Note:** This repository is public as required by the CC BY-SA 2.0 ShareAlike
clause. The ABCx3 game code is a separate work and is not affected by this
requirement.

### Attribution

> Italian word list derived from **Morph-it!** by Marco Baroni and Eros Zanchetta.
> University of Bologna, SLI-IACOBUCCI Lab.
> Source: https://docs.sslmit.unibo.it/doku.php?id=resources:morph-it
> Licensed under CC BY-SA 2.0 and LGPL.
>
> Reference: Baroni, M. and Zanchetta, E. (2008). Morph-it! A free corpus-based
> morphological resource for the Italian language. Proceedings of the 9th Meeting
> of the ACL SIGMORPHON, Columbus, Ohio.

## Processing

The raw source file was processed with `process_words.py`:

1. **Proper nouns excluded** — entries tagged `NPR` (proper names, place names,
   person names) are removed. Morph-it! tags proper nouns explicitly, making
   this a clean filter.
2. **Non-alphabetic entries removed** — punctuation, symbols, emoticons, digits,
   spaces, apostrophes (e.g. `'ndrangheta`, `4x4`, emoticons) are excluded.
3. **Accent-stripping** — Italian word games (Scarabeo) use only unaccented a–z
   tiles; accented vowels are normalised to their plain equivalents:
   à→a, è/é→e, ì/î/ï→i, ò/ó/ô→o, ù/ú→u.
   This matches the traditional Italian Scrabble (Scarabeo) tile convention.
4. **Pure abbreviations removed** — two-letter measurement and political-party
   abbreviations (`br`, `cc`, `ct`, `dc`, `dg`, `ds`, `dt`, `gr`, `gt`) are
   excluded. Abbreviations widely used as standalone Italian nouns (`cd`, `dj`)
   are retained.
5. **Single-letter words removed** — not valid in word games.
6. **Deduplicated and sorted** alphabetically.

### Stats

| Metric | Count |
|---|---|
| Source entries (Morph-it! v0.4.8) | 505,074 |
| Removed proper nouns (NPR) | 2,848 |
| Removed non-alpha / symbols | 5,454 |
| Removed single-letter | 8 |
| Removed abbreviations | 22 |
| **Unique words after processing** | **393,253** |

## Word quality

- ✅ Comprehensive inflections included (all verb conjugations across all persons,
  tenses and moods; noun singular/plural; adjective m/f/s/p and superlative forms)
- ✅ No proper nouns, place names, or person names (filtered by NPR tag)
- ✅ Pure a–z (26 Latin letters only; accents stripped to match Scarabeo rules)
- ✅ No hyphens, digits, apostrophes, or special characters
- ✅ Corpus-attested Italian (derived from the CORIS/CODIS reference corpus)
- ⚠️ The source was extracted from a newspaper corpus, so some very common
  everyday words may have lower frequency or be absent; coverage is strongest for
  formal written Italian
- ⚠️ A small number of adjectives derived from proper names (e.g. `casertano`,
  `zurliniano`) are present; these are established Italian common adjectives
  with their own dictionary entries

## Alphabet

```
abcdefghijklmnopqrstuvwxyz
```

## Usage in ABCx3

The processed file `words_it-IT.txt` is imported into the `dict_it_it`
database table. The bag configuration uses the standard Italian alphabet
(26 Latin letters a–z, matching Scarabeo rules).

## Reproducing the processed file

```bash
python3 process_words.py morph-it_048.txt words_it-IT.txt
```

where `morph-it_048.txt` is the raw lexicon file from the Morph-it! archive
(`morph-it.tgz`) downloaded from
[https://docs.sslmit.unibo.it/doku.php?id=resources:morph-it](https://docs.sslmit.unibo.it/doku.php?id=resources:morph-it).
