"""Real changes that create a new spec, each also with one planted conflict: the set real4.

    python experiments/real/planted.py CASES OUT

CASES is the folder that history.py and merge_check.py made. Taken are the
changes our merge accepts that touch no existing scenario (the spec is new)
and add 14 to 31 scenarios: the ones that the pool of batch.py left out for
having nothing before them. Each is written twice:

    OUT/<case>_real/      the change as it is; nothing planted, no known answer
    OUT/<case>_planted/   the same, with one scenario of ours added to the change

The planted scenario (PLANTED below) repeats the condition of one scenario of
the change, word for word, and demands something that cannot hold together
with what that scenario demands. So the two clash, and expected.json names
the pair. That is the only known answer we have on real text.
"""
import json
import re
import shutil
import sys
from pathlib import Path

# case -> (spec file of the change, requirement and scenario that exist,
#          name of our requirement, its sentence, name of our scenario, what it demands)
PLANTED = {
    "2025-08-19-bulk-validation-interactive-selection": (
        "cli-validate", "Top-level validate command", "Non-interactive environments do not prompt",
        "Quiet default", "The CLI SHALL validate everything when it cannot ask.", "No arguments in a script",
        ["validate all changes and all specs", "exit with code 0"]),
    "2025-09-12-add-view-dashboard-command": (
        "cli-view", "Dashboard Display", "No OpenSpec directory",
        "Empty dashboard", "The dashboard SHALL be shown in any directory.", "Nothing to show",
        ["system displays an empty dashboard", "system displays no error message"]),
    "2025-11-06-add-shell-completions": (
        "cli-completion", "Shell Detection", "Non-Zsh shell detection",
        "Shell fallback", "The completion command SHALL work in every shell.", "Other shells use the Zsh script",
        ["generate the Zsh completion script", "do not throw an error"]),
    "2025-12-21-add-config-command": (
        "cli-config", "Config Get", "Get non-existent key",
        "Lenient lookup", "A missing key SHALL NOT be an error.", "Missing key is not an error",
        ["print `undefined`", "exit with code 0"]),
    "2025-12-24-add-artifact-graph-core": (
        "artifact-graph", "Schema Loading", "Cyclic dependencies detected",
        "Tolerant loading", "The system SHALL load every schema it can parse.", "Cycles are loaded",
        ["the system returns an ArtifactGraph with all artifacts and dependencies", "the system throws no error"]),
    "2025-12-25-add-change-manager": (
        "change-creation", "Change Creation", "Duplicate change rejected",
        "Idempotent creation", "Creating a change twice SHALL succeed.", "Existing change reused",
        ["the system returns the existing change directory", "the system throws no error"]),
    "2025-12-28-add-artifact-workflow-cli": (
        "cli-artifact-workflow", "Status Command", "Unknown change",
        "Status of a missing change", "The status command SHALL NOT fail for a change it does not know.", "Unknown change is empty",
        ["the system displays an empty status table", "the system displays no error"]),
    "2026-01-06-opsx-archive-command": (
        "opsx-archive-skill", "Task Completion Check", "No tasks file",
        "Tasks are required", "A change SHALL have a tasks file before it is archived.", "Missing tasks file",
        ["display a warning that the change has no tasks", "do not proceed"]),
    "2026-02-17-add-feedback-command": (
        "cli-feedback", "Error handling", "gh CLI execution failure",
        "Silent failure", "A failed submission SHALL NOT disturb the user.", "Failed submission is ignored",
        ["the system displays no error output", "exits with code 0"]),
    "2026-02-17-add-opsx-onboard-skill": (
        "opsx-onboard-skill", "Codebase Analysis for Task Suggestions", "Codebase scanning",
        "Fast onboarding", "Onboarding SHALL NOT read the codebase.", "No scan",
        ["agent does not scan the codebase", "agent asks the user to name a task"]),
    "2026-02-17-add-verify-skill": (
        "opsx-verify-skill", "Coherence Verification", "No design.md",
        "Design is mandatory", "Verification SHALL require a design.", "Missing design fails",
        ["run the design adherence check", "report a CRITICAL issue"]),
    "2026-10-19-add-update-workflow": (
        "opsx-update-skill", "Update Workflow Command", "Revise without advancing the frontier",
        "Complete on update", "An update SHALL leave no artifact missing.", "Missing artifacts are created",
        ["the skill updates that artifact", "it creates every artifact of the schema that does not yet exist"]),
    "2026-10-19-add-version-command": (
        "cli-version", "Report the installed version", "Source checkout",
        "Default scope", "The scope SHALL always name a package manager.", "Checkout reported as global",
        ["the command reports `scope` as `global`", "it names npm as the package manager that owns the checkout"]),
}

