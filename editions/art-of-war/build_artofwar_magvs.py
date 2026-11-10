#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Supreme excellence consists in breaking the enemy's resistance
without fighting." -- Sun Tzŭ, The Art of War, III. 2, in the Giles
translation printed in this volume.

THE ART OF WAR -- A Teacher's Revision (MAGVS) -- built, not copied.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. -- The Flagpole on this
volume claims THE REVISION AND THE APPARATUS ONLY. Sun Tzŭ's text is
the work of antiquity, and Lionel Giles's translation and notes
(1910) are public domain; no claim reaches for either, and the title
page of the built book says so in plain words.

MECHANISM / DOCTRINE -- how this builder works, and why:

  INPUT   Project Gutenberg eBook #132, plain text: Lionel Giles's
          1910 translation of Sun Tzŭ, complete -- his own Preface,
          his Introduction in its seven parts (Sun Wu and his Book;
          The Text of Sun Tzŭ; The Commentators; Appreciations of
          Sun Tzŭ; Apologies for War; Bibliography; Footnotes), and
          the thirteen chapters with Giles's critical notes standing
          in place after the sections they gloss.
  PROCESS The Gutenberg file is hard-wrapped at ~72 columns; this
          builder reflows it to book measure (paragraphs are split on
          blank lines, wrapped lines are joined). Gutenberg's emphasis
          convention (_word_) is rendered as true italic type -- the
          Noto Serif italic face is registered for exactly this, so
          Giles's emphases survive as type, not as punctuation. The
          emphasis spans in the printed body are COUNTED by the
          builder and the count is printed in the book's apparatus:
          the desk states what it measured, not what it assumed.
          The electronic file's own furniture is NOT part of the
          1910 book: the Project Gutenberg license header and license
          text, and the etext converter's own preface (Bob Sutton's
          conversion note), are excluded, and the exclusion is
          DECLARED in the built book's apparatus (dispositions
          marked, never vanished). Giles's arrangement is kept
          entire: his Introduction's subheads stand as subheads in
          the flow, and his footnotes to the Introduction stand
          gathered under his own "Footnotes" head, exactly as the
          etext carries them.
  OUTPUT  THE-ART-OF-WAR-MAGVS.pdf -- the complete Giles edition in
          Teacher's Edition dress: doctrine logo, title block,
          four-element content test, Reviser's Preface, contents,
          the text, closing apparatus (Table of Authorities,
          Colophon), Flagpole front and back, resolving page footers
          "-- N of M -- | All Rights Reserved, Without Prejudice |
          Flagpole of Claim and Coinage reserved".
  TOLERANCE  Any step that would change a word of Sun Tzŭ in
          Giles's English fails the edition. Normalizations are
          confined to typography (reflow, italics) and are declared
          in the book itself.

  Two-pass build: the contents page needs unit page numbers, so the
  book is composed twice -- pass one measures where each unit falls,
  pass two prints the numbers. The contents page is exactly one page
  in both passes, so the measurement cannot drift.

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
SOURCE = HERE / "source" / "pg132.txt"          # Project Gutenberg #132
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "THE-ART-OF-WAR-MAGVS.pdf"

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

# Unit headings exactly as they stand in the 1910 text (MECHANISM:
# matched against stripped source lines; the desk invents no
# structure). The Introduction's own subheads, in Giles's order.
INTRO_SUBHEADS = ["Sun Wu and his Book", "The Text of Sun Tzŭ",
                  "The Commentators", "Appreciations of Sun Tzŭ",
                  "Apologies for War", "Bibliography", "Footnotes"]
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
          "X", "XI", "XII", "XIII"]
CHAPTER_RE = re.compile(r"^Chapter ([IVX]+)\.\s+(.+)$")

