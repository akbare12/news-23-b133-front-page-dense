#!/usr/bin/env python3
"""news-23 b133 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 hero scenes + 10 cards + 18 ALSO. PIL only; run: python3 draw.py
Writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

BG = (246, 241, 231)
INK = (17, 17, 17)
RED = (166, 25, 46)
GOLD = (184, 134, 11)
GOLD_L = (200, 155, 60)
NAVY = (11, 31, 58)
NAVY_L = (16, 61, 122)
GREEN = (30, 122, 52)
TEAL = (11, 122, 107)
PURPLE = (106, 27, 154)
GRAY = (90, 90, 90)
MAP_GREEN = (205, 230, 197)
MAP_EDGE = (140, 175, 130)
CREAM = (242, 235, 216)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x_right, y, label, fill):
    """Right-aligned pill chip; returns left edge x."""
    f = font(SANS_B, 9)
    tw = d.textlength(label, font=f)
    w = int(tw) + 12
    x0 = x_right - w
    d.rounded_rectangle([x0, y, x_right, y + 14], radius=7, fill=fill)
    d.text((x0 + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x0


def kospi_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # buildings with lit windows
    import random
    rnd = random.Random(23)
    bx = x0 + 6
    while bx < x0 + w - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(38, 78)
        by = y0 + h - bh - 16
        d.rectangle([bx, by, bx + bw, y0 + h - 16], fill=(18, 48, 88))
        d.rectangle([bx, by, bx + bw, by + 4], fill=(28, 68, 118))
        for wy in range(by + 9, y0 + h - 20, 11):
            for wx in range(bx + 5, bx + bw - 5, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
        bx += bw + 5
    # descending orange chart, kept well below the big label
    pts = []
    n = 7
    for i in range(n):
        px = x0 + 34 + i * (w - 76) // (n - 1)
        py = y0 + 60 + i * 6 + (0 if i < 3 else (i - 2) * 3)
        pts.append((px, py))
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 6), "-3.3%", font=font(SANS_B, 34), fill=(255, 255, 255))
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(7, 22, 42))
    d.text((x0 + 8, y0 + h - 14),
           "KOSPI 4,708.54  ·  -161 PTS  ·  SAMSUNG -3.1%  ·  HYNIX -2.5%",
           font=font(SANS_B, 8), fill=(255, 214, 90))


def guterres_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=GREEN)
    d.text((x0 + 12, y0 + 4), "150", font=font(SANS_B, 40), fill=(255, 214, 90))
    lines = wrap(d, "DELEGATES BACK A RISK FRAMEWORK", font(SANS_B, 15), 190)
    yy = y0 + 50
    for ln in lines:
        d.text((x0 + 12, yy), ln, font=font(SANS_B, 15), fill=(255, 214, 90))
        yy += 18
    # globe on the right
    cx, cy, r = x0 + w - 62, y0 + h // 2 + 4, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 240, 214))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 180, 120), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 180, 120))
    d.line([cx - r, cy, cx + r, cy], fill=(120, 180, 120), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=(120, 180, 120), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 180, 360, fill=(120, 180, 120), width=2)
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(18, 92, 40))
    d.text((x0 + 8, y0 + h - 14), "BRIDGETOWN SUMMIT, BARBADOS",
           font=font(SANS_B, 9), fill=(255, 214, 90))


def power_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    d.text((x0 + 10, y0 + 8), "NARROWEST SINCE 2018", font=font(SANS_B, 13), fill=INK)
    d.text((x0 + w - 78, y0 + 8), "GAP 5.3", font=font(SANS_B, 13), fill=RED)
    bars = [("78.9", "US", NAVY, 0.789), ("73.6", "CHINA", RED, 0.736),
            ("40.5", "INDIA", GOLD, 0.405)]
    yy = y0 + 30
    for val, name, color, frac in bars:
        d.text((x0 + 10, yy), val, font=font(SANS_B, 15), fill=INK)
        bx = x0 + 62
        bw = int((w - 78) * frac)
        d.rectangle([bx, yy + 2, bx + bw, yy + 17], fill=color)
        d.text((bx + 6, yy + 3), name, font=font(SANS_B, 11), fill=(255, 255, 255))
        yy += 22
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(226, 216, 188))
    d.text((x0 + 8, y0 + h - 14), "ASIA POWER INDEX 2026  ·  LOWY INSTITUTE",
           font=font(SANS_B, 9), fill=(90, 70, 20))


def hero_text(d, x0, x1, y, headline, body, source):
    f_h = font(SANS_B, 17)
    lines = wrap(d, headline, f_h, x1 - x0)
    yy = y
    for ln in lines[:2]:
        d.text((x0, yy), ln, font=f_h, fill=INK)
        yy += 21
    f_b = font(SANS, 11)
    blines = wrap(d, body, f_b, x1 - x0)
    by = y + 44
    for ln in blines[:2]:
        d.text((x0, by), ln, font=f_b, fill=(40, 40, 40))
        by += 13
    d.text((x0, y + 72), source, font=font(SANS, 10), fill=GRAY)
    chip(d, x1, y + 70, "REPORTED", NAVY_L)


CARDS = [
    ("1", "AMERICAS", (166, 25, 46), "BESSENT: NVIDIA ANSWERS",
     "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", (166, 25, 46), "FBI PROBES NCIC HACK",
     "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", (106, 27, 154), "IRAN STRIKES MAY RESUME",
     "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", (11, 94, 122), "US FUTURES JUMP 3%",
     "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", (178, 91, 0), "SKUBAL'S $450M METS DEAL",
     "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", (178, 91, 0), "TOM JACKSON DIES AT 75",
     "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", (51, 51, 51), "STATES SUE SPACEX",
     "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", (11, 94, 122), "ANTHROPIC IPO: $107.3B",
     "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", (30, 122, 52), "3 MISSILES CROSSED AIRSPACE",
     "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("10", "SPACE", (51, 51, 51), "RUSSIAN NUCLEAR SATELLITE",
     "May carry a nuke.", "Reuters", "CLAIM"),
]

ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands probe [CLAIM]",
    "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]

PINS = [
    (1, 388, 636), (2, 118, 756), (3, 378, 606), (4, 88, 656), (5, 108, 626),
    (6, 268, 616), (7, 238, 640), (8, 224, 612), (9, 284, 644), (10, 214, 598),
    (11, 298, 678), (12, 292, 708), (13, 268, 748),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.text((10, 4), "THE WORLD TODAY", font=font(SERIF_B, 46), fill=INK)
    d.text((1014, 22), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 16),
           fill=GOLD, anchor="ra")
    # --- kicker ---
    d.rectangle([0, 58, W, 80], fill=RED)
    d.text((10, 63), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
           font=font(SANS_B, 13), fill=(255, 255, 255))

    # --- number strip: 2 rows x 5 ---
    nums = [
        ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    for i, (val, lab) in enumerate(nums):
        col = i % 5
        row = i // 5
        x = 10 + col * 201
        yv = 84 + row * 40
        d.text((x, yv), val, font=font(SANS_B, 23), fill=INK)
        d.text((x, yv + 26), lab, font=font(SANS_B, 10), fill=(60, 60, 60))

    # --- region bar with counts ---
    regions = [("ASIA-PACIFIC 7", 7, NAVY_L), ("AMERICAS 8", 8, RED),
               ("MIDDLE EAST 6", 6, PURPLE), ("EUROPE 5", 5, TEAL),
               ("AFRICA 3", 3, GREEN), ("WORLD 2", 2, GOLD)]
    rx = 10
    for label, count, color in regions:
        seg_w = int(1004 * count / 31)
        d.rectangle([rx, 166, rx + seg_w, 184], fill=color)
        d.text((rx + seg_w / 2, 170), label, font=font(SANS_B, 11),
               fill=(255, 255, 255), anchor="ma")
        rx += seg_w

    # --- UTC strip ---
    d.text((10, 188), "THE DAY IN UTC   ~00:00 Kospi dives   ~05:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
           font=font(SANS, 11), fill=(60, 60, 60))
    d.text((1014, 188), "~ APPROX", font=font(SANS, 11), fill=GRAY, anchor="ra")

    # --- hero scenes ---
    cols = [(10, 336), (344, 670), (678, 1014)]
    kospi_scene(d, cols[0][0], 204, cols[0][1] - cols[0][0], 110)
    guterres_scene(d, cols[1][0], 204, cols[1][1] - cols[1][0], 110)
    power_scene(d, cols[2][0], 204, cols[2][1] - cols[2][0], 110)
    hero_text(d, cols[0][0], cols[0][1], 318, "AI ROUT HITS ASIA",
              "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
              "KOREA EXCHANGE")
    hero_text(d, cols[1][0], cols[1][1], 318, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
              "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
              "UNITED NATIONS")
    hero_text(d, cols[2][0], cols[2][1], 318, "US LEAD OVER CHINA AT RECORD LOW",
              "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
              "LOWY INSTITUTE")

    # --- more of the day ---
    d.rectangle([0, 404, W, 424], fill=INK)
    d.text((10, 408), "MORE OF THE DAY  —  10 STORIES", font=font(SANS_B, 13), fill=(255, 255, 255))
    cw, gap = 194, 8
    for i, (num, cat, color, head, body, src, tag) in enumerate(CARDS):
        col, row = i % 5, i // 5
        x = 10 + col * (cw + gap)
        y = 428 + row * 64
        d.text((x, y + 2), num, font=font(SANS_B, 11), fill=RED)
        d.text((x + 24 if len(num) == 1 else x + 30, y + 2), cat,
               font=font(SANS_B, 10), fill=color)
        f_h = font(SANS_B, 11)
        hlines = wrap(d, head, f_h, cw)
        hy = y + 15
        for ln in hlines[:2]:
            d.text((x, hy), ln, font=f_h, fill=INK)
            hy += 13
        d.text((x, y + 42), body, font=font(SANS, 10), fill=(40, 40, 40))
        d.text((x, y + 53), src, font=font(SANS, 9), fill=GRAY)
        chip(d, x + cw, y + 52, tag, NAVY_L if tag == "REPORTED" else RED)

    # --- where it happened ---
    d.rectangle([0, 562, W, 582], fill=INK)
    d.text((10, 566), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=(255, 255, 255))
    # map blobs
    d.polygon([(18, 640), (60, 600), (120, 596), (150, 630), (140, 700), (120, 760),
               (90, 790), (40, 770), (18, 720)], fill=MAP_GREEN, outline=MAP_EDGE)
    d.polygon([(170, 610), (230, 592), (300, 600), (320, 650), (300, 720), (270, 780),
               (220, 790), (180, 750), (168, 680)], fill=MAP_GREEN, outline=MAP_EDGE)
    d.polygon([(330, 620), (380, 596), (414, 620), (414, 700), (390, 760), (340, 770),
               (322, 700)], fill=MAP_GREEN, outline=MAP_EDGE)
    f_pin = font(SANS_B, 10)
    for num, px, py in PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=f_pin, fill=(255, 255, 255), anchor="mm")
    d.text((10, 792), "Pins 1–13:  1 Seoul  ·  2 Bridgetown  ·  3 Beijing  ·  4 Washington",
           font=font(SANS, 9), fill=(60, 60, 60))
    d.text((10, 805), "5 New York  ·  6 Kyiv  ·  7 Paris  ·  8 London  ·  9 Warsaw  ·  10 Manchester",
           font=font(SANS, 9), fill=(60, 60, 60))
    d.text((10, 818), "11 Beirut  ·  12 Gaza  ·  13 Khartoum",
           font=font(SANS, 9), fill=(60, 60, 60))

    # --- ALSO ---
    ax = 436
    d.text((ax, 586), "ALSO ON MONDAY", font=font(SANS_B, 13), fill=INK)
    f_a = font(SANS, 12)
    for i, item in enumerate(ALSO):
        col = i // 9
        row = i % 9
        x = ax + col * 292
        y = 606 + row * 26
        label = f"{14 + i}. {item}"
        if "[CLAIM]" in label:
            base = label.replace(" [CLAIM]", "")
            d.text((x, y), base, font=f_a, fill=INK)
            tw = d.textlength(base, font=f_a)
            d.text((x + tw + 4, y), "[CLAIM]", font=font(SANS_B, 12), fill=RED)
        else:
            d.text((x, y), label, font=f_a, fill=INK)

    # --- DATE CHECK ---
    d.rectangle([8, 858, 1016, 928], outline=RED, width=2)
    d.text((16, 864), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  STORIES DATED 23 NOV ONLY",
           font=font(SANS_B, 12), fill=RED)
    d.text((16, 884), "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
           font=font(SANS, 11), fill=INK)
    d.text((16, 899), "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
           font=font(SANS, 11), fill=INK)
    d.text((16, 914), "NOT YET — Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
           font=font(SANS, 11), fill=INK)

    # --- footer ---
    d.text((10, 936), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=font(SANS, 10), fill=GRAY)
    d.text((10, 950), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, independently unconfirmed · ONGOING = still developing.",
           font=font(SANS, 10), fill=GRAY)
    d.text((10, 964), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=font(SANS, 10), fill=GRAY)
    d.line([(10, 992), (1014, 992)], fill=GOLD, width=2)
    d.text((512, 998), "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions",
           font=font(SANS_B, 12), fill=GOLD, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
