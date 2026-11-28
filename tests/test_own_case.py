"""Tests for step 53: an example contradicts a rule only in its own case. No LLM, no GPU.

A conflict with an example counts as it is only if the example's own case
makes the other rules apply (step 45) and cannot be when those rules are
obeyed (step 53).
"""

from speccheck.change import with_examples
from speccheck.checks import analyze, is_doubtful
from speccheck.explain import evidence


def model(rules: list[dict], examples: tuple, facts: tuple = ()) -> dict:
    """A formal model about parcels and a whole run; the rules named in `examples` are examples."""
    names = ("ship_called", "ship_succeeded", "ship_refused", "asks_lost_parcel", "asks_held_parcel", "record_written")
    formal = {"situation": "run",
              "symbols": [{"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": False}
                          for name in names],
              "background": [{"id": f"F{n}", "text": "", "formula": fact} for n, fact in enumerate(facts, start=1)],
              "rules": [{"status": "accepted", "text": "", **rule} for rule in rules]}

    class Merged:  # as change.Merged: only the scenarios are looked at
        scenarios = {rule["id"]: {"example": True} for rule in rules if rule["id"] in examples}

    return with_examples(formal, Merged)


def conflicts(findings):
    return [f for f in findings if f["type"] == "conflict"]


# "WHEN any call of ship_parcel is made THEN it never succeeds for a parcel that is on hold", with the
# restriction lost in translation; "WHEN a call of ship_parcel succeeds THEN one record is written".
NEVER = {"id": "R6", "antecedent": "ship_called", "consequent": "(not ship_succeeded)"}
RECORD = {"id": "R7", "antecedent": "ship_succeeded", "consequent": "record_written"}
# "WHEN dana asks to ship parcel k9, which the depot cannot find THEN ship_parcel is refused".
REFUSED = {"id": "R11", "antecedent": "asks_lost_parcel", "consequent": "ship_refused"}
# Check 6: where R11 is obeyed, ship_parcel was called.
CALLED = "(=> (and asks_lost_parcel ship_refused) ship_called)"


def test_an_example_that_can_be_obeyed_with_the_rule_in_its_own_case_does_not_describe_the_conflict():
    formal = model([NEVER, RECORD, REFUSED], examples=("R11",), facts=(CALLED,))
    (conflict,) = conflicts(analyze(formal))
    # Found in a run in which ship_parcel succeeded: the condition of R7, and nothing R11 says.
    assert conflict["rules"] == ["R6", "R11"] and conflict["facts"] == ["F1"]
    assert conflict["beyond_example"] == ["R11"] and is_doubtful(conflict)
    assert "or can be the case with them obeyed" in evidence(conflict, formal)
    # As it was before step 53: the example's case makes R6 apply, and that was enough.
    (conflict,) = conflicts(analyze(formal, own_case=False))
    assert not is_doubtful(conflict)
    # Read as a rule for all cases, R11 clashes with R6 wherever a call succeeds.
    (conflict,) = conflicts(analyze(model([NEVER, RECORD, REFUSED], examples=(), facts=(CALLED,))))
    assert not is_doubtful(conflict)


def test_an_example_that_breaks_the_rule_by_what_it_demands_itself_is_a_conflict():
    # "WHEN dana sends a rush request for parcel k4, which is on hold THEN ship_parcel succeeds once".
    succeeds = {"id": "R12", "antecedent": "asks_held_parcel", "consequent": "ship_succeeded"}
    called = "(=> (and asks_held_parcel ship_succeeded) ship_called)"
    (conflict,) = conflicts(analyze(model([NEVER, RECORD, succeeds], examples=("R12",), facts=(called,))))
    assert conflict["rules"] == ["R6", "R12"] and not is_doubtful(conflict)
