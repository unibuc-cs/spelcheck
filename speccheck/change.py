"""change.py: check an OpenSpec change against the specs that already exist. No LLM here.

In an OpenSpec project the specs say what the system does today, and new work
arrives as a change, a folder that holds only the difference:

    openspec/specs/auth/spec.md                          what exists
        ### Requirement: Account Lockout
        #### Scenario: Lockout threshold
        - **WHEN** the number of failed attempts on an account reaches 5
        - **THEN** the system locks the account

    openspec/changes/admin-never-locked/specs/auth/spec.md      the change (a "delta")
        ## ADDED Requirements
        ### Requirement: Administrator Access
        #### Scenario: Administrators are never locked out
        - **WHEN** the account belongs to an administrator
        - **THEN** the system does not lock the account

Neither file has a conflict on its own; together they do. This module does the
two steps around the usual pipeline (cli.py, with --change):

1. merge(): apply the change to the specs, as `openspec archive` would, and
   write everything into ONE document. Every scenario gets a label, R1, R2,
   ..., written into its header ("#### Scenario R4: Lockout threshold"). The
   read step uses a document's own labels as rule ids, so afterwards we know
   which rules the change added or modified.
2. The merged document is formalized and checked like any spec.
3. about_change(): keep the findings that involve the change. A conflict
   among requirements that existed before is not the change's fault.

A delta file has up to four sections, applied in this order:

    ## RENAMED Requirements     - FROM: `### Requirement: Old name`
                                - TO: `### Requirement: New name`
    ## REMOVED Requirements     ### Requirement: <name>      (the text below it is a reason)
    ## MODIFIED Requirements    ### Requirement: <name>      (the full new text)
    ## ADDED Requirements       ### Requirement: <name>      (the full text)

Requirements are matched by their name. A capability that has no spec yet gets
one from its ADDED requirements.

Known limit: a REMOVED requirement can open a gap, and the removed rule is not
in the merged document. That gap is found, but nothing ties it to the change,
so it is not selected in step 3.
"""

import re
from pathlib import Path
from typing import NamedTuple

from .logic import Vocabulary

REQUIREMENT = re.compile(r"^###\s+Requirement:\s*(.+?)\s*$")
SCENARIO = re.compile(r"^####\s+Scenario:\s*(.*?)\s*$")
SECTION = re.compile(r"^##\s+(ADDED|MODIFIED|REMOVED|RENAMED)\s+Requirements\s*$", re.IGNORECASE)
RENAME = re.compile(r"^\s*-\s*(FROM|TO):\s*`?\s*###\s+Requirement:\s*(.+?)\s*`?\s*$", re.IGNORECASE)


class Merged(NamedTuple):
    """The specs after a change, as one document. Plain data, so that it can be saved as JSON."""
    name: str           # the change's folder name
    text: str           # the document; every scenario header carries its label
    scenarios: dict     # label -> {"capability", "requirement", "scenario", "status"};
    #                     status is "existing", "added" or "modified"
    changed_text: list  # the text of each added or modified requirement above its
    #                     first scenario (its SHALL sentence), see changed_rules
    removed: list       # "capability/requirement" for each requirement the change removes


