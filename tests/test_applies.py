"""Tests for check 6 of probe.py: does what one rule demands make another rule apply? No LLM, no GPU.

The LLM is replaced by a stand-in with fixed answers, so these tests check
which pairs are asked about and what is done with the answers.
"""

from speccheck import probe
from speccheck.change import with_examples
from speccheck.checks import analyze, is_doubtful
from speccheck.logic import Vocabulary
from speccheck.probe import APPLIES_SYSTEM, _bridge_pairs, applies

NAMES = ("check_in_succeeds", "run_has_plan", "approved_earlier", "manager_asked", "late_arrival_run",
         "night_code_given", "walk_in_request", "checked_in_once", "plan_written_once", "record_written")


def formal(rules: list[dict], facts: list[str] = (), examples: tuple = ()) -> dict:
    """A formal model about the runs of a front desk; the rules named in `examples` are examples."""
    model = {
        "situation": "run",
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}",
                     "event": name in ("check_in_succeeds", "manager_asked", "walk_in_request")} for name in NAMES],
        "background": [{"id": f"F{n}", "text": text, "formula": text} for n, text in enumerate(facts, start=1)],
        "rules": [{"status": "accepted", **rule} for rule in rules],
    }

    class Merged:  # as change.Merged: only the scenarios are looked at
        scenarios = {rule["id"]: {"example": True} for rule in rules if rule["id"] in examples}

    return with_examples(model, Merged)


GATE = {"id": "R1", "trigger": "check_in_succeeds", "antecedent": "(and check_in_succeeds run_has_plan)",
        "consequent": "approved_earlier",
        "text": "WHEN a call of check_in_guest succeeds in a run with a plan THEN an earlier call of ask_manager was approved"}
NOBODY = {"id": "R4", "trigger": "manager_asked", "antecedent": "manager_asked", "consequent": "(not late_arrival_run)",
          "text": "WHEN a call of ask_manager is made THEN the run is not a late-arrival run"}
LATE = {"id": "R5", "trigger": "check_in_succeeds", "antecedent": "(and check_in_succeeds late_arrival_run)",
        "consequent": "night_code_given",
        "text": "WHEN a call of check_in_guest succeeds in a late-arrival run THEN the answer gives the night code"}


class FakeLLM:
    """Stands in for llm.LLM: "yes" when the requirement is one of `linked` (rule texts), else "no"."""

    def __init__(self, linked: tuple = (), by: str = "demand"):
        self.linked, self.prompts, self.by = linked, [], by   # by: what the answers say makes B true

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        assert system == probe._about(APPLIES_SYSTEM, {"situation": "run"}) and "ONE run of that system" in system
        self.prompts.append(user)
        requirement = user.split("\n\nStatement B:")[0]
        answer = "yes" if any(text in requirement for text in self.linked) else "no"
        return [{"reason": "", "answer": answer, "by": self.by if answer == "yes" else "none",
                 "fact": "An approved call is a call that was made." if answer == "yes" else ""}] * samples


def asked(model: dict) -> list[tuple]:
    """(a, b, the part of b's condition) for each question that check 6 would ask."""
    return [(a["id"], b["id"], part) for a, b, part in _bridge_pairs(Vocabulary(model["symbols"]), model)]


def conflicts(model: dict) -> list[dict]:
    return [f for f in analyze(model) if f["type"] == "conflict"]


def test_a_chain_of_three_rules_is_asked_about_where_one_demand_could_make_another_rule_apply():
    model = formal([GATE, NOBODY, LATE])
    assert conflicts(model) == []  # no two of the three clash by themselves
    # In a late-arrival run with a plan R4 cannot apply. Does what R1 demands there make it apply?
    # The same is asked of R5, which applies in such a run as well.
    assert asked(model) == [("R1", "R4", {"manager_asked": True}), ("R5", "R4", {"manager_asked": True})]


def test_an_answer_that_the_requirement_says_so_is_a_fact_and_the_chain_is_found():
    model, llm = formal([GATE, NOBODY, LATE]), FakeLLM(linked=(GATE["text"],))
    applies(llm, model, Vocabulary(model["symbols"]), temperature=0.7)
    # The words of R1, and the part of R4's condition as one statement.
    assert llm.prompts[0] == f"Requirement:\n{GATE['text']}\n\nStatement B:\n- TRUE: manager_asked (about manager_asked)"
    assert model["apply_pairs"] == [
        {"rules": ["R1", "R4"], "part": {"manager_asked": True}, "answers": {"yes": 8, "no": 0, "unclear": 0},
         "by": {"condition": 0, "demand": 8}},
        {"rules": ["R5", "R4"], "part": {"manager_asked": True}, "answers": {"yes": 0, "no": 8, "unclear": 0}}]
    assert model["background"] == [{
        "id": "F1", "between": ["R1", "R4"], "about": "applies", "support": "8/8",
        "formula": "(=> (and (and check_in_succeeds run_has_plan) approved_earlier) manager_asked)",
        "text": "Where R1 applies and is obeyed, a part of the condition of R4 holds: "
                "An approved call is a call that was made."}]
    (conflict,) = conflicts(model)
    assert conflict["rules"] == ["R1", "R4"] and conflict["facts"] == ["F1"] and not is_doubtful(conflict)
    assert conflict["when"] == {"check_in_succeeds": True, "late_arrival_run": True, "run_has_plan": True}


