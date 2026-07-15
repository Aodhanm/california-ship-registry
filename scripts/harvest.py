#!/usr/bin/env python3
"""Ship-registry Phase 0 harvester (2026-07-14).

Seeds ships-draft.csv + visits-draft.csv from the Archives of California
calendar (ca-catalog-export.json). Every output row is status=draft: this is
recall-oriented seeding for human review, not the registry. Two passes:
pass 1 collects ship names that appear adjacent to a vessel-type word;
pass 2 finds all occurrences of those names across the whole calendar
(italic/quoted), so records that mention a known ship without a type word
still seed a row. Citations = the C-A record itself (volume, doc, scan, url).
"""
import json, re, csv, os, sys, unicodedata, collections

CAT_PATH = os.path.expanduser('~/archives-of-california/ca-catalog-export.json')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

TYPE_WORDS = (r'fragata|balandra|bergant[ií]n|goleta|corbeta|nav[ií]o|paquebote?|'
              r'buque|embarcaci[oó]n|lancha|falucho|schooner|brig(?:antine)?|'
              r'frigate|sloop|corvette|bark|barque|ship|vessel|whaler|transport')
SHIPVOCAB = re.compile(r'\b(?:' + TYPE_WORDS + r'|arribada)\b', re.I)

# name adjacent to a type word (allowing a nationality adjective between),
# quoted with * ' " “ ‘ or unquoted-capitalized
NATION = (r"(?:american[ao]?|rus[ao]|inglés|inglesa|english|british|español[a]?|"
          r"spanish|mexican[ao]?|frances[a]?|french|de\s+S\.?\s*M\.?|de\s+guerra)")
NAME_AFTER_TYPE = re.compile(
    r'\b(?:' + TYPE_WORDS + r')\s+(?:' + NATION + r')?\s*'
    r'[*\'"“‘]{1,2}([A-ZÁÉÍÓÚÑ][\w\'. áéíóúñü-]{1,28}?)[*\'"”’]', re.I)
NAME_TYPE_AFTER = re.compile(   # "the Princesa frigate" is rare; "Goleta 'X'" covered above
    r'[*\'"“‘]{1,2}([A-ZÁÉÍÓÚÑ][\w\'. áéíóúñü-]{1,28}?)[*\'"”’]\s*'
    r'(?:\((?:[^)]*)\)\s*)?(?:,?\s*(?:' + NATION + r'))?\s*(?:' + TYPE_WORDS + r')', re.I)

FLAG_HINTS = [
    ('russia', re.compile(r'\brus[ao]s?\b|\brussian\b|\bRAC\b|\bSitka\b|\bRoss\b', re.I)),
    ('usa', re.compile(r'american[ao]?s?\b|\bboston\b|\banglo[- ]?american', re.I)),
    ('britain', re.compile(r'\bingl[eé]s[a]?\b|\binglesa\b|\benglish\b|\bbritish\b|\bNoroeste\b|\bNW Company\b', re.I)),
    ('spain', re.compile(r'\bespañol[a]?\b|\bde S\.? ?M\.?\b|\bSan Blas\b|\breal servicio\b', re.I)),
    ('mexico', re.compile(r'\bmexican[ao]\b', re.I)),
    ('france', re.compile(r'\bfrances[a]?\b|\bfrench\b', re.I)),
]
PURPOSE_HINTS = [
    ('otter', re.compile(r'nutria|otter|peleter|baidark|cayuco', re.I)),
    ('contraband', re.compile(r'contraband|smuggl', re.I)),
    ('supply', re.compile(r'v[ií]veres|memoria[s]?\b|auxilio|maíz|situado|supply|supplies|cargamento', re.I)),
    ('exploration', re.compile(r'expedici[oó]n|exploring|survey|reconoc', re.I)),
    ('whaler', re.compile(r'ballener|whal', re.I)),
    ('warship', re.compile(r'de guerra|warship|corsario|privateer|navy|escuadra', re.I)),
]
OUTCOME_HINTS = [
    ('seized', re.compile(r'apres[oó]|apresad|seiz|confiscat|captur', re.I)),
    ('wrecked', re.compile(r'naufrag|wreck|varad|encall', re.I)),
    ('deserters', re.compile(r'desert', re.I)),
    ('refused', re.compile(r'se le neg|refus|desatendid|no sean admitidos', re.I)),
    ('arrived', re.compile(r'arribada|arrib[oó]|llegada|lleg[oó]|entrada|anchor|arr\b', re.I)),
    ('departed', re.compile(r'salida|sali[oó]|zarp|sailed|departure', re.I)),
]
BAJA = re.compile(r'Loreto|Baja Cal|Antigua Cal|San Jos[eé] del Cabo|Todos Santos|Santo Domingo|San Vicente|San Quint[ií]n|frontera|Comond[uú]|Rosario\b', re.I)

