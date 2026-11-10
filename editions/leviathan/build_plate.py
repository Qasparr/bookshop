#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Non est super terram potestas quae comparetur ei." -- Job 41:33
(Vulgate numbering 41:24), the verse Hobbes set over his beast.

PLATE I -- LEVIATHAN: an original emblem, struck programmatically.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man.

MECHANISM / DOCTRINE -- what this plate is, and what it is not:

  The 1651 frontispiece of Leviathan is an engraving associated with
  Abraham Bosse's circle: a crowned giant, his body composed of the
  multitude of his subjects, sword in the right hand and crozier in
  the left, town and country beneath him. That image is Hobbes's own
  concept for his book. This plate takes the CONCEPT and nothing
  else: it is drawn fresh, in geometry, by this program -- a crowned
  head; a torso and arms built literally of many small circles, the
  multitude made visible as the brief of the emblem requires; the
  sword and the crozier as clean emblem shapes, both held upright
  and both kept inside the frame; a walled town and open country in
  the band below. No line of the 1651 engraving is traced, copied,
  or imitated in its draftsmanship; the homage is to the idea, and
  the edition's apparatus says exactly that.

  The head is left featureless by design: Hobbes, in the Dedicatory
  printed in this volume, speaks "not of the men, but (in the
  Abstract) of the Seat of Power." The emblem figures the seat, not
  a sitter.

  House rule (ART-REPORT, 2026-11-02): no plate carries lettering.
  The book's typography lives in the book. This image is art only;
  its caption stands in the PDF beneath it.

  Colours are the canonical livery: purple field, gold figure and
  tooling, green the living rule and the land.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / "PLATE-I-LEVIATHAN-EMBLEM.png"

W, H = 1800, 2400
PURPLE = (43, 12, 78)
GOLD = (232, 190, 92)
GOLD_D = (146, 108, 38)
GREEN = (46, 204, 113)


def base():
    img = Image.new("RGB", (W, H), PURPLE)
    px = img.load()
    cx, cy = W / 2, H * 0.42
    for y in range(H):
        for x in range(0, W, 4):
            d = math.hypot(x - cx, y - cy) / (W * 0.78)
            f = max(0.0, 1.0 - d) * 24
            edge = 1.0 - 0.30 * max(0.0, (math.hypot(x - W / 2, y - H / 2)
                                           / (W * 0.85) - 0.55))
            for dx in range(4):
                if x + dx < W:
                    px[x + dx, y] = (int((PURPLE[0] + f) * edge),
                                     int((PURPLE[1] + f * 0.4) * edge),
                                     int((PURPLE[2] + f * 1.4) * edge))
    return img


def frame(drw):
    for inset, col, wd in [(70, GOLD, 7), (88, GREEN, 3), (104, GOLD, 2)]:
        drw.rectangle([inset, inset, W - inset, H - inset],
                      outline=col, width=wd)
    for cx, cy in [(70, 70), (W - 70, 70), (70, H - 70), (W - 70, H - 70)]:
        s = 24
        drw.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s),
                     (cx - s, cy)], outline=GOLD, width=4)


