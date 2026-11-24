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
steps around the usual pipeline (cli.py, with --change):

1. merge(): apply the change to the specs, as `openspec archive` would, and
   write everything into ONE document. Every scenario gets a label, R1, R2,
   ..., written into its header ("#### Scenario R4: Lockout threshold"). The
   read step uses a document's own labels as rule ids, so afterwards we know
   which rules the change added or modified.
   The scenarios that the change removes stay in that document, with labels
   of their own, X1, X2, ... They are formalized with the same symbols as the
   rest, which is what step 3 needs.
2. The merged document is formalized like any spec.
3. after_model(): the removed rules are taken out of the formal model and
   kept apart in it ("removed_rules"). The checks run on what is left. The
   removed rules cannot cause or hide a finding; they serve one question
   (checks.find_gaps): is there a situation that a removed rule covered and
   that no rule covers now? That gap was opened by the change.
4. about_change(): keep the findings that involve the change. A conflict
   among requirements that existed before is not the change's fault.

A delta file has up to four sections, applied in this order:

    ## RENAMED Requirements     - FROM: `### Requirement: Old name`
                                - TO: `### Requirement: New name`
    ## REMOVED Requirements     ### Requirement: <name>      (the text below it is a reason)
    ## MODIFIED Requirements    ### Requirement: <name>      (the full new text)
    ## ADDED Requirements       ### Requirement: <name>      (the full text)

Requirements are matched by their name, and inside a MODIFIED requirement the
scenarios are matched by theirs. So a scenario has one of four states:

    existing   it was there, and its text is the same (also inside a
               requirement that the change rewrites)
    modified   it was there, with another text
    added      it is new
    removed    its requirement is REMOVED, or the new text of its MODIFIED
               requirement has no scenario of that name

A capability that has no spec yet gets one from its ADDED requirements.
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
    """The specs with a change applied, as one document. Plain data, so that it can be saved as JSON."""
    name: str           # the change's folder name
    text: str           # the document; every scenario header carries its label
    scenarios: dict     # label -> {"capability", "requirement", "scenario", "status"};
    #                     status is "existing", "added", "modified" or "removed"
    changed_text: list  # the text above the first scenario (the SHALL sentence) of each
    #                     added requirement, and of each modified one where it changed
    removed: list       # "capability/requirement" for each requirement the change removes
    removed_text: list = ()  # the SHALL sentence of each removed requirement


class _Requirement(NamedTuple):
    """One requirement of a spec, while the change is applied."""
    sentence: list   # the lines above its first scenario
    scenarios: list  # (name, lines below the header, status), in document order
    status: str      # "existing", "added", "removed", or "modified": its sentence has new words


