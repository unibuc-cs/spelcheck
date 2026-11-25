"""Tests for change.py: merging an OpenSpec change, and which findings belong to it. No LLM.

The formal models are saved ones or written by hand, as in test_checks.py.
"""

import json
from pathlib import Path

import pytest

from speccheck.change import about_change, after_model, changed_rules, merge
from speccheck.checks import analyze
from speccheck.explain import evidence

ROOT = Path(__file__).parent.parent
AUTH = ROOT / "specs" / "auth_change" / "openspec" / "changes" / "admin-never-locked"

SPEC = """# shop Specification

## Purpose

A small shop.

## Requirements

### Requirement: Checkout

The system SHALL take payments.

#### Scenario: Card accepted

- **WHEN** a customer pays
- **AND** the card is accepted
- **THEN** the system confirms the order

#### Scenario: Card refused

- **WHEN** a customer pays
- **AND** the card is not accepted
- **THEN** the system asks for another card

### Requirement: Newsletter

The system SHALL send a newsletter.

#### Scenario: Monday

- **WHEN** a week begins
- **THEN** the system sends the newsletter

### Requirement: Returns

The system SHALL take goods back.

#### Scenario: Goods returned

- **WHEN** a customer returns goods
- **THEN** the system refunds the price
"""


def project(folder: Path, deltas: dict) -> Path:
    """Write an OpenSpec project with the shop spec and one change; return the change folder.

    deltas  capability -> the text of its delta file
    """
    spec = folder / "openspec" / "specs" / "shop" / "spec.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    change = folder / "openspec" / "changes" / "c1"
    for capability, text in deltas.items():
        delta = change / "specs" / capability / "spec.md"
        delta.parent.mkdir(parents=True)
        delta.write_text(text, encoding="utf-8")
    return change


def states(merged) -> dict:
    """Label -> (requirement, scenario, status), in document order."""
    return {label: (s["requirement"], s["scenario"], s["status"]) for label, s in merged.scenarios.items()}


def test_every_scenario_gets_a_label_and_the_added_one_is_marked():
    """The login example: four scenarios exist, the change adds the fifth."""
    merged = merge(AUTH)

    assert list(merged.scenarios) == ["R1", "R2", "R3", "R4", "R5"]
    assert merged.scenarios["R3"] == {"capability": "auth", "requirement": "Account Lockout",
                                      "scenario": "Lockout threshold", "status": "existing"}
    assert merged.scenarios["R5"]["status"] == "added"
    # The label is in the document that the LLM reads, so that it comes back as the rule's id.
    assert "#### Scenario R5: Administrators are never locked out" in merged.text
    assert "- **THEN** the system does not lock the account" in merged.text


def test_the_four_kinds_of_delta_are_applied(tmp_path):
    """RENAMED, REMOVED, MODIFIED and ADDED, matched by the requirement's name."""
    merged = merge(project(tmp_path, {"shop": """## RENAMED Requirements

- FROM: `### Requirement: Newsletter`
- TO: `### Requirement: Weekly mail`

## REMOVED Requirements

### Requirement: Returns

**Reason**: Returns go through the supplier now.

## MODIFIED Requirements

### Requirement: Checkout

The system SHALL take payments by card.

#### Scenario: Card accepted

- **WHEN** a customer pays
- **AND** the card is accepted
- **THEN** the system confirms the order

## ADDED Requirements

### Requirement: Gift cards

The system SHALL sell gift cards.

#### Scenario: Gift card bought

- **WHEN** a customer buys a gift card
- **THEN** the system sends the code by email
"""}))

    assert states(merged) == {
        "R1": ("Checkout", "Card accepted", "existing"),    # the same words as before
        "X1": ("Checkout", "Card refused", "removed"),      # the new text has no such scenario
        "R2": ("Weekly mail", "Monday", "existing"),        # renamed only
        "X2": ("Returns", "Goods returned", "removed"),     # its requirement is removed
        "R3": ("Gift cards", "Gift card bought", "added"),
    }
    assert merged.removed == ["shop/Returns"]
    # What the change removes stays in the document, under its own labels.
    assert "#### Scenario X1: Card refused" in merged.text
    assert "#### Scenario X2: Goods returned" in merged.text
    # The sentences that are new, and the one that is gone.
    assert merged.changed_text == ["the system shall take payments by card.",
                                   "the system shall sell gift cards."]
    assert merged.removed_text == ["the system shall take goods back."]


def test_inside_a_rewritten_requirement_only_the_scenario_with_new_words_is_modified(tmp_path):
    merged = merge(project(tmp_path, {"shop": """## MODIFIED Requirements

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
"""}))

    assert states(merged)["R1"] == ("Checkout", "Card accepted", "existing")
    assert states(merged)["R2"] == ("Checkout", "Card refused", "modified")
    assert merged.changed_text == []  # the sentence of the requirement is the same


