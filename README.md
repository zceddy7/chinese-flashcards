# Chinese Flashcards

A single-file Chinese flashcard app. **No install, no build, no account, works offline** — open
`index.html` in a browser and study. Progress is saved in the browser's local storage.

**[Download the latest version](../../releases/latest)** · or clone the repo · or
[grab `index.html` directly](../../raw/main/index.html) and double-click it.

---

## What's in it

**10,450 cards** — 7,412 words and 3,038 phrases, introduced **most-common-first**, so the
vocabulary you actually need comes up before the rare stuff.

- **Two answer modes.** *Tapping* — flip the card and grade yourself. *Typing* — type the answer
  and have it checked.
- **Per-direction mastery.** Progress is tracked for each *direction* separately, not per card.
  你好 is six skills: 汉字→English, English→汉字, 汉字→pinyin, pinyin→汉字, pinyin→English,
  English→pinyin. Recognising a word doesn't mean you can produce it, so each direction needs its
  own five correct answers before it retires to the **Got it pile**.
- **Pick your directions.** Study only pinyin→English, or only English→汉字, or any mix.
- **Categories.** 16 topics (food, travel, feelings, …), 11 word types (verbs, conjunctions,
  measure words, …), plus Misc. Multi-select, and cards can belong to several — 吃饭 is *food*,
  *home* and a *verb*.
- **Words / phrases filter.** One button.
- **Tone palette.** Type `zen me`, tap `ě`, get `zěn me`. Tapping a toned vowel upgrades the plain
  letter you already typed rather than inserting a second one.
- **Forgiving answer checking.** Tones are partial credit (`hong` for `hóng` counts, with a nudge);
  case and spacing are ignored; a card glossed "he / him" accepts `he`, `him`, or the whole thing.
- **Audio.** Chinese text-to-speech on any card showing hanzi or pinyin — never on a card where
  hearing it would give away the answer.
- **Character style.** Microsoft YaHei (how characters look in phone messaging) or SimSun (print).
- **Add your own.** One at a time, or paste a whole list — tab / `|` / `;` / comma separated, with
  a live preview and duplicate detection.

## Keyboard

| Key | Does |
| --- | --- |
| `space` | reveal the answer |
| `1` / `2` | Again / Got it |
| `Enter` | check a typed answer, then advance |
| `s` | replay audio |

## Where the data comes from

Nothing here was written from memory — for a language app a wrong tone is worse than a missing word.

- **Words** — HSK 1–6 vocabulary from
  [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary), whose
  definitions come from [CC-CEDICT](https://www.mdbg.net/chinese/dictionary) and whose frequency
  ranks come from SUBTLEX-CH (subtitle frequencies — real-world usage).
- **Phrases** — [Tatoeba](https://tatoeba.org) sentence pairs, filtered to sentences built only
  from HSK vocabulary and 3–14 characters long, so they're practical rather than random. Pinyin
  generated with [pypinyin](https://github.com/mozillazg/python-pinyin), fed the dictionary
  readings so a word reads the same on a phrase card as on its own card.
- **44 curated essentials** — HSK word lists don't contain 你好 (they treat it as 你 + 好), so
  greetings and everyday expressions were added by hand and tone-checked.

See [NOTICE.md](NOTICE.md) for licences and attribution.

### Known limits

- **Topic tags are keyword-derived** from the English glosses, so they're imperfect. Word types
  (verb/noun/conjunction/…) come from the dataset's own part-of-speech tags and are reliable.
  ~17% of cards land in **Misc**.
- **Cards you add go to Misc**, since tagging runs at build time, not in the browser.
- Progress lives in browser local storage: **per browser, not synced**, and cleared if you clear
  site data.

## Rebuilding the deck

Only needed if you want to change the deck. `tools/` holds the scripts; see
[tools/README.md](tools/README.md).

## Licence

App code: [MIT](LICENSE).

> [!IMPORTANT]
> **The deck data embedded in `index.html` is not MIT.** The word definitions derive from
> CC-CEDICT (**CC-BY-SA 4.0** — ShareAlike) and the phrases from Tatoeba (**CC-BY 2.0 FR**).
> Both require attribution, and ShareAlike carries over to modified versions of the data.
> Read [NOTICE.md](NOTICE.md) before redistributing.
