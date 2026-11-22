#!/usr/bin/env python3
# =====================================================================
# 93
#
# "Render unto Caesar the things which are Caesar's; and unto God
#  the things that are God's." — Matthew 22:21 (KJV)
#
# RECEIPT.PY — THE BOOKSHOP RECEIPT BOOK AND TAX JAR
# A Scientific Illuminist treatment of the till: every payment that
# lands is receipted, numbered, and split at the door — a set-aside
# for taxes into its own envelope, the remainder spendable — so that
# when taxes come due, the amount is already standing in the jar.
#
# Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
# (Greek, -ARR, All Rights Reserved, Without Prejudice)
# IX day of November, Dies Lunae, Sol in Scorpio,
# Anno V:xii e.n. (2026 e.v.)
#
# Classification: Enterprise • Educational • Research & Development
# Method of Science, Aim of Religion
#
# Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR,
# All Rights Reserved, Without Prejudice. Right of claim hereby
# reserved and coined under the authority of the Living Man.
#
# =====================================================================
# DOCTRINE — WHAT THIS TOOL IS, AND WHAT IT IS NOT
#
# MECHANISM: A single-file, standard-library-only command line tool.
# It keeps three records in its own directory:
#   ledger.jsonl — one JSON object per payment, append-only. This is
#                  the book of record (the Schedule C memory).
#   coupons.txt  — thank-you coupon codes, one per line, with the
#                  receipt that issued them and their status.
#   receipts/    — one human-readable .txt receipt per payment.
# config.json (created on first run) holds the tax set-aside rate
# and the coupon threshold; both are the founder's to set.
#
# DOCTRINE: Sales and contributions are DIFFERENT KINDS and are
# never mixed in the ledger: a sale is a purchase of goods; a
# contribution is support toward completing the work and is NOT a
# tax-deductible donation — the receipt says so in plain words,
# every time, because the truth is printed or it is not printed.
# The tax set-aside is an INTERNAL PLANNING ESTIMATE — a jar on the
# shelf, not a tax document and not tax advice. Income is taxable
# whether or not any 1099-K ever arrives; the ledger is the record
# that outlives the payment app's paperwork either way.
# A thank-you coupon attached to a contribution is a GIFT from the
# seller, of no cash value; it changes nothing about the character
# of the contribution itself.
# =====================================================================

import argparse
import json
import secrets
import string
import subprocess
import sys
import tempfile
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

# ---------------------------------------------------------------------
# HOUSE CONSTANTS
# MECHANISM: The seller line is printed identically on every receipt;
#              the payment rail is the only rail the house receives on.
# DOCTRINE:    SPARROW is the founder's coined form — Sole
#              Proprietorship, All Rights Reserved — and it is the
#              legal shape of this till.
# ---------------------------------------------------------------------
SELLER_LINE = "Johnathan 'Qasparr' Monroe (SPARROW — Sole Proprietorship, ARR)"
PAYMENT_RAIL = "Cash App $axoneme"
DETROIT = ZoneInfo("America/Detroit")

# ---------------------------------------------------------------------
# DEFAULT CONFIGURATION
# MECHANISM: Written to config.json on first run; editable by the
#              founder through the `rate` command or by hand.
# DOCTRINE:  The default set-aside of 25% is a planning jar, sized
#              to cover self-employment tax (≈15.3%) with headroom
#              for income tax — an estimate, never a promise.
# ---------------------------------------------------------------------
DEFAULT_CONFIG = {
    "tax_rate": 0.25,          # fraction of each receipt swept to the jar
    "coupon_threshold": 10.00, # contribution at/above this earns a coupon
    "coupon_ebooks": 3,        # ebooks one coupon redeems
}

# Receipt-number prefixes, per kind. DOCTRINE: the two kinds carry
# different prefixes so a number alone tells the kind at a glance.
PREFIX = {"sale": "BOOK", "contribution": "CONTRIB"}

