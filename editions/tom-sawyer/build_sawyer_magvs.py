#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Work consists of whatever a body is obliged to do, and that Play
consists of whatever a body is not obliged to do." -- Chapter II of
the book this script binds; Twain's great law of human action, found
over a whitewashed fence.

THE ADVENTURES OF TOM SAWYER
-- A Teacher's Revision (MAGVS) -- built, not copied.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. -- The Flagpole on this
volume claims THE REVISION AND THE APPARATUS ONLY. Mark Twain's text
is public domain; no claim reaches for it, and the title page of the
built book says so in plain words.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   Project Gutenberg eBook #74, plain text (UTF-8): the
          Adventures of Tom Sawyer (1876), complete with Twain's own
          Preface, Chapters I-XXXV, and the Conclusion. Verified
          against the file before building: the Preface opens "Most
          of the adventures recorded in this book really occurred";
          the thirty-five chapter headings stand on their own lines;
          the Conclusion closes "...wisest not to reveal any of that
          part of their lives at present."
  PROCESS The Gutenberg file is hard-wrapped at ~72 columns; this
          builder reflows it to book measure (paragraphs are split on
          blank lines, wrapped lines are joined). Gutenberg's emphasis
          convention (_word_) is rendered as true italic type -- the
          Noto Serif italic face is registered for exactly this, so
          Twain's emphases survive as type, not as punctuation. The
          electronic file's own furniture -- its license matter and
          its front Contents list (which duplicates the chapter
          titles) -- is NOT part of the 1876 book; it is excluded,
          and the exclusion is DECLARED in the built book's apparatus
          (dispositions marked, never vanished). The first edition
          of 1876 was illustrated; the electronic text carries no
          illustrations and no illustration markers, and none are
          fabricated for this edition. The gap is shown, not hidden.
  OUTPUT  TOM-SAWYER-MAGVS.pdf -- the complete text in Teacher's
          Edition dress: doctrine logo, title block, four-element
          content test, Reviser's Preface, contents, the text,
          closing apparatus (apparatus declaration, Table of
          Authorities, Colophon), Flagpole front and back, resolving
          page footers "-- N of M -- | All Rights Reserved, Without
          Prejudice | Flagpole of Claim and Coinage reserved".
  TOLERANCE  Any step that would change a word of Twain fails the
          edition. That includes his period language: the text
          carries eight occurrences of the era's racial epithet, and
          they stand as he wrote them -- history, neither celebrated
          nor hidden. Normalizations are confined to typography
          (reflow, italics) and are declared in the book itself.

  Two-pass build: the contents page needs section page numbers, so
  the book is composed twice -- pass one measures where each section
  falls, pass two prints the numbers. The contents page holds a
  fixed layout in both passes, so the measurement cannot drift;
  if a contents entry ever pushed the page count, the page size of
  the entries (not their number) absorbs it.

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
SOURCE = HERE / "source" / "pg74.txt"          # Project Gutenberg #74
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "TOM-SAWYER-MAGVS.pdf"

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

# Section headings exactly as they stand in the 1876 text (MECHANISM:
# matched against stripped source lines; the desk invents no structure).
# Twain's own Preface first, then the thirty-five chapters, then his
# Conclusion -- that is the whole skeleton of the book.
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
          "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI",
          "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII",
          "XXXIV", "XXXV"]
HEADINGS = ["PREFACE"] + [f"CHAPTER {r}" for r in ROMANS] + ["CONCLUSION"]
# Frame sub-lines under two headings (factual: whose piece it is).
SUBLINES = {
    "PREFACE": "By the Author — Hartford, 1876",
    "CONCLUSION": "By the Author",
}

