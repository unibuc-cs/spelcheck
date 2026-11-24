# Research log (the full record)

**You do not need to read this file to understand the project.** The findings are
summarized in [research.md](research.md). This file is the archive behind it: every
experiment, trial and correction in the order it happened, with all tables and the
exact prompts that were tried. It is kept for writing the paper.

Entry names: `E` = experiment with a table, `T` = small trial or probe, `L` = lesson
from a bug, `C` = correction of something we had wrong, `D` = decision.

## Common setup

- **Model:** `Qwen/Qwen3.8-27B-FP8`, served locally with vLLM 0.31.0 on 2x H100 80GB
  (`--data-parallel-size 2`). Every LLM call of the pipeline goes to this one local
  model; no other model is involved anywhere.
- **Model settings:** its "thinking" mode is off (see T2), answers are forced into a
  JSON schema, at most 4096 output tokens.
- **Pipeline defaults:** read step at temperature 0 (one call); 8 samples per rule at
  temperature 0.7; entropy thresholds 0.4 (accepted) and 1.0 (rejected); conflicts
  triggered by at most 2 rules; at most 3 gaps. Changes over time: assumed facts from
  E2; conflicts triggered by up to 3 rules from E4; links (formalize step 5) from E5.
- **Specs and the conflicts we expect** (rule numbers = position in the document):

  | Spec | Format | Expected conflicts | Source of the expectation |
  |---|---|---|---|
  | `order` | Kiro EARS | {2,3}, {1,5} | the Kiro blog reports them |
  | `auth_openspec` | OpenSpec | {1,4}, {3,5} | we seeded them when writing the spec |
  | `delete_property` | Kiro EARS | {2,4} | the Kiro blog's "remove the record" vs soft deletion. Kiro finds it with its LLM refinement stage, not the solver (see C1) |

  E1 and E2 used our own paraphrase of the `delete_property` text; from E3 on the
  file holds the blog's wording. Each experiment file stores the text it used.

- **Scoring:** a run "finds the expected conflicts" when all of them are in its list
  of conflicts. Rules are matched by position, because the model renumbers rules that
  have no label (L6).

---

## E1 — How stable are the findings? (2026-11-17)

**Question.** The LLM is the only random part. How often does the same spec give the
expected conflicts, and which setting matters?

**Setup.** 3 specs x 4 settings x 10 runs = 120 pipeline runs, 5.4 minutes on 2 GPUs.
No domain facts (the code before E2).

| Spec | Setting | Expected found | Runs with other conflicts | Gaps per run (gaps: runs) | Rule flagged ambiguous (rule: runs) |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 0 | 0: 10 | none |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 0 | 0: 10 | rule 3: 8 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 0 | 0: 10 | rule 3: 5, rule 5: 1 |
| auth_openspec | 8 samples, symbols also vary | 6/10 | 1 | 0: 3, 1: 1, 3: 6 | rule 1: 1, rule 2: 2, rule 3: 7, rule 4: 1, rule 5: 1 |
| delete_property | 1 greedy translation | 0/10 | 0 | 1: 9, 2: 1 | none |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 0 | 1: 5, 2: 5 | rule 4: 8 |
| delete_property | 8 samples, T=1.0 | 0/10 | 0 | 1: 8, 2: 2 | rule 4: 6 |
| delete_property | 8 samples, symbols also vary | 0/10 | 0 | 1: 6, 2: 4 | rules 1, 2, 3: 1 each, rule 4: 7 |
| order | 1 greedy translation | 10/10 | 0 | 1: 10 | none |
| order | 8 samples, T=0.7 (default) | 10/10 | 0 | 1: 10 | none |
| order | 8 samples, T=1.0 | 10/10 | 0 | 1: 10 | rule 3: 1 |
| order | 8 samples, symbols also vary | 10/10 | 0 | 1: 10 | none |

"Symbols also vary" = the read step runs at temperature 0.7, so each run gets a
different symbol list. In the other rows the read step is at temperature 0.

**What it shows.**

1. **The symbol-choosing (read) step is the fragile part.** With fixed symbols the
   login spec gives both conflicts in 10/10 runs. When the symbols are re-drawn on
   every run it drops to 6/10, and one run reports a conflict nobody planted.
2. **Sampling more translations per rule does not help recall.** Conflict recall is
   the same for 1 greedy translation and for 8 samples at T=0.7 or T=1.0, on all three
   specs. All samples of a rule share one symbol list, so they cannot repair it.
3. **Sampling is what makes ambiguity visible.** "Reaches 5 failed attempts" (login,
   rule 3) splits into "= 5" and ">= 5" in 8/10 runs at T=0.7, 5/10 at T=1.0, and by
   construction never with a single translation. Nobody planted this ambiguity.
4. **`delete_property` is missed in 0/40 runs.** Its rule 4 (soft deletion) is flagged
   ambiguous in 6 to 8 of 10 runs, so the pipeline senses something there but cannot
   name the conflict. Cause: see T1.
5. **Gaps follow the symbols.** Login: 0 gaps in all 30 fixed-symbol runs, 0 to 3 when
   the symbols vary.

**Raw data.** Only the table was saved: [experiments/results/E1_stability.md](experiments/results/E1_stability.md).
The 120 formalizations were not kept. From E2 on every formalization is saved.

---

## T1 — Domain facts as hard truths (2026-11-17, dropped)

**Question.** `delete_property` is missed because "remove the record" and "soft
deletion" become two unrelated symbols. If the LLM also states the domain facts that
link symbols, does the solver see the clash?

**Setup.** One extra LLM question, 8 samples at T=0.7; a fact kept if at least half of
the samples state it; kept facts added as hard constraints to every solver query. One
run per spec. The prompt saw only the symbols, not the requirements:

> You are given the symbols of a formal model, each with its meaning. List the facts
> that always hold between these symbols purely because of what they mean, whatever any
> requirement says. Typical cases: two symbols that cannot both be true (a door cannot
> be open and closed), one symbol that implies another, a quantity that cannot be
> negative. Give only facts that are certain from the meaning of the words. Do not
> guess how the system is supposed to behave. Return an empty list if there are none.

**Result.**

| Spec | Facts kept | Effect on findings |
|---|---|---|
| delete_property | none | unchanged: one gap, conflict still missed |
| order | 5 (below) | conflict {R2,R3} kept, **conflict {R1,R5} lost**, gap changed |
| auth_openspec | none | unchanged |

Facts kept for `order` (agreement of 8 samples):

| Agreement | Fact | Formula |
|---|---|---|
| 8/8 | A canceled-and-refunded order has been canceled | `(=> order_canceled_and_refunded order_canceled)` |
| 8/8 | A canceled-and-refunded order has its payments refunded | `(=> order_canceled_and_refunded payments_refunded)` |
| 7/8 | An order cannot be both fulfilled and canceled | `(not (and order_fulfilled order_canceled))` |
| 7/8 | An order cannot be both fulfilled and on backorder | `(not (and order_fulfilled order_on_backorder))` |
| 7/8 | An order cannot be both canceled and on backorder | `(not (and order_canceled order_on_backorder))` |

**Why it failed.**

- **order.** The third fact is a business rule, not a truth about the words, yet 7 of
  8 samples state it. In the situation that triggers R1/R5 (submitted, inventory
  available, canceled-and-refunded) the facts alone already forbid fulfilment. R1 then
  contradicts the facts by itself, the check took that for "a situation the spec
  forbids", and the conflict was dropped.
- **delete_property.** The read step had described the symbol for "remove the Property
  record" as *"no longer accessible as an active record (logically deleted)"*. It had
  quietly picked the meaning of "remove" that agrees with the soft-deletion rule. With
  that description no fact separates the two symbols, and none should.

**Conclusions.**

1. Agreement between samples does not make a fact true. LLM-proposed facts must never
   be able to remove a finding. This led to the design of E2.
2. A conflict can be lost before any logic runs: when the model chooses symbols it
   reads the document charitably and harmonizes two requirements that disagree.

**Raw data.** Not saved; the numbers above are from the session record.

---

## T2 — The model's "thinking" mode for the read step (2026-11-17, one probe)

**Question.** Does the read step choose better symbols if the local Qwen model is
allowed to reason before it answers ("thinking" mode, a switch of the same model)?

**Setup.** One call: read step on `delete_property`, temperature 0, thinking on,
8192 output tokens.

**Result.** 108.9 seconds, 38,648 characters of reasoning, stopped at the token limit
before producing any answer (`finish_reason = length`).

**Conclusion.** Not usable as tried; thinking is off everywhere. This is a single
probe, not evidence that thinking cannot help: a larger token budget or a cap on the
reasoning was not tried.

---

## E2 — Domain facts that can only add findings (2026-11-17)

**Question.** Same as T1, without its failure: can sampled domain facts reveal clashes
between different phrases while never hiding a finding?

**Design.**

- Facts are sampled like rules (8 answers). A fact is kept when it *follows from* the
  facts of more than half of the answers (checked by Z3, so wording does not matter).
  Facts that are true by logic alone, repeat a kept fact, or contradict better
  supported ones are dropped.
- The conflict search runs twice: with the rules alone, then with the facts. From the
  second run only conflicts that need a fact are added, each naming its facts. Gaps
  ignore the facts.
- Guaranteed by construction and by a test: the findings without facts are a subset
  of the findings with facts.
- The report lists every assumed fact and marks each conflict that depends on one.

**Solver side (no LLM), verified.** 10 tests pass. Replaying the five `order` facts of
T1, including the wrong one, now leaves the findings exactly as without facts. A
hand-written fact on a two-symbol version of the delete clash gives the conflict with
the fact named.

**The facts prompt** differs from T1 in one paragraph, a test the model must apply:
*"A fact is about meaning, never about desired behaviour. Test each one: it must stay
true even for a badly built system that breaks every requirement."* Full text: in the
experiment file.

### E2a — 120 runs (3 specs x 4 settings x 10)

Each run is scored twice from the same formalization: with the facts switched off
("rules alone") and on ("with facts").

| Spec | Setting | Expected found: rules alone | Expected found: with facts | Runs with other conflicts (alone / with facts) | Facts kept per run (facts: runs) |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 10/10 | 0 / 0 | 1: 10 |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 / 0 | 0: 8, 1: 2 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 10/10 | 0 / 0 | 0: 9, 1: 1 |
| auth_openspec | 8 samples, symbols also vary | 3/10 | **7/10** | 0 / 0 | 0: 3, 1: 2, 2: 3, 3: 2 |
| delete_property | 1 greedy translation | 0/10 | **3/10** | 0 / 0 | 0: 7, 1: 1, 10: 1, 11: 1 |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 0/10 | 0 / 0 | 0: 9, 1: 1 |
| delete_property | 8 samples, T=1.0 | 0/10 | 0/10 | 0 / 0 | 0: 9, 2: 1 |
| delete_property | 8 samples, symbols also vary | 0/10 | **3/10** | 0 / 0 | 0: 6, 1: 4 |
| order | 1 greedy translation | 10/10 | 10/10 | 0 / 0 | 5: 10 |
| order | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 / 0 | 2: 4, 4: 1, 5: 5 |
| order | 8 samples, T=1.0 | 10/10 | 10/10 | 0 / 0 | 2: 5, 4: 3, 5: 2 |
| order | 8 samples, symbols also vary | 10/10 | 10/10 | 0 / 0 | 0: 2, 3: 1, 5: 5, 7: 2 |

Gaps and ambiguity flags are in [experiments/results/E2a_facts.md](experiments/results/E2a_facts.md).
No run failed.

**What it shows.**

1. **Facts did no harm in 120 runs.** No finding was removed (by construction, and
   asserted on every run). No unexpected conflict was added: all 10 conflicts that
   depend on a fact are expected ones.
2. **Facts recover clashes between two phrases.** Login spec with varying symbols:
   3/10 from the rules alone, 7/10 with facts. In the 4 recovered runs the read step
   had made separate symbols for "grant access" and "deny access", and the fact
   "access cannot be both granted and denied" (6/8 to 8/8 agreement) linked them.
3. **`delete_property`: from 0/40 to 6/40, and still 0/10 with the default settings.**
   All 6 use the fact "a record cannot be both removed and retained". The other 34 runs:
   - 9 runs: no symbol for "retained" at all (the soft-deletion rule got a policy
     symbol such as `soft_deletion_implemented`).
   - 23 runs: no fact links removal and retention. In almost all of them the read
     step describes the "removed" symbol as *"no longer accessible as an active record
     (logically deleted)"*, the charitable reading seen in T1, and under that reading
     the two do not exclude each other.
   - 2 runs: the linking fact was kept (5/8, 6/8) but the soft-deletion rule itself
     was rejected as unstable (samples split 3/2/2/1 and 4/2/1/1), so it was left
     out of the conflict check.
4. **The vote costs recall on this spec.** With one greedy answer there is no vote
   and every stated fact is kept (up to 11): 3/10. With 8 samples and the majority
   rule: 0/10 at both temperatures. The linking fact is stated by a minority of
   answers. Unvoted facts still added no unexpected conflict in 30 greedy runs.
5. **Wrong facts still get a majority.** On `order`, "an order cannot be both
   fulfilled and canceled", the business rule that broke T1, is kept in 17 of the 30
   runs with 8 samples (agreement 5/8 to 8/8) and in all 10 greedy runs. With the
   add-only design the findings are the three Kiro findings in all 40 runs.
6. **Run-to-run variance is large at n=10.** Login, symbols vary, rules alone: 6/10
   in E1, 3/10 here, 9/10 in E2b, same settings. Single rates from 10 runs are rough.

**Raw data.** [experiments/results/E2a_facts.json](experiments/results/E2a_facts.json): all 120
formalizations with their facts, plus the three prompts. Re-score without a GPU:
`python -m experiments.stability --rescore experiments/results/E2a_facts.json`.

### E2b — the same 120 runs again, keeping every raw answer

Same code, prompts and settings as E2a. The file also holds all sampled answers (the
8 translations of every rule and the 8 fact lists), so clustering and voting can be
redone offline.

| Spec | Setting | Expected found: rules alone | Expected found: with facts | Runs with other conflicts (alone / with facts) | Facts kept per run (facts: runs) |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 10/10 | 0 / 0 | 1: 10 |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 / 0 | 0: 10 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 10/10 | 0 / 0 | 0: 10 |
| auth_openspec | 8 samples, symbols also vary | 9/10 | 9/10 | 1 / 1 | 0: 10 |
| delete_property | 1 greedy translation | 0/10 | 1/10 | 0 / 0 | 0: 8, 1: 1, 9: 1 |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 2/10 | 0 / 0 | 0: 8, 1: 2 |
| delete_property | 8 samples, T=1.0 | 0/10 | 1/10 | 0 / 0 | 0: 9, 1: 1 |
| delete_property | 8 samples, symbols also vary | 0/10 | 1/10 | 0 / 0 | 0: 8, 1: 2 |
| order | 1 greedy translation | 10/10 | 10/10 | 0 / 0 | 5: 10 |
| order | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 / 0 | 2: 3, 4: 1, 5: 5, 7: 1 |
| order | 8 samples, T=1.0 | 10/10 | 10/10 | 0 / 0 | 0: 1, 2: 6, 4: 2, 6: 1 |
| order | 8 samples, symbols also vary | 10/10 | 10/10 | 0 / 0 | 2: 3, 3: 1, 5: 5, 7: 1 |

The one "other" conflict (login, symbols vary) comes from the rules alone, not from a
fact. No run failed. Raw data: [experiments/results/E2b_facts_samples.json](experiments/results/E2b_facts_samples.json).

### E2a + E2b together (240 runs)

| | Rules alone | With facts |
|---|---|---|
| `order`: expected conflicts found | 80/80 | 80/80 |
| `auth_openspec`, temperature-0 symbols | 60/60 | 60/60 |
| `auth_openspec`, symbols vary | 12/20 | 16/20 |
| `delete_property`, all settings | 0/80 | 11/80 |
| `delete_property`, default settings | 0/20 | 2/20 |
| Runs where facts removed a finding | | 0/240 |
| Runs where facts added an unexpected conflict | | 0/240 |
| Conflicts that depend on a fact | | 15, all expected |

Ambiguity flags with the default settings, over the three experiments:

| Rule | E1 | E2a | E2b |
|---|---|---|---|
| login rule 3, "reaches 5" (= 5 or >= 5) | 8/10 | 6/10 | 4/10 |
| delete_property rule 4, soft deletion | 8/10 | 5/10 | 9/10 |

**Conclusion of E2.** The add-only design holds: in 240 runs facts never cost a
finding and never produced a wrong one, while wrong facts were present in many runs.
The gain is real where the read step gives two phrases two symbols (login with
varying symbols), and small on `delete_property`, where the miss is decided earlier,
by how the read step describes "remove" (T3).

**Examples kept.** Two runs with a fact-dependent conflict were copied to
`experiments/examples/` (`delete_property_found` from E2b, `auth_split_symbols` from
E2a) and passed through the explanation step. In both, the explanation names the
assumption in plain words; for delete-property the proposed change is "mark the
Property record as deleted rather than removing it". Two cases, read by hand.