def test_a_new_capability_gets_a_spec_of_its_own(tmp_path):
    merged = merge(project(tmp_path, {"loyalty": """## Purpose

Points for regular customers.

## ADDED Requirements

### Requirement: Points

The system SHALL give points.

#### Scenario: Purchase

- **WHEN** a customer pays
- **THEN** the system adds points to the customer's account
"""}))

    assert merged.scenarios["R5"] == {"capability": "loyalty", "requirement": "Points",
                                      "scenario": "Purchase", "status": "added"}
    assert "# loyalty Specification" in merged.text and "Points for regular customers." in merged.text


@pytest.mark.parametrize("delta", [
    "## MODIFIED Requirements\n\n### Requirement: Shipping\n\nThe system SHALL ship.\n",
    "## REMOVED Requirements\n\n### Requirement: Shipping\n",
    "## ADDED Requirements\n\n### Requirement: Checkout\n\nThe system SHALL take payments.\n",
])
def test_a_delta_that_does_not_fit_the_spec_is_refused(tmp_path, delta):
    """Modifying or removing what is not there, or adding what is: `openspec archive` refuses these too."""
    with pytest.raises(ValueError, match="Requirement|requirement"):
        merge(project(tmp_path, {"shop": delta}))


def test_only_the_findings_that_involve_the_change_are_selected():
    """The login example, with the saved formal model of the same five scenarios.

    R3 (lock at 5 failed attempts) against the added R5 (never lock an
    administrator) is the change's conflict. R1 against R4 was there before.
    """
    merged = merge(AUTH)
    model = json.loads((ROOT / "specs" / "auth_openspec" / "formal.json").read_text(encoding="utf-8"))
    changed = [changed_rules(model, merged)]
    assert changed == [{"R5"}]
    assert after_model(model, merged) is model  # the change removes nothing

    selected = [finding for finding in analyze(model) if about_change(finding, [model], changed)]
    assert [(finding["type"], finding["rules"]) for finding in selected] == [("conflict", ["R3", "R5"])]


def test_rules_without_a_label():
    """The read step may turn a requirement's SHALL sentence into a rule of its own."""
    merged = merge(AUTH)
    model = json.loads((ROOT / "specs" / "auth_openspec" / "formal.json").read_text(encoding="utf-8"))
    extra = {"antecedent": "true", "consequent": "true"}
    model["rules"] += [
        # the sentence of the added requirement: part of the change
        {**extra, "id": "X1", "text": "Administrators MUST always be able to reach the system."},
        # the sentence of a requirement that existed before: not part of it
        {**extra, "id": "X2", "text": "The system SHALL authenticate users by password."},
    ]
    assert changed_rules(model, merged) == {"R5", "X1"}

    # A label that did not come back: we cannot tell which rules are the change's.
    model["rules"] = [rule for rule in model["rules"] if rule["id"] != "R5"]
    with pytest.raises(ValueError, match="R5"):
        changed_rules(model, merged)


def test_a_gap_belongs_to_the_change_when_a_changed_rule_reacts_to_its_event():
    """Two events with one case each left open; only one of the two rules is the change's."""
    model = {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": "", "event": event}
                    for name, event in (("guest_arrives", True), ("host_present", False),
                                        ("parcel_arrives", True), ("member_present", False),
                                        ("pass_printed", False), ("parcel_handed_over", False))],
        "rules": [
            {"id": "R1", "trigger": "parcel_arrives",
             "antecedent": "(and parcel_arrives member_present)", "consequent": "parcel_handed_over"},
            {"id": "R2", "trigger": "guest_arrives",
             "antecedent": "(and guest_arrives host_present)", "consequent": "pass_printed"},
        ],
    }
    gaps = {finding.get("event", "none"): finding for finding in analyze(model) if finding["type"] == "gap"}
    assert set(gaps) == {"parcel_arrives", "guest_arrives", "none"}

    changed = [{"R2"}]
    assert about_change(gaps["guest_arrives"], [model], changed)
    assert not about_change(gaps["parcel_arrives"], [model], changed)
    assert not about_change(gaps["none"], [model], changed)  # no event happens: nobody's gap


# ------------------------------------------------------------ what a change removes


def visitors(removed: list[dict]) -> dict:
    """A formal model as the LLM makes it for a merged document: the rules X... are removed ones.

    R1 lets a listed visitor in. X1 (calls a nurse for an unlisted visitor) and
    X2 (the only rule for a tour request) are rules that a change may remove.
    """
    names = (("visitor_checks_in", True), ("tour_requested", True), ("visitor_on_list", False),
             ("door_opened", False), ("nurse_called", False), ("date_proposed", False))
    return {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": event}
                    for name, event in names],
        "background": [
            {"id": "F1", "text": "a voted fact", "formula": "(not (and door_opened nurse_called))"},
            {"id": "F2", "text": "a link of X1", "formula": "(=> nurse_called (not door_opened))", "restates": "X1"},
            {"id": "F3", "text": "a fact about two outcomes", "formula": "(not (and door_opened nurse_called))",
             "between": ["R1", "X1"]},
        ],
        "rules": [{"id": "R1", "status": "accepted", "trigger": "visitor_checks_in", "text": "listed visitor",
                   "antecedent": "(and visitor_checks_in visitor_on_list)", "consequent": "door_opened"}] + removed,
    }


