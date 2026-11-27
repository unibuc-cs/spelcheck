"""probe.py: double-checks what the LLM decided earlier, by asking it simple questions.

Why: earlier steps keep whatever most of 8 LLM answers say. But 8 answers
from the same model often repeat the same mistake. So here the LLM gets a
different, simpler question, about ONE requirement at a time.

Five checks. Each question is asked 8 times and the answers are counted.

1. Does the requirement really mean what we translated?

     "WHEN the failed attempts reach 5, lock the account"
     our translation:          exactly 5 attempts
     another possible reading: 5 or more attempts
     question:  "6 attempts, account not locked: which reading do the
                 words mean, A, B, or either?"
     result:    if our translation gets half of the answers or fewer, the
                requirement is reported as ambiguous.

2. Does the requirement really say what a link claims?

     A link is an extra fact made in step 5, e.g. "removing the record
     means it is no longer kept in the database".
     question:  "The owner confirmed deletion, and the record is still in
                 the database. Does the requirement allow that?"
     result:    if most answers say no ("impossible"), the link is kept;
                otherwise it is dropped.

3. Does the requirement agree with a fact that contradicts it?

     A fact is a general truth voted in step 4. Some facts make a
     requirement impossible to obey, e.g. the fact "a deleted record is
     removed" against the requirement "keep deleted records for audits".
     Only such facts are asked about.
     question:  "Does the requirement agree with this fact?"
     result:    if most answers say "contradicts", the fact is dropped.

4. Can what two requirements demand both be the case?  (outcomes, below)

     Two rules that can apply in the same situation, written with different
     symbols: "take the price from the balance" became payment_taken, and
     "refuse all payments" became payment_refused. To Z3 both can be true,
     so it sees no conflict, unless a fact says that they exclude each other.
     question:  "A: payment_taken is TRUE. B: payment_refused is TRUE.
                 Can both hold in the same snapshot?"
     result:    if most answers say "impossible", that becomes an assumed
                fact, (not (and payment_taken payment_refused)). Like every
                assumed fact it can only add a conflict, and the report
                quotes it.

5. Can the conditions of two requirements that clash both hold?  (conditions, below)

     Two rules that clash only in a situation that cannot happen: "WHEN
     tasks.md does not exist THEN proceed without a warning" and "WHEN the
     agent reads tasks.md AND incomplete tasks are found THEN display a
     warning". To Z3 a file can be read and not exist, so it reports a
     conflict there, unless a fact says that the two conditions exclude each
     other.
     question:  "A: tasks_md_exists is FALSE. B: tasks_md_read is TRUE,
                 all_tasks_complete is FALSE. Can both hold in the same
                 snapshot?"
     result:    if most answers say "impossible", that becomes an assumed
                fact, (not (and <condition of one> <condition of the other>)).
                A conflict proven from the rules alone then stays in the
                report, marked doubtful; one that needs an assumed fact is
                not found any more (checks.find_conflicts).

    Check 6     for two rules a and b: does what a demands make b apply?
                The other checks compare what two rules demand, or their two
                conditions. A contradiction can also be a chain:

                    R1  "WHEN a call of check_in_guest succeeds in a run with a plan
                         THEN an earlier call of ask_manager in the run was approved"
                    R4  "WHEN a call of ask_manager is made THEN the run is not a late-arrival run"
                    R5  "WHEN a call of check_in_guest succeeds in a late-arrival run THEN ..."

                In a late-arrival run with a plan in which a guest is checked
                in, R1 demands an approved call, and R4 says that no such
                call is made there. No two of the three clash by themselves:
                nothing says that an approved call is a call that was made.
                So the model is asked, with the words of R1: "Where this
                requirement applies and is obeyed, is this the case: a call
                of ask_manager is made?" If most answers say "yes", it is an
                assumed fact, and Z3 finds the conflict of R1 and R4 with
                it. Asked only where the answer can add a finding (see
                `applies`).

In formal.json the answers end up under "probes" (in a rule), "check" (in a
link or a fact), "outcome_pairs", "condition_pairs" and "apply_pairs"; a fact
of checks 4 to 6 has "between", one of check 5 also "about": "conditions",
and one of check 6 "about": "applies".

A spec about an agent that calls tools has rules about a whole run ("WHEN a
call of ship_parcel succeeds in a run with a plan THEN an earlier
request_signoff was approved"). When the formal model says so
("situation": "run", set by `formalize(whole_run=True)`), checks 4 and 5 also
ask about two rules that react to two different happenings, since both can
be in one run, and their prompts say "run" where they say "snapshot" (_about).
"""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import NamedTuple

import z3

from .llm import LLM
from .logic import Vocabulary, describe


class Question(NamedTuple):
    """One question of step 6, and where its answers are stored."""

    system: str                # the instructions: QUESTION_SYSTEM (check 1) or LINK_SYSTEM (check 2)
    schema: dict               # the form of the answer
    prompt: str                # the requirement, the readings or the situation, as the LLM sees them
    answers: int               # how many answers to draw
    record: dict               # where the answers go: a situation of check 1, or a link's "check"
    translation_first: bool | None  # check 1: is the translation shown as reading A? (check 2: None)


# The majority rule of the whole pipeline: a voted fact, a link, a second
# reader's confirmation each need more than this share of the answers
# (formalize.py uses it too).
MAJORITY = 0.5
# Answers drawn per reading or link, spread over its situations (and orders).
ANSWERS = 8
# At most this many other readings are tried per rule.
MAX_READINGS = 3
# Check 4 asks about at most this many pairs of rules, the first ones in the
# document. The six-rule specs of the evaluation have 2 to 5 pairs each.
MAX_PAIRS = 40

READINGS_SYSTEM = """\
You look for other ways to read ONE requirement. You get the requirement, the \
symbols of a formal model, and the reading the requirement was given so far, \
in words and in logic.

People do not always take the same meaning from the same words. Give the two \
or three most plausible other readings, even when the requirement seems clear \
to you: each one is checked against the words afterwards, and a reading the \
words do not support does no harm. Look first at the words that decide what \
applies to what:
- "if", "only", "unless": a reading in which the word covers a different part \
of the sentence (all of it, or only the last part);
- "and", "or": a reading in which they group the conditions differently;
- a boundary (exactly, at least, more than, within, between, after): a reading \
with the boundary value included or excluded.

Each reading must be one a developer could defend from the words alone. Use \
only the symbols that the reading so far uses: other readings of the same \
words, not readings about other facts.

Write each reading like the given one: reading (one sentence), antecedent and \
consequent as SMT-LIB boolean expressions over the listed symbols, in prefix \
notation: (and a b), (or a b), (not a), (=> a b), (= x 5), (>= x 5), true. \
Compare an Enum symbol with one of its values like this: (= state closed)."""

READINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "readings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "reading": {"type": "string"},
                    "antecedent": {"type": "string"},
                    "consequent": {"type": "string"},
                },
                "required": ["reading", "antecedent", "consequent"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["readings"],
    "additionalProperties": False,
}

QUESTION_SYSTEM = """\
You get ONE requirement, two readings of it, and one concrete situation in \
which the two readings disagree: one says the situation obeys the \
requirement, the other says it breaks it.

Do the words of the requirement, read exactly as written, decide which \
reading is meant? Answer:
- A: the words support reading A, not reading B.
- B: the words support reading B, not reading A.
- either: a careful reader could take the words either way.

The situation is a list of facts, each marked TRUE or FALSE, or given a \
value. A fact marked FALSE is not the case. Facts that are not listed may be \
either way.

First give the reason in one or two sentences, then the answer."""

QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "answer": {"enum": ["A", "B", "either"]},
    },
    "required": ["reason", "answer"],
    "additionalProperties": False,
}

LINK_SYSTEM = """\
You decide what ONE requirement implies. You get the requirement and a \
situation in which it applies.

Assume that the system does everything the requirement demands, with its \
words read exactly as written, in their plain meaning. Could all the listed \
facts then still be true?

The situation is a list of facts, each marked TRUE or FALSE, or given a \
value. A fact marked FALSE is not the case.

Answer:
- possible: the requirement can be fully obeyed while all the facts are true.
- impossible: obeying the requirement, as written, rules out these facts.
- unclear: the words can reasonably be read both ways.

First give the reason in one or two sentences, then the answer."""

LINK_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "answer": {"enum": ["possible", "impossible", "unclear"]},
    },
    "required": ["reason", "answer"],
    "additionalProperties": False,
}

FACT_SYSTEM = """\
You decide whether ONE requirement agrees with a statement that was assumed \
to hold in every situation of the system the requirement is about.

Read the requirement exactly as written, in its plain meaning. Answer:
- agrees: the statement can hold in every situation the requirement is about.
- contradicts: the words of the requirement show situations in which the \
statement is false.
- unclear: the words can reasonably be read both ways.

First give the reason in one or two sentences, then the answer."""

FACT_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "answer": {"enum": ["agrees", "contradicts", "unclear"]},
    },
    "required": ["reason", "answer"],
    "additionalProperties": False,
}


OUTCOMES_SYSTEM = """\
You get two statements, A and B, about ONE snapshot of a software system. \
Each is a list of facts, each marked TRUE or FALSE, or given a value. A fact \
marked FALSE is not the case.

Can A and B both hold in the same snapshot? Judge only by what the facts \
mean, as their descriptions say. Answer:
- impossible: A and B exclude each other by their meaning (a lamp cannot be \
lit and dark at once; if every drawer is shut, the top drawer is not open).
- possible: both can hold together (a form can be signed and also dated), \
even if a system would rarely do both. This is also the answer when one of \
them would usually cause, need or leave a trace of the other, or of its \
opposite: do not assume how the system works, or that anything succeeds or is \
written down (a letter can be sent back unopened with no note made of it; a \
pot can be hot although nobody lit the stove today). And it is the answer \
when A and B can be about two different things: two objects, a limit and \
what happened, all of one kind and some of another (a jar can be made for 40 \
marbles and hold none; every window upstairs can be shut while one downstairs \
is open). If one statement alone looks like something no system would do, \
that is no reason: judge only whether the two exclude each other.
- unclear: the descriptions can reasonably be read both ways.

First give the reason in one or two sentences, then the answer. If the answer \
is impossible, also write the fact that excludes the two as one plain \
sentence ("A lamp cannot be lit and dark at once."); otherwise leave "fact" \
empty."""

OUTCOMES_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "answer": {"enum": ["possible", "impossible", "unclear"]},
        "fact": {"type": "string"},
    },
    "required": ["reason", "answer", "fact"],
    "additionalProperties": False,
}


