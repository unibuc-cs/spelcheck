"""Tests for the questions of formalize step 6 (probe.py), the marks on doubtful
conflicts, and the findings that depend on the reading of an ambiguous rule.

No LLM, no GPU: the LLM is replaced by a stand-in that answers by a fixed
policy, so these tests check what the code does with the answers.
"""

from speccheck.checks import analyze, settled
from speccheck.explain import evidence, render
from speccheck.logic import Vocabulary
from speccheck.probe import FACT_SYSTEM, LINK_SYSTEM, QUESTION_SYSTEM, READINGS_SYSTEM, question


def bools(*names, events=()):
    """Symbol entries for yes/no symbols; those named in `events` are events."""
    return [{"name": name, "sort": "Bool", "values": [], "description": name, "event": name in events}
            for name in names]


def ambiguities(findings):
    """Only the ambiguity findings (a one-rule spec also has gaps)."""
    return [f for f in findings if f["type"] == "ambiguity"]


def conflicts(findings):
    return [f for f in findings if f["type"] == "conflict"]


class FakeLLM:
    """Stands in for llm.LLM.

    readings      the other readings it proposes for every rule
    prefer        the reading text it says the words support, or None for "either"
    link_answers  its answers to link questions, in order
    fact_answers  fact sentence -> its answer about that fact ("agrees" if not listed)
    """

    def __init__(self, readings=(), prefer=None, link_answers=(), fact_answers=None):
        self.readings = list(readings)
        self.prefer = prefer
        self.link_answers = list(link_answers)
        self.fact_answers = fact_answers or {}

    def ask(self, system, user, schema, samples=1, temperature=0.0):
        if system == READINGS_SYSTEM:
            return [{"readings": self.readings}]
        if system == LINK_SYSTEM:
            given, self.link_answers = self.link_answers[:samples], self.link_answers[samples:]
            return [{"reason": "", "answer": answer} for answer in given]
        if system == FACT_SYSTEM:
            sentence = user.split("Statement:\n")[1]
            return [{"reason": "", "answer": self.fact_answers.get(sentence, "agrees")}] * samples
        assert system == QUESTION_SYSTEM
        # The readings are shown as A and B, in both orders: answer with the
        # label of the preferred one, wherever it stands.
        if self.prefer is None:
            answer = "either"
        else:
            answer = "A" if f"Reading A: {self.prefer} [" in user else "B"
        return [{"reason": "", "answer": answer}] * samples


# ------------------------------------------------------------ doubtful conflicts


def test_a_conflict_the_facts_call_impossible_is_marked_doubtful():
    """Two symbols for complementary conditions can both be true for the solver.

    "At least 24 hours" and "less than 24 hours" became two yes/no symbols,
    so the solver finds a situation where both rules apply. The fact that
    they exclude each other does not remove the conflict (facts never remove
    findings), but marks it as doubtful.
    """
    formal = {
        "symbols": bools("at_least_24h", "less_than_24h", "fee"),
        "background": [{"id": "F1", "text": "", "formula": "(not (and at_least_24h less_than_24h))"}],
        "rules": [
            {"id": "B3", "antecedent": "at_least_24h", "consequent": "(not fee)"},
            {"id": "B4", "antecedent": "less_than_24h", "consequent": "fee"},
        ],
    }
    assert conflicts(analyze(formal)) == [
        {"type": "conflict", "rules": ["B3", "B4"],
         "when": {"at_least_24h": True, "less_than_24h": True}, "doubted_by": ["F1"]},
    ]


def test_a_conflict_that_needs_two_events_at_once_is_marked_doubtful():
    """A visitor signs up while a subscriber changes an address: two events at once.

    One snapshot allows it, so the solver proves the clash; the conflict is
    kept but marked, because requirements are written for one event at a time.
    """
    formal = {
        "symbols": bools("signup", "address_changed", "email_sent", events=("signup", "address_changed")),
        "rules": [
            {"id": "N1", "antecedent": "signup", "consequent": "(not email_sent)"},
            {"id": "N5", "antecedent": "address_changed", "consequent": "email_sent"},
        ],
    }
    (conflict,) = conflicts(analyze(formal))
    assert conflict["simultaneous_events"] == ["address_changed", "signup"]

    # The same clash with one event and one state is not marked.
    formal["symbols"] = bools("signup", "address_changed", "email_sent", events=("signup",))
    (conflict,) = conflicts(analyze(formal))
    assert "simultaneous_events" not in conflict


