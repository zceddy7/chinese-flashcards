# Build the word deck from the HSK vocabulary dataset.
# Output: words.json  -> [[hanzi, pinyin, english, freqRank], ...] sorted by frequency.
import json, re, sys

d = json.load(open('hsk.json', encoding='utf-8'))

CORE = {'n1','n2','n3','n4','n5','n6','o1','o2','o3','o4','o5','o6'}

# Meanings that describe the entry rather than translate it.
JUNK_RE = re.compile(
    r'^(old |unofficial |erroneous )?variant of |^used in |^see |^abbr\. for |^surname |'
    r'^\(old\)|^same as |^equivalent to ', re.I)

def is_proper(form):
    # A capitalised pinyin syllable marks a name/place, not the everyday reading.
    return form['i']['y'][:1].isupper()

def usable_meanings(form):
    return [m for m in form['m'] if not JUNK_RE.search(m)]

def score_form(form):
    """form[0] is often a surname or rare reading (说->shuì, 都->Dū), so rank
    forms by how much real meaning they carry and demote proper nouns."""
    ms = usable_meanings(form)
    if not ms:
        return -100
    s = len(ms) * 10
    if is_proper(form):
        s -= 60
    return s

def pick_form(entry):
    best = max(entry['f'], key=score_form)
    return best if score_form(best) > -100 else None

# Trim a CC-CEDICT style gloss down to something that fits on a flashcard.
NOISE_RE = re.compile(r'^(also|Taiwan|old|Cantonese|Mainland) pr\.', re.I)
# Leading tags that add nothing on a flashcard. "(classifier ...)" is NOT here:
# for words like 个 that IS the meaning.
TAG_RE = re.compile(
    r'^\((bound form|literary|coll\.|colloquial|dialect|old|archaic|slang|fig\.|'
    r'pronoun|adverb|adjective|adj\.|verb|noun|conjunction|preposition|interjection)\)\s*', re.I)
# A parenthetical that leans on Chinese to explain itself, e.g. "(as opposed to 您)".
HAN_PAREN_RE = re.compile(r'\([^)]*[一-鿿][^)]*\)')

def clean_meaning(ms):
    out = []
    for m in ms:
        m = m.strip()
        if NOISE_RE.search(m):
            continue
        # Glosses that are entirely parenthetical ARE the definition — unwrap
        # rather than delete, or 了 "(completed action marker)" vanishes.
        whole = re.match(r'^\((.+)\)$', m)
        if whole and '(' not in whole.group(1):
            m = whole.group(1)
        m = TAG_RE.sub('', m)
        m = HAN_PAREN_RE.sub('', m)
        m = re.sub(r'\s+', ' ', m).strip(' ;,')
        if not m or re.search(r'[一-鿿]', m):
            continue
        if m.lower() in (o.lower() for o in out):
            continue
        out.append(m)
        if len(out) == 3:
            break
    if not out:
        return ''
    # Cut at a gloss boundary rather than mid-word.
    parts = []
    for o in out:
        if len('; '.join(parts + [o])) > 72:
            break
        parts.append(o)
    return ('; '.join(parts) if parts else out[0][:72]).rstrip(' ;,')

rows = []
skipped = 0
for e in d:
    if not (set(e['l']) & CORE):
        continue
    q = e.get('q')
    if not q:
        continue
    form = pick_form(e)
    if not form:
        skipped += 1
        continue
    eng = clean_meaning(usable_meanings(form))
    if not eng:
        skipped += 1
        continue
    py = re.sub(r'\s+', ' ', form['i']['y']).strip()
    rows.append([e['s'], py, eng, q])

rows.sort(key=lambda r: r[3])
# Dedupe on the characters, keeping the most frequent entry.
seen, final = set(), []
for r in rows:
    if r[0] in seen:
        continue
    seen.add(r[0])
    final.append(r)

json.dump(final, open('words.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f'words: {len(final)}  (skipped {skipped} with no usable gloss)')
print('\n--- top 25 by frequency ---')
for r in final[:25]:
    print(f'  {r[0]:<6} {r[1]:<14} {r[2]}')
print('\n--- spot-check known polyphones ---')
idx = {r[0]: r for r in final}
for w in ['说','个','和','都','还','了','的','是','长','行','银行','中国','觉得']:
    r = idx.get(w)
    print(f'  {w:<4} -> {r[1]:<12} {r[2][:46]}' if r else f'  {w} MISSING')
