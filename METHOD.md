# Method statement

*How this dataset was built, and what it can and cannot claim. (Companion to `CODEBOOK.md`; adapted from the data-paper draft.)*

## Sources & build order
The registry was built source-family by source-family, each layer attached with typed citations: **(1)** the seed harvest from the *Archives of California* documentary calendar (the author's item-level catalog of the Bancroft C-A 1–63 Savage transcripts — most rows link to a specific manuscript leaf); **(2)** Bancroft's *History of California* I–II narrative sweep; **(3)** Bancroft's own consolidated vessel lists (HoC III–V, 1825–48); **(4)** Ogden (1941) otter-trade itineraries; **(5)** a Russian layer from RAC/AVPRI-grounded notes, **with absences stated** (`data/russian-absent.txt`) rather than silently omitted; **(6)** curated canonical voyages; **(7)** ongoing ingests as the calendar grows (e.g., the 1826/1827 Santa Bárbara customs ledgers of C-A 40, leaf-verified).

## The unit & the model
One row = one **visit** (one vessel · one anchorage · one time), after SlaveVoyages' voyage-level design. Stable IDs (`v0001…`) make single visits citable. Conservative merging: two records collapse into one visit only on ship + year + (where present) month + anchorage; over-splitting is preferred to silent loss, and `sources_disagree` records collation conflicts instead of resolving them invisibly.

## Quality control
- **Build guards** (`scripts/check.py`): codebook schema/vocabulary; every row ≥1 parseable citation; date sanity; dedup warnings.
- **The false-positive register** (`FALSE-POSITIVE-REGISTER.md`): seven documented "fake ship" classes (decree phantoms, era-conflations, persons-as-ships, places/demonyms, OCR garbles, mis-flags, mention-vs-visit). **Every new source re-triggers all seven.**
- **Leaf verification**: manuscript-derived ship names are verified against the scanned leaf before entering the tables (a policy adopted after it caught real misreads — *Nilo* not "Wilcox", *Jackman* not "Jackson").
- **Nothing auto-accepted**: uncertain rows stay `status=draft` and route to `REVIEW-QUEUE.md`.

## What the numbers mean — and don't
This is an attempted census of **documented** visits, not a reconstruction of true traffic. Three structural caveats: **contraband is under-recorded by design** (a coast whose foreign trade was often illegal leaves official-record gaps exactly where the activity was); decade totals reflect **record survival and harvest coverage** as well as traffic (the 1830s are currently coverage-thin pending the full Bancroft-list re-parse); and the large unnamed-vessel share (~26%) is evidence of traffic that cannot be attributed to hulls.
