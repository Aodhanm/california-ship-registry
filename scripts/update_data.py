#!/usr/bin/env python3
"""Safely refresh the data embedded in index.html after a data change.

WHY THIS EXISTS. index.html is a hand-maintained page (its About/source apparatus,
figures, and CSS were tuned by hand and have diverged from build_site.py, which is
quarantined). The ONLY thing that changes on a data edit is the embedded JSON. This
script updates exactly that and NOTHING else: it splices the current visits/ships
arrays into the existing index.html between the known markers, leaving every byte of
hand-written HTML untouched. It therefore cannot regress the prose the way a full
regenerate can. This is the supported way to update the site after editing data.

Guarded: refuses to run unless scripts/check.py passes (HARD 0), so bad data never
reaches the page. Verifies the spliced arrays re-parse before writing.
"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, 'index.html')

# 1. guards must pass
if subprocess.run([sys.executable, os.path.join(HERE, 'check.py')]).returncode != 0:
    sys.exit('GUARDS FAILED, index.html NOT updated')

# 2. load + serialize exactly as the page expects (same shape build_site.py used)
visits = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'visits.csv'))))
for v in visits:
    v['n_records'] = int(v['n_records'])
    v['citations'] = json.loads(v['citations'])
ships = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'ships.csv'))))
Vj = json.dumps(visits, ensure_ascii=False, separators=(',', ':'))
Sj = json.dumps(ships,  ensure_ascii=False, separators=(',', ':'))

# 3. splice ONLY the V and S arrays, between their literal markers
html = open(INDEX).read()
try:
    a = html.index('const V=') + len('const V=')
    b = html.index(';const S=', a)
    c = b + len(';const S=')
    d = html.index(';const G=', c)
except ValueError:
    sys.exit('markers not found (const V= / ;const S= / ;const G=) — index.html structure changed; splice aborted')
new = html[:a] + Vj + html[b:c] + Sj + html[d:]

# 4. verify the spliced arrays re-parse before writing
if len(json.loads(new[a:new.index(';const S=', a)])) != len(visits):
    sys.exit('post-splice V array did not re-parse to the expected length; aborted')

open(INDEX, 'w').write(new)
print(f'index.html data refreshed: {len(visits)} visits, {len(ships)} ships (hand-written HTML untouched)')
