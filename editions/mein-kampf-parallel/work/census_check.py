#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93

CENSUS CHECK — MEIN KAMPF: A PARALLEL CRITICAL EDITION (MAGVS).

MECHANISM: reads the built PDF's running heads (pdftotext, page by
page) and verifies the edition's facing claim mechanically, for
every section: each spread pairs an EVEN verso (DEUTSCH) with the
following ODD recto (ENGLISH) carrying the IDENTICAL paragraph
range; the ranges of a section cover 1..N completely — no gaps, no
overlaps, no split unaccounted (a split sub-unit repeats its unit
number in both heads, which this checker reports as an OVERLAP
flag for the desk to reconcile against the build log).

DOCTRINE: the census is the audit of the alignment claim itself —
if the heads lie, the edition lies; the checker trusts nothing the
builder printed except what the pages carry.

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice).
Scientific Illuminism: the Method of Science, the Aim of Religion.

Usage: python3 census_check.py [pdf] [--expect-pages N]
"""

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ED = HERE.parent


def load_pb():
    spec = importlib.util.spec_from_file_location(
        "pb", ED / "build_meinkampf_parallel_magvs.py")
    pb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pb)
    return pb


HEAD = re.compile(r"(DEUTSCH|ENGLISH) — (.+?), ¶ (\d+)(?:–(\d+))?")


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 and \
        not sys.argv[1].startswith("--") else ED / \
        "MEIN-KAMPF-PARALLEL-MAGVS-VOL1.pdf"
    pb = load_pb()
    german = dict(pb.sib.load_sections())
    names = {}
    for key, _hd, _he, run_de, run_en in pb.BRICK1:
        names[run_de] = key
        names[run_en] = key

    raw = subprocess.run(["pdftotext", str(pdf_path), "-"],
                         capture_output=True, text=True).stdout
    pages = raw.split("\f")
    heads = {}      # key -> [(page, side, a, b)]
    order = []
    for pno, ptext in enumerate(pages, start=1):
        m = HEAD.search(ptext)
        if not m:
            continue
        side, sname, a, b = m.group(1), m.group(2), int(m.group(3)), \
            int(m.group(4) or m.group(3))
        key = names.get(sname)
        if key is None:
            print(f"  !! p.{pno}: unknown section name {sname!r}")
            continue
        if key not in heads:
            heads[key] = []
            order.append(key)
        heads[key].append((pno, side, a, b))

    anomalies = 0
    total_spreads = 0
    for key in order:
        rows = heads[key]
        n = len(german[key])
        problems = []
        covered = []
        if len(rows) % 2:
            problems.append(f"odd head count {len(rows)}")
        for i in range(0, len(rows) - 1, 2):
            (p1, s1, a1, b1), (p2, s2, a2, b2) = rows[i], rows[i + 1]
            total_spreads += 1
            if not (s1 == "DEUTSCH" and s2 == "ENGLISH"):
                problems.append(f"spread {i//2+1}: sides {s1}/{s2}")
            if p1 % 2 != 0 or p2 != p1 + 1:
                problems.append(
                    f"spread {i//2+1}: folios {p1}/{p2} not even/odd pair")
            if (a1, b1) != (a2, b2):
                problems.append(
                    f"spread {i//2+1}: ranges {a1}–{b1} vs {a2}–{b2}")
            covered.extend(range(a1, b1 + 1))
        if covered != list(range(1, n + 1)):
            problems.append(
                f"coverage != 1..{n} (got {len(covered)} units, "
                f"first break at "
                f"{next((j + 1 for j in range(min(len(covered), n)) if covered[j] != j + 1), None)})")
        start = rows[0][0]
        print(f"{key}: {len(rows)//2} spreads, start p.{start}, "
              f"coverage 1..{n} — " +
              ("OK" if not problems else "PROBLEMS: " +
               "; ".join(problems)))
        anomalies += len(problems)
    print(f"TOTAL: {total_spreads} spreads, {anomalies} anomalies")
    return 1 if anomalies else 0


if __name__ == "__main__":
    sys.exit(main())

# 93 — Live, Love, and let Love, Live.
