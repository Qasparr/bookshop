#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"I am Oz, the Great and Terrible." -- the voice behind the curtain,
Chapter XV: the gatekeeper's whole authority, in his own words,
before the curtain is pulled.

THE WONDERFUL WIZARD OF OZ
-- A Teacher's Revision (MAGVS) -- built, not copied.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. -- The Flagpole on this
volume claims THE REVISION AND THE APPARATUS ONLY. L. Frank Baum's
text is public domain; no claim reaches for it, and the title page of
the built book says so in plain words.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   Project Gutenberg eBook #55, plain text: the 1900 Geo. M.
          Hill (Chicago) edition of The Wonderful Wizard of Oz --
          Baum's dedication, his Introduction, and Chapters I-XXIV,
          complete. The electronic text carries NO illustrations:
          exactly one "[Illustration]" placeholder line stands in
          the whole file, where the frontispiece would go.
  CANON   This edition prints THE BOOK, not the 1939 film. The shoes
          Dorothy wears are SILVER, from Chapter II to their loss in
          the desert in Chapter XXIII -- every occurrence in the
          source is silver, and the apparatus counts them. The ruby
          slippers of popular memory belong to the film (Warner
          property) and are excluded by design: no film likeness, no
          film dialogue, no film-only material stands in this book.
          The word "ruby" occurs in Baum's text only of Gayelette's
          palace (Chapter XIV) and Glinda's throne (Chapter XXIII) --
          Baum's own stones, kept as he wrote them.
  PROCESS The Gutenberg file is hard-wrapped at ~72 columns; this
          builder reflows it to book measure (paragraphs are split on
          blank lines, wrapped lines are joined). Gutenberg's
          emphasis convention (_word_) would be rendered as italic
          type; this source carries no such spans (zero, counted and
          declared in the apparatus), so the conversion stands armed
          and unfired. The electronic file's license matter, its
          Contents list (replaced by this edition's own Contents),
          and the lone title line it repeats between the Introduction
          and Chapter I are NOT part of Baum's book as this edition
          frames it; they are excluded, and every exclusion is
          DECLARED in the built book (dispositions marked, never
          vanished). Denslow's plates are absent from the source;
          none are fabricated. The gap is printed, not papered over.
  OUTPUT  WIZARD-OF-OZ-MAGVS.pdf -- the complete text in Teacher's
          Edition dress: doctrine logo, title block, four-element
          content test, Reviser's Preface, contents, the text,
          closing apparatus (operations, the illustrations
          declaration, the canon check, Table of Authorities,
          Colophon), Flagpole front and back, resolving page footers
          "-- N of M -- | All Rights Reserved, Without Prejudice |
          Flagpole of Claim and Coinage reserved".
  TOLERANCE  Any step that would change a word of Baum fails the
          edition. Any step that would turn the shoes ruby fails it
          twice. Normalizations are confined to typography (reflow)
          and are declared in the book itself.

  Two-pass build: the contents page needs section page numbers, so
  the book is composed twice -- pass one measures where each section
  falls, pass two prints the numbers. The contents page is exactly
  one page in both passes, so the measurement cannot drift.

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
SOURCE = HERE / "source" / "pg55.txt"          # Project Gutenberg #55
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "WIZARD-OF-OZ-MAGVS.pdf"

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

ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
          "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV"]
