#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Non est super terram potestas quae comparetur ei." -- Job 41, the
verse Hobbes himself cites at the end of his twenty-eighth chapter:
"the two last verses of the one and fortieth of Job."

LEVIATHAN -- A Teacher's Revision (MAGVS) -- built, not copied.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. -- The Flagpole on this
volume claims THE REVISION AND THE APPARATUS ONLY. Thomas Hobbes's
text is public domain; no claim reaches for it, and the title page of
the built book says so in plain words.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   Project Gutenberg eBook #3207, plain text -- the source of
          record secured at this program's founding (2026-11-02):
          SHA-256 3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b204f
          60475009b7294, re-verified byte for byte at this build. The
          e-text descends from the Pelican Classics edition, which was
          prepared from the first edition (1651); its own
          Transcriber's Notes declare the chain and its interventions.
  PROCESS The file is hard-wrapped at ~72 columns; the builder
          reflows it to book measure. Hobbes's marginal summary notes
          stand in the file as single-line blocks between his
          paragraphs; the builder sets them in place as centered
          subheads -- they are his text, in his order, wearing frame
          typography. Nothing else is re-ordered. The builder asserts
          the founding census as it parses: Dedicatory Epistle,
          Introduction, forty-seven chapters in four Parts
          (16/15/12/4), A Review and Conclusion closing on FINIS.
          A failed assertion fails the build, not the book.
  OUTPUT  LEVIATHAN-MAGVS.pdf -- the complete book in Teacher's
          Edition dress: doctrine logo, title block, a typographic
          frontispiece leaf, the 1651 imprint transcribed, the
          four-element content test, Reviser's Preface, contents,
          Hobbes's text whole, closing apparatus (operations and
          source declared, Table of Authorities, Colophon),
          publisher's imprint (Bleats Publishing Group; SPARROW,
          proprietor), Flagpole front and back, resolving footers.
  TOLERANCE  Any step that would change a word of Hobbes fails the
          edition. Normalizations are confined to typography and
          furniture (reflow, subhead setting of the margin notes,
          part-divider leaves) and are declared in the book itself.

  THE FRONTISPIECE, stated plainly: Plate I of this program stood
  OPEN from the founding (the 2026-11-02 generation in the ruled
  register was declined by the image tooling; see the program's
  ART-REPORT). For this binding the desk struck an original
  programmatic emblem twice (build_plate.py; the sovereign composed
  as geometry -- a multitude of circles under a crown, sword and
  crozier upright, town and country below). Both strikes were
  viewed whole and judged below frontispiece standard: the figure
  reads as a diagram, not a sovereign. Per the rule that a
  dignified typographic leaf beats a poor drawing, the edition
  binds a TYPOGRAPHIC frontispiece leaf (the Job motto, in the
  classical inscriptional spelling of this house) and declares
  the emblem UNCHARTED in its apparatus. The 1651 engraving
  frontispiece (attributed to Abraham Bosse) is neither copied
  nor traced anywhere in this volume; the homage is to Hobbes's
  concept, stated in words.

  Multi-pass build: the contents page needs section page numbers,
  so the book is composed repeatedly until the table of contents
  is stable. Page-number tokens are printed at a fixed width in
  every pass, so entry heights cannot drift between passes; the
  loop asserts stability before the file is written.

  fpdf2 discipline (house gotcha, AGENTS.md 2026-10-04): every
  multi_cell is called with new_x=XPos.LMARGIN, new_y=YPos.NEXT so
  the pen returns to the left margin instead of dying at the right.
