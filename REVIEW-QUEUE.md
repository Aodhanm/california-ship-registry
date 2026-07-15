# Review queue — uncertain ship identities (2026-07-15 vigilance pass)

*The confident merges/drops are applied (see harvest.py ALIAS + STOP_NAMES). These need a human ruling or a source check. Add rulings here; the alias table encodes them.*

## Identity conflations to split
- **descubierta** — the cluster mixes Malaspina's corvette *Descubierta* (Monterey 1791) with Savage's rendering of Vancouver's *Discovery* as "Fragata Descubierta" (the 1793 reservadísima!). Split by date/context: 1791 = Malaspina; 1792–94 = Vancouver.
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
