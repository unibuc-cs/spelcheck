"""evaluate.py: how good is the formal check on specs with known defects?

    python -m experiments.evaluate --base-url http://localhost:18200/v1 --specs experiments/sets/eval2 --name E7_eval2
    python -m experiments.evaluate --rescore experiments/results/E7_eval2.json
    python -m experiments.evaluate --rescore experiments/results/E7_eval2.json --second-base-url http://localhost:18201/v1

The first form asks the LLM. Every spec folder under --specs is formalized
`--runs` times; each run makes `--symbol-sets` formal models of the spec (the
first with the usual symbols, the others with varied ones). `--temperature`
is the variety of the 8 answers per rule, fact list, link and question
(default 0.7); the read step of the first symbol set stays at 0. Everything is
saved to experiments/results/<name>.json: the formal models with all raw answers, the
expected findings and the prompts.

The third form adds formalize step 7 to saved runs: a second model translates
every rule of every saved formal model again, and the file is saved with its
answers. (The two models then never need the GPUs at the same time.)

All forms then score the saved runs with the solver and write
experiments/results/<name>.md. No GPU is needed for that, so the same runs can be
scored again after a change to checks.py, or under other settings.

What is counted, from the expected.json next to each spec (see make_eval.py):

    planted conflicts found    over all (expected conflict, run) pairs
    unexpected conflicts       reported conflicts that were neither expected
                               nor "allowed"; on a clean spec: false alarms
    planted ambiguities found  over all (expected ambiguous rule, run) pairs
    ambiguity flags on clean   rules flagged as ambiguous in the clean specs
    the other reading          for each flagged rule: does its other reading
                               change a conflict or a gap? (reading_effects)
    planted gaps found         over all (expected gap, run) pairs; and the gaps
                               reported on clean specs (gap_scores)

The score is given for several ways of running the check ("configurations"),
each switching one part on or off. All are computed from the same LLM runs.
"""

import argparse
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

from speccheck import formalize as formalize_module
from speccheck import probe as probe_module
from speccheck.checks import analyze, combine, find_gaps, settled
from speccheck.formalize import formalize_sets, judge_second, second_reading
from speccheck.llm import LLM
from speccheck.logic import Vocabulary

# How the check is run by default. Each configuration below changes some of it:
#   sets         symbol sets used (the first n formal models of a run)
#   rule         "any": a finding counts if found with at least one symbol set;
#                "majority": only if found with more than half of them
#   facts        use the assumed facts and links
#   max_group    rules triggered together at most, when hunting conflicts
#   questions    report the ambiguities found by questions (formalize step 6)
#   link_checks  leave out the links and facts that step 6 rejected
#   settle       share of the answers a translation needs to stand (step 6)
#   doubtful     count the conflicts marked doubtful (False: set them aside)
#   second       use the second reader (step 7); only if the runs have one
#   repair       keep the facts that the vote kept thanks to the parentheses
#                repair (False: see without_repair)
DEFAULT = {"sets": 1, "rule": "any", "facts": True, "max_group": 3,
           "questions": True, "link_checks": True, "doubtful": True, "settle": 0.5,
           "second": False, "repair": True}

CONFIGURATIONS = [
    ("default (1 symbol set)",               {}),
    ("doubtful conflicts set aside",         {"doubtful": False}),
    ("without step 6 (no questions, nothing checked)", {"questions": False, "link_checks": False}),
    ("without step 6, doubtful set aside",   {"questions": False, "link_checks": False, "doubtful": False}),
    ("without checks of links and facts",    {"link_checks": False}),
    ("translation needs 7 of 8 answers",     {"settle": 0.75}),
    ("second reader",                        {"second": True}),
    ("second reader, without step 6",        {"second": True, "questions": False, "link_checks": False}),
    ("second reader, 7 of 8 answers",        {"second": True, "settle": 0.75}),
    ("without assumed facts and links",      {"facts": False}),
    ("facts vote without the parentheses repair", {"repair": False}),
    ("pairs of rules only",                  {"max_group": 2}),
    ("3 symbol sets, found with any",        {"sets": 3}),
    ("3 symbol sets, found with most",       {"sets": 3, "rule": "majority"}),
    ("5 symbol sets, found with any",        {"sets": 5}),
    ("5 symbol sets, found with most",       {"sets": 5, "rule": "majority"}),
]

# Files that speccheck itself writes next to a spec; never the spec.
OUTPUT_FILES = ("report.md", "refined.md")