README = """# real4: 13 changes of a real OpenSpec project, each also with one planted conflict (held-out in E27)

Except for the planted scenarios, these files are not ours. They are archived
changes of the OpenSpec tool's own repository,
https://github.com/Fission-AI/OpenSpec, as of commit
f1cd852f4edce22b8df9548a4df889172ca8ff25 (2026-11-24). That project is under
the MIT licence; its text is in `LICENSE-OpenSpec`.

Each of the 13 changes creates a new spec (14 to 31 scenarios), so there is no
spec file before it. They are the changes that the pool of `real1` to `real3`
left out for that reason (`experiments/real/planted.py` writes this set). Each
is here twice:

| Folder | What it is |
|---|---|
| `<case>_real/` | the change as it is. `expected.json` is empty: nobody planted anything, so there is no known answer |
| `<case>_planted/` | the same change with one scenario of ours added at the end of its ADDED section. It repeats the condition of an existing scenario word for word and demands something that cannot hold together with what that scenario demands. `expected.json` names the pair |

In a folder:

| Path | What it is |
|---|---|
| `openspec/changes/<change>/specs/<name>/spec.md` | the change: its ADDED section is the whole new spec |
| `after/<name>/spec.md` | only in `<case>_real/`: the spec after the commit that archived the change, as the project's own tool wrote it |
| `expected.json` | the planted conflict, or nothing |

The planted scenarios, and the scenario each one clashes with, are listed in
`experiments/real/planted.py`.
"""


def scenario_condition(text: str, requirement: str, scenario: str) -> list[str]:
    """The lines of a scenario up to its THEN: its GIVEN, WHEN and the ANDs that follow them."""
    in_requirement = in_scenario = False
    lines = []
    for line in text.splitlines():
        if line.startswith("### Requirement:"):
            in_requirement, in_scenario = line[len("### Requirement:"):].strip() == requirement, False
        elif line.startswith("#### Scenario:"):
            in_scenario = in_requirement and line[len("#### Scenario:"):].strip() == scenario
        elif in_scenario and re.match(r"\s*-\s*\*\*THEN\*\*", line):
            return lines
        elif in_scenario and re.match(r"\s*-\s*\*\*(GIVEN|WHEN|AND)\*\*", line):
            lines.append(line.strip())
    raise ValueError(f"no scenario {requirement!r} / {scenario!r} with a THEN")


def with_planted(text: str, block: str) -> str:
    """The change file with our requirement at the end of its ADDED section."""
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "## ADDED Requirements")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[:end] + ["", *block.splitlines(), ""] + lines[end:]) + "\n"


if __name__ == "__main__":
    cases, out = Path(sys.argv[1]), Path(sys.argv[2])
    rows = json.loads((cases / "merge_check.json").read_text(encoding="utf-8"))
    picked = sorted((row for row in rows if "error" not in row and row["before"] == 0 and 14 <= row["scenarios"] <= 31),
                    key=lambda row: row["case"])
    assert {row["case"] for row in picked} == set(PLANTED), "PLANTED does not name the changes that were picked"
    shutil.rmtree(out, ignore_errors=True)
    for row in picked:
        case = row["case"]
        spec, requirement, scenario, our_requirement, sentence, our_scenario, demands = PLANTED[case]
        plain = out / f"{case}_real"
        shutil.copytree(cases / case / "openspec", plain / "openspec")
        shutil.copytree(cases / case / "after", plain / "after")
        (plain / "expected.json").write_text(json.dumps({"conflicts": [], "gaps": [], "covered": []}) + "\n", encoding="utf-8")

        planted = out / f"{case}_planted"
        shutil.copytree(cases / case / "openspec", planted / "openspec")
        (file,) = planted.glob(f"openspec/changes/*/specs/{spec}/spec.md")
        text = file.read_text(encoding="utf-8")
        condition = scenario_condition(text, requirement, scenario)
        then = [f"- **THEN** {demands[0]}"] + [f"- **AND** {more}" for more in demands[1:]]
        block = "\n".join([f"### Requirement: {our_requirement}", sentence, "", f"#### Scenario: {our_scenario}", *condition, *then])
        file.write_text(with_planted(text, block), encoding="utf-8", newline="\n")
        pair = [f"{spec}/{requirement}/{scenario}", f"{spec}/{our_requirement}/{our_scenario}"]
        (planted / "expected.json").write_text(json.dumps({"conflicts": [pair], "gaps": [], "covered": []}) + "\n", encoding="utf-8")
        print(f"{case}: {row['scenarios']} scenarios | planted against {requirement} / {scenario}")
    (out / "README.md").write_text(README, encoding="utf-8", newline="\n")
    print(f"wrote {len(picked)} changes, each plain and planted, to {out}")
