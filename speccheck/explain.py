"""explain.py: stage 3, from findings to a report a person can read. LLM.

The solver's findings are facts about formulas. This stage says them in the
words of the requirements and attaches two choices to each, as Kiro does:

    A) keep the requirements as they are
    B) one specific change

The LLM only rewords. It is given each finding as a fact and cannot alter it.
The one decision it makes is which scenarios are worth showing (`judge`).

Four functions, used in this order:

    evidence   one solver finding as an exact fact sheet (no LLM)
    explain    the LLM words each defect (conflict, gap, ambiguity)
    judge      the LLM picks the surprising scenarios and words them
    render     the Markdown report

"models" below is the list of formal models of the document (formal.json
dicts). There is one, unless several symbol sets were asked for; a finding
then says in "model" which one its witness is written in.
"""

from concurrent.futures import ThreadPoolExecutor

from .llm import LLM
from .logic import describe

EXPLAIN_SYSTEM = """\
You explain one finding of an automated requirements analysis to the author \
of the requirements. The finding was proven by a logic solver: state it as a \
fact, do not question or soften it.

The finding names a situation as a list of facts, each marked TRUE or FALSE \
(or given a value). Describe exactly that situation: a fact marked FALSE is \
not the case.

Write for someone who has never seen formal logic. Use the wording of the \
requirements. Never mention symbol names, formulas, samples or the solver. \
Refer to requirements by their ids.

Answer with:
- situation: restate the listed situation in one plain sentence, fact by \
fact, in the listed order. A fact marked TRUE is the case. A fact marked \
FALSE is NOT the case: say it with "no" or "not" (FALSE: a file was uploaded \
-> "no file was uploaded"). Write "any" if no situation is listed.
- title: a few words naming the problem.
- explanation: two or three sentences saying what the problem is and that it \
appears in the situation you just restated. Do not describe any other \
situation.
- option_a: one sentence on what it means to keep the requirements as written.
- option_b: one sentence proposing a specific change to the requirements that \
removes the problem.

Only when the finding is an ambiguity: the explanation describes the two \
readings and ends with "Which did you mean?", option_a keeps the first \
reading, and option_b is a rewording that states the second reading. The \
logic shown in brackets after each reading tells you precisely how the two \
differ; say that difference in plain words. Do not ask that question for a \
conflict or a gap.

If the finding lists assumptions, it holds only if they are true. Say so in \
the explanation and state each assumption in plain words.

If the finding says it may be a false alarm (assumed facts make its \
situation impossible, or it needs two events at the same moment), say so, \
and say why in plain words."""

# "situation" comes first on purpose. The model writes the fields in this
# order, so it has to restate the proven situation fact by fact before it
# explains anything. Without this step it tended to drift to a more "natural"
# situation, e.g. describing an order as submitted when the fact was FALSE.
EXPLAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "situation": {"type": "string"},
        "title": {"type": "string"},
        "explanation": {"type": "string"},
        "option_a": {"type": "string"},
        "option_b": {"type": "string"},
    },
    "required": ["situation", "title", "explanation", "option_a", "option_b"],
    "additionalProperties": False,
}

JUDGE_SYSTEM = """\
You judge one consequence of a set of requirements for their author. A logic \
solver proved that the requirements allow, or rule out, one concrete \
behaviour. That is a fact: do not question it.

Decide whether it is surprising, given the goal the document states: would \
the author most likely NOT have intended it? An allowed behaviour is \
surprising when it defeats the purpose of a requirement or of the goal. A \
ruled-out situation is surprising when it can plainly happen in real use. A \
consequence that is harmless or obviously intended is not surprising. Most \
consequences are not surprising.

The behaviour is given as a list of facts, each marked TRUE or FALSE (or \
given a value). Write for someone who has never seen formal logic. Use the \
wording of the requirements. Never mention symbol names, formulas or the \
solver. Refer to requirements by their ids.

Answer with:
- situation: restate the listed facts in one plain sentence, fact by fact, in \
the listed order. A fact marked FALSE is NOT the case: say it with "no" or \
"not".
- surprise: 0 = intended or harmless, 1 = odd but harmless, 2 = probably not \
intended, 3 = clearly against the goal.
- title: a few words naming the behaviour.
- explanation: two or three sentences: what the requirements allow (or rule \
out) in the situation you just restated, and why the author may not want that.
- option_a: one sentence: keep the requirements, so the behaviour stays \
allowed (or ruled out).
- option_b: one sentence proposing a specific change to the requirements \
that forbids (or allows) it."""

