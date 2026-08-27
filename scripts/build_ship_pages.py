#!/usr/bin/env python3
"""Generate the static, crawlable layer of the California Ship Registry.

WHY THIS EXISTS. index.html is a single page that embeds every vessel and every
visit as JavaScript arrays, so 401 vessels and 2,072 visits share one URL and a
search engine can offer a reader nothing more specific than the front door. A
search for a named vessel (Aranzazu, Maria Ester) returns Islapedia and the
Maritime Heritage Project, which have a page per vessel, and not this registry,
which has better data. This script gives each vessel its own address.

IT NEVER TOUCHES index.html. That page is hand-maintained; scripts/build_site.py
is quarantined for exactly that reason, and scripts/update_data.py is the only
sanctioned way to refresh its embedded data. This script only READS
data/ships.csv and data/visits.csv, the same source those use, and writes into
ships/ plus sitemap.xml.

Usage:
    python3 scripts/build_ship_pages.py            # write into the repo
    python3 scripts/build_ship_pages.py /tmp/out   # dry run into a scratch dir
"""
import collections
import csv
import datetime
import html
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT
SITE = 'https://ships.archivesofcalifornia.com'
TODAY = datetime.date.today().isoformat()

# An aggregate bucket for visits whose vessel was never named. Not a vessel, so
# it gets no page of its own; its visits stay in the interactive registry.
AGGREGATE_IDS = {'(unnamed vessel)'}

FLAG_LABEL = {'spain': 'Spain', 'usa': 'United States', 'russia': 'Russia',
              'britain': 'Britain', 'mexico': 'Mexico', 'france': 'France',
              'hawaii': 'Hawaii', 'chile': 'Chile', 'peru': 'Peru',
              'ecuador': 'Ecuador', 'argentina': 'Argentina', '': 'not established'}

CITE_LABEL = {
    'ca-record': 'Archives of California (BANC MSS C-A)',
    'hoc': 'Bancroft, History of California',
    'hoc-list': 'Bancroft, History of California, vessel lists',
    'ogden': 'Ogden, The California Sea Otter Trade',
    'russian-attest': 'Russian-American Company records',
    'published-primary': 'Published primary source',
    'published-secondary': 'Published secondary source',
    'attested-secondary': 'Secondary attestation',
    'archival': 'Archival source',
    'primary-archival': 'Primary archival source',
}


def esc(s):
    return html.escape(str(s if s is not None else ''), quote=True)


def slugify(s):
    # Transliterate accents first. Without this "Aranzazu" with its acute becomes
    # "ar-nzazu", which is both an ugly URL and useless for the vessel-name
    # searches these pages exist to win.
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'x'


def write(relpath, text):
    p = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)


def primary_name(variants):
    """name_variants looks like "Princesa (71); La Princesa (1)"."""
    first = (variants or '').split(';')[0].strip()
    return re.sub(r'\s*\(\d+\)\s*$', '', first).strip() or first


