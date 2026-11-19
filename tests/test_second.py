"""Tests for formalize step 7: a second model translates every rule again.

No LLM, no GPU: the second model is a stand-in that returns fixed translations,
so these tests check what the code does with them.
"""

from speccheck.checks import analyze
from speccheck.formalize import second_reading


class FakeSecond:
    """Stands in for llm.LLM: the same translations for every rule."""

    def __init__(self, translations):
        self.translations = translations

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        return self.translations[:samples]


def formal_three_reports():
    """"WHEN a comment has been reported three times THEN hide it", read as exactly 3."""
    return {
        "symbols": [{"name": "report_count", "sort": "Int", "values": [], "description": "reports so far"},
                    {"name": "comment_hidden", "sort": "Bool", "values": [], "description": "hidden"}],
        "background": [],
        "rules": [{"id": "M3", "text": "WHEN a comment has been reported three times THEN hide it.",
                   "status": "accepted", "reading": "exactly three reports",
                   "antecedent": "(= report_count 3)", "consequent": "comment_hidden"}],
    }


AT_LEAST = {"reading": "three reports or more", "antecedent": "(>= report_count 3)",
            "consequent": "comment_hidden"}
EXACTLY = {"reading": "the third report", "antecedent": "(= 3 report_count)",  # written
           "consequent": "comment_hidden"}                                      # differently
BROKEN = {"reading": "unusable", "antecedent": "(>= report_count", "consequent": "comment_hidden"}


def ambiguities(findings):
    return [f for f in findings if f["type"] == "ambiguity"]


def test_a_second_model_that_reads_otherwise_makes_the_rule_ambiguous():
    formal = formal_three_reports()
    second_reading(FakeSecond([AT_LEAST] * 7 + [EXACTLY]), formal)

    second = formal["rules"][0]["second"]
    assert second["support"] == "1/8" and second["confirms"] is False
    assert second["antecedent"] == "(>= report_count 3)"  # its most common other reading
    # They differ only when there are more than 3 reports and the comment is not hidden.
    assert second["differs_when"]["report_count"] > 3 and second["differs_when"]["comment_hidden"] is False

    (finding,) = ambiguities(analyze(formal))
    assert finding["found_by"] == "models" and finding["second_support"] == "1/8"
    # The experiments can switch the second reader off.
    assert ambiguities(analyze(formal, second=False)) == []


def test_a_second_model_that_confirms_changes_nothing():
    formal = formal_three_reports()
    second_reading(FakeSecond([EXACTLY] * 6 + [AT_LEAST] * 2), formal)
    assert formal["rules"][0]["second"]["support"] == "6/8"
    assert formal["rules"][0]["second"]["confirms"] is True
    assert ambiguities(analyze(formal)) == []


def test_half_of_the_answers_do_not_confirm():
    """4 of 8 is not more than half: a split second model is a sign of ambiguity too."""
    formal = formal_three_reports()
    second_reading(FakeSecond([AT_LEAST] * 4 + [EXACTLY] * 4), formal)
    assert formal["rules"][0]["second"]["confirms"] is False
    assert len(ambiguities(analyze(formal))) == 1


def test_leaving_out_the_event_is_not_another_reading():
    """The second model writes the count alone; the translation also names the event.

    Wherever the event happens (and the rule only reacts to it), both say the
    same: the second model confirms the translation.
    """
    formal = {
        "symbols": [{"name": "failed_deliveries", "sort": "Int", "values": [], "description": ""},
                    {"name": "delivery_failed", "sort": "Bool", "values": [], "description": "", "event": True},
                    {"name": "order_returned", "sort": "Bool", "values": [], "description": ""}],
        "background": [],
        "rules": [{"id": "D5", "text": "WHEN a delivery fails for the second time THEN return the order.",
                   "status": "accepted", "reading": "",
                   "antecedent": "(and delivery_failed (= failed_deliveries 2))", "consequent": "order_returned"}],
    }
    count_alone = {"reading": "", "antecedent": "(= failed_deliveries 2)", "consequent": "order_returned"}
    second_reading(FakeSecond([count_alone] * 8), formal)
    assert formal["rules"][0]["second"]["confirms"] is True
    assert ambiguities(analyze(formal)) == []


def test_a_second_model_without_usable_answers_says_nothing():
    formal = formal_three_reports()
    second_reading(FakeSecond([BROKEN] * 8), formal)
    assert formal["rules"][0]["second"] == {"support": "0/8", "confirms": False}
    assert ambiguities(analyze(formal)) == []  # no other reading to ask about
