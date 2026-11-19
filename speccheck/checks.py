"""checks.py: stage 2, the formal analysis. Z3 only, no LLM.

Input : a formal.json dict (symbols + background + rules, see plan.md section 6).
Output: a list of findings, each a plain dict ready for findings.json:

    {"type": "conflict",  "rules": [...], "when": {...}}
    {"type": "conflict",  "rules": [...], "facts": [...], "when": {...}}
    {"type": "gap",       "when": {...}}
    {"type": "ambiguity", "rule": "...", "status": ..., "found_by": ...,
                          "readings": [...], "differs_when": {...}}

"when" is a witness: a concrete situation (symbol -> value) the user can read.
A conflict with a "facts" list holds only if those assumed facts are true; a
conflict without one is proven from the requirements alone. A conflict that
is likely a false alarm is kept but marked doubtful, with "doubted_by" (see
find_conflicts) or "simultaneous_events" (see _simultaneous_events).

Three entry points:

    analyze         the defects of one formal.json: ambiguities, conflicts, gaps
    find_scenarios  behaviours one formal.json allows or forbids (not defects)
    combine         merges the findings of several formal models of one document

Every rule is an implication `antecedent => consequent`, so a rule only says
something in the situations where its antecedent holds. Both checks below are
built on that: conflicts force antecedents to hold, gaps force them not to.
"""

import itertools

import z3

from .logic import Rule, Vocabulary

# The share of the answers a translation needs to stand (see settled). The
# experiments also try 0.75 ("at least 7 of 8").
SETTLE = 0.5

# At most this many distinct uncovered situations are reported (find_gaps).
MAX_GAPS = 3


def analyze(formal: dict, max_group: int = 3, questions: bool = True,
            link_checks: bool = True, settle: float = SETTLE, second: bool = True) -> list[dict]:
    """Run every check on one formal.json and return all findings.

    max_group    how many rules may be triggered together when hunting conflicts
                 (1 = each rule alone, 2 = also every pair, 3 = also every triple).
    questions    use the answers of formalize step 6 (see settled)
    link_checks  leave out the links and facts that step 6 rejected
    settle       share of the answers a translation needs to stand (see settled)
    second       use the second reader of formalize step 7, if it ran (see settled)

    The switches exist so that the experiments can score the same formal
    models with and without steps 6 and 7.
    """
    vocab = Vocabulary(formal["symbols"])
    # Each rule with the status that steps 6 and 7 give it (see settled).
    decided = [settled(rule, settle, questions, second) for rule in formal["rules"]]
    # Assumed facts, fact id -> formula (the "background" list of formal.json).
    # They are guesses of the LLM about what the symbols mean, so only the
    # conflict check uses them, and only to ADD findings (or cast doubt).
    facts = {fact["id"]: vocab.parse(fact["formula"]) for fact in formal.get("background", [])
             if not (link_checks and fact.get("check", {}).get("verdict") == "rejected")}
    # Rules without a stable formalization cannot be checked; they are reported
    # as ambiguities instead.
    rules = [vocab.rule(r) for r in decided if r.get("status") != "rejected"]
    return (
        find_ambiguities(decided)
        + find_conflicts(vocab, rules, facts, max_group)
        + find_gaps(vocab, rules)
    )


# ------------------------------------------------------------------- ambiguity


def settled(rule: dict, settle: float = SETTLE, questions: bool = True, second: bool = True) -> dict:
    """The rule with the status that steps 6 and 7 of formalize give it.

    questions  step 6, check 1 (probe.py): if the translation gets more than
               `settle` of the answers about every other reading, it stands,
               also when its samples had split (the split was noise).
               Otherwise the words leave the choice open: ambiguous.
    second     step 7 (formalize.second_reading): if a second model does not
               confirm the translation (no more than half of its answers mean
               the same), the rule is ambiguous ("found_by": "models"), unless
               it already is. Its most common other reading is the alternative.

    An ambiguous rule is reported, and the author is asked which reading is meant.
    """
    if rule.get("status") == "rejected":
        return rule
    decided = _answered(rule, settle) if questions else rule
    other = rule.get("second", {})
    if (second and other.get("confirms") is False and "reading" in other
            and decided.get("status") == "accepted"):
        decided = {**decided, "status": "ambiguous", "found_by": "models",
                   "alternative": {key: other[key] for key in ("reading", "antecedent", "consequent")},
                   "differs_when": other["differs_when"]}
    return decided


