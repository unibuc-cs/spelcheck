"""Trying the change check on a real OpenSpec project, from its git history. No planted answers.

The project is cloned outside the repository's tracked files and only read:

    git clone --no-checkout https://github.com/Fission-AI/OpenSpec.git .scratch/real/OpenSpec
    python experiments/real/history.py .scratch/real/OpenSpec .scratch/real_cases     the changes, each next to the specs before it
    python experiments/real/merge_check.py .scratch/real_cases                        our merge against the project's own result
    python experiments/real/batch.py .scratch/real_cases .scratch/real_batch 3 0      every third change of the pool, as a set
    python -m experiments.evaluate --base-url ... --specs .scratch/real_batch --runs 1 --symbol-sets 1 --name E23_real_batch1
    python experiments/real/tally.py experiments/results/E23_real_batch1.json         what the conflicts rest on, the gaps
    python experiments/real/translations.py experiments/results/E23_real_batch1.json  why the translations of a rule disagree

A real project is too large to formalize as one document (44 spec files here),
so each change is checked against the spec files it touches, as they were in
the commit before the change was archived. research_log.md, E23.
"""
