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
    --incremental     with --change: the cheaper way, off by default. The
                      specs that exist are formalized once, and that formal
                      model is kept in openspec/.speccheck/base.json. For
                      the change, only its new scenarios are formalized
                      (written as new.md, not merged.md), with the symbols
                      of that model. A change then costs about a seventh of
                      a full run, and a change that only removes costs
                      nothing before the wording. It finds a little less: on
                      the held-out eval14, 50 of the 54 planted conflicts
                      that the full run found (research_log.md, E20).
                      The saved model is made again, by one full run, when
                      the text of the specs has changed (so also after a
                      change was archived into them) or when another model
                      is used. Delete the file to force that. Not with
                      --symbol-sets, --second-base-url or --review.
    --whole-run       the rules are about a whole run of the system, in which
                      several things happen one after the other (an agent
                      that calls tools: "WHEN a call of ship_parcel succeeds
                      in a run with a plan THEN an earlier request_signoff
                      was approved"), not about one moment. Two rules that
                      react to two different happenings can then clash: the
                      conflict is not marked doubtful, and step 6 asks about
                      the pair like about any other.
    --examples PATTERN
                      with --change: a scenario whose text (its name and the
                      lines below it) matches the pattern is an example, one
                      concrete case and not a rule for all cases. A conflict
                      with examples is marked doubtful, unless every example
                      in it says by itself that the other rules apply in its
                      case. PATTERN is a regular expression, e.g. "^Example:".
    --against PATTERN with --change: check the change only against the spec
                      files whose name matches ("billing-*"), besides the
                      files it touches.

A project whose specs have more than 100 scenarios (change.PART_LIMIT) is too
large for one document. Its change is checked in parts: one document for
each spec file that the change does not touch, with that file and the files
the change touches. The documents and formal models of the parts are written
into parts/ (merged_01.md, formal_01.json, ...), the parts are formalized at
the same time, and one report is written. A finding among the rules of the
change says in how many parts it was found as it is shown, and what is not
doubtful comes first. Not with --symbol-sets, --second-base-url or --review;
scenarios are not looked for. --incremental does not split a project: it
keeps one model of all the specs, which must fit one document.

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
import hashlib
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from .change import (Merged, about_change, after_model, base_document, changed_rules, combine_parts, merge, parts,
                     report_lines, with_examples)
from .checks import analyze, combine, find_scenarios
from .explain import explain, judge, render
from .formalize import formalize, formalize_sets
from .llm import LLM
from .refine import confirm, refine, refined_text


def main() -> None:
    parser = argparse.ArgumentParser(prog="speccheck", description="Check a requirements spec for conflicts, gaps and ambiguities.")
    parser.add_argument("spec", type=Path, nargs="?", help="the requirements document (Markdown or plain text)")
    parser.add_argument("--change", type=Path, help="an OpenSpec change folder (openspec/changes/NAME) to check against the specs that exist")
    parser.add_argument("--incremental", action="store_true",
                        help="with --change: the cheaper way, off by default. The specs that exist are formalized "
                             "once and kept in openspec/.speccheck/base.json; for the change, only its new "
                             "scenarios are formalized. Finds a little less than the full run (README.md)")
    parser.add_argument("--base-url", help="OpenAI-compatible server, e.g. http://localhost:18200/v1")
    parser.add_argument("--model", help="model name (default: the model the server offers)")
    parser.add_argument("--samples", type=int, default=8, help="answers drawn per rule and for the domain facts")
    parser.add_argument("--temperature", type=float, default=0.7, help="variety of those answers")
    parser.add_argument("--symbol-sets", type=int, default=1, help="formalize this many times, each with its own symbols")
    parser.add_argument("--formal", type=Path, nargs="+", help="reuse these formal model files instead of asking the LLM")
    parser.add_argument("--second-base-url", help="a second model's server: it translates every rule again (off by default)")
    parser.add_argument("--out", type=Path, help="output folder (default: the spec's folder)")
    parser.add_argument("--review", action="store_true", help="also let the LLM review the text (off by default)")
    parser.add_argument("--whole-run", action="store_true",
                        help="the rules are about a whole run of the system, in which several things happen "
                             "(an agent that calls tools), not about one moment")
    parser.add_argument("--examples", metavar="PATTERN",
                        help="with --change: a scenario whose text matches this regular expression is one "
                             "concrete case, not a rule; a conflict in a situation that says more than the "
                             "example does is marked doubtful")
    parser.add_argument("--against", metavar="PATTERN",
                        help="with --change: check it only against the spec files whose name matches (billing-*), "
                             "besides the files it touches")
    args = parser.parse_args()

    if bool(args.spec) == bool(args.change):
        parser.error("give a spec file, or --change with an OpenSpec change folder")
    if args.incremental and not args.change:
        parser.error("--incremental goes with --change")
    if args.incremental and (args.symbol_sets > 1 or args.second_base_url or args.review):
        parser.error("--incremental cannot be combined with --symbol-sets, --second-base-url or --review: "
                     "it formalizes only the new scenarios of the change, once")
    if (args.examples or args.against) and not args.change:
        parser.error("--examples and --against go with --change")
    if args.incremental and args.against:
        parser.error("--incremental cannot be combined with --against: it uses the saved model of all the specs")
    pieces = []  # a project too large for one document: the document of each part (change.parts)
    if args.change:
        try:
            re.compile(args.examples or "")
        except re.error as error:
            parser.error(f"--examples: '{args.examples}' is not a regular expression ({error})")
        # The specs with the change applied, as one document with labelled
        # scenarios; with --incremental, only the new scenarios of the change.
        groups = [None] if args.incremental else parts(args.change, args.against)
        merged = merge(args.change, on_base=args.incremental, examples=args.examples,
                       only=None if args.incremental else set().union(*groups))
        if len(groups) > 1:
            if args.symbol_sets > 1 or args.second_base_url or args.review:
                parser.error(f"the specs have {len(merged.scenarios)} scenarios, so the change is checked in "
                             f"{len(groups)} parts: not with --symbol-sets, --second-base-url or --review")
            pieces = [merge(args.change, only=group, examples=args.examples) for group in groups]
        spec_text, title, out = merged.text, args.change.name, args.out or args.change
    else:
        merged = None
        spec_text = args.spec.read_text(encoding="utf-8")
        title = args.spec.parent.name or args.spec.stem
        out = args.out or args.spec.parent
    out.mkdir(parents=True, exist_ok=True)
    if merged:
        (out / ("new.md" if args.incremental else "merged.md")).write_text(spec_text, encoding="utf-8")
    llm = LLM(args.base_url, args.model) if args.base_url else None
    if args.review and not llm:
        parser.error("--review needs the LLM: give --base-url")
    # The rules of the change: step 6 asks about their pairs first.
    first = {label for label, scenario in merged.scenarios.items()
             if scenario["status"] in ("added", "modified")} if merged else None

    # Stage 1: text -> logic. Either ask the LLM, or load saved results.
    # `models` is a list: one formal model per symbol set (usually one), or
    # one for each part of a large project.
    if args.formal:
        models = [json.loads(path.read_text(encoding="utf-8")) for path in args.formal]
        if pieces and len(models) != len(pieces):
            parser.error(f"the change is checked in {len(pieces)} parts: --formal needs their {len(pieces)} "
                         f"formal models, in order (parts/formal_*.json)")
    elif llm and pieces:
        (out / "parts").mkdir(exist_ok=True)
        print(f"speccheck: {len(merged.scenarios)} scenarios, too many for one document; "
              f"checking the change in {len(pieces)} parts", file=sys.stderr)
        jobs = [(args.base_url, llm.model, piece, args.samples, args.temperature, args.whole_run, first)
                for piece in pieces]
        models = []
        with ProcessPoolExecutor(max_workers=min(len(pieces), 32)) as pool:
            for number, model in enumerate(pool.map(_formalize_part, jobs), start=1):
                print(f"speccheck: part {number} of {len(pieces)} "
                      + ("could not be formalized" if "error" in model else "formalized"), file=sys.stderr)
                (out / "parts" / f"merged_{number:02}.md").write_text(pieces[number - 1].text, encoding="utf-8")
                _save(out / "parts" / f"formal_{number:02}.json", model)
                models.append(model)
    elif llm and args.incremental:
        # The saved model of the specs that exist, with the new scenarios of
        # the change added to it. A change that only removes adds nothing.
        base = _base_model(llm, args.change.parent.parent, args.samples, args.temperature, args.whole_run)
        models = [formalize(llm, spec_text, args.samples, args.temperature, base=base,
                            whole_run=args.whole_run, first=first) if spec_text else base]
        _save(out / "formal.json", models[0])
    elif llm:
        second = LLM(args.second_base_url) if args.second_base_url else None
        models = formalize_sets(llm, spec_text, args.symbol_sets, args.samples, args.temperature,
                                second=second, whole_run=args.whole_run, first=first)
        for number, model in enumerate(models, start=1):
            _save(out / ("formal.json" if number == 1 else f"formal_{number}.json"), model)
    else:
        parser.error("give --base-url (to formalize with the LLM) or --formal (to reuse a formal.json)")

    # A large project: the parts that could not be formalized are left out,
    # and the report names them.
    failed = []
    if pieces:
        common = set.intersection(*groups)
        names = [", ".join(sorted(group - common)) for group in groups]
        failed = [f"`{name}` ({model['error']})" for name, model in zip(names, models) if "error" in model]
        pieces = [piece for piece, model in zip(pieces, models) if "error" not in model]
        models = [model for model in models if "error" not in model]
        if not models:
            sys.exit("speccheck: no part could be formalized: " + "; ".join(failed))

    # A change: which rules it added or modified, and the formal model without
    # the rules it removes (they stay in formal.json, and apart in `models`).
    # The rules of the scenarios that are examples (--examples) are marked.
    if merged:
        documents = pieces or [merged] * len(models)
        changed = [changed_rules(model, document) for model, document in zip(models, documents)]
        models = [with_examples(after_model(model, document), document)
                  for model, document in zip(models, documents)]

    # Stage 2: logic -> findings. Z3 only. Each model is checked by itself;
    # `combine` merges the results and counts how many models agree. For a
    # project in parts, combine_parts does that, and no scenarios are looked
    # for: a scenario is a consequence of a whole document.
    if pieces:
        findings, scenarios = combine_parts([analyze(model) for model in models], models, changed), []
    else:
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

    note, rules_table = (report_lines(merged, set().union(*changed) if pieces else changed[0], len(others))
                         if merged else ([], []))
    if pieces:
        note += ["", f"The specs have {len(merged.scenarios)} scenarios with this change, too many for one "
                     f"document. The change was checked in {len(pieces)} parts: the spec files it touches, next "
                     "to one other spec file at a time. A finding among the rules of the change says in how many "
                     "parts it was found. A conflict that needs rules of three spec files is not found this way."]
        if failed:
            note += ["", f"{len(failed)} part(s) could not be formalized, so the change was not checked "
                         f"against: {'; '.join(failed)}."]
    report = render(findings, models, title, note, parts=bool(pieces)) + "".join(f"{line}\n" for line in rules_table)
    (out / "report.md").write_text(report, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy encoding
    print(report)


def _formalize_part(job: tuple) -> dict:
    """Formalize the document of one part of a large project. Runs in a worker process.

    job = (base_url, model name, the part's document (a Merged), samples,
    temperature, whole_run, the rules of the change). Returns the formal
    model, or {"error": the reason} when the part could not be formalized in
    two tries: the LLM failed, it did not keep the scenario labels, or it
    made a rule without a label (the id of such a rule could be the label
    that a scenario of another part has).
    """
    base_url, model_name, piece, samples, temperature, whole_run, first = job
    reason = ""
    for _ in range(2):
        try:
            llm = LLM(base_url, model_name)
            model = formalize(llm, piece.text, samples, temperature, whole_run=whole_run, first=first)
            changed_rules(model, piece)  # raises if a scenario label did not come back
            unlabelled = [rule["id"] for rule in model["rules"] if rule["id"] not in piece.scenarios]
            if unlabelled:
                raise ValueError(f"the read step made rules without a scenario label ({', '.join(unlabelled)})")
            return model
        except Exception as error:  # one part must not stop the others
            reason = str(error)
    return {"error": reason}


def _base_model(llm: LLM, openspec_dir: Path, samples: int, temperature: float, whole_run: bool = False) -> dict:
    """The formal model of the specs that exist (openspec/specs), made once and then kept.

    It is saved in openspec/.speccheck/base.json with what it was made from:
    a fingerprint of the specs (of their labelled text) and the name of the
    model. It is used as long as both are the same, and made again, by one
    full run, when one of them is not: the specs were edited, a change was
    archived into them, or another model is asked. Which of the two happened
    is said on the error stream, since it decides what the run costs. A model
    made for moments is not used for whole runs (--whole-run), nor the other
    way round.
    """
    document = base_document(openspec_dir / "specs")
    fingerprint = hashlib.sha256(document.text.encode("utf-8")).hexdigest()
    saved = openspec_dir / ".speccheck" / "base.json"
    if saved.exists():
        kept = json.loads(saved.read_text(encoding="utf-8"))
        if (kept.get("fingerprint") == fingerprint and kept.get("model") == llm.model
                and (kept["formal"].get("situation") == "run") == whole_run):
            print(f"speccheck: using the saved model of the specs ({saved})", file=sys.stderr)
            return kept["formal"]
    print(f"speccheck: formalizing the specs that exist; their model is saved in {saved}", file=sys.stderr)
    formal = formalize(llm, document.text, samples, temperature, whole_run=whole_run)
    changed_rules(formal, document)  # stops here if a scenario label did not come back
    saved.parent.mkdir(exist_ok=True)
    _save(saved, {"fingerprint": fingerprint, "model": llm.model, "formal": formal})
    return formal


def _save(path: Path, data) -> None:
    """Write a JSON file that is pleasant to read and to diff."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
