# California Ship Registry, 1769–1846

*(Title span reflects the data: no post-1846 rows yet; extends to 1848 when the conquest/gold-eve shipping lands in Phase 2.)*

**v0.1 — LIVE DRAFT: https://ships.archivesofcalifornia.com/** The first machine-readable registry of documented vessel visits to the Californias, from the founding of Alta California to the eve of the gold rush. Companion to the [*Archives of California*](https://archivesofcalifornia.com) calendar of the Savage transcripts.

- **Unit of record:** the *visit* — one vessel, one anchorage, one time — each row carrying its evidence (manuscript-leaf citations with scan links).
- **Open `index.html` locally** to use the tool (visits table · ship index · map · traffic curve). Regenerate after data edits: `python3 scripts/build_site.py`.
- **Data:** `data/visits.csv` · `data/ships.csv` · `data/gazetteer.csv`. Vocabularies + field definitions: `CODEBOOK.md` (normative, versioned).
- **v0.1 provenance:** seeded from the calendar alone (scripts/harvest.py + merge.py); every row `status=draft`. Pending source families: Bancroft HoC narrative → Ogden 1941 + Archer 1973 → the Russian record → Howay/Cook. Completeness claimed for Alta California only.
- Public as a working draft since v0.1.6 (banner marks status); essays + core sources land by v1.0. DOI on publication.

Author: Aodhan (ORCID 0009-0002-8630-3768). Built with Claude-assisted extraction; method statement in the site's About pane.

- Data quality: see `FALSE-POSITIVE-REGISTER.md` (7 fake-ship classes + guards) and `REVIEW-QUEUE.md`.