# Answers the second model gives per rule in step 7.
SECOND_SAMPLES = 8

# Answers per rule and per fact list in the runs (formalize's default).
SAMPLES = 8


def one_run(job: tuple) -> dict:
    """Formalize one spec once, with several symbol sets.

    job = (base_url, spec_text, symbol_sets, temperature).
    Returns {"models": [...]} or {"error": ...}. Runs in a worker process.
    """
    base_url, spec_text, symbol_sets, temperature = job
    try:
        # keep_samples: the raw LLM answers are saved too, for later study.
        return {"models": formalize_sets(LLM(base_url), spec_text, symbol_sets,
                                         temperature=temperature, keep_samples=True)}
    except Exception as error:  # a failed run is a result too, not a reason to stop the batch
        return {"error": str(error)}


def collect(base_url: str, specs_root: Path, runs: int, symbol_sets: int, temperature: float) -> dict:
    """Ask the LLM: formalize every spec under `specs_root`, `runs` times."""
    llm = LLM(base_url)
    specs = {}
    for expected_file in sorted(specs_root.glob("*/expected.json")):
        folder = expected_file.parent
        spec_file = next(p for p in sorted(folder.glob("*.md")) if p.name not in OUTPUT_FILES)
        specs[folder.name] = {"text": spec_file.read_text(encoding="utf-8"),
                              **json.loads(expected_file.read_text())}

    jobs = [name for name in specs for _ in range(runs)]
    with ProcessPoolExecutor(max_workers=32) as pool:
        results = list(pool.map(one_run, [(base_url, specs[name]["text"], symbol_sets, temperature)
                                          for name in jobs]))
    return {
        "model": llm.model,
        "date": datetime.now().isoformat(timespec="seconds"),
        "runs_per_spec": runs,
        "symbol_sets": symbol_sets,
        "temperature": temperature,
        # The exact prompts, so the experiment can be understood after they change.
        "prompts": {"read": formalize_module.READ_SYSTEM,
                    "formalize": formalize_module.FORMALIZE_SYSTEM,
                    "facts": formalize_module.FACTS_SYSTEM,
                    "readings": probe_module.READINGS_SYSTEM,
                    "question": probe_module.QUESTION_SYSTEM,
                    "link": probe_module.LINK_SYSTEM,
                    "fact": probe_module.FACT_SYSTEM},
        "specs": specs,
        "runs": [{"spec": name, **result} for name, result in zip(jobs, results)],
    }


def rejudge_second(data: dict) -> None:
    """Redo the Z3 part of step 7 on the saved answers of the second model.

    Like the checks, the judgement is redone each time saved runs are scored,
    so a change to formalize.judge_second needs no GPU.
    """
    for run in data["runs"]:
        for model in run.get("models", []):
            vocab = Vocabulary(model["symbols"])
            for rule in model["rules"]:
                answers = rule.get("second", {}).get("samples")
                if answers is not None:
                    rule["second"] = {**judge_second(vocab, rule, answers, SECOND_SAMPLES),
                                      "samples": answers}


def second_one(job: tuple) -> dict:
    """Formalize step 7 on one saved formal model. Runs in a worker process.

    job = (base_url, formal model). Returns the model with "second" in its rules,
    or {"error": ...}.
    """
    base_url, model = job
    try:
        second_reading(LLM(base_url), model, samples=SECOND_SAMPLES, keep_samples=True)
        return model
    except Exception as error:  # one failed model is a result, not a reason to stop
        return {"error": str(error)}


def add_second_readings(data: dict, base_url: str) -> None:
    """Formalize step 7 on every saved formal model, with the model at `base_url`."""
    models = [model for run in data["runs"] for model in run.get("models", [])]
    with ProcessPoolExecutor(max_workers=32) as pool:
        done = list(pool.map(second_one, [(base_url, model) for model in models]))
    failed = 0
    for model, result in zip(models, done):
        if "error" in result:
            failed += 1
        else:
            model.update(result)
    data["second_model"] = LLM(base_url).model
    data["second_failed"] = failed


def without_repair(model: dict) -> dict:
    """The model as if the facts vote had not repaired any formula (T19).

    A voted fact stays only if the vote without the repair, on the same saved
    answers, kept it or something that implies it; the links all stay. Step 6
    ran with all the facts, so this is close to a run without the repair, not
    exactly one. On runs made before the repair nothing changes.
    """
    if "fact_samples" not in model:
        return model
    vocab = Vocabulary(model["symbols"])
    old = [vocab.parse(fact["formula"]) for fact in
           formalize_module._agreed_facts(vocab, model["fact_samples"], SAMPLES, repair=False)]
    background = [fact for fact in model["background"]
                  if "restates" in fact or vocab.implies(old, vocab.parse(fact["formula"]))]
    return {**model, "background": background}


