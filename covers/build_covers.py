#!/usr/bin/env python3
# 93 — THE BOOKSHOP COVERS: hardcover leather, purple · gold · green.
# Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
# (Greek, -ARR, All Rights Reserved, Without Prejudice).
# MECHANISM: programmatic foil-and-leather press — PIL only. A deep
# purple leather field (noise grain, vignette), gold double tooling
# with a green pinstripe, debossed gold titles (shadow pass then foil
# pass), the TVRRIS VERITATIS seal seated on every front. Exact
# strings, no generative lettering — the press never garbles a title.
# DOCTRINE: the canonical colours are the mark's law (ruled
# 2026-11-06): purple the field, gold the word, green the living rule.
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1800, 2700
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SEAL = os.path.expanduser("~/workspace/templates/doctrine-logo.png")

PURPLE = (43, 12, 78)
PURPLE_D = (26, 6, 48)
GOLD = (232, 190, 92)
GOLD_D = (146, 108, 38)
GREEN = (46, 204, 113)
CREAM = (243, 233, 210)

def leather():
    rng = np.random.default_rng(93)
    grain = rng.normal(0, 7, (H // 3, W // 3)).astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    base[:] = PURPLE
    g = np.asarray(Image.fromarray(((grain - grain.min()) / (grain.ptp()) * 255).astype(np.uint8)).resize((W, H)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255.0
    base += (g[..., None] - 0.5) * 22
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    base *= (1 - 0.28 * np.clip(d - 0.55, 0, 1))[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

def wrap(drw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if drw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def foil_text(img, xy, text, font, fill=GOLD, anchor="mm", shadow=True):
    drw = ImageDraw.Draw(img)
    if shadow:
        drw.text((xy[0] + 3, xy[1] + 4), text, font=font, fill=(12, 3, 24), anchor=anchor)
    drw.text(xy, text, font=font, fill=fill, anchor=anchor)

def frame(img):
    drw = ImageDraw.Draw(img)
    for inset, col, wd in [(86, GOLD, 7), (104, GREEN, 3), (122, GOLD, 2)]:
        drw.rectangle([inset, inset, W - inset, H - inset], outline=col, width=wd)
    for cx, cy in [(86, 86), (W - 86, 86), (86, H - 86), (W - 86, H - 86)]:
        s = 26
        drw.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], outline=GOLD, width=4)

def front(slug, title, subtitle, author, year):
    img = leather(); frame(img)
    drw = ImageDraw.Draw(img)
    y = 330
    ft = ImageFont.truetype(SERIFB, 118)
    for line in wrap(drw, title, ft, W - 420):
        foil_text(img, (W // 2, y), line, ft); y += 148
    y += 26
    drw.line([W // 2 - 260, y, W // 2 + 260, y], fill=GREEN, width=5); y += 84
    if subtitle:
        fs = ImageFont.truetype(SERIF, 52)
        for line in wrap(drw, subtitle, fs, W - 460):
            foil_text(img, (W // 2, y), line, fs, fill=CREAM); y += 72
        y += 30
    fa = ImageFont.truetype(SERIFB, 76)
    foil_text(img, (W // 2, y), author, fa); y += 96
    fy = ImageFont.truetype(SERIF, 46)
    foil_text(img, (W // 2, y), f"· {year} ·", fy, fill=GREEN)
    seal = Image.open(SEAL).convert("RGB")
    # The seal's black surround is keyed out to the leather purple so the
    # medallion sits IN the cover, not on it as a pasted square.
    arr = np.asarray(seal).astype(np.int16)
    black = (arr.max(axis=2) < 28)
    arr[black] = PURPLE
    seal = Image.fromarray(arr.astype(np.uint8))
    seal.thumbnail((460, 460))
    img.paste(seal, (W // 2 - seal.width // 2, 1560))
    band_y = H - 330
    drw.rectangle([140, band_y, W - 140, band_y + 118], outline=GOLD, width=3)
    fb = ImageFont.truetype(SERIFB, 58)
    foil_text(img, (W // 2, band_y + 60), "TEACHER'S REVISION (MAGVS)", fb, fill=GREEN)
    img.save(os.path.join(OUT, f"FRONT-{slug}.png"))

def back(slug, title_short, synopsis, pull):
    img = leather(); frame(img)
    drw = ImageDraw.Draw(img)
    fh = ImageFont.truetype(SERIFB, 60)
    foil_text(img, (W // 2, 300), "THE TEACHER'S REVISION", fh)
    foil_text(img, (W // 2, 386), "(MAGVS)", fh, fill=GREEN)
    drw.line([W // 2 - 300, 470, W // 2 + 300, 470], fill=GOLD, width=4)
    fs = ImageFont.truetype(SERIF, 54)
    y = 620
    for line in wrap(drw, synopsis, fs, W - 420):
        foil_text(img, (W // 2, y), line, fs, fill=CREAM, shadow=False); y += 80
    y += 70
    drw.line([W // 2 - 200, y, W // 2 + 200, y], fill=GREEN, width=4); y += 110
    fp = ImageFont.truetype(SERIF, 50)
    for line in wrap(drw, pull, fp, W - 460):
        foil_text(img, (W // 2, y), line, fp); y += 74
    ff = ImageFont.truetype(SERIF, 36)
    y = H - 560
    for line in ["Flagpole of Claim and Coinage:", "Johnathan 'Qasparr' Monroe, ARR,",
                 "All Rights Reserved, Without Prejudice.",
                 "The revision and apparatus are the reviser's;",
                 "the master's text is public domain and stands",
                 "unaltered in substance."]:
        foil_text(img, (W // 2, y), line, ff, fill=CREAM, shadow=False); y += 52
    y += 26
    foil_text(img, (W // 2, y), "SPARROW · SOLE PROPRIETORSHIP", ImageFont.truetype(SERIFB, 40), fill=GREEN)
    img.save(os.path.join(OUT, f"BACK-{slug}.png"))

BOOKS = [
    ("douglass", "NARRATIVE OF THE LIFE OF FREDERICK DOUGLASS", "AN AMERICAN SLAVE — WRITTEN BY HIMSELF",
     "FREDERICK DOUGLASS", "1845",
     "Born enslaved and forbidden letters, he taught himself to read in secret — and wrote himself free. The 1845 Narrative is the testimony that shook a nation's conscience: a man seizing the pen that the law denied him, and proving with it that he was never property.",
     "“I would unite with anybody to do right and with nobody to do wrong.”"),
    ("huckfinn", "THE ADVENTURES OF HUCKLEBERRY FINN", "TOM SAWYER'S COMRADE",
     "MARK TWAIN", "1885",
     "A boy and a runaway on a raft, deciding right and wrong for themselves against the whole rigged conscience of the shore. Huck's choice — “All right, then, I'll go to hell” — is the sovereign act at the heart of American letters, printed here exactly as Twain wrote it, dialect and all, never sanitized.",
     "The great American novel of conscience, unbowdlerized."),
    ("sawyer", "THE ADVENTURES OF TOM SAWYER", "",
     "MARK TWAIN", "1876",
     "Whitewash fences, midnight graveyards, a cave, a funeral attended by the supposedly dead — Tom Sawyer is boyhood itself before the world gets its hooks in, and the seed of everything Twain would become. The original text, whole and unabridged, under the Teacher's Revision apparatus.",
     "“He had discovered a great law of human action.”"),
    ("oz", "THE WONDERFUL WIZARD OF OZ", "",
     "L. FRANK BAUM", "1900",
     "Baum's American fairy tale in its true book form — the silver shoes, the deadly poppy field, the Wizard unmasked as a humbug from Omaha. No film likeness, no ruby substitutions: the 1900 text as Baum wrote it, the founding myth of the road that leads home by going forward.",
     "The book, not the movie — silver shoes and all."),
    ("leviathan", "LEVIATHAN", "OR, THE MATTER, FORME AND POWER OF A COMMON-WEALTH, ECCLESIASTICALL AND CIVILL",
     "THOMAS HOBBES", "1651",
     "Hobbes's great engine of 1651: man in the state of nature, the covenant, and the mortal god to whom we owe our peace and defence. The Teacher's Revision (MAGVS) founded 2026 — the Commonwealth weighed chapter by chapter under Scientific Illuminism, its doctrine answered, never silently altered.",
     "“The condition of man… is a condition of war of everyone against everyone.”"),
]

for slug, title, sub, author, year, syn, pull in BOOKS:
    front(slug, title, sub, author, year)
    back(slug, title, syn, pull)
    print("struck:", slug)
print("ALL COVERS STRUCK")
