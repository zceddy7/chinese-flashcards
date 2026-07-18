# Bake the Lucide icons the UI uses into the app.
#
# Lucide (https://lucide.dev), ISC licence. Each icon is a small stroke-based SVG
# using stroke="currentColor", so it inherits the colour of whatever button it
# sits in. We inline them (offline, no font/CDN) as an ICONS map between the
# ICONS-START / ICONS-END markers. Idempotent; cached under _icon_cache.
#
# Add an icon: put its Lucide name in NAMES and re-run.
# Usage:  python build_icons.py
import os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")
CACHE = os.path.join(HERE, "_icon_cache")
BASE = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/"

# UI action -> Lucide icon name (what each replaces)
NAMES = {
    "trophy":     "trophy",       # Got it pile
    "settings":   "settings",     # Study settings
    "plus":       "plus",         # Add cards
    "skip":       "skip-forward", # Skip
    "shuffle":    "shuffle",      # Reshuffle word
    "refresh":    "refresh-cw",   # New set
    "volume":     "volume-2",     # play audio
    "turtle":     "turtle",       # slow playback
    "snail":      "snail",        # slower playback
    "headphones": "headphones",   # listening prompt
    "image":      "image",        # picture prompt
    "lightbulb":  "lightbulb",    # hint
    "sparkles":   "sparkles",     # AI review
    "check":      "check",        # generic confirm
    "undo":       "undo-2",       # return to study
}


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name + ".svg")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    data = urllib.request.urlopen(BASE + name + ".svg", timeout=30).read().decode("utf-8")
    open(path, "w", encoding="utf-8").write(data)
    return data


def clean(svg):
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\s+", " ", svg).strip()
    svg = svg.replace("> <", "><")
    return svg


def main():
    icons = {}
    for key, lucide in NAMES.items():
        icons[key] = clean(fetch(lucide))

    body = ",\n".join(
        '"%s":%s' % (k, __import__("json").dumps(v, ensure_ascii=False))
        for k, v in icons.items()
    )
    block = (
        "/* ICONS-START — Lucide (https://lucide.dev), ISC licence. Inline SVGs,\n"
        "   stroke=currentColor so they take the button's colour. tools/build_icons.py. */\n"
        "const ICONS = {\n" + body + "\n};\n"
        "/* ICONS-END */"
    )

    src = open(APP, encoding="utf-8").read()
    marker = re.compile(r"/\* ICONS-START.*?/\* ICONS-END \*/", re.S)
    if marker.search(src):
        out = marker.sub(lambda m: block, src, count=1)
    else:
        anchor = re.compile(r"(/\* IMAGES-END \*/\n)")
        m = anchor.search(src)
        if not m:
            raise SystemExit("IMAGES-END marker not found — can't place ICONS")
        out = src[: m.end()] + "\n" + block + "\n" + src[m.end():]

    open(APP, "w", encoding="utf-8", newline="\n").write(out)
    kb = sum(len(v.encode("utf-8")) for v in icons.values()) / 1024
    sys.stdout.buffer.write(
        ("embedded %d Lucide icons (~%.1f KB)\n" % (len(icons), kb)).encode("utf-8"))


if __name__ == "__main__":
    main()
