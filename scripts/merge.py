#!/usr/bin/env python3
"""Phase 1a merge pass (2026-07-14): collapse the Phase-0 draft rows into
visit-level rows + the ships table + the anchorage gazetteer.

Conservative merge rule: two draft rows describe the SAME visit only when they
share the ship, the year, and (when both have one) the month and the anchorage.
Everything else stays separate — over-splitting is honest (a reviewer merges),
over-merging is silent data loss. Every visit keeps ALL constituent citations.
Adjudications encoded from the plan: the two Junos split by era; the 'William
Shaler' cluster re-identified as the Lelia Byrd (the record names her master);
'[Erminia?]' stays flagged. All rows keep status=draft until reviewed.
"""
import csv, os, re, json, collections, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')

# ---- adjudications (plan §1a) ----
def adjudicate(cluster, year):
    if cluster == 'juno':
        try: y = int(str(year)[:4])
        except ValueError: y = 0
        return 'juno-1767' if y and y < 1800 else 'juno-rac'
    if cluster == 'william shaler':
        return 'lelia byrd'    # ca12-d73 names the master as the vessel
    return cluster

# ---- gazetteer: canonical anchorages (name variants -> canonical, lat, lon) ----
GAZ = [
 ('Monterey',      ['monterey', 'monterrey', 'mont.'],               36.603, -121.892),
 ('San Francisco', ['san francisco', 's. francisco', 'sn francisco', 'yerba buena', 's.n fran.co'], 37.808, -122.465),
 ('San Diego',     ['san diego', 's. diego', 'sn diego'],            32.714, -117.173),
 ('Santa Bárbara', ['santa barbara', 'sta barbara', 'sta. barbara', 's.ta barbara'], 34.408, -119.685),
 ('San Pedro',     ['san pedro', 's. pedro'],                        33.712, -118.280),
 ('Refugio',       ['refugio'],                                      34.462, -120.070),
 ('Bodega',        ['bodega', 'puerto de la bodega'],                38.308, -123.049),
 ('San Luis Obispo', ['san luis obispo', 's. luis obispo', 'slo'],   35.178, -120.735),
 ('Santa Cruz',    ['santa cruz', 'sta cruz', 'branciforte'],        36.960, -122.023),
 ('San Juan Capistrano', ['san juan capistrano', 's. juan capistrano'], 33.460, -117.680),
 ('Santa Catalina I.', ['santa catalina', 'sta catalina', 'catalina'], 33.396, -118.421),
 ('Loreto',        ['loreto'],                                       26.010, -111.343),
 ('San Blas',      ['san blas', 's. blas', 'sn blas'],               21.540, -105.285),
 ('Cabo San Lucas',['cabo san lucas', 'san lucas'],                  22.880, -109.912),
 ('San Quintín',   ['san quintin', 's. quintin', 'santa quintin'],   30.398, -115.996),
 ('Fort Ross',     ['ross', 'fuerte de ross'],                       38.514, -123.245),
 ('Sitka',         ['sitka', 'nueva arcangel', 'new archangel'],     57.053, -135.335),
]
def gaz_lookup(place):
    p = unicodedata.normalize('NFD', str(place).lower())
    p = ''.join(c for c in p if unicodedata.category(c) != 'Mn')
    for canon, variants, lat, lon in GAZ:
        for v in variants:
            if v in p: return canon
    return ''

def month_of(datestr):
    m = re.match(r'(\d{4})-(\d{2})', str(datestr))
    return m.group(2) if m else ''
def year_of(datestr):
    m = re.match(r'(\d{4})', str(datestr))
    return m.group(1) if m else ''

