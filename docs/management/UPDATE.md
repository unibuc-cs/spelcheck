# Updating the paper and slides

The documents describe one fixed project version. The source archives, manifests, saved experiments and evidence index are the record needed for the next update.

## What this edition preserves

The current source baseline is commit `498dea06df250964013b2abb2b06c94d341b223b`, dated 24 November 2026. Its files are in `snapshot/2026-11-24-498dea0/source.zip`. This documentation edition is dated 25 November 2026. The adjacent `manifest.json` records the Git tree, archive checksum, every original file's checksum, dependency lock versions and model configuration from the deployment scripts. `SHA256SUMS.txt` also covers the manifest itself.

The previous snapshot, `snapshot/2026-11-24-18752f2/`, is preserved unchanged. The previous full delivery remains in `speccheck-management-2026-11-24.zip` in the working folder. The new delivery includes both source snapshots, but excludes earlier delivery ZIPs and earlier PDF variants.

Each source archive contains all tracked files at its revision, including raw experiment JSON, inputs and expected defects, saved formal models, result overlays and original result files. It excludes virtual environments, local caches and credentials, model weights, GPU services and Git history. It supports inspection and solver replay once dependencies are available; it does not promise identical samples from a new model run.

The snapshot revision is the version being explained. E19 froze its design at `07ecd38`; E20 froze it at `373ae4c`. The model-name cache check and stricter option combinations in `498dea0` came after E20. Most older experiments do not record their exact producing revision. Preserve these distinctions when citing results.

Archive creation disables automatic checkout line-ending conversion and checks every archived file against its Git blob identifier. The manifest also includes normalized text hashes so future Windows checkouts can distinguish line-ending changes from content changes.

## Inspect or verify the current baseline

From the original repository root in PowerShell:

```powershell
& .\docs\management\scripts\snapshot.ps1
```

This verifies the current archive and every archived file against the manifest. It never replaces an existing snapshot with different content. To verify the previous baseline, pass `-Revision 18752f24cbfd625d23d7ae5bd967af43ee7af718` explicitly.

To extract a checked working copy of the current baseline:

```powershell
& .\docs\management\scripts\snapshot.ps1 `
  -ExtractTo .\docs\management\build\baseline-498dea0
```

The snapshot script resolves the chosen revision through Git, so it needs the original Git history. With only the delivered folder, unzip the current `source.zip` into a fresh directory and compare that directory with the manifest:

```powershell
& .\docs\management\scripts\compare-snapshot.ps1 `
  -NewProjectDirectory C:\Work\speccheck-baseline
```

Expect no added, changed, removed or line-ending-only files. `Get-FileHash -Algorithm SHA256` can independently check the archive against `SHA256SUMS.txt`. Preserve a damaged or incomplete snapshot for inspection instead of overwriting it.

## Compare the next project version

Point the comparison script at the new version, whether it is a Git checkout or an ordinary directory:

```powershell
& .\docs\management\scripts\compare-snapshot.ps1 `
  -NewProjectDirectory C:\Work\speccheck-next
```

The default manifest is the current `498dea0` snapshot. Read `build/snapshot-diff.json` for added, changed and removed paths, hashes and likely documentation topics. Line-ending differences are separate. The comparison skips this documentation package, runtime caches (including `.speccheck`), virtual environments and build outputs. It skips directory links rather than traversing outside the project and does not modify the source.

To repeat the comparison from the first edition instead, specify its manifest:

```powershell
& .\docs\management\scripts\compare-snapshot.ps1 `
  -NewProjectDirectory C:\Work\speccheck-next `
  -ManifestPath .\docs\management\snapshot\2026-11-24-18752f2\manifest.json `
  -OutputPath .\docs\management\build\diff-from-first-edition.json
```

Use `evidence/claims.json` to locate the affected claims, formulas, diagrams and examples:

- `formalize.py`, `probe.py` or `logic.py`: translation steps, vocabulary reuse and the meaning of the guarantees.
- `checks.py`: conflict, gap and scenario semantics, including removal seeds and witnesses.
- `change.py`: merge, scenario provenance, deleted/replaced rules and sentence-level edit coverage.
- `cli.py`: mode restrictions, cache validity, saved artifacts and replay order.
- New benchmark inputs or results: inventory, configuration, scoring units and evidence claims.
- Deployment scripts or dependency locks: runtime, capacity and reproduction instructions.

## Revise the explanation and evidence together

1. Preserve the previous full delivery and source snapshot before making changes.
2. Choose the exact new source revision. Run `snapshot.ps1 -Revision <full-commit>` to create a separate dated directory. Without Git history, preserve the supplied files and record that provenance instead of inventing a commit.
3. Inspect the implementation and original evidence behind each affected claim. Revisit the known incremental boundary: sentence-only or broader contextual edits can require full formalization, and the current cache key omits parameters such as temperature and sample count.
4. Update the paper first. Keep requirement IDs and notation stable where possible. Main text should carry essential definitions, concrete examples and evaluation conclusions; detailed algorithms belong in the appendices.
5. Update `evidence/metrics.json`, the claims index, shared figures and slides together. Preserve the same research questions and refresh slide numbers, appendix letters and links after reordering.
6. Check replay order. A change's saved raw `formal.json` can still contain deleted rules: apply the matching change metadata and `after_model` before solver analysis. `merged.md`, incremental `new.md`, the cached base and a replayed formal model have different roles.
7. Recheck examples against the new extracted snapshot, run its offline suite, build both PDFs, inspect every rendered page and slide, and rebuild the delivered sources independently.
8. Update the edition note, validation records, snapshot/comparison defaults and package filename. Keep the preceding edition intact.

For evaluation, distinguish findings, flagged rules and repeated runs. Keep doubtful-filtered results beside default results where that changes the interpretation. Formalization request counts exclude explanation and scenario judging; compare warm changes and initial base cost separately. Any saving including bases depends on how many changes reuse each base. Do not pool different configurations or historical sets into one project accuracy figure.

All current evaluation sets have informed development. The next design needs a fresh set (`eval15` is the currently named next set), plus independently supplied projects before making claims about ordinary deployment accuracy.

The final handoff should include revised PDFs, editable sources, the new snapshot, updated evidence and the edition note. That is what the next update can start from.
