"""Tests for step 44: specs about the whole runs of an agent system. No LLM, no GPU.

Five things: a situation can be a whole run, a scenario can be an example,
a link that only renames is asked about with both symbols in view, the pairs
with a rule of a change are asked about first, and a project too large for
one document is checked in parts.
"""

import json
import sys
from pathlib import Path

import pytest

from speccheck import change as change_module
from speccheck import cli, probe
from speccheck.change import combine_parts, merge, parts, with_examples
from speccheck.checks import analyze, is_doubtful
from speccheck.explain import evidence, render
from speccheck.logic import Vocabulary
from speccheck.probe import (CONDITIONS_SYSTEM, LINK_SYSTEM, OUTCOMES_SYSTEM, _about, _clashing_pairs, _first,
                             _open_pairs, _renamed, outcomes, question)


def symbols(*names, events=(), numbers=()):
    """Symbol entries: yes/no symbols, those in `numbers` whole numbers; `events` are marked as events."""
    return [{"name": name, "sort": "Int" if name in numbers else "Bool", "values": [],
             "description": f"about {name}", "event": name in events} for name in names]


def conflicts(findings):
    return [f for f in findings if f["type"] == "conflict"]


# ------------------------------------------------------- a situation is a run

# "WHEN a call of ship_parcel succeeds in a run with a plan THEN an earlier request_signoff was approved" and
# "WHEN an express request is handled in a run THEN request_signoff is not called in the run".
SHIP = {"id": "R2", "trigger": "ship_succeeds", "antecedent": "(and ship_succeeds run_has_plan)",
        "consequent": "signoff_called"}
EXPRESS = {"id": "R6", "trigger": "express_request", "antecedent": "express_request",
           "consequent": "(not signoff_called)"}


def runs(rules: list[dict], situation: str | None = None) -> dict:
    """A formal model about the runs of a dispatcher; `situation` as formalize(whole_run=True) sets it."""
    return {
        "symbols": symbols("ship_succeeds", "run_has_plan", "express_request", "signoff_called", "signoff_approved",
                           "audit_written", events=("ship_succeeds", "express_request")),
        "background": [],
        "rules": [{"status": "accepted", "text": "", **rule} for rule in rules],
        **({"situation": situation} if situation else {}),
    }


def test_two_happenings_in_one_run_are_no_reason_for_doubt():
    (conflict,) = conflicts(analyze(runs([SHIP, EXPRESS])))
    assert conflict["simultaneous_events"] == ["express_request", "ship_succeeds"] and is_doubtful(conflict)
    (conflict,) = conflicts(analyze(runs([SHIP, EXPRESS], situation="run")))
    assert conflict["rules"] == ["R2", "R6"] and not is_doubtful(conflict)


def test_in_a_run_the_pairs_of_two_happenings_are_asked_about():
    # What the two demand shares no symbol: "an earlier sign-off was approved" and "no sign-off is called".
    approved = {**SHIP, "consequent": "signoff_approved"}
    for check, rules in ((_open_pairs, [approved, EXPRESS]), (_clashing_pairs, [SHIP, EXPRESS])):
        model = runs(rules)
        assert check(Vocabulary(model["symbols"]), model) == []  # two different events: skipped
        model = runs(rules, situation="run")
        ((first, second, _, _),) = check(Vocabulary(model["symbols"]), model)
        assert (first["id"], second["id"]) == ("R2", "R6")


def test_the_questions_speak_of_a_run():
    for prompt in (OUTCOMES_SYSTEM, CONDITIONS_SYSTEM):
        assert _about(prompt, {}) == prompt
        for_runs = _about(prompt, {"situation": "run"})
        assert "ONE run of a software system" in for_runs and "in the same run?" in for_runs
        assert "snapshot" not in for_runs


class Answers:
    """Stands in for llm.LLM: one answer for each kind of question, by its prompt."""

    def __init__(self, link="impossible", outcome="possible"):
        self.answer = {LINK_SYSTEM: link, OUTCOMES_SYSTEM: outcome}
        self.asked = []

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        self.asked.append((system, user))
        return [{"reason": "", "answer": self.answer[system], "fact": ""}] * samples


# ------------------------------------------------- the pairs of a change first


