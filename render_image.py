#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261119 (compact v2).

A dense broadsheet front page summing up the world news of Thursday
19 November 2026: masthead, a full-width lead (Trump-Xi-Putin trilateral
in Shenzhen), four photo stories, a second row of two, and a three-column
briefs grid — 37 stories across 7 regions. Everything fits in 1024x1024.

PHOTOS ARE REAL, freely licensed, verified against their source pages:
  trilateral_01.jpg - Trump, Xi and Putin at the trilateral meeting,
                      Shenzhen, 19 Nov 2026 (President of Russia / Kremlin,
                      CC BY 4.0)
  bridge_collapse.jpg - Crimean Bridge after the 16-17 Nov 2026 strikes
                      (Security Service of Ukraine, CC BY 4.0)
  peacepalace.jpg   - The Peace Palace, The Hague (Thomas Wolf, CC BY-SA 3.0 de)
  vangogh.jpg       - Vincent van Gogh, "Chataigniers en fleurs" (1890),
                      public domain (artist died 1890)
  lead_carrier.jpg  - US Navy ships sail in formation, RIMPAC 2026
                      (US Navy photo, public domain)
Anthropic and GTA VI use flat PIL illustrations (no freely licensed photo
of the IPO moment or of GTA VI artwork exists that we may use).
Output: entry.png beside this file (1024x1024 PNG, <= 1 MiB).
No network, deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1024
MARGIN = 26

PAPER = (250, 246, 236)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
GRAY = (85, 85, 85)
LIGHT_RULE = (200, 192, 175)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
OLIVE = (77, 124, 15)
BURGUNDY = (157, 23, 77)
GOLD = (180, 130, 29)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")


def font(path, size):
    return ImageFont.truetype(path, size)


def italic(size):
    if os.path.exists(SERIF_ITALIC):
        return ImageFont.truetype(SERIF_ITALIC, size)
    return ImageFont.truetype(SANS_ITALIC, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, text, fnt, max_w, lh, fill):
    for ln in wrap(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def place_photo(img, path, x, y, w, h, centering=(0.5, 0.5)):
    im = Image.open(os.path.join(PHOTOS, path)).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=centering)
    img.paste(im, (x, y))
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)


def caption(d, x, y, text, max_w, size=9):
    fnt = font(SANS, size)
    return draw_text_block(d, x, y, text, fnt, max_w, size + 2, GRAY)


def kicker(d, x, y, text, color, size=13):
    fnt = font(SANS_BOLD, size)
    d.text((x, y), text, font=fnt, fill=color)
    return y + size + 3


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 245, 235))
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)
    vals = [18, 26, 22, 34, 30, 44, 40, 56, 52, 70, 66, 84]
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = h * v / 100.0
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h],
                    fill=TEAL)
    pts = [(x + i * bw + bw / 2, y + h - h * v / 100.0) for i, v in enumerate(vals)]
    d.line(pts, fill=RED, width=3)
    f = font(SANS_BOLD, 12)
    d.text((x + 6, y + 4), "$81.3bn", font=f, fill=NAVY)


def draw_neon_city(d, x, y, w, h):
    bands = [(255, 122, 89), (255, 94, 120), (168, 85, 247), (76, 29, 149)]
    bh = h / len(bands)
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    cx, cy, r = x + w - 30, y + 22, 14
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 64))
    import random
    rnd = random.Random(19)
    bx = x
    while bx < x + w - 12:
        bw = rnd.randint(14, 26)
        bhgt = rnd.randint(h // 3, int(h * 0.72))
        d.rectangle([bx, y + h - bhgt, bx + bw, y + h], fill=(30, 20, 60))
        for wy in range(y + h - bhgt + 5, y + h - 3, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 3],
                                fill=(255, 214, 64) if rnd.random() < 0.6 else (64, 224, 208))
        bx += bw + 3
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)


