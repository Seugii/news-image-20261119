#!/usr/bin/env python3
"""The World in One Page — 19 November 2026.

Renders a dense broadsheet front page summing up the world news of
Thursday, 19 November 2026 in a single 1024x1024 PNG. Pure Python +
Pillow, no network at runtime, fully deterministic: two runs write
identical bytes.

Usage: python3 main.py
Writes entry.png to $MAKEFUN_OUTPUT_DIR, else /output/entry.png when
that directory exists, else ./entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W, H = 1024, 1024
PAPER = (250, 246, 236)
NAVY = (22, 35, 63)
INK = (51, 51, 51)
GREY = (96, 96, 92)
MAGENTA = (157, 23, 77)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
GOLD = (180, 130, 29)
GREEN = (77, 124, 15)

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(BASE, "photos")

SERIF_B = os.path.join(BASE, "fonts", "LiberationSerif-Bold.ttf")
SERIF = os.path.join(BASE, "fonts", "LiberationSerif-Regular.ttf")
SERIF_I = os.path.join(BASE, "fonts", "LiberationSerif-Italic.ttf")
SANS_B = os.path.join(BASE, "fonts", "LiberationSans-Bold.ttf")
SANS = os.path.join(BASE, "fonts", "LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text utils

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    if not words:
        return []
    lines = []
    cur = words[0]
    for word in words[1:]:
        trial = cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading, max_lines=None):
    """Draw a wrapped paragraph; return the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def center(draw, cx, y, text, fnt, color):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=color)
    return y


# ---------------------------------------------------------------- image utils

