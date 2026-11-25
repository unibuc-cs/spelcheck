"""Tests for the repair of a symbol list that the read step made with names that are not words
(formalize._usable). No LLM, no GPU.
"""

from speccheck.formalize import READ_SYSTEM, _read, _usable
from speccheck.logic import Vocabulary


def symbol(name: str, sort: str = "Bool", values: tuple = (), event: bool = False) -> dict:
    return {"name": name, "sort": sort, "values": list(values), "description": f"about {name}", "event": event}


def test_a_list_without_slips_comes_back_as_it_is():
    symbols = [symbol("job_started", event=True), symbol("job_status", "Enum", ("queued", "passed", "failed")),
               symbol("run_minutes", "Int")]
    assert _usable(symbols) == (symbols, {})


def test_a_value_that_is_not_a_word_is_made_one():
    symbols = [symbol("job_status", "Enum", ("queued", "timed out", "in-progress", ".hidden")),
               symbol("answer_status", "Enum", ("200", "201", "409"))]
    usable, renamed = _usable(symbols)
    assert usable[0]["values"] == ["queued", "timed_out", "in_progress", "hidden"]
    # A number cannot be a name: it gets the name of its symbol in front.
    assert usable[1]["values"] == ["answer_status_200", "answer_status_201", "answer_status_409"]
    assert renamed == {}
    assert symbols[0]["values"][1] == "timed out"      # the list that was given is not touched
    vocab = Vocabulary(usable)                         # and Z3 takes the repaired one
    assert vocab.parse("(and (= job_status timed_out) (= answer_status answer_status_201))") is not None


def test_one_name_for_two_things():
    symbols = [symbol("shell", "Enum", ("zsh", "bash", "bash")), symbol("zsh"),
               symbol("os", "Enum", ("linux", "bash")), symbol("zsh", "Int")]
    usable, _ = _usable(symbols)
    assert [s["name"] for s in usable] == ["shell", "zsh", "os"]             # of two symbols "zsh" the first stays
    assert usable[0]["values"] == ["shell_zsh", "bash"]                      # the value gives way to the symbol
    assert usable[2]["values"] == ["linux", "os_bash"]                       # and to the value of an earlier symbol
    Vocabulary(usable)


def test_an_enum_with_one_value_becomes_a_yes_no_symbol():
    usable, _ = _usable([symbol("skills_dir", "Enum", ("skills",)), symbol("mode", "Enum", ())])
    assert [(s["name"], s["sort"], s["values"]) for s in usable] == [("skills_dir", "Bool", []), ("mode", "Bool", [])]
    Vocabulary(usable)


def test_a_symbol_name_that_is_not_a_word_and_the_trigger_that_names_it():
    class FakeLLM:
        def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
            assert system == READ_SYSTEM
            return [{"rules": [{"id": "R1", "text": "WHEN the user runs dep release THEN ...", "trigger": "dep-release-run"},
                               {"id": "R2", "text": "WHILE a freeze is in force ...", "trigger": ""}],
                     "symbols": [symbol("dep-release-run", event=True), symbol("release_state", "Enum", ("live", "rolled back")),
                                 symbol("2nd_try")]}]

    rules, symbols = _read(FakeLLM(), "the document", 0.0)
    assert [s["name"] for s in symbols] == ["dep_release_run", "release_state", "s_2nd_try"]
    assert symbols[1]["values"] == ["live", "rolled_back"]
    assert [rule["trigger"] for rule in rules] == ["dep_release_run", ""]
    assert Vocabulary(symbols).events == {"dep_release_run"}
