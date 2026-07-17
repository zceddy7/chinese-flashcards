# Tag every card with categories. Word types come from the dataset's own
# part-of-speech field; topics come from keyword lexicons over the English gloss.
# A card can carry several; anything untagged falls back to "misc".
# Output: cats.json {"order": [...ids...], "words": [...], "phrases": [...]}
import json, re, sys
from collections import Counter

words = json.load(open('words.json', encoding='utf-8'))
phrases = json.load(open('phrases.json', encoding='utf-8'))
supp = json.load(open('supplement.json', encoding='utf-8'))
hsk = json.load(open('hsk.json', encoding='utf-8'))

# --- bit order (must stay under 31 for JS bitwise ops) --------------------
TOPICS = ["food","travel","people","time","work","body","home","nature",
          "money","feel","animal","cloth","color","sport","tech","lang"]
TYPES  = ["verb","noun","adj","adv","pron","num","measure","conj","prep","particle","idiom"]
ORDER  = TOPICS + TYPES + ["misc"]
BIT = {c: 1 << i for i, c in enumerate(ORDER)}
assert len(ORDER) <= 31, len(ORDER)

# --- part of speech -> word type -----------------------------------------
POS_MAP = {
    "v":"verb","vd":"verb","vg":"verb","vn":"verb",
    "n":"noun","ng":"noun","nz":"noun","nr":"noun","nt":"noun","nx":"noun","an":"noun",
    "a":"adj","ad":"adj","ag":"adj","b":"adj","z":"adj",
    "d":"adv","dg":"adv",
    "r":"pron","rg":"pron",
    "m":"num","mg":"num",
    "q":"measure",
    "c":"conj",
    "p":"prep",
    "u":"particle","y":"particle",
    "i":"idiom","l":"idiom",
}
POS_BY_WORD = {}
PLACE_WORDS = set()
for e in hsk:
    tags = set()
    for p in e.get("p", []):
        if p in POS_MAP:
            tags.add(POS_MAP[p])
        if p == "ns":
            PLACE_WORDS.add(e["s"])          # place names -> travel topic
    if tags:
        POS_BY_WORD[e["s"]] = tags