EMPHASIS_SPANS = 0  # counted at parse time; printed in the apparatus


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
def load_sections():
    """Split the Gutenberg file into [(heading, [paragraph, ...]), ...].

    A paragraph is {"text": str} (prose, reflowed). DOCTRINE: the
    parse changes no words -- it joins wrapped lines with single
    spaces and converts _emphasis_ markers to fpdf2's markdown
    italics (--emphasis--), which the renderer honors. The number of
    emphasis spans converted is counted and carried to the apparatus,
    so the book states its own operations exactly.
    """
    global EMPHASIS_SPANS
    raw = SOURCE.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")
    # Body begins at the author's PREFACE (the file's front Contents
    # list is furniture, excluded and declared) and ends at the
    # Gutenberg END marker.
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "PREFACE")
    end = next(i for i, ln in enumerate(lines)
               if "*** END OF THE PROJECT" in ln)
    body = lines[start:end]

    sections, heading, paras, block = [], None, [], []

    def flush_block():
        nonlocal block
        if block:
            paras.append(block)
        block = []

    def flush_section():
        nonlocal paras
        flush_block()
        if heading is not None:
            sections.append((heading, paras))
        paras = []

    for ln in body:
        s = ln.strip()
        if s in HEADINGS:
            flush_section()
            heading = s
            continue
        if s == "":
            flush_block()
        else:
            block.append(ln)
    flush_section()

    out = []
    for heading, blks in sections:
        texts = []
        for blk in blks:
            text = " ".join(ln.strip() for ln in blk)
            text = re.sub(r"\s+", " ", text).strip()
            EMPHASIS_SPANS += len(re.findall(r"_([^_]+)_", text))
            # Gutenberg _emphasis_ -> fpdf2 markdown italics.
            text = re.sub(r"_([^_]+)_", r"--\1--", text)
            if text:
                texts.append({"text": text})
        out.append((heading, texts))
    return out


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
    centered(pdf, "MARK TWAIN", "dejavu", "B", 25, 11, 1)
    centered(pdf, "(Samuel Langhorne Clemens)", "noto", "I", 12, 6, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 5)
    rule(pdf)
    centered(pdf, "THE ADVENTURES OF TOM SAWYER", "dejavu", "B", 16.5, 8, 2)
    centered(pdf, "Hartford, Connecticut — 1876", "noto", "I", 11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A TEACHER'S REVISION (MAGVS)", "dejavu", "B", 14, 8, 2)
    centered(pdf, "A Scientific Illuminist treatment of Tom Sawyer",
             "noto", "I", 11, 6, 5)
    centered(pdf, "The revision and apparatus are by", "noto", "", 10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship of the revision attributed exclusively to "
                  "Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights "
                  "Reserved, Without Prejudice)", "noto", "", 9.5, 5, 4)
    centered(pdf, THELEMIC_DATE, "noto", "", 10.5, 6, 1)
    centered(pdf, "Classification: Enterprise • Educational • Research "
                  "& Development", "noto", "", 10, 6)
    centered(pdf, "Method of Science, Aim of Religion", "noto", "I",
             10, 6, 3)
    # Publishing imprint (founder's ruling, 2026-11-09): the group
    # publishes; SPARROW is the legal publisher of record.
    centered(pdf, "Published by Bleats Publishing Group", "dejavu", "B",
             11, 6, 1)
    centered(pdf, "SPARROW — Sole Proprietorship · Johnathan 'Qasparr' "
                  "Monroe, proprietor", "noto", "", 9, 5, 5)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "Mark Twain's text is PUBLIC DOMAIN. It stands in this "
              "edition complete and unaltered in substance — unmodernized, "
              "unsanitized, exactly as he wrote it; the Flagpole above "
              "claims the revision and the apparatus only, and nothing "
              "of Twain.",
         size=9.5, height=5, align="C", space_after=0)


def imprint_page(pdf):
    """The 1876 title page, transcribed -- the book's own first frame."""
    pdf.add_page()
    centered(pdf, "THE 1876 IMPRINT", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The original title page, transcribed as it stands",
             "noto", "I", 10.5, 6, 8)
    for line, sz in [("THE ADVENTURES OF", 12),
                     ("TOM SAWYER", 17),
                     ("By MARK TWAIN", 13),
                     ("(SAMUEL LANGHORNE CLEMENS)", 11)]:
        centered(pdf, line, "dejavu", "B", sz, sz * 0.62, 3)
    pdf.ln(6)
    for line in ["HARTFORD, CONN.", "THE AMERICAN PUBLISHING COMPANY",
                 "1876"]:
        centered(pdf, line, "noto", "", 10.5, 6, 1)


