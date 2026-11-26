"""Tests for check 5 of probe.py: the question whether the conditions of two rules that clash
can both hold. No LLM, no GPU.

The LLM is replaced by a stand-in with fixed answers, so these tests check
which pairs are asked about and what is done with the answers.
"""

from speccheck.checks import analyze
from speccheck.logic import Vocabulary
from speccheck.probe import CONDITIONS_SYSTEM, _clashing_pairs, conditions


def formal(rules: list[dict], facts: list[str] = (), events=("tasks_read", "folder_made")) -> dict:
    """A formal model over a few yes/no symbols; `events` are the ones marked as events."""
    names = ("tasks_read", "folder_made", "tasks_file_exists", "all_tasks_complete", "warning_shown",
             "quiet_mode", "strict_mode", "summary_shown")
    return {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}",
                     "event": name in events} for name in names],
        "background": [{"id": f"F{n}", "text": text, "formula": text} for n, text in enumerate(facts, start=1)],
        "rules": [{"status": "accepted", "text": "", **rule} for rule in rules],
    }


# "WHEN the agent reads tasks.md AND incomplete tasks are found THEN display a warning" and
# "WHEN tasks.md does not exist THEN proceed without a warning": to Z3 a file can be read and not exist.
WARN = {"id": "R5", "trigger": "tasks_read",
        "antecedent": "(and tasks_read (not all_tasks_complete))", "consequent": "warning_shown"}
NO_FILE = {"id": "R7", "trigger": "", "antecedent": "(not tasks_file_exists)", "consequent": "(not warning_shown)"}


class FakeLLM:
    """Stands in for llm.LLM: gives the same list of answers to every question."""

    def __init__(self, answers: list[str]):
        self.answers = answers
        self.prompts = []

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        assert system == CONDITIONS_SYSTEM
        self.prompts.append(user)
        return [{"reason": "", "answer": answer,
                 "fact": "A file that does not exist cannot be read." if answer == "impossible" else ""}
                for answer in self.answers]


def asked(model: dict) -> list[tuple]:
    """The ids of the pairs that check 5 would ask about."""
    return [(first["id"], second["id"]) for first, second, _, _ in _clashing_pairs(Vocabulary(model["symbols"]), model)]


def conflicts(model: dict) -> list[dict]:
    return [f for f in analyze(model) if f["type"] == "conflict"]


def test_two_rules_that_clash_under_two_different_conditions_are_asked_about():
    model = formal([WARN, NO_FILE])
    first, second, first_only, second_only = _clashing_pairs(Vocabulary(model["symbols"]), model)[0]
    assert (first["id"], second["id"]) == ("R5", "R7")
    assert first_only == {"tasks_read": True, "all_tasks_complete": False} and second_only == {"tasks_file_exists": False}


def test_pairs_that_are_not_asked_about():
    # Both can be obeyed when both apply: there is no conflict to doubt.
    summary = {**NO_FILE, "consequent": "summary_shown"}
    assert asked(formal([WARN, summary])) == []
    # The same condition: the two apply together by their words.
    opposite = {**WARN, "id": "R6", "consequent": "(not warning_shown)"}
    assert asked(formal([WARN, opposite])) == []
    # A rule and a special case of it.
    special = {**WARN, "id": "R6", "antecedent": "(and tasks_read (not all_tasks_complete) quiet_mode)",
               "consequent": "(not warning_shown)"}
    assert asked(formal([WARN, special])) == []
    # Two different events: that conflict is marked doubtful anyway.
    other_event = {"id": "R8", "trigger": "folder_made", "antecedent": "folder_made", "consequent": "(not warning_shown)"}
    assert asked(formal([WARN, other_event])) == []
    # The two never apply together: Z3 sees it, or an assumed fact says it.
    never = {**NO_FILE, "antecedent": "all_tasks_complete"}
    assert asked(formal([WARN, never])) == []
    assert asked(formal([WARN, NO_FILE], ["(=> tasks_read tasks_file_exists)"])) == []
    # A condition that is not one definite state cannot be shown as a list of facts.
    vague = {**NO_FILE, "antecedent": "(or (not tasks_file_exists) strict_mode)"}
    assert asked(formal([WARN, vague])) == []
    # A rejected rule takes no part.
    assert asked(formal([WARN, {**NO_FILE, "status": "rejected"}])) == []


def test_most_answers_impossible_gives_a_fact_and_the_fact_casts_doubt_on_the_conflict():
    model = formal([WARN, NO_FILE])
    (before,) = conflicts(model)
    assert before["rules"] == ["R5", "R7"] and "doubted_by" not in before  # proven from the rules alone

    llm = FakeLLM(["impossible"] * 7 + ["possible"])
    conditions(llm, model, Vocabulary(model["symbols"]), temperature=0.7)

    # The model saw what only one condition says and what only the other says, and no requirement text.
    assert llm.prompts == ["Statement A:\n- FALSE: all_tasks_complete (about all_tasks_complete)\n- TRUE: tasks_read (about tasks_read)\n\n"
                           "Statement B:\n- FALSE: tasks_file_exists (about tasks_file_exists)"]
    assert model["condition_pairs"] == [{"rules": ["R5", "R7"], "answers": {"possible": 1, "impossible": 7, "unclear": 0}}]
    assert model["background"] == [{
        "id": "F1", "between": ["R5", "R7"], "about": "conditions", "support": "7/8",
        "text": "The conditions of R5 and R7 cannot both hold: A file that does not exist cannot be read.",
        "formula": "(not (and (and tasks_read (not all_tasks_complete)) (not tasks_file_exists)))"}]
    # The conflict is still reported, and the fact casts doubt on it.
    (after,) = conflicts(model)
    assert after["rules"] == ["R5", "R7"] and after["doubted_by"] == ["F1"]


def test_without_a_majority_the_conflict_stays_as_it_is():
    model = formal([WARN, NO_FILE])
    conditions(FakeLLM(["impossible"] * 4 + ["possible"] * 4), model, Vocabulary(model["symbols"]), temperature=0.7)
    assert model["background"] == [] and model["condition_pairs"][0]["answers"]["impossible"] == 4
    assert "doubted_by" not in conflicts(model)[0]


def test_a_conflict_that_needs_an_assumed_fact_is_not_found_any_more():
    # The two outcomes are written with two symbols; a fact of check 4 says that they exclude each other.
    summary = {**NO_FILE, "consequent": "summary_shown"}
    model = formal([WARN, summary], ["(not (and warning_shown summary_shown))"])
    assert [f["rules"] for f in conflicts(model)] == [["R5", "R7"]]
    conditions(FakeLLM(["impossible"] * 8), model, Vocabulary(model["symbols"]), temperature=0.7)
    assert conflicts(model) == []


def test_only_pairs_with_a_new_rule_are_asked_about_when_rules_are_added():
    model = formal([WARN, NO_FILE])
    model["condition_pairs"] = [{"rules": ["R1", "R2"], "answers": {}}]
    llm = FakeLLM(["possible"] * 8)
    conditions(llm, model, Vocabulary(model["symbols"]), temperature=0.7, only={"R9"})
    assert llm.prompts == [] and model["condition_pairs"] == [{"rules": ["R1", "R2"], "answers": {}}]
    conditions(llm, model, Vocabulary(model["symbols"]), temperature=0.7, only={"R7"})
    assert len(llm.prompts) == 1 and [pair["rules"] for pair in model["condition_pairs"]] == [["R1", "R2"], ["R5", "R7"]]