# ---------------------------------------------------------------------
# THE ARTIST-SPLIT CATALOG (added XXII day of November, 2026 e.v.,
# at the founder's order, the day D-BLOK's single took the shelf)
# MECHANISM: A small table of items whose sale price divides at the
#              door between the artist and the house. The key is the
#              item name as it is receipted — the Cash App note word,
#              matched stripped and uppercased, so the note the buyer
#              was told to write is the key the book looks up. A sale
#              whose item stands in this table carries an
#              "artist_split" record in its ledger row and prints
#              the division on its receipt; a sale whose item does
#              NOT stand here is a house sale, whole and unsplit,
#              and its receipt is unchanged in every line.
# DOCTRINE:  The split is the artist's standing in the till, ruled
#              by the founder: on a sale of the artist's own work
#              through the house store, 75% of the price is the
#              artist's and 25% is the house's. The division is
#              printed on the receipt itself — the buyer sees whose
#              work was bought and how the money divides — because
#              the truth is printed or it is not printed.
# ROUNDING:  The artist's share is rounded to the cent FIRST; the
#              house takes the remainder, so the two shares always
#              sum to the sale price to the cent. At the shelf price
#              of $2.50: D-BLOK $1.88, the house $0.62.
# THE ENVELOPE ON A SPLIT SALE (ruled XXII day of November, 2026
#              e.v.: the founder asked how the professionals figure
#              the tax set-aside on a split sale — on the whole or
#              on the house's share — and ruled "Do it how they do
#              it"): the professional method is that the artist's
#              share is a pass-through — money the house holds for
#              the artist and pays out, never the house's kept
#              income — so the tax set-aside is figured on the
#              HOUSE'S SHARE ONLY, never on the whole price. At the
#              shelf price: 25% of the house's $0.62 is $0.155,
#              rounded HALF-UP to the cent (see round_half_up_cents)
#              — $0.16 in the jar. On a house sale the envelope
#              rides on the whole receipt, as it always has.
# ---------------------------------------------------------------------
ARTIST_SPLITS = {
    "CONCRETE MAZE": {
        "artist": "D-BLOK",
        "artist_share": 0.75,
        "house_name": "Johnathan",
    },
}

# ---------------------------------------------------------------------
# THE SALE NOTIFICATION (added XXII day of November, 2026 e.v.,
# at the founder's order of the same day)
# MECHANISM: When a sale receipt is minted, the founder is told by
#              email: the item, the receipt number, the amount —
#              and, on a split SKU, the division's amounts. The send
#              rides the Gmail connector CLI, the one send path on
#              this box a script can invoke; it delivers when the
#              founder's Gmail stands connected here. The gate is a
#              config key — "sale_notifications" — that the default
#              config NEVER seeds: it is set by hand in the real
#              till's config.json alone, so the self-test's temp
#              house and every scratch ledger stay silent by
#              construction, and only a real mint in the real book
#              can ever notify. Every gated mint appends its attempt
#              to notifications.jsonl beside the ledger — SENT with
#              the mail path's answer, or FAILED with its error —
#              and reports the outcome on stderr; the receipt's own
#              text and the mint itself never wait on the mail.
# DOCTRINE:  The till tells its keeper. A sale the founder learns
#              of late is a book half-kept; the notification is the
#              doorbell on the same door the split happens at. And
#              an undelivered notification is never a silent one:
#              it stands in the outbox, marked FAILED, in the open.
# PRIVACY:   The email carries the item, the number, and the money
#              — never the buyer's name. Buyer names stay in the
#              house's local records, as the shop's law has always
#              held; the doorbell rings the sale, not the person.
# ---------------------------------------------------------------------
# The founder's own address, seated here at his order of
# XXII day of November, 2026 e.v. — sale notifications go to him.
NOTIFY_EMAIL = "sykosys93@gmail.com"
NOTIFY_CLI = ["/opt/hatch/bin/hatch_gws_cli", "gmail", "+send"]