def test_the_pairs_with_a_rule_of_the_change_come_first():
    pairs = [({"id": a}, {"id": b}, {}, {}) for a, b in (("R1", "R2"), ("R1", "R9"), ("R3", "R4"), ("R9", "R4"))]
    assert _first(pairs, None) == pairs
    assert [(a["id"], b["id"]) for a, b, _, _ in _first(pairs, {"R9"})] == [
        ("R1", "R9"), ("R9", "R4"), ("R1", "R2"), ("R3", "R4")]


def test_when_not_every_pair_is_asked_about_those_of_the_change_are(monkeypatch):
    monkeypatch.setattr(probe, "MAX_PAIRS", 1)
    audit = {"id": "R1", "trigger": "ship_succeeds", "antecedent": "ship_succeeds", "consequent": "audit_written"}
    approved = {**SHIP, "consequent": "signoff_approved"}
    express = {**EXPRESS, "trigger": "ship_succeeds", "antecedent": "ship_succeeds"}
    model = runs([audit, approved, express])
    outcomes(Answers(), model, Vocabulary(model["symbols"]), 0.7)
    assert model["outcome_pairs"][0]["rules"] == ["R1", "R2"] and model["outcome_pairs_skipped"] == 2
    model = runs([audit, approved, express])
    outcomes(Answers(), model, Vocabulary(model["symbols"]), 0.7, first={"R6"})
    assert model["outcome_pairs"][0]["rules"] == ["R1", "R6"]


# ------------------------------------------------- a link that only renames


def settings() -> dict:
    """Two settings with names that differ by one word, and a link that takes one for the other."""
    return {
        "symbols": symbols("max_parcels", "max_batch_parcels", numbers=("max_parcels", "max_batch_parcels")),
        "background": [{"id": "F1", "text": "",
                        "formula": "(=> (and true (= max_parcels 20)) (= max_batch_parcels 20))",
                        "restates": "S1", "antecedent": "true", "consequent": "(= max_batch_parcels 20)"}],
        "rules": [
            # "rejected" only so that no readings are probed (as in test_probe.py).
            {"id": "S1", "text": "The setting `shipping.max_parcels` MUST be 20.", "status": "rejected",
             "antecedent": "true", "consequent": "(= max_parcels 20)"},
            {"id": "S2", "text": "The setting `shipping.max_batch_parcels` MUST be 50.", "status": "rejected",
             "antecedent": "true", "consequent": "(= max_batch_parcels 50)"},
        ],
    }


def test_a_link_that_moves_a_demand_to_another_symbol_is_shown_with_both():
    model = settings()
    vocab = Vocabulary(model["symbols"])
    assert _renamed(vocab, model["rules"][0], model["background"][0]) == ({"max_parcels": 20},
                                                                         {"max_batch_parcels": 21})
    # Not the same demand on another symbol: the usual link, which says a thing in other terms.
    other = {**model["background"][0], "consequent": "(<= max_batch_parcels 50)"}
    assert _renamed(vocab, model["rules"][0], other) is None


def test_a_renaming_link_stays_only_if_the_two_symbols_cannot_differ():
    for outcome, verdict, found in (("possible", "rejected", []), ("impossible", "confirmed", [["S1", "S2"]])):
        model, llm = settings(), Answers(link="impossible", outcome=outcome)
        question(llm, model, Vocabulary(model["symbols"]), "", temperature=0.7)
        check = model["background"][0]["check"]
        assert check["renames"] == {"own": {"max_parcels": 20}, "other": {"max_batch_parcels": 21},
                                    "answers": {"possible": 8 * (outcome == "possible"),
                                                "impossible": 8 * (outcome == "impossible"), "unclear": 0}}
        assert check["verdict"] == verdict
        # The second question shows both symbols, each with its description.
        (prompt,) = [user for system, user in llm.asked if system == OUTCOMES_SYSTEM]
        assert "about max_parcels" in prompt and "about max_batch_parcels" in prompt
        for rule in model["rules"]:
            rule["status"] = "accepted"
        assert [c["rules"] for c in conflicts(analyze(model))] == found


def test_a_link_in_other_terms_gets_no_second_question():
    model = settings()
    model["background"][0].update(formula="(=> (and true (= max_parcels 20)) (<= max_batch_parcels 50))",
                                  consequent="(<= max_batch_parcels 50)")
    llm = Answers()
    question(llm, model, Vocabulary(model["symbols"]), "", temperature=0.7)
    assert "renames" not in model["background"][0]["check"]
    assert [system for system, _ in llm.asked] == [LINK_SYSTEM]


