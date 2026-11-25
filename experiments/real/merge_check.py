"""Does speccheck's merge do to the specs what the project's own archive step did? No LLM.

    python experiments/real/merge_check.py CASES

For each case of history.py: apply the change to the specs as they were before (change.merge), and
compare the scenarios that result with those of the spec files after the archive commit.
"""
import json
import sys
from collections import Counter
from pathlib import Path

from speccheck.change import base_document, merge

root = Path(sys.argv[1])
cases = json.loads((root / "cases.json").read_text(encoding="utf-8"))
rows, errors = [], Counter()
for case in cases:
    if "skipped" in case:
        continue
    folder = root / case["case"]
    row = {"case": case["case"], "capabilities": len(case["capabilities"])}
    try:
        row["before"] = len(base_document(folder / "openspec" / "specs").scenarios) if any((folder / "openspec" / "specs").iterdir()) else 0
        merged = merge(folder / "openspec" / "changes" / case["name"])
    except Exception as error:  # a file our parser or merge does not accept
        row["error"] = f"{type(error).__name__}: {error}"[:160]
        errors[row["error"].split(":")[1].strip()[:40]] += 1
        rows.append(row)
        continue
    states = Counter(s["status"] for s in merged.scenarios.values())
    row.update(scenarios=len(merged.scenarios), added=states["added"], modified=states["modified"],
               removed=states["removed"], characters=len(merged.text))
    ours = {(s["capability"], s["requirement"], s["scenario"]) for s in merged.scenarios.values() if s["status"] != "removed"}
    if (folder / "after").exists() and any((folder / "after").iterdir()):
        try:
            after = base_document(folder / "after")
            theirs = {(s["capability"], s["requirement"], s["scenario"]) for s in after.scenarios.values()}
            row["same_as_archive"] = ours == theirs
            row["only_ours"], row["only_theirs"] = len(ours - theirs), len(theirs - ours)
        except Exception as error:
            row["after_error"] = f"{type(error).__name__}: {error}"[:120]
    rows.append(row)

(root / "merge_check.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
good = [r for r in rows if "error" not in r]
print(len(rows), "cases |", len(good), "merged |", len(rows) - len(good), "refused")
for row in rows:
    if "error" in row:
        print("   refused:", row["case"], "|", row["error"][:130])
compared = [r for r in good if "same_as_archive" in r]
print("compared with the archive's own result:", len(compared), "| the same scenarios:", sum(r["same_as_archive"] for r in compared))
for r in compared:
    if not r["same_as_archive"]:
        print("   differs:", r["case"], "| only ours", r["only_ours"], "| only theirs", r["only_theirs"])
sizes = sorted(r["scenarios"] for r in good)
print("scenarios in the merged document: min", sizes[0], "median", sizes[len(sizes) // 2], "max", sizes[-1],
      "| at most 140:", sum(s <= 140 for s in sizes))
print("changes with something added or modified:", sum(r["added"] + r["modified"] > 0 for r in good),
      "| that remove a scenario:", sum(r["removed"] > 0 for r in good))
