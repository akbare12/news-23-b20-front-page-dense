#!/usr/bin/env python3
"""news-23 b20 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories, 1024x1024, PIL only. Written fresh in this session."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (245, 240, 225)      # paper cream
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GOLD = (184, 134, 11)
NAVY = (24, 48, 88)
TEAL = (14, 90, 86)
GREEN = (46, 110, 58)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)

SERIF_B = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
           "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
           "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
SANS_B = ["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def fb(size):
    return font(SANS_B, size)


def fr(size):
    return font(SANS, size)


def serif(size):
    return font(SERIF_B, size)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, fnt, maxw):
    """Shrink font until text fits maxw; returns (font, text)."""
    size = fnt.size
    f = fnt
    while d.textlength(text, font=f) > maxw and size > 8:
        size -= 1
        f = font(SANS_B, size) if f is not None else f
    return f


def chip(d, x, y, label, fill, fg=(255, 255, 255), size=9):
    f = fb(size)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 1), label, font=f, fill=fg)
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 14  # margin
R = W - M  # 1010

# ---------- masthead ----------
d.rectangle([0, 0, W, 62], fill=(12, 12, 12))
d.text((M, 8), "THE WORLD TODAY", font=serif(42), fill=(255, 255, 255))
d.text((R - d.textlength("MONDAY  23 NOVEMBER 2026", font=fb(20)), 20),
       "MONDAY  23 NOVEMBER 2026", font=fb(20), fill=(212, 175, 55))

# ---------- kicker ----------
d.text((M, 68), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=fb(14), fill=DARKRED)

# ---------- number strip (5 big numbers) ----------
nums = [("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", (122, 90, 10)), ("$450M", "SKUBAL DEAL", GREEN),
        ("$107.3B", "ANTHROPIC IPO", (110, 40, 130))]
col_w = (W - 2 * M) // 5
for i, (n, lab, col) in enumerate(nums):
    x = M + i * col_w
    d.text((x, 88), n, font=fb(26), fill=col)
    d.text((x, 118), lab, font=fb(11), fill=INK)
    if i:
        d.line([(x - 6, 90), (x - 6, 132)], fill=(200, 192, 170), width=1)

# ---------- THE DAY IN NUMBERS ----------
d.rectangle([M, 138, R, 152], fill=(30, 30, 30))
d.text((M + 6, 140), "THE DAY IN NUMBERS", font=fb(11), fill=(212, 175, 55))
d.text((M + 148, 140), "-5.8% intraday low   \u00b7   165 missiles in a week   \u00b7   12,000 cleared   \u00b7   264 kg seized   \u00b7   2% tax backed",
       font=fr(11), fill=(255, 255, 255))

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 6", (46, 110, 58)), ("AMERICAS 9", NAVY),
           ("MIDDLE EAST 6", (150, 100, 20)), ("EUROPE 5", TEAL),
           ("AFRICA 3", (90, 60, 90)), ("WORLD 2", (100, 100, 100))]
seg_w = (W - 2 * M) // 6
for i, (lab, col) in enumerate(regions):
    x = M + i * seg_w
    d.rectangle([x, 156, x + seg_w - 2, 172], fill=col)
    f = fb(11)
    tw = d.textlength(lab, font=f)
    d.text((x + (seg_w - 2 - tw) / 2, 159), lab, font=f, fill=(255, 255, 255))

# ---------- hero scenes ----------
HX = [M, 352, 690]
HW = 320
HY0, HY1 = 178, 290  # scene box
heroes = [
    dict(num=1, title="AI ROUT HITS ASIA",
         body="Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="KOREA EXCHANGE"),
    dict(num=2, title="GUTERRES: REGULATE AI BEFORE IT\u2019S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         src="UNITED NATIONS"),
    dict(num=3, title="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         src="LOWY INSTITUTE"),
]

# scene 1: Kospi night skyline + falling chart
x0 = HX[0]
d.rectangle([x0, HY0, x0 + HW, HY1], fill=(16, 24, 52))
for sx, sy in [(x0 + 30, HY0 + 14), (x0 + 90, HY0 + 8), (x0 + 150, HY0 + 18),
               (x0 + 210, HY0 + 10), (x0 + 270, HY0 + 16), (x0 + 300, HY0 + 8)]:
    d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
d.text((x0 + 10, HY0 + 6), "-3.3%", font=fb(30), fill=(255, 90, 70))
pts = [(x0 + 12, HY0 + 52), (x0 + 70, HY0 + 46), (x0 + 120, HY0 + 58),
       (x0 + 180, HY0 + 50), (x0 + 240, HY0 + 66), (x0 + 305, HY0 + 78)]
d.line(pts, fill=(255, 90, 70), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 60))
import random
random.seed(23)
for bx in range(x0 + 8, x0 + HW - 8, 26):
    bh = random.randint(18, 46)
    d.rectangle([bx, HY1 - bh, bx + 20, HY1], fill=(38, 52, 96))
    for wy in range(HY1 - bh + 5, HY1 - 4, 9):
        for wx in (bx + 4, bx + 12):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 100))
d.rectangle([x0, HY1 - 16, x0 + HW, HY1], fill=(0, 0, 0))
d.text((x0 + 8, HY1 - 14), "KOSPI  4,708.54   \u00b7   -161 PTS", font=fb(11), fill=(255, 255, 255))

# scene 2: Guterres globe + flags
x0 = HX[1]
d.rectangle([x0, HY0, x0 + HW, HY1], fill=TEAL)
d.text((x0 + 10, HY0 + 6), "150 DELEGATES", font=fb(28), fill=(255, 220, 80))
d.text((x0 + 10, HY0 + 38), "BACK A RISK FRAMEWORK", font=fb(15), fill=(255, 255, 255))
# flags
for fx, fc in [(x0 + 18, RED), (x0 + 62, (40, 90, 200)), (x0 + 106, (240, 200, 40))]:
    d.line([(fx, HY0 + 66), (fx, HY0 + 108)], fill=(255, 255, 255), width=2)
    d.polygon([(fx, HY0 + 66), (fx + 30, HY0 + 74), (fx, HY0 + 82)], fill=fc)
# podium
d.polygon([(x0 + 150, HY1), (x0 + 200, HY0 + 78), (x0 + 250, HY1)], fill=(120, 70, 30))
# globe
cx, cy, gr = x0 + 268, HY0 + 66, 44
d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(190, 220, 235), outline=(255, 255, 255), width=2)
d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], outline=(90, 130, 160))
d.ellipse([cx - 16, cy - gr, cx + 16, cy + gr], outline=(90, 130, 160))
d.line([(cx - gr, cy), (cx + gr, cy)], fill=(90, 130, 160))
d.ellipse([cx - 26, cy - 30, cx - 10, cy - 14], fill=(70, 160, 90))
d.ellipse([cx + 6, cy + 8, cx + 24, cy + 26], fill=(70, 160, 90))
d.rectangle([x0, HY1 - 16, x0 + HW, HY1], fill=(0, 0, 0))
d.text((x0 + 8, HY1 - 14), "UN  \u00b7  BRIDGETOWN", font=fb(11), fill=(255, 255, 255))

# scene 3: US-China-India bars
x0 = HX[2]
d.rectangle([x0, HY0, x0 + HW, HY1], fill=(248, 244, 232))
d.text((x0 + 10, HY0 + 6), "NARROWEST SINCE 2018", font=fb(13), fill=INK)
d.text((x0 + HW - 8 - d.textlength("GAP 5.3", font=fb(13)), HY0 + 6), "GAP 5.3", font=fb(13), fill=GOLD)
bars = [("78.9", "US", NAVY, 38), ("73.6", "CHINA", RED, 35), ("40.5", "INDIA", GOLD, 19)]
bw = 62
for i, (val, lab, col, bh) in enumerate(bars):
    bx = x0 + 24 + i * 100
    d.text((bx + (bw - d.textlength(val, font=fb(16))) / 2, HY0 + 28), val, font=fb(16), fill=col)
    d.rectangle([bx, HY1 - 34 - bh + 8, bx + bw, HY1 - 34 + 8], fill=col)
    d.text((bx + (bw - d.textlength(lab, font=fb(11))) / 2, HY1 - 22), lab, font=fb(11), fill=INK)

# hero headlines + bodies + source/chip
for i, h in enumerate(heroes):
    x0 = HX[i]
    y = HY1 + 6
    d.ellipse([x0, y + 2, x0 + 18, y + 20], fill=RED)
    d.text((x0 + 6, y + 3), str(h["num"]), font=fb(12), fill=(255, 255, 255))
    lines = wrap(d, h["title"], fb(16), HW - 24)
    ly = y
    for ln in lines[:2]:
        d.text((x0 + 24, ly), ln, font=fb(16), fill=INK)
        ly += 18
    by = y + 38
    blines = wrap(d, h["body"], fr(11), HW - 4)
    for ln in blines[:2]:
        d.text((x0, by), ln, font=fr(11), fill=(40, 40, 40))
        by += 12
    d.text((x0, by + 1), h["src"], font=fr(9), fill=GREY)
    chip(d, x0 + HW - 62, by - 1, "REPORTED", NAVY)

# ---------- cards ----------
d.text((M, 372), "MORE OF THE DAY \u2014 10 STORIES", font=fb(15), fill=INK)
d.line([(M, 390), (R, 390)], fill=INK, width=2)
cards = [
    (4, "AMERICAS", NAVY, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants to know of violations over China sales.", "Reuters", "REPORTED"),
    (5, "FBI", (90, 40, 110), "FBI PROBES NCIC HACK", "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED"),
    (6, "WHITE HOUSE", (150, 100, 20), "TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could resume in the New Year.", "Reuters", "REPORTED"),
    (7, "MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "Bloomberg", "REPORTED"),
    (8, "SPORT", (40, 90, 130), "SKUBAL\u2019S $450M METS DEAL", "Two-time Cy Young winner signs nine years, largest ever for a pitcher.", "ESPN", "REPORTED"),
    (9, "SPORT", (40, 90, 130), "TOM JACKSON DIES AT 75", "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED"),
    (10, "LEGAL", (110, 40, 130), "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED"),
    (11, "TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED"),
    (12, "EUROPE", (150, 60, 40), "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM"),
    (13, "SPACE", (90, 90, 90), "RUSSIAN NUCLEAR SATELLITE", "Intel claims Moscow built a satellite to carry a nuclear warhead.", "Reuters", "CLAIM"),
]
CW = 194
CGAP = 6
CY0, CH = 396, 92
for idx, (num, cat, col, head, body, src, tag) in enumerate(cards):
    row, c = divmod(idx, 5)
    x = M + c * (CW + CGAP)
    y = CY0 + row * (CH + 6)
    d.rectangle([x, y, x + CW, y + CH], fill=(255, 255, 255), outline=(210, 202, 182))
    d.rectangle([x, y, x + CW, y + 15], fill=col)
    d.text((x + 5, y + 2), cat, font=fb(9), fill=(255, 255, 255))
    ntxt = str(num)
    d.text((x + CW - 8 - d.textlength(ntxt, font=fb(10)), y + 2), ntxt, font=fb(10), fill=(255, 255, 255))
    hl = wrap(d, head, fb(12), CW - 10)
    hy = y + 19
    for ln in hl[:2]:
        d.text((x + 5, hy), ln, font=fb(12), fill=INK)
        hy += 14
    bl = wrap(d, body, fr(10), CW - 10)
    by = hy + 1
    for ln in bl[:2]:
        d.text((x + 5, by), ln, font=fr(10), fill=(50, 50, 50))
        by += 12
    d.text((x + 5, y + CH - 15), src, font=fr(9), fill=GREY)
    chip(d, x + CW - 60, y + CH - 16, tag, RED if tag == "CLAIM" else NAVY)

# ---------- map + ALSO ----------
d.text((M, 592), "WHERE IT HAPPENED", font=fb(14), fill=INK)
d.text((494, 592), "ALSO ON MONDAY", font=fb(14), fill=INK)
d.line([(M, 610), (R, 610)], fill=INK, width=2)
# map box
d.rectangle([M, 614, 480, 806], fill=(214, 230, 240))
for gx in range(M + 20, 480, 24):
    d.line([(gx, 614), (gx, 806)], fill=(190, 210, 224), width=1)
for gy in range(614 + 20, 806, 24):
    d.line([(M, gy), (480, gy)], fill=(190, 210, 224), width=1)
continents = [
    [(35, 640), (150, 625), (185, 665), (160, 715), (110, 735), (45, 700)],  # N America
    [(150, 740), (195, 735), (190, 795), (160, 800)],                        # S America
    [(320, 632), (360, 628), (366, 656), (325, 662)],                        # Europe
    [(320, 672), (370, 668), (378, 745), (332, 758)],                        # Africa
    [(365, 625), (472, 620), (478, 680), (440, 720), (400, 715), (368, 668)],  # Asia
    [(420, 775), (460, 772), (465, 795), (425, 798)],                        # Australia
]
for poly in continents:
    d.polygon(poly, fill=(150, 190, 120), outline=(110, 160, 90))
pins = [(1, 460, 658), (2, 185, 700), (3, 438, 636), (4, 140, 665), (5, 160, 650),
        (6, 398, 668), (7, 120, 665), (8, 60, 670), (9, 95, 685), (10, 115, 700),
        (11, 335, 632), (12, 362, 652), (13, 392, 632)]
for num, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    t = str(num)
    d.text((px - d.textlength(t, font=fb(9)) / 2, py - 6), t, font=fb(9), fill=(255, 255, 255))
pin_legend = "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago \u00b7 8 San Francisco \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow"
pl = wrap(d, pin_legend, fr(10), 466)
py = 812
for ln in pl:
    d.text((M, py), ln, font=fr(10), fill=(60, 60, 60))
    py += 12

# ALSO list (18 items, two columns of 9)
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over exam chaos", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col, row = divmod(i, 9)
    ax = 494 + col * 262
    ay = 618 + row * 20
    f = fr(11)
    txt = item
    while d.textlength(txt, font=f) > 256 and len(txt) > 20:
        txt = txt[:-4].rstrip() + "\u2026"
    d.text((ax, ay), txt, font=f, fill=INK)

# ---------- DATE CHECK ----------
d.rectangle([M, 852, R, 936], outline=RED, width=2, fill=(255, 244, 240))
d.text((M + 8, 858), "DATE CHECK", font=fb(14), fill=RED)
d.text((M + 108, 860), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=fb(11), fill=INK)
dc1 = "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)"
dc2 = "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff"
for j, ln in enumerate(wrap(d, dc1, fr(11), R - M - 16)):
    d.text((M + 8, 880 + j * 14), ln, font=fr(11), fill=INK)
for j, ln in enumerate(wrap(d, dc2, fr(11), R - M - 16)):
    d.text((M + 8, 908 + j * 14), ln, font=fr(11), fill=INK)

# ---------- footer ----------
d.text((M, 944), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=fr(10), fill=GREY)
d.text((M, 958), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side\u2019s claim, not independently confirmed \u00b7 ONGOING = still developing",
       font=fr(10), fill=GREY)
d.rectangle([0, 978, W, H], fill=(12, 12, 12))
foot = "Scenes are drawn illustrations, not photographs.  \u00b7  THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(foot, font=fb(12))) / 2, 992), foot, font=fb(12), fill=(212, 175, 55))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
