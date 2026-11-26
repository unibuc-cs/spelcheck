# Evaluation of the change check (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T14:17:56)

16 specs, 16 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 43 | 0/0 | 0/0 | 53 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 16 | 0/0 | 0/0 | 23 |
| without assumed facts and links | 0/0 |  | 0/0 | 20 | 0/0 | 0/0 | 22 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 18 |
| doubtful findings set aside | 0/0 |  | 0/0 | 17 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 16 where nothing was planted.
- Labels: 16 of 16 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 161 requests, 212,545 tokens read, 105,982 tokens written (16 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-zod-validation_real | 1 | nothing expected | none | 2 | 0 | 2 |
| 2025-08-19-fix-update-tool-selection_real | 1 | nothing expected | [R5, R8]: 1 | 0 | 0 | 0 |
| 2025-09-29-add-multi-agent-init_real | 1 | nothing expected | [R13, R15]: 1 | 2 | 0 | 0 |
| 2025-09-29-update-agent-file-name_real | 1 | nothing expected | none | 1 | 0 | 2 |
| 2025-10-14-add-github-copilot-prompts_real | 1 | nothing expected | none | 4 | 0 | 1 |
| 2025-10-14-add-windsurf-workflows_real | 1 | nothing expected | [R16, R29]: 1 | 0 | 0 | 3 |
| 2025-10-14-update-cli-init-root-agents_real | 1 | nothing expected | [R13, R24]: 1 | 1 | 0 | 5 |
| 2025-10-22-add-factory-slash-commands_real | 1 | nothing expected | none | 0 | 0 | 6 |
| 2026-01-06-add-per-change-schema-metadata_real | 1 | nothing expected | [R16, R18]: 1, [R16, R22]: 1, [R16, R25]: 1, [R22, R23]: 1 | 2 | 0 | 4 |
| 2026-04-23-add-kimi-cli-skills-only-support_real | 1 | nothing expected | none | 2 | 0 | 0 |
| 2026-08-15-add-dsh-support_real | 1 | nothing expected | [R8, R9]: 1 | 1 | 0 | 0 |
| 2026-10-19-add-skill-cli-auto-approval_real | 1 | nothing expected | none | 0 | 0 | 6 |
| 2026-10-19-fix-archive-retirement-guidance_real | 1 | nothing expected | none | 0 | 0 | 4 |
| 2026-10-19-fix-schemas-root-selection_real | 1 | nothing expected | [R13, R38]: 1, [R29, R37]: 1, [R32, R37]: 1, [R33, R37]: 1, [R34, R36]: 1, [R34, R37]: 1, [R36, R39]: 1, [R37, R39]: 1, [R9, R29]: 1, [R9, R32]: 1, [R9, R33]: 1, [R9, R34]: 1 | 0 | 0 | 6 |
| 2026-10-19-rename-bob-to-ibm-bob_real | 1 | nothing expected | none | 1 | 0 | 0 |
| 2026-10-19-warn-on-purpose-placeholder_real | 1 | nothing expected | [R1, R4, R32]: 1, [R1, R4, R36]: 1, [R11, R32]: 1, [R2, R4, R32]: 1, [R2, R4, R36]: 1, [R20, R32]: 1, [R27, R32]: 1, [R27, R33]: 1, [R27, R36]: 1, [R3, R4, R32]: 1, [R3, R4, R36]: 1, [R32, R33]: 1, [R32, R36]: 1, [R32, R39]: 1, [R34, R35]: 1, [R35, R36]: 1, [R35, R39]: 1, [R4, R8, R32]: 1, [R4, R8, R36]: 1, [R5, R33]: 1, [R7, R32]: 1, [R7, R36]: 1 | 2 | 0 | 14 |
