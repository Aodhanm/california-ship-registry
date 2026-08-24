#!/usr/bin/env python3
"""Extract Bancroft's annual fleet lists from the clean IA scans of Hist. Cal. III-V.

The lists are footnotes in the marine chapters, headed 'Vessels of YYYY:'. Three
things make a naive regex fail:
  1. the header is itself OCR-garbled ('2Vcsselsof 1832:', '.-is of 1833:');
  2. the footnote is INTERRUPTED by page-body prose and running heads, then resumes;
  3. it ends at a chapter break or the next footnote, not at a period.
So: anchor loosely on year+colon, take a generous window, split on commas, and keep
only fragments that look like a vessel name. Interpolated prose does not survive the
filter because prose fragments are long and contain lowercase sentence structure.
"""
import re, pathlib, json, collections

STOP = re.compile(r'CHAPTER\s+[IVXL]+|^\s*$')
NOISE = re.compile(r'^(LIST OF VESSELS|MARINE|COMMERCE|MISSIONS|MARITIME AFFAIRS|FOREIGN|IMMIGRATION|'
                   r'THE|AND|OF|IN|AT|BY|FOR|WITH|SAN|SANTA|CHAPTER|VOL)\b', re.I)

def looks_like_vessel(s):
    s = s.strip(' .;:')
    if not (2 < len(s) < 30): return False
    if not re.match(r"^[A-ZÁÉÍÓÚÑ]", s): return False
    if len(s.split()) > 3: return False
    if NOISE.match(s): return False
    # prose gives itself away: a lowercase word followed by another lowercase word
    if re.search(r'\b[a-z]{3,}\s+[a-z]{3,}\b', s): return False
    if re.search(r'\d{3,}', s): return False                 # page numbers
    if re.match(r'^[A-Z]{4,}$', s): return False             # running heads
    return True

def clean(s):
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'[^A-Za-zÁÉÍÓÚÑá-úñ0-9 \'\.\-]', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' .-')
    return s

def extract(path, vol):
    t = pathlib.Path(path).read_text(errors='ignore')
    t = re.sub(r'-\s*\n\s*', '', t)          # rejoin hyphen-broken words
    t = re.sub(r'\s+', ' ', t)
    out = {}
    # loose header: any token ending in a 'vessels'-ish string, then 'of YYYY:'
    heads = list(re.finditer(r'(?:[Vv][a-z\'\.\-]{0,4}s[sc][el][sl]s?|\.\-is|essels)\s*of\s*(1[78]\d\d)\s*[:;]', t))
    for i, m in enumerate(heads):
        yr = int(m.group(1))
        if not (1820 <= yr <= 1850): continue
        end = heads[i+1].start() if i+1 < len(heads) else m.end() + 4200
        seg = t[m.end(): min(end, m.end() + 4200)]
        cut = re.search(r'CHAPTER\s+[IVXL]+', seg)
        if cut: seg = seg[:cut.start()]
        names = set()
        for frag in re.split(r',|\band\b', seg):
            c = clean(frag)
            if looks_like_vessel(c): names.add(c)
        if len(names) >= 4:
            out.setdefault(yr, set()).update(names)
    return {y: sorted(v) for y, v in out.items()}

ALL = collections.defaultdict(set)
for vol, f in [('III','ia-v03.txt'), ('IV','ia-v04.txt'), ('V','ia-v05.txt')]:
    got = extract(f, vol)
    print(f"vol {vol}: {len(got)} years, {sorted(got)}")
    for y, ns in got.items(): ALL[y].update(ns)

print()
print("ANNUAL FLEETS")
tot = set()
for y in sorted(ALL):
    print(f"  {y}: {len(ALL[y]):2d}  {', '.join(sorted(ALL[y])[:10])}{' …' if len(ALL[y])>10 else ''}")
    tot |= ALL[y]
print(f"\nyears {min(ALL)}–{max(ALL)} ({len(ALL)}) · {len(tot)} distinct vessels")
json.dump({str(k): sorted(v) for k, v in ALL.items()}, open('fleets-final.json','w'), ensure_ascii=False, indent=1)
