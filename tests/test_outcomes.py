"""Tests for check 4 of probe.py: the questions about pairs of outcomes. No LLM, no GPU.

The LLM is replaced by a stand-in with fixed answers, so these tests check
which pairs are asked about and what is done with the answers.
"""

from speccheck.checks import analyze
from speccheck.logic import Vocabulary
from speccheck.probe import OUTCOMES_SYSTEM, _as_facts, _open_pairs, outcomes


def formal(rules: list[dict], facts: list[str] = (), events=("card_tapped", "top_up")) -> dict:
    """A formal model over a few yes/no symbols; `events` are the ones marked as events."""
    names = ("card_tapped", "top_up", "balance_covers", "canteen_closed", "payment_taken",
             "payment_refused", "receipt_printed", "balance_raised")
    return {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}",
                     "event": name in events} for name in names],
        "background": [{"id": f"F{n}", "text": text, "formula": text} for n, text in enumerate(facts, start=1)],
        "rules": [{"status": "accepted", "text": "", **rule} for rule in rules],
    }


# "Take the price" and "refuse all payments", written with two symbols.
TAKE = {"id": "C1", "trigger": "card_tapped",
        "antecedent": "(and card_tapped balance_covers)", "consequent": "payment_taken"}
REFUSE = {"id": "C6", "trigger": "", "antecedent": "canteen_closed", "consequent": "payment_refused"}


class FakeLLM:
    """Stands in for llm.LLM: gives the same list of answers to every question about outcomes."""

    def __init__(self, answers: list[str]):
        self.answers = answers
        self.prompts = []

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        assert system == OUTCOMES_SYSTEM
        self.prompts.append(user)
        return [{"reason": "", "answer": answer,
                 "fact": "A payment cannot be both taken and refused." if answer == "impossible" else ""}
                for answer in self.answers]


def asked(model: dict) -> list[tuple]:
    """The ids of the pairs that check 4 would ask about."""
    return [(first["id"], second["id"]) for first, second, _, _ in _open_pairs(Vocabulary(model["symbols"]), model)]


def test_a_pair_is_asked_about_when_a_missing_fact_could_hide_a_conflict():
    """An event rule and a state rule that can apply together, with outcomes Z3 cannot relate."""
    model = formal([TAKE, REFUSE])
    first, second, first_demands, second_demands = _open_pairs(Vocabulary(model["symbols"]), model)[0]
    assert (first["id"], second["id"]) == ("C1", "C6")
    assert first_demands == {"payment_taken": True} and second_demands == {"payment_refused": True}


def test_pairs_that_are_not_asked_about():
    # Two different events: a conflict between them would be marked doubtful anyway.
    top_up = {"id": "C3", "trigger": "top_up", "antecedent": "top_up", "consequent": "balance_raised"}
    assert asked(formal([TAKE, top_up])) == []
    # A symbol in common: Z3 already sees how the two outcomes relate.
    receipt = {"id": "C2", "trigger": "", "antecedent": "canteen_closed", "consequent": "(not payment_taken)"}
    assert asked(formal([TAKE, receipt])) == []
    # The two rules never apply together.
    other_case = {"id": "C2", "trigger": "card_tapped",
                  "antecedent": "(and card_tapped (not balance_covers))", "consequent": "payment_refused"}
    assert asked(formal([TAKE, other_case])) == []
    # An assumed fact already says that the two outcomes exclude each other.
    assert asked(formal([TAKE, REFUSE], ["(not (and payment_taken payment_refused))"])) == []
    # An outcome that is not one definite state cannot be shown as a list of facts.
    vague = {**REFUSE, "consequent": "(or payment_refused receipt_printed)"}
    assert asked(formal([TAKE, vague])) == []
    # A rejected rule takes no part.
    assert asked(formal([TAKE, {**REFUSE, "status": "rejected"}])) == []


def test_only_a_definite_outcome_is_shown_as_facts():
    vocab = Vocabulary(formal([])["symbols"])
    assert _as_facts(vocab, vocab.parse("(and (not payment_taken) receipt_printed)")) == {
        "payment_taken": False, "receipt_printed": True}
    assert _as_facts(vocab, vocab.parse("(or payment_taken receipt_printed)")) is None
    assert _as_facts(vocab, vocab.parse("true")) is None


def test_most_answers_impossible_gives_a_fact_and_the_fact_gives_the_conflict():
    model = formal([TAKE, REFUSE])
    assert [f for f in analyze(model) if f["type"] == "conflict"] == []  # to Z3 both can be true

    llm = FakeLLM(["impossible"] * 6 + ["possible"] * 2)
    outcomes(llm, model, Vocabulary(model["symbols"]), temperature=0.7)

    # The model saw the two outcomes as facts, and no requirement text.
    assert llm.prompts == ["Statement A:\n- TRUE: payment_taken (about payment_taken)\n\n"
                           "Statement B:\n- TRUE: payment_refused (about payment_refused)"]
    assert model["outcome_pairs"] == [{"rules": ["C1", "C6"],
                                       "answers": {"possible": 2, "impossible": 6, "unclear": 0}}]
    assert model["background"] == [{
        "id": "F1", "between": ["C1", "C6"], "support": "6/8",
        "text": "What C1 and C6 demand cannot both be the case: A payment cannot be both taken and refused.",
        "formula": "(not (and payment_taken payment_refused))"}]
    # The solver now proves the conflict, and says which fact it needs.
    conflict = next(f for f in analyze(model) if f["type"] == "conflict")
    assert conflict["rules"] == ["C1", "C6"] and conflict["facts"] == ["F1"]
    assert conflict["when"] == {"card_tapped": True, "balance_covers": True, "canteen_closed": True}


def test_without_a_majority_nothing_is_assumed():
    model = formal([TAKE, REFUSE])
    outcomes(FakeLLM(["impossible"] * 4 + ["possible"] * 3 + ["unclear"]), model,
             Vocabulary(model["symbols"]), temperature=0.7)
    assert model["background"] == []
    assert model["outcome_pairs"][0]["answers"] == {"possible": 3, "impossible": 4, "unclear": 1}