def reported(run: dict, config: dict) -> tuple[set, set]:
    """What one run reports under one configuration.

    Returns (conflicts, ambiguous rules). A conflict is a sorted tuple of rule
    numbers (position in the document), an ambiguous rule is its number.
    """
    models = run["models"][:config["sets"]]
    if not config["facts"]:
        models = [{**model, "background": []} for model in models]
    if not config["repair"]:
        models = [without_repair(model) for model in models]
    # readings=False: only the counts are needed here (see reading_effects).
    findings = combine([analyze(model, config["max_group"], questions=config["questions"],
                                link_checks=config["link_checks"], settle=config["settle"],
                                second=config["second"], readings=False)
                        for model in models])
    number = {r["id"]: index for index, r in enumerate(models[0]["rules"], start=1)}

    def counts(finding: dict) -> bool:
        """Does this finding pass the configuration's rule ("any" / "majority")?"""
        found = int(finding["support"].split("/")[0]) if "support" in finding else 1
        return found * 2 > len(models) if config["rule"] == "majority" else True

    def doubtful(finding: dict) -> bool:
        return "doubted_by" in finding or "simultaneous_events" in finding

    conflicts = {tuple(sorted(number[r] for r in f["rules"])) for f in findings
                 if f["type"] == "conflict" and counts(f)
                 and (config["doubtful"] or not doubtful(f))}
    ambiguous = {number[f["rule"]] for f in findings if f["type"] == "ambiguity" and counts(f)}
    return conflicts, ambiguous


def reading_effects(data: dict) -> list[str]:
    """A table: how often does the other reading of a flagged rule change another finding?

    For the default configuration and the first symbol set of every run. An
    ambiguous rule is checked with its first reading; checks._try_other_readings
    tries the other one and says what changes. Each flag is counted once, under
    the strongest change: a conflict (one appears or is gone), else a gap (a
    rule then applies in it), else nothing.
    """
    counts = Counter()  # (planted or not, what changes) -> flags
    for run in data["runs"]:
        if "models" not in run:
            continue
        model = run["models"][0]
        number = {rule["id"]: index for index, rule in enumerate(model["rules"], start=1)}
        planted = set(data["specs"][run["spec"]].get("ambiguous", []))
        for finding in analyze(model, second=DEFAULT["second"]):
            effect = finding.get("other_reading")
            if effect is not None:
                what = ("conflict" if effect["removes"] or effect["adds"]
                        else "gap" if effect["covers_gaps"] else "nothing")
                counts["planted" if number[finding["rule"]] in planted else "other", what] += 1
    lines = ["| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |",
             "|---|---|---|---|---|"]
    for who in ("planted", "other"):
        changes = [counts[who, what] for what in ("conflict", "gap", "nothing")]
        lines.append(f"| {who} | {sum(changes)} | " + " | ".join(map(str, changes)) + " |")
    return lines