CSS = """/* Static-page layer for the California Ship Registry. Tokens copied verbatim
   from index.html's inline theme so the generated pages match it. Emitted by
   scripts/build_ship_pages.py; do not edit by hand. */
:root{
  --deep:#0A141C; --ground:#0E1A24; --plate:#132330; --plate-2:#182936;
  --ink:#E2E8EC; --ink-soft:#A8BCC9; --ink-faint:#7E96A6;
  --rule:#223644; --rule-soft:#16242F;
  --accent:#5FA8C4; --accent-deep:#8FCDE2; --brass:#CBA64E;
  --ok:#6FB9AA; --warn:#D3A44A; --miss:#D9705F;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --body:Charter,Georgia,"Iowan Old Style",Cambria,serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--body);
  font-size:16px;line-height:1.55}
a{color:var(--accent-deep);text-decoration:none}
a:hover{text-decoration:underline}
header.top{background:var(--deep);border-bottom:1px solid var(--rule);padding:14px 22px;
  display:flex;align-items:baseline;gap:0 16px;flex-wrap:wrap}
header.top .wordmark{font-family:var(--serif);font-size:19px;color:var(--ink)}
header.top nav{margin-left:auto;display:flex;flex-wrap:wrap}
header.top nav a{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-faint);padding:6px 10px}
header.top nav a:hover{color:var(--accent-deep);text-decoration:none}
main{max-width:880px;margin:0 auto;padding:24px 22px 40px}
h1{font-family:var(--serif);font-size:31px;line-height:1.15;margin:0 0 6px;color:var(--ink)}
h2{font-family:var(--serif);font-size:20px;margin:28px 0 8px;color:var(--accent-deep);
  border-bottom:1px solid var(--rule);padding-bottom:5px}
.kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-faint);margin:0 0 14px}
.summ{color:var(--ink-soft)}
dl.facts{display:grid;grid-template-columns:auto 1fr;margin:16px 0;border-top:1px solid var(--rule-soft)}
dl.facts dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-faint);padding:9px 18px 9px 0;border-bottom:1px solid var(--rule-soft);white-space:nowrap}
dl.facts dd{margin:0;padding:9px 0;border-bottom:1px solid var(--rule-soft)}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--plate);
  border:1px solid var(--rule);margin-top:10px}
th{background:var(--plate-2);color:var(--ink-faint);text-align:left;padding:8px 9px;
  font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase}
td{padding:8px 9px;border-top:1px solid var(--rule-soft);vertical-align:top;color:var(--ink-soft)}
ul.plain{list-style:none;padding:0}
ul.plain li{padding:7px 0;border-bottom:1px solid var(--rule-soft)}
ul.src li{font-size:14px;color:var(--ink-faint)}
.cols{columns:2;column-gap:26px}
.visit{border:1px solid var(--rule);background:var(--plate);padding:12px 14px;margin:12px 0}
.visit .when{font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--brass)}
.visit .exc{margin:7px 0 0;color:var(--ink)}
.tag{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-faint);border:1px solid var(--rule);padding:1px 6px;margin-right:5px}
footer{max-width:880px;margin:0 auto;padding:16px 22px 46px;border-top:1px solid var(--rule);
  font-size:13px;color:var(--ink-faint)}
footer p{margin:5px 0}
@media(max-width:640px){.cols{columns:1}h1{font-size:25px}
  dl.facts{grid-template-columns:1fr}dl.facts dt{padding-bottom:0;border-bottom:none}}
"""

CITE = ('Coyne, Aodhan. <i>California Ship Registry, 1769 to 1846</i>. '
        'archivesofcalifornia.com, ' + TODAY[:4] + '.')


