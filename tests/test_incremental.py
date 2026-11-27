"""Tests for adding rules to a formal model that exists (formalize with `base`), and for
the labels that `speccheck --change --incremental` needs. No LLM, no GPU.

The LLM is replaced by a stand-in with fixed answers, so these tests check
which questions are asked and what is done with the answers.
"""

from pathlib import Path

from speccheck.change import after_model, base_document, changed_rules, merge
from speccheck.checks import analyze
from speccheck.formalize import (FACTS_SYSTEM, FORMALIZE_SYSTEM, READ_MORE, READ_SYSTEM, formalize)
from speccheck.probe import APPLIES_SYSTEM, CONDITIONS_SYSTEM, OUTCOMES_SYSTEM, READINGS_SYSTEM
from tests.test_change import project


def symbol(name: str, event: bool = False) -> dict:
    return {"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": event}


def base() -> dict:
    """The formal model of a spec with one rule: "take the price when the card is tapped"."""
    return {
        "symbols": [symbol("card_tapped", event=True), symbol("payment_taken"), symbol("canteen_closed")],
        "background": [],
        "rules": [{"id": "R1", "text": "WHEN a card is tapped THEN the system takes the price", "trigger": "card_tapped",
                   "status": "accepted", "clusters": [8], "entropy": 0.0, "reading": "take the price",
                   "antecedent": "card_tapped", "consequent": "payment_taken", "probes": []}],
    }


class FakeLLM:
    """Stands in for llm.LLM.

    read          its answer to the read step
    translations  rule id -> its translation (given by every sample)
    """

    def __init__(self, read: dict, translations: dict):
        self.read, self.translations = read, translations
        self.calls = []  # (which prompt, the user message)

    def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
        if system.startswith(READ_SYSTEM):
            self.calls.append(("read with the symbols so far" if system.endswith(READ_MORE) else "read", user))
            return [self.read]
        if system.startswith(FORMALIZE_SYSTEM):
            rule_id = user.split("Requirement ")[1].split(":")[0]
            # Step 5 asks for a rule again, in the terms of the other rules (a longer prompt).
            self.calls.append(("translate" if system == FORMALIZE_SYSTEM else "restate", rule_id))
            return [self.translations[rule_id]] * samples
        if system == FACTS_SYSTEM:
            self.calls.append(("facts", user))
            return [{"facts": []}] * samples
        if system == READINGS_SYSTEM:
            self.calls.append(("readings", user.split("Requirement ")[1].split(":")[0]))
            return [{"readings": []}]
        if system == CONDITIONS_SYSTEM:  # check 5: can the conditions of two rules that clash both hold?
            self.calls.append(("conditions", user))
            return [{"reason": "", "answer": "possible", "fact": ""}] * samples
        if system == APPLIES_SYSTEM:  # check 6: does what one rule demands make another rule apply?
            self.calls.append(("applies", user))
            return [{"reason": "", "answer": "no", "fact": ""}] * samples
        assert system == OUTCOMES_SYSTEM
        self.calls.append(("outcomes", user))
        return [{"reason": "", "answer": "impossible", "fact": "A payment cannot be taken and refused."}] * samples

    def asked(self, what: str) -> list:
        return [detail for which, detail in self.calls if which == what]


NEW_TEXT = "#### Scenario N1: Holidays\n- **WHEN** the canteen is closed\n- **THEN** the system refuses all payments\n"


