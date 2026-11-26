"""Tests for the formal layer (logic.py + checks.py). No LLM, no GPU.

The formalizations here are written by hand, so these tests check the solver
logic alone: given a correct formal.json, are the right findings produced?
The vote on sampled domain facts (formalize.py) is tested the same way, with
hand-written "LLM answers".
"""

import json
from pathlib import Path

import pytest

from speccheck.checks import _families, analyze, combine, find_gaps, find_scenarios
from speccheck.formalize import _agreed_facts, _links, _symbols_to_hide
from speccheck.logic import Vocabulary


def test_order_spec_reproduces_the_kiro_findings():
    """The order example must give exactly the three findings of the Kiro blog."""
    formal = json.loads((Path(__file__).parent / "order_formal.json").read_text())

    assert analyze(formal) == [
        # R2 demands a backorder, R3 forbids all backorders.
        {"type": "conflict", "rules": ["R2", "R3"],
         "when": {"order_submitted": True, "inventory_available": False}},
        # Resubmitting a canceled-and-refunded order: R1 says fulfill, R5 says do not.
        {"type": "conflict", "rules": ["R1", "R5"],
         "when": {"order_submitted": True, "inventory_available": True,
                  "canceled_and_refunded": True}},
        # Nothing happens and the order is not canceled-and-refunded: no rule fires.
        # inventory_available is absent because its value does not matter here.
        {"type": "gap",
         "when": {"order_submitted": False, "order_canceled": False,
                  "canceled_and_refunded": False}},
    ]


def test_numbers_and_enums_work_too():
    """A different domain, using Int and Enum symbols and a pairwise conflict."""
    formal = {
        "symbols": [
            {"name": "temperature", "sort": "Int", "values": [], "description": "room temperature in C"},
            {"name": "window_open", "sort": "Bool", "values": [], "description": "a window is open"},
            {"name": "mode", "sort": "Enum", "values": ["off", "cooling"], "description": "what the unit does"},
        ],
        "rules": [
            {"id": "T1", "antecedent": "(> temperature 30)", "consequent": "(= mode cooling)"},
            {"id": "T2", "antecedent": "window_open", "consequent": "(= mode off)"},
        ],
    }
    findings = analyze(formal)
    conflicts = [f for f in findings if f["type"] == "conflict"]
    gaps = [f for f in findings if f["type"] == "gap"]

    # Neither rule is wrong alone; they clash only when both fire (hot + window open).
    assert [c["rules"] for c in conflicts] == [["T1", "T2"]]
    assert conflicts[0]["when"]["window_open"] is True
    assert conflicts[0]["when"]["temperature"] > 30
    # Cool room, window closed: nothing is specified.
    assert gaps and gaps[0]["when"]["window_open"] is False
    assert gaps[0]["when"]["temperature"] <= 30


def test_a_forbidden_situation_is_not_a_conflict():
    """`locked` is a condition in A1 and a demand in A2/A3.

    Forcing "locked and admin" contradicts A3 alone: that is a situation the
    spec forbids, not a clash between rules, and it must not be reported. It
    must also not hide the real clash between A2 and A3.
    """
    formal = {
        "symbols": [
            {"name": "locked", "sort": "Bool", "values": [], "description": ""},
            {"name": "admin", "sort": "Bool", "values": [], "description": ""},
            {"name": "failures", "sort": "Int", "values": [], "description": ""},
            {"name": "access", "sort": "Bool", "values": [], "description": ""},
        ],
        "rules": [
            {"id": "A1", "antecedent": "locked", "consequent": "(not access)"},
            {"id": "A2", "antecedent": "(>= failures 5)", "consequent": "locked"},
            {"id": "A3", "antecedent": "admin", "consequent": "(not locked)"},
        ],
    }
    conflicts = [f for f in analyze(formal) if f["type"] == "conflict"]
    assert [c["rules"] for c in conflicts] == [["A2", "A3"]]


def test_a_consistent_and_complete_spec_has_no_findings():
    formal = {
        "symbols": [
            {"name": "door_open", "sort": "Bool", "values": [], "description": ""},
            {"name": "light_on", "sort": "Bool", "values": [], "description": ""},
        ],
        "rules": [
            {"id": "L1", "antecedent": "door_open", "consequent": "light_on"},
            {"id": "L2", "antecedent": "(not door_open)", "consequent": "(not light_on)"},
        ],
    }
    assert analyze(formal) == []


