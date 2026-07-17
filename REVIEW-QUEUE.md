# Review queue — uncertain ship identities (2026-07-15 vigilance pass)

*The confident merges/drops are applied (see harvest.py ALIAS + STOP_NAMES). These need a human ruling or a source check. Add rulings here; the alias table encodes them.*

## ⭐ PENDING SOURCE-FAMILY INGEST — C-A 40 (staged 2026-07-16, NOT yet merged)
Staged from **C-A 40** (Dep. St. Pap., Benicia — *Commissary & Treasury*, `168036070_81_2`), a fresh archival customs source — **independent corroboration of the 1826 Santa Bárbara port activity** already partly captured from C-A 41/C-A 18. Files: `data/ca40-new.csv` (**12 new visits**) + `data/ca40-attach.csv` (**4 corroborations**). Validated against the guard vocab (flags/visit_type/status) + the 7 false-positive classes; all `status=draft`.
- **The 1826 Sta Bárbara customs ledger (C-A 40 d68, n65)** = a ship-by-ship duty register → precise arrival dates + duty amounts. New rows: **Spry** (19 Jun), **Jackson** (27 Jun), **Fígaro** (13 Sep), **Thomas Nowlan** (22 Oct), **Courier** (28 Oct), **McCulloch[?]** (9 Dec). NEW ship_ids to create: `spry, jackson, figaro, mcculloch, wilcox, bravo, morelos`.
- **Individual-document visits**: *Rover* at Monterey from **Canton** (Capⁿ J.R. Cooper, d38); *Jackson* at Monterey w/ supercargo **Wm A. Gale** (d9); *Wilcox* at Sta Bárbara $1824 duties (d7, later a charge vs Comisario Herrera); *Harbinger* at San Diego from the **Sandwich Islands**, left without sales (d54/d55); *Bravo* (mexico, tobacco-monopoly supply from Acapulco, d60); *Morelos* (mexico national warship, presidio supply, d2/d11).
- **Corroborations (ca40-attach.csv)** → add a C-A 40 citation to existing rows: *Eliza* v1449 (ledger 2 Sep vs C-A 18's 31 Aug — minor date disagreement), *Rover* v1457, *Washington* v1458/v1469, *Olive Branch* v1468.
- ⚠ **Washington** & **Eliza** are common names (see the split-queue note below) — the ledger visit is a discrete duty entry; confirm same vessel before collapsing. **McCulloch[?]** = uncertain Savage rendering.
- **TO MERGE**: fold `ca40-new.csv` into `visits.csv` (assign v-ids), add the 7 new ships to `ships.csv`, apply `ca40-attach.csv` citations, then re-run `check.py` + the data-quality gate. *(Left un-merged here to avoid hand-reimplementing the build assembly; the source rows are validated & ready.)*

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