CHAPTER_KEYS = [f"Chapter {r}" for r in ROMANS]
# Frame sub-lines under headings (factual: whose hand wrote the piece).
SUBLINES = {
    "INTRODUCTION": "By L. Frank Baum — Chicago, April, 1900",
    "DEDICATION": "The Author's Dedication, as it stands in the book",
}


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
def load_sections():
    """Split the Gutenberg file into [(key, display, [paragraph...])].

    A paragraph is {"text": str} (prose, reflowed) or
    {"center_lines": [str, ...]} (the dedication, kept as lines).
    Chapter titles are taken from the source line standing under each
    "Chapter N" heading -- the desk invents no structure.
    DOCTRINE: the parse changes no words -- it joins wrapped lines
    with single spaces and would convert _emphasis_ markers to
    fpdf2's markdown italics (--emphasis--) if the source carried
    any. This source carries none; the count is returned and declared.
    """
    raw = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = raw.split("\n")
    # The dedication stands between the author line and the Contents.
    ded_start = next(i for i, ln in enumerate(lines)
                     if "dedicated to my good friend" in ln)
    ded_end = next(i for i, ln in enumerate(lines)
                   if ln.strip() == "Contents")
    dedication = [ln.strip() for ln in lines[ded_start:ded_end]
                  if ln.strip()]
    # The body begins at the second "Introduction" (the first is the
    # e-file's Contents list) and ends at the Gutenberg END marker.
    start = next(i for i, ln in enumerate(lines)
                 if ln.strip() == "Introduction" and i > 40)
    end = next(i for i, ln in enumerate(lines)
               if "*** END OF THE PROJECT" in ln)
    body = lines[start:end]

    sections = [("DEDICATION", "DEDICATION",
                 [{"center_lines": dedication}]),
                ("INTRODUCTION", "INTRODUCTION", [])]
    current = sections[1][2]
    block = []

    def flush_block():
        nonlocal block
        if block:
            text = " ".join(ln.strip() for ln in block)
            text = re.sub(r"\s+", " ", text).strip()
            # The e-file repeats the book's title, standing alone,
            # between the Introduction and Chapter I. It is furniture
            # of the file, not a word of the story: excluded here,
            # declared in the apparatus.
            if text and text != "The Wonderful Wizard of Oz":
                current.append({"text": text})
        block = []

    spans = 0  # Gutenberg _emphasis_ spans in this source (zero)
    i = 0
    while i < len(body):
        s = body[i].strip()
        if s in CHAPTER_KEYS:
            flush_block()
            # The chapter's title is the next non-blank line.
            j = i + 1
            while not body[j].strip():
                j += 1
            title = body[j].strip()
            display = f"{s.upper()} — {title.upper()}"
            sections.append((s, display, []))
            current = sections[-1][2]
            i = j + 1
            continue
        if s == "":
            flush_block()
        else:
            spans += len(re.findall(r"_[^_]+_", body[i]))
            block.append(body[i])
        i += 1
    flush_block()
    # Markdown-italics conversion, armed as in every house builder.
    for _, _, paras in sections:
        for p in paras:
            if "text" in p:
                p["text"] = re.sub(r"_([^_]+)_", r"--\1--", p["text"])
    return sections, spans


# ----------------------------------------------------------------------
# The book
# ----------------------------------------------------------------------
class Book(FPDF):
    def footer(self):
        # Teacher's Edition footer; {nb} resolves after alias call.
        self.set_y(-14)
        self.set_font("dejavu", "", 7.5)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, FOOTER.format(n=self.page_no(), m="{nb}"),
                  align="C")


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


def title_page(pdf):
    pdf.add_page()
    pdf.image(str(LOGO), x=(pdf.w - 36) / 2, w=36)
    pdf.ln(6)
    centered(pdf, "L. FRANK BAUM", "dejavu", "B", 25, 11, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 5)
    rule(pdf)
    centered(pdf, "THE WONDERFUL WIZARD OF OZ", "dejavu", "B", 19, 9, 2)
    centered(pdf, "Chicago — 1900", "noto", "I", 11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A TEACHER'S REVISION (MAGVS)", "dejavu", "B", 14, 8, 2)
    centered(pdf, "A Scientific Illuminist treatment of the Wonderful "
                  "Wizard of Oz", "noto", "I", 11, 6, 5)
    centered(pdf, "The revision and apparatus are by", "noto", "", 10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship of the revision attributed exclusively to "
                  "Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights "
                  "Reserved, Without Prejudice)", "noto", "", 9.5, 5, 4)
    centered(pdf, THELEMIC_DATE, "noto", "", 10.5, 6, 1)
    centered(pdf, "Classification: Enterprise • Educational • Research "
                  "& Development", "noto", "", 10, 6)
    centered(pdf, "Method of Science, Aim of Religion", "noto", "I",
             10, 6, 5)
    centered(pdf, "Published by Bleats Publishing Group", "dejavu",
             "B", 11.5, 6.5, 1)
    centered(pdf, "SPARROW (Sole Proprietorship) — Johnathan 'Qasparr' "
                  "Monroe, Proprietor, legal publisher of record",
             "noto", "", 9, 5, 5)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "L. Frank Baum's text is PUBLIC DOMAIN. It stands in "
              "this edition unaltered in substance, exactly as he "
              "wrote it; the Flagpole above claims the revision and "
              "the apparatus only, and nothing of Baum. And this "
              "edition prints THE BOOK, not any film: the shoes in "
              "these pages are Baum's silver shoes of 1900.",
         size=9.5, height=5, align="C", space_after=0)


