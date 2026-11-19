"""fact_threshold.py: how strict should the vote on domain facts be? No GPU.

A domain fact is kept when more than a share MAJORITY of the sampled
answers imply it (formalize.py). This script redoes that vote with other
shares on the raw answers saved by stability.py, runs the solver checks again,
and counts what each share finds.

    python -m experiments.fact_threshold experiments/results/E2b_facts_samples.json

It needs an experiment file whose runs include the raw answers ("fact_samples"),
which stability.py saves. Runs with a single sample are skipped: there is
nothing to vote on.
"""

import argparse
import json
from pathlib import Path

from speccheck import formalize
from speccheck.checks import analyze
from speccheck.logic import Vocabulary

# The shares tried. With 8 samples "more than 0.5" means at least 5 answers,
# 0.3 means at least 3, 0.2 at least 2, and 0 keeps every fact that was stated.
SHARES = [0.5, 0.3, 0.2, 0.0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("raw", type=Path, help="an experiments/results/<name>.json written by stability.py")
    args = parser.parse_args()
    data = json.loads(args.raw.read_text(encoding="utf-8"))

    lines = [
        f"# Vote threshold for domain facts (from {args.raw.name}, runs with 8 samples)",
        "",
        "A fact is kept when more than the given share of the 8 answers imply it. "
        "\"Expected found\" = runs in which all expected conflicts were found. "
        "\"Other\" = runs with a conflict that was not expected.",
        "",
        "| Spec | Share | Expected found | Other | Facts kept per run (average) |",
        "|---|---|---|---|---|",
    ]
    for name, spec in data["specs"].items():
        expected = {tuple(sorted(conflict)) for conflict in spec["expected"]}
        # Only runs that have something to vote on.
        runs = [r["formal"] for r in data["runs"]
                if r["spec"] == name and "formal" in r and len(r["formal"].get("fact_samples", [])) > 1]
        for share in SHARES:
            formalize.MAJORITY = share  # the vote below reads this setting
            found = other = facts = 0
            for formal in runs:
                # Redo the vote of formalize.py step 4 on the saved answers.
                vocab = Vocabulary(formal["symbols"])
                asked = len(formal["fact_samples"])
                background = formalize._agreed_facts(vocab, formal["fact_samples"], asked)
                # Score by rule position, as stability.py does.
                number = {rule["id"]: index for index, rule in enumerate(formal["rules"], start=1)}
                conflicts = {tuple(sorted(number[r] for r in f["rules"]))
                             for f in analyze({**formal, "background": background})
                             if f["type"] == "conflict"}
                found += expected <= conflicts
                other += bool(conflicts - expected)
                facts += len(background)
            lines.append(f"| {name} | more than {share} | {found}/{len(runs)} | {other} "
                         f"| {facts / len(runs):.1f} |")
    report = "\n".join(lines) + "\n"
    args.raw.with_name(args.raw.stem + "_threshold.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