def test_an_assumed_fact_reveals_a_clash_between_two_phrases():
    """Two rules demand opposite things in different words (two symbols).

    The rules alone do not clash. With the domain fact that links the two
    symbols they do, and the finding names the fact it depends on.
    """
    formal = {
        "symbols": [
            {"name": "deletion_confirmed", "sort": "Bool", "values": [], "description": ""},
            {"name": "record_removed", "sort": "Bool", "values": [], "description": ""},
            {"name": "record_retained", "sort": "Bool", "values": [], "description": ""},
        ],
        "background": [],
        "rules": [
            {"id": "D1", "antecedent": "deletion_confirmed", "consequent": "record_removed"},
            {"id": "D2", "antecedent": "true", "consequent": "record_retained"},
        ],
    }
    assert [f for f in analyze(formal) if f["type"] == "conflict"] == []

    formal["background"] = [
        {"id": "F1", "text": "A record that is removed is not retained.",
         "formula": "(not (and record_removed record_retained))"},
    ]
    assert [f for f in analyze(formal) if f["type"] == "conflict"] == [
        {"type": "conflict", "rules": ["D1", "D2"], "facts": ["F1"],
         "when": {"deletion_confirmed": True}},
    ]


def test_assumed_facts_never_remove_a_finding():
    """Facts may add findings but must leave the ones proven without them alone.

    These are the five facts the LLM proposed for the order spec in an earlier
    trial. The third is not a real domain truth. Used as hard truths they made
    the R1/R5 conflict disappear; now the findings must be exactly the same as
    without any fact.
    """
    formal = json.loads((Path(__file__).parent / "order_formal.json").read_text())
    without_facts = analyze(formal)

    formal["background"] = [
        {"id": "F1", "text": "", "formula": "(=> canceled_and_refunded order_canceled)"},
        {"id": "F2", "text": "", "formula": "(=> canceled_and_refunded payments_refunded)"},
        {"id": "F3", "text": "", "formula": "(not (and order_fulfilled order_canceled))"},
        {"id": "F4", "text": "", "formula": "(not (and order_fulfilled order_backordered))"},
        {"id": "F5", "text": "", "formula": "(not (and order_canceled order_backordered))"},
    ]
    assert analyze(formal) == without_facts


def test_one_rule_against_a_fact_is_not_a_conflict():
    """A single rule that contradicts an assumed fact is not reported.

    With one snapshot and no notion of time, "WHEN the door is open, close it"
    contradicts "a closed door is not open" by itself. That is an artefact of
    the model, not a defect of the spec.
    """
    formal = {
        "symbols": [
            {"name": "door_open", "sort": "Bool", "values": [], "description": ""},
            {"name": "door_closed", "sort": "Bool", "values": [], "description": ""},
        ],
        "background": [
            {"id": "F1", "text": "", "formula": "(not (and door_open door_closed))"},
        ],
        "rules": [
            {"id": "C1", "antecedent": "door_open", "consequent": "door_closed"},
        ],
    }
    assert [f for f in analyze(formal) if f["type"] == "conflict"] == []


def test_fact_vote_keeps_what_most_samples_agree_on():
    """The vote on sampled domain facts: majority by logic, not by wording."""
    vocab = Vocabulary([
        {"name": name, "sort": "Bool", "values": [], "description": ""}
        for name in ("open", "closed", "locked")
    ])

    def answer(*formulas):
        return {"facts": [{"text": formula, "formula": formula} for formula in formulas]}

    answers = [
        answer("(not (and open closed))", "(=> locked closed)"),
        answer("(=> open (not closed))",            # the first fact in other words
               "(or open (not open))",              # true by logic alone: dropped
               "(=> closed unknown_symbol)"),       # unusable: ignored
        answer("(= open (not closed))"),            # stronger: implies the first fact
        answer(),                                   # an answer without facts
    ]
    kept = _agreed_facts(vocab, answers, asked=4)

    # "open and closed exclude each other" follows from 3 of the 4 answers.
    # "locked implies closed" (1 of 4) and "open = not closed" (1 of 4) have no majority.
    assert kept == [{"id": "F1", "text": "(=> open (not closed))",
                     "formula": "(=> open (not closed))", "support": "3/4"}]


def test_fact_vote_repairs_missing_outer_parentheses():
    """">= count 0" is read as "(>= count 0)"; other slips are still dropped."""
    vocab = Vocabulary([{"name": "count", "sort": "Int", "values": [], "description": ""},
                        {"name": "open", "sort": "Bool", "values": [], "description": ""}])
    answers = [{"facts": [{"text": "never negative", "formula": formula}]}
               for formula in (">= count 0", ">= count 0", "(>= count 0)", "(!= count -1)")]

    assert _agreed_facts(vocab, answers, asked=4) == [
        {"id": "F1", "text": "never negative", "formula": "(>= count 0)", "support": "3/4"}]
    # Without the repair only one answer says it: no majority.
    assert _agreed_facts(vocab, answers, asked=4, repair=False) == []
    # A bare symbol is already a formula and is left as it is.
    assert _agreed_facts(vocab, [{"facts": [{"text": "t", "formula": "open"}]}] * 2, asked=2) == [
        {"id": "F1", "text": "t", "formula": "open", "support": "2/2"}]


