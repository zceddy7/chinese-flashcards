# Bake cartoon illustrations for concrete nouns into the app.
#
# Art: OpenMoji (https://openmoji.org), CC BY-SA 4.0 — colour SVGs, genuinely
# drawn vector cartoons (not the viewer's system emoji font), so every device
# shows the same picture and it stays sharp at any size. Only concrete,
# depictable nouns get one; abstract nouns (situation, economy, ...) don't.
#
# What it does: for each hanzi -> emoji-codepoint below that ALSO exists in the
# baked deck, download the OpenMoji SVG, strip its ids (many would collide when
# several are injected into the page over time), and write an IMAGES map into
# index.html between the IMAGES-START / IMAGES-END markers. Idempotent: re-runs
# replace the block. SVGs are cached under _img_cache so re-runs are offline.
#
# Usage:  python build_images.py
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")
CACHE = os.path.join(HERE, "_img_cache")
BASE = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/color/svg/"

# hanzi -> OpenMoji filename stem (Unicode codepoints, uppercase hex, '-' joined)
NOUN_EMOJI = {
    # people & body
    "人": "1F9D1", "手": "270B", "口": "1F444", "嘴": "1F444", "眼睛": "1F441",
    "眼": "1F441", "脚": "1F9B6", "腿": "1F9B5", "牙": "1F9B7", "骨": "1F9B4",
    "血": "1FA78", "心": "2764", "耳朵": "1F442", "鼻子": "1F443",
    # animals
    "狗": "1F415", "猫": "1F408", "马": "1F40E", "鱼": "1F41F", "牛": "1F404",
    "鸡": "1F414", "鸟": "1F426", "猪": "1F416", "羊": "1F411", "兔": "1F407",
    "老虎": "1F405", "大象": "1F418", "熊": "1F43B", "猴": "1F412", "鸭": "1F986",
    "蛇": "1F40D", "龙": "1F409", "虫": "1F41B", "兔子": "1F407", "老鼠": "1F401",
    # food & drink
    "苹果": "1F34E", "香蕉": "1F34C", "面包": "1F35E", "蛋": "1F95A",
    "茶": "1F375", "咖啡": "2615", "牛奶": "1F95B", "米": "1F33E", "饭": "1F35A",
    "肉": "1F356", "糖": "1F36C", "盐": "1F9C2", "蛋糕": "1F370", "菜": "1F96C",
    "酒": "1F377", "水": "1F4A7", "鸡蛋": "1F95A", "西瓜": "1F349", "橙子": "1F34A",
    # objects
    "书": "1F4D6", "药": "1F48A", "笔": "1F58A", "刀": "1F52A", "枪": "1F52B",
    "包": "1F45C", "卡": "1F4B3", "球": "26BD", "票": "1F3AB", "钱": "1F4B5",
    "美元": "1F4B5", "床": "1F6CF", "灯": "1F4A1", "钥匙": "1F511", "伞": "2602",
    "镜子": "1FA9E", "帽子": "1F9E2", "眼镜": "1F453", "手表": "231A", "表": "231A",
    "椅子": "1FA91", "窗户": "1FA9F", "石头": "1FAA8", "地图": "1F5FA",
    "信": "2709", "照片": "1F5BC", "相机": "1F4F7", "礼物": "1F381", "旗": "1F3F3",
    "钟": "23F0", "衣服": "1F455", "鞋": "1F45F", "手机": "1F4F1", "电脑": "1F4BB",
    "电视": "1F4FA", "电话": "260E", "钢琴": "1F3B9", "枕头": "1F6CF",
    # places & buildings
    "房子": "1F3E0", "房间": "1F3E0", "楼": "1F3E2", "医院": "1F3E5",
    "学校": "1F3EB", "银行": "1F3E6", "桥": "1F309", "车站": "1F689",
    "商店": "1F3EA", "教室": "1F3EB",
    # vehicles
    "车": "1F697", "汽车": "1F697", "飞机": "2708", "船": "1F6A2",
    "火车": "1F686", "自行车": "1F6B2", "公共汽车": "1F68C",
    # nature & weather
    "火": "1F525", "山": "26F0", "海": "1F30A", "树": "1F333", "花": "1F33C",
    "草": "1F33F", "叶子": "1F343", "月": "1F319", "星": "2B50", "太阳": "2600",
    "雪": "2744", "云": "2601", "雨": "1F327", "电": "26A1", "月亮": "1F319",
    "星星": "2B50", "水果": "1F34F",
}


def fetch(stem):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, stem + ".svg")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    url = BASE + stem + ".svg"
    data = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    open(path, "w", encoding="utf-8").write(data)
    return data


def clean(svg):
    # Trim the XML/comment noise, drop id attributes (they'd collide when several
    # illustrations pass through the same container), and collapse whitespace.
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r'\s+id="[^"]*"', "", svg)
    svg = re.sub(r">\s+<", "><", svg)
    return svg.strip()


def deck_hanzi(src):
    have = set()
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("],"):
            try:
                row = json.loads(s[:-1])
            except Exception:
                continue
            if len(row) == 5 and row[0]:
                have.add(row[0])
    return have


def main():
    src = open(APP, encoding="utf-8").read()
    have = deck_hanzi(src)

    images, missing_deck, missing_art = {}, [], []
    for hanzi, stem in NOUN_EMOJI.items():
        if hanzi not in have:
            missing_deck.append(hanzi)
            continue
        try:
            images[hanzi] = clean(fetch(stem))
        except Exception as e:
            missing_art.append(f"{hanzi} ({stem}): {e}")

    body = ",\n".join(
        json.dumps(h, ensure_ascii=False) + ":" + json.dumps(svg, ensure_ascii=False)
        for h, svg in images.items()
    )
    block = (
        "/* IMAGES-START — cartoon art for concrete nouns. OpenMoji, CC BY-SA 4.0.\n"
        "   Regenerate with tools/build_images.py. Keyed by hanzi; value is inline SVG. */\n"
        "const IMAGES = {\n" + body + "\n};\n"
        "/* IMAGES-END */"
    )

    marker = re.compile(r"/\* IMAGES-START.*?/\* IMAGES-END \*/", re.S)
    if marker.search(src):
        out = marker.sub(lambda m: block, src, count=1)
    else:
        # Insert right after the PHRASES array closes (end of the baked deck).
        anchor = re.compile(r"(const PHRASES = \[.*?\n\];\n)", re.S)
        m = anchor.search(src)
        if not m:
            raise SystemExit("PHRASES block not found — can't place IMAGES")
        out = src[: m.end()] + "\n" + block + "\n" + src[m.end():]

    open(APP, "w", encoding="utf-8", newline="\n").write(out)
    kb = sum(len(v.encode("utf-8")) for v in images.values()) / 1024
    def out_line(s):
        sys.stdout.buffer.write((s + "\n").encode("utf-8"))
    out_line(f"embedded {len(images)} illustrations (~{kb:.0f} KB of SVG)")
    if missing_deck:
        out_line("skipped (not in deck): " + " ".join(missing_deck))
    if missing_art:
        out_line("art fetch failed:\n  " + "\n  ".join(missing_art))


if __name__ == "__main__":
    main()