def _answered(rule: dict, settle: float) -> dict:
    """The rule with the status that the answers of step 6, check 1, give it (see settled).

    Probes written by the first version of step 6 (experiments E6, E7) carry
    their own verdict ("confirmed" or "ambiguous"), which is used as it is.
    """
    probes = rule.get("probes", [])
    if not probes:
        return rule

    def stands(probe: dict) -> bool:
        if "verdict" in probe:  # the first version of the questions
            return probe["verdict"] == "confirmed"
        answers = probe["answers"]
        total = sum(answers.values())
        return total == 0 or answers["translation"] > settle * total

    open_ = [probe for probe in probes if not stands(probe)]
    if not open_:
        return {**rule, "status": "accepted"}
    # The other reading against which the translation got the fewest answers.
    probe = min(open_, key=lambda candidate: candidate["answers"]["translation"])
    return {**rule, "status": "ambiguous", "found_by": "questions", "answers": probe["answers"],
            "alternative": {key: probe[key] for key in ("reading", "antecedent", "consequent")},
            "differs_when": probe["situations"][0]["when"] if probe["situations"] else {}}


def find_ambiguities(rules: list[dict]) -> list[dict]:
    """Report the rules that could not be pinned down to one meaning.

    rules  the rule dicts of formal.json, as settled() decided them.

    Each finding says in "found_by" how the rule was found: "samples" (its 8
    translations split by meaning, step 3), "questions" (check 1 of step 6)
    or "models" (a second model reads it otherwise, step 7).
    """
    def reading(translation: dict) -> str:
        """One interpretation: the model's sentence plus the exact logic.

        The sentences of two readings can sound alike while the logic differs
        (e.g. "= 5" versus ">= 5"), so the logic is what makes them comparable.
        """
        return (f"{translation['reading']} "
                f"[in logic: {translation['antecedent']} => {translation['consequent']}]")

    findings = []
    for rule in rules:
        if rule.get("status") not in ("ambiguous", "rejected"):
            continue
        alternative = rule.get("alternative", {})
        finding = {
            "type": "ambiguity",
            "rule": rule["id"],
            "status": rule["status"],                 # "ambiguous": ask; "rejected": must be rewritten
            "found_by": rule.get("found_by", "samples"),
            "split": rule.get("clusters", []),        # how the samples divided, e.g. [5, 3]
            # The two most common interpretations (absent if no sample was usable).
            "readings": [reading(t) for t in (rule, alternative) if "reading" in t],
            # A situation in which the two interpretations demand different things.
            "differs_when": rule.get("differs_when", {}),
        }
        if "answers" in rule:  # how the answers to the questions fell
            finding["answers"] = rule["answers"]
        if finding["found_by"] == "models":  # how many answers of the second model confirm
            finding["second_support"] = rule["second"]["support"]
        findings.append(finding)
    return findings


# -------------------------------------------------------------------- conflicts


def find_conflicts(vocab: Vocabulary, rules: list[Rule], facts: dict, max_group: int) -> list[dict]:
    """Find situations in which the rules cannot all be obeyed.

    The search (see _search) runs twice:

        1. with the rules alone. What it finds is proven from the requirements
           and nothing else.
        2. with the assumed domain facts added. From this run only the
           conflicts that need a fact are kept, and only if no conflict of
           run 1 already explains them.

    The facts are guesses of the LLM, so this order matters: a fact can add a
    finding (which then lists the facts it depends on), but it can never remove
    a finding of run 1. An earlier version used the facts as hard truths in a
    single run, and one wrong fact made a real conflict disappear.

    What the facts may do to a finding of run 1 is cast doubt on it. If they
    say the situation of the conflict cannot happen, the finding stays and
    gets a "doubted_by" list of those facts. Example: "at least 24 hours" and
    "less than 24 hours" as two yes/no symbols can both be true for the
    solver; the fact that they exclude each other marks the resulting
    conflict as doubtful.
    """
    proven = _search(vocab, rules, {}, max_group, doubt=facts)
    if not facts:
        return proven
    assumed = _search(vocab, rules, facts, max_group)
    return proven + [
        finding for finding in assumed
        if "facts" in finding
        and not any(set(p["rules"]) <= set(finding["rules"]) for p in proven)
    ]


