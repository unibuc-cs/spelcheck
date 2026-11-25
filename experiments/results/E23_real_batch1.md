# Evaluation of the change check (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T16:25:17)

16 specs, 11 runs scored, 5 failed.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 29 | 0/0 | 0/0 | 39 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 29 | 0/0 | 0/0 | 21 |
| without assumed facts and links | 0/0 |  | 0/0 | 3 | 0/0 | 0/0 | 21 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 10 |
| doubtful findings set aside | 0/0 |  | 0/0 | 10 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 34 where nothing was planted.
- Labels: 11 of 16 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 140 requests, 188,311 tokens read, 94,283 tokens written (11 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-change-commands_real | 1 | nothing expected | [R1, R10]: 1, [R1, R7]: 1, [R10, R12]: 1, [R10, R13]: 1, [R10, R14]: 1, [R10, R15]: 1, [R10, R17]: 1, [R7, R12]: 1, [R7, R13]: 1, [R7, R14]: 1, [R7, R15]: 1, [R7, R17]: 1 | 1 | 0 | 12 |
| 2025-08-19-adopt-delta-based-changes_real | 1 | nothing expected | none | 1 | 0 | 1 |
| 2025-08-19-structured-spec-format_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-09-29-add-slash-command-support_real | 1 | nothing expected | none | 0 | 0 | 3 |
| 2025-09-29-update-markdown-parser-crlf_real | 0 | nothing expected | none | 0 | 0 | 0 |
| 2025-10-14-add-kilocode-workflows_real | 1 | nothing expected | none | 0 | 0 | 5 |
| 2025-10-14-enhance-validation-error-messages_real | 0 | nothing expected | none | 0 | 0 | 0 |
| 2025-10-22-add-cline-support_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-12-23-extend-shell-completions_real | 1 | nothing expected | [R1, R10]: 1, [R1, R8]: 1, [R1, R9]: 1, [R2, R10]: 1, [R2, R19]: 1, [R2, R32]: 1, [R2, R9]: 1, [R3, R10]: 1, [R3, R32]: 1, [R3, R8]: 1, [R4, R8]: 1, [R4, R9]: 1, [R8, R10]: 1, [R8, R9]: 1, [R9, R10]: 1 | 3 | 0 | 5 |
| 2026-01-06-make-apply-instructions-schema-aware_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2026-07-11-add-grok-build-skills-only-support_real | 0 | nothing expected | none | 0 | 0 | 0 |
| 2026-10-19-add-amp-support_real | 1 | nothing expected | none | 2 | 0 | 10 |
| 2026-10-19-add-status-next-step_real | 1 | nothing expected | none | 1 | 0 | 0 |
| 2026-10-19-fix-cli-local-date-semantics_real | 0 | nothing expected | none | 0 | 0 | 0 |
| 2026-10-19-fix-spec-parser-fidelity_real | 0 | nothing expected | none | 0 | 0 | 0 |
| 2026-10-19-spec-diffs_real | 1 | nothing expected | [R16, R18]: 1, [R6, R12]: 1 | 2 | 0 | 1 |