def gap_scores(data: dict) -> list[str]:
    """A table: are the planted gaps found, and what else is reported as a gap?

    For the default configuration and the first symbol set of every run. The
    gaps are searched over all situations, as before step 26, and once for
    each event (checks.find_gaps), so that the two can be compared on the
    same runs; the last row leaves out the gaps that the assumed facts mark
    as doubtful.

    A planted gap names a requirement by its number: its other case was
    removed from the spec (make_eval.py, "gap" versions). It counts as found
    when a reported gap is a situation in which the event of that requirement
    happens: the event the read step named as its trigger, or an event in its
    condition. The same test on the "covered" requirements of a clean spec
    gives the false alarms: there both cases are covered.
    """
    def events_of(model: dict, vocab: Vocabulary, number: int) -> set:
        """The events requirement `number` (position in the document) reacts to."""
        if number > len(model["rules"]):
            return set()
        rule = model["rules"][number - 1]
        events = {rule.get("trigger")} & vocab.events
        try:
            events |= vocab.symbols_in(vocab.parse(rule.get("antecedent", "true"))) & vocab.events
        except ValueError:
            pass
        return events

    lines = ["| Gap search | Planted gaps found | Clean runs with a gap on a covered event "
             "| Gaps on clean specs, with an event | Gaps on clean specs, all |",
             "|---|---|---|---|---|"]
    # by_event: the search of step 26; aside: leave out the gaps that the
    # assumed facts mark as doubtful (the facts that step 6 rejected not used).
    for label, by_event, aside in (("over all situations (as before step 26)", False, False),
                                   ("once for each event", True, False),
                                   ("once for each event, doubtful set aside", True, True)):
        found = planted = alarms = covered_runs = with_event = on_clean = 0
        for run in data["runs"]:
            if "models" not in run:
                continue
            spec, model = data["specs"][run["spec"]], run["models"][0]
            vocab = Vocabulary(model["symbols"])
            decided = [settled(rule, DEFAULT["settle"], DEFAULT["questions"], DEFAULT["second"])
                       for rule in model["rules"]]
            facts = {fact["id"]: vocab.parse(fact["formula"]) for fact in model.get("background", [])
                     if fact.get("check", {}).get("verdict") != "rejected"}
            gaps = find_gaps(vocab, [vocab.rule(rule) for rule in decided
                                     if rule.get("status") != "rejected"], by_event, doubt=facts)
            if aside:
                gaps = [gap for gap in gaps if "doubted_by" not in gap]

            def happens_in_a_gap(number: int) -> bool:
                return any(gap["when"].get(event) is True
                           for gap in gaps for event in events_of(model, vocab, number))

            planted += len(spec.get("gaps", []))
            found += sum(happens_in_a_gap(number) for number in spec.get("gaps", []))
            if run["spec"].endswith("_clean"):
                on_clean += len(gaps)
                with_event += sum(any(gap["when"].get(event) is True for event in vocab.events)
                                  for gap in gaps)
                if "covered" in spec:
                    covered_runs += 1
                    alarms += any(happens_in_a_gap(number) for number in spec["covered"])
        lines.append(f"| {label} | {found}/{planted} | {alarms}/{covered_runs} | {with_event} | {on_clean} |")
    return lines


