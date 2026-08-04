# False-positive register — known fake-ship classes

*The catalog of ways a non-ship (or duplicate) gets minted as a vessel, each with how it's detected and where the guard lives. **Run through this whenever new records/sources are added** — a new volume or book re-triggers every class. Discovered 2026-07-14/15. Companion to REVIEW-QUEUE.md (open items) and the C-A calendar's `ca-data-issue-register.md`.*

## How the guards are wired
- `scripts/harvest.py` — `NONSHIP_RECORDS` (drop specific (ca_vol, doc) records), `STOP_NAMES` (never-a-ship tokens), `ALIAS` (merge spelling twins).
- `scripts/merge.py` — `SHIP_FLAGS` (authoritative national identity), `adjudicate()` (era-splits one name into real ships), `SHIP_FLAGS` overrides stray record flag-hints.
- `scripts/hoc_sweep.py` — `HOMONYMS` (common English words needing maritime context), `NEWSTOP`.
- `scripts/mexperiod_sweep.py` — `strict_clean()` garble gate + fuzzy-attach to established ships.
- `scripts/check.py` — build guards (flag vocab, citations, dates, dedup) block a bad build.

---

## Class 1 — the policy/decree phantom
A record about a *law or order concerning ships* becomes a "ship visit."
- **Example:** the 1794 general foreign-exclusion order (C-A 7 d284) → a fake "American *Descubierta*" in 1794. The words "Descubierta" + "American/Boston" in the exclusion text fooled the matcher.
- **Tell:** excerpt is a general order/decree/regulation, no specific arriving vessel; often flagged with a nationality that contradicts the ship name.
- **Guard:** `NONSHIP_RECORDS` in harvest.py. **When adding records: any "orden/bando/reglamento sobre buques extranjeros" is a policy, not a visit.**

## Class 2 — one name, several real ships (era-conflation)
Spanish scribes reused/translated names; distinct vessels collapse into one cluster.
- **Examples:** two *Junos* (1767 Cádiz transport ≠ 1806 RAC ship); *Descubierta* = Vancouver's *Discovery* (British, 1792–95) + a Russian imperial corvette (1819–21) + Malaspina's corvette (1791, Spanish); *Catalina* (Lima trader 1813 ≠ later Mexican *Catalina*).
- **Tell:** a cluster spanning decades and/or flags that don't cohere.
- **Guard:** `adjudicate()` in merge.py, split by year. **When adding: check any multi-decade or multi-flag cluster before trusting it.**

## Class 3 — the person-as-ship
A captain, supercargo, or owner named where a ship is expected.
- **Examples:** "William Shaler" (master of the *Lelia Byrd*, ca12-d73) → merged to *lelia byrd*; "Kendrick," "Sarrasoff" (=Boris Tarasov the patrón); "Lázaro," "Thomas Marshall," "Juan José" from crime/fine records.
- **Tell:** the name is a personal name; the record is about a person's act (murder, fine, appointment), not an arrival.
- **Guard:** `NONSHIP_RECORDS` (record-specific) or `STOP_NAMES` (if never a ship). **When adding: a two-word Anglo/Hispanic personal-name shape with only 1 visit and a person-context excerpt is suspect.**

## Class 4 — the place/demonym-as-ship
A port, region, river, or demonym in italics/quotes.
- **Examples:** "Californio" from a *padrón* (demonym) — but the real *Californio* goleta (ca14-d16) is kept; "Sto Domingo" from a salary decree; "Río Pájaro" (a river); "Sonora"/"Catalina" the province/island (handled as HoC homonyms).
- **Tell:** the token is also a place/people name; excerpt is about population, funds, geography.
- **Guard:** `NONSHIP_RECORDS` for the bad record (keep the name if it IS a ship elsewhere); `HOMONYMS` in hoc_sweep.py. **When adding: same name can be both — drop the record, not the name.**