STATS = {"spans": 0}   # emphasis spans in the printed body, counted


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
def load_units():
    """Split the Gutenberg file into units.

    Returns [(kind, key, title, blocks), ...] where kind is one of
    "giles_preface", "introduction", "chapter"; blocks are dicts
    {"text": str} (prose, reflowed) or {"subhead": str} (Giles's
    subheads inside the Introduction, kept in the flow).
    DOCTRINE: the parse changes no words -- it joins wrapped lines
    with single spaces and converts _emphasis_ markers to fpdf2's
    markdown italics (--emphasis--), which the renderer honors.
    """
    raw = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = raw.split("\n")
    # Body begins at the second "Preface by Lionel Giles" (the first
    # is the Contents list) and ends at the Gutenberg END marker.
    start = next(i for i, ln in enumerate(lines)
                 if ln.strip() == "Preface by Lionel Giles" and i > 100)
    end = next(i for i, ln in enumerate(lines)
               if "*** END OF THE PROJECT" in ln)
    body = lines[start:end]

    units, kind, key, title, blocks, block = [], None, None, None, [], []

    def flush_block():
        nonlocal block
        if block:
            blocks.append(block)
        block = []

    def flush_unit():
        nonlocal blocks
        flush_block()
        if kind is not None:
            units.append((kind, key, title, blocks))
        blocks = []

    for ln in body:
        s = ln.strip()
        m = CHAPTER_RE.match(s)
        if s == "Preface by Lionel Giles":
            flush_unit()
            kind, key, title = "giles_preface", "giles_preface", \
                "PREFACE BY LIONEL GILES"
            continue
        if s == "INTRODUCTION":
            flush_unit()
            kind, key, title = "introduction", "introduction", \
                "INTRODUCTION"
            continue
        if kind == "introduction" and s in INTRO_SUBHEADS:
            flush_block()
            blocks.append([("SUBHEAD", s)])
            continue
        if m:
            flush_unit()
            kind, key = "chapter", f"ch{m.group(1)}"
            title = s
            continue
        if s == "":
            flush_block()
        else:
            block.append(ln)
    flush_unit()

    # Census assertions (the gate): Giles's Preface, the Introduction
    # with all seven of its parts, and exactly XIII chapters in order.
    kinds = [u[0] for u in units]
    assert kinds[0] == "giles_preface" and kinds[1] == "introduction", \
        f"front units out of order: {kinds[:2]}"
    chapters = [u for u in units if u[0] == "chapter"]
    assert [u[1] for u in chapters] == [f"ch{r}" for r in ROMANS], \
        f"chapter census failed: {[u[1] for u in chapters]}"
    subs = [b[0][1] for u in units if u[0] == "introduction"
            for b in u[3] if b and b[0][0] == "SUBHEAD"]
    assert subs == INTRO_SUBHEADS, f"introduction subheads: {subs}"

    out = []
    for kind, key, title, blks in units:
        paras = []
        for blk in blks:
            if blk and blk[0][0] == "SUBHEAD":
                paras.append({"subhead": blk[0][1]})
                continue
            text = " ".join(ln.strip() for ln in blk)
            text = re.sub(r"\s+", " ", text).strip()
            STATS["spans"] += len(re.findall(r"_[^_]+_", text))
            # Gutenberg _emphasis_ -> fpdf2 markdown italics.
            text = re.sub(r"_([^_]+)_", r"--\1--", text)
            if text:
                paras.append({"text": text})
        out.append((kind, key, title, paras))
    return out