def notification_text(row: dict):
    """Compose the sale notification: subject and body for a row.

    MECHANISM: Pure composition — no sending lives here, so the
    self-test can prove the text (split amounts and all) without
    the mail path ever being touched.
    """
    subject = (f"Bookshop sale — {row['item']} — "
               f"Receipt {row['receipt_no']}")
    lines = [
        "A sale was receipted at the bookshop till.",
        "",
        f"Item:    {row['item']}",
        f"Receipt: {row['receipt_no']}",
        f"Amount:  {money(row['amount'])}",
        f"Paid by: {PAYMENT_RAIL}",
    ]
    if row.get("artist_split"):
        sp = row["artist_split"]
        lines += [
            "",
            "Artist split:",
            f"  {sp['artist']}: {sp['artist_share']:.0%} of the "
            f"sale = {money(sp['artist_amount'])}",
            f"  {sp['house_name']}: {1 - sp['artist_share']:.0%} of "
            f"the sale = {money(sp['house_amount'])}",
        ]
    lines += ["", "93 — Live, Love, and let Love, Live."]
    return subject, "\n".join(lines)


def notify_sale(home: Path, cfg: dict, row: dict) -> bool:
    """Email the founder a sale, if this house is the real till.

    MECHANISM: The gate is double — the row must be a sale, and the
    house config must carry "sale_notifications": true, a key the
    default config never seeds (see the section head). Past the
    gate, the Gmail CLI is invoked once; the attempt and its
    outcome are appended to notifications.jsonl either way, and
    the outcome prints on stderr. Returns True only on a send the
    mail path accepted. A failed send never fails the mint.
    """
    if row["kind"] != "sale" or cfg.get("sale_notifications") is not True:
        return False
    subject, body = notification_text(row)
    entry = {
        "date": now_iso(),
        "receipt_no": row["receipt_no"],
        "to": NOTIFY_EMAIL,
        "subject": subject,
    }
    try:
        proc = subprocess.run(
            NOTIFY_CLI + ["--to", NOTIFY_EMAIL, "--subject", subject,
                          "--body", body],
            capture_output=True, text=True, timeout=120)
        entry["status"] = "SENT" if proc.returncode == 0 else "FAILED"
        entry["detail"] = (proc.stdout or proc.stderr).strip()[:300]
    except Exception as exc:  # the mail path is a courtesy, never a gate
        entry["status"] = "FAILED"
        entry["detail"] = f"{type(exc).__name__}: {exc}"[:300]
    with (home / "notifications.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[sale notification {entry['status']} -> {NOTIFY_EMAIL}]",
          file=sys.stderr)
    return entry["status"] == "SENT"


# =====================================================================
# DIRECTORY AND FILE PLUMBING
# MECHANISM: Every record lives beside this script (or beside the
#            directory handed to run() when the self-test drives it
#            against a temporary home — the real ledger is never
#            touched by tests).
# =====================================================================
def ensure_home(home: Path) -> dict:
    """Create the bookshop home if absent; load (or seed) config."""
    home.mkdir(parents=True, exist_ok=True)
    (home / "receipts").mkdir(exist_ok=True)
    cfg_path = home / "config.json"
    if not cfg_path.exists():
        cfg_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n",
                            encoding="utf-8")
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def load_ledger(home: Path) -> list:
    """Read every JSON line of the ledger; an absent ledger is empty."""
    path = home / "ledger.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def next_number(home: Path, kind: str) -> str:
    """Next receipt number for a kind: count that kind, add one.

    MECHANISM: Numbering is derived from the ledger itself, so the
    book can never issue the same number twice even if a receipt
    file is deleted — the ledger, not the folder, is the authority.
    """
    count = sum(1 for row in load_ledger(home) if row["kind"] == kind)
    return f"{PREFIX[kind]}-{count + 1:04d}"


def money(x: float) -> str:
    """Format a float as a plain dollars-and-cents string."""
    return f"${x:,.2f}"


def round_half_up_cents(x) -> float:
    """Round a dollar figure to the cent, halves rounding UP.

    MECHANISM: Decimal arithmetic on the decimal strings of the
    factors, so a true half-cent — the house's $0.62 × 25% =
    $0.155 — rounds up to $0.16, the way a till is figured by
    hand, where the binary float round() would banker's-round
    the half down. Used for the tax set-aside on a split sale
    (the ruling at the artist-split catalog); the standing
    house-receipt set-aside keeps its standing round().
    """
    cents = Decimal(str(x)).quantize(Decimal("0.01"),
                                      rounding=ROUND_HALF_UP)
    return float(cents)


