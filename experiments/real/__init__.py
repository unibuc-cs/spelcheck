"""Trying the change check on a real OpenSpec project, from its git history. No planted answers.

The project is cloned outside the repository's tracked files and only read:

    git clone --no-checkout https://github.com/Fission-AI/OpenSpec.git .scratch/real/OpenSpec
    python experiments/real/history.py .scratch/real/OpenSpec .scratch/real_cases     the changes, each next to the specs before it
    python -m experiments.real.merge_check .scratch/real_cases                        our merge against the project's own result
    python experiments/real/batch.py .scratch/real_cases .scratch/real_batch 3 0      every third change of the pool, as a set
    python -m experiments.evaluate --base-url ... --specs .scratch/real_batch --runs 1 --symbol-sets 1 --name E23_real_batch1
    python -m experiments.real.tally experiments/results/E23_real_batch1.json         what the conflicts rest on, the gaps
    python -m experiments.real.translations experiments/results/E23_real_batch1.json  why the translations of a rule disagree

A real project is too large to formalize as one document (44 spec files here),
so each change is checked against the spec files it touches, as they were in
the commit before the change was archived. research_log.md, E23, T27 and E24.

The three batches that were run are kept in experiments/sets/real1 to real3,
with the licence of the project they come from; they can be run from there:

    python -m experiments.evaluate --base-url ... --specs experiments/sets/real2 --runs 1 --symbol-sets 1 --name ...

real4 and real5 are written by planted.py: changes that create a new spec,
each also with one scenario of ours that clashes with one of its own.

    python experiments/real/planted.py .scratch/real_cases experiments/sets/real4 real4
    python experiments/real/planted.py .scratch/real_cases experiments/sets/real5 real5
"""
