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
find_conflicts), "simultaneous_events" (see _simultaneous_events) or
"beyond_example" (see _mark_examples); is_doubtful tests the three. A conflict
or gap that is gone with the other reading of an ambiguous rule says so in
"depends_on_reading", and the ambiguity lists what its other reading changes
in "other_reading" (see _try_other_readings).

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

# The marks of a finding that is likely a false alarm (see the module docstring).
DOUBTS = ("doubted_by", "simultaneous_events", "beyond_example")


def is_doubtful(finding: dict) -> bool:
    """Is the finding marked as a likely false alarm?"""
    return any(finding.get(mark) for mark in DOUBTS)


def analyze(formal: dict, max_group: int = 3, questions: bool = True,
            link_checks: bool = True, settle: float = SETTLE, second: bool = True,
            readings: bool = True) -> list[dict]:
    """Run every check on one formal.json and return all findings.

    max_group    how many rules may be triggered together when hunting conflicts
                 (1 = each rule alone, 2 = also every pair, 3 = also every triple).
    questions    use the answers of formalize step 6 (see settled)
    link_checks  leave out the links and facts that step 6 rejected
    settle       share of the answers a translation needs to stand (see settled)
    second       use the second reader of formalize step 7, if it ran (see settled)
    readings     say which findings depend on the reading of an ambiguous rule
                 (see _try_other_readings)

    The switches exist so that the experiments can score the same formal
    models with and without steps 6 and 7, and can skip `readings` where only
    the counts matter.
    """
    vocab = Vocabulary(formal["symbols"])
    # Each rule with the status that steps 6 and 7 give it (see settled).
    decided = [settled(rule, settle, questions, second) for rule in formal["rules"]]
    # Assumed facts, fact id -> formula (the "background" list of formal.json).
    # They are guesses of the LLM about what the symbols mean, so they may only
    # ADD conflicts, or cast doubt on a conflict or a gap.
    facts = {fact["id"]: vocab.parse(fact["formula"]) for fact in formal.get("background", [])
             if not (link_checks and fact.get("check", {}).get("verdict") == "rejected")}
    # Rules without a stable formalization cannot be checked; they are reported
    # as ambiguities instead.
    rules = [vocab.rule(r) for r in decided if r.get("status") != "rejected"]
    ambiguities = find_ambiguities(decided)
    # A spec about whole runs ("situation": "run", formalize): several things
    # happen in a run, so two events in one conflict are no reason for doubt.
    whole_run = formal.get("situation") == "run"
    conflicts = find_conflicts(vocab, rules, facts, max_group, whole_run)
    _mark_special_cases(vocab, rules, conflicts)
    _mark_examples(vocab, rules, facts, conflicts, {rule["id"] for rule in formal["rules"] if rule.get("example")})
    # The rules that a change removes (change.after_model). They take no part
    # in any check; they only show which gap the change opened.
    lost = [vocab.rule(rule) for rule in formal.get("removed_rules", []) if rule.get("status") != "rejected"]
    gaps = find_gaps(vocab, rules, doubt=facts, lost=lost)
    if readings:
        _try_other_readings(vocab, decided, rules, facts, max_group, ambiguities, conflicts, gaps, whole_run)
        # The ambiguities whose answer changes another finding come first.
        ambiguities.sort(key=lambda finding: not any(finding.get("other_reading", {}).values()))
    return ambiguities + conflicts + gaps


