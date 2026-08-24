# Data paper, scaffold (for the *Journal of Open Humanities Data*)

*Structure and source-pointers only. **Prose is Aodhan's**, each section lists the argument beats and which repo docs supply the material; write from those, don't lift them verbatim. JOHD "data paper" template followed (short: ~1,000–2,000 words + tables). Target once the dataset has a DOI (Phase 1).*

---

## Title (draft options, Aodhan picks)
- "The California Ship Registry, 1769–1846: A Documentary Register of Vessel Visits to the Californias"
- alt framing foregrounding the method: "Publishing a Dataset's Refusals: The California Ship Registry, 1769–1846"

## Abstract *(150–200 words, Aodhan writes)*
Beats to hit: what it is (first machine-readable registry of documented vessel visits to Alta California, founding→gold rush) · unit = the visit, each with manuscript-leaf citations + scan links · sources (C-A calendar → Bancroft → Ogden) · size (401 ships / 2,072 visits, 100% source-reviewed) · the distinctive contribution (the phantom taxonomy; the dataset publishes its refusals) · the empirical payoff (the four-empire traffic shift). Source: README + TRAFFIC.md.

## (1) Context / Overview *(Aodhan writes)*
- **The gap:** no machine-readable register of pre-1846 California shipping exists; the maritime record is scattered across the destroyed C-A originals (Savage transcripts), Bancroft, Ogden, Howay, the Russian archives. Source: lit context in METHOD.md + the historiography.
- **Relation to the parent project:** companion to the *Archives of California* calendar (BANC MSS C-A; DOI 10.5281/zenodo.21327098), this registry is a derived, purpose-built layer. Source: CITATION.cff `isDerivedFrom`.
- **Why it matters:** quantifies the imperial/commercial transformation of the coast (Spanish supply monopoly → American otter smuggling → Russian frontier → American hide-trade dominance). Source: TRAFFIC.md.

## (2) Method *(the intellectual core, Aodhan writes; this is the novel bit)*
- **Seeding:** documented harvester (`scripts/harvest.py` + `merge.py`) over the C-A calendar; the visit as unit; both page-number systems; leaf-deep citations. Source: METHOD.md, CODEBOOK.md.
- **Corroboration:** roster-wide audit against Bancroft (all 7 vols) + Ogden (1941 appendix); every ship traced to a reliable source. Source: OGDEN-RECONCILIATION.md, the corroboration audit in FALSE-POSITIVE-REGISTER.md.
- **⭐ The phantom taxonomy, the methodological contribution.** "A dataset's credibility lives in its refusals." The seven false-ship classes (policy phantom, era-conflation, person-as-ship, place-as-ship, OCR garble, mis-flagging, retrospective mention), each with its detection test and guard. This is what distinguishes the dataset from a naive name-scrape and is the paper's citable idea. Source: PHANTOM-SHIPS.md + FALSE-POSITIVE-REGISTER.md.
- **Quality control:** the draft→reviewed→verified tiers; the verification protocol (all firsts + ⭐-records + a seeded ≥10% sample, logged); the excerpt-integrity audit (266/337 links machine-validated). Source: CODEBOOK.md verification protocol, verification-log.csv, EXCERPT-AUDIT.md.
- **Limitations (state them plainly):** contraband under-recorded by design (counts are a floor); Alta-only completeness; **flag reliability is period-dependent**, strong for the Spanish era, weaker for the Mexican (1822+), where a documented flag audit corrected 43 harvest-artifact `spain` rows and installed a post-1821 Spain ceiling guard (CODEBOOK "Flag reliability"; the *Asia* is the one genuine post-1821 Spanish visit); the excerpt is a snippet, not evidence. Source: CODEBOOK limits, PROVENANCE.md, TRAFFIC.md caveats.

## (3) Dataset description *(mostly structured fields, Aodhan fills the DOI/version)*
| item | value |
|---|---|
| Object name | California Ship Registry, 1769–1846 |
| Format | CSV (visits.csv, ships.csv, gazetteer.csv, verification-log.csv) + a normative CODEBOOK; self-contained HTML viewer |
| Creation dates | 2026-07 (seed) – ongoing |
| Dataset creators | Coyne, Aodhan (ORCID 0009-0002-8630-3768) |
| Language | English + Spanish (verbatim manuscript quotations) |
| License | CC-BY-4.0 (data/docs), MIT (code) |
| Repository / DOI | github.com/Aodhanm/california-ship-registry · Zenodo DOI *(pending Phase 1 mint)* |
| Temporal coverage | 1767–1848 (title span 1769–1846) |
| Spatial coverage | Alta California (Baja incidental) |
| Size | 401 vessels · 2,072 visits |

## (4) Reuse potential *(Aodhan writes)*
- Borderlands / Pacific-world historians: quantified traffic, per-vessel itineraries, leaf-linked evidence.
- Record-linkage / DH methods: the phantom taxonomy is a transferable pattern for any registry built from manuscript calendars + OCR'd print.
- Cross-dataset: links to the C-A calendar (record-level), the maps site, and, via masters/supercargoes, toward the ECPP person layer.
- The `sources_disagree` field and the verification log make it auditable and extensible by others. Source: CODEBOOK, ROADMAP Phase 4.

---

## Working notes
- **Gate:** submit after the DOI mint (Phase 1), JOHD requires the dataset be openly archived with a DOI.
- **Figure:** the stacked-area traffic chart (visits/half-decade × flag) from TRAFFIC.md is the one exhibit; generate it as a real figure before submission.
- **Word budget:** JOHD data papers are short; the phantom taxonomy + traffic finding are the two things to spend words on.
- **Venue check:** re-verify JOHD's current scope/word-limit before writing (per publication-venues dossier in the vault).
