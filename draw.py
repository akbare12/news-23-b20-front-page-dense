#!/usr/bin/env python3
"""Draw the news-image-20261123 front page: Monday 23 November 2026.

Dense front page: masthead + number strip + region bar + UTC strip +
3 hero scenes + 10 small cards + world map with numbered pins +
ALSO list + DATE CHECK. 31 stories, 6 regions.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
PAPER = (252, 250, 244)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (16, 42, 92)
BLUE = (24, 68, 140)
TEAL = (12, 110, 96)
GREEN = (26, 122, 58)
AMBER = (178, 120, 20)
ORANGE = (196, 88, 16)
PURPLE = (96, 48, 140)
GRAY = (90, 90, 90)
LIGHT = (226, 220, 205)
OCEAN = (207, 227, 238)
LAND = (232, 220, 192)
GRID = (190, 210, 222)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FDIR, name), size)
    except OSError:
        return ImageFont.truetype(os.path.join(FDIR, "DejaVuSans.ttf"), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 25)
F_KICK = font("DejaVuSans-Oblique.ttf", 15)
F_NUM = font("DejaVuSans-Bold.ttf", 26)
F_NUML = font("DejaVuSans.ttf", 11)
F_BAR = font("DejaVuSans-Bold.ttf", 13)
F_UTC = font("DejaVuSans.ttf", 12)
F_UTCB = font("DejaVuSans-Bold.ttf", 12)
F_HT = font("DejaVuSans-Bold.ttf", 21)
F_HK = font("DejaVuSans-Bold.ttf", 11)
F_HB = font("DejaVuSans.ttf", 13)
F_HS = font("DejaVuSans.ttf", 10)
F_CT = font("DejaVuSans-Bold.ttf", 14)
F_CK = font("DejaVuSans-Bold.ttf", 10)
F_CB = font("DejaVuSans.ttf", 11)
F_CS = font("DejaVuSans.ttf", 9)
F_SEC = font("DejaVuSans-Bold.ttf", 14)
F_AL = font("DejaVuSans.ttf", 12)
F_ALB = font("DejaVuSans-Bold.ttf", 12)
F_DC = font("DejaVuSans-Bold.ttf", 13)
F_DCB = font("DejaVuSans.ttf", 12)
F_FT = font("DejaVuSans.ttf", 10)
F_PIN = font("DejaVuSans-Bold.ttf", 10)


def wrap(d, text, f, maxw, max_lines=None):
    """Wrap text to maxw; optionally cap lines with ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " ...", font=f) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def text_lines(d, x, y, lines, f, fill, leading=None):
    if leading is None:
        leading = f.size + 3
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def chip(d, x, y, label, fill):
    w_ = d.textlength(label, font=F_CS) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=F_CS, fill=(255, 255, 255))
    return w_


CHIP_FILL = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE, "DENIAL": PURPLE}

# ---------------------------------------------------------------- data
NUMBERS = [
    ("-3.3%", "Kospi"),
    ("5.3", "US-China gap"),
    ("11,762", "Ebola cases"),
    ("10T won", "Seoul fund"),
    ("2%", "billionaire tax"),
    ("$450M", "Skubal deal"),
    ("165", "missiles / week"),
    ("$107.3B", "Anthropic IPO"),
]

REGIONS = [
    ("NORTH AMERICA 8", BLUE),
    ("EUROPE 6", (196, 88, 16)),
    ("MIDDLE EAST 6", PURPLE),
    ("AFRICA 3", TEAL),
    ("ASIA-PACIFIC 6", (24, 68, 140)),
    ("WORLD 2", (90, 90, 90)),
]

UTC = [
    ("~00:00", "ASIA OPENS"),
    ("06:30", "KOSPI -3.3%"),
    ("~09:00", "SEOUL FUND"),
    ("14:30", "WALL ST +3%"),
    ("~16:00", "GUTERRES"),
    ("~21:00", "FBI HACK"),
]

