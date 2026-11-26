# speccheck: management paper and presentation

Start with **[paper.pdf](paper.pdf)**: 37 pages, comprising 2 front-matter pages, 18 main-text pages, 1 reference page and 16 appendix pages. The companion **[slides.pdf](slides.pdf)** has 32 main slides and 11 appendix slides, 43 in total. Authentication is the presentation's running example, from the early definitions through OpenSpec change checking. The paper also retains order processing as a secondary example. Deletion versus retention is a brief supporting example for assumptions. Both documents describe source revision `498dea06df250964013b2abb2b06c94d341b223b`. The paper edition is dated 25 November 2026; an introductory slide was added on 26 November.

The language is deliberately colleague-to-colleague. Essential definitions, short listings and examples stay in the main argument. Detailed pseudocode and replay instructions are in the technical appendices. Constructed examples are distinguished from saved experiment output.

## What changed in this edition

The presentation now explains the four finding types together, before the detailed method. It follows six sections: Problem and example, Findings, Method, Changes, Evaluation, and Limitations and next steps. Slide titles name the topic within each section. The authentication specification is introduced first, and the definitions use its predicates and concrete cases throughout. This editorial revision retains the application baseline and historical evaluation results.

The 26 November addition is **The proposed administrator exception**, immediately after the existing-project overview. It shows the actual ADDED Administrator Access requirement and the concrete clash at five failed attempts: lock the administrator account versus do not lock it. The later detailed change slide remains in place. The paper and source baseline are unchanged.

The early overview distinguishes conflicts, gaps, ambiguity and generated scenarios. Each definition has a small formal question and a witness. Generated scenarios include both allowed and ruled-out consequences; they are output examples, distinct from the OpenSpec scenarios in the input. A solver witness can show that two readings differ, but does not establish which English interpretation is intended.

The later OpenSpec walkthrough explains delta operations and scenario provenance using the same project. The saved administrator change uses ADDED only. A separate constructed variation removes the invalid-password response and demonstrates gap attribution. A workflow diagram explains what saved-base reuse preserves and what still gets checked.

E19 and E20 extend the evaluation. The cost comparison includes the initial base-building cost and the measured loss in conflict detection. Full formalization remains the default. Incremental mode currently extracts scenario edits; a requirement-sentence-only edit can reuse the old model without translating the new sentence. This limitation is explicit in the method and discussion.

See **[EDITION-2026-11-25.md](EDITION-2026-11-25.md)** for the changes, evidence boundaries and preserved revisions.

## What is included

- `paper.tex` and `sections/`: the paper, algorithms and bibliography.
- `slides.tex`: the Beamer deck, including presenter notes in the source.
- `shared/`: common notation, colors, and editable diagrams.
- `evidence/`: evaluation metrics, claims-to-source index, review records and checked examples.
- `snapshot/2026-11-24-498dea0/`: complete tracked source and recorded evidence for this edition, with checksums.
- `snapshot/2026-11-24-18752f2/`: the previous source snapshot, preserved unchanged.
- `UPDATE.md`: how to update this edition when the project changes.
- `scripts/`: build, snapshot verification, comparison, packaging and example checks.

Snapshot directory dates are the source commits' dates. The archived application commit is dated 24 November; the paper was revised on 25 November and the slide introduction on 26 November. Later application code and results in the user's current project are outside this edition's preserved source and evidence. The update uses the archived `498dea0` implementation and leaves current project work alone. Earlier delivery ZIPs remain in the working folder and are excluded from the new delivery ZIP; their names and checksums are recorded in the edition notes.

## Structure and presentation route

The paper and presentation cover the same six topics. The table gives the slide order, with Findings before Method so the audience sees the four types before the implementation. The paper introduces the definitions in its opening discussion and keeps its detailed Method section before Findings. The cover is slide 1. Detailed algorithms are in the appendix, with links from the main slides and back.

| Main slides | Part |
| --- | --- |
| 2-5 | 1. Problem and example |
| 6-10 | 2. Findings |
| 11-15 | 3. Method |
| 16-21 | 4. Changes |
| 22-28 | 5. Evaluation |
| 29-32 | 6. Limitations and next steps |