def page(title, desc, canon, body, ld=None):
    ldtag = ''
    if ld:
        ldtag = ('<script type="application/ld+json">'
                 + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script>\n')
    return (
        '<!DOCTYPE html>\n<html lang="en" data-theme="dark">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{esc(title)}</title>\n'
        f'<meta name="description" content="{esc(desc)}">\n'
        f'<link rel="canonical" href="{canon}">\n'
        '<meta property="og:type" content="article">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{canon}">\n'
        '<link rel="stylesheet" href="/assets/pages.css">\n'
        + ldtag +
        '</head>\n<body>\n'
        '<header class="top"><a class="wordmark" href="/">California Ship Registry</a>'
        '<nav><a href="/">Registry</a><a href="/ships/">Vessels</a>'
        '<a href="/key-voyages.html">Key voyages</a><a href="/flags.html">Flags</a></nav></header>\n'
        '<main>\n' + body + '\n</main>\n'
        '<footer><p>' + CITE + '</p>'
        '<p>Data CC BY 4.0. Every visit records the source it rests on. A visit is evidence that a '
        'record was made, not proof that a hull was present; see the registry for what it does not '
        'know. Generated ' + TODAY + '.</p>'
        '<p><a href="/">Return to the interactive registry</a></p></footer>\n</body>\n</html>\n')


def render_citations(raw):
    try:
        cits = json.loads(raw or '[]')
    except Exception:
        return []
    out = []
    for c in cits:
        label = CITE_LABEL.get(c.get('type'), c.get('type') or 'Source')
        if c.get('type') == 'ca-record' and c.get('ca') and c.get('doc'):
            label += f", C-A {c['ca']}, doc {c['doc']}"
            if c.get('scan'):
                label += f" (scan {c['scan']})"
        detail = c.get('ref') or c.get('note') or ''
        url = c.get('url')
        txt = esc(label) + (f': {esc(detail)}' if detail else '')
        out.append(f'<li><a href="{esc(url)}">{txt}</a></li>' if url else f'<li>{txt}</li>')
    return out


def main():
    ships = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'ships.csv'), encoding='utf-8')))
    visits = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'visits.csv'), encoding='utf-8')))
    by_ship = collections.defaultdict(list)
    for v in visits:
        by_ship[v['ship_id']].append(v)

    real = [s for s in ships if s['ship_id'] not in AGGREGATE_IDS]

    # Slugs must be unique on disk. Two ids differ only by apostrophe character
    # (U+0027 vs U+2019) and collide; disambiguate deterministically rather than
    # silently overwriting one page with the other.
    slugs, seen = {}, collections.Counter()
    for s in sorted(real, key=lambda r: r['ship_id']):
        base = slugify(primary_name(s['name_variants']) or s['ship_id'])
        seen[base] += 1
        slugs[s['ship_id']] = base if seen[base] == 1 else f'{base}-{seen[base]}'

    # Several distinct vessels share a name (Fama, Morelos, Santa Rosa, Eagle and
    # others). Duplicate <title> tags are a real problem, so add the recorded span
    # and then the flag until every title in a colliding group is distinct.
    name_groups = collections.defaultdict(list)
    for s_ in real:
        name_groups[primary_name(s_['name_variants'])].append(s_)
    title_of = {}
    for nm, grp in name_groups.items():
        if len(grp) == 1:
            title_of[grp[0]['ship_id']] = nm
            continue
        for disc in ('span', 'flag', 'id'):
            cand = {}
            for s_ in grp:
                if disc == 'span':
                    sp = ' to '.join(x for x in [s_.get('first_seen'), s_.get('last_seen')] if x)
                    cand[s_['ship_id']] = f'{nm} ({sp})' if sp else nm
                elif disc == 'flag':
                    fl = FLAG_LABEL.get((s_.get('flag_guess') or '').strip(), '')
                    sp = ' to '.join(x for x in [s_.get('first_seen'), s_.get('last_seen')] if x)
                    cand[s_['ship_id']] = f'{nm} ({sp}, {fl})' if fl else f'{nm} ({sp})'
                else:
                    cand[s_['ship_id']] = f"{nm} [{s_['ship_id']}]"
            if len(set(cand.values())) == len(grp):
                title_of.update(cand)
                break
        else:
            title_of.update({s_['ship_id']: f"{nm} [{s_['ship_id']}]" for s_ in grp})

    urls = [SITE + '/', SITE + '/ships/', SITE + '/key-voyages.html', SITE + '/flags.html']
    rows = []

    for s in real:
        sid = s['ship_id']
        name = primary_name(s['name_variants'])
        sl = slugs[sid]
        vs = sorted(by_ship.get(sid, []), key=lambda v: (v.get('date_from') or ''))
        canon = f'{SITE}/ships/{sl}.html'
        flag = FLAG_LABEL.get((s.get('flag_guess') or '').strip(), s.get('flag_guess') or 'not established')
        span = ' to '.join(x for x in [s.get('first_seen'), s.get('last_seen')] if x)
        if s.get('first_seen') and s.get('first_seen') == s.get('last_seen'):
            span = s['first_seen']
        anchorages = [a for a in dict.fromkeys(v.get('anchorage') or '' for v in vs) if a]
        desc = (f'{name}: {len(vs)} recorded visit' + ('s' if len(vs) != 1 else '')
                + f' to the Californias{", " + span if span else ""}'
                + (f', calling at {", ".join(anchorages[:4])}' if anchorages else '')
                + f'. Flag {flag}. Every visit cited to its source.')[:300]

        facts = [('Flag', esc(flag))]
        if span:
            facts.append(('Recorded span', esc(span)))
        facts.append(('Recorded visits', str(len(vs))))
        variants = [x.strip() for x in (s.get('name_variants') or '').split(';') if x.strip()]
        if len(variants) > 1:
            facts.append(('Name as written', ', '.join(esc(x) for x in variants)))
        if anchorages:
            facts.append(('Anchorages', ', '.join(esc(a) for a in anchorages[:12])))
        if s.get('status'):
            facts.append(('Record status', esc(s['status'])))

        body = [f'<p class="kicker">Vessel</p><h1>{esc(name)}</h1>',
                f'<p class="summ">{esc(desc)}</p>',
                '<dl class="facts">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in facts) + '</dl>']

        body.append(f'<h2>Recorded visits</h2>')
        for v in vs:
            when = v.get('date_from') or ''
            if v.get('date_to') and v['date_to'] != v.get('date_from'):
                when += ' to ' + v['date_to']
            tags = [t for t in [v.get('visit_type'), v.get('region'), v.get('purpose'), v.get('outcome')] if t]
            head = ' '.join(f'<span class="tag">{esc(t)}</span>' for t in tags)
            where = v.get('anchorage') or ''
            body.append('<div class="visit">'
                        f'<div class="when">{esc(when)}{" &middot; " + esc(where) if where else ""}</div>'
                        f'<div>{head}</div>'
                        + (f'<p class="exc">{esc(v.get("excerpt"))}</p>' if v.get('excerpt') else ''))
            cits = render_citations(v.get('citations'))
            if cits:
                body.append('<ul class="plain src">' + ''.join(cits) + '</ul>')
            if v.get('sources_disagree'):
                body.append(f'<p class="kicker">Sources disagree: {esc(v["sources_disagree"])}</p>')
            body.append('</div>')

        body.append('<p><a href="/ships/">All vessels in the registry</a> &middot; '
                    '<a href="/">Search the interactive registry</a></p>')

        ld = {'@context': 'https://schema.org', '@type': 'Vehicle', 'name': name,
              'description': desc, 'url': canon,
              'vehicleConfiguration': 'Sailing vessel'}
        write(f'ships/{sl}.html', page(f'{title_of[sid]} | California Ship Registry', desc, canon,
                                       '\n'.join(body), ld))
        urls.append(canon)
        rows.append((name, s, sl, len(vs), span, flag))

    # ---------- the vessel register ----------
    rows.sort(key=lambda r: r[0].lower())
    trs = ''.join(
        f'<tr><td><a href="/ships/{sl}.html">{esc(nm)}</a></td><td>{esc(flag)}</td>'
        f'<td>{esc(span)}</td><td>{n}</td></tr>'
        for nm, s, sl, n, span, flag in rows)
    agg = sum(len(by_ship.get(a, [])) for a in AGGREGATE_IDS)
    idesc = (f'Every named vessel recorded in the Californias between 1769 and 1846: {len(rows)} '
             f'vessels across {len(visits)} recorded visits, each cited to its source.')
    ibody = ('<h1>Vessels of the registry</h1>'
             f'<p class="summ">{esc(idesc)}</p>'
             f'<p class="kicker">A further {agg} visits are recorded for vessels never named in the '
             'sources; those are searchable in the interactive registry.</p>'
             '<table><thead><tr><th>Vessel</th><th>Flag</th><th>Recorded span</th>'
             '<th>Visits</th></tr></thead><tbody>' + trs + '</tbody></table>')
    write('ships/index.html', page('Vessels | California Ship Registry', idesc,
                                   SITE + '/ships/', ibody,
                                   {'@context': 'https://schema.org', '@type': 'Dataset',
                                    'name': 'Vessels of the California Ship Registry, 1769 to 1846',
                                    'description': idesc, 'url': SITE + '/ships/',
                                    'license': 'https://creativecommons.org/licenses/by/4.0/'}))

    write('assets/pages.css', CSS)
    write('robots.txt',
          '# California Ship Registry. All crawlers welcome, including AI crawlers.\n'
          '# Data CC BY 4.0.\n'
          'User-agent: *\nAllow: /\n\n'
          f'Sitemap: {SITE}/sitemap.xml\n')
    write('sitemap.xml',
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)
          + '</urlset>\n')

    print(f'wrote into {OUT}:')
    print(f'  {len(rows)} vessel pages, 1 vessel register, assets/pages.css, robots.txt, '
          f'sitemap.xml ({len(urls)} urls)')
    print(f'  excluded the aggregate bucket(s) {sorted(AGGREGATE_IDS)} carrying {agg} visits')


if __name__ == '__main__':
    main()