def test_an_answer_that_it_does_not_adds_nothing():
    model = formal([GATE, NOBODY, LATE])
    applies(FakeLLM(), model, Vocabulary(model["symbols"]), temperature=0.7)
    assert model["background"] == [] and len(model["apply_pairs"]) == 2 and conflicts(model) == []


def test_a_step_that_the_condition_alone_gives_is_a_fact_about_the_condition():
    # "WHEN a call of ask_manager is refused THEN the answer says so": where this applies, a call was made,
    # whatever is answered. In a late-arrival run R4 forbids that call by itself: no clash of the two rules.
    refused = {"id": "R7", "trigger": "manager_refused", "antecedent": "manager_refused", "consequent": "answer_says_so",
               "text": "WHEN a call of ask_manager is refused THEN the answer says so"}
    names = [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": True}
             for name in ("manager_refused", "answer_says_so")]

    def model() -> dict:
        one = formal([refused, NOBODY, LATE])
        return {**one, "symbols": one["symbols"] + names}

    one = model()
    assert ("R7", "R4", {"manager_asked": True}) in asked(one)
    applies(FakeLLM(linked=(refused["text"],), by="condition"), one, Vocabulary(one["symbols"]), temperature=0.7)
    (fact,) = one["background"]
    assert fact["formula"] == "(=> manager_refused manager_asked)" and fact["text"].startswith("Where R7 applies, a part")
    assert one["apply_pairs"][0]["by"] == {"condition": 8, "demand": 0}
    assert conflicts(one) == []
    # Had the answers said that it takes what R7 demands, the same situation would be a conflict of R4 and R7.
    other = model()
    applies(FakeLLM(linked=(refused["text"],), by="demand"), other, Vocabulary(other["symbols"]), temperature=0.7)
    assert other["background"][0]["formula"] == "(=> (and manager_refused answer_says_so) manager_asked)"
    assert [sorted(c["rules"]) for c in conflicts(other)] == [["R4", "R7"]]


def test_pairs_that_are_not_asked_about():
    # No rule forbids the call in a late-arrival run: R4 can apply wherever R1 does.
    harmless = {**NOBODY, "consequent": "record_written"}
    assert asked(formal([GATE, harmless, LATE])) == []
    # What R1 demands is the condition of R4 itself: Z3 sees the chain, and finds the conflict.
    same_symbol = {**GATE, "consequent": "manager_asked"}
    model = formal([same_symbol, NOBODY, LATE])
    assert asked(model) == [("R5", "R4", {"manager_asked": True})]
    assert [c["rules"] for c in conflicts(model)] == [["R1", "R4"]]
    # A fact says it already.
    assert asked(formal([GATE, NOBODY, LATE], facts=["(=> approved_earlier manager_asked)"])) == [
        ("R5", "R4", {"manager_asked": True})]


# "WHEN lea sends a walk-in request THEN the plan is written once AND check_in_guest succeeds once AND
# ask_manager is never called": an example that breaks R1 by what it demands itself.
WALK_IN = {"id": "R6", "trigger": "walk_in_request", "antecedent": "walk_in_request",
           "consequent": "(and plan_written_once checked_in_once (not manager_asked))",
           "text": "WHEN lea sends a walk-in request THEN the plan is written once AND check_in_guest succeeds once "
                   "AND ask_manager is never called"}
APPROVED_IS_ASKED = "(not (and approved_earlier (not manager_asked)))"  # a fact that check 4 gave


def test_an_example_whose_demand_makes_a_rule_apply_describes_the_situation():
    model = formal([GATE, WALK_IN], facts=[APPROVED_IS_ASKED], examples=("R6",))
    (conflict,) = conflicts(model)
    # Nothing in the formulas says that "succeeds once" is "a call succeeds": the example does not make R1 apply.
    assert conflict["rules"] == ["R1", "R6"] and conflict["beyond_example"] == ["R6"]
    assert asked(model) == [("R1", "R6", {"walk_in_request": True}),
                            ("R6", "R1", {"check_in_succeeds": True}), ("R6", "R1", {"run_has_plan": True})]
    # The words of the example say it.
    applies(FakeLLM(linked=(WALK_IN["text"],)), model, Vocabulary(model["symbols"]), temperature=0.7)
    demand = "(and walk_in_request (and plan_written_once checked_in_once (not manager_asked)))"
    assert [fact["formula"] for fact in model["background"][1:]] == [
        f"(=> {demand} check_in_succeeds)", f"(=> {demand} run_has_plan)"]
    (conflict,) = conflicts(model)
    assert conflict["rules"] == ["R1", "R6"] and not is_doubtful(conflict)


def test_at_most_a_number_of_questions_and_for_a_change_only_those_with_its_rules(monkeypatch):
    model = formal([GATE, NOBODY, LATE])
    applies(FakeLLM(), model, Vocabulary(model["symbols"]), temperature=0.7, first={"R5"})
    assert [pair["rules"] for pair in model["apply_pairs"]] == [["R5", "R4"]]  # R1 and R4 were there before
    monkeypatch.setattr(probe, "MAX_PAIRS", 1)
    model = formal([GATE, NOBODY, LATE])
    applies(FakeLLM(), model, Vocabulary(model["symbols"]), temperature=0.7)
    assert [pair["rules"] for pair in model["apply_pairs"]] == [["R1", "R4"]] and model["apply_pairs_skipped"] == 1