def test_bad_symbols_are_rejected():
    """Symbol lists that would silently distort the analysis must be refused."""
    def symbol(name, sort, values=()):
        return {"name": name, "sort": sort, "values": list(values), "description": ""}

    for bad in [
        [symbol("state", "Enum", ["only_one"])],          # could never be anything else
        [symbol("x", "Bool"), symbol("x", "Int")],         # duplicate name
        [symbol("a", "Enum", ["on", "off"]), symbol("b", "Enum", ["on", "idle"])],  # shared member
        [symbol("not-an-identifier", "Bool")],
        [symbol("x", "String")],
    ]:
        with pytest.raises(ValueError):
            Vocabulary(bad)


def test_bad_formulas_are_rejected():
    """The parser must refuse anything that is not one boolean expression over known symbols."""
    vocab = Vocabulary([{"name": "x", "sort": "Bool", "values": [], "description": ""}])
    for bad in ["(and x unknown_symbol)", "(+ 1 2)", "x) (assert (not x)", "(and x"]:
        with pytest.raises(ValueError):
            vocab.parse(bad)


def test_a_conflict_that_needs_three_rules_is_found():
    """No rule and no pair of rules clashes here; all three together do."""
    def symbol(name):
        return {"name": name, "sort": "Bool", "values": [], "description": ""}

    formal = {
        "symbols": [symbol(n) for n in ("member", "weekend", "sale", "discount", "free_shipping")],
        "rules": [
            {"id": "P1", "antecedent": "member", "consequent": "discount"},
            {"id": "P2", "antecedent": "weekend", "consequent": "free_shipping"},
            {"id": "P3", "antecedent": "sale", "consequent": "(not (and discount free_shipping))"},
        ],
    }
    conflicts = [f for f in analyze(formal) if f["type"] == "conflict"]
    assert conflicts == [{"type": "conflict", "rules": ["P1", "P2", "P3"],
                          "when": {"member": True, "sale": True, "weekend": True}}]
    # With pairs only, it is missed.
    assert [f for f in analyze(formal, max_group=2) if f["type"] == "conflict"] == []


def test_scenarios_list_what_the_rules_allow_and_rule_out():
    """`locked` is a condition in A1 and forbidden for admins by A3."""
    def symbol(name):
        return {"name": name, "sort": "Bool", "values": [], "description": ""}

    formal = {
        "symbols": [symbol(n) for n in ("locked", "admin", "access")],
        "rules": [
            {"id": "A1", "antecedent": "locked", "consequent": "(not access)"},
            {"id": "A3", "antecedent": "admin", "consequent": "(not locked)"},
        ],
    }
    scenarios = find_scenarios(formal)
    # Allowed: access is denied although the account is not locked (A1 does not apply).
    assert {"type": "scenario", "verdict": "accepted", "rules": ["A1"],
            "when": {"access": False, "locked": False}} in scenarios
    # Ruled out: a locked administrator account. A1 would apply, A3 makes it impossible.
    assert {"type": "scenario", "verdict": "rejected", "rules": ["A3", "A1"],
            "when": {"admin": True, "locked": True}} in scenarios


def test_findings_of_several_symbol_sets_are_merged_and_counted():
    conflict_ab = {"type": "conflict", "rules": ["A", "B"], "when": {"x": True}}
    with_facts = {"type": "conflict", "rules": ["B", "A"], "facts": ["F1"], "when": {"y": True}}
    conflict_cd = {"type": "conflict", "rules": ["C", "D"], "when": {"z": True}}
    gap = {"type": "gap", "when": {"x": False}}

    # One model: nothing changes.
    assert combine([[conflict_ab, gap]]) == [conflict_ab, gap]

    merged = combine([[with_facts, gap], [conflict_ab, conflict_cd, gap], [conflict_ab]])
    assert merged == [
        # Found with all 3 sets. The version proven without facts is shown (model 1).
        {**conflict_ab, "model": 1, "support": "3/3"},
        {**conflict_cd, "model": 1, "support": "1/3"},
        # Gaps cannot be matched across symbol sets: those of the first model are kept.
        {**gap, "model": 0},
    ]