## Class 5 — OCR-garble duplicates
The same real ship OCR'd two ways → a fake second ship.
- **Examples:** "Pilrjrim"=Pilgrim, "Wilminfjton"=Wilmington, "Pocahontaa"=Pocahontas, "Leanidas"=Leonidas, "Buitre"/"Vulture" (translation twin), "El otro Boston"/"Otter" (the Spanish pun).
- **Tell:** implausible letter patterns (fj, rj, tk, triple letters, low vowel ratio); or a clean name that's a spelling variant of an existing ship.
- **Guard:** `strict_clean()` gate + fuzzy-attach in mexperiod_sweep.py; `ALIAS` map in harvest.py for known twins. Garbles land in `data/mexlist-suspects.csv` for hand-repair. **When adding OCR text: expect garbles; route uncertain names to review, never mint.**

## Class 6 — the mis-flagged real ship
A real ship gets the wrong nationality from a stray context word.
- **Examples:** the Spanish *Aránzazu* flagged "American" (it carried a captured Irishman → "Englishman" in the text); the San Blas fleet mis-flagged from foreigner-aboard records.
- **Tell:** a core-fleet ship with a flag that contradicts its known identity.
- **Guard:** `SHIP_FLAGS` in merge.py is now **authoritative** — the known identity overrides record hints; flag_basis records "attested/inferred". **When adding: add confidently-known ships to SHIP_FLAGS so hints can't override them.**

## Class 7 — the retrospective mention / report (not a visit)
A record recalling a past ship, or reporting a rumored one.
- **Examples:** the 1806 measles recap naming the 1803 *Alexander*; the 1807 *Eagle* intelligence warning; Indian/rumor reports of ships at Bodega.
- **Tell:** past-tense recollection, or "noticias de / se dice / dicen los indios."
- **Guard:** `visit_type` = `mention` / `reported?` (MENTIONS set + REPORTED regex in merge.py); excluded from traffic totals. **When adding: a report of a ship is evidence about intelligence, not a visit.**

---

## Standing rule for new data
After ANY new records/volumes/books are ingested, re-run the pipeline, then:
1. Read `data/mexlist-suspects.csv` and any new single-visit clusters.
2. Sort the ship list by n_visits ascending — new 1-visit ships are where fakes hide.
3. Check any new multi-decade or multi-flag cluster (Class 2).
4. Spot-check flags on core-fleet ships (Class 6).
5. Everything uncertain → REVIEW-QUEUE.md, `status=draft`, never a confident row.

---

## Sweep log — 2026-07-27 (the "not a ship at all" pass)
Aodhan flagged that the live list still showed obvious non-ships (e.g. *California*). Re-read every zero-maritime-context cluster against the Bancroft text; sank **24 phantoms / 114 visits** (430→406 ships, 2187→2073 visits). All are now HARD-guarded by `DROPPED_SHIP_IDS` in `check.py` and blocked at harvest by `STOP_NAMES`.

