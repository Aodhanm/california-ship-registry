# Review queue — uncertain ship identities (2026-07-15 vigilance pass)

*The confident merges/drops are applied (see harvest.py ALIAS + STOP_NAMES). These need a human ruling or a source check. Add rulings here; the alias table encodes them.*

## ⭐ C-A 40 INGEST — RE-STAGED, LEAF-VERIFIED (2026-07-16, NOT yet merged)
First staged then retracted (first-pass name errors), now **re-built from a careful leaf-by-leaf re-read** (scale 2–3) of both customs ledgers. Files: `data/ca40-new.csv` (**13 visits, 6 new ships**) + `data/ca40-attach.csv` (**8 corroborations**). Guard vocab + citations validated; all `status=draft`.
- **Leaf-verified names** (correcting the first pass): brig ***Nilo*** (not "Wilcox", d7 n5), frigate ***Jackman*** + pailebot ***Spy*** (not "Jackson", d9/d68), the 1826 goleta ***Spry[?]*** likely = existing ship ***Spray*** (attach), ***Tomasa*** = a name-variant of ***Thomas Nowlan*** (existing).
- **1826 SB ledger (d68, n65):** *Washington $193, Spry[?] $723, Jackman $448, Eliza $1112, Fígaro $533, Thomas Nowlan $2199, Rover $812, Courier $1536, Olive Branch $510, McCulloch[?] $813* — gross $9,744.
- **1827 SB ledger (n81, 2nd cuatrimestre):** *Courier* (×3 incl. San Pedro), *Tomasa* (×2), *Francesa* $400, *Carmen* $14, *Harbinger* (×3 incl. San Pedro), *Amiga* $232 — total $3,943.
- **New ship_ids:** `jackman, figaro, mcculloch, nilo, francesa, amiga`. **Corroborations** (existing 1826/1827 SB rows): courier, eliza, olive branch, rover, washington, gen. bravo, spray.
- ⚠ **Reviewer flags:** ***Francesa*** may be a demonym ("the French one"), not a ship name — verify at n81 before minting; *Washington*/*Eliza* common names (see split-queue); *McCulloch[?]*/*Spry[?]* uncertain Savage renderings.
- **TO MERGE:** fold `ca40-new.csv` into `visits.csv` (assign v-ids) + add the 6 new ships to `ships.csv`, apply `ca40-attach.csv` citations, then re-run `check.py` + the 7-class gate.

## Identity conflations to split
- ✅ **descubierta SPLIT 2026-07-15** (Aodhan caught the fake 1794 US ship): 1792–95 → merged into *discovery* (Vancouver, British); 1819–21 → *descubierta-rus* (the Russian imperial corvette); pre-1792 Malaspina reserved. The 1794 'American Descubierta' was a PHANTOM = C-A 7 d284, a foreign-EXCLUSION policy order (no ship) — dropped via NONSHIP_RECORDS. Flags for the core Spanish fleet made authoritative (the Aránzazu-carrying-an-Irishman was mis-flagged USA → now spain).
- **washington** (5v, 1825–29) — likely more than one vessel (the *Washington* schooner vs others).
- **enrique** (1797–1840) — at least the 1800 courier ship + later uses; probably 2–3 vessels.
- **eagle** (1807–22) — the 1807 New-York warning (a *report*, not a visit) vs the 1816 *Eagle* on the coast.

## Probably real, need one source check each
- **net-siut** (1799), **tic-me-mash** (1825), **oguahi** (1824) — non-European renderings; real vessels? (cf. Hawaiian-named brigs: *Tamaahmaah*, *Karimoko* are real.)
- **la elisa** (1801) → the *Eliza* (1799)? Plausible return visit; merge only with a source.
- **isaac tarlar / iron tarlar / javier sartar** (1824) — garbles of the *Young Tartar* family or of *Isaac Todd*? One leaf check.
- **la catalina** (1803, "usa") — which Catalina? Predates the Lima *Catalina* (1813).
- **santa barbara / san francisco / refugio / catalina** — place-name vessels; verify each isn't a place misparse.
- **el pelao / el rey** (1781) — boat nicknames in a padrón context? Check the record.
- **bruja / diga / cadiac / reisos / plant / ruperto / tester / vinas** — garbles or fragments; one record-read each.
- **mercedes** (1797–1801, "usa") — flag suspicious; likely = *N.S. de la Merced* family (Spanish).
- **levante** — dropped as the wind; if a record genuinely names a ship *Levante*, restore with citation.

