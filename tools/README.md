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
```

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
