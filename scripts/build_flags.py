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
# A run of zeros this long or longer is absence, not a measurement, and is not
# drawn. A single isolated zero inside a continuous presence IS a measurement
# (that flag was here either side of it) and is kept, so the line does not
# develop a one-year hole that reads as a rendering fault.
MIN_ZERO_RUN = 2
# Four flags carry enough records in this window to be a trend. France (7 rows)
# and Argentina (2) do not: they are three discrete arrivals - La Perouse 1786,
# Roquefeuil 1817, Bouchard 1818 - and a rolling share would draw three events as
# a trickle. They are emitted as named events instead, and excluded from the
# denominator note below.
NAMED = ["spain", "usa", "russia", "britain", "france"]
LABEL = {"spain": "Spain", "usa": "United States", "russia": "Russia",
         "britain": "Britain", "france": "France", "other": "Argentina"}

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

# FIRST recorded arrival per flag. A centred rolling mean spreads a value
# backwards across half its window, so without this clamp every flag's line
# lifts off the axis two years before the flag actually appears - it dated the
# Russian arrival to 1804 (really 1806, the Juno), the American to 1794 (1796),
# the British to 1790 (1792, the Chatham) and the French to 1784 (1786, La
# Perouse). First arrival is the historically meaningful moment in this series,
# so it must not be smoothed. Below a flag's first record its share is zero, flat.
first_year = {}
for y, f in sorted(rows):
    first_year.setdefault(f, y)

years = list(range(Y0, Y1 + 1))
half = WINDOW // 2
series, annual = {}, {}
for k in NAMED + ["other"]:
    smooth, raw = [], []
    for y in years:
        win = range(y - half, y + half + 1)
        wn = sum(n_by_year.get(w, 0) for w in win)
        wk = sum(ann[w][k] for w in win if w in ann)
        arrived = k in first_year and y >= first_year[k]
        # No line before a flag arrives. A flat zero would draw absence as a
        # measurement, and the eye reads it as "present, at nil" rather than
        # "not here yet". The line simply begins at the first recorded arrival.
        val = round(100 * wk / wn, 1) if (wn >= MIN_WINDOW_N and arrived) else None
        smooth.append({"year": y, "share": val, "window_n": wn})
        n = n_by_year.get(y, 0)
        raw.append({"year": y, "n": n,
                    "share": round(100 * ann[y][k] / n, 1) if (n and arrived) else None})
    # suppress sustained zero runs: a flag absent for several years running has no
    # share to plot, and a flat line along the axis reads as presence-at-nil
    i = 0
    while i < len(smooth):
        if smooth[i]["share"] == 0.0:
            j = i
            while j < len(smooth) and smooth[j]["share"] == 0.0: j += 1
            if j - i >= MIN_ZERO_RUN:
                for m in range(i, j): smooth[m]["share"] = None
            i = j
        else:
            i += 1
    series[k], annual[k] = smooth, raw

# the flag-integrity evidence, carried in the data file so the page cannot drift from it
byname = collections.defaultdict(set)
for v in V:
    nm = (v.get("name_as_written") or "").strip().lower()
    fl = (v.get("flag") or "").strip()
    if nm and fl: byname[nm].add(fl)
conflicted = sorted(n for n, f in byname.items() if len(f) > 1)


# ---------------------------------------------------------------------------
# FIRST VISIT PER FLAG. Curated, not derived: the earliest row per flag is not
# always the earliest *arrival*. The registry's earliest American row is an
# offshore sighting of 28 May 1796, reclassified as such on 2026-08-04; the
# first American ship actually to enter a Californian port is the Otter, five
# months later. Each entry below names the vessel, the date, the place and the
# registry's own attestation, so a reader can weigh it.
#
# Verified against Bancroft, Hist. Cal. I: "The first intercourse of the
# Californians with subjects of a foreign power was with the French under Jean
# Francois Galaup de La Perouse in the autumn of 1786" - which he also calls
# "the first visit of a foreigner to California". His chapter XXIV is headed
# "Vancouver's First Visit, 1792-1794". There is no British arrival in Alta
# California before Vancouver in November 1792. The nearest thing to one is the
# BRITISH-BUILT hull Princesa Real - the sloop Princess Royal, seized from
# Britain at Nootka in 1789 - which touched Monterey in September 1790 under
# Manuel Quimper and SPANISH colours. A British ship, not a British visit.
FIRST_VISITS = [
  {"flag": "spain",   "label": "Spain",         "year": 1769, "date": "1769",
   "vessels": "San Antonio · San Carlos (Sacred Expedition)", "place": "San Diego",
   "who": "Portol\u00e1 and Serra", "attestation": "inferred / draft",
   "note": "The founding voyages; the registry dates the first landfall to 1769."},
  {"flag": "france",  "label": "France",        "year": 1786, "date": "14-24 Sept 1786",
   "vessels": "Boussole · Astrolabe", "place": "Monterey",
   "who": "La P\u00e9rouse", "attestation": "stated / reviewed",
   "note": "The first visit by any foreign power. Bancroft: 'the first intercourse of "
           "the Californians with subjects of a foreign power'."},
  {"flag": "britain", "label": "Britain",       "year": 1792, "date": "14 Nov 1792",
   "vessels": "Discovery", "place": "San Francisco",
   "who": "Vancouver", "attestation": "stated / reviewed / exact date",
   "note": "The first foreign warship into San Francisco Bay. Nothing British precedes it: "
           "the Princesa Real at Monterey in 1790 was the captured British sloop Princess "
           "Royal sailing under Spanish colours."},
  {"flag": "usa",     "label": "United States", "year": 1796, "date": "29 Oct 1796",
   "vessels": "Otter, of Boston", "place": "Monterey",
   "who": "Dorr", "attestation": "reviewed / port-call",
   "note": "The first American ship in a Californian port. An offshore sighting of 28 May "
           "1796 precedes it but is a sighting, not an arrival."},
  {"flag": "russia",  "label": "Russia",        "year": 1806, "date": "8 Apr 1806",
   "vessels": "Juno", "place": "San Francisco",
   "who": "Rezanov", "attestation": "VERIFIED / exact date",
   "note": "Rezanov's provisioning voyage from Sitka; one of only thirteen rows in the "
           "registry at verified status."},
  {"flag": "argentina", "label": "Argentina",   "year": 1818, "date": "20 Nov 1818",
   "vessels": "La Argentina · Santa Rosa", "place": "Monterey, then Refugio",
   "who": "Bouchard", "attestation": "stated / reviewed",
   "note": "Not a visit but an attack: the only foreign assault Spanish California suffered."},
]

