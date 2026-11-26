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

In formal.json the answers end up under "probes" (in a rule), "check" (in a
link or a fact), "outcome_pairs" and "condition_pairs"; a fact of check 4 or
5 has "between", and one of check 5 also "about": "conditions".
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
even if a system would rarely do both.
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
    for link in links:
        when = _link_situation(vocab, link, facts)
        if when is not None:
            link["check"] = {"when": when}
            prompt = (f"Requirement:\n{text_of[link['restates']]}\n\n"
                      f"Situation:\n{describe(when, descriptions)}")
            questions.append(Question(LINK_SYSTEM, LINK_SCHEMA, prompt, ANSWERS,
                                      record=link["check"], translation_first=None))
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
            counts = _count(link["check"], LINK_SCHEMA, keep_answers)
            total = sum(counts.values())
            confirmed = not total or counts["impossible"] > MAJORITY * total
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


def outcomes(llm: LLM, formal: dict, vocab: Vocabulary, temperature: float,
             keep_answers: bool = False, only: set | None = None) -> None:
    """Step 6, check 4: for rules that can apply together, can both get what they demand?

    Runs after the other checks, on the links and facts they left standing.
    The model sees only the two outcomes, as facts with their descriptions,
    not the requirements: like the facts question of step 4, it is asked what
    the symbols mean, not what the system should do.

    Adds to formal:
        "outcome_pairs"  every pair asked about, with the count of its answers
        "background"     one assumed fact for each pair that most answers call
                         impossible:
                             {"id": "F4", "between": ["C1", "C6"], "support": "7/8",
                              "formula": "(not (and payment_taken payment_refused))", ...}

    keep_answers  also store every answer with its reason (for the experiments)
    only          ask only about pairs with one of these rules, and keep the
                  pairs that the model has already (formalize with `base`)
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    pairs = [pair for pair in _open_pairs(vocab, formal)
             if only is None or pair[0]["id"] in only or pair[1]["id"] in only]
    if len(pairs) > MAX_PAIRS:
        formal["outcome_pairs_skipped"] = len(pairs) - MAX_PAIRS
        pairs = pairs[:MAX_PAIRS]

    def ask(pair: tuple) -> list[dict]:
        _, _, first_demands, second_demands = pair
        prompt = (f"Statement A:\n{describe(first_demands, descriptions)}\n\n"
                  f"Statement B:\n{describe(second_demands, descriptions)}")
        return llm.ask(OUTCOMES_SYSTEM, prompt, OUTCOMES_SCHEMA, ANSWERS, temperature)

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
               keep_answers: bool = False, only: set | None = None) -> None:
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
    """
    descriptions = {s["name"]: s["description"] for s in formal["symbols"]}
    pairs = [pair for pair in _clashing_pairs(vocab, formal)
             if only is None or pair[0]["id"] in only or pair[1]["id"] in only]
    if len(pairs) > MAX_PAIRS:
        formal["condition_pairs_skipped"] = len(pairs) - MAX_PAIRS
        pairs = pairs[:MAX_PAIRS]

    def ask(pair: tuple) -> list[dict]:
        _, _, first_only, second_only = pair
        prompt = (f"Statement A:\n{describe(first_only, descriptions)}\n\n"
                  f"Statement B:\n{describe(second_only, descriptions)}")
        return llm.ask(CONDITIONS_SYSTEM, prompt, OUTCOMES_SCHEMA, ANSWERS, temperature)

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


def _clashing_pairs(vocab: Vocabulary, formal: dict) -> list[tuple]:
    """Check 5: the pairs of rules to ask about, as (rule, rule, what only the condition of one
    says, what only the condition of the other says).

    A pair is asked about when it would be reported as a conflict that is
    not doubtful, and its two conditions are different enough to exclude each
    other:

    - both rules can apply in one situation that the assumed facts allow, and
      there they cannot both be obeyed (with the facts);
    - they do not react to two different events (that conflict is marked
      doubtful anyway, see checks._search);
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
    for index, (first, a, a_events, a_condition) in enumerate(usable):
        for second, b, b_events, b_condition in usable[index + 1:]:
            if a_events and b_events and not a_events & b_events:
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
      marked doubtful anyway, see checks._search);
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
    for index, (first, a, a_events, a_demands) in enumerate(usable):
        for second, b, b_events, b_demands in usable[index + 1:]:
            if a_events and b_events and not a_events & b_events:
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