def _mark_examples(vocab: Vocabulary, rules: list[Rule], facts: dict, conflicts: list[dict],
                   examples: set) -> None:
    """Mark the conflicts that need more than an example says ("beyond_example").

    examples  the ids of the rules that are examples ("example": true in the
              formal model, set from `speccheck --examples`)

    An example describes one concrete case, not a rule for all cases:

        R9   "WHEN dana asks to return parcel k7 AND k7 was delivered
              THEN book_return is called once ..."
        R10  "WHEN the same request runs while k7 is still in the warehouse
              THEN book_return is never called ..."

    Read as rules, R9 and R10 clash for a parcel that was delivered and is
    still in the warehouse. But each is about its own case, and R9 does not
    say that its parcel is in the warehouse. So a conflict with an example
    counts as it is only when the case of one example is the whole situation:
    its condition and what it demands, with the assumed facts, entail the
    conditions of the other rules of the conflict. Then the example itself
    says that they apply ("WHEN dana sends an express request THEN
    ship_parcel succeeds three times", against a rule about every successful
    ship_parcel). Otherwise the situation says more than any example in it,
    and the conflict is kept and marked as doubtful, with the examples among
    its rules:

        "beyond_example": ["R9", "R10"]
    """
    by_id = {rule.id: rule for rule in rules}
    given = list(facts.values())

    def is_whole_situation(example: Rule, others: list[Rule]) -> bool:
        case = given + [example.antecedent, example.consequent]
        return not vocab.impossible(case) and all(vocab.implies(case, other.antecedent) for other in others)

    for finding in conflicts:
        chosen = [by_id[rule_id] for rule_id in finding["rules"]]
        inside = [rule for rule in chosen if rule.id in examples]
        if inside and not any(is_whole_situation(example, [rule for rule in chosen if rule is not example])
                              for example in inside):
            finding["beyond_example"] = [rule.id for rule in inside]


def weakness(finding: dict) -> tuple:
    """Lower is stronger: not doubtful first, then proven from the rules alone (see combine)."""
    return (is_doubtful(finding), "facts" in finding)


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
        if rule.get("empty"):  # its translation demands nothing (formalize._judge)
            finding["found_by"] = "empty"
        if "answers" in rule:  # how the answers to the questions fell
            finding["answers"] = rule["answers"]
        if finding["found_by"] == "models":  # how many answers of the second model confirm
            finding["second_support"] = rule["second"]["support"]
        findings.append(finding)
    return findings


def _try_other_readings(vocab: Vocabulary, decided: list[dict], rules: list[Rule], facts: dict,
                        max_group: int, ambiguities: list[dict], conflicts: list[dict],
                        gaps: list[dict], whole_run: bool = False) -> None:
    """Say which findings depend on the reading chosen for an ambiguous rule.

    An ambiguous rule has two readings, and the checks use the first one.
    Which one the author meant is exactly what is not known. So each ambiguous
    rule is tried once more with its other reading, one rule at a time, with
    all other rules as they are. Example, a login spec:

        R3   "WHEN the number of failed attempts reaches 5 THEN lock the account"
             reading 1   (= failed_attempts 5)      the one the checks use
             reading 2   (>= failed_attempts 5)
        gap  "6 failed attempts, no password submitted": no rule applies
             with reading 2, R3 applies there, so this gap depends on how R3 is read

    Nothing is removed and no finding is added. The findings only get more
    to say (they are changed in place):

        conflict["depends_on_reading"]   the ambiguous rules with whose other
        gap["depends_on_reading"]        reading this finding is gone, each with
                                         that other reading in words:
                                         {"R3": "lock at 5 or more failed attempts"}
        ambiguity["other_reading"]       what the rule's other reading changes:
            {"removes": [[rule ids], ...],   conflicts that are gone
             "adds": [[rule ids], ...],      conflicts that appear
             "covers_gaps": 1}               gaps in which a rule then applies

    decided  the rule dicts as settled() left them; `rules` are those of them
             that the checks used, compiled.
    """
    reported = {frozenset(conflict["rules"]) for conflict in conflicts}
    position = {rule["id"]: index for index, rule in enumerate(decided)}
    finding_of = {finding["rule"]: finding for finding in ambiguities}

    def in_document_order(groups) -> list[list[str]]:
        return sorted(sorted(group, key=position.get) for group in groups)

    for rule in decided:
        other = rule.get("alternative", {})
        if rule.get("status") != "ambiguous" or "antecedent" not in other:
            continue
        try:
            reading = vocab.rule({"id": rule["id"], "trigger": rule.get("trigger"), **other})
        except ValueError:
            continue  # the other reading is not a formula over the symbols
        variant = [reading if compiled.id == rule["id"] else compiled for compiled in rules]

        found = {frozenset(conflict["rules"])
                 for conflict in find_conflicts(vocab, variant, facts, max_group, whole_run)}
        for conflict in conflicts:
            if frozenset(conflict["rules"]) not in found:
                conflict.setdefault("depends_on_reading", {})[rule["id"]] = other.get("reading", "")

        # A gap stays a gap when, in its situation, still no conditional rule
        # can apply (rules that always apply do not count, as in find_gaps).
        conditions = [compiled.antecedent for compiled in variant
                      if not vocab.impossible([z3.Not(compiled.antecedent)])]
        covered = [gap for gap in gaps
                   if not conditions
                   or not vocab.impossible(vocab.assignment(gap["when"]) + [z3.Or(conditions)])]
        for gap in covered:
            gap.setdefault("depends_on_reading", {})[rule["id"]] = other.get("reading", "")

        finding_of[rule["id"]]["other_reading"] = {
            "removes": in_document_order(reported - found),
            "adds": in_document_order(found - reported),
            "covers_gaps": len(covered),
        }