def question(llm: LLM, formal: dict, vocab: Vocabulary, symbol_list: str,
             temperature: float, keep_answers: bool = False, only: set | None = None) -> None:
    """Step 6: check 1 on the rules, check 2 on the links, check 3 on the facts of `formal`.

    formal        the formal model: "probes" are added to its rules, and a
                  "check" to its links and to the facts that check 3 tests
    symbol_list   the symbols as shown to the model in the other steps
    keep_answers  also store every answer with its reason, and the readings
                  the model proposed (for the experiments)
    only          the ids of the rules to ask about, or None for all. Used
                  when rules were added to a model whose other rules have
                  their answers already (formalize with `base`).
    """
    def asked(rule_id: str) -> bool:
        return only is None or rule_id in only

    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    text_of = {rule["id"]: rule["text"] for rule in formal["rules"]}
    agreed = [rule for rule in formal["rules"] if rule["status"] == "accepted" and asked(rule["id"])]
    split = [rule for rule in formal["rules"]
             if rule["status"] == "ambiguous" and "alternative" in rule and asked(rule["id"])]
    # formal["background"] holds both kinds of assumed facts. A voted fact
    # (step 4) has an id, a text and a formula. A link (step 5) has, besides,
    # "restates": the id of the rule it restates, and the agreed restatement
    # itself, which check 2 needs:
    #     {"id": "F1", "restates": "D2",
    #      "formula": "(=> (and deletion_confirmed property_record_removed)
    #                      (not property_record_retained_in_db))",
    #      "antecedent": "deletion_confirmed",
    #      "consequent": "(not property_record_retained_in_db)", ...}
    links = [fact for fact in formal["background"] if "restates" in fact and asked(fact["restates"])]
    # Z3 picks only situations that the voted facts allow, so that they are
    # realistic (a record is not both removed and kept). The links are left
    # out: they are what check 2 tests. So are the facts of check 4
    # ("between"), which a base model may have.
    voted = {fact["id"]: fact for fact in formal["background"]
             if "restates" not in fact and "between" not in fact}
    facts = [vocab.parse(fact["formula"]) for fact in voted.values()]

    # Check 1, the LLM: other readings of the rules whose samples agreed. (For a
    # rule whose samples split, the other reading is the second group.)
    def readings_of(rule: dict) -> list[dict]:
        prompt = (f"Symbols:\n{symbol_list}\n\nRequirement {rule['id']}:\n{rule['text']}\n\n"
                  f"Its reading so far: {rule['reading']}\n"
                  f"In logic: antecedent {rule['antecedent']}, consequent {rule['consequent']}")
        answers = llm.ask(READINGS_SYSTEM, prompt, READINGS_SCHEMA)
        return answers[0]["readings"][:MAX_READINGS] if answers else []

    with ThreadPoolExecutor(max_workers=16) as pool:
        proposals = list(pool.map(readings_of, agreed))

    # Checks 1 and 2, with Z3: drop the readings that mean the same as the
    # translation, and pick the situations to ask about.
    for rule, proposed in zip(agreed, proposals):
        rule["probes"] = _other_readings(vocab, rule, proposed, facts, same_symbols=True)
        if keep_answers:
            rule["proposed_readings"] = proposed
    for rule in split:
        rule["probes"] = _other_readings(vocab, rule, [rule["alternative"]], facts, same_symbols=False)
    questions: list[Question] = []
    for rule in agreed + split:
        for probe in rule["probes"]:
            # The 8 answers are spread over the situations and the two orders.
            share = max(1, ANSWERS // (2 * len(probe["situations"]))) if probe["situations"] else 0
            for situation in probe["situations"]:
                for translation_first in (True, False):
                    prompt = _pair_prompt(rule, probe, situation, translation_first, descriptions)
                    questions.append(Question(QUESTION_SYSTEM, QUESTION_SCHEMA, prompt, share,
                                              record=situation, translation_first=translation_first))
    rule_of = {rule["id"]: rule for rule in formal["rules"]}
    for link in links:
        when = _link_situation(vocab, link, facts)
        if when is not None:
            link["check"] = {"when": when}
            prompt = (f"Requirement:\n{text_of[link['restates']]}\n\n"
                      f"Situation:\n{describe(when, descriptions)}")
            questions.append(Question(LINK_SYSTEM, LINK_SCHEMA, prompt, ANSWERS,
                                      record=link["check"], translation_first=None))
        # A link that only renames (see _renamed) is also asked about with
        # both symbols in view: can the one hold and the other not?
        apart = _renamed(vocab, rule_of[link["restates"]], link)
        if apart:
            own, other = apart
            link.setdefault("check", {})["renames"] = {"own": own, "other": other}
            prompt = (f"Statement A:\n{describe(own, descriptions)}\n\n"
                      f"Statement B:\n{describe(other, descriptions)}")
            questions.append(Question(_about(OUTCOMES_SYSTEM, formal), OUTCOMES_SCHEMA, prompt, ANSWERS,
                                      record=link["check"]["renames"], translation_first=None))
    # Check 3, Z3: the voted facts that make a requirement impossible to obey.
    voted_formulas = {fact_id: vocab.parse(fact["formula"]) for fact_id, fact in voted.items()}
    suspects: dict[str, dict] = {}  # fact id -> the first rule it contradicts
    for rule in formal["rules"]:
        if rule.get("status") != "rejected" and asked(rule["id"]):
            for fact_id in _contradicting_facts(vocab, vocab.rule(rule), voted_formulas):
                suspects.setdefault(fact_id, rule)
    for fact_id, rule in suspects.items():
        voted[fact_id]["check"] = {"against": rule["id"]}
        prompt = f"Requirement:\n{rule['text']}\n\nStatement:\n{voted[fact_id]['text']}"
        questions.append(Question(FACT_SYSTEM, FACT_SCHEMA, prompt, ANSWERS,
                                  record=voted[fact_id]["check"], translation_first=None))

    # All three checks: ask every question at once.
    def ask(question: Question) -> list[dict]:
        return llm.ask(question.system, question.prompt, question.schema, question.answers, temperature)

    with ThreadPoolExecutor(max_workers=16) as pool:
        replies = list(pool.map(ask, questions))
    for question, answers in zip(questions, replies):
        question.record.setdefault("replies", []).append((question.translation_first, answers))

    # Count the answers, and decide about the links and facts.
    for rule in agreed + split:
        for probe in rule["probes"]:
            _decide_reading(probe, keep_answers)
    # A link is used only when most answers say "impossible" (or none came back).
    for link in links:
        if "check" in link:
            confirmed = True
            if "when" in link["check"]:
                counts = _count(link["check"], LINK_SCHEMA, keep_answers)
                total = sum(counts.values())
                confirmed = not total or counts["impossible"] > MAJORITY * total
            # A link that only renames: the two symbols must be one thing, so
            # most answers must say that the one cannot hold without the other.
            if "renames" in link["check"]:
                counts = _count(link["check"]["renames"], OUTCOMES_SCHEMA, keep_answers)
                total = sum(counts.values())
                confirmed = confirmed and (not total or counts["impossible"] > MAJORITY * total)
            link["check"]["verdict"] = "confirmed" if confirmed else "rejected"
    # A voted fact already has a majority behind it, so it is left out only when
    # most answers say the requirement contradicts it.
    for fact_id in suspects:
        counts = _count(voted[fact_id]["check"], FACT_SCHEMA, keep_answers)
        rejected = counts["contradicts"] > MAJORITY * sum(counts.values())
        voted[fact_id]["check"]["verdict"] = "rejected" if rejected else "confirmed"


def _other_readings(vocab: Vocabulary, rule: dict, proposed: list[dict], facts: list,
                    same_symbols: bool) -> list[dict]:
    """Check 1: the readings that differ from the translation, and their situations.

    same_symbols  keep only readings over the translation's own symbols. Used
                  for readings the model proposes: one with other symbols
                  usually borrows a condition from another requirement ("only
                  if the order is not canceled"), and the answers would then
                  be about that requirement, not about these words.

    For each reading kept, up to two situations: one in which the translation
    is obeyed and the reading broken, and, if there is one, the other way round.
    """
    translation = vocab.rule(rule)
    kept, kept_rules = [], []
    for reading in proposed:
        try:
            other = vocab.rule({"id": rule["id"], **reading})
        except (ValueError, KeyError):
            continue  # unknown symbol or malformed formula
        if same_symbols and not vocab.symbols_in(other.formula) <= vocab.symbols_in(translation.formula):
            continue  # a reading about other facts
        if vocab.same_meaning(translation, other):
            continue  # means the same as the translation
        if any(vocab.same_meaning(other, earlier) for earlier in kept_rules):
            continue  # means the same as a reading already kept
        relevant = vocab.symbols_in(translation.formula) | vocab.symbols_in(other.formula)
        situations = []
        for translation_obeyed in (True, False):
            differ = ([translation.formula, z3.Not(other.formula)] if translation_obeyed
                      else [z3.Not(translation.formula), other.formula])
            model = vocab.model(differ + facts)
            if model is None:
                model = vocab.model(differ)  # the facts rule it out; ask anyway
            if model is not None:
                situations.append({"when": vocab.witness(model, relevant),
                                   "translation_says": "obeyed" if translation_obeyed else "broken"})
        kept_rules.append(other)
        kept.append({"reading": reading["reading"], "antecedent": reading["antecedent"],
                     "consequent": reading["consequent"], "situations": situations})
    return kept


def _pair_prompt(rule: dict, probe: dict, situation: dict, translation_first: bool,
                 descriptions: dict) -> str:
    """Check 1: the question about one situation (requirement, readings A and B, facts)."""
    says = situation["translation_says"]
    translation = (rule["reading"], rule["antecedent"], rule["consequent"], says)
    other = (probe["reading"], probe["antecedent"], probe["consequent"],
             "broken" if says == "obeyed" else "obeyed")
    first, second = (translation, other) if translation_first else (other, translation)

    def block(label: str, reading: tuple) -> str:
        sentence, antecedent, consequent, verdict = reading
        return (f"Reading {label}: {sentence} [in logic: {antecedent} => {consequent}]\n"
                f"In the situation below, reading {label} says the requirement is {verdict}.")

    return (f"Requirement:\n{rule['text']}\n\n{block('A', first)}\n\n{block('B', second)}\n\n"
            f"Situation:\n{describe(situation['when'], descriptions)}")


def _link_situation(vocab: Vocabulary, link: dict, facts: list) -> dict | None:
    """Check 2: a situation in which the rule applies and the link's claim is false.

    For D2: deletion_confirmed = TRUE, property_record_retained_in_db = TRUE.
    The situation uses only the symbols of the restatement that the link keeps
    ("antecedent", "consequent"), not D2's own symbol property_record_removed:
    that symbol's description ("removed from the active data set") is the
    lenient reading that the link is there to get around.
    """
    restated = vocab.rule({"id": link["restates"], "antecedent": link["antecedent"],
                           "consequent": link["consequent"]})
    broken = [restated.antecedent, z3.Not(restated.consequent)]
    model = vocab.model(broken + facts)
    if model is None:
        model = vocab.model(broken)
    if model is None:
        return None
    return vocab.witness(model, vocab.symbols_in(restated.formula))


def _renamed(vocab: Vocabulary, rule: dict, link: dict) -> tuple[dict, dict] | None:
    """Is the link the rule's own demand, moved to another symbol? Then: a case of the two apart.

    Step 5 hides the symbol with which a rule says what it demands, and the
    model writes the demand with the symbols of the other rules. That finds
    two names for one thing. It also happens that the model takes the nearest
    name for another thing:

        rule    "... `shipping.max_parcels` is the integer 20"   (= shipping_max_parcels 20)
        link    the same demand, for the limit of a batch        (= shipping_max_batch_parcels 20)

    Check 2 confirms such a link, because its question does not show the
    rule's own symbol: the model takes the one it sees for the one in the
    requirement. So when the restatement is the rule's own demand with one
    symbol swapped for another of its kind, a second question shows both:

        A: shipping_max_parcels = 20 (the most parcels in one request)
        B: shipping_max_batch_parcels = 21 (the most parcels in one batch)

    If the two are one thing, A and B cannot both hold. Returned are A and B,
    or None when the link is not of this shape.
    """
    own = vocab.rule(rule).consequent
    restated = vocab.parse(link["consequent"])
    own_names, other_names = vocab.symbols_in(own), vocab.symbols_in(restated)
    if len(own_names) != 1 or len(other_names) != 1 or own_names == other_names:
        return None
    (own_name,), (other_name,) = own_names, other_names
    own_symbol, other_symbol = vocab.variables[own_name], vocab.variables[other_name]
    if own_symbol.sort() != other_symbol.sort():
        return None
    if not vocab.impossible([z3.Xor(z3.substitute(own, (own_symbol, other_symbol)), restated)]):
        return None  # not the same demand
    holds = vocab.model([own])
    if holds is None:
        return None
    # A value of the other symbol that breaks the restatement; for a number,
    # the one next to the value of the rule's own symbol (20 and 21).
    near = []
    if z3.is_arith(own_symbol):
        value = holds.eval(own_symbol, model_completion=True)
        near = [[other_symbol == value + step] for step in (1, -1)]
    broken = next((model for model in (vocab.model([z3.Not(restated)] + extra) for extra in near + [[]])
                   if model is not None), None)
    if broken is None:
        return None
    return vocab.witness(holds, own_names), vocab.witness(broken, other_names)


def _decide_reading(probe: dict, keep_answers: bool) -> None:
    """Check 1: count the answers about one other reading (checks.settled decides)."""
    counts = {"translation": 0, "other": 0, "either": 0}
    for situation in probe["situations"]:
        for translation_first, replies in situation.pop("replies", []):
            for reply in replies:
                if reply["answer"] == "either":
                    counts["either"] += 1
                # "A" is the translation when it was shown first, else "B" is.
                elif (reply["answer"] == "A") == translation_first:
                    counts["translation"] += 1
                else:
                    counts["other"] += 1
                if keep_answers:
                    situation.setdefault("answers", []).append(
                        {**reply, "translation_first": translation_first})
    probe["answers"] = counts


def _count(check: dict, schema: dict, keep_answers: bool) -> dict:
    """Checks 2 and 3: count the answers to one question, by answer, and store them."""
    replies = [reply for _, answers in check.pop("replies", []) for reply in answers]
    counts = {choice: 0 for choice in schema["properties"]["answer"]["enum"]}
    for reply in replies:
        counts[reply["answer"]] += 1
    check["answers"] = counts
    if keep_answers:
        check["replies"] = replies
    return counts


def _contradicting_facts(vocab: Vocabulary, rule, facts: dict) -> list[str]:
    """Check 3: the smallest set of facts that makes `rule` impossible to obey.

    facts  fact id -> formula (the voted facts)

    Returns [] when the rule can be obeyed somewhere it applies (or never
    applies). Otherwise the ids of a set of facts that rules that out, from
    which no fact can be dropped.
    """
    obeyed = [rule.antecedent, rule.consequent]
    if vocab.impossible([rule.antecedent]) or not vocab.impossible(obeyed + list(facts.values())):
        return []
    needed = list(facts)
    for fact_id in list(needed):
        others = [other for other in needed if other != fact_id]
        if vocab.impossible(obeyed + [facts[other] for other in others]):
            needed = others  # not needed: the rule is impossible to obey without it
    return needed


# ------------------------------------------------------------------- check 4


# Check 5 asks about two conditions. Its prompt says more than that of check
# 4 about what "impossible" may rest on. Asked with the prompt of check 4, the
# model also called impossible what a well-behaved system would merely
# prevent: "An out-of-service machine cannot accept a container insertion",
# for a rule that says what the machine does when it is out of service (T33).
CONDITIONS_SYSTEM = """\
You get two statements, A and B, about ONE snapshot of a software system and \
its surroundings. Each is a list of facts, each marked TRUE or FALSE, or \
given a value. A fact marked FALSE is not the case. A is the situation in \
which one requirement applies, B the situation in which another applies.

Can A and B both be the case in the same snapshot? Judge only by what the \
facts mean, as their descriptions say. Answer:
- impossible: by the meaning of the words alone, one cannot be true while \
the other is (a candle that was never lit cannot be blown out; a jar cannot \
be both sealed and open).
- possible: both can be the case together. This is also the answer when one \
of them is a state in which the other should not happen, is not allowed, or \
would be unusual. Do not assume that the system or its users prevent \
anything, or that anything succeeds (a lawn can be closed to walkers, and \
someone can still walk on it).
- unclear: the descriptions can reasonably be read both ways.

First give the reason in one or two sentences, then the answer. If the answer \
is impossible, also write the fact that excludes the two as one plain \
sentence ("A candle that was never lit cannot be blown out."); otherwise \
leave "fact" empty."""


def _about(prompt: str, formal: dict) -> str:
    """The prompt of a question about two statements, for the kind of situation the spec is about.

    A moment (the default), or a whole run of the system, in which things
    happen one after the other ("situation": "run" in the formal model).
    """
    if formal.get("situation") != "run":
        return prompt
    return (prompt
            .replace("ONE snapshot of a software system", "ONE run of a software system")
            .replace("ONE snapshot of that system", "ONE run of that system")
            .replace("in the same snapshot?",
                     "in the same run? A run goes from a request to its end, and what the "
                     "statements say may happen at different times in it."))


def _first(pairs: list[tuple], first: set | None) -> list[tuple]:
    """The pairs with one of the rules in `first` in front, in their order (see outcomes)."""
    if not first:
        return pairs
    return sorted(pairs, key=lambda pair: not (pair[0]["id"] in first or pair[1]["id"] in first))


def outcomes(llm: LLM, formal: dict, vocab: Vocabulary, temperature: float,
             keep_answers: bool = False, only: set | None = None, first: set | None = None) -> None:
    """Step 6, check 4: for rules that can apply together, can both get what they demand?

    Runs after the other checks, on the links and facts they left standing.
    The model sees only the two outcomes, as facts with their descriptions,
    not the requirements: like the facts question of step 4, it is asked what
    the symbols mean, not what the system should do.

    The prompt says what does not make two outcomes impossible (step 50). On
    a real project the wrong answers had two shapes (research_log.md, T46).
    The model said how a system works: "a request that is refused generates
    an audit event, so the audit log cannot be empty". Or it took statements
    about two things for statements about one: "a run cannot have zero tool
    calls if the maximum is 40".

    Adds to formal:
        "outcome_pairs"  every pair asked about, with the count of its answers
        "background"     one assumed fact for each pair that most answers call
                         impossible:
                             {"id": "F4", "between": ["C1", "C6"], "support": "7/8",
                              "formula": "(not (and payment_taken payment_refused))", ...}

    keep_answers  also store every answer with its reason (for the experiments)
    only          ask only about pairs with one of these rules, and keep the
                  pairs that the model has already (formalize with `base`)
    first         the rules whose pairs are asked about first. At most
                  MAX_PAIRS pairs are asked about; when a change is checked,
                  its rules come last in the document, and in a long one
                  they would not be reached
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    pairs = _first([pair for pair in _open_pairs(vocab, formal)
                    if only is None or pair[0]["id"] in only or pair[1]["id"] in only], first)
    if len(pairs) > MAX_PAIRS:
        formal["outcome_pairs_skipped"] = len(pairs) - MAX_PAIRS
        pairs = pairs[:MAX_PAIRS]
    system = _about(OUTCOMES_SYSTEM, formal)

    def ask(pair: tuple) -> list[dict]:
        _, _, first_demands, second_demands = pair
        prompt = (f"Statement A:\n{describe(first_demands, descriptions)}\n\n"
                  f"Statement B:\n{describe(second_demands, descriptions)}")
        return llm.ask(system, prompt, OUTCOMES_SCHEMA, ANSWERS, temperature)

    with ThreadPoolExecutor(max_workers=16) as pool:  # LLM calls only
        replies = list(pool.map(ask, pairs))

    formal["outcome_pairs"] = [] if only is None else list(formal.get("outcome_pairs", []))
    for (first, second, _, _), answers in zip(pairs, replies):
        counts = Counter({choice: 0 for choice in OUTCOMES_SCHEMA["properties"]["answer"]["enum"]})
        counts.update(reply["answer"] for reply in answers)
        record = {"rules": [first["id"], second["id"]], "answers": dict(counts)}
        if keep_answers:
            record["replies"] = answers
        formal["outcome_pairs"].append(record)
        if counts["impossible"] > MAJORITY * len(answers):
            sentence = next((reply["fact"].strip() for reply in answers
                             if reply["answer"] == "impossible" and reply["fact"].strip()), "")
            formal["background"].append({
                "id": f"F{len(formal['background']) + 1}",
                "text": (f"What {first['id']} and {second['id']} demand cannot both be the case"
                         + (f": {sentence}" if sentence else ".")),
                "formula": f"(not (and {first['consequent']} {second['consequent']}))",
                "support": f"{counts['impossible']}/{len(answers)}",
                "between": [first["id"], second["id"]],
            })


def conditions(llm: LLM, formal: dict, vocab: Vocabulary, temperature: float,
               keep_answers: bool = False, only: set | None = None, first: set | None = None) -> None:
    """Step 6, check 5: for two rules that clash, can their conditions both hold?

    Runs last, on all the facts that the other checks left or added. The
    model sees the two conditions as facts with their descriptions, without
    what the two conditions say alike, and not the requirements. The question
    is that of check 4, two statements about one snapshot, with a prompt of
    its own (CONDITIONS_SYSTEM) and the same form of answer.

    Adds to formal:
        "condition_pairs"  every pair asked about, with the count of its answers
        "background"       one assumed fact for each pair that most answers call
                           impossible:
                               {"id": "F9", "between": ["R5", "R7"], "about": "conditions",
                                "support": "7/8", "formula": "(not (and <condition of R5> <condition of R7>))", ...}

    keep_answers  also store every answer with its reason (for the experiments)
    only          ask only about pairs with one of these rules, and keep the
                  pairs that the model has already (formalize with `base`)
    first         the rules whose pairs are asked about first (see outcomes)
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    pairs = _first([pair for pair in _clashing_pairs(vocab, formal)
                    if only is None or pair[0]["id"] in only or pair[1]["id"] in only], first)
    if len(pairs) > MAX_PAIRS:
        formal["condition_pairs_skipped"] = len(pairs) - MAX_PAIRS
        pairs = pairs[:MAX_PAIRS]
    system = _about(CONDITIONS_SYSTEM, formal)

    def ask(pair: tuple) -> list[dict]:
        _, _, first_only, second_only = pair
        prompt = (f"Statement A:\n{describe(first_only, descriptions)}\n\n"
                  f"Statement B:\n{describe(second_only, descriptions)}")
        return llm.ask(system, prompt, OUTCOMES_SCHEMA, ANSWERS, temperature)

    with ThreadPoolExecutor(max_workers=16) as pool:  # LLM calls only
        replies = list(pool.map(ask, pairs))

    formal["condition_pairs"] = [] if only is None else list(formal.get("condition_pairs", []))
    for (first, second, _, _), answers in zip(pairs, replies):
        counts = Counter({choice: 0 for choice in OUTCOMES_SCHEMA["properties"]["answer"]["enum"]})
        counts.update(reply["answer"] for reply in answers)
        record = {"rules": [first["id"], second["id"]], "answers": dict(counts)}
        if keep_answers:
            record["replies"] = answers
        formal["condition_pairs"].append(record)
        if counts["impossible"] > MAJORITY * len(answers):
            sentence = next((reply["fact"].strip() for reply in answers
                             if reply["answer"] == "impossible" and reply["fact"].strip()), "")
            formal["background"].append({
                "id": f"F{len(formal['background']) + 1}",
                "text": (f"The conditions of {first['id']} and {second['id']} cannot both hold"
                         + (f": {sentence}" if sentence else ".")),
                "formula": f"(not (and {first['antecedent']} {second['antecedent']}))",
                "support": f"{counts['impossible']}/{len(answers)}",
                "between": [first["id"], second["id"]],
                "about": "conditions",
            })


APPLIES_SYSTEM = """\
You get ONE requirement of a software system, and a statement B about ONE \
snapshot of that system. B is not given: it may be true or false, and you \
have to say which. B is written as a fact marked TRUE or FALSE; B marked \
FALSE says that the fact is not the case.

Only some situations count: those in which the condition of the requirement \
is the case (what comes after WHEN, WHILE or IF; a requirement without such \
a part has no condition, and every situation counts), and in which the \
system has done everything the requirement demands, with its words read \
exactly as written. A situation in which the condition is not the case does \
not count, although the requirement is not broken in it. Must B be true in \
every situation that counts? Answer:
- yes: by the meaning of the requirement's words alone, B is true in every \
situation that counts (if it demands that a letter was answered, a letter \
was received; if it demands that every window is shut, the kitchen window is \
shut).
- no: there can be a situation that counts in which B is false. Look for one \
before you answer. This is also the answer when B would usually come before what \
the requirement demands, or when a system would need B to bring it about. \
Do not assume how the system works, or that anything succeeds (if it demands \
that the gate is open, nobody need have opened it today; if it demands that \
the bell is rung once, the bell need not have been heard).
- unclear: the words can reasonably be read both ways.

First give the reason in one or two sentences, then the answer. If the answer \
is yes, also write what connects the two as one plain sentence ("A letter \
that was answered was received."); otherwise leave "fact" empty.

If the answer is yes, say in "by" what makes B true. "condition": B is true \
as soon as the condition of the requirement is the case, whatever the system \
then does (the condition is that a letter is sent back, and B says that a \
letter arrived). "demand": it takes what the requirement demands (it demands \
that a letter was answered, and B says that a letter was received). If the \
answer is not yes, write "none"."""

APPLIES_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "answer": {"enum": ["yes", "no", "unclear"]},
        "fact": {"type": "string"},
        "by": {"enum": ["condition", "demand", "none"]},
    },
    "required": ["reason", "answer", "fact", "by"],
    "additionalProperties": False,
}


