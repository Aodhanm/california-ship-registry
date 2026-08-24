# Provenance and reproducibility

*How `data/visits.csv` and `data/ships.csv` were built, and what "reproducible"
means for a curated historical dataset. Last updated 2026-08-24.*

## The dataset is curated, not generated

`visits.csv` is **not** the output of a single script you can re-run. It is a
curated register. Trying to regenerate it from one command would defeat its
purpose: the value is in the thousands of individual adjudications (this name is a
real hull, that one is a place; these two records are one visit, those are two;
this flag is wrong), and each of those is a judgement recorded against a source,
not a rule a parser could re-derive. Over-merging is silent data loss; the register
errs toward keeping rows separate and letting a reviewer combine them.

This is the same model as SlaveVoyages and other source-critical registers: the
authoritative object is the reviewed table plus its per-row citations, and
reproducibility means **any row can be re-checked against the source it cites**,
not that a script re-emits the table.

## Build lineage

1. **Phase 0 — seed.** `scripts/harvest.py` swept the *Archives of California*
   calendar (BANC MSS C-A) for vessel vocabulary; `scripts/merge.py` collapsed the
   draft rows into visit-level rows, a ships table, and the anchorage gazetteer
   (~1,294 draft visits). This is the ONLY step `merge.py` performs, and it reads
   `data/visits-draft.csv`, which lives in the vault working copy, not here.
   `merge.py` is now gated so it cannot overwrite the curated file (see below).

2. **Source-family folds** (each documented in `REVIEW-QUEUE.md` and
   `FALSE-POSITIVE-REGISTER.md`, dates in the git log): the Bancroft *History of
   California* roster sweep (7 vols); Ogden's 1941 otter-trade appendix; a Russian
   attestation layer (with 98 stated absences); the C-A 40 and C-A 30 customs
   ledgers (leaf-verified); Bancroft's consolidated Mexican-period vessel lists; a
   calendar re-harvest at 19,755 records; and hand-curated exploration/Vallejo rows.
   Manuscript-derived names are leaf-verified before minting (the C-A 40 lesson).

3. **Phantom purges — the seven false-ship classes.** Policy phantoms,
   era-conflations, person-as-ship, place-as-ship, OCR garbles, mis-flaggings, and
   retrospective mentions are detected and removed, each with its test and guard
   (`PHANTOM-SHIPS.md`, `FALSE-POSITIVE-REGISTER.md`). Sunk phantoms and non-ship
   C-A records are hard-guarded in `check.py` (`DROPPED_SHIP_IDS`,
   `DROPPED_CA_RECORDS`) so a re-harvest can never re-mint them.

4. **Per-visit review** to the `draft → reviewed → verified` tiers, with all
   "firsts", all starred records, and a seeded >=10% sample checked against the
   cited leaf (`verification-log.csv`, `AUDIT-2026-07-18.md`, `EXCERPT-AUDIT.md`).

Individual curation passes are kept as dated, auditable scripts, e.g.
`scripts/apply_flag_fixes_2026-08-24.py` (the post-1821 flag-artifact correction),
so every batch change is a readable record of what changed and why.

## The reproducible guarantee: `check.py`

`python3 scripts/check.py` is the reproducible contract. It re-derives and enforces,
on every build, that the published table satisfies its invariants:

- schema/vocabulary conformance (flags, visit types, statuses);
- every row carries at least one parseable citation;
- date sanity and `date_from <= date_to`;
- **flag floors** — no flag predates its nation's first documented California hull;
- **the post-1821 Spain ceiling** — no port-level `spain` flag after independence,
  bar an explicit allowlist for the genuine last Spanish-naval visit (the *Asia*);
- sunk phantoms and adjudicated non-ship records can never reappear;
- the Ogden schedule-attachment year-consistency guard (the *Loo Choo* lesson).

A green `check.py` (HARD 0) is the machine-checkable statement that the dataset is
internally consistent with its own documented rules. It is what a reader runs to
trust the file, and what a contributor must keep green.

## The citable unit

The DOI is minted against a **tagged git snapshot** archived on Zenodo. That frozen
snapshot, not any local rebuild, is the reproducible, citable object. Zenodo's
version DOIs let later curation ship as new versions without disturbing an existing
citation.

## Extending the register

Stage new rows in a source-family CSV (never edit `visits.csv` by a bulk parser);
leaf-verify manuscript-derived vessel names at scale 2–3 before minting; apply via a
dated script; then re-run `check.py` and walk the seven false-ship classes
(`FALSE-POSITIVE-REGISTER.md`). Only then fold into `visits.csv`.
