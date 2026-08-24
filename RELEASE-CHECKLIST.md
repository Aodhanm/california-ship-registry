# Release checklist — DOI staging

The citation infrastructure is staged and one-click ready. The DOI mint needs **your Zenodo login** (Claude can't authenticate) — same flow as the [Archives of California](https://github.com/Aodhanm/archives-of-california) DOI (`10.5281/zenodo.21327098`).

## Staged (done by Claude)
- [x] `CITATION.cff` — CFF 1.2.0, author Coyne/Aodhan/ORCID, CC-BY-4.0, dataset.
- [x] `.zenodo.json` — Zenodo deposit metadata (title, creator, license, keywords, `isDerivedFrom` the C-A DOI).
- [x] Data at 2,072 visits / 401 ships, all `reviewed`, every ship source-corroborated, guards green (`check.py` HARD 0).
- [x] `LICENSE` — CC-BY-4.0 (data/docs) + MIT (code) split, already populated (the old "empty" note below is stale).
- [x] Flag-artifact pass done (post-1821 `spain` fixed + ceiling guard); `PROVENANCE.md` written; `CODEBOOK.md` frozen. See REVIEW-QUEUE "DOI-readiness status".

## Your turn (one-time Zenodo↔GitHub link)
1. Sign in at **zenodo.org** with GitHub → **Settings → GitHub** → flip the toggle **ON** for `Aodhanm/california-ship-registry`.
2. Decide the version (suggest **v0.2.0** — the corroborated/reviewed dataset; README currently says v0.1). Bump the README banner if so.
3. Tell Claude "cut the release" — Claude will `git tag v0.2.0` + `gh release create v0.2.0`. Zenodo's webhook mints the DOI automatically from `.zenodo.json`.
4. Claude backfills the new DOI into `CITATION.cff` (`doi:` line), README, and the site footer.

## Notes
- Don't create the GitHub release before step 1, or Zenodo won't catch it.
- ~~LICENSE file is currently empty~~ — DONE: LICENSE holds the CC-BY-4.0 (data/docs) + MIT (code) split.
- Per your dataset-as-publication strategy, this DOI *is* publication #2 (the C-A DOI being #1).
- Scope at mint: the register spans 1769–1848; the Mexican-period flag field is documented as less reliable (CODEBOOK) and the *Flags at Anchor* figure is deliberately scoped to 1769–1821. You can mint the full span as v1.0 (recommended — versioning lets the Mexican-period audit ship as v1.1) or narrow to 1769–1821; that scope call is yours at mint time.
