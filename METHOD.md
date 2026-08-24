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

## ⭐ Reliability by period (read this before using the data)
The register is **not uniformly finished across its span**, and it says so plainly:

- **1769–1821 (Spanish period) is the clean, reliable core.** Coverage is dense, flags are sound (the source language and the flag coincide, and every flag is floor-guarded), and this is the span the *Flags at Anchor* figure is scoped to. Analysis on this window is on firm ground.
- **1822–1846 (Mexican period) is still in progress.** Treat it as provisional. Two known limits. **(1)** The register is **probably missing many vessels** here: 77 of the 198 vessels staged from Bancroft's own consolidated lists (`data/mexlist-stage.csv`) remain unmerged, 31 of them American, blocked on OCR-garbled names that need a page read; so decade totals for the 1830s–40s are a **floor**, not a count. **(2)** **Some flags and other row-level errors are still present.** The gross post-1821 `spain` artifact has been corrected per row and a ceiling guard installed (see below), but residual issues remain (e.g. the *volunteer* russia mis-flags; the *mexicana*/*san carlos* era-conflations); see REVIEW-QUEUE.md.
- **v1.1 is coming soon** and will fold the unmerged Bancroft vessels and complete the Mexican-period flag audit.

## What the numbers mean — and don't
This is an attempted census of **documented** visits, not a reconstruction of true traffic. Three structural caveats: **contraband is under-recorded by design** (a coast whose foreign trade was often illegal leaves official-record gaps exactly where the activity was); decade totals reflect **record survival and harvest coverage** as well as traffic (the 1830s and 1840s are coverage-thin pending the full Bancroft-list re-parse; see the period note above and REVIEW-QUEUE.md); and the large unnamed-vessel share (~26%) is evidence of traffic that cannot be attributed to hulls. ⚠ **On flags:** the post-1821 `spain` artifact (43 rows the harvester mis-flagged from Spanish-language records) was corrected per row on 2026-08-24 (reassigning the Chilean insurgent-navy and Mexican vessels, applying four Bancroft-verbatim fixes, keeping the one genuine Spanish case, the *Asia*, and leaving the rest blank rather than guessing), and `check.py` now hard-guards against any post-1821 `spain` port-call. Even so, per the period note, **flag analysis is safest confined to 1769–1821** until the Mexican-period audit ships in v1.1.
