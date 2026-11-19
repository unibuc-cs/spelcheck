"""speccheck: a minimal Kiro-style requirements checker.

Pipeline (see plan.md for the picture):

    spec text --formalize.py--> formal.json --checks.py--> findings --explain.py--> report.md
                  (LLM + Z3)                  (Z3 only)                 (LLM)

The text becomes logic, a solver proves conflicts and gaps, and the result is
worded in plain language. cli.py runs the three stages.

Suggested reading order of the code:
llm.py, logic.py, formalize.py, probe.py, checks.py, explain.py, cli.py.
(refine.py is an optional LLM review of the text, off by default.)
"""