# As in EXPLAIN_SCHEMA, "situation" comes first so the model restates the
# proven facts before it judges them.
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "situation": {"type": "string"},
        "surprise": {"enum": [0, 1, 2, 3]},
        "title": {"type": "string"},
        "explanation": {"type": "string"},
        "option_a": {"type": "string"},
        "option_b": {"type": "string"},
    },
    "required": ["situation", "surprise", "title", "explanation", "option_a", "option_b"],
    "additionalProperties": False,
}

# Scenarios are shown only if the judge scores them at least this high, and
# only the highest-scored few: the report is about defects first.
MIN_SURPRISE = 2
MAX_SCENARIOS = 3


def evidence(finding: dict, formal: dict) -> str:
    """State one solver finding in exact, technical words. No LLM involved.

    formal  the formal model the finding's witness is written in.

    This text is the "fact sheet" given to the LLM, and it is also printed in
    the report under each explanation so the reader can see what was proven.
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}

    def situation(witness: dict) -> str:
        """A witness as text, on the lines after the sentence that names it."""
        return "\n" + describe(witness, descriptions)

    if finding["type"] == "conflict":
        text = (f"Requirements {', '.join(finding['rules'])} cannot all be obeyed "
                f"in this situation:{situation(finding['when'])}")
        # A conflict that needs assumed facts is only as true as those facts,
        # so they are spelled out as part of what was proven.
        fact_texts = {fact["id"]: fact["text"] for fact in formal.get("background", [])}
        if finding.get("facts"):
            text += "\nThis depends on assumptions that are not stated in the requirements:"
            text += "".join(f"\n- {fact_id}: {fact_texts[fact_id]}" for fact_id in finding["facts"])
        if finding.get("doubted_by"):
            text += ("\nBut these assumed facts say that this situation cannot happen, "
                     "so the conflict may be a false alarm:")
            text += "".join(f"\n- {fact_id}: {fact_texts[fact_id]}" for fact_id in finding["doubted_by"])
        if finding.get("simultaneous_events"):
            text += ("\nBut this situation needs these events to happen at the same moment: "
                     f"{', '.join(finding['simultaneous_events'])}. The requirements are "
                     "probably not meant for that, so the conflict may be a false alarm.")
        # The conflict was found with the first reading of an ambiguous rule.
        for rule_id, reading in finding.get("depends_on_reading", {}).items():
            text += (f"\nBut {rule_id} is ambiguous (see its finding). With its other reading "
                     f"these requirements do not clash. That reading: {reading}")
        return text
    if finding["type"] == "gap":
        text = (f"No requirement says what the system must do "
                f"in this situation:{situation(finding['when'])}")
        if finding.get("quiet"):
            text += ("\nNo event happens in this situation, so this may only mean that "
                     "the system waits.")
        if finding.get("doubted_by"):
            fact_texts = {fact["id"]: fact["text"] for fact in formal.get("background", [])}
            text += ("\nBut these assumed facts say that this situation cannot happen, "
                     "so the gap may be a false alarm:")
            text += "".join(f"\n- {fact_id}: {fact_texts[fact_id]}" for fact_id in finding["doubted_by"])
        for rule_id, reading in finding.get("depends_on_reading", {}).items():
            text += (f"\nBut {rule_id} is ambiguous (see its finding). With its other reading "
                     f"a requirement applies in this situation. That reading: {reading}")
        return text
    if finding["type"] == "scenario" and finding["verdict"] == "accepted":
        rule = finding["rules"][0]
        return (f"The requirements allow this behaviour:{situation(finding['when'])}"
                f"\nRequirement {rule} does not apply in it, and yet what {rule} demands is the case.")
    if finding["type"] == "scenario":
        forbidder, other = finding["rules"]
        return (f"The requirements rule out this situation:{situation(finding['when'])}"
                f"\nRequirement {other} would apply in it, but requirement {forbidder} makes it impossible.")
    # ambiguity
    if finding.get("found_by") == "questions":
        answers = finding["answers"]
        text = (f"Requirement {finding['rule']} has no single clear meaning. Shown both "
                f"readings and the situation below, and asked whether the words decide "
                f"between them, the answers were: {answers['translation']} for reading 1, "
                f"{answers['other']} for reading 2, {answers['either']} 'either'.")
    elif finding.get("found_by") == "models":
        text = (f"Requirement {finding['rule']} has no single clear meaning. Two independent "
                f"models read it differently: only {finding['second_support']} translations by "
                f"the second model mean the same as reading 1; reading 2 is its most common "
                f"other reading.")
    else:
        split = "/".join(str(n) for n in finding.get("split", [])) or "none usable"
        text = (f"Requirement {finding['rule']} has no single clear meaning "
                f"(independent translations split {split}).")
    for number, reading in enumerate(finding["readings"], start=1):
        text += f"\nReading {number}: {reading}"
    if finding["differs_when"]:
        text += f"\nThe readings differ in this situation:{situation(finding['differs_when'])}"
    # What the answer to this question changes in the rest of the report.
    effect = finding.get("other_reading")
    if effect is not None:
        changes = ([f"the conflict between {', '.join(group)} is gone" for group in effect["removes"]]
                   + [f"a conflict between {', '.join(group)} appears" for group in effect["adds"]]
                   + ([f"a requirement applies in {effect['covers_gaps']} of the gaps reported below"]
                      if effect["covers_gaps"] else []))
        text += ("\nWith reading 2 instead of reading 1: " + "; ".join(changes) + "." if changes
                 else "\nChoosing reading 2 instead of reading 1 changes no conflict and no gap.")
    if finding["status"] == "rejected":
        text += "\nIt was left out of the conflict and gap checks and should be rewritten."
    return text


def _requirements(models: list[dict]) -> str:
    """The requirements as "id: text" lines, for the prompts."""
    return "\n".join(f"{r['id']}: {r['text']}" for r in models[0]["rules"])


def explain(llm: LLM, findings: list[dict], models: list[dict]) -> list[dict]:
    """Ask the LLM to word each defect. Returns them with the wording added.

    Each returned finding has the extra keys situation, title, explanation,
    option_a, option_b. ("situation" is the model's own restatement of the
    witness; it is kept in findings.json but not printed in the report.)
    """
    requirements = _requirements(models)

    def explain_one(finding: dict) -> dict:
        # The fact sheet names the assumed facts a finding depends on (if any),
        # so the model sees exactly the facts that matter and no others.
        sheet = evidence(finding, models[finding.get("model", 0)])
        answers = llm.ask(EXPLAIN_SYSTEM, f"Requirements:\n{requirements}\n\nFinding:\n{sheet}",
                          EXPLAIN_SCHEMA)
        # If the model fails to answer, the finding is still reported, unworded.
        return {**finding, **(answers[0] if answers else {})}

    with ThreadPoolExecutor(max_workers=16) as pool:
        return list(pool.map(explain_one, findings))


def judge(llm: LLM, scenarios: list[dict], models: list[dict], spec_text: str) -> list[dict]:
    """Ask the LLM how surprising each scenario is. Returns the top ones, worded.

    spec_text  the document itself: the judge needs the goal it states.

    The scenarios are proven; the judge only scores how much each deserves the
    author's attention ("surprise", 0 to 3). Those scored below MIN_SURPRISE
    are dropped, and at most MAX_SCENARIOS are returned, highest score first.
    """
    requirements = _requirements(models)

    def judge_one(scenario: dict) -> dict:
        sheet = evidence(scenario, models[scenario.get("model", 0)])
        prompt = f"Document:\n{spec_text}\n\nRequirements:\n{requirements}\n\nConsequence:\n{sheet}"
        answers = llm.ask(JUDGE_SYSTEM, prompt, JUDGE_SCHEMA)
        return {**scenario, **(answers[0] if answers else {"surprise": 0})}

    with ThreadPoolExecutor(max_workers=16) as pool:
        judged = list(pool.map(judge_one, scenarios))
    worth_showing = [scenario for scenario in judged if scenario["surprise"] >= MIN_SURPRISE]
    return sorted(worth_showing, key=lambda scenario: -scenario["surprise"])[:MAX_SCENARIOS]


def render(findings: list[dict], models: list[dict], title: str) -> str:
    """Build the Markdown report. Works with or without the LLM wording.

    The report is the formal analysis: what the solver proved. If the optional
    review ran (refine.py), its notes follow as a second part, kept apart so
    the reader always knows how much to trust a finding.
    """
    solver = [f for f in findings if f["type"] != "review"]
    notes = [f for f in findings if f["type"] == "review"]
    counts = {kind: sum(f["type"] == kind for f in solver)
              for kind in ("conflict", "gap", "ambiguity", "scenario")}
    doubtful = {kind: sum(f["type"] == kind and bool(f.get("doubted_by") or f.get("simultaneous_events"))
                          for f in solver)
                for kind in ("conflict", "gap")}
    lines = [
        f"# Requirements analysis: {title}",
        "",
        f"{len(models[0]['rules'])} requirements analysed"
        + (f" with {len(models)} symbol sets" if len(models) > 1 else "")
        + f": {counts['conflict']} conflict(s)"
        + (f" ({doubtful['conflict']} doubtful)" if doubtful["conflict"] else "")
        + f", {counts['gap']} gap(s)"
        + (f" ({doubtful['gap']} doubtful)" if doubtful["gap"] else "") + ", "
        f"{counts['ambiguity']} ambiguity(ies)"
        + (f", {counts['scenario']} scenario(s) to confirm" if counts["scenario"] else "") + "."
        + (f" Review of the text: {len(notes)} note(s)." if notes else ""),
    ]

    def section(level: str, number: int, kind: str, finding: dict, footer: str) -> list[str]:
        """One finding: heading, explanation with the two options, footer."""
        heading = finding.get("title", "")
        block = ["", f"{level} {number}. {kind}" + (f": {heading}" if heading else ""), ""]
        if "explanation" in finding:
            block += [
                finding["explanation"],
                "",
                f"- **A) Keep as-is:** {finding['option_a']}",
                f"- **B) Change:** {finding['option_b']}",
                "",
            ]
        return block + [footer]

    # The solver's findings.
    for number, finding in enumerate(solver, start=1):
        if finding["type"] == "scenario":
            kind = "Scenario, allowed" if finding["verdict"] == "accepted" else "Scenario, ruled out"
        else:
            kind = finding["type"].capitalize()
        remarks = []
        if finding.get("facts"):
            remarks.append("if the assumed facts hold")
        if finding.get("doubted_by"):
            remarks.append("doubtful: the assumed facts say this situation cannot happen")
        if finding.get("simultaneous_events"):
            remarks.append("doubtful: needs two events at the same moment")
        if finding.get("quiet"):
            remarks.append("no event happens")
        if finding.get("depends_on_reading"):
            remarks.append(f"depends on the reading of {', '.join(finding['depends_on_reading'])}")
        if "support" in finding:  # several symbol sets were used
            found, total = finding["support"].split("/")
            remarks.append(f"found with {found} of {total} symbol sets")
        if remarks:
            kind += f" ({', '.join(remarks)})"
        # The footer is the exact fact behind the wording, so the reader can check it.
        sheet = evidence(finding, models[finding.get("model", 0)])
        lines += section("##", number, kind, finding, f"*Proven:* {sheet}")

    # The notes of the optional review, as a part of their own.
    if notes:
        lines += ["", "## Review of the text (not proven)", "",
                  "The model's reading of the requirements as written. "
                  "These notes are a judgement, not a proof."]
    for number, note in enumerate(notes, start=len(solver) + 1):
        about = f"requirements {', '.join(note['rules'])}" if note["rules"] else "the document"
        if note.get("proven"):
            footer = (f"*Review, and proven:* the solver found a conflict between "
                      f"{about} too (see above).")
        else:
            footer = f"*Review, not proven:* the reviewing model's reading of {about}."
        lines += section("###", number, f"Review ({note['kind']})", note, footer)
    return "\n".join(lines) + "\n"