def main():
    rows = list(csv.DictReader(open(os.path.join(DATA, 'visits-draft.csv'))))
    for r in rows:
        r['ship_cluster'] = adjudicate(r['ship_cluster'], r['date'])
        r['anchorage'] = gaz_lookup(r['place_raw'] or r['excerpt'])
    named = [r for r in rows if r['ship_name_raw']]
    unnamed = [r for r in rows if not r['ship_name_raw']]

    groups = collections.defaultdict(list)
    for r in named:
        key = (r['ship_cluster'], year_of(r['date']), month_of(r['date']) or '?',
               r['anchorage'] or '?')
        groups[key].append(r)
    # second-stage: fold month='?' rows into a same-year+anchorage dated group
    merged = {}
    for key, g in sorted(groups.items()):
        cl, yr, mo, anc = key
        if mo == '?' :
            for (c2, y2, m2, a2), tgt in merged.items():
                if c2 == cl and y2 == yr and m2 != '?' and (anc in ('?', a2)):
                    tgt.extend(g); g = None; break
        if g is not None: merged[key] = list(g)

    visits = []
    def mk_visit(cluster, g, named_flag):
        dates = sorted(x['date'] for x in g if x['date'])
        cites = [dict(type='ca-record', ca=x['ca_volume'], doc=x['doc_id'],
                      scan=x['scan'], url=x['ia_url']) for x in g]
        anc = next((x['anchorage'] for x in g if x['anchorage']), '')
        flags = collections.Counter(f for x in g for f in x['flag_hints'].split('|') if f)
        purs = collections.Counter(f for x in g for f in x['purpose_hints'].split('|') if f)
        outs = collections.Counter(f for x in g for f in x['outcome_hints'].split('|') if f)
        region = 'baja' if all(x['region_guess'] == 'baja?' for x in g) else \
                 ('alta/baja?' if any(x['region_guess'] == 'baja?' for x in g) else 'alta')
        return dict(
            ship_id=cluster,
            name_as_written='; '.join(sorted({x['ship_name_raw'] for x in g if x['ship_name_raw']})),
            date_from=dates[0] if dates else '', date_to=dates[-1] if dates else '',
            date_confidence='mixed' if len({x['date_confidence'] for x in g}) > 1
                            else (g[0]['date_confidence'] or ''),
            anchorage=anc, region=region,
            flag=flags.most_common(1)[0][0] if flags else '',
            purpose='|'.join(k for k, _ in purs.most_common(3)),
            outcome='|'.join(k for k, _ in outs.most_common(3)),
            n_records=len(g),
            citations=json.dumps(cites, ensure_ascii=False),
            excerpt=max((x['excerpt'] for x in g), key=len),
            visit_type='port-call?' if anc else 'unlocated',
            status='draft', sources_disagree='')
    for (cl, yr, mo, anc), g in merged.items():
        visits.append(mk_visit(cl, g, True))
    for r in unnamed:
        visits.append(mk_visit('(unnamed vessel)', [r], False))
    visits.sort(key=lambda v: (v['date_from'] or '9999', v['ship_id']))
    for i, v in enumerate(visits, 1): v['visit_id'] = f'v{i:04d}'

    # ships table
    ships = collections.defaultdict(lambda: dict(variants=collections.Counter(),
                                                 first='9999', last='0000', n=0,
                                                 flags=collections.Counter()))
    for v in visits:
        if v['ship_id'] == '(unnamed vessel)': continue
        srec = ships[v['ship_id']]
        for nm in v['name_as_written'].split('; '):
            if nm: srec['variants'][nm] += 1
        if v['date_from']: srec['first'] = min(srec['first'], v['date_from'][:4])
        if v['date_to']: srec['last'] = max(srec['last'], v['date_to'][:4])
        srec['n'] += 1
        if v['flag']: srec['flags'][v['flag']] += 1

    cols = ['visit_id', 'ship_id', 'name_as_written', 'date_from', 'date_to',
            'date_confidence', 'anchorage', 'region', 'flag', 'purpose',
            'outcome', 'visit_type', 'n_records', 'excerpt', 'citations',
            'sources_disagree', 'status']
    with open(os.path.join(DATA, 'visits.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for v in visits: w.writerow(v)
    with open(os.path.join(DATA, 'ships.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ship_id', 'name_variants', 'flag_guess', 'first_seen',
                    'last_seen', 'n_visits', 'status'])
        for k, s in sorted(ships.items()):
            w.writerow([k, '; '.join(f'{n} ({c})' for n, c in s['variants'].most_common()),
                        s['flags'].most_common(1)[0][0] if s['flags'] else '',
                        s['first'] if s['first'] != '9999' else '',
                        s['last'] if s['last'] != '0000' else '', s['n'], 'draft'])
    with open(os.path.join(DATA, 'gazetteer.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anchorage', 'variants', 'lat', 'lon'])
        for canon, variants, lat, lon in GAZ:
            w.writerow([canon, '; '.join(variants), lat, lon])

    named_v = [v for v in visits if v['ship_id'] != '(unnamed vessel)']
    print(f"visits: {len(visits)} ({len(named_v)} named-ship, "
          f"{len(visits)-len(named_v)} unnamed) | ships: {len(ships)} | "
          f"anchorage located: {sum(1 for v in visits if v['anchorage'])}")
    per = collections.Counter(v['date_from'][:3]+'0s' for v in visits if v['date_from'])
    print("visits by decade:", dict(sorted(per.items())))

if __name__ == '__main__':
    main()
