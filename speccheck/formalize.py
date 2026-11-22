"""formalize.py: stage 1, from spec text to formal.json. LLM + Z3.

Seven steps (the last one optional). Z3 only answers questions about
formulas ("can any situation tell these two apart?"); the grouping, voting
and counting below is done by this file:

    1. read     one LLM call lists the atomic rules of the document, with the
                event each one reacts to (its trigger), and the symbols
                (variables) needed to express them.
    2. sample   each rule is translated to logic N times, independently.
    3. cluster  the N translations are put in groups that mean the same: two
                go together when Z3 proves that no situation tells them apart.
                If they (nearly) all mean the same, the rule is accepted. If
                they split into two camps, the rule is ambiguous, and the
                second camp is the other reading that step 6 asks about. If
                they scatter, the rule is rejected as too unclear.
    4. facts    the LLM is asked N times which domain facts connect the
                symbols ("a door cannot be open and closed"). A fact is kept
                when Z3 proves that it follows from more than half of the N
                answers.
    5. links    a rule whose outcome has a symbol that no other rule uses
                ("remove the record") is translated N more times, with only
                the outcomes of the other rules ("the record is retained").
                If most answers agree ("not retained"), that meaning becomes
                an assumed fact, a "link" (example: _links).
    6. probe    three checks by questions about one requirement (probe.py):
                is the translation the only reading of the words? does the
                rule demand what its link claims? does it agree with the
                facts that make it impossible to obey?
    7. second   optional: a second model, of another family, translates every
                rule N times as in step 2. For each answer Z3 is asked whether
                it means the same as the translation; if no more than half
                do, the rule is ambiguous (example: second_reading).

`formalize` does this once. `formalize_sets` does it K times, each time with
its own symbols, so that findings can be checked against that choice.

The prompts below are generic: nothing in this file is about any one spec.
"""

import math
from concurrent.futures import ThreadPoolExecutor

import z3

from .llm import LLM
from .logic import Rule, Vocabulary
from .probe import MAJORITY, question

# Entropy thresholds for the cluster step (natural logarithm).
# With 8 samples:  8/0 -> 0.00, 7/1 -> 0.38   accepted
#                  6/2 -> 0.56, 5/3 -> 0.66   ambiguous
#                  4/2/2 -> 1.04              rejected
LOW_ENTROPY = 0.4
HIGH_ENTROPY = 1.0

# The read step copies every requirement word for word and lists every symbol,
# so its answer grows with the document. For the 30-requirement spec in
# experiments/sets/size it is about 15,000 characters, roughly 4,000 to 5,000
# tokens: some 150 tokens per requirement. An answer that is cut off is not
# valid JSON, and the whole run fails.
# The server sets the upper bound: the prompt and the answer together must fit
# in its context window (--max-model-len 32768 in experiments/slurm/serve.sbatch),
# and vLLM refuses a request that asks for more. 24576 leaves 8192 tokens for
# the prompt (the instructions and the document), and is enough for about 150
# requirements. On a server with a smaller window, lower it.
READ_MAX_TOKENS = 24576

# ---------------------------------------------------------------- step 1: read

