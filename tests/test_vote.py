"""Tests for the vote among the translations of a rule that differ in the symbols they use
(formalize._vote, through _judge). No LLM, no GPU.
"""

from speccheck.formalize import _judge
from speccheck.logic import Vocabulary

SYMBOLS = [{"name": name, "sort": sort, "values": [], "description": name, "event": False}
           for name, sort in [("move_succeeds", "Bool"), ("message_shown", "Bool"), ("summary_shown", "Bool"),
                              ("specs_updated", "Bool"), ("failed_attempts", "Int"), ("account_locked", "Bool")]]
VOCAB = Vocabulary(SYMBOLS)


def answers(*counted: tuple) -> list[dict]:
    """(how often, antecedent, consequent) -> the translations of one rule."""
    return [{"reading": "", "antecedent": antecedent, "consequent": consequent}
            for count, antecedent, consequent in counted for _ in range(count)]


def test_translations_that_differ_in_symbols_vote_for_what_they_share():
    judged = _judge(VOCAB, answers((3, "move_succeeds", "message_shown"),
                                   (2, "move_succeeds", "(and message_shown summary_shown)"),
                                   (1, "move_succeeds", "(and message_shown specs_updated)"),
                                   (1, "move_succeeds", "(and message_shown specs_updated summary_shown)")))
    # Four meanings, which used to be "rejected". All seven entail the first one.
    assert judged["clusters"] == [3, 2, 1, 1]
    assert (judged["status"], judged["consequent"], judged["voted"]) == ("accepted", "message_shown", "7/7")
    assert "alternative" not in judged


def test_the_strongest_translation_with_a_majority_is_chosen():
    # 5 of 8 say both outcomes: that has a majority by itself, and it is the stronger one.
    judged = _judge(VOCAB, answers((5, "move_succeeds", "(and message_shown summary_shown)"),
                                   (3, "move_succeeds", "message_shown")))
    assert (judged["status"], judged["consequent"], judged["voted"]) == ("accepted", "(and message_shown summary_shown)", "5/8")
    # 4 of 8 is not more than half: what all eight entail is the message alone.
    judged = _judge(VOCAB, answers((4, "move_succeeds", "(and message_shown summary_shown)"),
                                   (4, "move_succeeds", "message_shown")))
    assert (judged["status"], judged["consequent"], judged["voted"]) == ("accepted", "message_shown", "8/8")


def test_two_readings_with_the_same_symbols_stay_a_question():
    judged = _judge(VOCAB, answers((5, "(= failed_attempts 5)", "account_locked"),
                                   (3, "(>= failed_attempts 5)", "account_locked")))
    assert judged["status"] == "ambiguous" and "voted" not in judged
    assert judged["alternative"]["antecedent"] == "(>= failed_attempts 5)"
    # Also when a third translation uses another symbol: the two readings are still there.
    judged = _judge(VOCAB, answers((4, "(= failed_attempts 5)", "account_locked"),
                                   (3, "(>= failed_attempts 5)", "account_locked"),
                                   (1, "(= failed_attempts 5)", "(and account_locked message_shown)")))
    assert judged["status"] != "accepted" and "voted" not in judged


def test_without_a_majority_nothing_changes():
    judged = _judge(VOCAB, answers((4, "move_succeeds", "message_shown"), (4, "move_succeeds", "summary_shown")))
    assert judged["status"] == "ambiguous" and "voted" not in judged


def test_a_vote_for_a_translation_that_demands_nothing_rejects_the_rule():
    judged = _judge(VOCAB, answers((5, "move_succeeds", "true"), (3, "move_succeeds", "message_shown")))
    assert judged["status"] == "rejected" and judged["empty"] is True and judged["voted"] == "8/8"


def test_translations_that_agree_do_not_vote():
    judged = _judge(VOCAB, answers((7, "move_succeeds", "message_shown"), (1, "move_succeeds", "summary_shown")))
    assert judged["status"] == "accepted" and "voted" not in judged
