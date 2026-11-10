<!--
=====================================================================
93

"I know that men are won over less by the written word than by the
spoken." -- the author of the text under audit, in his Vorwort.
This edition answers the written word with the written record --
in both of the book's languages at once, facing each other, so that
no reader of either tongue ever has to take the other's word for
what the page says.

MEIN KAMPF, ERSTER BAND -- A PARALLEL CRITICAL EDITION (MAGVS):
BUILD PLAN AND TRANSLATION PROTOCOL.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice).
X day of November, Dies Martis, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved
and coined under the authority of the Living Man. -- The Flagpole
on this volume claims THE TRANSLATION, THE APPARATUS AND THE AUDIT
ONLY. The German text is public domain (first published 1925; the
author died 1945); no claim reaches for it, and the title page
says so.
=====================================================================
-->

# ARCHITECTURE — MEIN KAMPF PARALLEL CRITICAL EDITION (MAGVS), VOL. 1

## I. THE COMMISSION

Commissioned by the founder, 2026-11-10: a TRUE PARALLEL-TEXT
edition of Mein Kampf, Volume One — the German text on the verso,
a NEW house English translation on the facing recto — built in
bricks alongside a second team's parallel Leviathan, and bound in
the same Teacher's Edition dress as the house's Critical Edition
of the German text alone (the sibling volume, 307 pp, which this
edition EXTENDS and does not replace, reopen, or alter).

## II. INPUTS

1. THE GERMAN TEXT OF RECORD is the secured source of the sibling
   edition, byte-for-byte, and nothing else:
   `../mein-kampf/source/mk-vol1-eher1943-ocr.txt` — Internet
   Archive OCR full text of the Eher unabridged printing,
   851.–855. Auflage 1943; SHA-256
   a5de081b761e16a03aa3ec2465a5141c6e2d5e224391016a2222bb420d30cb19;
   census and limits declared in `../mein-kampf/source/
   SOURCE-LEDGER.md`, which this edition incorporates by reference
   and reprints in brief on its Source leaf. The sections are
   extracted by the SIBLING BUILDER'S OWN loader (imported, not
   re-implemented), so the German printed here cannot drift from
   the German printed there: one source file, one loader, one text.
