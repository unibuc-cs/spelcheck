"""cli.py: runs the three stages on one spec file and writes the results.

    python -m speccheck SPEC.md --base-url http://localhost:18200/v1
    python -m speccheck --change openspec/changes/NAME --base-url http://localhost:18200/v1

Written next to the spec (or into --out):

    formal.json     stage 1: the spec as logic: symbols, assumed facts, rules  (formalize.py)
    findings.json   stage 2: what the solver proved, with its wording          (checks.py)
    report.md       stage 3: the same, in plain language                       (explain.py)

Options that change what is done:

    --change DIR      check an OpenSpec change against the specs that exist
                      (change.py), instead of one spec file. The change is
                      applied to the specs, the result is written as merged.md
                      and goes through the three stages; the report then shows
                      the findings that involve an added or modified
                      requirement, and the gaps that a removed one leaves
                      open. In findings.json every finding says so
                      ("about_change"), and the others are not worded.
                      merged.md and formal.json also hold what the change
                      removes (labels X1, X2, ...); the checks leave it out.

    --symbol-sets K   formalize K times, each time with its own symbols. Every
                      finding then says with how many of the K sets it was
                      found. The extra models are saved as formal_2.json ...
    --formal FILE...  no formalization: reuse saved formal model(s).
    --second-base-url URL
                      a second model, of another family, translates every
                      rule again (formalize step 7); where its reading differs,
                      the rule is reported as ambiguous. Off by default.
    (no --base-url)   no LLM at all: needs --formal; the report holds the
                      proven facts without wording, and no scenarios.
    --review          also let an LLM review the text itself (refine.py).
                      Optional and off by default.
"""

import argparse
import json
import sys
from pathlib import Path

from .change import about_change, after_model, changed_rules, merge, report_lines
from .checks import analyze, combine, find_scenarios
from .explain import explain, judge, render
from .formalize import formalize_sets
from .llm import LLM
from .refine import confirm, refine, refined_text


def main() -> None:
    parser = argparse.ArgumentParser(prog="speccheck", description="Check a requirements spec for conflicts, gaps and ambiguities.")
    parser.add_argument("spec", type=Path, nargs="?", help="the requirements document (Markdown or plain text)")
    parser.add_argument("--change", type=Path, help="an OpenSpec change folder (openspec/changes/NAME) to check against the specs that exist")
    parser.add_argument("--base-url", help="OpenAI-compatible server, e.g. http://localhost:18200/v1")
    parser.add_argument("--model", help="model name (default: the model the server offers)")
    parser.add_argument("--samples", type=int, default=8, help="answers drawn per rule and for the domain facts")
    parser.add_argument("--temperature", type=float, default=0.7, help="variety of those answers")
    parser.add_argument("--symbol-sets", type=int, default=1, help="formalize this many times, each with its own symbols")
    parser.add_argument("--formal", type=Path, nargs="+", help="reuse these formal model files instead of asking the LLM")
    parser.add_argument("--second-base-url", help="a second model's server: it translates every rule again (off by default)")
    parser.add_argument("--out", type=Path, help="output folder (default: the spec's folder)")
    parser.add_argument("--review", action="store_true", help="also let the LLM review the text (off by default)")
    args = parser.parse_args()

    if bool(args.spec) == bool(args.change):
        parser.error("give a spec file, or --change with an OpenSpec change folder")
    if args.change:
        # The specs with the change applied, as one document with labelled scenarios.
        merged = merge(args.change)
        spec_text, title, out = merged.text, args.change.name, args.out or args.change
    else:
        merged = None
        spec_text = args.spec.read_text(encoding="utf-8")
        title = args.spec.parent.name or args.spec.stem
        out = args.out or args.spec.parent
    out.mkdir(parents=True, exist_ok=True)
    if merged:
        (out / "merged.md").write_text(spec_text, encoding="utf-8")
    llm = LLM(args.base_url, args.model) if args.base_url else None
    if args.review and not llm:
        parser.error("--review needs the LLM: give --base-url")

    # Stage 1: text -> logic. Either ask the LLM, or load saved results.
    # `models` is a list: one formal model per symbol set (usually one).
    if args.formal:
        models = [json.loads(path.read_text(encoding="utf-8")) for path in args.formal]
    elif llm:
        second = LLM(args.second_base_url) if args.second_base_url else None
        models = formalize_sets(llm, spec_text, args.symbol_sets, args.samples, args.temperature,
                                second=second)
        for number, model in enumerate(models, start=1):
            _save(out / ("formal.json" if number == 1 else f"formal_{number}.json"), model)
    else:
        parser.error("give --base-url (to formalize with the LLM) or --formal (to reuse a formal.json)")

    # A change: which rules it added or modified, and the formal model without
    # the rules it removes (they stay in formal.json, and apart in `models`).
    if merged:
        changed = [changed_rules(model, merged) for model in models]
        models = [after_model(model, merged) for model in models]

    # Stage 2: logic -> findings. Z3 only. Each model is checked by itself;
    # `combine` merges the results and counts how many models agree.
    findings = combine([analyze(model) for model in models])
    scenarios = combine([find_scenarios(model) for model in models])

    # A change: only the findings that involve one of its rules go on to stage
    # 3. `others` are those among the requirements that existed before.
    others = []
    if merged:
        for finding in findings + scenarios:
            finding["about_change"] = about_change(finding, models, changed)
        others = [finding for finding in findings if not finding["about_change"]]
        findings = [finding for finding in findings if finding["about_change"]]
        scenarios = [scenario for scenario in scenarios if scenario["about_change"]]

    # Stage 3: findings -> plain language. Skipped when there is no LLM. The
    # defects are all worded; of the scenarios only the surprising ones stay.
    if llm:
        findings = explain(llm, findings, models) + judge(llm, scenarios, models, spec_text)

    # Optional review (--review): the LLM reads the text itself. Its notes use
    # the rule ids of the formal model, and each contradiction it names is
    # compared with the conflicts the solver proved.
    if args.review:
        notes = confirm(refine(llm, spec_text, models[0]["rules"]), findings)
        findings += notes
        (out / "refined.md").write_text(refined_text(models[0]["rules"], notes, title), encoding="utf-8")
    _save(out / "findings.json", findings + others)

    note, rules_table = report_lines(merged, changed[0], len(others)) if merged else ([], [])
    report = render(findings, models, title, note) + "".join(f"{line}\n" for line in rules_table)
    (out / "report.md").write_text(report, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy encoding
    print(report)


def _save(path: Path, data) -> None:
    """Write a JSON file that is pleasant to read and to diff."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
