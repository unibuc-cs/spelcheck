"""refine.py: OPTIONAL review of the text by an LLM. Off by default (`--review`).

This project is about the formal analysis; nothing in the three stages needs
this file. It exists because Kiro has such a stage ("refinement") and finds one
of its two blog examples with it, not with the solver.

The formal stages find only what survives the translation to logic. Some
defects do not survive it: when the model picks the symbols, it tends to read
two requirements that disagree in a way that makes them agree. Here the same
document is read once as plain text, by an LLM asked to take every requirement
at its word.

It produces review notes of three kinds:

    contradiction   requirements that cannot all be obeyed as written
    wording         a requirement that cannot be tested or built as written
    missing         a situation the goal implies and no requirement covers

Each note proposes one concrete change: the new text of a requirement, or a
new requirement. A note is the model's judgement, not a proof. The report
keeps notes apart from the solver's findings and marks them as such.

A note is a finding dict like the others (see checks.py):

    {"type": "review", "kind": "contradiction", "rules": ["D2", "D4"],
     "rewrite": {"rule": "D2", "text": "<new text of D2>"},
     "proven": false,
     "title": ..., "explanation": ..., "option_a": ..., "option_b": ...}

    rules    the requirements involved (empty for "missing")
    rewrite  the proposed change; "rule" is null when a requirement is added
    proven   contradictions only: did the solver prove a conflict between
             these requirements as well? (set by `confirm`)
"""

import re

from .llm import LLM

REFINE_SYSTEM = """\
You review a software requirements document before it is analysed formally. \
You get the document and the list of its requirements, each with an id.

Work backward from the goal the document states (its user story or purpose). \
What does success look like? What must hold for it to be reached, and what \
could prevent it? Then read every requirement literally, exactly as written, \
and note the problems you find. There are three kinds:

- contradiction: the requirement and one or more others can apply in the \
same situation and demand incompatible outcomes, as they are written. Take \
each one at its word: do not assume a reading that makes them agree. Any \
problem that involves a second requirement is a contradiction, not wording.
- wording: a problem the requirement has by itself: a tester could not \
decide whether the system passes it. It has a vague qualifier (fast, \
user-friendly, appropriate), or it prescribes an implementation (a storage \
technique, an algorithm, a screen layout) where it should state the \
behaviour that can be observed. Do not ask for more detail than a tester \
needs.
- missing: a situation the goal implies has no requirement: an error, a \
refusal, a cancellation.

Note only problems you are sure of. A sound document gets an empty list. \
Write at most one note per requirement: if it has several problems, pick the \
most serious kind and mention the others in the explanation. Write at most \
three "missing" notes, the most important ones.

Each note has:
- kind: contradiction, wording or missing.
- rule: the id of the requirement to rewrite. Empty for "missing".
- clashes_with: for a contradiction, the ids of the other requirements \
involved. Otherwise empty.
- title: a few words naming the problem.
- explanation: two or three sentences in plain words, quoting the words of \
the requirements that cause the problem. For a contradiction, name the \
situation in which the requirements clash.
- option_a: one sentence on what it means to keep the requirements as written.
- new_text: the full text of the rewritten requirement (for "missing": of \
the new requirement), in the style of the document, fixing every problem \
you mentioned. It states observable behaviour, never a design choice."""

