# Apply 一 / 不 tone sandhi to the pinyin baked into index.html.
#
# The dictionary readings use citation tone (一 = yī, 不 = bù); in speech these
# change tone with what follows. This rewrites the embedded pinyin to the spoken
# sandhi, which is what a pronunciation app should show.
#
# Rules
#   不  -> bú   before a 4th-tone syllable; else stays bù.
#           (skipped in A不A reduplication, where 不 is neutral: 是不是.)
#   一  -> yí   before a 4th-tone syllable
#          yì   before a 1st/2nd/3rd-tone syllable
#          yī   kept when counting/ordinal: final position, after 第, after a
#               digit char, before 月/号/日 (dates); neutralised in A一A (想一想).
#
# Rows whose hanzi and pinyin don't line up 1:1 (erhua merges, odd entries) are
# left untouched and reported, so nothing is corrupted silently.
#
# Usage:
#   python fix_sandhi.py            # preview only, writes _sandhi_preview.txt
#   python fix_sandhi.py --apply    # rewrite ../index.html in place
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")

TONES = {1: "āēīōūǖ", 2: "áéíóúǘ", 3: "ǎěǐǒǔǚ", 4: "àèìòùǜ"}
DIGITS = set("零二三四五六七八九十百千万亿两")   # 一's neighbours that keep it yī
DATE_AFTER = set("月号日")
ORDINAL_BEFORE = set("第")
# following chars where a changed 一 is *plausibly* an unmarked ordinal — flagged
# for human review, not skipped.
REVIEW_AFTER = set("楼班组队号届期版课页章层路年级中所")


def is_cjk(ch):
    return "一" <= ch <= "鿿" or "㐀" <= ch <= "䶿"


def tone_of(syl):
    for t, chars in TONES.items():
        if any(c in syl for c in chars):
            return t
    return 0  # neutral / toneless


def align(hanzi, pinyin):
    """Return per-hanzi-char syllable indices, the syllable list, and whether it
    lined up cleanly (every syllable consumed by a Chinese char)."""
    syls = pinyin.split()
    mapping = []   # (char, syllable_index or None)
    si = 0
    for ch in hanzi:
        if is_cjk(ch):
            mapping.append((ch, si if si < len(syls) else None))
            if si < len(syls):
                si += 1
        else:
            mapping.append((ch, None))
    return mapping, syls, (si == len(syls))


def retone(syl, tone):
    """Re-mark a bare 'yi'/'bu' style syllable to the given tone (1-4)."""
    base = syl  # 'yī' -> we build from the vowel; simplest: map known cases
    # strip any existing tone mark on the vowel
    plain = syl
    for chars in TONES.values():
        for c in chars:
            plain = plain.replace(c, {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
                                       "ē": "e", "é": "e", "ě": "e", "è": "e",
                                       "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
                                       "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
                                       "ū": "u", "ú": "u", "ǔ": "u", "ù": "u",
                                       "ǖ": "v", "ǘ": "v", "ǚ": "v", "ǜ": "v"}[c])
    # plain is like 'yi' or 'bu'; put the tone on the single vowel
    vowel = "i" if "i" in plain else "u" if "u" in plain else None
    if vowel is None:
        return syl
    marks = {"i": "īíǐì", "u": "ūúǔù"}[vowel]
    return plain.replace(vowel, marks[tone - 1])