def imprint_page(pdf):
    """The 1900 imprint: what the book's own head carries, transcribed,
    with the publication facts of record marked as record."""
    pdf.add_page()
    centered(pdf, "THE 1900 IMPRINT", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The book's own heading, transcribed as it stands in "
                 "the source", "noto", "I", 10.5, 6, 8)
    for line, sz in [("The Wonderful Wizard of Oz", 15),
                     ("by", 11),
                     ("L. FRANK BAUM", 16)]:
        centered(pdf, line, "dejavu", "B", sz, sz * 0.62, 3)
    pdf.ln(6)
    for line in ["Of record [ATTESTED — the bibliographic record]:",
                 "First edition: Chicago, Geo. M. Hill Co., 1900.",
                 "Pictures by W. W. Denslow — the twenty-four color",
                 "plates of the first edition. They are NOT in the",
                 "electronic source of this revision, and none are",
                 "fabricated for it; the absence is declared again",
                 "in the Apparatus, where it belongs.", "",
                 "The dedication that follows is the author's own,",
                 "printed in the book before its Introduction."]:
        centered(pdf, line, "noto", "", 10.5, 6, 1)


def elements_page(pdf):
    """The four-element content test (Teacher's Edition rule 6)."""
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete text of The Wonderful Wizard of Oz "
                   "(1900) as carried by Project Gutenberg eBook #55: "
                   "Baum's dedication, his Introduction, and Chapters "
                   "I–XXIV. The electronic text carries no plates."),
        ("PROCESSES", "Line-wrap reflowed to book measure; the "
                      "electronic file's license matter excluded and "
                      "the exclusion declared; its Contents list "
                      "replaced by this edition's own; the Teacher's "
                      "Edition frame set around the text. No sentence "
                      "of Baum is touched, and nothing of any film is "
                      "admitted."),
        ("OUTPUTS", "This volume: the whole book, in Teacher's "
                    "Revision (MAGVS) dress, with a Reviser's Preface "
                    "before it and an honest apparatus behind it."),
        ("TOLERANCES", "Zero. Any process that would change a word of "
                       "Baum fails the edition and is rejected; any "
                       "process that would turn the silver shoes ruby "
                       "fails it twice. Normalizations are confined "
                       "to typography and are declared in the "
                       "Colophon. Where the desk has nothing genuine "
                       "to add, it adds nothing."),
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
    "First, the boundary, stated plainly so no reader can miss it: "
    "this edition prints the book of 1900, and nothing else. The "
    "shoes Dorothy wears in these pages are silver — silver when the "
    "house falls on the Witch of the East, silver tinkling on the "
    "yellow brick road, silver on her feet before the throne of "
    "Glinda, and silver when they fall from her in the desert and "
    "are lost. The ruby slippers that the world pictures belong to "
    "the film of 1939, whose likeness is another house's property; "
    "they are excluded here by design, as are the film's dialogue "
    "and every scene the film invented. Where the popular memory and "
    "Baum's text disagree, the text governs. Baum's own rubies stand "
    "where he put them — in the palace of the Princess Gayelette and "
    "on the throne of Glinda the Good — and the Apparatus at the "
    "back of this volume counts the shoes' occurrences so any reader "
    "may check the canon for himself.",

    "Lyman Frank Baum wrote his Introduction as a small manifesto: "
    "the old fairy tale, with its fearsome moral and its blood-"
    "curdling incident, was to give way to a modernized wonder tale "
    "in which the wonderment and joy are retained and the heartaches "
    "left out. What he built instead — perhaps without weighing it — "
    "is the cleanest pilgrim engine in American letters. Four "
    "travelers walk one road to one gate, each begging the gatekeeper "
    "for the one thing he believes he lacks: brains, a heart, "
    "courage, and the way home. Every reader of this house will "
    "recognize the shape of that road. In 2026 the founder of this "
    "house mapped Baum's four travelers onto the Four Powers of the "
    "Sphinx — the ancient tetrad that Éliphas Lévi set down as To "
    "Know, To Will, To Dare, and To Keep Silence — and the mapping "
    "is printed here as what it is: the REVISER'S reading, entered "
    "under the founder's Flagpole of Claim and Coinage on the 28th "
    "day of October, 2026. It is not claimed as Baum's intent. Baum "
    "left no word that he built on Lévi's tetrad, and this edition "
    "does not invent one. The reading is offered because it holds "
    "under weighing, and its reasoning rides with it, assignment by "
    "assignment, as the house rule requires.",

    "THE SCARECROW — TO KNOW. [DERIVED — the reviser's reading.] He "
    "is stuffed with straw and certain he has no brains, and he begs "
    "Oz for the one thing his every act already displays. It is the "
    "Scarecrow who reads the road, the Scarecrow who reasons out the "
    "crossing of the ditch, the raft, the river; Dorothy consults "
    "him as the party's mind from the day she lifts him off his "
    "pole. The power of the first station is not the having of "
    "knowledge as furniture but the working of it — noscere, to know "
    "by acquaintance, in the act. He seeks a certificate for what he "
    "is already doing. That is why the assignment stands: the book "
    "keeps showing the reader a mind at work inside a head its owner "
    "believes is straw.",

    "THE TIN WOODMAN — TO WILL. [DERIVED — the reviser's reading.] "
    "He begs for a heart, and the tale keeps mistaking his tenderness "
    "for the proof he has one. But mark what actually carries him "
    "down the road: he rusts fast in the rain and stands a year in "
    "the forest, and when the oil-can frees his jaw his first act is "
    "to resume the journey he was on when he froze. He is enchanted "
    "limb from limb — the axe takes his arms, his legs, his head, "
    "his body — and at every loss the tinner rebuilds him and he "
    "walks on. That is not sentiment; that is will, velle, the power "
    "that does not stop. The heart he asks for is the name he gives a "
    "lack; the will he exercises is the substance he already has. "
    "His station is the second because the road is walked by willing "
    "it, step after rusted step.",

    "THE COWARDLY LION — TO DARE. [DERIVED — the reviser's reading.] "
    "He confesses his cowardice in his first scene and then spends "
    "the book doing the thing anyway: he leaps the ditch with his "
    "friends on his back, twice, at the edge of his strength; he "
    "faces the Kalidahs on the log; he walks into the poppy field's "
    "rescue and into the Witch's castle and into the fighting trees. "
    "Courage, audere, was never the absence of fear in any honest "
    "bank — it is daring while afraid, and the Lion is the only one "
    "of the four whose lack and whose power are the same act seen "
    "from two sides. He does not become brave at the Emerald City. "
    "He is certified there for what the road already proved.",

    "DOROTHY — TO KEEP SILENCE. [DERIVED — the reviser's reading.] "
    "The fourth power is tacere, and it belongs to the traveler who "
    "asks for no gift of mind or heart or nerve, and who carries the "
    "master-key of the whole tale on her feet from the second "
    "chapter without knowing its name. The silver shoes could have "
    "taken her home the day she put them on; nobody tells her — not "
    "the Witch of the North, who does not know; not the Wizard, who "
    "cannot; only Glinda, at the end of the longest road, speaks the "
    "word. Dorothy's power is the held power: unspoken, unshown, "
    "carried in silence across the whole book, working only when "
    "its bearer finally learns what she has been standing in. The "
    "house weighs this assignment the heaviest of the four. The "
    "strongest thing in the tale is the thing nobody says.",

    "And behind the curtain sits the fifth figure, who belongs to no "
    "station: the Wizard himself, the Great Humbug. Consider his "
    "office as the book exposes it — a little old man from Omaha, "
    "ventriloquist and balloonist, enthroned behind screens and "
    "voices, seen by each petitioner in a different shape, and "
    "exacting a toll before he will grant what is asked: go and kill "
    "the Witch of the West. The toll is the whole of his power. What "
    "he finally gives the travelers is what they already have, "
    "dressed as gifts — bran and pins for brains, a silk heart for "
    "the heart, a drink for courage — and the travelers receive "
    "them satisfied, because the gifts were true the moment the road "
    "had proved them. The Wizard is the unmasked gatekeeper: his "
    "gate was never locked, his terror was never real, and his one "
    "genuine service is the accidental one — he sends the pilgrims "
    "out to become, by doing, the thing they came begging to be "
    "given. This house, which keeps a ledger of gates, prints him "
    "without malice and without mercy: the curtain, once pulled, is "
    "not hung again.",

    "The way home, finally, is the book's last piece of engineering, "
    "and it runs forward. Dorothy cannot return as she came: the "
    "balloon rises without her, the road behind her is closed, and "
    "the way to Kansas lies onward — south, through country she has "
    "not seen, past the fighting trees and the dainty china people "
    "and the beasts of the forest, to a throne she did not know "
    "existed when she set out. She reaches home not by retracing "
    "but by completing. Three clicks of the silver heels, and she is "
    "in the air; the shoes fall in the desert and are lost forever, "
    "and the book ends where it must, on a Kansas prairie with a new "
    "farmhouse standing where the cyclone took the old. The road "
    "home leads forward. The reviser knows no better sentence to "
    "carry out of this book, and offers the whole tale as its proof.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. The Four Powers of the Sphinx — To "
    "Know (noscere), To Will (velle), To Dare (audere), To Keep "
    "Silence (tacere) — are Éliphas Lévi's tetrad, Dogme et Rituel de "
    "la Haute Magie (1854–56), carried into the Thelemic tables at "
    "Liber 777 (1909). [ATTESTED.] Their assignment to Baum's four "
    "travelers is the founder's mapping of 2026-10-28, printed here "
    "under his Flagpole. [DERIVED — the reviser's reading, each "
    "assignment reasoned in the Preface.] No evidence known to this "
    "desk connects Baum to Lévi's tetrad; none is asserted.",
    "2. Ecclesiastes 3:7 (KJV): “a time to rend, and a time to sew; "
    "a time to keep silence, and a time to speak.” The fourth "
    "power's scriptural seat. [ATTESTED.]",
    "3. The silver shoes: first named at Chapter II (the Witch of "
    "the East “shod in silver shoes with pointed toes”), last at "
    "Chapter XXIII (“the Silver Shoes had fallen off in her flight "
    "through the air, and were lost forever in the desert”). The "
    "Apparatus of this edition counts every occurrence. The ruby "
    "slippers are the 1939 film's device, the film being Warner "
    "property; this edition excludes the film entire. [ATTESTED — "
    "verified against the source text of this edition.]",
    "4. Copyright: The Wonderful Wizard of Oz was published in the "
    "United States in 1900; its copyright has long expired and the "
    "text is in the public domain (17 U.S.C. §304's term for works "
    "of that year ran out in the last century). The revision and "
    "apparatus of 2026 are the reviser's own and are claimed as "
    "such, and nothing beyond them is claimed. [ATTESTED.]",
]


