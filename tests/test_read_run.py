"""Tests for the read step of a spec about whole runs (formalize.READ_RUN). No LLM, no GPU."""

from speccheck.formalize import READ_AGAIN, READ_MORE, READ_RUN, READ_SYSTEM, _read, _read_again


def symbol(name: str) -> dict:
    return {"name": name, "sort": "Bool", "values": [], "description": f"about {name}", "event": True}


class FakeLLM:
    """Stands in for llm.LLM: keeps the system prompt of every call, and answers with one rule and one symbol."""

    def __init__(self):
        self.systems = []

    def ask(self, system, user, schema, samples=1, temperature=0.0, max_tokens=4096):
        self.systems.append(system)
        return [{"rules": [{"id": "R1", "text": "WHEN a call of ask_keeper is made THEN ...", "trigger": "ask_keeper_called"}],
                 "symbols": [symbol("ask_keeper_called")]}]


def test_a_spec_about_moments_is_read_as_before():
    llm = FakeLLM()
    _read(llm, "the document", 0.0)
    assert llm.systems == [READ_SYSTEM] and "whole runs" not in READ_SYSTEM


def test_a_spec_about_runs_is_told_that_a_symbol_is_a_fact_about_the_run():
    llm = FakeLLM()
    _read(llm, "the document", 0.0, whole_run=True)
    assert llm.systems == [READ_SYSTEM + READ_RUN]
    assert "a fact about the run as a whole" in READ_RUN and "is being sent" in READ_RUN


def test_the_second_read_and_the_read_on_a_saved_model_are_told_too():
    llm = FakeLLM()
    known = [symbol("join_group_succeeded")]
    _read(llm, "the document", 0.0, known, whole_run=True)
    _read_again(llm, [{"id": "R1", "text": "WHEN ..."}], known, 0.0, whole_run=True)
    _read_again(llm, [{"id": "R1", "text": "WHEN ..."}], known, 0.0)
    assert llm.systems == [READ_SYSTEM + READ_RUN + READ_MORE,
                           READ_SYSTEM + READ_RUN + READ_MORE + READ_AGAIN,
                           READ_SYSTEM + READ_MORE + READ_AGAIN]