def test_a_trigger_counts_even_when_the_translation_leaves_it_out():
    """"A connection attempt fails for the third time", translated as the count alone.

    As a count, the rule looks like a state, and its clash with another event
    seems to need one event only. The read step named the event it reacts to
    (its trigger), so the conflict is marked: it needs two events at once.
    """
    formal = {
        "symbols": [{"name": "failed_connections", "sort": "Int", "values": [], "description": ""},
                    *bools("connection_failed", "unblock_pressed", "blocked",
                           events=("connection_failed", "unblock_pressed"))],
        "rules": [
            {"id": "R1", "antecedent": "(= failed_connections 3)", "consequent": "blocked",
             "trigger": "connection_failed"},
            {"id": "R2", "antecedent": "unblock_pressed", "consequent": "(not blocked)",
             "trigger": "unblock_pressed"},
        ],
    }
    (conflict,) = conflicts(analyze(formal))
    assert conflict["simultaneous_events"] == ["connection_failed", "unblock_pressed"]
    del formal["rules"][0]["trigger"]  # without it, a count and one event
    (conflict,) = conflicts(analyze(formal))
    assert "simultaneous_events" not in conflict


def test_one_rule_reacting_to_an_event_is_not_two_events():
    """D2 reacts to the owner's confirmation; D4 always applies (soft deletion).

    "deleted" is marked as an event, and it is in D4's antecedent, but D4
    does not react to it: the conflict needs one event, and stays undoubted.
    """
    formal = {
        "symbols": bools("confirmed", "deleted", "removed", "retained", events=("confirmed", "deleted")),
        "background": [{"id": "F1", "text": "", "formula": "(=> removed (not retained))"}],
        "rules": [
            {"id": "D2", "antecedent": "confirmed", "consequent": "removed", "trigger": "confirmed"},
            {"id": "D4", "antecedent": "deleted", "consequent": "retained", "trigger": ""},
        ],
    }
    (conflict,) = conflicts(analyze(formal))
    assert conflict["rules"] == ["D2", "D4"] and "simultaneous_events" not in conflict


# ------------------------------------------------------------------- readings


def formal_with_one_rule(status="accepted", alternative=None):
    """A fine is due on a loan of exactly 14 days (one possible reading)."""
    rule = {"id": "L5", "text": "WHEN a member has had a book on loan for 14 days, add a fine.",
            "status": status, "reading": "exactly 14 days",
            "antecedent": "(= loan_days 14)", "consequent": "fine_added"}
    if alternative:
        rule["alternative"] = alternative
    return {
        "symbols": [{"name": "loan_days", "sort": "Int", "values": [], "description": "days on loan"},
                    *bools("fine_added")],
        "background": [],
        "rules": [rule],
    }


# Other readings the stand-in proposes: one that differs, one that only
# rewrites the translation (and must be dropped), one that is malformed.
AT_LEAST = {"reading": "14 days or more", "antecedent": "(>= loan_days 14)", "consequent": "fine_added"}
READINGS = [
    AT_LEAST,
    {"reading": "the same", "antecedent": "(= 14 loan_days)", "consequent": "fine_added"},
    {"reading": "broken", "antecedent": "(>= loan_days", "consequent": "fine_added"},
]


def test_a_rule_is_ambiguous_when_the_words_do_not_decide():
    formal = formal_with_one_rule()
    question(FakeLLM(READINGS, prefer=None), formal, Vocabulary(formal["symbols"]), "", temperature=0.7)

    (probe,) = formal["rules"][0]["probes"]  # the rewrite and the malformed one are dropped
    assert probe["answers"] == {"translation": 0, "other": 0, "either": 8}
    # The only situation where the readings differ: 15 days or more, no fine.
    (situation,) = probe["situations"]
    assert situation["when"]["fine_added"] is False and situation["when"]["loan_days"] > 14

    (finding,) = ambiguities(analyze(formal))
    assert finding["found_by"] == "questions"
    # The experiments can switch the questions off.
    assert ambiguities(analyze(formal, questions=False)) == []


def test_answers_for_the_translation_confirm_it():
    formal = formal_with_one_rule()
    question(FakeLLM(READINGS, prefer="exactly 14 days"), formal, Vocabulary(formal["symbols"]),
             "", temperature=0.7)
    assert formal["rules"][0]["probes"][0]["answers"] == {"translation": 8, "other": 0, "either": 0}
    assert ambiguities(analyze(formal)) == []
    assert settled(formal["rules"][0])["antecedent"] == "(= loan_days 14)"


def test_answers_for_the_other_reading_make_the_rule_ambiguous():
    """The 8 samples agreed on "exactly 14"; asked, the words support "14 or more".

    The translation is not replaced silently: the author is asked.
    """
    formal = formal_with_one_rule()
    question(FakeLLM(READINGS, prefer="14 days or more"), formal, Vocabulary(formal["symbols"]),
             "", temperature=0.7)
    assert formal["rules"][0]["probes"][0]["answers"] == {"translation": 0, "other": 8, "either": 0}
    (finding,) = ambiguities(analyze(formal))
    assert finding["found_by"] == "questions"