### E2 threshold — how strict should the vote be? (offline, on E2b's raw answers)

**Question.** E2a hinted that the majority vote throws away the fact
`delete_property` needs. Would a lower threshold find more, and at what price?

**Setup.** `experiments/fact_threshold.py` redoes the vote on the saved answers of the
90 E2b runs that have 8 samples (30 per spec), with four thresholds, then runs the
checks again. No GPU.

| Spec | Fact kept if implied by | Expected found | Runs with other conflicts | Facts kept per run |
|---|---|---|---|---|
| auth_openspec | at least 5 of 8 (default) | 29/30 | 1 | 0.0 |
| auth_openspec | at least 3 of 8 | 29/30 | 1 | 0.4 |
| auth_openspec | at least 2 of 8 | 29/30 | 1 | 0.7 |
| auth_openspec | at least 1 of 8 (no vote) | 29/30 | 1 | 1.4 |
| delete_property | at least 5 of 8 (default) | 4/30 | 0 | 0.2 |
| delete_property | at least 3 of 8 | 6/30 | 0 | 0.4 |
| delete_property | at least 2 of 8 | 7/30 | 0 | 1.6 |
| delete_property | at least 1 of 8 (no vote) | 7/30 | **4** | 4.6 |
| order | at least 5 of 8 (default) | 30/30 | 0 | 3.6 |
| order | at least 3 of 8 | 30/30 | 0 | 5.4 |
| order | at least 2 of 8 | 30/30 | 0 | 5.8 |
| order | at least 1 of 8 (no vote) | 30/30 | **5** | 6.8 |

(The login "1" is the rules-alone conflict noted above, the same at every threshold.)

**What it shows.**

1. **Without a vote, facts start to produce wrong conflicts**: 9 of 90 runs get an
   unexpected conflict when every stated fact is kept. So the add-only rule is not
   enough by itself; the vote is what keeps fact-based findings clean.
2. **Any vote of 2 or more removed all of them** in this data.
3. **A lower threshold gains little**: `delete_property` 4/30 at the default, 6/30 and
   7/30 at lower thresholds. With 30 runs these differences are within noise.

**Decision.** The default stays "more than half". Table:
[experiments/results/E2b_facts_samples_threshold.md](experiments/results/E2b_facts_samples_threshold.md).

---

## T3 — Telling the read step to read literally (2026-11-17, probes, not adopted)

**Question.** E2a blames the charitable symbol description for most `delete_property`
misses. Does an instruction in the read prompt remove it?

**Setup.** One extra bullet in the read prompt, default settings, facts on.

- **v1** (1 run per spec): *"Take every requirement literally and on its own. Never
  bend the meaning of one requirement so that it agrees with another: if two
  requirements seem to disagree, the symbols must let that disagreement show. A
  description says what the words of the requirement say, not what would make the
  document consistent."*
