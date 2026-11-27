"""Tests for asking checks 4 to 6 again on saved runs (experiments.evaluate: _without_pairs, additions, load).
No LLM, no GPU.
"""

import json

from experiments.evaluate import _without_pairs, additions, load


def model() -> dict:
    """A saved formal model that has the three checks: a voted fact, a link, and one fact of each check."""
    return {
        "symbols": [],
        "rules": [],
        "background": [
            {"id": "F1", "text": "voted", "formula": "(not (and a b))", "support": "7/8"},
            {"id": "F2", "text": "a link", "formula": "(=> a c)", "restates": "R1", "support": "8/8"},
            {"id": "F3", "text": "two outcomes", "formula": "(not (and c d))", "between": ["R1", "R2"], "support": "6/8"},
            {"id": "F4", "text": "two conditions", "formula": "(not (and a e))", "between": ["R1", "R3"],
             "about": "conditions", "support": "5/8"},
            {"id": "F5", "text": "a rule applies", "formula": "(=> c e)", "between": ["R2", "R3"], "about": "applies",
             "support": "8/8"}],
        "outcome_pairs": [{"rules": ["R1", "R2"], "answers": {"possible": 2, "impossible": 6, "unclear": 0}}],
        "outcome_pairs_skipped": 3,
        "condition_pairs": [{"rules": ["R1", "R3"], "answers": {"possible": 3, "impossible": 5, "unclear": 0}}],
        "apply_pairs": [{"rules": ["R2", "R3"], "part": {"e": True}, "answers": {"yes": 8, "no": 0, "unclear": 0}}],
    }


def test_the_three_checks_are_taken_out_and_the_rest_stays():
    one = model()
    _without_pairs(one)
    assert [fact["id"] for fact in one["background"]] == ["F1", "F2"]
    assert not {"outcome_pairs", "outcome_pairs_skipped", "condition_pairs", "apply_pairs"} & set(one)


def test_answers_that_were_asked_again_stand_for_the_earlier_ones(tmp_path):
    source = tmp_path / "runs.json"
    data = {"prompts": {"outcomes": "old", "conditions": "c", "applies": "a"}, "specs": {},
            "runs": [{"spec": "one", "models": [model()]}, {"spec": "two", "error": "stopped"}]}
    source.write_text(json.dumps(data), encoding="utf-8")

    # What again_one leaves in a model: the three checks asked again. Here check 4 says "possible" now,
    # so check 5 had no pair to ask about, and check 6 gave its fact again.
    asked = data["runs"][0]["models"][0]
    _without_pairs(asked)
    asked["outcome_pairs"] = [{"rules": ["R1", "R2"], "answers": {"possible": 8, "impossible": 0, "unclear": 0}}]
    asked["condition_pairs"] = []
    asked["apply_pairs"] = [{"rules": ["R2", "R3"], "part": {"e": True}, "answers": {"yes": 7, "no": 1, "unclear": 0}}]
    asked["background"].append({"id": "F3", "text": "a rule applies", "formula": "(=> c e)", "between": ["R2", "R3"],
                                "about": "applies", "support": "7/8"})
    data["prompts"]["outcomes"] = "new"
    data["again_added"], data["again_failed"] = "2026-11-27T18:00:00", 0
    file = tmp_path / "again.json"
    file.write_text(json.dumps(additions(data, source, "again")), encoding="utf-8")

    saved = json.loads(file.read_text(encoding="utf-8"))
    assert saved["source"] == source.as_posix() and saved["prompts"] == {"outcomes": "new", "conditions": "c", "applies": "a"}
    assert saved["added"][1] == []                               # the run that stopped has no model
    loaded = load(file)
    back = loaded["runs"][0]["models"][0]
    assert [(fact["id"], fact["support"]) for fact in back["background"]] == [("F1", "7/8"), ("F2", "8/8"), ("F3", "7/8")]
    assert back["outcome_pairs"][0]["answers"]["possible"] == 8 and back["condition_pairs"] == []
    assert "outcome_pairs_skipped" not in back                   # the earlier asking left 3 out, this one none
    assert loaded["prompts"]["outcomes"] == "new" and loaded["again_added"] == "2026-11-27T18:00:00"
    # The source is as it was.
    assert len(load(source)["runs"][0]["models"][0]["background"]) == 5