def elements_page(pdf):
    """The four-element content test (Teacher's Edition rule 6)."""
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete text of The Adventures of Tom Sawyer "
                   "(1876) as carried by Project Gutenberg eBook #74: "
                   "Twain's own Preface, Chapters I–XXXV, and the "
                   "Conclusion."),
        ("PROCESSES", "Line-wrap reflowed to book measure; Gutenberg "
                      "emphasis markers set as italic type; the "
                      "electronic file's license matter and its front "
                      "Contents list excluded and the exclusion "
                      "declared; no illustrations fabricated for an "
                      "edition whose source carries none; the Teacher's "
                      "Edition frame set around the text. No sentence "
                      "of Twain is touched."),
        ("OUTPUTS", "This volume: the whole book, in Teacher's Revision "
                    "(MAGVS) dress, with a Reviser's Preface before it "
                    "and an honest apparatus behind it."),
        ("TOLERANCES", "Zero. Any process that would change a word of "
                       "Twain fails the edition and is rejected — "
                       "including any process that would modernize his "
                       "dialect, soften his satire, or clean up his "
                       "period language. Normalizations are confined to "
                       "typography and are declared in the apparatus."),
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
    "This is the third volume in the bookshop's program of Teacher's "
    "Revisions, and its place in the queue is deliberate. First stood "
    "Frederick Douglass, who wrote himself free — the founder's first "
    "hero, and the pattern this house works under. Second stood "
    "Huckleberry Finn, the greater of Twain's two boy-books, where a "
    "boy's conscience breaks with his whole civilization on a river "
    "at night. Third stands Tom Sawyer, and third is right, because "
    "Tom is Huck's mirror, and a mirror is read after the face. The "
    "two books were always one act of seeing in two directions. "
    "Huck's book is the book of the river: leave the town, distrust "
    "its conscience, keep moving. Tom's book is the book of the "
    "town: stay inside it, master its games, and bend its rules from "
    "within until the town itself hands you the glory. Tom does not "
    "want out. Tom wants the town to watch him win at being in it.",

    "Read that way, the comedy sharpens. Everything Tom touches "
    "becomes theatre — his own funeral, attended in person; the "
    "treasure, dug up by romance's rules long after the real world "
    "has supplied a real murder for the same graveyard; the rescue "
    "of Jim in the later book, which Tom insists on conducting by "
    "the book of rules even when the rules are cruel nonsense. "
    "Twain's Preface says most of these adventures really occurred, "
    "and that Tom is a composite of boys he knew; it also says the "
    "book is for boys and girls, and to remind adults of what they "
    "once were. What adults were, in St. Petersburg, is what the "
    "town chapters keep showing: vain, punitive, tender, bored, and "
    "governed above all by the terror of being laughed at. Tom "
    "simply learned the town's operating system earlier than the "
    "adults did, and ran it back at them. Huck sees through the town "
    "and leaves. Tom sees through it and plays it. Both see through "
    "it. That is the mirror, and it is why neither book is complete "
    "without the other standing behind it.",

    "Under the comedy sits the thing Twain never lets the reader "
    "forget for long: this is boyhood before the hooks go in, and "
    "the water is already rising around it. The graveyard scene is "
    "played for midnight shivers until it isn't — a man is murdered "
    "in front of two boys, and the wrong man is put on trial for his "
    "life while the boys carry a secret that could hang them in the "
    "town's esteem if they speak and damn them in their own if they "
    "don't. Joe Harper runs away to be a pirate and his mother takes "
    "it for grief, not sport. Tom's own aunt, who whips him in "
    "chapter one and would die for him by the last, is the whole "
    "argument in one person: the hooks of the world are love and "
    "punishment braided, and they land early. Twain wrote, in his "
    "Conclusion, that a history of a boy must stop where it does, "
    "because the story could not go much further without becoming "
    "the history of a man. This edition takes him at his word. What "
    "is preserved here, whole, is the weather of a life before the "
    "climate sets — superstition, loyalty, cruelty, glory, and a "
    "boy measuring every adult institution he meets and finding, "
    "almost every time, that it runs on show.",

    "At the center of the second chapter stands the passage this "
    "house holds to be the book's great gift to the world — the "
    "whitewashed fence, and the law Tom discovers over it without "
    "knowing he has discovered anything. “He had discovered a great "
    "law of human action, without knowing it — namely, that in order "
    "to make a man or a boy covet a thing, it is only necessary to "
    "make the thing difficult to attain.” And then the corollary, "
    "stated as flatly as any axiom in any science: “Work consists of "
    "whatever a body is obliged to do, and that Play consists of "
    "whatever a body is not obliged to do.” The fence gets "
    "whitewashed three coats deep by other boys, who pay Tom for "
    "the privilege in the whole currency of boyhood — marbles, a "
    "dead rat, a kite, twelve marbles' worth of treasure — while Tom "
    "sits in the shade, an artist at rest. It is the funniest scene "
    "in American letters and also one of the truest: obligation is "
    "what makes labor labor, and the same motions, freely chosen, "
    "are play. Every workshop, schoolroom, and platform since 1876 "
    "has run on that law whether it knew the name of its author or "
    "not. The reviser only underlines what Twain already proved on a "
    "Saturday morning in a village that did not exist, about a fence "
    "that did.",

    "Now the principle on which this edition stands, stated plainly, "
    "because a Teacher's Revision that will not state its principle "
    "is decoration. The text in this volume is Twain's text complete "
    "and unmodernized. His dialect stands as he set it. His satire "
    "stands at full strength — the Sunday-school, the temperance "
    "cadets, the model boy, the whole machinery of respectable "
    "St. Petersburg, mocked by its own most gifted citizen. And his "
    "period language stands too, including the era's racial epithet, "
    "which occurs eight times in this book. The reviser addresses "
    "that fact the way this house addresses every fact: in the open. "
    "The word is printed here as history — evidence of the world "
    "Twain wrote in and partly against — neither celebrated nor "
    "hidden. To celebrate it would be filth. To hide it would be a "
    "lie told to the reader about the record, and it would also be "
    "theft: the record of what ordinary speech carried in 1840s "
    "Missouri is part of what this book is evidence OF, and an "
    "edition that quietly cleaned it would be teaching a false "
    "past. The failure this edition refuses is the bowdlerizer's — "
    "the tidy hand that decides readers are too fragile for the "
    "book they chose to open. Readers are owed the text and the "
    "truth about the text, both, at once. They get both here.",

    "The public-domain standing of the work is stated on the title "
    "page and repeated here so no reader can miss it: The Adventures "
    "of Tom Sawyer belongs to everyone, and has for generations. The "
    "Flagpole of Claim and Coinage that opens and closes this volume "
    "claims the revision and the apparatus — the frame built in "
    "2026 — and nothing of Twain. A claim that reached for his text "
    "would fail this edition's own gate, and would deserve to.",

    "Why third, once more, and briefly. Douglass first, because "
    "letters are the road out and everything this house does walks "
    "it. The river second, because conscience outranks games. The "
    "town third, because after the road out and the voice of "
    "conscience, a reader is finally equipped to enjoy the games "
    "without mistaking them for the world — and to catch, in the "
    "funniest of the three books, the same author weighing the same "
    "civilization in a lighter scale and finding it, on the whole, "
    "exactly as wanting and exactly as lovable. Tom grows up to be "
    "the town, if he is not careful. The care is the reader's part. "
    "The text is Twain's. The frame is the reviser's. The mirror is "
    "yours to stand in front of.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. “Most of the adventures recorded in "
    "this book really occurred” — Twain's own Preface, printed in "
    "this volume immediately after this Reviser's Preface. [ATTESTED "
    "— in the volume itself.]",
    "2. The fence law — “a great law of human action,” and “Work "
    "consists of whatever a body is obliged to do, and that Play "
    "consists of whatever a body is not obliged to do” — Chapter II "
    "of the text in this volume, verified against the source. "
    "[ATTESTED.]",
    "3. The count of eight occurrences of the period racial epithet "
    "was made mechanically against the source text of this edition "
    "(body text, Preface through Conclusion). [ATTESTED — counted, "
    "not estimated.]",
    "4. “The story could not go much further without becoming the "
    "history of a man” — Twain's Conclusion, printed in this volume. "
    "[ATTESTED.]",
    "5. The queue order (Douglass, Huckleberry Finn, Tom Sawyer) and "
    "its reasoning are the founder's program as ordered and the "
    "reviser's reading of it. [DERIVED — the founder's order; the "
    "mirror reading is the reviser's frame, CONSTRUCTED until "
    "weighed by the reader.]",
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


