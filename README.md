# California Ship Registry, 1769–1846

*(Title span reflects the data: no post-1846 rows yet; extends to 1848 when the conquest/gold-eve shipping lands in Phase 2.)*

**v0.2.0, LIVE DRAFT: https://ships.archivesofcalifornia.com/** The first machine-readable registry of documented vessel visits to the Californias, from the founding of Alta California to the eve of the gold rush. Companion to the [*Archives of California*](https://archivesofcalifornia.com) calendar of the Savage transcripts.

- **Unit of record:** the *visit*, one vessel, one anchorage, one time, each row carrying its evidence (manuscript-leaf citations with scan links).
- **Open `index.html` locally** to use the tool (visits table · ship index · map · traffic curve). Regenerate after data edits: `python3 scripts/build_site.py`.
- **Data:** `data/visits.csv` · `data/ships.csv` · `data/gazetteer.csv`. Vocabularies + field definitions: `CODEBOOK.md` (normative, versioned).
- **Provenance:** seeded from the calendar (scripts/harvest.py + merge.py), then corroborated (2026-07) against Bancroft's *History of California* (all 7 vols) and Adele Ogden's *California Sea Otter Trade* (1941, incl. her vessel appendix). A roster-wide audit checked every ship against a reliable source. **401 ships / 2,072 visits; every ship (100%) is source-corroborated (`reviewed` at ship level)** against a C-A manuscript, Bancroft, or Ogden. Individual visit rows stay `status=draft` until leaf-verified (the `verified` tier below), so most visits are draft-tier by design. Remaining source families: Archer 1973 → the Russian record (Khlebnikov, Tikhmenev) → Howay/Cook. Completeness claimed for Alta California only. See `ROADMAP.md`.
- **Verification (`verified` tier):** launched 2026-07-28 with a documented protocol (`CODEBOOK.md`) and log (`data/verification-log.csv`). Each `verified` visit is checked against the manuscript page scan. **Coverage: 15 visits leaf-verified**, all 6 leaf-checkable FIRSTS + two batches (⭐-records: Favorita, Santiago, Concepción, Activo, Volunteer, Jorge Henríquez, Fama, morelos-corvette; 2 excerpt-mismatches caught & corrected), toward a target of ≥10% of named, scan-linked visits (~103).
- **DOI-ready:** `CITATION.cff` + `.zenodo.json` are staged; see `RELEASE-CHECKLIST.md` for the one-time Zenodo↔GitHub step. Essays + a data paper land by v1.0.

Author: Aodhan (ORCID 0009-0002-8630-3768). Built with Claude-assisted extraction; method statement in the site's About pane.

- Data quality: see `FALSE-POSITIVE-REGISTER.md` (7 fake-ship classes + guards) and `REVIEW-QUEUE.md`.

**More:** [Method statement](METHOD.md) · [Phantom Ships, the vessels that never were](PHANTOM-SHIPS.md) · [Firsts (draft)](FIRSTS.md) · [Codebook](CODEBOOK.md) · [Review queue](REVIEW-QUEUE.md)
