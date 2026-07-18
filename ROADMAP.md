# Roadmap

Ideas noted for later, roughly in the order worth doing. Nothing here is started.

---

## 1. Export / import progress  ← do first

**Why:** all progress lives in one browser's `localStorage` under key
`chinese-flashcards-v1`. Clearing site data, switching browsers, or a new machine wipes it with no
recovery. The deck file syncs (it's in a repo / OneDrive); the progress does not.

**Shape:** a "Download backup" button that dumps `state` to a JSON file, and a "Restore" that reads
one back through the same merge path `load()` already uses. Roughly 30 lines. Also doubles as the
way to move progress between machines.

**Watch for:** restoring an older backup shouldn't drop newer built-in cards — run it through
`mergeBuiltIn()` rather than replacing `state.cards` wholesale.

## 2. Daily new-card limit + a session finish line  ← largely handled

**Update:** the **~20-item rotation** now does most of this. Only ~20 *directions* are ever in play;
each graduates after 5 correct in a row and the next by frequency takes its slot, so the header shows
`20 in rotation · N got it · M to go` and the "to go" count actually drops. What's *not* done: a
per-day cap or a midnight reset — the rotation is continuous, not day-scoped. See `ROTATION_SIZE`,
`refillRotation()`, `poolUnits()` and the `unitKey`/`benched` machinery in `index.html`.

**Why:** the header reads "62,700 new" and never visibly drops. It's demotivating and it's an
artefact of how the deck was scaled up. Every real SRS caps new cards per day (Anki defaults to 20).

**Shape:** `state.newPerDay` (default ~20) plus `state.dayKey` / `state.newToday` so the count
resets at local midnight. `buildQueue()` already separates `due` from `fresh` and caps the refill
at `NEW_BATCH = 40` — that's the hook. Then show "20 new + 45 reviews left today" and a real done
screen when the day's goal is met, instead of only when the entire deck is exhausted.

## 3. Mastered shouldn't be permanent

**Note:** graduation is **per-direction** — a direction retires after 5 correct in a row (a miss
resets it), and the 20-item rotation is made of directions. The resurface-at-60/180-days idea below
still applies: retired directions leave for good until you return them by hand from the Got it pile.

**Why:** five in a row retires a direction forever (`MASTER_AT = 5`, then it leaves the queue). But
you will forget 商店 in six months and the app can never find out. This was an explicit request, so
it's a change to discuss rather than assume.

**Shape:** keep the Got it pile, but let retired directions resurface once at ~60 days and again at
~180. Surviving that is real mastery. `INTERVALS` currently stops at 16 days.

## 4. Edit / delete cards

**Why:** the oldest known gap. A typo in a card you added is unfixable except via Reset progress.
Duplicate detection is by hanzi only, so a card with a wrong definition can't be corrected by
re-pasting — the import skips it as a duplicate.

**Shape:** a browse/search panel listing cards with inline edit + delete. Overlaps with item 6.

## 5. Phone support (installable PWA)

**Why:** flashcards are a bus-stop activity, and this is already a single self-contained file.

**Shape:** a web app manifest + a small service worker caching `index.html`, so it installs and
runs offline on Android/iOS. Layout is already responsive; re-check tone-palette tap targets and
the audio controls at phone widths.

---

## Smaller things

- **Leech handling.** A card failed twenty times just keeps returning. Flag directions with a high
  lapse count and suspend or surface them.
- **Search the deck.** No way to look up a word you half-remember. 10k+ cards and no browse.
- **A Greetings category.** The 44 curated essentials — 你好 included — all landed in **Misc**,
  because "hello" matches no topic lexicon. See `tools/build_categories.py`.
- **Numbers category has strays.** The dataset's part-of-speech tags mark 来, 把, 头, 负 as
  numerals (they appear in constructions like 十来个). 多少 is tagged Pronoun, not Number. Small
  enough to hand-fix.
- **Storage headroom.** Baseline is ~1.2 MB of a ~5 MB quota; heavy study grows `prog`. `save()`
  already catches quota errors and warns, but the deck could be stored separately from progress so
  only progress is persisted.
- **Clarify the listening chip labels.** "🎧 Listen → English" reads as "listen to English" to new
  eyes; it means hear the Chinese, recall the English. "🎧 Hear 汉字 → English" is unambiguous.
- ~~**Phrase pinyin nits.** `pypinyin` misses some 不/一 tone sandhi inside Tatoeba phrases.~~
  **Done.** `tools/fix_sandhi.py` now applies 一/不 sandhi across the whole deck (140 不 + 253 一),
  keeping citation tone for ordinals/dates/counting. Third-tone sandhi (你好 → ní hǎo) is still not
  written, matching standard pinyin convention.