def dot(drw, x, y, r, fill=GOLD):
    drw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def main():
    img = base()
    drw = ImageDraw.Draw(img)
    frame(drw)
    cx = W / 2

    # --- Head: a gold disc, featureless (the Seat, not a sitter) ----
    head_y, head_r = 560, 98
    drw.ellipse([cx - head_r, head_y - head_r, cx + head_r,
                 head_y + head_r], fill=GOLD)
    drw.ellipse([cx - 62, head_y - 62, cx + 62, head_y + 62],
                outline=GOLD_D, width=4)

    # --- Crown: band seated on the disc, five points ----------------
    band_y = head_y - head_r + 6        # 468: overlaps the disc's top
    drw.rectangle([cx - 104, band_y, cx + 104, band_y + 34], fill=GOLD)
    for k in range(-2, 3):
        x = cx + k * 52
        drw.polygon([(x - 25, band_y + 2), (x, band_y - 72),
                     (x + 25, band_y + 2)], fill=GOLD)
        dot(drw, x, band_y - 88, 11, fill=GREEN if k == 0 else GOLD)
    drw.line([cx - 126, band_y + 52, cx + 126, band_y + 52],
             fill=GREEN, width=5)

    # --- The multitude: torso of circles ----------------------------
    profile = [8, 9, 10, 10, 10, 9, 9, 8, 8, 8, 9, 9, 10, 11, 11]
    y0, dy, r, step = 726, 52, 20, 50
    for i, half in enumerate(profile):
        y = y0 + i * dy
        for k in range(-half, half + 1):
            dot(drw, cx + k * step, y, r)
    # neck dots
    dot(drw, cx, 672, r)

    # --- Arms of circles: shoulder out and up, forearm down ---------
    def arm(sign):
        pts = []
        sx, sy = cx + sign * 460, 700
        for t in range(5):                       # upper arm, rising out
            pts.append((sx + sign * 46 * t, sy - 36 * t))
        ex, ey = pts[-1]
        for t in range(1, 5):                    # forearm, descending
            pts.append((ex + sign * 34 * t, ey + 54 * t))
        return pts
    arm_r, arm_l = arm(-1), arm(1)
    for pts in (arm_r, arm_l):
        for (x, y) in pts:
            dot(drw, x, y, r)

    # --- Sword, held upright in the right hand (viewer's left) ------
    hx, hy = arm_r[-1]                            # the hand
    drw.line([hx, hy + 66, hx, hy - 300], fill=GOLD, width=13)   # blade core
    drw.polygon([(hx - 15, hy - 288), (hx + 15, hy - 288),
                 (hx, hy - 384)], fill=GOLD)                     # point
    drw.line([hx - 52, hy + 8, hx + 52, hy + 8], fill=GOLD,
             width=15)                                           # guard
    dot(drw, hx, hy + 52, 14, fill=GREEN)                         # pommel
    dot(drw, hx, hy, 24)                                         # hand

    # --- Crozier, held upright in the left hand (viewer's right) ----
    hx2, hy2 = arm_l[-1]
    top_y, bot_y = hy2 - 430, hy2 + 470
    drw.line([hx2, bot_y, hx2, top_y + 40], fill=GOLD, width=14)  # staff
    ccx, ccy = hx2 - 52, top_y + 52               # curl curls inward
    for t in range(30):                           # spiral of dots
        a = -math.pi / 2 + t / 29 * math.pi * 1.8
        rr = 56 * (1 - t / 40)
        dot(drw, ccx + rr * math.cos(a), ccy + rr * math.sin(a), 8)
    dot(drw, hx2, hy2, 24)                        # hand over the staff

    # --- The land: town and country under the ground line -----------
    gy = 1700
    drw.line([190, gy, W - 190, gy], fill=GOLD, width=5)
    tx = 250                                       # the walled town
    drw.rectangle([tx, gy - 118, tx + 420, gy], outline=GOLD, width=5)
    for bx, bw, bh in [(tx + 18, 88, 186), (tx + 148, 108, 236),
                       (tx + 296, 88, 166)]:
        drw.rectangle([bx, gy - bh, bx + bw, gy], outline=GOLD, width=4)
        drw.polygon([(bx - 8, gy - bh), (bx + bw / 2, gy - bh - 54),
                     (bx + bw + 8, gy - bh)], outline=GREEN, width=4)
    spx = tx + 202                                 # the church spire
    drw.polygon([(spx - 15, gy - 236), (spx, gy - 352),
                 (spx + 15, gy - 236)], outline=GOLD, width=4)
    dot(drw, spx, gy - 374, 9, fill=GREEN)
    for hx_, hw in [(1120, 250), (1360, 310), (1590, 200)]:   # hills
        drw.arc([hx_ - hw / 2, gy - 128, hx_ + hw / 2, gy + 58],
                start=180, end=360, fill=GREEN, width=5)
    trx = 1470                                     # one tree
    drw.line([trx, gy, trx, gy - 118], fill=GOLD, width=7)
    for rr, yy in [(62, gy - 158), (44, gy - 202)]:
        drw.ellipse([trx - rr, yy - rr, trx + rr, yy + rr],
                    outline=GREEN, width=5)
    for fx in range(1100, 1650, 92):               # furrows
        drw.line([fx, gy + 44, fx + 42, gy + 44], fill=GOLD_D, width=4)
    for x in range(250, W - 230, 52):              # the multitude at rest
        dot(drw, x, gy + 98, 7, fill=GOLD_D)

    img.save(OUT)
    print("PLATE STRUCK:", OUT, img.size)


if __name__ == "__main__":
    main()

# 93 -- Live, Love, and let Love, Live.