def _search(vocab: Vocabulary, rules: list[Rule], facts: dict, max_group: int,
            doubt: dict | None = None) -> list[dict]:
    """One conflict search, taking the given facts (id -> formula) as true.

    Asking "can all rules hold together?" is not enough: implications are all
    satisfied when no antecedent holds. So we pick a small group of rules, force
    their antecedents to hold, and ask two questions:

        1. Can that situation happen at all?           (must be satisfiable)
        2. Can all rules be obeyed in that situation?  (a conflict if not)

    doubt  facts that are NOT taken as true here, but checked against each
           conflict found: those that rule its situation out are listed in the
           finding's "doubted_by".
    """
    findings = []
    # Groups of rule ids already known to trigger a conflict. Any bigger group
    # containing one of them would only rediscover the same conflict.
    known_triggers: list[set] = []

    for size in range(1, max_group + 1):
        for group in itertools.combinations(rules, size):
            ids = {rule.id for rule in group}
            if any(trigger <= ids for trigger in known_triggers):
                continue

            # Question 1: a situation where every rule of the group applies
            # (and which the facts allow).
            antecedents = [rule.antecedent for rule in group]
            firing = list(facts.values()) + antecedents
            situation = vocab.model(firing)
            if situation is None:
                continue  # e.g. "inventory available" and "inventory unavailable"

            # Question 2: which rules (and facts), if any, make that situation impossible?
            culprits = _minimal_conflict(vocab, antecedents, rules, facts)
            if culprits is None:
                continue
            # If one rule alone rules the situation out, the rules do not clash:
            # the situation is simply one the spec forbids. This happens when a
            # symbol is both a condition in one rule and a demand in another,
            # e.g. forcing "the account is locked" (a condition) for an
            # administrator, when another rule says "never lock administrators".
            # The same holds for one rule together with the facts, so a conflict
            # that depends on facts always involves at least two rules.
            if any(vocab.impossible(firing + [rule.formula]) for rule in rules):
                continue

            known_triggers.append(ids)
            culprit_rules, culprit_facts = culprits
            # Show only the symbols the trigger talks about; the rest is noise.
            relevant = set().union(*(vocab.symbols_in(rule.antecedent) for rule in group))
            finding = {"type": "conflict", "rules": culprit_rules}
            if culprit_facts:  # the key is present only when the proof needs a fact
                finding["facts"] = culprit_facts
            finding["when"] = vocab.witness(situation, relevant)
            # Do the facts in `doubt` say that these rules can never apply
            # together? (No rules are passed: only the situation is tested.)
            excluded = _minimal_conflict(vocab, antecedents, [], doubt) if doubt else None
            if excluded:
                finding["doubted_by"] = excluded[1]
            # Does the conflict need two different events at the same moment?
            # When the read step named the event each rule reacts to (its
            # trigger), that is the question for the rules that clash (not for
            # the group that found the situation, which may hold more rules).
            # Formal models made before then only have the events in the
            # antecedents (_simultaneous_events).
            clashing = [rule for rule in rules if rule.id in culprit_rules]
            if all(rule.trigger is not None for rule in clashing):
                events = sorted({rule.trigger for rule in clashing if rule.trigger})
                events = events if len(events) >= 2 else []
            else:
                events = _simultaneous_events(vocab, firing)
            if events:
                finding["simultaneous_events"] = events
            findings.append(finding)

    # Keep each set of culprits once, and drop a conflict when a smaller reported
    # conflict is part of it: fixing the smaller one is the first thing to do.
    kept, seen = [], set()
    for finding in findings:
        culprits = frozenset(finding["rules"])
        explained = any(set(other["rules"]) < culprits for other in findings)
        if culprits not in seen and not explained:
            seen.add(culprits)
            kept.append(finding)
    return kept


def _simultaneous_events(vocab: Vocabulary, forced: list) -> list[str]:
    """The events a conflict needs at the same moment, if it needs two or more.

    For formal models without triggers (made before the read step named
    them): the events are found in the antecedents. forced is what the
    conflict's situation must satisfy (the facts and the antecedents).

    Symbols marked "event" in formal.json are things that happen at one moment
    (a request, a click, an arrival). One snapshot lets any number of them
    happen together, but requirements are written for one at a time: a
    conflict that only appears when two different events coincide ("a visitor
    signs up" while "a subscriber changes the address") is likely an artefact.
    Returns [] when the situation is possible with at most one event.
    """
    names = sorted(vocab.events)
    events = [vocab.variables[name] for name in names]
    if len(events) < 2 or not vocab.impossible(forced + [z3.AtMost(*events, 1)]):
        return []
    situation = vocab.model(forced)
    if situation is None:
        return []
    return [name for name, event in zip(names, events)
            if z3.is_true(situation.eval(event, model_completion=True))]


