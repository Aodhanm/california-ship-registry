#!/usr/bin/env python3
"""Build guards (v0.2). Hard failures block the site build; warnings print.
1. schema/vocab vs the codebook  2. every row >=1 parseable citation
3. date sanity  4. dedup (same ship+anchorage+overlapping span w/o note) -> warn
"""
import csv, json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS = {'', 'spain', 'usa', 'russia', 'britain', 'mexico', 'france'}
VTYPES = {'port-call', 'port-call?', 'offshore-presence', 'resident', 'sighting',
          'reported?', 'mention', 'unlocated'}
STATUS = {'draft', 'reviewed', 'verified'}
hard, warn = [], []
rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'visits.csv'))))
seen_ids = set()
spans = {}
for r in rows:
    vid = r['visit_id']
    if vid in seen_ids: hard.append(f"duplicate visit_id {vid}")
    seen_ids.add(vid)
    if r['flag'] not in FLAGS: hard.append(f"{vid}: bad flag {r['flag']!r}")
    if r['visit_type'] not in VTYPES: hard.append(f"{vid}: bad visit_type {r['visit_type']!r}")
    if r['status'] not in STATUS: hard.append(f"{vid}: bad status {r['status']!r}")
    try:
        c = json.loads(r['citations'])
        if not c: hard.append(f"{vid}: no citations")
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