HEROES = [
    dict(num=1, kicker="SEOUL \u00b7 MARKETS", scene="kospi",
         title="AI ROUT HITS ASIA \u2014 KOSPI -3.3%",
         body="Kospi closes 4,708.54, sheds 161 pts; intraday -5.8%. "
              "Samsung -3.1%, SK Hynix -2.5%.",
         source="Yonhap \u00b7 Reuters", chip="REPORTED"),
    dict(num=2, kicker="BRIDGETOWN \u00b7 UNITED NATIONS", scene="guterres",
         title="GUTERRES: REGULATE AI BEFORE IT\u2019S TOO LATE",
         body="UN chief urges global AI safety rules at Bridgetown; "
              "150 back a risk framework.",
         source="UN News \u00b7 AP", chip="REPORTED"),
    dict(num=3, kicker="LOWY INSTITUTE \u00b7 ASIA POWER INDEX 2026", scene="power",
         title="US LEAD OVER CHINA AT RECORD LOW",
         body="US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. "
              "India third at 40.5.",
         source="Lowy Institute", chip="REPORTED"),
]

CARDS = [
    (4, "WASHINGTON \u00b7 TRADE", "Bessent demands Nvidia answers",
     "Treasury chief wants to know who approved China sales.",
     "Reuters", "REPORTED", BLUE),
    (5, "WASHINGTON \u00b7 CYBER", "FBI probes hack of police database",
     "Intruders hit the NCIC system used by police nationwide.",
     "AP", "REPORTED", BLUE),
    (6, "NEW YORK \u00b7 SPORT", "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner signs record nine-year, $450M deal.",
     "ESPN", "REPORTED", BLUE),
    (7, "SAN FRANCISCO \u00b7 MARKETS", "Anthropic IPO: $107.3B, largest ever",
     "Raised at $83/share on 19 Nov; debut close $97.17.",
     "Bloomberg", "REPORTED", BLUE),
    (8, "WARSAW \u00b7 WAR", "Poland: 3 missiles cross airspace",
     "Kyiv: 3 Kh-101s entered Poland Friday; Tusk: provocation.",
     "AP", "CLAIM", RED),
    (9, "PARIS \u00b7 TAX", "Paris: 100+ back 2% billionaire tax",
     "Economists and unions rally behind France's wealth tax.",
     "AFP", "REPORTED", TEAL),
    (10, "KYIV \u00b7 WAR", "Zelenskyy: 165 missiles in a week",
     "Moscow fired 165 missiles in seven days; US delays Patriots.",
     "Kyiv", "CLAIM", RED),
    (11, "ANTALYA \u00b7 CLIMATE", "COP31: the day after",
     "Sunday's collapse: 194 nations reject the Antalya pact.",
     "CNN", "REPORTED", TEAL),
    (12, "GAZA \u00b7 WAR", "Gaza: two killed in Israeli strike",
     "Two killed in southern Gaza as the ceasefire frays.",
     "AP", "REPORTED", RED),
    (13, "DRC \u00b7 HEALTH", "Ebola teams trapped by fighting",
     "Fighting traps Ebola teams in Ituri; WHO: 11,762 cases.",
     "WHO", "REPORTED", GREEN),
]

ALSO = [
    (14, "Trump: Iran strikes may resume"),
    (15, "US futures jump 3% at open"),
    (16, "Tom Jackson dies at 75"),
    (17, "10 States sue SpaceX on AI"),
    (18, "Intel: Russian nuke satellite"),
    (19, "Manchester: 12,000 cleared"),
    (20, "Benghazi: UN demands port probe"),
    (21, "Israel unity talks resume"),
    (22, "West Bank settler attacks"),
    (23, "Iran war: no deal in sight"),
    (24, "Lebanon seizes 264 kg explosives"),
    (25, "Bahrain: Iran strike hits plant"),
    (26, "Sudan downs drones in Khartoum"),
    (27, "Bangladesh: Hasina jailed"),
    (28, "Seoul minister quits in exam row"),
    (29, "SK Telecom -7.3% as hype cools"),
    (30, "China eases margin rules"),
    (31, "Seoul readies 10T-won fund"),
]

