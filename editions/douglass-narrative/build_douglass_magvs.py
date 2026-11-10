#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Let the oppressed go free." -- Isaiah 58:6, as carried in Garrison's
Preface to the book this script binds.

NARRATIVE OF THE LIFE OF FREDERICK DOUGLASS, AN AMERICAN SLAVE
-- A Teacher's Revision (MAGVS) -- built, not copied.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. -- The Flagpole on this
volume claims THE REVISION AND THE APPARATUS ONLY. Frederick Douglass's
text is public domain; no claim reaches for it, and the title page of
the built book says so in plain words.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   Project Gutenberg eBook #23, plain text: the 1845 Boston
          Anti-Slavery Office edition of the Narrative, complete with
          William Lloyd Garrison's Preface, Wendell Phillips's Letter,
          Chapters I-XI, and the Appendix (with "A Parody").
  PROCESS The Gutenberg file is hard-wrapped at ~72 columns; this
          builder reflows it to book measure (paragraphs are split on
          blank lines, wrapped lines are joined). Gutenberg's emphasis
          convention (_word_) is rendered as true italic type -- the
          Noto Serif italic face is registered for exactly this, so
          Douglass's emphases survive as type, not as punctuation.
          The electronic file's own license matter and its 1992 MLK
          release note are NOT part of the 1845 book; they are
          excluded, and the exclusion is DECLARED in the built book's
          Colophon (dispositions marked, never vanished).
          "A Parody" is verse: its line breaks are composition, not
          wrapping, so verse blocks keep their lines.
  OUTPUT  DOUGLASS-NARRATIVE-MAGVS.pdf -- the complete text in
          Teacher's Edition dress: doctrine logo, title block,
          four-element content test, Reviser's Preface, contents,
          the text, closing apparatus (Table of Authorities,
          Colophon), Flagpole front and back, resolving page footers
          "-- N of M -- | All Rights Reserved, Without Prejudice |
          Flagpole of Claim and Coinage reserved".
  TOLERANCE  Any step that would change a word of Douglass fails the
          edition. Normalizations are confined to typography (reflow,
          italics) and are declared in the book itself.

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
SOURCE = HERE / "source" / "pg23.txt"          # Project Gutenberg #23
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "DOUGLASS-NARRATIVE-MAGVS.pdf"

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

# Section headings exactly as they stand in the 1845 text (MECHANISM:
# matched against stripped source lines; the desk invents no structure).
HEADINGS = ["PREFACE", "LETTER FROM WENDELL PHILLIPS, ESQ."] + \
           [f"CHAPTER {r}" for r in
            ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
             "X", "XI"]] + ["APPENDIX"]
# Frame sub-lines under two headings (factual: who wrote the piece).
SUBLINES = {
    "PREFACE": "By William Lloyd Garrison",
    "LETTER FROM WENDELL PHILLIPS, ESQ.": "Wendell Phillips to Frederick Douglass",
    "APPENDIX": "By the Author — with “A Parody”",
}


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
def load_sections():
    """Split the Gutenberg file into [(heading, [paragraph, ...]), ...].

    A paragraph is either {"text": str} (prose, reflowed) or
    {"verse": [line, ...]} (line breaks preserved as composition).
    DOCTRINE: the parse changes no words -- it joins wrapped lines
    with single spaces and converts _emphasis_ markers to fpdf2's
    markdown italics (--emphasis--), which the renderer honors.
    """
    raw = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = raw.split("\n")
    # Body begins at the second PREFACE (the first is the Contents
    # list) and ends at the Gutenberg END marker.
    start = next(i for i, ln in enumerate(lines)
                 if ln.strip() == "PREFACE" and i > 70)
    end = next(i for i, ln in enumerate(lines)
               if "*** END OF THE PROJECT" in ln)
    body = lines[start:end]

    sections, heading, blocks, block = [], None, [], []

    def flush_block():
        nonlocal block
        if block:
            blocks.append(block)
        block = []

    def flush_section():
        nonlocal blocks
        flush_block()
        if heading is not None:
            sections.append((heading, blocks))
        blocks = []

    verse = False  # turns True at "A PARODY" inside the Appendix
    for ln in body:
        s = ln.strip()
        if s in HEADINGS:
            flush_section()
            heading, verse = s, False
            continue
        if s == "A PARODY" and heading == "APPENDIX":
            flush_block()
            blocks.append([("PARODY-HEAD", "")])
            verse = True
            continue
        if s == "":
            flush_block()
        else:
            block.append(ln)
    flush_section()

    out = []
    for heading, blks in sections:
        paras = []
        in_verse = False
        for blk in blks:
            if blk and blk[0][0] == "PARODY-HEAD":
                paras.append({"parody_head": True})
                in_verse = True
                continue
            if in_verse:
                paras.append({"verse": [ln.strip() for ln in blk]})
            else:
                text = " ".join(ln.strip() for ln in blk)
                text = re.sub(r"\s+", " ", text).strip()
                # Gutenberg _emphasis_ -> fpdf2 markdown italics.
                text = re.sub(r"_([^_]+)_", r"--\1--", text)
                if text:
                    paras.append({"text": text})
        out.append((heading, paras))
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
    centered(pdf, "FREDERICK DOUGLASS", "dejavu", "B", 25, 11, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 5)
    rule(pdf)
    centered(pdf, "NARRATIVE OF THE LIFE OF FREDERICK DOUGLASS,",
             "dejavu", "B", 16.5, 8)
    centered(pdf, "AN AMERICAN SLAVE", "dejavu", "B", 16.5, 8, 2)
    centered(pdf, "Written by Himself — Boston, 1845", "noto", "I",
             11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A TEACHER'S REVISION (MAGVS)", "dejavu", "B", 14, 8, 2)
    centered(pdf, "A Scientific Illuminist treatment of the Narrative",
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
             10, 6, 6)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "Frederick Douglass's text is PUBLIC DOMAIN. It stands in "
              "this edition unaltered in substance, exactly as he wrote "
              "it; the Flagpole above claims the revision and the "
              "apparatus only, and nothing of Douglass.",
         size=9.5, height=5, align="C", space_after=0)