Slide 2 introduces the existing project and slide 3 its proposed administrator change. Slide 5 introduces the four questions. Slides 6-10 define the authentication predicates, conflict, gap, ambiguity and generated scenarios in that order. Appendix A gives the authentication model; the order example is no longer part of the slide walkthrough.

Appendices A-K occupy PDF pages 33-43 and are for questions, outside the planned 34 minutes 30 seconds for the main talk. The active presenter-note timings total 2,070 seconds; the cover note remains commented out. This is a pacing plan, not a measured rehearsal. The main slides retain short listings and diagrams; all eleven detailed algorithms are available in the paper's technical appendices. Review records in `evidence/` identify the document version checked.

The earlier 25 November review covered all 37 paper pages and the previous 42-slide deck, with clean builds. The [26 November slide review](evidence/slide-update-2026-11-26.json) records the insertion, its match to the archived delta, the clean 43-page build and checked navigation. The pre-edit slide source and PDF are preserved in `build/before-admin-intro-2026-11-26/`.

The evaluation distinguishes conflict detection and extra alarms, ambiguity and extra questions, changes in context, and scale/cost. Historical E17 and E18 results keep their original identities. E19 tested design `07ecd38`; E20 tested `373ae4c`. The current cache and command-line restrictions in `498dea0` were added after E20 and were not measured by it.

Source pointers remain in the editable LaTeX and evidence index. Internal file references, package instructions and review notes do not appear as paper or slide footers.

## Read the examples

The links below are pinned to the documented source revision, so future repository changes do not alter the examples discussed here.