# -------------------------------------------------------------------- conflicts


def find_conflicts(vocab: Vocabulary, rules: list[Rule], facts: dict, max_group: int,
                   whole_run: bool = False) -> list[dict]:
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
    proven = _search(vocab, rules, {}, max_group, doubt=facts, whole_run=whole_run)
    if not facts:
        return proven
    assumed = _search(vocab, rules, facts, max_group, whole_run=whole_run)
    return proven + [
        finding for finding in assumed
        if "facts" in finding
        and not any(set(p["rules"]) <= set(finding["rules"]) for p in proven)
    ]


def _mark_special_cases(vocab: Vocabulary, rules: list[Rule], conflicts: list[dict]) -> None:
    """Say of a conflict between two rules when one of them applies only where the other does.

    Real specs state a rule and, next to it, its exceptions:

        R1  "WHEN createChange(projectRoot, 'add-auth') is called THEN the system creates
             openspec/changes/add-auth/ directory"
        R2  "WHEN createChange(projectRoot, 'add-auth') is called and openspec/changes/add-auth/
             already exists THEN the system throws an error ..."

    The two clash wherever R2 applies, and their author meant that: R2 is the
    exception. The solver cannot know what was meant, but it can prove the
    form: the condition of R2 entails the condition of R1, and not the other
    way round. Such a conflict gets

        "special_case": {"general": "R1", "special": "R2"}

    and the report says so. It stays a conflict, and it is not doubtful: R1
    does not say "unless". Two rules with the same condition get no mark, and
    neither does a conflict of three rules. A rule that always applies ("THE
    system SHALL NOT ...") is not a general rule in this sense: every rule is
    a special case of it, so the mark would say nothing.
    """
    by_id = {rule.id: rule for rule in rules}
    for finding in conflicts:
        if len(finding["rules"]) != 2:
            continue
        first, second = (by_id[rule_id] for rule_id in finding["rules"])
        first_is_special = vocab.implies([first.antecedent], second.antecedent)
        second_is_special = vocab.implies([second.antecedent], first.antecedent)
        if first_is_special != second_is_special:
            general, special = (second, first) if first_is_special else (first, second)
            if not vocab.impossible([z3.Not(general.antecedent)]):  # the general rule has a condition
                finding["special_case"] = {"general": general.id, "special": special.id}


def _search(vocab: Vocabulary, rules: list[Rule], facts: dict, max_group: int,
            doubt: dict | None = None, whole_run: bool = False) -> list[dict]:
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
    family = _families(vocab, rules, facts)

    for size in range(1, max_group + 1):
        for group in itertools.combinations(rules, size):
            ids = {rule.id for rule in group}
            if any(trigger <= ids for trigger in known_triggers):
                continue
            if len({family[id(rule)] for rule in group}) > 1:
                continue  # rules with no symbol in common cannot clash (see _families)

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
            if events and not whole_run:  # in a whole run, several things happen
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


