#!/usr/bin/env python3
"""Audit the registry's `flag` field against Bancroft's own consolidated vessel lists.

Produces data/flag-corrections-proposed.csv. It PROPOSES; it does not write
visits.csv. Per METHOD.md nothing is auto-accepted: every row here is a
candidate for REVIEW-QUEUE.md, to be accepted or rejected by hand.
"""
import csv, collections, difflib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ms = list(csv.DictReader(open(ROOT/"data"/"mexlist-stage.csv")))
V  = list(csv.DictReader(open(ROOT/"data"/"visits.csv")))

bflag, brow = {}, {}
for r in ms:
    sid = (r.get("ship") or "").strip().lower()
    f = (r.get("flag") or "").strip().lower()
    if sid and f: bflag[sid] = f; brow[sid] = r

props = []
for v in V:
    y = (v.get("date_from") or "")[:4]
    if not y.isdigit(): continue
    y = int(y)
    cur = (v.get("flag") or "").strip().lower()
    sid = (v.get("ship_id") or "").strip().lower()
    nm  = (v.get("name_as_written") or "").strip()

    b, how = bflag.get(sid), "ship_id"
    if b is None and nm:
        m = difflib.get_close_matches(nm.lower(), list(bflag), n=1, cutoff=0.82)
        if m: b, how, sid = bflag[m[0]], f"fuzzy:{m[0]}", m[0]

    # Rule 1: Spain had no California trade after 1821. Bancroft lists no
    # Spanish-flagged vessel anywhere in HoC III-V (1825-48).
    if cur == "spain" and y >= 1822:
        props.append({
          "visit_id": v.get("visit_id",""), "ship_id": v.get("ship_id",""),
          "name_as_written": nm, "date_from": v.get("date_from",""),
          "current_flag": cur, "proposed_flag": b or "REVIEW",
          "confidence": "high" if b else "medium",
          "matched_by": how if b else "none",
          "bancroft_master": (brow.get(sid,{}) or {}).get("master",""),
          "bancroft_tons": (brow.get(sid,{}) or {}).get("tons",""),
          "bancroft_years": (brow.get(sid,{}) or {}).get("years",""),
          "evidence": ("Bancroft HoC vol " + (brow.get(sid,{}) or {}).get("vol","?") +
                       " lists this vessel as " + b + "." if b else
                       "Spain had no California trade after 1821 and Bancroft lists no "
                       "Spanish-flagged vessel in HoC III-V; flag needs re-determination."),
        })
    # Rule 2: any other flat contradiction with Bancroft, post-1821
    elif b and cur and b != cur and y >= 1822:
        props.append({
          "visit_id": v.get("visit_id",""), "ship_id": v.get("ship_id",""),
          "name_as_written": nm, "date_from": v.get("date_from",""),
          "current_flag": cur, "proposed_flag": b, "confidence": "medium",
          "matched_by": how,
          "bancroft_master": brow[sid].get("master",""),
          "bancroft_tons": brow[sid].get("tons",""),
          "bancroft_years": brow[sid].get("years",""),
          "evidence": "Bancroft HoC vol " + brow[sid].get("vol","?") + " lists it as " + b + ".",
        })

props.sort(key=lambda p: (p["date_from"], p["name_as_written"]))
out = ROOT/"data"/"flag-corrections-proposed.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(props[0].keys())); w.writeheader(); w.writerows(props)

have = {(v.get("ship_id") or "").strip().lower() for v in V}
missing = [r for r in ms if (r.get("ship") or "").strip().lower() not in have]

print(f"wrote {out}: {len(props)} proposed corrections")
print("  by confidence:", dict(collections.Counter(p["confidence"] for p in props)))
print("  proposed flags:", dict(collections.Counter(p["proposed_flag"] for p in props).most_common()))
print(f"\nunmerged Bancroft vessels: {len(missing)} of {len(ms)} staged")
print("  by flag:", dict(collections.Counter((r.get('flag') or 'unknown').strip() or 'unknown' for r in missing).most_common()))
