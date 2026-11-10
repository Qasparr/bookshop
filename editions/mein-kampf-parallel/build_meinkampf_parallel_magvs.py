#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"I know that men are won over less by the written word than by the
spoken." -- the author of the text under audit, in his Vorwort.
This edition answers the written word with the written record --
in both of the book's languages at once, facing each other, so
that no reader of either tongue ever has to take the other's word
for what the page says.

MEIN KAMPF, ERSTER BAND -- A PARALLEL CRITICAL EDITION (MAGVS):
the German text on the verso, a NEW house English translation on
the facing recto, paragraph for paragraph. Built in bricks under
../ARCHITECTURE.md, which is this builder's governing spec.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice) -- and see
the Reservation leaf in the front matter for the founder's
completed doctrine of that formula (2026-11-10): ARR stands in
this volume as an invocation of the Living Man's Reservation,
which is where the authority stands. The German text is public
domain; the Flagpole claims THE TRANSLATION, THE APPARATUS AND
THE AUDIT ONLY.
X day of November, Dies Martis, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   The German text of record is the sibling edition's
          secured source (Eher unabridged printing, 851.-855.
          Auflage 1943; SHA-256 a5de081b...cb19), extracted by the
          SIBLING BUILDER'S OWN loader, imported -- one source
          file, one loader, one text, so the German here cannot
          drift from the German there. The English is this house's
          own translation, one paragraph for one paragraph, from
          translations/en-<section>.txt. The chapter notes are
          CARRIED from the sibling builder's data, unchanged.
  PROCESS The alignment unit is the PARAGRAPH. The builder
          asserts the English and German counts equal per section
          and fails the build if they are not. Pages are composed
          in SPREADS -- verso (even folio) German, recto (odd
          folio) the English of the same units -- packed greedily
          by dry-run measurement (fpdf2 heights measured on a
          scratch document at the set measure) and closed before
          either side would overflow; each page's running head
          states its paragraph range. A section always opens on a
          fresh verso; a blank leaf is inserted when parity
          requires it and is printed as a blank, marked with the
          edition's rule and nothing else. A unit too long for one
          page is split at a sentence boundary into numbered
          sub-units on both sides, and the split is recorded in
          the build log; no Brick 1 unit required a split.
  OUTPUT  MEIN-KAMPF-PARALLEL-MAGVS-VOL1.pdf, cumulative with
          each brick. Brick 1: front matter (title page, the
          Reservation leaf, source leaf, elements leaf, Reviser's
          Preface for the parallel edition, the Translation
          Protocol in brief, contents); Widmung, Vorwort and
          Kapitel 1 in parallel, each followed by its translator's
          notes and its carried notes.
  TOLERANCE  Any step that would change a word of the German body
          fails the edition. Any translation choice that softens,
          omits, or improves the original fails the translation
          (ARCHITECTURE.md SSIV). What the desk cannot verify it
          marks UNVERIFIED; what the German cannot responsibly
          bear it marks UNCHARTED, with the locus.

  Two-pass build, as with the sibling editions: pass one
  measures, pass two prints the contents numbers. fpdf2
  discipline (house gotcha, AGENTS.md 2026-10-04): every
  multi_cell is called with new_x=XPos.LMARGIN, new_y=YPos.NEXT.
"""

import importlib.util
import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ----------------------------------------------------------------------
# Paths, the sibling loader, and constants
# ----------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "mein-kampf" / "build_meinkampf_magvs.py"
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "MEIN-KAMPF-PARALLEL-MAGVS-VOL1.pdf"
TRANS_DIR = HERE / "translations"

NOTO = "/usr/share/fonts/truetype/noto"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

_spec = importlib.util.spec_from_file_location("sibling_builder",
                                               SIBLING)
sib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sib)   # data + loader only; main() is guarded

FLAGPOLE = ("Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, "
            "ARR, All Rights Reserved, Without Prejudice. Right of claim "
            "hereby reserved and coined under the authority of the "
            "Living Man.")
FOUNDER_FORM = ("in the authority of the Living Man, standing in his "
                "Reservation of rights, without prejudice")
THELEMIC_DATE = ("X day of November, Dies Martis, Sol in Scorpio, "
                 "Anno V:xii e.n. (2026 e.v.)")
FOOTER = ("— {n} of {m} — | All Rights Reserved, Without Prejudice | "
          "Flagpole of Claim and Coinage reserved")

BODY_SIZE, BODY_H, BODY_SPACE = 10.5, 5.8, 2.2
HEAD_Y = 12.5            # running head baseline block
CONTENT_TOP = 26.0       # first baseline area on body pages
PAGE_BOTTOM = 259.0      # Letter 279.4 - bottom margin ~20

# Brick 1 sections, in the book's own order. head_de/head_en are the
# spread headings; run_de/run_en the running-head section names.
BRICK1 = [
    ("widmung", "WIDMUNG", "THE DEDICATION", "WIDMUNG", "DEDICATION"),
    ("vorwort", "VORWORT", "FOREWORD", "VORWORT", "FOREWORD"),
    ("kap1", "1. KAPITEL — IM ELTERNHAUS", "CHAPTER 1 — IN THE "
     "PARENTS' HOME", "1. KAPITEL", "CHAPTER 1"),
    ("kap2", "2. KAPITEL — WIENER LEHR- UND LEIDENSJAHRE",
     "CHAPTER 2 — VIENNA YEARS OF LEARNING AND SUFFERING",
     "2. KAPITEL", "CHAPTER 2"),
]


def load_translation(key):
    """Parse translations/en-<key>.txt ([key:n] blocks) into an
    ordered list of English paragraphs, one for one with the
    German loader's list for the same section."""
    text = (TRANS_DIR / f"en-{key}.txt").read_text(encoding="utf-8")
    parts = re.split(r"^\[[a-z0-9]+:\d+\]\s*$", text, flags=re.M)
    paras = [re.sub(r"\s+", " ", p).strip() for p in parts]
    paras = [p for p in paras if p]
    heads = re.findall(r"^\[([a-z0-9]+):(\d+)\]\s*$", text, flags=re.M)
    assert [k for k, _n in heads] == [key] * len(paras), \
        f"translation file en-{key}.txt: block keys diverge"
    assert [int(n) for _k, n in heads] == list(range(len(paras))), \
        f"translation file en-{key}.txt: block order is not 0..n-1"
    return paras