def crop_fill(path, tw, th, focus_y=0.5):
    """Load an image and centre-crop it to the target aspect, then resize.

    focus_y (0..1) picks the vertical centre of the crop band.
    """
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    target = tw / th
    src = sw / sh
    if src > target:
        # too wide: crop width
        cw = int(sh * target)
        x0 = (sw - cw) // 2
        img = img.crop((x0, 0, x0 + cw, sh))
    else:
        # too tall: crop height around focus_y
        ch = int(sw / target)
        cy = int(sh * focus_y)
        y0 = max(0, min(sh - ch, cy - ch // 2))
        img = img.crop((0, y0, sw, y0 + ch))
    return img.resize((tw, th), Image.LANCZOS)


def place_photo(page, draw, photo, x, y, w, h, border=True):
    page.paste(photo, (x, y))
    if border:
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=(30, 30, 30), width=1)


# ---------------------------------------------------------------- illustrations

def draw_chart(d, x, y, w, h):
    """Flat bar chart with a rising red line (Anthropic IPO panel)."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(248, 248, 244),
                outline=(30, 30, 30), width=1)
    n = 7
    gap = 4
    bw = (w - 10 - gap * (n - 1)) // n
    base = y + h - 8
    heights = [10, 16, 22, 27, 33, 40, 48]
    pts = []
    for i, hh in enumerate(heights):
        bx = x + 5 + i * (bw + gap)
        top = base - hh
        d.rectangle([bx, top, bx + bw - 1, base], fill=(18, 122, 92))
        pts.append((bx + bw // 2, top - 2))
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=(200, 30, 30), width=2)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(200, 30, 30))
    d.text((x + 6, y + 3), "$81.3bn", font=font(SERIF_B, 15), fill=(22, 35, 63))


def draw_city(d, x, y, w, h):
    """Neon city at dusk (GTA VI panel): gradient sky, sun, towers."""
    top = (255, 122, 60)
    mid = (232, 72, 130)
    bot = (88, 44, 140)
    for yy in range(h):
        t = yy / max(1, h - 1)
        if t < 0.5:
            k = t / 0.5
            c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.5) / 0.5
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
        d.line([(x, y + yy), (x + w - 1, y + yy)], fill=c)
    # sun
    sx, sy, sr = x + w - 22, y + 14, 9
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 64))
    # towers
    towers = [(0, 30, 16, 58), (18, 22, 12, 58), (32, 34, 14, 58),
              (48, 18, 12, 58), (62, 28, 14, 58), (78, 24, 12, 58),
              (92, 36, 12, 58)]
    for tx, ty, twd, th in towers:
        d.rectangle([x + tx, y + ty, x + tx + twd - 1, y + th - 1],
                    fill=(24, 16, 40))
        # lit windows
        for wy in range(y + ty + 4, y + th - 3, 6):
            for wx in range(x + tx + 3, x + tx + twd - 2, 5):
                if (wx + wy) % 11 < 4:
                    d.point((wx, wy), fill=(255, 205, 90))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(30, 30, 30), width=1)


# ---------------------------------------------------------------- content

LEAD_BODY = (
    "The first-ever trilateral summit of the US, China and Russia lasted "
    "about 90 minutes at the APEC forum. No immediate breakthrough, but "
    "a joint declaration: reform the UN, produce more oil, open a "
    "dialogue on nuclear risk, and condemn the ICC."
)
LEAD_ITALIC = (
    "Trump met Putin for ~42 minutes and Xi for ~1 hour separately; "
    "New START expired in February."
)

PHOTO_STORIES = [
    {
        "kicker": "UKRAINE", "color": RED,
        "head": "Bridge hit a third time",
        "photo": ("bridge_collapse.jpg", 0.5),
        "caption": "Crimean Bridge after the 17 Nov strikes (SBU, CC BY 4.0)",
        "body": ("Traffic suspended again; rail halted too. The road arch "
                 "crumbled into the sea on Monday-Tuesday."),
    },
    {
        "kicker": "JUSTICE", "color": BLUE,
        "head": "Court: Myanmar committed genocide",
        "photo": ("peacepalace.jpg", 0.38),
        "caption": "The Peace Palace, The Hague (T. Wolf, CC BY-SA 3.0)",
        "body": ("ICJ rules 9-6 that Myanmar committed genocide against "
                 "the Rohingya in 2017; ~10,000 killed. First state ever "
                 "found responsible."),
    },
    {
        "kicker": "ECONOMY", "color": TEAL,
        "head": "Anthropic IPO: a record $81.3bn",
        "photo": None,
        "caption": "Illustration: the record share sale (no photo of the moment)",
        "body": ("Priced at $83 a share, it tops SpaceX's $75bn record. "
                 "Total deal $107.3bn; shares debut on Nasdaq as ANT, "
                 "valued ~$1.5tn."),
    },
    {
        "kicker": "CULTURE", "color": GOLD,
        "head": "Van Gogh sells for $190.4m",
        "photo": ("vangogh.jpg", 0.5),
        "caption": "\u2018Ch\u00e2taigniers en fleurs\u2019 (1890), public domain",
        "body": ("A record for the artist at Sotheby's New York; buyer is "
                 "dealer Bill Acquavella. Previous record: $117.2m in 2022."),
    },
]

BRIEFS = [
    [  # column 1
        ("APEC: Xi urges open trade",
         "China pushes a free-trade roadmap at Shenzhen."),
        ("Coalition of the Willing in Berlin",
         "Allies meet as Abu Dhabi talks end with no deal."),
        ("India-Japan 2+2 in Tokyo",
         "Foreign and defence ministers hold a first 2+2."),
        ("Wales meet Modi in Delhi",
         "The Prince and Princess of Wales meet India's PM."),
        ("Russia hits Ukraine's power grid",
         "Strikes target energy sites as winter closes in."),
        ("EU proposes a \u20ac45bn loan to Kyiv",
         "Brussels tables a big new loan for Ukraine."),
        ("US-Venezuela military pact",
         "Washington and Caracas sign a cooperation deal."),
        ("IAEA: N. Korea enrichment",
         "Inspectors say Pyongyang grew uranium work."),
        ("Trump: Iran eyes chem, bio arms",
         "US says Tehran explores chemical, biological arms."),
        ("Xi, Putin decry protectionism",
         "The two leaders hit out at sanctions at APEC."),
    ],
    [  # column 2
        ("Saudi coalition hits 60 Houthi sites",
         "Strikes across Yemen target Houthi positions."),
        ("Israel delays E1 settlement",
         "E1 paused; a settler kills a woman near Jericho."),
        ("Gaza: UN warns of cold deaths",
         "About 1.7m displaced; strikes go on."),
        ("COP31: ministers try to unblock talks",
         "Antalya stalls on 1.5C and north-south splits."),
        ("Cyclone Akvan nears India's coast",
         "Landfall expected ~20 Nov near Andhra, Odisha."),
        ("Bangladesh: Yunus home set on fire",
         "Violence hits 28 districts in fresh turmoil."),
        ("NASA launches CRS-25 to the ISS",
         "A Northrop Grumman cargo craft lifts off."),
        ("Jeffries picked as Speaker candidate",
         "House Democrats select Hakeem Jeffries."),
        ("US measles status lost",
         "America loses measles elimination status."),
        ("Myanmar rejects the ICJ finding",
         "The junta denies genocide; the ruling is binding."),
    ],
    [  # column 3
        ("Bilaterals: 42 min, then an hour",
         "Trump met Putin ~42 min and Xi ~1 hr alone."),
        ("The ICC, condemned by the three",
         "The declaration says the court must not abuse power."),
        ("New START is gone; talks to follow",
         "The last treaty lapsed; a risk dialogue opens."),
        ("ICJ: 9-6, reparations to be set",
         "Safe return and compensation ordered; sum later."),
        ("Anthropic: $107.3bn in all",
         "Total includes a $26bn private placement."),
        ("Van Gogh: 2nd at Sotheby's ever",
         "Only Klimt's $236.4m portrait cost more there."),
        ("Bridge: rail traffic also stopped",
         "Russia confirms trains are halted too."),
        ("GTA VI: 17m presale copies",
         "Players queued at midnight; firms gave a day off."),
        ("Hormuz stays shut",
         "The strait remains closed; tankers rerouted."),
        ("Kremlin: atmosphere was \u2018good\u2019",
         "Moscow says the trilateral went well."),
    ],
]


# ---------------------------------------------------------------- render

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W - 1, 84], fill=NAVY)
    center(d, W // 2, 8, "THE WORLD IN ONE PAGE", font(SERIF_B, 46),
           (255, 255, 255))
    center(d, W // 2, 62,
           "WORLD NEWS \u00b7 37 STORIES \u00b7 7 REGIONS \u00b7 "
           "SUMMED UP IN A SINGLE IMAGE",
           font(SANS, 13), (235, 235, 235))

    # ---- date
    center(d, W // 2, 90, "THURSDAY, 19 NOVEMBER 2026",
           font(SERIF_B, 22), NAVY)

    # ---- double rule under the date
    d.rectangle([24, 117, 1000, 119], fill=NAVY)
    d.rectangle([24, 122, 1000, 122], fill=NAVY)

    # ---- lead: kicker tag + headline
    d.rectangle([24, 128, 239, 151], fill=MAGENTA)
    center(d, 131, 134, "DIPLOMACY \u00b7 SHENZHEN", font(SANS_B, 13),
           (255, 255, 255))
    y = para(d, 24, 156,
             "Three at one table: Trump, Xi and Putin meet in Shenzhen",
             font(SERIF_B, 40), NAVY, 976, 44, max_lines=2)

    # ---- lead: body text (left) and photo (right)
    y = para(d, 24, 244, LEAD_BODY, font(SERIF, 14), INK, 480, 19)
    y = para(d, 24, y + 6, LEAD_ITALIC, font(SERIF_I, 14), INK, 480, 19)
    lead = crop_fill(os.path.join(PHOTOS, "trilateral_01.jpg"), 476, 112,
                     focus_y=0.45)
    place_photo(img, d, lead, 522, 246, 476, 112)
    para(d, 522, 362,
         "Trump, Xi and Putin at the trilateral, Shenzhen, 19 Nov. "
         "(Kremlin, CC BY 4.0)",
         font(SERIF_I, 10), GREY, 476, 13, max_lines=1)

    # ---- double rule under the lead
    d.rectangle([24, 380, 1000, 382], fill=NAVY)
    d.rectangle([24, 385, 1000, 385], fill=NAVY)

    # ---- row 1: four photo stories
    col_x = [24, 271, 518, 765]
    col_w = 235
    for cx, story in zip(col_x, PHOTO_STORIES):
        d.text((cx, 393), story["kicker"], font=font(SANS_B, 13),
               fill=story["color"])
        para(d, cx, 411, story["head"], font(SERIF_B, 17), NAVY, col_w,
             19, max_lines=2)
        if story["photo"] is not None:
            name, fy = story["photo"]
            pic = crop_fill(os.path.join(PHOTOS, name), col_w, 66,
                            focus_y=fy)
            place_photo(img, d, pic, cx, 448, col_w, 66)
        else:
            draw_chart(d, cx, 446, col_w, 66)
        para(d, cx, 516, story["caption"], font(SERIF_I, 10), GREY,
             col_w, 12, max_lines=2)
        para(d, cx, 542, story["body"], font(SERIF, 12), INK, col_w, 15,
             max_lines=4)

    # ---- rule under row 1
    d.rectangle([24, 591, 1000, 592], fill=NAVY)

    # ---- row 2: Iran (photo) and GTA VI (illustration)
    carrier = crop_fill(os.path.join(PHOTOS, "lead_carrier.jpg"), 140, 58,
                        focus_y=0.5)
    place_photo(img, d, carrier, 24, 598, 140, 58)
    para(d, 24, 660, "US Navy, RIMPAC 2026 (public domain)",
         font(SERIF_I, 9), GREY, 150, 11, max_lines=1)
    d.text((180, 598), "MIDDLE EAST", font=font(SANS_B, 13), fill=MAGENTA)
    para(d, 180, 616, "Iran hits Gulf states after US strikes",
         font(SERIF_B, 17), NAVY, 360, 20, max_lines=1)
    para(d, 180, 638,
         "Tehran retaliates after the US hit Qeshm Island; the Strait of "
         "Hormuz stays shut and energy prices swing.",
         font(SERIF, 12), INK, 360, 15, max_lines=2)

    draw_city(d, 560, 598, 104, 58)
    para(d, 560, 660, "Illustration: Vice City at dusk (no Rockstar art)",
         font(SERIF_I, 9), GREY, 120, 11, max_lines=2)
    d.text((680, 598), "TECH \u00b7 GAMES", font=font(SANS_B, 13), fill=GREEN)
    para(d, 680, 616, "GTA VI is out \u2014 and it is a 99",
         font(SERIF_B, 17), NAVY, 320, 20, max_lines=1)
    para(d, 680, 638,
         "After 13 years, Grand Theft Auto VI launches on PS5 and Xbox. "
         "Presales hit $1.65bn; Metacritic 99, 2.3m watch on Twitch.",
         font(SERIF, 12), INK, 320, 15, max_lines=2)

    # ---- rule under row 2
    d.rectangle([24, 687, 1000, 688], fill=NAVY)

    # ---- the world in brief
    d.text((24, 695), "THE WORLD IN BRIEF", font=font(SERIF_B, 16), fill=NAVY)
    d.rectangle([24, 716, 1000, 716], fill=NAVY)
    brief_x = [24, 354, 684]
    brief_w = 306
    for bx, column in zip(brief_x, BRIEFS):
        by = 726
        for head, body in column:
            d.text((bx, by), head, font=font(SERIF_B, 12), fill=NAVY)
            d.text((bx, by + 14), body, font=font(SERIF, 11), fill=INK)
            by += 27

    # ---- footer
    d.rectangle([24, 1005, 1000, 1006], fill=NAVY)
    center(d, W // 2, 1012,
           "Sources: Reuters \u00b7 USA Today \u00b7 The Times \u00b7 AP \u00b7 "
           "Bloomberg \u00b7 UN News \u00b7 Sotheby's \u00b7 ICJ \u2014 "
           "19 November 2026",
           font(SERIF, 11), GREY)
    return img


def out_path():
    d = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if d and os.path.isdir(d):
        return os.path.join(d, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return "entry.png"


def main():
    img = render()
    img.save(out_path(), format="PNG")


if __name__ == "__main__":
    main()