def brief(d, x, y, max_w, head, body, color=NAVY):
    """One brief: bold headline (1 line) + grey body (1 line). Returns y below."""
    f_h = font(SANS_BOLD, 12)
    y = draw_text_block(d, x, y, head, f_h, max_w, 14, color)
    f_b = font(SANS, 11)
    y = draw_text_block(d, x, y, body, f_b, max_w, 13, GRAY)
    return y + 2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-84) -----------------------------------------------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    f_mast = font(SERIF_BOLD, 48)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 10), t, font=f_mast,
           fill=(255, 255, 255))
    f_sub = font(SANS, 13)
    s = "WORLD NEWS  ·  37 STORIES  ·  7 REGIONS  ·  SUMMED UP IN A SINGLE IMAGE"
    d.text(((W - d.textlength(s, font=f_sub)) / 2, 64), s, font=f_sub,
           fill=(201, 210, 224))

    # ---- date strip (88-122) -------------------------------------------
    f_date = font(SANS_BOLD, 22)
    dt = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 90), dt, font=f_date,
           fill=NAVY)
    d.line([(0, 118), (W, 118)], fill=INK, width=3)
    d.line([(0, 122), (W, 122)], fill=INK, width=1)

    # ---- lead: trilateral (128-~318) -----------------------------------
    f_tag = font(SANS_BOLD, 15)
    tag = "DIPLOMACY  ·  SHENZHEN"
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([MARGIN, 130, MARGIN + tw + 20, 130 + 26], fill=BURGUNDY)
    d.text((MARGIN + 10, 134), tag, font=f_tag, fill=(255, 255, 255))

    f_head = font(SANS_BOLD, 34)
    head = "Three at one table: Trump, Xi and Putin meet in Shenzhen"
    y = 162
    for ln in wrap(d, head, f_head, W - 2 * MARGIN):
        d.text((MARGIN, y), ln, font=f_head, fill=NAVY)
        y += 40

    f_body = font(SANS, 15)
    body = ("The first-ever trilateral summit of the US, China and Russia "
            "lasted about 90 minutes at the APEC forum. No immediate "
            "breakthrough, but a joint declaration: reform the UN, produce "
            "more oil, open a dialogue on nuclear risk, and condemn the ICC.")
    yb = draw_text_block(d, MARGIN, 246, body, f_body, 470, 20, (51, 51, 51))
    quote = ("Trump met Putin for ~42 minutes and Xi for ~1 hour separately; "
             "New START expired in February.")
    yq = draw_text_block(d, MARGIN, yb + 8, quote, italic(14), 470, 18, INK)

    place_photo(img, "trilateral_01.jpg", 522, 246, 476, 112)
    cap_end = caption(d, 522, 362,
                      "Trump, Xi and Putin at the trilateral, Shenzhen, 19 Nov. (Kremlin, CC BY 4.0)",
                      476, size=9)

    lead_bottom = max(yq, cap_end)
    rule_y = lead_bottom + 8
    d.line([(0, rule_y), (W, rule_y)], fill=INK, width=3)
    d.line([(0, rule_y + 4), (W, rule_y + 4)], fill=INK, width=1)

    # ---- row 1: four photo stories (y0 ~ 340-520) ---------------------
    y0 = rule_y + 10
    col_w = 232
    gap = 12
    xs = [MARGIN + i * (col_w + gap) for i in range(4)]
    f_h = font(SANS_BOLD, 15)
    f_b = font(SANS, 11)

    x = xs[0]
    kicker(d, x, y0, "UKRAINE", RED, size=12)
    draw_text_block(d, x, y0 + 16, "Bridge hit a third time", f_h, col_w, 18, INK)
    place_photo(img, "bridge_collapse.jpg", x, y0 + 54, col_w, 68)
    c1 = caption(d, x, y0 + 126, "Crimean Bridge after the 17 Nov. strikes (SBU, CC BY 4.0)", col_w, size=9)
    b1 = draw_text_block(d, x, c1 + 2,
                         "Traffic suspended again; rail halted too. The road arch "
                         "crumbled into the sea on Monday-Tuesday.",
                         f_b, col_w, 14, GRAY)

    x = xs[1]
    kicker(d, x, y0, "JUSTICE", BLUE, size=12)
    draw_text_block(d, x, y0 + 16, "Court: Myanmar committed genocide", f_h, col_w, 18, INK)
    place_photo(img, "peacepalace.jpg", x, y0 + 54, col_w, 68)
    c2 = caption(d, x, y0 + 126, "The Peace Palace, The Hague (T. Wolf, CC BY-SA 3.0)", col_w, size=9)
    b2 = draw_text_block(d, x, c2 + 2,
                         "ICJ rules 9-6 that Myanmar committed genocide against the "
                         "Rohingya in 2017; ~10,000 killed. First state ever found "
                         "responsible.",
                         f_b, col_w, 14, GRAY)

    x = xs[2]
    kicker(d, x, y0, "ECONOMY", TEAL, size=12)
    draw_text_block(d, x, y0 + 16, "Anthropic IPO: a record $81.3bn", f_h, col_w, 18, INK)
    draw_chart(d, x, y0 + 54, col_w, 68)
    c3 = caption(d, x, y0 + 126, "Illustration: the record share sale (no photo of the moment)", col_w, size=9)
    b3 = draw_text_block(d, x, c3 + 2,
                         "Priced at $83 a share, it tops SpaceX's $75bn record. Total "
                         "deal $107.3bn; shares debut on Nasdaq as ANT, valued ~$1.5tn.",
                         f_b, col_w, 14, GRAY)

    x = xs[3]
    kicker(d, x, y0, "CULTURE", GOLD, size=12)
    draw_text_block(d, x, y0 + 16, "Van Gogh sells for $190.4m", f_h, col_w, 18, INK)
    place_photo(img, "vangogh.jpg", x, y0 + 54, col_w, 68, centering=(0.5, 0.35))
    c4 = caption(d, x, y0 + 126, "'Chataigniers en fleurs' (1890), public domain", col_w, size=9)
    b4 = draw_text_block(d, x, c4 + 2,
                         "A record for the artist at Sotheby's New York; buyer is "
                         "dealer Bill Acquavella. Previous record: $117.2m in 2022.",
                         f_b, col_w, 14, GRAY)

    row1_bottom = max(b1, b2, b3, b4)
    rule2_y = row1_bottom + 5
    d.line([(0, rule2_y), (W, rule2_y)], fill=INK, width=2)

    # ---- row 2: Iran (photo), GTA VI (illustration) --------------------
    y2 = rule2_y + 7
    place_photo(img, "lead_carrier.jpg", MARGIN, y2, 140, 58)
    ic = caption(d, MARGIN, y2 + 62, "US Navy, RIMPAC 2026 (public domain)", 140, size=9)
    kicker(d, 182, y2, "MIDDLE EAST", BURGUNDY, size=12)
    yy = draw_text_block(d, 182, y2 + 16, "Iran hits Gulf states after US strikes", f_h, 310, 18, INK)
    ib = draw_text_block(d, 182, yy + 2,
                         "Tehran retaliates after the US hit Qeshm Island; the Strait "
                         "of Hormuz stays shut and energy prices swing.",
                         f_b, 310, 14, GRAY)
    d.line([(508, y2), (508, max(ic, ib))], fill=LIGHT_RULE, width=1)

    draw_neon_city(d, 524, y2, 140, 58)
    gc = caption(d, 524, y2 + 62, "Illustration: Vice City at dusk (no Rockstar art)", 140, size=9)
    kicker(d, 680, y2, "TECH  ·  GAMES", OLIVE, size=12)
    yy = draw_text_block(d, 680, y2 + 16, "GTA VI is out — and it is a 99", f_h, 316, 18, INK)
    gb = draw_text_block(d, 680, yy + 2,
                         "After 13 years, Grand Theft Auto VI launches on PS5 and Xbox. "
                         "Presales hit $1.65bn; Metacritic 99, 2.3m watch on Twitch.",
                         f_b, 316, 14, GRAY)

    row2_bottom = max(ic, ib, gc, gb)
    rule3_y = row2_bottom + 5
    d.line([(0, rule3_y), (W, rule3_y)], fill=INK, width=2)

    # ---- briefs grid: 3 columns, 9 each -------------------------------
    y3 = rule3_y + 7
    f_sec = font(SANS_BOLD, 12)
    d.text((MARGIN, y3), "THE WORLD IN BRIEF", font=f_sec, fill=NAVY)
    d.line([(MARGIN + 140, y3 + 6), (W - MARGIN, y3 + 6)], fill=LIGHT_RULE, width=1)
    yb0 = y3 + 18

    col_x = [MARGIN, 358, 690]
    col_w2 = 306
    y = yb0
    y = brief(d, col_x[0], y, col_w2, "APEC: Xi urges open trade",
              "China pushes a free-trade roadmap at Shenzhen.")
    y = brief(d, col_x[0], y, col_w2, "Coalition of the Willing in Berlin",
              "Allies meet as Abu Dhabi talks end with no deal.")
    y = brief(d, col_x[0], y, col_w2, "India-Japan 2+2 in Tokyo",
              "Foreign and defence ministers hold a first 2+2.")
    y = brief(d, col_x[0], y, col_w2, "Wales meet Modi in Delhi",
              "The Prince and Princess of Wales meet India's PM.")
    y = brief(d, col_x[0], y, col_w2, "Russia hits Ukraine's power grid",
              "Strikes target energy sites as winter closes in.")
    y = brief(d, col_x[0], y, col_w2, "EU proposes a €45bn loan to Kyiv",
              "Brussels tables a big new loan for Ukraine.")
    y = brief(d, col_x[0], y, col_w2, "US-Venezuela military pact",
              "Washington and Caracas sign a cooperation deal.")
    y = brief(d, col_x[0], y, col_w2, "IAEA: N. Korea expands enrichment",
              "Inspectors say Pyongyang grew uranium work.")
    y = brief(d, col_x[0], y, col_w2, "Trump: Iran eyes chem, bio arms",
              "US says Tehran explores chemical, biological arms.")
    y = brief(d, col_x[0], y, col_w2, "Xi, Putin decry protectionism",
              "The two leaders hit out at sanctions at APEC.")
    col1_bottom = y

    y = yb0
    y = brief(d, col_x[1], y, col_w2, "Saudi coalition hits 60 Houthi sites",
              "Strikes across Yemen target Houthi positions.")
    y = brief(d, col_x[1], y, col_w2, "Israel delays E1 settlement",
              "E1 paused; a settler kills a woman near Jericho.")
    y = brief(d, col_x[1], y, col_w2, "Gaza: UN warns of cold deaths",
              "About 1.7m displaced; strikes go on.")
    y = brief(d, col_x[1], y, col_w2, "COP31: ministers try to unblock talks",
              "Antalya stalls on 1.5C and north-south splits.")
    y = brief(d, col_x[1], y, col_w2, "Cyclone Akvan nears India's coast",
              "Landfall expected ~20 Nov near Andhra, Odisha.")
    y = brief(d, col_x[1], y, col_w2, "Bangladesh: Yunus home set on fire",
              "Violence hits 28 districts in fresh turmoil.")
    y = brief(d, col_x[1], y, col_w2, "NASA launches CRS-25 to the ISS",
              "A Northrop Grumman cargo craft lifts off.")
    y = brief(d, col_x[1], y, col_w2, "Jeffries picked as Speaker candidate",
              "House Democrats select Hakeem Jeffries.")
    y = brief(d, col_x[1], y, col_w2, "US measles status lost",
              "America loses measles elimination status.")
    y = brief(d, col_x[1], y, col_w2, "Myanmar rejects the ICJ finding",
              "The junta denies genocide; the ruling is binding.")
    col2_bottom = y

    y = yb0
    y = brief(d, col_x[2], y, col_w2, "Bilaterals: 42 min, then an hour",
              "Trump met Putin ~42 min and Xi ~1 hr alone.")
    y = brief(d, col_x[2], y, col_w2, "The ICC, condemned by the three",
              "The declaration says the court must not abuse power.")
    y = brief(d, col_x[2], y, col_w2, "New START is gone; talks to follow",
              "The last arms treaty lapsed; a risk dialogue opens.")
    y = brief(d, col_x[2], y, col_w2, "ICJ: 9-6, reparations to be set",
              "Safe return and compensation ordered; sum later.")
    y = brief(d, col_x[2], y, col_w2, "Anthropic: $107.3bn in all",
              "Total includes a $26bn private placement.")
    y = brief(d, col_x[2], y, col_w2, "Van Gogh: 2nd at Sotheby's ever",
              "Only Klimt's $236.4m portrait cost more there.")
    y = brief(d, col_x[2], y, col_w2, "Bridge: rail traffic also stopped",
              "Russia confirms trains are halted too.")
    y = brief(d, col_x[2], y, col_w2, "GTA VI: 17m presale copies",
              "Players queued at midnight; firms gave a day off.")
    y = brief(d, col_x[2], y, col_w2, "Hormuz stays shut",
              "The strait remains closed; tankers rerouted.")
    y = brief(d, col_x[2], y, col_w2, "Kremlin: atmosphere was 'good'",
              "Moscow says the trilateral went well.")
    col3_bottom = y

    briefs_bottom = max(col1_bottom, col2_bottom, col3_bottom)

    # ---- footer --------------------------------------------------------
    ftr_y = briefs_bottom + 3
    d.line([(0, ftr_y), (W, ftr_y)], fill=INK, width=2)
    f_src = font(SANS, 11)
    src = ("Sources: Reuters  ·  USA Today  ·  The Times  ·  AP  ·  Bloomberg  ·  "
           "UN News  ·  Sotheby's  ·  ICJ  —  19 November 2026")
    d.text(((W - d.textlength(src, font=f_src)) / 2, ftr_y + 5), src,
           font=f_src, fill=GRAY)

    print("layout: briefs_bottom", briefs_bottom, "footer rule", ftr_y,
          "footer text ends", ftr_y + 5 + 11)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
