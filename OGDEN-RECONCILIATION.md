# Ogden ↔ Bancroft reconciliation (2026-07-27)

*What Adele Ogden's vessel itineraries add to the registry, what Bancroft independently corroborates, and what is still garbled. Companion to `FALSE-POSITIVE-REGISTER.md` and `REVIEW-QUEUE.md`.*

## Sources in play
- **Ogden itineraries** (`data/ogden-itineraries.csv`) — an **OCR extraction** of Adele Ogden's trading-vessel itineraries (*The California Sea Otter Trade, 1784–1848*, and her vessel card-file). **89 distinct vessels / 898 port-call rows.** It is OCR, not a clean transcription — garbles survive in it (e.g. the ship name literally stored as `CaAuIFrorniA`).
- **Bancroft** — enters the registry two ways: (a) `[Bancroft list YYYY-Y]` = his printed **marine lists** in *History of California* (84 ship rows, mostly 1841–48, a **partial** ingest); (b) `ca-record` / `Bancroft Hist.Cal.` citations on the C-A-manuscript and narrative visits (the bulk of the dataset).

## Headline numbers
| | vessels |
|---|---|
| Ogden raw (distinct) | **89** |
| → live in registry as ships | **64** (288 visits, all `status=draft`) |
| Ogden vessels **corroborated** by Bancroft/C-A/other | **40** |
| Ogden vessels **Ogden-only** in our data | **41** |
| Ogden vessels that were **OCR garbles** (merged into the real ship) | **8** |
| Bancroft printed-marine-list ships (disjoint set) | **84** |
| **Ogden ∩ Bancroft-marine-list (same ship_id)** | **0** |

## Finding 1 — the two sources are siloed
No ship currently carries **both** an `[Ogden itinerary]` visit and a `[Bancroft list]` citation. Ogden's 64 and Bancroft's printed-list 84 are wholly disjoint ship_ids, even where they must be the same hull (e.g. Ogden's *Loo Choo* / *Don Quixote* also stand in Bancroft's 1840s marine lists). **The cross-link was never made.** ⇒ biggest remaining data-quality task: ingest Bancroft's full marine lists and merge against Ogden by name+year, so a vessel in both shows one row with two authorities.

⚠ **"Ogden-only" ≠ "absent from Bancroft's books."** It means *not yet cross-linked to a Bancroft/C-A row in our data*. Bancroft's *History* marine lists and Pioneer Register almost certainly contain most of the "Ogden-only" ships below; we just haven't ingested that slice.

## Finding 2 — Ogden's real added value (the 41 "Ogden-only")
These are overwhelmingly **real** Anglo-American / Hawaiian / Russian trading and otter-hunting vessels of the 1800s–1840s — exactly the traffic the Spanish/Mexican C-A manuscripts under-record. Ogden is the authority that captures them:

*Well-documented real ships* — Loo Choo (41 visits), Waverly, Don Quixote, Owhyhee, O'Cain, Forester, Kutusov (Kutuzov), Ilmen, Alciope, Admittance, Avon, Maryland, Monsoon, Traveller, Harriet Blanchard, Griffon, Karimoku (Kalanimoku), Kamehameha, Okhotsk, Prince Lee Boo, Butterworth, Jackal, Diana, Isabella, Phoenix, Amethyst, Charon, Katherine, Becket, Crusader, Victoria, Morse, Clementine, Bordeaux Packet, Rasselas, Joseph Peabody, Tamana. → these are keep-and-corroborate: match each to a Bancroft marine-list line to move it from draft toward reviewed.

## Finding 3 — still garbled (flagged, NOT minted)
Resolve against Ogden's clean catalog before asserting a name:
- **`caauifrornia` (7) + `califorma` (5)** — Ogden's file *does* list a vessel **"California"** (1823–1831 out of San Blas; and 1845–1846). So this is probably a **real trading vessel California**, distinct from the sunk place-phantom `california` — but the OCR is too mangled to mint the clean name safely. **Do not restore "california" as a ship_id** (it is HARD-guarded as a phantom); use a disambiguated id (e.g. `california-schr`) only after confirming the vessel and its dates in Ogden.
- **`william inttle` (2)** — garble; likely *William Little* or *William & Ann*. One catalog check.
- **`dhualle` (2)** — garble; unresolved.

## Finding 4 — garbles already fixed this pass
Merged into the real ship (Ogden OCR twins): `actwo`+`actwwo`→*Activo*, `chirtkov`→*Chirikov*, `iimen`→*Ilmen*, `loussa`→*Louisa*, `maraquita`→*Mariquita*, `liclipse`→*Eclipse*; and the internal apostrophe twin `o' cain`→*o'cain*. All encoded in harvest `ALIAS`.

## Recommended next steps
1. **Ingest Bancroft's full marine lists** (Hist. Cal. II–V) and cross-merge with Ogden by name+year → kills the silo, corroborates the 41 Ogden-only, and surfaces vessels Ogden lacks.
2. **Resolve the 3 garble flags** against Ogden's clean catalog (esp. the *California* vessel).
3. Promote matched Ogden vessels from `status=draft` → `reviewed`.

---

# Bancroft marine-list ingest + three-source merge (2026-07-27, same day)

