"""Tests for the second read: rules that lack a symbol for what they demand are read again,
alone, and translated again with the symbols that this adds (formalize._read_again).
No LLM, no GPU: the LLM is a stand-in with fixed answers.
"""

from speccheck.formalize import FACTS_SYSTEM, FORMALIZE_SYSTEM, READ_AGAIN, READ_SYSTEM, formalize
from speccheck.probe import OUTCOMES_SYSTEM, READINGS_SYSTEM

ALARM = "WHEN the door opens THEN the alarm sounds"
LIGHT = "WHEN the door opens THEN the hall light is switched on"


def symbol(name: str, event: bool = False) -> dict:
    return {"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": event}


FIRST_READ = {"rules": [{"id": "R1", "text": ALARM, "trigger": "door_opened"},
                        {"id": "R2", "text": LIGHT, "trigger": "door_opened"}],
              # No symbol for the hall light.
              "symbols": [symbol("door_opened", event=True), symbol("alarm_sounds")]}
# The second read spells its symbol as the document does; the name is repaired.
SECOND_READ = {"rules": [{"id": "R2", "text": LIGHT, "trigger": ""}], "symbols": [symbol("hall light on")]}


def translation(consequent: str) -> dict:
    return {"reading": "", "antecedent": "door_opened", "consequent": consequent}


class FakeLLM:
    """Stands in for llm.LLM.

    second_read  its answers to the second read, one for each try (an empty list: no valid JSON)
    light        the eight translations of R2 once the list has a symbol for the light
    """

    def __init__(self, second_read: list, light: list | None = None):
        self.second_read, self.light = list(second_read), light or [translation("hall_light_on")] * 8
        self.calls = []  # (which prompt, the user message)

    def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
        if system.startswith(READ_SYSTEM):
            if not system.endswith(READ_AGAIN):
                self.calls.append(("read", user))
                return [FIRST_READ]
            self.calls.append(("read again", user))
            return self.second_read.pop(0) if self.second_read else []
        if system.startswith(FORMALIZE_SYSTEM):
            rule_id = user.split("Requirement ")[1].split(":")[0]
            self.calls.append(("translate" if system == FORMALIZE_SYSTEM else "restate", rule_id))
            if rule_id == "R1":
                return [translation("alarm_sounds")] * samples
            # Without a symbol for the light, the model writes that R2 demands nothing.
            return self.light if "hall_light_on" in user else [translation("true")] * samples
        if system == FACTS_SYSTEM:
            self.calls.append(("facts", user))
            return [{"facts": []}] * samples
        if system == READINGS_SYSTEM:
            return [{"readings": []}]
        assert system == OUTCOMES_SYSTEM
        return [{"reason": "", "answer": "possible", "fact": ""}] * samples

    def asked(self, what: str) -> list:
        return [detail for which, detail in self.calls if which == what]


def rule(formal: dict, rule_id: str) -> dict:
    return next(r for r in formal["rules"] if r["id"] == rule_id)


def test_a_rule_without_a_symbol_is_read_again_and_translated_again():
    llm = FakeLLM(second_read=[[SECOND_READ]])
    formal = formalize(llm, "the document", keep_samples=True)

    # One second read: it is shown the symbols so far and the one rule that lacks a symbol.
    (again,) = llm.asked("read again")
    assert "- alarm_sounds: Bool" in again and LIGHT in again and ALARM not in again
    assert formal["reread"] == {"rules": ["R2"], "symbols": ["hall_light_on"]}
    assert [s["name"] for s in formal["symbols"]] == ["door_opened", "alarm_sounds", "hall_light_on"]

    # R2 was translated a second time, with the longer list, and is accepted with that translation.
    assert llm.asked("translate") == ["R1", "R2", "R2"]
    light = rule(formal, "R2")
    assert (light["status"], light["consequent"], light["reread"]) == ("accepted", "hall_light_on", True)
    assert "empty" not in light and light["trigger"] == "door_opened"
    assert light["samples"][0]["consequent"] == "hall_light_on" and light["first_samples"][0]["consequent"] == "true"
    assert "reread" not in rule(formal, "R1")

    # The facts are asked for again, with the list that has the new symbol.
    assert ["hall_light_on" in user for user in llm.asked("facts")] == [False, True]


def test_rules_that_have_their_symbols_are_not_read_again():
    llm = FakeLLM(second_read=[])
    FIRST_READ["symbols"].append(symbol("hall_light_on"))
    try:
        formal = formalize(llm, "the document")
    finally:
        FIRST_READ["symbols"].pop()
    assert llm.asked("read again") == [] and "reread" not in formal
    assert llm.asked("translate") == ["R1", "R2"] and len(llm.asked("facts")) == 1
    assert rule(formal, "R2")["status"] == "accepted"


def test_a_second_read_that_adds_no_symbol_changes_nothing():
    llm = FakeLLM(second_read=[[{"rules": [], "symbols": []}]])
    formal = formalize(llm, "the document")
    assert formal["reread"] == {"rules": ["R2"], "symbols": []}
    assert llm.asked("translate") == ["R1", "R2"] and len(llm.asked("facts")) == 1
    light = rule(formal, "R2")
    assert (light["status"], light["empty"], light["demand_nothing"]) == ("rejected", True, 8)


def test_a_new_translation_is_taken_only_if_it_is_accepted():
    # With the new symbol the eight answers split four to four, over the same symbols: two readings.
    split = [translation("hall_light_on")] * 4 + [translation("(not hall_light_on)")] * 4
    llm = FakeLLM(second_read=[[SECOND_READ]], light=split)
    formal = formalize(llm, "the document", keep_samples=True)
    light = rule(formal, "R2")
    # The rule stays as the first round left it, and the new answers are kept for the record.
    assert (light["status"], light["empty"], light["consequent"]) == ("rejected", True, "true")
    assert "reread" not in light and len(light["reread_samples"]) == 8 and light["samples"][0]["consequent"] == "true"
    # No translation that was taken uses the new symbol, so it does not stay,
    # and the facts are not asked for again: the run is as it was.
    assert formal["reread"] == {"rules": ["R2"], "symbols": []}
    assert [s["name"] for s in formal["symbols"]] == ["door_opened", "alarm_sounds"]
    assert len(llm.asked("facts")) == 1


def test_a_second_read_that_cannot_be_used_does_not_stop_the_run():
    llm = FakeLLM(second_read=[])  # no valid JSON, three times
    formal = formalize(llm, "the document")
    assert len(llm.asked("read again")) == 3
    assert formal["reread"] == {"rules": ["R2"], "symbols": []}
    assert rule(formal, "R1")["status"] == "accepted" and rule(formal, "R2")["status"] == "rejected"