# lon, lat per story number (map pins)
PINS = {
    1: (128.0, 38.0), 2: (-59.6, 13.1), 3: (-150.0, -20.0),
    4: (-79.0, 37.0), 5: (-72.0, 42.5), 6: (-74.5, 39.5),
    7: (-122.4, 37.8), 8: (19.0, 52.0), 9: (2.3, 48.9),
    10: (30.5, 50.4), 11: (30.7, 36.9), 12: (33.8, 31.2),
    13: (29.8, 1.8), 14: (-82.0, 34.5), 15: (-70.0, 44.0),
    16: (-105.0, 39.7), 17: (-97.7, 30.3), 18: (37.6, 55.7),
    19: (-2.2, 53.5), 20: (20.1, 32.1), 21: (35.0, 31.5),
    22: (36.2, 32.6), 23: (51.4, 35.7), 24: (36.0, 34.2),
    25: (50.6, 26.2), 26: (32.5, 15.6), 27: (90.4, 23.8),
    28: (123.0, 40.5), 29: (131.0, 34.0), 30: (116.4, 39.9),
    31: (124.0, 34.5),
}
CLAIM_PINS = {8, 10, 18, 20}

# simplified continent polygons (lon, lat)
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-85, 76),
     (-80, 73), (-76, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 42),
     (-75, 35), (-80, 32), (-84, 30), (-90, 28), (-97, 26), (-105, 22),
     (-110, 25), (-117, 33), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-160, 58), (-168, 66)],
    # Greenland
    [(-45, 60), (-32, 68), (-22, 70), (-32, 76), (-50, 76), (-58, 70),
     (-55, 64), (-45, 60)],
    # South America
    [(-80, 10), (-77, 5), (-70, 0), (-60, -2), (-50, -5), (-40, -8),
     (-35, -12), (-38, -20), (-42, -25), (-50, -30), (-58, -35),
     (-65, -42), (-70, -50), (-72, -55), (-74, -48), (-73, -38),
     (-72, -28), (-75, -20), (-80, -12), (-81, -5), (-80, 10)],
    # Europe
    [(-10, 36), (-2, 44), (-4, 48), (0, 50), (4, 53), (8, 57), (12, 56),
     (18, 56), (21, 58), (24, 62), (28, 66), (32, 70), (40, 68),
     (38, 62), (32, 60), (28, 55), (24, 52), (20, 48), (16, 45),
     (12, 44), (8, 44), (3, 43), (-1, 38), (-9, 37), (-10, 36)],
    # Africa
    [(-10, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 20), (43, 12), (48, 11), (51, 6), (48, 0), (42, -5),
     (40, -12), (36, -20), (32, -28), (26, -34), (19, -35), (15, -30),
     (12, -18), (13, -10), (12, 0), (9, 4), (0, 5), (-8, 5),
     (-15, 10), (-17, 15), (-16, 22), (-13, 30), (-10, 35)],
    # Asia
    [(-168, 66), (-150, 66), (-140, 70), (-130, 72), (-110, 74),
     (-90, 75), (-70, 73), (-50, 70), (-30, 70), (30, 70), (40, 68),
     (50, 70), (60, 70), (70, 73), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 65),
     (162, 60), (158, 55), (150, 60), (142, 55), (140, 45), (135, 40),
     (130, 35), (127, 35), (122, 32), (120, 28), (115, 23), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15),
     (77, 8), (75, 12), (72, 20), (68, 25), (62, 25), (58, 26),
     (55, 28), (52, 28), (50, 30), (48, 32), (45, 30), (42, 32),
     (40, 36), (35, 36), (32, 42), (30, 48), (28, 55), (30, 60),
     (32, 66), (40, 68)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -35), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20), (113, -22)],
]


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (75.0 - lat) / 130.0 * h
    return x, y