# -------------------------------------------------------------------- examples

SHIPPING = """# shipping Specification

## Purpose

A dispatcher assistant ships parcels.

## Requirements

### Requirement: Audit

Every shipment SHALL be audited.

#### Scenario: Every shipment is audited

- **WHEN** a call of `ship_parcel` succeeds
- **THEN** the run writes one audit entry

### Requirement: Requests

The assistant SHALL handle the requests below.

#### Scenario: Example: a complete address

- **WHEN** dana asks to ship parcel k7
- **AND** the address of k7 is complete
- **THEN** `ship_parcel` is called once

#### Scenario: The postcode is missing

- **WHEN** the same request runs while the address of k7 has no postcode
- **THEN** `ship_parcel` is never called

```yaml
kind: example
request: ship k7
```
"""

DEPOT = """# depot Specification

## Purpose

The depot.

## Requirements

### Requirement: Stock

The depot SHALL count its stock.

#### Scenario: Goods arrive

- **WHEN** goods arrive
- **THEN** the stock goes up

#### Scenario: Goods leave

- **WHEN** goods leave
- **THEN** the stock goes down
"""

GIFTS = """## ADDED Requirements

### Requirement: Gifts

A parcel SHALL carry a gift.

#### Scenario: A gift in every parcel

- **WHEN** a call of `ship_parcel` succeeds
- **THEN** a gift is added

#### Scenario: Example: no gift without a postcode

- **WHEN** dana asks to ship parcel k7 while its address has no postcode
- **THEN** no gift is added
"""


def project(folder: Path) -> Path:
    """An OpenSpec project with two spec files and a change that adds a third; returns the change folder."""
    for capability, text in (("depot", DEPOT), ("shipping", SHIPPING)):
        spec = folder / "openspec" / "specs" / capability / "spec.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(text, encoding="utf-8")
    delta = folder / "openspec" / "changes" / "add-gifts" / "specs" / "gifts" / "spec.md"
    delta.parent.mkdir(parents=True)
    delta.write_text(GIFTS, encoding="utf-8")
    return delta.parent.parent.parent


def examples_of(merged) -> list[str]:
    return [label for label, scenario in merged.scenarios.items() if scenario.get("example")]


def test_a_scenario_is_an_example_when_the_pattern_is_in_its_name_or_below_it(tmp_path):
    change = project(tmp_path)
    assert examples_of(merge(change)) == []
    assert examples_of(merge(change, examples="^Example:")) == ["R4", "R7"]
    assert examples_of(merge(change, examples="^kind: example$")) == ["R5"]  # a line below its name
    assert examples_of(merge(change, examples="^Example:|^kind: example$")) == ["R4", "R5", "R7"]


def returns(rules: list[dict], examples: tuple, facts: tuple = ()) -> dict:
    """A formal model about parcels; the rules named in `examples` are examples (as --examples marks them)."""
    model = {"symbols": symbols("return_asked", "delivered", "in_warehouse", "customer_cancels", "return_booked",
                                "express", "shipped", "signoff_approved"),
             "background": [{"id": f"F{n}", "text": "", "formula": fact} for n, fact in enumerate(facts, start=1)],
             "rules": [{"status": "accepted", "text": "", **rule} for rule in rules]}

    class Merged:  # as change.Merged: only the scenarios are looked at
        scenarios = {rule["id"]: {"example": True} for rule in rules if rule["id"] in examples}

    return with_examples(model, Merged)


# "WHEN dana asks to return parcel k7 AND k7 was delivered THEN book_return is called once" and
# "WHEN the same request runs while k7 is still in the warehouse THEN book_return is never called".
BOOKED = {"id": "R9", "antecedent": "(and return_asked delivered)", "consequent": "return_booked"}
NOT_BOOKED = {"id": "R10", "antecedent": "(and return_asked in_warehouse)", "consequent": "(not return_booked)"}


