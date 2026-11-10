#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"I know that men are won over less by the written word than by the
spoken." -- the author of the text under audit, in his Vorwort.
This edition answers the written word with the written record.

MEIN KAMPF, ERSTER BAND (EINE ABRECHNUNG) -- A CRITICAL TEACHER'S
REVISION (MAGVS) -- built, not copied.

Authorship of the APPARATUS attributed exclusively to Johnathan
'Qasparr' Monroe (Greek, -ARR, All Rights Reserved, Without
Prejudice). The text under audit is Adolf Hitler's. It is named as
his because a critical edition names its author; it is framed as
what it is: the text printed whole, and answered.
IX day of November, Dies Lunae, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved
and coined under the authority of the Living Man. -- The Flagpole
on this volume claims THE APPARATUS AND THE AUDIT ONLY. The German
text is public domain (first published 1925; the author died
1945); no claim reaches for it, and the title page says so.

MECHANISM / DOCTRINE -- how this builder works, and why:

  FRAMING (the founder's design, non-negotiable): this is an audit,
          not an endorsement. The German body is printed whole and
          unaltered; there is NO English translation of the body
          (the standard English translations are in copyright and
          none is used). The apparatus is English: notes after every
          chapter carrying present-day correlations, and a full
          TOWER AUDIT -- a claim register tiering the volume's
          factual claims, autobiographical legends, prophecies and
          racial doctrine against the standard historical record
          (Kershaw; Ullrich; Hamann; Weber; the Institut fuer
          Zeitgeschichte critical edition, 2016).
  INPUT   The German text of Band 1 as secured in the Source Ledger
          (source/SOURCE-LEDGER.md): Internet Archive OCR full text
          of the Eher unabridged printing, 851.-855. Auflage 1943,
          SHA-256 a5de081b...cb19, cross-checked against a second
          witness. Census: Widmung, Vorwort, Kapitel 1-12,
          Schlusswort -- complete.
  PROCESS The OCR stream is reflowed to book measure: wrapped lines
          joined (a line ending in a hyphen joins directly, keeping
          the hyphen; all other line joins take one space), and the
          OCR's doubled inter-word spaces collapsed. These are
          spacing operations; they touch no word. The source's own
          Impressum page and its printed Inhaltsverzeichnis are
          excluded and the exclusion DECLARED (the edition supplies
          its own contents); the Widmung and Vorwort are text and
          stand. OCR artifact classes (merged letterspaced-emphasis
          words; rare single-letter misreads) are printed as found,
          declared in the apparatus, never silently emended.
  OUTPUT  MEIN-KAMPF-MAGVS-VOL1.pdf -- the complete German text of
          Volume One in Teacher's Edition dress, with the English
          apparatus described above.
  TOLERANCE  Any step that would change a word of the German body
          fails the edition. Any audit tier asserted without its
          reasoning fails the audit. What the desk cannot verify it
          marks UNVERIFIED; it does not invent.

  Two-pass build, as with the sibling editions: pass one measures,
  pass two prints the contents numbers. fpdf2 discipline (house
  gotcha, AGENTS.md 2026-10-04): every multi_cell is called with
  new_x=XPos.LMARGIN, new_y=YPos.NEXT.
"""

import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ----------------------------------------------------------------------
# Paths and constants
# ----------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source" / "mk-vol1-eher1943-ocr.txt"
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "MEIN-KAMPF-MAGVS-VOL1.pdf"

NOTO = "/usr/share/fonts/truetype/noto"        # body face: full German
DEJAVU = "/usr/share/fonts/truetype/dejavu"    # display face

FLAGPOLE = ("Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, "
            "ARR, All Rights Reserved, Without Prejudice. Right of claim "
            "hereby reserved and coined under the authority of the "
            "Living Man.")
THELEMIC_DATE = ("IX day of November, Dies Lunae, Sol in Scorpio, "
                 "Anno V:xii e.n. (2026 e.v.)")
FOOTER = ("— {n} of {m} — | All Rights Reserved, Without Prejudice | "
          "Flagpole of Claim and Coinage reserved")

# The sections of Band 1, in the book's own order. "key" indexes the
# English notes; "title" is the book's own (from its Inhaltsverzeichnis).
SECTIONS = [
    ("widmung", "WIDMUNG", "The Dedication"),
    ("vorwort", "VORWORT", "Foreword"),
] + [(f"kap{i}", f"{i}. KAPITEL — {t}", None) for i, t in enumerate([
    "Im Elternhaus",
    "Wiener Lehr- und Leidensjahre",
    "Allgemeine politische Betrachtungen aus meiner Wiener Zeit",
    "München",
    "Der Weltkrieg",
    "Kriegspropaganda",
    "Die Revolution",
    "Beginn meiner politischen Tätigkeit",
    "Die „Deutsche Arbeiterpartei“",
    "Ursachen des Zusammenbruchs",
    "Volk und Rasse",
    "Die erste Entwicklungszeit der Nationalsozialistischen "
    "Deutschen Arbeiterpartei",
], start=1)] + [
    ("schluss", "SCHLUSSWORT", "Concluding Word (November 1926)"),
]
EXPECTED_TITLE = {
    "kap1": "Im Elternhaus", "kap2": "Wiener Lehr",
    "kap3": "Allgemeine politische", "kap4": "München",
    "kap5": "Der Weltkrieg", "kap6": "Kriegspropaganda",
    "kap7": "Die Revolution", "kap8": "Beginn meiner politischen",
    "kap9": "Deutsche Arbeiterpartei", "kap10": "Ursachen des Zusammenbruchs",
    "kap11": "Volk und Rasse", "kap12": "Die erste Entwicklungszeit",
}


# ----------------------------------------------------------------------
# Source preparation
# ----------------------------------------------------------------------
def _blocks(lines):
    """Group raw lines into paragraph blocks on blank lines; each
    block is reflowed: lines joined with one space, except after a
    trailing hyphen, where the join is direct (declared rule)."""
    blocks, cur = [], []
    for ln in lines:
        s = re.sub(r"\s+", " ", ln).strip()
        if s == "":
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(s)
    if cur:
        blocks.append(cur)
    paras = []
    for blk in blocks:
        text = ""
        for i, ln in enumerate(blk):
            if i == 0:
                text = ln
            elif text.endswith("-"):
                text += ln
            else:
                text += " " + ln
        paras.append(re.sub(r"\s+", " ", text).strip())
    return [p for p in paras if p]


def load_sections():
    """Split the secured OCR text into [(key, [paragraph, ...]), ...]
    by the line map verified at securing (see SOURCE-LEDGER.md):
    front furniture (title/Impressum page) excluded, Widmung from
    its heading to the Vorwort heading, Vorwort to the printed
    Inhaltsverzeichnis, the Verzeichnis itself excluded, then the
    twelve chapter headings 'N. KAPITEL' in order, Schlusswort last.
    The census is ASSERTED: a build on a broken census fails here,
    it does not bind a partial book."""
    lines = SOURCE.read_text(encoding="utf-8").split("\n")
    flat = [re.sub(r"\s+", " ", ln).strip() for ln in lines]

    def find(word, start=0):
        return next(i for i in range(start, len(flat)) if flat[i] == word)

    i_wid = find("Widmung")
    i_vor = find("Vorwort", i_wid)
    i_toc = find("Inhaltsverzeichnis", i_vor)
    kap_at = []
    # The printed Inhaltsverzeichnis lists the same "N. KAPITEL"
    # lines; the body headings are the SECOND set, after the
    # part-title "Erster Band" that closes the front matter. Start
    # the search there or the census binds the table of contents.
    pos = find("Erster Band", i_toc)
    for n in range(1, 13):
        pos = next(i for i in range(pos, len(flat))
                   if flat[i] == f"{n}. KAPITEL")
        kap_at.append(pos)
    i_schluss = find("Schlusswort", kap_at[-1])

    sections = {"widmung": _blocks(lines[i_wid:i_vor]),
                "vorwort": _blocks(lines[i_vor:i_toc])}
    # The heading word itself is a block in the OCR stream; the
    # builder prints its own headings, so lift it out of the body.
    for key, word in [("widmung", "Widmung"), ("vorwort", "Vorwort")]:
        if sections[key] and sections[key][0] == word:
            sections[key].pop(0)
    for n, at in enumerate(kap_at, start=1):
        end = kap_at[n] if n < 12 else i_schluss
        paras = _blocks(lines[at:end])
        # The heading line itself is the region's first block (the
        # builder prints its own headings); the chapter title is
        # the block after it. Lift both out of the body.
        if paras and re.fullmatch(r"\d{1,2}\.\s*KAPITEL", paras[0]):
            paras.pop(0)
        title = paras.pop(0)
        assert EXPECTED_TITLE[f"kap{n}"] in title or \
            title.startswith(EXPECTED_TITLE[f"kap{n}"][:12]), \
            f"census failure at chapter {n}: title block reads {title!r}"
        sections[f"kap{n}"] = paras
    sections["schluss"] = _blocks(lines[i_schluss:])
    if sections["schluss"] and sections["schluss"][0] == "Schlusswort":
        sections["schluss"].pop(0)
    out = [(key, sections[key]) for key, _h, _s in SECTIONS]
    assert all(len(p) > 3 for _k, p in out), "a section came up empty"
    return out


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


# ----------------------------------------------------------------------
# The Reviser's Preface (English; the apparatus voice of the edition)
# ----------------------------------------------------------------------
PREFACE_PARAS = [
    "This is the most dangerous book on this house's shelf, and it "
    "is shelved deliberately, under guard of an audit. Mein Kampf — "
    "the first volume printed here entire — was written in 1924 by "
    "Adolf Hitler, a failed Austrian painter turned Munich agitator, "
    "while he served a prison sentence for high treason after his "
    "attempted putsch of 8–9 November 1923. It was published in "
    "Munich on 18 July 1925 by the Franz Eher Verlag. Part "
    "autobiography, part party program, part racial doctrine, it "
    "became the founding text of the movement that took power in "
    "Germany in 1933 and then did, in office, much of what this "
    "volume announces: the destruction of German democracy, the "
    "Nuremberg Laws, the war of annihilation in the East, and the "
    "murder of six million Jews — men, women, and children killed "
    "for the fact of their birth — alongside millions of other "
    "victims: Poles and Soviet citizens in their tens of millions, "
    "Roma, the disabled, political and religious dissenters, "
    "prisoners of war. Any edition of this book that does not begin "
    "by stating what it caused has already begun to lie.",

    "The reviser's position is stated once, here, without euphemism, "
    "and is not repeated as decoration through the volume: the "
    "doctrine in this text is condemned — its racial teaching is "
    "false as science, its history is falsified where it matters "
    "most, its scapegoat mechanism is a fraud, and its program was "
    "a crime carried out. What follows this preface is not rhetoric "
    "against the book. It is something the book's author never "
    "permitted his own claims: examination. Every factual claim of "
    "consequence in this volume is entered in the Tower Audit at "
    "the back of this edition and tiered — PROVEN, SUPPORTED, "
    "CONTESTED, FALSE, or UNVERIFIED — against the standard "
    "historical record, with its reasoning printed beside it. The "
    "audit, not the preface, is the condemnation with receipts.",

    "Why print the text whole, then, and in German? Three reasons, "
    "each a matter of method. First: the text is the evidence. The "
    "Institut für Zeitgeschichte in Munich reached the same "
    "conclusion after decades in which the German copyright was "
    "used to keep the book out of print, and in 2016 published its "
    "own critical edition — because a text that circulates only as "
    "legend is believed in the dark and quoted in fragments, while "
    "a text that stands open can be weighed line by line. Second: "
    "the German matters. The in-copyright English translations are "
    "other men's work and are not used here; the body of this "
    "edition is the author's own language, unaltered, so that "
    "nothing in the audit depends on a translator's mercy — the "
    "short fragments quoted inside the English notes are the "
    "house's own renderings and are marked as such. Third: an "
    "audited text can be answered, and an unaudited one can only be "
    "feared. Fear is what this book has always traded in. The "
    "Method of Science is this house's answer to it.",

    "The reader is warned, plainly: parts of this volume — above "
    "all the eleventh chapter — are poisonous reading, a sustained "
    "defamation of a people, written to license what was later "
    "done to them. It is printed here because suppressing the "
    "evidence of how a catastrophe argued for itself does not "
    "unmake the catastrophe, and because the argument is still "
    "made, in our own century, by men who count on their audience "
    "never having read the original closely enough to see its "
    "machinery. The notes after every chapter name that machinery "
    "where it operates and set beside it, soberly, its present-day "
    "correlations: the propaganda technique now measured in "
    "laboratories, the betrayal-legend now reused as a template, "
    "the racial science now refuted by the genome itself.",

    "A word on the dedication that opens the book. The Widmung "
    "names sixteen men who died in the 1923 putsch and made them "
    "the movement's first martyrs — the seed of the blood-cult "
    "that later marched past their memorials every 9 November. "
    "Four Munich policemen also died that day, doing their duty "
    "against the putsch; the dedication does not name them. The "
    "omission is the book in miniature: a memory with the "
    "inconvenient dead removed. The audit restores them, in its "
    "first group of entries, to the record.",

    "What this edition is not: it is not an endorsement, not a "
    "rehabilitation, not a trophy, and not a provocation. No word "
    "of the German text has been altered, softened, or cut — "
    "alteration would destroy the evidence, and this house does "
    "not destroy evidence; it weighs it. The Flagpole of Claim and "
    "Coinage on this volume claims the apparatus and the audit "
    "only. The text's author is named because a critical edition "
    "names its author. The honor in this book, such as it is, "
    "belongs entirely to the answering of it.",
]

PREFACE_NOTES = [
    "Notes to the Preface — 1. The standard scholarly benchmarks "
    "used throughout the audit: Ian Kershaw, Hitler 1889–1936: "
    "Hubris (1998) and Hitler 1936–1945: Nemesis (2000); Volker "
    "Ullrich, Adolf Hitler: Die Jahre des Aufstiegs 1889–1939 "
    "(2013; Eng. Hitler: Ascent, 2016); Brigitte Hamann, Hitlers "
    "Wien (1996; Eng. Hitler's Vienna, 1999); Thomas Weber, "
    "Hitler's First War (2010); and Mein Kampf: Eine kritische "
    "Edition, ed. Christian Hartmann et al., Institut für "
    "Zeitgeschichte, Munich–Berlin, 2016. [ATTESTED.]",
    "2. Victim figures in the preface follow the standard "
    "consensus: approximately six million Jews murdered in the "
    "Holocaust; total deaths in the European war, including "
    "Soviet military and civilian dead, in the tens of millions. "
    "[ATTESTED — the consensus of the historical record.]",
    "3. The German copyright in this work, held after 1945 by the "
    "Free State of Bavaria, expired at the end of 2015, seventy "
    "years after the author's death; the text has since been "
    "public domain in Germany as in the United States (first "
    "published 1925). The IfZ critical edition (note 1) followed "
    "in January 2016. [ATTESTED.]",
]

# ----------------------------------------------------------------------
# Notes and correlations (English), printed after each section.
# Anchors quote short German fragments; renderings are the house's.
# ----------------------------------------------------------------------
CHAPTER_NOTES = {
    "widmung": [
        "The sixteen names are the putschists killed on 9 November "
        "1923 at the Feldherrnhalle and in the courtyard of the War "
        "Ministry. The names themselves are a matter of record "
        "[PROVEN — see Audit A-W]. The dedication's function is the "
        "auditable act: it founds a martyrology. The four policemen "
        "killed resisting the putsch — whose names the movement "
        "never carved anywhere — are restored in the Audit.",
        "Correlation, present day: the ritual built on this page — "
        "the annual 9 November re-enactment march, the Blutfahne "
        "(the flag carried in 1923, later used to consecrate other "
        "flags by touch), the Ehrentempel sarcophagi of 1935 — is "
        "the textbook case historians use for the manufacture of a "
        "political religion. The method — a founding blood-sacrifice, "
        "a calendar feast, relics — predates and survives this "
        "movement; the note names it so the reader watches it work.",
    ],
    "vorwort": [
        "The Foreword is dated Landsberg, 16 October 1924. Its "
        "author was serving a five-year sentence for high treason "
        "and was released that December, after roughly nine months "
        "in a fortress confinement whose comforts (visitors, "
        "secretarial help from fellow prisoners, a stream of gifts) "
        "are documented. Present-day correlation: the leniency of "
        "Weimar courts toward right-wing violence — the political "
        "scientist Emil Julius Gumbel tabulated it as early as 1922 "
        "— is the institutional background without which neither "
        "the book nor the career is intelligible.",
        "„...zur Zerstörung der von der jüdischen Presse betriebenen "
        "üblen Legendenbildung über meine Person“ — “to destroy the "
        "evil legend-manufacture about my person carried on by the "
        "Jewish press” (house rendering). The autobiography is "
        "announced, in its own foreword, as a weapon against "
        "legends; the Tower Audit tests its legends in return, "
        "beginning with the Vienna chapters (Audit A5).",
    ],
    "kap1": [
        "Braunau am Inn, the border, and the demand that "
        "German-Austria “return to the great German motherland” open "
        "the book because they are its first program: Anschluss. "
        "Correlation: the demand was executed in March 1938 to "
        "cheering crowds, and is answered in the present order by "
        "the Austrian State Treaty of 1955 and the European "
        "settlement that made the border at the Inn a formality — "
        "the “life-task” of the opening page now crosses a bridge "
        "with a bicycle lane.",
        "„Gleiches Blut gehört in ein gemeinsames Reich“ — “Like "
        "blood belongs in a common Reich” (house rendering). In the "
        "printed book the sentence stands in letterspaced emphasis; "
        "in the OCR source it survives as a merged line and is "
        "printed as found (see Apparatus). The sentence is the "
        "whole doctrine in eight words: belonging assigned by blood, "
        "not by consent. The house doctrine — belonging by covenant "
        "and proof — is its exact negation, and the Audit (D1–D2) "
        "marks the claim's scientific standing.",
    ],
    "kap2": [
        "The Vienna chapter is the founding legend: the destitute "
        "orphan, the building sites, the self-education, the "
        "conversion. Brigitte Hamann's archival reconstruction "
        "(Hitler's Vienna) is the standing correction: the men's "
        "home in the Meldemannstraße was orderly and even "
        "comfortable by the standards of the day; the watercolors "
        "sold, through dealers who included the Jewish art dealer "
        "Samuel Morgenstern; the orphan's pension ran until 1913. "
        "See Audit A4–A6.",
        "The chapter's most revealing silence is a name: Dr. Eduard "
        "Bloch, the Linz family doctor — a Jew — who treated the "
        "author's dying mother in 1907 and was thanked in writing "
        "by the son. After 1938 Bloch received the author's "
        "personal protection and was permitted to emigrate. The "
        "legend requires a Vienna of uniform hatred; the record "
        "keeps producing exceptions the legend cannot digest.",
        "Correlation, present day: the retrospective conversion "
        "narrative — the moment in the capital when the scales fell "
        "— is now a standard component of extremist autobiography "
        "across movements. Historians' inability to find the "
        "conversion in the Vienna record (Audit A5) is itself the "
        "finding: the scene is a genre requirement, not a memory.",
    ],
    "kap3": [
        "The parliament passage — the Reichsrat watched from the "
        "gallery and found contemptible — is genuinely observed in "
        "its surface detail and wholly tendentious in its "
        "conclusion: that representation itself is a fraud. "
        "Correlation: the argument's present-day descendants "
        "(parliament as theater, deliberation as weakness, the "
        "single will as authenticity) are catalogued in the "
        "comparative literature on democratic backsliding; the "
        "chapter is their early, candid statement.",
        "The two Vienna teachers named with admiration are real and "
        "their influence documented: Georg von Schönerer, the "
        "pan-German racial nationalist, and Karl Lueger, Vienna's "
        "mayor, the master of antisemitism as electoral technique — "
        "“Wer ein Jud ist, bestimme ich” (“I decide who is a Jew”) "
        "is attributed to Lueger and the author learned the lesson "
        "in cynicism if not the words. See Audit B7 on the claim "
        "that democracy is a Jewish device: parliamentary "
        "institutions are centuries older than Jewish emancipation.",
    ],
    "kap4": [
        "The Munich chapter performs a delicate omission. The "
        "author arrived in May 1913, a young man who had failed to "
        "register for Austrian military service; in January 1914 "
        "Munich police arrested him at the instance of the Austrian "
        "consulate, and he was examined at Salzburg and found unfit "
        "for service. None of this is in the chapter, which gives "
        "the move to Germany a purely ideal motive. See Audit A8.",
        "Correlation: the pattern — the memoir that edits out the "
        "policeman at the door — is why this house audits "
        "autobiography against records at all. The chapter is a "
        "standing exhibit in the difference between a life and its "
        "authorized version.",
    ],
    "kap5": [
        "The war chapter is the book's second legend: the volunteer "
        "of August 1914, the kneeling thanksgiving, four years at "
        "the front. The regimental record (Thomas Weber, Hitler's "
        "First War) gives a dispatch runner of the List Regiment's "
        "headquarters staff — brave work, decorated work (Audit "
        "A10), but headquarters work, with its leaves, its billets, "
        "and its comparative safety behind the line his rhetoric "
        "claims. The gap between the service and the narration is "
        "the auditable quantity.",
        "The chapter's closing movement — the gas, the blindness, "
        "Pasewalk, the resolve — is constructed as a conversion "
        "scene parallel to Vienna's, and historians treat it as "
        "literature laid over a documented hospital stay (Audit "
        "A11). Present-day correlation: the twice-told conversion — "
        "once by reading, once by suffering — is the autobiography's "
        "load-bearing myth, and the Audit marks both tellings "
        "UNVERIFIED as scenes while confirming the hospital record "
        "beneath the second.",
    ],
    "kap6": [
        "This is the most technically accomplished chapter in the "
        "book and the one most read today: a field manual of mass "
        "persuasion — restrict the message to a few points, repeat "
        "them without cease, address feeling before reason, never "
        "argue with the opponent's case but assault his person. "
        "Correlation, measured: experimental psychology has since "
        "given the mechanism its laboratory name — the illusory "
        "truth effect (Hasher, Goldstein & Taylor, 1977, and fifty "
        "years of successors): repeated statements are believed "
        "more, independent of their truth. The chapter describes "
        "the effect from the practitioner's side, half a century "
        "early.",
        "Correlation, present day: analysts of state disinformation "
        "(the RAND corporation's “firehose of falsehood” model, "
        "2016) describe a method — high volume, multichannel, "
        "rapid, repetitive, shameless about consistency — that this "
        "chapter anticipates in print. The note does not claim the "
        "modern practitioners learned it here; it records that the "
        "author of 1924 already understood the machine he was "
        "describing, and said the quiet parts in a book anyone "
        "could buy.",
        "The chapter praises British propaganda and scorns German. "
        "Historians credit the observation in part (Audit B4). What "
        "the chapter omits: Germany's own extensive propaganda "
        "apparatus, and that the “superiority” of enemy propaganda "
        "became, after 1918, a load-bearing excuse — the army was "
        "not outfought, it was out-talked. See Audit B1.",
    ],
    "kap7": [
        "The Revolution chapter exists to lay the defeat of 1918 "
        "anywhere but on the army that lost it. The documented "
        "sequence runs the other way: the High Command demanded an "
        "armistice on 29 September 1918 because the front was "
        "breaking; the naval mutiny at Kiel and the November "
        "revolution followed the collapse, they did not cause it. "
        "Audit B1–B3 gives the stab-in-the-back legend its tier: "
        "FALSE, with the Judenzählung file as its standing refutation.",
        "Correlation, present day: the betrayal template — victory "
        "stolen by an internal enemy, the true defeat always "
        "elsewhere — is the most durable single device in this "
        "book. It recurs wherever a lost contest is re-narrated as "
        "a stolen one. The audit's interest is structural: a "
        "community that accepts the template has agreed in advance "
        "never to examine a defeat, which is why the device is "
        "worth naming wherever it reappears.",
    ],
    "kap8": [
        "Here the record suddenly firms up, because the army kept "
        "paper. The author of 1919 was a Reichswehr education "
        "officer under Captain Karl Mayr, paid to instruct troops "
        "against Bolshevism — a state employee of the republic he "
        "was learning to destroy. The chapter's first firm document "
        "is the Gemlich letter of 16 September 1919 (Audit C4): "
        "programmatic antisemitism, in writing, dated — the anchor "
        "against which the Vienna conversion legend (Audit A5) is "
        "weighed and found retrospective.",
        "Correlation: radicalization timelines matter in the "
        "present-day study of extremism for the same reason they "
        "matter here — the subject's own account of when he became "
        "what he became is the least reliable document in the file. "
        "The desk's rule generalizes: date a conversion by its "
        "first surviving paper, not by its best story.",
    ],
    "kap9": [
        "The German Workers' Party of Anton Drexler — a locksmith's "
        "circle of a few dozen men — is described accurately as to "
        "its smallness and dishonestly as to its emptiness: the "
        "ideas were already there (Audit C3), and the author's "
        "contribution was not the doctrine but the voice, the "
        "organization, and the will. His membership legend — the "
        "seventh member — is FALSE (Audit C2): card number 555, "
        "the numbering rigged from 501 to seem larger. A movement "
        "that begins by inflating its own roster has told you its "
        "method in miniature.",
        "The 25-point program he announced for the party on 24 "
        "February 1920 already contains, in its fourth point, the "
        "definition on which everything later stands: citizenship "
        "by blood, and “no Jew” a citizen. The Nuremberg Laws of "
        "1935 are that point, enacted. The audit trail from a "
        "beer-hall program to a statute book runs fifteen years and "
        "is entirely documented — which is the answer to any later "
        "plea that no one could have known.",
    ],
    "kap10": [
        "The long collapse chapter blames the pre-war Reich's "
        "errors — and, in its notorious digression, syphilis, "
        "prostitution, and the Jews, in an epidemiology with no "
        "basis in any record (Audit D5). The digression matters "
        "because it shows the method at its purest: a real social "
        "anxiety (venereal disease in a garrison Europe) is "
        "assigned an ethnic author, and the assignment, repeated, "
        "becomes the explanation.",
        "Correlation, present day: the disease-and-minority "
        "conflation is among the oldest continuously running "
        "programs in the conspiracy repertoire — plague, cholera, "
        "and every epidemic since has been assigned the same "
        "authorship by the same kind of pamphlet. Public-health "
        "historiography documents the pattern; this chapter is one "
        "of its set texts.",
    ],
    "kap11": [
        "The eleventh chapter is the book's doctrinal core and its "
        "most poisonous: the racial taxonomy, the Aryan as "
        "culture-founder, the Jew as anti-man, the “sin against "
        "blood and race” as the original sin of the world. The "
        "Audit (D1–D4) tiers it in full; the summary is short. As "
        "science it is FALSE — refuted by genetics, anthropology, "
        "and the ordinary historical record of every continent. As "
        "history it is FALSE. As rhetoric it is the permit for "
        "everything that followed: a text that defines a people as "
        "a pathogen has already decided what is to be done with "
        "pathogens, and the men of 1941–45 cited the decision.",
        "The chapter leans, as its movement did, on the Protocols "
        "of the Elders of Zion — a fabrication plagiarized from an "
        "1864 French satire, exposed in The Times in 1921, years "
        "before this volume printed, and adjudicated a forgery at "
        "Berne in 1934–35. The exposure changed nothing in the "
        "movement's use of it, which is the single most instructive "
        "fact in this book about how such texts work: refutation "
        "is received as further proof. See Audit B6.",
        "Correlation, present day: the chapter's taxonomy survives "
        "in the present century's “race science” underground, whose "
        "claims the American Society of Human Genetics answered "
        "formally in 2018: genetics “demonstrates that humans "
        "cannot be divided into biologically distinct subcategories.” "
        "The refutation the author never faced in 1925 is now the "
        "recorded consensus of the science he counterfeited.",
    ],
    "kap12": [
        "The closing chapter is organizational: halls, hecklers, "
        "the protection squad that became the SA, the purchase of "
        "the Völkischer Beobachter (Audit C5), the discovery — told "
        "with genuine insight — that a movement is built by holding "
        "the room. Read as a manual of movement-building it remains "
        "instructive in the way a lockpick is instructive: the "
        "technique is real, and its ends are in the Audit.",
        "The chapter ends at the edge of the putsch it does not "
        "narrate (the putsch belongs to the Widmung and the "
        "Schlusswort, its failure unexamined between them). What "
        "the narrative voice never does — here or anywhere in the "
        "volume — is record a doubt, an error, or a debt. A "
        "memoir without a single admitted mistake is not a memoir "
        "but a monument; monuments are weighed differently, and "
        "the Audit has weighed this one.",
    ],
    "schluss": [
        "The Schlusswort is dated by its own content to November "
        "1926 and was not part of the 1925 first edition; it rides "
        "in later Eher printings, including the 1943 witness this "
        "edition prints (see Apparatus, item 2). Its presence is a "
        "standing lesson in editions: the “same book” is a moving "
        "object, and an honest edition declares which printing it "
        "stands on.",
        "Its prophecy — victory by “almost mathematical certainty,” "
        "the racial state that “must one day become lord of the "
        "earth” — is the volume's last auditable claim, and history "
        "has returned its verdict: 1945, the regime destroyed, "
        "Germany divided, the prophet dead by his own hand in a "
        "bunker under the capital he had promised the earth. The "
        "Audit closes the register on it (C6): FALSE in the event. "
        "What survived the prophecy is the book — and the answering "
        "of it, which is the work of this edition.",
    ],
}


# ----------------------------------------------------------------------
# THE TOWER AUDIT (English) -- the claim register of this volume.
# Each item: the claim as the text makes it; the tier; the reasoning
# against the standard record. Tiers: PROVEN / SUPPORTED /
# CONTESTED / FALSE / UNVERIFIED.
# ----------------------------------------------------------------------
AUDIT = [
    ("GROUP W — THE DEDICATION AND THE FRONT MATTER", [
        ("W1", "The Widmung names the sixteen men of the movement "
               "who fell on 9 November 1923 before the Feldherrnhalle "
               "and in the War Ministry courtyard.",
         "PROVEN",
         "The sixteen names, occupations, and birth dates as printed "
         "accord with the historical record of the Beer Hall Putsch's "
         "dead. What the Audit marks is not the list but its use: "
         "see W2."),
        ("W2", "The dedication's frame: those sixteen are the day's "
               "dead who matter — the martyrs of a national rising.",
         "FALSE",
         "False by omission, which is the frame's method. Four Munich "
         "policemen also died on 9 November 1923, killed resisting an "
         "armed attempt to overthrow the constitutional order; the "
         "dedication erases them. A memory with the inconvenient dead "
         "removed is not remembrance but recruitment — and the cult "
         "built on this page (annual re-enactment, the Blutfahne, the "
         "1935 Ehrentempel) ran on the erasure for twelve years."),
    ]),
    ("GROUP A — THE LIFE AS WRITTEN", [
        ("A1", "He was born on 20 April 1889 at Braunau am Inn, son "
               "of the customs official Alois Hitler and his wife "
               "Klara, née Pölzl.",
         "PROVEN",
         "Parish and civil records; the family circumstances are "
         "documented in full by Kershaw and Ullrich. The memoir's "
         "genealogical silences (the Schicklgruber name-change of "
         "1876, the uncertain grandfather) belong to the record, not "
         "to this text, which does not mention them."),
        ("A2", "His father's death in 1903 reduced the family to "
               "poverty, and the boy's youth was a schooling in want.",
         "CONTESTED",
         "Alois Hitler died a pensioned senior customs official "
         "leaving assets; Klara drew a widow's pension and the "
         "children orphan's benefits, and the household remained "
         "respectable lower-middle-class. Hardship after Klara's "
         "death in 1907 was real but neither immediate nor total. "
         "The poverty shading is the memoir's, deepened for effect "
         "(Ullrich; Kershaw)."),
        ("A3", "The Vienna Academy of Fine Arts rejected him (1907 "
               "and 1908), and so an artist's career was thwarted by "
               "an uncomprehending institution.",
         "PROVEN",
         "The rejections are documented — the 1907 examination "
         "verdict survives (“sample drawings unsatisfactory; few "
         "heads”), and the examiners' advice to try architecture, "
         "for which he lacked the required school-leaving "
         "certificate. The cosmic-injustice frame built on the fact "
         "is the author's addition, not the record's."),
        ("A4", "In Vienna he lived in utter destitution, a starving "
               "outcast who shared the lot of the poorest workers.",
         "CONTESTED",
         "The season of genuine destitution (late 1909, shelters and "
         "benches) is real. The portrait as a whole is not: from "
         "1910 he lived in the orderly Meldemannstraße men's home, "
         "earned regular money painting postcards and watercolors "
         "sold for him by dealers — among them the Jewish dealers "
         "Samuel Morgenstern and Josef Neumann — received his "
         "orphan's pension until May 1913, and then a share of his "
         "father's estate. Hamann's archival work is the standing "
         "correction; destitution was a chapter, and he made it the "
         "whole book."),
        ("A5", "By the end of the Vienna years he was already a "
               "fully formed antisemite, converted there by "
               "observation and reading.",
         "CONTESTED",
         "The dating of the conversion is a central scholarly "
         "dispute, and the memoir is its chief — and interested — "
         "witness. For Vienna: the antisemitic milieu and its "
         "pamphlets are documented (Hamann). Against the memoir's "
         "scene: no antisemitic statement survives from the Vienna "
         "years; he did business with Jewish dealers and wrote "
         "gratefully to his Jewish family doctor, Eduard Bloch, "
         "whom he personally protected after 1938. The first firm "
         "documentary anchor is Munich, 16 September 1919 (see C4). "
         "The conversion, as narrated, is retrospective construction."),
        ("A6", "In Vienna and in the trenches he educated himself "
               "systematically by voracious reading — history, art, "
               "politics, military science.",
         "UNVERIFIED",
         "No reading record, library trace, or contemporary "
         "testimony independent of his circle establishes the "
         "curriculum. That he read newspapers and pamphlets is "
         "plausible and partly attested; the self-portrait of the "
         "systematic autodidact is self-report, and is marked as such."),
        ("A7", "In August 1914, though an Austrian citizen, he was "
               "permitted to volunteer for a Bavarian regiment and "
               "served in the 16th Bavarian Reserve Infantry (the "
               "List Regiment).",
         "PROVEN",
         "The enlistment and the regiment are documented, as is his "
         "service as a dispatch runner. The permission story in its "
         "dramatic form (a petition to the Bavarian king) rests on "
         "his word alone — see A8. What the memoir never supplies "
         "is the other file: see A8."),
        ("A8", "He left Austria for Munich in 1913 from ideal "
               "motives alone — longing for Germany and disgust at "
               "the multinational Habsburg state.",
         "FALSE",
         "False in its completeness. He had failed to register for "
         "Austrian military service, was sought for it, and in "
         "January 1914 was arrested in Munich at the Austrian "
         "consulate's instance, taken to Salzburg, examined, and "
         "found unfit (“too weak”). The ideal motives may also be "
         "his; the memoir's claim that they were the whole of it is "
         "contradicted by the police file it omits."),
        ("A9", "He served four years as a front-line fighting "
               "soldier, repeatedly in the thick of the battle.",
         "CONTESTED",
         "He was a Meldegänger — a dispatch runner attached to "
         "regimental headquarters. The duty was dangerous and took "
         "him forward under fire; it was not a rifleman's war, and "
         "headquarters service carried billets, leave, and shelter "
         "the front line did not. Thomas Weber's regimental "
         "research (Hitler's First War) measured the distance "
         "between the service and the narration; the Audit records "
         "the measurement."),
        ("A10", "He was awarded the Iron Cross, First Class, in "
                "1918 (and the Second Class in 1914).",
         "PROVEN",
         "Both awards are documented. The First Class — rare for a "
         "corporal — was recommended by the regimental adjutant, "
         "Lieutenant Hugo Gutmann. Gutmann was a Jew. The memoir, "
         "which misses no occasion, does not name him."),
        ("A11", "Blinded by British mustard gas near Ypres in "
                "October 1918, he lay in Pasewalk hospital when the "
                "revolution came, and there — weeping at the news — "
                "resolved to become a politician.",
         "CONTESTED",
         "The gassing (night of 13–14 October 1918, south of "
         "Ypres), the temporary blindness, and the Pasewalk "
         "hospitalization are documented in regimental and medical "
         "records: PROVEN. The conversion scene built on them — "
         "the tears, the resolve, the second birth of the "
         "politician — appears first in this book, uncorroborated "
         "by any contemporary trace, and is a literary construction "
         "on a factual frame: the scene is UNVERIFIED, the frame "
         "PROVEN, and the Audit marks the composite CONTESTED so "
         "that neither half borrows the other's credit."),
        ("A12", "On 2 August 1914 he stood in the Munich crowd on "
                "the Odeonsplatz, sank to his knees, and thanked "
                "heaven with a full heart.",
         "UNVERIFIED",
         "Self-report. A photograph by Heinrich Hoffmann said to "
         "show him in that crowd was publicized by the movement "
         "years later; the identification has been asserted and "
         "doubted and cannot now be settled. The scene's function "
         "in the memoir — the people's ecstasy made personal — is "
         "clearer than its fact."),
    ]),
    ("GROUP B — THE DEFEAT AND THE REVOLUTION", [
        ("B1", "The German army was undefeated in the field in "
               "1918 and was destroyed by a stab in the back from "
               "the home front.",
         "FALSE",
         "The Dolchstoß legend is a fabrication, and its "
         "fabricators are known. After the failure of the spring "
         "offensives and the Allied Hundred Days, with Germany's "
         "allies collapsing, the High Command itself — Ludendorff, "
         "29 September 1918 — demanded an immediate armistice "
         "because the front could not hold. The revolution followed "
         "the collapse it is blamed for. The legend was constructed "
         "afterward, by the very command that had demanded the "
         "armistice, to relocate the defeat from the army to the "
         "civilians — and this volume is its most consequential "
         "repetition."),
        ("B2", "The strikes, mutinies, and November collapse were "
               "the work of Jews and Marxists acting as one enemy "
               "(the “November criminals”).",
         "FALSE",
         "As a causal claim it has no evidence and a great deal "
         "against it. The January 1918 strikes and the November "
         "collapse arose from hunger, blockade, casualties, and "
         "military defeat; their makers were German workers, "
         "sailors, and soldiers of every confession. The ethnic "
         "attribution is performed by assertion throughout this "
         "volume and documented nowhere in it — the scapegoat "
         "mechanism in its working clothes."),
        ("B3", "Jews shirked military service in the war while "
               "profiting from it at home.",
         "FALSE",
         "Some 100,000 German Jews served in the war; about 12,000 "
         "died in service. The Prussian War Ministry's own 1916 "
         "“Jewish census” (Judenzählung), ordered under antisemitic "
         "pressure to demonstrate shirking, in fact recorded "
         "proportional front-line service — and its results were "
         "suppressed for that reason. The claim in this volume is "
         "the census's intended conclusion, printed after the "
         "census itself had refuted it."),
        ("B4", "Allied — above all British — propaganda was vastly "
               "superior to German propaganda and materially helped "
               "to decide the war.",
         "SUPPORTED",
         "British propaganda's reach and craft are widely credited "
         "by historians of the war, and the German effort's failures "
         "are documented. The Audit marks the observation SUPPORTED "
         "and its use in this volume — as exculpation of the German "
         "command, whose failures were operational, not rhetorical "
         "— as argument, for which the text offers no evidence."),
        ("B5", "Marxism is a Jewish doctrine and movement: “the "
               "Jewish doctrine of Marxism,” one enemy under two "
               "names.",
         "FALSE",
         "An equation by fiat. Marxism's theorists, parties, and "
         "millions of adherents were of every origin; its German "
         "party was the empire's largest and most patriotic in its "
         "own self-understanding until 1914. The equation's function "
         "in this volume is tactical — it lets every opponent be "
         "fought as the same opponent — and its evidentiary basis, "
         "here and everywhere, is nil."),
        ("B6", "The Protocols of the Elders of Zion — the "
               "conspiracy this volume's world-picture codifies — "
               "describe a real Jewish plan for world domination.",
         "FALSE",
         "The Protocols are a forgery: fabricated in the orbit of "
         "the Tsarist secret police, plagiarized in large part from "
         "Maurice Joly's 1864 satire Dialogue aux enfers, exposed "
         "in The Times by Philip Graves in 1921 — before this "
         "volume was written — and adjudicated a forgery by the "
         "Berne court in 1934–35. No claim in this book better "
         "deserves its tier, and none better illustrates the "
         "Audit's rule that a refutation printed before the claim "
         "is part of the claim's record."),
        ("B7", "Parliamentary democracy is a Jewish invention and "
               "instrument for the destruction of peoples.",
         "FALSE",
         "Parliamentary institutions in England run from the "
         "thirteenth century through 1688, centuries before Jewish "
         "emancipation anywhere in Europe; representative bodies "
         "on the continent likewise predate it. The claim is not an "
         "error of dates but a device: it converts a political "
         "preference (for dictatorship) into an ethnic fact, so "
         "that opposing the preference can be reclassified as "
         "defending the conspiracy."),
    ]),
    ("GROUP C — THE MOVEMENT'S FIRST YEARS", [
        ("C1", "On 12 September 1919 he attended the German "
               "Workers' Party at the Sterneckerbräu as an army "
               "observer, intervened in debate, and was urged to "
               "join.",
         "PROVEN",
         "In outline: the meeting, his attendance as an education "
         "officer and informant of the Reichswehr under Captain "
         "Karl Mayr, and his recruitment are documented in army "
         "records and correspondence. The dramatic coloring — the "
         "professorial opponent demolished, the instant conversion "
         "of the room — is the author's varnish on a documented frame."),
        ("C2", "He was the seventh member of the party.",
         "FALSE",
         "His membership card bore number 555. The party numbered "
         "its cards from 501 precisely to seem larger than it was; "
         "“seventh” survives from committee mythology and from his "
         "own retellings. The Audit notes the symmetry: the "
         "movement's first falsified document is its own roster."),
        ("C3", "The little party he joined had no ideas and no "
               "program until he gave it both.",
         "CONTESTED",
         "The DAP's founders — Anton Drexler, Karl Harrer, and the "
         "circle around Gottfried Feder — brought a fully stocked "
         "völkisch, antisemitic, anti-Marxist inventory; what they "
         "lacked was a speaker and an organizer. The 25-point "
         "program of 24 February 1920 was announced and shaped by "
         "him but jointly authored. His contribution was decisive; "
         "the claim that it was creatio ex nihilo is the founder-myth "
         "again, and is marked as contested accordingly."),
        ("C4", "His letter to Adolf Gemlich (16 September 1919) "
               "already sets the goal of a “rational antisemitism” "
               "culminating in “the removal of the Jews altogether.”",
         "PROVEN",
         "The letter survives, written at Mayr's instance in reply "
         "to a soldier's query, and is the earliest dated, "
         "documentary statement of his programmatic antisemitism. "
         "Its importance to the Audit is chronological: it anchors "
         "in Munich in 1919 the ideology the memoir narrates as "
         "complete in Vienna by 1913 (see A5)."),
        ("C5", "The party acquired the Völkischer Beobachter in "
               "December 1920 and built it into the movement's organ.",
         "PROVEN",
         "The purchase — with funds in which army-linked money "
         "played a part — and the paper's conversion into the "
         "party's daily are documented. The chapter's account of "
         "the paper's role in holding the movement's narrative is, "
         "if anything, understated."),
        ("C6", "The Schlusswort (November 1926): persecution has "
               "left the movement “stronger and inwardly firmer than "
               "ever,” and its victory, and the world mastery of the "
               " racially purified state, follow with “almost "
               "mathematical certainty.”",
         "FALSE",
         "The party's refoundation (February 1925) and survival are "
         "fact. The prophecy is the claim, and history has marked "
         "it: the movement's state was destroyed utterly in 1945, "
         "its leader dead by suicide, its capital occupied, its "
         "country divided for forty-five years. A prophecy of "
         "inevitable world dominion that ends in national "
         "catastrophe is not unlucky; it is FALSE, and the Audit "
         "closes this volume's register on it deliberately."),
    ]),
    ("GROUP D — RACE DOCTRINE AS SCIENCE AND HISTORY", [
        ("D1", "Mankind divides into discrete races ranked by "
               "inborn creative capacity: the “Aryan” the sole "
               "culture-founder, the Jew the culture-destroyer.",
         "FALSE",
         "False as science: human genetic variation is real, "
         "clinal, and shallow — populations shade into one another "
         "and share the overwhelming bulk of their variation; no "
         "discrete racial hierarchy of capacity exists in the "
         "genome. The consensus is recorded and unanimous in form: "
         "the UNESCO statements of 1950–51, and the American "
         "Society of Human Genetics' statement of 2018 repudiating "
         "attempts “to link genetics and racial supremacy.” False "
         "as history: agriculture, cities, writing, and statecraft "
         "arose independently on several continents, none of them "
         "waiting for the chapter's taxonomy."),
        ("D2", "Cultures rise and fall by the purity or “poisoning” "
               "of their blood; race mixture is the mechanism of "
               "decline (“the sin against blood and race is the "
               "original sin of this world”).",
         "FALSE",
         "No biological mechanism is offered because none exists; "
         "the rises and falls the text gestures at have documented "
         "political, economic, climatic, and military causes, "
         "weighed by ordinary historiography. As argument the claim "
         "is unfalsifiable — every flourishing mixed society is "
         "reclassified, every pure one mourned in advance — and "
         "unfalsifiability is the mark of dogma, the precise "
         "opposite of the Method of Science under which this Audit "
         "is conducted."),
        ("D3", "The Jew is by nature incapable of creating culture, "
               "a state, or genuine art, and can only imitate, trade "
               "in, and corrode the creations of others.",
         "FALSE",
         "Refuted by the ordinary record of the very cities this "
         "book describes: the Vienna and Munich of the author's own "
         "lifetime, in which Jewish scientists, physicians, "
         "composers, writers, and jurists stood at the documented "
         "center of German culture — a record so plain that the "
         "claim can be maintained only by redefining every "
         "counterexample as theft, which is D4's maneuver and is "
         "marked there."),
        ("D4", "What Jews produce in culture is appropriated Aryan "
               "substance, worn as mimicry.",
         "FALSE",
         "The maneuver that makes D3 unfalsifiable, audited "
         "separately because it is the mechanism rather than a "
         "claim: any Jewish achievement is reclassified as evidence "
         "of imitation, any absence as evidence of incapacity. A "
         "rule that confirms itself on every outcome is not a "
         "finding but a trap, and traps are identified, not debated."),
        ("D5", "Syphilis and prostitution in the old Vienna were "
               "Jewish phenomena and instruments, as Chapter X's "
               "long digression argues.",
         "FALSE",
         "Venereal disease in pre-1914 Europe tracked armies, "
         "garrisons, urbanization, and poverty in every country and "
         "confession; no epidemiological record assigns it an ethnic "
         "authorship. The digression's sources are the period's "
         "antisemitic pamphlet literature, and its function — a "
         "real public-health anxiety ethnicized into a warrant — "
         "is the volume's method in miniature (see the notes to "
         "Chapter X)."),
        ("D6", "France, by the “negrification” of its blood through "
               "colonial troops and mixing, is ceasing to be a "
               "European people and power.",
         "FALSE",
         "No demographic basis existed then or exists now. France's "
         "African soldiers were colonial troops of a French empire "
         "that fielded them, in the event, in 1914–18 and again in "
         "1939–45 — the second time in the army that liberated "
         "France under de Gaulle, an outcome this volume's racial "
         "arithmetic cannot express. The claim is a fantasy of the "
         "taxonomy, and the taxonomy is D1: FALSE."),
    ]),
    ("GROUP E — THE BIG LIE AND THE PROGRAM STATED", [
        ("E1", "The “big lie”: the broad masses fall victim more "
               "readily to a great lie than to a small one — a "
               "technique the text attributes to the Jews and to "
               "Marxism.",
         "FALSE",
         "The attribution is FALSE: it is offered without evidence "
         "and none exists; it is the volume's characteristic "
         "projection, the accuser describing his own method as the "
         "enemy's (Chapter VI is the manual). The described "
         "mechanism — that scale and repetition purchase belief — "
         "is, by contrast, SUPPORTED by later experimental "
         "psychology (the illusory truth effect, 1977 onward), "
         "which is why the passage is quoted in present-day "
         "disinformation research — almost always with its "
         "attribution amputated. The Audit restores the attribution "
         "and tiers the whole as the text presents it: FALSE."),
        ("E2", "Program: Germany requires land at the expense of "
               "the East; soil is the people's by right of need and "
               "strength (the argument of Chapters XI–XII, sealed by "
               "the Schlusswort's “lord of the earth”).",
         "PROVEN",
         "Proven as a statement of intent, which is the tier that "
         "matters for a program: the text says it, in this volume, "
         "plainly. The IfZ editors and Kershaw alike treat the "
         "passages as documentary evidence of intent afterward "
         "executed — in the war of annihilation from 1941 and the "
         "Generalplan Ost, the projected demographic "
         "re-engineering of Eastern Europe at the cost of tens of "
         "millions of lives. No later plea that the program was "
         "metaphor survives its own text."),
        ("E3", "Program: France is the mortal enemy and must be "
               "defeated and rendered harmless before Germany's "
               "eastern policy can proceed.",
         "PROVEN",
         "Proven as stated program (the closing argument of this "
         "volume's political chapters), and executed in May–June "
         "1940 — a fact the Audit records without adornment, since "
         "the fate of this item and of E2 is the standing answer to "
         "the consolation that the book was never meant literally. "
         "It was meant literally. It was also, in its ends, "
         "catastrophic for its own country — see C6."),
    ]),
]

AUDIT_INTRO = [
    "The Tower Audit is this edition's claim register for the "
    "volume: the factual claims, autobiographical legends, "
    "prophecies, and doctrines on which the book stands, entered "
    "one by one and tiered against the standard historical record. "
    "The tiers are the house tiers, defined on the Elements page: "
    "PROVEN (established by documents or records independent of the "
    "author), SUPPORTED (the weight of the record favors it), "
    "CONTESTED (the record is divided, incomplete, or cuts both "
    "ways), FALSE (contradicted by the record), UNVERIFIED (no "
    "evidence independent of the author's word).",
    "Two rules of the house govern the register. First, no tier "
    "without its reasoning: an item that cannot state why it stands "
    "where it stands does not stand. Second, composite claims are "
    "marked composite — where a documented fact carries a literary "
    "construction on its back (A11 is the type case), the Audit "
    "tiers the composite CONTESTED and says which half is which, so "
    "that neither the fact nor the construction borrows the other's "
    "credit. The benchmarks are named in the Preface's notes: "
    "Kershaw, Ullrich, Hamann, Weber, and the Institut für "
    "Zeitgeschichte critical edition of 2016. Where those "
    "authorities divide, the item is CONTESTED and the division is "
    "the finding.",
    "The register covers Volume One. It is built to extend: "
    "Volume Two's claims will take the next numbers in each group "
    "when that volume is bound.",
]


# ----------------------------------------------------------------------
# Frame pages
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
    centered(pdf, "Volume One (1925) — the German text, printed "
                  "whole, and answered", "noto", "I", 11.5, 6, 6)
    rule(pdf)
    centered(pdf, "A CRITICAL TEACHER'S REVISION (MAGVS)",
             "dejavu", "B", 13.5, 8, 2)
    centered(pdf, "An audit, not an endorsement", "noto", "BI",
             11.5, 6, 5)
    centered(pdf, "The apparatus and the Tower Audit are by",
             "noto", "", 10.5, 6)
    centered(pdf, "Johnathan 'Qasparr' Monroe", "dejavu", "B", 13, 7, 1)
    centered(pdf, "Authorship of the apparatus and audit attributed "
                  "exclusively to Johnathan 'Qasparr' Monroe (Greek, "
                  "-ARR, All Rights Reserved, Without Prejudice)",
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
              "printed here whole and unaltered. No English "
              "translation of the body is printed, and none of the "
              "in-copyright translations is used. The Flagpole above "
              "claims the apparatus and the audit only.",
         size=9.5, height=5, align="C", space_after=0)


def source_leaf(pdf):
    pdf.add_page()
    centered(pdf, "THE SOURCE OF THIS EDITION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Named, hashed, and declared before it is built on",
             "noto", "I", 10.5, 6, 6)
    para(pdf, "The German text printed in this volume is the text of "
              "the Internet Archive item “MeinKampfBand1-Eine"
              "Abrechnung” — the OCR full text of the Eher unabridged "
              "printing of Mein Kampf, 851.–855. Auflage, 1943 — as "
              "secured and hashed in the edition's Source Ledger "
              "(SHA-256 a5de081b761e16a03aa3ec2465a5141c6e2d5e22"
              "439016a2222bb420d30cb19) and cross-checked against a "
              "second Archive witness (SHA-256 8dae35c5…) on every "
              "test passage. Band 1 was first published on 18 July "
              "1925; the text was essentially stable across Eher "
              "printings. Two edition facts ride with that basis and "
              "are declared rather than smoothed: later printings "
              "carry small authorial corrections to the early text, "
              "and the Schlusswort that closes this volume was "
              "written in November 1926 and is not part of the 1925 "
              "first edition. A first-edition facsimile collation is "
              "UNCHARTED future work.")
    para(pdf, "The OCR state is declared in the Apparatus: the 1943 "
              "printing is Antiqua type and OCRs cleanly; ß and "
              "umlauts are intact; the stream's doubled spaces are "
              "collapsed in typesetting; a small residue of merged "
              "words (where the original sets emphasis in "
              "letterspaced type) and rare single-letter misreads "
              "are printed as found and flagged — never silently "
              "emended. The body's orthography is the 1943 printing's "
              "(daß, muß, and the rest), unmodernized.")
    para(pdf, "How to read this edition: the German text stands in "
              "the book's own order — Widmung, Vorwort, the twelve "
              "chapters, the Schlusswort. After each section stand "
              "English NOTES AND CORRELATIONS. The TOWER AUDIT at "
              "the back is the claim register, and may be read first "
              "by any reader who prefers the verdicts before the "
              "evidence. Short German fragments quoted inside the "
              "English apparatus carry the house's own renderings, "
              "marked as such.")


def elements_page(pdf):
    pdf.add_page()
    centered(pdf, "THE EDITION'S FOUR ELEMENTS", "dejavu", "B", 13, 8, 2)
    centered(pdf, "Inputs · Processes · Outputs · Tolerances",
             "noto", "I", 10.5, 6, 6)
    items = [
        ("INPUTS", "The complete German text of Band 1 from the "
                   "secured, hashed source named on the Source leaf: "
                   "Widmung, Vorwort, Kapitel 1–12, Schlusswort."),
        ("PROCESSES", "OCR reflowed to book measure under the "
                      "declared join rules; doubled spaces collapsed; "
                      "the source printing's Impressum page and its "
                      "printed Inhaltsverzeichnis excluded and the "
                      "exclusion declared; English chapter notes and "
                      "the Tower Audit composed against the standard "
                      "historical record and bound behind the text. "
                      "No sentence of the German body is touched."),
        ("OUTPUTS", "This volume: the whole German text of Volume "
                    "One in Critical Teacher's Revision (MAGVS) "
                    "dress, answered by its apparatus."),
        ("TOLERANCES", "Zero for the body: any process that would "
                       "change a German word fails the edition. Zero "
                       "for the Audit: any tier asserted without its "
                       "reasoning fails the item. What cannot be "
                       "verified is marked UNVERIFIED; what is open is "
                       "marked UNCHARTED; nothing is invented."),
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
              "evidence independent of the author's word). Apparatus "
              "labels: ATTESTED, DERIVED, CONSTRUCTED, UNCHARTED, as "
              "in the sibling editions.",
         size=10, space_after=0)


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
    entries = [("The Source of This Edition", toc.get("source")),
               ("The Edition's Four Elements", toc.get("elements")),
               ("Reviser's Preface", toc.get("preface"))]
    for key, head, sub in SECTIONS:
        label = head.title() if key in ("widmung", "vorwort",
                                        "schluss") else head
        entries.append((label, toc.get(key)))
        entries.append((f"Notes and Correlations — {label}",
                        toc.get(key + ":notes")))
    entries += [("THE TOWER AUDIT — Claim Register of This Volume",
                 toc.get("audit")),
                ("Apparatus of the Revision", toc.get("apparatus")),
                ("Table of Authorities", toc.get("authorities")),
                ("Colophon", toc.get("colophon"))]
    for name, page in entries:
        pdf.set_font("noto", "", 10.5)
        label = f"{name}    {page}" if page else name
        pdf.multi_cell(0, 6.4, label, new_x=XPos.LMARGIN,
                       new_y=YPos.NEXT)


def body_sections(pdf, sections, toc):
    by_key = dict(sections)
    for key, head, sub in SECTIONS:
        pdf.add_page()
        toc[key] = pdf.page_no()
        if key.startswith("kap"):
            num, title = head.split(" — ", 1)
            centered(pdf, num + ".", "dejavu", "B", 13, 8, 1)
            centered(pdf, title.upper(), "dejavu", "B", 14.5, 8, 1)
        else:
            centered(pdf, head, "dejavu", "B", 15, 10, 1)
            if sub:
                centered(pdf, sub, "noto", "I", 10.5, 6, 2)
        rule(pdf, 50)
        pdf.ln(2)
        for p in by_key[key]:
            para(pdf, p)
        # English notes ride immediately behind their section.
        pdf.add_page()
        toc[key + ":notes"] = pdf.page_no()
        centered(pdf, "NOTES AND CORRELATIONS", "dejavu", "B", 12, 8, 1)
        centered(pdf, head.title() if not key.startswith("kap") else
                 head, "noto", "I", 10.5, 6, 3)
        rule(pdf, 40)
        for i, note in enumerate(CHAPTER_NOTES[key], start=1):
            para(pdf, f"{i}. {note}", size=10, height=5.4,
                 space_after=1.8)


def audit_pages(pdf, toc):
    pdf.add_page()
    toc["audit"] = pdf.page_no()
    centered(pdf, "THE TOWER AUDIT", "dejavu", "B", 15, 10, 1)
    centered(pdf, "The Claim Register of This Volume",
             "noto", "I", 11, 6, 5)
    for p in AUDIT_INTRO:
        para(pdf, p)
    for group, items in AUDIT:
        pdf.ln(3)
        if pdf.get_y() > pdf.h - 50:
            pdf.add_page()
        centered(pdf, group, "dejavu", "B", 11.5, 7, 3)
        for code, claim, tier, why in items:
            if pdf.get_y() > pdf.h - 42:
                pdf.add_page()
            pdf.set_font("dejavu", "B", 10.5)
            pdf.multi_cell(0, 5.8, f"{code} — [{tier}]",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            para(pdf, f"Claim: {claim}", size=10.5, height=5.6,
                 space_after=0.6)
            para(pdf, why, size=10, height=5.4, space_after=3.4)


def apparatus_pages(pdf, toc):
    pdf.add_page()
    toc["apparatus"] = pdf.page_no()
    centered(pdf, "APPARATUS OF THE REVISION", "dejavu", "B", 13, 8, 2)
    centered(pdf, "What was done to the text, stated in the open",
             "noto", "I", 10.5, 6, 4)
    para(pdf, "The German text in this edition is the secured OCR "
              "text named in the Source Ledger (local copy retained "
              "with the edition's files). The following operations, "
              "and no others, were performed upon it by the builder:")
    for line in [
        "1. The OCR stream's hard line-wrapping was reflowed into "
        "book paragraphs: wrapped lines are joined with one space, "
        "except after a line-ending hyphen, where the join is direct "
        "and the hyphen kept. The stream's doubled inter-word "
        "spaces were collapsed to one. These are spacing operations; "
        "no word was added, removed, reordered, or respelled.",
        "2. Edition basis, declared: the witness is the Eher "
        "unabridged printing of 1943 (851.–855. Auflage), not a "
        "facsimile of the 1925 first edition. Later printings carry "
        "small authorial corrections, and the Schlusswort (November "
        "1926) is not part of the 1925 book. A first-edition "
        "collation is marked UNCHARTED and has not been performed.",
        "3. Excluded, and declared here rather than vanished: the "
        "1943 printing's Impressum page (its copyright and "
        "print-run furniture) and its printed Inhaltsverzeichnis. "
        "The edition supplies its own contents. Both exclusions "
        "stand in the source file, which the desk retains.",
        "4. OCR artifacts, printed as found: (a) about a dozen loci "
        "where the original's letterspaced emphasis defeated the "
        "OCR and words stand merged — the type case is the first "
        "chapter's “GleichesBlutgehörtineingemeinsamesReich” for "
        "“Gleiches Blut gehört in ein gemeinsames Reich”; (b) rare "
        "single-letter misreads — suspected loci include “ihren "
        "kauf” (Schluß des 12. Kapitels) for “ihren Lauf” and “lö.” "
        "in the Widmung's dateline for “16.” Neither class is "
        "silently emended; both are declared, so that no reader "
        "mistakes the scan's faults for the author's words, or the "
        "author's words for the scan's.",
        "5. No English translation of the body is printed. The "
        "standard translations (Manheim, 1943, and its fellows) are "
        "in copyright and were not used, consulted for the text, or "
        "reproduced. Short fragments quoted within the English "
        "notes carry the house's own renderings, marked as such.",
        "6. Body face: Noto Serif, which carries the German "
        "diacritics entire (ä ö ü Ä Ö Ü ß) and the German quotation "
        "marks as printed. The text's pre-reform orthography stands "
        "unmodernized.",
    ]:
        para(pdf, line, size=10, space_after=1.0)
    para(pdf, "No part of the German body has been abridged. If a "
              "future printing of this edition corrects an OCR "
              "artifact against a better witness, the correction will "
              "be entered as a dated addendum, as this house enters "
              "all dispositions: marked, never vanished.", size=10,
         space_after=1.4)

    toc["authorities"] = pdf.page_no()
    pdf.ln(1)
    centered(pdf, "TABLE OF AUTHORITIES (CONDENSED)", "dejavu", "B",
             12, 8, 3)
    for a in [
        "Hitler, Adolf. Mein Kampf. Erster Band: Eine Abrechnung. "
        "Munich: Franz Eher Nachf., 18 July 1925. (Text as printed "
        "in the unabridged Eher edition, 851.–855. Auflage, 1943 — "
        "see Apparatus, item 2.)",
        "Internet Archive item “MeinKampfBand1-EineAbrechnung” — "
        "OCR source text of the 1943 printing; SHA-256 as recorded "
        "in the edition's Source Ledger; cross-witness “AdolfHitler"
        "MeinKampfDEUTSCH” as recorded there.",
        "Hartmann, Christian, et al. (eds.). Hitler, Mein Kampf: "
        "Eine kritische Edition. Munich–Berlin: Institut für "
        "Zeitgeschichte, 2016 — the scholarly benchmark edition.",
        "Kershaw, Ian. Hitler 1889–1936: Hubris (1998); Hitler "
        "1936–1945: Nemesis (2000).",
        "Ullrich, Volker. Adolf Hitler: Die Jahre des Aufstiegs "
        "1889–1939 (2013); Eng. Hitler: Ascent 1889–1939 (2016).",
        "Hamann, Brigitte. Hitlers Wien: Lehrjahre eines Diktators "
        "(1996); Eng. Hitler's Vienna (1999).",
        "Weber, Thomas. Hitler's First War (2010).",
        "The Gemlich letter, Adolf Hitler to Adolf Gemlich, 16 "
        "September 1919 — the Audit's documentary anchor (C4).",
        "Hasher, Lynn, David Goldstein & Thomas Taylor. “Cognitive "
        "Consequences of Believing in False Information” / the "
        "illusory truth effect, Journal of Verbal Learning and "
        "Verbal Behavior 16 (1977) — and successors.",
        "UNESCO Statements on Race (1950, 1951); American Society "
        "of Human Genetics, statement on genetics and racial "
        "supremacy (2018) — for Audit D1.",
        "Graves, Philip. “The Truth about ‘The Protocols’,” The "
        "Times, 16–18 August 1921; Berne trial judgment (1934–35) "
        "— for Audit B6.",
        "The Teacher's Edition format (house directive, 2026) — "
        "the dress of this revision.",
    ]:
        para(pdf, a, size=10, space_after=1.0)

    pdf.add_page()
    toc["colophon"] = pdf.page_no()
    centered(pdf, "COLOPHON", "dejavu", "B", 13, 9, 6)
    para(pdf, "This Critical Teacher's Revision (MAGVS) of Mein "
              "Kampf, Erster Band, was generated on " + THELEMIC_DATE +
              ", by a programmatic builder (fpdf2, Noto Serif and "
              "DejaVu Serif faces) from the public-domain source "
              "named in the Table of Authorities, under the "
              "Teacher's Edition format of this house.")
    para(pdf, "Published by Bleats Publishing Group. SPARROW (Sole "
              "Proprietorship) — Johnathan 'Qasparr' Monroe, "
              "Proprietor — is the legal publisher of record.")
    para(pdf, "The apparatus, the notes, and the Tower Audit are "
              "the work of Johnathan 'Qasparr' Monroe, to whom their "
              "authorship is attributed exclusively, ARR — All "
              "Rights Reserved, Without Prejudice. The German text "
              "is public domain and is claimed by no one in this "
              "volume. This edition is an audit, not an endorsement.")
    para(pdf, "Method of Science. Aim of Religion.", align="C")
    pdf.ln(4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C", space_after=4)
    centered(pdf, "93 — Live, Love, and let Love, Live.", "dejavu",
             "B", 12, 8)


def build(toc, folio_total=None):
    Book.folio_total = folio_total
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, margin=20)
    pdf.alias_nb_pages()
    pdf.set_title("Mein Kampf, Erster Band — A Critical Teacher's "
                  "Revision (MAGVS)")
    pdf.set_author("Adolf Hitler (author of the text); Johnathan "
                   "'Qasparr' Monroe (reviser; apparatus and audit)")
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
    source_leaf(pdf)
    toc["source"] = 2
    elements_page(pdf)
    toc["elements"] = 3
    preface_page(pdf)
    toc["preface"] = 4
    contents_page(pdf, toc)
    body_sections(pdf, sections, toc)
    audit_pages(pdf, toc)
    apparatus_pages(pdf, toc)
    return pdf, toc


def main():
    toc = {}
    pdf, toc = build(toc)                      # pass one: measure
    folio_total = pdf.pages_count
    pdf, toc = build(toc, folio_total)         # pass two: print
    pdf.output(str(OUT))
    print(f"BUILT {OUT}")
    print(f"pages: {pdf.pages_count}")
    print(f"bytes: {OUT.stat().st_size}")
    tiers = {}
    n_items = 0
    for _g, items in AUDIT:
        for _c, _cl, tier, _w in items:
            tiers[tier] = tiers.get(tier, 0) + 1
            n_items += 1
    print(f"audit items: {n_items} | tiers: {tiers}")
    print(f"chapter notes: "
          f"{sum(len(v) for v in CHAPTER_NOTES.values())} notes over "
          f"{len(CHAPTER_NOTES)} sections")
    for k, v in toc.items():
        print(f"  {k}: p.{v}")


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
