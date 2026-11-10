# THE BOOKSHOP RECEIPT BOOK AND TAX JAR

*For Johnathan 'Qasparr' Monroe (SPARROW — Sole Proprietorship, ARR).
One tool: `receipt.py`, in this folder. It needs nothing but Python 3.*

## When a payment lands on Cash App ($axoneme)

Run ONE command. Pick sale or contribution — they are different
kinds of money and the book never mixes them.

**A book sale:**
```
python3 receipt.py sale --item "THE NINE VOWELS (MAGVS PDF)" --amount 9.00 --from "Buyer Name"
```
Add `--note "whatever they wrote in the Cash App note"` when you
want their note kept with the record.

**A contribution:**
```
python3 receipt.py contribution --amount 25.00 --from "Their Name"
```
(Use `--item "Bleats contribution"` if it was for a project.)

The tool prints the receipt, saves it to `receipts/`, and adds one
line to the book (`ledger.jsonl`). Receipt numbers run on their own
tracks: sales are BOOK-0001, BOOK-0002…; contributions are
CONTRIB-0001, CONTRIB-0002…

**See where you stand, any time:**
```
python3 receipt.py balance
```
**Change the tax set-aside rate (default 25%):**
```
python3 receipt.py rate            # just shows the rate
python3 receipt.py rate --set 0.30 # set it to 30%
```

## The tax jar — how it works, in plain words

Every receipt is split at the door: a percentage (25% unless you
change it) is marked as set aside in the **tax envelope**, and the
rest is spendable. The envelope number in `balance` is the amount
standing reserved for taxes. When tax time comes, that is the pile
the taxes get paid from.

**The envelope is a planning estimate, not tax advice.** The
25% default is sized to cover self-employment tax (about 15.3%)
with headroom left for income tax. Your real tax bill is figured at
filing time from your real numbers — the jar just makes sure the
money is still there when the bill arrives.

**Income is taxable whether or not any 1099-K ever shows up.**
Payment apps only have to send a 1099-K above a federal dollar
threshold; below it, no form arrives — and the income is still
income. That is why this ledger exists: `ledger.jsonl` is your own
record of every payment, and it is what a Schedule C gets built
from at tax time. Keep it; it outlives the app's paperwork.

**Quarterly estimated payments exist.** If the jar grows into real
money over a year, the IRS expects estimated tax paid in four
installments during the year rather than all at filing. The balance
command's envelope total is the number to watch; a tax preparer or
the IRS's own estimated-tax worksheet turns it into amounts and
dates when the sums justify it.

## Sales and contributions are not the same money

- A **sale** is a purchase. The buyer bought a book.
- A **contribution** is support toward completing the work. It is
  **NOT a tax-deductible donation** — there is no charity here to
  deduct against — and every contribution receipt says so in plain
  words, so no giver is ever misled.
- Both kinds are taxable income to the seller. Both go in the same
  ledger, under their own kind, and are never merged.

## Thank-you coupons

A contribution of **$10 or more** earns the giver a coupon code
(THANKS-XXXXXX) printed on their receipt: a thank-you gift,
redeemable for any **3 ebooks** from the bookshop list, no cash
value, one use. Codes are kept in `coupons.txt` with the receipt
that issued them, marked ISSUED (cross a code out to REDEEMED when
it is used). A coupon is a gift from the seller. It does **not**
turn a contribution into a purchase, and it does not change what
the contribution is: support, not a deductible donation.

## Prove the tool before trusting it

```
python3 receipt.py selftest
```
Runs the whole flow in a throwaway folder — never touching the real
ledger — and checks the numbering, the splits, the coupon gate, and
that the totals reconcile. It should print ALL PASS.

---

93 — Live, Love, and let Love, Live.
