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
          notes and its carried notes. Brick 2 added Kapitel 2
          (349 units); Brick 3 added Kapitel 3 (420 units, the
          volume's largest); Bricks 4-9 added Kapitel 4-9 (159,
          110, 71, 136, 49 and 48 units), each in the same
          facing form. Brick 9 also corrected the spread
          packer's first-spread capacity (see plan_spreads):
          per-face heading-priced caps, verified to leave the
          standing spreads of Kapitel 1-8 untouched.
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
    ("kap3", "3. KAPITEL — ALLGEMEINE POLITISCHE "
     "BETRACHTUNGEN AUS MEINER WIENER ZEIT",
     "CHAPTER 3 — GENERAL POLITICAL CONSIDERATIONS FROM MY "
     "VIENNA TIME", "3. KAPITEL", "CHAPTER 3"),
    ("kap4", "4. KAPITEL — MÜNCHEN", "CHAPTER 4 — MUNICH",
     "4. KAPITEL", "CHAPTER 4"),
    ("kap5", "5. KAPITEL — DER WELTKRIEG",
     "CHAPTER 5 — THE WORLD WAR", "5. KAPITEL", "CHAPTER 5"),
    ("kap6", "6. KAPITEL — KRIEGSPROPAGANDA",
     "CHAPTER 6 — WAR PROPAGANDA", "6. KAPITEL", "CHAPTER 6"),
    ("kap7", "7. KAPITEL — DIE REVOLUTION",
     "CHAPTER 7 — THE REVOLUTION", "7. KAPITEL", "CHAPTER 7"),
    ("kap8", "8. KAPITEL — BEGINN MEINER POLITISCHEN "
     "TÄTIGKEIT", "CHAPTER 8 — BEGINNING OF MY POLITICAL "
     "ACTIVITY", "8. KAPITEL", "CHAPTER 8"),
    ("kap9", "9. KAPITEL — DIE DEUTSCHE ARBEITERPARTEI",
     "CHAPTER 9 — THE GERMAN WORKERS' PARTY", "9. KAPITEL",
     "CHAPTER 9"),
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
    ("kap3", 4):
        "Parlamentswanzen ('parliament-bedbugs'): the chapter's "
        "parliament vocabulary is a compound field — Parlament, "
        "Parlamentarier ('parliamentarian'), Parlamentarismus "
        "(the heading at ¶50) — and its invective compounds are "
        "carried whole into the English, never dissolved into a "
        "politer periphrasis. The ruling is collected in the "
        "Glossary. [The compound's first occurrence.]",
    ("kap3", 41):
        "Printed 'versäum ten': a word of the witness broken "
        "across a space (versäumten, 'neglected') — the same "
        "locus class as Kapitel 1, ¶31. The English translates "
        "the evident reading; the German page is not emended.",
    ("kap3", 46):
        "Printed 'der Grund stein': the word Grundstein "
        "('foundation stone') broken across a space in the "
        "witness. Translated per evident sense.",
    ("kap3", 77):
        "“Spottgeburt aus Dreck und Feuer” is a quotation — "
        "Goethe, Faust — carried in the English word for word "
        "as the author carries it: 'mock-birth out of dirt and "
        "fire.' The borrowing is the author's; the Audit, not "
        "the translation, weighs the use he makes of it.",
    ("kap3", 108):
        "The F-to-L misread class of this witness (declared at "
        "Kapitel 2) runs through this stretch: here 'Lührer' "
        "for Führer, 'Leilschen' for Feilschen ('haggling'), "
        "'Perikies' for Perikles; and at ¶110 'Lederhändler' "
        "for Federhändler ('quill-trader'). The German page "
        "prints each as found; the English translates the "
        "evident readings.",
    ("kap3", 129):
        "Propaganda: the word's first occurrence in the "
        "volume. It is rendered 'propaganda' throughout, in "
        "the word's period sense — the organized working upon "
        "the mass mind, which the author here names as the "
        "press's office and later chapters raise to a doctrine "
        "of the movement. The ruling is collected in the "
        "Glossary. [First occurrence.]",
    ("kap3", 158):
        "Printed 'Schliefern': an OCR misread of Schleichern "
        "('sneaks'). Translated per evident sense.",
    ("kap3", 161):
        "Führer: rendered 'leader' throughout the edition, and "
        "the compounds with it — Führergedanke ('leader-"
        "thought', the heading at ¶96), Führertum. The word "
        "stands already four times in Kapitel 2, where no note "
        "was set; the ruling is stated here, where the chapter "
        "makes the word's office its subject (the 'free "
        "election of the leader' in a 'Germanic democracy'), "
        "and is collected in the Glossary. The title-sense the "
        "word later acquired is not read back into the text of "
        "1925.",
    ("kap3", 170):
        "Printed 'als ihr größte Stadt': the possessive stands "
        "defective in the witness (ihre größte Stadt, 'their "
        "greatest city'). The English translates the evident "
        "reading; the locus is flagged, not repaired, on the "
        "German page.",
    ("kap3", 244):
        "Printed 'Die Fage in Österreich': an OCR misread of "
        "Die Frage ('the question'); and at ¶246 the word "
        "auszudrücken stands broken across a space ('auszu "
        "drücken'). Translated per evident sense in both "
        "places.",
    ("kap3", 285):
        "Printed 'großen zielen': the noun stands lower-case "
        "in the witness (großen Zielen, 'great goals') — a "
        "case fault of the scan. The English translates the "
        "evident reading.",
    ("kap3", 370):
        "Printed 'zu hegen': an OCR misread of zu liegen ('to "
        "lie') — the same misread stands at ¶140 ('bei ihr "
        "hegt' for bei ihr liegt). Translated per evident "
        "sense in both places.",
    ("kap4", 2):
        "Printed 'heb und teuer': an OCR misread of lieb und "
        "teuer ('dear and precious'). Translated per evident "
        "sense.",
    ("kap4", 4):
        "The hegen-for-liegen misread of Kapitel 3 recurs in "
        "this witness's Kapitel 4: here 'hegt wohl "
        "mitbegründet' for liegt wohl mitbegründet, and again "
        "at ¶146 ('Verschlagenheit hegen' for Verschlagenheit "
        "liegen). Translated per evident sense in both places.",
    ("kap4", 42):
        "Lebensraum ('living-space'): the word's first "
        "occurrence in the volume, here in its plain spatial "
        "sense — the room at a people's disposal. Rendered "
        "'living-space' throughout the edition; where the "
        "later chapters raise the word into the doctrine of "
        "soil to be taken in the East, the rendering does not "
        "change, and the Audit weighs the doctrine. The ruling "
        "is collected in the Glossary. [First occurrence.]",
    ("kap4", 48):
        "“Er kennt seine Pappenheimer” — 'he knows his "
        "Pappenheimer': the saying is Schiller's (Wallenstein), "
        "of the general who knows his men and what they are "
        "good for. Carried in the English as the author carries "
        "it, untranslated in the name.",
    ("kap4", 98):
        "Printed 'Welthandelspobtik': an OCR garble of "
        "Welthandelspolitik ('world-trade policy'). Translated "
        "per evident sense.",
    ("kap4", 104):
        "Printed 'erhabenen Eehrern': an OCR misread of "
        "erhabenen Lehrern ('sublime teachers'). Translated "
        "per evident sense.",
    ("kap4", 136):
        "The 'poet-word' quoted — “Und setzet ihr nicht das "
        "Leben ein, nie wird euch das Leben gewonnen sein” — "
        "is Schiller's, from Wallenstein. The author quotes "
        "without naming; the English carries the verse as he "
        "carries it.",
    ("kap4", 149):
        "A dense run of this witness's F-for-L misread class "
        "closes the chapter: here 'des Rätsels Fösung' for "
        "Lösung and 'marxistische Fehre' for Lehre; at ¶151 "
        "'diese Fehre der Zerstörung', 'in meinem heben' for "
        "in meinem Leben, 'politischen Febens' for "
        "politischen Lebens, and 'theoretische Fiteratur' for "
        "theoretische Literatur. The German page prints each "
        "as found; the English translates the evident readings "
        "throughout.",
    ("kap5", 6):
        "Printed 'sich wieder zuzückzuverlieren': a doubled-"
        "syllable garble of sich wieder zurückzuverlieren ('to "
        "lose itself back again'). Translated per evident "
        "sense.",
    ("kap5", 14):
        "Printed 'dem Schicksal seinen kauf zu lassen': kauf "
        "for Lauf — the idiom is dem Schicksal seinen Lauf "
        "lassen, 'to let fate have its course'. Translated "
        "per evident sense.",
    ("kap5", 16):
        "Printed 'der günstigen Stunden des Fosschlagens': "
        "Fosschlagens for Losschlagens ('of striking loose'), "
        "an F-for-L misread of the class this witness carries "
        "throughout. Translated per evident sense.",
    ("kap5", 17):
        "Printed 'an der Fage': Fage for Frage, as at Kapitel "
        "3, ¶245. Translated per evident sense.",
    ("kap5", 40):
        "Printed twice in this paragraph 'Fiedes' and 'Fied' "
        "for Liedes and Lied ('the sounds of a song... the "
        "song also reached us'), F-for-L misreads. Translated "
        "per evident sense.",
    ("kap5", 42):
        "Printed 'des Regiments Fist': Fist for List. The "
        "author's own regiment — the Bavarian Reserve Infantry "
        "Regiment named for its commander, Oberst List — is a "
        "matter of record; a name is a fact, and the house's "
        "standing ruling (Kapitel 2, ¶196) restores the fact in "
        "the English while the German page prints the witness "
        "as found.",
    ("kap5", 80):
        "Printed 'allein hegt die allererste Voraussetzung': "
        "hegt for liegt, the hegen-for-liegen misread already "
        "entered at Kapitel 3, ¶140, and Kapitel 4, ¶5. "
        "Translated per evident sense.",
    ("kap5", 89):
        "Printed 'stürmischem E rohe rungs willen': the word "
        "Eroberungswillen ('will-to-conquest') broken by the "
        "scan into spaced fragments. Translated as the evident "
        "word.",
    ("kap5", 94):
        "Printed 'die Dummheit der Fügner': Fügner for Lügner "
        "('liars'), an F-for-L misread. Translated per evident "
        "sense.",
    ("kap6", 12):
        "The hegen-for-liegen misread runs through this "
        "chapter: here 'eines im Kampfe hegenden Volkes' for "
        "liegenden; at ¶14 'in der Kürze des Verfahrens "
        "hege' for liege; at ¶26 and ¶30 'hegt' for liegt. "
        "Translated per evident sense throughout (cf. Kapitel "
        "3, ¶140; Kapitel 4, ¶5; Kapitel 5, ¶81).",
    ("kap6", 37):
        "Printed 'seien des Gegners kennenlernte': seien for "
        "seiten — 'which he came to know on himself from the "
        "sides of the opponent'. Translated per evident sense.",
    ("kap6", 38):
        "Printed '„Krampf1': in this witness the closing "
        "quotation mark after Krampf is misread as the figure "
        "1. The German page prints it as found.",
    ("kap7", 43):
        "A run of this witness's F-for-L class: 'Fazarett' "
        "here and at ¶47 for Lazarett (hospital); '„massein' "
        "for „masseln — the front slang for grumbling (cf. "
        "¶29, where the class reads it correctly); and at "
        "¶45 'bei der Feitung' for bei der Leitung ('at the "
        "direction'). Translated per evident sense "
        "throughout.",
    ("kap7", 81):
        "Printed 'ein grellrotes Ficht': Ficht for Licht "
        "('light'), an F-for-L misread. Translated per "
        "evident sense.",
    ("kap7", 114):
        "Printed 'dem des Lrühjahrs': Lrühjahrs for "
        "Frühjahrs ('of spring') — the witness's F/L misread "
        "class running in reverse. Translated per evident "
        "sense.",
    ("kap7", 116):
        "The F/L class concentrated to the edge of sense: "
        "printed 'die „Lührer“' for Führer, '„Lreiheit, "
        "Schönheit und Würde“' for Freiheit, 'an der Lront' "
        "for an der Front, 'den roten Letzen' for den roten "
        "Fetzen ('the red rag'), and at ¶118 'Lreilich' for "
        "Freilich. Translated per evident sense throughout.",
    ("kap7", 126):
        "The stone's inscription adapts the Thermopylae "
        "epitaph — Simonides' lines for the Spartan dead, "
        "long canonical in Germany in Schiller's rendering: "
        "'Wanderer, kommst du nach Sparta, verkündige "
        "dorten, du habest uns hier liegen gesehn, wie das "
        "Gesetz es befahl.' The author sets Deutschland in "
        "Sparta's place and duty in the law's; the English "
        "carries his words as he gives them.",
    ("kap8", 0):
        "Printed 'Schmiedt Ernst': the comrade's name stands "
        "in the witness transposed and spelled Schmiedt for "
        "Schmidt. A name is a fact (cf. Kapitel 2, ¶196); "
        "the English gives it in its natural order and "
        "spelling.",
    ("kap8", 19):
        "Twice in this paragraph 'hegt' for liegt ('the "
        "greatness of the one lies... its significance lies') "
        "— the hegen-for-liegen misread entered at Kapitel "
        "3, ¶140. Translated per evident sense in both "
        "places.",
    ("kap9", 22):
        "The sentence stands in this witness without its "
        "second verb: 'Der Vorsitzende der "
        "„Reichsorganisation“ war ein Herr Harrer, der von "
        "München Anton Drexler' — the chairman of the Munich "
        "organization is named without a 'was'. The office "
        "and the man are both matters of the record the "
        "chapter itself keeps; the English supplies the verb "
        "per evident construction, and the German page "
        "prints the sentence as found.",
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


