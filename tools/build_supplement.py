# HSK word lists omit everyday set expressions (你好 is 你 + 好 to them), so add
# them explicitly. Pinyin is generated, not hand-typed, using the same dictionary
# readings as the rest of the deck.
import json, re, sys
from pypinyin import pinyin, Style, load_phrases_dict

words = json.load(open('words.json', encoding='utf-8'))
phrases = json.load(open('phrases.json', encoding='utf-8'))

custom = {}
for hanzi, py, _e, _q in words:
    s = py.split()
    if len(hanzi) > 1 and len(s) == len(hanzi) and all('一' <= c <= '鿿' for c in hanzi):
        custom[hanzi] = [[x] for x in s]
load_phrases_dict(custom)

# (hanzi, english, kind)
ESSENTIALS = [
    ("你好", "hello", "w"),
    ("您好", "hello (polite)", "w"),
    ("你好吗", "how are you?", "p"),
    ("我很好", "I'm fine", "p"),
    ("早上好", "good morning", "p"),
    ("中午好", "good afternoon", "p"),
    ("晚上好", "good evening", "p"),
    ("拜拜", "bye-bye", "w"),
    ("好久不见", "long time no see", "p"),
    ("很高兴认识你", "nice to meet you", "p"),
    ("你叫什么名字", "what's your name?", "p"),
    ("我叫", "my name is", "p"),
    ("你是哪国人", "what country are you from?", "p"),
    ("我是美国人", "I'm American", "p"),
    ("我不明白", "I don't understand", "p"),
    ("我明白了", "I understand; got it", "p"),
    ("我听不懂", "I don't understand (spoken)", "p"),
    ("我看不懂", "I can't read it", "p"),
    ("请说慢一点", "please speak slower", "p"),
    ("请再说一遍", "please say it again", "p"),
    ("什么意思", "what does it mean?", "p"),
    ("怎么说", "how do you say it?", "p"),
    ("你会说英语吗", "do you speak English?", "p"),
    ("我会说一点中文", "I speak a little Chinese", "p"),
    ("多少钱", "how much does it cost?", "p"),
    ("太贵了", "too expensive", "p"),
    ("便宜一点", "a bit cheaper", "p"),
    ("我要这个", "I want this one", "p"),
    ("买单", "the bill, please", "w"),
    ("怎么走", "how do I get there?", "p"),
    ("在哪里", "where is it?", "p"),
    ("洗手间在哪里", "where is the bathroom?", "p"),
    ("请帮我", "please help me", "p"),
    ("救命", "help!", "w"),
    ("小心", "be careful", "w"),
    ("不好意思", "excuse me; sorry", "p"),
    ("麻烦你了", "sorry to trouble you", "p"),
    ("没事", "it's nothing; no worries", "p"),
    ("没问题", "no problem", "p"),
    ("真的吗", "really?", "p"),
    ("太好了", "great!", "p"),
    ("我爱你", "I love you", "p"),
    ("生日快乐", "happy birthday", "p"),
    ("新年快乐", "happy new year", "p"),
    ("身体健康", "good health", "p"),
    ("恭喜", "congratulations", "w"),
    ("中国菜", "Chinese food", "w"),
    ("好吃", "delicious", "w"),
    ("我饿了", "I'm hungry", "p"),
    ("我渴了", "I'm thirsty", "p"),
    ("我累了", "I'm tired", "p"),
    ("我不知道", "I don't know", "p"),
    ("我知道了", "I see; I know now", "p"),
    ("当然可以", "of course", "p"),
    ("给我看看", "let me have a look", "p"),
    ("等一会儿", "wait a moment", "p"),
    ("快点儿", "hurry up", "w"),
    ("加油", "come on; go for it", "w"),
]

def strip_punct(s):
    return re.sub(r'[，。？！、；：\s]', '', s)

have = {strip_punct(r[0]) for r in words} | {strip_punct(r[0]) for r in phrases}

# pypinyin misses 不/一 sandhi and some neutral tones in these set phrases.
# Small enough a list to check by hand; each correction is deliberate.
OVERRIDE = {
    "好久不见": "hǎo jiǔ bú jiàn",     # 不 -> bú before a 4th tone
    "请再说一遍": "qǐng zài shuō yí biàn",  # 一 -> yí before a 4th tone
    "等一会儿": "děng yí huìr",         # 一 sandhi + erhua
    "我不明白": "wǒ bù míng bai",       # 明白 is neutral on the 2nd syllable
    "多少钱": "duō shao qián",          # 多少 is neutral, as on its own card
    "早上好": "zǎo shang hǎo",          # 早上 neutral, to match 晚上好
}

def to_pinyin(s):
    if s in OVERRIDE:
        return OVERRIDE[s]
    return ' '.join(p[0] for p in pinyin(s, style=Style.TONE)).strip()

out, skipped = [], []
for i, (hz, en, kind) in enumerate(ESSENTIALS):
    key = strip_punct(hz)
    if key in have:
        skipped.append(hz)
        continue
    have.add(key)
    # Rank 0..N puts the essentials ahead of raw frequency: a learner needs
    # 你好 before the particle 的.
    out.append([hz, to_pinyin(hz), en, i, kind])

json.dump(out, open('supplement.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f'supplement: {len(out)} added, {len(skipped)} already covered ({" ".join(skipped)})')
print()
for r in out:
    print(f'  {r[0]:<8} {r[1]:<26} {r[2]}  [{r[4]}]')
