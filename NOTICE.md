# Notice & attribution

The **application code** in `index.html` and `tools/` is MIT licensed (see [LICENSE](LICENSE)).

The **deck data embedded in `index.html`** (the `WORDS` and `PHRASES` arrays) is derived from the
third-party sources below and remains under their licences. If you redistribute this file, you are
redistributing that data too — keep this notice with it.

---

## 1. Word definitions and pinyin — CC-BY-SA 4.0

Sourced via [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary) by
Yanis Zafirópulos (MIT licensed), which takes its dictionary definitions from:

> **CC-CEDICT** — <https://www.mdbg.net/chinese/dictionary?page=cc-cedict>
> Licensed under the Creative Commons Attribution-ShareAlike 4.0 International License
> (<https://creativecommons.org/licenses/by-sa/4.0/>).

Because CC-CEDICT is **ShareAlike**, the definitions in this deck — and any modified version of
them — must stay under CC-BY-SA 4.0 with attribution. That applies to the data, not to the app
code around it.

Frequency ranks in the same dataset derive from **SUBTLEX-CH**
(<http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-ch>), and its part-of-speech
tags — used here for the Verbs/Nouns/Conjunctions categories — come from SUBTLEX-CH and
[HanLP](https://github.com/hankcs/HanLP).

## 2. Phrases — CC-BY 2.0 FR

> **Tatoeba** — <https://tatoeba.org>
> Sentences and translations from the Tatoeba Project, licensed under
> Creative Commons Attribution 2.0 France (<https://creativecommons.org/licenses/by/2.0/fr/>).

Used here: Mandarin sentences paired with English translations, filtered and converted to
simplified characters. Attribution to Tatoeba and its contributors is required.

## 3. Pinyin generation for phrases — MIT

> **pypinyin** — <https://github.com/mozillazg/python-pinyin> (MIT)
> **jieba** — <https://github.com/fxsjy/jieba> (MIT)
> **zhconv** — <https://github.com/gumblex/zhconv> (MIT)

Used at build time only; no part of them ships in `index.html`.

## 4. Noun illustrations — CC BY-SA 4.0

> **OpenMoji** — <https://openmoji.org>
> The open-source emoji and icon project, licensed under
> Creative Commons Attribution-ShareAlike 4.0 International
> (<https://creativecommons.org/licenses/by-sa/4.0/>).

The cartoon illustrations shown on concrete-noun cards (the `IMAGES` map in
`index.html`) are OpenMoji colour SVGs, embedded at build time by
`tools/build_images.py`. Because OpenMoji is **ShareAlike**, these images — and any
modified version — must stay under CC BY-SA 4.0 with attribution to OpenMoji. That
applies to the embedded art, not to the app code around it.

## 5. UI icons — ISC

> **Lucide** — <https://lucide.dev>
> Icon set licensed under the ISC licence (a fork of Feather Icons).

The interface icons (the `ICONS` map in `index.html`) are Lucide SVGs, inlined at
build time by `tools/build_icons.py`. The ISC licence permits use with attribution;
its copyright notice is reproduced here for the Lucide and Feather contributors.

## 6. Curated essentials

The 44 everyday expressions listed in `tools/build_supplement.py` (你好, 早上好, 多少钱, …) were
written for this project and are covered by the MIT licence above. HSK word lists omit them
because they parse as compounds.

---

## Summary

| Part | Licence |
| --- | --- |
| App code (`index.html` markup/CSS/JS, `tools/*.py`) | MIT |
| Word definitions + pinyin in the deck | CC-BY-SA 4.0 (CC-CEDICT) |
| Phrase sentences + translations | CC-BY 2.0 FR (Tatoeba) |
| Noun illustrations (`IMAGES` in `index.html`) | CC-BY-SA 4.0 (OpenMoji) |
| UI icons (`ICONS` in `index.html`) | ISC (Lucide) |
| Curated essentials | MIT |