# --- topic lexicons ------------------------------------------------------
# Matched as whole words against the English gloss.
LEX = {
"food": """eat eating ate drink drinking food foods meal meals rice noodle noodles bread meat fish
 chicken pork beef lamb egg eggs fruit apple banana orange grape watermelon vegetable vegetables
 tea coffee wine beer milk juice sugar salt soup restaurant cook cooking taste tastes tasty hungry
 thirsty delicious breakfast lunch dinner supper dish dishes bowl cup chopsticks menu snack cake
 candy chocolate spicy sour sweet bitter salty fry fried boil boiled bake baked steam dumpling tofu
 sauce oil flour cheese butter banquet appetite feast dine cuisine kitchen recipe pepper vinegar
 garlic onion potato tomato peanut melon pear cherry drinkable edible""",
"travel": """travel travels trip trips journey tour tourist train bus taxi car bicycle bike subway
 metro plane airplane aircraft flight airport station ticket tickets hotel hostel road roads street
 streets highway map luggage baggage suitcase passport visa customs drive driving ride riding fly
 flying sail abroad overseas foreign country countries city cities town village province county
 district capital address direction north south east west northeast northwest southeast southwest
 arrive arrival depart departure destination route path bridge port harbor harbour border embassy
 sightseeing vacation holiday tourism guide traveler traveller""",
"people": """person people man men woman women child children boy girl baby family father mother
 dad mom parent parents son daughter brother sister sibling grandfather grandmother grandpa grandma
 uncle aunt cousin nephew niece husband wife spouse marry married marriage friend friends friendship
 neighbor neighbour colleague classmate guest host stranger crowd public society community relative
 relatives adult teenager youth elderly gentleman lady couple""",
"time": """time times day days week weeks month months year years hour hours minute minutes second
 seconds morning noon afternoon evening night midnight today tomorrow yesterday now then later
 early earlier late soon already yet always never often sometimes usually seldom rarely again
 moment period century decade season spring summer autumn fall winter date calendar clock watch
 schedule anniversary birthday weekend weekday daily weekly monthly yearly annual past future
 present recent recently ago during while until since begin beginning end ending finish""",
"work": """work works working job jobs career profession occupation office company firm business
 factory boss manager employee employer staff worker colleague salary wage income career meeting
 conference project task duty responsibility interview resume hire employ employment unemployed
 retire retirement school schools student students teacher teachers class classroom lesson lessons
 study studies studying learn learning education university college degree exam examination test
 homework grade course subject library research science math mathematics history geography read
 reading write writing pen pencil book books notebook paper knowledge train training practice""",
"body": """body head hair face eye eyes ear ears nose mouth tooth teeth tongue lip neck shoulder arm
 arms hand hands finger leg legs foot feet knee back chest heart stomach blood bone skin brain
 health healthy sick sickness ill illness disease pain painful ache hurt injury wound doctor nurse
 hospital clinic medicine drug pill fever cough cold flu tired tiredness sleep sleepy rest exercise
 strong weak fat thin tall short height weight cure treat treatment operation patient symptom""",
"home": """home house houses apartment flat room rooms bedroom bathroom kitchen living door window
 wall floor ceiling roof stair furniture table chair sofa bed desk lamp light shelf cupboard closet
 drawer mirror curtain carpet blanket pillow towel soap brush key lock box bag bottle glass plate
 knife fork spoon pot pan bowl clean cleaning wash washing tidy garden yard garage rent landlord
 neighborhood address build building tool object thing things stuff""",
"nature": """nature natural weather rain rainy snow snowy wind windy cloud cloudy sun sunny sunshine
 moon star sky air temperature hot cold warm cool climate storm thunder lightning fog mountain hill
 river lake sea ocean beach island forest tree trees flower flowers grass leaf leaves plant plants
 stone rock sand soil earth world land field farm environment pollution water fire ice season
 spring summer autumn winter countryside landscape""",
"money": """money cash coin bill price cost costs expensive cheap buy buying bought sell selling sold
 shop shops shopping store market supermarket mall pay paying paid payment purchase spend spending
 save saving bank account credit debit card loan debt rich poor wealth wealthy income salary wage
 profit loss discount sale bargain free charge fee tax economy economic business trade customer
 change wallet purse yuan dollar euro pound currency exchange receipt refund order deliver""",
"feel": """feel feeling feelings emotion happy happiness glad joy joyful pleased delight sad sadness
 unhappy sorrow cry angry anger mad annoyed upset afraid fear fright scared nervous worry worried
 anxious calm relax relaxed excited exciting excitement bored boring surprise surprised shock love
 loving like dislike hate hatred enjoy enjoyment fun funny laugh smile proud pride shame ashamed
 shy jealous lonely lonely miss hope hopeful disappointed satisfied comfortable uncomfortable
 grateful thankful regret sorry mood temper""",
"animal": """animal animals cat cats dog dogs bird birds fish horse cow pig sheep goat chicken duck
 rabbit mouse rat tiger lion elephant monkey bear wolf fox snake insect bug bee butterfly ant
 spider fly mosquito pet zoo wing tail feather claw paw egg nest""",
"cloth": """clothes clothing clothe wear wearing wore dress dresses shirt tshirt trousers pants jeans
 skirt coat jacket sweater suit uniform shoe shoes boot sock hat cap scarf glove belt tie button
 pocket sleeve collar cotton silk wool leather fashion style size fit wardrobe underwear pyjamas
 jewelry ring necklace bracelet watch glasses umbrella bag handbag""",
"color": """color colour colored red blue green yellow black white gray grey brown pink purple orange
 golden gold silver bright dark light colorful""",
"sport": """sport sports game games play playing player ball football soccer basketball baseball
 tennis volleyball swim swimming run running jog race racing jump climb ski skate ride bicycle
 gym exercise fitness team match competition compete win winning won lose losing lost score goal
 champion medal olympic coach train training hobby leisure music song sing singing dance dancing
 movie film theater theatre concert art painting draw drawing photo photograph camera travel
 chess card party festival holiday celebrate""",
"tech": """computer laptop internet网 web website online offline email phone telephone mobile cellphone
 smartphone message text call app application software hardware program programming code data file
 folder screen keyboard mouse click download upload network wifi digital electronic electricity
 machine engine technology technical science scientific robot battery charge camera television tv
 radio video audio record player device system server database password account user""",
"lang": """language languages chinese english word words sentence grammar speak speaking spoke talk
 talking say saying said tell telling told ask asking question answer reply respond explain
 explanation mean meaning translate translation interpret dictionary read reading write writing
 letter character pronounce pronunciation accent dialect listen listening hear hearing understand
 conversation chat discuss discussion argue argument debate express expression communicate
 communication news report announce introduce describe""",
}
# Words whose everyday sense keeps firing on the wrong gloss:
#   "to bear hardships" -> animal, "on account of" -> money, "bright future" -> color.
# Dropping them costs a few true hits and removes many wrong ones.
BANNED = {
    "animal":  {"bear", "fly"},
    "color":   {"bright", "dark", "light"},
    "money":   {"account", "change", "save", "saving", "free", "charge", "order"},
    "feel":    {"miss"},
    "sport":   {"travel", "card", "train", "training", "play", "playing"},
    "work":    {"train", "training"},
    "tech":    {"account", "charge", "网", "record", "player"},
    "home":    {"thing", "things", "stuff", "object", "build", "building", "light", "glass"},
    "travel":  {"go", "walk"},
    "lang":    {"letter", "character"},
}