def applies(llm: LLM, formal: dict, vocab: Vocabulary, temperature: float,
            keep_answers: bool = False, only: set | None = None, first: set | None = None) -> None:
    """Step 6, check 6: does what one rule demands make another rule apply?

    Runs last, on all the facts that the other checks left or added. The
    model gets the words of rule a and one part of the condition of rule b,
    as a statement B, and says whether B must be true wherever a applies and
    is obeyed. Six things in this were learned on saved runs
    (research_log.md, T39, T42, T43, T47, T48):

    - the words of the requirement are shown, not the symbols of what it
      demands. The description of a symbol can say less than the requirement
      ("an approval was granted", for a rule that an earlier request for
      approval in the run was approved; a count of calls, for "succeeds once");
    - the prompt is its own (APPLIES_SYSTEM) and says that what a system
      would need is not what the words say. Asked with the prompt of check 4
      or of check 2, the model also answered "impossible" for "to give the
      return label it must have found the parcel";
    - B is shown alone. Shown with the condition of a as a situation, the
      model judged those facts too, and called situations impossible for
      reasons that had nothing to do with B;
    - B is a statement to judge, and the prompt says that it is not given.
      Shown as "Fact B", marked TRUE, the model took it as given where it is
      one of the cases in which a applies ("a call of X or Y is made", and B
      about Y), found that a then applies, and said yes;
    - the prompt says which situations count: those in which the condition of
      the requirement is the case and the system has done what it demands.
      Told to "take any situation in which the requirement applies", some
      answers took any run of a system that has the rule, also one in which
      its condition is not met, and said no to a right step. Asked twice on
      the same runs, such a step had 8 of 8 answers once and 3 of 8 the
      second time (T47, T48);
    - a "yes" also says what makes B true: what a demands, or the condition
      of a alone ("WHEN a call returns a refusal ...", and B "a call is
      made"). In the second case the fact is "condition of a => B". With the
      demand of a in it, a situation that b forbids by itself ("WHEN a call
      is made THEN the run is not an emergency run", in an emergency run in
      which a call returns a refusal) was reported as a conflict of a and b.

    Adds to formal:
        "apply_pairs"  every question asked, with the count of its answers,
                       and for a "yes" what the answers say makes B true:
                           {"rules": ["R1", "R4"], "part": {"ask_manager_called": true},
                            "answers": {"yes": 8, "no": 0, "unclear": 0},
                            "by": {"condition": 0, "demand": 8}}
        "background"   one assumed fact for each question that most answers
                       say yes to:
                           {"id": "F9", "between": ["R1", "R4"], "about": "applies", "support": "8/8",
                            "formula": "(=> (and <condition of R1> <demand of R1>) ask_manager_called)", ...}

    With such a fact Z3 knows that where a is obeyed, that part of b's
    condition holds. checks.py then finds a conflict that needs the step from
    a to b, and an example whose own demand makes a rule apply describes the
    situation of their conflict (checks._mark_examples).

    keep_answers, only: as in `outcomes`. At most MAX_PAIRS questions.
    first  the rules of a change, when one is checked: only the pairs with
           one of them are asked about. The conflict that an answer adds is
           between the two rules of its pair, and a conflict among the rules
           that existed before is not shown as the change's.
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    pairs = [pair for pair in _bridge_pairs(vocab, formal)
             if (only is None or pair[0]["id"] in only or pair[1]["id"] in only)
             and (not first or pair[0]["id"] in first or pair[1]["id"] in first)]
    if len(pairs) > MAX_PAIRS:
        formal["apply_pairs_skipped"] = len(pairs) - MAX_PAIRS
        pairs = pairs[:MAX_PAIRS]
    system = _about(APPLIES_SYSTEM, formal)

    def ask(pair: tuple) -> list[dict]:
        a, _, part = pair
        prompt = f"Requirement:\n{a['text']}\n\nStatement B:\n{describe(part, descriptions)}"
        return llm.ask(system, prompt, APPLIES_SCHEMA, ANSWERS, temperature)

    with ThreadPoolExecutor(max_workers=16) as pool:  # LLM calls only
        replies = list(pool.map(ask, pairs))

    formal["apply_pairs"] = [] if only is None else list(formal.get("apply_pairs", []))
    for (a, b, part), answers in zip(pairs, replies):
        counts = Counter({choice: 0 for choice in APPLIES_SCHEMA["properties"]["answer"]["enum"]})
        counts.update(reply["answer"] for reply in answers)
        record = {"rules": [a["id"], b["id"]], "part": part, "answers": dict(counts)}
        if keep_answers:
            record["replies"] = answers
        formal["apply_pairs"].append(record)
        if counts["yes"] > MAJORITY * len(answers):
            (name, value), = part.items()
            sentence = next((reply["fact"].strip() for reply in answers
                             if reply["answer"] == "yes" and reply["fact"].strip()), "")
            # Does the condition of a alone give B, whatever a demands? Then the
            # fact says so. With "(and condition demand) => B" in its place, a
            # situation that b forbids by itself would look like a clash of a
            # and b: the solver needs the demand of a to get B (checks._search).
            by = Counter(reply.get("by") for reply in answers if reply["answer"] == "yes")
            given = by["condition"] > by["demand"]
            record["by"] = {"condition": by["condition"], "demand": by["demand"]}
            when = a["antecedent"] if given else f"(and {a['antecedent']} {a['consequent']})"
            formal["background"].append({
                "id": f"F{len(formal['background']) + 1}",
                "text": (f"Where {a['id']} applies{'' if given else ' and is obeyed'}, "
                         f"a part of the condition of {b['id']} holds" + (f": {sentence}" if sentence else ".")),
                "formula": f"(=> {when} {name if value else f'(not {name})'})",
                "support": f"{counts['yes']}/{len(answers)}",
                "between": [a["id"], b["id"]],
                "about": "applies",
            })


def _bridge_pairs(vocab: Vocabulary, formal: dict) -> list[tuple]:
    """Check 6: the questions to ask, as (rule a, rule b, one part of the condition of b).

    A pair (a, b) is asked about when the answer can add a finding or lift a
    doubt, and only then:

    - the condition of b is one definite state of its symbols, so that a part
      of it can be shown as a fact;
    - if b applied where a applies, the two could not both be obeyed. That
      is: in some situation in which a applies, alone or with one more rule
      c, the rules can all be obeyed (with the assumed facts); the condition
      of b can hold there as well; and then a and b, these two alone, clash.
      So if what a demands makes b apply, a and b are in conflict there;
    - a part of the condition of b is a yes/no fact that a neither gives nor
      excludes: it is not a symbol of what a demands, and Z3 with the facts
      cannot tell. One question is asked for each such part.

    A rejected rule takes no part, and an ambiguous one is taken with its
    first reading, as in checks.py.
    """
    facts = [vocab.parse(fact["formula"]) for fact in formal["background"]
             if fact.get("check", {}).get("verdict") != "rejected"]
    rules = [(data, vocab.rule(data)) for data in formal["rules"] if data.get("status") != "rejected"]
    # Solvers that are asked many times, with the conditions as assumptions.
    obeyed, allowed = vocab.solver([rule.formula for _, rule in rules] + facts), vocab.solver(facts)

    def possible(solver: z3.Solver, *conditions) -> bool:
        return solver.check(*conditions) == z3.sat

    pairs = []
    for first, a in rules:
        # The situations in which a applies and the rules can all be obeyed:
        # a alone (c is a itself), or a with one more rule.
        situations = [[a.antecedent, c.antecedent] for _, c in rules
                      if possible(obeyed, a.antecedent, c.antecedent)]
        case, demanded = [a.antecedent, a.consequent], vocab.symbols_in(a.consequent)
        for second, b in rules:
            condition = _as_facts(vocab, b.antecedent) if b is not a and situations else None
            if not condition or not possible(allowed, *case, b.antecedent):
                continue  # no definite condition, or b never applies where a is obeyed
            parts = {name: value for name, value in condition.items()
                     if isinstance(value, bool) and name not in demanded
                     and possible(allowed, *case, z3.Not(vocab.assignment({name: value})[0]))}
            if not parts:
                continue  # nothing left to ask: Z3 knows already whether b applies
            both = vocab.solver([a.formula, b.formula] + facts)
            if any(possible(allowed, *situation, b.antecedent) and not possible(both, *situation, b.antecedent)
                   for situation in situations):
                pairs += [(first, second, {name: value}) for name, value in parts.items()]
    return pairs


def _clashing_pairs(vocab: Vocabulary, formal: dict) -> list[tuple]:
    """Check 5: the pairs of rules to ask about, as (rule, rule, what only the condition of one
    says, what only the condition of the other says).

    A pair is asked about when it would be reported as a conflict that is
    not doubtful, and its two conditions are different enough to exclude each
    other:

    - both rules can apply in one situation that the assumed facts allow, and
      there they cannot both be obeyed (with the facts);
    - they do not react to two different events (that conflict is marked
      doubtful anyway, see checks._search), unless the spec is about whole
      runs;
    - each condition is one definite state of its symbols, so that it can be
      shown as a list of facts (not "x or y", not "at least 5");
    - each condition says something that the other does not. Two rules with
      the same condition, or a rule and a special case of it ("... AND the
      folder already exists"), can apply together by their words.

    A rejected rule takes no part, and an ambiguous one is taken with its
    first reading, as in checks.py.
    """
    facts = [vocab.parse(fact["formula"]) for fact in formal["background"]
             if fact.get("check", {}).get("verdict") != "rejected"]
    usable = []  # (rule dict, compiled rule, the events it reacts to, its condition as facts)
    for data in formal["rules"]:
        if data.get("status") != "rejected":
            rule = vocab.rule(data)
            condition = _as_facts(vocab, rule.antecedent)
            if condition:
                usable.append((data, rule, vocab.events_of(data), condition))
    pairs = []
    whole_run = formal.get("situation") == "run"
    for index, (first, a, a_events, a_condition) in enumerate(usable):
        for second, b, b_events, b_condition in usable[index + 1:]:
            if not whole_run and a_events and b_events and not a_events & b_events:
                continue  # two different events
            a_only = {name: value for name, value in a_condition.items() if name not in b_condition}
            b_only = {name: value for name, value in b_condition.items() if name not in a_condition}
            if not a_only or not b_only:
                continue  # the same condition, or one is a special case of the other
            if vocab.impossible([a.antecedent, b.antecedent] + facts):
                continue  # they never apply together, as Z3 or the facts already say
            if not vocab.impossible([a.antecedent, b.antecedent, a.consequent, b.consequent] + facts):
                continue  # both can be obeyed there: nothing to doubt
            pairs.append((first, second, a_only, b_only))
    return pairs


def _open_pairs(vocab: Vocabulary, formal: dict) -> list[tuple]:
    """Check 4: the pairs of rules to ask about, as (rule, rule, what one demands, what the other demands).

    A pair is asked about when a missing fact could hide a conflict between
    the two, and only then:

    - both rules can apply in one situation that the assumed facts allow;
    - they do not react to two different events (that conflict would be
      marked doubtful anyway, see checks._search), unless the spec is about
      whole runs;
    - what they demand shares no symbol (otherwise Z3 already relates the
      two), and no assumed fact already says that the two exclude each other;
    - what each demands is one definite state of its symbols, so that it can
      be shown as a list of facts (not "x or y", not "at least 5").

    A rejected rule takes no part, and an ambiguous one is taken with its
    first reading, as in checks.py.
    """
    facts = [vocab.parse(fact["formula"]) for fact in formal["background"]
             if fact.get("check", {}).get("verdict") != "rejected"]
    usable = []  # (rule dict, compiled rule, the events it reacts to, what it demands as facts)
    for data in formal["rules"]:
        if data.get("status") != "rejected":
            rule = vocab.rule(data)
            demands = _as_facts(vocab, rule.consequent)
            if demands:
                usable.append((data, rule, vocab.events_of(data), demands))
    pairs = []
    whole_run = formal.get("situation") == "run"
    for index, (first, a, a_events, a_demands) in enumerate(usable):
        for second, b, b_events, b_demands in usable[index + 1:]:
            if not whole_run and a_events and b_events and not a_events & b_events:
                continue  # two different events
            if a_demands.keys() & b_demands.keys():
                continue  # a symbol in common: Z3 sees how the two relate
            if vocab.impossible([a.antecedent, b.antecedent] + facts):
                continue  # they never apply together
            if vocab.impossible([a.consequent, b.consequent] + facts):
                continue  # the facts already say that the two exclude each other
            pairs.append((first, second, a_demands, b_demands))
    return pairs


def _as_facts(vocab: Vocabulary, formula: z3.BoolRef) -> dict | None:
    """A formula as one value for each of its symbols, or None if it does not fix them all.

    (and (not door_unlocked) attempt_logged)  ->  {"door_unlocked": False, "attempt_logged": True}
    (or a b), (>= count 5), true              ->  None
    """
    names = vocab.symbols_in(formula)
    model = vocab.model([formula])
    if not names or model is None:
        return None
    values = vocab.witness(model, names)
    fixed = vocab.implies([formula], z3.And(*vocab.assignment(values)))
    return values if fixed else None
