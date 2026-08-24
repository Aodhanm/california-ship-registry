#!/usr/bin/env python3
"""One-off, auditable flag-defect fix for the DOI-readiness pass (2026-08-24).

Context: the Phase-0 harvester defaulted Spanish-LANGUAGE records to flag=spain.
That produced 43 rows dated 1822+ flagged `spain`, which is provably wrong: Spain
had no California trade after independence and Bancroft records zero Spanish vessels
in HoC III-V. This script corrects them PER ROW from each row's own excerpt / a
verbatim Bancroft entry, never by blanket inference:

  * chile   - Lord Cochrane's insurgent (Chilean) navy vessels, named as such.
  * mexico  - vessels shown in Mexican national service (San Blas mail/supply,
              "brig mexicano", Mexican-Empire commissioner) or settled by Bancroft.
  * britain - Ayacucho 1830 = "Engl. brig, Joseph Snook" (Bancroft HoC III, verbatim).
  * spain   - KEPT only for the genuine last Spanish-naval presence (the Asia
              capitulation, 1825) + one reported Spanish-warship threat (a mention).
  * ''      - blank where `spain` is wrong but no source settles the real flag
              (honest "undetermined" - the dataset's stated ethic is to publish its refusals).

Two rows are dropped as place-as-ship phantoms (class 4 of the taxonomy), each
verbatim-confirmed: v1885 "el paraje San Antonio" (a land parcel), v2120 "una viña
llamada Sta Gertrudis" (a vineyard).

Also: cowlitz v1976 usa->britain (Bancroft: "Engl. bark, Wm Brotchie", HBC vessel).

Every change is listed below with its evidence. Run once; then check.py must pass.
"""
import csv, os, collections

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
VISITS = os.path.join(DATA, 'visits.csv')
SHIPS = os.path.join(DATA, 'ships.csv')

# visit_id -> (new_flag, reason)
FLAG = {
    # --- Chilean insurgent navy (Cochrane), named in the excerpt ---
    'v1242': ('chile', "Cochrane's insurgent squadron (Chilean navy) - La Independencia"),
    'v1243': ('chile', "Cochrane's privateers (Chilean navy) - brig El Alcion"),
    # --- Mexican national / San Blas service, or Bancroft-verified Mexican ---
    'v1249': ('mexico', "Mexican(Imperial) war-brig San Carlos, mid-1822"),
    'v1252': ('mexico', "war-brig San Carlos brought Imperial commissioner Fernandez, Aug 1822"),
    'v1397': ('mexico', "Mexican war-brig Morelos, San Blas ('save the Nation'); leaf-verified 1st Mexican-flag national vessel"),
    'v1503': ('mexico', "mail-schooner Matamoros, from San Blas (Loreto port register)"),
    'v1504': ('mexico', "sloop Sirena, from San Blas (Loreto port register)"),
    'v1569': ('mexico', "Maria Ester = 'Mex. brig, owned by Henry Virmond' (Bancroft HoC III, verbatim)"),
    'v1709': ('mexico', "schooner Mexicana, Mexican Loreto-San Diego mail"),
    'v1725': ('mexico', "Mexican brig Catalina (Monterey arrivals register 1830-31)"),
    'v1741': ('mexico', "schooner Margarita, Mexican govt transport (Padres expulsion to San Blas)"),
    'v1774': ('mexico', "Mexican brig Catalina (Snook), criminal case to San Blas"),
    'v1777': ('mexico', "'bergantin mexicano Catalina' (explicit)"),
    'v1783': ('mexico', "Catalina listed distinctly from 'Eng. Ayacucho' in the SD 1833 register - Mexican"),
    'v1786': ('mexico', "brig Catalina (Echeandia/Bandini departed on her)"),
    'v1797': ('mexico', "sloop Mariquita, San Blas/Guaymas (Mexican coaster)"),
    'v1915': ('mexico', "Clarita = 'Mex. bark, Chas Wolter' (Bancroft HoC IV, verbatim)"),
    'v1926': ('mexico', "brig Catalina (contraband arms case, Nov 1840)"),
    'v1932': ('mexico', "brig Catalina (duties applied to Virmond debt)"),
    'v2004': ('mexico', "brig Catalina (SD Castillo spiking, 1842)"),
    # --- Britain, Bancroft verbatim (whole-vessel identity applied to its stray flags) ---
    'v1679': ('britain', "Ayacucho 1830 = 'Engl. brig, 232t, Joseph Snook' (Bancroft HoC III, verbatim)"),
    'v1724': ('britain', "Ayacucho 1831 = same English brig (Bancroft ship identity); stray russia flag corrected"),
    'v1951': ('mexico', "Clarita 1841 = same Mexican bark (Bancroft ship identity); stray russia flag corrected"),
    'v1976': ('britain', "Cowlitz = 'Engl. bark, Wm Brotchie', HBC vessel (Bancroft HoC IV, verbatim)"),  # was usa, not spain
    # --- Blank: spain is wrong, no source settles the true flag ---
    'v1268': ('', "Ann - Ogden itinerary, flag undetermined"),
    'v1269': ('', "Ann - Ogden itinerary, flag undetermined"),
    'v1270': ('', "Ann - Ogden itinerary, flag undetermined"),
    'v1363': ('', "Nieves - 1825 supply-cargo mention, flag undetermined"),
    'v1376': ('', "unnamed Mazatlan/San Blas vessel mention, flag undetermined"),
    'v1496': ('', "unnamed - treasury duty statement, flag undetermined"),
    'v1621': ('', "unnamed - schooner Dolores dispatch, flag undetermined"),
    'v1680': ('', "Brookline - American per flag-audit, pending verbatim confirm"),
    'v1681': ('', "Leonor - flag undetermined (Mexican per flag-audit, unconfirmed)"),
    'v1682': ('', "Vitor - flag undetermined"),
    'v1683': ('', "Volunteer - American per flag-audit, pending verbatim confirm"),
    'v1752': ('', "unnamed - comandante's voyage account, flag undetermined"),
    'v1796': ('', "Legaspi - put in during storm bound San Blas, flag undetermined"),
    'v1910': ('', "unnamed - Graham-Affair narrative, flag undetermined"),
    'v1921': ('', "Leonidas - Graham deportation charter, flag undetermined (US vs Mex disputed)"),
    'v2048': ('', "Don Quijote - excerpt is a timber decree, ship support absent; blank + review"),
}
# visit_id -> (keep-flag) but reclassify as a mention so the port-call guard exempts it
VTYPE_MENTION = {
    'v1387': "abandoned 1792 Spanish exploration brig Sutil on the San Blas beach - a derelict mention, not an 1825 visit",
    'v1691': "reported Spanish warship threatening the coast (Mazatlan news) - a mention",
}
# genuine post-1821 spain PORT-CALLS, kept and allow-listed in check.py
KEEP_SPAIN_PORTCALL = {'v1389', 'v1393'}  # the Asia capitulation, Monterey 1825
# place-as-ship phantoms to drop (class 4), verbatim-confirmed
DROP = {
    'v1885': "'el paraje San Antonio' - a land parcel (SLO alcalde petition), not a vessel; C-A 63 d364",
    'v2120': "'una vina llamada Sta Gertrudis' - a vineyard at Mission San Buenaventura, not a vessel; C-A 63 d395",
}