# ----------------------------------------------------------------------
# The book
# ----------------------------------------------------------------------
class Book(FPDF):
    folio_total = None    # page count, learned from pass one

    def footer(self):
        # Teacher's Edition footer, resolving on every page.
        self.set_y(-14)
        self.set_font("dejavu", "", 7.5)
        self.set_text_color(90, 90, 90)
        total = self.folio_total if self.folio_total else "{nb}"
        self.cell(0, 8, FOOTER.format(n=self.page_no(), m=total),
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
    pdf.ln(5)
    centered(pdf, "SUN TZU", "dejavu", "B", 25, 11, 1)
    centered(pdf, "Author", "noto", "I", 12, 6, 4)
    rule(pdf)
    centered(pdf, "THE ART OF WAR", "dejavu", "B", 16.5, 8, 2)
    centered(pdf, "The oldest military treatise in the world",
             "noto", "I", 11.5, 6, 5)
    rule(pdf)
    centered(pdf, "Translated from the Chinese, with Introduction "
                  "and Critical Notes, by", "noto", "", 10.5, 6)
    centered(pdf, "LIONEL GILES, M.A.", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Assistant in the Department of Oriental Printed "
                  "Books and MSS. in the British Museum — 1910",
             "noto", "I", 10, 5.5, 5)
    centered(pdf, "A TEACHER'S REVISION (MAGVS)", "dejavu", "B", 14, 8, 2)
    centered(pdf, "A Scientific Illuminist treatment of the Giles "
                  "edition", "noto", "I", 11, 6, 4)
    centered(pdf, "The revision and apparatus are by", "noto", "",
             10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship of the revision attributed exclusively to "
                  "Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights "
                  "Reserved, Without Prejudice)", "noto", "", 9.5, 5, 3)
    centered(pdf, THELEMIC_DATE, "noto", "", 10.5, 6, 1)
    centered(pdf, "Classification: Enterprise • Educational • Research "
                  "& Development", "noto", "", 10, 6)
    centered(pdf, "Method of Science, Aim of Religion", "noto", "I",
             10, 6, 3)
    centered(pdf, PUBLISHER, "dejavu", "B", 10.5, 6)
    centered(pdf, PROPRIETOR, "noto", "", 9, 5, 5)
    para(pdf, FLAGPOLE, size=9.5, height=5, align="C", space_after=4)
    para(pdf, "Sun Tzŭ's text is the work of antiquity and belongs to "
              "everyone; Lionel Giles's translation, Introduction, and "
              "notes (1910) are PUBLIC DOMAIN in the United States. "
              "Both stand in this edition unaltered in substance; the "
              "Flagpole above claims the revision and the apparatus "
              "only, and nothing of Sun Tzŭ or of Giles.",
         size=9.5, height=5, align="C", space_after=0)


def imprint_page(pdf):
    """The 1910 title page and dedication, transcribed -- the book's
    own first frame, as the edition received it."""
    pdf.add_page()
    centered(pdf, "THE 1910 IMPRINT", "dejavu", "B", 13, 8, 2)
    centered(pdf, "The original title page, transcribed as it stands",
             "noto", "I", 10.5, 6, 8)
    for line, sz in [("Sun Tzŭ", 12),
                     ("on", 11),
                     ("THE ART OF WAR", 17),
                     ("THE OLDEST MILITARY TREATISE IN THE WORLD", 11),
                     ("Translated from the Chinese with Introduction "
                      "and Critical Notes", 11),
                     ("BY", 11),
                     ("LIONEL GILES, M.A.", 14),
                     ("Assistant in the Department of Oriental Printed "
                      "Books and MSS. in the British Museum", 10),
                     ("1910", 12)]:
        centered(pdf, line, "dejavu", "B", sz, sz * 0.62, 3)
    pdf.ln(8)
    rule(pdf, 50)
    centered(pdf, "THE DEDICATION OF 1910", "dejavu", "B", 11.5, 7, 4)
    for line in ["To my brother",
                 "CAPTAIN VALENTINE GILES, R.G.",
                 "in the hope that",
                 "a work 2400 years old",
                 "may yet contain lessons worth consideration",
                 "by the soldier of today",
                 "this translation",
                 "is affectionately dedicated."]:
        centered(pdf, line, "noto", "", 10.5, 6, 1)


def elements_page(pdf):
    """The four-element content test (Teacher's Edition rule 6)."""
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete Giles edition of 1910 as carried by "
                   "Project Gutenberg eBook #132: Giles's Preface, his "
                   "Introduction in its seven parts with its footnotes, "
                   "and the thirteen chapters of Sun Tzŭ with Giles's "
                   "critical notes standing in place."),
        ("PROCESSES", "Line-wrap reflowed to book measure; Gutenberg "
                      "emphasis markers set as italic type; the "
                      "electronic file's own furniture (license matter, "
                      "the converter's preface) excluded and the "
                      "exclusion declared; the Teacher's Edition frame "
                      "set around the text. No sentence of Sun Tzŭ or "
                      "of Giles is touched."),
        ("OUTPUTS", "This volume: the whole book, in Teacher's "
                    "Revision (MAGVS) dress, with a Reviser's Preface "
                    "before it and an honest apparatus behind it."),
        ("TOLERANCES", "Zero. Any process that would change a word "
                       "of the translation fails the edition and is "
                       "rejected. Normalizations are confined to "
                       "typography and are declared in the apparatus. "
                       "Where the desk has nothing genuine to add, it "
                       "adds nothing."),
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
    "This book stands sixth in the bookshop's program of Teacher's "
    "Revisions, and it changes the shelf's weather. The five before "
    "it are testimony, conscience, boyhood, myth, and the "
    "Commonwealth: what a man suffered and wrote, what a boy decided "
    "on a river, what a child dreamed down a road of yellow brick, "
    "what a philosopher built out of fear. Sun Tzŭ is the shelf's "
    "cold eye — the oldest military treatise in the world, thirteen "
    "short chapters that have been read in secret by rulers, "
    "generals, and insurgents for roughly twenty-four centuries. It "
    "is here because the house that publishes it works under "
    "doctrine in a contested world, and this is the founding text "
    "of strategy itself: the first book that treats conflict not as "
    "fate or glory but as a problem to be solved with knowledge, "
    "measure, and economy.",

    "Read it first for what it actually teaches, because the popular "
    "summary — war is deception, strike hard — is the least of it. "
    "The treatise's summit is a refusal: “Hence to fight and conquer "
    "in all your battles is not supreme excellence; supreme "
    "excellence consists in breaking the enemy's resistance without "
    "fighting.” Everything in the book bends toward that economy. "
    "Chapter II is an accountant's chapter, counting the cost of a "
    "campaign in treasure, food, and broken chariots until prolonged "
    "war stands exposed as a kind of defeat. Chapter I opens not "
    "with a trumpet but with a reckoning — five constant factors, "
    "seven comparisons, the weighing done in advance: “the general "
    "who wins a battle makes many calculations in his temple ere "
    "the battle is fought.” And the final chapter, on spies, is "
    "really a chapter about knowledge: “this foreknowledge cannot "
    "be elicited from spirits; it cannot be obtained inductively "
    "from experience, nor by any deductive calculation” — it must "
    "be gotten from men who know. The ideal Sun Tzŭ holds up is a "
    "sovereign who would rather not fight at all, and who arranges "
    "the ground, the information, and the alliances so completely "
    "that fighting becomes the enemy's worst option and his own "
    "last.",

    "Where the house agrees with the old general, it agrees on the "
    "record, and the agreements are not small. [DERIVED — the "
    "reviser's reading.] First: measure before motion. The temple "
    "calculations of Chapter I are the ancestor of this house's own "
    "discipline — weigh first, prove at the gate, let the number "
    "end the argument; no claim acts until it is justified. Second: "
    "knowledge from evidence, not from omens. Sun Tzŭ's "
    "foreknowledge comes from men and observation, never from "
    "spirits; the house's standard is the same shape — attested, "
    "derived, constructed, each tier labeled, nothing conjured. "
    "Third: the true target is the plan, not the person. The acme "
    "is to break resistance, to balk the design, to take the state "
    "whole rather than ruin it — the house's audits likewise weigh "
    "works, texts, and numbers, and its law is that proofs gate "
    "rewards, never rights; persons are not the quarry. A strategy "
    "that wins without destroying what it wins is, in the house's "
    "own idiom, duty multiplied with the right, not severed from "
    "it.",

    "Where the house parts from Sun Tzŭ, it parts on the record "
    "too, and the parting is principled, not polite. [CONSTRUCTED — "
    "the reviser's frame.] The treatise founds itself on a "
    "sentence the house cannot build on: “All warfare is based on "
    "deception.” Deception is Sun Tzŭ's element — feigned disorder, "
    "simulated weakness, the bait and the ambush — and inside a "
    "war, against an enemy in arms, the desk does not pretend the "
    "doctrine is ineffective; twenty-four centuries have weighed "
    "it. But the founder's root law, the Line, runs the other way: "
    "public is public and private is private, transparency toward "
    "power and privacy toward the person, no hidden terms, no "
    "telemetry games played on one's own people. A house whose "
    "charter is that no voice shall be silenced does not practice "
    "feigning against its own users, ever; deception may describe "
    "a battlefield, but it is refused as a constitution. The spy "
    "chapters part company the same way: Sun Tzŭ's five classes of "
    "secret agent are an instrument the house will study as "
    "history and decline as policy within its own walls, where the "
    "rule is no logs, no spying, the user above all. And beneath "
    "both partings sits the deepest one: Sun Tzŭ's sovereign is "
    "the state, and the people's substance is his to spend; the "
    "house's sovereign is the user, and the seat of command is "
    "inverted. The desk prints the disagreement in the open "
    "because a Teacher's Revision that only applauds its author "
    "is a courtier, not a teacher.",

    "A word for the translator, whose work is half of what stands "
    "in this volume. Lionel Giles — Assistant in the Department of "
    "Oriental Printed Books and Manuscripts in the British Museum, "
    "as his title page styles him — published this translation in "
    "1910, and it remained the scholarly standard in English for "
    "half a century. What he built was not a bare rendering: it is "
    "the Chinese master's thirteen chapters carried inside a "
    "critical edition — his own Preface, an Introduction in seven "
    "parts that weighs Sun Wu's historicity, the text's "
    "transmission, the ancient commentators, and the literature of "
    "war in China, and notes throughout that argue with the "
    "commentators and with his predecessor translators in the "
    "open. This revision keeps Giles's arrangement entire: his "
    "Introduction stands in his order, his notes stand where he "
    "set them, and his name stands on the title page as "
    "translator, with Sun Tzŭ first and largest as author. The one "
    "loss the edition cannot repair is the electronic file's own: "
    "its converter, working without Chinese, transliterated the "
    "characters Giles printed, and recorded the loss honestly in "
    "his own preface to the etext. That preface is the file's, not "
    "the 1910 book's, and it is excluded here — declared in the "
    "apparatus, not vanished. The Chinese characters are restored "
    "nowhere by conjecture. What Giles wrote in English stands "
    "complete.",

    "The public-domain standing is doubled and is stated plainly. "
    "The treatise itself is the work of antiquity — traditionally "
    "ascribed to Sun Wu, general of Wu in the age of the Spring "
    "and Autumn annals — and belongs to everyone, as it has for "
    "two dozen centuries. Giles's translation, Introduction, and "
    "notes, published in 1910, are public domain in the United "
    "States. The Flagpole of Claim and Coinage that opens and "
    "closes this volume claims the revision and the apparatus — "
    "the frame built in 2026 — and nothing of the ancient master "
    "or of his translator. This book is revised not because it "
    "needs correction but because it deserves weighing: the "
    "founder's house reads its enemies' classics and its own "
    "doctrine with the same instrument, and prints both the "
    "agreements and the partings where any reader can check them.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. “Supreme excellence consists in "
    "breaking the enemy's resistance without fighting”: Chapter "
    "III, § 2 (Attack by Stratagem), verified against the source "
    "text of this edition. [ATTESTED — in the volume itself.]",
    "2. “All warfare is based on deception”: Chapter I, § 18 "
    "(Laying Plans). “The general who wins a battle makes many "
    "calculations in his temple ere the battle is fought”: Chapter "
    "I, § 26. “This foreknowledge cannot be elicited from spirits…”: "
    "Chapter XIII, § 5 (The Use of Spies). All verified against the "
    "source. [ATTESTED.]",
    "3. The Line (“Public is public. Private is private. Period.”), "
    "the house telemetry rule (none unless the user opts in, "
    "revocable at any time), and the motto NVLLA VOX TACEBITVR are "
    "the founder's recorded doctrine (2026-10-28). [ATTESTED — "
    "founder's record.]",
    "4. The map of agreements and partings drawn in the third and "
    "fourth movements of this Preface is the reviser's reading, "
    "offered for weighing, not attributed to Sun Tzŭ or to Giles. "
    "[CONSTRUCTED — the reviser's frame.]",
    "5. Giles's standing and the 1910 date are from the edition's "
    "own title page, transcribed in this volume; his service at "
    "the British Museum is stated there in his own styling. "
    "[ATTESTED — in the volume.]",
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