def fix_row(hanzi, pinyin):
    mapping, syls, ok = align(hanzi, pinyin)
    if not ok:
        return pinyin, [], True   # skipped
    new = syls[:]
    changes = []   # (char, old_syl, new_syl, flag)
    n = len(mapping)
    for k, (ch, si) in enumerate(mapping):
        if si is None:
            continue
        syl = syls[si]
        low = syl.lower()
        # next Chinese char + its syllable
        nxt_char, nxt_si = None, None
        for (c2, s2) in mapping[k + 1:]:
            if is_cjk(c2):
                nxt_char, nxt_si = c2, s2
                break
        prev_char = None
        for (c0, _s0) in reversed(mapping[:k]):
            if is_cjk(c0):
                prev_char = c0
                break
        nxt_tone = tone_of(syls[nxt_si]) if nxt_si is not None else None

        if ch == "不" and low == "bù":
            # A不A reduplication -> leave (neutral in speech)
            if prev_char and nxt_char and prev_char == nxt_char:
                continue
            if nxt_tone == 4:
                new[si] = retone("bu", 2)  # bú
                changes.append((ch, syl, new[si], ""))
        elif ch == "一" and low == "yī":
            if nxt_si is None:                        # final -> yī
                continue
            if prev_char in ORDINAL_BEFORE:           # 第一 -> yī
                continue
            if prev_char and prev_char in DIGITS:     # 十一 etc -> yī
                continue
            if nxt_char in DATE_AFTER:                # 一月/一号/一日 -> yī
                continue
            if nxt_char and is_cjk(nxt_char) and nxt_char in DIGITS:
                continue
            if prev_char and nxt_char and prev_char == nxt_char:   # 想一想 -> neutral
                new[si] = "yi"
                changes.append((ch, syl, new[si], "A一A"))
                continue
            if nxt_tone == 4:
                new[si] = retone("yi", 2)  # yí
            elif nxt_tone in (1, 2, 3):
                new[si] = retone("yi", 4)  # yì
            else:
                continue                              # neutral follower -> leave
            flag = "review?" if (nxt_char in REVIEW_AFTER) else ""
            changes.append((ch, syl, new[si], flag))
    return " ".join(new), changes, False


def grab(name, src):
    m = re.search(r"const " + name + r" = \[\n(.*?)\n\];", src, re.S)
    return m


def main():
    apply = "--apply" in sys.argv
    src = open(APP, encoding="utf-8").read()

    total = {"不": 0, "一": 0}
    skipped = 0
    samples = {"不": [], "一": [], "review": []}
    new_src = src

    for name in ("WORDS", "PHRASES"):
        m = grab(name, src)
        block = m.group(1)
        out_lines = []
        for line in block.splitlines():
            s = line.strip()
            if not (s.startswith("[") and s.endswith("],")):
                out_lines.append(line)
                continue
            try:
                row = json.loads(s[:-1])
            except Exception:
                out_lines.append(line)
                continue
            hanzi, pinyin = row[0], row[1]
            newp, changes, skip = fix_row(hanzi, pinyin)
            if skip:
                skipped += 1
            for (ch, old, nw, flag) in changes:
                total[ch] += 1
                bucket = "review" if flag == "review?" else ch
                if len(samples[bucket]) < 40:
                    samples[bucket].append((name, hanzi, pinyin, newp, f"{old}->{nw}", flag))
            if newp != pinyin:
                row[1] = newp
                line = json.dumps(row, ensure_ascii=False, separators=(",", ":")) + ","
            out_lines.append(line)
        new_block = "\n".join(out_lines)
        new_src = new_src.replace(m.group(1), new_block, 1)

    if apply:
        open(APP, "w", encoding="utf-8", newline="\n").write(new_src)
        msg = f"APPLIED. Rewrote pinyin: 不 x{total['不']}, 一 x{total['一']}. Skipped (misaligned): {skipped}.\n"
        sys.stdout.buffer.write(msg.encode("utf-8"))
        return

    # preview
    out = []
    out.append(f"PREVIEW ONLY — no files changed.\n")
    out.append(f"不 changes: {total['不']}    一 changes: {total['一']}    skipped (misaligned, left as-is): {skipped}\n")
    for title, key in [("不 -> bú examples", "不"), ("一 -> yí/yì examples", "一"),
                       ("一 changes to DOUBLE-CHECK (could be ordinals)", "review")]:
        out.append(f"\n=== {title} ===")
        for (name, h, oldp, newp, ch, flag) in samples[key]:
            out.append(f"[{name[:1]}] {h}\n      {oldp}\n   -> {newp}   ({ch})")
    open(os.path.join(HERE, "_sandhi_preview.txt"), "w", encoding="utf-8").write("\n".join(out))
    sys.stdout.buffer.write((f"wrote _sandhi_preview.txt  (不={total['不']}, 一={total['一']}, skipped={skipped})\n").encode("utf-8"))


if __name__ == "__main__":
    main()