def _minimal_conflict(vocab: Vocabulary, situation: list, rules: list[Rule],
                      facts: dict) -> tuple[list[str], list[str]] | None:
    """Return the smallest set of rules and facts that cannot hold in `situation`.

    The result is (rule ids, fact ids). Returns None when all rules can be
    obeyed there (no conflict).

    Each rule and each fact gets an on/off switch (a fresh boolean). Z3 is asked
    to check with all switches on; if that fails it names the switches it needed
    for the contradiction (the "unsat core").
    """
    solver = vocab.solver(situation)
    # label -> formula. The ':' cannot appear in a spec symbol, so a switch never
    # clashes with one. Facts come first: they are then the first to be dropped
    # below, which gives the explanation that leans on the fewest assumptions.
    parts = {f"fact:{fact_id}": formula for fact_id, formula in facts.items()}
    parts.update({f"rule:{rule.id}": rule.formula for rule in rules})
    switches = {label: z3.Bool(label, vocab.ctx) for label in parts}
    for label, formula in parts.items():
        solver.add(z3.Implies(switches[label], formula))

    # First try with the facts switched off: a contradiction that needs no fact
    # is the better explanation. Only then switch everything on.
    rules_only = [switches[label] for label in parts if label.startswith("rule:")]
    for switched_on in (rules_only, list(switches.values())):
        if solver.check(*switched_on) == z3.unsat:
            break
    else:
        return None  # the rules can all be obeyed, even with every fact on
    core = {switch.decl().name() for switch in solver.unsat_core()}
    needed = [label for label in parts if label in core]

    # Z3's core is not guaranteed to be minimal. Try dropping each part in turn:
    # if the contradiction survives without it, the part was not needed.
    for label in list(needed):
        others = [other for other in needed if other != label]
        if solver.check(*(switches[other] for other in others)) == z3.unsat:
            needed = others

    def ids(kind: str) -> list[str]:
        """The ids of the needed parts of one kind ("rule" or "fact")."""
        return [label.split(":", 1)[1] for label in needed if label.startswith(kind + ":")]

    return ids("rule"), ids("fact")


# ------------------------------------------------------------------------- gaps


def find_gaps(vocab: Vocabulary, rules: list[Rule]) -> list[dict]:
    """Find situations in which no rule says what the system must do.

    A situation is uncovered when every conditional rule's antecedent is false.
    Rules that always apply (e.g. "SHALL NOT place any order on backorder") are
    constraints, not responses to a situation, so they do not count as coverage.

    The assumed domain facts are not used here: a fact can only declare
    situations impossible, so it could only make a gap disappear.
    """
    conditional = [
        rule for rule in rules
        # "not antecedent" is impossible  <=>  the antecedent is always true.
        if not vocab.impossible([z3.Not(rule.antecedent)])
    ]
    if not conditional:
        return []
    antecedents = [rule.antecedent for rule in conditional]
    nothing_fires = [z3.Not(antecedent) for antecedent in antecedents]
    # Only symbols used in some antecedent can decide whether a rule fires.
    relevant = set().union(*(vocab.symbols_in(antecedent) for antecedent in antecedents))

    findings = []
    already_reported = []  # formulas excluding the gaps found so far
    while len(findings) < MAX_GAPS:
        situation = vocab.model(nothing_fires + already_reported)
        if situation is None:
            break  # every (remaining) situation triggers at least one rule
        when = vocab.witness(situation, relevant)

        # Generalize the example. Z3 returned one exact situation, but usually
        # only a few symbols matter. Drop a symbol if, with the others fixed,
        # no value of it could make any rule fire.
        for name in list(when):
            rest = {k: v for k, v in when.items() if k != name}
            if vocab.impossible(vocab.assignment(rest) + [z3.Or(antecedents)]):
                when = rest

        findings.append({"type": "gap", "when": when})
        if not when:
            break  # no symbol matters: no rule can ever fire, nothing more to find
        # Exclude this whole family of situations and look for a different gap.
        already_reported.append(z3.Not(z3.And(vocab.assignment(when))))
    return findings


