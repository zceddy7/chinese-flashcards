# Build the phrase deck from Tatoeba cmn<->eng sentence pairs.
# Output: phrases.json -> [[hanzi, pinyin, english, score], ...] easiest first.
import json, re, sys
from collections import defaultdict
import zhconv, jieba
from pypinyin import pinyin, Style, load_phrases_dict

# --- frequency + vocabulary from the HSK dataset -------------------------
hsk = json.load(open('hsk.json', encoding='utf-8'))
FREQ = {}
for e in hsk:
    q = e.get('q')
    if q and (e['s'] not in FREQ or q < FREQ[e['s']]):
        FREQ[e['s']] = q
VOCAB = set(FREQ)
HAN_CHARS = set(''.join(VOCAB))

# Teach pypinyin the dictionary readings the word deck uses, so a word reads the
# same on a phrase card as on its own card (朋友 -> "péng you", not "péng yǒu").
words = json.load(open('words.json', encoding='utf-8'))
custom, injected = {}, 0
for hanzi, py, _eng, _q in words:
    sylls = py.split()
    # Only injectable when syllables line up 1:1 with characters.
    if len(hanzi) > 1 and len(sylls) == len(hanzi) and all('一' <= c <= '鿿' for c in hanzi):
        custom[hanzi] = [[s] for s in sylls]
        injected += 1
if custom:
    load_phrases_dict(custom)
print(f'injected {injected} dictionary readings into pypinyin', file=sys.stderr)

# --- load sentences ------------------------------------------------------
def load_tsv(path):
    out = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 3:
                out[p[0]] = p[2]
    return out

cmn = load_tsv('cmn_sentences.tsv')
eng = load_tsv('eng_sentences.tsv')
links = defaultdict(list)
with open('cmn-eng_links.tsv', encoding='utf-8') as f:
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) == 2:
            links[p[0]].append(p[1])
print(f'loaded cmn={len(cmn)} eng={len(eng)} links={len(links)}', file=sys.stderr)

# --- filters -------------------------------------------------------------
HAN_RE = re.compile(r'[一-鿿]')
ZH_PUNCT = '，。？！、；：""''（）《》…—·~ '
ALLOWED_RE = re.compile(r'^[一-鿿' + re.escape(ZH_PUNCT) + r']+$')
# Tatoeba leans hard on a few placeholder names; they crowd out useful phrases.
NAMES = ['汤姆', '汤米', '玛丽', '玛丽亚', '约翰', '杰克', '露西', '南希', '鲍勃', '肯', '迈克']
NAME_RE = re.compile('|'.join(NAMES))
ENG_OK_RE = re.compile(r"^[A-Za-z0-9 ,.\-'!?\"();:$%&/]+$")

def han_len(s):
    return len(HAN_RE.findall(s))

rows = {}
for cid, ztext in cmn.items():
    eids = links.get(cid)
    if not eids:
        continue
    z = zhconv.convert(ztext.strip(), 'zh-cn')      # unify traditional -> simplified
    if not ALLOWED_RE.match(z) or NAME_RE.search(z):
        continue
    n = han_len(z)
    if n < 3 or n > 14:                              # short enough to actually learn
        continue
    # Every token must be known vocabulary, so phrases stay learnable.
    toks = [t for t in jieba.cut(z) if HAN_RE.search(t)]
    if not toks or any(t not in VOCAB and not set(t) <= HAN_CHARS for t in toks):
        continue
    # Rank by the rarest word in the sentence: all-common words sort first.
    ranks = [FREQ.get(t) or max((FREQ.get(c, 99999) for c in t), default=99999) for t in toks]
    score = max(ranks)

    cands = [eng[e].strip() for e in eids if e in eng]
    cands = [c for c in cands if ENG_OK_RE.match(c) and 3 <= len(c) <= 60]
    if not cands:
        continue
    english = min(cands, key=len)                    # the plainest translation

    prev = rows.get(z)
    if prev is None or score < prev[3]:
        rows[z] = [z, None, english, score]

items = sorted(rows.values(), key=lambda r: (r[3], han_len(r[0])))
print(f'candidate phrases: {len(items)}', file=sys.stderr)

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 2500
items = items[:LIMIT]

# --- pinyin --------------------------------------------------------------
PUNCT_MAP = {'，': ',', '。': '.', '？': '?', '！': '!', '、': ',', '；': ';', '：': ':'}
def to_pinyin(s):
    parts = [p[0] for p in pinyin(s, style=Style.TONE)]
    out = []
    for p in parts:
        p = PUNCT_MAP.get(p, p)
        if p in ',.?!;:':
            if out:
                out[-1] = out[-1] + p                # attach, don't float
        elif HAN_RE.search(p) or p.strip() == '':
            continue
        else:
            out.append(p)
    return ' '.join(out).strip()

for r in items:
    r[1] = to_pinyin(r[0])

items = [r for r in items if r[1]]
json.dump(items, open('phrases.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f'phrases written: {len(items)}')
print('\n--- 25 easiest ---')
for r in items[:25]:
    print(f'  {r[0]:<16} {r[1]:<28} {r[2]}')