def test_new_rules_are_added_to_a_model_with_its_symbols():
    """Only the new rule goes through the steps, and it can clash with a rule of the base."""
    llm = FakeLLM(
        read={"rules": [{"id": "N1", "text": "WHEN the canteen is closed THEN the system refuses all payments",
                         "trigger": ""}],
              # One new symbol; the model also lists one that exists, which is not added twice.
              "symbols": [symbol("payment_refused"), symbol("canteen_closed")]},
        translations={"N1": {"reading": "refuse payments", "antecedent": "canteen_closed",
                             "consequent": "payment_refused"}})
    model = formalize(llm, NEW_TEXT, base=base())

    # The read step saw the symbols of the base before the document.
    [shown] = llm.asked("read with the symbols so far")
    assert shown.startswith("Symbols of the system so far:\n- card_tapped: Bool, event - about card_tapped")
    assert shown.endswith("Document:\n" + NEW_TEXT)
    assert [s["name"] for s in model["symbols"]] == ["card_tapped", "payment_taken", "canteen_closed",
                                                     "payment_refused"]
    assert [rule["id"] for rule in model["rules"]] == ["R1", "N1"]
    # Translations and other readings were asked for the new rule alone. Its outcome has a
    # symbol of its own, so step 5 also asked for it in the terms of the base's outcomes.
    assert llm.asked("translate") == ["N1"] and llm.asked("readings") == ["N1"]
    assert llm.asked("restate") == ["N1"]
    # One question about two outcomes: what R1 demands against what N1 demands.
    assert len(llm.asked("outcomes")) == 1
    assert model["background"] == [{
        "id": "F1", "between": ["R1", "N1"], "support": "8/8",
        "text": "What R1 and N1 demand cannot both be the case: A payment cannot be taken and refused.",
        "formula": "(not (and payment_taken payment_refused))"}]
    conflict = next(f for f in analyze(model) if f["type"] == "conflict")
    assert conflict["rules"] == ["R1", "N1"] and conflict["facts"] == ["F1"]
    # The two rules clash now, so the model was asked whether their conditions can hold
    # together ("a card is tapped", "the canteen is closed"). They can: nothing is added.
    assert len(llm.asked("conditions")) == 1
    assert model["condition_pairs"] == [{"rules": ["R1", "N1"], "answers": {"possible": 8, "impossible": 0, "unclear": 0}}]
    # And whether what one of them demands makes the other apply ("the price is taken": is the
    # canteen closed then?). It does not: nothing is added.
    assert [(pair["rules"], pair["part"]) for pair in model["apply_pairs"]] == [
        (["R1", "N1"], {"canteen_closed": True}), (["N1", "R1"], {"card_tapped": True})]
    assert len(llm.asked("applies")) == 2


def test_the_facts_are_asked_again_only_when_a_symbol_is_new():
    llm = FakeLLM(
        read={"rules": [{"id": "N1", "text": "WHEN the canteen is closed THEN the system takes no price",
                         "trigger": ""}], "symbols": []},
        translations={"N1": {"reading": "take nothing", "antecedent": "canteen_closed",
                             "consequent": "(not payment_taken)"}})
    model = formalize(llm, NEW_TEXT, base=base())

    assert llm.asked("facts") == []                    # the symbols of the base were enough
    assert len(model["symbols"]) == 3
    # The new rule uses the symbol of the old one, so Z3 sees the clash without any fact.
    assert [(f["rules"], f.get("facts")) for f in analyze(model) if f["type"] == "conflict"] == [(["R1", "N1"], None)]


def test_without_a_base_everything_is_as_before():
    llm = FakeLLM(
        read={"rules": base()["rules"][:1], "symbols": base()["symbols"]},
        translations={"R1": {"reading": "take the price", "antecedent": "card_tapped", "consequent": "payment_taken"}})
    model = formalize(llm, "R1: WHEN a card is tapped THEN the system takes the price")

    assert [which for which, _ in llm.calls][:1] == ["read"] and len(llm.asked("facts")) == 1
    assert [rule["id"] for rule in model["rules"]] == ["R1"] and model["outcome_pairs"] == []


# ------------------------------------------------- the labels of a change on a base

REWRITTEN = """## MODIFIED Requirements

### Requirement: Checkout

The system SHALL take payments.

#### Scenario: Card accepted

- **WHEN** a customer pays
- **AND** the card is accepted
- **THEN** the system confirms the order

#### Scenario: Card refused

- **WHEN** a customer pays
- **AND** the card is not accepted
- **THEN** the system asks for another card and records the attempt

## REMOVED Requirements

### Requirement: Returns

## ADDED Requirements

### Requirement: Gift cards

The system SHALL sell gift cards.

#### Scenario: Gift card bought

- **WHEN** a customer buys a gift card
- **THEN** the system sends the code by email
"""