# -------------------------------------------------------------------- scenarios


def find_scenarios(formal: dict) -> list[dict]:
    """List behaviours the spec allows or forbids, for the author to confirm.

    Conflicts and gaps are defects. A scenario is not: it is a consequence of
    the rules that the author may not have intended. Two kinds are proven here:

        accepted   what rule R demands may also happen when R does not apply.
                   ("fulfil the order" is demanded when stock is available; is
                   it also allowed when stock is not available?)
        rejected   a situation the rules make impossible: rule Q applies in
                   it, and rule R alone rules it out.
                   (an administrator account that is locked)

    There can be many, and most are unremarkable. explain.py asks an LLM judge
    which ones are surprising and shows only those.

    Each scenario: {"type": "scenario", "verdict": "accepted" | "rejected",
                    "rules": [...], "when": {...}}
    """
    vocab = Vocabulary(formal["symbols"])
    rules = [vocab.rule(r) for r in formal["rules"] if r.get("status") != "rejected"]
    everything = [rule.formula for rule in rules]
    scenarios = []

    # accepted: all rules hold, rule R does not apply, yet R's demand is met.
    for rule in rules:
        situation = vocab.model(everything + [z3.Not(rule.antecedent), rule.consequent])
        if situation is not None:
            relevant = vocab.symbols_in(rule.formula)
            scenarios.append({"type": "scenario", "verdict": "accepted", "rules": [rule.id],
                              "when": vocab.witness(situation, relevant)})

    # rejected: Q and R can apply together, but then R's demand cannot be met.
    for forbidder in rules:
        for other in rules:
            if other is forbidder:
                continue
            both_apply = [other.antecedent, forbidder.antecedent]
            situation = vocab.model(both_apply)
            if situation is not None and vocab.impossible(both_apply + [forbidder.consequent]):
                relevant = vocab.symbols_in(z3.And(both_apply))
                scenarios.append({"type": "scenario", "verdict": "rejected",
                                  "rules": [forbidder.id, other.id],
                                  "when": vocab.witness(situation, relevant)})
    return scenarios


# ---------------------------------------------------------- several symbol sets


def combine(findings_per_model: list[list[dict]]) -> list[dict]:
    """Merge the findings of K formal models of the same document.

    The choice of symbols is the fragile step of the formalization. So the
    same document can be formalized K times with K symbol sets (same rules,
    same rule ids). A finding that shows up with most symbol sets does not
    depend on that choice; one that shows up with a single set does.

    Findings are matched by what they are about: a conflict by its set of
    rules, an ambiguity by its rule, a scenario by its verdict and rules.
    Each merged finding gets:

        "support"  e.g. "3/5": found with 3 of the 5 symbol sets
        "model"    index of the formal model its witness is written in

    Gaps cannot be matched (a gap is a situation over one model's own
    symbols), so the gaps of the first model are kept as they are.
    With a single model the findings come back unchanged.
    """
    total = len(findings_per_model)
    if total == 1:
        return findings_per_model[0]

    def weakness(f: dict) -> tuple:
        """Lower is stronger: not doubtful first, then proven from the rules alone."""
        return ("doubted_by" in f or "simultaneous_events" in f, "facts" in f)

    merged: dict[tuple, dict] = {}   # key -> the finding shown for it
    seen_in: dict[tuple, int] = {}   # key -> number of models that have it
    for index, findings in enumerate(findings_per_model):
        for finding in findings:
            if finding["type"] == "gap":
                if index == 0:
                    merged[("gap", len(merged))] = {**finding, "model": 0}
                continue
            if finding["type"] == "ambiguity":
                key = ("ambiguity", finding["rule"])
            else:  # conflict or scenario
                key = (finding["type"], finding.get("verdict"), frozenset(finding["rules"]))
            seen_in[key] = seen_in.get(key, 0) + 1
            # Show the first occurrence, unless a later one is stronger.
            if key not in merged or weakness(finding) < weakness(merged[key]):
                merged[key] = {**finding, "model": index}

    for key, finding in merged.items():
        if key in seen_in:
            finding["support"] = f"{seen_in[key]}/{total}"
    # Keep the usual order of types; within a type, best supported first.
    order = {"ambiguity": 0, "conflict": 1, "gap": 2, "scenario": 3}
    return sorted(merged.values(),
                  key=lambda f: (order[f["type"]], -int(f.get("support", "0/1").split("/")[0])))