LEX_RE = {}
for cat, blob in LEX.items():
    terms = {t.strip().lower() for t in blob.split() if t.strip()}
    terms -= BANNED.get(cat, set())
    terms = sorted(terms, key=len, reverse=True)
    LEX_RE[cat] = re.compile(r'\b(' + '|'.join(re.escape(t) for t in terms) + r')\b', re.I)

# Parentheses hold usage notes, not the meaning — "to miss (train, opportunity
# etc)" is not about travel. Match against the gloss with them removed.
PAREN_RE = re.compile(r'\([^)]*\)')

def topics_for(text):
    text = PAREN_RE.sub(' ', text)
    out = set()
    for cat, rx in LEX_RE.items():
        if rx.search(text):
            out.add(cat)
    return out

def mask_for(cats):
    m = 0
    for c in cats:
        m |= BIT[c]
    return m

def tag_word(hanzi, english):
    cats = topics_for(english)
    cats |= POS_BY_WORD.get(hanzi, set())
    if hanzi in PLACE_WORDS:
        cats.add("travel")
    if not cats:
        cats = {"misc"}
    return cats

def tag_phrase(english):
    cats = topics_for(english)
    if not cats:
        cats = {"misc"}
    return cats

# --- apply ---------------------------------------------------------------
tally = Counter()
out_words = []
for h, p, e, q in words:
    cats = tag_word(h, e)
    tally.update(cats)
    out_words.append([h, p, e, q, mask_for(cats)])

out_phrases = []
for h, p, e, q in phrases:
    cats = tag_phrase(e)
    tally.update(cats)
    out_phrases.append([h, p, e, q, mask_for(cats)])

out_supp = []
for h, p, e, q, kind in supp:
    cats = tag_word(h, e) if kind == "w" else tag_phrase(e)
    tally.update(cats)
    out_supp.append([h, p, e, q, kind, mask_for(cats)])

json.dump({"order": ORDER, "words": out_words, "phrases": out_phrases, "supp": out_supp},
          open('cats.json', 'w', encoding='utf-8'), ensure_ascii=False)

total = len(out_words) + len(out_phrases) + len(out_supp)
print(f'tagged {total} cards\n')
print(f'{"category":<12}{"cards":>7}')
for c in ORDER:
    print(f'  {c:<10}{tally[c]:>7}')
print(f'\nmisc share: {tally["misc"]/total:.1%}')
