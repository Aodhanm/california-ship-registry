#!/usr/bin/env python3
"""Build guards (v0.2). Hard failures block the site build; warnings print.
1. schema/vocab vs the codebook  2. every row >=1 parseable citation
3. date sanity  4. dedup (same ship+anchorage+overlapping span w/o note) -> warn
"""
import csv, json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS = {'', 'spain', 'usa', 'russia', 'britain', 'mexico', 'france', 'hawaii', 'chile', 'peru', 'ecuador', 'argentina'}
VTYPES = {'port-call', 'port-call?', 'offshore-presence', 'resident', 'sighting',
          'reported?', 'mention', 'unlocated'}
STATUS = {'draft', 'reviewed', 'verified'}
# Sunk phantoms — non-ships adjudicated out (2026-07-27, see FALSE-POSITIVE-REGISTER.md).
# A HARD guard so a re-harvest or stray row can never re-mint them. Read the Bancroft
# text: each of these is a place / month / demonym / person / policy, not a hull.
DROPPED_SHIP_IDS = {
    # HoC narrative-sweep homonyms
    'california', 'june', 'fernando', 'american', 'sitka', 'trinidad',
    'times', 'henry', 'friend', 'edward', 'tartar',
    # C-A / print-list phantoms (policy bundles, person-names, mis-parses)
    'congreso mejicano', 'don', 'adela', 'grafton', 'la paloma', 'spray',
    'hebe', 'tagle', 'caminante', 'rita', 'rosalia', 'neptuno', 'peruano',
    # 2026-07-27 OCR garbles: merged into a real ship (must not re-mint as their own row)
    'actwo', 'actwwo', 'chirtkov', 'iimen', 'taaso', 'loussa', 'maraquita',
    'fetvorite', 'guadidupc', 'elizabeih', 'vafidalia', 'plowhoij', 'liclipse', 'oajaca',
    # 2026-07-27 unrecoverable print-list garbles (no confident reading — asserted nothing)
    'oivvi', 'panjir', 'xylon', 'suxden', 'suaanita', 'toidon', 'nadednik', 'apoho',
    # 2026-07-27 queue-resolution drops (mis-parses / place-names)
    'net-siut','tester','vinas','san francisco','santa barbara','bruja','reisos','ynez','cadiac','la elisa','tic-me-mash','javier sartar','diga',
    # 2026-08-04 phantom purge: the 1767 Cadiz Juno (never in CA; distinct from the 1806 Russian Juno)
    'juno-1767',
}
# 2026-08-04: C-A records adjudicated as NON-ship documents (policy/person/no-hull; see
# FALSE-POSITIVE-REGISTER.md). A re-harvest must not re-mint visits from them.
DROPPED_CA_RECORDS = {
    ('1','2'), ('4','141'), ('4','187'), ('6','87'), ('13','103'), ('14','191'),
    ('15','173'), ('16','34'), ('16','467'), ('17','334'), ('18','22'), ('18','32'),
    ('18','388'), ('20','254'), ('22','2044'), ('46','107'), ('48','82'),
    ('55','208'), ('63','433'),
}
# First documented arrival per flag, leaf-verified (FIRSTS.md). A flagged visit dated
# provably BEFORE its nation's first hull in California is a phantom or a mis-flag.
# Precision-aware: a bare '1796' does not violate the '1796-10-29' floor; '1796-05' does.
FLAG_FLOORS = {
    'spain':   '1769',        # San Carlos / San Antonio, San Diego 1769 (registry scope opens)
    'france':  '1786-09',     # Laperouse's Boussole & Astrolabe, Monterey, Sept 1786
    'britain': '1792-11-13',  # Vancouver's Discovery, San Francisco (C-A 54 d1077 leaf-verified)
    'usa':     '1796-10-29',  # Otter (Dorr), Monterey (HoC I + C-A 24 leaf-verified)
    'russia':  '1806-04-08',  # Juno (Rezanov), San Francisco (C-A 12 d100 leaf-verified)
    'mexico':  '1822',        # adhesion year; first flag-confirmed hull = Morelos 1825
}
def _before_floor(date, floor):
    """True only if `date` is provably earlier than `floor` at its own precision."""
    if not date: return False
    dp, fp = date.split('-'), floor.split('-')
    for a, b in zip(dp, fp):
        if a < b: return True
        if a > b: return False
    return False  # equal at the row's precision -> not provably before
