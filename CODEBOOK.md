# California Ship Registry, 1769–1846 — Codebook (v0.1 draft)

*The codebook is part of the dataset. Every field and vocabulary below is normative; changes are versioned.*

## Unit of observation
A **visit**: one vessel at one anchorage (or in one documented offshore event) at one time, as evidenced by one or more sources. A vessel has many visits; a visit may carry many citations.

## visits.csv
| field | meaning |
|---|---|
| visit_id | stable citable ID (`v0001`…), assigned chronologically at v0.1; never reused |
| ship_id | key into ships.csv; `(unnamed vessel)` = a documented ship event whose vessel the source does not name |
| name_as_written | the vessel's name(s) exactly as the source writes them (Savage's spellings preserved: 'Lelia Bird', 'Sowaroff') |
| date_from / date_to | ISO date or bare year; the span of the evidencing records, NOT verified arrival/departure dates until status=verified |
| date_confidence | exact / year / inferred / mixed (constituents disagree) |
| anchorage | canonical name from gazetteer.csv; empty = not yet located |
| region | alta / baja / alta-baja? — the completeness claim covers ALTA only (Baja incidental after the 1804 split) |
| flag | best-evidence national flag (spain, usa, russia, britain, mexico, france, hawaii, chile, peru, ecuador) |
| flag_basis | **how the flag is known**: `stated` = the evidencing record says it ("fragata americana") · `attested/inferred` = filled from the hand table in merge.py (SHIP_FLAGS) — vessels whose nationality is beyond doubt from standard authorities (Bancroft, Ogden 1941, Thurman 1967) or from context (the San Blas royal fleet, expedition vessels). Marked † in the viewer. Ambiguous names (e.g. two Columbias) are deliberately NOT filled |
| purpose | supply · exploration · otter · contraband · whaler · warship · (hide-tallow, missionary reserved) |
| outcome | arrived · departed · seized · wrecked · refused · deserters · traded |
| visit_type | port-call / offshore-presence / resident / sighting / unlocated (draft) |
| n_records | number of C-A records merged into this row |
| citations | JSON array; types: ca-record (C-A volume+doc+scan+IA url) · hoc (Bancroft vol:page) · ogden (page) · russian · other |
| sources_disagree | stated conflicts between sources (dates, names, facts) — disagreement is data |
| status | draft (machine-seeded, unreviewed) → reviewed → verified (checked at the source page/leaf) |

## ships.csv
ship_id · name_variants (with counts) · flag_guess · first_seen/last_seen (year) · n_visits · status.
Known identity notes: TWO Junos (juno-1767 = the Cádiz transport of the Catalan Volunteers; juno-rac = the Russian-American Company ship, 1806); 'william shaler' re-identified as **lelia byrd** (the record names her master as the vessel, C-A 12 doc 73); 'ilmen[?]' = the bracketed '[Erminia?]' rendering, unconfirmed against Russian sources.

## gazetteer.csv
Canonical anchorages with name variants and coordinates. Published as its own table; grows as visits are located.

## Provenance & limits (v0.1)
Seeded entirely from the *Archives of California* calendar (leaf-verified catalog of the Savage transcripts, archivesofcalifornia.com) by a documented harvester (scripts/harvest.py + merge.py). **Every row is status=draft.** Pending source families, in order: Bancroft HoC narrative 1769–1824 → Ogden 1941 appendix + Archer 1973 → the Russian record (Gibson–Istomin, Khlebnikov, Tikhmenev, Ivashintsov) → Howay/Cook cross-checks. Absence of a row ≠ absence of a ship: contraband is under-recorded by design — that asymmetry is a finding, not a flaw.
