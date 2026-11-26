# Evaluation of the change check (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T15:21:04)

16 specs, 16 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 25 | 0/0 | 0/0 | 42 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 19 | 0/0 | 0/0 | 27 |
| without assumed facts and links | 0/0 |  | 0/0 | 11 | 0/0 | 0/0 | 22 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 12 |
| doubtful findings set aside | 0/0 |  | 0/0 | 12 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 31 where nothing was planted.
- Labels: 16 of 16 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 147 requests, 164,667 tokens read, 96,048 tokens written (16 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-skip-specs-archive-option_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-08-19-adopt-verb-noun-cli-structure_real | 1 | nothing expected | [R4, R10]: 1 | 1 | 0 | 0 |
| 2025-09-29-add-agents-md-config_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-09-29-improve-init-onboarding_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-10-14-add-codex-slash-command-support_real | 1 | nothing expected | none | 4 | 0 | 1 |
| 2025-10-14-add-non-interactive-init-options_real | 1 | nothing expected | [R11, R20]: 1, [R4, R17]: 1, [R4, R18]: 1, [R4, R19]: 1, [R4, R20]: 1 | 0 | 0 | 3 |
| 2025-10-14-update-cli-init-enter-selection_real | 1 | nothing expected | none | 0 | 0 | 4 |
| 2025-10-22-add-crush-support_real | 1 | nothing expected | none | 0 | 0 | 3 |
| 2025-12-28-restructure-schema-directories_real | 1 | nothing expected | [R1, R3]: 1, [R1, R4]: 1, [R1, R5]: 1, [R1, R6]: 1 | 1 | 0 | 3 |
| 2026-02-17-multi-provider-skill-generation_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2026-07-28-fix-schema-init-force-validation-order_real | 1 | nothing expected | [R1, R13]: 1 | 0 | 0 | 4 |
| 2026-10-19-add-init-agents-target_real | 1 | nothing expected | none | 2 | 0 | 9 |
| 2026-10-19-add-validation-findings-report_real | 1 | nothing expected | [R11, R22]: 1, [R11, R41]: 1, [R11, R49]: 1, [R11, R52]: 1, [R28, R52]: 1, [R37, R40]: 1, [R37, R41]: 1, [R7, R41]: 1, [R7, R52]: 1, [R8, R40]: 1, [R8, R41]: 1, [R8, R52]: 1 | 1 | 0 | 1 |
| 2026-10-19-fix-opencode-commands-directory_real | 1 | nothing expected | none | 3 | 0 | 0 |
| 2026-10-19-fix-windows-archive-claim-release_real | 1 | nothing expected | none | 0 | 0 | 7 |
| 2026-10-19-suppress-telemetry-notice-in-json_real | 1 | nothing expected | [R10, R11]: 1, [R11, R14]: 1 | 0 | 0 | 4 |
