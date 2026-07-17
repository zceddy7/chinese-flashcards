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
- **Listening cards.** 🎧 The card plays the audio and nothing else — recall the English, the
  pinyin, or the characters from sound alone. Two slow-down buttons (**60%** and **40%**) for when
  it goes past too fast.
- **Hint button.** Reveals the pinyin without giving the answer away. It hides itself whenever the
  pinyin *is* the answer being asked for.
- **A small rotation, not the whole deck.** Only ~20 items are in play at once, so the deck feels
  learnable instead of endless. Get one right **5 times in a row** and it graduates to the **Got it
  pile**, and the next (most-common-first) drops into its slot. A miss resets it to 0. Adjust the
  size under *Study settings → In rotation*.
- **Each direction stands alone.** 你好→hello and hello→你好 are separate items with separate
  progress — recognising a word isn't the same as producing it. So the rotation is 20 *directions*
  (drawn from the directions you turn on: 汉字→English, English→汉字, 汉字→pinyin, pinyin→汉字,
  pinyin→English, English→pinyin, and three listening ones), and each graduates on its own.
- **Skip and reshuffle.** *Skip* parks the current item and moves on, no change to progress.
  *Reshuffle card* sends the current one back into the big pile and pulls a fresh one; *New 20*
  sends the whole on-deck set back and grabs 20 new items.
- **Noun pictures.** Concrete nouns show a cartoon illustration — 🍎 for 苹果, 🐟 for 鱼 — so the
  object attaches to the characters and pinyin, not to an English word. The picture only appears
  when it can't give the answer away (when English is the prompt, or after you reveal).
- **Pick your directions.** Study only pinyin→English, or only 🎧→English, or any mix.
- **Categories.** 16 topics (food, travel, feelings, …), 11 word types (verbs, conjunctions,
  measure words, …), plus Misc. Multi-select, and cards can belong to several — 吃饭 is *food*,
  *home* and a *verb*.
- **Words / phrases filter.** One button.
- **Tone palette.** Type `zen me`, tap `ě`, get `zěn me`. Tapping a toned vowel upgrades the plain
  letter you already typed rather than inserting a second one.
- **Forgiving answer checking.** Tones are partial credit (`hong` for `hóng` counts, with a nudge);
  case and spacing are ignored; a card glossed "he / him" accepts `he`, `him`, or the whole thing.
- **Audio.** Chinese text-to-speech on any card showing hanzi or pinyin — never on a card where
  hearing it would give away the answer. Uses the browser's own speech engine, so it needs a
  Chinese voice installed; listening cards disappear if the browser has no speech at all.
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
| `k` | skip this item |

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
- **Noun illustrations** — cartoon SVGs from [OpenMoji](https://openmoji.org) (CC BY-SA 4.0),
  embedded at build time for concrete nouns.

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
> CC-CEDICT (**CC-BY-SA 4.0** — ShareAlike), the phrases from Tatoeba (**CC-BY 2.0 FR**), and the
> noun illustrations from OpenMoji (**CC-BY-SA 4.0**). All require attribution, and ShareAlike
> carries over to modified versions. Read [NOTICE.md](NOTICE.md) before redistributing.