REFINE_SCHEMA = {
    "type": "object",
    "properties": {
        "notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"enum": ["contradiction", "wording", "missing"]},
                    "rule": {"type": "string"},
                    "clashes_with": {"type": "array", "items": {"type": "string"}},
                    "title": {"type": "string"},
                    "explanation": {"type": "string"},
                    "option_a": {"type": "string"},
                    "new_text": {"type": "string"},
                },
                "required": ["kind", "rule", "clashes_with", "title",
                             "explanation", "option_a", "new_text"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["notes"],
    "additionalProperties": False,
}


def refine(llm: LLM, spec_text: str, rules: list[dict]) -> list[dict]:
    """Ask the LLM to review the document. Returns the review notes.

    spec_text  the document as the user wrote it (it holds the goal / user story)
    rules      its requirements as the read step listed them: {"id", "text"}.
               They are passed along so the notes use the same ids as the
               formal track.
    """
    listing = "\n".join(f"{rule['id']}: {rule['text']}" for rule in rules)
    prompt = f"Document:\n{spec_text}\n\nRequirements:\n{listing}"
    answers = llm.ask(REFINE_SYSTEM, prompt, REFINE_SCHEMA)
    return _notes(answers[0]["notes"], rules) if answers else []


def _one_line(text: str) -> str:
    """Put a text of the model on one line, without Markdown heading marks.

    The model writes a new requirement "in the style of the document", which
    can mean several lines starting with "####". The report and refined.md
    need plain one-line texts.
    """
    return " ".join(re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE).split())


def _notes(raw_notes: list[dict], rules: list[dict]) -> list[dict]:
    """Turn the model's raw notes into findings, dropping the unusable ones."""
    known = {rule["id"] for rule in rules}
    notes = []
    rewritten = set()  # ids that already have a proposed new text
    for raw in raw_notes:
        raw = {**raw, **{key: _one_line(raw[key])
                         for key in ("title", "explanation", "option_a", "new_text")}}
        if raw["kind"] == "missing":
            involved, target = [], None
            option_b = f'Add the requirement: "{raw["new_text"]}"'
        else:
            target = raw["rule"]
            # The model must point at requirements that exist, and each
            # requirement gets one new text only (refined.md needs one).
            if target not in known or target in rewritten:
                continue
            others = [r for r in raw["clashes_with"] if r in known and r != target]
            if raw["kind"] == "contradiction" and not others:
                continue  # a contradiction needs a second requirement
            involved = [target] + others
            rewritten.add(target)
            option_b = f'Rewrite {target} as: "{raw["new_text"]}"'
        notes.append({
            "type": "review",
            "kind": raw["kind"],
            "rules": involved,
            "rewrite": {"rule": target, "text": raw["new_text"]},
            "title": raw["title"],
            "explanation": raw["explanation"],
            "option_a": raw["option_a"],
            "option_b": option_b,
        })
    return notes


def confirm(notes: list[dict], solver_findings: list[dict]) -> list[dict]:
    """Mark each contradiction note: did the solver prove it too?

    The two tracks are independent, so agreement between them is worth showing.
    A note counts as proven when the solver found a conflict among (some of)
    the requirements the note names.
    """
    conflicts = [set(f["rules"]) for f in solver_findings if f["type"] == "conflict"]
    for note in notes:
        if note["kind"] == "contradiction":
            note["proven"] = any(conflict <= set(note["rules"]) for conflict in conflicts)
    return notes


def refined_text(rules: list[dict], notes: list[dict], title: str) -> str:
    """Build refined.md: the requirements with every proposed change applied.

    The user can read it, edit it, and run speccheck on it again.
    """
    new_text = {note["rewrite"]["rule"]: note["rewrite"]["text"]
                for note in notes if note["rewrite"]["rule"] is not None}
    added = [note["rewrite"]["text"] for note in notes if note["rewrite"]["rule"] is None]
    added_ids = [f"NEW{number}" for number in range(1, len(added) + 1)]

    lines = [
        f"# Refined requirements: {title}",
        "",
        "The requirements of the analysed document with the proposals of the review applied.",
        f"Amended: {', '.join(new_text) or 'none'}. Added: {', '.join(added_ids) or 'none'}.",
        "",
    ]
    lines += [f"- {rule['id']}: {new_text.get(rule['id'], rule['text'])}" for rule in rules]
    lines += [f"- {new_id}: {text}" for new_id, text in zip(added_ids, added)]
    return "\n".join(lines) + "\n"