def now_iso() -> str:
    """Current timestamp, ISO format, in the founder's timezone."""
    return datetime.now(DETROIT).isoformat(timespec="seconds")


# =====================================================================
# THE COUPON PRESS
# MECHANISM: A code is THANKS- plus six letters/digits drawn from a
#            CSPRNG; uniqueness is checked against coupons.txt.
# DOCTRINE:  The coupon is a thank-you GIFT — no cash value, one use —
#            and its issuance is recorded both in the ledger line of
#            the contribution and in coupons.txt, so a code can be
#            honored (or refused, if already redeemed) on sight.
# =====================================================================
def mint_coupon(home: Path, receipt_no: str) -> str:
    path = home / "coupons.txt"
    existing = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(line.split()[0])
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "THANKS-" + "".join(secrets.choice(alphabet) for _ in range(6))
        if code not in existing:
            break
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{code}  {receipt_no}  ISSUED\n")
    return code


# =====================================================================
# THE RECEIPT ITSELF
# MECHANISM: One function renders the receipt text; it is written to
#            receipts/<no>.txt AND printed to stdout, byte-identical,
#            so what the buyer is sent is what the book holds.
# DOCTRINE:  The set-aside line is labeled an internal planning
#            estimate ON THE RECEIPT — the buyer is never handed a
#            tax document, and the founder is never confused about
#            which paper is which. A contribution's receipt carries
#            the standing truth in plain words, without exception.
# =====================================================================
def render_receipt(row: dict, cfg: dict) -> str:
    lines = [
        "=" * 62,
        f"RECEIPT {row['receipt_no']}",
        "=" * 62,
        f"Date:    {row['date']}",
        f"Seller:  {SELLER_LINE}",
        f"Buyer:   {row['from']}",
        f"Item:    {row['item']}",
        f"Amount:  {money(row['amount'])}",
        f"Paid by: {PAYMENT_RAIL}",
    ]
    if row.get("note"):
        lines.append(f"Note:    {row['note']}")
    lines.append("-" * 62)
    # MECHANISM: on a split sale the set-aside was figured on the
    # house's share only (the ruling at the artist-split catalog),
    # and the line SAYS SO — its base is printed, so the paper
    # never lets a reader take the jar for a whole-price sweep.
    # On every other receipt the line stands exactly as it has
    # always stood, word for word and cent for cent.
    if row.get("artist_split"):
        lines.append(
            f"Tax set-aside (internal planning estimate, "
            f"{cfg['tax_rate']:.0%} of the house share): "
            f"{money(row['tax_set_aside'])}")
    else:
        lines.append(
            f"Tax set-aside (internal planning estimate, "
            f"{cfg['tax_rate']:.0%}): {money(row['tax_set_aside'])}")
    lines += [
        "  ^ The seller's own tax jar. This line is not a tax",
        "    document and gives the buyer no deduction.",
    ]
    # MECHANISM: the division prints only on a split sale's receipt —
    # the block exists in the row only when the catalog divided the
    # price, so every other receipt keeps its exact standing shape.
    # DOCTRINE:  the percentages AND the dollar amounts both print:
    # a share stated without its amount is a promise, not a division.
    if row.get("artist_split"):
        sp = row["artist_split"]
        lines += [
            "-" * 62,
            "Artist split — this sale divides at the door:",
            f"  {sp['artist']}: {sp['artist_share']:.0%} of the sale "
            f"= {money(sp['artist_amount'])}",
            f"  {sp['house_name']}: {1 - sp['artist_share']:.0%} of "
            f"the sale = {money(sp['house_amount'])}",
        ]
    if row["kind"] == "contribution":
        lines += [
            "-" * 62,
            "This is a contribution toward completing the work.",
            "It is NOT a tax-deductible donation.",
        ]
        if row.get("coupon"):
            lines += [
                "-" * 62,
                f"THANK-YOU COUPON: {row['coupon']}",
                f"Redeemable for any {cfg['coupon_ebooks']} ebooks from "
                f"the bookshop list.",
                "(thank-you gift · no cash value · one use)",
            ]
    lines += [
        "=" * 62,
        "93 — Live, Love, and let Love, Live.",
        "=" * 62,
        "",
    ]
    return "\n".join(lines)