def test_the_share_a_translation_needs_can_be_raised():
    """6 of 8 answers for the translation: enough at the default, not at 7 of 8."""
    rule = {**formal_with_one_rule()["rules"][0],
            "probes": [{**AT_LEAST, "situations": [], "answers": {"translation": 6, "other": 0, "either": 2}}]}
    assert settled(rule)["status"] == "accepted"
    assert settled(rule, settle=0.75)["status"] == "ambiguous"


def test_a_split_in_the_samples_is_settled_by_the_words():
    """The samples split between two readings; the question decides between them."""
    formal = formal_with_one_rule(status="ambiguous", alternative=AT_LEAST)
    # Nothing is proposed for a rule whose samples split: its second group is the other reading.
    question(FakeLLM(readings=[], prefer="exactly 14 days"), formal, Vocabulary(formal["symbols"]),
             "", temperature=0.7)
    assert [p["reading"] for p in formal["rules"][0]["probes"]] == ["14 days or more"]
    assert ambiguities(analyze(formal)) == []                       # the words decide: noise
    assert len(ambiguities(analyze(formal, questions=False))) == 1  # as the samples left it


# ------------------------------------------- findings that depend on a reading


def test_a_conflict_that_the_other_reading_adds_or_removes_is_named():
    """L5 is ambiguous: a fine at exactly 14 days, or from 14 days on.

    L6 says that a loan of 20 days has no fine. With "exactly 14" the two
    never apply together; with "14 or more" they clash at 20 days. Whichever
    reading the checks use, the report must say that the other one differs.
    """
    no_fine_at_20 = {"id": "L6", "text": "", "status": "accepted",
                     "antecedent": "(= loan_days 20)", "consequent": "(not fine_added)"}

    # The checks use "exactly 14": no conflict, but the other reading has one.
    formal = formal_with_one_rule(status="ambiguous", alternative=AT_LEAST)
    formal["rules"].append(no_fine_at_20)
    findings = analyze(formal)
    assert conflicts(findings) == []
    (ambiguity,) = ambiguities(findings)
    assert ambiguity["other_reading"]["adds"] == [["L5", "L6"]]
    assert ambiguity["other_reading"]["removes"] == []
    assert "a conflict between L5, L6 appears" in evidence(ambiguity, formal)

    # The checks use "14 or more": the conflict is found, and marked.
    exactly = {"reading": "exactly 14 days", "antecedent": "(= loan_days 14)", "consequent": "fine_added"}
    formal = formal_with_one_rule(status="ambiguous", alternative=exactly)
    formal["rules"][0].update(AT_LEAST)
    formal["rules"].append(no_fine_at_20)
    findings = analyze(formal)
    (conflict,) = conflicts(findings)
    assert conflict["depends_on_reading"] == ["L5"]
    assert ambiguities(findings)[0]["other_reading"]["removes"] == [["L5", "L6"]]
    assert "Conflict (depends on the reading of L5)" in render(findings, [formal], "loans")

    # The experiments can switch this off: the findings are then as before.
    plain = analyze(formal, readings=False)
    assert "depends_on_reading" not in conflicts(plain)[0] and "other_reading" not in ambiguities(plain)[0]


def test_a_gap_that_the_other_reading_covers_is_named():
    """ "WHEN motion is detected at night, switch the lamp on": must it be night?

    Reading 1 needs motion and night, so there are two gaps: "it is not
    night" and "no motion". With reading 2 (motion is enough) a rule applies
    when it is not night, so only that gap depends on the reading.
    """
    formal = {
        "symbols": bools("motion", "night", "lamp_on", events=("motion",)),
        "background": [],
        "rules": [{"id": "A1", "text": "", "status": "ambiguous", "reading": "motion at night",
                   "antecedent": "(and motion night)", "consequent": "lamp_on",
                   "alternative": {"reading": "any motion", "antecedent": "motion",
                                   "consequent": "lamp_on"}}],
    }
    findings = analyze(formal)
    gaps = {tuple(f["when"].items()): f.get("depends_on_reading") for f in findings if f["type"] == "gap"}
    assert gaps == {(("night", False),): ["A1"], (("motion", False),): None}
    (ambiguity,) = ambiguities(findings)
    assert ambiguity["other_reading"] == {"removes": [], "adds": [], "covers_gaps": 1}
    assert "Gap (depends on the reading of A1)" in render(findings, [formal], "lamp")