def draw_scene_kospi(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(12, 22)
        bh = rnd.randint(18, 42)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(10, 26, 60))
        for wy in range(y + h - bh + 4, y + h - 4, 7):
            for wx in range(bx + 3, bx + bw - 3, 6):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 210, 90))
        bx += bw + 3
    # falling chart
    pts = [(x + 10, y + 16), (x + 55, y + 20), (x + 100, y + 18),
           (x + 145, y + 26), (x + 190, y + 34), (x + 235, y + 46),
           (x + 275, y + 58), (x + 305, y + 66)]
    d.line(pts, fill=(255, 90, 90), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x + 10, y + 4), "KOSPI 4,708.54", font=F_HS, fill=(255, 255, 255))
    d.text((x + w - 62, y + 4), "-3.3%", font=font("DejaVuSans-Bold.ttf", 22),
           fill=(255, 90, 90))


def draw_scene_guterres(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(18, 64, 120))
    # globe
    cx, cy, r = x + 62, y + 44, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 190, 230),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - 14, cy - 20, cx + 2, cy - 2], fill=(70, 160, 90))
    d.ellipse([cx + 2, cy + 6, cx + 18, cy + 22], fill=(70, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=1)
    # AI network nodes
    import random
    rnd = random.Random(11)
    nodes = []
    for _ in range(7):
        nodes.append((x + 130 + rnd.randint(0, 150), y + 10 + rnd.randint(0, 55)))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            d.line([nodes[i], nodes[j]], fill=(160, 200, 240), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 210, 90))
    # podium + speaker
    d.rectangle([x + 200, y + 62, x + 260, y + h - 4], fill=(120, 72, 30))
    d.ellipse([x + 222, y + 30, x + 238, y + 46], fill=(20, 20, 20))
    d.polygon([(x + 214, y + 62), (x + 246, y + 62), (x + 238, y + 46),
               (x + 222, y + 46)], fill=(20, 20, 20))
    d.text((x + 10, y + h - 16), "150 delegates", font=F_HS, fill=(255, 255, 255))


