#!/usr/bin/env python3
"""First pass at the 63 OCR-garbled vessel names blocking the Bancroft-list merge.

Method, and its limits. Each garbled string gets a candidate reading, which is
then tested against the full text of Bancroft, Hist. Cal. III-V in the vault -
not by raw frequency, which rewards common words, but by whether the candidate
appears within 90 characters of a ship word (ship/brig/schr/tons/Capt./cargo...).

Tiers: CONFIRMED (>=3 ship-context hits), plausible (1-2), UNRESOLVED (0).
A fourth tier, AMBIGUOUS, marks readings whose candidate is also a common word
or a frequent surname in Bancroft - Smith, Wilson, Rosa, Balance - where the hit
count proves nothing about a vessel. Those need a human eye on the printed list.

NOTHING here is applied. Output is a proposal for REVIEW-QUEUE.md.
"""
import csv, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANC = pathlib.Path.home()/"vault"/"07 Files"/"Raw"/"papers"/"bancroft-history-california"

READINGS = {
 "AijantcJio":"Ayacucho", "ArmcUa":"Amelia", "Balavcfi":"Balance", "BamstaJble":"Barnstable",
 "BoUna":"Bolivar", "Brayttnza":"Braganza", "CaJalina":"Catalina", "Columhiw":"Columbia",
 "Conrtanlc":"Constante", "Drlphos":"Delphos", "Expadon":"Esperanza", "Feighton":"Leighton",
 "Franl'Un":"Franklin", "HaalUio":"Rosalia", "Htfik":"Hopewell", "IVandsca":"Francisca",
 "Ilopnoe.ll":"Hopewell", "JRosa":"Rosa", "LaUaina":"Lahaina", "Lconidatt":"Leonidas",
 "Lfonor":"Leonor", "Lnijramjf":"Lagrange", "Martlta":"Martha", "MathUde":"Mathilde",
 "MaynoVa":"Magnolia", "Mcujruder":"Magruder", "MedkiM":"Medicis", "Mntkar":"Matador",
 "MoreloB":"Morelos", "Niiifa":"Ninfa", "OencralJackson":"General Jackson", "Pararjon":"Paragon",
 "Peraviiin":"Peruvian", "Pilrjrim":"Pilgrim", "Poifcifla":"Rosalia", "PorahontciJi":"Pocahontas",
 "PrescoU":"Prescott", "Prwuivera":"Primavera", "Ruswll":"Russell", "Snnth":"Smith",
 "Soledtul":"Soledad", "SterUon":"Sterling", "Strrlimj":"Sterling", "Valleyficid":"Valleyfield",
 "WUmimjUm":"Wilmington", "Washinfjton":"Washington", "WhUon":"Wilson", "Whafeman":"Whaleman",
 "Wilminfjton":"Wilmington",
}
# candidates that are also common words or frequent surnames: a hit count is not evidence
AMBIGUOUS = {"Smith", "Wilson", "Rosa", "Balance", "Washington", "Columbia", "Russell"}

TXT = "\n".join((BANC/f"vol{v}-{y}.txt").read_text(errors="ignore")
                for v, y in [(3,"1825-1840"), (4,"1840-1845"), (5,"1846-1848")])
SHIP = r'(?:ship|bark|barque|brig|schr|schooner|sloop|vessel|whaler|tons?|Capt\.?|master|arrived|sailed|cargo|hide)'

sus = {r["garbled_name"]: r for r in csv.DictReader(open(ROOT/"data"/"mexlist-suspects.csv"))}
rows = []
for g, meta in sorted(sus.items()):
    cand = READINGS.get(g)
    if not cand:
        rows.append({"garbled": g, "vol": meta.get("vol",""), "span": meta.get("span",""),
                     "proposed": "", "ship_context_hits": 0, "tier": "NO CANDIDATE",
                     "note": "no reading proposed; needs the printed page"})
        continue
    pat = re.compile(r'(?:'+SHIP+r'[^.]{0,90}\b'+re.escape(cand)+r'\b|\b'+re.escape(cand)+r'\b[^.]{0,90}'+SHIP+r')', re.I)
    n = len(pat.findall(TXT))
    if cand in AMBIGUOUS:
        tier, note = "AMBIGUOUS", ("reading is plausible but the word is common in Bancroft "
                                   "in other senses; hit count is not evidence of a vessel")
    elif n >= 3: tier, note = "CONFIRMED", "appears repeatedly in a ship context in Bancroft III-V"
    elif n >= 1: tier, note = "plausible", "appears in a ship context, but only once or twice"
    else:        tier, note = "UNRESOLVED", "candidate not found in a ship context; reading unsupported"
    rows.append({"garbled": g, "vol": meta.get("vol",""), "span": meta.get("span",""),
                 "proposed": cand, "ship_context_hits": n, "tier": tier, "note": note})

out = ROOT/"data"/"mexlist-degarble-proposed.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

import collections
c = collections.Counter(r["tier"] for r in rows)
print(f"wrote {out}: {len(rows)} names")
for k in ["CONFIRMED","plausible","AMBIGUOUS","UNRESOLVED","NO CANDIDATE"]:
    if c[k]: print(f"  {k:14s} {c[k]}")
print("\nCONFIRMED readings:")
for r in rows:
    if r["tier"] == "CONFIRMED":
        print(f"   {r['garbled']:16s} -> {r['proposed']:16s} ({r['ship_context_hits']} ship-context hits)")
