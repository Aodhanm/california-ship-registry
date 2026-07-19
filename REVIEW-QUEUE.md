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
