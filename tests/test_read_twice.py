"""Tests for a rule that the read step returns twice, once for each event it reacts to (formalize._once).
No LLM, no GPU.
"""

import pytest

from speccheck.change import Merged, changed_rules
from speccheck.formalize import _once, _read

TWO_CALLS = "WHEN a call of ask_chef or hire_waiters is made THEN the agent making it is the order agent"


def rule(label: str, text: str, trigger: str = "") -> dict:
    return {"id": label, "text": text, "trigger": trigger}


def test_an_answer_without_such_a_rule_comes_back_as_it_is():
    rules = [rule("R1", "WHEN a call of confirm_order succeeds THEN ...", "confirm_order_succeeded"),
             rule("R2", TWO_CALLS, "ask_chef_called"), rule("R3", "WHILE the kitchen is closed ...")]
    assert _once(rules) == rules


def test_a_rule_that_came_back_once_for_each_of_its_events_is_one_rule():
    rules = [rule("R1", "WHEN a call of confirm_order succeeds THEN ...", "confirm_order_succeeded"),
             rule("R2", TWO_CALLS, "ask_chef_called"), rule("R2", TWO_CALLS, "hire_waiters_called"),
             rule("R3", "WHILE the kitchen is closed ...")]
    once = _once(rules)
    assert [r["id"] for r in once] == ["R1", "R2", "R3"]
    assert once[1] == rule("R2", TWO_CALLS, "")            # it reacts to no single event
    assert rules[1]["trigger"] == "ask_chef_called"        # the answer that was given is not touched


def test_three_copies_and_a_line_break_in_one_of_them():
    three = "WHEN a call of book_room, swap_room or release_room is made THEN the date is in term time"
    rules = [rule("R3", three, "book_room_called"), rule("R3", three.replace(" THEN", "\nTHEN"), "swap_room_called"),
             rule("R3", three, "release_room_called")]
    assert _once(rules) == [rule("R3", three, "")]


def test_copies_with_one_trigger_keep_it():
    rules = [rule("R2", TWO_CALLS, "tool_called"), rule("R2", TWO_CALLS, "tool_called")]
    assert _once(rules) == [rule("R2", TWO_CALLS, "tool_called")]


def test_two_rules_with_one_label_and_other_words_stay_two():
    rules = [rule("R2", "WHEN a call of ask_chef is made THEN ...", "ask_chef_called"),
             rule("R2", "WHEN a call of hire_waiters is made THEN ...", "hire_waiters_called")]
    assert _once(rules) == rules
    scenarios = {"R1": {"status": "existing"}, "R2": {"status": "existing"}}
    with pytest.raises(ValueError, match="did not keep the scenario labels R2"):
        changed_rules({"rules": [rule("R1", "...")] + rules}, Merged("a-change", "", scenarios, [], []))


def test_the_read_step_gives_the_change_check_each_label_once():
    def symbol(name: str) -> dict:
        return {"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": name.endswith("_called")}

    class FakeLLM:
        def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
            return [{"rules": [rule("R1", "WHEN a call of confirm_order succeeds THEN ...", "confirm_order_succeeded"),
                               rule("R2", TWO_CALLS, "ask_chef_called"), rule("R2", TWO_CALLS, "hire_waiters_called"),
                               rule("R3", "WHEN a call of hire_waiters is made in a pick-up run THEN ...", "hire_waiters_called")],
                     "symbols": [symbol("confirm_order_succeeded"), symbol("ask_chef_called"), symbol("hire_waiters_called"),
                                 symbol("agent_is_order_agent")]}]

    rules, _ = _read(FakeLLM(), "the document", 0.0)
    assert [(r["id"], r["trigger"]) for r in rules] == [("R1", "confirm_order_succeeded"), ("R2", ""),
                                                        ("R3", "hire_waiters_called")]
    scenarios = {"R1": {"status": "existing"}, "R2": {"status": "existing"}, "R3": {"status": "added"}}
    assert changed_rules({"rules": rules}, Merged("a-change", "", scenarios, [], [])) == {"R3"}