def test_a_rule_restated_without_its_private_symbol_becomes_a_link():
    """Step 5 of formalize.py, with hand-written "LLM answers".

    D2's outcome `removed` is used by no other rule, so nothing can clash with
    it. Translated again without that symbol, 6 of 8 answers say "not
    retained". That becomes a link (an assumed fact), and with it the solver
    finds the conflict with D4.
    """
    symbols = [{"name": name, "sort": "Bool", "values": [], "description": ""}
               for name in ("confirmed", "removed", "retained")]
    rules = [
        {"id": "D2", "status": "accepted", "antecedent": "confirmed", "consequent": "removed"},
        {"id": "D4", "status": "accepted", "antecedent": "true", "consequent": "retained"},
    ]
    vocab = Vocabulary(symbols)
    hidden = _symbols_to_hide(vocab, rules)
    # D2 may use its own condition and D4's outcome; D4 only D2's outcome.
    assert hidden == {"D2": {"removed"}, "D4": {"confirmed", "retained"}}

    agree = {"reading": "the record is no longer retained", "antecedent": "confirmed",
             "consequent": "(not retained)"}
    cannot = {"reading": "", "antecedent": "confirmed", "consequent": "none"}
    links = _links(vocab, [rules[0]], hidden, [[agree] * 6 + [cannot] * 2], asked=8, facts=[])
    assert links == [{
        "id": "F1",
        "text": "What D2 demands, in the terms of the other requirements: the record is no longer retained",
        "formula": "(=> (and confirmed removed) (not retained))",
        "support": "6/8",
        "restates": "D2",
        "antecedent": "confirmed",
        "consequent": "(not retained)",
    }]
    # Without a majority (4 of 8) there is no link.
    assert _links(vocab, [rules[0]], hidden, [[agree] * 4 + [cannot] * 4], asked=8, facts=[]) == []

    formal = {"symbols": symbols, "background": links, "rules": rules}
    assert [f for f in analyze(formal) if f["type"] == "conflict"] == [
        {"type": "conflict", "rules": ["D2", "D4"], "facts": ["F1"], "when": {"confirmed": True}},
    ]


def lockers(with_the_full_locker_rule: bool) -> dict:
    """A courier scans a parcel; a recipient enters a pickup code. Both are events."""
    rules = [
        {"id": "P1", "antecedent": "(and parcel_scanned compartment_free)", "consequent": "compartment_opened"},
        {"id": "P2", "antecedent": "(and parcel_scanned (not compartment_free))", "consequent": "other_locker_shown"},
        {"id": "P3", "antecedent": "code_entered", "consequent": "compartment_opened"},
    ]
    if not with_the_full_locker_rule:
        del rules[1]
    return {
        "symbols": [{"name": name, "sort": "Bool", "values": [], "description": "",
                     "event": name in ("parcel_scanned", "code_entered")}
                    for name in ("parcel_scanned", "compartment_free", "code_entered",
                                 "compartment_opened", "other_locker_shown")],
        "rules": rules,
    }


def test_a_gap_is_looked_for_once_for_each_event():
    """Without the rule for a full locker, scanning a parcel has an uncovered case.

    The gap is reported for that event. Entering a code is always covered.
    The gap in which no event happens comes last, marked as quiet.
    """
    gaps = [f for f in analyze(lockers(with_the_full_locker_rule=False)) if f["type"] == "gap"]
    assert gaps == [
        {"type": "gap", "event": "parcel_scanned",
         "when": {"code_entered": False, "compartment_free": False, "parcel_scanned": True}},
        {"type": "gap", "when": {"code_entered": False, "parcel_scanned": False}, "quiet": True},
    ]

    # With both cases of the scan covered, only the quiet gap is left.
    gaps = [f for f in analyze(lockers(with_the_full_locker_rule=True)) if f["type"] == "gap"]
    assert gaps == [{"type": "gap", "when": {"code_entered": False, "parcel_scanned": False}, "quiet": True}]


