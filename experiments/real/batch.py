"""Pick the real changes to run and lay them out as an evaluation set (no expected findings).

    python experiments/real/batch.py CASES OUT STEP OFFSET

The pool: changes our merge accepts, with at least 5 scenarios in the spec files they touch before
the change, at least one scenario added or reworded, and at most 60 scenarios in the merged document.
Of the pool, in date order, every STEP-th case starting at OFFSET is copied to OUT/<case>_real/.
"""
import json, shutil, sys
from pathlib import Path

root, out, step, offset = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rows = json.loads((root / "merge_check.json").read_text(encoding="utf-8"))
pool = sorted((r for r in rows if "error" not in r and r["before"] >= 5 and r["added"] + r["modified"] >= 1
               and r["scenarios"] <= 60), key=lambda r: r["case"])
picked = pool[offset::step]
shutil.rmtree(out, ignore_errors=True)
for row in picked:
    target = out / f"{row['case']}_real"
    shutil.copytree(root / row["case"] / "openspec", target / "openspec")
    (target / "expected.json").write_text(json.dumps({"conflicts": [], "gaps": [], "covered": []}) + "\n", encoding="utf-8")
(out / "picked.json").write_text(json.dumps(picked, indent=1), encoding="utf-8")
print("pool", len(pool), "| picked", len(picked), "| scenarios", sum(r["scenarios"] for r in picked),
      "| added", sum(r["added"] for r in picked), "modified", sum(r["modified"] for r in picked), "removed", sum(r["removed"] for r in picked))
for row in picked:
    print("  ", row["case"], row["scenarios"])