# ----------------------------------------------------------------------
# Translator's notes (marked [TN]) -- for loci and loaded terms of
# Brick 1, under the Protocol (ARCHITECTURE.md SSIV.4 and SSIV.6).
# Keyed: (section, unit index 0-based) -> note text.
# ----------------------------------------------------------------------
TN = {
    ("widmung", 0):
        "Volk (here ihres Volkes, 'of their people'): the word's "
        "range — a people as nation, as ethnic body, as the "
        "collective subject of history — is held by no single "
        "English word. 'People' is the rendering chosen here and "
        "held throughout the edition; where the text narrows Volk "
        "toward blood and descent, a note names the German rather "
        "than bending the English. [First occurrence.]",
    ("widmung", 4):
        "Bewegung ('movement'): rendered 'movement' throughout. "
        "In this text the word is never a mere motion: it names "
        "the National Socialist movement as one collective actor, "
        "and — as here, 'our movement' — carries the loyalty of a "
        "confession. [First occurrence.]",
    ("widmung", 5):
        "The dateline as printed in the witness reads 'lö.Oktober "
        "1924' — an OCR misread of '16. Oktober 1924', declared in "
        "the edition's Apparatus. The English translates the "
        "evident sense; the German page prints the locus as found.",
    ("kap1", 1):
        "This sentence stands in the printed book in letterspaced "
        "emphasis; the OCR witness merges it "
        "('GleichesBlutgehörtineingemeinsamesReich'). The German "
        "page prints the locus as found; the English translates "
        "the evident reading: Gleiches Blut gehört in ein "
        "gemeinsames Reich.",
    ("kap1", 8):
        "Three single-letter OCR misreads stand in this paragraph "
        "as printed: 'im Lreien' for im Freien ('in the open'), "
        "'keinen Lall' for keinen Fall ('in no case'), 'in Lorm' "
        "for in Form ('in the form of'). The English translates "
        "the evident sense in each place; the German page is not "
        "silently emended.",
    ("kap1", 18):
        "Two single-letter misreads as printed: 'Lormulare' for "
        "Formulare ('forms') and 'Lechtboden' for Fechtboden "
        "('fencing-ground'). Translated per evident sense.",
    ("kap1", 25):
        "Printed merged in the witness ('ichwurdeNationalist') — "
        "a letterspaced emphasis line defeated by the OCR. Read: "
        "ich wurde Nationalist.",
    ("kap1", 27):
        "One sentence in the original — ich lernte Geschichte "
        "ihrem Sinne nach verstehen und begreifen — stands in the "
        "witness merged and split across two paragraph blocks "
        "('…verstehenundbe' / 'greifen.'). The English keeps the "
        "same break, so the facing pages stay in step; read the "
        "two units as one sentence.",
    ("kap1", 30):
        "Two loci as printed: 'Nationalitäten-staa t' (a word the "
        "OCR broke across a space) and 'das heben und Wachsen' "
        "for das Leben und Wachsen ('the life and growth'). "
        "Translated per evident sense.",
    ("kap1", 33):
        "The three strata stand in the printed book in "
        "letterspaced emphasis; the witness merges them "
        "('dieKämpfer d i e L a u e n dieVerräter'). Read: die "
        "Kämpfer, die Lauen, die Verräter.",
    ("kap1", 36):
        "Printed 'mit fünfzehn fahren': an OCR misread of mit "
        "fünfzehn Jahren ('at fifteen years').",
    ("kap1", 39):
        "völkisch: the adjective of Volk in its narrowed period "
        "sense — not 'national' and not merely 'popular', but 'of "
        "the Volk' as a blood-and-descent body, set here against "
        "'dynastic' in the same breath. Rendered 'folkish' "
        "throughout the edition, deliberately unlovely: 'national' "
        "would launder the narrowing, 'racial' would overshoot "
        "it. The ruling is collected in the Glossary. [First "
        "occurrence.]",
    ("kap1", 43):
        "Printed merged ('Wesentlichesbehalten, "
        "Unwesentlichesvergessen') — letterspaced emphasis "
        "defeated by the OCR. Read: Wesentliches behalten, "
        "Unwesentliches vergessen.",
    ("kap1", 51):
        "This whole sentence stands merged in the witness, the "
        "letterspaced emphasis of the printed book defeated "
        "across five lines of OCR. The German page prints it as "
        "found; the English translates the evident reading.",
    ("kap2", 12):
        "Marxismus and Judentum named together, as the chapter's "
        "programme. Judentum is rendered 'Jewry' throughout the "
        "edition — the collective noun the German carries — "
        "never softened to 'the Jews' where the abstraction is "
        "the author's own. [First occurrence.]",
    ("kap2", 19):
        "Weltanschauung: rendered 'world-view' throughout — the "
        "author's own keystone term for a total doctrine held as "
        "faith; 'ideology' would modernise it past recognition. "
        "[First occurrence.]",
    ("kap2", 49):
        "Printed 'Liier rächt sich': an OCR misread of Hier "
        "rächt sich.",
    ("kap2", 95):
        "Printed 'ätzende Lrechheit': an OCR misread of ätzende "
        "Frechheit ('corroding impudence').",
    ("kap2", 102):
        "Printed 'Die hebe bürgerliche Mitwelt': an OCR misread "
        "of Die liebe bürgerliche Mitwelt.",
    ("kap2", 125):
        "Printed 'zwei wichtigsten Tragen': an OCR misread of "
        "zwei wichtigsten Fragen.",
    ("kap2", 155):
        "Printed 'fe mehr ich mich': an OCR misread of je mehr "
        "ich mich.",
    ("kap2", 162):
        "Printed 'die Lurcht vor dem wilden Köter': an OCR "
        "misread of die Furcht.",
    ("kap2", 175):
        "The F-to-L misread class runs through this stretch of "
        "the chapter: here 'in den Lormen' for in den Formen; "
        "then Forderungen as 'Lorderungen' (¶176, ¶179), Feinde "
        "as 'Leinde' (¶177), Frage as 'Lrage' (¶182, ¶185). The "
        "German page prints every instance as found; the "
        "English translates the evident readings.",
    ("kap2", 202):
        "A single letter stands as its own unit in the witness "
        "— a printed divider mark of the book's internal "
        "sectioning, carried as found.",
    ("kap2", 246):
        "Printed 'innerpolitischen Febens' and 'erster Finie': "
        "OCR misreads of innerpolitischen Lebens and erster "
        "Linie.",
    ("kap2", 253):
        "Printed 'süßlichen Fobeshymnen': an OCR misread of "
        "süßlichen Lobeshymnen ('sugary praise-hymns').",
    ("kap2", 254):
        "Printed 'Dr. Karl Fueger': an OCR misread of Dr. Karl "
        "Lueger, the Christian-Social mayor of Vienna. The "
        "German page prints the name as found; the English "
        "restores the evident reading, the locus flagged here "
        "and in the Apparatus of OCR Loci — a name is a fact, "
        "and the fact is Lueger.",
    ("kap2", 332):
        "Printed 'die Lolgen', 'Die Lrage', 'letzten Lorm': OCR "
        "misreads of die Folgen, Die Frage, letzten Form.",
    ("kap2", 336):
        "Printed 'Kenntnis der fudenfrage': an OCR misread of "
        "Kenntnis der Judenfrage.",
    ("kap2", 342):
        "The witness reads 'das ewig nur auf dieser lebt' — "
        "the noun is wanting (the printed book reads auf dieser "
        "Erde lebt). The English supplies 'earth' per the "
        "evident sense; the gap is flagged here, not repaired "
        "on the German page.",
    ("kap2", 345):
        "Rasse: rendered 'race' throughout the edition. The "
        "word is the load-bearing term of the book's doctrine "
        "and is neither narrowed to 'breed' nor widened to "
        "'species'; its period scientific pretension is part of "
        "what the Tower Audit weighs. [First occurrence.]",
}