def draw_scene_power(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(252, 250, 244))
    d.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1)
    d.text((x + 8, y + 4), "ASIA POWER INDEX 2026", font=F_HK, fill=NAVY)
    d.text((x + w - 62, y + 4), "GAP 5.3", font=F_HK, fill=RED)
    rows = [("US", 78.9, BLUE), ("CHINA", 73.6, RED), ("INDIA 3rd", 40.5, GRAY)]
    yy = y + 24
    for label, val, col in rows:
        d.text((x + 8, yy), label, font=F_HS, fill=INK)
        bx = x + 78
        bw = int((w - 150) * val / 80.0)
        d.rectangle([bx, yy, bx + bw, yy + 13], fill=col)
        d.text((bx + bw + 6, yy - 1), f"{val}", font=F_HS, fill=INK)
        yy += 18


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    # grid
    for gx in range(1, 12):
        gx0 = x + gx * w / 12
        d.line([(gx0, y), (gx0, y + h)], fill=GRID, width=1)
    for gy in range(1, 6):
        gy0 = y + gy * h / 6
        d.line([(x, gy0), (x + w, gy0)], fill=GRID, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x, y, w, h) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(200, 185, 150))
    # pins
    for num, (lon, lat) in PINS.items():
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        col = AMBER if num in CLAIM_PINS else RED
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
                  outline=(255, 255, 255), width=1)
        d.text((px - 3 if num < 10 else px - 6, py - 5), str(num),
               font=F_PIN, fill=(255, 255, 255))
    d.text((x + 4, y + h - 12), "N \u2191", font=F_HS, fill=INK)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # top rule
    d.rectangle([0, 0, W, 8], fill=RED)
    # masthead
    d.text((16, 12), "THE WORLD TODAY", font=F_MAST, fill=INK)
    d.text((W - 16 - d.textlength("31 STORIES \u00b7 6 REGIONS", font=F_BAR), 22),
           "31 STORIES \u00b7 6 REGIONS", font=F_BAR, fill=RED)
    d.text((16, 74), "MONDAY 23 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.text((16, 102), "AI rout rattles Asia  \u00b7  Guterres: regulate AI now  \u00b7  "
                      "US lead over China at record low",
           font=F_KICK, fill=INK)
    d.line([(16, 122), (W - 16, 122)], fill=INK, width=2)
    # number strip
    y0, y1 = 128, 172
    cw = (W - 32) / 8.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 16 + i * cw
        d.text((cx + cw / 2 - d.textlength(num, font=F_NUM) / 2, y0),
               num, font=F_NUM, fill=RED)
        d.text((cx + cw / 2 - d.textlength(lab, font=F_NUML) / 2, y0 + 32),
               lab, font=F_NUML, fill=INK)
        if i:
            d.line([(cx, y0 + 2), (cx, y1 - 4)], fill=LIGHT, width=1)
    d.line([(16, y1), (W - 16, y1)], fill=INK, width=1)
    # region bar
    y0, y1 = 176, 198
    total = sum(len(t) for t, _ in REGIONS)
    rx = 16
    for label, col in REGIONS:
        seg = (W - 32) * len(label) / total
        d.rectangle([rx, y0, rx + seg, y1], fill=col)
        d.text((rx + 8, y0 + 4), label, font=F_BAR, fill=(255, 255, 255))
        rx += seg
    # UTC strip
    y0 = 204
    d.rectangle([16, y0, W - 16, y0 + 20], fill=NAVY)
    d.text((24, y0 + 4), "THE DAY IN UTC", font=F_UTCB, fill=(255, 210, 90))
    ux = 150
    for t, lab in UTC:
        s = f"{t}  {lab}"
        d.text((ux, y0 + 4), s, font=F_UTC, fill=(255, 255, 255))
        ux += d.textlength(s, font=F_UTC) + 16
    # heroes
    hy, hh = 230, 200
    hw = (W - 32 - 16) / 3.0
    for i, hero in enumerate(HEROES):
        hx = 16 + i * (hw + 8)
        d.rectangle([hx, hy, hx + hw, hy + hh], fill=PAPER, outline=LIGHT, width=1)
        sc = {"kospi": draw_scene_kospi, "guterres": draw_scene_guterres,
              "power": draw_scene_power}[hero["scene"]]
        sc(d, hx + 1, hy + 1, hw - 2, 84)
        ty = hy + 90
        d.text((hx + 8, ty), hero["kicker"], font=F_HK, fill=NAVY)
        ty += 15
        lines = wrap(d, hero["title"], F_HT, hw - 16, max_lines=2)
        ty = text_lines(d, hx + 8, ty, lines, F_HT, INK, leading=22)
        ty += 2
        blines = wrap(d, hero["body"], F_HB, hw - 16, max_lines=2)
        ty = text_lines(d, hx + 8, ty, blines, F_HB, INK, leading=15)
        chip(d, hx + hw - 84, hy + hh - 18, hero["chip"],
             CHIP_FILL[hero["chip"]])
        d.text((hx + 8, hy + hh - 16), f"#{hero['num']}  Source: {hero['source']}",
               font=F_HS, fill=GRAY)
    # cards: 2 rows x 5 cols
    cy0 = 438
    chh = 104
    cw2 = (W - 32 - 4 * 8) / 5.0
    for idx, (num, kicker, title, body, source, chip_lab, col) in enumerate(CARDS):
        r, c = divmod(idx, 5)
        cx = 16 + c * (cw2 + 8)
        cy = cy0 + r * (chh + 6)
        d.rectangle([cx, cy, cx + cw2, cy + chh], fill=PAPER, outline=LIGHT, width=1)
        d.rectangle([cx, cy, cx + cw2, cy + 20], fill=col)
        d.text((cx + 6, cy + 4), f"#{num}", font=F_CK, fill=(255, 255, 255))
        d.text((cx + 34, cy + 4), kicker, font=F_CK, fill=(255, 255, 255))
        ty = cy + 23
        tlines = wrap(d, title, F_CT, cw2 - 12, max_lines=2)
        ty = text_lines(d, cx + 6, ty, tlines, F_CT, INK, leading=15)
        blines = wrap(d, body, F_CB, cw2 - 12, max_lines=2)
        ty = text_lines(d, cx + 6, ty + 2, blines, F_CB, INK, leading=12)
        chip(d, cx + cw2 - 66, cy + chh - 18, chip_lab, CHIP_FILL[chip_lab])
        d.text((cx + 6, cy + chh - 16), source, font=F_CS, fill=GRAY)
    # map + ALSO
    my0 = 660
    mh = 212
    d.text((16, my0), "THE WORLD \u2014 WHERE IT HAPPENED", font=F_SEC, fill=RED)
    d.text((16 + 300, my0), "Red pin = reported \u00b7 Amber pin = claim",
           font=F_HS, fill=GRAY)
    draw_map(d, 16, my0 + 20, 480, mh - 20)
    ax = 516
    d.text((ax, my0), "ALSO ON MONDAY \u2014 18 MORE STORIES", font=F_SEC, fill=RED)
    ay = my0 + 22
    col_w = (W - 16 - ax - 8) / 2.0
    for i, (num, txt) in enumerate(ALSO):
        col_i, row_i = divmod(i, 9)
        lx = ax + col_i * (col_w + 8)
        ly = ay + row_i * 21
        d.text((lx, ly), f"{num}", font=F_ALB, fill=RED)
        lines = wrap(d, txt, F_AL, col_w - 24, max_lines=1)
        text_lines(d, lx + 22, ly, lines, F_AL, INK, leading=13)
    # DATE CHECK
    dy0, dy1 = 884, 962
    d.rectangle([16, dy0, W - 16, dy1], outline=RED, width=2)
    d.rectangle([16, dy0, W - 16, dy0 + 22], fill=RED)
    d.text((24, dy0 + 4), "DATE CHECK", font=F_DC, fill=(255, 255, 255))
    d.text((24, dy0 + 26),
           "Every story above happened or was first reported on Monday "
           "23 November 2026.",
           font=F_DCB, fill=INK)
    d.text((W - 16 - d.textlength("WIRES READ UP TO 23:00 UTC", font=F_DCB), dy0 + 26),
           "WIRES READ UP TO 23:00 UTC", font=F_DCB, fill=RED)
    left = ("LEFT OUT (not 23 Nov): Dems reach 258 (22 Nov) \u00b7 "
            "Sparta II fire (22 Nov) \u00b7 El Chapo captured (22 Nov) \u00b7 "
            "EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 "
            "ICJ Myanmar (19 Nov).")
    ly = text_lines(d, 24, dy0 + 44, wrap(d, left, F_DCB, W - 48, max_lines=2),
                    F_DCB, INK, leading=15)
    nyet = ("NOT YET: Dymer search continues (14 missing) \u00b7 4 House races "
            "uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped "
            "Ebola staff.")
    text_lines(d, 24, ly + 2, wrap(d, nyet, F_DCB, W - 48, max_lines=1),
               F_DCB, INK, leading=15)
    # footer
    fy = 970
    d.text((16, fy), "SOURCES: AP \u00b7 Reuters \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap "
                     "\u00b7 ESPN \u00b7 CNN \u00b7 Lowy Institute \u00b7 UN News \u00b7 "
                     "WHO \u00b7 Kyiv",
           font=F_FT, fill=GRAY)
    d.text((16, fy + 14), "REPORTED = confirmed by its source \u00b7 CLAIM = one side "
                          "alleges \u00b7 DENIAL = disputed \u00b7 ONGOING = still developing",
           font=F_FT, fill=GRAY)
    d.text((16, fy + 28), "Scenes are drawn illustrations, not photographs.",
           font=F_FT, fill=GRAY)
    d.text((W - 16 - d.textlength("THE WORLD TODAY \u00b7 23 NOV 2026", font=F_FT), fy + 28),
           "THE WORLD TODAY \u00b7 23 NOV 2026", font=F_FT, fill=GRAY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(f"saved {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