def merge(change_dir: Path) -> Merged:
    """Apply the change in `change_dir` to its project's specs; return them as one labelled document.

    change_dir is openspec/changes/<name>; the specs are in openspec/specs,
    two folders up. A delta that names a requirement which does not exist (or
    adds one that does) raises ValueError, as `openspec archive` refuses it.
    """
    specs_dir = change_dir.parent.parent / "specs"
    specs = {}  # capability -> [the lines before its first requirement, {requirement name: _Requirement}]
    for spec_file in sorted(specs_dir.glob("**/spec.md")):
        capability = spec_file.parent.relative_to(specs_dir).as_posix()
        preamble, requirements = _requirements(spec_file.read_text(encoding="utf-8").splitlines())
        specs[capability] = [preamble, {name: _parsed(lines, "existing") for name, lines in requirements.items()}]

    for delta_file in sorted((change_dir / "specs").glob("**/spec.md")):
        capability = delta_file.parent.relative_to(change_dir / "specs").as_posix()
        sections = _sections(delta_file.read_text(encoding="utf-8").splitlines())
        if capability not in specs:  # a new capability: only ADDED makes sense
            purpose = sections.get("PURPOSE") or ["(new with this change)"]
            specs[capability] = [[f"# {capability} Specification", "", "## Purpose", "", *purpose, "",
                                  "## Requirements", ""], {}]
        requirements = specs[capability][1]

        def existing(name: str, section: str) -> str:
            if name not in requirements or requirements[name].status == "removed":
                raise ValueError(f"{delta_file}: {section} names the requirement '{name}', "
                                 f"which is not in the spec of '{capability}'")
            return name

        for old, new in sections.get("RENAMED", []):
            # Rebuild the dict so that the requirement keeps its place in the document.
            existing(old, "RENAMED")
            specs[capability][1] = requirements = {new if name == old else name: requirement
                                                   for name, requirement in requirements.items()}
        for name in sections.get("REMOVED", {}):
            # It stays in the document, marked: step 3 of the module docstring needs its rules.
            gone = requirements[existing(name, "REMOVED")]
            requirements[name] = _Requirement(gone.sentence, [(scenario, lines, "removed")
                                                              for scenario, lines, _ in gone.scenarios], "removed")
        for name, lines in sections.get("MODIFIED", {}).items():
            requirements[name] = _rewritten(requirements[existing(name, "MODIFIED")], _parsed(lines, "added"))
        for name, lines in sections.get("ADDED", {}).items():
            if name in requirements and requirements[name].status != "removed":
                raise ValueError(f"{delta_file}: ADDED names the requirement '{name}', "
                                 f"which the spec of '{capability}' already has")
            requirements[name] = _parsed(lines, "added")

    # Write everything into one document, and label the scenarios on the way:
    # R1, R2, ... for those that are in the specs after the change, X1, X2, ...
    # for those that the change removes.
    document, scenarios, changed_text, removed, removed_text = [], {}, [], [], []
    count = {"R": 0, "X": 0}
    for capability, (preamble, requirements) in specs.items():
        document += preamble
        for name, requirement in requirements.items():
            document += ["", f"### Requirement: {name}", *requirement.sentence]  # surplus blank lines go below
            sentence = _plain(" ".join(requirement.sentence))
            if requirement.status == "removed":
                removed.append(f"{capability}/{name}")
                removed_text.append(sentence)
            elif requirement.status == "added" or (requirement.status == "modified" and sentence):
                changed_text.append(sentence)
            for scenario, lines, status in requirement.scenarios:
                letter = "X" if status == "removed" else "R"
                count[letter] += 1
                label = f"{letter}{count[letter]}"
                scenarios[label] = {"capability": capability, "requirement": name,
                                    "scenario": scenario, "status": status}
                document += [f"#### Scenario {label}: {scenario}", *lines]
        document.append("")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(document)).strip() + "\n"
    return Merged(change_dir.name, text, scenarios, [body for body in changed_text if body], removed,
                  [body for body in removed_text if body])


def _parsed(lines: list[str], status: str) -> _Requirement:
    """The lines below a requirement's header, split into its sentence and its scenarios."""
    sentence, scenarios = [], []
    for line in lines:
        header = SCENARIO.match(line)
        if header:
            scenarios.append((header.group(1), [], status))
        elif scenarios:
            scenarios[-1][1].append(line)
        else:
            sentence.append(line)
    return _Requirement(sentence, scenarios, status)


def _rewritten(old: _Requirement, new: _Requirement) -> _Requirement:
    """A MODIFIED requirement: its new text, with the state of every scenario.

    A scenario of the new text is "existing" when the old text has one of the
    same name with the same words, "modified" when the words differ, "added"
    when the name is new. A scenario that only the old text has is kept at the
    end, as "removed". The sentence of the requirement counts as changed (see
    Merged.changed_text) only if its words differ.
    """
    before = {scenario: lines for scenario, lines, _ in old.scenarios}
    scenarios = []
    for scenario, lines, _ in new.scenarios:
        if scenario not in before:
            status = "added"
        else:
            same = _plain(" ".join(before[scenario])) == _plain(" ".join(lines))
            status = "existing" if same else "modified"
        scenarios.append((scenario, lines, status))
    kept = {scenario for scenario, _, _ in new.scenarios}
    scenarios += [(scenario, lines, "removed") for scenario, lines, _ in old.scenarios if scenario not in kept]
    # The state of the requirement itself says whether its sentence changed.
    same_sentence = _plain(" ".join(old.sentence)) == _plain(" ".join(new.sentence))
    return _Requirement(new.sentence, scenarios, "existing" if same_sentence else "modified")


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


def _is_sentence_of(rule: dict, sentences: list[str]) -> bool:
    """Is this rule one of these requirement sentences, taken by the read step for a rule of its own?"""
    text = _plain(rule.get("text", ""))
    return bool(text) and any(text in sentence or sentence in text for sentence in sentences)