2. THE CARRIED APPARATUS: the sibling edition's chapter notes and
   correlations (33 notes across the volume's sections) and its
   TOWER AUDIT (36 items, six groups, tiered PROVEN / SUPPORTED /
   CONTESTED / FALSE / UNVERIFIED with reasoning), imported from
   the sibling builder's data and printed in this edition's back
   matter and section notes, attributed as carried.
3. THE TRANSLATION: the house's own, made for this edition under
   the Protocol at §IV. No other translation is an input. None.

## III. PROCESSES — THE PARALLEL MECHANISM

1. ALIGNMENT UNIT. The unit of alignment is the PARAGRAPH. The
   loader yields each section as an ordered list of German
   paragraphs; the translation file for that section yields an
   ordered list of English paragraphs, ONE FOR ONE, in the same
   order. The builder asserts the counts equal and FAILS THE BUILD
   if they are not. A paragraph too long for one page is split at
   a sentence boundary into numbered sub-units on both sides,
   marked with a continuation sign (¶ n, cont.) — the split is a
   typesetting act, recorded in the build log, touching no word.
2. THE SPREAD. Pages are composed in spreads: a verso (even folio)
   carrying German, the facing recto (odd folio) carrying the
   English of THE SAME units. The composer packs units greedily,
   measuring both sides at the set measure (fpdf2 dry-run heights)
   and closing the spread before either side would overflow its
   page; both pages of a spread therefore always carry identical
   unit ranges, stated in each page's running head ("¶ 12–18").
   A chapter always opens on a fresh verso; a blank leaf is
   inserted when parity requires it, and the blank is printed as
   a blank — marked with the edition's rule and nothing else.
3. RUNNING HEADS. Verso head: `DEUTSCH — n. KAPITEL, ¶ a–b`.
   Recto head: `ENGLISH — CHAPTER n, ¶ a–b`. The reader can check
   the facing claim on any opening in one glance: that checkability
   IS the edition's method, the Zero-Point discipline made typographic.
4. NOTES. Translator's notes (marked [TN]) ride at the foot of
   the recto where their term first occurs, or in the section's
   endnotes where they are long. The carried chapter notes print
   after each section's parallel text, as in the sibling edition.
5. DRESS. Teacher's Edition: doctrine-logo head on the title page;
   title block with authorship and Thelemic date; Classification;
   Flagpole front and back; front matter in Roman-numbered
   sections; page footers "— N of M — | All Rights Reserved,
   Without Prejudice | Flagpole of Claim and Coinage reserved";
   Table of Authorities; Colophon; the four-element content test
   stated on the Elements leaf.
6. TWO-PASS BUILD, as with the sibling editions: pass one
   measures, pass two prints the contents numbers. fpdf2
   discipline: every multi_cell passes
   new_x=XPos.LMARGIN, new_y=YPos.NEXT.

## IV. THE TRANSLATION PROTOCOL (non-negotiable)

1. OWN WORK ONLY. The translation is made by this desk directly
   from the German text of record. The standard English
   translation by Ralph Manheim (1943) is under copyright: it is
   NEVER consulted, copied, or paraphrased — not for a word, not
   for a cadence, not to check a difficulty. Difficulties are
   resolved from the German, from dictionaries, and from the
   translator's judgment, and where judgment is uncertain the
   uncertainty is footnoted, not hidden. Any rendering a reader
   may think resembles another translation resembles it because
   the German admits a narrow range of honest English, not
   because it was seen.
2. FIDELITY IS LITERAL AND UNSPARING. The translation renders
   what the text says: its claims, its slurs, its racial doctrine,
   its threats — without softening, omission, euphemism, or
   editorializing inside the translation itself. To soften this
   text would be to falsify the evidence; to omit would be to
   destroy it. The founder's law governs the whole edition:
   JUDGMENT COMES LAST, NEVER FIRST — judgment lives where it
   belongs, in the preface, the notes, and the Tower Audit, and
   the translation keeps its hands clean of it.
3. SYNTAX. German sentence architecture is carried into English
   as far as English bears it; where a German period must be
   broken for English sense, it is broken at a clause joint and
   the break is silent (a punctuation act, not a wording act).
   The 1943 printing's orthography (daß, muß) is the German
   page's; the English page uses modern English spelling.
4. LOADED TERMS. Contested or loaded terms receive a translator's
   note at first occurrence — Volk, völkisch, Rasse, Lebensraum,
   Weltanschauung, Führer, Bewegung, Gleichschaltung class terms,
   the period's racial vocabulary, and institutional names —
   stating the German word, its literal range, the rendering
   chosen, and the reason. Thereafter the chosen rendering is
   used consistently; a glossary in the back matter collects the
   rulings so any reader can audit the consistency.
5. NAMES AND FACTS. Proper names, dates, figures, and place
   names are rendered as the German gives them. Where the German
   text states a falsehood, the translation states the same
   falsehood — correction is the Audit's office, and it is
   exercised there, with receipts.
6. OCR HONESTY. The German is printed as found, including the
   source's declared OCR loci (merged letterspaced-emphasis
   words; rare single-letter misreads). The translation of a
   corrupt locus translates the evident sense and carries a [TN]
   flag naming the locus as printed — never a silent fix on
   either page.

## V. OUTPUTS

`MEIN-KAMPF-PARALLEL-MAGVS-VOL1.pdf` — cumulative with each brick:
front matter; Widmung, Vorwort, and Kapitel 1–12 in parallel;
Schlusswort in parallel; the carried Tower Audit, the glossary of
translation rulings, the apparatus of OCR loci, the TITLE
REGISTER (including Entry J-1, the Japanese witness, filed by
founder's addendum 2026-11-10 — apparatus/TITLE-REGISTER-
JAPANESE-WITNESS.md; bibliographic citation only, the Manabe
translation's status flagged UNVERIFIED in terms, no text of any
Japanese translation reproduced), Table of Authorities, and
Colophon in the final brick.

## VI. TOLERANCES

Any step that would change a word of the German body fails the
edition. Any translation choice that softens, omits, or improves
the original fails the translation. Any audit tier asserted
without its reasoning fails the audit. What the desk cannot
verify it marks UNVERIFIED; what the German cannot responsibly
bear it marks UNCHARTED, with the locus. It does not invent.

## VII. THE BRICK LEDGER (builds as they stand)

- BRICK 1 — Architecture + protocol (this document); front matter
  (title page, source leaf, elements leaf, Reviser's Preface for
  the parallel edition, the Protocol in brief, contents); Widmung,
  Vorwort, and Kapitel 1 complete in parallel, with carried notes.
- BRICKS 2–13 — Kapitel 2–12, one chapter per brick, each with its
  carried notes, cumulative PDF, page count verified, facing
  alignment spot-checked, committed and pushed per brick.
- FINAL BRICK — Schlusswort in parallel; Tower Audit (carried,
  complete); glossary of translation rulings; OCR-loci apparatus;
  Title Register (Entry J-1, the Japanese witness, as filed);
  Table of Authorities; Colophon. Bound-volume announcement is
  the desk's, on the founder's standing pattern, at completion.
- LEDGER NOTE: errors found at proof in any house document are
  corrected with a dated note in this ledger — the house marks,
  it does not vanish.

93 — Live, Love, and let Love, Live.
