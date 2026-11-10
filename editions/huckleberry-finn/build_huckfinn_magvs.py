#!/usr/bin/env python3
# =====================================================================
# 93 — THE ADVENTURES OF HUCKLEBERRY FINN, TEACHER'S REVISION (MAGVS)
# ---------------------------------------------------------------------
# Epigraph: "All right, then, I'll go to hell." — Huck Finn, Ch. XXXI
#           (the sovereign act this edition exists to honour)
#
# IX day of November, Dies Lunae, Sol in Scorpio, Anno V:xii e.n.
# (2026 e.v.)
#
# Authorship of the REVISION AND APPARATUS attributed exclusively to
# Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights Reserved,
# Without Prejudice). The novel itself is by MARK TWAIN (Samuel
# Langhorne Clemens, 1835-1910), credited first and largest, and is
# in the public domain in the United States (first published 1884 UK
# / 1885 US). The Flagpole claims the revision and apparatus ONLY.
#
# Scientific Illuminism: Method of Science, Aim of Religion.
# Classification: Enterprise • Educational • Research & Development
#
# Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR,
# All Rights Reserved, Without Prejudice. Right of claim hereby
# reserved and coined under the authority of the Living Man.
# =====================================================================
# MECHANISM / DOCTRINE — how this builder works, line by line in
# spirit:
#
# INPUTS    : Project Gutenberg ebook #76 plain text (pg76.txt),
#             fetched verbatim; the Doctrine logo; DejaVu Serif.
# PROCESSES : (1) The Gutenberg text is split at its own seams —
#             NOTICE, EXPLANATORY, and the chapter heads Twain's
#             printers set (CHAPTER I. ... CHAPTER XLII. and
#             CHAPTER THE LAST, the forty-third unit). Hard-wrapped
#             lines are re-flowed into paragraphs on blank-line
#             boundaries ONLY; no word is added, removed, modernised,
#             or sanitised. Dialect stands byte-for-byte in substance.
#             (2) The book is built TWICE by the same code: pass one
#             counts pages and records each chapter's opening page;
#             pass two prints the Contents with true page numbers
#             and footers whose "N of M" resolves to the real total.
# OUTPUTS   : HUCKLEBERRY-FINN-MAGVS.pdf — the complete novel in
#             Teacher's Edition dress, with Reviser's Preface,
#             Table of Authorities, Colophon, Flagpole front & back.
# TOLERANCES: Chapter census must equal 43 units (I-XLII + THE LAST);
#             first body line and last line are asserted against the
#             source ("You don't know about me..." / "THE END. YOURS
#             TRULY, _HUCK FINN_."). Any mismatch fails the build.
#
# DOCTRINE  : Apparatus, never alteration. The bowdlerizer's pen is
#             the one instrument this house will not pick up.
# =====================================================================

import re
import sys
import time
from pathlib import Path

from fpdf import FPDF

HERE = Path(__file__).resolve().parent
SRC = HERE / "source" / "pg76.txt"
OUT = HERE / "HUCKLEBERRY-FINN-MAGVS.pdf"
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAGE_W, PAGE_H = 152.4, 228.6          # 6 x 9 in trade hardcover trim
MARGIN = 16.0
BODY_W = PAGE_W - 2 * MARGIN

FLAGPOLE = ("Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, "
            "ARR, All Rights Reserved, Without Prejudice. Right of claim "
            "hereby reserved and coined under the authority of the "
            "Living Man.")
FOOTER_TXT = ("| All Rights Reserved, Without Prejudice | "
              "Flagpole of Claim and Coinage reserved")
MOTTO = "93 \u2014 Live, Love, and let Love, Live."

TOTAL_PAGES = {"n": 0}   # filled by pass one, read by pass two footers