"""

import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ----------------------------------------------------------------------
# Paths and constants (MECHANISM: everything the build touches, named)
# ----------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source" / "pg3207.txt"        # Project Gutenberg #3207
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "LEVIATHAN-MAGVS.pdf"
SOURCE_SHA256 = ("3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b"
                 "204f60475009b7294")

NOTO = "/usr/share/fonts/truetype/noto"        # body face: true italics
DEJAVU = "/usr/share/fonts/truetype/dejavu"    # display face

FLAGPOLE = ("Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, "
            "ARR, All Rights Reserved, Without Prejudice. Right of claim "
            "hereby reserved and coined under the authority of the "
            "Living Man.")
THELEMIC_DATE = ("IX day of November, Dies Lunae, Sol in Scorpio, "
                 "Anno V:xii e.n. (2026 e.v.)")
FOOTER = ("— {n} of {m} — | All Rights Reserved, Without Prejudice | "
          "Flagpole of Claim and Coinage reserved")
PUBLISHER = "Published by Bleats Publishing Group"
PROPRIETOR = ("SPARROW (Sole Proprietorship) — Johnathan 'Qasparr' "
              "Monroe, Proprietor, legal publisher of record")

ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
          "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI",
          "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII",
          "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
          "XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII"]
# Part furniture: (part heading, part title, first chapter roman).
# Boundaries per the founding census and the book's own contents list.
PARTS = [("PART THE FIRST", "OF MAN", "I"),
         ("PART THE SECOND", "OF COMMON-WEALTH", "XVII"),
         ("PART THE THIRD", "OF A CHRISTIAN COMMON-WEALTH", "XXXII"),
         ("PART THE FOURTH", "OF THE KINGDOME OF DARKNESSE", "XLIV")]
PART_OF = {}
for _pi, (_h, _t, _first) in enumerate(PARTS):
    _start = ROMANS.index(_first)
    _end = (ROMANS.index(PARTS[_pi + 1][2]) if _pi + 1 < len(PARTS)
            else len(ROMANS))
    for _r in ROMANS[_start:_end]:
        PART_OF[_r] = _pi

PLATE_PAGE = 2     # physical page of the unfoliated frontispiece leaf


def folio_no(physical):
    """Printed folio of a physical page. The frontispiece leaf
    (physical page PLATE_PAGE) is unfoliated front matter: pages
    before it count as themselves, pages after it count one less."""
    return physical if physical < PLATE_PAGE else physical - 1


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
CHAP_RE = re.compile(r"^CHAPTER ([IVXL]+)\.?\s*(.*)$")


def _blocks(lines, notes=True):
    """Split source lines into blocks on blank lines; classify each
    block as prose (reflowed) or as one of Hobbes's marginal summary
    notes (a single short line, in his Title Case, standing between
    paragraphs exactly where he set it). DOCTRINE: the parse changes
    no words -- wrapped lines are joined with single spaces."""
    raw_blocks, cur = [], []
    for ln in lines:
        if ln.strip() == "":
            if cur:
                raw_blocks.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        raw_blocks.append(cur)
    out = []
    for blk in raw_blocks:
        text = " ".join(s.strip() for s in blk)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if (notes and len(blk) == 1 and len(text) <= 78
                and len(text.split()) <= 9
                and text[-1] not in ".;:!?," and text[0].isupper()):
            out.append({"note": text})
        else:
            out.append({"text": text})
    return out


def load_units():
    """Parse the secured file into the book's units, asserting the
    founding census (47 chapters, 16/15/12/4) as it goes."""
    raw = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = raw.split("\n")
    ded_start = next(i for i, ln in enumerate(lines)
                     if ln.startswith("TO MY MOST HONOR"))
    contents_at = next(i for i, ln in enumerate(lines)
                       if ln.strip() == "CONTENTS OF THE CHAPTERS")
    intro_at = next(i for i, ln in enumerate(lines)
                    if ln.strip() == "THE INTRODUCTION")
    finis_at = next(i for i, ln in enumerate(lines)
                    if ln.strip() == "FINIS")

    units = [{"kind": "dedicatory", "key": "dedicatory",
              "title": "THE DEDICATORY EPISTLE",
              "blocks": _blocks(lines[ded_start:contents_at],
                                notes=False)}]

    body = lines[intro_at:finis_at]
    cur = None
    chapters = []

    def flush():
        nonlocal cur
        if cur is not None:
            chapters.append(cur)
        cur = None

    i = 0
    while i < len(body):
        s = body[i].strip()
        m = CHAP_RE.match(s)
        if m:
            flush()
            heading = [s]
            i += 1
            while i < len(body) and body[i].strip() != "":
                heading.append(body[i].strip())
                i += 1
            cur = {"kind": "chapter", "num": m.group(1),
                   "key": "ch" + m.group(1),
                   "title": " ".join(heading), "lines": []}
            continue
        if s == "A REVIEW, AND CONCLUSION":
            flush()
            cur = {"kind": "review", "key": "review",
                   "title": s, "lines": []}
            i += 1
            continue
        if cur is None:
            cur = {"kind": "intro", "key": "intro",
                   "title": "THE INTRODUCTION", "lines": []}
        cur["lines"].append(body[i])
        i += 1
    flush()

    for u in chapters:
        u["blocks"] = _blocks(u.pop("lines"))
        units.append(u)

    nums = [u["num"] for u in units if u["kind"] == "chapter"]
    assert nums == ROMANS, f"chapter census failed: {nums[:8]}..."
    counts = [0, 0, 0, 0]
    for n in nums:
        counts[PART_OF[n]] += 1
    assert counts == [16, 15, 12, 4], f"part census failed: {counts}"
    assert units[1]["kind"] == "intro" and units[-1]["kind"] == "review"
    return units


# ----------------------------------------------------------------------
# The book
# ----------------------------------------------------------------------
class Book(FPDF):
    folio_total = None    # foliated page count, learned between passes

    def footer(self):
        if self.page_no() == PLATE_PAGE:
            return            # the frontispiece leaf is unfoliated
        self.set_y(-14)
        self.set_font("dejavu", "", 7.5)
        self.set_text_color(90, 90, 90)
        total = self.folio_total if self.folio_total else "{nb}"
        self.cell(0, 8, FOOTER.format(n=folio_no(self.page_no()),
                                      m=total), align="C")


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


# Leviathan in its own letters (lamed-vav-yod-tav-final nun). The
# codepoints are stored in REVERSE order on purpose and the fact is
# declared, here and in the book's apparatus: the fpdf2 renderer
# draws left to right and performs no bidi reordering, so the
# reversed string is what makes the word READ correctly on the
# page (lamed rightmost, final nun leftmost). The letter values
# ride in transliteration beside it; nothing is disguised.
HEBREW_LEVIATHAN = "ןתיול"  # final nun, tav, yod, vav, lamed


def hebrew_line(pdf, caption):
    pdf.ln(2)
    pdf.set_font("hebrew", "", 20)
    pdf.multi_cell(0, 11, HEBREW_LEVIATHAN, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    centered(pdf, caption, "noto", "I", 9.5, 5, 4)


def title_page(pdf):
    pdf.add_page()
    pdf.image(str(LOGO), x=(pdf.w - 36) / 2, w=36)
    pdf.ln(6)
    centered(pdf, "THOMAS HOBBES", "dejavu", "B", 25, 11, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 5)
    rule(pdf)
    centered(pdf, "LEVIATHAN", "dejavu", "B", 21, 10, 1)
    centered(pdf, "OR THE MATTER, FORME, & POWER OF A",
             "dejavu", "B", 13.5, 7)
    centered(pdf, "COMMON-WEALTH ECCLESIASTICALL AND CIVILL",
             "dejavu", "B", 13.5, 7, 2)
    centered(pdf, "London — 1651", "noto", "I", 11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A TEACHER'S REVISION (MAGVS)", "dejavu", "B", 14, 8, 2)
    centered(pdf, "A Scientific Illuminist treatment of Leviathan",
             "noto", "I", 11, 6, 5)
    centered(pdf, "The revision and apparatus are by", "noto", "", 10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship of the revision attributed exclusively to "
                  "Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights "
                  "Reserved, Without Prejudice)", "noto", "", 9.5, 5, 3)
    centered(pdf, PUBLISHER, "dejavu", "B", 11, 6, 1)
    centered(pdf, PROPRIETOR, "noto", "", 9, 5, 4)
    centered(pdf, THELEMIC_DATE, "noto", "", 10.5, 6, 1)
    centered(pdf, "Classification: Enterprise • Educational • Research "
                  "& Development", "noto", "", 10, 6)
    centered(pdf, "Method of Science, Aim of Religion", "noto", "I",
             10, 6, 6)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "Thomas Hobbes's text is PUBLIC DOMAIN. It stands in "
              "this edition unaltered in substance; the Flagpole above "
              "claims the revision and the apparatus only, and nothing "
              "of Hobbes. No word of his is modernized, abridged, or "
              "silently corrected by this edition — where the source "
              "text itself differs from the print of 1651, the "
              "apparatus declares the difference and its provenance.",
         size=9.5, height=5, align="C", space_after=0)


PLATE_CAPTION = [
    "PLATE I — THE FRONTISPIECE LEAF",
    "An original typographic plate of this edition. The motto is the "
    "verse Hobbes himself sets over his beast, cited by him at the "
    "end of Chapter XXVIII from “the two last verses of the one and "
    "fortieth of Job” (Job 41:33 in the Hebrew numbering; 41:24 in "
    "the Vulgate). It is printed here in the classical inscriptional "
    "spelling of this house, every U written V, as Rome wrote.",
    "The famous engraved frontispiece of 1651 — the crowned giant "
    "composed of his subjects, sword and crozier in hand, attributed "
    "to Abraham Bosse — is Hobbes's own concept for his book. It is "
    "NOT copied, traced, or reproduced in this volume. Two original "
    "programmatic emblem strikes in homage to that concept were made "
    "for this binding and were judged by the desk, viewed whole, to "
    "fall below frontispiece standard; they do not ship, and the "
    "emblem stands marked UNCHARTED in the apparatus. A dignified "
    "leaf of type stands in its place, and says so.",
]


def frontispiece_page(pdf):
    """The typographic plate leaf: physical page 2, unfoliated.
    Concentric rings as the only device — the circle of the covenant,
    drawn in the livery — over the Job motto in inscriptional Latin."""
    pdf.add_page()
    pdf.set_draw_color(150, 120, 40)
    pdf.set_line_width(0.5)
    pdf.rect(18, 18, pdf.w - 36, pdf.h - 36)
    pdf.set_draw_color(46, 140, 80)
    pdf.set_line_width(0.25)
    pdf.rect(21, 21, pdf.w - 42, pdf.h - 42)
    cx = pdf.w / 2
    cy = 74
    for r, col in [(26, (150, 120, 40)), (19, (46, 140, 80)),
                   (12, (150, 120, 40))]:
        pdf.set_draw_color(*col)
        pdf.set_line_width(0.6)
        pdf.ellipse(cx - r, cy - r, 2 * r, 2 * r)
    pdf.set_y(cy + 38)
    centered(pdf, "NON EST SVPER TERRAM POTESTAS", "dejavu", "B",
             15.5, 9, 1)
    centered(pdf, "QVAE COMPARETVR EI", "dejavu", "B", 15.5, 9, 4)
    centered(pdf, "“There is no power on earth that may be compared "
                  "unto him”", "noto", "I", 11, 6, 3)
    rule(pdf, 50)
    pdf.ln(2)
    centered(pdf, PLATE_CAPTION[0], "dejavu", "B", 12, 8, 3)
    for p in PLATE_CAPTION[1:]:
        para(pdf, p, size=10, height=5.4, align="C", space_after=3)


def imprint_page(pdf):
    """The 1651 title page, transcribed as the secured text prints it."""
    pdf.add_page()
    centered(pdf, "THE 1651 IMPRINT", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The original title page, transcribed as it stands",
             "noto", "I", 10.5, 6, 8)
    for line, sz in [("LEVIATHAN", 19),
                     ("OR THE MATTER, FORME, & POWER OF A", 12.5),
                     ("COMMON-WEALTH ECCLESIASTICALL AND CIVILL", 12.5)]:
        centered(pdf, line, "dejavu", "B", sz, sz * 0.62, 3)
    pdf.ln(4)
    for line in ["Thomas Hobbes of Malmesbury", "",
                 "Printed for Andrew Crooke, at the Green Dragon",
                 "in St. Paul’s Churchyard, 1651."]:
        centered(pdf, line, "noto", "", 10.5, 6, 1)


def elements_page(pdf):
    """The four-element content test (Teacher's Edition rule 6)."""
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete text of Leviathan as carried by "
                   "Project Gutenberg eBook #3207 — the source of "
                   "record secured at this program's founding on "
                   "2026-11-02 (SHA-256 3de1e492…09b7294, re-verified "
                   "at this build): the Dedicatory Epistle, the "
                   "Introduction, forty-seven chapters in four Parts, "
                   "and A Review, and Conclusion, closing on FINIS."),
        ("PROCESSES", "Line-wrap reflowed to book measure; Hobbes's "
                      "marginal summary notes set in place as "
                      "centered subheads; part-divider leaves "
                      "supplied as declared editorial furniture; the "
                      "Teacher's Edition frame set around the text. "
                      "No sentence of Hobbes is touched."),
        ("OUTPUTS", "This volume: the whole book, in Teacher's "
                    "Revision (MAGVS) dress, with a Reviser's Preface "
                    "before it and an honest apparatus behind it."),
        ("TOLERANCES", "Zero. Any process that would change a word "
                       "of Hobbes fails the edition and is rejected. "
                       "Where the secured text differs from the print "
                       "of 1651 — it descends through the Pelican "
                       "Classics edition, and its transcriber declares "
                       "his own interventions — the apparatus states "
                       "the difference and its provenance instead of "
                       "smoothing it."),
    ]
    for head, body in items:
        pdf.set_font("dejavu", "B", 11)
        pdf.multi_cell(0, 6, head, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        para(pdf, body, space_after=4)
    para(pdf, "Tier labels used in this edition: ATTESTED (in the "
              "record or in the text itself), DERIVED (drawn from the "
              "record by stated reasoning), CONSTRUCTED (the reviser's "
              "frame, hypothesis until weighed), UNCHARTED (named as "
              "open, never filled by invention).",
         size=10, space_after=0)


# ----------------------------------------------------------------------
# The Reviser's Preface (original prose of the revision; the desk's
# hand appears ONLY in frame pages like this one, never in the text)
# ----------------------------------------------------------------------
PREFACE_PARAS = [
    "This volume completes a debt. On the second day of November "
    "2026 the founder of this house founded a Teacher's Revision "
    "(MAGVS) of three texts under one program: Thomas Hobbes's "
    "Leviathan, Aleister Crowley's essay Duty, and Crowley's poem "
    "The Pentagram. The grouping had its reasoning stated on its "
    "face — the Commonwealth ordered from outside, conduct ordered "
    "from inside, and the instrument by which the operator seats "
    "himself at the center of the ordered figure. The founding brick "
    "secured the sources, weighed the names, and built first "
    "apparatus for all three strands. The two Crowley strands "
    "remain their own works for their own day. This book is "
    "Leviathan alone, and it is Leviathan whole: the flagship of "
    "the program, bound at last.",

    "Hobbes published Leviathan in London in 1651, an old man by "
    "the reckoning of his century, writing in Paris — the "
    "Dedicatory Epistle printed in this volume is dated there, "
    "April 15/25, 1651 — while his country finished a civil war "
    "that had killed its king. The book is the first systematic "
    "work of political philosophy in the English tongue, and it is "
    "built like the geometry Hobbes revered. His method is "
    "definition before doctrine. In the Introduction he bids the "
    "reader know himself — read thy self — for the similitude of "
    "the passions is the same in all men, and a man who has read "
    "himself has the characters of mankind. From that reading he "
    "raises the book's founding figure: Nature, the art by which "
    "God made and governs the world, is imitated by the art of "
    "man, which “can make an Artificial Animal” — and the greatest "
    "of these artificial animals is the Commonwealth, the "
    "Artificiall Man, whose body is the multitude, whose joints "
    "are magistrates, whose nerves are reward and punishment, and "
    "whose soul is sovereignty. Everything that follows is the "
    "anatomy of that animal, dissected in his own order: sense, "
    "imagination, speech, reason; the passions; power and worth; "
    "then the disease of the state of nature and its cure.",

    "The cure begins from the book's most famous diagnosis. Men "
    "are by nature sufficiently equal — the weakest has strength "
    "enough to kill the strongest, by secret machination or by "
    "confederacy — and from that equality, where there is no "
    "common power, proceeds diffidence, and from diffidence, war: "
    "the war of every man against every man, in which the life of "
    "man is “solitary, poore, nasty, brutish, and short.” Against "
    "that war Hobbes sets the laws of nature, which he defines "
    "without ornament as dictates of reason: the first and "
    "fundamental law, “seek Peace, and follow it”; the second, "
    "that a man be willing, when others are so too, to lay down "
    "his right to all things. Rights laid down by covenant are "
    "gathered into one person — a man, or an assembly — who bears "
    "the person of them all, and this, Hobbes says, is the "
    "generation of “that great LEVIATHAN, or rather (to speake "
    "more reverently) of that Mortall God, to which wee owe under "
    "the Immortall God, our peace and defence.” For “Covenants, "
    "without the Sword, are but Words, and of no strength to "
    "secure a man at all.” The sovereign so generated holds rights "
    "that cannot be forfeited for injustice, because every subject "
    "has authorized all his actions in advance; and the liberty "
    "that remains to the subject is real but bounded — liberty, "
    "in Hobbes's settled signification, is the “absence of "
    "externall Impediments” to motion, and for subjects it lives "
    "chiefly in the silence of the law.",

    "Half the book — Parts the Third and Fourth — is Scripture, "
    "and a reader who skips it has read half of Hobbes. He argues "
    "at enormous length, from the Bible itself, that the kingdom "
    "of God by covenant ended with the people's election of Saul; "
    "that no church, clergy, or private interpreter may set its "
    "reading of Scripture against the civil sovereign's; that what "
    "is necessary to salvation is one article — Jesus is the "
    "Christ — joined to obedience to the laws. The Fourth Part, "
    "Of the Kingdome of Darknesse, names the enemy plainly: a "
    "confederacy of deceivers who, by dark and erroneous doctrines, "
    "extinguish the light of nature and of the gospel alike, and "
    "farm men's fears of spirits, purgatory, and excommunication "
    "into a power that rivals the Commonwealth. Whatever a "
    "reader's theology, the political point is one piece with "
    "Parts the First and Second: there can be only one public "
    "reason in a commonwealth, and every rival jurisdiction "
    "raised over men's consciences is a seed of the war the book "
    "exists to end. Hobbes's aim, from the first page to FINIS, "
    "is peace — peace by science: a doctrine of justice as "
    "certain, he believed, as the doctrine of triangles.",

    "The founding of this program weighed the book's name before "
    "it annotated a line, and the weighing is recorded here with "
    "its reasoning, as the house rule requires. Leviathan enters "
    "the program first as a Hebrew word — the beast of Job "
    "41, of Psalm 74 and 104, of Isaiah 27 — and in Hebrew's own "
    "bank, mispar hechrechi, it weighs 496: lamed 30, vav 6, "
    "yod 10, tav 400, final nun 50. [DERIVED — computed from the "
    "attested spelling by the attested bank, by the house "
    "instrument.] In English "
    "ordinal, LEVIATHAN weighs 92 — one short of this house's "
    "standing number, 93. The desk records that as what it is: a "
    "near miss and a zero point, not a bridge. The discipline that "
    "prints the miss beside the hit is the same discipline that "
    "runs this whole edition.",

    "Where the reviser's house answers Hobbes, it answers him in "
    "the open and in the reviser's own name; nothing in this "
    "section is Hobbes's doctrine, and the text that follows is "
    "unannotated by it, so the reader may weigh the disagreement "
    "with the evidence whole. [CONSTRUCTED — the reviser's frame "
    "throughout this section.] The agreements are genuine, and "
    "they are not small. Hobbes insists that terms be settled "
    "before they are argued — that insignificant speech, words "
    "without settled meaning, is the first abuse from which "
    "absurdity and sedition grow; this edition's method, and this "
    "house's, is that insistence wearing another coat. Hobbes "
    "teaches that a covenant without enforcement is breath; the "
    "house's discipline answers: proofs, not claims — a thing "
    "stands when it can be checked. And Hobbes's diagnosis stands "
    "unrefuted by four centuries: where power is unorganized and "
    "every man is his own garrison, the issue is war, and peace "
    "is an artifact — made, or not made.",

    "The disagreements are equally genuine, and they go to the "
    "seat of the whole machine. Hobbes's covenant cannot be "
    "revoked: the sovereign judges even what doctrines may be "
    "taught, and the subject, having authorized all, can complain "
    "of nothing. The founder's doctrine holds the contrary seat: "
    "the living man is sovereign over his own will, his property, "
    "and his data; an authority that may not be questioned fails "
    "the house's gate, which is fail-closed — no justification, "
    "no action. Where Hobbes gathers every transferred right into "
    "one unaccountable hand, the house's Handshake Clause lays "
    "down the opposite law of transfer: every right transferred "
    "is transferred multiplied by its duty, and a bargain that "
    "severs duty from right is void at the handshake. Where "
    "Hobbes, fearing the multitude's judgment, would have the "
    "sovereign license what may be read, this publishing house is "
    "chartered on the contrary policy, and prints it on its seal: "
    "no voice shall be silenced; the user above all. These are "
    "the founder's positions, set down as his, in his preface, "
    "before Hobbes's book — and then Hobbes's book, entire, so "
    "that the mortal god may make his own case to the reader "
    "without the reviser's thumb on the scale. That is what a "
    "Teacher's Revision is for: not to win the argument by "
    "editing, but to seat both parties at one table with the "
    "evidence whole.",

    "What this edition does, stated as plainly as the apparatus "
    "states it again at the back. The text is the complete "
    "Leviathan of the secured electronic source: Dedicatory "
    "Epistle, Introduction, forty-seven chapters in their four "
    "Parts, and A Review, and Conclusion, closing on Hobbes's "
    "FINIS. That source descends from the Pelican Classics "
    "edition, prepared from the first edition; its spelling and "
    "punctuation stand as Hobbes's proof-read text presents them "
    "through that chain, and the transcriber's own declared "
    "interventions — quotation marks introduced where the "
    "original's italics marked quotation, chapter headings set "
    "wholly in capitals — are declared in the apparatus, not "
    "hidden. Hobbes's marginal summary notes, which the first "
    "edition set in its margins as a running index, stand in the "
    "electronic text as single lines between his paragraphs; this "
    "edition sets them in place as centered subheads, in his "
    "order, as his words. The charter of 2026-11-02 projected a "
    "deeper brick-by-brick apparatus over every chapter "
    "(bricks L-1 through L-12); the founding brick's apparatus on "
    "the Introduction and Chapters 1–3 stands in the program's "
    "work papers, and the full brick sequence remains UNCHARTED "
    "future work — it is not claimed here, because it is not "
    "done. What is done is the book: bound, complete, and weighed. "
    "A book first. The rest, in its season.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. The Job motto. Hobbes cites Job at "
    "the end of Chapter XXVIII for “the greatnesse of his power”: "
    "the passage stands in the text of this edition in English, "
    "sourced by Hobbes himself to “the two last verses of the one "
    "and fortieth of Job.” The first draft of this program's "
    "charter repeated the common claim that the 1651 title page "
    "bears the verse in Latin; the founding census of the secured "
    "text found the title page printing title, author, and printer "
    "only, and the claim was struck by evidence and stands in the "
    "charter as a marked FOUNDING ERRATUM. Whether the 1651 print "
    "or its engraved frontispiece carries the Latin is UNVERIFIED "
    "from the secured file and awaits print collation. "
    "[ATTESTED — the census; the erratum stands in CHARTER.md.]",
    "2. The 1651 frontispiece — the crowned sovereign composed of "
    "the multitude, sword in the right hand, crozier in the left, "
    "landscape beneath — is attributed to Abraham Bosse, working "
    "from Hobbes's conception. It is not reproduced in this "
    "edition. [ATTESTED as the common attribution.]",
    "3. The Pelican derivation. The electronic source states it "
    "“was prepared from the Pelican Classics edition of "
    "Leviathan, which in turn was prepared from the first "
    "edition.” The file does not name the Pelican editor or "
    "printing; the 1968 Macpherson edition is the common "
    "candidate and is recorded here as a candidate only — NOT "
    "asserted. [ATTESTED — the file's statement; UNVERIFIED — "
    "the editor.]",
    "4. The answering tradition. Locke's Two Treatises (1689) and "
    "Rousseau's Social Contract (1762) are the canonical replies "
    "the centuries set against this book; the reviser's answer in "
    "this preface takes its place in that line, at its stated "
    "tier, and claims no higher seat. [ATTESTED — the record of "
    "the tradition.]",
    "5. The founding weighing (Leviathan = 496) was computed by the "
    "house instrument (pontifex ptk) at the founding and re-run "
    "at this revision; the expectation was stated before the "
    "weighing, and the tool, not the expectation, is the "
    "authority. [DERIVED.]",
]


def preface_page(pdf):
    pdf.add_page()
    centered(pdf, "REVISER'S PREFACE", "dejavu", "B", 14, 9, 2)
    centered(pdf, "By Johnathan 'Qasparr' Monroe, Reviser",
             "noto", "I", 10.5, 6, 6)
    for idx, p in enumerate(PREFACE_PARAS):
        if idx == 4:
            hebrew_line(pdf, "Leviathan, in its own letters — "
                             "weighed in the paragraph following")
        para(pdf, p)
    pdf.ln(2)
    rule(pdf, 40)
    for n in PREFACE_NOTES:
        para(pdf, n, size=9, height=4.8, space_after=1.6)


def contents_entries(toc):
    """(label, key) pairs in book order; page numbers ride from toc."""
    entries = [("PLATE I — THE FRONTISPIECE LEAF", "plate"),
               ("The 1651 Imprint", "imprint"),
               ("The Edition's Four Elements", "elements"),
               ("Reviser's Preface", "preface"),
               ("The Dedicatory Epistle — Hobbes to Francis Godolphin",
                "dedicatory")]
    for pi, (head, title, _first) in enumerate(PARTS):
        entries.append((f"{head} — {title}", f"part{pi}"))
        if pi == 0:
            entries.append(("THE INTRODUCTION", "intro"))
        first = ROMANS.index(_first)
        last = (ROMANS.index(PARTS[pi + 1][2]) if pi + 1 < len(PARTS)
                else len(ROMANS))
        for r in ROMANS[first:last]:
            entries.append((f"CHAPTER {r}", "ch" + r))
    entries += [("A REVIEW, AND CONCLUSION", "review"),
                ("Apparatus of the Revision", "apparatus"),
                ("Table of Authorities", "authorities"),
                ("Colophon", "colophon")]
    return entries


def contents_page(pdf, toc, units_by_key):
    pdf.add_page()
    centered(pdf, "CONTENTS", "dejavu", "B", 14, 9, 8)
    for label, key in contents_entries(toc):
        if key.startswith("ch"):
            label = units_by_key[key]["title"].replace(". ", " — ", 1)
        page = toc.get(key)
        # Fixed-width token in every pass: entry heights cannot drift.
        token = f"{page:>3}" if isinstance(page, int) else "999"
        if key == "plate":
            token = "  —"
        is_part = key.startswith("part")
        if is_part:
            pdf.ln(2.5)
            pdf.set_font("dejavu", "B", 10.5)
            pdf.multi_cell(0, 6.2, f"{label}    {token}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            pdf.set_font("noto", "", 9.5)
            pdf.multi_cell(0, 5.6, f"{label}    {token}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def part_divider(pdf, pi, toc):
    head, title, _first = PARTS[pi]
    pdf.add_page()
    toc[f"part{pi}"] = folio_no(pdf.page_no())
    pdf.ln(58)
    centered(pdf, head, "dejavu", "B", 19, 11, 3)
    rule(pdf, 70)
    centered(pdf, title, "dejavu", "B", 15, 9, 6)
    first = ROMANS.index(_first)
    last = (ROMANS.index(PARTS[pi + 1][2]) if pi + 1 < len(PARTS)
            else len(ROMANS))
    span = f"Chapters {ROMANS[first]}–{ROMANS[last - 1]}"
    if pi == 0:
        span = "The Introduction, and Chapters I–XVI"
    centered(pdf, span, "noto", "I", 11, 6, 2)
    centered(pdf, "Part-divider leaf — editorial furniture of this "
                  "edition, declared in the apparatus", "noto", "",
             8.5, 5)


def unit_pages(pdf, units, toc):
    for u in units:
        pdf.add_page()
        toc[u["key"]] = folio_no(pdf.page_no())
        if u["kind"] == "dedicatory":
            centered(pdf, u["title"], "dejavu", "B", 14, 9, 1)
            centered(pdf, "Hobbes to Mr. Francis Godolphin of "
                          "Godolphin — Paris, April 15/25 1651",
                     "noto", "I", 10.5, 6, 2)
            rule(pdf, 50)
            pdf.ln(2)
            for j, b in enumerate(u["blocks"]):
                if j == 0:
                    centered(pdf, b["text"], "dejavu", "B", 11, 6.4, 5)
                else:
                    para(pdf, b["text"])
            continue
        centered(pdf, u["title"], "dejavu", "B", 13.5, 8, 1)
        rule(pdf, 50)
        pdf.ln(2)
        for b in u["blocks"]:
            if "note" in b:
                pdf.ln(1.6)
                centered(pdf, b["note"], "noto", "I", 10.5, 6, 1.6)
            else:
                para(pdf, b["text"])
        if u["kind"] == "review":
            pdf.ln(6)
            centered(pdf, "FINIS", "dejavu", "B", 13, 8)


def apparatus_pages(pdf, toc):
    pdf.add_page()
    toc["apparatus"] = folio_no(pdf.page_no())
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "What was done to the text, stated in the open",
             "noto", "I", 10.5, 6, 4)
    para(pdf, "The text of Leviathan in this edition is the text of "
              "Project Gutenberg eBook #3207, the source of record "
              "secured at this program's founding on 2026-11-02 and "
              "re-verified at this build (SHA-256 " + SOURCE_SHA256 +
              "). The file's own header credits Edward White and "
              "David Widger; its Transcriber's Notes state that the "
              "e-text “was prepared from the Pelican Classics edition "
              "of Leviathan, which in turn was prepared from the "
              "first edition.” The following operations, and no "
              "others, were performed upon it by the builder:")
    for line in [
        "1. The Gutenberg file's hard line-wrapping was reflowed "
        "into book paragraphs. No word was added, removed, or "
        "reordered.",
        "2. Hobbes's marginal summary notes — the running index "
        "the first edition set in its margins — stand in the "
        "electronic text as single lines between his paragraphs. "
        "This edition sets them in place as centered italic "
        "subheads, in his order, as his words. They are text, not "
        "apparatus, and the builder's census counts them rather "
        "than inventing them.",
        "3. Part-divider leaves (Part the First through Part the "
        "Fourth) are editorial furniture of this edition, inserted "
        "at the part boundaries of the book's own contents list "
        "and declared on their faces. The electronic text carries "
        "the parts in its contents list, not as body divisions.",
        "4. Excluded, and declared here rather than vanished: the "
        "Project Gutenberg license header and license text, and "
        "the e-text's Transcriber's Notes. Neither is part of the "
        "book of 1651; the substance of the Transcriber's Notes — "
        "the Pelican derivation and the interventions next "
        "declared — is carried in item 5 and in the Preface, and "
        "the whole stands in the source file, which the desk "
        "retains.",
        "5. Normalization, declared at its true depth. This "
        "edition modernizes nothing. But the source is not the "
        "print of 1651: it descends through the Pelican Classics "
        "edition, and its transcriber declares his own "
        "interventions in the file — quotation marks introduced "
        "where the original's italics indicated quotation, and "
        "chapter headings set wholly in capitals where Hobbes "
        "used a mixture of capitals and italics. Hobbes's "
        "spelling and punctuation stand as the first edition "
        "presents them through that chain, per the transcriber's "
        "stated aim. Where the Pelican text itself regularized "
        "anything, that is the Pelican's doing, upstream of this "
        "edition, and it is declared here rather than hidden. "
        "The Greek words Hobbes prints in the Greek alphabet "
        "stand in the plain-text file only as that file carries "
        "them; this edition restores nothing by conjecture.",
        "6. The census, asserted by the builder at parse: "
        "Dedicatory Epistle; the Introduction; forty-seven "
        "chapters — Part I, sixteen (I–XVI); Part II, fifteen "
        "(XVII–XXXI); Part III, twelve (XXXII–XLIII); Part IV, "
        "four (XLIV–XLVII); A Review, and Conclusion, closing "
        "on FINIS. One printed quirk of the source stands "
        "uncorrected, as it stands: the heading of Chapter XL "
        "wants its full stop.",
    ]:
        para(pdf, line, size=10, space_after=1.0)
    para(pdf, "THE FRONTISPIECE. Plate I of this program stood open "
              "from the founding: the 2026-11-02 Art Report records "
              "that generation in the ruled register was declined "
              "by the image tooling and no plate was produced. For "
              "this binding, two original programmatic emblem "
              "strikes were made (the sovereign composed as "
              "geometry — a multitude of circles under a crown, "
              "sword and crozier upright, town and country below; "
              "builder preserved with the edition) and were judged "
              "by the desk, viewed whole, to fall below "
              "frontispiece standard. The edition therefore binds "
              "the typographic frontispiece leaf at Plate I and "
              "marks the emblem UNCHARTED. The 1651 engraved "
              "frontispiece, attributed to Abraham Bosse, is "
              "nowhere copied or traced in this volume.",
         size=10, space_after=1.0)
    para(pdf, "THE PROGRAM. This volume is Leviathan the book. The "
              "founding charter (2026-11-02) projected a "
              "brick-by-brick apparatus over every chapter "
              "(bricks L-1–L-12); the founding apparatus on the "
              "Introduction and Chapters 1–3 stands in the "
              "program's work papers, and the brick sequence "
              "remains UNCHARTED future work, not claimed here. "
              "The charter's companion strands — Crowley's Duty "
              "and The Pentagram — carry their own founding "
              "apparatus (D-1, the first pass over Duty's four "
              "sections; P-1, the Pentagram deep dive) in the same "
              "work papers; their bound editions are separate "
              "works for another day, and nothing in this volume "
              "pretends to be them.",
         size=10, space_after=1.0)
    hebrew_line(pdf, "Leviathan, in its own letters")
    para(pdf, "THE WEIGHING OF THE NAME. Leviathan, in Hebrew's own "
              "bank, mispar hechrechi: lamed 30 + vav 6 + yod 10 + "
              "tav 400 + final nun 50 (the final nun at its letter's "
              "value in this bank) = 496 "
              "[DERIVED — the house instrument, pontifex ptk, "
              "weighed at the founding and re-run at this revision]. "
              "(The Hebrew above is set as display type in Noto "
              "Serif Hebrew; the toolchain performs no bidi "
              "reordering, so the letter values are carried in "
              "transliteration here — the limitation declared, not "
              "disguised.) "
              "LEVIATHAN, English ordinal, = 92: recorded in the "
              "founding ledger as a near miss to 93 — a zero point, "
              "printed here with the hit, per the discipline that "
              "the misses stand beside the bridges.",
         size=10, space_after=1.4)

    toc["authorities"] = folio_no(pdf.page_no())
    pdf.ln(1)
    centered(pdf, "TABLE OF AUTHORITIES (CONDENSED)", "dejavu", "B",
             12, 8, 3)
    for a in [
        "Hobbes, Thomas. Leviathan, or The Matter, Forme, & Power "
        "of a Common-wealth Ecclesiasticall and Civill. London: "
        "Andrew Crooke, 1651.",
        "Project Gutenberg eBook #3207 — the electronic source text "
        "of this revision (Pelican Classics derivation; credits "
        "Edward White and David Widger), secured 2026-11-02, "
        "SHA-256 " + SOURCE_SHA256 + ".",
        "Job 41; Psalm 74:14; Psalm 104:26; Isaiah 27:1 — the "
        "scriptural seats of Leviathan's name.",
        "The frontispiece of the 1651 edition, attributed to "
        "Abraham Bosse — the concept's ancestor; not reproduced.",
        "Charter and Start Report of this program (house papers, "
        "2026-11-02) — the founding census, the weighing ledger, "
        "and the FOUNDING ERRATUM on the title-page epigraph.",
        "Locke, John. Two Treatises of Government (1689); "
        "Rousseau, Jean-Jacques. Du contrat social (1762) — the "
        "answering tradition named in the Preface.",
        "The Teacher's Edition format (house directive, 2026) — "
        "the dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.0)

    pdf.add_page()
    toc["colophon"] = folio_no(pdf.page_no())
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Teacher's Revision (MAGVS) of Leviathan was "
              "generated on " + THELEMIC_DATE + ", by a programmatic "
              "builder (fpdf2, Noto Serif and DejaVu Serif faces) "
              "from the public-domain source named in the Table of "
              "Authorities, under the Teacher's Edition format of "
              "this house. It completes the Leviathan strand's "
              "standing debt from the founding of 2026-11-02: the "
              "book, bound whole.")
    para(pdf, "The revision, the Reviser's Preface, and the "
              "apparatus are the work of Johnathan 'Qasparr' Monroe, "
              "to whom their authorship is attributed exclusively, "
              "ARR — All Rights Reserved, Without Prejudice. Thomas "
              "Hobbes's text is public domain and is claimed by no "
              "one in this volume.")
    para(pdf, PUBLISHER + ". " + PROPRIETOR + ".", align="C")
    para(pdf, "Method of Science. Aim of Religion.", align="C")
    pdf.ln(4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C", space_after=4)
    centered(pdf, "93 — Live, Love, and let Love, Live.", "dejavu",
             "B", 12, 8)


def compose(units, toc_in, folio_total):
    Book.folio_total = folio_total
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    pdf.set_title("Leviathan — Teacher's Revision (MAGVS)")
    pdf.set_author("Thomas Hobbes (author); Johnathan 'Qasparr' "
                   "Monroe (reviser)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")
    pdf.add_font("noto", "", f"{NOTO}/NotoSerif-Regular.ttf")
    pdf.add_font("noto", "B", f"{NOTO}/NotoSerif-Bold.ttf")
    pdf.add_font("noto", "I", f"{NOTO}/NotoSerif-Italic.ttf")
    pdf.add_font("noto", "BI", f"{NOTO}/NotoSerif-BoldItalic.ttf")
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")
    pdf.add_font("hebrew", "", f"{NOTO}/NotoSerifHebrew-Regular.ttf")
    pdf.add_font("hebrew", "B", f"{NOTO}/NotoSerifHebrew-Bold.ttf")

    toc = {}
    units_by_key = {u["key"]: u for u in units}
    title_page(pdf)
    frontispiece_page(pdf)     # the plate leaf: physical 2, unfoliated
    imprint_page(pdf)
    toc["imprint"] = folio_no(pdf.page_no())
    elements_page(pdf)
    toc["elements"] = folio_no(pdf.page_no())
    preface_page(pdf)
    toc["preface"] = folio_no(pdf.page_no())
    contents_page(pdf, toc_in, units_by_key)
    # Hobbes's own order: the Dedicatory, then Part the First opens
    # with its divider before the Introduction it contains. Each
    # part's divider is struck exactly once, when its first unit
    # is reached -- the tracking set lives here, in the one loop
    # that walks the whole book in order.
    parts_done = set()
    for u in units:
        if u["kind"] == "intro":
            part_divider(pdf, 0, toc)
            parts_done.add(0)
        elif u["kind"] == "chapter":
            pi = PART_OF[u["num"]]
            if pi not in parts_done:
                part_divider(pdf, pi, toc)
                parts_done.add(pi)
        unit_pages(pdf, [u], toc)
    apparatus_pages(pdf, toc)
    return pdf, toc


def main():
    import hashlib
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert digest == SOURCE_SHA256, f"source hash drift: {digest}"
    units = load_units()
    toc, prev_toc, folio_total = {}, None, None
    pdf = None
    for attempt in range(4):
        pdf, toc = compose(units, toc, folio_total)
        new_total = pdf.pages_count - 1     # the plate leaf unfoliated
        if toc == prev_toc and folio_total == new_total:
            break
        prev_toc, folio_total = toc, new_total
    else:
        raise SystemExit("contents did not stabilize")
    pdf.output(str(OUT))
    notes = sum(1 for u in units for b in u["blocks"] if "note" in b)
    words = sum(len(b.get("text", "").split()) for u in units
                for b in u["blocks"])
    print(f"BUILT {OUT}")
    print(f"physical pages: {pdf.pages_count}")
    print(f"folios: {folio_total}")
    print(f"bytes: {OUT.stat().st_size}")
    print(f"units: {len(units)} (dedicatory + introduction + "
          f"47 chapters + review)")
    print(f"margin notes set as subheads: {notes}")
    print(f"body words (prose blocks): {words}")
    for key in ["dedicatory", "intro", "chXIII", "chXVII", "chXLIV",
                "review", "apparatus", "colophon"]:
        print(f"  {key}: folio {toc.get(key)}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
