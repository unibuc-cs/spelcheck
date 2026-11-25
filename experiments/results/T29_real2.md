# Evaluation of the change check (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T22:37:19)

16 specs, 16 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 13 | 0/0 | 0/0 | 42 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 7 | 0/0 | 0/0 | 23 |
| without assumed facts and links | 0/0 |  | 0/0 | 5 | 0/0 | 0/0 | 9 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 13 |
| doubtful findings set aside | 0/0 |  | 0/0 | 13 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 68 where nothing was planted.
- Labels: 16 of 16 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 121 requests, 129,637 tokens read, 83,481 tokens written (16 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-skip-specs-archive-option_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-08-19-adopt-verb-noun-cli-structure_real | 1 | nothing expected | [R4, R10]: 1 | 1 | 0 | 0 |
| 2025-09-29-add-agents-md-config_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-09-29-improve-init-onboarding_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-10-14-add-codex-slash-command-support_real | 1 | nothing expected | [R1, R4]: 1, [R17, R28]: 1 | 4 | 0 | 0 |
| 2025-10-14-add-non-interactive-init-options_real | 1 | nothing expected | [R1, R19]: 1, [R5, R19]: 1, [R6, R19]: 1 | 0 | 0 | 1 |
| 2025-10-14-update-cli-init-enter-selection_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-10-22-add-crush-support_real | 1 | nothing expected | none | 0 | 0 | 1 |
| 2025-12-28-restructure-schema-directories_real | 1 | nothing expected | none | 2 | 0 | 0 |
| 2026-02-17-multi-provider-skill-generation_real | 1 | nothing expected | [R27, R52]: 1, [R27, R53]: 1 | 0 | 0 | 1 |
| 2026-07-28-fix-schema-init-force-validation-order_real | 1 | nothing expected | none | 0 | 0 | 2 |
| 2026-10-19-add-init-agents-target_real | 1 | nothing expected | [R16, R40]: 1, [R16, R41]: 1, [R38, R50]: 1, [R49, R50]: 1 | 3 | 0 | 18 |
| 2026-10-19-add-validation-findings-report_real | 1 | nothing expected | none | 1 | 0 | 1 |
| 2026-10-19-fix-opencode-commands-directory_real | 1 | nothing expected | none | 2 | 0 | 1 |
| 2026-10-19-fix-windows-archive-claim-release_real | 1 | nothing expected | none | 0 | 0 | 9 |
| 2026-10-19-suppress-telemetry-notice-in-json_real | 1 | nothing expected | [R10, R11]: 1 | 0 | 0 | 6 |
