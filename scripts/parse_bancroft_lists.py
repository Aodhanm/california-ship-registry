#!/usr/bin/env python3
"""Parse Bancroft's 'List of vessels in Californian ports' sections from the clean scans.

Entry format, alphabetical:
    Adam, Amer. ship, 296 tons; Daniel Fallon, master; at S. Francisco in Oct. 1826.
    Alert, Amer. ship, 342 tons; Faucon, master, ...; Bryant & Sturgis, owners; ...

Anchor on the '<n> tons' tokens, which only occur inside these lists, then walk back to
the entry's opening name. That is far more robust than trying to match section headings,
which the OCR mangles.
"""
import re, pathlib, json, collections

FLAG = [(r'\bAmer\b|\bAm\.\b|American', 'usa'), (r'\bMex\b|Mexican', 'mexico'),
        (r'\bEngl?\b|British|\bBrit\b', 'britain'), (r'\bRuss\b|Russian', 'russia'),
        (r'\bFrench?\b|\bFr\.\b', 'france'), (r'\bSpan\b|Spanish', 'spain'),
        (r'\bHawaii|Sandwich|\bHawn\b', 'hawaii'), (r'\bChil', 'chile'), (r'\bPeruv', 'peru')]
TYPE = r'ship|brig|bark|barque|schr|schooner|sloop|whaler|steamer|frigate|launch|corvette|pilot-boat'

def parse(path, vol):
    t = pathlib.Path(path).read_text(errors='ignore')
    t = re.sub(r'-\s*\n\s*', '', t); t = re.sub(r'\s+', ' ', t)
    out = []
    for m in re.finditer(r'\b(\d{2,4})\s*tons\b', t):
        head = t[max(0, m.start()-170): m.start()]
        # the entry begins after the previous sentence end; take the last such break
        parts = re.split(r'(?<=[.;])\s+(?=[A-ZÁÉÍÓÚÑ])', head)
        cand = parts[-1] if parts else head
        nm = re.match(r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑá-úñ'\.\- ]{1,26}?)\s*,", cand)
        if not nm: continue
        name = re.sub(r'\s+', ' ', nm.group(1)).strip(' .-')
        if not (2 < len(name) < 28) or len(name.split()) > 3: continue
        if re.match(r'^(The|And|Of|At|In|On|List|Vessels|Amer|Mex|Engl|Russ)$', name, re.I): continue
        tail = t[m.start(): m.start()+230]
        ctx  = cand + ' ' + tail
        flag = next((f for p, f in FLAG if re.search(p, ctx, re.I)), '')
        typ  = (re.search(TYPE, ctx, re.I) or [None]) and (re.search(TYPE, ctx, re.I).group(0).lower() if re.search(TYPE, ctx, re.I) else '')
        mast = re.search(r'([A-Z][A-Za-z\'\.\- ]{2,26}),\s*master', tail)
        yrs  = sorted(set(re.findall(r'\b(18[0-4]\d)\b', tail)))
        ports= sorted(set(re.findall(r'\b(?:S\.|San|Sta|Santa|Monterey|Bodega|Sausalito)\s*[A-ZÁ][a-zá-ú]+|Monterey|Bodega', tail)))
        out.append({'vol': vol, 'name': name, 'tons': int(m.group(1)), 'flag': flag,
                    'type': typ, 'master': mast.group(1).strip() if mast else '',
                    'years': yrs, 'ports': ports[:4]})
    # dedupe on name+tons
    seen = {}
    for r in out: seen.setdefault((r['name'].lower(), r['tons']), r)
    return list(seen.values())

ALL = []
for vol, f in [('III','ia-v03.txt'), ('IV','ia-v04.txt'), ('V','ia-v05.txt')]:
    rows = parse(f, vol)
    print(f"vol {vol}: {len(rows)} vessel entries with tonnage")
    ALL += rows
print(f"\nTOTAL: {len(ALL)} entries")
print("  with a flag:  ", sum(1 for r in ALL if r['flag']))
print("  with a master:", sum(1 for r in ALL if r['master']))
print("  with years:   ", sum(1 for r in ALL if r['years']))
print("  flags:", dict(collections.Counter(r['flag'] or ', ' for r in ALL).most_common()))
json.dump(ALL, open('banc-vessel-entries.json','w'), ensure_ascii=False, indent=1)
print("\nsample:")
for r in sorted(ALL, key=lambda r: r['name'])[:14]:
    print(f"  {r['name']:22s} {r['tons']:>4d}t {r['flag']:8s} {r['type']:9s} {r['master'][:20]:20s} {','.join(r['years'][:3])}")