def record_payment(home: Path, kind: str, item: str, buyer: str,
                   amount: float, note: str = "") -> dict:
    """Book one payment: split it, number it, ledger it, print it.

    MECHANISM: on a house receipt, set_aside = round(amount ×
    rate, 2); on a split receipt the envelope is figured on the
    house's share only, rounded half-up to the cent (the ruling
    at the artist-split catalog). The net is the remainder, so
    set-aside + net always sums to the amount to the cent.
    DOCTRINE:  The split happens AT THE DOOR, on every receipt —
    the jar is filled before the money can be spent, not after.
    """
    cfg = ensure_home(home)
    receipt_no = next_number(home, kind)
    # MECHANISM: the artist-split catalog is consulted FIRST, at
    # the door, because the tax jar's base depends on its answer.
    # The artist's share is rounded to the cent first and the
    # house takes the remainder (see ROUNDING at the catalog), so
    # the two shares always sum to the amount. On a split sale
    # the set-aside is then figured on the HOUSE'S SHARE ONLY —
    # the artist's share is a pass-through, never the house's
    # kept income (the founder's ruling of XXII Nov 2026: the
    # professional method) — and rounded half-up to the cent.
    # On a house sale the jar sweeps the whole receipt, as it
    # always has.
    # DOCTRINE:  the division is booked in the ledger row itself,
    # so the book can always answer, for any split sale, exactly
    # what the artist is owed — the memory is in the book, not
    # in a head.
    split = ARTIST_SPLITS.get(item.strip().upper())
    artist_split = None
    if split is not None:
        artist_amount = round(amount * split["artist_share"], 2)
        artist_split = {
            "artist": split["artist"],
            "artist_share": split["artist_share"],
            "artist_amount": artist_amount,
            "house_name": split["house_name"],
            "house_amount": round(amount - artist_amount, 2),
        }
        set_aside = round_half_up_cents(
            Decimal(str(artist_split["house_amount"]))
            * Decimal(str(cfg["tax_rate"])))
    else:
        set_aside = round(amount * cfg["tax_rate"], 2)
    row = {
        "date": now_iso(),
        "kind": kind,
        "receipt_no": receipt_no,
        "item": item,
        "from": buyer,
        "amount": round(amount, 2),
        "tax_set_aside": set_aside,
        "net_spendable": round(amount - set_aside, 2),
        "note": note,
    }
    # The division computed above rides in the row, beside the
    # jar's figures and independent of them: the artist split
    # divides the PRICE, the jar sweeps its ruled base, and the
    # receipt prints both.
    if artist_split is not None:
        row["artist_split"] = artist_split
    # DOCTRINE: a coupon rides only on a contribution, and only at or
    # above the threshold — generosity has a stated gate, kept alike
    # for every giver, so no giver is promised what another was not.
    if kind == "contribution" and amount >= cfg["coupon_threshold"]:
        row["coupon"] = mint_coupon(home, receipt_no)
    with (home / "ledger.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    text = render_receipt(row, cfg)
    (home / "receipts" / f"{receipt_no}.txt").write_text(text,
                                                         encoding="utf-8")
    print(text, end="")
    # The doorbell rings only after the mint stands complete —
    # ledger, receipt file, and print — and only in the real till:
    # notify_sale's own gate keeps test and scratch houses silent.
    notify_sale(home, cfg, row)
    return row


# =====================================================================
# THE BALANCE — READING THE BOOK BACK
# MECHANISM: Totals are recomputed from the ledger on every call;
#            nothing is cached, so the report can never drift from
#            the book. The tax envelope is the sum of every set-aside
#            ever swept — the amount standing reserved for taxes.
# =====================================================================
def report_balance(home: Path) -> None:
    ensure_home(home)
    rows = load_ledger(home)
    print("=" * 62)
    print("BOOKSHOP BALANCE")
    print("=" * 62)
    total_env = 0.0
    total_net = 0.0
    for kind in ("sale", "contribution"):
        sub = [r for r in rows if r["kind"] == kind]
        gross = sum(r["amount"] for r in sub)
        env = sum(r["tax_set_aside"] for r in sub)
        total_env += env
        total_net += sum(r["net_spendable"] for r in sub)
        print(f"{kind.capitalize() + 's':14s} count {len(sub):4d}   "
              f"gross {money(gross):>12s}   to jar {money(env):>10s}")
    print("-" * 62)
    print(f"{'TOTAL GROSS':14s} {money(total_env + total_net):>18s}")
    print(f"{'TAX ENVELOPE':14s} {money(total_env):>18s}   "
          f"(reserved for taxes)")
    print(f"{'SPENDABLE':14s} {money(total_net):>18s}")
    print("=" * 62)


# =====================================================================
# THE SELF-TEST — THE TOOL PROVES ITSELF IN A TEMPORARY HOUSE
# MECHANISM: run() takes a home directory; the test passes a temp
#            dir, so the real ledger is never seeded with test data.
# DOCTRINE:  A tool that keeps the money book must prove its sums
#            before it is trusted with a single real payment:
#            numbering increments per kind; every split sums to its
#            amount; coupons issue only at/above the threshold; the
#            balance reconciles against the ledger to the cent.
# =====================================================================
def selftest() -> int:
    results = []

    def check(name, ok):
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {name}")

    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        import io, contextlib
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink):
            s1 = record_payment(home, "sale", "TEST BOOK A", "Ann", 9.00)
            s2 = record_payment(home, "sale", "TEST BOOK B", "Bob", 12.00)
            c1 = record_payment(home, "contribution", "Support", "Cy", 9.99)
            c2 = record_payment(home, "contribution", "Support", "Dee", 10.00)
        check("sale numbering increments (BOOK-0001, BOOK-0002)",
              (s1["receipt_no"], s2["receipt_no"]) == ("BOOK-0001", "BOOK-0002"))
        check("contribution numbering is its own series (CONTRIB-0001…)",
              (c1["receipt_no"], c2["receipt_no"]) ==
              ("CONTRIB-0001", "CONTRIB-0002"))
        rows = load_ledger(home)
        check("every split sums to its amount",
              all(abs(r["tax_set_aside"] + r["net_spendable"]
                      - r["amount"]) < 0.005 for r in rows))
        check("default rate sweeps 25% ($9.00 sale sets aside $2.25)",
              s1["tax_set_aside"] == 2.25)
        check("no coupon below the $10 threshold ($9.99 contribution)",
              "coupon" not in c1)
        check("coupon issues at the threshold ($10.00 contribution)",
              c2.get("coupon", "").startswith("THANKS-"))
        check("coupon recorded in coupons.txt as ISSUED",
              c2["coupon"] in (home / "coupons.txt").read_text())
        check("receipt files written for every payment",
              all((home / "receipts" / f"{r['receipt_no']}.txt").exists()
                  for r in rows))
        gross = sum(r["amount"] for r in rows)
        env = sum(r["tax_set_aside"] for r in rows)
        net = sum(r["net_spendable"] for r in rows)
        check("balance reconciles (gross = envelope + spendable)",
              abs(gross - (env + net)) < 0.005 and len(rows) == 4)
        # The artist split proves itself in the same temp house: a
        # catalog sale divides 75/25 with shares summing to the
        # price; a house sale carries no split and prints none.
        cfg = ensure_home(home)
        with contextlib.redirect_stdout(sink):
            sp = record_payment(home, "sale", "CONCRETE MAZE", "Eve",
                                2.50)
        spt = sp.get("artist_split", {})
        check("split SKU divides at the shelf price ($1.88 / $0.62)",
              spt.get("artist") == "D-BLOK"
              and spt.get("artist_amount") == 1.88
              and spt.get("house_amount") == 0.62)
        check("split shares sum to the sale price",
              abs(spt.get("artist_amount", 0)
                  + spt.get("house_amount", 0) - sp["amount"]) < 0.005)
        # The envelope on a split sale rides on the house's share
        # only (the founder's ruling: the professional method) —
        # 25% of $0.62 is $0.155, rounded half-up to $0.16, where
        # a whole-price sweep would have taken $0.62.
        check("split set-aside rides on the house share only ($0.16)",
              sp["tax_set_aside"] == 0.16)
        check("house sale carries no artist split",
              "artist_split" not in s1)
        sp_text = render_receipt(sp, cfg)
        check("the division prints on the split receipt",
              "Artist split" in sp_text and "D-BLOK" in sp_text
              and "$1.88" in sp_text and "$0.62" in sp_text)
        check("split set-aside line names its base and its amount",
              "Tax set-aside (internal planning estimate, 25% of "
              "the house share): $0.16" in sp_text)
        check("no split prints on a house receipt",
              "Artist split" not in render_receipt(s1, cfg))
        check("house set-aside line unchanged in word and cent",
              "Tax set-aside (internal planning estimate, 25%): "
              "$2.25" in render_receipt(s1, cfg))
        # The sale notification proves its text and its gate in the
        # same temp house: the split figures ride the body, a house
        # sale's body carries none, and the gate — the real till's
        # config key, never seeded here — stays shut, so no send is
        # attempted and no outbox is written.
        n_subject, n_body = notification_text(sp)
        check("notification names item, receipt and amount",
              "CONCRETE MAZE" in n_subject
              and sp["receipt_no"] in n_subject and "$2.50" in n_body)
        check("notification carries the split amounts",
              "D-BLOK" in n_body and "$1.88" in n_body
              and "$0.62" in n_body)
        check("house notification carries no split",
              "Artist split" not in notification_text(s1)[1]
              and "$9.00" in notification_text(s1)[1])
        check("notification gate stays shut in a test house",
              notify_sale(home, cfg, sp) is False
              and not (home / "notifications.jsonl").exists())
    print("-" * 62)
    print(f"SELFTEST: {'ALL PASS' if all(results) else 'FAILURES PRESENT'} "
          f"({sum(results)}/{len(results)})")
    return 0 if all(results) else 1