def _families(vocab: Vocabulary, rules: list[Rule], facts: dict) -> dict[int, int]:
    """Sort the rules into families that share symbols.

    Two rules are in one family when they have a symbol in common, directly
    or through other rules and the given facts:

        R1   order_submitted => order_fulfilled          family 0
        R5   order_canceled  => (not order_fulfilled)    family 0: shares order_fulfilled
        P1   page_printed    => counter_raised           family 1: nothing in common

    Rules of two families cannot contradict each other: the solver can obey
    each family without looking at the other. Forcing rules of two families
    to apply together can therefore only find again what one family shows
    alone, and _search skips such groups. A document about one subject is
    usually one family. A document made of unrelated parts (several specs
    checked together) is not, and there this saves most of the work.

    Returns id(rule) -> the number of its family. The key is the Python
    object, not the rule's own id: those come from the LLM and may repeat.
    """
    head: dict[str, str] = {}  # symbol -> a symbol nearer to the one that names its family

    def name_of(symbol: str) -> str:
        while head.setdefault(symbol, symbol) != symbol:
            symbol = head[symbol]
        return symbol

    for formula in [rule.formula for rule in rules] + list(facts.values()):
        symbols = sorted(vocab.symbols_in(formula))
        for other in symbols[1:]:
            head[name_of(other)] = name_of(symbols[0])

    numbers: dict[str, int] = {}
    families = {}
    for rule in rules:
        symbols = sorted(vocab.symbols_in(rule.formula))
        # A rule without any symbol ("true => true") is a family of its own.
        name = name_of(symbols[0]) if symbols else f"rule {id(rule)}"
        families[id(rule)] = numbers.setdefault(name, len(numbers))
    return families


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


