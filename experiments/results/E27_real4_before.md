# Evaluation of the change check (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T15:35:07)

26 specs, 52 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | planted | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 24/26 | 24/26 | 0/0 | 329 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 24/26 | 24/26 | 0/0 | 148 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 15/26 | 15/26 | 0/0 | 217 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 79 |
| doubtful findings set aside | 0/0 |  | 0/0 | 77 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 202 where nothing was planted.
- Labels: 52 of 52 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 116 requests, 110,420 tokens read, 73,587 tokens written (52 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-bulk-validation-interactive-selection_planted | 2 | [R6, R22]: 0/2 | [R1, R21]: 2, [R1, R2]: 2, [R18, R20]: 1, [R3, R21]: 2, [R3, R4]: 2, [R5, R6]: 1, [R7, R18]: 1 | 6 | 0 | 0 |
| 2025-08-19-bulk-validation-interactive-selection_real | 2 | nothing expected | [R1, R21]: 2, [R1, R2]: 2, [R2, R5]: 1, [R4, R5]: 2, [R5, R21]: 1, [R5, R6]: 2, [R7, R18]: 2 | 6 | 0 | 0 |
| 2025-09-12-add-view-dashboard-command_planted | 2 | [R2, R15]: 2/2 | [R1, R6]: 1, [R6, R8]: 1 | 0 | 0 | 0 |
| 2025-09-12-add-view-dashboard-command_real | 2 | nothing expected | [R1, R2]: 1, [R1, R6]: 2, [R4, R10]: 2, [R4, R11]: 1, [R4, R12]: 1, [R4, R5]: 1, [R4, R7]: 1, [R6, R8]: 2 | 1 | 0 | 0 |
| 2025-11-06-add-shell-completions_planted | 2 | [R5, R32]: 2/2 | [R1, R2]: 1, [R14, R22]: 2, [R14, R23]: 2, [R14, R25]: 2, [R17, R22]: 2, [R17, R23]: 2, [R17, R25]: 2 | 0 | 0 | 0 |
| 2025-11-06-add-shell-completions_real | 2 | nothing expected | [R1, R2]: 2 | 0 | 0 | 0 |
| 2025-12-21-add-config-command_planted | 2 | [R7, R26]: 2/2 | [R10, R11]: 2, [R10, R12]: 2, [R10, R17]: 2, [R11, R12]: 2, [R11, R23]: 1, [R12, R23]: 1, [R14, R17]: 2, [R15, R17]: 2, [R15, R18]: 2, [R15, R20]: 2, [R15, R23]: 2, [R15, R25]: 2, [R18, R22]: 2, [R2, R18]: 2, [R2, R20]: 2, [R2, R23]: 2, [R2, R25]: 2, [R20, R22]: 2, [R22, R25]: 2, [R5, R18]: 2, [R5, R20]: 2, [R5, R25]: 2, [R5, R8]: 2, [R9, R10]: 1, [R9, R17]: 2, [R9, R23]: 1 | 0 | 0 | 0 |
| 2025-12-21-add-config-command_real | 2 | nothing expected | [R1, R15]: 1, [R1, R17]: 1, [R1, R18]: 1, [R1, R20]: 1, [R1, R23]: 1, [R1, R25]: 1, [R1, R2]: 1, [R1, R3]: 1, [R1, R4]: 1, [R1, R5]: 1, [R1, R7]: 2, [R1, R8]: 1, [R10, R12]: 1, [R10, R15]: 1, [R10, R17]: 1, [R10, R18]: 1, [R10, R20]: 1, [R10, R25]: 1, [R11, R12]: 1, [R14, R17]: 2, [R14, R18]: 1, [R14, R20]: 1, [R14, R23]: 1, [R14, R25]: 1, [R15, R18]: 2, [R15, R20]: 2, [R15, R23]: 1, [R15, R25]: 2, [R18, R22]: 2, [R2, R10]: 1, [R2, R14]: 1, [R2, R15]: 1, [R2, R18]: 2, [R2, R20]: 2, [R2, R23]: 1, [R2, R25]: 2, [R2, R3]: 1, [R2, R4]: 1, [R2, R5]: 1, [R2, R7]: 2, [R2, R8]: 1, [R20, R22]: 2, [R22, R25]: 2, [R3, R10]: 1, [R3, R14]: 1, [R3, R15]: 1, [R3, R18]: 1, [R3, R20]: 1, [R3, R23]: 1, [R3, R25]: 1, [R3, R4]: 2, [R3, R5]: 1, [R3, R7]: 1, [R3, R8]: 2, [R4, R10]: 1, [R4, R14]: 1, [R4, R15]: 1, [R4, R18]: 1, [R4, R20]: 1, [R4, R23]: 1, [R4, R25]: 1, [R4, R5]: 1, [R4, R7]: 1, [R5, R10]: 1, [R5, R14]: 1, [R5, R15]: 1, [R5, R18]: 2, [R5, R20]: 2, [R5, R25]: 2, [R7, R10]: 1, [R7, R14]: 1, [R7, R15]: 2, [R7, R18]: 1, [R7, R20]: 1, [R7, R25]: 1, [R8, R10]: 1, [R8, R14]: 1, [R8, R15]: 1, [R8, R18]: 1, [R8, R20]: 1, [R8, R25]: 1, [R9, R12]: 1 | 0 | 0 | 0 |
| 2025-12-24-add-artifact-graph-core_planted | 2 | [R3, R22]: 2/2 | [R15, R16]: 2, [R2, R22]: 1, [R9, R13]: 2 | 4 | 0 | 0 |
| 2025-12-24-add-artifact-graph-core_real | 2 | nothing expected | [R1, R3]: 2, [R1, R4]: 2, [R1, R5]: 2, [R10, R11]: 1, [R11, R13]: 1, [R15, R16]: 2, [R9, R12]: 1, [R9, R13]: 1 | 10 | 0 | 0 |
| 2025-12-25-add-change-manager_planted | 2 | [R2, R15]: 2/2 | [R5, R9]: 1, [R6, R9]: 1, [R7, R9]: 1 | 3 | 0 | 0 |
| 2025-12-25-add-change-manager_real | 2 | nothing expected | [R1, R2]: 2, [R2, R4]: 2, [R5, R11]: 1, [R6, R11]: 1, [R7, R11]: 1 | 3 | 0 | 0 |
| 2025-12-28-add-artifact-workflow-cli_planted | 2 | [R5, R30]: 2/2 | [R25, R26]: 2, [R6, R7]: 2 | 5 | 0 | 0 |
| 2025-12-28-add-artifact-workflow-cli_real | 2 | nothing expected | [R2, R27]: 1, [R25, R26]: 1, [R6, R27]: 1, [R6, R7]: 1 | 5 | 0 | 0 |
| 2026-01-06-opsx-archive-command_planted | 2 | [R7, R15]: 2/2 | [R1, R11]: 1, [R3, R11]: 1, [R3, R9]: 1, [R4, R11]: 1, [R4, R5]: 1, [R5, R11]: 1, [R6, R11]: 1, [R9, R11]: 1 | 5 | 0 | 0 |
| 2026-01-06-opsx-archive-command_real | 2 | nothing expected | [R10, R11]: 1, [R4, R5]: 1, [R5, R7]: 2 | 4 | 0 | 0 |
| 2026-02-17-add-feedback-command_planted | 2 | [R14, R22]: 2/2 | [R1, R4]: 2, [R1, R7]: 2 | 2 | 0 | 0 |
| 2026-02-17-add-feedback-command_real | 2 | nothing expected | [R1, R4]: 2, [R1, R7]: 1, [R4, R12]: 1, [R4, R13]: 1, [R4, R15]: 1, [R4, R8]: 1, [R7, R12]: 1, [R7, R13]: 1, [R7, R15]: 1 | 4 | 0 | 0 |
| 2026-02-17-add-opsx-onboard-skill_planted | 2 | [R3, R18]: 2/2 | none | 0 | 0 | 0 |
| 2026-02-17-add-opsx-onboard-skill_real | 2 | nothing expected | none | 0 | 0 | 0 |
| 2026-02-17-add-verify-skill_planted | 2 | [R14, R27]: 2/2 | [R20, R21]: 1, [R4, R6]: 2 | 2 | 0 | 0 |
| 2026-02-17-add-verify-skill_real | 2 | nothing expected | [R14, R15]: 2, [R14, R16]: 1, [R20, R23]: 1, [R3, R24]: 1, [R3, R25]: 1, [R3, R26]: 1, [R4, R6]: 2 | 2 | 0 | 0 |
| 2026-10-19-add-update-workflow_planted | 2 | [R2, R24]: 2/2 | [R10, R11]: 1, [R19, R20]: 1, [R3, R17]: 2, [R3, R20]: 1 | 7 | 0 | 0 |
| 2026-10-19-add-update-workflow_real | 2 | nothing expected | [R19, R20]: 2, [R2, R18]: 2, [R2, R22]: 2, [R3, R17]: 2, [R3, R20]: 1, [R7, R18]: 1 | 7 | 0 | 0 |
| 2026-10-19-add-version-command_planted | 2 | [R3, R15]: 2/2 | [R10, R12]: 2, [R11, R12]: 2, [R6, R10]: 2, [R6, R11]: 2, [R6, R12]: 2, [R6, R7]: 2, [R6, R8]: 2, [R7, R12]: 2, [R7, R8]: 2, [R8, R10]: 2, [R8, R11]: 2 | 2 | 0 | 0 |
| 2026-10-19-add-version-command_real | 2 | nothing expected | [R1, R3]: 2, [R11, R12]: 2, [R3, R4]: 2, [R4, R12]: 2, [R5, R8]: 1, [R6, R11]: 2, [R6, R12]: 2, [R6, R7]: 1, [R6, R8]: 2, [R7, R12]: 1, [R7, R8]: 1, [R8, R11]: 2 | 1 | 0 | 0 |