# ---------------------------------------------------------------------
# SOURCE PARSING — split Twain's text at Twain's own seams.
# ---------------------------------------------------------------------
def load_source():
    raw = SRC.read_text(encoding="utf-8")
    # Strip only the Gutenberg licence shell (start/end markers).
    raw = raw.split("*** START OF THE PROJECT GUTENBERG EBOOK 76 ***", 1)[1]
    raw = raw.split("*** END OF THE PROJECT GUTENBERG EBOOK 76 ***", 1)[0]
    lines = raw.splitlines()

    def find_exact(text, start=0):
        for i in range(start, len(lines)):
            if lines[i].strip() == text:
                return i
        raise ValueError(f"seam not found: {text}")

    notice_i = find_exact("NOTICE.")
    expl_i = find_exact("EXPLANATORY")
    # Body begins at the CHAPTER I. that follows the scene-setting line.
    scene_i = next(i for i, l in enumerate(lines)
                   if l.startswith("Scene: The Mississippi Valley"))
    body_i = find_exact("CHAPTER I.", scene_i)

    def paragraphs(a, b):
        """Re-flow hard-wrapped lines a..b into paragraphs."""
        paras, buf = [], []
        for ln in lines[a:b]:
            if ln.strip():
                buf.append(ln.strip())
            elif buf:
                paras.append(" ".join(buf)); buf = []
        if buf:
            paras.append(" ".join(buf))
        return paras

    notice = paragraphs(notice_i + 1, expl_i)
    explanatory = paragraphs(expl_i + 1, body_i - 4)  # drop title/scene lines

    # Chapter heads in the body: CHAPTER I. ... CHAPTER THE LAST
    head_re = re.compile(r"^CHAPTER (?:[IVXL]+\.?|THE LAST\.?)$")
    heads = [i for i in range(body_i, len(lines))
             if head_re.match(lines[i].strip())]
    chapters = []
    for k, h in enumerate(heads):
        end = heads[k + 1] if k + 1 < len(heads) else len(lines)
        title = lines[h].strip().rstrip(".")
        chapters.append((title, paragraphs(h + 1, end)))
    return notice, explanatory, chapters


# ---------------------------------------------------------------------
# PDF SCAFFOLD — footer carries the resolving "N of M" on every page.
# ---------------------------------------------------------------------
class Book(FPDF):
    def footer(self):
        self.set_y(-11)
        self.set_font("sans", "", 6.5)
        self.cell(0, 5, f"\u2014 {self.page_no()} of {TOTAL_PAGES['n']} "
                        f"\u2014 {FOOTER_TXT}", align="C")


def new_book():
    pdf = Book(orientation="P", unit="mm", format=(PAGE_W, PAGE_H))
    pdf.set_margins(MARGIN, 14, MARGIN)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("serif", "", SERIF)
    pdf.add_font("serif", "B", SERIF_B)
    pdf.add_font("sans", "", SANS)
    pdf.add_font("sans", "B", SANS_B)
    return pdf


def para(pdf, text, size=10.5, lh=5.1, align="J", font="serif",
         style="", space_after=2.2, indent=0):
    """One paragraph. new_x/new_y pinned: chained multi_cell calls
    otherwise strand the pen at the right margin (house gotcha)."""
    pdf.set_font(font, style, size)
    if indent:
        pdf.set_x(MARGIN + indent)
    pdf.multi_cell(BODY_W - indent, lh, text, align=align,
                   new_x="LMARGIN", new_y="NEXT")
    pdf.ln(space_after)