# =====================================================================
# THE COMMAND TABLE
# MECHANISM: argparse subcommands — sale, contribution, balance,
#            rate, selftest. `rate` with no --set only reports.
# =====================================================================
def run(argv=None, home=None) -> int:
    home = home or Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(
        prog="receipt.py",
        description="The bookshop receipt book and tax jar.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sale", help="receipt a book sale")
    p.add_argument("--item", required=True)
    p.add_argument("--amount", required=True, type=float)
    p.add_argument("--from", required=True, dest="buyer")
    p.add_argument("--note", default="")

    p = sub.add_parser("contribution", help="receipt a contribution")
    p.add_argument("--amount", required=True, type=float)
    p.add_argument("--from", required=True, dest="buyer")
    p.add_argument("--item", default="Contribution")
    p.add_argument("--note", default="")

    sub.add_parser("balance", help="print ledger totals")

    p = sub.add_parser("rate", help="view or set the tax set-aside rate")
    p.add_argument("--set", type=float, default=None, dest="new_rate")

    sub.add_parser("selftest", help="prove the tool in a temp directory")

    args = ap.parse_args(argv)
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "balance":
        report_balance(home)
        return 0
    if args.cmd == "rate":
        cfg = ensure_home(home)
        if args.new_rate is not None:
            if not 0.0 <= args.new_rate <= 1.0:
                print("Rate must be between 0 and 1.", file=sys.stderr)
                return 2
            cfg["tax_rate"] = args.new_rate
            (home / "config.json").write_text(
                json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        print(f"Tax set-aside rate: {cfg['tax_rate']:.0%} "
              f"of every receipt, swept to the tax envelope.")
        return 0
    record_payment(home, args.cmd, args.item, args.buyer,
                   args.amount, args.note)
    return 0


if __name__ == "__main__":
    sys.exit(run())

# =====================================================================
# 93 — Live, Love, and let Love, Live.
# =====================================================================