READ_SYSTEM = """\
You prepare a software requirements document for formal analysis.

1. rules: list every atomic requirement: each statement of what the system \
shall or shall not do, and under which condition. One acceptance criterion or \
one scenario is one rule. Copy its text word for word (join a multi-line \
scenario into one sentence). Use the document's own label as id (such as "R1" \
or "2.3"); if there are no labels, number them R1, R2, ... Leave out titles, \
user stories and explanations. trigger: the name of the event symbol (see \
below) for the happening the rule reacts to, such as connection_failed for \
"WHEN a connection attempt fails for the third time"; empty when the rule \
reacts to a state ("WHILE ...") or always applies.

2. symbols: the variables needed to write ALL the rules in logic. Together \
they describe one snapshot of the system: what is the case or is happening \
(events, inputs, states), and what the system does in response.
- sort "Bool" for a yes/no fact, "Int" or "Real" for a quantity, "Enum" for \
exactly one of several named values (list at least two in "values"; otherwise \
leave "values" empty). A single state that either holds or not is a Bool. \
All names, including enum values, must be distinct.
- names are lowercase snake_case.
- A symbol stands for one observable fact about the system or its \
environment (a lamp is lit, a file exists, access is granted), not for a \
sentence of the document. Break a phrase down into the facts it is about.
- A symbol never holds a condition or a restriction: words like "only", \
"if", "unless", "all" belong in the logic, not in a symbol name (not \
lamp_lit_only_at_night, but lamp_lit and is_night).
- Rules that concern the same fact must share its symbol, even when they use \
different words, so that a clash between them can be seen: "switch the lamp \
off" and "the lamp stays lit" are both about lamp_lit. Opposites share one \
symbol too: "unavailable" is "not available".
- Something that happens at one moment (a request is made, a button is \
pressed, a train arrives, an attempt fails) gets its own Bool symbol with \
event: true, separate from the properties of what was sent. Also when the \
document counts it: "the fifth wrong password" is the event \
wrong_password_entered, and "a connection attempt fails for the third time" \
is the event connection_failed, each plus a quantity for the count. Every \
other symbol (a state, a quantity, something the system does) has event: false.
- If a phrase could reasonably mean more than one observable fact (for \
example "disable" may mean switched off, or merely hidden), declare a symbol \
for each of those facts so the difference can be expressed.
- description: one phrase that pins the meaning down."""

READ_SCHEMA = {
    "type": "object",
    "properties": {
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                    "trigger": {"type": "string"},
                },
                "required": ["id", "text", "trigger"],
                "additionalProperties": False,
            },
        },
        "symbols": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sort": {"enum": ["Bool", "Int", "Real", "Enum"]},
                    "values": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"},
                    "event": {"type": "boolean"},
                },
                "required": ["name", "sort", "values", "description", "event"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["rules", "symbols"],
    "additionalProperties": False,
}

# -------------------------------------------------------------- step 2: sample

FORMALIZE_SYSTEM = """\
You translate ONE requirement into logic, using a given list of symbols.

Answer with:
- reading: one sentence, in your own words, saying exactly what the \
requirement demands and in which situations.
- antecedent: an SMT-LIB boolean expression for the situations in which the \
requirement applies (its WHEN / WHILE / IF / WHERE part). Write true if it \
always applies.
- consequent: an SMT-LIB boolean expression for what must hold in those \
situations (its SHALL / THEN part).

SMT-LIB uses prefix notation: (and a b), (or a b), (not a), (=> a b), \
(= x y), (< x 5), (>= x 0), (+ x y), true, false. A lone symbol needs no \
parentheses. Compare an Enum symbol with one of its values like this: \
(= state closed).

Put the whole condition in the antecedent: the consequent states only what \
must hold, and is never itself an implication.

A symbol marked "event" is something that happens at one moment. When the \
requirement reacts to such a happening, its event symbol is part of the \
antecedent, also when a count says which time it is ("the fifth wrong \
password": the event, and the count is 5).

Use only the listed symbols. Translate what this requirement says and nothing \
more: add no conditions from other requirements or from common sense."""

FORMALIZE_SCHEMA = {
    "type": "object",
    "properties": {
        "reading": {"type": "string"},
        "antecedent": {"type": "string"},
        "consequent": {"type": "string"},
    },
    "required": ["reading", "antecedent", "consequent"],
    "additionalProperties": False,
}


# --------------------------------------------------------------- step 4: facts

FACTS_SYSTEM = """\
You are given the symbols of a formal model of a software system, each with \
its meaning. Each symbol is one fact about a single snapshot of the system.

List the domain facts that connect these symbols: statements that hold in \
EVERY possible snapshot purely because of what the symbols mean. Typical cases:
- two things cannot both be the case (a door cannot be open and closed);
- one thing is part of another, or implies it (a signed-and-dated form is a \
signed form);
- a quantity has a natural bound (a count is never negative).

A fact is about meaning, never about desired behaviour. Test each one: it \
must stay true even for a badly built system that breaks every requirement. \
"A locked door is not open" passes the test. "A locked door sounds an alarm" \
fails it: that is a requirement.

Give only facts you are certain of. Return an empty list if there are none.

Each fact has:
- text: the fact in one plain sentence.
- formula: the same fact as an SMT-LIB boolean expression over the symbols, \
in prefix notation: (not (and a b)), (=> a b), (>= x 0)."""

