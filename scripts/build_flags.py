#!/usr/bin/env python3
"""Derive the annual flag-composition series from visits.csv.

TWO deliberate restrictions, both forced by the data rather than by taste.

1. SCOPE: 1769-1821 only. After Mexican independence the registry's `flag`
   field is not sound. 43 visits dated 1822 or later are flagged 'spain',
   including vessels named Morelos, Matamoros and Mariquita (Mexican) and
   Brookline, Volunteer and Leonidas (American); 19% of post-1821 rows carry a
   vessel name that appears under a different flag elsewhere in the file,
   against 7% before 1822. METHOD.md already lists "mis-flags" as one of the
   seven standing false-positive classes. Until that audit is done, the
   Mexican period cannot carry a composition chart.

2. MEASURE: share, smoothed. Raw annual arrivals track documentary survival as
   much as traffic (1797 alone holds 65 visits, largely one densely catalogued
   stretch of San Blas supply runs). The plotted line is therefore a 5-year
   CENTRED rolling share, suppressed wherever its window holds fewer than 20
   records; the unsmoothed annual value is emitted alongside it so the figure
   can show the scatter it was computed from, and the annual n travels with
   every point.
"""
import csv, json, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
V = list(csv.DictReader(open(ROOT/"data"/"visits.csv")))

Y0, Y1 = 1769, 1821
WINDOW, MIN_WINDOW_N = 5, 20
NAMED = ["spain", "usa", "russia", "britain"]
LABEL = {"spain": "Spain", "usa": "United States", "russia": "Russia",
         "britain": "Britain", "other": "Other flags"}

rows, out_of_scope, no_date, no_flag = [], 0, 0, 0
for v in V:
    y = (v.get("date_from") or "")[:4]
    f = (v.get("flag") or "").strip().lower()
    if not y.isdigit(): no_date += 1; continue
    if not f:           no_flag += 1; continue
    y = int(y)
    if not (Y0 <= y <= Y1): out_of_scope += 1; continue
    rows.append((y, f if f in NAMED else "other"))

ann = collections.defaultdict(collections.Counter)
for y, f in rows: ann[y][f] += 1
n_by_year = {y: sum(ann[y].values()) for y in ann}

years = list(range(Y0, Y1 + 1))
half = WINDOW // 2
series, annual = {}, {}
for k in NAMED + ["other"]:
    smooth, raw = [], []
    for y in years:
        win = range(y - half, y + half + 1)
        wn = sum(n_by_year.get(w, 0) for w in win)
        wk = sum(ann[w][k] for w in win if w in ann)
        smooth.append({"year": y, "share": round(100 * wk / wn, 1) if wn >= MIN_WINDOW_N else None,
                       "window_n": wn})
        n = n_by_year.get(y, 0)
        raw.append({"year": y, "share": round(100 * ann[y][k] / n, 1) if n else None, "n": n})
    series[k], annual[k] = smooth, raw

# the flag-integrity evidence, carried in the data file so the page cannot drift from it
byname = collections.defaultdict(set)
for v in V:
    nm = (v.get("name_as_written") or "").strip().lower()
    fl = (v.get("flag") or "").strip()
    if nm and fl: byname[nm].add(fl)
conflicted = sorted(n for n, f in byname.items() if len(f) > 1)

out = {
  "title": "Flags at anchor in California, 1769–1821",
  "measure": "share of recorded arrivals; 5-year centred rolling mean, annual values shown behind",
  "window": WINDOW, "min_window_n": MIN_WINDOW_N,
  "year_range": [Y0, Y1],
  "generated_from": "data/visits.csv",
  "n_in_scope": len(rows), "n_total": len(V),
  "excluded": {"after_1821": out_of_scope, "no_date": no_date, "no_flag": no_flag},
  "labels": LABEL, "order": NAMED + ["other"],
  "years": years,
  "n_by_year": {str(y): n_by_year.get(y, 0) for y in years},
  "series": series, "annual": annual,
  "flag_integrity": {
    "conflicted_names": len(conflicted),
    "examples": [n for n in conflicted if n in
                 ("eagle", "cossack", "brookline", "catalina", "ayacucho", "columbia")],
    "post_1821_spain_rows": sum(1 for v in V
        if (v.get("date_from") or "")[:4].isdigit() and int(v["date_from"][:4]) >= 1822
        and (v.get("flag") or "").strip() == "spain"),
  },
  "caveats": [
    "Scope is 1769–1821. The registry's flag field is not reliable after Mexican independence: "
    "43 visits dated 1822 or later are flagged Spanish, among them vessels named Morelos, Matamoros "
    "and Mariquita, and the American Brookline, Volunteer and Leonidas. 19% of post-1821 rows carry a "
    "vessel name that appears under a different flag elsewhere in the file, against 7% before 1822.",
    "The line is a 5-year centred rolling share, blank wherever its window holds fewer than 20 records. "
    "Faint points behind it are the unsmoothed annual values; the strip beneath gives each year's n.",
    "Flag is the flag as attested or inferred in the record, not a vessel's registry. Within this window "
    "56% of rows are 'attested/inferred' rather than plainly stated.",
    "Most visit rows remain at draft status in the registry's own review workflow.",
  ],
}
p = ROOT/"data"/"flags-by-year.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1))
old = ROOT/"data"/"flags-by-decade.json"
if old.exists(): old.unlink()
print(f"wrote {p}")
print(f"  in scope {len(rows)} of {len(V)}; excluded after-1821 {out_of_scope}, no-date {no_date}, no-flag {no_flag}")
print(f"  flag-conflicted vessel names across the whole file: {len(conflicted)}")
for k in NAMED:
    vals = [d['share'] for d in series[k] if d['share'] is not None]
    print(f"  {k:8s} smoothed range {min(vals):5.1f} – {max(vals):5.1f}  ({len(vals)} plotted years)")