- **[Authentication base specification (OpenSpec)](https://github.com/unibuc-cs/spelcheck/blob/498dea06df250964013b2abb2b06c94d341b223b/specs/auth_change/openspec/specs/auth/spec.md):** the main running example, with four login and account-lockout scenarios, including the phrase "reaches 5" used to explain ambiguity.
- **[Administrator-access change (OpenSpec)](https://github.com/unibuc-cs/spelcheck/blob/498dea06df250964013b2abb2b06c94d341b223b/specs/auth_change/openspec/changes/admin-never-locked/specs/auth/spec.md):** the proposed requirement that administrators must not be locked out. It shows why a change must be checked with the existing specification.
- **[Order requirements (EARS)](https://github.com/unibuc-cs/spelcheck/blob/498dea06df250964013b2abb2b06c94d341b223b/specs/order/requirements.md):** a secondary worked example retained in the paper, with separate order rule IDs and predicates. Its removal variation is constructed; no OpenSpec order project is claimed.

These small cases let the audience follow each reasoning step and check it by hand. They explain the method; the separate evaluation section reports measured results and their limits. The examples do not establish performance on independent production requirements.

The slides abbreviate the saved authentication symbols as `p` (password submitted), `v` (password correct), `g` (access granted), `d` (access denied), `n` (failed attempts), `ell` (account locked), and `h` (administrator). The examples use separate versions of the same project:

| Finding | Version and witness |
| --- | --- |
| Conflict | Actual administrator addition: `n=5`, `h=true`; R3 requires lockout and R5 forbids it. |
| Gap | Constructed baseline variation without R2: `p=true`, `v=false`, `ell=false`, `n=0`; no conditional response applies. |
| Ambiguity | Original threshold: `n=6`, `ell=false` separates exactly five from five or more. |
| Generated scenario | Original baseline allows `g=true` without `p`; with R5 added, a locked administrator submitting a password is ruled out by R5 alone. |

These are not four defects in one unchanged document. The gap and allowed snapshot are constructed from the saved baseline-rule readings, while the administrator conflict and threshold probe have saved evidence. The scenario examples describe one snapshot, not a history of previous logins.

For OpenSpec, existing capability specifications live under `openspec/specs/`; a proposed change holds its delta specifications under `openspec/changes/<change>/specs/`. The checker loads the existing project and combines it with that delta for analysis without archiving or overwriting the base. Authentication already has Login and Account Lockout requirements; its actual administrator delta adds one requirement to the existing `auth` capability. The saved base contains older findings, so it is not presented as defect-free.

The implementation in `speccheck/change.py` applies **RENAMED → REMOVED → MODIFIED → ADDED**, regardless of section order in the delta. A rename changes the name used by later operations. MODIFIED contains the full new body of the named requirement, including every scenario that should remain; unrelated requirements omitted from the delta stay unchanged. A new capability can be introduced at a new path through ADDED requirements.

Within a modified requirement, the scenario name and normalized body determine its state: `existing` for the same name and text, `modified` for the same name with different text, `added` for a new name, and `removed` when an old name is omitted or its requirement is removed. Normalization ignores case, extra whitespace and selected Markdown marks; it does not establish semantic equivalence. The four original authentication scenarios remain `existing` in the actual administrator change, and the fifth is `added`.

## Build the PDFs

Use a TeX installation with pdfLaTeX, BibTeX, Beamer, TikZ/PGFPlots, newtx, algorithm/algorithmicx, natbib, cleveref and the standard packages in the preambles. The build uses direct passes; Perl and latexmk are not required.

From the repository root in PowerShell:

```powershell
& .\docs\management\scripts\build.ps1
```

From a standalone delivered folder, run `scripts/build.ps1` there. It resolves paths from its own location. Use `-Target paper` or `-Target slides` to build just one. Add `-Render` to create page images using `pdftoppm`; rendering tools are not needed merely to compile the PDFs. Logs and previews go under `build/`.

If an earlier PDF is open and Windows prevents replacement, use `-PdfSuffix '-updated'` to write separate PDFs. To package those under the standard names, run `scripts/package.ps1 -PaperPdf <paper path> -SlidesPdf <slides path>`. Earlier PDF variants remain in the working folder and are excluded from the delivery ZIP.

The stored `speccheck-management-2026-11-25.zip` is the previous packaged edition; its adjacent `.sha256` file records the checksum. The current slide source and PDF include the 26 November addition, which is outside that ZIP. Both source snapshots are included in the packaged edition; previous delivery ZIPs are not nested inside it. The delivery before the earlier definition-focused revision is preserved as `speccheck-management-2026-11-25-before-finding-definitions.zip`, with SHA-256 `2e013a9fc325d28884fd1c2486afece2194ddde1918398c73156f8a3943a1713`. The edition notes list earlier preserved deliveries as well.

The diagrams and charts are native LaTeX/TikZ/PGFPlots sources. The paper and slides have no network dependency at build time.

## Recheck the examples

Extract the current snapshot into `build/baseline-498dea0`. In the original repository:

```powershell
& .\docs\management\scripts\snapshot.ps1 `
  -ExtractTo .\docs\management\build\baseline-498dea0
```

In a standalone package, unzip `snapshot/2026-11-24-498dea0/source.zip` into that directory and use the comparison script described in `UPDATE.md`.

With the project dependencies from the archived `uv.lock` available, run the example script using that project's interpreter. For the current Windows workspace:

```powershell
& .\.venv\Scripts\python.exe .\docs\management\scripts\verify-examples.py
```

The script imports the extracted source and checks 40 examples and boundary cases. Nine authentication checks cover the saved conflict and ambiguity, exact formula/event details, the constructed missing-response case, and allowed and ruled-out consequences. The other checks cover order and visitor examples, removal attribution, event retirement and unsupported sentence-only incremental edits. All 40 passed without LLM calls; results are in `evidence/example-checks.json`. The archived project also has a recorded run of 70 offline tests; see `evidence/validation.json`.

The original model experiments remain historical evidence. This package does not include model weights or GPU services and does not claim that resampling will recreate identical model answers.

## Updating later

Keep the whole package, especially the snapshot and evidence index. Follow **[UPDATE.md](UPDATE.md)** and compare the next source version with the archived revision first. The update can then identify which explanations, diagrams, examples and evaluation claims need to change without relying on chat history.