rows = list(csv.DictReader(open(VISITS)))
cols = rows[0].keys()
changes, dropped = [], []
kept = []
for r in rows:
    vid = r['visit_id']
    if vid in DROP:
        dropped.append((vid, r['ship_id'], DROP[vid])); continue
    if vid in FLAG:
        newf, why = FLAG[vid]
        if r['flag'] != newf:
            changes.append((vid, r['ship_id'], r['flag'], newf, why)); r['flag'] = newf
    if vid in VTYPE_MENTION and r['visit_type'] != 'mention':
        changes.append((vid, r['ship_id'], r['visit_type']+'(vt)', 'mention', VTYPE_MENTION[vid]))
        r['visit_type'] = 'mention'
    kept.append(r)

# ships.csv flag_guess: set ONLY from this EXPLICIT verified map (no mode-recompute,
# which would regress ships that carry OTHER pre-existing bad flags, e.g. volunteer's
# 8 spurious russia visits). Ships not listed keep their current flag_guess.
# mexicana (1791-1831) and san carlos (1769-1822) are era-conflations kept at spain
# (the dominant Spanish exploration/packet vessel); their 1822/1831 reuse-of-name rows
# are correctly flagged at the VISIT level. Both are logged for a v1.1 ship split.
SHIP_FLAG = {
    'ayacucho': 'britain', 'cowlitz': 'britain',
    'maria ester': 'mexico', 'clarita': 'mexico', 'catalina': 'mexico',
    'matamoros': 'mexico', 'sirena': 'mexico', 'margarita': 'mexico',
    'mariquita': 'mexico', 'morelos': 'mexico',
    'la independencia': 'chile', 'el alcion': 'chile',
    'vitor': '', 'legaspi': '', 'don quijote': '',
}
by_ship = collections.defaultdict(list)
for r in kept:
    by_ship[r['ship_id']].append(r)
srows = list(csv.DictReader(open(SHIPS)))
scols = srows[0].keys()
sout, sdropped = [], []
for s in srows:
    sid = s['ship_id']
    if sid not in by_ship:                       # ship now has no visits -> drop it
        sdropped.append(sid); continue
    if sid in SHIP_FLAG and s['flag_guess'] != SHIP_FLAG[sid]:
        changes.append((f'SHIP:{sid}', sid, s['flag_guess'], SHIP_FLAG[sid], 'verified ship flag'))
        s['flag_guess'] = SHIP_FLAG[sid]
    s['n_visits'] = str(len(by_ship[sid]))
    sout.append(s)

with open(VISITS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(cols)); w.writeheader(); w.writerows(kept)
with open(SHIPS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(scols)); w.writeheader(); w.writerows(sout)

print(f"=== FLAG/VTYPE CHANGES ({len(changes)}) ===")
for vid, sid, old, new, why in changes:
    print(f"  {vid:10} {sid[:18]:18} {old or '(blank)':10} -> {new or '(blank)':10} | {why}")
print(f"\n=== DROPPED VISITS ({len(dropped)}) ===")
for vid, sid, why in dropped:
    print(f"  {vid} {sid} | {why}")
print(f"\n=== DROPPED SHIPS (now orphaned) ({len(sdropped)}) === {sdropped}")
print(f"\nvisits: {len(rows)} -> {len(kept)} | ships: {len(srows)} -> {len(sout)}")
print(f"KEEP_SPAIN_PORTCALL allowlist for check.py: {sorted(KEEP_SPAIN_PORTCALL)}")
