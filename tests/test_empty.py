"""Tests for a rule whose translation demands nothing (formalize._judge and how it is reported).
No LLM, no GPU.
"""

from speccheck.checks import find_ambiguities
from speccheck.explain import evidence, render
from speccheck.formalize import _judge
from speccheck.logic import Vocabulary


# --------------------------------------------------- a rule that demands nothing


SYMBOLS = [{"name": "templates_command_run", "sort": "Bool", "values": [], "description": "the templates command is run", "event": True},
           {"name": "paths_displayed", "sort": "Bool", "values": [], "description": "the template paths are displayed", "event": False}]


def answers(consequent: str, count: int = 8) -> list[dict]:
    return [{"reading": "When the templates command is run, the system must display the template paths.",
             "antecedent": "templates_command_run", "consequent": consequent}] * count


def test_a_translation_that_demands_nothing_is_rejected_although_all_agree():
    vocab = Vocabulary(SYMBOLS)
    judged = _judge(vocab, answers("true"))
    assert judged["clusters"] == [8] and judged["status"] == "rejected" and judged["empty"] is True
    # Also when it is written less plainly.
    assert _judge(vocab, answers("(or paths_displayed (not paths_displayed))"))["status"] == "rejected"
    # A translation that demands something is judged as before.
    usual = _judge(vocab, answers("paths_displayed"))
    assert usual["status"] == "accepted" and "empty" not in usual


def test_it_is_reported_as_not_checked_and_not_as_an_ambiguity():
    vocab = Vocabulary(SYMBOLS)
    rule = {"id": "R1", "text": "WHEN user runs templates THEN the system displays template paths", "trigger": "",
            **_judge(vocab, answers("true"))}
    model = {"symbols": SYMBOLS, "background": [], "rules": [rule]}
    [finding] = find_ambiguities(model["rules"])
    assert finding["type"] == "ambiguity" and finding["status"] == "rejected" and finding["found_by"] == "empty"

    sheet = evidence(finding, model)
    assert sheet.startswith("Requirement R1 could not be written in logic")
    assert "templates_command_run => true" in sheet and "left out of the conflict and gap checks" in sheet
    report = render([finding], [model], "templates")
    assert "0 ambiguity(ies), 1 requirement(s) not checked" in report
    assert "## 1. Not checked" in report and "Ambiguity" not in report
