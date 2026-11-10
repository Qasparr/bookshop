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

## NEXT

- **BRICK 10 — Kapitel 10** ("Ursachen des
  Zusammenbruchs"): write `translations/en-kap10.txt`
  (295 units; German dump already in
  `work/de-kap10.txt`), add the `("kap10", ...)` 5-tuple
  and the `labels` entries, move the contents closing
  line to "Kapitel 11–12", add [TN]s, rebuild, verify by
  census, commit, push. Then Bricks 11–13 likewise
  (Kapitel 11–12, one per brick), per ARCHITECTURE §VII.
- **FINAL BRICK** — Schlusswort in parallel; the carried Tower
  Audit entire (import `sib.AUDIT` + `sib.AUDIT_INTRO`); Glossary
  of Translation Rulings (seeded by the [TN] rulings: Volk,
  Bewegung, völkisch, and every first-occurrence note after);
  Apparatus of OCR Loci; Title Register (Entry J-1 prints from
  `apparatus/`); Table of Authorities; Colophon (the colophon
  carries the founder's form per the Reservation leaf).

## OPEN FLAGS

- The sibling builder's `AUDIT_INTRO` constant is referenced by
  the final brick; confirm its name in the sibling file when
  that brick is built (the audit body is `sib.AUDIT`).
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