def test_two_examples_of_one_request_clash_only_in_a_situation_that_neither_describes():
    (conflict,) = conflicts(analyze(returns([BOOKED, NOT_BOOKED], examples=())))
    assert not is_doubtful(conflict)  # read as two rules for all cases
    marked = returns([BOOKED, NOT_BOOKED], examples=("R9", "R10"))
    assert [rule.get("example") for rule in marked["rules"]] == [True, True]
    (conflict,) = conflicts(analyze(marked))
    assert conflict["beyond_example"] == ["R9", "R10"] and is_doubtful(conflict)
    assert ("R9, R10 are examples, one concrete case each, and what each describes does not make the other "
            "requirement(s) apply, or can be the case with them obeyed: this situation says more than they do."
            ) in evidence(conflict, marked)
    assert "doubtful: the situation says more than the example does" in render([conflict], [marked], "t")


def test_an_example_and_a_variant_of_it_are_two_cases():
    # "WHEN mira asks to borrow book b12 THEN lend_book is called once" and
    # "WHEN the same request runs while b12 is reserved THEN lend_book is never called".
    base = {"id": "R2", "antecedent": "return_asked", "consequent": "return_booked"}
    variant = {"id": "R4", "antecedent": "(and return_asked in_warehouse)", "consequent": "(not return_booked)"}
    marked = returns([base, variant], examples=("R2", "R4"))
    (conflict,) = conflicts(analyze(marked))
    # The variant makes the first example apply, but the first does not say what the variant adds.
    assert conflict["beyond_example"] == ["R2"] and is_doubtful(conflict)
    assert "R2 is an example, one concrete case, and what it describes" in evidence(conflict, marked)
    # As it was before step 45: one example that describes the situation was enough.
    (conflict,) = conflicts(analyze(marked, every_example=False))
    assert not is_doubtful(conflict) and conflict["special_case"] == {"general": "R2", "special": "R4"}
    # The first one as a rule for all cases: the variant is an example that breaks it.
    (conflict,) = conflicts(analyze(returns([base, variant], examples=("R4",))))
    assert not is_doubtful(conflict)


def test_two_examples_of_the_same_case_that_demand_opposite_things_are_a_conflict():
    same_case = {**NOT_BOOKED, "antecedent": BOOKED["antecedent"]}
    (conflict,) = conflicts(analyze(returns([BOOKED, same_case], examples=("R9", "R10"))))
    assert conflict["rules"] == ["R9", "R10"] and not is_doubtful(conflict)


def test_an_example_against_a_rule_counts_when_the_example_itself_makes_the_rule_apply():
    # "WHEN dana sends an express request THEN ship_parcel succeeds and nobody signs off", against
    # "WHEN a call of ship_parcel succeeds THEN a sign-off was approved": the example says that a parcel is shipped.
    example = {"id": "R7", "antecedent": "express", "consequent": "(and shipped (not signoff_approved))"}
    gate = {"id": "R2", "antecedent": "shipped", "consequent": "signoff_approved"}
    (conflict,) = conflicts(analyze(returns([gate, example], examples=("R7",))))
    assert conflict["rules"] == ["R2", "R7"] and not is_doubtful(conflict)
    # The same example against a rule about parcels in the warehouse: nothing in it says where its parcel is.
    elsewhere = {"id": "R2", "antecedent": "in_warehouse", "consequent": "signoff_approved"}
    marked = returns([elsewhere, example], examples=("R7",))
    (conflict,) = conflicts(analyze(marked))
    assert conflict["beyond_example"] == ["R7"] and is_doubtful(conflict)
    assert "R7 is an example, one concrete case, and what it describes" in evidence(conflict, marked)
    # An assumed fact can say that the example's case is one in which the rule applies.
    with_fact = returns([elsewhere, example], examples=("R7",), facts=("(=> express in_warehouse)",))
    (conflict,) = conflicts(analyze(with_fact))
    assert not is_doubtful(conflict)


# --------------------------------------------------- a large project, in parts


def test_a_small_project_is_one_document_and_a_large_one_is_checked_in_parts(tmp_path):
    change = project(tmp_path)
    assert parts(change) == [{"depot", "shipping", "gifts"}]
    assert parts(change, limit=6) == [{"gifts", "depot"}, {"gifts", "shipping"}]
    # Only against the spec files that a pattern names; the files of the change are always in.
    assert parts(change, against="ship*", limit=6) == [{"gifts", "shipping"}]
    assert parts(change, against="nothing*", limit=6) == [{"gifts"}]