# The arrivals too few to be a trend, named. Dates and vessels are the registry's own.
EVENTS = [
  {"year": 1786, "date": "14–24 Sept 1786", "flag": "france",
   "label": "La Pérouse", "vessels": "Astrolabe · Boussole", "place": "Monterey",
   "note": "The first foreign visit to Spanish California.", "status": "reviewed"},
  {"year": 1817, "date": "1817", "flag": "france",
   "label": "Roquefeuil", "vessels": "Bordelais", "place": "San Francisco",
   "note": "The corvette put in under stress of weather.", "status": "draft"},
  {"year": 1818, "date": "20 Nov 1818", "flag": "argentina",
   "label": "Bouchard", "vessels": "La Argentina · Santa Rosa", "place": "Monterey, then Refugio",
   "note": "The only foreign attack on Spanish California.", "status": "reviewed"},
]

# Defects found while building this figure, carried in the data so they cannot be lost.
REVIEW_FLAGS = [
  {"row": "france 1808-10-26 (unnamed)",
   "issue": "mention, not a visit: it is Spain's order to seize any French ship entering a "
            "Californian port, not a French ship arriving. Class: mention-vs-visit."},
  {"row": "france 1817-05-24 'Francia'",
   "issue": "probable duplicate of Bordelais the same day: the row's own excerpt glosses "
            "'la corveta Francia' as Roquefeuil's Bordelais. Class: era/name conflation."},
]

out = {
  "title": "Flags at anchor in California, 1769–1821",
  "measure": "share of recorded arrivals; 5-year centred rolling mean, annual values shown behind",
  "window": WINDOW, "min_window_n": MIN_WINDOW_N,
  "year_range": [Y0, Y1],
  "generated_from": "data/visits.csv",
  "n_in_scope": len(rows), "n_total": len(V),
  "excluded": {"after_1821": out_of_scope, "no_date": no_date, "no_flag": no_flag},
  "labels": LABEL, "order": NAMED + ["other"],
  "first_arrival": {k: first_year.get(k) for k in NAMED + ["other"]},
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
  "events": EVENTS,
  "first_visits": FIRST_VISITS,
  "review_flags": REVIEW_FLAGS,
  "caveats": [
    "Scope is 1769–1821. The registry's flag field is not reliable after Mexican independence: "
    "43 visits dated 1822 or later are flagged Spanish, among them vessels named Morelos, Matamoros "
    "and Mariquita, and the American Brookline, Volunteer and Leonidas. 19% of post-1821 rows carry a "
    "vessel name that appears under a different flag elsewhere in the file, against 7% before 1822.",
    "A line is drawn only where that flag was actually present. It begins at the flag's first "
    "recorded arrival, and it stops again wherever the flag is absent for two years or more: a "
    "flat line along the axis reads as 'here, at nil' rather than 'not here', which is why France "
    "appears as three separate episodes rather than one long line at zero. A single isolated zero "
    "inside a continuous presence is kept, because there it really is a measurement. "
    "The line is a 5-year centred rolling share, also blank wherever its window holds fewer than 20 records. "
    "Faint points behind it are the unsmoothed annual values; the strip beneath gives each year's n.",
    "Flag is the flag as attested or inferred in the record, not a vessel's registry. Within this window "
    "56% of rows are 'attested/inferred' rather than plainly stated.",
    "Most visit rows remain at draft status in the registry's own review workflow.",
    "France is 7 records across three separate occasions, not a trend; two of them are flagged for "
    "review (an 1808 decree that is a mention rather than a visit, and a probable duplicate in 1817). "
    "Argentina is Bouchard alone and is shown only as an arrival.",
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
