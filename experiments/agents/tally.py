"""tally.py: what speccheck reports on the changes of one project, as one table. No LLM.

    python -m experiments.agents.tally CHANGES OUT [OUT ...]

CHANGES  the folder that holds the changes of the project (openspec/changes)
OUT      a folder that `speccheck --change CHANGES/<name> --out OUT` wrote; or a
         folder of such folders

The reports of a large project are long, and what tells its changes apart is
not the number of conflicts. So for each change this prints one row:

    Conflicts, not doubtful            how many, and of them
      among the rules of the change    with the parts that found each ("16/24"):
                                       the rules of the change are translated once
                                       for each part, so this count says how far a
                                       conflict depends on the symbols
      with a rule of another spec file each is found in the part of that file
    Doubtful                           conflicts with a mark (checks.is_doubtful)
    Ambiguous, not checked             rules of the change

It reads findings.json and report.md of each folder, and the change itself for
the spec files that it touches.
"""

import json
import re
import sys
from pathlib import Path

from speccheck.change import merge
from speccheck.checks import is_doubtful


def row(changes: Path, out: Path) -> str:
    """The table row for the change that the report in `out` is about."""
    report = (out / "report.md").read_text(encoding="utf-8")
    name = re.match(r"# Requirements analysis: (.+)", report).group(1).strip()
    parts = re.search(r"analysed in (\d+) part", report)
    change = changes / name
    touched = {delta.parent.relative_to(change / "specs").as_posix() for delta in (change / "specs").glob("**/spec.md")}
    own = {label for label, scenario in merge(change).scenarios.items() if scenario["capability"] in touched}
    findings = [f for f in json.loads((out / "findings.json").read_text(encoding="utf-8")) if f.get("about_change")]
    conflicts = [f for f in findings if f["type"] == "conflict"]
    plain = [f for f in conflicts if not is_doubtful(f)]
    inside = [f for f in plain if own.issuperset(f["rules"])]
    # Best supported first; a conflict of a project that fits one document has no count.
    counts = sorted((f.get("parts", "1/1") for f in inside), key=lambda count: -int(count.split("/")[0]))
    ambiguous = [f for f in findings if f["type"] == "ambiguity"]
    unchecked = sum(f.get("found_by") == "empty" for f in ambiguous)
    return (f"| {name} | {parts.group(1) if parts else 1} | {len(plain)} | {len(inside)}"
            + (f" ({', '.join(counts)})" if counts else "")
            + f" | {len(plain) - len(inside)} | {len(conflicts) - len(plain)} | {len(ambiguous) - unchecked} | {unchecked} |")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    changes = Path(sys.argv[1])
    folders = []
    for given in map(Path, sys.argv[2:]):
        folders += [given] if (given / "findings.json").exists() else sorted(
            folder for folder in given.iterdir() if (folder / "findings.json").exists())
    print("| Change | Parts | Conflicts, not doubtful | Among the rules of the change (parts that found each) "
          "| With a rule of another spec file | Doubtful | Ambiguous rules | Rules not checked |")
    print("|---|---|---|---|---|---|---|---|")
    for folder in folders:
        print(row(changes, folder))


if __name__ == "__main__":
    main()
