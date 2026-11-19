"""Tests for the optional review (refine.py, `--review`). No LLM, no GPU.

The LLM is replaced by a stand-in that returns a hand-written answer, so these
tests check what the code does with the model's notes: which it keeps, how it
compares them with the solver, and how the report shows them.
"""

from speccheck.explain import render
from speccheck.refine import confirm, refine, refined_text

RULES = [
    {"id": "D1", "text": "WHEN deletion is confirmed, THE System SHALL remove the record."},
    {"id": "D2", "text": "THE System SHALL retain all records."},
    {"id": "D3", "text": "THE System SHALL respond quickly."},
]


def note(kind, rule, clashes_with=(), new_text="new text"):
    """One raw note, in the shape the LLM is asked to answer with."""
    return {"kind": kind, "rule": rule, "clashes_with": list(clashes_with), "title": "t",
            "explanation": "e", "option_a": "a", "new_text": new_text}


class FakeLLM:
    """Stands in for llm.LLM: always answers with the notes it was given."""

    def __init__(self, notes):
        self.notes = notes

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        return [{"notes": self.notes}]


def test_review_keeps_usable_notes_and_drops_the_rest():
    notes = refine(FakeLLM([
        note("contradiction", "D1", ["D2"], "WHEN deletion is confirmed, mark the record as deleted."),
        note("wording", "D3", new_text="THE System SHALL respond within 2 seconds."),
        # A new requirement written over several lines with a Markdown heading:
        # it must come out as one plain line.
        note("missing", "", new_text="#### Scenario: no record\nIF the record does not exist,\nTHEN show an error."),
        note("contradiction", "D2", ["D9"]),   # dropped: D9 does not exist, no partner left
        note("wording", "D7"),                 # dropped: D7 does not exist
        note("wording", "D1"),                 # dropped: D1 already has a new text
    ]), "the document", RULES)

    assert [(n["kind"], n["rules"], n["rewrite"]["rule"]) for n in notes] == [
        ("contradiction", ["D1", "D2"], "D1"),
        ("wording", ["D3"], "D3"),
        ("missing", [], None),
    ]
    assert notes[0]["option_b"] == 'Rewrite D1 as: "WHEN deletion is confirmed, mark the record as deleted."'
    assert notes[2]["option_b"] == ('Add the requirement: "Scenario: no record IF the record '
                                    'does not exist, THEN show an error."')


def test_a_contradiction_note_is_marked_when_the_solver_proved_it_too():
    notes = refine(FakeLLM([note("contradiction", "D1", ["D2"]),
                            note("contradiction", "D3", ["D2"])]), "", RULES)
    solver_findings = [{"type": "conflict", "rules": ["D1", "D2"], "when": {}}]

    confirm(notes, solver_findings)
    assert [n["proven"] for n in notes] == [True, False]


def test_refined_text_applies_every_proposal():
    notes = refine(FakeLLM([
        note("contradiction", "D1", ["D2"], "WHEN deletion is confirmed, mark the record as deleted."),
        note("missing", "", new_text="IF the record does not exist, THEN show an error."),
    ]), "", RULES)

    assert refined_text(RULES, notes, "demo").splitlines()[3:] == [
        "Amended: D1. Added: NEW1.",
        "",
        "- D1: WHEN deletion is confirmed, mark the record as deleted.",
        "- D2: THE System SHALL retain all records.",
        "- D3: THE System SHALL respond quickly.",
        "- NEW1: IF the record does not exist, THEN show an error.",
    ]


def test_report_keeps_review_notes_apart_from_proven_findings():
    formal = {"symbols": [], "rules": RULES}
    notes = confirm(refine(FakeLLM([note("contradiction", "D1", ["D2"])]), "", RULES), [])
    gap = {"type": "gap", "when": {}}

    report = render([gap] + notes, [formal], "demo")
    formal_part, review_part = report.split("## Review of the text")
    assert "## 1. Gap" in formal_part and "*Proven:*" in formal_part
    assert "### 2. Review (contradiction)" in review_part
    assert "*Review, not proven:*" in review_part