def merge(change_dir: Path) -> Merged:
    """Apply the change in `change_dir` to its project's specs; return them as one labelled document.

    change_dir is openspec/changes/<name>; the specs are in openspec/specs,
    two folders up. A delta that names a requirement which does not exist (or
    adds one that does) raises ValueError, as `openspec archive` refuses it.
    """
    specs_dir = change_dir.parent.parent / "specs"
    # capability -> [preamble lines, {requirement name: its lines}, {requirement name: status}]
    specs = {}
    for spec_file in sorted(specs_dir.glob("**/spec.md")):
        capability = spec_file.parent.relative_to(specs_dir).as_posix()
        preamble, requirements = _requirements(spec_file.read_text(encoding="utf-8").splitlines())
        specs[capability] = [preamble, requirements, dict.fromkeys(requirements, "existing")]

    removed = []
    for delta_file in sorted((change_dir / "specs").glob("**/spec.md")):
        capability = delta_file.parent.relative_to(change_dir / "specs").as_posix()
        sections = _sections(delta_file.read_text(encoding="utf-8").splitlines())
        if capability not in specs:  # a new capability: only ADDED makes sense
            purpose = sections.get("PURPOSE") or ["(new with this change)"]
            specs[capability] = [[f"# {capability} Specification", "", "## Purpose", "", *purpose, "",
                                  "## Requirements", ""], {}, {}]
        _, requirements, status = specs[capability]

        def existing(name: str, section: str) -> str:
            if name not in requirements:
                raise ValueError(f"{delta_file}: {section} names the requirement '{name}', "
                                 f"which is not in the spec of '{capability}'")
            return name

        for old, new in sections.get("RENAMED", []):
            # Rebuild the dict so that the requirement keeps its place in the document.
            existing(old, "RENAMED")
            specs[capability][1] = requirements = {new if name == old else name: lines
                                                   for name, lines in requirements.items()}
            specs[capability][2] = status = {new if name == old else name: value
                                             for name, value in status.items()}
        for name in sections.get("REMOVED", {}):
            del requirements[existing(name, "REMOVED")]
            del status[name]
            removed.append(f"{capability}/{name}")
        for name, lines in sections.get("MODIFIED", {}).items():
            requirements[existing(name, "MODIFIED")] = lines
            status[name] = "modified"
        for name, lines in sections.get("ADDED", {}).items():
            if name in requirements:
                raise ValueError(f"{delta_file}: ADDED names the requirement '{name}', "
                                 f"which the spec of '{capability}' already has")
            requirements[name] = lines
            status[name] = "added"

    # Write everything into one document, and label the scenarios on the way.
    document, scenarios, changed_text = [], {}, []
    for capability, (preamble, requirements, status) in specs.items():
        document += preamble
        for name, lines in requirements.items():
            document += ["", f"### Requirement: {name}"]  # surplus blank lines are removed below
            headers = [index for index, line in enumerate(lines) if SCENARIO.match(line)]
            if status[name] != "existing":
                changed_text.append(_plain(" ".join(lines[:headers[0]] if headers else lines)))
            for index, line in enumerate(lines):
                if index in headers:
                    label = f"R{len(scenarios) + 1}"
                    scenario = SCENARIO.match(line).group(1)
                    scenarios[label] = {"capability": capability, "requirement": name,
                                        "scenario": scenario, "status": status[name]}
                    line = f"#### Scenario {label}: {scenario}"
                document.append(line)
        document.append("")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(document)).strip() + "\n"
    return Merged(change_dir.name, text, scenarios, [body for body in changed_text if body], removed)


def _requirements(lines: list[str]) -> tuple[list[str], dict]:
    """Split a spec into the lines before its first requirement, and {requirement name: its lines}.

    A requirement's lines run from below its "### Requirement:" header to the
    next such header (or the next delta section, or the end).
    """
    preamble, requirements, current = [], {}, None
    for line in lines:
        header = REQUIREMENT.match(line)
        if header:
            current = requirements.setdefault(header.group(1), [])
        elif SECTION.match(line):
            current = None
        elif current is not None:
            current.append(line)
        elif not requirements:
            preamble.append(line)
    return preamble, requirements


def _sections(lines: list[str]) -> dict:
    """Read a delta file: {"ADDED": {name: lines}, "MODIFIED": {...}, "REMOVED": {...},
    "RENAMED": [(old name, new name)], "PURPOSE": lines (only for a new capability)}."""
    found, kind, chunk = {}, "", []

    def close() -> None:
        if kind == "RENAMED":
            names = [RENAME.match(line).groups() for line in chunk if RENAME.match(line)]
            found[kind] = [(old, new) for (_, old), (_, new) in zip(names[0::2], names[1::2])]
        elif kind == "PURPOSE":
            found[kind] = [line for line in chunk if line.strip()]
        elif kind:
            found[kind] = _requirements(chunk)[1]

    for line in lines:
        section = SECTION.match(line)
        if section or line.strip().lower() == "## purpose":
            close()
            kind, chunk = (section.group(1).upper() if section else "PURPOSE"), []
        else:
            chunk.append(line)
    close()
    return found


