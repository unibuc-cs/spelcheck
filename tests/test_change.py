"""Tests for change.py: merging an OpenSpec change, and which findings belong to it. No LLM.

The formal models are saved ones or written by hand, as in test_checks.py.
"""

import json
from pathlib import Path

import pytest

from speccheck.change import about_change, changed_rules, merge
from speccheck.checks import analyze

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

    assert [(s["requirement"], s["scenario"], s["status"]) for s in merged.scenarios.values()] == [
        ("Checkout", "Card accepted", "modified"),   # every scenario of a modified requirement
        ("Weekly mail", "Monday", "existing"),       # renamed only: its text did not change
        ("Gift cards", "Gift card bought", "added"),
    ]
    assert merged.removed == ["shop/Returns"]
    assert "Card refused" not in merged.text and "Goods returned" not in merged.text
    assert merged.changed_text == ["the system shall take payments by card.",
                                   "the system shall sell gift cards."]


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