# ----------------------------------------------------------------------
# Page furniture (the sibling pattern)
# ----------------------------------------------------------------------
def para(pdf, text, size=10.5, height=5.8, align="J", space_after=2.2,
         font="noto", style=""):
    pdf.set_font(font, style, size)
    pdf.multi_cell(0, height, text, align=align, markdown=True,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(space_after)


def centered(pdf, text, font, style, size, height, space_after=0.0,
             color=None):
    if color:
        pdf.set_text_color(*color)
    pdf.set_font(font, style, size)
    pdf.multi_cell(0, height, text, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if color:
        pdf.set_text_color(0, 0, 0)
    if space_after:
        pdf.ln(space_after)


def rule(pdf, width_mm=60):
    x = (pdf.w - width_mm) / 2
    pdf.set_draw_color(150, 120, 40)
    pdf.set_line_width(0.4)
    pdf.line(x, pdf.get_y(), x + width_mm, pdf.get_y())
    pdf.ln(4)


class Book(FPDF):
    folio_total = None

    def footer(self):
        self.set_y(-14)
        self.set_font("dejavu", "", 7.5)
        self.set_text_color(90, 90, 90)
        total = self.folio_total if self.folio_total else "{nb}"
        self.cell(0, 8, FOOTER.format(n=self.page_no(), m=total),
                  align="C")


def new_book():
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    for family, fname in [("noto", "NotoSerif")]:
        pdf.add_font(family, "", f"{NOTO}/{fname}-Regular.ttf")
        pdf.add_font(family, "B", f"{NOTO}/{fname}-Bold.ttf")
        pdf.add_font(family, "I", f"{NOTO}/{fname}-Italic.ttf")
        pdf.add_font(family, "BI", f"{NOTO}/{fname}-BoldItalic.ttf")
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")
    return pdf


# ----------------------------------------------------------------------
# Measurement: a scratch document at the same measure. Heights are
# the composer's only currency; nothing is packed by guess.
# ----------------------------------------------------------------------
_scratch = None


def measure(text):
    global _scratch
    if _scratch is None:
        _scratch = new_book()
        _scratch.add_page()
    pdf = _scratch
    pdf.set_font("noto", "", BODY_SIZE)
    page0, y0 = pdf.page_no(), pdf.get_y()
    pdf.multi_cell(0, BODY_H, text, align="J",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    usable = pdf.h - 20 - 20          # top margin + bottom margin
    height = (pdf.page_no() - page0) * usable + (pdf.get_y() - y0)
    if pdf.get_y() > pdf.h - 40:      # keep the scratch page usable
        pdf.add_page()
    return height + BODY_SPACE


SENTENCE = re.compile(r"(?<=[.!?…])\s+(?=[„\"'»A-ZÄÖÜ0-9])")


def split_unit(de, en, capacity, log, label):
    """Split an over-long unit at sentence boundaries into paired
    sub-units (ARCHITECTURE SSIII.1): the German sentences are
    grouped greedily under the capacity; the English is cut at the
    same sentence count where the counts agree, else at the
    nearest proportional character boundary at a sentence edge.
    The split is a typesetting act; it is logged, and touches no
    word."""
    de_s = SENTENCE.split(de)
    en_s = SENTENCE.split(en)
    groups, cur = [], []
    for s in de_s:
        trial = " ".join(cur + [s])
        if cur and measure(trial) > capacity:
            groups.append(cur)
            cur = [s]
        else:
            cur.append(s)
    if cur:
        groups.append(cur)
    if len(en_s) == len(de_s):
        en_groups, i = [], 0
        for g in groups:
            en_groups.append(en_s[i:i + len(g)])
            i += len(g)
    else:
        en_groups, i, total = [], 0, len(en)
        used_de = 0
        for g in groups[:-1]:
            used_de += len(" ".join(g))
            target = total * used_de / max(len(de), 1)
            acc = 0
            j = i
            while j < len(en_s) and acc < target:
                acc += len(en_s[j]) + 1
                j += 1
            en_groups.append(en_s[i:j])
            i = j
        en_groups.append(en_s[i:])
    out = [(" ".join(g), " ".join(e)) for g, e in zip(groups,
                                                     en_groups)]
    assert all(measure(a) <= capacity and measure(b) <= capacity
               for a, b in out), f"split of {label} still overflows"
    log.append(f"SPLIT {label}: 1 unit -> {len(out)} sub-units")
    return out


def plan_spreads(key, de_list, en_list, log):
    """Greedy spread packing (ARCHITECTURE SSIII.2): a spread is a
    list of unit indices; both pages of a spread always carry the
    identical range. Returns [(indices, [sub-paras or None...])] --
    in Brick 1 no unit splits, so sub-paras are the units
    themselves; the split path rewrites the unit stream first."""
    capacity_first = PAGE_BOTTOM - CONTENT_TOP - 30.0   # title block
    capacity = PAGE_BOTTOM - CONTENT_TOP
    units = list(zip(de_list, en_list))
    # Pre-split any unit that cannot stand alone on a fresh page.
    stream = []
    for i, (de, en) in enumerate(units):
        if measure(de) > capacity or measure(en) > capacity:
            for sub in split_unit(de, en, capacity, log,
                                  f"{key} ¶{i + 1}"):
                stream.append((i, sub))
        else:
            stream.append((i, (de, en)))
    spreads, cur, h_de, h_en = [], [], 0.0, 0.0
    for idx, (de, en) in stream:
        cap = capacity_first if not spreads and not cur else capacity
        hd, he = measure(de), measure(en)
        if cur and (h_de + hd > cap or h_en + he > cap):
            spreads.append(cur)
            cur, h_de, h_en = [], 0.0, 0.0
            cap = capacity
            assert hd <= cap and he <= cap, \
                f"{key} ¶{idx + 1} exceeds a fresh page"
        cur.append((idx, de, en))
        h_de += hd
        h_en += he
    if cur:
        spreads.append(cur)
    return spreads


# ----------------------------------------------------------------------
# Front matter (the parallel edition's own)
# ----------------------------------------------------------------------
def title_page(pdf):
    pdf.add_page()
    pdf.image(str(LOGO), x=(pdf.w - 36) / 2, w=36)
    pdf.ln(6)
    centered(pdf, "ADOLF HITLER", "dejavu", "B", 25, 11, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 5)
    rule(pdf)
    centered(pdf, "MEIN KAMPF", "dejavu", "B", 19, 9)
    centered(pdf, "ERSTER BAND — EINE ABRECHNUNG", "dejavu", "B",
             14.5, 8, 2)
    centered(pdf, "Volume One (1925) — the German text and a new "
                  "English translation, on facing pages",
             "noto", "I", 11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A PARALLEL CRITICAL EDITION (MAGVS)",
             "dejavu", "B", 13.5, 8, 2)
    centered(pdf, "A Teacher's Revision — an audit, not an "
                  "endorsement", "noto", "BI", 11.5, 6, 5)
    centered(pdf, "The translation, the apparatus and the Tower "
                  "Audit are by", "noto", "", 10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship attributed exclusively to Johnathan "
                  "'Qasparr' Monroe, " + FOUNDER_FORM,
             "noto", "", 9.5, 5, 4)
    centered(pdf, "Published by Bleats Publishing Group",
             "dejavu", "B", 11, 6, 1)
    centered(pdf, "SPARROW (Sole Proprietorship) — Johnathan "
                  "'Qasparr' Monroe, Proprietor, legal publisher "
                  "of record", "noto", "", 9.5, 5, 4)
    centered(pdf, THELEMIC_DATE, "noto", "", 10.5, 6, 1)
    centered(pdf, "Classification: Enterprise • Educational • "
                  "Research & Development", "noto", "", 10, 6)
    centered(pdf, "Method of Science, Aim of Religion", "noto", "I",
             10, 6, 6)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "The German text of Mein Kampf is PUBLIC DOMAIN "
              "(first published 1925; the author died 1945). It is "
              "printed here whole and unaltered on the verso. The "
              "English on the recto is this house's own translation, "
              "made for this edition from that German; no other "
              "translation was consulted or used. The Flagpole above "
              "claims THE TRANSLATION, THE APPARATUS AND THE AUDIT "
              "ONLY.",
         size=9.5, height=5, align="C", space_after=0)


def reservation_leaf(pdf):
    pdf.add_page()
    centered(pdf, "THE RESERVATION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The form of the claim in this edition",
             "noto", "I", 10.5, 6, 6)
    para(pdf, "The founder ruled, on the day this edition was "
              "commissioned (2026-11-10): \u201cNo ARR. In authority "
              "of the Living Man, standing in his Reservation.\u201d "
              "And, completing the doctrine in the same breath: "
              "\u201cStated like the cover with the Greek proof. "
              "ARR just invokes it.\u201d This leaf carries that "
              "doctrine into this volume, in terms.")
    para(pdf, "The doctrine is this. The letters \u201cARR\u201d do "
              "not constitute the right, do not grant it, and are "
              "not its source. Stated — as they stand stated on the "
              "cover of Black's Law 2nd Edition — Teacher's "
              "Revision (MAGVS), with the Greek proof — they "
              "INVOKE the Living Man's Reservation of rights. The "
              "authority stands where it has always stood: in the "
              "Living Man, standing in his Reservation. Accordingly, "
              "wherever in this volume the ARR formula stands — in "
              "the Flagpole, in the footers, in the colophon — it "
              "stands as that invocation, and the authorship of "
              "this edition's work is stated in the founder's form: "
              + FOUNDER_FORM + ".")
    para(pdf, "The bound of the doctrine, stated as plainly: the "
              "cover statement of the Black's is the canonical form "
              "of the invocation, and that volume stands exactly as "
              "issued — untouched, unamended, and unreopened by "
              "anything printed here. The same holds for the "
              "sibling Mein Kampf Critical Edition (MAGVS), which "
              "this parallel edition extends, and for every other "
              "issued work of the house: their forms are their own, "
              "as issued. This leaf declares the doctrine for this "
              "new edition only; it alters no other book.")


def source_leaf(pdf):
    pdf.add_page()
    centered(pdf, "THE SOURCE OF THIS EDITION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Named, hashed, and declared before it is built on",
             "noto", "I", 10.5, 6, 6)
    para(pdf, "The German text printed in this volume is the text of "
              "the Internet Archive item \u201cMeinKampfBand1-Eine"
              "Abrechnung\u201d — the OCR full text of the Eher "
              "unabridged printing of Mein Kampf, 851.–855. Auflage, "
              "1943 — as secured and hashed in the sibling edition's "
              "Source Ledger (SHA-256 a5de081b761e16a03aa3ec2465a51"
              "4c6e2d5e22 439016a2222bb420d30cb19) and cross-checked "
              "against a second Archive witness on every test "
              "passage. It is extracted for this edition by the "
              "sibling builder's own loader, imported, not "
              "re-implemented: one source file, one loader, one "
              "text, so the German on these versos cannot drift "
              "from the German of the Critical Edition. Band 1 was "
              "first published on 18 July 1925; later printings "
              "carry small authorial corrections, and the "
              "Schlusswort was written in November 1926 and is not "
              "part of the 1925 first edition. A first-edition "
              "facsimile collation is UNCHARTED future work.")
    para(pdf, "The OCR state is declared, as in the sibling edition: "
              "ß and umlauts intact; doubled spaces collapsed in "
              "typesetting; a small residue of merged words (where "
              "the original sets emphasis in letterspaced type) and "
              "rare single-letter misreads are printed as found and "
              "flagged in the translator's notes — never silently "
              "emended, on either page. The body's orthography is "
              "the 1943 printing's (daß, muß, and the rest), "
              "unmodernized.")
    para(pdf, "How to read this edition: every opening carries the "
              "same paragraphs in both tongues — German on the "
              "verso (the even page), the house's English on the "
              "facing recto. The running head of each page states "
              "the paragraph range it carries (\u00b6 a–b), so the "
              "facing claim can be checked on any opening in one "
              "glance: that checkability is the edition's method. "
              "After each section stand its translator's notes, "
              "then the NOTES AND CORRELATIONS carried from the "
              "Critical Edition. The TOWER AUDIT, carried entire, "
              "closes the volume in its final brick.")


def elements_page(pdf):
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete German text of Band 1 from the "
                   "secured, hashed source named on the Source "
                   "leaf; the carried apparatus of the Critical "
                   "Edition (its chapter notes and its Tower "
                   "Audit); and this edition's own translation, "
                   "made under the Protocol."),
        ("PROCESSES", "Paragraph-aligned facing composition: the "
                      "German on the verso, the English on the "
                      "recto, the same units in the same order, "
                      "the counts asserted equal at build. The "
                      "translation is made from the German alone; "
                      "the in-copyright standard translation is "
                      "never consulted. OCR loci are printed as "
                      "found and flagged. Judgment is confined to "
                      "the preface, the notes, and the Audit."),
        ("OUTPUTS", "This volume, cumulative with each brick: "
                    "front matter; Widmung, Vorwort, Kapitel 1–12 "
                    "and the Schlusswort in parallel; the Tower "
                    "Audit, the Glossary of Translation Rulings, "
                    "the Apparatus of OCR Loci, the Title "
                    "Register, the Table of Authorities, and the "
                    "Colophon in the final brick."),
        ("TOLERANCES", "Zero for the German body: any process "
                       "that would change a German word fails the "
                       "edition. The translation fails if it "
                       "softens, omits, or improves a word of the "
                       "original. Any audit tier asserted without "
                       "its reasoning fails the item. What cannot "
                       "be verified is marked UNVERIFIED; what is "
                       "open, UNCHARTED; nothing is invented."),
    ]
    for head, body in items:
        pdf.set_font("dejavu", "B", 11)
        pdf.multi_cell(0, 6, head, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        para(pdf, body, space_after=4)
    para(pdf, "Tiers used in the Audit: PROVEN (established by "
              "documents or records independent of the author), "
              "SUPPORTED (the weight of the record favors it), "
              "CONTESTED (the record divides or cuts both ways), "
              "FALSE (contradicted by the record), UNVERIFIED (no "
              "evidence independent of the author's word). "
              "Translator's notes are marked [TN]; apparatus "
              "labels: ATTESTED, DERIVED, CONSTRUCTED, UNCHARTED, "
              "as in the sibling editions.",
         size=10, space_after=0)


PREFACE_PARALLEL = [
    "The Critical Edition of this text, issued by this house, "
    "printed the German alone and answered it in English — in a "
    "preface, in notes after every chapter, and in a Tower Audit "
    "that tiers the volume's claims against the historical record. "
    "That design had one dependence built into it: every rendering "
    "quoted inside the English apparatus was the house's own, and "
    "a reader who could not read German had to take those "
    "renderings on trust. This edition removes the trust. The "
    "German stands on the verso; a complete English translation, "
    "made for this edition, stands on the recto — the same "
    "paragraphs, in the same order, under a running head that "
    "states the range each page carries. Any reader can now check "
    "any sentence against its original in one glance. Checkability "
    "is not this edition's ornament; it is its method — the "
    "Zero-Point discipline made typographic.",

    "The translation is literal, and it is unsparing. It renders "
    "what the text says — its claims, its slurs, its racial "
    "doctrine, its threats — without softening, omission, "
    "euphemism, or editorializing. To soften this text would be "
    "to falsify the evidence; to omit would be to destroy it. It "
    "was made directly from the German text of record named on "
    "the Source leaf. The standard English translation, Ralph "
    "Manheim's of 1943, is under copyright; it was never "
    "consulted, copied, or paraphrased — not for a word, not for "
    "a cadence, not to check a difficulty. Difficulties were "
    "resolved from the German and from the translator's judgment, "
    "and where judgment is uncertain, a translator's note "
    "([TN]) says so. Where the witness itself is corrupt — the "
    "OCR's merged emphasis lines and single-letter misreads, "
    "declared on the Source leaf — the English translates the "
    "evident sense and a [TN] names the locus exactly as "
    "printed, on both pages, so no reader mistakes the scan's "
    "faults for the author's words, or the author's words for "
    "the scan's.",

    "Judgment, in this edition, keeps its appointed place. The "
    "founder's law governs the whole: JUDGMENT COMES LAST, NEVER "
    "FIRST. The Reviser's Preface of the Critical Edition states "
    "the condemnation once, plainly — the doctrine of this text "
    "condemned as false in its science, falsified in its history, "
    "and criminal in its program and its sequel — and that "
    "preface stands as issued in its own volume. Here, the "
    "answering is carried, not repeated: the chapter notes of the "
    "Critical Edition are printed after each section, unchanged "
    "and attributed, and its Tower Audit closes this volume in "
    "the final brick. The translation itself carries no "
    "editorializing, because a translation that argues cannot be "
    "checked; this one can be, line by line, which is the "
    "stronger answer.",

    "Two pages, two disciplines. The German page keeps the 1943 "
    "printing entire: its orthography (daß, muß), its emphasis, "
    "its scars. The English page uses modern English spelling and "
    "carries German sentence architecture as far as English bears "
    "it; where a German period must be broken for English sense, "
    "it is broken at a clause joint, silently — a punctuation "
    "act, not a wording act. Contested and loaded terms — Volk, "
    "völkisch, and their fellows — receive a translator's note at "
    "first occurrence, stating the German word, its range, the "
    "rendering chosen, and the reason; the rulings are collected "
    "in the Glossary at the back, so the consistency of the "
    "translation can itself be audited.",

    "This volume contains the front matter and the opening "
    "of the book: the Widmung, the Vorwort, the first chapter, "
    "In the Parents' Home, and the second, Vienna Years of "
    "Learning and Suffering. The chapters follow, brick "
    "by brick, in the book's own order; the volume closes with "
    "the Schlusswort in parallel, the Tower Audit entire, the "
    "Glossary, the Apparatus of OCR Loci, the Title Register, "
    "the Table of Authorities, and the Colophon. The German text "
    "is public domain and is claimed by no one in this volume. "
    "The translation, the apparatus, and the audit are the "
    "house's work, and their authorship is stated on the title "
    "page in the founder's form: " + FOUNDER_FORM + ".",
]


def preface_page(pdf):
    pdf.add_page()
    centered(pdf, "REVISER'S PREFACE", "dejavu", "B", 14, 9, 2)
    centered(pdf, "To the Parallel Edition — by Johnathan "
                  "'Qasparr' Monroe, Reviser",
             "noto", "I", 10.5, 6, 6)
    for p in PREFACE_PARALLEL:
        para(pdf, p)


def protocol_page(pdf):
    pdf.add_page()
    centered(pdf, "THE TRANSLATION PROTOCOL IN BRIEF",
             "dejavu", "B", 13, 8, 2)
    centered(pdf, "The full Protocol stands in the edition's "
                  "Architecture", "noto", "I", 10.5, 6, 6)
    for line in [
        "1. OWN WORK ONLY. The translation is made by this desk "
        "directly from the German text of record. The standard "
        "English translation by Ralph Manheim (1943) is under "
        "copyright: never consulted, copied, or paraphrased — "
        "not for a word, not for a cadence, not to check a "
        "difficulty.",
        "2. FIDELITY IS LITERAL AND UNSPARING. The translation "
        "renders what the text says — claims, slurs, racial "
        "doctrine, threats — without softening, omission, "
        "euphemism, or editorializing inside the translation "
        "itself. Judgment lives in the preface, the notes, and "
        "the Tower Audit. Judgment comes last, never first.",
        "3. SYNTAX. German sentence architecture is carried into "
        "English as far as English bears it; a period broken for "
        "English sense is broken at a clause joint, silently. "
        "The German page keeps the 1943 orthography; the English "
        "page uses modern English spelling.",
        "4. LOADED TERMS receive a translator's note ([TN]) at "
        "first occurrence — the German word, its literal range, "
        "the rendering chosen, and the reason — and the chosen "
        "rendering is then held consistently; the Glossary "
        "collects the rulings.",
        "5. NAMES AND FACTS are rendered as the German gives "
        "them. Where the German states a falsehood, the "
        "translation states the same falsehood; correction is "
        "the Audit's office, exercised there, with receipts.",
        "6. OCR HONESTY. The German is printed as found, "
        "including the witness's declared loci. A corrupt locus "
        "is translated per its evident sense and flagged with a "
        "[TN] naming it as printed — never a silent fix, on "
        "either page.",
    ]:
        para(pdf, line, size=10.5, space_after=1.6)


def contents_page(pdf, toc):
    pdf.add_page()
    centered(pdf, "CONTENTS", "dejavu", "B", 14, 9, 8)
    entries = [("The Reservation — The Form of the Claim",
                toc.get("reservation")),
               ("The Source of This Edition", toc.get("source")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface to the Parallel Edition",
                toc.get("preface")),
               ("The Translation Protocol in Brief",
                toc.get("protocol"))]
    labels = {"widmung": ("Widmung — The Dedication",
                          "Widmung"),
              "vorwort": ("Vorwort — Foreword", "Vorwort"),
              "kap1": ("1. Kapitel — Im Elternhaus / Chapter 1 — "
                       "In the Parents' Home", "Kapitel 1"),
              "kap2": ("2. Kapitel — Wiener Lehr- und "
                       "Leidensjahre / Chapter 2 — Vienna Years "
                       "of Learning and Suffering", "Kapitel 2")}
    for key, _hd, _he, _rd, _re in BRICK1:
        name, short = labels[key]
        entries.append((f"{name} — in parallel", toc.get(key)))
        entries.append((f"Translator's Notes and Carried Notes — "
                        f"{short}", toc.get(key + ":notes")))
    for name, page in entries:
        pdf.set_font("noto", "", 10.5)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 6.4, label, new_x=XPos.LMARGIN,
                       new_y=YPos.NEXT)
    pdf.ln(4)
    para(pdf, "Kapitel 3–12, the Schlusswort in parallel, the "
              "Tower Audit entire, the Glossary of Translation "
              "Rulings, the Apparatus of OCR Loci, the Title "
              "Register, the Table of Authorities, and the "
              "Colophon follow in the bricks after this one; this "
              "contents grows with the volume.",
         size=10, space_after=0)