# known-identity aliases (verbatim variants -> cluster key); grow by hand
ALIAS = {
 'mercurio': 'mercury', 'mercury': 'mercury',
 'sowaroff': 'suvorov', 'suvorov': 'suvorov', 'suworow': 'suvorov',
 'aranzazu': 'aranzazu', 'aranzazú': 'aranzazu', 'arànzazu': 'aranzazu',
 'horcasitas': 'orcasitas', 'orcasitas': 'orcasitas',
 'valdez': 'valdes', 'valdés': 'valdes',
 'santa saturnina': 'saturnina', 'saturnina': 'saturnina',
 'erminia': 'ilmen[?]',   # probable Savage rendering of Il'mena — UNCONFIRMED, keep flagged
 'lelia bird': 'lelia byrd', 'lelia byrd': 'lelia byrd',  # Savage spells her 'Bird'

}
STOP_NAMES = {  # italic/quoted tokens that are NOT ships (false-positive guard)
 'california', 'californias', 'sobre', 'reglamento', 'diputación', 'diputacion',
 'san blas', 'monterey', 'monterrey', 'la paz',
}

def norm(name):
    n = unicodedata.normalize('NFD', name.lower().strip(' .*'))
    n = ''.join(c for c in n if unicodedata.category(c) != 'Mn')
    n = re.sub(r'\s+', ' ', n)
    return ALIAS.get(n, ALIAS.get(name.lower().strip(), n))

def main():
    CAT = json.load(open(CAT_PATH))
    # ---------- pass 1: type-adjacent names ----------
    names = collections.Counter()
    for r in CAT:
        blob = ' '.join(str(r.get(k) or '') for k in ('title', 'summary'))
        for pat in (NAME_AFTER_TYPE, NAME_TYPE_AFTER):
            for m in pat.finditer(blob):
                nm = m.group(1).strip()
                if norm(nm) in STOP_NAMES or len(nm) < 3: continue
                names[nm] += 1
    clusters = collections.defaultdict(lambda: collections.Counter())
    for nm, c in names.items(): clusters[norm(nm)][nm] += c
    known = set(clusters.keys())
    # broad finder for pass 2: any italic/quoted token that normalizes to a known ship
    QUOTED = re.compile(r'[*\'"“‘]{1,2}([A-ZÁÉÍÓÚÑ][\w\'. áéíóúñü-]{1,28}?)[*\'"”’]')

    # ---------- pass 2: visit rows ----------
    visits = []
    vid = 0
    for r in CAT:
        blob = ' '.join(str(r.get(k) or '') for k in ('title', 'summary', 'place'))
        found = set()
        for m in QUOTED.finditer(blob):
            nm = m.group(1).strip()
            k = norm(nm)
            if k in known and k not in STOP_NAMES: found.add((nm, k))
        has_vocab = bool(SHIPVOCAB.search(blob))
        if not found and not has_vocab: continue
        flags = [f for f, p in FLAG_HINTS if p.search(blob)]
        purps = [f for f, p in PURPOSE_HINTS if p.search(blob)]
        outs = [f for f, p in OUTCOME_HINTS if p.search(blob)]
        region = 'baja?' if BAJA.search(blob) else 'alta'
        base = dict(
            date=str(r.get('doc_date') or r.get('year') or ''),
            date_confidence=str(r.get('date_confidence') or ''),
            place_raw=str(r.get('place') or ''), region_guess=region,
            flag_hints='|'.join(flags), purpose_hints='|'.join(purps),
            outcome_hints='|'.join(outs),
            ca_volume=r['ca_volume'], doc_id=r['doc_id'],
            scan=str(r.get('scan') or ''), ia_url=str(r.get('ia_url') or ''),
            excerpt=re.sub(r'\s+', ' ', str(r.get('summary') or ''))[:120],
            status='draft')
        if found:
            for nm, k in sorted(found):
                vid += 1
                visits.append(dict(draft_id=f'p0-{vid:04d}', ship_name_raw=nm,
                                   ship_cluster=k, **base))
        else:
            vid += 1
            visits.append(dict(draft_id=f'p0-{vid:04d}', ship_name_raw='',
                               ship_cluster='(unnamed vessel)', **base))

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'ships-draft.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['cluster', 'variants (count)', 'total mentions'])
        for k, vs in sorted(clusters.items(), key=lambda x: -sum(x[1].values())):
            w.writerow([k, '; '.join(f'{n} ({c})' for n, c in vs.most_common()),
                        sum(vs.values())])
    cols = list(visits[0].keys())
    with open(os.path.join(OUT, 'visits-draft.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for v in visits: w.writerow(v)

    named = [v for v in visits if v['ship_name_raw']]
    print(f"ship clusters: {len(clusters)} | visit draft rows: {len(visits)} "
          f"({len(named)} named / {len(visits)-len(named)} unnamed-vessel)")
    print("top clusters:", [(k, sum(v.values())) for k, v in
          sorted(clusters.items(), key=lambda x: -sum(x[1].values()))[:15]])
    marquee = ['mercury', 'suvorov', 'rurik', 'juno', 'princesa', 'ilmen[?]',
               'concepcion', 'san carlos', 'lelia byrd', 'flora', 'columbia']
    print("marquee spot-check:")
    for m in marquee:
        n = sum(1 for v in visits if v['ship_cluster'] == m)
        print(f"  {m:12s} {n:3d} draft rows")

if __name__ == '__main__':
    main()
