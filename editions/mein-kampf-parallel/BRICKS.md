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

## NEXT

- **BRICK 3 — Kapitel 3** ("Allgemeine politische Betrachtungen
  aus meiner Wiener Zeit"): write `translations/en-kap3.txt`
  (420 units by the loader — the largest chapter of the volume;
  it may itself be laid in two sittings of one brick), add the
  `("kap3", ...)` 5-tuple to the builder's `BRICK1` list, extend
  both `labels` tables, move the contents closing line to
  "Kapitel 4–12", add [TN]s (watch first occurrences: Führer,
  Propaganda, Parlament compounds), rebuild, verify by census,
  commit, push. Then Bricks 4–13 likewise (Kapitel 4–12, one per
  brick), per ARCHITECTURE §VII.
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
