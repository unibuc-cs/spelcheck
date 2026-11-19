"""stability.py: how reliable are the findings? A batch experiment.

The LLM is the only random part of the pipeline, so the same spec can give
different findings on different runs. This script formalizes every spec many
times under several settings, and counts how often the conflicts we expect are
found by the solver: from the rules alone, and with the assumed domain facts.

    python -m experiments.stability --base-url http://localhost:18200/v1 --runs 10 --name E4
    python -m experiments.stability --rescore experiments/results/E3_refine.json

The first form asks the LLM and saves, for every run, the formalization (its
formal.json with all raw answers), together with the settings and the prompts,
to experiments/results/<name>.json. Both forms then run the solver checks on the saved
runs and write the summary tables to experiments/results/<name>.md. The second form
needs no GPU: after a change to checks.py the same runs can be scored again.

With --review every run also makes the optional LLM review of the text
(speccheck/refine.py), and the tables get the columns that compare it with
the solver. Without it those columns read "n/a".

Many runs are in flight at once. With `--data-parallel-size 2` the server
spreads them over two GPUs, so this is where the second GPU pays off. Each run
is its own process, because the Z3 solver must not be shared between threads.

"Expected" conflicts are read from an `expected.json` next to each spec, as
groups of rule numbers (position in the document). They are used only here,
for scoring; the pipeline never sees them.
"""

import argparse
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

from speccheck import formalize as formalize_module
from speccheck import refine as refine_module
from speccheck.checks import analyze
from speccheck.formalize import formalize
from speccheck.llm import LLM
from speccheck.refine import refine

# The settings compared: (label, samples per rule, temperature, read temperature).
SETTINGS = [
    ("1 greedy translation",          1, 0.0, 0.0),  # no sampling: ambiguity cannot be seen
    ("8 samples, T=0.7 (default)",    8, 0.7, 0.0),
    ("8 samples, T=1.0",              8, 1.0, 0.0),
    ("8 samples, symbols also vary",  8, 0.7, 0.7),  # a different symbol list on each run
]

# Files that speccheck itself writes next to a spec; never the spec.
OUTPUT_FILES = ("report.md", "refined.md")


def one_run(job: tuple) -> dict:
    """Run the LLM steps on one spec once.

    job = (base_url, review, spec_text, samples, temperature, read_temperature).
    Returns {"formal": ...} (plus "review" when asked for) or {"error": ...}.
    Runs in a worker process, so it opens its own connection to the server.
    """
    base_url, review, spec_text, samples, temperature, read_temperature = job
    try:
        llm = LLM(base_url)
        # keep_samples: the raw LLM answers are saved too, so the clustering and
        # the vote on facts can be studied later without asking the LLM again.
        result = {"formal": formalize(llm, spec_text, samples, temperature, read_temperature,
                                      keep_samples=True)}
        if review:
            # The review does not depend on the settings: it is one call at
            # temperature 0. Repeating it shows how much it varies on its own.
            result["review"] = refine(llm, spec_text, result["formal"]["rules"])
        return result
    except Exception as error:  # a failed run is a result too, not a reason to stop the batch
        return {"error": str(error)}


def collect(base_url: str, runs: int, review: bool) -> dict:
    """Ask the LLM: run every spec `runs` times per setting.

    Returns everything needed to score the experiment later without a GPU.
    """
    llm = LLM(base_url)
    # Every folder under specs/ that has an expected.json takes part.
    specs = {}
    for expected_file in sorted(Path("specs").glob("*/expected.json")):
        folder = expected_file.parent
        spec_file = next(p for p in sorted(folder.glob("*.md")) if p.name not in OUTPUT_FILES)
        specs[folder.name] = {
            "text": spec_file.read_text(encoding="utf-8"),
            "expected": json.loads(expected_file.read_text())["conflicts"],
        }

    # One job per (spec, setting, repetition); results come back in the same order.
    jobs = [(name, setting) for name in specs for setting in SETTINGS for _ in range(runs)]
    with ProcessPoolExecutor(max_workers=32) as pool:
        results = list(pool.map(
            one_run, [(base_url, review, specs[name]["text"], *setting[1:]) for name, setting in jobs]))

    return {
        "model": llm.model,
        "date": datetime.now().isoformat(timespec="seconds"),
        "runs_per_row": runs,
        # The exact prompts, so the experiment can be understood after they change.
        "prompts": {"read": formalize_module.READ_SYSTEM,
                    "formalize": formalize_module.FORMALIZE_SYSTEM,
                    "facts": formalize_module.FACTS_SYSTEM,
                    "refine": refine_module.REFINE_SYSTEM},
        "specs": specs,
        "runs": [{"spec": name, "setting": setting[0], **result}
                 for (name, setting), result in zip(jobs, results)],
    }


