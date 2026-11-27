"""speccheck on a real project of an agent system: TestingTheAgents. No planted answers.

The project is a testbed for the tests of an agent system. Its folder
trace-eval/openspec holds 33 spec files (24 about the application, `fs-*`, and
9 about the test harness, `testbed-*`) and four open changes that each add a
workflow. Its authors say in openspec/changes/README.md which of the four can
be built. It is cloned next to this repository and only read:

    git clone https://github.com/unibuc-cs/TestingTheAgents ../TestingTheAgents
    T=../TestingTheAgents/trace-eval/openspec/changes

    # each change against all 33 spec files, in parts (30 to 55 minutes on two GPUs)
    python -m speccheck --change $T/<name> --whole-run --examples "^use: scenario$" \
        --base-url URL --out out/agents_all/<name>
    # the same against the application's specs only, from the saved parts
    python -m speccheck --change $T/<name> --examples "^use: scenario$" --against "fs-*" \
        --formal "out/agents_all/<name>/parts/formal_*.json" --base-url URL --out out/agents/<name>
    # one table for all changes
    python -m experiments.agents.tally $T out/agents

In these specs an example is a scenario whose clause says `use: scenario`.
What was found: research_log.md, T36 to T38.
"""