Acted on Finding 1. The full Bancroft Mexican-period marine list was already staged in `data/mexlist-stage.csv` — **198 vessels** (Hist. Cal. vols III/IV/V, spans 1825-30 / 1831-5 / 1841-5 / 1846-8). Cross-matched it (ALIAS-aware) against the live roster:

| bucket | n | action |
|---|---|---|
| in **BOTH** Ogden & Bancroft-list | 17 | **corroborated** — added a Bancroft marine-list citation to each (kills the silo) |
| already present as a live ship | 123 | already covered |
| genuinely **new** real vessel, clean name | 8 | **added** |
| **phantom-name but real vessel (has tonnage)** | 10 | **flagged, NOT minted** — need the Bancroft page |
| OCR garble / thin | ~40 | left in stage; need the suspects-triage fixes applied |

**Corroborated (now Ogden + Bancroft):** convoy, eagle, griffon, mercury, okhotsk, washington, waverly, diana, crusader, mariquita, plant, volunteer, columbia, eliza, admittance, fama, louisa.

**Added as new Bancroft-marine-list vessels (with tonnage):** *Pilgrim* (155t — Dana's ship), *Wilmington* (364t), *Paragon* (309t), *Peruvian* (331t), *Affiance*, *Bowditch*, *Huntress*, *Corea*. Registry now **393 ships / 2,090 visits**.

## Finding 5 — the marine list has REAL vessels sharing a dropped phantom's name
Bancroft's *List of vessels* records vessels **with tonnage** named `Sitka` (russia 202t, Monterey), `Times` (britain 407t), `Friend` (usa 404t), `Fernando` (mexico 344t), `Trinidad` (mexico 170t), `California` (usa 379t; usa 422t), `Tartar` (usa 301t), `American` (88t), `Expadon` (france 397t). These are **not** the narrative-word phantoms we sank (the month, the demonym, the place) — they are real hulls. **But** the whole stage file is raw OCR, and these names are exactly where OCR error hides, so they are **flagged, not minted**: confirm each against the actual Hist. Cal. marine-list page, then add under a disambiguated id (e.g. `sitka-vessel`) — never the bare phantom id (those are HARD-guarded).

## Still open
- Apply the full `mexlist-suspects-triage.csv` garble fixes to the stage file, then re-run this match to trust the remaining ~40 stage vessels.
- Verify + mint the 10 phantom-name real vessels from the Bancroft page.
- **Coverage gap:** the staged list is Mexican-period only (1825-48). Bancroft's **Spanish-period** vessel list (Hist. Cal. I–II, pre-1825) is not ingested — the pre-1825 traffic rests on the C-A manuscripts alone.

---

# Bancroft-page verification of the phantom-tonnage vessels (2026-07-27)

Verified the 10 "phantom-name but has-tonnage" flags against Bancroft's actual *List of vessels* on Wikisource (hand-corrected transcription of Hist. Cal. vol III, ch.6, djvu p.146). **The pattern is confirmed: these are mostly mis-parses — the OCR grabbed a place/origin or an adjacent word and kept a neighbouring vessel's tonnage.**

| stage entry | verdict (verbatim Bancroft) |
|---|---|
| `Sitka` russia 202t | **mis-parse → the *Baikal*** — "*Baikal,* Russ. brig, 202 tons; up and down the coast from Ross to S. Diego each year 1826–30" (Sitka = her origin port). Already in registry. |
| `Tartar` usa 301t | **→ *Young Tartar*** — "*Young Tartar* (or *Jóven Tartar*), Engl. schr, 95 tons; John Brown master, 1826-7." Name resolves to a ship we already hold; the 301t is spurious. |
| `American` 88t | **not a vessel** — does not appear as a vessel name in the list (the demonym, as suspected). |
| `California` 379t / 422t | **not a vessel name** in the 1825-30 detailed list (mis-parse). 1841-5 entries unverified (tooling); left flagged. |
| `Times` britain 407t | **REAL — minted** as `times-whaler`: "*Times,* Engl. whaler, 407 tons; Wm Ross, master; at Sta B. Oct. 1828." Disambiguated id (never the dropped word `times`). |
| `Friend` 404t | not in the 1825-30 list; 1831-40 unverified; left flagged. |
| `Fernando`/`Trinidad`/`Expadon` (1841-5, Mexican/French, w/ tonnage) | **unverified** — vol IV chapter structure + repeated connection drops blocked the read. Left flagged; could be real Mexican/French vessels or mis-parses. |

**Net:** of the 10 flags, 2 are confirmed mis-parses of ships we already hold (Baikal, Young Tartar), 2 confirmed non-vessels (American, California-1825/30), **1 confirmed real and minted (Times)**, and 5 remain flagged pending a vol-IV read. **The discipline of flag-not-mint was correct** — blindly minting these would have re-created phantoms.

## Task-3 note (Spanish-period ingest) — deferred
Attempted to ingest Bancroft's Spanish-period (pre-1825) vessel lists (Hist. Cal. I–II). The exhaustive Wikisource transcription stalled repeatedly (slow raw-page fetches hitting watchdog timeouts + mid-response connection drops). Not completed this session. **Mitigating fact:** the Spanish period is already the registry's best-covered era via the C-A manuscripts (e.g. *Princesa* 70 visits, plus Concepción, Activo, San Carlos, Favorita, Aránzazu…), so a Bancroft Spanish-period pass would mainly *corroborate* existing ships (as the Mexican-period pass did) rather than add many new vessels. Left as a future task.
