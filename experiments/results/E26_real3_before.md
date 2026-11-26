# Evaluation of the change check (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T10:47:09)

16 specs, 32 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found |  | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 40 | 0/0 | 0/0 | 69 |
| doubtful conflicts set aside | 0/0 |  | 0/0 | 23 | 0/0 | 0/0 | 39 |
| without assumed facts and links | 0/0 |  | 0/0 | 24 | 0/0 | 0/0 | 39 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 35 |
| doubtful findings set aside | 0/0 |  | 0/0 | 34 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 101 where nothing was planted.
- Labels: 32 of 32 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 128 requests, 146,536 tokens read, 86,574 tokens written (32 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| 2025-08-19-add-zod-validation_real | 2 | nothing expected | [R15, R26]: 1, [R2, R15]: 1 | 4 | 0 | 3 |
| 2025-08-19-fix-update-tool-selection_real | 2 | nothing expected | [R5, R8]: 1 | 1 | 0 | 1 |
| 2025-09-29-add-multi-agent-init_real | 2 | nothing expected | [R13, R15]: 2, [R2, R10]: 1, [R6, R15]: 1, [R7, R15]: 2 | 4 | 0 | 1 |
| 2025-09-29-update-agent-file-name_real | 2 | nothing expected | none | 0 | 0 | 2 |
| 2025-10-14-add-github-copilot-prompts_real | 2 | nothing expected | [R8, R16]: 1, [R8, R17]: 1 | 9 | 0 | 3 |
| 2025-10-14-add-windsurf-workflows_real | 2 | nothing expected | [R14, R27]: 1, [R15, R27]: 1, [R25, R27]: 1 | 0 | 0 | 2 |
| 2025-10-14-update-cli-init-root-agents_real | 2 | nothing expected | none | 1 | 0 | 0 |
| 2025-10-22-add-factory-slash-commands_real | 2 | nothing expected | [R14, R41]: 2, [R15, R41]: 2, [R16, R31]: 1, [R16, R41]: 2, [R17, R41]: 2, [R18, R41]: 2, [R19, R41]: 2, [R20, R41]: 2, [R21, R41]: 2 | 0 | 0 | 11 |
| 2026-01-06-add-per-change-schema-metadata_real | 2 | nothing expected | [R16, R18]: 1 | 6 | 0 | 2 |
| 2026-04-23-add-kimi-cli-skills-only-support_real | 2 | nothing expected | [R18, R27]: 1, [R19, R27]: 1, [R25, R27]: 1, [R9, R27]: 2 | 3 | 0 | 2 |
| 2026-08-15-add-dsh-support_real | 2 | nothing expected | none | 2 | 0 | 0 |
| 2026-10-19-add-skill-cli-auto-approval_real | 2 | nothing expected | none | 0 | 0 | 9 |
| 2026-10-19-fix-archive-retirement-guidance_real | 2 | nothing expected | none | 0 | 0 | 12 |
| 2026-10-19-fix-schemas-root-selection_real | 2 | nothing expected | [R9, R29]: 1, [R9, R31]: 1, [R9, R33]: 1 | 0 | 0 | 8 |
| 2026-10-19-rename-bob-to-ibm-bob_real | 2 | nothing expected | none | 2 | 0 | 1 |
| 2026-10-19-warn-on-purpose-placeholder_real | 2 | nothing expected | none | 3 | 0 | 12 |