def centred(pdf, text, size, style="B", font="serif", lh=None, gap=2):
    pdf.set_font(font, style, size)
    pdf.multi_cell(BODY_W, lh or size * 0.52, text, align="C",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.ln(gap)


def rule(pdf, gap_before=1, gap_after=3):
    pdf.ln(gap_before)
    y = pdf.get_y()
    pdf.line(MARGIN + 30, y, PAGE_W - MARGIN - 30, y)
    pdf.ln(gap_after)


# ---------------------------------------------------------------------
# FRONT MATTER
# ---------------------------------------------------------------------
def title_page(pdf):
    pdf.add_page()
    pdf.image(str(LOGO), x=(PAGE_W - 34) / 2, y=14, w=34)
    pdf.ln(52)
    centred(pdf, "THE ADVENTURES OF", 15, gap=0)
    centred(pdf, "HUCKLEBERRY FINN", 21, gap=1)
    centred(pdf, "(Tom Sawyer's Comrade)", 11, style="", gap=3)
    centred(pdf, "A Scientific Illuminist treatment of Mark Twain's "
                 "Adventures of Huckleberry Finn (1884/85)", 9.5,
            style="", font="sans", lh=4.6, gap=5)
    centred(pdf, "By", 10, style="", gap=0)
    centred(pdf, "MARK TWAIN", 17, gap=5)   # the author, first & largest
    centred(pdf, "TEACHER'S REVISION (MAGVS)", 12, gap=1)
    centred(pdf, "Revision and Apparatus by Johnathan 'Qasparr' Monroe",
            10, style="", gap=4)
    para(pdf, "Authorship of this Revision and its Apparatus attributed "
              "exclusively to Johnathan 'Qasparr' Monroe (Greek, -ARR, "
              "All Rights Reserved, Without Prejudice). The novel is "
              "Twain's; no word of it is claimed, altered, modernised, "
              "or sanitised by this edition \u2014 apparatus, never "
              "alteration.", size=8.5, lh=4.2, align="C", font="sans")
    para(pdf, "IX day of November, Dies Lunae, Sol in Scorpio, "
              "Anno V:xii e.n. (2026 e.v.)", size=9, align="C",
         font="sans")
    para(pdf, "Classification: Enterprise \u2022 Educational \u2022 "
              "Research & Development\nMethod of Science, Aim of Religion",
         size=9, lh=4.4, align="C", font="sans")
    para(pdf, FLAGPOLE, size=8.5, lh=4.2, align="C", font="sans")
    rule(pdf)
    para(pdf, "PUBLIC DOMAIN: Adventures of Huckleberry Finn was first "
              "published in 1884 (United Kingdom) and 1885 (United "
              "States). It is in the public domain in the United States. "
              "Source text: Project Gutenberg ebook #76, reproduced "
              "complete and unexpurgated.", size=8.5, lh=4.2,
         align="C", font="sans")


def contents_page(pdf, chapters, toc_pages):
    pdf.add_page()
    centred(pdf, "CONTENTS", 14, gap=2)
    centred(pdf, "The Reviser's Preface \u00b7 Twain's NOTICE and "
                 "EXPLANATORY \u00b7 the Novel complete in forty-three "
                 "chapters (I\u2013XLII and CHAPTER THE LAST)",
            8.5, style="", font="sans", lh=4.2, gap=4)
    for title, _ in chapters:
        page = toc_pages.get(title, "")
        pdf.set_font("serif", "", 9.5)
        label = title.title() if title != "CHAPTER THE LAST" else \
            "Chapter the Last"
        dots = "." * max(3, 46 - len(label))
        pdf.multi_cell(BODY_W, 4.6, f"{label} {dots} {page}", align="L",
                       new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    para(pdf, "Closing apparatus: Table of Authorities \u00b7 Colophon "
              "\u00b7 the Flagpole.", size=9, font="sans", align="C")


PREFACE = [
    ("I \u00b7 WHY THIS BOOK",
     ["Of all the books this house will ever revise, this is the one "
      "that needed no argument. Ernest Hemingway's verdict stands at "
      "the head of the American shelf: all modern American literature "
      "comes from one book by Mark Twain called Huckleberry Finn. "
      "But the desk does not take even Hemingway on faith; the claim "
      "was weighed, and it holds. Before Huck, American fiction spoke "
      "with an English accent it had borrowed. After Huck, it spoke "
      "in the voice of a boy on a raft who was not supposed to be "
      "worth listening to \u2014 and every honest American sentence "
      "since has had to reckon with his.",
      "The book is a comedy that carries a tragedy in its cargo and "
      "a gospel in its hold. A runaway boy and an enslaved man float "
      "down the Mississippi on a raft, and the river keeps offering "
      "them freedom while the shore keeps calling them back to a "
      "civilisation built on a lie it called law. Every town on the "
      "bank is rigged: its religion, its respectability, its courts, "
      "its mobs. The raft is the one honest jurisdiction in the "
      "novel \u2014 two people, no master, and the current. This "
      "house, which is building its own road out of a rigged town, "
      "recognises the geography."]),
    ("II \u00b7 THE SOVEREIGN ACT",
     ["In Chapter XXXI the whole book comes to its point, and the "
      "point is a decision. Huck has written a letter betraying Jim "
      "to his enslaver, because everything he has been taught \u2014 "
      "church, school, law, conscience as the town manufactured it "
      "\u2014 tells him that helping a man steal himself is theft and "
      "sin. He holds the letter. He thinks of Jim's kindness, Jim's "
      "grief for his children, Jim standing his watch so the boy "
      "could sleep. And he says, trembling: 'All right, then, I'll "
      "go to hell' \u2014 and tears the letter up.",
      "Weigh what that act is. A boy with no philosophy, no allies, "
      "and no doubt at all about the punishment decides that his own "
      "judgment of a man's humanity outranks the combined authority "
      "of his church, his state, and his upbringing \u2014 and accepts "
      "damnation as the price of not betraying his friend. The house "
      "doctrine has a name for the primacy of the sovereign will "
      "over every gate and ledger raised against it, and it did not "
      "invent the thing: Twain wrote it in 1884, in dialect, from "
      "inside the very country that needed it most. Huck does not "
      "become an abolitionist. He becomes something rarer and more "
      "useful to study: a person whose loyalty to a known human "
      "being defeats an inherited abstraction. That is the whole "
      "engine of this book, and it is why the book still frightens "
      "the comfortable."]),
    ("III \u00b7 THE MAGVS METHOD: APPARATUS, NEVER ALTERATION",
     ["This edition revises everything around the novel and nothing "
      "in it. Twain's text stands exactly as he set it down: every "
      "dialect the EXPLANATORY boasts of, every word the squeamish "
      "have spent a hundred and forty years trying to lift out of "
      "it. The word at the centre of the quarrels is part of the "
      "historical record and part of Twain's instrument \u2014 he "
      "used it the way a surveyor uses a chain, to measure the "
      "distance between what his America said and what it did. To "
      "remove it would not protect a single reader; it would only "
      "falsify the measurement.",
      "The failures this edition refuses are named, because the "
      "house marks dispositions rather than vanishing them. The "
      "Concord Public Library banned the book in 1885 as trash fit "
      "only for the slums \u2014 the first of a long line of "
      "gatekeepers. School boards have chased it ever since. And in "
      "2011 a publisher issued an expurgated classroom edition "
      "substituting 'slave' for Twain's word throughout: the "
      "bowdlerizer's kindness, which trusts the reader with neither "
      "the text nor the truth. Each of these is the same act in "
      "different dress \u2014 someone deciding, for someone else, "
      "what may be read. The MAGVS answer is the Teacher's Edition "
      "answer: print the whole text, surround it with honest "
      "apparatus, tier every claim, and let the reader \u2014 who is "
      "sovereign \u2014 judge."]),
    ("IV \u00b7 THE FOUR-ELEMENT TEST AND THE PUBLIC DOMAIN",
     ["Inputs: the complete public-domain text (Project Gutenberg "
      "ebook #76) and the documented record of the book's making "
      "and banning. Processes: verification of the text at its "
      "seams (NOTICE, EXPLANATORY, forty-three chapters, the final "
      "line in Huck's own hand), then binding in Teacher's Edition "
      "dress with apparatus confined to the frame. Outputs: this "
      "volume \u2014 Twain whole, and a revision a reader can audit. "
      "Tolerances: zero altered words in the novel; every claim in "
      "the apparatus tiered and sourced; any failure found after "
      "issue is to be marked, never quietly vanished. A document "
      "that cannot state these four fails the Method of Science; "
      "one that zeroes the reader's claim to the whole text fails "
      "the Aim of Religion. This one states them, and stands.",
      "Twain needs no one's permission and neither does his reader: "
      "the book is public domain in the United States, free as the "
      "river. What this edition claims \u2014 under the Flagpole, "
      "front and back \u2014 is only its own work: the revision, the "
      "apparatus, the dress. The rest is America's, which is to say "
      "it belongs, as it always has, to whoever lights out for it."]),
]


def preface_pages(pdf):
    pdf.add_page()
    centred(pdf, "THE REVISER'S PREFACE", 14, gap=1)
    centred(pdf, "by the Editor of this Revision", 9.5, style="",
            font="sans", gap=3)
    for head, paras_ in PREFACE:
        pdf.ln(2)
        centred(pdf, head, 11, gap=2)
        for p in paras_:
            para(pdf, p)
    pdf.ln(2)
    para(pdf, "NOTES. Hemingway's judgment: Green Hills of Africa "
              "(1935). The 1885 Concord ban: the library committee's "
              "own published words, widely reprinted. The 2011 "
              "expurgated edition: NewSouth Books, ed. Alan Gribben "
              "\u2014 filed here as the marked counter-example, its "
              "text not used. Huck's decision: Chapter XXXI, quoted "
              "from the text of this edition.", size=8.5, lh=4.2,
         font="sans")


def twain_front(pdf, notice, explanatory):
    pdf.add_page()
    centred(pdf, "THE AUTHOR'S OWN FRONT MATTER", 11, font="sans",
            gap=4)
    centred(pdf, "NOTICE.", 13, gap=3)
    for p in notice:
        para(pdf, p, align="C")
    para(pdf, "BY ORDER OF THE AUTHOR\nPER G. G., CHIEF OF ORDNANCE.",
         size=9.5, align="C", font="sans", lh=4.6)
    pdf.ln(4)
    centred(pdf, "EXPLANATORY", 13, gap=3)
    for p in explanatory:
        para(pdf, p)
    centred(pdf, "Scene: The Mississippi Valley. Time: Forty to "
                 "fifty years ago.", 9.5, style="", gap=0)


# ---------------------------------------------------------------------
# CLOSING APPARATUS
# ---------------------------------------------------------------------
def closing_pages(pdf):
    pdf.add_page()
    centred(pdf, "TABLE OF AUTHORITIES (condensed)", 12, gap=3)
    for line in [
        "Twain, Adventures of Huckleberry Finn \u2014 first edition, "
        "Chatto & Windus (London, 1884); Charles L. Webster & Co. "
        "(New York, 1885). Text of this edition: Project Gutenberg "
        "ebook #76.",
        "Hemingway, Green Hills of Africa (1935) \u2014 the standing "
        "critical verdict quoted in the Preface.",
        "Ellison, 'Change the Joke and Slip the Yoke' (1958) \u2014 on "
        "Huck, Jim, and the American conscience.",
        "Concord (Mass.) Public Library committee report (1885) \u2014 "
        "the first ban, in the gatekeepers' own words.",
        "NewSouth Books expurgated edition (2011), ed. Gribben \u2014 "
        "cited as counter-example only; disposition: MARKED.",
        "United States copyright term, works of 1884/85 \u2014 public "
        "domain; no authority needed and none asked.",
    ]:
        para(pdf, line, size=9.5, lh=4.6)
    pdf.ln(3)
    centred(pdf, "COLOPHON", 12, gap=3)
    para(pdf, "This Teacher's Revision (MAGVS) was generated by the "
              "house press from the public-domain source named above; "
              "the text was verified at its seams and in its census "
              "of chapters before binding, and the ledgers of that "
              "verification stand in the build record. Authorship of "
              "the revision and apparatus is attributed exclusively "
              "to Johnathan 'Qasparr' Monroe, ARR, All Rights "
              "Reserved, Without Prejudice. Method of Science. Aim "
              "of Religion.", size=9.5, lh=4.6)
    pdf.ln(3)
    para(pdf, FLAGPOLE, size=9.5, lh=4.6, align="C", font="sans")
    centred(pdf, MOTTO, 11, gap=0)


# ---------------------------------------------------------------------
# BUILD — two passes: count, then print with resolving numbers.
# ---------------------------------------------------------------------
def build(chapters, notice, explanatory, toc_pages, out_path):
    pdf = new_book()
    title_page(pdf)
    contents_page(pdf, chapters, toc_pages)
    preface_pages(pdf)
    twain_front(pdf, notice, explanatory)
    starts = {}
    for title, paras_ in chapters:
        pdf.add_page()
        starts[title] = pdf.page_no()
        centred(pdf, title.title().upper() if title != "CHAPTER THE LAST"
                else "CHAPTER THE LAST", 14, gap=4)
        for p in paras_:
            para(pdf, p)
    closing_pages(pdf)
    if out_path:
        pdf.output(str(out_path))
    return starts, pdf.page_no()


def main():
    t0 = time.time()
    notice, explanatory, chapters = load_source()
    # --- Audit the census before any page is struck (TRVVTH gate). ---
    assert len(chapters) == 43, f"chapter census {len(chapters)} != 43"
    first = chapters[0][1][0]
    last = chapters[-1][1][-1]
    assert first.startswith("You don\u2019t know about me"), first[:60]
    assert "YOURS TRULY" in last and "HUCK FINN" in last, last[-60:]
    assert any("moral" in p for p in notice), "NOTICE moral line missing"
    assert any("dialects" in p for p in explanatory), "EXPLANATORY bad"
    print(f"source verified: 43 chapters, NOTICE + EXPLANATORY present")
    starts, total = build(chapters, notice, explanatory, {}, None)
    TOTAL_PAGES["n"] = total
    starts, total2 = build(chapters, notice, explanatory, starts, OUT)
    assert total2 == total, (total, total2)
    dt = time.time() - t0
    size = OUT.stat().st_size
    print(f"BUILT {OUT.name}: {total} pages, {size/1e6:.2f} MB, "
          f"{dt:.1f}s (two passes)")
    print(f"chapter I opens p.{starts[chapters[0][0]]}, "
          f"THE LAST opens p.{starts[chapters[-1][0]]}")


if __name__ == "__main__":
    sys.exit(main())

# =====================================================================
# 93 — Live, Love, and let Love, Live.
# =====================================================================