def test_ambiguities_that_change_another_finding_come_first():
    """M1 is ambiguous too, but neither of its readings touches any other rule."""
    formal = formal_with_one_rule(status="ambiguous", alternative=AT_LEAST)
    formal["symbols"] += bools("third_visit", "badge", "email")
    formal["rules"] = [
        {"id": "M1", "text": "", "status": "ambiguous", "reading": "a badge",
         "antecedent": "third_visit", "consequent": "badge",
         "alternative": {"reading": "a badge and an email", "antecedent": "third_visit",
                         "consequent": "(and badge email)"}},
        *formal["rules"],
        {"id": "L6", "text": "", "status": "accepted",
         "antecedent": "(= loan_days 20)", "consequent": "(not fine_added)"},
    ]
    first, second = ambiguities(analyze(formal))
    assert (first["rule"], second["rule"]) == ("L5", "M1")
    assert second["other_reading"] == {"removes": [], "adds": [], "covers_gaps": 0}
    assert "changes no conflict and no gap" in evidence(second, formal)


# ---------------------------------------------------------------------- links


def formal_with_a_link():
    """D2 demands `removed`, a symbol no other rule uses; a link says what it means."""
    return {
        "symbols": bools("confirmed", "removed", "retained"),
        "background": [{"id": "F1", "text": "", "formula": "(=> (and confirmed removed) (not retained))",
                        "restates": "D2", "antecedent": "confirmed", "consequent": "(not retained)"}],
        "rules": [
            {"id": "D2", "text": "WHEN deletion is confirmed, remove the record.", "status": "rejected",
             "antecedent": "confirmed", "consequent": "removed"},
            {"id": "D4", "text": "Retain all records.", "status": "rejected",
             "antecedent": "true", "consequent": "retained"},
        ],
    }


def accept_all(formal):
    """The rules are marked "rejected" above only so that no readings are probed."""
    for rule in formal["rules"]:
        rule["status"] = "accepted"


def test_a_link_the_answers_confirm_is_used():
    formal = formal_with_a_link()
    # Situation: deletion confirmed, record still retained. Can D2 be fully
    # obeyed while the record is retained? Mostly: impossible.
    question(FakeLLM(link_answers=["impossible"] * 7 + ["possible"]), formal,
             Vocabulary(formal["symbols"]), "", temperature=0.7)
    check = formal["background"][0]["check"]
    assert check["when"] == {"confirmed": True, "retained": True}
    assert check["verdict"] == "confirmed"
    accept_all(formal)
    assert [c["rules"] for c in conflicts(analyze(formal))] == [["D2", "D4"]]


def formal_with_a_wrong_fact():
    """D4 retains deleted records; two voted facts say a deleted record is not retained.

    F1 is right ("a removed record is not retained"), F3 is wrong for this
    spec ("a deleted property has its record removed"): together they make D4
    impossible to obey, which hides the clash of D2 ("remove") and D4.
    """
    return {
        "symbols": bools("confirmed", "deleted", "removed", "retained"),
        "background": [
            {"id": "F1", "text": "A removed record is not retained.", "formula": "(=> removed (not retained))"},
            {"id": "F3", "text": "A deleted property has its record removed.", "formula": "(=> deleted removed)"},
        ],
        "rules": [
            {"id": "D2", "text": "WHEN deletion is confirmed, remove the record.", "status": "accepted",
             "reading": "", "antecedent": "confirmed", "consequent": "removed"},
            {"id": "D4", "text": "Soft deletion: retain the records of deleted properties.", "status": "accepted",
             "reading": "", "antecedent": "deleted", "consequent": "retained"},
        ],
    }


def test_a_fact_the_requirement_contradicts_is_left_out():
    formal = formal_with_a_wrong_fact()
    assert conflicts(analyze(formal)) == []  # the wrong fact hides the clash
    question(FakeLLM(fact_answers={"A deleted property has its record removed.": "contradicts"}),
             formal, Vocabulary(formal["symbols"]), "", temperature=0.7)
    f1, f3 = formal["background"]
    assert f1["check"]["verdict"] == "confirmed" and f3["check"]["verdict"] == "rejected"
    assert f3["check"]["against"] == "D4"
    (conflict,) = conflicts(analyze(formal))
    assert conflict["rules"] == ["D2", "D4"] and conflict["facts"] == ["F1"]


def test_facts_the_requirement_agrees_with_are_kept():
    formal = formal_with_a_wrong_fact()
    question(FakeLLM(), formal, Vocabulary(formal["symbols"]), "", temperature=0.7)
    assert [fact["check"]["verdict"] for fact in formal["background"]] == ["confirmed", "confirmed"]
    assert conflicts(analyze(formal)) == []


def test_a_link_the_answers_do_not_confirm_is_left_out():
    formal = formal_with_a_link()
    question(FakeLLM(link_answers=["impossible"] * 3 + ["possible"] * 4 + ["unclear"]), formal,
             Vocabulary(formal["symbols"]), "", temperature=0.7)
    assert formal["background"][0]["check"]["verdict"] == "rejected"
    accept_all(formal)
    assert conflicts(analyze(formal)) == []
    # Without link checks the link is used, and the conflict comes back.
    assert [c["rules"] for c in conflicts(analyze(formal, link_checks=False))] == [["D2", "D4"]]