UNLISTED = {"id": "X1", "status": "accepted", "trigger": "visitor_checks_in", "text": "unlisted visitor",
            "antecedent": "(and visitor_checks_in (not visitor_on_list))", "consequent": "nurse_called"}
TOUR = {"id": "X2", "status": "accepted", "trigger": "tour_requested", "text": "tour request",
        "antecedent": "tour_requested", "consequent": "date_proposed"}


class Removes:
    """Stands in for a Merged in which X1 and X2 are removed scenarios."""
    scenarios = {"R1": {"status": "existing"}, "X1": {"status": "removed"}, "X2": {"status": "removed"}}
    changed_text, removed_text = [], []


def test_removed_rules_leave_the_model_and_take_what_came_from_them():
    after = after_model(visitors([UNLISTED, TOUR]), Removes)

    assert [rule["id"] for rule in after["rules"]] == ["R1"]
    assert [rule["id"] for rule in after["removed_rules"]] == ["X1", "X2"]
    # The voted fact stays; the link of X1 and the fact about R1 and X1 go.
    assert [fact["id"] for fact in after["background"]] == ["F1"]


def test_a_gap_that_a_removed_rule_covered_is_the_changes():
    """Both cases of "a visitor checks in" were covered; the change removes the rule for one of them."""
    after = after_model(visitors([UNLISTED, TOUR]), Removes)
    gaps = [finding for finding in analyze(after) if finding["type"] == "gap"]

    opened = next(gap for gap in gaps if gap.get("event") == "visitor_checks_in")
    assert opened["opened_by"] == ["X1"]
    assert opened["when"] == {"visitor_checks_in": True, "visitor_on_list": False}
    assert about_change(opened, [after], [set()])  # no rule was added or modified
    assert "the change removes it:\n- X1: unlisted visitor" in evidence(opened, after)
    # Nothing reacts to a tour request any more: that is a decision, not a gap.
    assert "tour_requested" not in {gap.get("event") for gap in gaps}


def test_a_removed_rule_that_names_two_events_is_asked_about_in_its_own_situation():
    """The model may read "the payment is refused" as an event of its own.

    The removed rule then needs two events at once. The usual gap search lets
    one event happen at a time, so it never reaches the situation that this
    rule covered; the search for a lost rule takes all of that rule's events.
    """
    model = {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": "", "event": event}
                    for name, event in (("buys_credit", True), ("payment_accepted", True),
                                        ("payment_refused", True), ("credit_added", False),
                                        ("error_shown", False))],
        "rules": [{"id": "R1", "status": "accepted", "trigger": "payment_accepted", "text": "",
                   "antecedent": "(and buys_credit payment_accepted)", "consequent": "credit_added"}],
        "removed_rules": [{"id": "X1", "status": "accepted", "trigger": "payment_refused", "text": "",
                           "antecedent": "(and buys_credit payment_refused)", "consequent": "error_shown"}],
    }
    opened = [f for f in analyze(model) if f.get("opened_by")]
    assert [(f["event"], f["opened_by"]) for f in opened] == [("buys_credit", ["X1"])]
    assert opened[0]["when"] == {"buys_credit": True, "payment_accepted": False, "payment_refused": True}


def test_the_same_gap_without_a_removed_rule_is_nobodys():
    """The spec never had a rule for the unlisted visitor: the gap is old."""
    model = visitors([])
    gap = next(f for f in analyze(model) if f["type"] == "gap" and f.get("event") == "visitor_checks_in")
    assert "opened_by" not in gap
    assert not about_change(gap, [model], [set()])


def test_headers_in_a_code_block_are_text(tmp_path: Path):
    """A spec that shows its own format in a code block does not get a requirement or a scenario from it."""
    change = project(tmp_path, {"shop": """## ADDED Requirements

### Requirement: Format

The system SHALL accept scenarios written like this:

```
### Requirement: Example
#### Scenario: Short name
- **WHEN** ...
- **THEN** ...
```

#### Scenario: Well-formed file

- **WHEN** a file follows the format
- **THEN** the system accepts the file
"""})
    merged = merge(change)
    added = [(s["requirement"], s["scenario"]) for s in merged.scenarios.values() if s["status"] == "added"]
    assert added == [("Format", "Well-formed file")]
    assert "#### Scenario: Short name" in merged.text      # still there, as text