# ----------------------------------------------------------------------
# The parallel body: spreads and notes
# ----------------------------------------------------------------------
def running_head(pdf, text):
    pdf.set_y(HEAD_Y)
    pdf.set_font("dejavu", "", 8)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(0, 4.5, text, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    y = pdf.get_y() + 1.5
    pdf.set_draw_color(150, 120, 40)
    pdf.set_line_width(0.3)
    pdf.line(22, y, pdf.w - 22, y)
    pdf.set_y(CONTENT_TOP)


def blank_leaf(pdf):
    """Parity leaf: printed as a blank, marked with the edition's
    rule and nothing else (ARCHITECTURE SSIII.2)."""
    pdf.add_page()
    pdf.set_y(pdf.h / 2 - 2)
    rule(pdf, 60)


def print_section(pdf, key, head_de, head_en, run_de, run_en,
                  spreads, toc, log):
    toc[key] = None
    for si, spread in enumerate(spreads):
        # Verso first: the next page must be EVEN.
        if (pdf.pages_count + 1) % 2 == 1:
            blank_leaf(pdf)
            log.append(f"{key}: parity blank before spread "
                       f"{si + 1} (folio {pdf.pages_count})")
        a, b = spread[0][0] + 1, spread[-1][0] + 1
        rng = f"\u00b6 {a}" if a == b else f"\u00b6 {a}–{b}"
        pdf.add_page()
        if toc[key] is None:
            toc[key] = pdf.page_no()
        running_head(pdf, f"DEUTSCH — {run_de}, {rng}")
        if si == 0:
            centered(pdf, head_de, "dejavu", "B", 13.5, 8, 3)
        for _idx, de, _en in spread:
            para(pdf, de)
        pdf.add_page()
        running_head(pdf, f"ENGLISH — {run_en}, {rng}")
        if si == 0:
            centered(pdf, head_en, "dejavu", "B", 13.5, 8, 3)
        for _idx, _de, en in spread:
            para(pdf, en)


def notes_pages(pdf, key, label, toc):
    pdf.add_page()
    toc[key + ":notes"] = pdf.page_no()
    tns = [(i, t) for (k, i), t in TN.items() if k == key]
    if tns:
        centered(pdf, "TRANSLATOR'S NOTES", "dejavu", "B", 12, 8, 1)
        centered(pdf, label, "noto", "I", 10.5, 6, 3)
        rule(pdf, 40)
        for i, t in tns:
            para(pdf, f"[TN \u00b6{i + 1}] {t}", size=10,
                 height=5.4, space_after=1.8)
        pdf.ln(3)
    centered(pdf, "NOTES AND CORRELATIONS", "dejavu", "B", 12, 8, 1)
    centered(pdf, label + " — carried from the Critical Edition "
                          "(MAGVS), unchanged",
             "noto", "I", 10.5, 6, 3)
    rule(pdf, 40)
    for i, note in enumerate(sib.CHAPTER_NOTES[key], start=1):
        para(pdf, f"{i}. {note}", size=10, height=5.4,
             space_after=1.8)


# ----------------------------------------------------------------------
# Build (two-pass, as with the sibling editions)
# ----------------------------------------------------------------------
def build(toc, folio_total=None, log=None):
    Book.folio_total = folio_total
    pdf = new_book()
    pdf.set_title("Mein Kampf, Erster Band — A Parallel Critical "
                  "Edition (MAGVS)")
    pdf.set_author("Adolf Hitler (author of the text); Johnathan "
                   "'Qasparr' Monroe (reviser; translation, "
                   "apparatus and audit)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")

    german = dict(sib.load_sections())
    title_page(pdf)
    reservation_leaf(pdf)
    toc["reservation"] = 2
    source_leaf(pdf)
    toc["source"] = 3
    elements_page(pdf)
    toc["elements"] = 4
    preface_page(pdf)
    toc["preface"] = 5
    protocol_page(pdf)
    toc["protocol"] = 6
    contents_page(pdf, toc)
    labels = {"widmung": "Widmung", "vorwort": "Vorwort",
              "kap1": "1. Kapitel — Im Elternhaus",
              "kap2": "2. Kapitel — Wiener Lehr- und Leidensjahre"}
    for key, head_de, head_en, run_de, run_en in BRICK1:
        de_list = german[key]
        en_list = load_translation(key)
        assert len(de_list) == len(en_list), \
            f"{key}: German {len(de_list)} != English {len(en_list)}"
        spreads = plan_spreads(key, de_list, en_list, log)
        log.append(f"{key}: {len(de_list)} units, "
                   f"{len(spreads)} spreads")
        print_section(pdf, key, head_de, head_en, run_de, run_en,
                      spreads, toc, log)
        notes_pages(pdf, key, labels[key], toc)
    return pdf, toc


def main():
    log = []
    toc = {}
    pdf, toc = build(toc, log=log)                 # pass one
    folio_total = pdf.pages_count
    log2 = []
    pdf, toc = build(toc, folio_total, log2)       # pass two
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"bytes: {OUT.stat().st_size}")
    for line in log2:
        print(f"  {line}")
    for k, v in toc.items():
        print(f"  toc {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