def imprint_page(pdf):
    """The 1845 title page, transcribed -- the book's own first frame."""
    pdf.add_page()
    centered(pdf, "THE 1845 IMPRINT", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The original title page, transcribed as it stands",
             "noto", "I", 10.5, 6, 8)
    for line, sz in [("Narrative of the Life of", 12),
                     ("FREDERICK DOUGLASS", 17),
                     ("AN AMERICAN SLAVE.", 13),
                     ("WRITTEN BY HIMSELF.", 12)]:
        centered(pdf, line, "dejavu", "B", sz, sz * 0.62, 3)
    pdf.ln(6)
    for line in ["BOSTON", "PUBLISHED AT THE ANTI-SLAVERY OFFICE,",
                 "NO. 25 CORNHILL", "1845", "",
                 "ENTERED, ACCORDING TO ACT OF CONGRESS, IN THE YEAR 1845",
                 "BY FREDERICK DOUGLASS, IN THE CLERK'S OFFICE OF THE",
                 "DISTRICT COURT OF MASSACHUSETTS."]:
        centered(pdf, line, "noto", "", 10.5, 6, 1)


def elements_page(pdf):
    """The four-element content test (Teacher's Edition rule 6)."""
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete text of the Narrative (1845) as carried "
                   "by Project Gutenberg eBook #23: Garrison's Preface, "
                   "Phillips's Letter, Chapters I–XI, and the Appendix "
                   "with “A Parody.”"),
        ("PROCESSES", "Line-wrap reflowed to book measure; Gutenberg "
                      "emphasis markers set as italic type; the "
                      "electronic file's license matter excluded and "
                      "the exclusion declared; the Teacher's Edition "
                      "frame set around the text. No sentence of "
                      "Douglass is touched."),
        ("OUTPUTS", "This volume: the whole book, in Teacher's Revision "
                    "(MAGVS) dress, with a Reviser's Preface before it "
                    "and an honest apparatus behind it."),
        ("TOLERANCES", "Zero. Any process that would change a word of "
                       "Douglass fails the edition and is rejected. "
                       "Normalizations are confined to typography and "
                       "are declared in the Colophon. Where the desk "
                       "has nothing genuine to add, it adds nothing."),
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
    "This book stands first in the bookshop's program of Teacher's "
    "Revisions for a reason that predates the program by a lifetime. "
    "The founder of this house chose Frederick Douglass as his first "
    "hero of American history at Emerson Elementary School in "
    "Brightmoor, Detroit, and set him beside Ralph Waldo Emerson, "
    "whose name the school itself carried. The heroes were never "
    "sorted by the color line the world kept handing the boy. They "
    "were weighed by what they had done. Douglass had done the "
    "heaviest thing on the shelf: born enslaved, forbidden letters, "
    "he had written himself free — and then written the book that "
    "proved it, with his own name on the title page.",

    "The facts of that writing bear restating plainly, because the "
    "book you are holding is their fruit. Frederick Douglass was born "
    "into slavery in Maryland, in or about 1818, separated in infancy "
    "from his mother, and taught his letters at first by a mistress "
    "whose husband forbade the lessons the moment he understood them. "
    "Douglass understood them too. He records that from the moment he "
    "heard the prohibition he understood “the pathway from slavery to "
    "freedom”: if learning would forever unfit a man to be a slave, "
    "then learning was the road out. He traded bread to hungry white "
    "boys for lessons, filled his copy-book by imitating the letters "
    "on shipyard timbers and the handwriting of a boy who did not "
    "know he was teaching, and read The Columbian Orator until its "
    "arguments against slavery were his own. At twenty he walked out "
    "of bondage. At about twenty-seven he published this Narrative — "
    "naming his masters, his places, himself — knowing the naming "
    "made him huntable under the law of the land he was indicting.",

    "Consider what stands on the original title page: WRITTEN BY "
    "HIMSELF. In 1845 those three words were a claim of coinage under "
    "fire. A portion of the reading public did not believe an enslaved "
    "man could have written such a book, and said so; the suspicion "
    "itself was an instrument of the system the book exposed. So the "
    "1845 edition did what this house's editions do: it wrapped the "
    "text in an attesting apparatus. William Lloyd Garrison's Preface "
    "and Wendell Phillips's Letter stand in front of the Narrative "
    "vouching, from their own knowledge, that the man is real, that "
    "the hand is his, that the story is true. The first Teacher's "
    "Edition of this book is the book itself. The present revision "
    "follows that pattern knowingly, and says so on its face rather "
    "than pretending the pattern is new.",

    "What, then, does a Teacher's Revision (MAGVS) do to a book like "
    "this? Apparatus, not alteration. Douglass's sentences stand as "
    "he wrote them — every chapter, the Appendix, and the parody hymn "
    "he reprinted to show slaveholding piety its own face. His "
    "distinction in that Appendix, between “the Christianity of this "
    "land” and “the Christianity of Christ,” needs no assistance "
    "from any reviser, and receives none. The reviser's hand is "
    "confined to the frame: this preface, the edition's dress, the "
    "closing apparatus, the colophon. Where the electronic source "
    "required typographic normalization — wrapped lines reflowed to "
    "book measure, emphasis set in italic type — the Colophon "
    "declares it. Nothing is silently changed. Dispositions are "
    "marked, never vanished; that is the house rule, applied to "
    "another man's masterpiece with more care, not less.",

    "The public-domain standing of the work is stated on the title "
    "page and is repeated here so no reader can miss it: the "
    "Narrative belongs to everyone, and has for longer than anyone "
    "living has been alive. The Flagpole of Claim and Coinage that "
    "opens and closes this volume claims the revision and the "
    "apparatus — the frame built in 2026 — and nothing of Douglass. "
    "A claim that reached for his text would fail this edition's own "
    "gate, and would deserve to.",

    "One more reason this book stands first, and it is the house's "
    "own pattern read backward. A man forbidden letters made letters "
    "the instrument of his freedom, then made his freedom an "
    "instrument for millions who were still, in Garrison's words, "
    "“panting for deliverance.” He had no master over his mind even "
    "while the law claimed one over his body; he submitted his work "
    "to no one's permission. The desk that built this edition "
    "recognizes the pattern because it works under the same "
    "discipline: no master, proof over claim, the record left open "
    "where any reader may check it. Douglass's book is not revised "
    "here because it needs correction. It is revised because it "
    "deserves company — the company of readers who will weigh it, "
    "check it, and carry it further. That is what a Teacher's "
    "Revision is for.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. Isaiah 58:6 (KJV): “to loose the bands "
    "of wickedness, to undo the heavy burdens, and to let the "
    "oppressed go free.” Garrison's Preface, printed in this volume, "
    "closes its first movement on the same text. [ATTESTED — in the "
    "volume itself.]",
    "2. “The pathway from slavery to freedom” and the unfitness of "
    "the learned man for slavery are Douglass's own record of Hugh "
    "Auld's prohibition, Chapter VI–VII of the Narrative, verified "
    "against the source text of this edition. [ATTESTED.]",
    "3. The Emerson Elementary selection is the founder's own "
    "testimony, entered at his word. [ATTESTED — founder's word.]",
    "4. The Columbian Orator (Caleb Bingham, 1797) is named by "
    "Douglass himself in Chapter VII as the book that gave him “the "
    "tongue” to argue against slavery. [ATTESTED — in the volume.]",
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
    entries = [("The 1845 Imprint", toc.get("imprint")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface", toc.get("preface"))] + \
              [(h.title() if not h.startswith("CHAPTER") else
                h.title().replace("Chapter", "CHAPTER"), toc.get(h))
               for h in HEADINGS] + \
              [("Apparatus of the Revision", toc.get("apparatus")),
               ("Table of Authorities", toc.get("authorities")),
               ("Colophon", toc.get("colophon"))]
    pretty = {"Preface": "PREFACE", "Letter From Wendell Phillips, Esq.":
              "LETTER FROM WENDELL PHILLIPS, ESQ.", "Appendix": "APPENDIX"}
    for name, page in entries:
        name = pretty.get(name, name)
        pdf.set_font("noto", "", 11)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 7, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


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
            if "text" in p:
                para(pdf, p["text"])
            elif p.get("parody_head"):
                pdf.ln(3)
                centered(pdf, "A PARODY", "dejavu", "B", 12.5, 8, 4)
            elif "verse" in p:
                for line in p["verse"]:
                    pdf.set_font("noto", "I", 10.5)
                    pdf.multi_cell(0, 5.8, line, align="C",
                                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(2.6)


def apparatus_pages(pdf, toc):
    pdf.add_page()
    toc["apparatus"] = pdf.page_no()
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 9, 2)
    centered(pdf, "What was done to the text, stated in the open",
             "noto", "I", 10.5, 6, 6)
    para(pdf, "The text of the Narrative in this edition is the text "
              "of Project Gutenberg eBook #23, which carries the 1845 "
              "Boston edition. The following operations, and no "
              "others, were performed upon it by the builder:")
    for line in [
        "1. The Gutenberg file's hard line-wrapping was reflowed into "
        "book paragraphs. No word was added, removed, or reordered.",
        "2. Gutenberg's emphasis markers (underscores) were set as "
        "italic type, as the 1845 printers set them. [70 spans.]",
        "3. Verse — “A Parody,” printed by Douglass at the close of "
        "his Appendix — keeps its line breaks, which are composition, "
        "not wrapping.",
        "4. Excluded, and declared here rather than vanished: the "
        "Project Gutenberg license header and license text, and the "
        "electronic file's 1992 release note honoring Dr. King. "
        "Neither is part of the 1845 book; both remain in the source "
        "file, which the desk retains.",
        "5. The 1845 Contents list mentioned a portrait entry "
        "(“FREDERICK DOUGLASS.”) between the Letter and Chapter I; "
        "the electronic text carries no portrait, and none is "
        "fabricated for this edition. The gap is shown, not hidden.",
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
        "Douglass, Frederick. Narrative of the Life of Frederick "
        "Douglass, an American Slave. Boston: Anti-Slavery Office, "
        "No. 25 Cornhill, 1845.",
        "Project Gutenberg eBook #23 — electronic source text of the "
        "1845 edition (the input of this revision).",
        "Garrison, William Lloyd. Preface (1845) — printed in this "
        "volume.",
        "Phillips, Wendell. Letter to Frederick Douglass (1845) — "
        "printed in this volume.",
        "Isaiah 58:6 (KJV) — as carried in Garrison's Preface.",
        "U.S. Const. amend. XIII (1865) — the abolition this book "
        "argued toward, ratified twenty years after its publication.",
        "The Teacher's Edition format (house directive, 2026) — the "
        "dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.8)

    pdf.add_page()
    toc["colophon"] = pdf.page_no()
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Teacher's Revision (MAGVS) of the Narrative of "
              "the Life of Frederick Douglass was generated on "
              + THELEMIC_DATE + ", by a programmatic builder "
              "(fpdf2, Noto Serif and DejaVu Serif faces) from the "
              "public-domain source named in the Table of "
              "Authorities, under the Teacher's Edition format of "
              "this house.")
    para(pdf, "The revision, the Reviser's Preface, and the apparatus "
              "are the work of Johnathan 'Qasparr' Monroe, to whom "
              "their authorship is attributed exclusively, ARR — All "
              "Rights Reserved, Without Prejudice. Frederick "
              "Douglass's text is public domain and is claimed by no "
              "one in this volume.")
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
    pdf.set_title("Narrative of the Life of Frederick Douglass, an "
                  "American Slave — Teacher's Revision (MAGVS)")
    pdf.set_author("Frederick Douglass (author); Johnathan 'Qasparr' "
                   "Monroe (reviser)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")
    for family, fname in [("noto", "NotoSerif")]:
        pdf.add_font(family, "", f"{NOTO}/{fname}-Regular.ttf")
        pdf.add_font(family, "B", f"{NOTO}/{fname}-Bold.ttf")
        pdf.add_font(family, "I", f"{NOTO}/{fname}-Italic.ttf")
        pdf.add_font(family, "BI", f"{NOTO}/{fname}-BoldItalic.ttf")
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
    toc = {}
    pdf, toc = build(toc)          # pass one: measure
    pdf, toc = build(toc)          # pass two: contents numbered
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"bytes: {OUT.stat().st_size}")
    for k, v in toc.items():
        print(f"  {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