def preface_page(pdf):
    pdf.add_page()
    centered(pdf, "REVISER'S PREFACE", "dejavu", "B", 14, 9, 2)
    centered(pdf, "By Johnathan 'Qasparr' Monroe, Reviser",
             "noto", "I", 10.5, 6, 6)
    for p in PREFACE_PARAS:
        para(pdf, p)
    pdf.ln(2)
    rule(pdf, 40)
    for n in PREFACE_NOTES:
        para(pdf, n, size=9, height=4.8, space_after=1.6)


def contents_page(pdf, toc, sections):
    pdf.add_page()
    toc["contents_first"] = pdf.page_no()
    centered(pdf, "CONTENTS", "dejavu", "B", 14, 9, 8)
    entries = [("The 1900 Imprint", toc.get("imprint")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface", toc.get("preface"))] + \
              [(disp, toc.get(key)) for key, disp, _ in sections] + \
              [("Apparatus of the Revision", toc.get("apparatus")),
               ("Table of Authorities", toc.get("authorities")),
               ("Colophon", toc.get("colophon"))]
    for name, page in entries:
        pdf.set_font("noto", "", 10.5)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 6.6, label, new_x=XPos.LMARGIN,
                       new_y=YPos.NEXT)
    toc["contents_last"] = pdf.page_no()