- **v2** (3 runs on delete_property, 1 on each other spec): v1 plus *"... adds no
  qualification the requirement does not state (for "block the sender", not "block or
  warn", "partly block" or "block where possible")"*.

**Result.**

| | delete_property | order | auth_openspec |
|---|---|---|---|
| v1 | not found (0/1). "Removed" described as *"removed from the system's active data store"*; symbols for both "removed" and "retained" exist; no fact agreed; rule 4 ambiguous 4/4 | 3 Kiro findings; 5 facts | "grant" and "deny" became two symbols; conflict {1,4} found only through the fact "access cannot be both granted and denied" (7/8); rule 1 newly ambiguous 6/2; 3 gaps |
| v2 | not found (0/3). Same description in all three runs; rule 4 ambiguous each time | 3 Kiro findings; 2 facts | unchanged from the normal prompt |

**Conclusion.** The instruction does not change how the model reads "remove the
record": it keeps adding "active". The model appears to hold that, next to a
soft-deletion rule, "remove" means logical removal. Two wordings, four runs on the
target spec, so this is an indication, not a rate. Not adopted. What the pipeline does
report for this spec in most runs is an ambiguity on the soft-deletion rule.

**Raw data.** Not saved (probe output only).

---

## C1 — Correction: how Kiro itself finds the delete-property contradiction (2026-11-17)

Re-reading the Kiro blog showed that we had set the wrong target for
`delete_property`. Quotes below were retrieved on 2026-11-17 through a page-reading
tool; check them against the page before citing.

**What the blog says.**

- The contradiction is reported by the **LLM-driven refinement stage**, not by the
  solver. Under the heading "Refinement: getting requirements to the right level of
  detail", the refinement analysis lists "Criterion 2 contradicts Criterion 4"
  ("Criterion 2 says 'remove the record,' which is a hard delete"). Refinement then
  rewrites criterion 2 to mark the record as deleted, and adds criteria for missing
  paths (active leases, nonexistent property, cancelled confirmation).
- The **solver** examples in the blog (conflict {R2,R3}, conflict {R1,R5}, the gap)
  all come from the order spec, which we reproduce in 80/80 runs.
- Separately, "remove the record" appears as an **ambiguity question** from
  auto-formalization (semantic entropy): *"The phrase 'remove the record' could mean
  the record is gone entirely, or marked as deleted and retained for audit."*
- **Scope:** the analysis "analyzes your `requirements.md`", plus the user story. The
  docs say it "reasons across your full requirement set - not just each requirement in
  isolation". Nothing in the blog or the docs mentions other existing specs, steering
  files or the codebase as input.
- Domain facts ("background assertions") are sampled and kept by "a frequency
  threshold", and the blog says extracting implicit domain knowledge "needs more work
  in the future".

**What this changes.**

1. `delete_property` at 2/20 is **not a failure to reproduce Kiro's solver**. Kiro does
   not get this finding from the solver either. Our expected conflict {2,4} stays as a
   measure of "can the formal layer see it", but must be labelled that way.
2. The closest formal-side counterpart in Kiro is the ambiguity question. We flag an
   ambiguity on this spec in most default runs, but on rule 4 (soft deletion), not on
   rule 2 ("remove the record") where Kiro asks it.
3. What is missing to reproduce Kiro on this example is the **refinement stage**
   (built next: T4, E3).
4. The idea "choose each requirement's symbols without showing the other requirements"
   is **withdrawn**. It tried to force the solver to do refinement's job, and it would
   cost shared symbols, on which the solid findings depend.
5. Our `specs/delete_property/requirements.md` paraphrased the blog. It was replaced
   by the blog's own wording before E3 ("... SHALL remove the Property record from the
   Platform", "... SHALL implement soft deletion to retain Property records in the
   database for audit purposes while hiding them from the user interface").

---

## T4 — Wording of the review prompt (2026-11-17, probes)

**Question.** The review track (`refine.py`) is one LLM call that reads the text and
notes contradictions, wording problems and missing cases. How much does its prompt
matter?

**Setup.** Review only, temperature 0, 6 to 10 calls per spec on an otherwise idle
server. Counted: calls that report each expected conflict as a "contradiction".

| Prompt | delete {2,4} | order {2,3} | order {1,5} | login {3,5} | login {1,4} |
|---|---|---|---|---|---|
| v1: first definitions of the three kinds | 6/6 | 6/6 | 0/6 | 1/6 | 0/6 |
| v2: sharper definitions (**adopted**) | 10/10 | 10/10 | 0/10 | 10/10 | 0/10 |
| v3: v2 + answer in steps "goal, obstacles, notes" + "compare every pair" | 0/10 | 10/10 | 0/10 | 0/10 | 0/10 |
| v4: v2 + "compare every pair of requirements" | 10/10 | 10/10 | 0/10 | 10/10 | 0/10 |

- **v1 to v2.** v1 filed the login clashes under "wording" ("R3 does not exclude
  administrators"). v2 defines a contradiction as "can apply in the same situation and
  demand incompatible outcomes" and adds "any problem that involves a second
  requirement is a contradiction, not wording". v1 also called "prompt for
  confirmation" vague and proposed a modal dialog; v2 adds "do not ask for more detail
  than a tester needs", and that note disappeared. With v2 the note "D4 prescribes an
  implementation" appears in 10 of 10, as in the Kiro blog.
- **v3.** Making the model list goal and obstacles first (to get more "missing" notes)
  made it lose the contradictions. Dropped.
- **v4.** Asking for pairwise comparison changed nothing.

**Conclusion.** The review is sensitive to how the prompt is built, more than to its
instructions: a scaffold meant to help removed its best finding. No wording made it
find the two conflicts that need several conditions to line up (order {1,5},
login {1,4}); the solver finds those.

**Raw data.** Not saved (probe output only). The adopted prompt is stored in the E3 file.

---

## E3 — Two tracks: solver and review (2026-11-17)

**Question.** With the review added, how often is each expected conflict found, by
which track, and does the review raise false alarms?

**Setup.** As E2 (3 specs x 4 settings x 10 runs = 120 runs), each run now also
making one review call. The review does not depend on the settings, so per spec it is
simply repeated 40 times. `delete_property` in the blog's wording. Review prompt v2.

How often each expected conflict is found (40 runs per spec):

| Expected conflict | Solver, rules alone | Solver, with facts | Review | Either track |
|---|---|---|---|---|
| order {2,3}: backorder demanded and forbidden | 40/40 | 40/40 | 40/40 | 40/40 |
| order {1,5}: fulfil a canceled-and-refunded order | 40/40 | 40/40 | 0/40 | 40/40 |
| login {1,4}: correct password on a locked account | 35/40 | 38/40 | 0/40 | 38/40 |
| login {3,5}: lock at 5 failures, never lock administrators | 40/40 | 40/40 | 31/40 | 40/40 |
| delete_property {2,4}: remove the record, retain the record | 0/40 | 1/40 | 40/40 | 40/40 |

Unexpected conflicts: none from the solver and none from the review, in 120 runs.

What the review notes, per spec (runs out of 40):

| Spec | Notes |
|---|---|
| order | contradiction {2,3}: 40. One "missing" note: 40 (25 "cancellation is not validated", 15 "nothing handles unavailable inventory") |
| login | contradiction {3,5}: 31; in the other 9 runs the same clash is filed as "wording" of rule 3. "wording" of rule 1: 8, of rule 5: 7. One "missing" note: 39, nearly always "no way to unlock an account" |
| delete_property | contradiction {2,4}: 40. "wording" of rule 4 (prescribes an implementation): 40. No "missing" note |

**What it shows.**

1. **The two tracks are complementary.** The solver nearly never finds
   delete_property {2,4}; the review never finds order {1,5} or login {1,4}. Together
   they find every expected conflict in 198 of 200 cases.
2. **Why the solver misses {2,4}:** in 40 of 40 runs the read step describes the
   symbol of rule 2 as *"removed from the Platform's active data set"* or similar, a
   reading under which rule 2 agrees with rule 4. The review, reading the words, says
   "remove ... from the Platform" against "retain ... in the database".
3. **What the review misses** are clashes that need conditions of two rules to hold
   at once (a submitted order that is also canceled-and-refunded; a correct password
   on a locked account). That is the case-by-case reasoning the solver does.
4. **No false alarm from the review here**, but its labels move: the login clash is a
   "contradiction" in 31 runs and "wording" in 9. In the idle-server probes of T4 it
   was 10 of 10. Server load changes the answers (L10).
5. **Compared with Kiro's own refinement result** for delete_property (blog): Kiro
   reports the contradiction, "criterion 4 mixes what and how", a wrong EARS pattern in
   criterion 5, and adds three missing cases. Our review reports the first two in 40
   of 40 runs, and none of the others.
6. **The loop closes** (one run). Applying the review's proposals gives `refined.md`;
   speccheck on that file: all five rules accepted 8 of 8 (rule 4 was ambiguous 4/4
   before), no conflict, no ambiguity, one remaining wording note.

Formal-track side numbers of E3 (facts, gaps, ambiguity flags per setting):
[experiments/results/E3_refine.md](experiments/results/E3_refine.md).

**Raw data.** [experiments/results/E3_refine.json](experiments/results/E3_refine.json): every
formalization with its raw answers, every review, the four prompts.

### E3 offline — can facts that few samples state recover delete_property?

**Question.** The solver misses delete_property {2,4} because no fact links "removed"
and "retained". Do some of the 8 sampled fact lists state that link, below the
majority?

**Setup.** No GPU: the 30 delete_property runs of E3 that have 8 samples. First we
count, per run, how many of the 8 fact lists imply "a removed record is not retained".
Then `experiments/fact_threshold.py` redoes the vote with lower thresholds on all
three specs (90 runs).

| Fact lists (of 8) that imply "removed excludes retained" | 0 | 1 | 2 | 3 | 4 | 5 or more |
|---|---|---|---|---|---|---|
| Runs (27 have both symbols; 3 have no such pair) | 4 | 7 | 5 | 9 | 2 | 0 |

The opposite statement ("a removed record is still retained") appears in 1 list of 8,
in 4 runs. So a minority states the link, the rest are silent, and almost none
disagrees. A majority is never reached.

| Spec | Fact kept if implied by | Expected found | Runs with other conflicts | Facts kept per run |
|---|---|---|---|---|
| delete_property | at least 5 of 8 (default) | 0/30 | 0 | 0.2 |
| delete_property | at least 3 of 8 | 4/30 | 1 | 2.7 |
| delete_property | at least 2 of 8 | 4/30 | **10** | 6.9 |
| delete_property | at least 1 of 8 | 3/30 | 5 | 16.3 |
| order | at least 5 / 3 / 2 of 8 | 30/30 each | 0 | 3.5 / 5.4 / 5.8 |
| order | at least 1 of 8 | 30/30 | 4 | 6.9 |
| auth_openspec | any threshold | 28/30 | 0 | 0.3 to 1.3 |

**Conclusion.** Lowering the threshold is not a way out: the conflict is found in at
most 4 of 30 runs, and wrong conflicts appear in up to 10. (On our earlier paraphrase
of this spec, E2, the same thresholds looked harmless; the blog's wording gives more
symbols and more stray facts.) The majority rule stays. The formal check has no
answer to this spec yet.

Table: [experiments/results/E3_refine_threshold.md](experiments/results/E3_refine_threshold.md).

---

## D1 — Decision: the formal part only (2026-11-17)

The LLM review of the text ("refinement", T4, E3) stays in the code but is switched
off by default (`--review` turns it on). Reason, from the project owner: reading the
text with an LLM is what every tool does; this work is about the formal check. The
review results above remain as a comparison point. The default pipeline, the saved
outputs under `specs/` and the experiments are formal-only from here on.

---

## T5 — Translating a rule again without its private symbols (2026-11-17, probe)

**Question.** The solver misses `delete_property` because "removed" is a symbol that
only rule 2 uses, so nothing can clash with it. What does the model say if rule 2 has
to be written without that symbol?

**Setup.** After a normal formalization, every rule whose consequent uses a symbol
that no other rule uses is translated 8 more times with that symbol hidden. The
answers are clustered by meaning as usual; "none" = cannot be expressed. Three runs on
`delete_property`, two on `order` and `auth_openspec`. Development specs only.

| Rule (hidden symbol) | Result |
|---|---|
| delete_property rule 2 ("remove the Property record"; `property_record_removed`) | 7/8, 8/8, 7/8: `deletion_confirmed => (not property_record_retained_in_db)` |
| delete_property rule 1 ("prompt for confirmation") | 4/8, 6/8, 7/8: `deletion_initiated => deletion_confirmed`, which is **wrong** |
| delete_property rules 3 and 4 | 8/8 and 7/8 "cannot be expressed", which is right |
| order rule 4 ("refund all payments") | 8/8, twice: `order_canceled => order_canceled_and_refunded` |
| auth_openspec rule 1 in a run with a separate "access denied" symbol | 8/8: `... => (not access_denied)` |

**Conclusions.**

1. Asked this way, the model takes "remove the record" literally: not retained in the
   database. That is the reading under which rule 2 clashes with rule 4. When it chose
   the symbols (read step) it had described the same phrase charitably in 40 of 40
   runs (E3). The question decides the reading.
2. Shown every other symbol, the model also "explains" an outcome by an event of
   another rule ("the system prompts for confirmation" becomes "the owner confirms").
   So the step was built to show only the rule's own condition and the *outcomes* of
   the other rules.
3. It finds the same links the open question about domain facts finds only sometimes
   ("granted excludes denied").

This became step 5 of `formalize.py` ("links"): an agreed restatement (more than half
of the samples) is added as an assumed fact, add-only like the others. Measured in E5.

---

## E4 — Evaluation on specs the prompts have not seen (2026-11-17)

**Question.** All earlier numbers come from the three specs the prompts were developed
on. What are the rates on other specs, and how often does a clean spec get a false
alarm?

**Setup.** `eval/`: 6 small specs in new domains (library, parking, thermostat,
upload, booking, vending), 3 in Kiro EARS and 3 in OpenSpec format, written after the
prompts were fixed. Each has a clean version and versions with one defect planted by
rule (`experiments/make_eval.py`): a *direct* conflict (a blanket prohibition or the
opposite outcome on the same trigger), an *overlap* conflict (an exception whose
condition can hold together with an existing rule), and for 3 specs an *ambiguity*.
21 specs, 3 runs each, 5 symbol sets per run = 315 formalizations. 16 planted
conflicts (48 with repetitions), 6 clean specs (18 runs), 3 planted ambiguities (9).
Code before step 5 (no links). Scored offline under seven configurations.

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts, all runs | Planted ambiguities found | Other ambiguity flags |
|---|---|---|---|---|---|---|---|
| 1 symbol set (default) | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 10 |
| 1 symbol set, without assumed facts | 24/48 | 9/21 | 15/27 | 0/18 | 2 | 1/9 | 10 |
| 1 symbol set, pairs of rules only | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 10 |
| 3 symbol sets, found with any | 42/48 | 18/21 | 24/27 | 2/18 | 5 | 3/9 | 22 |
| 3 symbol sets, found with most | 36/48 | 15/21 | 21/27 | 0/18 | 0 | 1/9 | 6 |
| 5 symbol sets, found with any | 45/48 | 18/21 | 27/27 | 2/18 | 5 | 5/9 | 26 |
| 5 symbol sets, found with most | 36/48 | 15/21 | 21/27 | 0/18 | 0 | 3/9 | 7 |

**What it shows.**

1. **Recall on unseen specs is 73% with the default settings** (35 of 48), against
   nearly 100% on the development specs (delete_property aside). The earlier numbers
   were optimistic, as expected.
2. **No false alarm on a clean spec** with one symbol set (0 of 18 runs). Two
   unexpected conflicts in the 45 runs with planted defects, both the same pair in
   `booking_overlap`.
3. **Assumed facts matter here: 50% without them, 73% with them.** On the development
   specs they hardly mattered. Unseen specs get more split symbols.
4. **Several symbol sets trade recall against false alarms, and the count separates
   them.** Reporting what any of 5 sets finds: 94% recall, but false alarms on 2 of 18
   clean runs. Reporting only what most sets find: 75% recall, no unexpected conflict
   at all. So "found with k of K" is a usable confidence.
5. **Triples of rules add nothing here.** No planted conflict needs three rules, and
   allowing triples produced no extra false alarm.
6. **Ambiguity detection is weak on planted ambiguities: 1 of 9** with one symbol
   set, while 10 other rules were flagged. "For 14 days" and the and/or scope were
   never flagged; "within 24 hours" once. The sampled translations mostly agree on one
   reading of a phrase we consider ambiguous.
7. **Consistent misses.** `parking_direct` (0/3: "keeps the barrier closed until an
   attendant opens it" against "opens the barrier") and `upload_direct` (0/3: "does
   not notify anyone" against "notifies the folder owner"; rule 6 is flagged ambiguous
   in 3 of 3 runs instead).

**Looking inside the cases** (read off the saved formal models; nothing was tuned):

| Case | What the formalization did |
|---|---|
| `upload_direct`, missed | Two symbols: `owner_notified` and `anyone_notified`, with no fact linking them. A split-symbol miss |
| `parking_direct`, missed | Rule 6 became `arrives => (not open or attendant_opens)`. That is faithful, and it leaves a way out (the attendant opens), so no forced situation is contradictory. Our planted "direct" conflict was not direct |
| `booking_overlap`, the 2 unexpected conflicts | "at least 24 hours" and "less than 24 hours" became two yes/no symbols that can both be true. A fact saying they exclude each other was kept, but facts are add-only, so it could not stop the false conflict |
| `vending_ambiguity`, `library_ambiguity`, not flagged | All 8 samples chose the same reading ("(credit or card) and in stock"; "exactly 14 days"). The model is sure where a human would ask |

Two things follow. A proven conflict whose situation the assumed facts call impossible
could be marked as doubtful (not removed: T1). And entropy over samples measures the
model's doubt, not the reader's. Both are observations made on the evaluation set, so
acting on them would use up the hold-out.

Per-spec table: [experiments/results/E4_eval.md](experiments/results/E4_eval.md).

**Raw data.** [experiments/results/E4_eval.json](experiments/results/E4_eval.json): all 315 formal
models with their raw answers, the expected findings, the prompts. Re-score:
`python -m experiments.evaluate --rescore experiments/results/E4_eval.json`.

**Hold-out rule.** The prompts must not be tuned on `eval/`. Step 5 (T5) was designed
on the development specs before E4's numbers were read.

---

## E5 — The same evaluation with links (2026-11-17)

**Question.** Step 5 ("links", T5) was built on the development specs. Does it help on
the unseen specs, and does it cause false alarms?

**Setup.** As E4, with step 5 switched on. Held-out set: 21 specs, 3 runs, 3 symbol
sets per run (189 formalizations). Development specs: 8 runs each, 1 symbol set. The
step was designed and fixed before any E4 or E5 number was read.

Held-out set, same counting as E4:

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts, all runs | Planted ambiguities found | Other ambiguity flags |
|---|---|---|---|---|---|---|---|
| 1 symbol set (default) | **44/48** | 21/21 | 23/27 | 0/18 | 2 | 2/9 | 7 |
| 1 symbol set, without assumed facts | 27/48 | 10/21 | 17/27 | 0/18 | 2 | 2/9 | 7 |
| 1 symbol set, pairs of rules only | 44/48 | 21/21 | 23/27 | 0/18 | 2 | 2/9 | 7 |
| 3 symbol sets, found with any | 48/48 | 21/21 | 27/27 | 1/18 | 3 | 5/9 | 21 |
| 3 symbol sets, found with most | 43/48 | 20/21 | 23/27 | 0/18 | 0 | 0/9 | 7 |

Development specs (8 runs each, default configuration):

| Spec | Expected conflicts found | Unexpected |
|---|---|---|
| order | {1,5}: 8/8, {2,3}: 8/8 | none |
| auth_openspec | {1,4}: 8/8, {3,5}: 8/8 | none |
| delete_property | {2,4}: **8/8** (1/40 before, E3) | none |

**What it shows.**

1. **Links raise recall on unseen specs from 73% to 92%** with the default settings
   (35/48 in E4, 44/48 here), and the two specs E4 always missed are now always found
   (`parking_direct`, `upload_direct`: 0/3 to 3/3).
2. **No new false alarm.** Clean specs: still 0 of 18 runs. The same two unexpected
   conflicts as in E4 (`booking_overlap`, the two-symbol "24 hours" case).
3. **`delete_property` is now found by the solver: 8 of 8 runs**, as a conflict that
   depends on the link "what rule 2 demands: the record is no longer retained in the
   database" (8 of 8 samples each time). This is the Kiro blog's contradiction, which
   Kiro itself gets from its LLM refinement stage.
4. **Assumed facts (voted facts plus links) carry a large part of the result:** 27/48
   without them, 44/48 with them.
5. **Symbol sets:** with 3 sets, "found with any" reaches 48/48 at the price of one
   false alarm on a clean run; "found with most" has no unexpected conflict at all.
6. **Not every link is right.** In the development runs a wrong link appeared in 3 of
   8 `delete_property` runs ("confirmation message shown" taken for "confirmation
   prompt"). It caused no finding. 28 of the 63 held-out runs made at least one link.
7. **Ambiguity stays weak:** 2 of 9 planted ambiguities.

E4 and E5 are separate LLM runs of 63 each, so part of the 35-to-44 difference is run
noise; the two always-missed specs turning into always-found is not.

Tables: [experiments/results/E5_eval_links.md](experiments/results/E5_eval_links.md),
[experiments/results/E5_dev_links.md](experiments/results/E5_dev_links.md).

**Raw data.** `experiments/results/E5_eval_links.json`, `experiments/results/E5_dev_links.json`.

---

## Notes on the new formal features (2026-11-17)

- **Conflicts that need three rules** are now searched (unit-tested on a hand-written
  case). On the held-out set they changed nothing: no planted conflict needs three
  rules, and no false alarm came from triples.
- **Scenarios** (behaviours the rules allow or rule out, as in Kiro): the solver lists
  one candidate per rule or pair; an LLM judge scores how surprising each is; at most
  three are shown. On the order spec the one shown is "the order is fulfilled although
  it was never submitted". There is no ground truth for scenarios, so there is no
  rate. First try: a yes/no judge kept 5 of 5 candidates on `delete_property`; a 0 to
  3 score with a threshold of 2 and a cap of 3 replaced it.

---

## D2 — Decision: a second held-out set (2026-11-18)

Better ambiguity detection and the two repairs (doubtful conflicts, checked
links) were designed after reading the results of E4 and E5 on `eval/`. So
`eval/` became development data, and `eval2/` was written as a new held-out set
before any of the new parts was tried on it.

`eval2/`: 6 new domains (transfer, newsletter, discounts, exam, pharmacy,
rental), half Kiro EARS and half OpenSpec. 30 specs: 6 clean, 6 with a planted
direct conflict, 6 with a planted overlap conflict, 12 with a planted
ambiguity. The ambiguities are of four kinds, chosen so that both readings make
sense in the domain: a boundary ("within", "between", "after"), the scope of
"and"/"or", the scope of "only", the scope of "if". The expected answers are in
each `expected.json`; generator: `experiments/make_eval.py`.

---

## T6 — Building step 6 on development data (2026-11-18, probes)

**Question.** All 8 samples can agree on a wrong translation, and on a wrong
link. Does a different kind of question reveal it: Z3 picks a concrete
situation, and the LLM says what ONE requirement, read on its own, demands
there?

**Setup.** Development specs only (`specs/`, and `eval/`, now development
data). 3 runs per spec per round. Four rounds:

| Round | What was tried | What happened |
|---|---|---|
| 1 | Readings: "list other readings, or an empty list". Links: "is the rule broken in this situation?" | Almost every rule got an empty list: the model is sure there is only one reading. Every link was confirmed, wrong ones too: the situation shows the rule applying but not its demand being met, so "broken" is the natural answer |
| 2 | Readings: always propose two or three. Links: "can the rule be fully obeyed while these facts hold?" | The right `delete_property` link (removed means not kept in the database) was confirmed 8/8 in 3 of 3 runs; a wrong one ("confirmation message" taken for "confirmation prompt") was rejected 5 to 3. The login translation "reaches 5" = "exactly 5", agreed by all 8 samples, was contradicted 8 of 8 when asked about 6 attempts. But readings that borrow a condition from another rule ("fulfil the order only if it is not canceled") got split answers: false flags |
| 3 | Other readings must use only the translation's own symbols | Planted ambiguities: "on loan for 14 days" 2/2 (sampling had never caught it), "within 24 hours" 2/2 (by sampling), the and/or case 0/2. Login "reaches 5": 2/2. Clean specs: 3 flags in 12 runs, each with 6 of 8 answers for the translation. The wrong link above was confirmed 7 to 1 in one run |
| 4 | One rule for every assumption: more than half of the answers (was 7 of 8 for translations) | The 3 clean-run flags of round 3 would not have been raised |

The design was then frozen, and E6 and E7 ran on it.

**Raw data.** Not saved (probe output only).

---

## E6 — The old evaluation set with step 6 (2026-11-18)

**Setup.** `eval/` (development data since D2), 21 specs x 3 runs, one symbol
set. The same runs are scored with and without step 6.

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs |
|---|---|---|---|---|---|
| default (with step 6) | 41/48 | 0/18 | 1 | 5/9 | 1 |
| without step 6 | 41/48 | 0/18 | 1 | 2/9 | 0 |
| doubtful conflicts set aside | 39/48 | 0/18 | 0 | 5/9 | 1 |
| without assumed facts and links | 26/48 | 0/18 | 1 | 5/9 | 1 |

Conflicts marked doubtful: 6 in 63 runs. `booking_ambiguity` (3,4) in 3 runs (an
allowed consequence of the planted ambiguity); `booking_overlap` (3,4) once,
the false alarm of E4 and E5; `library_overlap` (1,6) twice, an expected
conflict: the facts say a book reserved for another member is not "available",
which is one reading of the spec.

E5 found 44/48 on the same specs with the same pipeline without step 6; E6
finds 41/48. Different LLM runs: the run-to-run spread is about 3 of 48.

**Raw data.** [experiments/results/E6_eval_step6.json](experiments/results/E6_eval_step6.json), table
[experiments/results/E6_eval_step6.md](experiments/results/E6_eval_step6.md).

---

## E7 — The held-out set `eval2/` (2026-11-18)

**Setup.** 30 specs x 3 runs = 90 runs, one symbol set. Code frozen after T6.
12 planted conflicts (36 with repetitions), 6 clean specs (18 runs), 12
planted ambiguities (36).

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (with step 6) | **31/36** | 14/18 | 17/18 | **0/18** | 3 | **17/36** | 9 | 57 |
| without step 6 | 32/36 | 15/18 | 17/18 | 0/18 | 6 | 13/36 | 6 | 40 |
| without link checks | 32/36 | 15/18 | 17/18 | 0/18 | 6 | 17/36 | 9 | 57 |
| doubtful conflicts set aside | 31/36 | 14/18 | 17/18 | 0/18 | 3 | 17/36 | 9 | 57 |
| without assumed facts and links | 18/36 | 6/18 | 12/18 | 0/18 | 0 | 17/36 | 9 | 57 |
| pairs of rules only | 31/36 | 14/18 | 17/18 | 0/18 | 3 | 17/36 | 9 | 57 |

Planted ambiguities found, by kind (default):

| Kind | Found |
|---|---|
| boundary: "within", "between" (2 specs), "after" | 7/12 |
| scope of "and" / "or" (3 specs) | 5/9 |
| scope of "only" (2 specs) | 3/6 |
| scope of "if" (3 specs) | 2/9 |

**What it shows.**

1. **Conflicts: 31 of 36 (86%), no false alarm on clean specs.** Missed:
   `pharmacy_direct` in 3 of 3 runs ("reject the request" against "prepare the
   refill" was never linked), and one run each of `newsletter_direct` and
   `rental_overlap`. Assumed facts and links carry much of it: 18 of 36 without.
2. **Questions find more ambiguities: 13 → 17 of 36,** at a price of 3 more
   flags on clean specs (6 → 9 in 18 runs). On E6: 2 → 5 of 9, clean flags 0 → 1.
   "If" and "only" scopes are the weak kinds.
3. **Link checks halve the unexpected conflicts (6 → 3)** and cost one planted
   conflict (32 → 31, one run of `newsletter_direct`). 15 of 60 links were
   rejected.
4. **The doubtful mark did not trigger once.** The pattern it targets (two
   symbols for complementary conditions) did not occur in E7. On E6, setting
   doubtful conflicts aside removes 1 unexpected conflict and loses 2 expected
   ones. Kept as a mark, not used as a filter.
5. **The 3 unexpected conflicts:** `newsletter_direct` (5,6) twice: a visitor
   signs up at the same moment a subscriber changes an address, and "send no
   email" meets "send a confirmation email". Two events at once: an artefact of
   the one-snapshot model. `pharmacy_overlap` (2,3) once.
6. **Many other ambiguity flags** (57, of which 40 come from sampling alone).
   Some may be real ambiguities nobody planted; there is no ground truth for them.

**Raw data.** [experiments/results/E7_eval2.json](experiments/results/E7_eval2.json), table
[experiments/results/E7_eval2.md](experiments/results/E7_eval2.md).

---

## D3 — Decision: a third held-out set (2026-11-18)

The results of E7 were read to design the next two changes (questions that show
both readings; a mark on conflicts that need two events at once). So `eval2/`
became development data, and `eval3/` was written first, as the new held-out
set: 6 new domains (helpdesk, doors, streaming, claims, gym, moderation), 24
specs. 6 clean, 6 with a planted conflict, 12 with a planted ambiguity: 3 of
each kind (boundary, "and"/"or", "only", "if"). Its clean specs contain, as real
specs do, events whose outcomes would clash if they happened at the same moment.

---

## T7 — Rebuilding the reading questions (2026-11-18, development data)

**Question.** In E7 the questions about readings found "if" and "only"
ambiguities rarely, and flagged clear rules. Can a different question do both
better?

**Setup.** `eval2/`: its 9 ambiguity specs with "if", "only", boundary and
and/or readings, 6 clean specs, `newsletter_direct`; 2 runs each (18 planted
ambiguities, 12 clean runs).

| Version | The question | Planted found | Flags, clean specs | Other flags |
|---|---|---|---|---|
| E7 (for comparison: 3 runs, same specs) | "What does the requirement say about this situation?" obeyed / broken / unclear | 11 of 27 | 9 in 18 runs | many |
| v2 | Both readings shown: "Do the words decide which is meant?" A / B / either, asked in both orders | 5 of 18 | 0 in 12 runs | 4 |
| v3 | "Could a careful developer take the words in the other reading?" yes / no | 9 of 18 | 12 in 12 runs | 32 |

Answers for the translation (of 8) against its strongest other reading, v2:

| | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| planted ambiguous rules | 1 | | 1 | 2 | 2 | 4 | 3 |
| all other rules | 1 | 1 | 2 | 3 | 9 | 35 | 73 |

The two groups overlap: asked to choose, the model sides with its own reading of
rules a reader would query almost as often as of clear ones. v3 overlaps the
other way: the model calls nearly every proposed reading defensible.

**Decision.** Keep v2. The threshold is a parameter of the scoring (`settle`):
by default a translation stands when it gets more than half of the answers
(the rule used everywhere else); the stricter "at least 7 of 8" is scored too.
When the words do not support the translation, the author is asked; an earlier
draft that silently replaced the translation was dropped.

Also seen: in 2 of 2 runs the read step put "only" inside a symbol name
(`issue_sent_to_active_subscribers_only`), although a new prompt line forbids
it. No other reading can be written over such a symbol.

**Raw data.** Not saved (probe output only).

---

## E8 — The held-out set `eval3/` (2026-11-18)

**Setup.** 24 specs x 3 runs = 72 runs, one symbol set, code frozen after T7. 7
planted conflicts (21 with repetitions), 6 clean specs (18 runs), 12 planted
ambiguities (36). A run on `eval2/` (E9) was started alongside and stopped to
give E8 the GPUs; it has no results.

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags, clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|
| default, doubtful conflicts counted | 15/21 | 9/18 | 85 | 14/36 | 6 | 15 |
| **default, doubtful conflicts set aside** | **15/21** | **1/18** | **25** | 14/36 | 6 | 15 |
| without step 6 (sampling only), doubtful counted | 15/21 | 12/18 | 88 | 17/36 | 11 | 29 |
| without step 6, doubtful set aside | 15/21 | 4/18 | 28 | 17/36 | 11 | 29 |
| translation needs 7 of 8 answers | 15/21 | 9/18 | 85 | **21/36** | 11 | 36 |
| without assumed facts and links | 10/21 | 3/18 | 12 | 14/36 | 6 | 15 |

Planted ambiguities found, by kind (9 each):

| Kind | Sampling only | Questions, more than half (default) | Questions, 7 of 8 |
|---|---|---|---|
| boundary | 4 | 5 | 6 |
| "and" / "or" | 2 | 2 | 5 |
| "only" | 7 | 6 | 6 |
| "if" | 4 | 1 | 4 |
| all | 17 of 36 | 14 of 36 | 21 of 36 |

**What it shows.**

1. **The mark for two events at once works.** 48 conflicts got it, all of them
   false alarms; the facts mark added 12 more, also all false. No planted
   conflict was marked. Setting marked conflicts aside: false alarms on clean
   runs 9 → 1 of 18, unexpected conflicts 85 → 25, planted conflicts found
   unchanged (15 of 21).
2. **The 25 that remain** are all in `moderation`. "A comment receives its third
   report" was written as a counter, `(= comment_report_count 3)`, a state and
   not an event, so "a moderator approves a comment that has 3 reports" is a
   one-event situation, and the clash between "hide it" and "publish it" stands.
3. **Ambiguity: the questions are a dial, not a fix.** More than half
   (default): flags on clean specs 11 → 6 and other flags 29 → 15, but 14 instead
   of 17 planted ambiguities, and "if" falls from 4 to 1 of 9. At 7 of 8: 21 of
   36 found, the best so far, with as many clean-spec flags as sampling alone.
4. **"If" stays the hardest kind** (at best 4 of 9). "Only" is found well by
   sampling alone (7 of 9).
5. **Conflicts: 15 of 21 (71%)**, lower than on `eval2/` (31 of 36). Missed:
   `doors_overlap` in 6 of 6 ("unlocks all doors" against "keeps the door
   locked": two symbols, never linked).

**Raw data.** [experiments/results/E8_eval3.json](experiments/results/E8_eval3.json), table
[experiments/results/E8_eval3.md](experiments/results/E8_eval3.md).

---

## D4 — Decision: a fourth held-out set, and a caveat for E8 (2026-11-18)

**A fourth set.** The results of E8 were read to design steps 17 (events
written as states) and 18 (ambiguity beyond one model's judgment), so `eval3/`
became development data. `eval4/` was written first, before either step was
designed: 6 new domains (elevator, lockers, irrigation, attendance, printing,
delivery), 24 specs, laid out like `eval3/` (7 planted conflicts, 12 planted
ambiguities, 3 of each kind). On purpose, every spec has a counted event ("the
doors fail to close for the third time in a row"), the kind of event that E8
showed being written as a state.

**A caveat for E8.** The read prompt's example of a restriction kept out of a
symbol name ("not door_opened_only_for_staff, but door_opened and
person_is_staff") was added during T7, five minutes after `eval3/` was
written. `eval3/` has a doors spec whose planted ambiguity is an "only" case
("unlocks the door only for a valid badge"). That spec was found in 2 of 3
runs by sampling only, 3 of 3 by default, 3 of 3 at 7 of 8. Without it, the
"only" row of E8 would read 5 of 6, 3 of 6, 3 of 6. Whether the example helped
cannot be told from the data. Before E9 it is replaced by an example from no
evaluation domain.

---

## T8 — Events written as states, on development data (2026-11-18)

**Change (step 17).** Read prompt: something that happens gets an event symbol
also when the document counts it ("the fifth wrong password": the event, plus a
quantity for the count). Translation prompt: the symbol list marks the event
symbols, and a requirement that reacts to a happening has its event symbol in
the antecedent, also when a count says which time it is. Also: the read
prompt's restriction example moved from doors to lamps (D4).

**Setup.** `eval3/` (development data since D4), 72 runs as in E8 (T8). The
first wording of the translation sentence ended "also when a count or a state
is given as well"; it was then narrowed to counts and re-checked on helpdesk,
moderation, doors and the three development specs, 3 runs each (T8b).

| `eval3/` | E8 | T8 |
|---|---|---|
| Planted conflicts found | 15/21 | 13/21 |
| Clean runs with a false alarm, doubtful set aside | 1/18 | 0/18 |
| Unexpected conflicts, doubtful set aside | 25 | 2 |
| Unexpected conflicts, doubtful counted | 85 | 66 |
| Planted ambiguities: sampling only / default / 7 of 8 | 17 / 14 / 21 | 16 / 18 / 27 |
| Ambiguity flags on clean specs (default) | 6 | 5 |

**What it shows.**

1. **The event is there now.** Where the words describe a happening ("a
   comment receives its third report": clean, direct, ambiguity1), the read
   step made an event symbol in 9 of 9 runs (E8: 1 of 9), and the translation
   used it in 9 of 9 (E8: 0). The clashes with "a moderator approves" are now
   marked doubtful. The 2 left are in `moderation_ambiguity2`, "has been
   reported three times", worded as a state; a counter is a fair reading there.
2. **The first wording had a side effect.** "Also when ... a state is given"
   moved conditions into the antecedent: for "assign the ticket to an available
   agent", the reading `(and submitted agent_available) => assigned` rose from
   2 to 18 of 96 samples over the helpdesk specs, the rule scattered and was
   rejected in 2 of 3 `helpdesk_overlap` runs, and its planted conflict was
   lost. Narrowed to counts (T8b): `helpdesk_overlap` 3 of 3, moderation and
   doors as in T8, order 3 of 3 and login 3 of 3 for both conflicts.
3. **A regression found on the way, not caused by this step:
   `delete_property`.** D2/D4 is found in 2 of 4 (T8) and 1 of 3 (T8b) runs,
   against 8 of 8 in E5. The run saved before this step (E8-era prompts)
   already shows why: the read step now describes `property_deleted` as "the
   Property has been successfully deleted" (in E5: "the deletion process ...
   has been completed"), and D4 scatters. With that description the voted
   facts say, in 3 of 7 runs, that a deleted property is not retained; D4 then
   contradicts the facts on its own, and such a conflict is not reported (L8).
   The read-prompt changes of step 16 caused it; E8 could not show it, as it
   had no development specs.
4. **Ambiguity moved too** (default 14 → 18, at 7 of 8: 21 → 27). Development
   data only; the held-out run says more.

**Design frozen** after T8b, before E9 was started.

**Raw data.** `experiments/results/T8_eval3.json`, `T8_specs.json`, `T8b_subset.json`
(and `.md`).

---

## T9 — A second reader for ambiguity, on development data (2026-11-18)

**Change (step 18).** An optional formalize step 7: a second local model, of
another family, translates every rule 8 times with the prompt of step 2, and
Z3 compares each answer with the translation. The model is
`thelamapi/next-70b` (Llama architecture, 70B), which was already in the
cluster's model cache.

**Serving it took four starts.** Split over the two GPUs (tensor parallel),
NCCL failed ("unhandled cuda error"); one 8-bit copy per GPU then left too
little cache for an 8192-token window; an 8-bit cache needs bfloat16. What
works: 8-bit weights, 8-bit cache, bfloat16, a 6144-token window, one copy per
GPU (`experiments/slurm/serve_second.sbatch`). Its answers were added to the saved T8
runs (`eval3/`); 2803 of 2967 were usable formulas.

**Two rules for using it**, scored on the same runs:

| Rule | Planted ambiguities found: default / without step 6 / 7 of 8 | Flags on clean specs (default) | Other flags (default) |
|---|---|---|---|
| no second reader | 18 / 16 / 27 of 36 | 5 | 20 |
| ambiguous when the second model's majority reading differs | 20 / 16 / 27 | 9 | 30 |
| **ambiguous unless more than half of its answers mean the same** | **28 / 26 / 33** | 17 | 57 |

By kind, default, with the adopted rule: boundary 9 of 9, "if" 9 of 9, "only"
9 of 9, "and"/"or" 1 of 9 (without the second reader: 8, 3, 6, 1).

**Why the second rule.** On the planted ambiguous rules, the second model's 8
answers had no majority in 15 of 33 cases; on all other rules in 34 of 321.
It contradicted the translation outright in 6 of 33 and 17 of 321. Where the
words are ambiguous, the second model hesitates, and the first rule ignores
exactly that. The adopted rule is also the majority rule used for facts,
links and questions: the translation stands only if more than half of an
independent reader's answers mean the same. Its cost is many more flags.

**Design frozen** after T9, before any E9 score was read. E9's second-model
answers were collected with the code of the first rule; the judgement is
redone from the saved answers when they are scored.

**Raw data.** `experiments/results/T8_eval3.json` (now with the second model's
answers) and `.md`.

---

## E9 — The held-out set `eval4/` (2026-11-18)

**Setup.** 24 specs x 3 runs = 72 runs, one symbol set, with the frozen
designs of steps 17 (T8) and 18 (T9). 7 planted conflicts (21), 6 clean
specs (18 runs), 12 planted ambiguities (36). Qwen made the formal models;
the second model's answers were added afterwards (step 7, 8 per rule).

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags, clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|
| default, doubtful conflicts counted | 21/21 | 6/18 | 29 | 14/36 | 7 | 22 |
| **default, doubtful conflicts set aside** | **21/21** | **0/18** | **1** | 14/36 | 7 | 22 |
| without step 6 (sampling only) | 21/21 | 6/18 | 27 | 19/36 | 12 | 44 |
| translation needs 7 of 8 answers | 21/21 | 6/18 | 29 | 16/36 | 18 | 62 |
| **second reader** | 21/21 | 6/18 | 29 | **30/36** | 21 | 80 |
| second reader, without step 6 | 21/21 | 6/18 | 27 | 29/36 | 22 | 91 |
| second reader, 7 of 8 answers | 21/21 | 6/18 | 29 | 30/36 | 28 | 104 |
| without assumed facts and links | 18/21 | 1/18 | 8 | 14/36 | 7 | 22 |

Planted ambiguities found, by kind (9 each):

| Kind | Sampling only | Default | 7 of 8 | Second reader |
|---|---|---|---|---|
| boundary | 2 | 3 | 3 | 6 |
| "and" / "or" | 4 | 4 | 6 | 6 |
| "only" | 9 | 5 | 5 | 9 |
| "if" | 4 | 2 | 2 | 9 |
| all | 19 of 36 | 14 of 36 | 16 of 36 | 30 of 36 |

**What it shows.**

1. **Conflicts: 21 of 21, and no false alarm once doubtful conflicts are set
   aside** (1 unexpected conflict in 72 runs: a wrong voted fact in
   `printing_overlap`). The two-event mark went on 28 unexpected conflicts and
   on 2 "allowed" ones (a fair consequence of a planted ambiguity, which needs
   two events at once), never on a planted conflict.
2. **Counted events: half fixed.** The counted-event rule of each spec has an
   event symbol in 33 of 69 runs: always for "enters a wrong pickup code for
   the third time", "jams for the third time", "fails to deliver an order for
   the second time"; never for "the doors fail to close for the third time in
   a row", "the soil sensor fails to answer for the third time in a row", "is
   recorded as late for the third time" (each became a counter alone, e.g.
   `(= door_close_failure_count 3)`). No false alarm came of it here, because
   those rules clash with no other rule in these specs; the fix is not shown
   to work for failures and for things the system records.
3. **The second reader nearly doubles what is found: 14 → 30 of 36**, "if"
   2 → 9 and "only" 5 → 9 of 9, as on the development data (T9: 28 of 36). It
   holds without step 6 too (29 of 36). The price: flags on clean specs 7 → 21
   in 18 runs, other flags 22 → 80. Over all rules, it did not confirm the
   translation of 25 of 33 planted ambiguous rules and of 64 of 333 others.
4. **"7 of 8" does not hold up.** 27 of 36 on the development data (T8), 16 of
   36 here, with more flags. The second reader is the better way to buy
   recall.
5. **Step 6 still costs recall** (sampling only 19, default 14), as in E8,
   while it halves the flags. "And"/"or" stays the weakest kind with the second
   reader (6 of 9).

**Raw data.** [experiments/results/E9_eval4.json](experiments/results/E9_eval4.json) (with the
second model's answers), table [experiments/results/E9_eval4.md](experiments/results/E9_eval4.md).

---

## D5 — Decision: a fifth held-out set (2026-11-18)

E9 was read, so `eval4/` became development data. `eval5/` was written next,
before any change for steps 19 (`delete_property`) and 20 (failures as events)
was made or tried; the causes were known from T8 and E9. 6 new domains (cards,
messages, hotel, backup, oven, polls), 24 specs: 6 planted conflicts, 12
planted ambiguities (3 of each kind). Unlike `eval4/`, four clean specs have a
counted failure whose outcome clashes with another event's ("a PIN check fails
for the third time": block the card; "the cardholder unblocks the card":
unblock it), so a failure written as a counter shows as a false alarm. Two
planted conflicts are "remove" against "keep" (messages, backup), the pattern
of `delete_property`. Prompt examples written after this avoid its domains.

---

## T10, T11 — `delete_property` and failures as events, on development data (2026-11-18)

**Where `delete_property` was lost (T8 runs, traced).** The shortest proof of
a clash in the failing runs was "D4 against the facts", without D2: voted
facts such as "a deleted property has its record removed" with "a removed
record is not retained", or "a deleted property is not retained", make D4
impossible to obey wherever it applies, so every conflict of D4 falls under
the one-rule filter (L8). In E5 these runs had no voted facts at all. The
votes do not tell the facts apart (the right one tied the wrong one at 5 of 8).

**Tried and dropped, offline on all saved runs.**

| Change | `delete_property` | `eval3/` (E8 runs), doubtful set aside |
|---|---|---|
| none | 3 of 7 | 25 unexpected, 1 of 18 clean runs with a false alarm |
| the one-rule filter uses only the facts of the proof | 3 of 7 | 37, 3 of 18 |
| set aside the facts that make a rule impossible to obey | 4 of 7 | 34, 3 of 18 |

**Adopted.** (1) Check 3 (step 6): a voted fact that makes a requirement
impossible to obey is put to the LLM with the requirement's words, "agrees /
contradicts / unclear", and left out when more than half say "contradicts".
On the three saved failing runs it rejected the wrong fact each time it was
worded plainly (8 of 8 answers), recovered the conflict in one run, but also
rejected a right fact in another, and kept a hedged wrong fact ("... as an
active record") 6 to 2 in the third. (2) A link is kept even when the voted
facts imply it, so it survives when check 3 rejects one of them.

**Failures as events.** Naming "an attempt fails" as a happening in the read
prompt (T10, `eval4/`) gave the event in only 2 of 12 runs for "the doors fail
to close for the third time" and for the soil sensor. It also made the read
step mark "the property is deleted" as an event in 8 of 8 runs, so the D2/D4
conflict needed "two events" and was marked doubtful in all 8 (found in 8 of
8, but 0 of 8 once doubtful conflicts are set aside). Adopted instead (T11):
the read step names, for each rule, the event it reacts to (its trigger), and
a conflict is doubtful when its clashing rules react to two different events.
Formal models without triggers keep the old test.

| T11: 19 development specs x 3 runs | |
|---|---|
| counted happening has its event (elevator, irrigation, moderation) | 12 of 12 each (T10: 2, 2, —) |
| "is recorded as late for the third time" (attendance) | 5 of 12 |
| planted conflicts found, doubtful counted / set aside | 25 / 25 of 27 |
| unexpected conflicts, doubtful set aside | 0 |
| clean runs with a false alarm, doubtful set aside | 0 of 12 |
| `delete_property`, order, login | 3/3, 3/3, 2/3 and 3/3 |

The test first used the triggers of the rule group that found the situation;
D3 ("when the property is deleted, show a message") is in such a group and
reacts to "deleted", which marked D2/D4 again. It now uses the triggers of the
rules that clash.

**Design frozen** after T11, before E10.

**Raw data.** `experiments/results/T10_specs.json`, `T10_eval4.json`,
`T10_check3_cases.json`, `T11_subset.json` (and `.md`).

---

## E10 — The held-out set `eval5/` (2026-11-18)

**Setup.** 24 specs x 3 runs = 72 runs, one symbol set, the frozen designs of
T10/T11 (triggers, check 3, links kept). 6 planted conflicts (18), 6 clean
specs (18 runs), 12 planted ambiguities (36). No second reader.

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags, clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|
| default, doubtful conflicts counted | 14/18 | 11/18 | 41 | 15/36 | 0 | 7 |
| **default, doubtful conflicts set aside** | **11/18** | **0/18** | **0** | 15/36 | 0 | 7 |
| without step 6 (sampling only) | 14/18 | 15/18 | 61 | 20/36 | 2 | 19 |
| translation needs 7 of 8 answers | 14/18 | 11/18 | 41 | 20/36 | 9 | 33 |
| without assumed facts and links | 6/18 | 0/18 | 0 | 15/36 | 0 | 7 |

**What it shows.**

1. **Counted failures are events now: 72 of 72 runs.** In every spec, the
   counted-happening rule has an event symbol in its translation and as its
   trigger (E9: 33 of 69). Their clashes with another event (block / unblock
   a card, unprotected / protected, publish / hide results, stop / retry)
   are all marked: with doubtful conflicts set aside, 0 unexpected conflicts
   and 0 of 18 clean runs with a false alarm (41 and 11 of 18 counted).
2. **A new error: a state read as an event.** "WHEN a member is suspended THEN
   the system counts no vote of the member" got the trigger `member_suspended`
   in 3 of 3 runs, so the planted conflict with "WHEN a member casts a vote"
   needed "two events" and was marked doubtful. It is found when doubtful
   conflicts are counted (14 of 18), lost when they are set aside (11 of 18).
   The first planted conflict ever marked by the two-event test.
3. **"Remove" against "keep" was missed in `messages` (0 of 3).** "WHEN a
   member deletes a message THEN the system removes the message" against "the
   system keeps every message in the archive for five years": the link step
   restated "removes" as "not delivered", not as "not in the archive"; check 2
   rejected that link, and nothing else connects the two symbols. The same
   pattern in `backup` ("deletes the copy" against "keeps every backup copy")
   was found in 3 of 3.
4. **Check 3 never fired:** no voted facts made a requirement impossible to
   obey in these specs. Its effect is shown only on `delete_property` (T10).
5. **Ambiguity: as before** (15 of 36 by default, 20 by sampling only), with
   few flags on clean specs (0 by default).

**Raw data.** [experiments/results/E10_eval5.json](experiments/results/E10_eval5.json), table
[experiments/results/E10_eval5.md](experiments/results/E10_eval5.md).

---

## D6 — Decision: a sixth held-out set, and no new machinery for "remove" (2026-11-19)

**A sixth set.** E10 was read, so `eval5/` became development data. `eval6/`
was written next, before the change for step 21 (states read as events) was
made; its cause was known from E10. 6 new domains (charging, bikes, tickets,
warehouse, auctions, carwash), 24 specs, 6 planted conflicts, 12 planted
ambiguities (3 of each kind). Four planted conflicts pair a rule whose WHEN
part is a state ("WHEN the station is out of order", "WHEN the outside
temperature is below zero") with a rule that reacts to an event, so a state
read as an event shows as a planted conflict marked doubtful. One is "remove"
against "keep" again (auctions: "delete the listing" against "keep every
listing for seven years").

**No change for step 22.** In `messages_direct` (E10) the link step read
"removes the message" as "no longer delivered" (up to 7 of 8 answers), never
as "not in the archive". That is a reading the words allow: a chat can remove
a message from the channel and keep it in an archive. The Kiro blog asks the
author the same question about "remove the record". A repair would need more
LLM steps for a case where the words themselves are open, so it is left as a
known limit, and measured again in E11.

---

## T12 — A state written after WHEN, on development data (2026-11-19, dropped)

**Change tried.** Two sentences in the read prompt: a rule that reacts to a
state has no trigger "also when the document writes it after WHEN ("WHEN the
lamp is lit": the rule holds as long as the lamp is lit)", and "the lamp is
lit is a state, the lamp is switched on an event".

**Result** (`eval5/`, 72 runs; development specs, 12 runs). "WHEN a member is
suspended THEN the system counts no vote of the member" still got the trigger
`member_suspended` in 3 of 3 runs, so the planted conflict stayed marked
doubtful. Nothing else moved: counted failures kept their event in 72 of 72
runs; the development specs found 20 of 20 expected conflicts, none marked.

**Decision.** Dropped, and the prompt is back to the one of E10. "Is
suspended" can be read as the moment it happens as well as the state; a
further prompt change would be guessing. The conflict is still reported, with
the "doubtful" mark. E11 runs the design of E10 unchanged, on `eval6/`.

**Raw data.** `experiments/results/T12_specs.json`, `T12_eval5.json` (and `.md`).

---

## E11 — The held-out set `eval6/` (2026-11-19)

**Setup.** 24 specs x 3 runs = 72 runs, one symbol set, the design of E10
unchanged (T12 was dropped). 6 planted conflicts (18), 6 clean specs (18
runs), 12 planted ambiguities (36).

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags, clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|
| default, doubtful conflicts counted | 15/18 | 8/18 | 25 | 19/36 | 2 | 14 |
| **default, doubtful conflicts set aside** | **15/18** | **0/18** | **0** | 19/36 | 2 | 14 |
| without step 6 (sampling only) | 15/18 | 9/18 | 33 | 16/36 | 5 | 22 |
| translation needs 7 of 8 answers | 15/18 | 8/18 | 25 | 30/36 | 12 | 43 |
| without assumed facts and links | 12/18 | 0/18 | 0 | 19/36 | 2 | 14 |

**What it shows.**

1. **States after WHEN are read as states.** The four planted conflicts that
   pair "WHEN the station is out of order", "WHEN the venue is at full
   capacity", "WHEN the warehouse is closed for a holiday", "WHEN the outside
   temperature is below zero" with an event got no trigger in 12 of 12 runs,
   and were found, unmarked, in 12 of 12. "WHEN a member is suspended" (E10)
   was the exception, not the rule.
2. **No false alarm once doubtful conflicts are set aside** (8 of 18 clean runs
   counted), and no planted conflict marked.
3. **All three misses are "remove" against "keep" again** (`auctions_direct`,
   0 of 3), for a second reason: "keep every listing for seven years" became
   a setting, `(= listing_retention_years 7)`, not a fact about the listing,
   and "delete the listing" could not be restated against it ("cannot be
   expressed" in 7 to 8 of 8 answers). In E10 the link took another reading of
   "remove"; here there was nothing to link to. Both come from the choice of
   symbols.

**Raw data.** [experiments/results/E11_eval6.json](experiments/results/E11_eval6.json), table
[experiments/results/E11_eval6.md](experiments/results/E11_eval6.md).

---

## D7 — Decision: a seventh held-out set (2026-11-19)

E11 was read, so `eval6/` became development data. `eval7/` was written next,
before the changes for steps 23 ("remove" against "keep") and 24 (fewer flags
from the second reader) were made; their causes were known from E10, E11 and
the saved second-reader runs. 6 new domains (photos, taxi, lab, canteen,
skipass, fleet), 24 specs, 6 planted conflicts, 12 planted ambiguities (3 of
each kind). Three planted conflicts are "remove" against "keep", each worded
differently ("erases the photo" / "keep every photo for two years", "disposes
of the sample" / "keep every tested sample in the freezer for ten years",
"deletes the pass" / "keep every pass for the whole season"). Two clean specs
remove one thing and keep another ("erases the photo" / "keeps the upload log
entry for one year"), which must not clash.

---

## T13 — Fewer flags from the second reader, offline (2026-11-19)

**What the flags on clean specs are.** Of the second reader's flags on clean
specs (T9 on `eval3/`, E9 on `eval4/`), about a third are not readings of the
words but a modelling detail: the two models differ only in whether the
event is written into the rule.

```
"WHEN a courier fails to deliver an order for the second time THEN ..."
main model     (and delivery_failed (= failed_delivery_count 2)) => ...
second model   (= failed_delivery_count 2) => ...
```

**Change (step 24).** The second model's answer is compared with the
translation only in the situations where the events that the translation's
condition requires (its antecedent implies them) happen. The two above then
mean the same. A first version assumed every event named in the condition,
also a negated one ("has **not** scanned the card"), and lost a planted
ambiguity; it was corrected before the numbers below.

| Saved runs, second reader on | Planted ambiguities found | Flags on clean specs | Other flags |
|---|---|---|---|
| `eval3/` (T9), before → after | 28 → 28 of 36 | 17 → 13 | 57 → 45 |
| `eval4/` (E9), before → after | 30 → 30 of 36 | 21 → 15 | 80 → 59 |

A lower threshold instead (flag when at most k of 8 answers confirm) only
trades one for the other: on `eval4/`, k = 2 gives 26 of 36 with 15 clean
flags, k = 4 (the rule) 30 with 21.

---

## T14 — "Remove" against "keep", on development data (2026-11-19, dropped)

**Change tried (step 23).** One read-prompt sentence: removing something and
keeping it are opposites about one fact ("delete the email" and "keep every
email for a year" are both about email_stored, plus the email's age).

**Result** (`messages_direct`, `backup_overlap`, `auctions_direct`, their
clean versions, and the development specs; 3 runs each). Still 0 of 3 for
messages and auctions, 3 of 3 for backup, as before. The keep rule was now
written as a stored state with an age, but its 8 translations scattered
(`(< listing_age_years 7) => listing_stored`, `(>= listing_age_years 7) =>
listing_stored`, `true => (and listing_stored ...)`), so it was rejected and
left out of the checks in 6 of 6 runs; the remove rule kept its own symbol
(`listing_deleted`, `message_removed`). No false alarm on the clean versions.

**Decision.** Dropped; the prompt is back to the one of E11. A repair would
have the LLM judge pairs of requirements against each other, which is the
review stage this project leaves out (D1). "Remove" against "keep" stays a
known limit, measured again in E12.

**Raw data.** `experiments/results/T14_subset.json` (and `.md`).

---

## E12 — The held-out set `eval7/` (2026-11-19)

**Setup.** 24 specs x 3 runs = 72 runs, one symbol set. Qwen's prompts as in
E11 (T14 dropped); the second reader's comparison of T13; the second model's
answers added afterwards. 6 planted conflicts (18), 6 clean specs (18 runs),
12 planted ambiguities (36).

| Configuration | Planted conflicts found | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags, clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|
| default, doubtful conflicts counted | 13/18 | 0/18 | 3 | 17/36 | 5 | 27 |
| **default, doubtful conflicts set aside** | **13/18** | **0/18** | **1** | 17/36 | 5 | 27 |
| without step 6 (sampling only) | 13/18 | 0/18 | 10 | 19/36 | 3 | 14 |
| translation needs 7 of 8 answers | 13/18 | 0/18 | 3 | 26/36 | 8 | 40 |
| **second reader** | 13/18 | 0/18 | 3 | **32/36** | 9 | 40 |
| second reader, 7 of 8 answers | 13/18 | 0/18 | 3 | 33/36 | 12 | 53 |
| without assumed facts and links | 3/18 | 0/18 | 0 | 17/36 | 5 | 27 |

By kind, default → second reader: boundary 6 → 9, "and"/"or" 2 → 5, "if" 1 → 9,
"only" 8 → 9 (of 9).

**What it shows.**

1. **"Remove" against "keep": 7 of 9.** Found in `lab` ("disposes of the
   sample" / "keep every tested sample in the freezer") and `skipass`
   ("deletes the pass" / "keep every pass for the whole season") in 3 of 3,
   in `photos` in 1 of 3, where "keep every photo for two years" became a
   setting, `(= photo_retention_years 2)`, as in E11.
2. **The other miss is two unlinked symbols** (`canteen_overlap`, 0 of 3):
   "take the price" (`payment_taken`) against "refuse all payments"
   (`payment_refused`), with no fact or link saying they exclude each other.
3. **No false alarm on clean specs**, also with doubtful conflicts counted;
   the two clean specs that remove one thing and keep another stayed clean.
   Facts and links carry the result: without them, 3 of 18.
4. **The second reader: 17 → 32 of 36**, "if" 1 → 9, with 9 flags on clean
   specs (5 without it). The comparison of T13 changed nothing here: scored
   with the old comparison, the same 32 of 36 and 9 flags. The pattern it
   removes (the event left out of a counted happening) does not occur in
   these specs.

**Raw data.** [experiments/results/E12_eval7.json](experiments/results/E12_eval7.json) (with
the second model's answers), table [experiments/results/E12_eval7.md](experiments/results/E12_eval7.md).

---

## T15 — Findings that depend on the reading of an ambiguous rule, offline (2026-11-20)

**What the report did not say.** An ambiguous rule is reported as a question to
the author, but the checks go on with its first reading, and the conflicts
and gaps found with it did not mention that. Example, `specs/auth_openspec`:

```
R3          "WHEN the number of failed attempts on an account reaches 5 THEN the system locks the account"
reading 1   (= failed_attempts_count 5)     used by the checks (1 of 7 answers of step 6)
reading 2   (>= failed_attempts_count 5)    6 of 7 answers
gaps        failed_attempts_count = 6, 7, 8 with no password submitted
            with reading 2, R3 applies in all three: they are gaps of reading 1 only
```

**Change (step 25).** After the checks, each ambiguous rule is tried once more
with its other reading, one rule at a time, the other rules as they are
(`checks._try_other_readings`, Z3 only). A conflict that is not found then,
and a gap in which a rule then applies, get `depends_on_reading`. The
ambiguity gets `other_reading`: the conflicts that are gone, the conflicts
that appear, the number of gaps covered. Ambiguities that change another
finding are listed first; the others say "changes no conflict and no gap".
Nothing is removed, no finding is added, no prompt was changed.

**Check.** What is found cannot change, so no held-out set is needed. E3 and
E7 to E12 were scored with the code before and after: the same tables, apart
from the new one below. 39 tests, 3 of them new.

**How often does the other reading matter?** Default configuration, first
symbol set, flags with two readings (a rejected rule has none). Each flag is
counted once, under the strongest change:

| Saved runs | Flags | Changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| `eval2/` (E7) | 65 | 7 | 19 | 39 |
| `eval3/` (E8) | 24 | 2 | 3 | 19 |
| `eval4/` (E9) | 24 | 1 | 8 | 15 |
| `eval5/` (E10) | 18 | 0 | 8 | 10 |
| `eval6/` (E11) | 24 | 1 | 8 | 15 |
| `eval7/` (E12) | 31 | 4 | 2 | 25 |
| all | 186 | 15 | 48 | 123 |

| Flags on | Flags | Changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| rules with a planted ambiguity | 71 | 1 | 17 | 53 |
| other rules | 115 | 14 | 31 | 70 |

- One flag in three (63 of 186) changes another finding. For the other two
  thirds the report now says that the choice changes nothing.
- 15 flags change a conflict, 14 of them on rules where nothing was planted.
  Such flags count as the price of ambiguity detection (research.md 4.1);
  in these 14 the question decides whether a conflict exists.
- A planted ambiguity almost never changes a conflict (1 of 71): the planted
  versions reword one rule and plant no conflict.

**Limits.** One rule at a time: a finding that needs the other reading of two
rules is not seen. The wording prompt of stage 3 is unchanged; the title and
the *Proven* lines carry the mark, and the model is given those lines, but
whether its paragraph mentions the mark was not checked (no run with the LLM).

**Three measurements made on the way.** They were made with one-off scripts on
the saved runs, to see where the project could improve. The first two can be
read off the saved tables; the scripts are not in the repository.

- *Runs of one spec mostly agree.* The "By spec" tables of E5 and E7 to E12
  (default configuration) hold 60 planted conflicts, each with 3 runs: 46 were
  found in all 3 runs, 7 in 2, 1 in 1, 6 in none. So the unit that varies is
  the planted conflict, not the run: "13 of 18" is 6 conflicts, 3 runs each.
- *Every gap on `eval7/` is "nothing is happening".* 140 gaps in 72 runs
  (first symbol set), at least one in every run, and in none of them an event
  symbol is true. Asking for gaps in which an event happens gives a gap in 6
  of the 18 clean runs (for example in `skipass`: a pass used at a second gate
  five minutes or more after the first).
- *The solver stage grows fast with the number of rules.* On k independent
  copies of the order spec's formal model: 5 rules 0.1 s, 10 rules 0.4 s, 20
  rules 4.8 s, 30 rules 24 s, 40 rules 60 s. All specs so far have 5 to 8 rules.

**Raw data.** The tables of E7 to E12 in `experiments/results/` were written
again with today's `evaluate.py` and now hold the table above for their set
(`python -m experiments.evaluate --rescore experiments/results/E12_eval7.json`).
Their counts did not change; those of E7 and E8 also show the rows and labels
that were added to `evaluate.py` after they were first written.

---

## D8 — Decision: an eighth set with planted gaps, a long spec, and step 26 (2026-11-20)

All seven sets have been read, and T15 showed two things to change: the gaps
say nothing (all 140 on `eval7/` are "nothing is happening"), and the solver
stage slows down fast with the number of rules. The order of work:

**1. The sets were written first** (commit `5b4ad6a`, before any code of step 26).

- `eval8/`: six new domains (recycling, tolls, laundry, clinic, donations,
  meters), each clean, with one planted conflict (7 in all), two planted
  ambiguities (12 in all, 3 of each kind), and, new, a *gap* version: one of
  two complementary requirements is removed ("... AND the barcode is not on
  the deposit list" goes, "... AND the barcode is on the deposit list" stays).
- `size/`: one spec of 30 requirements (campsite), clean, with a planted
  conflict of each kind and a gap version. It is not part of the `eval8/` numbers.

**2. Then step 26, frozen with this entry, before any run on the new sets.**

- *Gaps once for each event.* For every event some rule reacts to (its
  trigger, or an event in its condition): is there a situation in which this
  event happens, no other event does, and no rule applies? At most one gap
  for each event, then one gap in which no event happens, marked. Without
  events to go by, the search is as before (plan.md 5.4).
- *Conflicts only among rules that share symbols*, directly or through other
  rules and the facts (`checks._families`). Rules without a common symbol
  cannot contradict each other.
- *The read step may answer with 8192 tokens* instead of 4096: it copies every
  requirement, so its answer grows with the document.

No prompt was changed.

**3. How a planted gap is scored, fixed before the run** (`evaluate.gap_scores`).
A planted gap names the requirement whose other case was removed. It is found
in a run when a reported gap is a situation in which the event of that
requirement happens (the trigger the read step named, or an event in its
condition). The same test on a clean spec, for the requirements whose two
cases are both there, counts a false alarm. Both searches, the old one and the
new one, are scored on the same runs.

**Checks on development data** (no LLM):

- The conflicts did not change: 1054 conflicts in the saved models of E5 and
  E7 to E12 (each model checked three ways: as it is, without facts, with
  pairs of rules only) have the same rules, the same marks and the same order
  before and after. In 10 of them another, equally valid set of facts is
  named, in 1 another example situation: Z3 returns a different proof when the
  questions before it differ.
- Gaps on the clean specs of `eval7/` (18 runs): 29 before, none with an
  event; 24 after, 6 with an event.
- Solver stage on k unrelated copies of the order spec: 40 rules 60 s before,
  2.3 s after; 80 rules 12.5 s. A document about one subject is one family,
  so there nothing is saved: the `size/` spec will show what that costs.
- 42 tests, 3 of them new.

---

## E13 — The held-out set `eval8/`, and the 30-requirement spec (2026-11-20)

**Setup.** The design of step 26, frozen in D8 (commit `78f107d`). `eval8/`: 30
spec versions, 3 runs each, 1 symbol set: 90 runs, none failed. `size/`: 4
versions of one 30-requirement spec, 3 runs each: 12 runs, none failed. One
server job of 31 minutes (the 90 runs took 16 minutes, the 12 long ones
together with T16 below 13 minutes). No second reader in this session.

### `eval8/`

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Flags on clean specs | Other flags |
|---|---|---|---|---|---|---|---|---|
| default | 18/21 | 6/9 | 12/12 | 4/18 | 37 | 20/36 | 3 | 11 |
| doubtful conflicts set aside | 18/21 | 6/9 | 12/12 | 0/18 | 0 | 20/36 | 3 | 11 |
| without step 6 | 18/21 | 6/9 | 12/12 | 8/18 | 56 | 13/36 | 4 | 20 |
| translation needs 7 of 8 answers | 18/21 | 6/9 | 12/12 | 4/18 | 37 | 23/36 | 9 | 40 |
| without assumed facts and links | 9/21 | 3/9 | 6/12 | 1/18 | 7 | 20/36 | 3 | 11 |

**Conflicts.** 18 of 21, and with doubtful conflicts set aside not one
unexpected conflict in 90 runs. All 37 unexpected conflicts were marked
doubtful (in `tolls`, "open the barrier" when a driver pays against "close the
barrier" when a vehicle leaves: two events). The one planted conflict that was
missed, in 3 of 3 runs, is the "remove" against "keep" of this set:

```
C3   "WHEN a patient cancels an appointment, ... SHALL delete the appointment and free the slot."
     appointment_cancelled => (and appointment_deleted slot_freed)              accepted
C6   "THE Clinic System SHALL keep every appointment in the patient's record for five years."
     (< years_since_appointment 5) => appointment_record_retained               run 1
     true => (and appointment_in_record (<= years_since_appointment 5))         run 2
     true => (=> (< years_since_appointment 5) appointment_in_record)           run 3
     rejected in all three runs: its 8 translations scatter over what "for five years" is
```

C6 is reported, as a rule that has to be rewritten, but it takes no part in
the conflict search. "Remove" against "keep" is now found in 10 of 21 runs
(E10 to E13).

**Ambiguities.** 20 of 36 with 3 flags on clean specs. By kind: "if" 8 of 9,
"only" 8 of 9, "and"/"or" 3 of 9, a boundary 1 of 9 ("is 90 percent full",
"one hour before the slot starts", "has been unpaid for 30 days": the model
reads all three one way).

| | and/or | boundary | if | only |
|---|---|---|---|---|
| default | 3/9 | 1/9 | 8/9 | 8/9 |
| without step 6 (sampling only) | 0/9 | 2/9 | 2/9 | 9/9 |
| translation needs 7 of 8 answers | 5/9 | 1/9 | 9/9 | 8/9 |

**Gaps: the first numbers.** Both searches were scored on the same 90 runs:

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 52 |
| once for each event | 18/18 | 4/18 | 25 | 43 |

- The search over all situations finds none of the planted gaps: its three
  gaps are variations of "nothing is happening". Asked once for each event,
  all 18 are found.
- The 4 false alarms have one cause, the one that also gives doubtful
  conflicts: two symbols for complementary conditions. In `laundry` (3 of 3
  runs) "the slot is free" and "the slot is taken" became `slot_is_free` and
  `slot_is_taken`, and the gap is "a resident books a slot that is neither
  free nor taken"; in `donations` (1 of 3) the same with "the payment
  succeeds" and "the payment fails".
- The other 21 gaps with an event on clean specs are cases the specs really
  leave open. 12 are counted events ("a card payment is declined, and it is
  not the third time"). 3 are "the first day of a month begins, and the
  supporter has no monthly donation". 6 are cases a reviewer would ask about,
  which we had left out without noticing: cancelling a booking one hour or
  less before the slot (`laundry`), and scanning a voucher that was already
  used (`recycling`).

**Ambiguity flags and the other reading** (T15's table on this set): of 20
flags with two readings, none changes a conflict, 11 a gap (10 of them on
planted rules), 9 nothing. More flags change a gap than in T15, because gaps
with an event exist now.

### `size/`: one spec of 30 requirements

| | Result |
|---|---|
| read step | all 12 runs list the right number of requirements (30, 31 or 29), with 66 to 69 symbols, 18 of them events |
| planted conflicts | 6 of 6: the direct one from the rules alone, the overlap with an assumed fact |
| clean spec | no conflict in 3 of 3 runs with doubtful ones set aside (one doubtful conflict in each run) |
| planted gap | 3 of 3 (0 of 3 with the search over all situations) |
| gaps on the clean spec | only the one with no event (9 gaps with the old search) |
| ambiguity flags on the clean spec | 7 in 3 runs, rejected rules included |
| solver stage, for one model | 26 to 34 s with the code before step 26, 0.4 to 0.9 s after |

The speed-up was not expected for one document about one subject. The 30
requirements fall into 16 to 18 families: booking, the barrier, the power
posts, the showers and the bill hardly share a symbol. One spec in one domain
is thin evidence; a document whose rules all meet in a few symbols would
still take the 30 seconds.

### T16: the development specs, 3 runs each

`order`: both conflicts in 3 of 3. `delete_property`: the blog's conflict in 3
of 3. `auth_openspec`: 3 of 3 and 2 of 3. No unexpected conflict with doubtful
ones set aside.

### The wording of the new marks

The three saved formal models in `specs/` were worded again with the current
checks (two server jobs of two minutes each), and the reports in `specs/` are
now these.

- *"No event happens."* The title says "Gap (no event happens)", and the model
  writes the gap as before ("... when no order has been submitted, canceled,
  or refunded").
- *"Depends on the reading of R3"*, first try. The fact sheet said only "R3 is
  ambiguous, and with its other reading a requirement applies". The model
  mentioned the dependence but made up what the two readings are ("whether
  the lock is a one-time event or a persistent state").
- *Second try.* The fact sheet now quotes the other reading
  (`depends_on_reading` holds it for each rule). The model then names both
  readings correctly ("exactly 5" and "at least 5"). But it wrote the gap as
  if it were the ambiguity: the title became "Ambiguous Locking Threshold"
  and the paragraph ends with "Which did you mean?", which the prompt allows
  for ambiguities only.

One report, one sample. The wording prompt was not changed; a sentence for
this case is the obvious next thing to try, on the development specs.

**Raw data.** [experiments/results/E13_eval8.json](experiments/results/E13_eval8.json),
[E13_size.json](experiments/results/E13_size.json),
[T16_specs.json](experiments/results/T16_specs.json), each with its table (`.md`).
`eval8/` and `size/` have now been read: they are development data. The tables
of E7 to E12 were written again and now hold the gap table for their set; in
all of `eval3/` to `eval7/` the search over all situations returned no gap
with an event. T15's table in them now counts the gaps of the new search, so
a few flags moved from "nothing" to "only a gap".

---

## E14 — One spec of 100 requirements, with a longer read answer (2026-11-22)

**Question.** The read step copies every requirement and lists every symbol,
so its answer grows with the document. For 30 requirements it was 4,000 to
5,000 tokens, against a limit of 8192. Does a document of 100 requirements fit
with a higher limit, and what happens to the findings and the time?

**Setup.** `size2/` was written first (commit `6f4e350`): a ferry line of 100
requirements in four versions, clean, direct, overlap and gap; 20 events have
both of their cases written ("covered"). Then the design of step 27 (commit
`00b253c`): the read answer may have 24576 tokens instead of 8192, and the LLM
client waits up to 30 minutes instead of 10. Nothing else changed since E13.
3 runs per version, 1 symbol set: 12 runs, none failed. Two servers with the
same model, vLLM 0.31.0 and flags: a cluster job with 2 GPUs (clean, direct)
and the workstation's GPUs 0 and 1 (overlap, gap). A second cluster job stayed
pending with `QOSGrpGRES`: the account may hold 2 GPUs at a time. The two
halves took 29 and 40 minutes; T17 ran on the workstation server from minute 12.

**The read answer.** A probe asked the read step for `ferry_clean` at
temperature 0, once with each limit:

| Limit | Finished | Answer tokens | Characters | Time |
|---|---|---|---|---|
| 8192 | no: cut off at the limit | 8192 | 28,999 | 141 s |
| 24576 | yes | 16,799 | 58,906 | 1,501 s |

- The prompt is 3,765 tokens, so prompt and answer take 20,564 of the server's
  32,768. The answer is about 170 tokens per requirement, more than the 150
  estimated from 30 requirements: the limit of 24576 holds about 140
  requirements, and the window about 150.
- With the old limit, every run on this spec fails: the answer is not valid
  JSON. With the new one, all 12 runs listed the right number of requirements
  (100, 101 or 99), with 203 to 207 symbols, 66 of them events.
- The long call took 25 minutes because the server was busy (E14's other half
  and T17): about 11 tokens a second, against 58 for the first call. The old
  client timeout of 10 minutes would have cut it and sent it again.

**Results.**

| | Result |
|---|---|
| planted conflicts | 6 of 6 (direct 3 of 3, overlap 3 of 3); without assumed facts and links 3 of 6 (overlap 0 of 3) |
| clean spec | a false alarm in 1 of 3 runs, not marked doubtful; the same conflict in 1 run of `ferry_direct` |
| planted gap | 3 of 3 (0 of 3 with the search over all situations) |
| gaps on the 20 covered events of the clean spec | none in 3 runs |
| other gaps with an event on the clean spec | 12 in 3 runs, cases the spec does leave open |
| rejected rules | F21 in 12 of 12 runs; 0 to 1 other rule per run |
| ambiguity flags | 4 on the clean spec in 3 runs, 24 on the other versions |
| solver stage, one model of 101 rules | 35 s (under 1 s for 30 requirements) |
| one full CLI run with the wording (`ferry_direct`) | 620 s, on the busy cluster server |

- *The false alarm.* F1 "WHEN a passenger requests a crossing AND seats are
  available ... reserve a seat" against F4 "WHEN a reserved seat has been
  unpaid for more than 30 minutes ... release the seat", with the assumed fact
  that a seat is not reserved and released at once. F4 was read as a state,
  with no trigger, so the two-event mark did not apply. With one snapshot and
  one `seat_reserved` for every seat, a new booking and an old unpaid one are
  the same seat: an artefact of time and of identity, not a defect.
- *F21 is rejected in every run.* "WHEN a booked vehicle has not checked in 30
  minutes before departure" scattered over `(<= minutes_before_departure 30)`,
  `(= ... 30)` and `(>= ... 30)`. The sentence is unclear (we wrote it), and
  the tool asks for it to be rewritten.
- *Other gaps.* "A customer enters a wrong password for the fourth time", "a
  group booking of 10 or fewer is paid", "a passenger without assistance or
  priority boarding arrives at the terminal": cases we left open.

**What does not scale yet.**

- *The second reader.* A translation prompt with the 206 symbols has 4,234
  tokens. The second model's server allows 6,144 for prompt and answer, and
  the answer may take 4,096, so every request would be refused. The answers
  themselves are about 60 tokens (61 in the probe): a lower answer limit for
  translations would make room.
- *The report.* A gap lists every other event as FALSE: about 70 lines per gap
  at this size, which buries the few facts that matter.
- *The solver stage* grows from under 1 s to 35 s for one model, and scoring
  the 12 runs under all configurations of `evaluate.py` took more than 10
  minutes on the laptop.

**Raw data.** [experiments/results/E14_size2.json](experiments/results/E14_size2.json)
(both halves in one file; `servers` says which ran where) and its table,
[E14_read_probe.json](experiments/results/E14_read_probe.json), and the full
CLI run in [experiments/examples/size2_ferry_direct](experiments/examples/size2_ferry_direct).

---

## T17 — The temperature of the samples: 0.3, 0.5 and 0.7 (2026-11-22)

**Question.** Every sample of the pipeline is drawn at 0.7: the 8
translations of a rule, the 8 fact lists, the 8 restatements of a link, the 8
answers to each question. 0.7 was only ever compared with 1.0 (E1). Is a
lower value better?

**Setup.** `eval8/` (development data), 3 runs per version, 1 symbol set, 90
runs per temperature, none failed; `evaluate.py --temperature` (commit
`52eefe3`). The read step stays at temperature 0, so the symbols are drawn as
before. 0.5 and then 0.7 ran on the workstation server, 0.3 on a new cluster
job, all on the same day and with the same model and flags. E13 (two days
earlier, the same design for specs of this size) is a second run at 0.7, which
shows how much two runs at the same temperature differ. During T17 the middle
retry temperature of the read step went from 0.5 to 0.3; a retry only happens
when the first read fails, which T18 found for 0 of 204 specs.

| Temperature | Planted conflicts | Clean runs with a false alarm (doubtful set aside) | Unexpected conflicts (all doubtful) | Planted ambiguities | Flags on clean specs | Other flags | Planted gaps | False gaps on covered events |
|---|---|---|---|---|---|---|---|---|
| 0.3 | 18/21 | 0/18 | 40 | 13/36 | 2 | 15 | 18/18 | 5/18 |
| 0.5 | 18/21 | 0/18 | 41 | 14/36 | 3 | 15 | 18/18 | 3/18 |
| 0.7 | 18/21 | 0/18 | 37 | 14/36 | 4 | 18 | 18/18 | 4/18 |
| 0.7 (E13) | 18/21 | 0/18 | 37 | 20/36 | 3 | 11 | 18/18 | 4/18 |

The ablations, planted ambiguities found (flags on clean specs, other flags):

| Temperature | default | sampling only (without step 6) | translation needs 7 of 8 answers | without assumed facts and links: conflicts |
|---|---|---|---|---|
| 0.3 | 13/36 (2, 15) | 11/36 (1, 10) | 18/36 (5, 31) | 9/21 |
| 0.5 | 14/36 (3, 15) | 13/36 (3, 16) | 19/36 (4, 29) | 9/21 |
| 0.7 | 14/36 (4, 18) | 15/36 (3, 21) | 25/36 (13, 42) | 9/21 |
| 0.7 (E13) | 20/36 (3, 11) | 13/36 (4, 20) | 23/36 (9, 40) | 9/21 |

Planted ambiguities by kind, default configuration:

| Temperature | and/or | boundary | if | only |
|---|---|---|---|---|
| 0.3 | 1/9 | 1/9 | 8/9 | 3/9 |
| 0.5 | 1/9 | 0/9 | 7/9 | 6/9 |
| 0.7 | 0/9 | 1/9 | 5/9 | 8/9 |
| 0.7 (E13) | 3/9 | 1/9 | 8/9 | 8/9 |

**What it shows.**

1. *Conflicts and gaps do not depend on the temperature* between 0.3 and 0.7:
   18 of 21 planted conflicts, 18 of 18 planted gaps and no false alarm with
   doubtful ones set aside, at every value. As in E1, the symbols decide the
   conflicts, and they come from the read step at temperature 0. The facts and
   links matter as much at 0.3 as at 0.7 (9 of 21 without them, everywhere).
2. *For ambiguities, two runs at 0.7 differ more than the temperatures do:* 14
   and 20 of 36. Only two trends are larger than that noise. Ambiguities of
   "only" fall from 8 of 9 (both runs at 0.7) to 6 at 0.5 and 3 at 0.3: these
   are found when the 8 translations split, and at a low temperature they
   split less. With "translation needs 7 of 8 answers" the finds are 23 and
   25 at 0.7, 19 at 0.5 and 18 at 0.3, with fewer flags elsewhere (40 and 42
   against 29 and 31): the same trade of finds for flags as always.
3. *Flags on clean specs* are 2, 3 and 4 in 18 runs: fewer at 0.3, but by one
   or two flags, within the noise.

**Decision.** The temperature stays 0.7. A lower one gains nothing measurable
for conflicts, gaps or false alarms, and loses the ambiguities of "only".
Nothing is adopted, so no held-out set is needed.

**Raw data.** [experiments/results/T17_eval8_t03.json](experiments/results/T17_eval8_t03.json),
[T17_eval8_t05.json](experiments/results/T17_eval8_t05.json),
[T17_eval8_t07.json](experiments/results/T17_eval8_t07.json), each with its table.

---

## T18 — How often is the first read answer unusable? (2026-11-22, probe)

**Question.** The read step asks at temperature 0 and, if the answer is
unusable, asks again at 0.5 and then 0.9. The values date from the first
commit and were never measured. Are they ever used?

**Setup.** Every version of `eval/` to `eval8/` and the three development
specs, 204 in all, read once at temperature 0 on the cluster server. For an
unusable answer (no valid JSON, or symbols that `Vocabulary` refuses), 8 more
answers at 0.2, 0.3, 0.5 and 0.9 would be counted.

**Result.** The first answer was usable for all 204 specs, so no retry was
needed and the retry temperatures change nothing measured so far. The middle
one was set to 0.3 afterwards (a little more variety first, then a lot); no
experiment can show a difference. The retry may still matter for the extra
symbol sets, whose read step runs at 0.7, and for answers cut off at the limit.

**Raw data.** [experiments/results/T18_read_retries.json](experiments/results/T18_read_retries.json).

---

## T19 — How often is a sampled fact dropped before the vote? (2026-11-22, probe)

**Question.** The facts question (step 4) sees only the symbol list. A fact
whose formula does not parse, for example because it names a symbol that is
not in the list, is dropped silently before the vote. How often does that
happen, and does it change which facts are kept?

**Setup.** Every saved run from E4 to E14 (1,827 formal models, all made with
today's facts prompt): each sampled fact was parsed again with
`Vocabulary.parse`, and the vote of `_agreed_facts` was redone with the
missing outer parentheses added back. No GPU.

**Result.** Of 31,646 sampled facts, 1,719 (5.4%) were dropped. Hardly any
were dropped for an invented symbol:

| Why it was dropped | Facts | Example |
|---|---|---|
| outer parentheses missing | 1,091 (3.4%) | `>= consecutive_failure_count 0` |
| type error | 366 (1.2%) | `=` with one argument; a term that is not true or false |
| operator that SMT-LIB does not have | 196 (0.6%) | `!=`, `/=`, `eq`, `&` |
| name not in the list | 49 (0.2%) | `null` (21), `TRUE`; only 2 look like a real fact: `reserve_price`, `exit_gate_closed` |
| other syntax | 17 | `[]`, `(⇒ a b)` |

No invented name was used by more than half of one run's answers, so the
vote never lost a fact for want of a symbol. With the parentheses repaired,
the vote keeps 2,434 facts instead of 2,319, in 65 of the 1,827 models and
never fewer: 89 are bounds ("the delivery failure count is never negative"),
20 implications and 6 exclusions ("a bid cannot be both accepted and
rejected"). Whether that changes any finding was not measured. Repairing the
formula would be a design change, so it would need `eval9/` first.

Apart from the facts themselves: 6,499 of the 14,591 answers were empty lists,
which the prompt allows; 25 answers were not valid JSON; and 21 answers were
dropped whole because their facts contradict each other.

**Raw data.** [experiments/results/T19_fact_drops.json](experiments/results/T19_fact_drops.json).

---

## E15 — Held-out `eval9/`, with the parentheses repair of the facts vote (2026-11-23)

**Question.** T19 found that the most common reason a sampled fact is dropped
is a formula without its outer parentheses (`>= count 0`). The facts vote now
adds them back. Does that change any finding, on the saved runs and on specs
it was not built on?

**Setup.** `eval9/` was written and committed first (e96592d): six new domains
(level crossing, research grants, animal shelter, swimming pool, phone
top-up, kindergarten pick-up), the same design as `eval8/`, 30 versions. Then
the repair was committed (3d25117), with a configuration of `evaluate.py`
that scores the same runs as if the vote had not repaired anything (it keeps
only the facts the old vote keeps; step 6 still ran with all of them). 90 runs
(3 per version, 1 symbol set, temperature 0.7) on one cluster job, 2 GPUs,
18 minutes.

**Dev check first, no GPU.** On every saved run of `eval/` to `eval8/` and the
two long specs, the facts that the repaired vote adds were put into the
models (unchecked by step 6), and the runs scored again. One run of about
1,800 changed: in `upload_overlap` (E4) the vote now keeps "a file cannot be
both stored and rejected" (5 of 8 answers, 2 of them without parentheses),
and the run finds its 3 planted conflicts. Nothing was lost, no false alarm
and no ambiguity flag appeared.

**Results on `eval9/`.**

| Configuration | Planted conflicts | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities | Flags on clean specs |
|---|---|---|---|---|---|
| default | 18/18 | 5/18 | 17 | 18/36 | 1 |
| doubtful conflicts set aside | 18/18 | 2/18 | 5 | 18/36 | 1 |
| facts vote without the repair | 18/18 | 5/18 | 17 | 18/36 | 1 |
| without assumed facts and links | 11/18 | 1/18 | 1 | 18/36 | 1 |
| without step 6 | 17/18 | 5/18 | 17 | 16/36 | 1 |

- **The repair changed nothing here.** 88 of 1,651 sampled facts (5.3%) had
  no outer parentheses. The repair made the vote keep 17 more facts in 9 of
  90 runs, and all of them are bounds ("the number of late arrivals is never
  negative"). No conflict needs a bound, so every row is the same with and
  without it.
- **All 18 planted conflicts were found**, 9 direct and 9 overlap, in every
  run. Without facts and links, 11 of 18.
- **The 2 clean runs with a false alarm are a real conflict** that we wrote
  into `shelter_clean` by mistake. R3: when the adoption fee is paid, the
  animal is removed from the website. R4: an animal in the shelter for more
  than 90 days is featured on the home page. An animal adopted after 90 days
  falls under both. It was found in 2 of 3 runs through a link ("when the fee
  is paid, the animal is not featured on the home page"). It is counted as a
  false alarm, because the expected file was not changed after reading the
  results.
- **The doubtful ones** are `crossing_clean` (and the same pair in
  `crossing_gap` and the ambiguity versions): "a train approaches" lowers the
  barriers, "a train has passed" raises them, which clash only if both events
  happen at once. All were marked.
- **Ambiguities** 18 of 36: "only" 9 of 9, "if" 6 of 9, boundary 2 of 9,
  "and/or" 1 of 9. One flag on the clean specs.
- **Gaps**: the 6 planted gaps in 18 of 18 runs; a gap on a covered event in
  3 of 18 clean runs (E13: 4 of 18).

**Decision.** The repair stays. It never lost anything; on the saved runs it
recovered one planted conflict (3 runs), on `eval9/` it changed nothing.
`eval9/` is development data from now on; the next design needs `eval10/`.

**Raw data.** [experiments/results/E15_eval9.json](experiments/results/E15_eval9.json)
(with its table, E15_eval9.md), and the dev check
[experiments/results/E15_dev_rescore.json](experiments/results/E15_dev_rescore.json).

---

## T20 — Facts that say "one of the two", and a doubtful mark on gaps (2026-11-23, development)

**Question.** The false gaps of E13 and E15 come from two symbols for two
complementary conditions, `slot_is_free` and `slot_is_taken`. To Z3 a slot can
then be neither, so "a resident books a slot" has a situation no rule covers.
A voted fact `(or slot_is_free slot_is_taken)` rules that situation out. Can
such facts mark these gaps as doubtful, the way conflicts are marked?

**Change** (`eval10/` was written and committed first, a3666f7):
- The facts prompt (step 4) gets one more typical case: "one of two things is
  always the case, because each is the opposite of the other (a switch is
  either on or off)".
- `find_gaps` gets the voted facts. For each event it first looks for a gap
  that the facts allow. If there is none, but there is one without the facts,
  that gap is still reported, with `doubted_by` (the facts that rule it out),
  and its title says "doubtful: the assumed facts say this situation cannot
  happen". A fact still never removes a gap.

**Setup.** `eval8/` and `eval9/` (90 runs each) and the three development
specs (9 runs): 3 runs per version, 1 symbol set, temperature 0.7, one cluster
job.

**Results.**

| | `eval8/` | `eval9/` |
|---|---|---|
| clean runs with a gap on a covered event | 5 of 18 | 3 of 18 |
| the same, doubtful gaps set aside | 3 of 18 | 3 of 18 |
| planted gaps | 17 of 18 | 18 of 18 |
| planted conflicts | 18 of 21 | 18 of 18 |
| clean runs with a false alarm (doubtful conflicts set aside) | 0 of 18 | 1 of 18 |
| planted ambiguities | 16 of 36 | 16 of 36 |

- The "one of the two" fact was voted in 2 of the 3 `laundry_clean` runs, and
  those two gaps were marked. In all 180 runs a fact of the form `(or ...)`
  was voted in 4 (laundry and tolls, all in `eval8/`); before the change, in
  none (E13, E15).
- Not marked: `donations` ("the payment succeeds" / "fails", 2 runs) and
  `topup` ("the payment is accepted" / "refused", 3 runs). The model never
  says that one of the two always holds. A payment can also be pending, so it
  is right not to.
- The planted gap missed in `meters_gap` is unrelated: the translation put
  the condition into the consequent.
- Development specs: 13 of 15 conflicts, as before (`auth_openspec` [1, 4]
  2 of 3, `delete_property` 2 of 3).

**Raw data.** [experiments/results/T20_eval8.json](experiments/results/T20_eval8.json),
T20_eval9.json and T20_specs.json, each with its table.

---

## E16 — Held-out `eval10/`, with the doubtful mark on gaps (2026-11-24)

**Question.** Does the design of T20 hold on specs it was not built on?

**Setup.** `eval10/` was written first (a3666f7): six new domains (baggage
drop, allotment gardens, car inspection, hospital visitors, fuel station,
passport office), the same design as `eval9/`, 30 versions. Three of them
have a pair of complementary conditions in two words: "within the weight
limit" / "overweight", "passes" / "fails", "still valid" / "expired". Then
the design was frozen (167b1d6). 90 runs (3 per version, 1 symbol set,
temperature 0.7) on one cluster job, 2 GPUs, 17 minutes.

**Results on `eval10/`.**

| Configuration | Planted conflicts | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities | Flags on clean specs |
|---|---|---|---|---|---|
| default | 18/18 | 0/18 | 0 | 7/36 | 1 |
| doubtful conflicts set aside | 18/18 | 0/18 | 0 | 7/36 | 1 |
| without assumed facts and links | 15/18 | 0/18 | 0 | 7/36 | 1 |
| without step 6 | 18/18 | 0/18 | 0 | 10/36 | 1 |

Gaps: the 6 planted gaps in 18 of 18 runs; a gap on a covered event in 5 of
18 clean runs, and still 5 with doubtful gaps set aside.

- **All 18 planted conflicts were found**, in every run, and no other
  conflict was reported on any version, even counting doubtful ones. This is
  the first held-out set without one.
- **The mark set aside none of the 5 false gaps.** In `baggage_clean` (2 of 3
  runs) the vote kept only "not both",
  `(=> bag_within_weight_limit (not bag_overweight))`. In `inspection_clean`
  (3 of 3 runs) no fact about `test_passed` and `test_failed` was voted at
  all. No `(or ...)` fact was voted in any of the 90 runs. `passports` gave no
  false gap.
- **Ambiguities 7 of 36, the fewest of any held-out set** (14 to 20 before):
  "if" 0 of 9, "and/or" 1 of 9, boundary 1 of 9, "only" 5 of 9. Sampling
  alone, which does not see the facts, found 10 of 36, with "if" also 0 of 9:
  the 8 translations agreed on those rules. So it is the set, not the change,
  which added no new kind of fact here.

**Decision.** The design stays: conflicts, false alarms and planted gaps are as
good as before or better. It does not solve the false gaps: of 54 clean runs
in T20 and E16, 13 had a false gap and 2 were marked. The model rarely says
that two conditions cover every case, and for some pairs (a payment can be
pending) it is right not to. This is recorded as a known limit and not tried
again. `eval10/` is development data from now on; the next design needs
`eval11/`.

**Raw data.** [experiments/results/E16_eval10.json](experiments/results/E16_eval10.json)
(with its table, E16_eval10.md).

---

## T21 — The check of an OpenSpec change, on development data (2026-11-24)

**Question.** Kiro, as documented, reads one requirements document. In an
OpenSpec project the specs say what the system does today
(`openspec/specs/<capability>/spec.md`), and new work arrives as a change that
holds only the difference (`openspec/changes/<name>/specs/.../spec.md`, with
`## ADDED`, `## MODIFIED`, `## REMOVED` and `## RENAMED Requirements`). Can
the pipeline say what a change breaks in the specs that exist, without being
changed itself?

**Design** (plan.md 5.10; the held-out set `eval11/` was written first,
f4215c9):

1. Our code (`speccheck/change.py`) applies the change to the specs, matching
   requirements by name, and writes one document. In it every scenario header
   gets a label: `#### Scenario R4: Locked account`.
2. The merged document is formalized and checked like any spec. The prompts,
   `formalize.py` and `checks.py` are untouched. The read prompt already says
   "Use the document's own label as id", so the rules come back with the
   labels as ids, and our code knows which rules the change added or modified.
3. Our code keeps the findings that involve the change: a conflict, a
   scenario or an ambiguity with an added or modified rule, and a gap for an
   event that such a rule reacts to. If a label does not come back, the tool
   stops.

**Setup.** There were no specs with changes, so development data was made
from sets that had been read. `make_eval.py change_dev` turns the six
OpenSpec-format specs of `eval9/` and `eval10/` into projects: the clean spec
is what exists, and each planted version becomes a change (a MODIFIED
requirement). That gives 22 cases: 4 with a conflict, 12 with an ambiguity, 6
with a gap; two versions that add a requirement without a scenario were left
out. The login spec was laid out by hand as a project, `specs/auth_change`:
four scenarios exist, and the change adds "administrators are never locked
out". 3 runs each, 1 symbol set, temperature 0.7; with the three development
specs and one report, one cluster job of 19 minutes.

**Results.**

- **The labels came back in 69 of 69 runs**, and the read step made no rule
  without a label (the SHALL sentence under a requirement's header was never
  taken for a rule).
- **`change_dev/`:** planted conflicts 12 of 12 (3 of 12 without assumed facts
  and links), planted gaps 18 of 18, planted ambiguities 13 of 36.
- **`specs/auth_change`:** the conflict between R3 (lock at 5 failed
  attempts) and the added R5 in 3 of 3 runs. The conflict between R1 and R4,
  which the spec had before the change, was found in 3 of 3 and left out in 3
  of 3.
- **2 other conflicts about a change**, both in `shelter_gap`: the real
  conflict of `shelter_clean` (E15). One of its two scenarios belongs to the
  requirement that the change rewrites, so it counts as changed although its
  text is the same.
- **45 gaps about a change in 66 runs**, 18 of them planted. The others are
  cases that the rewritten requirement does leave open: a counted event ("for
  the second time") at another count, or a condition that a reworded scenario
  added.
- The three development specs gave 15 of 15 conflicts, as expected: no prompt
  changed.

**Decision.** Frozen as built (58599e4). Noted and not changed: every
scenario of a modified requirement counts as changed, also one whose text
stayed the same.

**Raw data.** [experiments/results/T21_change_dev.json](experiments/results/T21_change_dev.json)
and T21_specs.json, each with its table; the saved run of the example is in
`specs/auth_change/`.

---

## E17 — Held-out `eval11/`: the check of an OpenSpec change (2026-11-24)

**Question.** Does the change check of T21 hold on projects it was not built
on?

**Setup.** `eval11/` was written first (f4215c9) and the design frozen in
58599e4. The set has six OpenSpec projects in new domains (museum, coworking
space, marina, cinema, conference, food bank). Each has two or three spec
files with six existing scenarios, in OpenSpec's own format: a SHALL sentence
under each requirement, and scenarios with WHEN / THEN bullets. Each project
comes with five changes:

| Version | The change | Must report |
|---|---|---|
| `clean` | adds a requirement with both of its cases (3 of the 6 also remove an unrelated requirement; 1 puts it into a new spec file) | nothing about the change |
| `direct` (3), `overlap` (3) | adds a requirement that clashes with an existing scenario | that conflict |
| `modified` | rewrites a requirement so that it clashes with a scenario in another spec file | that conflict |
| `gap` | adds a requirement that covers one of two cases | a gap for its event |
| `narrowed` | rewrites a requirement and drops one of its two complementary scenarios | a gap for its event |

The planted conflicts negate an existing outcome in its own words ("opens the
gate" / "does not open the gate"), on purpose: the set tests the merge and
the selection of findings, not the choice of symbols. 90 runs (3 per case, 1
symbol set, temperature 0.7) on one cluster job, 2 GPUs, 22 minutes.

**Results.** Only findings about the change count, as in the tool's report.

| Configuration | Planted conflicts | direct | overlap | modified | Clean changes with a conflict about the change | Other conflicts about the change |
|---|---|---|---|---|---|---|
| default | 36/36 | 9/9 | 9/9 | 18/18 | 0/18 | 0 |
| doubtful conflicts set aside | 33/36 | 9/9 | 9/9 | 15/18 | 0/18 | 0 |
| without assumed facts and links | 33/36 | 9/9 | 9/9 | 15/18 | 0/18 | 0 |

Planted gaps: 36 of 36 (`gap` 18 of 18, `narrowed` 18 of 18). Clean changes
with a gap on a covered event: 0 of 18.

- **The labels came back in 90 of 90 runs**, and no rule without a label was
  made.
- **Everything shown was planted.** The 90 reports would show 72 findings, 36
  conflicts and 36 gaps, and all 72 are the planted ones. 174 findings were
  left out: 90 gaps in which no event happens, 81 gaps on events of existing
  rules, and 3 ambiguities of existing rules. No conflict among existing
  rules was found.
- **3 planted conflicts are marked doubtful**, all in `cinema_modified`:
  "WHEN the projector of a hall is out of order" was read as an event,
  `projector_fault`, in 3 of 3 runs. The clash with "a customer asks for a
  seat" then seems to need two events at once. This is the limit seen in E10
  (a state read as an event). The same conflict is the only one that needs an
  assumed fact.
- **No ambiguity was flagged on a rule of a change.** None was planted.

**What this does not show.**
- The conflicts were worded to be found. What the earlier sets measure about
  the choice of symbols ("remove" against "keep") applies to changes as well.
- A gap opened by a REMOVED requirement is not attributed to the change. The
  set has no such case.
- The projects are small and written by us. No real OpenSpec project was
  tried.

**Decision.** The check stays as built. `eval11/` is development data from
now on; the next design needs `eval12/`.

**Raw data.** [experiments/results/E17_eval11.json](experiments/results/E17_eval11.json)
(with its table, E17_eval11.md).

---

## T22 — What the missed conflicts look like, and a question about pairs of outcomes (2026-11-24, development)

**Question.** Which planted conflicts are still missed, and why?

**The misses, from the saved runs (no GPU).** The eight held-out tests E8 to
E16 (`eval3/` to `eval10/`) planted 51 conflicts, 153 with their 3 runs each.
129 were found, 3 were found but marked doubtful, and 21 were missed:

| Cause | Runs | Where |
|---|---|---|
| The two rules demand opposite things with two different symbols, and no assumed fact connects them | 13 | `doors` 6 (`(not door_unlocked)` / `all_doors_unlocked`), `canteen` 3 (`payment_taken` / `payment_refused`), `messages` 3 (`message_removed` / `message_in_archive`), `oven` 1 (`heating_paused` / `heating_at_program_temp`) |
| "Keep for N years" became only a number | 5 | `auctions` 3, `photos` 2: `(= listing_retention_years 7)` against `listing_deleted` |
| The "keep" rule was rejected: its 8 translations disagreed | 3 | `clinic` |

In 13 of the 21 the same thing is missing: one piece of common sense, such as
"a payment cannot be taken and refused at once". The facts question of step 4
is open ("list the facts that connect these symbols") and often does not
mention the pair that matters; 45% of its answers are an empty list (T19).

**Design: probe check 4** (`probe.outcomes`; `eval12/` was written first,
c6e2231). The existing prompts do not change.

1. Our code and Z3 pick the pairs of rules to ask about: both rules can apply
   in one situation that the facts allow; they do not react to two different
   events; what they demand shares no symbol and is not already excluded by a
   fact; and what each demands is one definite state of its symbols.
2. The model is asked 8 times about the two outcomes alone, shown as facts
   with their descriptions, without the requirement texts: "Statement A:
   TRUE: payment_taken (...). Statement B: TRUE: payment_refused (...). Can A
   and B both hold in the same snapshot?" It answers possible, impossible or
   unclear.
3. If more than half of the answers say impossible, our code adds the assumed
   fact `(not (and payment_taken payment_refused))`, with the model's
   sentence and its support.
4. Z3 proves the conflict as before; the report says "if the assumed facts
   hold" and quotes the fact.

At most 40 pairs are asked about. The six-rule specs have 2 to 5; the specs
of 30 and 100 requirements have several hundred candidates, so there the
check covers only the first 40.

**Setup.** The check comes last in step 6 and needs only the formal model.
So it was run on the saved formal models of E8 to E16 (`evaluate.py --rescore
... --outcomes-base-url`), which gives a before and an after on the same 630
runs. Each `T22_<set>.json` holds only what the check added and names the
runs it belongs to. The development specs got a full run. One cluster job,
26 minutes.

**Results on `eval3/` to `eval10/`.** 1,434 pairs were asked about, 2.3 per
run, and 130 of them (9%) were called impossible by a majority.

| | Without the check | With it |
|---|---|---|
| planted conflicts found | 132 of 153 | 145 of 153 |
| the same, doubtful ones set aside | 129 of 153 | 142 of 153 |
| clean runs with a conflict that was not planted, doubtful ones set aside | 3 of 144 | 13 of 144 |
| conflicts that were not planted, all versions, doubtful ones set aside | 32 | 88 |

- **Recovered, 13 of the 21 misses:** `doors` 6 of 6, `canteen` 3 of 3,
  `photos` 2 of 2 ("the photo is erased" against "the retention period is 2
  years" was called impossible), `messages` 1 of 3, `oven` 1 of 1. Not
  recovered: `auctions` 3, `messages` 2, `clinic` 3.
- **The 56 added conflicts that were not planted**, by kind:

  | Kind | Conflicts | Example |
  |---|---|---|
  | the planted rule against a third rule | 20 | "refuse all payments" also clashes with "add the top-up to the balance" (`canteen`) |
  | two original rules, in a version with a planted defect | 14 | the same pairs as on the clean specs below |
  | two rules of a clean spec | 13 | "start the selected program" against "stop all brushes" when the emergency button is pressed (`carwash`, 6); "move to the calling floor" against "take the elevator out of service" (`elevator`, 3); `claims` 2, `irrigation` 1, `shelter` 1 |
  | involves the rule with the planted ambiguity | 9 | `claims`, `shelter` |

- **On the clean specs** the 10 new runs are 7 runs in which two rules really
  can apply together and nothing says which one wins (`carwash`, `elevator`,
  `irrigation`), 1 more run of the real conflict of `shelter_clean` (E15),
  and 2 runs of `claims_clean` that are an artefact: "reject the claim"
  (damage not covered) against "pay the claim" (a registered claim under
  1000 euros), where nothing says that a registered claim is a covered one.
  The scoring counts all 10 as false alarms.
- **The development specs** are unchanged: 15 of 15 conflicts, the conflict
  of `auth_change` in 3 of 3 runs, no other conflict.

**Raw data.** [experiments/results/T22_eval3.json](experiments/results/T22_eval3.json)
to T22_eval10.json (the answers to every question; each with its table,
which has rows with and without the check) and T22_specs.json.

---

## E18 — Held-out `eval12/`: the questions about pairs of outcomes (2026-11-24)

**Question.** Does check 4 of T22 find conflicts worded in other words, on
specs it was not built on, and what does it cost?

**Setup.** `eval12/` was written first (c6e2231) and the design frozen in
f2bb7ed. Six new domains (hospital beds, timesheets, aquarium, theatre
cloakroom, wind turbine, payroll), 36 versions: each spec has a clean, a
direct, an overlap, two ambiguity and a gap version. All 12 planted conflicts
say the opposite outcome in other words ("switch the heater on" / "cut the
power to the heater"); two are retention periods ("delete the payslips" /
"keep every payslip for ten years"). 108 runs (3 per version, 1 symbol set,
temperature 0.7) on one cluster job, 2 GPUs, 24 minutes. "Without the check"
is the same runs scored without the facts that check 4 added.

**Results on `eval12/`.**

| | Without the check | With it |
|---|---|---|
| planted conflicts found | 27 of 36 | 34 of 36 |
| direct (the same condition, the opposite outcome) | 9 of 18 | 16 of 18 |
| overlap (another condition, the opposite outcome) | 18 of 18 | 18 of 18 |
| clean runs with a conflict that was not planted | 0 of 18 | 3 of 18 |
| conflicts that were not planted, all versions | 1 | 28 |
| planted ambiguities found | 16 of 36 | 16 of 36 |
| planted gaps found | 17 of 18 | 17 of 18 |
| clean runs with a gap on a covered event | 0 of 18 | 0 of 18 |

410 pairs were asked about, 3.8 per run, and 58 (14%) were called impossible.

- **Gained, 7 of the 9 misses:** `beds_direct` 3 of 3 ("release the bed" /
  "hold the bed for 24 hours": `bed_released` and `bed_held`, 8 of 8 answers
  impossible), `cloakroom_direct` 3 of 3 (a retention period: "delete the
  token record" / "keep every token record for two years", which became
  `token_record_deleted` and `token_record_retained`), `payroll_direct` 1 of
  3.
- **Still missed, 2 runs of `payroll_direct`.** "Keep every payslip for ten
  years" became the number `(= payslip_retention_years 10)`: one run called
  it impossible together with "the payslips are deleted" (8 of 8, found),
  one split 4 to 4 (missed). In the third the rule became "a payslip younger
  than ten years is retained", which is not one definite state, so the pair
  was not asked about.
- **The overlap conflicts did not need the check**: 18 of 18 without it, 3 of
  18 without any assumed fact or link. The links of step 5 found them.
- **The 27 added conflicts that were not planted** are nearly all one pair. 24
  are in `cloakroom`, in all six versions: "WHEN a guest shows a token THEN
  the system releases the coat" against "WHEN a coat has been on its hook for
  more than 30 days THEN the system adds the coat to the list of unclaimed
  coats". A guest who collects a coat after more than 30 days falls under
  both, and 8 of 8 answers say that a coat cannot be released and on the
  unclaimed list at once. Over time there is no clash: the coat was listed
  before and is released now. So this is an artefact of the one-snapshot
  model, on a pair of rules that we wrote into the clean spec without seeing
  it. The other 3 are the planted rule of `timesheets_overlap` against a
  third rule ("withhold all timesheets from the managers" against "ask the
  manager for a comment").
- **The 3 clean runs with a conflict** are the 3 runs of `cloakroom_clean`.
- Ambiguities, gaps and false gaps are the same with and without the check.

**Decision.** The check stays, on by default. It finds most of the conflicts
that were missed (13 of 21 in T22, 7 of 9 here). The price is more conflicts
that nobody planted (clean runs with one: 3 to 13 of 144 in T22, 0 to 3 of 18
here); each of them says "if the assumed facts hold" and quotes the fact it
rests on. The gain was judged larger than the loss. The other two choices
were to make the check an option that is off by default, or to drop it. `eval12/` is development data from now on; the next design needs
`eval13/`.

**Raw data.** [experiments/results/E18_eval12.json](experiments/results/E18_eval12.json)
(with its table, E18_eval12.md).

---

## Lessons from bugs that changed results

| | What happened | Fix | Why it matters for a paper |
|---|---|---|---|
| L1 | The model declared an enum with one value. Every condition on it was silently always true, and the findings looked right by accident. | Enums with fewer than 2 values are refused; the read step retries. | Right-looking output is not evidence of a right formalization. |
| L2 | A false one-rule "conflict": forcing "admin and locked" contradicts "never lock administrators" alone. It also hid the real conflict of the same rule. | A situation that one rule alone forbids is not a conflict. | Forcing antecedents creates situations the spec itself excludes. |
| L3 | `A => C` and `true => (A => C)` were counted as two readings. | Samples are compared as whole formulas. | Ambiguity must be semantic, not about how a rule is split. |
| L4 | The explanation model read `x = false (the order was canceled)` as "the order was canceled". | Facts are written `TRUE:` / `FALSE:` in front. | The wording step can corrupt a proven finding. |
| L5 | The explanation model ended conflicts with "Which did you mean?". | Prompt states that only ambiguities ask. | Same. |
| L6 | Scoring by rule id was wrong: the model renumbers rules without labels. | Scoring by position. | Evaluation artefact. |
| L7 | Z3 was called from several threads and the process died without an error. | Only LLM calls run in threads. | Engineering. |
| L8 | One snapshot, no time: a single rule can contradict a domain fact by design ("WHEN the door is open, close it" vs "a closed door is not open"). | A conflict that depends on facts needs at least two rules. | Limits what fact-based findings can claim. |
| L9 | The explanation model drifted to a more "natural" situation for gaps: with `FALSE: order_submitted` proven, it wrote "when an order has been submitted". Seen in 2 of 2 gap explanations of one report run, despite L4. | The answer schema now starts with a `situation` field: the model must restate the proven situation fact by fact before it explains. After: 8 of 8 gap explanations faithful (6 in a probe, 2 in the regenerated reports). | Small numbers, but the direction is clear: make the model restate before it explains. |
| L10 | Temperature 0 does not make the read step repeatable on the batched server: in 10 "greedy" runs `delete_property` got 4 different symbol lists, `auth_openspec` 2, `order` 1 (E2a). | None; reported as it is. | "Fixed symbols" in E1 and E2 means "temperature 0", not "identical". |

---

## Open questions and threats to validity

- **Small evaluation.** 24 base specs in 99 versions over four sets, 63 to 90
  runs per experiment, one main model. The base specs and the planted defects
  were written by us. A paper needs more specs, more runs and other main models.
- **Hold-out sets.** Each set was read after its held-out run (E5, E7, E8, E9),
  so all four are development data now; ideas from reading E9 need a fifth set.
  One leak is known: a read-prompt example from the domain of a held-out spec
  (D4).
- **Ambiguity.** One model's judgment is the limit: whether it samples,
  answers about a situation, or chooses between two readings, it is confident
  on many rules a reader would query (T7). A second model of another family is
  not: with it, 30 of 36 planted ambiguities are found (E9), at the price of
  about one flag per clean spec. "And"/"or" scope is the weakest kind.
- **Events written as states.** The two-event mark relies on the read step
  marking events. Counted happenings now get an event symbol in about half of
  the cases (E9): not for failures ("fails to close for the third time") or
  things the system records ("is recorded as late for the third time").
- **A regression in `delete_property`.** Since the read-prompt changes of step
  16, the blog's second example is found in about half of the runs (T8), not 8
  of 8 (E5): a wrong voted fact makes D4 contradict the facts on its own.
- **Wrong links and facts.** A majority of samples can agree on a wrong link (3 of 8
  `delete_property` runs) or a wrong fact (E2). They are add-only, and no wrong finding
  came from one in E5, but nothing rules it out.
- **The false-alarm pattern.** Two complementary conditions modelled as two
  independent symbols ("at least 24 hours", "less than 24 hours") give a false
  conflict. 2 of 63 runs in both E4 and E5.
- **Scenarios and gaps are not scored.** There is no ground truth for them.
- **The explanation step is checked by hand only**, on a handful of findings (L4, L5,
  L9). There is no measured rate of faithful explanations.
- **Existing specs.** Kiro, as documented, analyses one `requirements.md`. In OpenSpec
  a change is a delta against existing specs. Checking a change against them is done
  by neither, as far as their docs say. Not built yet.
- **Charitable reading at symbol time** (T1, T3, E3) is still there in the read step.
  Links work around it by asking a different question; they do not remove it.
- **Code versions.** The project is not under version control, so earlier experiments
  cannot be re-run on the code of their time. Each experiment file stores its prompts
  and all formalizations, and can be re-scored without a GPU. Note: re-scoring an old
  file uses today's checks (for example conflicts of three rules). After the code
  cleanup of 2026-11-19 (shared grouping of translations, one majority constant),
  every count re-scores the same; only the example situation shown for a
  second-reader ambiguity can differ, because Z3 returns another valid one.
