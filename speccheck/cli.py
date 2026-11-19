"""cli.py: runs the three stages on one spec file and writes the results.

    python -m speccheck SPEC.md --base-url http://localhost:18200/v1

Written next to the spec (or into --out):

    formal.json     stage 1: the spec as logic: symbols, assumed facts, rules  (formalize.py)
    findings.json   stage 2: what the solver proved, with its wording          (checks.py)
    report.md       stage 3: the same, in plain language                       (explain.py)

Options that change what is done:

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

from .checks import analyze, combine, find_scenarios
from .explain import explain, judge, render
from .formalize import formalize_sets
from .llm import LLM
from .refine import confirm, refine, refined_text


def main() -> None:
    parser = argparse.ArgumentParser(prog="speccheck", description="Check a requirements spec for conflicts, gaps and ambiguities.")
    parser.add_argument("spec", type=Path, help="the requirements document (Markdown or plain text)")
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

    spec_text = args.spec.read_text(encoding="utf-8")
    title = args.spec.parent.name or args.spec.stem
    out = args.out or args.spec.parent
    out.mkdir(parents=True, exist_ok=True)
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

    # Stage 2: logic -> findings. Z3 only. Each model is checked by itself;
    # `combine` merges the results and counts how many models agree.
    findings = combine([analyze(model) for model in models])
    scenarios = combine([find_scenarios(model) for model in models])

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
    _save(out / "findings.json", findings)

    report = render(findings, models, title)
    (out / "report.md").write_text(report, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy encoding
    print(report)


def _save(path: Path, data) -> None:
    """Write a JSON file that is pleasant to read and to diff."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