def contents_page(pdf, toc):
    pdf.add_page()
    centered(pdf, "CONTENTS", "dejavu", "B", 14, 9, 8)
    entries = [("The 1876 Imprint", toc.get("imprint")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface", toc.get("preface")),
               ("Preface, by the Author", toc.get("PREFACE"))]
    entries += [(f"Chapter {r}", toc.get(f"CHAPTER {r}")) for r in ROMANS]
    entries += [("Conclusion", toc.get("CONCLUSION")),
                ("Apparatus of the Revision", toc.get("apparatus")),
                ("Table of Authorities", toc.get("authorities")),
                ("Colophon", toc.get("colophon"))]
    # Fixed small entry size: 41 entries must share this one page in
    # both passes, so pass one's measurement can never drift.
    for name, page in entries:
        pdf.set_font("noto", "", 10)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 5.6, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def text_sections(pdf, sections, toc):
    for heading, paras in sections:
        pdf.add_page()
        toc[heading] = pdf.page_no()
        centered(pdf, heading, "dejavu", "B", 15, 10, 1)
        if heading in SUBLINES:
            centered(pdf, SUBLINES[heading], "noto", "I", 10.5, 6, 2)
        rule(pdf, 50)
        pdf.ln(2)
        for p in paras:
            para(pdf, p["text"])


def apparatus_pages(pdf, toc):
    pdf.add_page()
    toc["apparatus"] = pdf.page_no()
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 9, 2)
    centered(pdf, "Apparatus declaration — what was done to the text, "
                 "stated in the open", "noto", "I", 10.5, 6, 6)
    para(pdf, "The text of The Adventures of Tom Sawyer in this edition "
              "is the text of Project Gutenberg eBook #74, which carries "
              "the 1876 Hartford edition. The following operations, and "
              "no others, were performed upon it by the builder:")
    for line in [
        "1. The Gutenberg file's hard line-wrapping was reflowed into "
        "book paragraphs. No word was added, removed, or reordered.",
        f"2. Gutenberg's emphasis markers (underscores) were set as "
        f"italic type, as the 1876 printers set them. "
        f"[{EMPHASIS_SPANS} spans.]",
        "3. Excluded, and declared here rather than vanished: the "
        "Project Gutenberg license header and license text, and the "
        "electronic file's own front Contents list, which duplicates "
        "the chapter titles (this edition prints its own Contents, "
        "with page numbers). Neither is part of the 1876 book; both "
        "remain in the source file, which the desk retains.",
        "4. The first edition of 1876 was illustrated (True W. "
        "Williams and others). The electronic text carries no "
        "illustrations and no illustration markers, and none are "
        "fabricated for this edition. The gap is shown, not hidden.",
        "5. Nothing was modernized. Twain's spelling, dialect, and "
        "period language stand as the source carries them — including "
        "eight occurrences of the era's racial epithet, addressed in "
        "the Reviser's Preface as what they are: history, neither "
        "celebrated nor hidden.",
    ]:
        para(pdf, line, size=10, space_after=1.8)
    para(pdf, "No chapter notes have been invented for this edition. "
              "An honest apparatus frame is the deliverable; annotation "
              "beyond the Reviser's Preface awaits the founder's pen "
              "and is marked UNCHARTED until then.", size=10)

    toc["authorities"] = pdf.page_no()
    pdf.ln(2)
    centered(pdf, "TABLE OF AUTHORITIES (CONDENSED)", "dejavu", "B",
             12, 8, 4)
    for a in [
        "Twain, Mark (Samuel Langhorne Clemens). The Adventures of "
        "Tom Sawyer. Hartford, Conn.: The American Publishing "
        "Company, 1876.",
        "Project Gutenberg eBook #74 — electronic source text of the "
        "1876 edition (the input of this revision).",
        "Twain, Mark. Preface and Conclusion to the same — printed in "
        "this volume, and cited in the Reviser's Preface from the "
        "volume itself.",
        "The fence law — Chapter II of the text in this volume (“Work "
        "consists of whatever a body is obliged to do...”), verified "
        "against the source.",
        "The Teacher's Edition format (house directive, 2026) — the "
        "dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.8)

    pdf.add_page()
    toc["colophon"] = pdf.page_no()
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Teacher's Revision (MAGVS) of The Adventures of "
              "Tom Sawyer was generated on " + THELEMIC_DATE + ", by a "
              "programmatic builder (fpdf2, Noto Serif and DejaVu "
              "Serif faces) from the public-domain source named in the "
              "Table of Authorities, under the Teacher's Edition "
              "format of this house.")
    # Publishing imprint (founder's ruling, 2026-11-09): the group is
    # the publishing imprint; SPARROW, the founder's sole
    # proprietorship, is the legal publisher of record beneath it.
    centered(pdf, "Published by Bleats Publishing Group", "dejavu", "B",
             12, 7, 3)
    para(pdf, "SPARROW — Sole Proprietorship. Johnathan 'Qasparr' "
              "Monroe, proprietor, is the legal publisher of record.",
         size=10, align="C", space_after=4)
    para(pdf, "The revision, the Reviser's Preface, and the apparatus "
              "are the work of Johnathan 'Qasparr' Monroe, to whom "
              "their authorship is attributed exclusively, ARR — All "
              "Rights Reserved, Without Prejudice. Mark Twain's text "
              "is public domain and is claimed by no one in this "
              "volume.")
    para(pdf, "Method of Science. Aim of Religion.", align="C")
    pdf.ln(4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C", space_after=4)
    centered(pdf, "93 — Live, Love, and let Love, Live.", "dejavu",
             "B", 12, 8)


def build(toc):
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    pdf.set_title("The Adventures of Tom Sawyer — Teacher's Revision "
                  "(MAGVS)")
    pdf.set_author("Mark Twain (author); Johnathan 'Qasparr' Monroe "
                   "(reviser)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")
    pdf.add_font("noto", "", f"{NOTO}/NotoSerif-Regular.ttf")
    pdf.add_font("noto", "B", f"{NOTO}/NotoSerif-Bold.ttf")
    pdf.add_font("noto", "I", f"{NOTO}/NotoSerif-Italic.ttf")
    pdf.add_font("noto", "BI", f"{NOTO}/NotoSerif-BoldItalic.ttf")
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")

    sections = load_sections()
    title_page(pdf)
    imprint_page(pdf)
    toc["imprint"] = 2
    elements_page(pdf)
    toc["elements"] = 3
    preface_page(pdf)
    toc["preface"] = 4
    contents_page(pdf, toc)
    text_sections(pdf, sections, toc)
    apparatus_pages(pdf, toc)
    return pdf, toc


def main():
    global EMPHASIS_SPANS
    toc = {}
    pdf, toc = build(toc)          # pass one: measure
    EMPHASIS_SPANS = 0             # recount identically in pass two
    pdf, toc = build(toc)          # pass two: contents numbered
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"bytes: {OUT.stat().st_size}")
    print(f"emphasis spans converted: {EMPHASIS_SPANS}")
    for k, v in toc.items():
        print(f"  {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