def test_a_scenario_has_the_same_label_in_every_part(tmp_path):
    change = project(tmp_path)
    whole = merge(change)
    assert list(whole.scenarios) == ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]
    part = merge(change, only={"gifts", "shipping"})
    assert list(part.scenarios) == ["R3", "R4", "R5", "R6", "R7"]
    assert all(part.scenarios[label] == whole.scenarios[label] for label in part.scenarios)
    assert "#### Scenario R6: A gift in every parcel" in part.text and "Goods arrive" not in part.text


def part_models() -> list[dict]:
    """The formal models of the two parts of `project` (limit 6), written by hand.

    R6 "a gift in every parcel" and R7 "no gift without a postcode" clash in
    both parts; R6 and R5 of the shipping spec ("never called" became "no
    gift either") clash in the part of that spec.
    """
    def rules(*some):
        return [{"status": "accepted", "text": f"text of {rule['id']}", **rule} for rule in some]

    gift = {"id": "R6", "antecedent": "ship_succeeds", "consequent": "gift_added"}
    no_gift = {"id": "R7", "antecedent": "(and ship_succeeds no_postcode)", "consequent": "(not gift_added)"}
    depot = {"symbols": symbols("ship_succeeds", "no_postcode", "gift_added", "goods_arrive", "stock_up",
                                events=("ship_succeeds", "goods_arrive")),
             "background": [],
             "rules": rules({"id": "R1", "antecedent": "goods_arrive", "consequent": "stock_up"},
                            {"id": "R2", "antecedent": "(not goods_arrive)", "consequent": "(not stock_up)"},
                            gift, no_gift)}
    shipping = {"symbols": symbols("ship_succeeds", "no_postcode", "gift_added", "audit_written", "request",
                                   events=("ship_succeeds",)),
                "background": [],
                "rules": rules({"id": "R3", "antecedent": "ship_succeeds", "consequent": "audit_written"},
                               {"id": "R4", "antecedent": "request", "consequent": "audit_written"},
                               {"id": "R5", "antecedent": "(and ship_succeeds request)",
                                "consequent": "(not gift_added)"},
                               gift, no_gift)}
    return [depot, shipping]


def test_the_findings_of_the_parts_are_put_together():
    models, changed = part_models(), [{"R6", "R7"}, {"R6", "R7"}]
    findings = combine_parts([analyze(model) for model in models], models, changed)
    found = {tuple(f["rules"]): f for f in conflicts(findings)}
    assert set(found) == {("R6", "R7"), ("R5", "R6")}
    assert found["R6", "R7"]["parts"] == "2/2" and found["R6", "R7"]["model"] == 0
    # One part holds R5, so there is nothing to count.
    assert "parts" not in found["R5", "R6"] and found["R5", "R6"]["model"] == 1
    # The gaps among the rules of one other file are not findings about the project.
    assert [f for f in findings if f["type"] == "gap"] == []


def test_a_count_of_parts_is_of_the_parts_that_have_the_finding_as_it_is_shown():
    models, changed = part_models(), [{"R6", "R7"}, {"R6", "R7"}]
    plain = {"type": "conflict", "rules": ["R6", "R7"], "when": {}}
    doubted = {**plain, "beyond_example": ["R7"]}
    other = {"type": "conflict", "rules": ["R5", "R6"], "when": {}, "beyond_example": ["R5"]}
    # Doubtful in one part and not in the other: shown as it is in the other, and counted there.
    (first, second) = combine_parts([[doubted], [other, plain]], models, changed)
    assert first["rules"] == ["R6", "R7"] and first["parts"] == "1/2" and not is_doubtful(first) and first["model"] == 1
    assert second["rules"] == ["R5", "R6"] and is_doubtful(second)  # what is doubtful comes last
    # Doubtful in both: counted in both.
    (only,) = combine_parts([[doubted], [doubted]], models, changed)
    assert only["parts"] == "2/2" and is_doubtful(only)


def test_a_gap_about_the_change_is_kept_only_if_every_part_has_it():
    models, changed = part_models(), [{"R6", "R7"}, {"R6", "R7"}]
    gap = {"type": "gap", "event": "ship_succeeds", "when": {"ship_succeeds": True}}
    in_both = combine_parts([[gap], [gap]], models, changed)
    assert [(f["type"], f["model"]) for f in in_both] == [("gap", 0)]
    assert combine_parts([[gap], []], models, changed) == []  # a rule of the other file covers it
    other = {"type": "gap", "event": "goods_arrive", "when": {"goods_arrive": True}}
    assert combine_parts([[other], [gap]], models, changed) == []  # not about the change, and not in both