hard, warn = [], []
rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'visits.csv'))))
seen_ids = set()
spans = {}
for r in rows:
    vid = r['visit_id']
    if r['ship_id'] in DROPPED_SHIP_IDS:
        hard.append(f"{vid}: sunk-phantom ship_id {r['ship_id']!r} — a non-ship; must not be re-minted")
    if vid in seen_ids: hard.append(f"duplicate visit_id {vid}")
    seen_ids.add(vid)
    if r['flag'] not in FLAGS: hard.append(f"{vid}: bad flag {r['flag']!r}")
    if r['visit_type'] not in VTYPES: hard.append(f"{vid}: bad visit_type {r['visit_type']!r}")
    if r['status'] not in STATUS: hard.append(f"{vid}: bad status {r['status']!r}")
    # sightings/mentions/reports may legitimately precede a first PORT entry (e.g. the
    # Otter sighted offshore May 1796); port-level visit types may not.
    if (r['flag'] in FLAG_FLOORS and r['visit_type'] not in ('sighting', 'reported?', 'mention')
            and _before_floor(r['date_from'], FLAG_FLOORS[r['flag']])):
        hard.append(f"{vid}: flag {r['flag']!r} dated {r['date_from']} — before that nation's first "
                    f"documented hull in California ({FLAG_FLOORS[r['flag']]}); phantom or mis-flag")
    try:
        c = json.loads(r['citations'])
        if not c: hard.append(f"{vid}: no citations")
        for cit in c:
            if cit.get('type') == 'ca-record' and (str(cit.get('ca')), str(cit.get('doc'))) in DROPPED_CA_RECORDS:
                hard.append(f"{vid}: cites C-A {cit['ca']} d{cit['doc']} — adjudicated a non-ship record; must not be re-minted")
            # 2026-08-04 Loo Choo lesson: the Ogden harvest attached swallowed entries' schedule
            # lines to the wrong vessel. An Ogden citation's own entry label ("s.v. 'Name, YEARS'")
            # must contain the visit's year (+/-1 for season overlap).
            if cit.get('type') == 'ogden' and r['date_from'][:4].isdigit():
                m = re.search(r"s\.v\. '[^']+?,\s*([0-9][0-9\-, ]*)'", cit.get('ref', ''))
                if m:
                    yrs = set()
                    for a, b in re.findall(r'(\d{4})(?:-(\d{2,4}))?', m.group(1)):
                        a = int(a); b = int(b) if len(b) == 4 else (int(str(a)[:2] + b) if b else a)
                        yrs.update(range(a, b + 1))
                    vy = int(r['date_from'][:4])
                    if yrs and not (min(yrs) - 1 <= vy <= max(yrs) + 1):
                        hard.append(f"{vid}: dated {vy} but its Ogden entry covers {sorted(yrs)} — mis-attached schedule line")
    except Exception:
        hard.append(f"{vid}: unparseable citations")
    for d in (r['date_from'], r['date_to']):
        if d and not (d[:4].isdigit() and 1500 <= int(d[:4]) <= 1850):
            hard.append(f"{vid}: bad date {d!r}")
    if r['date_from'] and r['date_to'] and r['date_from'][:4] > r['date_to'][:4]:
        hard.append(f"{vid}: date_from > date_to")
    if r['ship_id'] != '(unnamed vessel)' and r['anchorage'] and r['date_from']:
        k = (r['ship_id'], r['anchorage'], r['date_from'][:4])
        if k in spans and not r['sources_disagree']:
            warn.append(f"{vid}: possible dup of {spans[k]} ({k})")
        spans[k] = vid
print(f"guards: {len(rows)} rows | HARD {len(hard)} | warn {len(warn)}")
for h in hard[:15]: print("  HARD:", h)
if warn: print(f"  (first warns) " + "; ".join(warn[:5]))
if hard: sys.exit(1)
