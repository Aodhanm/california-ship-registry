# Excerpt-integrity audit, 2026-07-30

*Triggered by the verified-tier finding that `mercedes` and `sutil` carried an excerpt describing a **neighbouring** record on the same multi-record leaf (their real vessel mention was elsewhere on the leaf). This audit asks: how widespread is that, and are the underlying **linkages** sound?*

## Method
The `excerpt` field is a ~120-character snippet of a C-A record's summary. On the Spanish-period **index/cluster leaves** (many short records per page), the snippet often shows the *first* record's text, not the one naming the vessel. For every C-A-sourced, named-vessel visit, we checked (a) whether the ship name is in the **excerpt**, and if not, (b) whether it is in the **full catalog record** (title + summary + place, from `ca-catalog-export.json`, 24,154 records).

## Result
| | count |
|---|---|
| C-A named visits whose **excerpt** lacks the ship name | **337** |
| → ship name **is** in the full record (valid link, truncated excerpt) | **266** |
| → ship name **not** in the full record's indexed text | **71** |

**Conclusion: the pattern is overwhelmingly cosmetic.** 266/337 are machine-validated as correct links whose excerpt is merely truncated. The 71 residual are dominated by **real vessels with name-variant rendering**, the check misses them because the catalog summary uses a description or a spelling the token-match doesn't catch: e.g. *Otter* (1796, the first U.S. ship, leaf-verified), *Resolution*/*Resolución* (the 1795 whaler), *Discovery* (Vancouver), *Juno-1767* (the Cádiz transport of the Catalan Volunteers, linked thematically via the Voluntarios de Cataluña pay records, a documented identity in the CODEBOOK). The genuine false-link residue, after removing known-real vessels, is small.

## Disposition
- **No bulk excerpt rewrite.** Many excerpts are hand-curated (⭐ highlights, capitalised event tags); regenerating from the catalog would destroy that work for a cosmetic gain.
- **Excerpts are corrected opportunistically during the verified-tier leaf pass** (as done for `mercedes` and `sutil`, 2026-07-30).
- The 71 residual are the **priority queue** for the verified sample, leaf-reading them both verifies the visit and, where needed, corrects the excerpt.
- This audit is itself an **integrity finding**: the registry's vessel↔record linkages are sound (266 independently validated); the excerpt is a snippet, not the evidence, the citation + scan link is.

*Documented limitation, added to CODEBOOK: the `excerpt` is a leaf snippet and, on multi-record leaves, may not contain the named vessel; the authoritative evidence is the cited record + scan.*
