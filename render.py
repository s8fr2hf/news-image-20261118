#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page (1024x1024 PNG).

Build-time only: the entry program (main.py) just copies entry.png.
Deterministic: no network, no clock, no randomness. Run:
    python3 render.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), size)


def regular(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), size)


NAVY = (11, 37, 69)
GOLD = (201, 162, 39)
CREAM = (247, 243, 234)
INK = (20, 20, 20)
GREY = (90, 90, 90)
BORDER = (201, 201, 201)
RED = (180, 35, 24)
BLUE = (46, 111, 183)
AMBER = (166, 110, 15)
TEAL = (14, 124, 123)
WHITE = (255, 255, 255)


def wrap(draw, text, font, widths):
    """Wrap text into lines; widths is a list of max widths, reused for later lines."""
    words = text.split()
    lines = []
    line = ""
    i = 0
    while i < len(words):
        w = widths[min(len(lines), len(widths) - 1)]
        trial = (line + " " + words[i]).strip()
        if draw.textlength(trial, font=font) <= w or not line:
            line = trial
            i += 1
        else:
            lines.append(line)
            line = ""
    if line:
        lines.append(line)
    return lines


def draw_lines(draw, lines, x, y, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def icon_bridge(d, x, y, s=72):
    d.line([x + 4, y + 44, x + s - 4, y + 44], fill=NAVY, width=4)
    d.arc([x + 10, y + 12, x + s - 10, y + 52], 180, 360, fill=NAVY, width=4)
    d.line([x + 16, y + 44, x + 16, y + 62], fill=NAVY, width=3)
    d.line([x + s - 16, y + 44, x + s - 16, y + 62], fill=NAVY, width=3)
    d.line([x + 30, y + 44, x + 30, y + 62], fill=NAVY, width=3)
    d.line([x + s - 30, y + 44, x + s - 30, y + 62], fill=NAVY, width=3)
    d.line([x + 4, y + 66, x + s - 4, y + 66], fill=BLUE, width=3)
    d.line([x + 14, y + 70, x + s - 14, y + 70], fill=BLUE, width=2)
    # broken span: a red gap in the deck
    d.line([x + s // 2 - 6, y + 44, x + s // 2 + 6, y + 44], fill=RED, width=5)


def icon_drone(d, x, y, s=72):
    d.line([x + 6, y + 58, x + s - 6, y + 20], fill=GREY, width=2)
    d.line([x + 6, y + 58, x + s - 6, y + 58], fill=GREY, width=2)
    d.line([x + 6, y + 58, x + 22, y + 30], fill=GREY, width=2)
    d.polygon([(x + 40, y + 10), (x + 58, y + 34), (x + 40, y + 28)],
              fill=NAVY)
    d.ellipse([x + 34, y + 6, x + 46, y + 18], fill=RED)
    d.ellipse([x + 52, y + 28, x + 64, y + 40], fill=RED)


def icon_dots(d, x, y, s=72):
    for cx, cy, r in [(22, 24, 12), (46, 18, 9), (56, 42, 13),
                      (28, 50, 10), (48, 62, 8)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=RED)


def icon_senate(d, x, y, s=72):
    d.rectangle([x + 4, y + 26, x + 4 + 40, y + 46], fill=BLUE)
    d.rectangle([x + 4 + 40, y + 26, x + s - 4, y + 46], fill=RED)
    f = bold(15)
    d.text((x + 6, y + 50), "56", font=f, fill=BLUE)
    d.text((x + s - 26, y + 50), "44", font=f, fill=RED)


def panel(d, x, y, w, h, accent, kicker, headline, deck, icon):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([x, y, x + 8, y + h], fill=accent)
    ix = x + 18
    iy = y + 18
    icon(d, ix, iy)
    tx = x + 104
    tw = x + w - 18 - tx
    f_kick = bold(19)
    d.text((tx, y + 20), kicker, font=f_kick, fill=accent)
    hl = wrap(d, headline, bold(26), [tw])
    yy = draw_lines(d, hl[:2], tx, y + 48, bold(26), INK, 32)
    dl = wrap(d, deck, regular(20), [tw])
    draw_lines(d, dl[:3], tx, yy + 4, regular(20), (60, 60, 60), 26)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((24, 18), "THE WORLD IN ONE PICTURE", font=bold(46), fill=WHITE)
    d.text((24, 82), "WEDNESDAY  ·  18 NOVEMBER 2026",
           font=bold(30), fill=GOLD)
    d.rectangle([0, 148, W, 152], fill=GOLD)

    # Lead story
    d.rectangle([24, 168, 1000, 428], fill=CREAM, outline=BORDER, width=1)
    d.rectangle([24, 168, 32, 428], fill=RED)
    d.text((48, 184), "LEAD  ·  SHENZHEN, CHINA", font=bold(21), fill=RED)
    hl = wrap(d, "Trump, Xi and Putin set for historic three-way summit",
              bold(40), [620])
    draw_lines(d, hl, 48, 214, bold(40), INK, 48)
    deck = wrap(d, "Xi hosted Putin in Shenzhen on Wednesday. Trump "
                   "arrives for Thursday's first-ever trilateral "
                   "summit, with Ukraine and Iran on the agenda.",
                regular(23), [620])
    draw_lines(d, deck, 48, 316, regular(23), (60, 60, 60), 30)

    # Lead graphic: three leader circles
    for (cx, cy, col, txt, tcol) in [
            (758, 256, (31, 78, 121), "USA", WHITE),
            (862, 256, (192, 57, 43), "CHN", WHITE),
            (810, 336, WHITE, "RUS", NAVY)]:
        d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=col,
                  outline=NAVY, width=3)
        f = bold(26)
        tw = d.textlength(txt, font=f)
        d.text((cx - tw / 2, cy - 18), txt, font=f, fill=tcol)
    d.text((748, 396), "MEETING THURSDAY", font=bold(15), fill=GREY)

    # Story grid
    panel(d, 24, 444, 476, 212, BLUE, "UKRAINE",
          "Crimea bridge hit in Ukrainian strike",
          "Drones and missiles brought down an arch of the Kerch "
          "bridge. Moscow hit bridges in Kyiv in reply.", icon_bridge)
    panel(d, 524, 444, 476, 212, AMBER, "MIDDLE EAST",
          "Iran strikes Bahrain and Kuwait",
          "After US strikes on a missile site on Iran's Qeshm "
          "Island, Tehran's drones hit Bahrain and Kuwait.", icon_drone)
    panel(d, 24, 664, 476, 212, RED, "UNITED STATES · HEALTH",
          "US loses its measles-free status after 26 years",
          "A record outbreak of 5,400+ cases and 10 deaths ends "
          "26 years of measles elimination.", icon_dots)
    panel(d, 524, 664, 476, 212, TEAL, "UNITED STATES · POLITICS",
          "Democrats take the Senate, 56 seats to 44",
          "Mary Peltola beat Dan Sullivan in Alaska, completing "
          "the Democrats' midterm sweep.", icon_senate)

    # Ticker
    d.rectangle([24, 892, 1000, 972], fill=NAVY)
    tick = wrap(d, "ALSO ON 18 NOVEMBER:  Ebola in DR Congo kills 3 in 4 "
                   "children under 5  ·  Cyclone Akvan nears Odisha  ·  "
                   "An-12 crash in Siberia kills 19  ·  Cold kills in "
                   "Gaza's tent camps",
                regular(20), [940])
    draw_lines(d, tick[:2], 44, 906, regular(20), WHITE, 28)

    # Footer
    f = regular(16)
    ft = "Wednesday 18 November 2026  ·  Compiled from wire reports"
    d.text(((W - d.textlength(ft, font=f)) / 2, 986), ft, font=f, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
