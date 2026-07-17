# Replace the STARTER deck in the app with the generated WORDS + PHRASES data.
import json, re, io

APP = r'C:\Users\Zacha\OneDrive\Desktop\Chinese Flashcards.html'
cats = json.load(open('cats.json', encoding='utf-8'))
words = cats['words']       # [hanzi, pinyin, english, freq, catMask]
phrases = cats['phrases']
supp = cats['supp']         # [hanzi, pinyin, english, rank, kind, catMask]
CAT_ORDER = cats['order']

# Essentials lead: rank 0..N sits ahead of every frequency rank, and HSK ranks
# start at 1, so shift those to keep the ordering unambiguous.
OFFSET = 100
words = [[h, p, e, q + OFFSET, c] for h, p, e, q, c in words]
phrases = [[h, p, e, q + OFFSET, c] for h, p, e, q, c in phrases]
for h, p, e, q, kind, c in supp:
    (words if kind == 'w' else phrases).append([h, p, e, q, c])
words.sort(key=lambda r: r[3])
phrases.sort(key=lambda r: r[3])

def js_rows(rows):
    out = io.StringIO()
    for r in rows:
        out.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
        out.write(',\n')
    return out.getvalue()

block = (
    '// ---- Built-in deck -------------------------------------------------\n'
    '// Words: HSK 1-6 vocabulary. Pinyin and definitions come from the\n'
    '// complete-hsk-vocabulary dataset (CC-BY-SA); "q" is a SUBTLEX-CH style\n'
    '// frequency rank, lower = more common, and drives the order new cards are\n'
    '// introduced in. Phrases: Tatoeba (CC-BY) sentence pairs limited to HSK\n'
    '// vocabulary, pinyin generated with pypinyin using the dictionary readings\n'
    '// above. The last field is a category bitmask over CAT_ORDER: word types\n'
    '// come from the dataset\'s part-of-speech tags, topics from keyword matching\n'
    '// on the English gloss, and "misc" covers whatever neither reached.\n'
    '// Each row: [hanzi, pinyin, english, frequencyRank, categoryMask]\n'
    f'const CAT_ORDER = {json.dumps(CAT_ORDER)};\n\n'
    f'const WORDS = [\n{js_rows(words)}];\n\n'
    f'const PHRASES = [\n{js_rows(phrases)}];\n'
)

src = open(APP, encoding='utf-8').read()
pat = re.compile(r'// ---- Starter deck.*?\n\];\n', re.S)
if not pat.search(src):
    raise SystemExit('STARTER block not found — aborting so nothing is clobbered')
out = pat.sub(lambda m: block, src, count=1)
open(APP, 'w', encoding='utf-8', newline='\n').write(out)
print(f'injected {len(words)} words + {len(phrases)} phrases')
print('file size: %.1f KB' % (len(out.encode('utf-8')) / 1024))
