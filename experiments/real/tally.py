"""What the conflicts about the real changes rest on, and the ones proven from the rules alone."""
import json, sys
from collections import Counter
from experiments.evaluate import DEFAULT, findings_of, merged_of
from speccheck.change import about_change, after_model, changed_rules

data = json.load(open(sys.argv[1], encoding="utf-8"))
rest, per_case, gaps, amb, rules_n, changed_n = Counter(), {}, [], Counter(), 0, 0
plain = []
for run in data["runs"]:
    if "models" not in run:
        continue
    spec = data["specs"][run["spec"]]
    merged = merged_of(spec)
    changed = [changed_rules(m, merged) for m in run["models"]]
    models, findings = findings_of({**run, "models": [after_model(m, merged) for m in run["models"]]}, DEFAULT)
    mine = [f for f in findings if about_change(f, models, changed)]
    rules = {r["id"]: r for r in models[0]["rules"]}
    facts = {f["id"]: f for f in models[0].get("background", [])}
    rules_n += len(rules); changed_n += len(changed[0])
    c = Counter()
    for f in mine:
        c[f["type"]] += 1
        if f["type"] == "conflict":
            kinds = {"link" if "restates" in facts[i] else "pair question" if "between" in facts[i] else "voted fact" for i in f.get("facts", [])}
            rest[" + ".join(sorted(kinds)) or "the rules alone"] += 1
            if not f.get("facts"):
                plain.append((run["spec"], f, rules))
        if f["type"] == "gap":
            gaps.append((run["spec"], f))
    per_case[run["spec"]] = dict(c)
    amb[run["spec"]] = sum(r["status"] != "accepted" for r in rules.values())
print("runs:", len(per_case), "| rules:", rules_n, "| rules of the changes:", changed_n)
print("conflicts about the change rest on:", dict(rest))
print("changes with at least one conflict about them:", sum("conflict" in c for c in per_case.values()), "| with a gap:", sum("gap" in c for c in per_case.values()),
      "| with an ambiguity:", sum("ambiguity" in c for c in per_case.values()), "| with nothing:", sum(not c for c in per_case.values()))
print("rules not accepted (ambiguous or rejected), all rules:", sum(amb.values()))
for spec, f, rules in plain:
    print(f"\n-- from the rules alone: {spec} {f['rules']} doubtful {bool(f.get('doubted_by') or f.get('simultaneous_events'))} | when {str(f['when'])[:160]}")
    for rid in f["rules"]:
        print(f"     {rid}: {rules[rid]['text'][:260]}")
        print(f"         {rules[rid]['antecedent'][:120]} => {rules[rid]['consequent'][:150]}")
print()
for spec, f in gaps:
    print(f"gap in {spec[:44]} | event {f.get('event')} | opened_by {f.get('opened_by')} | doubtful {bool(f.get('doubted_by'))} | when {str(f['when'])[:170]}")