def score(run: dict) -> dict:
    """Run the solver checks on one saved run and reduce it to what we count.

    Every conflict becomes a sorted tuple of rule numbers, e.g. (2, 3). Rules
    are numbered by their position in the document (1 = first rule), not by
    id: for a spec without labels the model invents the ids, and they can
    change from run to run.
    """
    formal = run["formal"]
    number = {rule["id"]: index for index, rule in enumerate(formal["rules"], start=1)}

    def groups(findings: list[dict], wanted) -> set:
        return {tuple(sorted(number[r] for r in f["rules"])) for f in findings if wanted(f)}

    def is_conflict(finding: dict) -> bool:
        return finding["type"] == "conflict"

    findings = analyze(formal)
    return {
        "alone": groups(analyze({**formal, "background": []}), is_conflict),  # facts switched off
        "with_facts": groups(findings, is_conflict),
        # Contradictions named by the review (absent in files older than the review).
        "review": groups(run.get("review", []), lambda note: note["kind"] == "contradiction"),
        "notes": len(run.get("review", [])),
        "facts": len(formal.get("background", [])),
        "gaps": sum(f["type"] == "gap" for f in findings),
        "ambiguous": [number[f["rule"]] for f in findings if f["type"] == "ambiguity"],
    }


def tables(data: dict) -> str:
    """Score all saved runs and build the Markdown summary (two tables)."""
    def counted(values, unit: str) -> str:
        """Render a distribution, e.g. "1 gap(s): 9, 2 gap(s): 1"."""
        return ", ".join(f"{value} {unit}: {count}" for value, count in sorted(Counter(values).items()))

    has_review = any("review" in run for run in data["runs"])
    conflicts = [
        "| Spec | Setting | Solver, rules alone | Solver, with facts | Review | Solver or review "
        "| Unexpected: solver | Unexpected: review |",
        "|---|---|---|---|---|---|---|---|",
    ]
    details = [
        "| Spec | Setting | Facts kept per run | Gaps per run | Rule flagged ambiguous: in how many runs "
        "| Review notes per run |",
        "|---|---|---|---|---|---|",
    ]
    for name, spec in data["specs"].items():
        expected = {tuple(sorted(conflict)) for conflict in spec["expected"]}
        for setting in SETTINGS:
            runs = [r for r in data["runs"] if r["spec"] == name and r["setting"] == setting[0]]
            ok = [score(r) for r in runs if "formal" in r]
            total = f"/{len(runs)}"
            # The facts may only add conflicts. Stop loudly if that is ever broken.
            assert all(r["alone"] <= r["with_facts"] for r in ok)

            def review_cell(text: str) -> str:
                return text if has_review else "n/a"

            conflicts.append(
                f"| {name} | {setting[0]} "
                f"| {sum(expected <= r['alone'] for r in ok)}{total} "
                f"| {sum(expected <= r['with_facts'] for r in ok)}{total} "
                f"| {review_cell(str(sum(expected <= r['review'] for r in ok)) + total)} "
                f"| {review_cell(str(sum(expected <= r['with_facts'] | r['review'] for r in ok)) + total)} "
                f"| {sum(bool(r['with_facts'] - expected) for r in ok)} "
                f"| {review_cell(str(sum(bool(r['review'] - expected) for r in ok)))} |"
            )
            details.append(
                f"| {name} | {setting[0]} "
                f"| {counted((r['facts'] for r in ok), 'fact(s)')} "
                f"| {counted((r['gaps'] for r in ok), 'gap(s)')} | "
                + (", ".join(f"rule {rule}: {count}" for rule, count in
                             sorted(Counter(rule for r in ok for rule in r["ambiguous"]).items()))
                   or "none")
                + f" | {review_cell(counted((r['notes'] for r in ok), 'note(s)'))}"
                + (f" ({len(runs) - len(ok)} failed)" if len(ok) < len(runs) else "") + " |"
            )
    return "\n".join([
        f"# Stability experiment ({data['runs_per_row']} runs per row, model {data['model']}, {data['date']})",
        "",
        "## Runs in which all expected conflicts were found",
        "",
        "\"Unexpected\" = runs with at least one conflict (solver, with facts) or one "
        "contradiction (review) that was not expected.",
        "",
        *conflicts,
        "",
        "## Other counts",
        "",
        *details,
    ]) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", help="ask the LLM at this OpenAI-compatible server")
    parser.add_argument("--runs", type=int, default=10, help="repetitions per spec and setting")
    parser.add_argument("--name", default="experiment", help="output name: experiments/results/<name>.json and .md")
    parser.add_argument("--rescore", type=Path, help="score the runs saved in this .json again (no LLM)")
    parser.add_argument("--review", action="store_true", help="also run the optional LLM review in every run")
    args = parser.parse_args()

    if args.rescore:
        raw_file = args.rescore
        data = json.loads(raw_file.read_text(encoding="utf-8"))
    elif args.base_url:
        raw_file = Path("experiments/results") / f"{args.name}.json"
        data = collect(args.base_url, args.runs, args.review)
        raw_file.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        parser.error("give --base-url (to run the experiment) or --rescore (to score saved runs)")

    report = tables(data)
    raw_file.with_suffix(".md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