def changed_rules(model: dict, merged: Merged) -> set[str]:
    """The ids of the rules in `model` that the change added or modified.

    model is the formal model of the merged document, as the LLM made it.
    Usually the changed rules are the labels of the added and modified
    scenarios. The read step may also take a requirement's SHALL sentence for
    a rule of its own; such a rule has no label, and it counts as changed when
    its text is the sentence of an added requirement, or the new sentence of a
    modified one.

    Raises ValueError if a label is missing from the rules: then we cannot
    tell the rules of the change from the others.
    """
    ids = [rule["id"] for rule in model["rules"]]
    missing = [label for label in merged.scenarios if ids.count(label) != 1]
    if missing:
        raise ValueError(f"the read step did not keep the scenario labels {', '.join(missing)} "
                         f"(it returned the rules {', '.join(ids)})")
    changed = {label for label, scenario in merged.scenarios.items()
               if scenario["status"] in ("added", "modified")}
    changed |= {rule["id"] for rule in model["rules"]
                if rule["id"] not in merged.scenarios and _is_sentence_of(rule, merged.changed_text)}
    return changed


def after_model(model: dict, merged: Merged) -> dict:
    """The formal model of the specs after the change: the removed rules taken out, and kept apart.

    model is the formal model of the merged document. Returned is a model
    without the rules of the removed scenarios (and without the SHALL sentence
    of a removed requirement, if the read step made a rule of it), without the
    links and the facts about pairs of outcomes that came from them, and with
    those rules under "removed_rules". checks.analyze uses "removed_rules"
    for one thing: to see which gap the change opened.
    """
    gone = {label for label, scenario in merged.scenarios.items() if scenario["status"] == "removed"}
    gone |= {rule["id"] for rule in model["rules"]
             if rule["id"] not in merged.scenarios and _is_sentence_of(rule, list(merged.removed_text))}
    if not gone:
        return model
    return {
        **model,
        "rules": [rule for rule in model["rules"] if rule["id"] not in gone],
        "removed_rules": [rule for rule in model["rules"] if rule["id"] in gone],
        # A link restates one rule ("restates"); a fact of probe check 4 is about two ("between").
        "background": [fact for fact in model.get("background", [])
                       if fact.get("restates") not in gone and not gone & set(fact.get("between", []))],
    }


def about_change(finding: dict, models: list[dict], changed: list[set]) -> bool:
    """Does this finding involve the change?

    models   the formal models after the change (after_model), one for each symbol set
    changed  for each model, the ids from changed_rules

    - conflict, scenario: one of its rules is added or modified
    - ambiguity: its rule is added or modified
    - gap: a removed rule covered its situation ("opened_by", from
      checks.find_gaps); or its event is one that an added or modified rule
      reacts to, as its trigger or in its condition. The gap in which no
      event happens belongs to no rule.
    """
    index = finding.get("model", 0)  # the model the finding's situation is written in
    model, ids = models[index], changed[index]
    if finding["type"] == "ambiguity":
        return finding["rule"] in ids
    if finding["type"] in ("conflict", "scenario"):
        return bool(ids & set(finding["rules"]))
    if finding["type"] == "gap" and finding.get("opened_by"):
        return True
    if finding["type"] == "gap" and "event" in finding:
        vocab = Vocabulary(model["symbols"])
        return any(finding["event"] in vocab.events_of(rule)
                   for rule in model["rules"] if rule["id"] in ids)
    return False


def report_lines(merged: Merged, changed: set[str], left_out: int) -> tuple[list[str], list[str]]:
    """The two parts that a change adds to report.md: a note for the top, and the list of rules.

    changed   the changed rule ids of the first model
    left_out  how many findings were not selected (they involve existing rules only)
    """
    labels = {status: [label for label, scenario in merged.scenarios.items() if scenario["status"] == status]
              for status in ("added", "modified", "removed")}
    note = [f"Change `{merged.name}`, checked against the specs that exist: "
            f"{len(labels['added'])} scenario(s) added, {len(labels['modified'])} modified, "
            f"{len(labels['removed'])} removed"
            + (f" (requirements removed: {', '.join(merged.removed)})" if merged.removed else "") + ".",
            "",
            "Shown are the findings that involve an added or modified rule"
            + (f" ({', '.join(sorted(changed, key=_order))})" if changed else "")
            + (f", and the gaps that a removed rule ({', '.join(labels['removed'])}) leaves open"
               if labels["removed"] else "")
            + f". {left_out} other finding(s), among the existing requirements alone, are in findings.json."]
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