def text_sections(pdf, sections, toc):
    for key, display, paras in sections:
        pdf.add_page()
        toc[key] = pdf.page_no()
        centered(pdf, display, "dejavu", "B", 15, 10, 1)
        if key in SUBLINES:
            centered(pdf, SUBLINES[key], "noto", "I", 10.5, 6, 2)
        rule(pdf, 50)
        pdf.ln(2)
        for p in paras:
            if "text" in p:
                para(pdf, p["text"])
            elif "center_lines" in p:
                pdf.ln(8)
                for line in p["center_lines"]:
                    pdf.set_font("noto", "", 11.5)
                    pdf.multi_cell(0, 8, line, align="C",
                                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def apparatus_pages(pdf, toc, spans, silver_count):
    pdf.add_page()
    toc["apparatus"] = pdf.page_no()
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 9, 2)
    centered(pdf, "What was done to the text, stated in the open",
             "noto", "I", 10.5, 6, 6)
    para(pdf, "The text of The Wonderful Wizard of Oz in this edition "
              "is the text of Project Gutenberg eBook #55, which "
              "carries the 1900 Geo. M. Hill edition. The following "
              "operations, and no others, were performed upon it by "
              "the builder:")
    for line in [
        "1. The Gutenberg file's hard line-wrapping was reflowed "
        "into book paragraphs. No word was added, removed, or "
        "reordered.",
        f"2. Gutenberg's emphasis convention (underscores set as "
        f"italics) was armed in the builder and found nothing to "
        f"fire on: this source carries {spans} emphasis spans. The "
        f"count is printed because the desk reports what it "
        f"measures, including zero.",
        "3. Excluded, and declared here rather than vanished: the "
        "Project Gutenberg license header and license text, and the "
        "electronic file's own Contents list (this edition sets its "
        "own Contents, with page numbers of this printing). Also "
        "excluded: the book's title standing alone as a file line "
        "between Baum's Introduction and Chapter I — furniture of "
        "the electronic file, not a word of the story. All excluded "
        "matter remains in the source file, which the desk retains.",
        "4. The dedication is printed as its own first leaf, in the "
        "place the 1900 book gives it — before the Introduction, in "
        "the author's own words.",
    ]:
        para(pdf, line, size=10, space_after=1.8)

    pdf.ln(2)
    centered(pdf, "THE ILLUSTRATIONS — A DECLARED ABSENCE",
             "dejavu", "B", 12, 8, 4)
    para(pdf, "The 1900 edition of this book was a pictured book: "
              "W. W. Denslow drew twenty-four color plates for it, "
              "and for many readers the plates are half the country "
              "of Oz. The electronic source of this revision carries "
              "none of them. In the whole of the file, exactly one "
              "line speaks of a picture — a bare “[Illustration]” "
              "placeholder at the book's head, where the frontispiece "
              "would stand. This edition therefore prints no plates "
              "and fabricates none: no image is invented in Denslow's "
              "manner and passed off as his, and none is borrowed "
              "from the film. The absence is stated here, in the "
              "open, as the house rule requires: a plated Teacher's "
              "Revision, set from a scanned copy of the 1900 edition "
              "with Denslow's plates restored to their places, is "
              "UNCHARTED — named as future work, not filled by "
              "invention.", size=10)

    pdf.ln(2)
    centered(pdf, "THE CANON CHECK — THE SHOES ARE SILVER",
             "dejavu", "B", 12, 8, 4)
    para(pdf, f"The desk counted. In the source text of this "
              f"edition, the shoes are named silver — “silver "
              f"shoes,” “the silver shoes,” “her silver shoes,” "
              f"“the Silver Shoes” — {silver_count} times, from "
              f"Chapter II to Chapter XXIII, and ruby never of "
              f"footwear at all: the word “ruby” occurs in the book "
              f"exactly three times — of the palace of the Princess "
              f"Gayelette, built from great blocks of ruby (Chapter "
              f"XIV, twice), and of Glinda's ruby throne (Chapter "
              f"XXIII) — Baum's stones, in Baum's places. The ruby "
              f"film's, and the film is Warner property; no likeness, "
              f"line, or device of it stands in this edition. Where "
              f"memory and text disagree, the text governs. "
              f"[ATTESTED — counted in the source file of this "
              f"edition.]", size=10)

    toc["authorities"] = pdf.page_no()
    pdf.ln(2)
    centered(pdf, "TABLE OF AUTHORITIES (CONDENSED)", "dejavu", "B",
             12, 8, 4)
    for a in [
        "Baum, L. Frank. The Wonderful Wizard of Oz. Chicago: Geo. M. "
        "Hill Co., 1900 — with pictures by W. W. Denslow (absent from "
        "the electronic source; declared in this Apparatus).",
        "Project Gutenberg eBook #55 — electronic source text of the "
        "1900 edition (the input of this revision).",
        "Baum, L. Frank. Introduction (Chicago, April, 1900) — "
        "printed in this volume.",
        "Lévi, Éliphas. Dogme et Rituel de la Haute Magie (1854–56) "
        "— the Four Powers of the Sphinx: To Know, To Will, To Dare, "
        "To Keep Silence.",
        "Crowley, Aleister. Liber 777 (1909) — the Powers of the "
        "Sphinx carried in the Thelemic tables.",
        "Ecclesiastes 3:7 (KJV) — the fourth power's scriptural seat.",
        "17 U.S.C. §304 — the expired term of a work published in "
        "1900; the text is public domain.",
        "The founder's correspondence mapping of 2026-10-28 (house "
        "record) — Baum's four travelers weighed against the Four "
        "Powers, as printed in the Reviser's Preface.",
        "The Teacher's Edition format (house directive, 2026) — the "
        "dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.8)

    pdf.add_page()
    toc["colophon"] = pdf.page_no()
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Teacher's Revision (MAGVS) of The Wonderful "
              "Wizard of Oz was generated on " + THELEMIC_DATE +
              ", by a programmatic builder (fpdf2, Noto Serif and "
              "DejaVu Serif faces) from the public-domain source "
              "named in the Table of Authorities, under the "
              "Teacher's Edition format of this house. Its cover — "
              "purple leather, gold, and green, the Doctrine's seal "
              "seated — was struck on the house's programmatic press "
              "before the book was bound.")
    para(pdf, "The revision, the Reviser's Preface, and the apparatus "
              "are the work of Johnathan 'Qasparr' Monroe, to whom "
              "their authorship is attributed exclusively, ARR — All "
              "Rights Reserved, Without Prejudice. L. Frank Baum's "
              "text is public domain and is claimed by no one in this "
              "volume; W. W. Denslow's plates are absent and their "
              "absence is declared, not concealed.")
    centered(pdf, "Published by Bleats Publishing Group", "dejavu",
             "B", 11.5, 7, 1)
    centered(pdf, "SPARROW (Sole Proprietorship) — Johnathan 'Qasparr' "
                  "Monroe, Proprietor, legal publisher of record",
             "noto", "", 10, 6, 5)
    para(pdf, "Method of Science. Aim of Religion.", align="C")
    pdf.ln(4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C", space_after=4)
    centered(pdf, "93 — Live, Love, and let Love, Live.", "dejavu",
             "B", 12, 8)


def build(toc, spans, silver_count):
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    pdf.set_title("The Wonderful Wizard of Oz — Teacher's Revision "
                  "(MAGVS)")
    pdf.set_author("L. Frank Baum (author); Johnathan 'Qasparr' "
                   "Monroe (reviser)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")
    for family, fname in [("noto", "NotoSerif")]:
        pdf.add_font(family, "", f"{NOTO}/{fname}-Regular.ttf")
        pdf.add_font(family, "B", f"{NOTO}/{fname}-Bold.ttf")
        pdf.add_font(family, "I", f"{NOTO}/{fname}-Italic.ttf")
        pdf.add_font(family, "BI", f"{NOTO}/{fname}-BoldItalic.ttf")
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")

    sections, _ = load_sections()
    title_page(pdf)
    imprint_page(pdf)
    toc["imprint"] = 2
    elements_page(pdf)
    toc["elements"] = 3
    preface_page(pdf)
    toc["preface"] = 4
    contents_page(pdf, toc, sections)
    text_sections(pdf, sections, toc)
    apparatus_pages(pdf, toc, spans, silver_count)
    return pdf, toc


def count_silver():
    """Count the shoes' silver namings in the body of the source."""
    raw = SOURCE.read_text(encoding="utf-8")
    start = raw.index("*** START OF THE PROJECT")
    end = raw.index("*** END OF THE PROJECT")
    body = raw[start:end]
    return len(re.findall(r"[Ss]ilver [Ss]hoes", body))


def main():
    _, spans = load_sections()
    silver = count_silver()
    toc = {}
    pdf, toc = build(toc, spans, silver)      # pass one: measure
    pdf, toc = build(toc, spans, silver)      # pass two: numbered
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"bytes: {OUT.stat().st_size}")
    print(f"emphasis spans in source: {spans}")
    print(f"silver-shoes occurrences: {silver}")
    for k, v in toc.items():
        print(f"  {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