def test_saved_models_of_the_parts_are_taken_by_their_rules(tmp_path, monkeypatch, capsys):
    change = project(tmp_path / "project")
    monkeypatch.setattr(change_module, "PART_LIMIT", 6)
    for number, model in enumerate(part_models(), start=1):
        (tmp_path / f"formal_{number:02}.json").write_text(json.dumps(model), encoding="utf-8")
    pattern = str(tmp_path / "formal_*.json")  # expanded by the tool, in any shell

    def run(*options) -> str:
        monkeypatch.setattr(sys, "argv", ["speccheck", "--change", str(change), "--out", str(tmp_path / "out"),
                                          "--examples", "^Example:", *options])
        cli.main()
        capsys.readouterr()
        return (tmp_path / "out" / "report.md").read_text(encoding="utf-8")

    # In any order: each part takes the model that holds its rules.
    both = run("--formal", str(tmp_path / "formal_02.json"), str(tmp_path / "formal_01.json"))
    assert "7 requirements analysed in 2 part(s): 2 conflict(s)" in both and "found in 2 of 2 parts" in both
    assert run("--formal", pattern) == both
    # Against one spec file only: one document, and of the two saved models the one of that file.
    one = run("--formal", pattern, "--against", "ship*")
    assert "5 requirements analysed: 2 conflict(s)" in one and "parts" not in one.split("## The rules")[0]
    monkeypatch.setattr(sys, "argv", ["speccheck", "--change", str(change), "--formal", str(tmp_path / "none_*.json")])
    with pytest.raises(SystemExit):
        cli.main()


def test_a_part_with_a_rule_that_has_no_label_is_left_out(tmp_path, monkeypatch):
    piece = merge(project(tmp_path), only={"gifts", "depot"})
    model = part_models()[0]
    job = ("http://nowhere/v1", "a model", piece, 8, 0.7, False, None)
    monkeypatch.setattr(cli, "LLM", lambda base_url, model_name: None)
    monkeypatch.setattr(cli, "formalize", lambda *args, **options: model)
    assert cli._formalize_part(job) == model
    # R3 is the label of a scenario in the other part: a rule of that name here would be taken for it.
    extra = {**model, "rules": model["rules"] + [{**model["rules"][0], "id": "R3"}]}
    monkeypatch.setattr(cli, "formalize", lambda *args, **options: extra)
    assert cli._formalize_part(job) == {"error": "the read step made rules without a scenario label (R3)"}


@pytest.mark.parametrize("broken", [False, True])
def test_the_command_line_checks_a_large_project_in_parts(tmp_path, monkeypatch, capsys, broken):
    change = project(tmp_path / "project")
    monkeypatch.setattr(change_module, "PART_LIMIT", 6)
    saved = []
    for number, model in enumerate(part_models(), start=1):
        saved.append(tmp_path / f"formal_{number:02}.json")
        saved[-1].write_text(json.dumps({"error": "no answer"} if broken and number == 1 else model), encoding="utf-8")
    out = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", ["speccheck", "--change", str(change), "--out", str(out),
                                      "--examples", "^Example:", "--formal", *map(str, saved)])
    cli.main()
    report = (out / "report.md").read_text(encoding="utf-8")
    assert capsys.readouterr().out.strip() == report.strip()
    findings = {tuple(f["rules"]): f for f in json.loads((out / "findings.json").read_text(encoding="utf-8"))
                if f["type"] == "conflict"}
    assert findings["R5", "R6"]["about_change"] is True
    assert "| R7 | gifts | Gifts | Example: no gift without a postcode | **added** |" in report
    if broken:
        assert "requirements analysed in 1 part(s)" in report
        assert ("1 part(s) could not be formalized, so the change was not checked against: `depot` "
                "(no saved formal model of this part was given).") in report
        assert "parts" not in findings["R6", "R7"]
    else:
        assert "7 requirements analysed in 2 part(s): 2 conflict(s)" in report
        assert "The change was checked in 2 parts" in report
        assert "found in 2 of 2 parts" in report and findings["R6", "R7"]["parts"] == "2/2"
