# Evaluation of the change check (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T10:52:39)

16 specs, 32 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 78 | 0/0 | 0/0 | 104 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 30 | 0/0 | 0/0 | 46 |
| without assumed facts and links | 0/0 |  | 0/0 | 38 | 0/0 | 0/0 | 40 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 26 |
| doubtful findings set aside | 0/0 |  | 0/0 | 26 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 68 where nothing was planted.
- Labels: 32 of 32 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 145 requests, 175,616 tokens read, 100,978 tokens written (32 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-zod-validation_real | 2 | nothing expected | none | 0 | 0 | 4 |
| 2025-08-19-fix-update-tool-selection_real | 2 | nothing expected | [R5, R8]: 1 | 1 | 0 | 1 |
| 2025-09-29-add-multi-agent-init_real | 2 | nothing expected | [R13, R15]: 1, [R7, R15]: 1 | 3 | 0 | 0 |
| 2025-09-29-update-agent-file-name_real | 2 | nothing expected | none | 2 | 0 | 3 |
| 2025-10-14-add-github-copilot-prompts_real | 2 | nothing expected | none | 1 | 0 | 7 |
| 2025-10-14-add-windsurf-workflows_real | 2 | nothing expected | none | 1 | 0 | 6 |
| 2025-10-14-update-cli-init-root-agents_real | 2 | nothing expected | [R13, R24]: 1 | 0 | 0 | 6 |
| 2025-10-22-add-factory-slash-commands_real | 2 | nothing expected | [R11, R16, R31]: 1, [R11, R35]: 1, [R2, R16, R31]: 1, [R3, R35]: 1, [R6, R16, R31]: 1, [R6, R35]: 1 | 0 | 0 | 7 |
| 2026-01-06-add-per-change-schema-metadata_real | 2 | nothing expected | [R18, R21]: 1, [R18, R32]: 2, [R22, R23]: 1 | 6 | 0 | 4 |
| 2026-04-23-add-kimi-cli-skills-only-support_real | 2 | nothing expected | [R25, R27]: 1 | 2 | 0 | 9 |
| 2026-08-15-add-dsh-support_real | 2 | nothing expected | [R3, R5]: 1, [R3, R8]: 1, [R4, R5]: 1, [R4, R8]: 1, [R5, R6]: 1, [R5, R7]: 1, [R5, R8]: 1, [R6, R8]: 1, [R7, R8]: 1 | 1 | 0 | 7 |
| 2026-10-19-add-skill-cli-auto-approval_real | 2 | nothing expected | none | 0 | 0 | 6 |
| 2026-10-19-fix-archive-retirement-guidance_real | 2 | nothing expected | none | 0 | 0 | 13 |
| 2026-10-19-fix-schemas-root-selection_real | 2 | nothing expected | [R29, R38]: 1, [R31, R37]: 2, [R32, R37]: 2, [R33, R37]: 2, [R37, R40]: 2, [R38, R39]: 1 | 0 | 0 | 2 |
| 2026-10-19-rename-bob-to-ibm-bob_real | 2 | nothing expected | [R13, R16]: 1 | 2 | 0 | 1 |
| 2026-10-19-warn-on-purpose-placeholder_real | 2 | nothing expected | [R1, R32]: 2, [R1, R4, R40]: 1, [R11, R32]: 1, [R12, R32]: 2, [R14, R33]: 1, [R28, R32]: 1, [R3, R32]: 2, [R3, R4, R40]: 1, [R32, R33]: 2, [R32, R34]: 1, [R32, R36]: 2, [R32, R37]: 1, [R33, R34]: 1, [R33, R36]: 2, [R33, R40]: 1, [R36, R39]: 1, [R4, R12, R40]: 1, [R4, R28, R40]: 1, [R4, R34]: 1, [R4, R36]: 2, [R4, R37]: 1, [R4, R8, R40]: 1, [R4, R9, R40]: 1, [R5, R33]: 2, [R5, R34]: 1, [R5, R36]: 2, [R5, R37]: 1, [R6, R33]: 1, [R6, R36]: 1, [R6, R37]: 1, [R7, R32]: 1, [R8, R32]: 2, [R9, R32]: 1 | 7 | 0 | 28 |