def test_a_gap_the_facts_rule_out_is_marked_doubtful():
    """"Free" and "full" as two symbols: "neither" is a gap, unless a fact says one always holds."""
    def formal(rules: list, facts: list) -> dict:
        return {"symbols": [{"name": name, "sort": "Bool", "values": [], "description": "",
                             "event": name == "parcel_scanned"}
                            for name in ("parcel_scanned", "compartment_free", "locker_full",
                                         "compartment_opened", "other_locker_shown")],
                "background": [{"id": f"F{n}", "text": text, "formula": text}
                               for n, text in enumerate(facts, start=1)],
                "rules": rules}

    def scan_gap(formal: dict) -> dict:
        return next(f for f in analyze(formal) if f["type"] == "gap" and f.get("event") == "parcel_scanned")

    both = [{"id": "P1", "antecedent": "(and parcel_scanned compartment_free)", "consequent": "compartment_opened"},
            {"id": "P2", "antecedent": "(and parcel_scanned locker_full)", "consequent": "other_locker_shown"}]
    # "Not both" leaves "neither" possible: the gap stands.
    assert "doubted_by" not in scan_gap(formal(both, ["(not (and compartment_free locker_full))"]))
    # "One of the two always holds": the same gap is still reported, marked doubtful.
    gap = scan_gap(formal(both, ["(or compartment_free locker_full)"]))
    assert gap["doubted_by"] == ["F1"]
    assert gap["when"] == {"parcel_scanned": True, "compartment_free": False, "locker_full": False}
    # Without the rule for a full locker, the fact allows the gap: it is not marked.
    gap = scan_gap(formal(both[:1], ["(or compartment_free locker_full)"]))
    assert "doubted_by" not in gap and gap["when"]["compartment_free"] is False


def test_the_gap_search_over_all_situations_is_still_there():
    """The experiments compare: by_event=False searches as before, in any situation."""
    formal = lockers(with_the_full_locker_rule=False)
    vocab = Vocabulary(formal["symbols"])
    gaps = find_gaps(vocab, [vocab.rule(rule) for rule in formal["rules"]], by_event=False)
    assert 1 <= len(gaps) <= 3 and all("event" not in gap and "quiet" not in gap for gap in gaps)


def test_rules_with_nothing_in_common_are_not_tried_together():
    """Two unrelated parts in one document: the conflicts are those of each part."""
    symbols = [{"name": name, "sort": "Bool", "values": [], "description": ""}
               for name in ("order", "stock", "backorder", "page_printed", "counter_raised")]
    rules = [
        {"id": "R2", "antecedent": "(and order (not stock))", "consequent": "backorder"},
        {"id": "R3", "antecedent": "true", "consequent": "(not backorder)"},
        {"id": "P1", "antecedent": "page_printed", "consequent": "counter_raised"},
    ]
    vocab = Vocabulary(symbols)
    compiled = [vocab.rule(rule) for rule in rules]
    r2, r3, p1 = (_families(vocab, compiled, {})[id(rule)] for rule in compiled)
    assert r2 == r3 != p1
    # A fact that connects the two parts makes them one family.
    linked = _families(vocab, compiled, {"F1": vocab.parse("(=> counter_raised stock)")})
    assert len(set(linked.values())) == 1

    conflicts = [f for f in analyze({"symbols": symbols, "rules": rules}) if f["type"] == "conflict"]
    assert conflicts == [{"type": "conflict", "rules": ["R2", "R3"], "when": {"order": True, "stock": False}}]


def test_a_conflict_between_a_rule_and_a_special_case_of_it_says_so():
    """R2 applies only where R1 does (its condition entails R1's, not the other way round)."""
    def conflicts(rules: list[dict]) -> list[dict]:
        formal = {"symbols": [{"name": name, "sort": "Bool", "values": [], "description": name, "event": name == "called"}
                              for name in ("called", "folder_exists", "quiet", "folder_made", "error_thrown")],
                  "background": [],
                  "rules": [{"status": "accepted", "text": "", "trigger": "called", **rule} for rule in rules]}
        return [f for f in analyze(formal) if f["type"] == "conflict"]

    general = {"id": "R1", "antecedent": "called", "consequent": "folder_made"}
    special = {"id": "R2", "antecedent": "(and called folder_exists)", "consequent": "(not folder_made)"}
    (found,) = conflicts([general, special])
    assert found["rules"] == ["R1", "R2"] and found["special_case"] == {"general": "R1", "special": "R2"}
    assert "doubted_by" not in found and "simultaneous_events" not in found  # it stays a plain conflict
    # The order in the document does not matter.
    (found,) = conflicts([{**special, "id": "R1"}, {**general, "id": "R2"}])
    assert found["special_case"] == {"general": "R2", "special": "R1"}
    # A rule that always applies: every rule is a special case of it, so the mark would say nothing.
    (found,) = conflicts([{"id": "R1", "antecedent": "true", "consequent": "(not folder_made)"}, {**general, "id": "R2"}])
    assert "special_case" not in found
    # The same condition, or two conditions of which neither entails the other: no mark.
    (found,) = conflicts([general, {"id": "R2", "antecedent": "called", "consequent": "(not folder_made)"}])
    assert "special_case" not in found
    (found,) = conflicts([{**general, "antecedent": "(and called quiet)"}, special])
    assert "special_case" not in found
