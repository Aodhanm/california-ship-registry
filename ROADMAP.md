# Roadmap — toward a polished, academic, complete registry

*Where it stands (2026-07-28): 391 ships / 2,108 visits, **100% `reviewed`** (every ship corroborated against a reliable source), 5 marquee firsts `verified` at the manuscript leaf. Sources ingested: the Archives of California calendar (BANC MSS C-A), Bancroft's *History of California* (all 7 vols), and Adele Ogden's *California Sea Otter Trade* (1941) incl. her vessel appendix. Documentation: CODEBOOK, METHOD, PHANTOM-SHIPS, FALSE-POSITIVE-REGISTER, FIRSTS, OGDEN-RECONCILIATION, REVIEW-QUEUE, CITATION.cff + .zenodo.json + LICENSE (DOI staged). Cleanup is done; what remains is **verification depth, completeness, and publication.***

Legend: **[A]** = needs Aodhan (login/decision/prose) · **[C]** = Claude can execute · effort S/M/L.

---

## Phase 1 — Lock in the milestone: publish v0.2 + DOI  *(the payoff)*
The dataset is citable-ready; minting the DOI is what makes all the cleanup *count* (and it's portfolio-relevant for the Fall 2027 apps — dataset-as-publication, per the C-A precedent).
1. **[A]** Zenodo login → flip the GitHub↔Zenodo toggle for the repo (one-time). *(S)*
2. **[A]** Pick the version (suggest **v0.2.0** — the corroborated/reviewed dataset). *(S)*
3. **[C]** Cut `git tag v0.2.0` + `gh release create` → Zenodo auto-mints the DOI from `.zenodo.json`. *(S)*
4. **[C]** Backfill the DOI into `CITATION.cff`, README, site footer, and the umbrella site. *(S)*

## Phase 2 — Verification depth: the `verified` tier  *(what a referee will test)*
Right now 5 records are leaf-`verified`. To be defensible, define and hit a **stated verification standard**, not ad-hoc.
1. **[C]** Write a **verification protocol** into CODEBOOK: what must be leaf-checked before `verified` — (a) every FIRSTS claim, (b) every ⭐-flagged record, (c) a documented **random sample** (e.g. 8–10% of visits, seeded RNG, logged). *(M)*
2. **[C]** Execute it — the BookReader-JPEG leaf-read method is proven and repeatable. Log each in a `verification-log.csv`. *(L, incremental)*
3. **[C]** Publish a **coverage statement**: "X% of visits leaf-verified; all firsts verified." Peer reviewers want this number. *(S)*
4. **[C]** Resolve the standing identity splits at the leaf: `morelos` (1825 brig vs 1834 corvette), and re-check any remaining multi-decade/multi-flag clusters (Class 2). *(M)*

## Phase 3 — Completeness: ingest the remaining sources  *(fill the gaps)*
Named in the CODEBOOK roadmap; several are already on disk.
1. **[C]** **Archer 1973** (*already in the vault*, OCR'd) — Spanish NW-coast naval & San Blas activity; corroborate/add the exploration and supply vessels. *(M)*
2. **[C]** **The Russian record** — Gibson & Istomin, *Russian California* (Hakluyt, index compiled in vault) + Khlebnikov dispatches + the Fort Ross RAC library (both in vault). Adds/corroborates the RAC layer; would firm the Russian-vessel identities. *(L)*
3. **[A→C]** **Howay, "A List of Trading Vessels in the Maritime Fur Trade"** (BC Historical Quarterly, on archive.org — **needs obtaining**). Ogden herself builds on Howay; it's the authoritative NW-coast cross-check and the natural completeness partner. *(L)*
4. **[C]** **Fill the Spanish-period flag gaps** — the San Blas supply ships (1769–1824) that continued under Mexico after 1822 aren't all flag-confirmed; back-fill flags from Bancroft/C-A. *(M)*
5. **[A]** **Scope decisions** *(need a ruling)*: (a) extend to **1846–1848** conquest/gold-eve shipping? (b) **Baja California** — currently Alta-complete only; promote Baja from partial to in-scope, or state it as an explicit boundary. *(S decision, M/L execution)*

## Phase 4 — Scholarly apparatus & analysis  *(polish)*
1. **[C]** **Finish FIRSTS** — adjudicate every remaining claim; add "first vessel at each port," first of each rig, etc. *(M)*
2. **[C]** **Traffic analysis** — vessels/year and by flag; quantify the Spanish→Mexican→American shift and the fur-trade→hide-and-tallow transition. A figure or two for the data paper. *(M)*
3. **[C]** **Gazetteer completion** — coordinates for every anchorage so the map is complete; align place-names with the C-A calendar's gazetteer. *(M)*
4. **[C]** **Cross-dataset linkage** — deep-link visits to the C-A calendar records (partly done), to the maps site, and — where a master/supercargo is a person — toward the ECPP/person-layer bridge. *(M)*
5. **[C]** **Adopt a data standard** — a Frictionless `datapackage.json` (typed schema) + stable per-row IDs, so the CSVs are self-describing and tooling-friendly. *(S)*

## Phase 5 — The data paper  *(the academic output)*
1. **[A]** Choose venue — **Journal of Open Humanities Data** (JOHD) is the natural fit (short data paper + the DOI'd dataset); verify current scope/limits. *(S)*
2. **[C]** **Structure + assemble** the paper (Aodhan writes the prose — per our norm): context/motivation · **methods** (⭐ the seven-class phantom taxonomy — "a dataset's credibility lives in its refusals" — is the novel methodological contribution) · data description · completeness & limitations · reuse potential. Most of this text already exists across the repo docs; Claude organizes, Aodhan voices. *(M)*
3. **[A]** Draft the prose, submit. *(L, Aodhan's timing)*

---

## Sequencing (recommended)
**Now:** Phase 1 (DOI) — cheap, high-symbolic-value, unblocks citation. → **Then** Phase 2 protocol + a first verification batch (makes it referee-defensible). → **Then** Phase 3 Archer + Russian ingests (the biggest completeness gains, and both are on disk). → Phase 4/5 in parallel as the data paper takes shape.

**One-liner:** *cleanup is done; the arc from here is **verify deeper → grow with the on-disk sources → publish the dataset + a methods-forward data paper.***
