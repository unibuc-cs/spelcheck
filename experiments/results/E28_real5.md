# Evaluation of the change check (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T18:20:54)

16 specs, 32 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | planted | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 10/16 | 10/16 | 0/0 | 80 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 6/16 | 6/16 | 0/0 | 56 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 9/16 | 9/16 | 0/0 | 37 | 0/0 | 0/0 | 0 |
| without the questions about conditions | 10/16 | 10/16 | 0/0 | 87 | 0/0 | 0/0 | 0 |
| without the questions about conditions, doubtful set aside | 6/16 | 6/16 | 0/0 | 63 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 32 |
| doubtful findings set aside | 0/0 |  | 0/0 | 32 |
| without the questions about conditions | 0/0 |  | 0/0 | 32 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 0/0 | 32 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 77 where nothing was planted.
- Labels: 32 of 32 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 96 requests, 82,300 tokens read, 58,759 tokens written (32 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-interactive-show-command_planted | 2 | [R10, R12]: 2/2 | [R11, R12]: 2, [R2, R3]: 2, [R3, R4]: 2, [R5, R10]: 1, [R5, R11]: 1, [R5, R8]: 1, [R8, R12]: 2 | 4 | 0 | 0 |
| 2025-08-19-add-interactive-show-command_real | 2 | nothing expected | [R1, R2]: 2, [R12, R13]: 1, [R3, R4]: 2 | 4 | 0 | 0 |
| 2025-12-20-add-global-config-dir_planted | 2 | [R2, R12]: 0/2 | [R1, R12]: 1, [R1, R3]: 1, [R3, R12]: 1, [R5, R7]: 2, [R5, R8]: 2 | 0 | 0 | 0 |
| 2025-12-20-add-global-config-dir_real | 2 | nothing expected | [R5, R7]: 2, [R5, R8]: 2, [R6, R11]: 1 | 4 | 0 | 0 |
| 2025-12-28-add-instruction-loader_planted | 2 | [R2, R14]: 2/2 | none | 0 | 0 | 0 |
| 2025-12-28-add-instruction-loader_real | 2 | nothing expected | [R7, R10]: 2 | 0 | 0 | 0 |
| 2026-01-07-add-nix-flake-support_planted | 2 | [R9, R13]: 1/2 | [R10, R13]: 2 | 0 | 0 | 0 |
| 2026-01-07-add-nix-flake-support_real | 2 | nothing expected | none | 0 | 0 | 0 |
| 2026-01-09-add-flake-update-script_planted | 2 | [R5, R14]: 1/2 | [R1, R2]: 2 | 2 | 0 | 0 |
| 2026-01-09-add-flake-update-script_real | 2 | nothing expected | [R1, R2]: 2 | 2 | 0 | 0 |
| 2026-01-15-add-nix-ci-validation_planted | 2 | [R2, R14]: 1/2 | [R8, R11]: 1 | 0 | 0 | 0 |
| 2026-01-15-add-nix-ci-validation_real | 2 | nothing expected | [R1, R2]: 1 | 0 | 0 | 0 |
| 2026-02-17-project-local-schemas_planted | 2 | [R5, R14]: 2/2 | none | 6 | 0 | 0 |
| 2026-02-17-project-local-schemas_real | 2 | nothing expected | [R3, R6]: 1, [R4, R6]: 1, [R6, R11]: 1, [R6, R12]: 1 | 7 | 0 | 0 |
| 2026-02-17-schema-management-cli_planted | 2 | [R24, R35]: 1/2 | [R1, R4]: 2, [R1, R6]: 1, [R11, R12]: 1, [R11, R21]: 1, [R12, R35]: 1, [R13, R35]: 1, [R17, R19]: 1, [R25, R35]: 2, [R27, R35]: 2, [R30, R35]: 2, [R31, R35]: 2, [R35, R39]: 2, [R4, R35]: 1, [R4, R5]: 1, [R41, R45]: 1 | 2 | 0 | 0 |
| 2026-02-17-schema-management-cli_real | 2 | nothing expected | [R1, R30]: 1, [R1, R31]: 1, [R1, R4]: 1, [R11, R12]: 1, [R11, R13]: 1, [R11, R30]: 1, [R11, R31]: 1, [R11, R38]: 1, [R14, R16]: 1, [R14, R20]: 1, [R15, R16]: 1, [R15, R20]: 1, [R17, R19]: 1, [R18, R19]: 1, [R40, R41]: 1, [R40, R44]: 1, [R6, R20]: 1 | 1 | 0 | 0 |