FACTS_SCHEMA = {
    "type": "object",
    "properties": {
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "formula": {"type": "string"},
                },
                "required": ["text", "formula"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["facts"],
    "additionalProperties": False,
}

# Temperature of the read step for the extra symbol sets (see formalize_sets).
SET_TEMPERATURE = 0.7

# --------------------------------------------------------------- step 5: links

# Added to FORMALIZE_SYSTEM when a rule is translated again without the
# symbols that only this rule uses (see _links).
RESTATE_NOTE = """

Some facts this requirement talks about may have no symbol in the list. \
Express what it demands with the listed symbols as well as they allow. If \
they cannot express it at all, answer with consequent: none"""


def formalize(llm: LLM, spec_text: str, samples: int = 8, temperature: float = 0.7,
              read_temperature: float = 0.0, keep_samples: bool = False,
              second: LLM | None = None) -> dict:
    """Turn a requirements document into a formal.json dict.

    samples           answers drawn per rule (for the ambiguity check) and for
                      the domain facts (for the majority vote)
    temperature       variety of those answers
    read_temperature  variety of the read step. 0 asks for the most likely
                      rules and symbols; the experiments raise it to see how
                      much the findings depend on the choice of symbols.
    keep_samples      also store every raw LLM answer: under "samples" in each
                      rule and under "fact_samples". The checks ignore them.
                      The experiments use this so that the clustering and the
                      vote can be redone later without a GPU.
    second            a second model for step 7, or None to skip it
    """
    rules, symbols = _read(llm, spec_text, read_temperature)
    vocab = Vocabulary(symbols)
    shown = _symbol_list(symbols)

    # Steps 2 and 4 ask the LLM. Everything is sent at once; the server batches
    # the calls across its GPUs. The facts question sees only the symbols, not
    # the requirements, so that it cannot simply repeat a requirement as a "fact".
    with ThreadPoolExecutor(max_workers=16) as pool:
        fact_call = pool.submit(llm.ask, FACTS_SYSTEM, f"Symbols:\n{shown}",
                                FACTS_SCHEMA, samples, temperature)
        answers_per_rule = list(pool.map(
            lambda rule: _translate(llm, shown, rule, samples, temperature), rules))
        fact_answers = fact_call.result()

    # The Z3 work (step 3 and the vote of step 4) runs here, after the threads
    # are done: Z3 must not be used from several threads at the same time.
    formal_rules = [{**rule, **_judge(vocab, answers)}
                    for rule, answers in zip(rules, answers_per_rule)]
    background = _agreed_facts(vocab, fact_answers, samples)

    # Step 5: a rule whose outcome is written with symbols that no other rule
    # uses is translated once more, with the outcomes of the other rules
    # instead (see _symbols_to_hide and _links).
    hidden = _symbols_to_hide(vocab, formal_rules)
    to_restate = [rule for rule in formal_rules if rule["id"] in hidden]
    with ThreadPoolExecutor(max_workers=16) as pool:  # LLM calls only, again
        restatements = list(pool.map(
            lambda rule: _translate(llm, _symbol_list(symbols, hidden[rule["id"]]), rule,
                                    samples, temperature, FORMALIZE_SYSTEM + RESTATE_NOTE),
            to_restate))
    background += _links(vocab, to_restate, hidden, restatements, samples, background)

    formal = {
        "symbols": symbols,
        # Assumed domain facts. checks.py uses them only to find more conflicts.
        # The list can be edited by hand: each entry needs id, text and formula.
        "background": background,
        "rules": formal_rules,
    }
    # Step 6 (probe.py) adds "probes" to the rules, and a "check" to the links
    # and to the facts it tests.
    question(llm, formal, vocab, shown, temperature, keep_samples)
    # Step 7 (optional) adds "second" to the rules.
    if second is not None:
        second_reading(second, formal, samples, temperature, keep_samples)

    if keep_samples:
        for rule, answers in zip(formal_rules, answers_per_rule):
            rule["samples"] = answers
        for rule, answers in zip(to_restate, restatements):
            rule["restated_samples"] = answers
        formal["fact_samples"] = fact_answers
    return formal


def formalize_sets(llm: LLM, spec_text: str, sets: int, samples: int = 8,
                   temperature: float = 0.7, keep_samples: bool = False,
                   second: LLM | None = None) -> list[dict]:
    """Formalize the same document `sets` times, each time with its own symbols.

    The read step chooses the symbols, and the findings follow from that
    choice. Formalizing several times shows which findings depend on it
    (checks.combine counts them).

    The first model is the usual one (read step at temperature 0). The others
    use SET_TEMPERATURE, so the model picks different symbols. All models must
    list the same rules: one that splits the document differently is dropped,
    and the rule ids of the first model are used everywhere.

    Returns the formal models, at least one, at most `sets`.
    """
    first = formalize(llm, spec_text, samples, temperature, 0.0, keep_samples, second)
    models = [first]
    for _ in range(sets - 1):
        model = formalize(llm, spec_text, samples, temperature, SET_TEMPERATURE, keep_samples, second)
        if len(model["rules"]) != len(first["rules"]):
            continue  # a different list of rules: its findings could not be matched
        for rule, reference in zip(model["rules"], first["rules"]):
            rule["id"] = reference["id"]
        models.append(model)
    return models


def _translate(llm: LLM, symbol_list: str, rule: dict, samples: int, temperature: float,
               system: str = FORMALIZE_SYSTEM) -> list[dict]:
    """Ask a model to translate one rule into logic, `samples` times.

    This is the one question behind steps 2, 5 and 7. Step 5 shows fewer
    symbols and adds RESTATE_NOTE to the instructions; step 7 puts the very
    same question to the second model.

    symbol_list  the symbols the model may use, as _symbol_list writes them
    """
    prompt = f"Symbols:\n{symbol_list}\n\nRequirement {rule['id']}:\n{rule['text']}"
    return llm.ask(system, prompt, FORMALIZE_SCHEMA, samples, temperature)


def _symbol_list(symbols: list[dict], hidden: set = frozenset()) -> str:
    """The symbols as every prompt shows them, one per line, minus the hidden ones.

    Example line:  - order_submitted: Bool, event - An order has been submitted.
    """
    return "\n".join(
        f"- {s['name']}: {s['sort']}"
        + (f" {{{', '.join(s['values'])}}}" if s["sort"] == "Enum" else "")
        + (", event" if s.get("event") else "")
        + f" - {s['description']}"
        for s in symbols if s["name"] not in hidden
    )


def _read(llm: LLM, spec_text: str, first_temperature: float) -> tuple[list[dict], list[dict]]:
    """Step 1: extract the rules and the symbols, retrying if the symbols are unusable."""
    error = None
    # If the symbol list of the first answer is broken (duplicate or illegal
    # names), ask again with more randomness to get a different one.
    for temperature in (first_temperature, 0.5, 0.9):
        answers = llm.ask(READ_SYSTEM, spec_text, READ_SCHEMA, temperature=temperature,
                          max_tokens=READ_MAX_TOKENS)
        if not answers:
            error = "the model returned no valid JSON"
            continue
        try:
            Vocabulary(answers[0]["symbols"])  # raises ValueError on bad symbols
            return answers[0]["rules"], answers[0]["symbols"]
        except ValueError as problem:
            error = problem
    raise RuntimeError(f"could not get a usable symbol list: {error}")


# ------------------------------------------------------------- step 3: cluster


def _judge(vocab: Vocabulary, answers: list[dict]) -> dict:
    """Cluster the sampled translations of one rule and decide its status.

    Returns the fields that are added to the rule in formal.json:

        status        "accepted", "ambiguous" or "rejected"
        clusters      sizes of the groups of equivalent translations, e.g. [5, 3]
        entropy       how spread out the groups are (0 = full agreement)
        reading, antecedent, consequent    the most common translation
        alternative   the second most common one   } only when the rule
        differs_when  a situation where they differ } is not accepted
    """
    clusters = _group_by_meaning(vocab, answers)
    if not clusters:  # not a single usable translation
        return {"status": "rejected", "clusters": [], "entropy": 0.0}

    clusters.sort(key=len, reverse=True)
    sizes = [len(cluster) for cluster in clusters]
    # Shannon entropy of the cluster sizes: 0 when all samples agree, larger
    # the more evenly they are spread over more interpretations.
    entropy = -sum(n / sum(sizes) * math.log(n / sum(sizes)) for n in sizes)
    if entropy <= LOW_ENTROPY:
        status = "accepted"
    elif entropy <= HIGH_ENTROPY:
        status = "ambiguous"
    else:
        status = "rejected"

    best_answer, best_rule = _simplest(clusters[0])
    # abs() only turns the float "-0.0" of a single cluster into "0.0".
    result = {"status": status, "clusters": sizes, "entropy": abs(round(entropy, 3)), **best_answer}
    if status != "accepted":
        other_answer, other_rule = _simplest(clusters[1])
        result["alternative"] = other_answer
        result["differs_when"] = vocab.difference(best_rule, other_rule)
    return result


def _group_by_meaning(vocab: Vocabulary, answers: list[dict], given: list = (),
                      allowed=None) -> list[list[tuple[dict, Rule]]]:
    """Group translations by meaning: steps 3, 5 and 7 all count them this way.

    Each group is a list of (answer, compiled rule) that mean the same, in the
    order the answers came. An answer that cannot be compiled (an unknown
    symbol, a malformed formula, "none") does not count.

    given    what the comparison may take as true (step 7: the required events)
    allowed  a test a compiled answer must pass to count (step 5: no hidden symbol)
    """
    groups: list[list[tuple[dict, Rule]]] = []
    for answer in answers:
        try:
            compiled = vocab.rule({"id": "", **answer})
        except ValueError:
            continue
        if allowed is not None and not allowed(compiled):
            continue
        for group in groups:
            if vocab.same_meaning(group[0][1], compiled, given):
                group.append((answer, compiled))
                break
        else:
            groups.append([(answer, compiled)])
    return groups


def _simplest(cluster: list[tuple[dict, Rule]]) -> tuple[dict, Rule]:
    """Pick the shortest formula of a cluster; they all mean the same anyway."""
    return min(cluster, key=lambda pair: len(pair[0]["antecedent"]) + len(pair[0]["consequent"]))


# ---------------------------------------------------------- step 4: facts vote


def _agreed_facts(vocab: Vocabulary, answers: list[dict], asked: int) -> list[dict]:
    """Keep the domain facts that a majority of the sampled answers agree on.

    answers  the LLM's answers, each {"facts": [{"text": ..., "formula": ...}]}
    asked    how many answers were requested (some may have come back unusable)

    Two answers rarely word a fact the same way, so agreement is decided by
    logic: an answer "agrees" with a fact when the fact follows from that
    answer's own facts. "a and b exclude each other" therefore also counts as
    agreement with "a implies not b".

    Returns the "background" list of formal.json:
        {"id": "F1", "text": ..., "formula": ..., "support": "7/8"}
    """
    # Each answer becomes the list of its usable facts, as (fact dict, Z3 formula).
    usable: list[list[tuple[dict, z3.BoolRef]]] = []
    for answer in answers:
        facts = []
        for fact in answer["facts"]:
            try:
                facts.append((fact, vocab.parse(fact["formula"])))
            except ValueError:
                continue  # unknown symbol or malformed formula: this fact does not count
        # An answer that contradicts itself would "agree" with everything.
        if not vocab.impossible([formula for _, formula in facts]):
            usable.append(facts)

    # Count the agreement for every fact of every answer.
    candidates = []  # (number of agreeing answers, fact dict, Z3 formula)
    for facts in usable:
        for fact, formula in facts:
            if vocab.implies([], formula):
                continue  # true by logic alone (like "a or not a"): says nothing
            agreeing = sum(vocab.implies([f for _, f in other], formula) for other in usable)
            candidates.append((agreeing, fact, formula))
    # Best supported first; among equals the shortest formula.
    candidates.sort(key=lambda c: (-c[0], len(c[1]["formula"])))

    kept: list[dict] = []
    kept_formulas: list[z3.BoolRef] = []
    for agreeing, fact, formula in candidates:
        if agreeing <= MAJORITY * asked:
            continue  # no majority
        if vocab.implies(kept_formulas, formula):
            continue  # already said by the facts kept so far
        if vocab.impossible(kept_formulas + [formula]):
            continue  # contradicts the (better supported) facts kept so far
        kept_formulas.append(formula)
        kept.append({"id": f"F{len(kept) + 1}", "text": fact["text"],
                     "formula": fact["formula"], "support": f"{agreeing}/{asked}"})
    return kept


# ---------------------------------------------------------------- step 5: links


def _symbols_to_hide(vocab: Vocabulary, formal_rules: list[dict]) -> dict[str, set[str]]:
    """Which rules are translated again in step 5, and without which symbols.

    A rule qualifies when its consequent uses a symbol that no other rule
    uses. Such a private symbol hides meaning from the solver: "the record is
    removed", as a symbol of its own, cannot clash with "the record is
    retained", whatever the words say.

    For the second translation the model may use only
        - the symbols of the rule's own antecedent (when it applies), and
        - the symbols in the consequents of the OTHER rules (outcomes).
    Outcomes are linked to outcomes only. Shown everything, the model also
    "explained" outcomes by the events of other rules ("the system prompts for
    confirmation" became "the owner confirms").

    Returns {rule id: names to hide}, only for the rules that qualify.
    """
    compiled = {rule["id"]: vocab.rule(rule) for rule in formal_rules if rule["status"] != "rejected"}
    hide = {}
    for rule_id, rule in compiled.items():
        others = [other for other_id, other in compiled.items() if other_id != rule_id]
        used_elsewhere = set().union(*(vocab.symbols_in(other.formula) for other in others))
        other_outcomes = set().union(*(vocab.symbols_in(other.consequent) for other in others))
        private = vocab.symbols_in(rule.consequent) - used_elsewhere
        if private and other_outcomes:
            visible = vocab.symbols_in(rule.antecedent) | other_outcomes
            hide[rule_id] = set(vocab.variables) - visible
    return hide


def _links(vocab: Vocabulary, rules: list[dict], hidden: dict[str, set[str]],
           answers_per_rule: list[list[dict]], asked: int, facts: list[dict]) -> list[dict]:
    """Turn the second translations of step 5 into assumed facts ("links").

    rules             the rules that were translated again
    hidden            the symbols each of them was not shown (see _symbols_to_hide)
    answers_per_rule  the N answers for each of them
    asked             N
    facts             the facts kept so far (step 4)

    If more than half of the N answers agree on one meaning, written with the
    symbols the other rules use, that meaning is linked to the rule:

        rule            confirmed => record_removed          (private symbol)
        agreed answer   confirmed => (not record_retained)
        link            (confirmed and record_removed) => (not record_retained)

    The link is an assumed fact like those of step 4: checks.py uses it only
    to find more conflicts, and a conflict that needs it says so. An answer of
    "none" (the other symbols cannot express the rule) counts against a link.
    """
    kept = [vocab.parse(fact["formula"]) for fact in facts]
    links = []
    for rule, answers in zip(rules, answers_per_rule):
        # An answer that uses a symbol it was not shown does not count.
        clusters = _group_by_meaning(vocab, answers, allowed=lambda candidate: not (
            vocab.symbols_in(candidate.formula) & hidden[rule["id"]]))
        if not clusters:
            continue
        best = max(clusters, key=len)
        if len(best) <= MAJORITY * asked:
            continue  # no majority for one meaning
        answer, _ = _simplest(best)
        formula_text = f"(=> (and {answer['antecedent']} {rule['consequent']}) {answer['consequent']})"
        formula = vocab.parse(formula_text)
        # A link is kept even when the voted facts already imply it: step 6
        # may reject one of those facts (check 3), and the link must not go
        # with it.
        if vocab.impossible(kept + [formula]):
            continue  # contradicts the facts kept so far
        kept.append(formula)
        links.append({
            "id": f"F{len(facts) + len(links) + 1}",
            "text": f"What {rule['id']} demands, in the terms of the other requirements: {answer['reading']}",
            "formula": formula_text,
            "support": f"{len(best)}/{asked}",
            "restates": rule["id"],
            # The agreed restatement itself; step 6 checks the link with it.
            "antecedent": answer["antecedent"],
            "consequent": answer["consequent"],
        })
    return links


# ------------------------------------------------------- step 7: second reader


def second_reading(llm: LLM, formal: dict, samples: int = 8, temperature: float = 0.7,
                   keep_samples: bool = False) -> None:
    """Step 7 (optional): a second model translates every rule, and Z3 compares.

    llm     the second model, of another family than the one that made `formal`
    formal  the formal model, changed in place

    The 8 samples of step 2 come from one model, which makes the same choice
    again and again, also where a reader would hesitate (research.md 4.1). A
    second model is an independent reader. It gets exactly the prompt of
    step 2: the same symbols and the same requirement, 8 times. The
    translation is confirmed when more than half of its 8 answers mean the
    same (the majority rule of facts, links and questions). Example:

        requirement   "WHEN a comment has been reported three times THEN hide it"
        translation   (= report_count 3) => comment_hidden    main model, 8 of 8
        second model  (>= report_count 3) => comment_hidden   5 of its 8 answers
                      (= report_count 3) => comment_hidden    3 of its 8 answers
        verdict       not confirmed (3 of 8): the rule is ambiguous

    Adds rule["second"] to every rule that has a translation (see
    judge_second); checks.settled() turns "not confirmed" into an ambiguity.
    """
    shown = _symbol_list(formal["symbols"])
    rules = [rule for rule in formal["rules"] if rule.get("status") != "rejected"]
    with ThreadPoolExecutor(max_workers=16) as pool:  # LLM calls only; Z3 below
        answers_per_rule = list(pool.map(
            lambda rule: _translate(llm, shown, rule, samples, temperature), rules))

    vocab = Vocabulary(formal["symbols"])
    for rule, answers in zip(rules, answers_per_rule):
        rule["second"] = judge_second(vocab, rule, answers, samples)
        if keep_samples:
            rule["second"]["samples"] = answers


def judge_second(vocab: Vocabulary, rule: dict, answers: list[dict], asked: int) -> dict:
    """Step 7, the Z3 part: does the second model confirm the translation of `rule`?

    answers  the second model's translations of the rule
    asked    how many were requested (an unusable answer counts as not confirming)

    Returns the "second" entry of the rule:

        {"support": "3/8",      how many of its answers mean the same as the translation
         "confirms": False,     more than half of them?
         "reading", "antecedent", "consequent",   its most common OTHER reading, if any
         "differs_when": {...}}                   a situation where that one and the
                                                  translation differ

    The answers are compared only where the events that the translation's
    condition requires happen. Whether a model also writes the event into
    the rule is a detail of modelling, not a reading of the words:

        "WHEN a courier fails to deliver an order for the second time THEN ..."
        translation   (and delivery_failed (= failed_deliveries 2)) => ...
        answer        (= failed_deliveries 2) => ...        the same, once delivery_failed happens
    """
    translation = vocab.rule(rule)
    required = [vocab.variables[name] for name in sorted(vocab.events)
                if vocab.implies([translation.antecedent], vocab.variables[name])]

    same, others = 0, []  # answers that mean the translation; groups of other readings
    for group in _group_by_meaning(vocab, answers, required):
        if vocab.same_meaning(translation, group[0][1], required):
            same += len(group)
        else:
            others.append(group)

    second = {"support": f"{same}/{asked}", "confirms": same > MAJORITY * asked}
    if others:
        answer, compiled = _simplest(max(others, key=len))
        second.update({key: answer[key] for key in ("reading", "antecedent", "consequent")})
        second["differs_when"] = vocab.difference(translation, compiled, required)
    return second