def find_gaps(vocab: Vocabulary, rules: list[Rule], by_event: bool = True,
              doubt: dict | None = None, lost: list[Rule] = ()) -> list[dict]:
    """Find situations in which no rule says what the system must do.

    A situation is uncovered when every conditional rule's antecedent is false.
    Rules that always apply (e.g. "SHALL NOT place any order on backorder") are
    constraints, not responses to a situation, so they do not count as coverage.

    Nearly every spec has the gap "nothing is happening", and it says little.
    The useful gaps are those in which something happens. So when the rules
    react to events (formalize step 1 marks them), the question is asked once
    for each event, with no other event at the same moment:

        rules    "WHEN a courier scans a parcel AND a compartment is free THEN ..."
                 (the rule for "no compartment is free" is missing)
        event    parcel_scanned
        gap      parcel_scanned TRUE, compartment_free FALSE: no rule applies
                 -> {"type": "gap", "event": "parcel_scanned", "when": {...}}

    That gives at most one gap for each event. After them comes one gap in
    which no event happens, marked "quiet": True.

    Without events to go by (a formal model made before they were marked, or
    rules that react to states only), and with by_event=False (the experiments
    compare the two), the search is over all situations, at most MAX_GAPS gaps.

    doubt  the assumed domain facts (id -> formula). As with conflicts, they
           never remove a gap, they can only cast doubt on one. Example:

               rules  "WHEN a resident books a slot AND the slot is free THEN ..."
                      "WHEN a resident books a slot AND the slot is taken THEN ..."
               gap    slot_booked TRUE, slot_is_free FALSE, slot_is_taken FALSE
               fact   F2: a slot is either free or taken

           For each event, a gap the facts allow is looked for first. If there
           is none, the gap found without them is reported with "doubted_by":
           the facts that say it cannot happen (here F2).

    lost   rules that a change removes (change.py); `rules` are those that
           stay. For each lost rule, the situation it was written for is
           looked at first: its events happen and no others, and its
           condition holds. If no rule applies there now, that is a gap the
           change opened. Example:

               stays  "WHEN a visitor checks in AND the visitor is on the list THEN ..."
               lost   "WHEN a visitor checks in AND the visitor is not on the list THEN ..."
               gap    visitor_checks_in TRUE, visitor_on_list FALSE

           Such a gap has "opened_by": the id of the lost rule, and it takes
           the place of the usual gap for that event. A lost rule whose events
           no remaining rule reacts to gives no gap: nothing reacts to that
           event any more, by decision.
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

    def search(given: list, limit: int, keep: frozenset = frozenset()) -> list[dict]:
        """Up to `limit` different gaps among the situations in which `given` holds.

        keep  symbols that stay in the situation shown: the event that happens,
              or, for the gap without an event, the events that do not
        """
        found = []
        already_found = []  # formulas excluding the gaps found so far
        while len(found) < limit:
            situation = vocab.model(nothing_fires + given + already_found)
            if situation is None:
                break  # every (remaining) situation triggers at least one rule
            when = vocab.witness(situation, relevant | keep)

            # Generalize the example. Z3 returned one exact situation, but usually
            # only a few symbols matter. Drop a symbol if, with the others fixed,
            # no value of it could make any rule fire.
            for name in list(when):
                rest = {k: v for k, v in when.items() if k != name}
                if name not in keep and vocab.impossible(vocab.assignment(rest) + [z3.Or(antecedents)]):
                    when = rest

            found.append({"type": "gap", "when": when})
            if not when:
                break  # no symbol matters: no rule can ever fire, nothing more to find
            # Exclude this whole family of situations and look for a different gap.
            already_found.append(z3.Not(z3.And(vocab.assignment(when))))
        return found

    def doubted(given: list) -> list[str]:
        """The facts that rule out every uncovered situation in which `given` holds."""
        excluded = _minimal_conflict(vocab, nothing_fires + given, [], doubt) if doubt else None
        return excluded[1] if excluded else []

    def one_gap(given: list, keep: frozenset) -> list[dict]:
        """The gap among the situations in which `given` holds: one the facts
        allow if there is one, else the one without the facts, marked doubtful."""
        if doubt:
            allowed = search(given + list(doubt.values()), 1, keep)
            if allowed:
                return allowed
        return [{**gap, "doubted_by": doubted(given)} if doubt else gap
                for gap in search(given, 1, keep)]

    # The events some rule reacts to: named as its trigger, or used in its condition.
    reacted_to = sorted({rule.trigger for rule in conditional if rule.trigger}
                        | (vocab.events & relevant))
    if not by_event or not reacted_to:
        # Up to MAX_GAPS gaps, found as before; each one whose situations the
        # facts all rule out is marked.
        gaps = search([], MAX_GAPS)
        for gap in gaps:
            facts = doubted(vocab.assignment(gap["when"]))
            if facts:
                gap["doubted_by"] = facts
        return gaps

    happens = {name: vocab.variables[name] for name in sorted(vocab.events)}
    # First the gaps that a change opened (see `lost` above). The situation is
    # the lost rule's own: all of its events, also when it names two ("a
    # customer buys credit" and "the payment is refused").
    opened = {}  # event -> the gap that a lost rule for this event leaves open
    for rule in lost:
        its_events = ({rule.trigger} | vocab.symbols_in(rule.antecedent)) & vocab.events
        still_handled = sorted(its_events & set(reacted_to))
        if not still_handled or still_handled[0] in opened:
            continue  # nothing reacts to its events any more; or that event has its gap already
        only_these = [event if name in its_events else z3.Not(event) for name, event in happens.items()]
        # What the lost rule asked about stays in the situation shown.
        shown = frozenset(its_events | vocab.symbols_in(rule.antecedent))
        for gap in one_gap(only_these + [rule.antecedent], shown):
            opened[still_handled[0]] = {**gap, "opened_by": [rule.id]}

    findings = []
    for event in reacted_to:
        alone = [happens[event]] + [z3.Not(other) for name, other in happens.items() if name != event]
        for gap in [opened[event]] if event in opened else one_gap(alone, frozenset([event])):
            findings.append({"type": "gap", "event": event, **gap})
    nothing_happens = [z3.Not(event) for event in happens.values()]
    for gap in one_gap(nothing_happens, frozenset(vocab.events & relevant)):
        findings.append({**gap, "quiet": True})
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