def _head_lines(text):
    """Lines the chapter heading occupies at its measure: the
    scratch document set to the heading font, one multi_cell at
    the heading's line height (8), counted off the pen's
    travel. The heading is the first spread's only furniture
    beyond the running head, so its line count prices that
    spread's lost capacity exactly."""
    global _scratch
    if _scratch is None:
        _scratch = new_book()
        _scratch.add_page()
    pdf = _scratch
    pdf.set_font("dejavu", "B", 13.5)
    y0 = pdf.get_y()
    pdf.multi_cell(0, 8, text, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    lines = round((pdf.get_y() - y0) / 8)
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    return max(lines, 1)


def plan_spreads(key, de_list, en_list, log):
    """Greedy spread packing (ARCHITECTURE SSIII.2): a spread is a
    list of unit indices; both pages of a spread always carry the
    identical range. Returns [(indices, [sub-paras or None...])] --
    in Brick 1 no unit splits, so sub-paras are the units
    themselves; the split path rewrites the unit stream first.

    FIRST-SPREAD CAPACITY (corrected at Brick 9): a chapter's
    first spread also carries the chapter heading -- 8 mm per
    heading line plus 3 mm after it, per face, since the two
    headings wrap independently. The packer originally priced
    that furniture with a flat 30 mm allowance applied only to
    the spread's first unit: the accumulation checks for units
    2..n silently fell back to the full-page capacity, and
    Kapitel 9's first spread, packed to a measured 230.0 mm of
    German against a true 222, spilled one line onto an
    unpaired page and left its recto's pair blank. The caps are
    now per-face and hold for every unit of the first spread.
    The 2 mm measure bias is observed, not hoped: measure()
    over-reads a full standing page by 1.4-2.0 mm (Kapitel 3's
    first spread measures 215.6 against a true 214 and renders
    inside it), so each face's allowance is its heading cost
    less that bias. Verified non-invasive: the first spreads
    of Kapitel 1-8 pack identically under the corrected caps."""
    capacity = PAGE_BOTTOM - CONTENT_TOP
    heads = {k: (hd, he) for k, hd, he, _rd, _re in BRICK1}
    head_de, head_en = heads[key]
    cap_de_first = capacity - (_head_lines(head_de) * 8 + 1)
    cap_en_first = capacity - (_head_lines(head_en) * 8 + 1)
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
        cap_de = cap_de_first if not spreads else capacity
        cap_en = cap_en_first if not spreads else capacity
        hd, he = measure(de), measure(en)
        if cur and (h_de + hd > cap_de or h_en + he > cap_en):
            spreads.append(cur)
            cur, h_de, h_en = [], 0.0, 0.0
            assert hd <= capacity and he <= capacity, \
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
    "In the Parents' Home, the second, Vienna Years of "
    "Learning and Suffering, the third, General Political "
    "Considerations from My Vienna Time, the fourth, "
    "Munich, the fifth, The World War, the sixth, War "
    "Propaganda, the seventh, The Revolution, and the "
    "eighth, Beginning of My Political Activity, and the "
    "ninth, The German Workers' Party. The chapters "
    "follow, brick "
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
                       "of Learning and Suffering", "Kapitel 2"),
              "kap3": ("3. Kapitel — Allgemeine politische "
                       "Betrachtungen aus meiner Wiener Zeit / "
                       "Chapter 3 — General Political "
                       "Considerations from My Vienna Time",
                       "Kapitel 3"),
              "kap4": ("4. Kapitel — München / Chapter 4 — "
                       "Munich", "Kapitel 4"),
              "kap5": ("5. Kapitel — Der Weltkrieg / Chapter 5 "
                       "— The World War", "Kapitel 5"),
              "kap6": ("6. Kapitel — Kriegspropaganda / "
                       "Chapter 6 — War Propaganda",
                       "Kapitel 6"),
              "kap7": ("7. Kapitel — Die Revolution / "
                       "Chapter 7 — The Revolution",
                       "Kapitel 7"),
              "kap8": ("8. Kapitel — Beginn meiner "
                       "politischen Tätigkeit / Chapter 8 — "
                       "Beginning of My Political Activity",
                       "Kapitel 8"),
              "kap9": ("9. Kapitel — Die deutsche "
                       "Arbeiterpartei / Chapter 9 — The "
                       "German Workers' Party", "Kapitel 9")}
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
    para(pdf, "Kapitel 10–12, the Schlusswort in parallel, "
          "the "
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
              "kap2": "2. Kapitel — Wiener Lehr- und Leidensjahre",
              "kap3": "3. Kapitel — Allgemeine politische "
                      "Betrachtungen aus meiner Wiener Zeit",
              "kap4": "4. Kapitel — München",
              "kap5": "5. Kapitel — Der Weltkrieg",
              "kap6": "6. Kapitel — Kriegspropaganda",
              "kap7": "7. Kapitel — Die Revolution",
              "kap8": "8. Kapitel — Beginn meiner "
                      "politischen Tätigkeit",
              "kap9": "9. Kapitel — Die deutsche "
                      "Arbeiterpartei"}
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
