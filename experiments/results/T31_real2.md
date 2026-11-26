# Evaluation of the change check (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T14:48:09)

16 specs, 16 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 18 | 0/0 | 0/0 | 40 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 15 | 0/0 | 0/0 | 28 |
| without assumed facts and links | 0/0 |  | 0/0 | 7 | 0/0 | 0/0 | 13 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 8 |
| doubtful findings set aside | 0/0 |  | 0/0 | 8 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 20 where nothing was planted.
- Labels: 16 of 16 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 158 requests, 195,783 tokens read, 108,805 tokens written (16 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-skip-specs-archive-option_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-08-19-adopt-verb-noun-cli-structure_real | 1 | nothing expected | [R1, R8]: 1, [R4, R10]: 1, [R8, R9]: 1 | 0 | 0 | 1 |
| 2025-09-29-add-agents-md-config_real | 1 | nothing expected | [R18, R19]: 1 | 0 | 0 | 0 |
| 2025-09-29-improve-init-onboarding_real | 1 | nothing expected | none | 0 | 0 | 2 |
| 2025-10-14-add-codex-slash-command-support_real | 1 | nothing expected | none | 0 | 0 | 3 |
| 2025-10-14-add-non-interactive-init-options_real | 1 | nothing expected | [R4, R17]: 1, [R4, R19]: 1, [R4, R20]: 1 | 1 | 0 | 3 |
| 2025-10-14-update-cli-init-enter-selection_real | 1 | nothing expected | none | 0 | 0 | 0 |
| 2025-10-22-add-crush-support_real | 1 | nothing expected | none | 0 | 0 | 2 |
| 2025-12-28-restructure-schema-directories_real | 1 | nothing expected | [R1, R3]: 1, [R1, R4]: 1, [R1, R5]: 1 | 0 | 0 | 6 |
| 2026-02-17-multi-provider-skill-generation_real | 1 | nothing expected | [R34, R38]: 1, [R44, R45, R46]: 1 | 0 | 0 | 2 |
| 2026-07-28-fix-schema-init-force-validation-order_real | 1 | nothing expected | [R1, R12]: 1, [R1, R13]: 1 | 0 | 0 | 4 |
| 2026-10-19-add-init-agents-target_real | 1 | nothing expected | [R18, R50]: 1 | 5 | 0 | 5 |
| 2026-10-19-add-validation-findings-report_real | 1 | nothing expected | [R20, R27]: 1, [R20, R38]: 1 | 0 | 0 | 0 |
| 2026-10-19-fix-opencode-commands-directory_real | 1 | nothing expected | none | 2 | 0 | 0 |
| 2026-10-19-fix-windows-archive-claim-release_real | 1 | nothing expected | none | 0 | 0 | 6 |
| 2026-10-19-suppress-telemetry-notice-in-json_real | 1 | nothing expected | [R10, R11]: 1 | 0 | 0 | 6 |
