#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

"Non est super terram potestas quae comparetur ei." — Job 41, the
verse Hobbes himself cites at the end of his twenty-eighth chapter.

LEVIATHAN — A PARALLEL EDITION (MAGVS). The English of 1651 facing
the Latin of 1668, built in bricks, pushed as it grows.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice)
X day of November, Dies Martis, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved and
coined under the authority of the Living Man. — The Flagpole on this
volume claims THE EDITION AND THE APPARATUS ONLY. Thomas Hobbes's
texts, English and Latin, are public domain; no claim reaches for
them, and the title page of the built book says so in plain words.

MECHANISM / DOCTRINE — how this builder works, and why:

  INPUT   English: Project Gutenberg eBook #3207, the text of record
          secured at this program's founding (2026-11-02), file
          editions/leviathan/source/pg3207.txt, SHA-256
          3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b204f
          60475009b7294 — re-asserted byte for byte on every run,
          exactly as the parent edition's builder asserts it.
          Latin: Internet Archive item leviathansivedem00hobb, the
          1668 Blaeu Latin Leviathan (Amsterdam), file
          source/leviathansivedem00hobb_djvu.txt, SHA-256
          5a364c05fb3dc6cdf03ad6cb273835368911ef5aa0a935d011467b9501
          c62b4d — asserted on every run. Full provenance, hashes,
          defect register, and the honest list of what was NOT done:
          SOURCE-LEDGER.md in this directory. The Latin is a
          SINGLE-WITNESS OCR TEXT (ABBYY OCR, Archive confidence 74)
          and is labelled so wherever the book speaks of it.
  PROCESS The English is parsed by the parent edition's own census
          logic (Introduction + chapters by CHAPTER headings). The
          Latin is extracted by content seams (SOURCE-LEDGER §III.4)
          and cleaned ONLY by the declared classes printed in this
          file: running-head and display-debris removal; line-end
          dehyphenation; punctuation spacing; the ampersand classes
          (& = et; intra-word & = the ct ligature; &c/8c/6c = etc.);
          the long-s restoration (the 1668 ſ, which the OCR renders
          "f", is restored to s ONLY under the ordered rule table
          below — protected genuine-f stems stand; unresolved and
          garbled tokens stand as the OCR gave them and are counted
          in the build report and the brick's collation notes); the
          listed token repairs (fused-word splits, drop-cap
          restoration, margin-debris removal) — every repair is data
          in this file and is printed in the book's apparatus.
          The Latin's own orthography otherwise stands AS PRINTED
          in 1668 (u/v, i/j as the OCR carries them): this house's
          epigraphic respelling governs the house's own Latin only,
          never Hobbes's text.
          ALIGNMENT: units pair by chapter; within a unit, blocks
          pair by index (a margin note travels with the paragraph
          it heads). A pagination planner measures every block on a
          scratch document at final measure, then packs pairs into
          spreads — Latin on the verso (even leaf), English on the
          recto (odd leaf) — closing a spread when either face
          would overflow. Divergence (block-count drift, unpaired
          tails) is measured and printed in the collation notes,
          never silently harmonized.
  OUTPUT  LEVIATHAN-PARALLEL-MAGVS.pdf — cumulative: each brick
          rebuilds the whole book to date (front matter, all units
          built so far, the brick's collation notes, Table of
          Authorities, Colophon). Multi-pass until the contents
          page is stable, as in the parent edition.
  TOLERANCE  Any step that would change a word of Hobbes beyond the
          declared classes fails the edition. Any Latin reading not
          traceable to the secured OCR text through a declared
          class fails the edition. The builder asserts both source
          hashes, the English chapter census, every Latin seam,
          and the contents stability before it writes the file.

  FONT TOLERANCE, declared: this host's DejaVu Serif carries no
  italic face; the body is set in DejaVu Serif regular/bold as the
  commission specifies, and emphasis is carried by furniture
  (spacing, small heads), never by a synthetic oblique.

  fpdf2 discipline (house gotcha, AGENTS.md 2026-10-04): every
  multi_cell is called with new_x=XPos.LMARGIN, new_y=YPos.NEXT so
  the pen returns to the left margin instead of dying at the right.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ----------------------------------------------------------------------
# Paths, hashes, constants
# ----------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
EN_SOURCE = HERE.parent / "leviathan" / "source" / "pg3207.txt"
LA_SOURCE = HERE / "source" / "leviathansivedem00hobb_djvu.txt"
LOGO = Path.home() / "workspace" / "templates" / "doctrine-logo.png"
OUT = HERE / "LEVIATHAN-PARALLEL-MAGVS.pdf"
REPORT = HERE / "build-report.json"

EN_SHA256 = ("3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b204f"
             "60475009b7294")
LA_SHA256 = ("5a364c05fb3dc6cdf03ad6cb273835368911ef5aa0a935d011467b9501"
             "c62b4d")

DEJAVU = "/usr/share/fonts/truetype/dejavu"

FLAGPOLE = ("Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, "
            "ARR, All Rights Reserved, Without Prejudice. Right of claim "
            "hereby reserved and coined under the authority of the "
            "Living Man.")
THELEMIC_DATE = ("X day of November, Dies Martis, Sol in Scorpio, "
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

# Brick register: (unit key, English title, Latin title). The build is
# cumulative; a brick ships when its units stand in this list.
UNITS_ALL = [
    ("intro", "THE INTRODUCTION", "INTRODUCTIO"),
    ("chI", "CHAPTER I — Of Sense", "CAPVT I — De Sensu"),
    ("chII", "CHAPTER II — Of Imagination", "CAPVT II — De Imaginatione"),
    ("chIII", "CHAPTER III — Of Consequence, or Train of Imaginations",
     "CAPVT III — De Consequentia sive Serie Imaginationum"),
    ("chIV", "CHAPTER IV — Of Speech", "CAPVT IV — De Sermone"),
    ("chV", "CHAPTER V — Of Reason, and Science",
     "CAPVT V — De Ratione et Scientia"),
    ("chVI", "CHAPTER VI — Of the Interior Beginnings of Voluntary "
     "Motion, commonly called the Passions",
     "CAPVT VI — De Principiis internis Motus Voluntarii, quae "
     "vulgo Passiones appellantur"),
    ("chVII", "CHAPTER VII — Of the Ends or Resolutions of Discourse",
     "CAPVT VII — De Discursuum Determinationibus"),
    ("chVIII", "CHAPTER VIII — Of Virtues and Defects Intellectual",
     "CAPVT VIII — De Virtutibus Intellectualibus et Defectibus "
     "Oppositis"),
    ("chIX", "CHAPTER IX — Of the Several Subjects of Knowledge",
     "CAPVT IX — De Scientiarum Distributione"),
    ("chX", "CHAPTER X — Of Power, Worth, Dignity, Honour, and "
     "Worthiness", "CAPVT X — De Potentia, Dignitate, et Honore"),
    ("chXI", "CHAPTER XI — Of the Difference of Manners",
     "CAPVT XI — De Varietate Morum"),
    ("chXII", "CHAPTER XII — Of Religion",
     "CAPVT XII — De Religione"),
    ("chXIII", "CHAPTER XIII — Of the Natural Condition of Mankind",
     "CAPVT XIII — De Conditione generis Humani quantum attinet "
     "ad Felicitatem praesentis vitae"),
    ("chXIV", "CHAPTER XIV — Of the First and Second Natural Laws, "
     "and of Contracts",
     "CAPVT XIV — De Lege Naturae prima et fundamentali"),
    ("chXV", "CHAPTER XV — Of Other Laws of Nature",
     "CAPVT XV — De caeteris Legibus Naturae"),
    ("chXVI", "CHAPTER XVI — Of Persons, Authors, and Things "
     "Personated", "CAPVT XVI — De Personis et Authoribus"),
    ("chXVII", "CHAPTER XVII — Of the Causes, Generation, and "
     "Definition of a Commonwealth",
     "CAPVT XVII — De Causa, Generatione, et Definitione Civitatis"),
    ("chXVIII", "CHAPTER XVIII — Of the Rights of Sovereigns by "
     "Institution",
     "CAPVT XVIII — De Iure habentium Summam Potestatem in Civitate "
     "per Institutionem"),
    ("chXIX", "CHAPTER XIX — Of the Several Kinds of Commonwealth "
     "by Institution, and of the Succession to the Sovereign Power",
     "CAPVT XIX — De Generibus Civitatum per Institutionem, et de "
     "Successione ad Summam Potestatem"),
    ("chXX", "CHAPTER XX — Of Dominion Paternal and Despotical",
     "CAPVT XX — De Dominio Paterno et Despotico"),
    ("chXXI", "CHAPTER XXI — Of the Liberty of Subjects",
     "CAPVT XXI — De Libertate Civium"),
    ("chXXII", "CHAPTER XXII — Of Systems Subject, Political, and "
     "Private", "CAPVT XXII — De Systematibus Civium"),
    ("chXXIII", "CHAPTER XXIII — Of the Public Ministers of "
     "Sovereign Power",
     "CAPVT XXIII — De Potestatis Summae Ministris Publicis"),
    ("chXXIV", "CHAPTER XXIV — Of the Nutrition, and Procreation "
     "of a Commonwealth",
     "CAPVT XXIV — De Civitatis Facultate Nutritiva et Generativa"),
    ("chXXV", "CHAPTER XXV — Of Counsel", "CAPVT XXV — De Consilio"),
    ("chXXVI", "CHAPTER XXVI — Of Civil Laws",
     "CAPVT XXVI — De Legibus Civilibus"),
    ("chXXVII", "CHAPTER XXVII — Of Crimes, Excuses, and "
     "Extenuations",
     "CAPVT XXVII — De Criminibus, Excusationibus, et "
     "Extenuationibus"),
    ("chXXVIII", "CHAPTER XXVIII — Of Punishments, and Rewards",
     "CAPVT XXVIII — De Poenis et Praemiis"),
    ("chXXIX", "CHAPTER XXIX — Of Those Things That Weaken, or "
     "Tend to the Dissolution of a Commonwealth",
     "CAPVT XXIX — De iis rebus quae Civitatem labefactant, "
     "tenduntque ad dissolutionem eius"),
    ("chXXX", "CHAPTER XXX — Of the Office of the Sovereign "
     "Representative", "CAPVT XXX — De Officio Summi Imperantis"),
    ("chXXXI", "CHAPTER XXXI — Of the Kingdom of God by Nature",
     "CAPVT XXXI — De Regno Dei Naturali"),
    # Part III (De Civitate Christiana). Latin titles per each
    # chapter's own display, the contents leaf as witness (N15);
    # English titles as #3207 prints them, spelling modernized
    # only where Part I's practice modernized.
    ("chXXXII", "CHAPTER XXXII — Of the Principles of Christian "
     "Politiques",
     "CAPVT XXXII — De Politicae Christianae Principiis"),
    ("chXXXIII", "CHAPTER XXXIII — Of the Number, Antiquity, Scope, "
     "Authority, and Interpreters of the Books of Holy Scripture",
     "CAPVT XXXIII — De Numero, Antiquitate, Scopo, Authoritate et "
     "Interpretibus Librorum Sacrorum"),
    ("chXXXIV", "CHAPTER XXXIV — Of the Signification of Spirit, "
     "Angel, and Inspiration in the Books of Holy Scripture",
     "CAPVT XXXIV — De Significatione quam habent in Scripturis "
     "Sacris Vocabula Spiritus, Angelus, Inspiratio"),
    ("chXXXV", "CHAPTER XXXV — Of the Signification in Scripture of "
     "Kingdome of God, of Holy, Sacred, and Sacrament",
     "CAPVT XXXV — De Significatione in Scripturis Sacris "
     "Vocabulorum Regnum Dei, Sanctum, Sacrum et Sacramentum"),
    ("chXXXVI", "CHAPTER XXXVI — Of the Word of God, and of "
     "Prophets", "CAPVT XXXVI — De Verbo Dei et Prophetis"),
    ("chXXXVII", "CHAPTER XXXVII — Of Miracles, and Their Use",
     "CAPVT XXXVII — De Miraculis et eorum Usu"),
    ("chXXXVIII", "CHAPTER XXXVIII — Of the Signification in "
     "Scripture of Eternall Life, Hell, Salvation, the World to "
     "Come, and Redemption",
     "CAPVT XXXVIII — De Significatione quam habent in Scripturis "
     "Sacris Vocabula Vita Aeterna, Infernum, Salvatio, Mundus "
     "Venturus et Redemptio"),
    ("chXXXIX", "CHAPTER XXXIX — Of the Signification in Scripture "
     "of the Word Church",
     "CAPVT XXXIX — De Significatione quam habet in Scripturis "
     "Sacris Vocabulum Ecclesia"),
    ("chXL", "CHAPTER XL — Of the Rights of the Kingdome of God, "
     "in Abraham, Moses, High Priests, and the Kings of Judah",
     "CAPVT XL — De Iure Regni Dei in Abrahamo, Mose, Summis "
     "Sacerdotibus et Regibus Iudae"),
    ("chXLI", "CHAPTER XLI — Of the Office of Our Blessed Saviour",
     "CAPVT XLI — De Servatoris Nostri Benedicti Officio"),
    ("chXLII", "CHAPTER XLII — Of Power Ecclesiasticall",
     "CAPVT XLII — De Potestate Ecclesiastica"),
]
BRICK = 14
UNITS_BUILT = UNITS_ALL[:43]         # Parts I–II; Part III to XLII
BRICK_SCOPE = ("front matter, the whole of Part I (De Homine) — the "
               "Introduction and Chapters 1–16 — the whole of "
               "Part II (De Civitate), Chapters 17–31, and Part III "
               "(De Civitate Christiana) Chapters 32–42 in parallel")

# Latin seams in the secured djvu text, 1-based lines, by content
# (SOURCE-LEDGER §III.4): unit key -> (first line, last line).
LA_SEAMS = {
    "intro": (114, 210),
    "chI": (213, 278),
    "chII": (280, 504),
    "chIII": (506, 705),
    "chIV": (706, 1054),
    "chV": (1055, 1303),
    "chVI": (1304, 1709),
    "chVII": (1710, 1815),
    "chVIII": (1816, 2205),
    "chIX": (2206, 2265),
    "chX": (2266, 2595),
    "chXI": (2596, 2850),
    "chXII": (2851, 3260),
    "chXIII": (3261, 3420),
    "chXIV": (3421, 3727),
    "chXV": (3728, 4101),
    "chXVI": (4102, 4253),
    # Part II seams (Brick 6), located by content as Part I's were:
    # each seam opens at the chapter's own display line and closes
    # the line before the next display. Capvt XVII's display is the
    # spaced form at line 4254, directly under the PARS SECUNDA
    # display (lines 4245–4252, which stand inside Capvt XVI's seam
    # and are dropped there under the display classes, as Part I's
    # display was). Capvt XIX's display is likewise spaced (4704).
    "chXVII": (4254, 4409),
    "chXVIII": (4410, 4703),
    "chXIX": (4704, 5014),
    # Brick 7 seams, by content as before: XX's display is the
    # spaced form at 5015; XXI's at 5294; XXII's at 5642.
    "chXX": (5015, 5293),
    "chXXI": (5294, 5641),
    "chXXII": (5642, 6015),
    # Brick 8 seams, by content as before: XXIII's display at 6016,
    # XXIV's at 6125, XXV's at 6298 — the last in the machine's
    # F-for-P reading ('C A F V T XXV.'), for which the display
    # class is widened at this brick (see clean_latin_lines).
    "chXXIII": (6016, 6124),
    "chXXIV": (6125, 6297),
    "chXXV": (6298, 6493),
    # Brick 9 seams, by content as before: XXVI's display is the
    # spaced form at 6494 (its numeral without the press's point),
    # XXVII's at 6940, XXVIII's spaced at 7381 with its numeral
    # garbled ('X X V I I L').
    "chXXVI": (6494, 6939),
    "chXXVII": (6940, 7380),
    "chXXVIII": (7381, 7629),
    # Brick 10 seams, by content as before: XXIX's display at 7630,
    # XXX's at 7960, XXXI's at 8413 (its numeral garbled 'XXX L');
    # XXXI closes the line before Part III's first display (8736).
    "chXXIX": (7630, 7959),
    "chXXX": (7960, 8412),
    "chXXXI": (8413, 8735),
    # Brick 11 seams (Part III): XXXII's display at 8736 directly
    # under the PARS TERTIA display (8727–8733, inside XXXI's
    # seam, dropped there); XXXIII's at 8887, XXXIV's at 9200;
    # XXXIV closes the line before XXXV's display (9565).
    "chXXXII": (8736, 8886),
    "chXXXIII": (8887, 9199),
    "chXXXIV": (9200, 9564),
    # Brick 12 seams: XXXV's display at 9565, XXXVI's at 9778,
    # XXXVII's at 10244; XXXVII closes before XXXVIII's (10467).
    "chXXXV": (9565, 9777),
    "chXXXVI": (9778, 10243),
    "chXXXVII": (10244, 10466),
    # Brick 13 seams: XXXVIII's display at 10467, XXXIX's at
    # 10917 (a short chapter, 80 lines), XL's at 10997; XL closes
    # the line before XLI's display (11326).
    "chXXXVIII": (10467, 10916),
    "chXXXIX": (10917, 10996),
    "chXL": (10997, 11325),
    # Brick 14 seams: XLI's display at 11326, XLII's at 11563
    # (numeral garbled 'XLIL'; the chapter is fixed by its title,
    # 'De Potestate Ecclesiastica'); XLII closes the line before
    # XLIII's display (13924).
    "chXLI": (11326, 11562),
    "chXLII": (11563, 13923),
}

# ----------------------------------------------------------------------
# The Latin cleaning classes (declared in the ledger and the Preface)
# ----------------------------------------------------------------------
# Running heads / display debris: whole lines the edition never sets.
LA_DROP_LINE_RES = [
    re.compile(r"^Cap\.\s+\d+;?\.?\s+.*\d+,$"),            # "Cap. 4; De Homint. 13,"
    re.compile(r"^\d+\s+De Homine\. Cap\. \d+\.$"),        # "14 De Homine. Cap. 4."
    re.compile(r"^Cap\.\s+\S+\s+.*\s\d+$"),                # "Cap. i. De Hominc. 5"
    # Brick 7: the same heads with the chapter number itself
    # garbled past digits ('Cap. zo. T>e Civitate. i o i';
    # 'Cap. 2i„ De Civitate, icp'). The shape is the furniture's:
    # Cap. + short token + short token + Civit- + tail. Brick 8:
    # one head carries a fourth short token before the Civit-
    # word ('Cap. if. JDe Cwitate. yzj-'), admitted likewise.
    re.compile(r"^Cap\.\s+\S{1,4}\s+(\S{1,3}\s+)?\S{1,3}\s+"
               r"Civit\w*[.,]\s+.*$"),
    re.compile(r"^\S{1,3}\s+D\S*\s+Civitate\.\s+Cap\..*$"),  # "H4 D* Civitate. Cap. 22."
    re.compile(r"^Cap\.\s+\d+[.,]?\s+.*$"),  # running heads, tail garbled
    # Brick 6: Part II's running heads, in the machine's wide
    # spacing and with garbled tails the rules above cannot reach
    # ("86 De Civitate. Cap. i8„"; the leaf number itself split,
    # "8 4 D* Civitate. Cap. 17."; the signature read into the
    # number, "S8 De Civitate. Cap. i£."). Same class: press
    # furniture, never text.
    re.compile(r"^\d+\s+De\s+\w+\.\s+Cap\..*$"),
    re.compile(r"^[A-Z]\d+\s+De\s+\w+\.\s+Cap\..*$"),
    re.compile(r"^\d+\s+\d+\s+D\S*\s+Civitate\.\s+Cap\..*$"),
    re.compile(r"^\d+\s+\S{1,3}\s+Civita\w*\.\s+Cap\..*$"),
    re.compile(r"^\d+\)\d+\s+De\s+Civitate\.\s+Cap\..*$"),
    # The signature line at a leaf's foot, carrying its catchword
    # with it ("Leviat. n n n exerci-", "Leviat. 000 mam"): the
    # catchword's word stands whole at the next leaf's head.
    re.compile(r"^Leviat\.\s+.*$"),
    # Brick 8: a Part II head whose leaf number the machine read
    # as a word ('in De Civitate* Cap. 24.').
    re.compile(r"^\S{1,3}\s+De\s+Civitat\w*[^A-Za-z\s]?\s+Cap\..*$"),
    re.compile(r"^C\s*A-?$"),                              # drop-cap debris "C A-"
    re.compile(r"^[JjH\|\^\s]+$"),                         # initial-border debris
    re.compile(r"^LE\s+VIATHAN$"),
    re.compile(r"^P\s*A\s*R\s*S.*PRIMA$"),
    re.compile(r"^D\s*E\s+H\s*O\s*M\s*I\s*N\s*E\.$"),
    # Brick 10: the PARS TERTIA display standing inside Capvt
    # XXXI's seam tail, line by line as the machine gives it,
    # with its leaf-number debris ('*75').
    re.compile(r"^D\s+E$"),
    re.compile(r"^D\s+E\s+CIVITATE$"),
    re.compile(r"^CHRISTIANA\.$"),
    re.compile(r"^\*\d{1,3}$"),
    # Brick 10, completing the same class for PARS SECUNDA: its
    # display lines stood as note-shaped blocks at Capvt XVI's
    # tail through Brick 9 ('De Civitate', 'S I V E',
    # 'Repvblica.') — display furniture, never text (see N28).
    re.compile(r"^DE\s+CIVITATE$"),
    re.compile(r"^S\s*I\s*V\s*E$"),
    re.compile(r"^REPVBLICA\.$"),
    re.compile(r"^C\s*A\s*[PF]\s*V\s*T.*$"),               # chapter display lines
    re.compile(r"^G\s*A\s*P\s*V\s*T.*$"),                  # (OCR's G for C)
    re.compile(r"^De\s+(Senfu|Imaginatione|Confequcntia|Strmone)\.$"),
    re.compile(r"^\d{1,3}$"),                              # bare page numerals
    re.compile(r"^L\w{2,5}t\.$"),                          # signature "Leviat." as OCR'd
]

# Whole blocks that are press furniture (signature marks), never text.
LA_FURNITURE_BLOCKS = {
    "b bb", "b b b",
    # Brick 6, Capvt XVII: the signature shard and the catchword
    # standing alone at XVII's first leaf turn; the paragraph's own
    # first word stands whole at its head on the next leaf.
    "m m m 2 Neque",
    # Brick 6, Capvt XVII: a catchword shard ('Tertio' misread)
    # standing alone at the leaf turn; the word stands whole at
    # the next paragraph's head.
    "Tertid,",
    # Brick 6, Capvt XIX: the same class ('Potestas' misread),
    # standing alone before the leaf's running head.
    "Po:eilas",
    # Brick 7, Capvt XX: the ampersand's shard standing alone at
    # a leaf turn ('Sc', the machine's reading of &); the
    # conjunction itself stands at the next block's head.
    "Sc",
    # Brick 8, Capvt XXIV: the signature line with its catchword
    # ('omnium'), the signature itself misread ('Ltviat.'); the
    # catchword's word stands at the next leaf's head.
    "Ltviat. rts omniun»",
    # Brick 9, Capvt XXVIII: the decorated initial's shard
    # standing alone before the paragraph it ornaments ('A
    # Definitione Poenae deduco…'); the word stands whole at
    # the paragraph's head.
    "Ade*",
    # Brick 11 (Part III): leaf-turn catchwords standing alone,
    # each the first word of the paragraph that follows it —
    # Capvt XXXII's 'In' (before 'In his Verbis notanda…'),
    # Capvt XXXIII's 'Octo,', 'Capitis', 'Spiritu' (N29). The
    # 'In' entry also takes Capvt XIII's catchword of the same
    # shape, which had stood as a note since Brick 5.
    "In", "Octo,", "Capitis", "Spiritu",
    # Brick 11, recorded repair of an earlier part (N29): a
    # running head of Capvt XIII ('64 De Homine. Cap. 13.') that
    # the machine's garble carried past the head classes as a
    # text block; it is the press's furniture, listed here as
    # such. The leaf's catchword and text stand whole.
    '64 ®\'e Homine. Cap. 13."',
    # Brick 12 (Part III): a signature shard with its catchword
    # at a leaf turn in Capvt XXXV ('Leviat.' misread + gathering
    # letters + 'in', the next leaf's first word), and two
    # running heads of the Part III form standing alone as
    # blocks (Capvt XXXV's '194 … Cap. 36.' interleave and
    # Capvt XXXVII's '208 … Cap. 37.') — the heads' chapters and
    # leaves are the press's furniture (N30).
    "Levtat, c c c c in",
    "194 De Civitate chrisliana. Cap. $6.",
    "20 8 De Civitate chrisliana. • Cap. $&.",
    # Brick 12, Capvt XXXVII: the catchword 'Fidori' (the press's
    # 'Victori' misread) standing alone before the leaf's head;
    # the word stands at the next paragraph's head (N30).
    "Fidori",
    # Brick 12, Capvt XXXVI: the catchword shard '&de' — the
    # next leaf's opening '& de' read in the foot of the last.
    "&de",
    # Brick 13, Capvt XXXVIII: the catchword 'Iacobi.' standing
    # alone at the leaf turn; the word stands whole at the next
    # leaf's head ('Iacobi. Non est enim Deus mortuorum…').
    "Iacobi.",
    # Brick 14, Capvt XLII: two catchwords standing alone at
    # leaf turns ('Inquo' before 'In quo primum Concilio…';
    # 'Ccetus', Coetus misread, before 'Coetus tamen illos
    # elegit…'), and a running head of the Part III form
    # standing alone as a block ('196 De Civitate Christiana.
    # Cap. 42.', its numerals garbled) — its removal seats the
    # severed tail it interrupted under signature six (N32).
    "Inquo", "Ccetus",
    "1)6 De 'Civitate ckrisiiana. Cap. 42.",
}

# Margin-debris shards fused into body lines by the OCR (Capvt III,
# the Conjectura locus): removed, and the margin note restored as a
# subhead at the same locus — see REPAIR_NOTES in the apparatus data.
LA_DEBRIS_TOKENS = {"Ctxje8ura", "T-venti."}

# Listed token repairs: OCR reading -> restored reading. Fused-word
# splits restore a word boundary; drop-cap and ligature repairs
# restore a certain letter. Every entry is printed in the apparatus.
LA_REPAIRS = {
    "Aturam": "[N]aturam",          # the Introduction's drop cap
    "ideft": "id est", "aliudeft": "aliud est", "noneft": "non est",
    "noneftj": "non est", "cumfit": "cum sit", "tantumfit": "tantum sit",
    "quaeeft": "quae est", "futuraefunt": "futurae sunt",
    "fivefacultatem": "sive facultatem",
    "fomniumdiftinguere": "somnium distinguere",
    "fcientiamquamlibetacquirere": "scientiam quamlibet acquirere",
    "aliaquelocaconfecrata": "aliaque loca consecrata",
    "phantalmahabuiflehorribile": "phantasma habuisse horribile",
    "corporisfentientis": "corporis sentientis",
    "cordiumfuorum": "cordium suorum",
    "defuturotempore": "de futuro tempore",
    "minuseftin": "minus est in", "tamfortuitaeft": "tam fortuita est",
    "tantumexiftunt": "tantum existunt",
    "confequcntia": "consequentia", "ccnfiquens": "consequens",
    "qu£": "quae", "pra?fumtio": "praesumptio",
    "prasceffit": "praecessit", "praeceitifte": "praecessisse",
    "prasfenti": "praesenti", "prasfentis": "praesentis",
    "prasfumptio": "praesumptio", "raanifeftum": "manifestum",
    "senftonem": "sensionem", "fadtorum": "factorum",
    "Tinitum": "Finitum", "bonoremns": "honoremus",
    "inpartes": "in partes", "adionefque": "actionesque",
    "farcilegiam": "sacrilegiam", "fururis": "futuris",
    "fuura": "futura", "elafirum": "elastrum", "elaftris": "elastris",
    "objetlum": "Objectum", "disleremus": "disseremus",
    "neceslaria": "necessaria", "obstatquo": "obstat quo",
    "minusdicamus": "minus dicamus", "dcus": "Deus",
    "arshumana": "Ars humana", "rotuke": "rotulae",
    "nobilislimum": "nobilissimum", "opisicium": "opificium",
    "chrisiiana": "Christiana",
    # Capvt II, first paragraph (a noisier leaf; one-letter OCR
    # substitutions in certain words, sense fixed by the parallel
    # English at the same locus):
    "esle": "esse", "elte": "esse", "movealur": "moveatur",
    "seipsumj": "seipsum", "alirs": "aliis",
    "quasidesesla": "quasi desessa", "siia": "sua",
    "succeslionem": "successionem",
    # a decorated-initial column shard fused into Capvt IV's first
    # sentence ("collata tamen Semwh cum inventione"): deleted, the
    # sentence's own words being whole on both sides of it
    "semwh": "",
    # Brick 3 loci, same certainty classes:
    "irtus": "virtus",          # Capvt VIII ¶1: drop-cap V consumed
    "siint": "sunt",            # Capvt IX ¶1: ſunt misread whole
    "motta": "motus",           # Capvt IX: 'Magnitudo et Motus'
    "mwes": "mores",            # Capvt XI ¶1: 'Per Mores intelligo'
    "prajsentis": "praesentis", # Capvt XI: ſ read as j
    "scelicitatem": "felicitatem",  # Capvt XI: F read as Sc
    "ixjs": "ius",              # Capvt XIV ¶1: drop-cap I + 'us'
    # (Capvt XII's 'fructus' needed no repair: the fru- stem joined
    # the genuine-f protection table at Brick 5.)
    # Brick 6 loci, same certainty classes:
    "uod": "[Q]uod",            # Capvt XVII ¶1: drop-cap Q consumed
    "dlftinctio": "distinctio",  # Capvt XIX ¶1: D-i read as D-l,
                                # sense fixed by the English face
                                # ('The difference of Commonwealths')
}

# Phrase-level repairs (2): fusions spanning a word boundary that no
# token rule can reach. (1) Capvt VII ¶1 'vel m Adeptione' — the
# tail of 'in' fused as a stray token; the English face reads
# 'either in Adeption or Rejection'. (2) reserved.
LA_PHRASE_REPAIRS = [
    ("vel m Adeptione", "vel in Adeptione"),
]
# Repairs are keyed case-insensitively; the values carry the case.
LA_REPAIRS = {k.lower(): v for k, v in LA_REPAIRS.items()}

# FACSIMILE FIRST-BLOCK OVERRIDES for chapter openings whose
# decorated-initial leaves garble the same way (Brick 2): Capvt V
# (1668 p. 20; secured PDF leaf 28) and Capvt VI (1668 p. 25; PDF
# leaf 33). Each entry: (assertion substring of the garbled OCR
# block, [blocks to set]). The margin note the leaf carries is set
# first, as Hobbes's furniture.
LA_FACSIMILE_FIRST = {
    "chV": ("Xatm", [
        {"note": "Ratio."},
        {"text": "[Q]ui ratiocinatur, vel Totum quaerit Additione "
                 "partium; vel Residuum, Subtractione partis a "
                 "parte: id quod (si verbis fiat) nihil aliud est, "
                 "praeter Conceptionem consequentiae Nominis partis "
                 "ad Nomen totius, vel Nominum totius et partis ad "
                 "Nomen partis reliquae. Quanquam autem in rebus "
                 "quibusdam (ut in numeris) aliae sint operationes, "
                 "praeter Additionem et Subtractionem, ut "
                 "Multiplicatio et Divisio, in idem tamen recidunt; "
                 "nam Multiplicatio est aequalium inter se Additio; "
                 "et Divisio aliud non est, quam ejusdem rei, "
                 "quoties possumus, Subtractio. Neque Numeris solis "
                 "operationes illae conveniunt, sed omni rerum "
                 "generi, quarum una alteri addi vel auferri potest. "
                 "Sicut enim Arithmetici Addere et Subtrahere solent "
                 "in Numeris; ita Geometrae facere idem docent in "
                 "Lineis, Figuris, Angulis, Proportionibus, "
                 "Temporibus, Gradibus velocitatis, Virium, "
                 "Potentiae, et caeteris. Idem etiam Logici faciunt "
                 "in consequentiis verborum, Addentes duo nomina ad "
                 "faciendam propositionem, et duas propositiones ad "
                 "faciendum Syllogismum, et plures Syllogismos ad "
                 "faciendam Demonstrationem; et a summa sive "
                 "conclusione Syllogismi subtrahunt unam "
                 "propositionem, ad inveniendam alteram. Etiam "
                 "Scriptores Politici addunt simul plura pacta, ad "
                 "inveniendum hominis Officium; et Iuris Consulti "
                 "addunt simul Leges et Facta ad inveniendum, quid "
                 "sit in actionibus hominum privatorum Ius et "
                 "Injuria. Ubicunque locus est Additioni, et "
                 "Subtractioni, ibi etiam locus est Rationi; et ubi "
                 "illis locus non est, ibi neque rationi locus est."},
    ]),
    "chVI": ("Duosuntmotuumin", [
        {"note": "Motus Vitalis et Animalis."},
        {"text": "[D]uo sunt Motuum in Animalibus genera ipsis "
                 "propria. Quorum unus est Vitalis, in generatione "
                 "inceptus, et sine interruptione per totam vitam "
                 "continuatus; qualis est Motus Sanguinis, Pulsus, "
                 "Spirationis, Concoctionis, Nutritionis, "
                 "Excretionis, qui Imaginationis Auxilio non "
                 "indigent. Alter dicitur Animalis, et Voluntarius; "
                 "qualis est incessus, locutio, et artuum Motus, "
                 "qualem prius animo cogitaveramus. Sensum, Motum "
                 "esse in Organis, et Partibus internis corporis "
                 "humani, factum ab Objectis Visis, Auditis, etc. "
                 "Phantasiam autem esse ejusdem Motus post "
                 "Sensionem reliquias, dictum ante est in Cap. "
                 "primo et secundo. Quoniam autem incessus, "
                 "loquela, et similes Motus Voluntarii, semper "
                 "dependent ab aliqua praecedente cogitatione, Quo, "
                 "qua via, et Quid, manifestum est Phantasiam "
                 "Motuum omnium voluntariorum Principium internum "
                 "primum esse. Etsi autem sint qui Motum omnino "
                 "ullum esse negant, ubi res mota invisibilis, aut "
                 "spatium in quo movetur, propter brevitatem, "
                 "insensibile est, illud tamen non impedit, quo "
                 "minus hujusmodi Motus sint. Quantulumcunque enim "
                 "spatium sit, id quod Movetur per spatium majus, "
                 "cujus parvum illud spatium pars est, per illud "
                 "etiam necessario movebitur. Principia haec Motus "
                 "parva, intra humanum corpus sita, antequam "
                 "incedendo, loquendo, percutiendo, caeterisque "
                 "actionibus visibilibus appareant, vocantur "
                 "Conatus."},
    ]),
}

# FACSIMILE OVERRIDE — the Introduction's first printed page (1668
# p. 1; secured PDF leaf 9). The machine reading of this art page is
# shard-ridden past the reach of the token classes (the decorated
# initial's column interleaves the text). The leaf was rendered from
# the secured PDF and read at the desk; the blocks below are that
# reading, with the press's & resolved under the declared ampersand
# class and its ſ under the rule table. Basis: SOURCE-LEDGER
# amendment of 2026-11-10 (spot adjudication at a named locus).
LA_FACSIMILE_INTRO = [
    {"text": "[N]aturam, id est, illam, qua Mundum Deus condidit "
             "et gubernat, divinam Artem, eatenus imitatur Ars "
             "humana, ut possit inter alia producere artificiale "
             "Animal. Cum enim vita nihil aliud sit quam artuum "
             "motus, cujus principium est internum in parte aliqua "
             "Corporis principali, Quid obstat quo minus dicamus, "
             "Automata omnia, sive machinas omnes quae ab Elastris "
             "Rotulisque intus dispositis motum habent, ut Horologia "
             "in seipsis, habere etiam artificialem vitam? Quid est "
             "cor, nisi Elastrum, quid Nervi, nisi chordae, quid "
             "articuli, nisi totidem rotulae, motum, qualem voluit "
             "artifex, toti corpori impertientes? Neque animal "
             "tantum imitatur Ars, sed etiam nobilissimum animalium, "
             "Hominem. Magnus ille Leviathan, quae Civitas "
             "appellatur, opificium Artis est, et Homo artificialis, "
             "quanquam Homine naturali (propter cujus protectionem "
             "et salutem excogitatus est) et mole et robore multo "
             "major. In quo Is qui summam habet Potestatem, pro "
             "Anima est, corpus totum vivificante et movente. "
             "Magistratus et Praefecti, artificiales Artus. Praemia "
             "et Poenae summae Potestati appensae, et a quibus "
             "Membra ad suum cujusque opus perficiendum incitantur, "
             "Nervi sunt, qui idem faciunt in corpore naturali. "
             "Divitiae singularium hominum sunt pro robore. Salus "
             "populi, pro Negotio. Consiliarii per quos ea, quae "
             "cognitu necessaria illi sunt, suggeruntur pro Memoria "
             "sunt. AEquitas Legesque pro artificiali Ratione. "
             "Concordia, sanitas est. Seditio, Morbus. Bellum "
             "civile, Mors. Postremo Pacta quibus partes corporis "
             "hujus politici conglutinantur, imitantur divinum "
             "illud verbum Fiat, sive Faciamus Hominem, a Deo "
             "prolatum in principio cum crearet Mundum."},
    {"text": "Hominis hujus Artificialis naturam describens, "
             "considerabo"},
    {"text": "1. Materiam ejus, et Artificem, id est Hominem."},
    {"text": "2. Quo modo, et quibus Pactis factus est; quae Iura, "
             "quae Potestas sive Authoritas ejus est; et in quo "
             "residet Potestas summa."},
    {"text": "3. Quid est Civitas Christiana."},
    {"text": "4. Quid est Regnum Tenebrarum."},
]

# Garbles that stand as the OCR gave them (counted as residue in the
# report and the apparatus). No guessing: the facsimile adjudication
# of these loci is UNCHARTED.
LA_RESIDUE = {
    "afrkiamur", "ccmpcfta", "ccmpftta", "culofi", "eflk", "effecl",
    "efficut", "facli", "firaul", "frry", "fri", "fra", "flu", "fj",
    "fme", "iutef", "mentafem", "nifcor", "defun", "fadu", "forie",
    "fa", "efre", "recluruseft", "toteftaifumma",
    "tftfjquihominipeculiariseft", "fen", "fin", "pof", "ft",
    "mmm",          # Brick 6: signature debris inside Capvt XVII's
                    # definition paragraph ("tantam Potentiam mmm 2 &")
}

# Genuine-f protection: stems whose f is the press's real f, not ſ.
# (Initial-stem patterns evaluated on the lowercase token.)
LA_PROTECT_STEMS = (
    "fac", "faci", "fact", "facul", "fabul", "facin", "fam", "fast",
    "faun", "fall", "fem", "fenestr", "fenestr", "figment", "figur",
    "fid", "fili", "filu", "final", "finis", "finit", "finem", "firm",
    "fix", "flam", "flor", "fluct", "fluid", "fore", "form", "fort",
    "foss", "fue", "fui", "fut", "fulg", "fund", "funct", "frequen",
    "fret", "fru", "frat", "frau", "frag", "frang", "fren", "front",
)
# Medial genuine-f stems (assimilation and facio-compounds): a token
# containing one of these keeps the f inside the stem.
LA_PROTECT_MEDIAL = (
    "effic", "effect", "affic", "offic", "suffic", "profic", "infic",
    "perfic", "refic", "defici", "confic", "diffic", "differ",
    "defin", "confus", "confut", "artif",
)
LA_PROTECT_TOKENS = {
    "fecit", "feci", "fecisse", "seu", "fore", "forte", "fortis",
    "falsa", "falsi", "falsum", "falso", "falsae", "falsis",
    "stupefiunt",
}


def _long_s_token(tok):
    """Restore one token under the ordered long-s rules. Returns the
    restored token. Case: rules run on the lowercase form; an initial
    capital is restored after mapping."""
    if not tok or not any(c.isalpha() for c in tok):
        return tok
    cap = tok[0].isupper()
    t = tok.lower()
    if t in LA_RESIDUE:
        return tok
    if t in LA_REPAIRS:
        r = LA_REPAIRS[t]
        if r == "":
            return ""               # listed deletion (a shard)
        return (r[0].upper() + r[1:]) if cap and r[0].islower() else r
    # R0: the OCR's "fb" digraph reads the 1668 ſo (no native Latin fb).
    t2 = t.replace("fb", "so")
    if "f" not in t2:
        return (t2[0].upper() + t2[1:]) if cap and t2 else t2
    # Protection: whole-token and stem classes stand as printed.
    if t2 in LA_PROTECT_TOKENS:
        return tok
    if t2.startswith("falf"):            # falſ- : first f genuine
        r = "fals" + t2[4:].replace("f", "s")
        return (r[0].upper() + r[1:]) if cap else r
    if t2.startswith("fugg"):            # ſugger- (suggero)
        r = "sugg" + t2[4:].replace("f", "s")
        return (r[0].upper() + r[1:]) if cap else r
    if any(m in t2 for m in LA_PROTECT_MEDIAL):
        # keep the stem's f; map f outside the leftmost protected stem
        m = min((t2.find(m), m) for m in LA_PROTECT_MEDIAL if m in t2)
        i, stem = m
        head = t2[:i].replace("f", "s")
        tail = t2[i + len(stem):].replace("f", "s")
        r = head + stem + tail
        return (r[0].upper() + r[1:]) if cap else r
    if t2.startswith(LA_PROTECT_STEMS):
        # initial f genuine; medial f still maps (e.g. a protected
        # stem carrying a later ſ) except where a medial stem rules.
        r = t2[0] + t2[1:].replace("f", "s")
        return (r[0].upper() + r[1:]) if cap else r
    # fer- splits: genuine ferre/ferrum stems stand, else ſer-.
    if t2.startswith(("fert", "ferr", "fertil", "fervor")):
        r = t2[0] + t2[1:].replace("f", "s")
        return (r[0].upper() + r[1:]) if cap else r
    # Medial ff: ſſ -> ss, except protected assimilation stems above
    # and word-initial off- (offendere family keeps its ff).
    if "ff" in t2 and not t2.startswith("off"):
        t2 = t2.replace("ff", "ss")
    r = t2.replace("f", "s")
    return (r[0].upper() + r[1:]) if cap else r


def clean_latin_lines(lines):
    """Apply the declared cleaning classes to a unit's raw OCR lines.
    Returns a list of blocks: {"text": ...} prose, {"note": ...}
    margin notes (mirroring the English parse's furniture)."""
    kept = []
    in_title = False
    last_title_line = ""
    title_lines = 0
    # Brick 8: the class admits the machine's F-for-P reading of
    # the display (Capvt XXV stands as 'C A F V T' in the OCR).
    capvt_re = re.compile(r"^[CG]\s*A\s*[PF]\s*V\s*T\b")
    for ln in lines:
        s = ln.strip()
        if capvt_re.match(s):
            in_title = True           # chapter display: title follows
            last_title_line = ""
            title_lines = 0
            continue
        if in_title:
            if s == "":
                # the title block ends at a blank only once its
                # last line carries terminal punctuation; a blank
                # inside a wrapped title does not end it. Brick 7:
                # a ONE-LINE title trailing the press's comma is
                # the whole title (Capvt XX: 'De Dominio Paterno
                # & Despotico,') — without this, the state ate the
                # chapter's first paragraph. A wrapped title runs
                # to two lines or more before any blank, so the
                # comma rule is confined to the one-line case.
                # Brick 10: the machine's asterisk stands for a
                # title's final stop where the character failed
                # (Capvt XXIX: '…tenduntque ad dissolutionem
                # ejm*') — a blank after it closes the title too;
                # without this the state ate XXIX's first
                # paragraph whole. Eating a paragraph is the
                # worse failure, and the asterisk in this reading
                # is a word-final debris mark.
                if last_title_line.endswith((".", ";", "*")) \
                        or (title_lines == 1
                            and last_title_line.endswith(",")):
                    in_title = False
                continue
            last_title_line = s
            title_lines += 1
            continue                  # the chapter's own title lines
        if re.fullmatch(r"[A-Z];?", s):
            continue                  # a drop-cap shard standing alone
        if any(rx.match(s) for rx in LA_DROP_LINE_RES):
            continue
        kept.append(ln)
    # Join into blocks on blank lines, dehyphenating line ends.
    blocks, cur = [], []
    for ln in kept:
        if ln.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(ln.strip())
    if cur:
        blocks.append(cur)
    out = []
    for blk in blocks:
        # dehyphenate + join
        text = ""
        for i, piece in enumerate(blk):
            piece = " ".join(t for t in piece.split()
                             if t not in LA_DEBRIS_TOKENS)
            if i == 0:
                text = piece
            elif text.endswith("-") and piece[:1].islower():
                text = text[:-1] + piece
            elif text.endswith("-"):
                text = text[:-1] + piece
            else:
                text = text + " " + piece
        # ampersand classes (declared)
        text = re.sub(r"\b[86]c\b", "etc.", text)
        text = re.sub(r"&c\b", "etc.", text)
        text = re.sub(r"(?<=[A-Za-z])&(?=[A-Za-z])", "ct", text)
        text = text.replace(" & ", " et ")
        # token-level long-s restoration + repairs
        text = re.sub(r"[A-Za-zÀ-ÿ£?]+",
                      lambda m: _long_s_token(m.group(0)), text)
        # phrase-level repairs (listed at LA_PHRASE_REPAIRS)
        for old, new in LA_PHRASE_REPAIRS:
            text = text.replace(old, new)
        # punctuation spacing (typographic only)
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if text in LA_FURNITURE_BLOCKS:
            continue
        # margin note: a single short line-block standing alone
        if (len(blk) == 1 and len(text.split()) <= 9 and len(text) <= 78
                and text[0].isupper()):
            out.append({"note": text})
        else:
            out.append({"text": text})
    # Catchwords: a one-word block that repeats the next block's
    # first word is the press's catchword, not text. Declared class.
    dedup = []
    for i, b in enumerate(out):
        words = (b.get("text") or b.get("note") or "").split()
        if len(words) == 1 and i + 1 < len(out):
            nxt = (out[i + 1].get("text")
                   or out[i + 1].get("note") or "").split()
            if nxt and nxt[0].strip(",.;:") == words[0].strip(",.;:"):
                continue
        dedup.append(b)
    out = dedup
    # Leaf-break rejoin: the machine reading breaks the text at
    # every scanned leaf, and dropping the running heads leaves one
    # paragraph standing as two blocks. A prose block that ends
    # without terminal punctuation, followed by a prose block that
    # opens lowercase, is one paragraph across the leaf; rejoin it.
    # Declared class; margin notes break the chain, as they should.
    rejoined = []
    for idx, b in enumerate(out):
        # Brick 6 class (Capvt XVIII's loci): a note-shaped block
        # that ends mid-word — its text closing on a hyphen — or
        # that stands before a lone hyphenated fragment of its own
        # sentence, is no margin note: it is the opening of the
        # paragraph the leaf turn split ('Septimo, … vel' /
        # 'viola-' / 'violationem …'; 'Decimo, … Bel-' / 'lum …').
        # A margin head is complete in the margin and never ends
        # mid-word. Such fragments rejoin as text. Brick 9 adds
        # the third signature of the same split: a longer fragment
        # with no terminal punctuation whose continuation opens
        # lowercase (Capvt XXVIII's 'Nono, … Poena' / 'non est,
        # sed factum hostile') — a paragraph in this book does not
        # open lowercase except across a leaf turn, and a margin
        # head does not trail off unfinished. Brick 10 adds the
        # fourth: a fragment trailing off on a function word, its
        # clause grammatically incomplete, whatever case the
        # continuation opens with (Capvt XXIX's '…qui tres
        # Animas in eodem' / 'Homine esse docuerunt…').
        _frag_enders = {"in", "de", "ad", "cum", "et", "vel",
                        "aut", "ut", "per", "ex", "ab", "pro",
                        "sine", "inter", "contra", "eodem",
                        "eadem", "illo", "illa"}
        _last_word = (b.get("note", "").rstrip(".,;:!? ")
                      .split() or [""])[-1].lower()
        # Brick 12, the fifth signature: the continuation across
        # the leaf opens with the conjunction '&' (Capvt XXXVI's
        # '…Uniuscujusque ergo hominis Christiani,' / '& de
        # salute animae suae solliciti interest…') — no paragraph
        # in this book opens with '&' except across a leaf turn.
        # The sixth signature is the mirror of the first four:
        # the fragment ENDS the sentence the text block before it
        # left unfinished (Capvt XXXV's '…Sanctum enim in Regno'
        # / 'Dei, respondet vocabulo Publicum, in Civitatibus
        # humanis.') — it carries the terminal stop the block
        # before it lacks.
        _prev_unfinished = (
            rejoined and "text" in rejoined[-1]
            and rejoined[-1]["text"].rstrip()[-1:]
            not in (".", "!", "?", "…", "»", ")", '"'))
        if ("note" in b and (b["note"].endswith("-")
                or (b["note"][-1] not in ".!?"
                    and idx + 1 < len(out)
                    and "text" in out[idx + 1]
                    and (len(out[idx + 1]["text"].split()) == 1
                         and out[idx + 1]["text"].endswith("-")
                         or (len(b["note"]) >= 25
                             and out[idx + 1]["text"][:1].islower())
                         or (len(b["note"]) >= 25
                             and _last_word in _frag_enders)
                         or (len(b["note"]) >= 25
                             and out[idx + 1]["text"]
                             .startswith("&"))))
                or (len(b.get("note", "")) >= 25
                    and b.get("note", "").endswith(".")
                    and _prev_unfinished))):
            b = {"text": b["note"]}
        if (rejoined and "text" in b and "text" in rejoined[-1]
                and rejoined[-1]["text"]
                and rejoined[-1]["text"][-1] not in ".?!"
                and b["text"][:1].islower()):
            rejoined[-1] = {"text": rejoined[-1]["text"] + " "
                            + b["text"]}
        else:
            rejoined.append(b)
    out = rejoined
    # The Conjectura margin note, restored at its debris locus (the
    # shards stood inside Capvt III's prudence passage; the note is
    # set as Hobbes set it, in the margin — here, as a subhead).
    for i, b in enumerate(out):
        if "text" in b and "Prudentia est praesumptio Futuri" \
                in b["text"]:
            out.insert(i, {"note": "Conjectura eventi."})
            break
    return out


# ----------------------------------------------------------------------
# English source preparation (the parent edition's census logic)
# ----------------------------------------------------------------------
CHAP_RE = re.compile(r"^CHAPTER ([IVXL]+)\.?\s*(.*)$")


def _en_blocks(lines, notes=True):
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
                and text[-1] not in ".;:!?,"
                and text[0].isupper()):
            out.append({"note": text})
        else:
            out.append({"text": text})
    return out


def load_english_units():
    raw = EN_SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert hashlib.sha256(EN_SOURCE.read_bytes()).hexdigest() == EN_SHA256
    lines = raw.split("\n")
    intro_at = next(i for i, ln in enumerate(lines)
                    if ln.strip() == "THE INTRODUCTION")
    finis_at = next(i for i, ln in enumerate(lines)
                    if ln.strip() == "FINIS")
    body = lines[intro_at:finis_at]
    units, cur, i = [], None, 0

    def flush():
        nonlocal cur
        if cur is not None:
            units.append(cur)
        cur = None

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
    nums = [u["num"] for u in units if u["kind"] == "chapter"]
    assert nums == ROMANS, f"English census failed: {nums[:6]}"
    out = {}
    for u in units:
        u["blocks"] = _en_blocks(u.pop("lines"))
        out[u["key"]] = u
    return out


def load_latin_units():
    raw = LA_SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == LA_SHA256
    lines = raw.decode("utf-8", errors="replace").split("\n")
    out = {}
    for key, (a, b) in LA_SEAMS.items():
        seam = lines[a - 1:b]
        assert seam, f"empty Latin seam for {key}"
        out[key] = clean_latin_lines(seam)
    # The Introduction's first page is set from the facsimile
    # reading (LA_FACSIMILE_INTRO): the machine reading's first five
    # blocks (the great paragraph and the considerabo list) are
    # replaced, after asserting they are the blocks expected.
    intro = out["intro"]
    assert intro[0].get("text", "").startswith("[N]aturam"), \
        "Introduction incipit seam failed"
    assert any("Regnum" in (blk.get("text") or "")
               for blk in intro[:6]), "considerabo list seam failed"
    del intro[:5]
    out["intro"] = LA_FACSIMILE_INTRO + intro
    # Chapter openings on decorated-initial leaves (Brick 2):
    # first block set from the facsimile reading, as the Intro's.
    for key, (probe, blocks) in LA_FACSIMILE_FIRST.items():
        first = out[key][0].get("text", "")
        assert probe in first, f"facsimile seam failed for {key}"
        out[key] = blocks + out[key][1:]
    assert not any("Typographicae" in (blk.get("text") or "")
                   for blk in out["chIII"]), "Ch. IV seam overrun"
    return out


# ----------------------------------------------------------------------
# Pairing + pagination planning
# ----------------------------------------------------------------------
def pair_blocks(en_blocks, la_blocks):
    """Pair by index; a note block travels attached to the prose
    block that follows it (it is that paragraph's margin head)."""
    def attach(blocks):
        out, pending = [], []
        for b in blocks:
            if "note" in b:
                pending.append(b)
            else:
                out.append(pending + [b])
                pending = []
        if pending:
            out.append(pending)
        return out
    en_g, la_g = attach(en_blocks), attach(la_blocks)
    pairs = []
    for i in range(max(len(en_g), len(la_g))):
        pairs.append({
            "en": en_g[i] if i < len(en_g) else None,
            "la": la_g[i] if i < len(la_g) else None,
        })
    return pairs, len(en_g), len(la_g)


PAGE_W, PAGE_H = 215.9, 279.4          # Letter
MARG_L, MARG_R, MARG_T = 22.0, 22.0, 20.0
TEXT_W = PAGE_W - MARG_L - MARG_R
BODY_BOTTOM = PAGE_H - 18.0            # footer reserve
USABLE_H = BODY_BOTTOM - MARG_T

BODY_SIZE, BODY_H = 10.5, 5.6
NOTE_SIZE, NOTE_H = 9.0, 4.6


def measure(pdf, blocks, lang):
    """Height in mm of a block list on a scratch document."""
    if not blocks:
        return 0.0
    h = 0.0
    for b in blocks:
        if "note" in b:
            pdf.set_font("dejavu", "B", NOTE_SIZE)
            n = len(pdf.multi_cell(TEXT_W, NOTE_H, b["note"],
                                   dry_run=True, output="LINES"))
            h += n * NOTE_H + 2.2
        else:
            pdf.set_font("dejavu", "", BODY_SIZE)
            n = len(pdf.multi_cell(TEXT_W, BODY_H, b["text"],
                                   dry_run=True, output="LINES"))
            h += n * BODY_H + 2.4
    return h


def plan_spreads(pdf, units):
    """units: list of dicts with pairs + titles. Returns a plan:
    list of unit-plans, each a list of spreads; a spread is
    {"la": [pair-indices], "en": [pair-indices]} — indices into the
    unit's pair list, each side carrying its own face's blocks."""
    plan = []
    for u in units:
        spreads, cur, la_h, en_h = [], None, 0.0, 0.0

        def new_spread():
            return {"la": [], "en": []}
        cur = new_spread()
        HEAD_H = 26.0
        la_h = en_h = HEAD_H
        for idx, pair in enumerate(u["pairs"]):
            hl = measure(pdf, pair["la"], "la") if pair["la"] else 0.0
            he = measure(pdf, pair["en"], "en") if pair["en"] else 0.0
            if (la_h + hl > USABLE_H - 6.0
                    or en_h + he > USABLE_H - 6.0) \
                    and (cur["la"] or cur["en"]):
                spreads.append(cur)
                cur = new_spread()
                la_h = en_h = 0.0
            cur["la"].append((idx, pair["la"]))
            cur["en"].append((idx, pair["en"]))
            la_h += hl
            en_h += he
        if cur["la"] or cur["en"]:
            spreads.append(cur)
        plan.append({"unit": u, "spreads": spreads})
    return plan


# ----------------------------------------------------------------------
# The book
# ----------------------------------------------------------------------
class Book(FPDF):
    folio_total = None

    def footer(self):
        self.set_y(-14)
        self.set_font("dejavu", "", 7.5)
        self.set_text_color(90, 90, 90)
        total = self.folio_total if self.folio_total else "{nb}"
        self.cell(0, 8, FOOTER.format(n=self.page_no(), m=total),
                  align="C")
        self.set_text_color(0, 0, 0)


def para(pdf, text, size=BODY_SIZE, height=BODY_H, align="J",
         space_after=2.4, style="", font="dejavu"):
    pdf.set_font(font, style, size)
    pdf.multi_cell(0, height, text, align=align,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(space_after)


def centered(pdf, text, size, height=6.0, style="B", space_after=0.0,
             color=None, font="dejavu"):
    if color:
        pdf.set_text_color(*color)
    pdf.set_font(font, style, size)
    pdf.multi_cell(0, height, text, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if color:
        pdf.set_text_color(0, 0, 0)
    pdf.ln(space_after)


GOLD = (146, 110, 20)
GREEN = (20, 110, 60)
GREY = (90, 90, 90)


def head_rule(pdf, space_before=2.0, space_after=4.0):
    pdf.ln(space_before)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.4)
    pdf.line(MARG_L, pdf.get_y(), PAGE_W - MARG_R, pdf.get_y())
    pdf.ln(space_after)


def roman_head(pdf, numeral, title):
    centered(pdf, f"§{numeral}", 11, color=GOLD, space_after=1.0)
    centered(pdf, title, 13.5, space_after=2.0)
    head_rule(pdf)


# ----------------------------------------------------------------------
# Front matter (Brick 1 form; grows by amendment, never silently)
# ----------------------------------------------------------------------
PREFACE = [
    ("I", "WHY TWO FACES",
     ["This edition sets Thomas Hobbes's Leviathan twice on the "
      "same opening: the English of 1651 on the right-hand page, the "
      "Latin of 1668 on the left. Hobbes made both books. The Latin "
      "is no translation hung upon the English for ornament; it is "
      "the author at work again, seventeen years on, in another "
      "tongue, for another republic of readers — compressing here, "
      "expanding there, and in one great structural stroke setting "
      "an Appendix of three chapters where the English had closed "
      "with A Review, and Conclusion.",
      "A reader with both faces open can watch the same mind argue "
      "in two registers. That is the whole case for a parallel "
      "edition, and it needs no embellishment. Where the two texts "
      "diverge, this edition prints the divergence in its collation "
      "notes as evidence. It does not harmonize, and it does not "
      "look away."]),
    ("II", "THE SOURCES, IN BRIEF",
     ["The English face is Project Gutenberg eBook #3207 — the text "
      "of record of this program, secured at its founding on "
      "2026-11-02 and re-verified by hash at every build; it descends "
      "from the Pelican Classics edition, prepared from the first "
      "edition of 1651. The Latin face is the Leviathan of the Opera "
      "philosophica quae Latine scripsit omnia (Amsterdam: Joan "
      "Blaeu, 1668), secured on 2026-11-10 from the Internet Archive "
      "(item leviathansivedem00hobb) as that scan's machine-read "
      "text, and verified by imprint, dedicatee, and its own printed "
      "census before a page was built.",
      "The Latin is therefore, and is labelled throughout, a "
      "SINGLE-WITNESS OCR TEXT: machine reading of one scanned copy, "
      "not a collated critical text. The full provenance, the "
      "hashes of every secured file, the defect register, and the "
      "honest list of what was not done stand in the edition's "
      "SOURCE LEDGER, kept with the edition's working papers and "
      "summarized in the apparatus of this volume."]),
    ("III", "THE COLLATION METHOD",
     ["The unit of alignment is the chapter; within the chapter, "
      "paragraphs pair by order, Hobbes's marginal summaries riding "
      "with the paragraphs they head. The planner measures both "
      "faces and packs each opening so that paired paragraphs face "
      "each other; when one face runs longer, the opening turns and "
      "the drift is measured, not masked — each brick's collation "
      "notes print the drift table for its chapters.",
      "The Latin of 1668 is treated in this edition as a collation "
      "witness with its own authority — the standing question of "
      "this program's founding charter, whether the Latin should be "
      "taken as a witness at all, is answered here in the practice: "
      "yes, and its differences are the most instructive pages in "
      "the book."]),
    ("IV", "NORMALIZATIONS AND TOLERANCES, DECLARED",
     ["The English face changes nothing: reflow and the parent "
      "edition's furniture, as there declared. The Latin face "
      "reproduces the 1668 text in its own orthography — u and v, "
      "i and j stand as the press set them — normalized only by "
      "declared classes: the press's long s, which machine reading "
      "renders as f, is restored to s under a printed rule table "
      "(genuine f, as in forma and finis, is protected; what the "
      "rules cannot resolve stands as it was read, and is counted "
      "in the apparatus as residue); line-end hyphens are joined; "
      "the ampersand classes are resolved (the & of the press is "
      "its et; within a word it is the ct ligature; &c is etc.); "
      "running heads and the furniture of the folio page are not "
      "set as text; decorative initials the machine reading split "
      "or lost are restored in brackets and listed. Every one of "
      "these is a typographic class, stated once here and binding "
      "on every brick.",
      "What the classes cannot honestly carry, the edition prints "
      "as apparatus, not as Hobbes. First-edition facsimile "
      "collation is UNCHARTED in this edition: loci that need it "
      "are flagged, never resolved by preference. No Latin has "
      "been fabricated, completed, or retranslated at any locus."]),
]

CONTENT_TEST = (
    "THE FOUR-ELEMENT TEST OF THIS EDITION — Inputs: Gutenberg "
    "#3207 (hash of record) and the 1668 Blaeu Latin via Internet "
    "Archive leviathansivedem00hobb (hashes in the Source Ledger). "
    "Processes: hash assertion, census assertion, seam extraction, "
    "declared-class normalization, paragraph pairing, measured "
    "spread planning, multi-pass contents stabilization. Outputs: "
    "this volume, cumulative by brick, with its build report. "
    "Tolerances: no word of Hobbes changed beyond the declared "
    "classes; no Latin reading untraceable to the secured text; "
    "divergence printed, never harmonized.")

AUTHORITIES = [
    "Hobbes, Thomas. Leviathan, or The Matter, Forme, & Power of a "
    "Common-wealth Ecclesiasticall and Civill. London: Andrew "
    "Crooke, 1651.",
    "Hobbes, Thomas. Leviathan, sive De materia, forma, & potestate "
    "civitatis ecclesiasticae et civilis. In: Opera philosophica "
    "quae Latine scripsit omnia. Amsterdam: Joan Blaeu, 1668.",
    "Project Gutenberg eBook #3207 (Leviathan), with its "
    "Transcriber's Notes — the English text of record.",
    "Internet Archive item leviathansivedem00hobb — catalogue record, "
    "page-number index, and the secured files of the Source Ledger.",
    "The Bible (Job 41) — the edition's motto, Hobbes's own citation.",
    "Black's Law Dictionary, 2nd Edition (1910) — the parent "
    "program's standing authority for terms of art in the apparatus.",
]


def front_matter(pdf, toc_entries):
    """Returns nothing; composes the front matter. toc_entries is a
    list of (label, folio-or-None) printed on the contents leaf; on
    pass 1 folios may be None (printed as a fixed-width token)."""
    # --- Title leaf ---
    pdf.add_page()
    if LOGO.exists():
        pdf.image(str(LOGO), x=(PAGE_W - 34) / 2, y=18, w=34)
    pdf.set_y(58)
    centered(pdf, "LEVIATHAN", 30, height=11)
    centered(pdf, "A PARALLEL EDITION  ·  (MAGVS)", 13, color=GOLD,
             space_after=3)
    centered(pdf, "THE ENGLISH OF 1651  FACING  THE LATIN OF 1668",
             11.5, space_after=10)
    centered(pdf, "Thomas Hobbes", 12.5, style="", space_after=14)
    para(pdf, "The Flagpole on this volume claims the edition and "
              "the apparatus only. Thomas Hobbes's texts, English "
              "and Latin, are public domain; no claim reaches for "
              "them.", size=9.5, height=5.2, align="C")
    pdf.ln(6)
    centered(pdf, "Authorship attributed exclusively to", 10,
             style="", space_after=0)
    centered(pdf, "Johnathan 'Qasparr' Monroe", 13, space_after=1)
    centered(pdf, "(Greek, -ARR, All Rights Reserved, Without "
                  "Prejudice)", 9.5, style="", space_after=6)
    centered(pdf, THELEMIC_DATE, 10, style="", space_after=8)
    centered(pdf, "Enterprise • Educational • Research & Development",
             9.5, style="", space_after=1)
    centered(pdf, "Method of Science, Aim of Religion", 9.5,
             style="", space_after=10)
    para(pdf, FLAGPOLE, size=9.5, height=5.2, align="C")
    pdf.ln(8)
    centered(pdf, PUBLISHER, 10.5, space_after=0)
    centered(pdf, PROPRIETOR, 9, style="")
    # --- Reviser's Preface ---
    pdf.add_page()
    centered(pdf, "REVISER'S PREFACE", 16, space_after=2)
    centered(pdf, "TO THE PARALLEL EDITION", 11, color=GOLD,
             space_after=4)
    head_rule(pdf)
    for num, title, paras in PREFACE:
        roman_head(pdf, num, title)
        for p in paras:
            para(pdf, p)
    para(pdf, CONTENT_TEST, size=9.5, height=5.2)
    # --- Contents ---
    pdf.add_page()
    centered(pdf, "CONTENTS", 16, space_after=2)
    head_rule(pdf)
    for label, folio in toc_entries:
        pdf.set_font("dejavu", "", 10.5)
        tok = f"{folio:>4}" if folio is not None else "   —"
        pdf.multi_cell(0, 6.0, f"{label}    {tok}", align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)
    para(pdf, "The edition is cumulative by brick: the contents "
              "grow as the bricks land, and every brick is recorded "
              "in the colophon.", size=9.5, height=5.2)


def emit_blocks(pdf, blocks, side_label=None):
    """Set a list of blocks (notes as centered subheads, prose as
    justified paragraphs) at the current position."""
    for b in blocks or []:
        if "note" in b:
            pdf.ln(1.0)
            centered(pdf, b["note"], NOTE_SIZE, height=NOTE_H,
                     style="B", space_after=1.2, color=GOLD)
        else:
            para(pdf, b["text"])


def emit_parallel(pdf, plan, toc):
    """Emit the planned spreads; record each unit's opening folio."""
    for up in plan:
        u = up["unit"]
        first = True
        for spread in up["spreads"]:
            pdf.add_page()   # verso — Latin
            if pdf.page_no() % 2 != 0:
                raise AssertionError("verso parity failed")
            if first:
                toc[u["key"]] = pdf.page_no()
                centered(pdf, "LATINE · 1668", 9, color=GREY,
                         space_after=1)
                centered(pdf, u["la_title"], 14, space_after=1)
                centered(pdf, u["en_title"], 9.5, style="",
                         color=GREY, space_after=2)
                head_rule(pdf)
            else:
                centered(pdf, "LATINE · 1668", 8.5, style="",
                         color=GREY, space_after=2)
            for _idx, blocks in spread["la"]:
                emit_blocks(pdf, blocks)
            pdf.add_page()   # recto — English
            if first:
                centered(pdf, "ENGLISH · 1651", 9, color=GREY,
                         space_after=1)
                centered(pdf, u["en_title"], 14, space_after=1)
                centered(pdf, u["la_title"], 9.5, style="",
                         color=GREY, space_after=2)
                head_rule(pdf)
            else:
                centered(pdf, "ENGLISH · 1651", 8.5, style="",
                         color=GREY, space_after=2)
            for _idx, blocks in spread["en"]:
                emit_blocks(pdf, blocks)
            first = False


def collation_notes(pdf, report):
    pdf.add_page()
    centered(pdf, "COLLATION NOTES", 16, space_after=2)
    centered(pdf, f"BRICKS 1–{BRICK} — CUMULATIVE", 10.5,
             color=GOLD, space_after=4)
    head_rule(pdf)
    notes = [
        ("N1 — The Introduction's seat. In the 1668 volume the "
         "Introductio stands under the display of PARS PRIMA · DE "
         "HOMINE, inside Part I's heading; the English sets THE "
         "INTRODUCTION before Part I. The edition follows each "
         "text's own seating and notes the difference here, once."),
        ("N2 — The ending the Latin does not have. The English "
         "closes with A REVIEW, AND CONCLUSION; the Latin volume "
         "instead appends an APPENDIX of three chapters (De Symbolo "
         "Niceno; De Haeresi; De quibusdam Objectionibus contra "
         "Leviathan), printed pp. 325–365 of the 1668 book. When "
         "this edition reaches the end, the Appendix will face the "
         "Review as a structural divergence, not as a translation."),
        ("N3 — The Introduction's first page, adjudicated. The "
         "folio's opening page (1668 p. 1) carries the decorated "
         "initial, and the machine reading of that page interleaves "
         "the initial's column with the text until the token "
         "classes cannot honestly carry it. This page — and no "
         "other in Brick 1 — is set from a reading of the leaf "
         "itself, rendered from the secured facsimile PDF (leaf 9): "
         "the edition's first exercise of the Source Ledger's "
         "spot-adjudication provision, recorded in the Ledger's "
         "amendment. The initial itself is restored as [N]aturam. "
         "One typographic distinction is levelled by the declared "
         "font tolerance and recorded here so it is not lost "
         "silently: the 1668 page sets its equation-terms (Anima, "
         "Artus, Praemia et Poenae, Nervi, and their fellows) in "
         "italic; this edition's DejaVu Serif carries no italic "
         "face, and the equations stand in the body face."),
        ("N4 — A running head against its chapter. At printed "
         "p. 13, inside Capvt III's closing passage (the finite / "
         "infinite locus), the folio's running head reads 'Cap. 4' "
         "in the machine reading, ahead of Capvt IV's display at "
         "the passage's end. Whether the fault is the press's, the "
         "scan's, or the reading machine's is UNCHARTED — "
         "adjudication against the facsimile leaf has not been "
         "performed. The text is set by the display headings, and "
         "the anomaly stands here on the record."),
        ("N5 — 'fine', thirteen times. The machine reading's 'fine' "
         "in these chapters is the press's ſine (without), restored "
         "to sine under the rule table; finis and its true forms "
         "(finem, finis, finita) are protected and stand. The class "
         "is recorded because the two words share a shape in the "
         "OCR: the readings were adjudicated by context at every "
         "locus, and the count is printed so the adjudication can "
         "be audited."),
        ("N6 — The Conjectura margin note. Capvt III's margin "
         "carries 'Conjectura eventi' where the English margin "
         "treats of prudence and conjecture; the machine reading "
         "split the note and fused its shards into the body lines. "
         "The shards were removed under the declared debris class "
         "and the note set as a subhead at its locus, as Hobbes's "
         "own furniture sets it."),
        ("N7 — Paragraph drift, measured. "
         + report["drift_text"]),
        ("N8 — Residue, counted. After every declared class, "
         + report["residue_text"]
         + " These stand in the text exactly as the machine read "
         "them; each is a named locus for the facsimile collation "
         "that remains UNCHARTED."),
        ("N9 — One garbled sentence, flagged whole. Capvt III's "
         "sentence on place ('neque aliquid esse totum in uno "
         "loco, et totum in altero, tempore eodem…') is garbled in "
         "the machine reading beyond the declared classes (its "
         "reading carries 'eflk' and 'io altcro' among its ruins). "
         "The words are set as read, under the declared classes "
         "only; the English face carries the sense; the Latin "
         "locus is flagged for facsimile adjudication, UNCHARTED."),
        ("N10 — The repairs, counted. The listed token repairs "
         "(fused-word splits, drop-cap and ligature restorations, "
         "one-letter substitutions in certain words) applied in "
         "this brick number "
         + str(report["repairs_applied"])
         + " occurrences. The table itself stands printed in the "
         "builder, build_leviathan_parallel.py, which is part of "
         "this edition's record; the classes are declared in §IV "
         "of the Preface. No repair is applied that is not in the "
         "table."),
    ]
    if BRICK >= 2:
        notes += [
            ("N11 — Brick 2 scope. Capvt IV (De Sermone), Capvt V "
             "(De Ratione et Scientia), and Capvt VI (De Principiis "
             "internis Motus Voluntarii) join the parallel text. "
             "Capvt VI's title in the folio display runs to three "
             "lines and a second sentence (et de Orationibus quibus "
             "eae declarantur); the edition's heading carries the "
             "title's first sentence, and the whole stands here."),
            ("N12 — Capvt IV's opening display. The chapter's "
             "display heading stands in the machine reading with "
             "its initial misread ('G A P V T IV', 'Do Strmone'); "
             "the seam was fixed by content — the Typographicae "
             "passage that opens the English Chapter IV — and the "
             "heading is set from the census. The reading machine's "
             "forms stand in this note, not in the text."),
            ("N14 — Two more leaves adjudicated (Brick 2). The "
             "opening leaves of Capvt V (1668 p. 20) and Capvt VI "
             "(p. 25) carry decorated initials and garble in the "
             "same way as the Introduction's page; their first "
             "paragraphs, with the margin notes the leaves carry "
             "(Ratio.; Motus Vitalis et Animalis.), are set from "
             "readings of the leaves rendered from the secured "
             "facsimile PDF (leaves 28 and 33), under the same "
             "spot-adjudication provision, and the Ledger's "
             "amendment is extended to name them. One lesser shard "
             "of the same family in Capvt IV ('Semwh', an initial-"
             "column fragment fused into the chapter's first "
             "sentence) is deleted as a listed repair, the "
             "sentence's own words being whole on both sides of it."),
            ("N15 — Titles that differ within the volume (Brick "
             "3). Capvt VIII carries two title forms in the 1668 "
             "book itself: the contents leaf reads 'De Virtutibus "
             "et Defectibus Intellectualibus', the chapter's own "
             "display 'De Virtutibus Intellectualibus et "
             "Defectibusque Oppositis'; the edition's heading "
             "follows the chapter display. Capvt IX's Latin title, "
             "'De Scientiarum Distributione' — of the distribution "
             "of the sciences — answers an English title of another "
             "sense, 'Of the severall Subjects of Knowledge'; both "
             "stand as printed, the divergence recorded, not "
             "harmonized."),
            ("N16 — Capvt IX's tables (Brick 3). The English "
             "chapter prints its division of the sciences as two "
             "formal tables, which the machine reading carries as "
             "fifty-five small paragraph groups; the Latin casts "
             "the same division as continuous prose in twelve "
             "groups. Pairing follows group order; in this chapter "
             "the faces correspond by matter rather than by block, "
             "and the drift figure (N7) records the fact without "
             "forcing the tables into paragraphs."),
            ("N17 — Capvt XI's three titles (Brick 4). The "
             "contents leaf reads 'De Differentia Morum'; the "
             "chapter's own display reads 'De Varietate Morum'; "
             "the English chapter is 'Of the Difference of "
             "Manners'. The edition's heading follows the chapter "
             "display; all three forms stand recorded here, none "
             "harmonized."),
            ("N18 — Part I closes (Brick 5). With Capvt XVI the "
             "parallel text carries the whole of Pars Prima, De "
             "Homine — the Introduction and sixteen chapters — in "
             "both tongues. One correction of the desk's own "
             "record: Capvt XII's 'fructus' was announced at Brick "
             "4 as a listed repair; it is in fact carried by the "
             "genuine-f protection table (the fru- stem), extended "
             "at this brick together with frat-, frau-, frag-, "
             "frang-, fren-, and front-. "
             "The opening leaves of Capvt XV and Capvt XVI carry "
             "the decorated-initial garble more heavily than most; "
             "their first paragraphs stand as read, garble and "
             "all, under the residue rule — the English faces carry "
             "the sense, and the loci are flagged here rather than "
             "adjudicated. Capvt XIV's first word ('Ius') is "
             "restored as a listed repair, its drop-cap initial "
             "having fused. Part II, De Civitate, "
             "opens at Capvt XVII in the next brick; the Latin "
             "volume seats a part title there ('PARS SECUNDA / DE "
             "CIVITATE') as it did at the first, recorded at N1."),
            ("N13 — Drift and residue are cumulative. N7's drift "
             "table and N8's residue count are regenerated at every "
             "brick over the whole text built so far; their figures "
             "in this volume supersede the same notes in earlier "
             "bricks, which stand in the edition's git history."),
        ]
    if BRICK >= 6:
        notes += [
            ("N19 — Part II opens (Brick 6). Capvt XVII (De Causa, "
             "Generatione, et Definitione Civitatis), Capvt XVIII "
             "(De Iure habentium Summam Potestatem in Civitate per "
             "Institutionem), and Capvt XIX (De Generibus Civitatum "
             "per Institutionem, et de Successione ad Summam "
             "Potestatem) join the parallel text. The PARS SECUNDA "
             "display (DE CIVITATE SIVE REPVBLICA) stands in the "
             "machine reading at the close of Capvt XVI's seam and "
             "drops there under the display classes, as Part I's "
             "display did (N1). Capvt XVII's first word is restored "
             "as a listed repair — the decorated initial consumed "
             "its Q: '[Q]uod homines…'. Capvt XIX's first word is "
             "restored likewise ('Distinctio', the machine's D-l "
             "for D-i), its sense fixed by the English face."),
            ("N20 — A furniture correction, recorded whole (Brick "
             "6). Part II's running heads defeated the drop classes "
             "of Bricks 1–5 twice over: the machine sets them in "
             "wide spacing the patterns did not allow, and their "
             "tails garble past the anchors ('86 De Civitate. Cap. "
             "i8„'; '8 4 D* Civitate. Cap. 17.'; 'S8 De Civitate. "
             "Cap. i£.'; the signature line carrying its catchword, "
             "'Leviat. n n n exerci-'). The classes are widened to "
             "the spacing and the tails, and two consequences reach "
             "back into Part I, printed here rather than worked "
             "silently: running heads that stood in the earlier "
             "printings as note-shaped blocks (and two as text) now "
             "drop throughout the volume, as the furniture they "
             "are; and paragraph fragments a leaf turn split "
             "mid-word — known by their closing hyphen — now "
             "rejoin as the text they are, in Part II (Capvt "
             "XVIII's Septimo and Decimo paragraphs) and at one "
             "Part I locus (Capvt IV). The desk audited the "
             "correction word by word against Brick 5's text: no "
             "word of Hobbes is lost; what falls is heads, "
             "catchwords, and split fragments whose words stand "
             "whole at their paragraphs' heads. The earlier "
             "printings stand unaltered in the edition's git "
             "history; this volume supersedes them, as N13 "
             "declares. One debris token is added to the residue "
             "register: 'mmm', signature waste standing inside "
             "Capvt XVII's definition paragraph, counted at N8."),
            ("N21 — Brick 7 scope. Capvt XX (De Dominio Paterno "
             "et Despotico), Capvt XXI (De Libertate Civium), and "
             "Capvt XXII (De Systematibus Civium) join the "
             "parallel text. One title-form divergence stands on "
             "the record: Capvt XXX's heading, when its brick "
             "comes, will follow its chapter display ('De Officio "
             "Summi Imperantis'); the volume's contents leaf reads "
             "'De Officio Summi Imperii'. Both forms are the "
             "book's own; the display governs, as at N15 and N17."),
            ("N22 — A title-state repair, and the furniture "
             "widening continued (Brick 7). Capvt XX's display "
             "title ends with the press's comma ('De Dominio "
             "Paterno & Despotico,'), and the title state — which "
             "ends a chapter's title at a blank only after "
             "terminal punctuation, lest a wrapped title be cut — "
             "thereby ate the chapter's whole first paragraph "
             "('Civitatem per Acquisitionem voco…'). The state now "
             "also closes on a blank after a ONE-LINE title "
             "trailing a comma; a wrapped title runs to two lines "
             "or more before any blank, so no true title can be "
             "cut by the rule, and the paragraph stands restored. "
             "The running-head classes were widened once more for "
             "this brick's garbles (the chapter number itself "
             "misread: 'Cap. zo. T>e Civitate. i o i'; 'H4 D* "
             "Civitate. Cap. 22.'); three heads the Brick 6 "
             "printing still carried in Part I and Capvt XVIII "
             "fall with them, recorded here under N20's doctrine. "
             "One shard is listed as furniture: Capvt XX's 'Sc', "
             "the ampersand's debris at a leaf turn, its "
             "conjunction standing at the next block's head."),
            ("N23 — Brick 8 scope. Capvt XXIII (De Potestatis "
             "Summae Ministris Publicis), Capvt XXIV (De "
             "Civitatis Facultate Nutritiva et Generativa), and "
             "Capvt XXV (De Consilio) join the parallel text. "
             "Capvt XXV's display stands in the machine reading "
             "with its P read as F ('C A F V T XXV.'); the display "
             "class is widened to admit the variant, and the "
             "chapter's heading is set from the census, as at N12. "
             "One of the chapter's own running heads stands fused "
             "inside its first paragraph in the machine reading "
             "('Cap. if. JDe Cwitate. yzj-'), dropped under the "
             "widened head class of N22."),
            ("N24 — Capvt XXIII's first words, flagged whole "
             "(Brick 8). The chapter opens in the machine reading "
             "as 'Mlntsler?#£//«« is est qui in rebus…' — the words "
             "the English face gives as 'A Publique Minister is "
             "he, that…' (Minister Publicus is est, qui…) garbled "
             "past every declared class. They are set as read, "
             "under the residue rule; the English face carries "
             "the sense; the locus is flagged for the facsimile "
             "collation that remains UNCHARTED. Capvt XXIV's "
             "signature line, its catchword with it, is listed as "
             "furniture (the signature itself misread, 'Ltviat.'); "
             "the word it promised, 'omnium', stands at its "
             "paragraph's place: 'Vbi enim Civitas non est, ibi "
             "omnia omnium sunt'."),
            ("N25 — Brick 9 scope. Capvt XXVI (De Legibus "
             "Civilibus), Capvt XXVII (De Criminibus, "
             "Excusationibus, et Extenuationibus), and Capvt "
             "XXVIII (De Poenis et Praemiis) join the parallel "
             "text. Capvt XXVIII's display stands spaced in the "
             "machine reading with its numeral garbled ('X X V I "
             "I L'); the seam was fixed by content — the Poena "
             "definition that opens the English chapter — and "
             "the heading is set from the census, as at N12."),
            ("N26 — The leaf-split signatures, completed (Brick "
             "9). The rejoin class of N20 gains its third "
             "signature: a longer note-shaped fragment with no "
             "terminal punctuation whose continuation opens "
             "lowercase (Capvt XXVIII's 'Nono, … Poena' before "
             "'non est, sed factum hostile'). Five fragments in "
             "the earlier text convert with it — Capvt III's "
             "sign sentence, Capvt VI's two appetite fragments, "
             "Capvt XIV's pact-with-God fragment, Capvt XV's "
             "foro-interno fragment — each a paragraph's opening "
             "the leaf turn severed, each now standing as the "
             "text it is; the word-audit against the Brick 8 "
             "printing shows no word lost and no margin head "
             "demoted that reads as a complete summary. Capvt "
             "XXVIII's decorated-initial shard ('Ade*') is "
             "listed as furniture; its word stands whole at its "
             "paragraph's head ('A Definitione Poenae deduco…'). "
             "Capvt XXVII's one margin note stands as printed: "
             "'Et Mutilatio majus Crimen quam bonorum ereptio' — "
             "Hobbes's own summary, complete in the margin."),
            ("N27 — Part II closes (Brick 10). With Capvt XXIX "
             "(De iis rebus quae Civitatem labefactant, "
             "tenduntque ad dissolutionem eius), Capvt XXX, and "
             "Capvt XXXI (De Regno Dei Naturali) the parallel "
             "text carries the whole of Pars Secunda, De "
             "Civitate — fifteen chapters facing the English of "
             "Chapters 17–31. Capvt XXX's heading follows its "
             "chapter display, 'De Officio Summi Imperantis', "
             "against the contents leaf's 'De Officio Summi "
             "Imperii', as recorded forward at N21. Capvt XXIX's "
             "first paragraph stands restored: its title's final "
             "stop failed in the machine reading to an asterisk "
             "('…dissolutionem ejm*'), and the title state, "
             "waiting on terminal punctuation, had eaten the "
             "paragraph ('Quanquam immortale nihil sit, quod "
             "mortales faciunt…'); the state now closes on the "
             "asterisk as on a stop. The rejoin class gains its "
             "fourth signature — a fragment trailing off on a "
             "function word, its clause incomplete (Capvt XXIX's "
             "'…qui tres Animas in eodem' before 'Homine esse "
             "docuerunt…')."),
            ("N28 — The part displays, corrected whole (Brick "
             "10). N19 recorded that the PARS SECUNDA display "
             "drops inside Capvt XVI's seam under the display "
             "classes; in fact only its first line fell — three "
             "lines stood through Brick 9 as note-shaped blocks "
             "at the chapter's tail ('De Civitate', 'S I V E', "
             "'Repvblica.'). The record is corrected here, not "
             "smoothed: the display now drops whole, and PARS "
             "TERTIA's display, standing line by line inside "
             "Capvt XXXI's seam with its leaf-number debris "
             "('*75'), drops with it. Part displays are the "
             "press's furniture; the edition sets its own part "
             "seating in the contents and the colophon, and the "
             "Latin volume's seating of each part title before "
             "its first chapter stands recorded at N1 and here."),
            ("N29 — Part III opens (Brick 11). Capvt XXXII–"
             "XXXIV face the English of Chapters 32–34 under the "
             "PARS TERTIA display seated at N28. Four leaf-turn "
             "catchwords stand listed as furniture ('In', "
             "'Octo,', 'Capitis', 'Spiritu' — each the first "
             "word of the paragraph following it); Capvt "
             "XXXIII's Esther line stands as a margin note, "
             "complete in the margin as printed: 'Liber Esther "
             "in ipsa Captivitate, vel postea scriptus est.' A "
             "running head of the Part III form ('Cap. 33. De "
             "Civitate Christiana') stands fused at a paragraph "
             "head in Capvt XXXIII, as read — the line classes "
             "do not reach inside a paragraph. One recorded "
             "repair reaches back into Part I: a running head of "
             "Capvt XIII ('64 De Homine. Cap. 13.'), garbled past "
             "the head classes, had stood as a text block since "
             "Brick 5, beside its own leaf's catchword; both are "
             "furniture and are now listed as such. No word of "
             "the chapter is touched."),
            ("N30 — Capvt XXXV–XXXVII (Brick 12), and the measure "
             "of Part III. Two further leaf-split signatures join "
             "the rejoin class: the fifth, a fragment whose "
             "continuation opens with '&' (Capvt XXXVI's close: "
             "'…Uniuscujusque ergo hominis Christiani,' / '& de "
             "salute animae suae solliciti interest…', its "
             "catchword shard '&de' listed); the sixth, the "
             "mirror shape — a fragment carrying the terminal "
             "stop of the sentence the block before it left "
             "unfinished (Capvt XXXV: '…Sanctum enim in Regno' / "
             "'Dei, respondet vocabulo Publicum, in Civitatibus "
             "humanis.'). One earlier block converts under the "
             "sixth signature and is judged a severed tail, as "
             "read: Capvt VI's '…cepimus; …religio.' A signature "
             "shard and two standing heads of the Part III form "
             "are listed as furniture. Measured across the part "
             "so far, the Latin runs at 0.51–0.55 of the "
             "English's word count, chapter by chapter without "
             "exception — against 0.61–0.71 in Part I: the 1668 "
             "text is a condensed redaction throughout, and in "
             "this part uniformly so. The fact is printed, not "
             "harmonized; the facing is by paragraph, and the "
             "drift figures at N7 carry it chapter by chapter."),
            ("N31 — Capvt XXXVIII–XL (Brick 13). The part's "
             "condensation deepens in Capvt XXXIX: four Latin "
             "paragraph groups face nine English, the definitions "
             "of Ecclesia carried in long periods where the "
             "English divides them — the extreme of the measure "
             "recorded at N30, printed in the drift at N7. One "
             "catchword is listed ('Iacobi.', Capvt XXXVIII, the "
             "word standing whole at the next leaf's head). "
             "Capvt XL closes the patriarchal sequence at the "
             "seam of XLI's display, fixed by its title ('De "
             "Servatoris nostri Benedicti Officio')."),
            ("N32 — Capvt XLI–XLII (Brick 14). Capvt XLII, De "
             "Potestate Ecclesiastica, is the volume's long "
             "chapter — 48 pages in the 1668 printing (231–279 "
             "by its contents leaf) — and its display numeral is "
             "garbled in the machine reading ('CAPVT XLIL'); the "
             "chapter is fixed by its title and its matter, and "
             "the seam is set by content. Two catchwords are "
             "listed ('Inquo', 'Ccetus'), and one standing head "
             "of the Part III form ('196 De Civitate Christiana. "
             "Cap. 42.') — its listing seats the severed sentence "
             "tail it interrupted under the sixth signature: "
             "'…& jus habent Pastores sub se' / '…constituendi "
             "quos ipsi idoneos ad populum instruendum "
             "judicabunt.' No margin note stands in the chapter "
             "as cleaned: its summaries ride inside its "
             "paragraphs in this part of the book."),
        ]
    for n in notes:
        para(pdf, n, size=10, height=5.4)


def back_matter(pdf):
    pdf.add_page()
    centered(pdf, "TABLE OF AUTHORITIES", 15, space_after=2)
    centered(pdf, "(condensed)", 10, style="", color=GREY,
             space_after=4)
    head_rule(pdf)
    for a in AUTHORITIES:
        para(pdf, a, size=10, height=5.4)
    pdf.ln(4)
    centered(pdf, "COLOPHON", 15, space_after=4)
    para(pdf, "This volume was built at the desk of the parallel "
              "edition by the builder build_leviathan_parallel.py, "
              f"cumulative through Brick {BRICK}: {BRICK_SCOPE}, "
              "with collation notes. Sources asserted by hash at "
              "build time: "
              "Gutenberg #3207 (English) and Internet Archive "
              "leviathansivedem00hobb (Latin, 1668). Generation "
              "note: set in DejaVu Serif; no synthetic italics are "
              "used anywhere in the volume.", size=10, height=5.4)
    para(pdf, "Authorship attributed exclusively to Johnathan "
              "'Qasparr' Monroe (Greek, -ARR, All Rights Reserved, "
              "Without Prejudice). " + PUBLISHER + "; " + PROPRIETOR
              + ".", size=10, height=5.4)
    para(pdf, FLAGPOLE, size=10, height=5.4, align="C")
    centered(pdf, "93 — Live, Love, and let Love, Live.", 11,
             space_after=0)


def build_once(toc):
    en = load_english_units()
    la = load_latin_units()
    units, drift = [], []
    residue_tokens = {}
    for key, en_title, la_title in UNITS_BUILT:
        pairs, n_en, n_la = pair_blocks(en[key]["blocks"], la[key])
        units.append({"key": key, "en_title": en_title,
                      "la_title": la_title, "pairs": pairs})
        drift.append(f"{la_title.split('—')[0].strip()}: English "
                     f"{n_en} paragraph groups, Latin {n_la}; "
                     f"paired {min(n_en, n_la)}, unpaired tail "
                     f"{abs(n_en - n_la)}.")
    # residue census over the built Latin
    for key, _e, _l in UNITS_BUILT:
        for blk in la[key]:
            txt = blk.get("text") or blk.get("note") or ""
            for tok in re.findall(r"[A-Za-zÀ-ÿ]+", txt):
                if tok.lower() in LA_RESIDUE:
                    residue_tokens[tok.lower()] = \
                        residue_tokens.get(tok.lower(), 0) + 1
    n_res = sum(residue_tokens.values())
    # repairs census: occurrences in the raw seams of tokens whose
    # lowercase form stands in the repair table
    raw_lines = LA_SOURCE.read_bytes().decode(
        "utf-8", errors="replace").split("\n")
    n_rep = 0
    for key, _e, _l in UNITS_BUILT:
        a, b = LA_SEAMS[key]
        for ln in raw_lines[a - 1:b]:
            for tok in re.findall(r"[A-Za-zÀ-ÿ£?]+", ln):
                if tok.lower() in LA_REPAIRS:
                    n_rep += 1
    report = {
        "repairs_applied": n_rep,
        "drift_text": " ".join(drift),
        "residue_text": (
            f"{n_res} garbled or unresolved tokens stand across "
            f"Brick {BRICK}'s Latin "
            f"({len(residue_tokens)} distinct forms: "
            + ", ".join(sorted(residue_tokens)) + ")."),
        "residue_tokens": residue_tokens,
        "units": [{"key": u["key"], "pairs": len(u["pairs"])}
                  for u in units],
    }
    pdf = Book(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(MARG_L, MARG_T, MARG_R)
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_font("dejavu", "", f"{DEJAVU}/DejaVuSerif.ttf")
    pdf.add_font("dejavu", "B", f"{DEJAVU}/DejaVuSerif-Bold.ttf")
    # pass structure: front matter must end so the parallel section
    # opens on a verso (even physical leaf)
    toc_entries = [(t[1] + "  ·  " + t[2], toc.get(t[0]))
                   for t in UNITS_BUILT]
    toc_entries.insert(0, ("REVISER'S PREFACE", 2))
    front_matter(pdf, toc_entries)
    while pdf.page_no() % 2 == 0:
        pdf.add_page()          # parity leaf (furniture, declared)
    plan = plan_spreads(pdf, units)
    new_toc = {}
    pdf.set_auto_page_break(False)   # the planner owns the spreads
    emit_parallel(pdf, plan, new_toc)
    pdf.set_auto_page_break(True, margin=18)
    collation_notes(pdf, report)
    back_matter(pdf)
    report["pages"] = pdf.page_no()
    report["toc"] = new_toc
    return pdf, report


def main():
    toc, last = {}, None
    for _ in range(6):
        pdf, report = build_once(toc)
        if report["toc"] == toc and last == report["pages"]:
            break
        toc, last = report["toc"], report["pages"]
    Book.folio_total = report["pages"]
    pdf, report = build_once(toc)
    assert report["toc"] == toc, "contents did not stabilize"
    pdf.output(str(OUT))
    REPORT.write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"built {OUT.name}: {report['pages']} pages; "
          f"toc={report['toc']}")
    print("drift:", report["drift_text"])
    print("residue:", report["residue_text"])


if __name__ == "__main__":
    sys.exit(main())