def _plain(text: str) -> str:
    """Text without Markdown marks, case and extra spaces, for comparing two copies of a sentence."""
    return " ".join(re.sub(r"[*_`#]", "", text).lower().split())


def changed_rules(model: dict, merged: Merged) -> set[str]:
    """The ids of the rules in `model` that the change added or modified.

    Usually these are the labels of the added and modified scenarios. The read
    step may also take a requirement's SHALL sentence for a rule of its own;
    such a rule has no label, and it counts as changed when its text is the
    sentence of an added or modified requirement.

    Raises ValueError if a label is missing from the rules: then we cannot
    tell the rules of the change from the others.
    """
    ids = [rule["id"] for rule in model["rules"]]
    missing = [label for label in merged.scenarios if ids.count(label) != 1]
    if missing:
        raise ValueError(f"the read step did not keep the scenario labels {', '.join(missing)} "
                         f"(it returned the rules {', '.join(ids)})")
    changed = {label for label, scenario in merged.scenarios.items() if scenario["status"] != "existing"}
    for rule in model["rules"]:
        text = _plain(rule.get("text", ""))
        if rule["id"] not in merged.scenarios and text and any(text in body or body in text
                                                               for body in merged.changed_text):
            changed.add(rule["id"])
    return changed


def about_change(finding: dict, models: list[dict], changed: list[set]) -> bool:
    """Does this finding involve a rule that the change added or modified?

    models   the formal models (one for each symbol set)
    changed  for each model, the ids from changed_rules

    - conflict, scenario: one of its rules is changed
    - ambiguity: its rule is changed
    - gap: its event is one that a changed rule reacts to, as its trigger or in
      its condition. The gap in which no event happens belongs to no rule.
    """
    index = finding.get("model", 0)  # the model the finding's situation is written in
    model, ids = models[index], changed[index]
    if finding["type"] == "ambiguity":
        return finding["rule"] in ids
    if finding["type"] in ("conflict", "scenario"):
        return bool(ids & set(finding["rules"]))
    if finding["type"] == "gap" and "event" in finding:
        vocab = Vocabulary(model["symbols"])
        return any(finding["event"] in rule_events(vocab, rule)
                   for rule in model["rules"] if rule["id"] in ids)
    return False


def rule_events(vocab: Vocabulary, rule: dict) -> set[str]:
    """The events a rule reacts to: its trigger, and the events in its condition."""
    events = {rule.get("trigger")} & vocab.events
    try:
        events |= vocab.symbols_in(vocab.parse(rule.get("antecedent", "true"))) & vocab.events
    except ValueError:  # a rejected rule may have no formula that parses
        pass
    return events


def report_lines(merged: Merged, changed: set[str], left_out: int) -> tuple[list[str], list[str]]:
    """The two parts that a change adds to report.md: a note for the top, and the list of rules.

    changed   the changed rule ids of the first model
    left_out  how many findings were not selected (they involve existing rules only)
    """
    count = {status: sum(scenario["status"] == status for scenario in merged.scenarios.values())
             for status in ("added", "modified")}
    note = [f"Change `{merged.name}`, checked against the specs that exist: "
            f"{count['added']} scenario(s) added, {count['modified']} in modified requirements"
            + (f", {len(merged.removed)} requirement(s) removed ({', '.join(merged.removed)})"
               if merged.removed else "") + ".",
            "",
            f"Only findings that involve an added or modified rule ({', '.join(sorted(changed, key=_order))}) "
            f"are shown. {left_out} other finding(s), among the existing requirements alone, "
            "are in findings.json."]
    table = ["", "## The rules, by label", "",
             "| Rule | Spec | Requirement | Scenario | |", "|---|---|---|---|---|"]
    table += [f"| {label} | {scenario['capability']} | {scenario['requirement']} | {scenario['scenario']} "
              f"| {'' if scenario['status'] == 'existing' else '**' + scenario['status'] + '**'} |"
              for label, scenario in merged.scenarios.items()]
    return note, table


def _order(label: str) -> tuple:
    """Sort key that puts R2 before R10."""
    digits = re.sub(r"\D", "", label)
    return (int(digits) if digits else 0, label)