def tables(data: dict) -> str:
    """Score all saved runs under every configuration; build the Markdown summary."""
    def groups(spec: dict, key: str) -> set:
        return {tuple(sorted(group)) for group in spec.get(key, [])}

    def kind(name: str) -> str:
        """The version of a spec, from its folder name: clean, direct, overlap, ambiguity."""
        return name.rsplit("_", 1)[-1].rstrip("0123456789")

    ok_runs = [run for run in data["runs"] if "models" in run]
    summary = [
        "| Configuration | Planted conflicts found | direct | overlap "
        "| Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found "
        "| Ambiguity flags on clean specs | Other ambiguity flags |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for label, change in CONFIGURATIONS:
        config = {**DEFAULT, **change}
        if config["sets"] > data.get("symbol_sets", 1):
            continue  # the experiment did not make that many symbol sets
        if config["second"] and "second_model" not in data:
            continue  # no second reader was run on these runs
        found, total = Counter(), Counter()   # planted conflicts, by kind of spec
        false_alarm_runs = clean_runs = unexpected = 0
        ambiguity_found = ambiguity_total = clean_flags = other_flags = 0
        for run in ok_runs:
            spec = data["specs"][run["spec"]]
            expected, allowed = groups(spec, "conflicts"), groups(spec, "allowed")
            conflicts, ambiguous = reported(run, config)
            found[kind(run["spec"])] += len(expected & conflicts)
            total[kind(run["spec"])] += len(expected)
            extra = conflicts - expected - allowed
            unexpected += len(extra)
            wanted = set(spec.get("ambiguous", []))
            ambiguity_found += len(wanted & ambiguous)
            ambiguity_total += len(wanted)
            other_flags += len(ambiguous - wanted)
            if kind(run["spec"]) == "clean":
                clean_runs += 1
                false_alarm_runs += bool(extra)
                clean_flags += len(ambiguous)
        summary.append(
            f"| {label} | {sum(found.values())}/{sum(total.values())} "
            f"| {found['direct']}/{total['direct']} | {found['overlap']}/{total['overlap']} "
            f"| {false_alarm_runs}/{clean_runs} | {unexpected} "
            f"| {ambiguity_found}/{ambiguity_total} | {clean_flags} | {other_flags} |")

    # Per spec, for the default configuration: what was expected, what came out.
    details = ["| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) "
               "| Ambiguity flags (rule: runs) |",
               "|---|---|---|---|---|"]
    label, change = CONFIGURATIONS[0]
    config = {**DEFAULT, **change}
    for name, spec in data["specs"].items():
        runs = [run for run in ok_runs if run["spec"] == name]
        expected, allowed = groups(spec, "conflicts"), groups(spec, "allowed")
        hits, extras, flags = Counter(), Counter(), Counter()
        for run in runs:
            conflicts, ambiguous = reported(run, config)
            hits.update(expected & conflicts)
            extras.update(conflicts - expected - allowed)
            flags.update(ambiguous)
        wanted = set(spec.get("ambiguous", []))
        details.append(
            f"| {name} | {len(runs)} | "
            + (", ".join(f"{list(c)}: {hits[c]}/{len(runs)}" for c in sorted(expected)) or "none expected")
            + " | " + (", ".join(f"{list(c)}: {n}" for c, n in sorted(extras.items())) or "none")
            + " | " + (", ".join(f"{r}{' (planted)' if r in wanted else ''}: {n}"
                                 for r, n in sorted(flags.items())) or "none") + " |")

    # Planted ambiguities found by kind (boundary, and/or, only, if), for the
    # configurations that change how ambiguity is decided. Needs the "kind"
    # that make_eval.py writes into expected.json (eval3 on).
    kinds = sorted({spec["kind"] for spec in data["specs"].values() if "kind" in spec})
    by_kind = ["| Configuration | " + " | ".join(kinds) + " |", "|---|" + "---|" * len(kinds)]
    for label_k, change in CONFIGURATIONS:
        config = {**DEFAULT, **change}
        if change and (not {"questions", "settle", "second"} & change.keys() or "doubtful" in change):
            continue  # the same ambiguity findings as another row
        if config["sets"] > data.get("symbol_sets", 1) or (config["second"] and "second_model" not in data):
            continue
        found, total = Counter(), Counter()
        for run in ok_runs:
            spec = data["specs"][run["spec"]]
            if "kind" in spec:
                _, ambiguous = reported(run, config)
                found[spec["kind"]] += len(set(spec["ambiguous"]) & ambiguous)
                total[spec["kind"]] += len(spec["ambiguous"])
        by_kind.append(f"| {label_k} | " + " | ".join(f"{found[k]}/{total[k]}" for k in kinds) + " |")

    failed = len(data["runs"]) - len(ok_runs)
    return "\n".join([
        # Files written before the option existed were all made at 0.7.
        f"# Evaluation ({data['runs_per_spec']} runs per spec, {data['symbol_sets']} symbol sets per run, "
        f"temperature {data.get('temperature', 0.7)}, model {data['model']}, {data['date']})",
        "",
        f"{len(data['specs'])} specs, {len(ok_runs)} runs scored" + (f", {failed} failed" if failed else "")
        + (f"; second reader: {data['second_model']}" if "second_model" in data else "") + ".",
        "",
        "## By configuration",
        "",
        *summary,
        "",
        *(["## Planted ambiguities found, by kind", "", *by_kind, ""] if kinds else []),
        f"## Ambiguity flags and the other reading ({label})",
        "",
        *reading_effects(data),
        "",
        f"## Gaps ({label})",
        "",
        *gap_scores(data),
        "",
        f"## By spec ({label})",
        "",
        *details,
    ]) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", help="ask the LLM at this OpenAI-compatible server")
    parser.add_argument("--specs", type=Path, default=Path("experiments/sets/eval7"), help="folder with one sub-folder per spec")
    parser.add_argument("--runs", type=int, default=3, help="repetitions per spec")
    parser.add_argument("--symbol-sets", type=int, default=3, help="formal models made per run")
    parser.add_argument("--temperature", type=float, default=0.7,
                        help="variety of the 8 answers per rule, fact list, link and question")
    parser.add_argument("--name", default="evaluation", help="output name: experiments/results/<name>.json and .md")
    parser.add_argument("--rescore", type=Path, help="score the runs saved in this .json again (no LLM)")
    parser.add_argument("--second-base-url", help="with --rescore: add step 7 with the second model at this server")
    args = parser.parse_args()

    if args.rescore:
        raw_file = args.rescore
        data = json.loads(raw_file.read_text(encoding="utf-8"))
        rejudge_second(data)
        if args.second_base_url:
            add_second_readings(data, args.second_base_url)
            raw_file.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    elif args.base_url:
        raw_file = Path("experiments/results") / f"{args.name}.json"
        data = collect(args.base_url, args.specs, args.runs, args.symbol_sets, args.temperature)
        raw_file.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        parser.error("give --base-url (to run the evaluation) or --rescore (to score saved runs)")

    report = tables(data)
    raw_file.with_suffix(".md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