def pretty_title(title):
    """Contents-page form of a chapter title: source caps lowered to
    title case, small words kept small."""
    t = title.title()
    for small in [" And ", " By ", " On ", " Of ", " The ", " A "]:
        t = t.replace(small, small.lower())
    return t


def contents_page(pdf, toc, units):
    pdf.add_page()
    centered(pdf, "CONTENTS", "dejavu", "B", 14, 9, 8)
    entries = [("The 1910 Imprint", toc.get("imprint")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface", toc.get("preface")),
               ("Preface by Lionel Giles", toc.get("giles_preface")),
               ("Introduction (by Lionel Giles)",
                toc.get("introduction"))]
    for kind, key, title, _ in units:
        if kind == "chapter":
            m = CHAPTER_RE.match(title)
            entries.append((f"CHAPTER {m.group(1)} — "
                            f"{pretty_title(m.group(2))}",
                            toc.get(key)))
    entries += [("Apparatus of the Revision", toc.get("apparatus")),
                ("Table of Authorities", toc.get("authorities")),
                ("Colophon", toc.get("colophon"))]
    for name, page in entries:
        pdf.set_font("noto", "", 11)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 7, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


CHAPTER_SUBLINES = {
    "giles_preface": "By Lionel Giles — the translator's own frame",
    "introduction": "By Lionel Giles — in seven parts, with his "
                    "footnotes",
}


def text_units(pdf, units, toc):
    for kind, key, title, paras in units:
        pdf.add_page()
        toc[key] = pdf.page_no()
        centered(pdf, title, "dejavu", "B", 15, 10, 1)
        if key in CHAPTER_SUBLINES:
            centered(pdf, CHAPTER_SUBLINES[key], "noto", "I", 10.5,
                     6, 2)
        rule(pdf, 50)
        pdf.ln(2)
        for p in paras:
            if "text" in p:
                para(pdf, p["text"])
            elif "subhead" in p:
                pdf.ln(3)
                centered(pdf, p["subhead"], "dejavu", "B", 11.5, 7, 4)


def apparatus_pages(pdf, toc):
    pdf.add_page()
    toc["apparatus"] = pdf.page_no()
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "What was done to the text, stated in the open",
             "noto", "I", 10.5, 6, 4)
    para(pdf, "The text in this edition is the text of Project "
              "Gutenberg eBook #132, which carries Lionel Giles's "
              "1910 edition of Sun Tzŭ complete. The following "
              "operations, and no others, were performed upon it by "
              "the builder:")
    for line in [
        "1. The Gutenberg file's hard line-wrapping was reflowed "
        "into book paragraphs. No word was added, removed, or "
        "reordered.",
        f"2. Gutenberg's emphasis markers (underscores) were set as "
        f"italic type, as emphasis stands in the printed 1910 "
        f"edition. [{STATS['spans']} spans, counted by the builder "
        f"in the body it printed.]",
        "3. Giles's arrangement is kept entire: his Preface, his "
        "Introduction in its seven parts (the subheads stand as "
        "subheads in the flow), and the thirteen chapters in his "
        "order. His critical notes stand in place after the "
        "sections they gloss, as the etext carries them; the "
        "Introduction's footnotes — page footnotes in print — stand "
        "gathered under his own “Footnotes” head at the close of "
        "the Introduction.",
        "4. Excluded, and declared here rather than vanished: the "
        "Project Gutenberg license header and license text, and the "
        "etext converter's own preface (Bob Sutton's note on the "
        "conversion). Neither is part of the 1910 book; both remain "
        "in the source file, which the desk retains.",
        "5. The Chinese characters of the 1910 edition do not "
        "survive in the electronic text: its converter, by his own "
        "honest account in the excluded preface, transliterated "
        "them. They are restored in this edition nowhere, and by "
        "no conjecture. The loss is the file's, and it is recorded "
        "here so no reader mistakes the transliteration for the "
        "translator's page.",
        "6. The 1910 Contents page is not reprinted; this "
        "edition's Contents lists the same units in the same "
        "order, in the house dress.",
    ]:
        para(pdf, line, size=10, space_after=1.0)
    para(pdf, "No chapter notes have been invented for this "
              "edition. Giles's notes are the notes; annotation "
              "beyond the Reviser's Preface awaits the founder's "
              "pen and is marked UNCHARTED until then.", size=10,
         space_after=1.4)

    toc["authorities"] = pdf.page_no()
    pdf.ln(1)
    centered(pdf, "TABLE OF AUTHORITIES (CONDENSED)", "dejavu", "B",
             12, 8, 3)
    for a in [
        "Sun Tzŭ (Sun Wu, traditionally). The Art of War — thirteen "
        "chapters, Chinese text of antiquity (c. 5th century B.C. "
        "by the traditional ascription; Giles's Introduction weighs "
        "the ascription in this volume).",
        "Giles, Lionel, M.A. Sun Tzŭ on the Art of War: The Oldest "
        "Military Treatise in the World. Translated from the "
        "Chinese with Introduction and Critical Notes. 1910.",
        "Project Gutenberg eBook #132 — electronic source text of "
        "the Giles edition (the input of this revision).",
        "The founder's doctrine records — THE-LINE-DOCTRINE and "
        "THE-THREE-GROUPS (2026) — cited in the Reviser's Preface "
        "for the house's agreements and partings, and for nothing "
        "of Sun Tzŭ.",
        "The Teacher's Edition format (house directive, 2026) — "
        "the dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.0)

    pdf.add_page()
    toc["colophon"] = pdf.page_no()
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Teacher's Revision (MAGVS) of The Art of War "
              "was generated on " + THELEMIC_DATE + ", by a "
              "programmatic builder (fpdf2, Noto Serif and DejaVu "
              "Serif faces) from the public-domain source named in "
              "the Table of Authorities, under the Teacher's "
              "Edition format of this house.")
    para(pdf, "The revision, the Reviser's Preface, and the "
              "apparatus are the work of Johnathan 'Qasparr' "
              "Monroe, to whom their authorship is attributed "
              "exclusively, ARR — All Rights Reserved, Without "
              "Prejudice. Sun Tzŭ's text is the work of antiquity "
              "and Lionel Giles's translation and notes are public "
              "domain; neither is claimed by anyone in this volume.")
    centered(pdf, PUBLISHER, "dejavu", "B", 10.5, 6)
    centered(pdf, PROPRIETOR, "noto", "", 9, 5, 4)
    para(pdf, "Method of Science. Aim of Religion.", align="C")
    pdf.ln(4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C", space_after=4)
    centered(pdf, "93 — Live, Love, and let Love, Live.", "dejavu",
             "B", 12, 8)


def build(toc, folio_total=None, units=None):
    Book.folio_total = folio_total
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    pdf.set_title("The Art of War — Teacher's Revision (MAGVS)")
    pdf.set_author("Sun Tzu (author); Lionel Giles (translator); "
                   "Johnathan 'Qasparr' Monroe (reviser)")
    pdf.set_creator("MAGVS bookshop builder — the founder's desk")
    for family, fname in [("noto", "NotoSerif")]:
        pdf.add_font(family, "", f"{NOTO}/{fname}-Regular.ttf")
        pdf.add_font(family, "B", f"{NOTO}/{fname}-Bold.ttf")
        pdf.add_font(family, "I", f"{NOTO}/{fname}-Italic.ttf")
        pdf.add_font(family, "BI", f"{NOTO}/{fname}-BoldItalic.ttf")
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")

    if units is None:
        units = load_units()
    title_page(pdf)
    # Frame units: record the START page before composing (a unit
    # may flow over several pages; page_no() afterwards would name
    # its last page, not its first).
    toc["imprint"] = pdf.pages_count + 1
    imprint_page(pdf)
    toc["elements"] = pdf.pages_count + 1
    elements_page(pdf)
    toc["preface"] = pdf.pages_count + 1
    preface_page(pdf)
    contents_page(pdf, toc, units)
    text_units(pdf, units, toc)
    apparatus_pages(pdf, toc)
    return pdf, toc


def main():
    units = load_units()
    toc = {}
    pdf, toc = build(toc, units=units)       # pass one: measure
    folio_total = pdf.pages_count
    pdf, toc = build(toc, folio_total, units)  # pass two: numbered
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"emphasis spans counted: {STATS['spans']}")
    print(f"bytes: {OUT.stat().st_size}")
    for k, v in toc.items():
        print(f"  {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