## Split already applied, verify later
- **juno-1767** vs **juno-rac** (era split at 1800)
- **william shaler** → *lelia byrd* (captain-as-ship, ca12-d73)
- **el otro boston** → *otter* (the 1796 pun — DELIGHTFUL and real; cf. Bancroft: "called by the Spaniards the Otter Boston, El otro Boston")

## Humboldt Bay discovery (asked 2026-07-15)
The vessel that first entered Humboldt Bay (June 1806) was the **O'Cain** — American ship, Jonathan Winship master, but **on RAC contract with ~100 Aleut hunters** (the Russians' 'Bay of Rezanov' naming follows from the patronage). ⚠ NOT yet a row: neither Ogden nor any vault source confirms the Humboldt entry specifically (Ogden's ch. IV covers the 1806 Winship contract without naming the bay). TARGET SOURCE: the Winship log excerpts ('Solid Men of Boston,' Bancroft MS) or Bancroft, History of the Northwest Coast. Create the row only with one of those in hand. The O'Cain is already in the registry (3 Spanish-side visits, 1804–06).

## 1b-v vault-harvest dispositions (2026-07-15)
- ✅ curated in: **Kamchatka** (Golovnin, Monterey Oct 1818 — AGI Californias 8/3), **Activa** (Quadra, Monterey 1792-93), **Betsey of London** (Cabo San Lucas 1799), and earlier Boussole/Astrolabe/Daedalus.
- **Diana** — never visited CA (the Bolkhovitinov hits = the Khvostov Kuril raids); no row.
- **Pájaro** — a river, not a ship; candidate withdrawn.
- **Charon** — exists in RAC correspondence (Baranov's Oct 1812 overture 'via Elliott on the Charon,' OR RGB F.204) but no documented CA port visit yet; row awaits evidence.
- **Aiaks, Canton, Tamana** — Tamana handled by the Ogden extraction; the others' contexts are non-visits; remain queued.
- The rest of `data/vault-sweep-candidates.txt` (~520 lines, mostly noise) = the standing review file; work top-down by file-count when idle.

## Fake-ship purge (2026-07-15, "check all the footnotes")
- **63 OCR-garble Mexican-list names** quarantined to `data/mexlist-suspects.csv` (Pilrjrim=Pilgrim, Wilminfjton=Wilmington, Pocahontaa=Pocahontas, Leanidas=Leonidas, etc.) — the mexlist extractor now gates on a strict clean-name test + fuzzy-attaches garbles to established ships (51 corroborations) rather than minting duplicates. Only 100 clean new Mexican-period rows kept (was 181).
- **11 non-ship records dropped** via NONSHIP_RECORDS (harvest.py): demonym 'Californio' (padrón — the real goleta at ca14-d16 kept), place 'Sto Domingo', 'Patentes Reales' (royal patents), persons 'Lázaro'/'Thomas Marshall'/'Juan José', and spurious 'Cleusa/Apolonia/Ester/Cora/Andes' from vaccination/fund/tax records.
- Result: 479 → **424 ships**, 2,245 → **2,134 visits**; 0 US ships in 1794; guards green.
- ⚠ STILL TO REVIEW (lower-confidence, left in as draft): single-record Mexican warship names (Matamoros), the Tarlar/Sartar garble family, Hawaiian-named brigs (Tic-me-mash, Karimoko, Oguahi — likely real), and the 63 quarantined garbles (many are real ships needing spelling repair + re-merge).

## C-A 40 merge follow-ups (2026-07-18, from the A1 fold)
- **courier flag conflict:** ships.csv has `flag_guess=russia`, but the C-A 40 1826 SB ledger reads "frag. **Amⁿ** 'Courier'" (and HoC's Courier is the Boston hide-drogher, Capt. Cunningham — cf. v1485). Almost certainly **usa**; rule + fix flag.
- **thomas nowlan flag conflict:** ships.csv `flag_guess=britain` vs the C-A 40 ledger's "frag. **Amⁿ** 'Thomas Nowlan'". Sources disagree (movement reports call her Eng.); rule.
- **courier 1827 ledger entries ≠ existing rows:** the C-A 40 1827 ledger (n81) has Courier duty entries 4 May SB ($312), 24 May San Pedro ($81), 21 Aug SB ($240) — neither v1485 (Jan, San Pedro) nor v1494 (9 Jul, SF) matches. Likely 1–3 **new** 1827 Courier visits; create rows or rule as passes of the same coasting voyage.

## ⭐ v0.5 CALENDAR RE-HARVEST — STAGED (2026-07-18, NOT merged)
Phase 0 harvested the calendar at ~13k records; it now holds **19,755 / 60 volumes**. Re-ran harvest (redirected, drafts untouched) → diffed against every ca-record citation in the live table → **202 fresh rows** from post-Phase-0 volumes (33/29/30/62/39/57/28/40/23…). Files:
- `data/ca-calendar2-new.csv` — **60 new-visit candidates** (incl. the 1830s–40s ships the registry lacked: ***Natalia*** [the Híjar–Padrés colony brig], *Loriot*, *Leonidas*, *St. Louis*, *Alert*, *Thomas Perkins*, *Clementina*; + variants re-aliased to existing ships: albatros→albatross, providencia→providence, **apolo→apollon** [the 1823 SF wintering], **"Anglo-Am. Nº 8"→nilo**).
- `data/ca-calendar2-attach.csv` — **40 corroboration candidates** (existing ship+year matches).
- `data/ca-calendar2-stage.csv` — **84 unnamed-vessel events** (evidence of traffic, not mintable).
- `data/ca-calendar2-dropped.csv` — **18 documented-phantom recurrences** dropped w/ reasons (the FP classes recurring in fresh records, exactly as the standing rule predicts: persons *Apolonia/Cleusa/Ester*, the fort *Ross*, the pack-train *Recua*, the month *Junio*…).
- ⚠ **9 would-be NEW ships need a ruling before minting:** *carolina, congreso* (USS **Congress** 1846?), *descubierta* (era-adjudication), *el carlos* (= the *San Carlos*?), *juliann* (Julia Ann garble?), *magdalena, nueva california, orizaba, rosa* (10 rows — one Rosa or several?).
- **MERGE RULE:** manuscript-derived names get the C-A 40 lesson — leaf-verify ledger-class documents before minting; the *attach* file is lower-risk and can fold sooner.

## 📋 TRIAGE RESULTS (2026-07-18, A4 pre-classification) — the human list is SHORT
- **HoC staging (1,906 events) → `data/hoc-triage.csv`:** **284 auto-attach-safe** (ship+year already live; mechanical fold, sanction as a batch) · **538 strong-new** (known ship, dated, no row — mergeable after a sample-check) · **17 review-new-ship** (the actual rulings) · 1,020 weak (leave staged) · 47 noise.
- **Ogden 288 (`ogden-new.csv`):** ⭐ **every one already has a live same-ship-same-year row** — so this is ONE policy call (fold as attach-citations vs. keep as separate visit rows), not 288 rulings.
- **Mexlist garbles (63) → `data/mexlist-suspects-triage.csv`:** auto-proposed repairs w/ confidence scores; rest marked (manual) — a quick eyeball pass.
- **Aodhan's actual v1.0 decision set:** ① sanction the 284 auto-attaches ② the Ogden fold policy ③ the 17 new-ship rulings ④ the 9 calendar2 new-ship rulings (above) ⑤ the garble approvals ⑥ the standing identity splits (washington/enrique/eagle/Francesa/flag conflicts). Everything else is staged and safe.

## FIRSTS-derivation artifacts (2026-07-18)
- **Nootka-anchorage rows counted as CA visits** (v0177 *Mercury* 1790, v0178 *Princesa Real* 1790…) — decide: exclude `anchorage=Nootka` from the CA completeness claim / tag region.
- ***la hermosa mexicana*** (v1105, 1817, flag=mexico, pre-independence) — person-name FP suspect ("the beautiful Mexican woman"?); check the record.

## v0.5 calendar2 — PARTIAL FOLD (2026-07-18 late)
Per the merge rule ("attach folds sooner; existing-ship lower-risk"): **18 attaches applied** + **39 existing-ship visits merged (v2149–v2187)** → registry **2,187 visits / 430 ships**, guards HARD 0. Still gated: **21 held rows** in `ca-calendar2-new.csv` (the 9 would-be new ships + suspect-note rows — Aodhan rules) and **22 ambiguous attaches** left in `ca-calendar2-attach.csv` (multi-match ship+year — need per-row disambiguation, e.g. concepcion-1797 ×19).

## Unresolved OCR garbles from Ogden (2026-07-27 corroboration audit)
Roster-wide cross-check vs the local Bancroft 7-vol text + C-A citations: 395/398 ships corroborated by a reliable source. The only unresolved names — Ogden entries too OCR-mangled to identify a real vessel (Ogden lists *some* hull there; need her clean catalog):
- **`dhualle`** (2 visits, 1829, Monterey/Sta B.) — unidentified. Not the Danube (Robbins, wrecked 1830) on spelling; possibly a French visitor. Keep draft, do not assert a name.
- **`william inttle`** (2 visits, 1831, Monterey/Sta B.) — likely "William Little" but no Bancroft/C-A confirmation. Keep draft.
- Resolved this pass: `caauifrornia`→`california-sanblas` (Mex. San Blas vessel 1823-31), `califorma`→`california-1845` — both real per Ogden.

## Identity-split pass (2026-07-27)
- ✅ **enrique** — dropped 2 non-ship visits (1797 weaving/cloth record; 1840 "the foreigner Enrique (Henry)" = a person in the Graham Affair, Bancroft vol IV confirms). Cluster now = the real 1800 courier ship only.
- ✅ **eagle** — split off `eagle-frigate` (the 1814 Spanish-chartered frigate that seized the *Pedler* at S.L. Obispo, a distinct hull); the 1807 New-York report stays typed `mention`; 1821/1822/1825 stay as the American trader *Eagle*.
- ⚠ **washington** — NOT split (deliberately): two hulls are implied — a **140t schooner** (Robt Elwell master, 1825, from the Sandwich Islands) and a **52t goleta** (Capt. Thompson, 1826, chile cargo, per Vallejo) — but the other 14 visits (1824–29, incl. the Richardson/Charles Laing goleta) can't be confidently assigned between them just one year apart; the 52-vs-140t gap could be a recording error. Left as one cluster pending a source that resolves the two. Do not guess-assign.

## Draft-queue resolution (2026-07-27) — 27 → 7
Worked the whole draft queue against the local Bancroft text + C-A excerpts:
- **Merged into a real ship:** cadiac→*kodiak* (excerpt glosses "Cadiac (Kodiak)"), la elisa→*eliza*, tic-me-mash→*tamaahmaah* (Kamehameha), javier sartar→*predpriatie* (record is about the Predpriatie).
- **Renamed to a real ship:** diga→**cruiser** (excerpt: "la Fragata de guerra Rusa nombrada *Cruiser*").
- **Promoted (excerpt names the vessel):** el pelao (balandra, 1781), el rey (mail-frigate, 1781), refugio (Am. brig, Capt. Frome Thompson, 1833), thankful (bergantín, 1829), ruperto (brig, S. Pedro), oguahi (Am. brig 166t = O'ahu), mercedes (Spanish sloop captured 1799 — flag fixed spain).
- **Dropped as mis-parses/non-ships:** net-siut, tester, vinas (all garbled from the *single* 1799 Mercedes-capture record), san francisco + santa barbara (the places, from church/muster/Channel records), bruja + reisos + ynez (fragments from multi-ship registers naming Margarita/Peacock/Convoy). All HARD-guarded.
- **Still draft (7):** dhualle, william inttle (Ogden garbles — need her book); washington (140t vs 52t two-hull split); iron tarlar, isaac tarlar (1824 garbled frigate/schr — Isaac Todd? Young Tartar?); francesa (demonym vs name); mcculloch (the merchant vs a ship).

## Identity note (2026-07-27, from the FIRSTS leaf-pass)
- **morelos** — conflates TWO hulls: the 1825 Mexican war-**brig** *Morelos* (bergantín/transport from San Blas, convicts + supplies 1825–30) and the 1834 war-**corvette** *Morelos* (corbeta, cmdr Lucas Frey). Split by year/type when convenient (Class 2). The 1825 brig is the leaf-verified first Mexican-flag national vessel.

## Resolved from Ogden's BOOK (appendix, printed pp.155–184) — 2026-07-28
Ingested Ogden's authoritative vessel appendix ("Identified Vessels Engaged in the California Sea Otter Trade, 1786–1848"), read from the page images (the vault PDF), NOT the garbled OCR itineraries used earlier:
- **`william inttle` → `william little`** — Ogden p.176: *"William Little, 1831 — Sloop, 36 tons, 7 crew; captain, Henry Carter; owner, Henry Carter, Honolulu; otter skins, 478."* Real; renamed + reviewed.
- **`dhualle`** — Ogden p.175 prints the name as *"Dhualle"* (so the registry spelling is correct, not a garble): *"Brig, 182 tons; captain, William Warden; owner, at Hawaiian Islands; otter skins, 40 at Monterey"* (1829). Real; reviewed.
- ⭐ **`washington` split RESOLVED** (do next): Ogden shows two hulls — (a) the **Marshall & Wildes schooner, 45–52 tons** (Capts. ——Little then Alpheus Basil Thompson; trips 1824, 1826, 1828–29, 1829) and (b) the separate **140-ton schooner** (Robt Elwell, from the Sandwich Islands, 1825). Assign the 16 washington visits accordingly.
- **`iron tarlar`/`isaac tarlar` (1824)** — NOT in Ogden's otter appendix (they're C-A customs-record names); still need the C-A leaf or another source.
- Confirmed real (vindicating earlier merges): Actwo=*Activo* (Capt. Baridon, San Blas), Liclipse=*Eclipse* (343t, Capt. Joseph O'Cain), Plant (208t brig, Capt. Rutter, Bryant & Sturgis), Karimoku (formerly the *Becket*).
- **Follow-on:** the full appendix (~170 vessel-trips) is extracted to the vault (`raw/papers/ogden-appendix-identified-vessels-1941.txt`) — enrich matched registry vessels with Ogden's tonnage/captain/owner/otter-skin facts (facts, not prose — Ogden is still in copyright until ~2037, so no text in the public repo).

## Draft queue CLEARED — 2026-07-28 (100% reviewed)
Last drafts adjudicated at the C-A leaf:
- **`iron tarlar` + `isaac tarlar`** → merged. Leaf C-A 56 n247/n231: one real 1824 English merchant frigate at SF, Savage rendering it "Iven/Ivon Tarlar" (and "Tomas Farlan", Capt. Wm Chick, from Lima) — genuine vessel, name unrecoverable in Savage's own hand. Reviewed.
- **`mcculloch`** → real. Leaf C-A 40 n65: listed among vessels trafficking at Sta Bárbara (Washington, Spry, Jackman, Elisa, Thomas Newton, Rover, Courier, Olive Branch, McCulloch/McEither $813, Dec 1826). Reviewed.
- **`francesa`** → real. Leaf C-A 40 n81: a vessel entry in the 1827 customs ledger ("Mayo 8, 'Francesa', $400"), alongside Courier/Tomasa/Harbinger — a French vessel, not a stray demonym. Reviewed.
**Registry: 391 ships, ALL reviewed.**

## 2026-08-04 flag-floor purge — items needing a ruling
*(The purge itself is applied and logged in FALSE-POSITIVE-REGISTER.md; these are its residue.)*
- **v0878** — a 1807 R.O. about the U.S. ship ***Eagle*** sits attached to ship `betsy`; check whether the record mentions the *Betsy* at all or belongs on `eagle` (cf. the existing eagle-conflation item above).
- **Cleared russia flags worth one look each** (nationality word absent from the record, flag blanked): **v0964** (1813 "remisión de capitán de buque apresado" — likely the *Mercury*/Eayrs affair → would be *usa*), **v1037** (1816 English-language letter on anchoring at Refugio — Il'men/Lydia orbit?), **v1890** (1839 no-commerce order re a ship).
- **13 rows cite C-A records with no local catalog file** (couldn't full-abstract-check): v0076 v0389 v0456 v0795 v0803 v0884 v0886 v0923 v0928 v0975 v1001 v1016 v0369 — spot-check on the next pass.
- **v2124** — "bounded" multi-doc row whose single doc anchor (ca20 d224) doesn't match its summary; re-anchor or split.

## 2026-08-04b — Ogden appendix re-parse (the Loo Choo lesson)
The corrupted *Loo Choo* block is fixed (see FALSE-POSITIVE-REGISTER 2026-08-04b). **Open work:** ~12 appendix entries were swallowed by the parser and have NO itinerary rows — Jenny 1794, Garland 1798, Derby 1807, Dromo 1809, Cossack 1817, Loriot 1833–34, Bolívar Liberator (3 garbled headers), Lama 1837–38, California 1840/1842–46. Source is on disk (`~/vault/raw/papers/ogden-appendix-identified-vessels-1941.txt`, line refs in the register). Mint them entry-by-entry with real dates (the schedules carry day-level precision), NOT by re-running the bulk parser. ⚠ Jenny 1794 / Garland 1798 predate the usa floor — check each vessel's actual nationality in Ogden/Howay before flagging (Jenny was British-operated in 1794).
