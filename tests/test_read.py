"""Tests for reading a long document in pieces, and for a rule whose translation demands nothing.
No LLM, no GPU: the LLM is a stand-in with fixed answers.
"""

from speccheck.checks import find_ambiguities
from speccheck.explain import evidence, render
from speccheck.formalize import PIECE, READ_MORE, READ_SYSTEM, _judge, _pieces, _read_document
from speccheck.logic import Vocabulary


def requirement(number: int, scenarios: int = 3) -> str:
    """One OpenSpec requirement of about 500 characters."""
    lines = [f"### Requirement: Feature {number}", "", f"The system SHALL provide feature {number}.", ""]
    for scenario in range(1, scenarios + 1):
        lines += [f"#### Scenario: Case {number}.{scenario}", "",
                  f"- **WHEN** the user asks for feature {number} in the way of case {scenario}",
                  f"- **THEN** the system gives answer {number}.{scenario}", ""]
    return "\n".join(lines)


def long_document(requirements: int = 12) -> str:
    return ("# Tool Specification\n\n## Purpose\n\nA tool.\n\n## Requirements\n\n"
            + "\n".join(requirement(number) for number in range(1, requirements + 1)))


# ------------------------------------------------------------------- the pieces


def test_a_short_document_is_one_piece():
    text = "# Spec\n\n" + requirement(1)
    assert _pieces(text) == [text]


def test_a_long_document_is_cut_at_its_requirements():
    text = long_document()
    pieces = _pieces(text)
    assert len(pieces) > 1 and "\n".join(pieces) == text          # nothing lost, nothing moved
    assert all(len(piece) <= PIECE + PIECE // 8 for piece in pieces)
    # Every piece but the first starts with a requirement, and no scenario is cut off its requirement.
    assert all(piece.startswith("### Requirement:") for piece in pieces[1:])
    assert pieces[0].startswith("# Tool Specification")              # the title and purpose go with what follows
    assert all(piece.count("#### Scenario:") % 3 == 0 for piece in pieces)


def test_a_code_block_is_not_cut_and_its_headings_are_text():
    block = "```\n### Requirement: Example\n\n#### Scenario: Short name\n- **WHEN** ...\n```\n"
    text = long_document(6) + "\n" + block + "\n" + requirement(7)
    pieces = _pieces(text)
    assert "\n".join(pieces) == text
    assert sum(block in piece for piece in pieces) == 1
    assert not any(piece.startswith("### Requirement: Example") for piece in pieces)


def test_a_list_without_headings_is_cut_at_its_lines():
    lines = [f"- F{number}: WHEN event {number} happens, THE System SHALL do thing {number} and write it to the log."
             for number in range(1, 81)]
    text = "# Requirements: Ferry\n\n" + "\n".join(lines)
    pieces = _pieces(text)
    assert len(pieces) > 2 and "\n".join(pieces) == text
    assert all(piece.split("\n")[0].startswith(("# Requirements", "- F")) for piece in pieces)


# -------------------------------------------------------------- reading in pieces


class FakeLLM:
    """Stands in for llm.LLM in the read step: one rule and one new symbol for every scenario of a piece."""

    def __init__(self, labelled: bool = True):
        self.labelled, self.calls = labelled, []

    def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
        assert system.startswith(READ_SYSTEM)
        self.calls.append((system.endswith(READ_MORE), user))
        document = user.split("Document:\n")[-1]
        names = [line.split("Scenario: Case ")[1] for line in document.split("\n") if line.startswith("#### Scenario:")]
        rules = [{"id": f"S{name}" if self.labelled else f"R{number}", "text": f"case {name}", "trigger": ""}
                 for number, name in enumerate(names, start=1)]
        symbols = [{"name": "answer_" + name.replace(".", "_"), "sort": "Bool", "values": [],
                    "description": f"answer {name} is given", "event": False} for name in names]
        return [{"rules": rules, "symbols": symbols}]


def test_every_piece_is_read_with_the_symbols_so_far():
    llm = FakeLLM()
    rules, symbols = _read_document(llm, long_document(), 0.0)
    pieces = _pieces(long_document())

    assert len(llm.calls) == len(pieces)
    assert [with_symbols for with_symbols, _ in llm.calls] == [False] + [True] * (len(pieces) - 1)
    # The second piece is shown the symbols that the first one made, then its own text.
    second = llm.calls[1][1]
    assert second.startswith("Symbols of the system so far:\n- answer_1_1: Bool - answer 1.1 is given")
    assert second.endswith("Document:\n" + pieces[1])
    # All 36 rules, in the order of the document, and one symbol for each.
    assert [rule["id"] for rule in rules] == [f"S{r}.{s}" for r in range(1, 13) for s in range(1, 4)]
    assert len(symbols) == 36 and len({symbol["name"] for symbol in symbols}) == 36


def test_rules_numbered_again_in_a_later_piece_are_numbered_on():
    llm = FakeLLM(labelled=False)   # every piece comes back as R1, R2, ...
    rules, _ = _read_document(llm, long_document(), 0.0)
    assert [rule["id"] for rule in rules] == [f"R{number}" for number in range(1, 37)]
    assert [rule["text"] for rule in rules][:4] == ["case 1.1", "case 1.2", "case 1.3", "case 2.1"]


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