- **HoC-sweep homonyms (11):** `california` (the province — "Who First Saw Alta California?"), `june` (58 visits — the month), `fernando` (the College/Mission San Fernando & King Ferdinand III), `american` (demonym — "an American ship"), `sitka` (the Russian port), `trinidad` (Trinidad Bay), `times` ("Early Times", a book title), `henry`/`edward` (bibliography names — Peirce, Hale), `friend` (the word), `tartar` (mis-parse; the real *Young/Joven Tártaro* is kept separately).
- **C-A / print-list phantoms (13):** `congreso mejicano` (the Mexican Congress), `don` (title fragment), `adela` (an Indian-raid guard record), `grafton` (three deserters arriving overland), `la paloma` (the Martínez prosecution file), `spray` (a company account), `hebe` (a wounding *sumaria*), `tagle` (a person — the *Mercurio* prisoners), `caminante` (a treasury letter), `rita` (a church-state treatise), `rosalia` + `neptuno` (both pulled from one Apodaca free-trade *decree* bundle — Class 1), `peruano` (French-nationals property, 1849).
- **Saved by reading (kept):** `carmen` (real bergantín, C-A 40 ledger) and `clarion` (Gyzelaar's ship — it carried the 1818 Bouchard warning to Santa Bárbara).
- **Still open (separate task):** OCR-garble twins in the Ogden/Bancroft print lists (`actwwo`→Activo, `liclipse`→Eclipse, `caauifrornia`/`califorma`, `iimen`→Ilmen, `fetvorite`→Favorite, `oajaca`→Oaxaca, etc.) — Class 5, recoverable to real ships; needs a merge pass, not deletion. Two Class-7 reports to adjudicate: `la independencia` (Cochrane's squadron off Baja) and `el aventurero` (the viceroy's Bouchard dispatch).

## Sweep log — 2026-07-27 (Class 5 OCR-garble merge pass)
Followed the phantom pass by merging garbled print-list/Ogden names into their real ship rather than deleting (recovers the visit). **406→386 ships, 2073→2065 visits.**
- **Merged into an existing real ship (12):** `actwo`+`actwwo`→*activo*, `chirtkov`→*chirikov*, `iimen`→*ilmen*, `taaso`→*tasso*, `loussa`→*louisa*, `maraquita`→*mariquita*, `fetvorite`→*favourite*, `guadidupc`→*guadalupe*, `elizabeih`→*elizabeth*, `vafidalia`→*vandalia*, `plowhoij`→*plough boy*. (garble spelling preserved in `name_variants` as "var:", and in `name_as_written` per visit.)
- **Renamed id (real ship, no canonical in set):** `liclipse`→**eclipse** (Capt. O'Cain's Boston ship, 1806), `oajaca`→**oaxaca**.
- **Dropped as unrecoverable (8):** `oivvi`, `panjir`, `xylon`, `suxden`, `suaanita`, `toidon`, `nadednik`, `apoho` — 1-visit Bancroft-list entries whose OCR left no confident reading; asserting a name would be worse than the refusal.
- All encoded in harvest `ALIAS` (merges/renames) and the `check.py` HARD guard (merged + dropped ids can't re-mint).
- **Still open (flagged, untouched):** `caauifrornia`/`califorma` — garbles of "California": confirm whether Ogden's itinerary actually lists a real *California* vessel before restoring (else these are place-phantoms like the sunk `california`). `timorelan`, `baihtl` (=*Baikal*?), `william inttle` (=*William Little*?), `dhualle` — need one source-read each.

## Corroboration audit — 2026-07-27 (roster vs. the full Bancroft text)
New capability: all 7 vols of Bancroft's *History of California* are now local plain text (`~/vault/raw/papers/bancroft-history-california/`). Ran a whole-roster reality check: for each of the 398 ships, is its name attested in **any** reliable source — a C-A manuscript citation, a Bancroft marine-list citation, Bancroft's narrative text, or Ogden's itineraries?

**Result: 396/398 corroborated.** Only 2 unresolved, both OCR-mangled Ogden entries (`dhualle` 1829, `william inttle` 1831) that name *some* real hull we can't identify without Ogden's clean catalog — left `draft`, flagged in REVIEW-QUEUE, not asserted. 2 California garbles were identified and cleaned (`caauifrornia`→`california-sanblas`, `califorma`→`california-1845`).

**This is now a re-runnable guard.** After any new ingest, re-run the cross-check (roster name → grep the 7 Bancroft vols + check for a C-A/Ogden citation). Any ship attested by *nothing* is a phantom suspect. Note: Ogden-only ships are legitimately real (Ogden is the authority on the fur-trade traffic Bancroft under-records) — corroboration = C-A OR Bancroft OR Ogden, not Bancroft alone.

## Sweep log — 2026-08-04 (flag-floor purge + no-hull sweep; Aodhan-directed)
Trigger: "American-flagged ships in 1785" on the site. Root causes found: (a) era-conflation — early Spanish-period records merged by name into later American ships (*Fama* 1785 → the 1841–46 American *Fama*; the 1790 Nootka *Mercurio* → Eayrs's 1806–26 *Mercury*), then the flag back-fill stamped `usa` onto the early visits; (b) `(unnamed vessel)` rows minted from records that mention no hull at all. **2108→2085 visits; guards HARD 0.**

**First-arrival floors now a HARD guard** (`check.py FLAG_FLOORS`, leaf-verified per FIRSTS.md): spain 1769 · france 1786-09 (Lapérouse) · britain 1792-11-13 (*Discovery*, SF) · usa 1796-10-29 (*Otter*, Monterey) · russia 1806-04-08 (*Juno*, SF) · mexico 1822. Precision-aware (a bare "1796" doesn't violate a 1796-10-29 floor); `sighting`/`reported?`/`mention` rows are exempt (a hull may be sighted offshore before its first port entry). Plus `DROPPED_CA_RECORDS`: 19 C-A records adjudicated non-ship can never re-mint visits.

**Dropped (23 rows, archived with reasons in `data/dropped-visits.csv`):**
- **Leaf-verified drops (2):** v0130 — the "1786 Russian ship-captain": C-A 22 n356–57 read 2026-08-04 — the entry is **1792** (Loreto series, Set. 12, pp. 560–3), *"aprueba el procedim.to con el capit.o Rusis[?] por haber este llevado dos Indias crist.s"* — a person (likely an Indian *capitán*), **no vessel in the record**; "Ruso" was a misreading. v0125 — the "1785 French" row: C-A 3 n185–86 read — Arrillaga→Fages personal letter on Baja canoe-mail/fletes; only hull = the Spanish frigate *Princesa*, Guaymas→San Blas. Neither is a California ship visit.
- **Out of scope / not-CA (2):** v0001 (the 1767 Cádiz *Juno*, Sonora expedition — ship `juno-1767` retired; distinct from the 1806 Russian *Juno*), v0177 (1790 Floridablanca Nootka instructions; anchorage was Nootka, not California).
- **Policy/no-hull phantoms (16, full-abstract-checked against `~/archives-of-california/catalog`):** v0368 (English-conspiracy report, was flagged *usa*), v0184 (Nootka circular), v2125, v0077, v0153, v0169 (*capitancillo* = Indian headman), v0204, v0405, v0796, v1149, v1338, v1570, v1628, v1839, v2116, and v2134 (person-as-ship: "Santiago" in a C-A 46 personal letter).
- **Merged, not lost (3):** v0410 + v0411 + v2123 → **v0373**, the ***Phoenix*** episode: Bancroft HoC I, 537 — *"the English merchant vessel Phoenix, Captain Moore… touched at Santa Bárbara in August [1795] from Bengal for supplies"* and left the "Boston lad" sent to San Blas. One visit, four records, flag **britain** (was wrongly *usa* via Ogden-presence inference).

**Reflagged:** v0129 → new ship `fama-1785` (spain; split from the American *Fama*), v0178 *Princesa Real* → spain (the captured *Princess Royal*, Spanish-operated 1790 — keeps the British first = Vancouver 1792 honest), v2131 *Betsy* → usa (Winship's brig, per ships table), v1105 *Hermosa Mexicana* → spain (the record itself says "Spanish frigate"), v0478 *Otter* → `sighting` dated 1796-05-28 (offshore, ID inferred; first port entry stays 29 Oct), v0461 → `mention` (a 1796–98 diary, not one usa port-call). Six unsupported flags on unnamed rows cleared to blank (v0953, v0964, v1037, v1798, v1890, v2124 — nationality word absent from the full record).

**Citation repair:** 16 rows citing C-A 25 by pre-renumber doc-ids remapped **+463** (the 2026-07-28 ca25 renumber, old d1–49 → d464–512); spot-verified by excerpt↔catalog title match (e.g. v2131 → ca25 d482 "Brig *Betsy*; sick missionaries"). ca20 spot-checked: no drift.
