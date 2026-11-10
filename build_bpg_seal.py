#!/usr/bin/env python3
# 93 — THE BLEATS PUBLISHING GROUP SEAL (founder's commission 2026-11-09).
# Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
# (Greek, -ARR, All Rights Reserved, Without Prejudice).
# MECHANISM: PIL seal press — circular rim legend set letter by letter
# on the arc, the founder's gold goat silhouette (his master mark,
# tint preserved) seated in a purple field, green pinstripes per the
# colour canon (purple · gold · green, ruled 2026-11-06).
# DOCTRINE carried on the seal itself: the Bleats motto in the rim
# (SAY IT · SPRAY IT · OWN IT), the Latin motto in the field
# (VOX CAPRI · VOX POPVLI / NVLLA VOX TACEBITVR), and the policy line
# — the TST Constitution is the house policy; the user above all.
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 2400
C = S // 2
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
GOAT = os.path.expanduser("~/workspace/goals/bleat-social-platform/files/logo/bleat-gold-silhouette.png")
OUT = os.path.expanduser("~/workspace/bookshop/BLEATS-PUBLISHING-GROUP-SEAL.png")

GOLD = (232, 190, 92)
GOLD_D = (150, 112, 40)
GREEN = (46, 204, 113)
CREAM = (243, 233, 210)
FIELD = (46, 13, 84)
BAND = (30, 7, 56)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
drw = ImageDraw.Draw(img)

# Field disc with a soft radial lightening toward the center.
yy, xx = np.mgrid[0:S, 0:S]
r = np.sqrt((xx - C) ** 2 + (yy - C) ** 2)
disc = np.zeros((S, S, 4), np.uint8)
shade = np.clip(1 - r / 1250, 0, 1) * 26
disc[..., 0] = FIELD[0] + shade
disc[..., 1] = FIELD[1] + shade * 0.4
disc[..., 2] = FIELD[2] + shade * 1.4
disc[..., 3] = np.where(r <= 1170, 255, 0)
img = Image.fromarray(disc, "RGBA")
drw = ImageDraw.Draw(img)

def ring(radius, col, w):
    drw.ellipse([C - radius, C - radius, C + radius, C + radius], outline=col, width=w)

ring(1170, GOLD, 10)
ring(1148, GOLD_D, 3)
ring(952, GREEN, 8)
ring(930, GOLD, 4)

# Rim band fill between the rings.
band = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bd = ImageDraw.Draw(band)
bd.ellipse([C - 1145, C - 1145, C + 1145, C + 1145], fill=BAND + (255,))
bd.ellipse([C - 955, C - 955, C + 955, C + 955], fill=(0, 0, 0, 0))
img.paste(Image.alpha_composite(img, band), (0, 0))
drw = ImageDraw.Draw(img)
ring(1170, GOLD, 10); ring(1148, GOLD_D, 3); ring(952, GREEN, 8); ring(930, GOLD, 4)

def arc_text(text, radius, mid_deg, font, fill, flip=False):
    widths = [drw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + (len(text) - 1) * 6
    span = total / radius
    a = math.radians(mid_deg) - span / 2 * (-1 if flip else 1)
    step_sign = -1 if flip else 1
    for ch, wch in zip(text, widths):
        da = (wch / 2) / radius * step_sign
        a += da
        x = C + radius * math.cos(a)
        y = C + radius * math.sin(a)
        rot = -(math.degrees(a) + 90) if not flip else -(math.degrees(a) - 90)
        tile = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((70, 70), ch, font=font, fill=fill, anchor="mm")
        tile = tile.rotate(rot, resample=Image.BICUBIC, center=(70, 70))
        img.paste(tile, (int(x - 70), int(y - 70)), tile)
        a += ((wch / 2) + 6) / radius * step_sign

frim = ImageFont.truetype(SERIFB, 104)
arc_text("BLEATS PUBLISHING GROUP", 1050, -90, frim, GOLD)
arc_text("SAY IT · SPRAY IT · OWN IT", 1050, 90, frim, GOLD, flip=True)
for ang in (0, 180):
    x = C + 1050 * math.cos(math.radians(ang)); y = C + 1050 * math.sin(math.radians(ang))
    drw.polygon([(x, y - 18), (x + 18, y), (x, y + 18), (x - 18, y)], fill=GREEN)

# The founder's gold goat, seated in the field.
goat = Image.open(GOAT).convert("RGBA")
goat.thumbnail((880, 880))
img.paste(goat, (C - goat.width // 2, 560), goat)
drw = ImageDraw.Draw(img)

def ctext(y, text, font, fill, spacing=0):
    if spacing:
        w = sum(drw.textlength(ch, font=font) + spacing for ch in text)
        x = C - w / 2
        for ch in text:
            drw.text((x, y), ch, font=font, fill=fill)
            x += drw.textlength(ch, font=font) + spacing
    else:
        drw.text((C, y), text, font=font, fill=fill, anchor="ma")

ctext(1470, "VOX CAPRI · VOX POPVLI", ImageFont.truetype(SERIFB, 66), GOLD, spacing=4)
drw.line([C - 330, 1590, C + 330, 1590], fill=GREEN, width=6)
ctext(1630, "NVLLA VOX TACEBITVR", ImageFont.truetype(SERIF, 58), CREAM, spacing=4)
ctext(1780, "THE TST CONSTITUTION IS POLICY", ImageFont.truetype(SERIFB, 54), GOLD, spacing=2)
ctext(1870, "THE USER ABOVE ALL", ImageFont.truetype(SERIFB, 62), GREEN, spacing=4)

img.save(OUT)
print("SEAL STRUCK:", OUT, img.size)
