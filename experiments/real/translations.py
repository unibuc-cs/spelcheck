"""Why do the eight translations of a rule disagree? Reads the translations saved in a result file. No LLM.

    python -m experiments.real.translations RESULT.json [RESULT.json ...]

Every rule is translated eight times with the symbols that the read step
listed (formalize.py, steps 1 to 3). This script looks at what the eight say:

    answers that are not formulas    "and a b" without parentheses, a symbol that is not listed
    a translation that demands       its "then" part is always true (or always false): the model
    nothing                          understood the rule and found no symbol for what it demands
    symbols for each outcome         how many symbols that are not events the read step listed,
                                     against how many outcomes the rules have ("THEN a AND b AND c" is 3)

and, for each rule without an agreed translation (status ambiguous or
rejected), in what its translations differ. The first that fits:

    no symbol for the outcome        some translation demands nothing
    different symbols                the translations use other symbols for what is demanded
    the same symbols, combined       and / or / a condition inside, with the same symbols
    differently
    only the condition               they agree on what is demanded, not on when
"""
import json
import re
import sys
from collections import Counter

import z3

from speccheck.logic import Vocabulary


def outcomes(text: str) -> int:
    """How many things the rule demands: 1 + the number of "AND" after its THEN."""
    after = re.split(r"\bTHEN\b", text, maxsplit=1)
    return 1 + len(re.findall(r"\bAND\b", after[1])) if len(after) == 2 else 1


def empty(vocab: Vocabulary, formula) -> bool:
    """Does this "then" part say nothing: always true, or never true?"""
    return vocab.impossible([z3.Not(formula)]) or vocab.impossible([formula])


def meanings(vocab: Vocabulary, formulas: list) -> list:
    """One formula for each distinct meaning among `formulas`."""
    kept = []
    for formula in formulas:
        if not any(vocab.impossible([z3.Xor(formula, other)]) for other in kept):
            kept.append(formula)
    return kept


def cause(vocab: Vocabulary, rule: dict, names: set) -> str:
    """In what the translations of a rule without an agreed translation differ (see the module docstring)."""
    parsed = []
    for sample in rule["samples"]:
        try:
            used = frozenset(set(re.findall(r"[a-z_][a-z0-9_]*", sample["consequent"])) & names)
            parsed.append((vocab.parse(sample["antecedent"]), vocab.parse(sample["consequent"]), used))
        except Exception:  # not a formula over the listed symbols
            pass
    if len(parsed) < 2:
        return "too few usable answers"
    demanded = meanings(vocab, [then for _, then, _ in parsed])
    if any(empty(vocab, then) for then in demanded):
        return "no symbol for the outcome"
    if len(demanded) == 1:
        return "only the condition"
    if len({used for _, _, used in parsed}) > 1:
        return "different symbols"
    return "the same symbols, combined differently"


def main() -> None:
    for path in sys.argv[1:]:
        data = json.load(open(path, encoding="utf-8"))
        status, causes, hollow = Counter(), Counter(), Counter()
        answers = malformed = with_malformed = 0
        specs = []
        for run in data["runs"]:
            for model in run.get("models", [])[:1]:
                vocab = Vocabulary(model["symbols"])
                names = {symbol["name"] for symbol in model["symbols"]}
                rules = [rule for rule in model["rules"] if "samples" in rule]
                row = {"spec": run["spec"], "rules": len(rules), "outcomes": sum(outcomes(rule["text"]) for rule in rules),
                       "symbols": sum(not symbol.get("event") for symbol in model["symbols"]), "hollow": 0, "open": 0}
                for rule in rules:
                    status[rule["status"]] += 1
                    bad = 0
                    for sample in rule["samples"]:
                        try:
                            vocab.parse(sample["antecedent"]), vocab.parse(sample["consequent"])
                        except Exception:
                            bad += 1
                    answers, malformed, with_malformed = answers + len(rule["samples"]), malformed + bad, with_malformed + (bad > 0)
                    try:  # the translation that was chosen for the rule
                        if empty(vocab, vocab.parse(rule["consequent"])):
                            hollow[rule["status"]] += 1
                            row["hollow"] += 1
                    except Exception:
                        pass
                    if rule["status"] != "accepted":
                        row["open"] += 1
                        causes[cause(vocab, rule, names)] += 1
                specs.append(row)

        total = sum(status.values())
        print(f"\n== {path}\n   {total} rules: {dict(status)}")
        if not total:  # no run of this file finished
            continue
        print(f"   answers that are not formulas over the listed symbols: {malformed} of {answers} "
              f"({100 * malformed / answers:.1f}%), in {with_malformed} rules")
        print(f"   rules whose chosen translation demands nothing: {sum(hollow.values())} {dict(hollow)}")
        useless = total - status["accepted"] + hollow["accepted"]
        print(f"   rules of no use to the checks (no agreed translation, or one that demands nothing): "
              f"{useless} of {total} ({100 * useless / total:.0f}%)")
        print(f"   the {total - status['accepted']} rules without an agreed translation, by what their translations differ in:")
        for name, count in causes.most_common():
            print(f"      {count:4}  {name}")
        print("   by spec (symbols = those that are not events):")
        print(f"      {'rules':>5} {'outcomes':>8} {'symbols':>7} {'per outcome':>11} {'demand nothing':>14} {'not agreed':>10}")
        specs.sort(key=lambda row: row["symbols"] / row["outcomes"])
        shown = specs if len(specs) <= 16 else specs[:: len(specs) // 8]
        for row in shown:
            print(f"      {row['rules']:5} {row['outcomes']:8} {row['symbols']:7} {row['symbols'] / row['outcomes']:11.2f} "
                  f"{row['hollow']:14} {row['open']:10}   {row['spec'][:48]}")


if __name__ == "__main__":
    main()