def test_on_a_base_the_scenarios_that_stay_keep_their_labels(tmp_path: Path):
    change = project(tmp_path, {"shop": REWRITTEN})
    assert list(base_document(tmp_path / "openspec" / "specs").scenarios) == ["R1", "R2", "R3", "R4"]

    merged = merge(change, on_base=True)
    assert {label: (s["scenario"], s["status"]) for label, s in merged.scenarios.items()} == {
        "R1": ("Card accepted", "existing"),
        "R2": ("Card refused", "replaced"),      # its old rule, in the model of the base
        "N1": ("Card refused", "modified"),      # its new words
        "R3": ("Monday", "existing"),
        "R4": ("Goods returned", "removed"),
        "N2": ("Gift card bought", "added"),
    }
    # The document for the LLM has the new scenarios only, under their requirements.
    assert "#### Scenario N1: Card refused" in merged.text and "#### Scenario N2: Gift card bought" in merged.text
    assert "Card accepted" not in merged.text and "Goods returned" not in merged.text
    assert "### Requirement: Checkout" in merged.text and "# shop Specification" in merged.text


def test_a_replaced_rule_is_dropped_and_a_removed_one_is_kept_apart(tmp_path: Path):
    merged = merge(project(tmp_path, {"shop": REWRITTEN}), on_base=True)
    rule = {"status": "accepted", "trigger": "", "text": "", "antecedent": "true", "consequent": "true"}
    model = {"symbols": [], "background": [{"id": "F1", "formula": "true", "restates": "R2"}],
             "rules": [{**rule, "id": label} for label in ("R1", "R2", "R3", "R4", "N1", "N2")]}

    assert changed_rules(model, merged) == {"N1", "N2"}
    after = after_model(model, merged)
    assert [r["id"] for r in after["rules"]] == ["R1", "R3", "N1", "N2"]
    assert [r["id"] for r in after["removed_rules"]] == ["R4"]   # R2 was replaced, not removed
    assert after["background"] == []                              # the link of R2 went with it


def test_a_change_that_only_removes_has_nothing_new(tmp_path: Path):
    merged = merge(project(tmp_path, {"shop": "## REMOVED Requirements\n\n### Requirement: Returns\n"}),
                   on_base=True)
    assert merged.text == ""
    assert merged.scenarios["R4"]["status"] == "removed"


# ------------------------------------------------------------ the saved model of the specs


def test_the_model_of_the_specs_is_made_once_and_again_when_they_change(tmp_path: Path, capsys):
    """cli._base_model: saved next to the specs, reused, and made again for other specs or another model."""
    from speccheck.cli import _base_model

    project(tmp_path, {})
    openspec = tmp_path / "openspec"
    rule = {"reading": "", "antecedent": "customer_pays", "consequent": "order_confirmed"}
    llm = FakeLLM(read={"rules": [{"id": f"R{n}", "text": f"rule {n}", "trigger": ""} for n in range(1, 5)],
                        "symbols": [symbol("customer_pays", event=True), symbol("order_confirmed")]},
                  translations={f"R{n}": rule for n in range(1, 5)})
    llm.model = "model-a"

    first = _base_model(llm, openspec, samples=2, temperature=0.7)
    assert [r["id"] for r in first["rules"]] == ["R1", "R2", "R3", "R4"]
    assert (openspec / ".speccheck" / "base.json").exists()
    asked = len(llm.calls)

    # The same specs and the same model: nothing is asked.
    assert _base_model(llm, openspec, samples=2, temperature=0.7) == first
    assert len(llm.calls) == asked
    assert "using the saved model" in capsys.readouterr().err

    # Another model: made again.
    llm.model = "model-b"
    _base_model(llm, openspec, samples=2, temperature=0.7)
    assert len(llm.calls) == 2 * asked

    # The specs were edited: made again.
    spec = openspec / "specs" / "shop" / "spec.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace("refunds the price", "refunds the price in full"),
                    encoding="utf-8")
    _base_model(llm, openspec, samples=2, temperature=0.7)
    assert len(llm.calls) == 3 * asked
