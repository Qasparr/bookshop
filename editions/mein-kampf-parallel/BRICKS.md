<!--
=====================================================================
93

BRICKS LEDGER — MEIN KAMPF: A PARALLEL CRITICAL EDITION (MAGVS),
VOL. 1. The state of the build, brick by brick, so any later team
resumes without archaeology. Maintained by the building desk;
errors found at proof are corrected here with a dated note — the
house marks, it does not vanish.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice) — and see
the Reservation leaf of the edition for the founder's doctrine of
that formula (2026-11-10): ARR stands in this volume as an
invocation of the Living Man's Reservation.
X day of November, Dies Martis, Sol in Scorpio,
Anno V:xii e.n. (2026 e.v.)

Scientific Illuminism: the Method of Science, the Aim of Religion.
=====================================================================
-->

# BRICKS — STATE OF THE BUILD

## DONE

- **ARCHITECTURE + PROTOCOL** — `ARCHITECTURE.md` (governing
  spec). Pushed (with the edition's commissioning commits).
- **TITLE REGISTER, ENTRY J-1** — the Japanese witness,
  `apparatus/TITLE-REGISTER-JAPANESE-WITNESS.md`; pushed `f20d66a`;
  founder's form amendment pushed `b8f3bf2`; **boundary note**
  appended 2026-11-10 (17:19 EST ruling — the form ruling is
  bounded to this edition; Black's 2nd Ed MAGVS and every issued
  work keep their forms exactly as issued; completing doctrine:
  ARR *invokes* the Living Man's Reservation, it does not
  constitute it; Black's cover statement stands as the canonical
  form, untouched).
- **BRICK 1 — front matter + Widmung, Vorwort, Kapitel 1 in
  parallel.** Builder: `build_meinkampf_parallel_magvs.py`
  (imports the sibling builder's `load_sections()` — one source,
  one loader). Translations: `translations/en-{widmung,vorwort,
  kap1}.txt`, one English paragraph per German paragraph; counts
  asserted equal at build: **Widmung 7, Vorwort 10, Kapitel 1 62
  — 79 units, zero divergences** from the verified foundation.
  Front matter: title page (authorship in the founder's form),
  the Reservation leaf (the ARR doctrine in terms), source leaf,
  elements leaf, Reviser's Preface to the parallel edition, the
  Translation Protocol in brief, contents. Each section followed
  by its translator's notes ([TN], 14 in Brick 1) and its carried
  notes from the Critical Edition.
  **PDF: `MEIN-KAMPF-PARALLEL-MAGVS-VOL1.pdf` — 47 pages.**
  Verified: all 16 Brick 1 spreads pair an even verso with the
  odd recto carrying the identical ¶ range (Widmung ¶1–7;
  Vorwort ¶1–10; Kapitel 1 ¶1–6, 7–10, 11–14, 15–18, 19–20,
  21–23, 24–30, 31–34, 35–40, 41–44, 45–48, 49–53, 54–59,
  60–62 — complete, no gaps, no overlaps); sample pages rendered
  and inspected. No unit required a sentence split.
  Committed `24db8b9` (boundary note `b50b975`).
- **BRICK 2 — Kapitel 2** ("Wiener Lehr- und Leidensjahre"):
  `translations/en-kap2.txt`, **349 units one-for-one** (counts
  asserted at build); wired into the builder's `BRICK1` list and
  both label tables; preface and contents made cumulative.
  **17 [TN]s**: Judentum and Weltanschauung and Rasse at first
  occurrence; the chapter's F→L misread class (Liier, Lrechheit,
  Lurcht, Lormen/Lorderungen/Leinde/Lrage, Lolgen/Lorm);
  hebe/liebe, Tragen/Fragen, fe/je, Febens/Finie,
  Fobeshymnen/Lobeshymnen; the name locus **Fueger → Lueger**
  (¶254, restored in the English, flagged); fudenfrage/
  Judenfrage; the wanting noun at ¶342 (Erde supplied in the
  English, gap flagged); the bare divider unit "A" (¶202)
  carried as found.
  **PDF now 129 pages.** Verified by full running-head census:
  all 40 Kapitel 2 spreads pair even verso with odd recto at the
  identical ¶ range, coverage ¶1–349 complete, no gaps, no
  overlaps, no unit split; sample recto (p. 49) rendered and
  inspected.
- **BRICK 3 — Kapitel 3** ("Allgemeine politische Betrachtungen
  aus meiner Wiener Zeit"): `translations/en-kap3.txt`, **420
  units one-for-one** (counts asserted at build; the volume's
  largest chapter); wired into the builder's `BRICK1` list and
  both label tables; contents closing line moved to "Kapitel
  4–12"; preface made cumulative. **12 [TN]s**: the
  Parlamentswanzen compound field (¶5); the Führer ruling (¶162
  — rendered "leader" throughout; the note records that the
  word stands already four times in Kapitel 2, where no note
  was set, and that the post-1925 title-sense is not read
  back); Propaganda at its first occurrence in the volume
  (¶130); the Goethe locus "Spottgeburt aus Dreck und Feuer"
  (¶78); the chapter's F→L class (Lührer, Leilschen, Perikies,
  Lederhändler für Federhändler); Schliefern für Schleichern;
  hegen/hegt für liegen/liegt (¶140, ¶371); the broken words
  versäum ten, Grund stein, auszu drücken; Fage für Frage; the
  defective possessive at "ihr größte Stadt"; the lower-case
  "zielen". **PDF now 233 pages.** Verified by full running-head
  census: all 51 Kapitel 3 spreads pair even verso with odd
  recto at the identical ¶ range, coverage ¶1–420 complete, no
  gaps, no overlaps, no unit split (107 spreads whole-book,
  zero anomalies); opening spread (pp. 130–131) and the notes
  page (p. 232) rendered and inspected.

- **BRICK 4 — Kapitel 4** ("München"): `translations/
  en-kap4.txt`, **159 units one-for-one**; wired in as above;
  contents closing line moved to "Kapitel 5–12"; preface made
  cumulative. **8 [TN]s**: Lebensraum at its first occurrence
  in the volume (¶43 — plain spatial sense here; the ruling
  holds the rendering steady for the doctrine chapters);
  the hegen-for-liegen class recurring (¶5, ¶146); lieb und
  teuer misread as "heb und teuer"; Welthandelspobtik;
  Eehrern für Lehrern; the closing F-for-L cluster (Fösung,
  Fehre, Fiteratur, Febens, heben); the two Schiller loci
  (Pappenheimer; the Wallenstein poet-word). **PDF now 287
  pages.** Verified by census: all 26 Kapitel 4 spreads pair
  even verso with odd recto at the identical ¶ range, coverage
  ¶1–159 complete, no gaps, no overlaps (133 spreads
  whole-book, zero anomalies); opening spread (pp. 234–235)
  rendered and inspected.

- **BRICK 5 — Kapitel 5** ("Der Weltkrieg"):
  `translations/en-kap5.txt`, **110 units one-for-one**;
  wired in as above; contents closing line moved to
  "Kapitel 6–12"; preface made cumulative. **9 [TN]s**: the
  Regiment List name-locus ("Fist" for List, restored under
  the house's name ruling, cf. Kapitel 2 ¶196); the F-for-L
  class running through the chapter (Fage, Fosschlagens,
  Fiedes/Fied, Fügner); kauf for Lauf in the fate idiom;
  the doubled-syllable garble "zuzückzuverlieren"; the
  broken word "E rohe rungs willen" (Eroberungswillen);
  hegt for liegt again (¶81). **PDF now 322 pages.** Verified
  by census: all 17 Kapitel 5 spreads pair even verso with
  odd recto at the identical ¶ range, coverage ¶1–110
  complete, no gaps, no overlaps (150 spreads whole-book,
  zero anomalies); opening spread (pp. 288–289) rendered and
  inspected.

- **BRICK 6 — Kapitel 6** ("Kriegspropaganda"):
  `translations/en-kap6.txt`, **71 units one-for-one**;
  wired in as above; contents closing line moved to
  "Kapitel 7–12"; preface made cumulative. **3 [TN]s**: the
  hegen-for-liegen class collected across the chapter (¶13,
  ¶14, ¶26, ¶30); seien for seiten at the ¶37 seam;
  "Krampf1" (closing quote misread as the figure 1).
  **PDF now 342 pages.** Verified by census: all 9 Kapitel 6
  spreads pair even verso with odd recto at the identical
  ¶ range, coverage ¶1–71 complete, no gaps, no overlaps
  (159 spreads whole-book, zero anomalies); opening spread
  (pp. 324–325) rendered and inspected.

- **BRICK 7 — Kapitel 7** ("Die Revolution"):
  `translations/en-kap7.txt`, **136 units one-for-one**;
  wired in as above; contents closing line moved to
  "Kapitel 8–12"; preface made cumulative. German dumps for
  Kapitel 7–12 and the Schlusswort were also struck this
  brick via `sib.load_sections()` and verified against the
  loader's census (136 · 49 · 48 · 295 · 241 · 246 · 5) —
  `work/de-kap7.txt` … `de-schluss.txt`. **5 [TN]s**: the
  Fazarett cluster (¶44–45, ¶47); Ficht for Licht (¶82);
  Lrühjahrs — the F/L class reversed (¶115); the closing
  L-cluster (Lührer, Lreiheit, Lront, Letzen, Lreilich,
  ¶117–118); the Thermopylae epitaph adaptation (¶127).
  **PDF now 376 pages.** Verified by census: all 16
  Kapitel 7 spreads pair even verso with odd recto at the
  identical ¶ range, coverage ¶1–136 complete, no gaps, no
  overlaps (175 spreads whole-book, zero anomalies);
  opening spread (pp. 344–345) rendered and inspected.
  (Build incident, recorded per house practice: the ¶117
  [TN] first carried a straight ASCII quote where the
  German closing quote “ belongs, breaking the builder's
  syntax; caught at compile, the single character
  corrected, nothing else touched.)

- **BRICK 8 — Kapitel 8** ("Beginn meiner politischen
  Tätigkeit"): `translations/en-kap8.txt`, **49 units
  one-for-one**; wired in as above; contents closing line
  moved to "Kapitel 9–12"; preface made cumulative.
  **2 [TN]s**: the transposed name "Schmiedt Ernst"
  (¶1); hegt for liegt twice in the programmatist
  paragraph (¶20). **PDF now 394 pages.** Verified by
  census: all 8 Kapitel 8 spreads pair even verso with
  odd recto at the identical ¶ range, coverage ¶1–49
  complete, no gaps, no overlaps (183 spreads whole-book,
  zero anomalies); opening spread (pp. 378–379) rendered
  and inspected.

- **BRICK 9 — Kapitel 9** ("Die deutsche Arbeiterpartei"):
  `translations/en-kap9.txt`, **48 units one-for-one**;
  wired in as above; contents closing line moved to
  "Kapitel 10–12"; preface made cumulative. **1 [TN]**: the
  verb-less Harrer/Drexler sentence (¶23). **PDF now 410
  pages.** Verified by census: all 7 Kapitel 9 spreads pair
  even verso with odd recto at the identical ¶ range,
  coverage ¶1–48 complete (190 spreads whole-book, zero
  anomalies); opening spread (pp. 396–397) rendered and
  inspected.
  **BUILDER CORRECTION, same brick (marked, not
  vanished):** the first build of this brick FAILED the
  census — Kapitel 9's opening spread spilled one German
  line onto an unpaired page and left a blank recto pair.
  Cause found in `plan_spreads`: the first-spread title
  allowance (a flat 30 mm) was applied only while packing
  the spread's FIRST unit; the checks for units 2..n fell
  back to full-page capacity, and Kapitel 9's first spread
  packed to a measured 230.0 mm of German against a true
  first-page capacity of 222. The packer now prices the
  heading per face (8 mm per heading line + 3 mm after,
  less the 1.4–2.0 mm measure bias observed on standing
  pages) and holds the reduced caps for every unit of the
  first spread. Proof of non-invasion: after the fix,
  Kapitel 1–8 keep their exact standing start pages and
  spread counts; the whole book's census passes clean and
  the two unpaired pages are gone (412 → 410).

- **BRICK 10 — Kapitel 10** ("Ursachen des
  Zusammenbruchs"): `translations/en-kap10.txt`, **295
  units one-for-one**; wired in as above; contents
  closing line moved to "Kapitel 11–12"; preface made
  cumulative. **13 [TN]s**: Schliefern für Schleichern
  (¶72); hegt für liegt twice in the newspaper-reader
  paragraph (¶99); fede für Jede (¶117); the reversed
  L-run Lällen/Lolgen/Lrage (¶121); Fiebesleben and
  Taster für Laster (¶126); den heben Gott für lieben
  (¶128); hegen bleiben (¶138); Feidende/Fage (¶170,
  ¶171); the heading "Prostituierang" (¶176); **the
  truncated sentence (¶180)** — the witness's sentence
  lacks its completion: the secured OCR text itself
  breaks off at "zu" before the heading "Der
  Bolschewismus der Kunst" (verified against the raw
  secured OCR, `../mein-kampf/source/
  mk-vol1-eher1943-ocr.txt`, line 10473); the English
  carries the fragment uncompleted, the presumed
  completion ("sein scheint") is [UNVERIFIED] from this
  witness, and the locus is carried to the final
  Apparatus of OCR Loci — the same truncation necessarily
  stands in the sibling Critical Edition (one source,
  one loader), flagged for the desk; Flumanitätsdusel
  (¶219); hegt/hegen (¶252); heben für Leben twice and
  fugend für Jugend (¶282–285). **PDF now 509 pages.**
  Verified by census: all 48 Kapitel 10 spreads pair
  even verso with odd recto at the identical ¶ range,
  coverage ¶1–295 complete (238 spreads whole-book,
  zero anomalies; Kapitel 1–9 start pages unchanged,
  Kapitel 10 opening at p. 412); opening spread
  (pp. 412–413) rendered and inspected.

- **BRICK 11 — Kapitel 11** ("Volk und Rasse"):
  `translations/en-kap11.txt`, **241 units
  one-for-one**; wired in as above; contents closing
  line moved to "Kapitel 12"; preface made cumulative.
  **19 [TN]s** — the heaviest load of the volume, as
  the OPEN FLAG below foresaw: Febens and Bebens für
  Lebens (¶37); Bronnen für Brunnen (¶39); hegt für
  liegt (¶49; again ¶71, with verrichtet für
  verzichtet; again ¶177); dir für die (¶51); the
  broken "Kulture nt wicklung" and Fhlfskräfte für
  Hilfskräfte (¶53); Lreiheit and Lähigkeiten (¶60);
  the reversed run Lranzose/Lortkommen/Blasse Ahnung
  (¶114); heben für Leben (¶116); Föhn für Lohn
  (¶135); Taster für Laster (¶136); heben für Leben
  and Tage für Lage (¶151); Fichtes für Lichtes
  (¶152); Flandwerkers für Handwerkers (¶162); Fügen
  für Lügen (¶167); fuden für Juden (¶198); Füge für
  Lüge (¶199); the lettered stages of the Werdegang,
  a)–l), the last printed "1)" for "l)" (¶222).
  **PDF now 589 pages.** Verified by census: all 39
  Kapitel 11 spreads pair even verso with odd recto at
  the identical ¶ range, coverage ¶1–241 complete
  (277 spreads whole-book, zero anomalies; Kapitel
  1–10 start pages unchanged, Kapitel 11 opening at
  p. 510); opening spread (pp. 510–511) rendered and
  inspected.

- **BRICK 12 — Kapitel 12** ("Die erste
  Entwicklungszeit der Nationalsozialistischen
  Deutschen Arbeiterpartei"):
  `translations/en-kap12.txt`, **246 units
  one-for-one**; wired in as above; contents closing
  line moved to the Schlusswort and the closing
  apparatus; preface made cumulative. **6 [TN]s**:
  fetzt für jetzt (¶10); the hegen-for-liegen class
  collected across the chapter (¶41, anchoring ¶84,
  ¶95, ¶115, ¶141); the garble "Trätäklub" (¶174 —
  rendered "debating-club" per evident sense,
  [Reading UNVERIFIED], carried to the Apparatus);
  Feere für Leere (¶236); heben für Leben (¶243);
  the volume's narrative last line, "ihren kauf"
  für Lauf (¶246). **PDF now 658 pages.** Verified
  by census: all 34 Kapitel 12 spreads pair even
  verso with odd recto at the identical ¶ range,
  coverage ¶1–246 complete (311 spreads whole-book,
  zero anomalies; Kapitel 1–11 start pages
  unchanged, Kapitel 12 opening at p. 590); opening
  spread (pp. 590–591) and notes page (p. 658)
  rendered and inspected. Word-audit against the
  Brick 11 build: within pp. 1–589 only the preface
  page and the contents page differ, both by exactly
  this brick's wiring.
  **TWO CORRECTIONS at this brick, marked per house
  practice** (the draft wiring stood uncommitted in
  the working tree when this desk took the build
  up): (1) THE CHAPTER TITLE. The draft heading read
  "Die erste Entwicklungszeit der Bewegung". This
  ledger's own wiring note required the title from
  the sibling loader's section head; the printed
  book (and the sibling's SECTIONS table) read "Die
  erste Entwicklungszeit der Nationalsozialistischen
  Deutschen Arbeiterpartei" — "der Bewegung" is a
  phrase of the chapter's first paragraph, not its
  title. Corrected in the spread headings, the
  contents label, the notes label, and the preface's
  enumeration before the brick was built. (2) THE
  ¶49/¶50 SEAM. The draft English of ¶49 carried
  the whole of German ¶50's opening clause across
  the seam (the period restructured around its main
  verb); no word was lost, but the facing claim —
  the same paragraphs on both pages — failed at
  that seam. The English was re-broken at the
  German seam in the draft's own wording ("…must in
  the / sharpest manner make front against…"), as
  the edition keeps every other mid-sentence break
  in step (cf. Kapitel 1, ¶28).

- **BRICK 13 — Schlusswort**: `translations/
  en-schluss.txt`, **5 units one-for-one**; wired
  in as above; contents closing line moved to the
  closing apparatus alone. The Schlusswort's
  German is clean of the witness's misread
  classes — no merged emphasis, no F/L misreads,
  no broken words stand in it — and it carries
  **no [TN]**; its notes page carries the two
  carried notes of the Critical Edition alone.
  **PDF now 662 pages.** Verified by census: the
  Schlusswort's single spread pairs even verso
  with odd recto at ¶1–5 complete (312 spreads
  whole-book, zero anomalies; Kapitel 1–12 start
  pages unchanged, Schlusswort opening at
  p. 660); opening spread (pp. 660–661) rendered
  and inspected. Word-audit against the Brick 12
  build: within pp. 1–658 only the contents page
  differs, by exactly this brick's wiring.

- **FINAL BRICK — THE CLOSING APPARATUS; THE
  VOLUME IS COMPLETE.** In the contents' order:
  **the Tower Audit entire** (pp. 663–670) —
  imported from the sibling builder's data
  (`sib.AUDIT` + `sib.AUDIT_INTRO`, both constants
  confirmed in the sibling file) and printed
  unchanged under a carrier's note: **36 items in
  six groups** (W 2 · A 12 · B 7 · C 6 · D 6 ·
  E 3), tiers PROVEN 10 · SUPPORTED 1 ·
  CONTESTED 6 · FALSE 17 · UNVERIFIED 2 —
  **Glossary of Translation Rulings** (pp.
  671–672): twelve rulings collected from the
  first-occurrence [TN]s (Volk, Bewegung,
  völkisch, Judentum, Weltanschauung, Rasse,
  Propaganda, Führer, Lebensraum, the compound
  field, Names, Quotations) — **Apparatus of OCR
  Loci** (pp. 673–678): every locus flagged in a
  [TN], collected by section — 93 register
  entries, the collected runs among them —
  with the class
  introduction and the standing UNCHARTED
  (first-edition facsimile collation) declared;
  the source locus of Kapitel 10, ¶180 and the
  unverified reading of Kapitel 12, ¶174 carried
  in terms — **Title Register** (pp. 679–682):
  Entry J-1 printed entire from `apparatus/`,
  as filed, with the founder's form amendment
  and the boundary note; the Japanese glyphs
  ride the Noto Serif CJK fallback face,
  switched on for the back matter only (the
  house precedent of the Divine Nine Abroad III
  builder), so no standing page's typesetting
  shifted — **Table of Authorities** (p. 683),
  condensed, the three Japanese translations
  cited bibliographically and Manheim entered
  expressly as NOT an authority of this edition
  — **Colophon** (p. 684), carrying the
  founder's form per the Reservation leaf.
  **PDF now 684 pages — the volume stands
  bound and complete**: front matter; Widmung,
  Vorwort, Kapitel 1–12 and the Schlusswort in
  parallel (312 spreads); the closing apparatus.
  Verified: census re-run on the bound volume —
  312 spreads, zero anomalies, every section's
  coverage complete, every standing start page
  unchanged; word-audit against the Brick 13
  build — within pp. 1–662 only the contents
  page differs, by exactly this brick's entries;
  all 36 Audit item codes present in the bound
  text; the register's Japanese forms
  (『吾が鬪爭』『余の闘争』『我が闘争』, 眞鍋良一)
  extract and render as printed; audit opening
  (p. 663), glossary opening (p. 671), register
  opening (p. 679) and colophon (p. 684)
  rendered and inspected. Announcement is the
  desk's, on the founder's standing pattern.

## NEXT

- Nothing in this volume's scope. Volume 2 is a
  separate commission, on the founder's word.

## OPEN FLAGS

- CLOSED at the final brick: the sibling's
  `AUDIT_INTRO` constant exists under that name
  and was imported with `sib.AUDIT`, as wired.
- STANDING, unchanged: a first-edition (1925)
  facsimile collation remains UNCHARTED (entered
  in the Apparatus of OCR Loci and on the Source
  leaf); the Kapitel 10, ¶180 completion remains
  UNVERIFIED from this witness; the Kapitel 12,
  ¶174 reading remains UNVERIFIED.
- The contents page lists Brick 1 only, by design; it must grow
  with each brick (entries are computed from the section list —
  keep `contents_page` in step when sections are added).
- Any OCR locus in later chapters not covered by the sibling's
  declared classes gets a [TN] at its unit and a line in the
  final Apparatus of OCR Loci.
- Chapters 11 ("Volk und Rasse") will carry the heaviest [TN]
  load (Rasse and the period's racial vocabulary at first
  occurrence); the Protocol's unsparing-fidelity rule governs —
  the translation does not soften, the Audit answers.

93 — Live, Love, and let Love, Live.
