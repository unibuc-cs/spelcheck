"""Rebuild, from the history of a cloned OpenSpec project, each archived change next to the specs as
they were just before it. Reads the repository with git only; nothing in it is run.

    python experiments/real/history.py REPO OUT

For every folder openspec/changes/archive/<date>-<name>:
    A      the commit that added it (the archive commit)
    A^     its parent: the change is still active there, and the specs do not have it yet
A case is written to OUT/<date>-<name>/ as an OpenSpec project of its own:
    openspec/specs/<capability>/spec.md              the spec files the change touches, as of A^
    openspec/changes/<name>/specs/<capability>/...   the delta files, as of A (the archived copy)
    after/<capability>/spec.md                       the same spec files as of A, for comparison
and a line about it goes to OUT/cases.json.
"""
import json
import subprocess
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])


def git(*args: str) -> str | None:
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    return done.stdout.decode("utf-8", errors="replace") if done.returncode == 0 else None


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


archive = "openspec/changes/archive"
cases = []
for folder in git("ls-tree", "-d", "--name-only", "HEAD", archive + "/").split():
    dated = folder.rsplit("/", 1)[1]
    name = dated[11:] if dated[:4].isdigit() and dated[4] == "-" else dated
    case = {"case": dated, "name": name}
    added = git("log", "--diff-filter=A", "--format=%H", "--reverse", "--", folder)
    if not added or not added.split():
        cases.append({**case, "skipped": "no commit adds it"})
        continue
    commit = added.split()[0]
    before = commit + "^"
    deltas = [path for path in (git("ls-tree", "-r", "--name-only", commit, folder + "/specs") or "").split("\n")
              if path.endswith("/spec.md")]
    case.update(commit=commit[:10], date=(git("log", "-1", "--format=%ad", "--date=short", commit) or "").strip(),
                active_before=git("ls-tree", "-d", "--name-only", before, f"openspec/changes/{name}") not in (None, ""),
                capabilities=[path.split("/")[-2] for path in deltas])
    if not deltas:
        cases.append({**case, "skipped": "no delta specs"})
        continue
    root = out / dated
    new_capabilities = []
    for path in deltas:
        capability = path.split("/")[-2]
        write(root / "openspec" / "changes" / name / "specs" / capability / "spec.md", git("show", f"{commit}:{path}"))
        old = git("show", f"{before}:openspec/specs/{capability}/spec.md")
        if old is None:
            new_capabilities.append(capability)
        else:
            write(root / "openspec" / "specs" / capability / "spec.md", old)
        new = git("show", f"{commit}:openspec/specs/{capability}/spec.md")
        if new is not None:
            write(root / "after" / capability / "spec.md", new)
    proposal = git("show", f"{commit}:{folder}/proposal.md")
    if proposal:
        write(root / "openspec" / "changes" / name / "proposal.md", proposal)
    (root / "openspec" / "specs").mkdir(parents=True, exist_ok=True)
    cases.append({**case, "new_capabilities": new_capabilities})

write(out / "cases.json", json.dumps(cases, indent=1))
print(len(cases), "archived changes;", sum("skipped" not in c for c in cases), "written;",
      sum(c.get("active_before", False) for c in cases), "were active in the commit before their archive")
