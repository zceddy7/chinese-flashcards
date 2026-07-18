# Deck build scripts

You don't need these to use the app — the deck is already baked into `index.html`. They're here so
the deck is reproducible and its provenance is auditable.

## Requirements

```bash
pip install pypinyin jieba zhconv
```

## Sources to download first

```bash
# HSK vocabulary: definitions (CC-CEDICT), frequency ranks, parts of speech
curl -Lo hsk.json https://raw.githubusercontent.com/drkameleon/complete-hsk-vocabulary/main/complete.min.json

# Tatoeba sentence pairs (~25 MB for the English side)
curl -Lo cmn_sentences.tsv.bz2    https://downloads.tatoeba.org/exports/per_language/cmn/cmn_sentences.tsv.bz2
curl -Lo cmn-eng_links.tsv.bz2    https://downloads.tatoeba.org/exports/per_language/cmn/cmn-eng_links.tsv.bz2
curl -Lo eng_sentences.tsv.bz2    https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2
bunzip2 -k *.bz2
```

## Run in order

```bash
python build_words.py          # -> words.json       HSK 1-6, best reading per word
python build_phrases.py 3000   # -> phrases.json     Tatoeba, HSK-only vocabulary
python build_supplement.py     # -> supplement.json  essentials HSK omits (你好, …)
python build_categories.py     # -> cats.json        topics + word types
python inject.py               # rewrites ../index.html
python build_images.py         # embeds noun illustrations into ../index.html
```

`build_images.py` is independent of the deck build — it reads the hanzi already
baked into `index.html`, downloads the matching OpenMoji SVGs (CC BY-SA 4.0),
strips their ids, and writes an `IMAGES` map between the `IMAGES-START` /
`IMAGES-END` markers. Re-runs replace the block; downloads are cached under
`tools/_img_cache/` so repeat runs are offline. Add a noun by putting a
`hanzi -> codepoint` line in its `NOUN_EMOJI` map and re-running. It needs
network access only the first time each image is fetched.

`fix_sandhi.py` rewrites the baked pinyin to apply 一/不 tone sandhi (the spoken
tone, not the citation tone the dictionary gives). Run it with no args for a
preview (`_sandhi_preview.txt`) and `--apply` to rewrite `index.html`. It keeps
citation tone for ordinals/dates/counting and leaves rows it can't align cleanly.
It's idempotent — a second run finds nothing to change.

`build_icons.py` works the same way for the UI icons: it downloads the Lucide
SVGs (ISC) named in its `NAMES` map, inlines them as an `ICONS` map between the
`ICONS-START` / `ICONS-END` markers, and caches under `tools/_icon_cache/`. Add a
UI icon by adding a `key -> lucide-name` line and re-running. The app has no
emoji; every glyph in the chrome is a Lucide icon rendered from this map.

## Notes on the tricky bits

**Picking the right reading.** The dataset's first form for a word is often a surname or a rare
variant — taking it at face value gives 说 = `shuì` ("to persuade"), 都 = `Dū`, 个 = `gě`.
`build_words.py` scores the forms instead: proper nouns are demoted, "variant of …" glosses are
rejected, and the form carrying the most real meaning wins.

**Keeping whole-parenthetical glosses.** 了's only definition is "(completed action marker)".
Stripping parentheticals wholesale deletes it and silently drops the 2nd most common word in the
language, so a gloss that is *entirely* parenthetical gets unwrapped rather than emptied.

**Consistent pinyin.** `build_phrases.py` injects the word deck's dictionary readings into pypinyin
via `load_phrases_dict`, so 朋友 reads `péng you` inside a phrase, matching its own card.

**Category false positives.** Keyword matching on English glosses tags 吃苦 "to bear hardships" as
*animal* and 因为 "on account of" as *money* unless you intervene. `build_categories.py` strips
parentheses before matching (usage notes like "to miss (train, opportunity etc)" are not about
travel) and bans ~30 ambiguous words per lexicon.

**Frequency ordering.** HSK ranks are shifted by +100 so the curated essentials (rank 0–99) lead:
a learner should meet 你好 before the particle 的, even though 的 is the single most common word.
