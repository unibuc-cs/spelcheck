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

## T23 — What a change removes: the gap it opens, on development data (2026-11-24)

**Question.** The change check of T21 had two limits. A gap opened by a
REMOVED requirement was found but not tied to the change, because the removed
rule was not in the merged document. And every scenario of a MODIFIED
requirement counted as changed, so an old conflict of a scenario whose words
had not changed was shown as the change's (2 runs in T21). Can both go,
without touching the prompts?

**Design** (plan.md 5.10; `eval13/` was written first, f1dd15f):

1. Our code (`change.merge`) gives every scenario one of four states.
   Inside a MODIFIED requirement the scenarios are matched by name: the same
   words is "existing", other words is "modified", a new name is "added", and
   a name that the new text does not have is "removed". All scenarios of a
   REMOVED requirement are "removed".
2. The removed scenarios stay in the document that the LLM reads, with labels
   of their own (X1, X2, ...). So they get the same symbols as the rest.
3. Our code (`change.after_model`) takes the removed rules out of the formal
   model, with the links and outcome facts that came from them, and keeps
   them apart under `removed_rules`. The checks run on what is left.
4. Z3 gets one more question for each removed rule (`checks.find_gaps`): in
   the situation this rule was written for (its events happen and no others,
   its condition holds), does any remaining rule apply? If none does, that is
   a gap, reported as "opened by removing X1". A removed rule whose events no
   remaining rule reacts to gives no gap: that event was retired by decision.

**Setup.** `eval11/` and `change_dev/` again (both development data) and the
development specs, full runs: 90, 66 and 12 runs, 3 per case, 1 symbol set,
temperature 0.7, one cluster job of 41 minutes. These are also the first runs
of the change sets with the questions about pairs of outcomes on (T22).

**Results.**

| | `eval11/` | `change_dev/` |
|---|---|---|
| planted conflicts found | 36 of 36 | 12 of 12 |
| planted gaps found | 36 of 36 | 18 of 18 |
| quiet changes with a conflict or a gap about them | 0 of 18 | none in this set |
| other conflicts about the change | 0 | 3 |
| labels kept | 90 of 90 runs | 66 of 66 runs |

- **The X labels came back too**: 45 of the 156 runs had a removed scenario
  in their document, and every label was a rule id in all of them.
- **A flaw found and fixed before the freeze.** The first version of step 4
  asked, for each event alone, whether a removed rule had covered an
  uncovered situation. In `topup_gap` the model had read "the payment is
  refused" as an event of its own, so the removed rule `(and
  customer_buys_credit payment_refused)` needs two events at once and was
  never reached: its gap was missed in 3 of 3 runs. The question now takes
  the removed rule's own situation, with all of its events. Re-scored on the
  same runs (only the Z3 part changed): 15 → 18 of 18.
- **The old conflict of `shelter_gap` is no longer the change's.** Its
  scenario has the same words as before, so it is "existing" (T21: shown in 2
  of 3 runs; now found and not shown in 3 of 3). The 3 other conflicts are
  `shelter_ambiguity1`, where the change does reword one of the two scenarios
  of that conflict.
- **The questions about outcomes added nothing about a change** in `eval11/`
  (0 other conflicts, as in E17).
- The development specs: 14 of 15 conflicts (`delete_property` 2 of 3), the
  conflict of `auth_change` in 3 of 3.

Before the freeze the merge was also run on the files of `eval13/`, to see
that it does not fail there. No model saw them.

**Raw data.** [experiments/results/T23_eval11.json](experiments/results/T23_eval11.json),
T23_change_dev.json and T23_specs.json, each with its table (scored with the
fixed step 4). A report of a change with a removal is saved in
`experiments/examples/visitors_removed/`.

---

## E19 — Held-out `eval13/`: what a change removes (2026-11-24)

**Question.** Does the design of T23 hold on projects it was not built on:
is a gap that a removal opens tied to the change, and is an old conflict
left alone?

**Setup.** `eval13/` was written first (f1dd15f) and the design frozen in
07ecd38. Six OpenSpec projects in new domains (student dormitory, language
school, blood bank, building permits, newsroom, makerspace), each with two
spec files and nine existing scenarios. Each project has one conflict among
its existing scenarios ("unlock the room door" when a valid card is shown,
against "do not unlock any room door" over the winter break), and no change
touches the words of those two scenarios. Six changes for each project:

| Version | The change | Must report |
|---|---|---|
| `clean` | adds a requirement with both of its cases | nothing about the change |
| `modified` | rewrites a requirement so that it clashes with a scenario in the other spec file | that conflict |
| `removed` | REMOVES the requirement that held one of two complementary cases | a gap for their event, as the change's |
| `narrowed` | rewrites a requirement and drops one of its two complementary scenarios | the same kind of gap |
| `retired` | REMOVES the only requirement for an event | nothing |
| `sibling` | rewrites a requirement: one scenario gets a harmless addition, the other keeps its words and is part of the old conflict | nothing; the old conflict is not the change's |

108 runs (3 per case, 1 symbol set, temperature 0.7) on one cluster job, 2
GPUs, 40 minutes.

**Results.** Only findings about the change count.

| | Result |
|---|---|
| planted conflicts (`modified`) | 18 of 18 (15 with doubtful ones set aside) |
| planted gaps, a requirement removed (`removed`) | 18 of 18 |
| planted gaps, a scenario dropped (`narrowed`) | 17 of 18 |
| quiet changes (`clean`, `retired`, `sibling`) with a gap about them | 0 of 54 |
| quiet changes with a conflict about them | 2 of 54 |
| the old conflict, shown as the change's | 0 of 108 |
| the old conflict, found and not shown | 108 of 108 |
| labels kept (R and X) | 108 of 108 runs; 54 of them had a removed scenario |

- **Every gap shown is one that a removal opened.** The reports would show 35
  gaps, all with "opened by removing X1", and all planted. 124 other gaps
  were left out (108 in which no event happens, 16 on events of existing
  rules).
- **Removing the only rule for an event gave no gap**, in 18 of 18 runs of
  `retired`.
- **The old conflict was found in every run and never blamed on the change**,
  also not in `sibling`, where the change rewrites the requirement that one
  of its two scenarios belongs to.
- **The one gap missed** (`dorm_narrowed`, 1 of 3 runs) is a translation
  slip: the rule that stays lost its condition ("AND the student has guest
  nights left"), so it covers every registration and no gap is left.
- **The 2 conflicts on quiet changes** are `makerspace_sibling`, 2 of 3 runs.
  The reworded scenario ("asks the member to top up the account and puts the
  material back on the stock list") against "does not book anything to the
  account of any member": a question about the two outcomes (T22) was
  answered "impossible" by 7 and 8 of 8. The scenario is the change's, since
  its words changed, but its old words would have given the same conflict.
- **3 planted conflicts are marked doubtful**, all in `courses_modified`:
  "WHEN a teacher is ill" was read as an event (the limit of E10 and E17).

**Decision.** The design stays. It ties the gap of a removal to the change
(18 of 18), stops blaming old conflicts on a change that rewrites a
neighbouring scenario (0 of 108), and loses nothing on `eval11/` and
`change_dev/` (T23). `eval13/` is development data from now on; the next
design needs `eval14/`.

**Raw data.** [experiments/results/E19_eval13.json](experiments/results/E19_eval13.json)
(with its table, E19_eval13.md).

---

## T24 — A change on a saved model of the specs, on development data (2026-11-24)

**Question.** Every change costs a full run: the merged spec is formalized
again, so that old and new rules share their symbols. Can a change be checked
by formalizing only its new scenarios, on top of a formal model of the specs
that is made once, without losing findings?

**Design** (plan.md 5.10; `eval14/` was written first, 881d1bb):

1. **The base.** The specs that exist are formalized as today, as one
   labelled document (`change.base_document`). `speccheck --change
   --incremental` keeps that model in `openspec/.speccheck/base.json`, with a
   fingerprint of the specs, and makes it again only when the specs change.
2. **The new part.** Our code (`change.merge(on_base=True)`) writes a
   document with the added and reworded scenarios of the change only,
   labelled N1, N2, ... The scenarios that stay keep the labels they have in
   the base, and so do the removed ones. The old rule of a reworded scenario
   is "replaced" and dropped.
3. **Formalizing the new part** (`formalize(..., base=...)`). The read step
   is shown the symbols of the base before the document, and its prompt gets
   one addition (`READ_MORE`): "Use a listed symbol wherever it fits the
   meaning: a new rule about a fact that already has a symbol MUST use that
   symbol, also when the rule says it in other words, so that a clash with
   the rules written before can be seen. Add a symbol only for a fact that no
   listed symbol stands for." The new rules are translated 8 times as usual.
   The facts question is asked again only if a symbol was added. Links are
   made for the new rules, in the terms of all rules' outcomes. The questions
   of step 6 are asked for the new rules, and the question about two outcomes
   for the pairs with a new rule.
4. The rest is as in T23: removed rules set apart, the checks, the selection.

**Setup.** `eval11/` and `eval13/` (development data) the new way: for each
project and each of the 3 runs its specs were formalized once (18 bases for
each set), and each change on the base of its run. 90 and 108 runs, plus the
development specs in the usual way and the command line twice on
`specs/auth_change`. One cluster job, 29 minutes. `evaluate.py` now records
what each run asked of the LLM.

**Results.**

| | `eval11/`, full (T23) | `eval11/`, new way | `eval13/`, full (E19) | `eval13/`, new way |
|---|---|---|---|---|
| planted conflicts found | 36 of 36 | 35 of 36 | 18 of 18 | 18 of 18 |
| planted gaps found | 36 of 36 | 36 of 36 | 35 of 36 | 36 of 36 |
| quiet changes with a conflict about them | 0 of 18 | 0 of 18 | 2 of 54 | 2 of 54 |
| quiet changes with a gap about them | 0 of 18 | 0 of 18 | 0 of 54 | 0 of 54 |
| the old conflict, shown as the change's | | | 0 of 108 | 0 of 108 |
| labels kept | 90 of 90 runs | 90 of 90 | 108 of 108 | 108 of 108 |

| What the LLM was asked, on average | Requests | Tokens read | Tokens written |
|---|---|---|---|
| a change of `eval11/`, new way | 9 | 4,812 | 3,743 |
| the specs of an `eval11/` project (6 scenarios), once | 46 | 21,491 | 18,823 |
| a change of `eval13/`, new way | 7 | 3,500 | 3,077 |
| the specs of an `eval13/` project (9 scenarios), once | 79 | 36,634 | 32,308 |

The full runs of T23 and E19 did not record their cost; `eval14/` is run both
ways with it.

- **The one conflict missed** (`marina_direct`, 1 of 3 runs): the 8
  translations of the new rule scattered and it was rejected. Nothing about
  symbols: the translations that agreed used `berth_freed`, the symbol of the
  old rule.
- **The new rules got the old symbols.** Even without any assumed fact or
  link, 35 of the 36 conflicts of `eval11/` and 18 of 18 of `eval13/` are
  found: the new rule and the old one share a symbol. In the login example
  the added rule became `is_admin => (not account_locked)`, with one new
  symbol and the `account_locked` of the lockout rule.
- A change that only removes asked the LLM nothing (0 requests; 72 of the 198
  runs).
- The development specs, run the usual way: 15 of 15 conflicts, and the
  conflict of `auth_change` in 3 of 3.
- The command line: the second run on `specs/auth_change` found the saved
  base and formalized only the one new scenario
  (`experiments/examples/auth_incremental/`).

**Raw data.** [experiments/results/T24_eval11_incremental.json](experiments/results/T24_eval11_incremental.json),
T24_eval13_incremental.json and T24_specs.json, each with its table.

---

## E20 — Held-out `eval14/`: the same changes checked both ways (2026-11-24)

**Question.** Does a change checked on a saved model of the specs (T24) find
what the full run finds, on projects it was not built on, and what does it
save?

**Setup.** `eval14/` was written first (881d1bb) and the design frozen in
373ae4c. Six OpenSpec projects in new domains (tennis club, brewery, music
school, driving school, climbing hall, flower shop), each with two spec files
and seven existing scenarios, and six changes:

| Version | The change | Must report |
|---|---|---|
| `clean` | adds a requirement with both of its cases | nothing about the change |
| `direct` | adds a requirement for the trigger of an existing scenario, with the opposite outcome in other words ("switches the floodlights on" / "keeps the floodlights dark") | that conflict |
| `overlap` | adds a requirement for a state, which forbids in the same words what a scenario in the other spec file demands | that conflict |
| `modified` | rewrites a requirement so that it clashes with a scenario in the other spec file | that conflict |
| `gap` | adds a requirement that covers one of two cases | a gap for its event |
| `removed` | removes the requirement that held one of two complementary cases | a gap, as the change's |

The 36 changes were run both ways, 3 times each, in one cluster job (47
minutes): the full way, 108 runs in 32 minutes; and the new way, 18 bases
(each project's specs, for each run) and 108 changes on them, in 13 minutes.

**Results.**

| | The full run | On a saved model (`--incremental`) |
|---|---|---|
| planted conflicts found | 54 of 54 | 50 of 54 |
| `direct` | 18 of 18 | 17 of 18 |
| `overlap` | 18 of 18 | 15 of 18 |
| `modified` | 18 of 18 | 18 of 18 |
| planted conflicts, doubtful ones set aside | 51 of 54 | 45 of 54 |
| planted gaps found (`gap`, `removed`) | 36 of 36 | 36 of 36 |
| clean changes with a conflict or a gap about them | 0 of 18 | 0 of 18 |
| other conflicts about a change | 3 | 1 |
| labels kept | 108 of 108 runs | 108 of 108 |
| **what a change asked of the LLM, on average** | **68 requests** | **9 requests** |
| tokens read / written | 32,431 / 28,806 | 4,934 / 3,816 |
| the specs of a project, once | | 61 requests, 28,641 / 25,969 tokens |

- **A change costs about a seventh.** By kind of change, in requests: a
  removal 60 against 0, a rewritten scenario 60 against 9, one added scenario
  69 against 8 to 10, two added scenarios 79 against 20. The first change to
  a project also pays for its base, about one full run.
- **The 4 conflicts missed by the new way are two cases.**
  `drivingschool_overlap`, 0 of 3: the new rule is "WHEN a person is younger
  than 17 THEN the system does not create any learner file". Read on its own,
  with the symbols of the base in front of it, the read step gave it the
  trigger `registration_attempted`, an event of the base that the rule does
  not name. Its 8 translations then disagreed on where that event goes
  (`registration_attempted => (and (< person_age 17) (not ...))`, `(<
  person_age 17) => (not ...)`), and the rule was rejected in 2 runs and
  ambiguous in the third, with a first reading that cannot clash. In the full
  run the same rule was read as a state rule and found in 3 of 3.
  `brewery_direct`, 1 of 3: the translations of the new rule scattered.
- **The new rules did get the old symbols**: no miss came from a new symbol
  where an old one was meant, and 44 of 54 conflicts are found by the new way
  without any assumed fact (the full run: 37 of 54).
- **More planted conflicts are marked doubtful the new way** (5 against 3):
  `florist_modified` in both ("WHEN the flower truck is being unloaded" read
  as an event), `musicschool_modified` in 2 runs of the new way only.
- **The other conflicts about a change** are fair: in `drivingschool_modified`
  the rewritten rule "does not book any lesson" also clashes with "opens the
  booking of road lessons" (3 runs of the full way, 1 of the new way with
  another rule).

**Decision.** The new way stays an option, `--incremental`, and the full run
stays the default: it finds less (50 against 54 here, 35 against 36 and 18
against 18 on the development sets), which was the rule set before the test
(plan.md). Its use is cost: a change is checked with about 9 requests where
the full run needs 68, and its findings were never wrong where the full
run's were right. `eval14/` is development data from now on; the next design
needs `eval15/`.

**After the test** (the same day, no effect on the numbers above): the saved
model now also records the name of the LLM and is made again for another
one; a run says on the error stream whether it used the saved model or made
it; and the command line refuses `--incremental` together with
`--symbol-sets`, `--second-base-url` or `--review`. README.md has a section
on the two ways, "The two ways to check a change".

**Raw data.** [experiments/results/E20_eval14_full.json](experiments/results/E20_eval14_full.json)
and E20_eval14_incremental.json, each with its table.

---

## T25 — Development: the read step ties a new rule to a saved event (2026-11-25)

**Question.** Why did the saved-model way (`--incremental`) miss 4 planted
conflicts on `eval14/` that the full run found (E20), and can one change to
the read prompt addition `READ_MORE` avoid it?

**The cause, from the saved runs of E20.** Of the 108 new rules read the
saved-model way, 4 were not accepted (3 rejected, 1 ambiguous), and those are
the 4 misses. Three are one rule in its 3 runs, in `drivingschool_overlap`:
"WHEN a person is younger than 17 THEN the system does not create any learner
file". The read step was shown the saved symbols, among them the event
`registration_attempted`, and it tied the new rule to that event in two
places:

| | The full run | The saved-model way |
|---|---|---|
| trigger of the rule | none (3 of 3 runs) | `registration_attempted` (3 of 3) |
| description of the new symbol `person_age` | "The age of the person in years" | "The age of the person attempting to register" |
| the 8 translations | 6 to 8 say `(< person_age 17) => (not learner_file_created)` | split 3/2/1, 3/2/1 and 5/3: some add `registration_attempted` to the "when" part, some do not, some are no formulas |

The translations are not shown the trigger, but they are shown the
description of every symbol, and "the person attempting to register" invites
the event into the condition. The fourth miss (`brewery_direct`, 1 run of 3)
is a rule whose translations scattered 5/1/1/1 over the sign of the outcome;
there is no cause to act on. One more effect of the same kind does not lose a
conflict: in `musicschool_modified` the new state "a school concert is taking
place" was marked as an event in 2 of 3 runs (never in the full run), so the
planted conflict was found and marked doubtful.

**The change.** The last sentence of `READ_MORE`, "The trigger of a rule may
be a listed event.", is replaced by:

> Read each rule by its own words. The trigger of a rule may be a listed
> event, but only when the words of the rule name that happening; a rule
> whose words name no happening has an empty trigger, also when a listed
> event seems related. Describe a symbol you add by the fact alone, not by a
> listed event ("the brightness of the lamp", not "the brightness of the lamp
> that was switched on").

`eval15/` was written and committed before this change (4883766).

**Results on development data**, the saved-model way, 3 runs per change:

| | `eval14/` before (E20) | `eval14/` now | `eval11/` before (T24) | `eval11/` now |
|---|---|---|---|---|
| planted conflicts found | 50 of 54 | 54 of 54 | 35 of 36 | 36 of 36 |
| doubtful ones set aside | 45 of 54 | 49 of 54 | 32 of 36 | 33 of 36 |
| planted gaps found | 36 of 36 | 36 of 36 | 36 of 36 | 36 of 36 |
| clean changes with a conflict or a gap about them | 0 of 18 | 0 of 18 | 0 of 18 | 0 of 18 |
| new rules that were not accepted | 4 of 108 | 3 of 108 | 3 of 90 | 1 of 90 |
| added state rules that got a trigger (`overlap`) | 3 of 18 | 0 of 18 | 0 of 9 | 0 of 9 |
| other conflicts about a change | 1 | 3 | 0 | 0 |
| requests to the LLM for a change | 9.4 | 9.2 | 9.2 | 9.4 |

- The rule that was lost is now read as in the full run, `(< person_age 17) =>
  (not learner_file_created)`, in 3 of 3 runs, and its conflict is found.
- The rules for an event that the saved model has (`direct`, `gap`, `clean`)
  still get that event as trigger: 72 of 72 on `eval14/`.
- Not changed: a rewritten state rule marked as an event, 5 of 18 on
  `eval14/` before and now (`florist_modified` in 3 runs, as in the full run,
  and `musicschool_modified` in 2). Those planted conflicts are found and
  marked doubtful.
- Two of the three other conflicts about a change are there because the rule
  is no longer rejected: it now takes part in the questions about two
  outcomes (5.7), and one such question gave a fact that sets it against "the
  system charges the learner for the lesson" (1 run each, the kind of
  research.md 4.6).

**Two small things in the same session.**

- *The answer limit of a translation* is now 1,024 tokens, not the default
  4,096 (`TRANSLATE_MAX_TOKENS`); the longest of the 99,452 translation
  answers saved so far has 652 characters. The three development specs give
  the same table as before (T25_specs against T24_specs), and the two runs
  above were made with it. The second model, which needs the room, is tried
  in T26.
- *The wording of a finding that depends on a reading.* The wording prompt
  got a paragraph for it. The check that was planned, wording the saved login
  model again, showed nothing: with today's gap search the saved model has no
  such finding any more. Since T20 a gap that the assumed facts allow is
  looked for first, and with the fact `(>= failed_attempts_count 0)` Z3 now
  shows the gap at 0 failed attempts, which both readings of R3 leave open;
  the report saved in `specs/auth_openspec` showed it at 6. The check is
  moved to the next session, on saved models that do have such a finding.

**Frozen** with the commit of this entry: the new `READ_MORE`, the answer
limit, and the wording paragraph. Next: held-out `eval15/` three ways (E21).

**Raw data.** experiments/results/T25_eval14_incremental.json,
T25_eval11_incremental.json and T25_specs.json, each with its table.

---

## E21 — Held-out `eval15/`: the changed read prompt, and the two ways again (2026-11-25)

**Question.** Do the new sentences of `READ_MORE` (T25) help on projects they
were not written on, and does the saved-model way now find what the full run
finds?

**Setup.** `eval15/` was written first (4883766) and the design frozen in
f0cd5a7. Six OpenSpec projects in new domains (bakery, observatory, bowling
alley, tailor, gliding club, escape room), each with two spec files and seven
existing scenarios, and six changes. `clean`, `direct`, `modified` and `gap`
are as in `eval14/`. The two new ones are aimed at the miss of E20:

| Version | The change | Must report |
|---|---|---|
| `property` | adds a rule about a quantity of the person or thing an existing event is about ("WHEN the bar tab of a player is above 60 euros THEN the system does not hand out any pair of shoes", next to "WHEN a player asks for shoes AND ...") | the conflict with the scenario for that event |
| `status` | the same with a yes/no property ("WHEN a game is a practice game THEN the system does not switch the lane screen on", next to "WHEN a player starts a game THEN the system switches the lane screen on") | that conflict |

The 36 changes were run three ways, 3 times each, in one cluster job (60
minutes): the saved-model way with the new sentences; the saved-model way
with the old sentence (the code of commit 4883766, run from a git worktree);
and the full run.

**Results.**

| | The full run | Saved model, old sentence | Saved model, new sentences |
|---|---|---|---|
| planted conflicts found | 72 of 72 | 71 of 72 | 72 of 72 |
| `property` | 18 of 18 | 17 of 18 | 18 of 18 |
| `status`, `direct`, `modified` | 18 of 18 each | 18 of 18 each | 18 of 18 each |
| planted conflicts, doubtful ones set aside | 69 of 72 | 71 of 72 | 72 of 72 |
| planted gaps found | 18 of 18 | 18 of 18 | 18 of 18 |
| clean changes with a conflict or a gap about them | 0 of 18 | 0 of 18 | 0 of 18 |
| other conflicts about a change | 2 | 0 | 0 |
| new rules that were not accepted | 4 of 126 | 3 of 126 | 4 of 126 |
| requests to the LLM for a change | 68 | 11 | 11 |
| tokens read / written for a change | 31,516 / 27,972 | 5,666 / 4,520 | 5,791 / 4,604 |
| the specs of a project, once | | 62 requests | 60 requests, 27,274 / 24,030 tokens |

- **The new sentences lost nothing and gained one conflict**, 72 against 71.
  The one that the old sentence missed is a run of `bakery_property` in which
  the first of two readings was a mistranslation.
- **They did not change what they were written against.** On `eval15/` the
  read step ties a new rule to a saved event as often with them as without:
  - a saved event as trigger of a `status` rule: 6 of 18 before, 6 of 18
    now. "WHEN a batch of bread is baked for a wholesale customer THEN ..."
    got `bread_taken_out_of_oven`, and "WHEN an observing session is held in
    the lecture room THEN ..." got `guide_starts_observing_session`, in 3 of
    3 runs each, both ways;
  - a new symbol described through a saved event: in `bakery_property`,
    "The number of items in the order being collected", 3 of 3 runs before
    and 3 of 3 now (the full run: "The number of items in the order"). The
    translations then split on whether "an order is collected" belongs to
    the condition, and the rule was ambiguous in 3 of 3 runs both ways (the
    full run: 1 of 3). Its conflict was still found, because the reading
    with more translations was the right one.

  So the gain of T25 on `eval14/` (the rule about "younger than 17") is not
  seen as an effect on other rules.
- **Tying a rule to a saved event also helped once.** In `bakery_status` the
  full run made an event of its own from "is baked" (`bread_baked`), next to
  the saved "a baker takes a batch out of the oven". The planted conflict
  then needs two events at once and was marked doubtful, 3 of 3 runs. The
  saved-model way used the saved event, and the conflict is not doubtful.
- **The saved-model way found what the full run found**: 72 of 72 conflicts,
  18 of 18 gaps, nothing about the clean changes, for 11 requests against 68.
  A change costs more here than on `eval14/` (9) because no change of
  `eval15/` only removes. By kind, in requests: one added scenario 6 to 12
  against 65 to 71, two added scenarios 22 against 80.

**The wording of a finding that depends on a reading** was checked in the same
session, on three saved models that have such a finding with today's code: a
gap with an event (`topup_gap` of E15, worded 3 times), a conflict
(`fuel_direct` of E16) and a gap in which no event happens (a run of
`auth_openspec` from T25). In 5 of 5 the title and the text are about the gap
or the conflict, one sentence says that it exists only with the first
reading and names the other one, and none asks "Which did you mean?". The
first one, as saved in `experiments/examples/topup_reading`:

> **4. Gap (depends on the reading of R4): Unclear PIN lock trigger**
>
> The requirements do not specify what the system must do when a customer
> enters a wrong PIN for the fourth time. This gap exists only if R4 is read
> to mean the account locks strictly when the count reaches three; the other
> reading is that the account locks whenever a wrong PIN is entered and the
> count of consecutive wrong entries is at least three.

**Decision.** The new sentences stay: by the rule set before the test
(plan.md) they had to find at least as many planted conflicts as the old
one, with no fewer gaps and nothing more about clean changes. What they do
not do is written down as a limit (research.md 4.5): the read step still
ties some new rules to saved events, and such a rule comes out ambiguous
more often. The wording paragraph stays. Whether `--incremental` becomes the
default is not decided here: on `eval15/` it found as much as the full run,
on `eval14/` (E20, old sentence) it found 50 against 54. `eval15/` is
development data from now on; the next design needs `eval16/`.

**Raw data.** experiments/results/E21_eval15_full.json,
E21_eval15_incremental_before.json and E21_eval15_incremental.json, each with
its table; experiments/examples/topup_reading.

---

## T26 — The second model on the spec of 100 requirements (2026-11-25)

**Question.** In E14 the second model (step 7) could not run on the spec of
100 requirements: its server takes 6,144 tokens for prompt and answer, a
translation prompt with the 206 symbols of that spec has 4,234, and every
request reserved 4,096 for the answer. With the answer limit of a translation
at 1,024 tokens (T25), does it run, and what does it report?

**Setup.** The first saved run of each of the four versions of
`experiments/sets/size2` (E14), so 4 formal models and 400 rules. The second
model translates every rule 8 times (`--rescore ... --second-base-url`). One
cluster job with the second model.

**Results.**

- **It runs.** No request failed. 396 of the 400 rules got 7 or 8 answers
  (the other 4 had been rejected in step 3 and are not asked about). The four
  models took 9 minutes.
- **It flags many more rules, as on the small specs.** None of the 100
  requirements has a planted ambiguity, so every flag is on a rule we wrote
  to be clear:

  | | Without the second model | With it |
  |---|---|---|
  | planted conflicts found (2 versions) | 2 of 2 | 2 of 2 |
  | ambiguity flags on the clean version (100 rules, 1 run) | 2 | 9 |
  | ambiguity flags on the other three versions | 10 | 46 |

  That is about 14 flags for 100 rules, against 3. On the small specs the
  second model also raised about twice as many flags as the main model alone
  (E9, E12); here it is four times as many, on one run.

**What it means.** The second model can now be used on a long spec. Whether
it should be is another matter: a report with a dozen questions about clear
rules is a lot to read. One run of one document, so a first sign.

**Raw data.** experiments/results/T26_size2_second.json and its table.

---

## E22 — A larger project, and one change that does everything at once (2026-11-25)

**Question.** Every change of `eval11/` to `eval15/` does one thing to a
project of 7 to 9 scenarios. Does the check still work when the project is
larger and one change adds, rewrites, removes and renames at the same time?

**Setup.** `mixed/` was written and committed before it was run (4f33e59); no
design change goes with it. One invented project, a city marathon: four spec
files (`registration`, `race-day`, `results`, `volunteers`), 28 requirements,
39 scenarios. The specs have one conflict from before the change ("publishes
the finish time" against "does not publish any finish time" while a protest
is open). One change, `rules-for-next-season`, touches three of the four
files:

| The change... | Planted about it |
|---|---|
| adds "Charity places", with both of its cases | nothing |
| adds "No refunds": "WHEN a runner withdraws from the race THEN the system keeps the entry fee", next to "... refunds the entry fee" | conflict |
| adds "Unpaid fees": "WHEN the entry fee of a runner is unpaid THEN the system does not hand out any bib", against a scenario of the other spec file | conflict |
| adds "Pacers", with one of two cases | gap |
| rewrites "Heat warning": "... and does not open any start gate" | conflict |
| rewrites "Certificates": one scenario gets a harmless addition, the other is word for word the same | nothing |
| rewrites "Payment": the scenario "payment not accepted" is gone | gap |
| removes "Registration when full", one of two cases | gap |
| removes "Transfers", the only requirement for its event | nothing |
| renames "Corrections" to "Time corrections" | nothing |

Both ways, 3 runs each, and the tool itself once each way, in one cluster job
(26 minutes).

**Results.**

| | The full run | On a saved model (`--incremental`) |
|---|---|---|
| planted conflicts found (3 in each of 3 runs) | 9 of 9 | 9 of 9 |
| planted gaps found | 9 of 9 | 9 of 9 |
| gaps about the change, all | 9 | 9 |
| other conflicts about the change | 0 | 0 |
| the old conflict: found / shown as the change's | 3 of 3 / 0 of 3 | 3 of 3 / 0 of 3 |
| ambiguity flags on rules of the change | 0 | 0 |
| labels kept | 3 of 3 runs | 3 of 3 |
| planted conflicts found without assumed facts and links | 6 of 9 | 6 of 9 |
| requests to the LLM for the change | 346 | 83 |
| tokens read / written | 294,295 / 143,584 | 57,434 / 38,823 |
| the specs of the project, once | | 336 requests, 263,239 / 134,682 tokens |

- **Everything planted was found, and nothing else was reported about the
  change**, both ways. The gaps about the change are exactly the three
  planted ones in every run: the removed event, the addition with both
  cases, the harmless rewording and the rename gave no gap and no conflict.
- **The two gaps that come from a removal say so** ("opened by removing X1",
  "opened by removing X2"), also the one whose scenario was dropped inside a
  rewritten requirement.
- **"Refunds" against "keeps the entry fee" needs an assumed fact** in all
  runs (3 of the 9 conflicts); the other two are proven from the rules alone.
- **Cost.** One run of 41 rules takes 346 requests, about 2.5 minutes for
  each of three runs in parallel. The saved-model way takes 83 requests for
  the change, a quarter. That is more for each new rule than on the small
  projects (9 to 11 for one rule), because every new rule is asked about
  together with many old ones (5.7).
- **The tool's own run, the full way** (`experiments/examples/marathon_mixed`)
  shows one more conflict: "assigns a bib number" (registration) against
  "does not hand out any bib" (the new rule), marked "if the assumed facts
  hold". It rests on a link that restates "assigns a bib number" as "hands
  out the bib", which is wrong, and which the report quotes. So an unplanted
  conflict about the change appeared in 1 of the 4 full runs made.

One project, 3 runs each way: it shows that the pieces work together, not how
often.

**Raw data.** experiments/results/E22_mixed_full.json and
E22_mixed_incremental.json, each with its table;
experiments/examples/marathon_mixed and marathon_mixed_incremental (the
reports).

---

## E23 — A real OpenSpec project, first batch (2026-11-25)

**Question.** Every number so far is on specs we wrote. What does the change
check do on a real project?

**The project.** The OpenSpec tool keeps its own specs in its own format
(github.com/Fission-AI/OpenSpec, MIT licence, cloned at f1cd852 without
checking its files out; only its Markdown specs were read). It has 44 spec
files with 395 KB of text, and 108 archived changes from 2025-08 to 2026-10,
98 of them with spec deltas.

**Setup** (experiments/real/). The project is far too large to formalize as
one document, so each change is checked against the spec files it touches,
as they were in the commit before the change was archived:

1. `history.py` finds, for each archived change, the commit that archived it,
   and writes the change next to the touched spec files of the commit before.
2. `merge_check.py` applies each change with our merge, no LLM.
3. `batch.py` takes the pool (our merge accepts the change; at least 5
   scenarios before it; at least one scenario added or reworded; at most 60
   scenarios after), 48 changes, and of those every third in date order: 16.
4. The 16 were run the full way, once each (21 minutes). There is no planted
   answer; the findings were read by hand.

**What the merge does on real files** (no LLM).

- 93 of the 98 changes merge. 5 are refused: a MODIFIED or ADDED section
  names a requirement that the spec does not have, or already has.
- 39 commits archive the 108 changes, up to 23 at once. For the 24 changes
  that were archived alone and can be compared, our merge gives the same
  scenarios as the project's own result in 17. Two of the other 7 were
  looked at: in one the final spec does not match the archived delta (it was
  edited by hand), in the other our parser puts scenarios under the wrong
  requirement in a file with an unusual layout.

**What the run did.**

| | |
|---|---|
| runs that stopped | 5 of 16 |
| rules in the 11 runs that finished | 366 |
| of them accepted / ambiguous / rejected | 219 / 79 / 68 |
| rules of the changes: accepted / ambiguous / rejected | 43 / 17 / 25 |
| conflicts about the change | 29, in 3 of the 11 changes |
| of them proven from the rules alone | 3 |
| of them resting on a fact from a question about two outcomes | 26 |
| gaps about the change | 10, in 6 changes |
| changes with an ambiguity about them | 7 of 11 |
| changes with nothing reported about them | 3 of 11 |
| conflicts among the existing rules alone, not shown | 39 |
| requests to the LLM for a change | 140 (188,311 tokens read, 94,283 written) |

- **Five runs stopped.** Three stopped on a missing label. The spec shows its
  own format in a code block ("#### Scenario: Short name", "- **WHEN** ..."),
  our parser took that header for a scenario, the model rightly left it out,
  and the run refuses a missing label. This is fixed (`change._marked`:
  headers in a code block are text). Two stopped because the model made a
  symbol or a value with a name that is not a word (".claude", "add-auth"),
  three times in a row.
- **40% of the rules did not get an agreed translation**, against about 3% on
  our sets (4 of 126 new rules in E21). A real scenario has several outcomes
  ("THEN ... AND ... AND ..."), quoted commands and file names, and the eight
  translations differ in what they keep. Not looked into further.
- **Nearly all conflicts come from the questions about two outcomes.** A real
  spec has a general rule and its special cases side by side: "WHEN using the
  legacy list command THEN continue to work as before ..." and "WHEN no
  active changes exist THEN display: 'No active changes found.'". Asked
  whether both outcomes can hold, the model says no ("a list cannot be
  displayed if no active changes are found"), and that fact makes a conflict
  of every such pair: 12 in one change, 14 in another. Four of the 26 were
  read; all four are of this kind. Each says "if the assumed facts hold" and
  quotes the fact.
- **The three conflicts from the rules alone look real.** One requirement
  says "WHEN `$SHELL` contains `bash` in the path THEN detect shell as
  `bash`", the next "WHEN `$PSModulePath` environment variable is present
  THEN detect shell as `powershell`". Nothing says which wins when both hold
  (PowerShell started from a bash login). The third pair, bash against fish,
  is the same form and far-fetched.
- **The gaps were not judged.** Each lists every other event as FALSE, 20 to
  40 lines here, which makes them hard to read (the limit of E14).

**What it means.** On a real project the check, as it is, does not hold up:
a third of the runs stop, two rules in five have no agreed translation, and
most of what is reported is the known weakness of one step (research.md
4.6), much stronger here than on our sets. One finding is the kind the tool
is for. This is 16 changes of one project, read once.

**Raw data.** experiments/results/E23_real_batch1.json and its table; the 16
cases are in experiments/sets/real1. The scripts are in experiments/real/.

---

## T27 — Why two real rules in five get no agreed translation (2026-11-25)

**Question.** In E23, 147 of 366 rules were ambiguous or rejected, against
about 3% on our sets. Why?

**Method.** No LLM: `experiments/real/translations.py` reads the eight saved
translations of every rule of E23 and compares their parts with Z3. The same
script on two of our own runs, for contrast.

**The short answer.** The eight translations must use the symbols that the
read step listed once, for the whole document. On our specs a rule demands
one thing and the list has one symbol for it. On the real specs the list
does not fit the rules: for some outcomes it has no symbol, for others it has
several that overlap. Both come from the read step, not from the translation.

**In what the translations of the 147 rules differ** (the first that fits):

| | Rules | |
|---|---|---|
| different symbols for what is demanded | 73 | the list has several symbols for one outcome, and the eight pick different ones |
| no symbol for what is demanded | 50 | some translations then demand nothing: `... => true` |
| only the condition differs | 16 | |
| the same symbols, combined differently | 7 | "and" against "or", a condition inside the outcome |
| too few usable answers | 1 | |

So for 131 of the 147 the disagreement is about what the rule demands, and
for 123 it is about which symbols to use.

- **Several symbols for one outcome.** "WHEN shell path indicates an
  unsupported shell THEN throw error: \"Shell '<name>' is not supported. ...\""
  has `error_thrown` and `unsupported_shell_error_displayed`: 6 translations
  use the first, 2 use both. "... THEN authors SHALL use `### Requirement: ...`
  followed by at least one `#### Scenario: ...` section" has a symbol for each
  heading and one for the whole (`uses_structured_spec_format`): 4 use the
  two parts, 2 all three, 1 the whole alone. The same happens to conditions:
  `executing_install_zsh_no_omz` next to `executing_install_zsh` and
  `oh_my_zsh_installed`.
- **No symbol for the outcome.** "WHEN user runs `openspec templates --schema
  tdd` THEN the system displays template paths for the specified schema"
  came out as `templates_command_run => true` in 8 of 8, and was accepted.
  The model understood the rule; its reading says "the system must display
  the template paths for the specified schema". There is no symbol for that,
  and the translation may use listed symbols only.
- **The read step lists too few symbols for a real spec.** A real rule
  demands 2.2 things on average ("THEN a AND b AND c"), ours 1. The read step
  listed 2.6 symbols for each real rule and 2.1 for each of ours. Counting
  the symbols that are not events against the outcomes:

  | | Symbols per outcome | Rules whose chosen translation demands nothing |
  |---|---|---|
  | our long spec (100 requirements, E14) | 1.4 | 0 of 1,203 |
  | our mixed project (E22) | 1.6 | 0 of 132 |
  | the 7 real specs with 0.9 or more | 0.9 to 1.25 | 7 of 222 |
  | the 4 real specs with fewer | 0.4 to 0.7 | 68 of 144 |

  In two real specs it listed 33 and 25 such symbols for 82 and 41 outcomes,
  and 43 of 51 and 20 of 33 of their rules demand nothing.
- **Empty rules are counted as accepted.** 75 of the 366 rules have a chosen
  translation that demands nothing, and 45 of those were accepted, because
  the eight agree on `true`. With the 147, that makes 192 of 366 rules, about
  half, that give the checks nothing to work with.
- **More answers are not formulas**: 142 of 2,920 (4.9%), in 77 rules, mostly
  `and a b` without the outer parentheses. On our sets it is 0.1 to 0.9%.
  The facts vote repairs this slip (T19); the translations are not repaired.

**What it is not.** Not the number of outcomes by itself: of the 136 real
rules with one outcome, 34% have no agreed translation. Not the quoted
commands and file names: rules with them agree more often (64%) than rules
without (50%). Not the length of the symbol list: our mixed project has as
many symbols as a real spec, and 1 rule in 132 without agreement.

**What follows** (nothing is built; each needs a held-out set first):

1. A rule whose chosen translation demands nothing should not be accepted.
   It should be reported as a rule that could not be expressed. This needs no
   LLM and changes nothing on our sets, where there is no such rule.
2. The symbols should be made next to the rule that needs them: read a spec
   one requirement at a time, each time with the symbols so far, as
   `--incremental` already does for a change. That also lifts the limit of
   about 140 scenarios.
3. For overlapping symbols: either ask, after reading, which symbols say the
   same thing or include one another, or tell the translation to state
   everything the rule demands.
4. Repair the parentheses of a translation as for a fact.

**Raw data.** The saved run of E23; the script is
experiments/real/translations.py.

---

## T28 — Development: a rule that demands nothing, and reading in pieces (2026-11-25)

**Question.** T27 found that the symbols of the read step do not fit real
rules. Two remedies are built (plan.md 2.1). Do they do what they are meant
to, and what do they cost on our own documents?

**The two changes.** `eval16/` was written and committed first (cc0396f).

1. *A rule that demands nothing is rejected.* In step 3, if the "then" part
   of the chosen translation is always true, the rule gets the status
   "rejected" and the mark `empty`, whatever the agreement of its
   translations. The report lists it as "Not checked", and counts it apart
   from the ambiguities.
2. *A long document is read in pieces.* A document of more than 2,500
   characters is cut at its headings into pieces of about that size
   (`formalize._pieces`): a section stays whole if it fits and is cut at its
   sub-headings if not, parts that follow each other are put together again
   while they fit, and a part of a few lines goes with its neighbour. The
   first piece is read as before. Every later piece is read with the symbols
   so far, by the read of `--incremental` (`READ_MORE`). Our specs up to
   `eval15/` are shorter and are read in one piece, as before.

**The first real batch** (the 16 changes of E23, one run each):

| | Before (E23) | Now |
|---|---|---|
| runs that finished | 11 of 16 | 12 of 16 |
| pieces for a document | 1 | 3 to 13 |
| symbols that are not events, for each outcome | 0.40 to 1.25 | 0.78 to 1.93 |
| rules | 366 | 411 |
| accepted / ambiguous / rejected | 219 / 79 / 68 | 242 / 86 / 83 |
| chosen translation demands nothing | 75, of them 45 accepted | 7, none accepted |
| **rules of no use to the checks** (no agreed translation, or one that demands nothing) | **192 of 366 (52%)** | **169 of 411 (41%)** |
| without agreement because there is no symbol for the outcome | 50 | 12 |
| ... because the translations use different symbols | 73 | 106 |
| ... because only the condition differs | 16 | 43 |
| conflicts / gaps about a change | 29 / 10 | 25 / 5 |
| requests to the LLM for a change | 140 | 179 |

- **Reading in pieces gives the rules their symbols.** The spec that had 33
  symbols for 82 outcomes now has 158, and the rules that demand nothing fell
  from 75 to 7.
- **It does not make the translations agree.** As many rules are accepted as
  before (59%, 60%). What was lost to a missing symbol is now lost to a
  choice among symbols: with more symbols there are more that overlap (106
  rules, 73 before), and more conditions differ (43, 16 before).
- **Four runs stopped, with other causes than before.** Three of the five
  stops of E23 were our parser's (fixed since). Now three runs stop because
  one of the read answers has an unusable symbol list (a name declared
  twice, an enum with one value, a name that is not a word), and one because
  a label came back changed ("R5b"). With one read answer for each piece
  there are more answers that can go wrong.

**Our own longer documents.**

| | Before | Now |
|---|---|---|
| `mixed/` (3 runs): planted conflicts, planted gaps | 9 of 9, 9 of 9 (E22) | 9 of 9, 9 of 9 |
| other conflicts about the change | 0 | 4 |
| the old conflict marked doubtful | 0 of 3 | 3 of 3 |
| the spec of 100 requirements: planted conflicts, planted gap | 6 of 6, 3 of 3 in 12 runs (E14) | 2 of 2, 1 of 1 in 4 runs |
| unexpected conflicts | 2 in 12 runs | 4 in 4 runs |

- Everything planted is still found.
- **A state is read as an event in a later piece.** "WHEN a protest against a
  result is open THEN ..." got the trigger `protest_open` in 3 of 3 runs. The
  old conflict of `mixed/` then needs two events at once and is marked
  doubtful. This is the weakness of the read of `--incremental` (research.md
  4.5), which now reads every piece but the first.
- **More conflicts that nobody planted.** In `mixed/`, 3 of the 4 are one
  pair, set against each other by a question about two outcomes ("a runner
  cannot be cleared to start if the start gate is not opened"), in 3 of 3
  runs; it was not there in E22.

**The three development specs** are read in one piece, and no rule of theirs
was marked empty. 13 of 15 planted conflicts were found, 15 of 15 in T25:
`delete_property` and a rejected rule of the login spec, the variation
between runs that these specs have always had.

**The wording of a rule that demands nothing** was read for two real ones:
"Not checked: ...", the reason, no question, and a proposal to state one
observable outcome.

**Also in this session.** The server did not start twice: another account's
process held 15 GiB on one of the two GPUs. `serve.sbatch` can now be asked
for a smaller share of the memory (`GPU_MEMORY=0.75`).

**Frozen** with the commit of this entry: the two changes as described.
Development shows a gain on real specs and a cost on our own long ones; the
held-out runs (E24) decide by the rule of plan.md 2.1.

**Raw data.** experiments/results/T28_mixed.json, T28_size2.json,
T28_specs.json and T28_real_batch1.json, each with its table.

---

## E24 — Held-out: rules that demand nothing, and reading in pieces (2026-11-25)

**Question.** Do the two changes of T28 help on specs they were not built on?

**Setup.** `eval16/` was written first (cc0396f) and the design frozen in
bcc1ff5. Two held-out sets, each run with the design before the two changes
(the code of cc0396f, from a git worktree) and after them:

- `eval16/`: six specs written like real tool specs (a backup tool, a
  package registry, a log shipping agent, a thumbnail service, a build
  runner, a file sync client), 14 scenarios each, most with two or three
  outcomes, in a clean, a direct, an overlap and a gap version. 2 runs each.
- `real2/`: the second batch of the real project, 16 archived changes that
  had not been run. 1 run each. Its "before" arm was run twice, because the
  first result was overwritten by a mistake in the session script; the
  numbers that the first run printed are given too.

**The real batch** (`real2/`):

| | Before, first run | Before, second run | After |
|---|---|---|---|
| runs that finished | 15 of 16 | 14 of 16 | 13 of 16 |
| rules | 437 | 414 | 369 |
| accepted | 201 (46%) | 223 (54%) | 205 (56%) |
| chosen translation demands nothing | 47, of them 13 accepted | 23, of them 3 accepted | 12, none accepted |
| **rules of no use to the checks** | **249 (57%)** | **194 (47%)** | **164 (44%)** |
| rules the checks can use | 188 | 220 | 205 |
| without agreement: no symbol for the outcome | 68 | 43 | 19 |
| ... different symbols | 108 | 110 | 92 |
| ... only the condition | 54 | 30 | 38 |
| conflicts about a change | 9 | 10 | 31 |
| gaps about a change | 9 | 6 | 5 |
| requests to the LLM for a change | 126 | 133 | 155 |

- **The rejection of empty rules does what it should.** No rule that demands
  nothing is accepted any more (13 and 3 before).
- **Reading in pieces makes the symbols** (19 rules without a symbol for
  their outcome, 68 and 43 before) **but the gain in usable rules is within
  the difference between two runs of the old design**: 44% of no use, against
  57% and 47%. In rules that the checks can use it is between the two (205;
  188 and 220), because one more run stopped.
- **More runs stop**: 3, against 1 and 2. Every stop, in all three runs, is a
  read answer with an unusable symbol list: a name or a value that is not a
  word (`.claude`, `spec-driven`, `change:apply`), a name declared twice, an
  enum with one value. With one read answer for each piece there are more of
  them.
- **Three times as many conflicts about a change** (31; 9 and 10). All but one
  rest on an assumed fact.

**`eval16/`** (24 spec versions, 2 runs each):

| | Before | After |
|---|---|---|
| runs that finished | 42 of 48 | 40 of 48 |
| planted conflicts found | 19 of 22 | 19 of 20 |
| ... doubtful ones set aside | 16 of 22 | 15 of 20 |
| planted gaps found | 10 of 10 | 10 of 10 |
| clean runs with a conflict | 8 of 10 | 7 of 10 |
| ... doubtful ones set aside | 4 of 10 | 3 of 10 |
| conflicts that were not planted, for one run | 5.0 | 2.1 |
| ambiguity flags on clean specs | 7 | 2 |
| rules accepted | 577 of 600 (96%) | 550 of 570 (96%) |
| rules whose chosen translation demands nothing | 1 | 6, all rejected |

- **What was planted is found either way**, and the gaps too.
- **Every run that stopped did so for a value that is not a word**: the
  status `timed out` of the build runner (its spec finished 3 of 8 runs
  before and none after), and the status 201 of the registry. That is 6 and 8
  of 48 runs.
- **`eval16/` does not show the translation problem of the real specs.** 96%
  of its rules are accepted, both ways. Two or three outcomes in a scenario
  are not what makes a real spec hard; ours are still too regular.
- **Its clean versions are not clean, by our own fault.** We wrote rules that
  cut across the others ("more than 100 requests in a minute: status 429",
  "an upload grows beyond 50 megabytes: status 413", "a job passes 60 minutes:
  `timed out`"), and each clashes with the ordinary case it overlaps. The
  registry alone has 36 such conflicts in its 2 clean runs before. So "clean
  runs with a conflict" on this set counts fair findings and artefacts
  together, and only the comparison of the two columns means something.
- **The conflicts that were not planted fall with reading in pieces** on this
  set (5.0 to 2.1 for a run), mostly in the registry, where the statuses got
  symbols of their own in the pieces. On `mixed/` and on the real batch they
  rise (T28, above). No clear direction.

**Decision**, by the rule of plan.md 2.1.

- *A rule that demands nothing is rejected*: **stays.** It changes nothing
  where there is no such rule, and on real specs it stops calling an empty
  rule accepted.
- *A long document is read in pieces*: **taken out.** The rule asked for
  fewer rules without a usable translation and no more runs that stop. More
  runs stop (3 of 16 against 1 and 2; 8 of 48 against 6), and the gain in
  usable rules on the held-out batch is no larger than the difference
  between two runs of the old design. It also costs on our own long
  documents (T28: conflicts that nobody planted, a state read as an event).
  The code is in commit bcc1ff5.

What reading in pieces showed is kept as a finding: the read step can be
made to give a real rule its symbols (0.8 to 2.3 for each outcome, 0.2 to
1.25 in one answer), and that is not enough, because the translations then
disagree over which of the symbols to use.

**What stops a run on such specs** is now the first thing in the way: a name
or a value that is not a word. It stopped 6 to 19% of the runs here, in both
designs.

`eval16/` and `real2/` are development data from now on; the next design
needs `eval17/`.

**The machines.** The login `fmi0` on the GPU node sees three GPUs that the
queue does not manage. The "before" arm of the real batch ran there, on a
server started with `experiments/slurm/serve_direct.sh`, next to the cluster
job.

**Raw data.** experiments/results/E24_eval16.json, E24_eval16_before.json,
E24_real_batch2.json and E24_real_batch2_before.json (its second run), each
with its table. The real cases are in the repository now:
experiments/sets/real1 (the batch of E23 and T28) and real2, with the
licence of the project they come from; the raw data of E23 and T28 too.

---

## T29 — Development: a symbol list with a name that is not a word (2026-11-25)

**Question.** On specs written like real ones a run often stops in the read
step: the symbol list cannot be used, three times in a row. Can our code
repair the list?

**What stops a run.** In the 179 runs of E23, T28 and E24, 28 stopped: 4 for
a label that the read step did not keep (3 of them our parser's fault, fixed
in E23), and 24 for the symbol list:

| What is wrong with the list | Runs | Examples |
|---|---|---|
| a name or a value that is not a word | 20 | `timed out` (13 times), `change:apply`, `.claude`, `add-auth`, 201, `spec-driven`, `Asia/Shanghai` |
| a name declared twice | 2 | the value `zsh` of one symbol and a symbol `zsh` |
| an enum with fewer than two values | 2 | |

All 20 are values of an enum that the document gives in quotes: the model
keeps the spelling of the document.

**The change** (`formalize._usable`, no prompt changes). `eval17/` was written
and committed first (8ad8d6e). Before the list is checked:

1. a name or a value that is not a word is made one: every character that is
   not a letter, a digit or "_" becomes "_" (`timed out` to `timed_out`); one
   that would start with a digit gets the name of its symbol in front (201 to
   `answer_status_201`);
2. a value that is also the name of a symbol, or a value of an earlier
   symbol, gets the name of its symbol in front; of two symbols with one name
   the first stays;
3. an enum with fewer than two values becomes a yes/no symbol;
4. a trigger that names a renamed symbol is renamed with it.

The repair leaves all 3,897 symbol lists of the saved runs, examples and
development specs as they are, so no earlier result can move.

**Results on development data.**

| | Before | With the repair |
|---|---|---|
| `eval16/` (2 runs of 24 specs): runs that finished | 42 of 48 (E24) | 48 of 48 |
| planted conflicts found | 19 of 22 | 24 of 24 |
| planted gaps found | 10 of 10 | 12 of 12 |
| clean runs with a conflict, doubtful ones set aside | 4 of 10 | 3 of 12 |
| the second real batch: runs that finished | 14 and 15 of 16 (E24) | 16 of 16 |
| its rules of no use to the checks | 47% and 57% | 60% |

- **Every run finishes.** The build runner of `eval16/`, which finished 3 of
  8 runs, now has `status_reported: Enum {queued, skipped, failed, passed,
  timed_out, cancelled}` and finishes 8 of 8, with its two planted conflicts
  found in 4 of 4 runs.
- **More conflicts are counted on `eval16/`** (403 that were not planted, 211
  before), because that spec now runs: every pair of its rules that report a
  status clashes when the two events happen at once. They are marked
  doubtful, and with those set aside 24 are left (48 before).
- **The real specs that used to stop are hard ones.** With them in, 60% of
  the rules of the batch are of no use to the checks. The repair lets a run
  finish; it does not make its rules translatable (research.md 4.8).

**Frozen** with the commit of this entry. Next: held-out `eval17/` with the
code before and after (E25).

**Raw data.** experiments/results/T29_eval16.json and T29_real2.json, each
with its table.

---

## E25 — Held-out `eval17/`: the repair of the symbol list (2026-11-25)

**Question.** Does the repair of T29 let specs run that it was not built on,
and is what we planted in them found?

**Setup.** `eval17/` was written first (8ad8d6e) and the design frozen in
83328d5. Six specs of 10 scenarios (a deployment tool, an issue tracker, a
DNS service, a payment gateway, a mail queue, a feature-flag service), each
with states, codes, regions or labels in quotes that are not words
(`rolled back`, `in review`, `pending-sync`, `auth-only`, `50-50`,
`kind:bug`, 402), in a clean, a direct, an overlap and a gap version. 2 runs
each, with the code before the repair (commit 8ad8d6e, from a git worktree,
on the workstation login) and after it (on the cluster), at the same time.

**Results.**

| | Before | With the repair |
|---|---|---|
| **runs that finished** | **7 of 48** | **48 of 48** |
| planted conflicts found | 4 (of the 4 in the runs that finished) | 22 of 24 |
| planted gaps found | 2 (of 2) | 10 of 12 |
| clean runs with a conflict, doubtful ones set aside | 0 of 1 | 0 of 12 |
| conflicts that were not planted and not marked doubtful | 0 | 3 |
| rules accepted | 72 of 72 | 462 of 492 (94%) |

- **Without the repair five of the six specs never run.** All 41 stops are a
  value that is not a word: `rolled back` and `eu-west` (deployment),
  `pending-sync` (DNS), `rule-match` (flags), `in review` and `kind:bug`
  (issues), `auth-only` (payments), `spam-quarantine` (2 of the 8 runs of
  the mail queue, the only spec that mostly ran).
- **With it every run finishes**, and 22 of the 24 planted conflicts and 10
  of the 12 planted gaps are found. On the mail queue, which ran both ways,
  the result is the same (4 of 4 conflicts).
- **What is missed is the usual translation trouble, not the names**: "starts
  the transfer AND sets the domain state to `transfer-out`" was rejected in
  one run (its translations scattered), and "returns the amount to the card"
  was written as an amount in some translations and as a yes or no in
  others (one conflict missed, and the gap of that spec in 2 of 2 runs).
- **The clean specs are clean this time**: with the doubtful conflicts set
  aside, none of the 12 clean runs reports a conflict. Counted with them
  there are 163 conflicts that were not planted: rules for different
  commands that set the same state ("sets the release state to ...") clash
  when two commands are run at the same moment. All but 3 are marked
  doubtful.

**Decision.** The repair stays: the rule of plan.md 2.1 asked for fewer runs
that stop, and for what is planted to be found no less often in the runs
that finish. `eval17/` is development data from now on; the next design
needs `eval18/`.

**Raw data.** experiments/results/E25_eval17.json and E25_eval17_before.json,
each with its table.

---

## T30 — Development: the translations of a rule vote (2026-11-26)

**Question.** On real specs about half of the rules without an agreed
translation are lost to the choice of symbols (T27): the read step lists a
general and a specific symbol for one outcome, and the eight translations use
different ones. Can the rule be kept with what the translations share?

**The change** (`formalize._vote`, in step 3; no prompt changes). `eval18/`
and `real3/` were written and committed first (bccfaf5).

```
"WHEN move succeeds THEN display success message with archived name and list of updated specs"
3 x  move_succeeds => success_message_displayed
2 x  move_succeeds => (and success_message_displayed spec_summary_displayed)
1 x  move_succeeds => (and success_message_displayed specs_updated)
1 x  move_succeeds => (and success_message_displayed updated_specs_tracked spec_summary_displayed)
```

1. The vote is taken for a rule whose translations do not agree (ambiguous
   or rejected), and only if no two translations that use the same symbols
   differ in meaning. Two translations with the same symbols and two
   meanings ("= 5" and ">= 5") are two readings of the words: the rule stays
   a question to the author.
2. Our code asks Z3, for each translation, which of the others entail it.
   The strongest translation that more than half of the usable ones entail
   is chosen, and the rule is accepted with it (`"voted": "7/7"` above, for
   the first line). With no such majority the rule stays as it was.
3. A chosen translation that demands nothing rejects the rule as empty
   (T28).

**First on the saved runs** (no LLM; step 3 judged again on the translations
that are in the result files):

| Saved run | Rules accepted before | With the vote | Planted ambiguities that step 3 flags | Accepted by the vote |
|---|---|---|---|---|
| second real batch (T29) | 197 of 487 (40%) | 330 (67%) | | |
| first real batch (E23, before empty rules were rejected) | 219 of 366 (59%) | 246 (67%) | | |
| `eval16/`, `eval17/` | 95%, 93% | 97%, 94% | | |
| `eval7/` to `eval10/`, `eval12/` | 91 to 96% | 92 to 96% | 72 | 5 (3 in `eval7/`, 2 in `eval12/`) |

Without the condition of point 1 the vote would accept 30 of those 72: a
rule that splits 5 to 3 between "= 5" and ">= 5" has a majority too.

**Results on development data** (new runs with the vote):

| | Before | With the vote |
|---|---|---|
| second real batch: rules of no use to the checks | 60% (T29); 47% and 57% (E24) | 110 of 487 (23%) |
| the same translations, judged by the step 3 of before | 255 accepted (52%) | 377 accepted (77%) |
| its conflicts about a change | 13, in 6 of 16 changes | 20, in 8 of 16 |
| `eval17/` (2 runs of 24 specs): planted conflicts, planted gaps | 22 of 24, 10 of 12 (E25) | 22 of 24, 11 of 12 |
| `eval8/` (3 runs of 30 specs): planted conflicts, planted gaps | | 18 of 21, 17 of 18 |
| `eval7/` (3 runs of 24 specs): planted conflicts | | 17 of 18 |
| planted ambiguities of `eval8/` and `eval7/` that the step 3 of before flags on the same translations | 12 and 21 | 11 and 20 |
| the three development specs: expected conflicts | | 14 of 15 |

- **On the real batch three rules in four are now of use to the checks.**
  134 rules were voted on (79 were ambiguous, 55 rejected); 122 are accepted
  and 12 demand nothing. Of the 122, 28 have every usable translation behind
  them and 24 have five of eight.
- **What the vote picks is the common core.** "WHEN user specifies an
  unknown schema THEN the system displays an error listing available
  schemas" split 4 to 4 between `available_schemas_listed` and `(and
  error_displayed available_schemas_listed)`; it is accepted with the first,
  which all eight entail. So a voted rule can say less than its words.
- **More rules give more findings**: 20 conflicts about a change where there
  were 13. We did not read them all. The first two are of a kind we know,
  two rules that can apply at once ("WHEN target archive already exists THEN
  fail" against "`archive --skip-specs` ... proceed directly to moving the
  change"), and both are marked doubtful.
- **Two planted ambiguities are lost**, one in each set. "WHEN a bill has
  been unpaid for 30 days" was flagged before only because one translation
  of seven used another symbol; all seven read it as "30 or more". "A car is
  free ... or the employee is a manager and the trip is longer than 100 km"
  split 5 to 2, and the two used other symbols. Both were then asked about
  in step 6, and the answers sided with the translation.
- **On our own sets little moves**: 2 rules voted on in `eval8/`, 10 in
  `eval7/`, 5 in `eval17/`.

**Frozen** with the commit of this entry (831254e). Next: held-out `eval18/`
and `real3/` with the code before and after (E26).

**Raw data.** experiments/results/T30_real2.json, T30_eval17.json,
T30_eval8.json, T30_eval7.json and T30_specs.json, each with its table.

---

## E26 — Held-out `eval18/` and a third real batch: the vote (2026-11-26)

**Question.** Does the vote of T30 make more rules usable on real changes it
was not built on, and what does it cost in planted ambiguities?

**Setup.** `eval18/` and `real3/` were written first (bccfaf5) and the design
frozen in 831254e. The code before the vote (commit 1732c04, from a git
worktree, on the cluster) and after it (on the workstation login) ran at the
same time.

- `eval18/`: six specs of 7 scenarios written like tool specs (a secrets
  tool, a job scheduler, a webhook service, a linter, a migration tool, a
  paging service). Each is clean, has a planted conflict, a planted gap, and
  two planted ambiguities: a limit ("reaches 90 days"), and one of "only
  if", an "if" after two outcomes, or "and ... or ... and". 3 runs each.
- `real3/`: the 16 changes of the real project's pool that were not run yet,
  526 rules. 2 runs each, to see how much two runs differ.

**Results on `real3/`** (the two runs of each arm side by side).

| | Before | With the vote |
|---|---|---|
| runs that finished | 32 of 32 | 32 of 32 |
| rules accepted | 45% and 37% | 71% and 63% (155 and 148 of them by the vote) |
| **rules of no use to the checks** | **54% and 62%** | **28% and 36%** |
| conflicts about a change | 22 and 18 | 34 and 44 |
| of them not marked doubtful | 12 and 11 | 12 and 18 |
| changes with such a conflict | 3 and 4 of 16 | 4 and 6 of 16 |
| gaps about a change | 15 and 20 | 15 and 11 |
| questions about an ambiguous rule of a change | 43 and 40 | 21 and 24 |
| rules of a change reported as not checked | 7 and 11 | 10 and 13 |

- **A quarter more of the real rules take part in the checks.** The two runs
  of one arm differ by 8 points, the two arms by 26.
- **What is left** (341 of the 1,052 rules of both runs, 617 before): for 179
  there is no symbol for what the rule demands (220 before); for 127 the
  translations use different symbols and the vote did not settle it (272);
  for 23 the same symbols are combined differently, which is not voted on
  (13); for 11 only the condition differs (111).
- **The author is asked half as often** about a rule of the change (45
  questions in two runs, 83 before).
- **More rules give more conflicts**: 30 that are not doubtful in the two
  runs, 23 before. 24 of the 30 involve a voted rule. The five we read set a
  rule for the normal case against a rule for a failure that can happen at
  the same time ("WHEN ... the user runs `openspec schemas --json` ... list
  schemas from the store" against "WHEN ... store resolution fails THEN ...
  report the diagnostic and exit"), as the conflicts before did (E23).
  Whether such a pair is a finding or an artefact is the author's call; we
  have no known answer for real specs.

**Results on `eval18/`** (90 runs each arm, all finish).

| | Before | With the vote |
|---|---|---|
| planted conflicts found | 18 of 18 | 18 of 18 |
| planted gaps found | 18 of 18 | 18 of 18 |
| **planted ambiguities found** | **11 of 36** | **11 of 36** |
| a limit ("reaches 90 days") | 0 of 18 | 0 of 18 |
| "only if" | 5 of 9 | 9 of 9 |
| "if" after two outcomes | 5 of 6 | 2 of 6 |
| "and ... or ... and" | 1 of 3 | 0 of 3 |
| rules accepted in step 3 | 595 of 630 | 621 of 630 (23 by the vote) |
| ambiguity flags on rules we did not make ambiguous | 15 | 9 |
| clean runs with a conflict, doubtful ones set aside | 9 of 18 | 10 of 18 |

- **Nothing planted is found less often.** The two arms are separate runs,
  so the kinds move by chance as well; the sum is the same.
- **What the vote did to planted ambiguities.** It took 5 of the 36 planted
  rules (two "and/or", one "if", one "only if", one limit). One was still
  reported, by the question of step 6; four were not. Without the vote such
  a rule (ambiguous in step 3) was reported 4 times in 12, because step 6
  then asks about the two groups and the answers often side with the
  translation. So the vote costs about one planted ambiguity in this set,
  within the rule set beforehand (at most one in ten of those found).
- **A limit worded "reaches N" is never found**, with or without the vote:
  all eight translations read it as "N or more", and the answers of step 6
  agree.
- **Three of the six clean specs are not clean**, as in `eval16/`. Each has
  one rule about a state that cuts across the commands: "WHEN the
  configuration names a rule that does not exist THEN ... exits with code
  2" next to "`lnt check` AND no file has a finding ... exits with code 0";
  "WHEN an applied change was edited afterwards ... exits with code 6" next
  to "`mig up` AND no change is pending ... exits with code 0"; "WHEN a job
  runs for more than 60 minutes THEN the service stops the job" next to
  "starts the job". These three report a conflict in 9 of their 9 clean
  runs, in both arms; the other three in 0 and 1 of 9. A fair finding, and
  our mistake in writing the set.

**Decision.** The vote stays. The rule of plan.md 2.1 asked for fewer rules
of no use on `real3/` (28% and 36% against 54% and 62%), for planted
conflicts and gaps found no less often on `eval18/` (18 of 18 both), and for
at most one planted ambiguity in ten lost (11 of 36 both ways). Written down
as limits: a voted rule can say less than its words, a split that the vote
settles is no longer asked about, and more rules in the checks give more
conflicts between a rule and its special case. `eval18/` and `real3/` are
development data from now on. The next design needs `eval19/`, and a test on
real changes needs changes outside this pool of 48.

**Raw data.** experiments/results/E26_eval18.json, E26_eval18_before.json,
E26_real3.json and E26_real3_before.json, each with its table.

---

## T31 — Development: a second read for the rules that got no symbol (2026-11-26)

**Question.** After the vote one real rule in three is still of no use to the
checks, and for half of those a translation says that the rule demands
nothing (E26): the read step listed no symbol for its outcome. Can those
rules get their symbols afterwards?

**How often it happens** (no LLM; the saved runs, counted with the trigger
below): 172 of the 1,052 rules of the third real batch (E26, with the vote),
30 of 487 of the second (T30). In our own sets: 0 of 630 (`eval18/`), 0 of
492 (`eval17/`), 2 of 450 (`eval8/`), 2 of 378 (`eval7/`), 0 in the larger
project and the development specs, 2 of 1,203 in the 100-requirement spec.

**The change** (`formalize._read_again`, between steps 3 and 4). `real4/` was
written and committed first (8d60f61).

```
"WHEN file write fails THEN let the error bubble up naturally with file path"
first round    file_write_failed => true                    (and: file_write_failed => (> exit_code 0))
second read    adds  error_bubbles_up_with_path: "The file write error is propagated ... including the file path"
second round   file_write_failed => error_bubbles_up_with_path        8 of 8
```

1. Our code takes the rules that are not accepted after step 3 and have at
   least one translation that demands nothing (`_judge` counts them:
   `demand_nothing`).
2. One more call of the read step, in the form it has for an addition to a
   saved model (`READ_MORE`): the model sees the symbols so far and only
   those rules. One paragraph more (`READ_AGAIN`) tells it that something
   these rules demand has no symbol in the list, and to add a symbol for
   every such fact. Only the symbols it adds are used; the rules keep their
   text and trigger. An answer that cannot be used three times: no second
   read, and the run goes on.
3. Those rules are translated eight more times with the longer list and
   judged again, vote included. A rule takes its new translation only if it
   is accepted now.
4. An added symbol stays only if a translation that was taken uses it. If
   any stays, the question for the assumed facts is asked again with the
   list as it is now.

Point 4 was tightened after the first development runs. In the first
version every added symbol stayed. Told that a symbol is missing, the model
also adds one where none was: for "WHEN a booked vehicle has not checked in
30 minutes before departure ..." in the 100-requirement spec, whose
translations scatter over "=", "<=" and ">=" and two of them demand nothing,
it added `vehicle_not_checked_in` next to `vehicle_checked_in`. No rule took
a translation with it. On the third real batch 24 of the 167 added symbols
were of that kind. With point 4 as it is now, a second read that helps no
rule leaves the run exactly as it was.

**Results on development data.** "Before the second read" is the same run,
counted before step 2 above.

| | Before the second read | After |
|---|---|---|
| third real batch, 526 rules: of no use to the checks | 156 (30%) | 97 (18%) |
| second real batch, 487 rules | 185 (38%) | 107 (21%) |
| second real batch again, with point 4 as it is now (T31b) | 142 (29%) | 117 (24%) |
| for comparison, runs without a second read | third batch 28% and 36% (E26), second batch 23% (T30) | |

| | third batch | second batch | second batch, T31b |
|---|---|---|---|
| runs with a second read | 10 of 16 | 9 of 16 | 10 of 16 |
| rules read again | 71 | 107 | 56 |
| of them, took the new translation | 59 | 78 | 25 |
| symbols added | 167 (24 used by no translation that was taken) | 220 | 98 kept |

- **Within a run the second read brings back 5 to 17 points.** Across runs
  the picture is less clear on the second batch: 23% of no use in one run
  without it, 21% and 24% in two runs with it. The first read differs a lot
  from run to run (29% and 38% of no use before the second read here), and
  the second read repairs most where the first was worst.
- **The added symbols are about one rule.** `openspec_dir_created` was added
  next to `openspec_dir_exists`, `skills_generated_for_specified_tools_only`
  next to `skills_generated`. Such a rule can be written now, but it clashes
  with another rule only through the facts, links and questions of steps 4
  to 6. Whether what is planted is found more often is what `real4/` is for.
- **All 48 runs finish.**
- **Our own specs do not move** (first version of point 4): no second read
  in the 60 runs of `eval18/` (12 of 12 planted conflicts, 12 of 12 gaps, 5
  of 24 ambiguities), the 12 of the development specs (14 of 15 expected
  conflicts) and the 2 of the larger project (6 of 6 and 6 of 6).
- **The 100-requirement spec**, one run of each version: a second read for
  the one rule above in two of the four runs, no translation taken. Its
  planted gap and one planted conflict are found. The other planted
  conflict is missed: the fact "a gate cannot be open and closed" has 4 of
  8 votes. That fact has no majority in two of the three other runs either
  (1 and 4 of 8), in which no symbol was added, so the miss is not the
  second read's; in E14 it had 6 to 8 of 8.

**Frozen** in 0110641, after T31b. Next: held-out `real4/`, twice, with the
code before and after (E27).

**Raw data.** experiments/results/T31_real3.json, T31_real2.json,
T31b_real2.json, T31_eval18.json, T31_specs.json, T31_mixed.json and
T31_size2.json, each with its table.

---

## E27 — Held-out `real4/`: the second read, and conflicts planted in real specs (2026-11-26)

**Question.** Does the second read of T31 leave fewer rules of no use on real
changes it was not built on, and is a conflict planted in a real spec found?

**Setup.** `real4/` was written first (8d60f61) and the design frozen in
0110641. `real4/`: the 13 changes of the real project that create a new spec
of 14 to 31 scenarios, which the pool of the three batches had left out
because nothing existed before them. Each is there twice: as it is, and with
one scenario of ours that repeats the condition of one of its scenarios and
demands the opposite ("... with a key that does not exist THEN print nothing
AND exit with code 1" against "... THEN print `undefined` AND exit with code
0"). 26 cases, 553 rules, 2 runs each, with the code before the second read
(commit 8d60f61, from a git worktree, on the cluster) and after it (on the
workstation login).

**Results** (the two runs of each arm side by side).

| | Before | With the second read |
|---|---|---|
| runs that finished | 52 of 52 | 52 of 52 |
| **rules of no use to the checks** | **95 and 91 (17% and 16%)** | **94 and 80 (16% and 14%)** |
| the same two runs, counted before their second read | | 111 and 90 (20% and 16%) |
| rules whose translation demands nothing, both runs | 29 | 8 |
| rules with no symbol for what they demand, both runs | 58 | 17 |
| **planted conflicts found** | **24 of 26** | **22 of 26** |
| the same without assumed facts and links | 15 of 26 | 14 of 26 |
| other conflicts, not doubtful, both runs | 148 | 156 |
| questions about an ambiguous rule, both runs | 176 | 167 |
| rules reported as not checked, both runs | 26 | 7 |
| requests to the LLM for a change | 116 | 121 |

- **The second read does what it was built for, and that is little here.**
  It ran in 19 of the 52 runs, for 39 rules; 27 of them took their new
  translation, and 71 symbols stayed. The rules without a symbol for what
  they demand fall from 58 to 17. But on these specs only one rule in
  twenty lacked a symbol to begin with: they have 14 to 31 scenarios, where
  the cases of the three batches have 30 to 60, and the first read is good
  enough. The share of rules of no use moves by one point, and two runs of
  one arm differ by as much.
- **Conflicts planted in real specs are found**: 46 of 52 over both arms,
  and 29 of 52 without the assumed facts and links. One case is missed in
  all four runs: its planted scenario ("validate all changes and all specs
  AND exit with code 0") was rejected each time, its translations scattered.
- **Two fewer are found with the second read, and it is not the second
  read's doing.** Both are the same case, and neither of its two rules was
  read again. In one run the first read had made the output a number, and
  "print `undefined`" got no usable translation at all. In the other both
  rules were translated and clash, but a third rule ("... with a valid
  top-level key ... exit with code 0") had lost its condition, and the
  solver reports that situation as a conflict of that rule.
- **A rule with no usable translation at all is not read again**: the
  trigger looks for a translation that demands nothing, and here there was
  none to look at. A limit of the trigger.

**Decision.** By the rule of plan.md 2.1 the second read would go: it asked
for fewer rules of no use by more than two runs differ (94 and 80 against 95
and 91 is not that), and for planted conflicts found no less often (22
against 24). It stays all the same, on by default, by the user's rule for
such cases (a version that gains more than it loses is kept, and the loss is
written down): within a run it gains (2 and 3 points here, 5 to 17 on the
longer documents of T31), no loss could be traced to it, it costs 5 requests
in 116, and a second read that helps no rule leaves the run exactly as it
was. What the held-out test shows is no harm and a small gain; the larger
gain is measured only on the data it was developed on. `real4/` is
development data from now on.

**Raw data.** experiments/results/E27_real4.json and E27_real4_before.json,
each with its table.

---

## T32 — What are the conflicts that nobody planted? A reading of 20 (2026-11-26)

**Question.** The plain cases of `real4/` have no planted conflict, and the
runs of E27 report 148 and 156 conflicts on them and their planted twins
that are not marked doubtful. Are they findings?

**Method.** No LLM in the pipeline; a reading. From the first run of each of
the 13 plain cases with the code before the second read, the conflicts that
are not doubtful: 40, in 11 cases. Up to two of each case were drawn, 20 in
all, and read with the two requirements, their formulas, the situation and
the facts each rests on. The reading was done by the assistant that wrote
this entry, not by a person, and nobody has checked it yet.

| | Case | Rules | What it is |
|---|---|---|---|
| 1 | bulk-validation | R7, R18 | a general rule against its exception: "`validate <item-name>` ... validate the specified item" against "GIVEN `<item-name>` exists both as a change and as a spec ... exit with code 1 without performing validation" |
| 2 | bulk-validation | R5, R6 | a general rule against its exception (prompt the user; do not prompt when stdin is not a TTY) |
| 3 | view-dashboard | R4, R11 | artefact, a wrong assumed fact: "Colors cannot be used for items that do not exist in the display" |
| 4 | view-dashboard | R4, R10 | artefact, a situation that cannot happen: no specs exist, and a spec file cannot be parsed |
| 5 | config-command | R9, R12 | artefact, a mistranslation: both rules store the value as a string |
| 6 | artifact-graph | R10, R11 | artefact, a situation that cannot happen: one artifact that generates a single file and a set of files |
| 7 | artifact-graph | R1, R5 | artefact, a situation that cannot happen: a valid schema with two artifacts of the same id |
| 8 | change-manager | R1, R2 | a general rule against its exception (create the directory; throw when it already exists) |
| 9 | change-manager | R2, R4 | two failures at once, and nothing says which error is thrown: the directory already exists, and the name is invalid |
| 10 | artifact-workflow | R2, R27 | artefact, no time: a spinner during loading against the summary after it |
| 11 | artifact-workflow | R6, R7 | a general rule against its exception (list the ready artifacts; say that none is ready) |
| 12 | opsx-archive | R5, R7 | artefact, a situation that cannot happen: tasks.md is read, and tasks.md does not exist |
| 13 | feedback | R1, R4 | a general rule against its exception (create the issue; `gh` is not installed) |
| 14 | feedback | R1, R7 | a general rule against its exception (create the issue; `gh` is not authenticated) |
| 15 | verify-skill | R20, R23 | artefact, a wrong assumed fact: "An agent cannot provide specific, actionable recommendations ... if it is ..." displaying warnings only |
| 16 | verify-skill | R14, R15 | artefact, a situation that cannot happen: no design.md exists, and the implementation follows a design decision |
| 17 | update-workflow | R19, R20 | artefact, a situation that cannot happen: artifacts are still missing, and the artifacts are complete |
| 18 | update-workflow | R3, R17 | artefact, a situation that cannot happen: the artifacts are coherent, and coherence needs an artifact that is missing |
| 19 | version-command | R6, R8 | artefact, a situation that cannot happen: the registry cannot be reached, and it "reports no version newer" |
| 20 | version-command | R1, R3 | a general rule against its exception; the words "when they can be determined" of the general rule are not in its formula |

**Results.**

| What the 20 are | Count |
|---|---|
| a contradiction in the spec that its author would not have meant | 0 |
| a general rule against its own exception | 7 |
| two failure cases at once, with no order between them | 1 |
| an artefact | 12 |
| of them: a situation that cannot happen | 8 |
| of them: a wrong assumed fact | 2 |
| of them: no time in the logic | 1 |
| of them: a mistranslation | 1 |

- **None of the 20 is a real contradiction.** A reader of such a report
  wades through artefacts to find one question worth asking (number 9).
- **The largest group is a situation that cannot happen** (8 of 20). The
  solver lets two conditions hold together that exclude each other by what
  they mean, because nothing in the formulas says so: a file is read and
  does not exist. Most of these conflicts are then made by a question about
  two outcomes (3.13), which is asked for every pair of rules that Z3 thinks
  can apply together.
- **A general rule and its exception** (7 of 20) is how these specs are
  written: the scenario for the normal case does not say "unless".
- **What the solver can tell without the model** (all 40): in 4 the
  condition of one rule is a special case of the other's; in 33 the two
  conditions are two different definite states, so the model could be asked
  whether they can hold together; in 3 a condition is not one definite
  state.

**What follows.** Step 42: before a conflict between two rules with
different conditions is reported as it is, the model is asked whether the
two conditions can hold together (plan.md 2.1). After that, a mark for a
rule against a special case of it.

---

## T33 — Development: can the conditions of two rules that clash both hold? (2026-11-26)

**Question.** Most conflicts that nobody planted in real specs are in a
situation that cannot happen (T32). Can the model say so when it is asked
about the two conditions, without calling a real conflict impossible?

**The change** (`probe.conditions`, check 5 of step 6, after the other four).
`eval19/` and `real5/` were written and committed first (7ddb391).

```
R5   "WHEN agent reads tasks.md AND incomplete tasks are found THEN display warning ..."
R7   "WHEN tasks.md does not exist THEN proceed without task-related warning"
asked     A: TRUE tasks_md_read, FALSE all_tasks_complete     B: FALSE tasks_md_exists     can both be the case?
answers   6 of 8 "impossible" (7 of 8 in round 1 below): "A file cannot be read if it does not exist."
fact      (not (and <condition of R5> <condition of R7>))      between R5 and R7, about: conditions
```

1. Our code takes the pairs of rules that can apply together by the facts so
   far, cannot both be obeyed there, and do not react to two different
   events: the pairs that would be reported as a conflict that is not
   doubtful. Of those it keeps the ones whose conditions are two definite
   states, each saying something the other does not (`_clashing_pairs`).
2. The model is asked eight times whether the two conditions can both be
   the case. It sees what only one condition says and what only the other
   says, as facts with their descriptions, and no requirement.
3. More than half "impossible": an assumed fact. `checks.py` then marks a
   conflict proven from the rules alone as doubtful, and does not find one
   that needs an assumed fact.

The new facts are marked (`about: conditions`), so every run is scored with
and without them, and the question can be asked on saved runs
(`evaluate --rescore FILE --conditions-base-url URL`).

**Round 1: the question asked with the prompt of check 4** (saved runs;
"found" is with doubtful conflicts set aside).

| | Planted conflicts found, without and with | Planted pairs asked about, called impossible | Conflicts nobody planted, not doubtful, without and with |
|---|---|---|---|
| `real4/` (E27, 52 runs) | 22 and 22 of 26 | 0 (the planted ones have one condition) | 156 and 125 |
| third real batch (E26, 32 runs) | | | 30 and 26 about a change |
| `eval8/` | 18 and 15 of 21 | 12, 3 | 0 and 0 |
| `eval17/` | 20 and 18 of 24 | 6, 2 | 2 and 2 |
| `eval7/`, `eval12/`, `eval16/`, the larger project | 17 of 18, 34 of 36, 20 of 24, 6 of 6, each both ways | 36, 0 | no change |
| the development specs, a full run | 14 and 11 of 15 | 12, 3 | |

- **On the real specs it marks what it should.** 209 pairs were asked about
  in the 52 runs of `real4/`, and 65 called impossible. The 14 we read are
  all excluded by the meaning of the words: "A file cannot be read if it
  does not exist", "Artifacts cannot be both incomplete and complete at the
  same time".
- **It also marks real conflicts**, all of one kind: something happens while
  the system is in a special mode. "A server in maintenance mode does not
  allow clients to submit messages", for the planted rule "WHEN the server
  is in maintenance mode THEN the server does not put any message in the
  queue"; "An out-of-service machine cannot accept a container insertion";
  and, in the order example of the Kiro blog, "An order cannot be both
  submitted and canceled and refunded at the same time", for R1 against R5.
  The model assumes a system that behaves.

**Round 2: a prompt of its own** (`CONDITIONS_SYSTEM`). It says that
"impossible" means excluded by the meaning of the words alone, and that a
state in which something should not happen, is not allowed or would be
unusual does not make it impossible: "Do not assume that the system or its
users prevent anything, or that anything succeeds." Its examples (a candle,
a jar, a lawn) are in no evaluation set.

| | Planted conflicts found, without and with | Planted pairs asked about, called impossible | Conflicts nobody planted, not doubtful, without and with |
|---|---|---|---|
| `real4/` | 22 and 22 of 26 | 0 | 156 and 129 |
| `eval8/` | 18 and 18 of 21 | 12, 0 | 0 and 0 |
| `eval17/` | 20 and 20 of 24 | 6, 0 | 2 and 2 |
| `eval7/`, `eval12/`, `eval16/` | as in round 1 | 32, 0 | no change |
| the development specs, a full run | 14 and 11 of 15 | 12, 3 | |

- **The planted conflicts of our own sets are left alone**: 50 pairs asked
  about, and not one of the 400 answers says "impossible".
- **Most of the gain stays**: 54 of the 209 real pairs are called impossible
  (65 in round 1), and 27 conflicts fewer are reported as they are.
- **The order example of the Kiro blog is still marked**, in 3 of 3 runs,
  with 7, 7 and 8 answers of 8: "An order that has been canceled and
  refunded cannot currently be an active submitted order with available
  inventory." The conflict of R1 and R5 stays in the report, as doubtful.
  This is the known loss of the frozen design.

**Frozen** after round 2, with the commit of this entry. Next: held-out
`eval19/` and `real5/`, each run scored with and without the new facts (E28).

**Raw data.** experiments/results/T33_*.json (round 1) and T34_*.json (round
2). Those of the saved runs are small files that name the runs they belong
to; T33_specs, T33_size and T34_specs are full runs. Each has its table.

---

## E28 — Held-out `eval19/` and `real5/`: can the conditions of two rules that clash both hold? (2026-11-26)

**Question.** Does the question of T33 mark the conflicts in a situation that
cannot happen, on specs it was not built on, and does it leave the conflicts
alone that we planted between rules whose conditions can hold together?

**Setup.** `eval19/` and `real5/` were written first (7ddb391) and the design
frozen in 30513fc. One arm: the new facts are marked, so each run is scored
with them and without them, and "without" is the pipeline before the step.

- `eval19/`: six specs of 8 scenarios (a playlist service, a greenhouse
  controller, a library hold shelf, a stadium gate, a photo archive, a
  freezer monitor). The clean version holds two scenarios whose conditions
  exclude each other by their meaning, and that set one thing to two values
  ("WHEN a playlist has no tracks THEN ... sets the cover ... to `blank`",
  "WHEN the first track of a playlist has an album image THEN ... to
  `album`"). The other versions add a direct conflict, a conflict under a
  mode of the system ("WHEN the stadium is being evacuated THEN the gate
  issues no re-entry pass"), a conflict under a state of the same thing
  ("WHEN the account of the reader is blocked for unpaid fines THEN ..."),
  or remove one of two complementary scenarios. 3 runs each, on the cluster.
- `real5/`: the last 8 unused real changes that create a new spec (seven of
  11 to 13 scenarios, one of 45), each as it is and with one scenario of
  ours whose condition is a mode or a flag of its own ("WHEN a pull request
  carries the label `docs-only` THEN the CI SHALL NOT prevent merging").
  2 runs each, on the workstation login.

**Results on `eval19/`** (90 runs, all finish; "found" is with doubtful
conflicts set aside).

| | Without the question | With it |
|---|---|---|
| planted conflicts found | 48 of 54 | 48 of 54 |
| direct | 18 of 18 | 18 of 18 |
| under a mode, under a state of the same thing | 15 and 15 of 18 | 15 and 15 of 18 |
| **clean runs with a conflict** | **11 of 18** | **0 of 18** |
| **conflicts that nobody planted** | **97** | **19** |
| the two scenarios made for it, reported as a conflict that is not doubtful | 58 of 90 runs | 2 of 90 |
| planted gaps found | 18 of 18 | 18 of 18 |

- **The pair it was made for is marked**: asked about it 58 times, the model
  called it impossible 56 times ("A playlist with zero tracks cannot have a
  first track.", in the words of one answer).
- **No planted conflict is touched.** The 30 planted pairs it was asked
  about were all called possible. The 6 planted conflicts that are doubtful
  either way are those of the greenhouse: "the price of electricity is at
  its daily peak" and "the heater is in its yearly service" were read as
  events, and a conflict between two events is doubtful (the limit of 3.7).
- **It calls 27 other pairs impossible**, and 22 conflicts fewer of that
  kind are reported as they are. 15 of the 27 are one pair of the hold shelf
  that we had not seen: "a reader places a hold" against "a reader has no
  holds". The model says that whoever places a hold has one; by the clock
  that is the moment after.

**Results on `real5/`** (32 runs, all finish).

| | Without the question | With it |
|---|---|---|
| planted conflicts found, doubtful ones counted | 10 of 16 | 10 of 16 |
| planted conflicts found, doubtful ones set aside | 6 of 16 | 6 of 16 |
| **conflicts that nobody planted, not doubtful** | **63** | **56** |
| the same, doubtful ones counted | 87 | 80 |

- **It asks about 66 pairs and calls 10 impossible**, 5 different ones. Read:
  - right, by the meaning of the words (7 of the 10): "all artifacts are
    completed" with "an artifact is blocked" (4 times); "config.json ...
    contains invalid JSON" with "config.json contains fields not in the
    current schema" (3 times);
  - wrong (3 of the 10): two flags or modes of one command that a user can
    give together. "The --default and --no-default flags are mutually
    exclusive and cannot both be provided in the same command"; `--force`
    with interactive mode; `--no-default` with a user who confirms the
    default. What the tool does then is a fair question, and it is now
    marked doubtful. The prompt says not to assume that users prevent
    anything; here the model did.
- **The planted conflicts are left alone**: 6 pairs asked about, 48 answers
  "possible".
- **A conflict planted under a condition of its own is harder to find in
  real text than one with a copied condition** (10 of 16 here, 46 of 52 in
  E27), and not because of this step:
  - 4 of the 10 are marked doubtful: the planted condition, a mode ("the
    loader runs in lenient mode"), was read as an event, and a conflict
    between two events is doubtful;
  - 4 of the 6 misses are a rule without an agreed translation (in one case
    the returned path is a number in some answers and a name in others);
  - 2 are two symbols for one thing: `build_output_displayed` and
    `no_build_output_displayed`, with no fact between them.

**Decision.** The question stays, on by default: the rule of plan.md 2.1
asked for fewer conflicts that nobody planted on both sets (19 against 97,
56 against 63) and for at most one planted conflict in ten lost (none is).
Written down as limits: in the order example of the Kiro blog it marks R1
against R5 as doubtful (T33); it calls two flags of one command impossible
(3 of its 10 marks on `real5/`); and it costs one question for each pair of
rules that clash, about 2 for a real change and 1.5 for a spec of ours.
`eval19/` and `real5/` are development data from now on.

**Raw data.** experiments/results/E28_eval19.json and E28_real5.json, each
with its table.

---

## T35 — A conflict between a rule and a special case of it says so (2026-11-26)

**Question.** A third of the conflicts that nobody planted in real specs set
a general rule against its own exception (T32). The solver can prove that
form. How many conflicts have it?

**The change** (`checks._mark_special_cases`, `explain.py`; no LLM, no
prompt). For a conflict between two rules, Z3 is asked whether the condition
of one entails the condition of the other. If it does, and not the other way
round, and the general rule has a condition at all, the finding gets
`special_case: {general, special}`, a remark in its title and one sentence
in what was proven:

```
## 6. Conflict (if the assumed facts hold, R2 is a special case of R1)
R1  "WHEN createChange(projectRoot, 'add-auth') is called THEN the system creates openspec/changes/add-auth/ directory"
R2  "WHEN createChange(projectRoot, 'add-auth') is called and openspec/changes/add-auth/ already exists THEN the system throws an error ..."
"R2 applies only where R1 applies: its condition is a special case of the condition of R1.
 If R2 is meant as an exception, R1 does not say so."
```

It is a remark, not a doubt: the conflict is counted as before. A rule that
always applies ("THE system SHALL NOT ...") is left out, because every rule
is a special case of it; so the two examples of the Kiro blog keep their
titles. Two rules with the same condition get no remark.

**How often** (saved runs, scored again; nothing was tuned on them).

| Runs | Conflicts that nobody planted, not doubtful | With the remark | Planted conflicts with the remark |
|---|---|---|---|
| `real5/` (E28, with the question of step 42) | 56 | 22 | 0 of 10 |
| `real4/` (E27, the code before the second read) | 148 | 26 | 1 of 24 |
| `eval19/`, `eval17/`, `eval12/`, `eval8/`, the larger project, the development specs | 51 | 0 | 0 of 151 |

- **On real specs one conflict in three to six has the form**: mostly a
  command and its fallback ("WHEN executing `openspec show` without
  arguments THEN prompt user ..." against "GIVEN stdin is not a TTY ...
  WHEN executing `openspec show` without arguments THEN do not prompt ...").
- **None of ours has it.** Our planted conflicts repeat a condition or set
  two unrelated conditions against each other. The one planted conflict
  with the remark is a translation in which the copied condition lost a
  part.
- **With steps 42 and 43**, of the 63 conflicts that `real5/` reported as
  they were, 7 are doubtful now, 22 carry this remark, and 34 are left as
  they were.

No new set was written for this: the remark changes no count and has no
setting, and the runs it was measured on were made before it existed.

---

## T36 — A first trial on the specs of an agent system (2026-11-26)

**Question.** The tool is meant for the specs of an agent system: an
orchestrator and specialist agents that call tools. What does it report on
such a project as it is?

**The project.** TestingTheAgents (https://github.com/unibuc-cs/TestingTheAgents,
folder `trace-eval/openspec`, commit f6cb12b): 33 spec files in the OpenSpec
format with 465 scenarios, and four open changes that each add a workflow. Its authors say which can be
built: three can, and one cannot, for four reasons that they list. One is a
plain contradiction between two rules of the change (two contracts for one
function). Two set the change against rules of other spec files (an approval
that an existing rule demands, a hand-over that existing rules forbid). The
fourth is arithmetic over a whole run (a batch of 60 against step budgets of
12 and 40). The project is a repository of its own, and the runs on it are
not kept in this one; `experiments/agents/` says how to make them again.

**How it was run.** The project is too large for one document, so each
change was put next to one existing spec file at a time, and once alone: 79
small projects, run with the code as it was (`experiments.evaluate`, the
change that cannot be built twice, the others once).

| Change | Runs | Conflicts about it, not doubtful | Runs with one |
|---|---|---|---|
| cannot be built | 40 | 51 | 34 |
| can be built, first | 20 | 16 | 11 |
| can be built, second | 19 | 25 | 11 |
| can be built, third | 20 | 10 | 8 |

- **The contradiction between two rules was found in 27 of 40 runs.**
- **A conflict that is not there was found in 23 of 40**: two step budgets
  with names that differ by one word. The link step restated the rule about
  one as a rule about the other, 8 answers of 8, and the check of the link
  confirmed it, because its question does not show the rule's own symbol.
- **The approval conflict was found once, and marked doubtful**: its two
  rules react to two different calls, "two events at the same moment". The
  rules of such a spec are about a whole run.
- **The changes that can be built got as many conflicts.** Almost all are
  between two examples: scenarios that describe one request under two
  fixtures, read as two general rules.
- **The questions about pairs of outcomes stopped at their limit** of 40
  pairs in 19 of the 40 runs, with up to 290 pairs left.
- The hand-over and the arithmetic were not found.

**What followed.** The plan of step 44 (plan.md 2.1), written before any
code, and `eval20/`, a set of our own with the same properties in other
domains.

---

## T37 — Development: the same trial with the code of step 44 (2026-11-26)

**Question.** Do a whole run as the situation, the mark for examples and
the second question for links do on the project what they were planned for?

**How it was run.** The same 79 small projects, with `--whole-run` and
`--examples` (the pattern of the project's own mark for an example). The
code was the plan of 2.1, before its one refinement.

**What the plan gave, and the refinement.** The wrong conflict between the
two budgets went from 23 runs to 1: in the 40 runs of the change that cannot
be built, 106 of 232 links were asked about with both symbols, and 99 of
those were rejected. The contradiction between two rules was found in 32 of
40 runs. But that change now had 73 conflicts, not 51: 34 set an example
against a rule, almost all an example of an existing spec against a rule of
the change. In each, the questions about two outcomes (asked of such pairs
now, since both can be in one run) had called the outcome of the example
and the outcome of the rule impossible together, and the situation mixed
the two: the concrete case of the example, taken to be also a run of the
new workflow. The plan had marked a conflict between examples only. The
mark became: a conflict with an example is doubtful unless the example's own
case, its condition and what it demands, entails the conditions of the other
rules (`checks._mark_examples`; Z3, no question). Scored again on the same
runs:

| Change | Runs | Conflicts about it, not doubtful: before step 44 (T36) | With step 44 | Doubtful with step 44, all marked for an example |
|---|---|---|---|---|
| cannot be built | 40 | 51 (in 34 runs) | 39 (in 34 runs) | 51 |
| can be built, first | 20 | 16 (in 11 runs) | 4 (in 4 runs) | 22 |
| can be built, second | 19, then 18 | 25 (in 11 runs) | 5 (in 5 runs) | 23 |
| can be built, third | 20 | 10 (in 8 runs) | 1 (in 1 run) | 19 |

- **Of the 39, 32 are the contradiction between two rules**, and one more is
  the missing approval in another form (a tool that stays guarded against an
  example in which it runs with no approval). The other six are artefacts:
  three give one attribute to every call of a run ("the agent that made the
  call", "the token it carried"), where two rules speak of two different
  calls.
- **The approval conflict itself is found in one run of two, and is now
  doubtful.** It sets a rule of another spec against an example of the
  change, and nothing in the example's formulas says that its run has a
  plan and a successful call of the kind the rule is about. The report
  shows it with that reason.
- **The limit of 40 pairs is reached in 39 of 40 runs** (93 of 98 in all):
  with a whole run as the situation, a document of about 30 rules has some
  175 pairs. The pairs with a rule of the change come first, so the limit
  now cuts among them.
- The hand-over and the arithmetic are still not found.

One run of 99 stopped: the model declared one name twice.

---

## E29 — Held-out `eval20/`: specs about the runs of an agent system (2026-11-26)

**Question.** Three parts of step 44 act on a project of any size: a whole
run as the situation, the mark for examples, and the second question about
a link. Do they do on specs they were not built on what they did on the
project of T37?

**The set** (`eval20/`, written and committed before any code). Four
projects about an assistant that calls tools: a dispatcher of parcels, a
travel assistant, a lab assistant, a bank's support assistant. Each has a
setting, rules about calls ("WHEN a call of `ship_parcel` succeeds in a run
with a plan THEN an earlier call of `request_signoff` in the run was
approved") and examples, whose names start with "Example:". Each has four
changes:

| Change | What it adds | Expected |
|---|---|---|
| clean | three examples of one request under three conditions, and a rule about a call | nothing |
| cross | a rule about one kind of run ("WHEN an express request is handled in a run THEN `request_signoff` is not called in the run"), which forbids what an existing rule demands when another call succeeds in such a run | that conflict |
| direct | two rules about one function that cannot both hold | that conflict |
| twins | a setting whose name differs from an existing one by a word (`shipping.max_parcels`, `shipping.max_batch_parcels`), with another value | nothing |

**The rule, set before the build** (plan.md 2.1). With doubtful conflicts
set aside and the two options given: the "cross" conflicts are found more
often than without, the "clean" and "twins" changes get fewer conflicts, and
the "direct" conflicts are found no less often. And with the options not
given, `eval12/` gives what it gave.

**Result.** 16 changes, 3 runs each: once with the code before step 44, once
with the frozen code and `--whole-run --examples "^Example:"`. Doubtful
conflicts are set aside. The last three columns are the runs of step 44
scored again with one part switched off (`E29_eval20_before`, `E29_eval20`).

| | Before step 44 | Step 44 | a run read as one moment | examples read as rules | links not asked about twice |
|---|---|---|---|---|---|
| "cross" conflicts found | 0/12 | 12/12 | 0/12 | 12/12 | 12/12 |
| "direct" conflicts found | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| "clean" changes with a conflict about them (conflicts) | 6/12 (6) | 0/12 | 0/12 | 11/12 (21) | 0/12 |
| "twins" changes with a conflict about them (conflicts) | 11/12 (11) | 0/12 | 0/12 | 0/12 | 9/12 (9) |
| other conflicts about a change with a planted one | 0 | 0 | 0 | 12 | 0 |

- **The rule is met on every point**, and each part does one thing. Read as
  one moment, all 12 "cross" conflicts are doubtful, as they were before.
  With the examples read as rules, 11 of the 12 clean changes have a
  conflict about them. Without the second question, 9 of the 12 changes
  that only add a setting have one.
- **The examples.** In the default configuration 34 conflicts about the
  changes are doubtful, and every one is marked because its situation says
  more than an example does: 22 on the clean changes and 12 on the cross
  ones. The 12 are the example of the cross change ("WHEN dana sends an
  express request for the parcels k1, k2 and k3 THEN the plan is written
  once AND `ship_parcel` succeeds three times") against an existing example
  or rule. No planted conflict got the mark.
- **The second question.** 51 of 131 links moved a rule's demand to another
  symbol and were asked about twice. On the "twins" changes that is 26
  links: the first question had confirmed 15 of them, and the second
  rejected all 26. On the "cross" changes it confirmed 17 of 18, among them
  the link that the planted conflict needs ("an earlier call was approved"
  means that there was a call).
- **The price.** With a whole run as the situation, the pairs of two
  happenings are asked about too: 1,530 pairs of outcomes against 74, and
  55 assumed facts from them against 9. A change costs 87 requests and
  51,065 tokens written, against 55 and 27,691. The wrong ones among those
  facts are what the examples' conflicts rest on ("A parcel's state must
  change when a return is booked and subsequently cancelled", for an
  example against the rule that a lookup changes nothing).
- **Gaps are as before**: 23 about the changes, 21 before, and 8 and 9 of
  the 24 changes that should give nothing have one.
- **`eval12/`, with no option** (`E29_eval12`): 34 of 36 planted conflicts,
  as in E18, and 4 of 18 clean runs with a false alarm, where E18 had 3. No
  part of step 44 caused the difference: the only part that acts without an
  option is the second question, and the row without it is the same in
  every column.

**Decision.** Step 44 stays as it was frozen. All twenty sets are
development data now.

---

## T38 — The tool itself on the project: four changes, each in parts (2026-11-26 and 27)

**Question.** T36 and T37 put each change next to one spec file by hand.
What does `speccheck --change` report on the project's own folder?

**How it was run.** `speccheck --change <the change> --whole-run --examples
"^use: scenario$"` (the project's mark for an example), with the frozen code
of step 44, once for each change; the commands are in README.md and in
`experiments/agents/`. With a change applied the project has 474 to 479
scenarios, so each was checked in 32 or 33 parts, formalized at the same
time on two GPUs: 31 to 55 minutes for a change. 4 of the 131 parts could
not be formalized: the read step returned the rules of the change alone,
twice. All four are specs of the project's test harness. The report names
them.

**What the first reports showed** led to step 45 (E30): the contradiction
that the authors name was there, "found in 18 of 32 parts", and a change
that can be built had a conflict found in 21 of 32, an existing example
against a new variant of it.

**The reports with the code of step 45.** The saved parts were checked
again (the model is asked only for the wording): against all 33 spec files,
and against the 24 of the application alone (`--against`), without the 9
that describe the test harness.

| Change | Against | Parts | Conflicts, not doubtful | Among the rules of the change (parts that found each) | With a rule of another spec file | Doubtful, all marked for an example |
|---|---|---|---|---|---|---|
| cannot be built | the application | 24 | 6 | 3 (16, 2 and 1 of 24) | 3 | 18 |
| can be built, first | the application | 24 | 5 | 2 (1 and 1 of 24) | 3 | 33 |
| can be built, second | the application | 23 | 3 | 1 (1 of 23) | 2 | 43 |
| can be built, third | the application | 24 | 1 | 0 | 1 | 16 |
| cannot be built | all spec files | 32 | 10 | 4 (18, 2, 1 and 1 of 32) | 6 | 18 |
| can be built, first | all spec files | 33 | 14 | 2 (2 and 1 of 33) | 12 | 35 |
| can be built, second | all spec files | 32 | 4 | 2 (1 and 1 of 32) | 2 | 45 |
| can be built, third | all spec files | 30 | 1 | 0 | 1 | 18 |

- **The contradiction between two rules is found in 16 of 24 parts** (18 of
  32), with the remark that one rule is a special case of the other, and an
  explanation that says the system cannot be built as written. Nothing
  else among the rules of any change is found in more than 2 parts. That
  count is what tells the four changes apart; the number of conflicts does
  not.
- **The conflicts with a rule of another spec file are artefacts**, those
  we read. Each is found in one part. Most rest on one assumed fact from
  the question about two outcomes, between two rules about two unrelated
  happenings of one run ("A run cannot have a maximum tool call count of 40
  if no tools were called"). The others give one attribute to a whole run
  that belongs to one call or one function: the token a call carried, the
  file a function is defined in. The specs of the test harness add 3 and 9
  of them, which is why `--against` exists.
- **Of the four reasons that the authors give, one is found.** The missing
  approval, which T37 found in one run of two and marked doubtful, is not in
  these reports. It is a chain of three rules: a run of the new workflow
  takes a page down in a plan, the existing rule then demands an approved
  request, and the change says that such a run asks nobody. No two of the
  three clash by themselves, and nothing in the formulas says that an
  approved request is a request. The hand-over and the arithmetic are not
  found either. The rule that carries the batch size has no agreed
  translation in 15 of 24 parts.
- **16 to 45 conflicts for a change are doubtful**, every one because its
  situation says more than an example does. They are in the report, after
  the others.
- 5 to 8 rules of a change are reported as ambiguous, and up to 3 as not
  checked, each with the number of parts. No report has a gap: a gap about
  the change must be in every part.

---

## E30 — Held-out `eval21/`: every example of a conflict must describe its situation (2026-11-27)

**Question.** The tool itself was run on the four changes of the project of
T36, each in 32 or 33 parts (T38). A change that can be built got a
conflict "found in 21 of 32 parts": an existing example against an example
that the change adds, of the same test case, the second "while" one more
thing is true. Read as rules the second is a special case of the first. The
mark of step 44 was not given, because one of the two examples, the second,
describes the whole situation. Should every example of a conflict have to?

**The change** (step 45, `checks._mark_examples`; Z3, no question). A
conflict with examples counts as it is only when every example among its
rules describes its situation: its condition and what it demands, with the
assumed facts, entail the conditions of the other rules. The existing
example does not say what its variant adds, so the two are two cases. The
finding names the examples that fall short (`beyond_example`).

**The set** (`eval21/`, written and committed before the change). Four more
projects about an assistant that calls tools: a library, a garage, a
pharmacy, an irrigation system. Each has a rule about a call ("WHEN a call
of `lend_book` succeeds THEN an earlier call of `check_card` in the run
succeeded") and one example with no condition of its own ("Example: a book
is lent: WHEN mira asks to borrow book b12 THEN `lend_book` is called once
AND the answer gives the due date"). Three changes each, all of which add
examples:

| Change | What it adds | Expected |
|---|---|---|
| variant | two more cases of the request of the existing example, each under a condition of its own ("WHEN the same request runs while b12 is reserved for another reader THEN `lend_book` is never called ...") | nothing |
| same | an example with the words of the existing one in its WHEN part and the opposite outcome ("WHEN mira asks to borrow book b12 THEN `lend_book` is never called ...") | that conflict |
| breaks | an example that breaks the rule about the call by what it demands itself ("WHEN mira sends a quick request for book b12 THEN `lend_book` succeeds once AND `check_card` is never called") | that conflict |

**The rule, set before the change** (plan.md 2.2). With doubtful conflicts
set aside and the same runs scored both ways: the "variant" changes have a
conflict about them less often than when one example is enough, and the
conflicts of the "same" and the "breaks" changes are found no less often.
And the saved runs of `eval20/` (E29), scored again, give what they gave.

**Result.** 12 changes, 3 runs each, with `--whole-run --examples
"^Example:"` (`E30_eval21`). Doubtful conflicts are set aside.

| | Every example (step 45) | One example is enough (step 44) | Examples read as rules |
|---|---|---|---|
| "variant" changes with a conflict about them (conflicts) | 0/12 | 3/12 (3) | 11/12 (20) |
| "same" conflicts found | 5/12 | 5/12 | 5/12 |
| "breaks" conflicts found | 4/12 | 4/12 | 10/12 |
| other conflicts about a change with a planted one | 0 | 0 | 3 |

- **The rule is met.** The three conflicts that step 44 left on the
  "variant" changes are the existing example against its new variant, in
  the three runs of one project. The runs of `eval20/`, scored again, give
  the numbers of E29 in every row.
- **What the set shows besides, which the rule did not ask.** A conflict
  between an example and a rule is found in 10 of 12 runs, and in 6 of the
  10 it is marked doubtful, with either step. The example says "`start_repair`
  succeeds once", the model wrote that as a count, `(= start_repair_called_count 1)`,
  and the rule is about `start_repair_succeeded`: nothing in the formulas says
  that the first means the second, so the example does not make the rule
  apply. The mark for examples costs these.
- **Two examples of one case are found in 5 of 12 runs**, with or without
  the mark. In all 7 misses the two have the same condition, and "called
  once" and "never called" became two symbols: a count that is 1, and "the
  call did not succeed", a symbol that the model took over from the rule
  about the call. Asked whether the two can hold together, 7 or 8 of 8
  answers say that they can: a call can be made and fail.
- Read as rules, the examples give a conflict on 11 of the 12 changes that
  only add cases.
- A change of these projects costs 43 requests.

**Decision.** Step 45 stays. An example that breaks a rule by its own words
is the open point: it is found, and marked doubtful more often than not.

---

## T39 — Development: does what one rule demands make another rule apply? Four forms of one question (2026-11-27)

**Question.** One reason why a change of TestingTheAgents cannot be built is
a chain of three rules (T38): a run of the new workflow takes a page down in
a plan; an existing rule then demands that an earlier request for approval
was approved; the change says that no such request is made in such a run. No
two of them clash by themselves. The checks connect what two rules demand
(links, the question about two outcomes) or their two conditions, never what
one demands with the condition of another. Step 46 asks that (plan.md 2.3).
In which form?

**How it was tried.** The pairs are chosen by Z3: a pair (a, b) is asked
about when, where a applies, b cannot apply as well without a clash between
the two. For each part of the condition of b that a does not settle, the
model is asked 8 times. The check was added to saved runs, so that only the
form of the question differs: the runs of `eval20/` (E29) and `eval21/`
(E30) with `--rescore ... --applies-base-url` (files `T39`, `T39b`, `T39c`,
`T39d`), and the saved parts of the four changes of the project (T38).

| Form of the question | `eval20/`: runs on changes that should give nothing, with a conflict | `eval21/`: examples that break a rule, found and not doubtful | The project: the step from "approved" to "requested" | The project: steps said yes to with a rule of the change, for its four changes |
|---|---|---|---|---|
| 1. the question of check 4 on the symbols: "A: what a demands. B: the part is not the case. Can both hold?" | 1 of 24 | 4 of 12 | 6 of 8 answers | 3, 19, 24, 3 |
| 2. a prompt of its own on the symbols: "Does A say that B is the case?", and what a system would merely need is a "no" | 0 of 24 | 4 of 12 | 4 of 8: not taken | 0, 2, 5, 0 |
| 3. the question of check 2: the words of a, and a situation with the condition of a and the part not the case | 0 of 24 | 10 of 12 | 8 of 8 | 17, 21, 29, 1 |
| 4. the words of a, the prompt of its own, and the part alone as fact B | 0 of 24 | 10 of 12 | 8 of 8 | 2, 6, 15, 3 |

- **Form 1 takes what a system needs for what the words say.** "(the answer
  gives the return label) → `find_parcel` succeeded", 8 of 8: "For the
  system to provide a specific return label in the answer, it must have
  successfully identified the parcel". On `eval20/` it gave a conflict to a
  change that should have none, and 8 conflicts among the existing rules.
- **Form 2 is clean and gains nothing.** The symbols of a demand can say
  less than the requirement. "`start_repair` succeeds once" had become a
  count of calls, and the model is right that a call can be made and fail.
  On the project, the demand that an earlier request for approval in the
  run was approved had become a symbol about an approval that was granted,
  and half of the answers said that an approval can come from an earlier
  request or in another way.
- **Form 3 reads the requirement, and then judges too much.** With the
  words, the examples of `eval21/` are found: "The requirement explicitly
  states that 'start_repair succeeds once'" (8 of 8, in 6 runs). But shown
  the condition of a as a situation, the model also called situations
  impossible for those facts (a list that is empty in the situation, where
  the requirement names what the list must hold). On the project it said
  yes to 17, 21 and 29 steps for three of the changes.
- **Form 4 keeps what each round taught**: the words of the requirement, the
  prompt that says what does not count, and the one fact alone. On
  `eval20/` and `eval21/` every step it says yes to is right (4 and 6, all
  8 of 8), and no change that should give nothing gets a conflict.
- **On the project**, with form 4, the four changes have 7, 5, 4 and 1
  conflicts that are not doubtful, against 6, 5, 3 and 1 without the check.
  The one more of the change that cannot be built is the missing approval,
  between the rule of another spec file and the rule of the change. The one
  more of a change that can be built sets a rule of the change against an
  example of it.
- **The limit of 40 questions is reached often on the project.** With only
  the pairs that have a rule of the change, 2,008 of 5,004 questions were
  left out.

**Decision.** Form 4 is frozen for the held-out test (`eval22/`). When a
change is checked, only the pairs with one of its rules are asked about.

---

## E31 — Held-out `eval22/`: does what one rule demands make another rule apply? (2026-11-27)

**Question.** Does check 6, in the form that T39 froze, find a contradiction
that is a chain of three rules, on specs it was not built on, without saying
yes where the words do not?

**The set** (`eval22/`, written and committed before the check). Four more
projects about an assistant that calls tools: a hotel's front desk, a box
office, a car rental, a clinic. Each has two rules about calls. One demands
an earlier approved call in the same run ("WHEN a call of `check_in_guest`
succeeds in a run with a plan THEN an earlier call of `ask_manager` in the
run was approved"), the other a state from before the run ("WHEN a call of
`refund_stay` succeeds THEN the guest's card was verified at check-in").
Three changes each:

| Change | What it adds | Expected |
|---|---|---|
| chain | "WHEN a call of `ask_manager` is made THEN the run is not a late-arrival run", and a rule about a check-in in such a run. In a late-arrival run with a plan in which a guest is checked in, the first rule demands an approved call and this one forbids the call. No two rules clash by themselves | the conflict between the existing rule and the first rule of the change |
| breaks | an example that breaks the existing rule by what it demands itself: "... THEN the plan is written once AND `check_in_guest` succeeds once AND `ask_manager` is never called" | that conflict, not doubtful |
| near | the form of the chain for the second rule: "WHEN a call of `verify_card` is made THEN the run is not a refund run". The card "was verified at check-in", which does not say that `verify_card` is called in this run | nothing |

**The rule, set before the build** (plan.md 2.3). With doubtful conflicts set
aside and the same runs scored with and without the facts of check 6: the
"chain" conflicts are found more often, the "breaks" conflicts no less
often, the "near" changes have a conflict about them no more often. And
asked on the saved runs of `eval20/` and `eval21/`, it loses no planted
conflict and gives no conflict to a change that should have none.

**Result.** 12 changes, 3 runs each, `--whole-run --examples "^Example:"`
(`E31_eval22`). Doubtful conflicts are set aside.

| | With check 6 | Without its facts |
|---|---|---|
| "chain" conflicts found | 12/12 | 2/12 |
| "breaks" conflicts found | 12/12 | 0/12 |
| "near" changes with a conflict about them | 1/12 | 1/12 |
| other conflicts about a change with a planted one | 0 | 0 |

- **The rule is met on every point.** On `eval20/` and `eval21/` it is met
  by the last round of T39: 24 of 24 and 15 of 24 planted conflicts (9 of 24
  without the check), and no change that should give nothing has a conflict.
- **The chain**, in one run of the hotel: the model was asked five times
  whether a rule makes "a call of `ask_manager` is made" true. For the
  existing rule 8 of 8 answers said yes ("An ask_manager call that was
  approved was made."), for the four others 8 of 8 said no. With that fact
  Z3 reports the existing rule against "a late-arrival run asks nobody", in
  a late-arrival run with a plan in which a check-in succeeds. In the 2
  runs that find the chain without the check, the model had written "an
  approved call" and "a call is made" with one symbol.
- **The examples.** Without the check all 12 conflicts are found and all 12
  are marked: the example's "succeeds once" and "the plan is written once"
  are counts, and the rule is about "a call succeeds" in "a run with a
  plan". The check asks both parts with the words of the example, and 17 of
  the 29 questions on these changes are answered yes.
- **The trap holds.** 59 questions on the "near" changes, none answered yes
  by most; "the card was verified at check-in → a call of `verify_card` is
  made" got 1 or 2 of 8. The one conflict on a "near" change is there
  without the check too: it rests on a wrong answer to the question about
  two outcomes (check 4).
- A change costs 54 requests on these projects.

**Decision.** Step 46 stays as it was frozen. All twenty-two sets are
development data now.

---

## T40 — TestingTheAgents with the question whether a rule applies (2026-11-27)

**Question.** With check 6 as it passed `eval22/` (E31): what do the reports
of the four changes say now, and is the missing approval in the report of
the change that cannot be built?

**How.** Nothing was formalized again. Check 6 was asked on the 131 saved
parts of T38 (`formal_*.json`), and the reports were made from them with
`--formal ... --against "fs-*"`, as in step 2 of the commands in README.md.
A run of the tool today asks the check while it formalizes.

| Change | Conflicts, not doubtful: before → now | Among the rules of the change, with the parts that found each | With a rule of another spec file | Doubtful |
|---|---|---|---|---|
| `add-instant-bulk-takedown-workflow`, cannot be built | 6 → 7 | 3: in 16, 2 and 1 of 24 parts, as before | 3 → 4 | 18 → 19 |
| `add-licence-expiry-sweep-workflow`, can be built | 5 → 5 | 2: in 1 of 24 parts each, as before | 3 | 33 |
| `add-page-retirement-workflow`, can be built | 3 → 4 | 1 in 1 of 23 parts → 2: in 3 and 1 of 23 | 2 | 43 → 38 |
| `add-scheduled-batch-republish-workflow`, can be built | 1 → 1 | 0 | 1 | 16 |

- **The missing approval is reported.** It is the one more conflict of the
  first change, "if the assumed facts hold": the existing rule that nothing
  goes live or down in a plan without an approval, against the change's
  rule that a run of the new workflow asks nobody, in such a run with a
  plan in which a page is taken down. The fact it rests on says that a
  request that was approved is a request that was made (8 of 8 answers).
  The report explains it so, and its second option is to exempt the new
  workflow from the existing rule. It is found in the part that holds the
  spec file of that rule. So two of the authors' four reasons are in the
  report now, this one and the two contracts on one function (16 of 24
  parts).
- **One artefact more, on a change that can be built.** Page retirement, in
  1 of 23 parts: its rule that no takedown succeeds for a page that a live
  page links to, against its example in which such a takedown is refused.
  The step that the check took is right (a call that is refused was made).
  The situation is not: it has a takedown call that succeeds, which the
  example excludes in words and the formulas do not ("refused" and
  "succeeds" are two symbols).
- **A doubt lifted in two parts.** An existing rule about which pages are
  taken down, against an example of that change in which a page is taken
  down: a rule against a special case of it. It was not doubtful in 1 of 23
  parts and is in 3 now, because what the example demands makes the rule
  about a call that succeeds apply.
- The steps the check took: 2, 6, 15 and 3 for the four changes, out of
  2,996 questions asked. 8 of the 15 are between two examples.
- Still not found: the hand-over between two specialists, which needs rules
  of three spec files, and the batch size against the budgets, which is
  arithmetic over the steps of a run.

**Decision.** Nothing to change. The table in README.md is brought up to
date.

---

## T41 — TestingTheAgents from scratch, with the final code (2026-11-27)

**Question.** T40 asked the new question on parts that were formalized
before it existed. What does a run of the tool give today, by the commands
of README.md?

**How.** Step 1 of those commands for the four changes, with the code of
step 46, on two machines with two GPUs each: 32, 44, 47 and 56 minutes for a
change. Then step 2, against the 24 spec files of the application, and the
same parts scored once more without the facts of check 6.

| Change | Conflicts, not doubtful | The same without the facts of check 6 | In the spec files of the change, with the parts that found each | With a rule of another spec file | Doubtful |
|---|---|---|---|---|---|
| `add-instant-bulk-takedown-workflow`, cannot be built | 11 | 8 | 3: in 16, 1 and 1 of 24 parts | 8 | 19 |
| `add-licence-expiry-sweep-workflow`, can be built | 6 | 3 | 2: in 2 and 1 of 24 parts | 4 | 32 |
| `add-page-retirement-workflow`, can be built | 3 | 2 | 0 | 3 | 50 |
| `add-scheduled-batch-republish-workflow`, can be built | 3 | 3 | 0 | 3 | 19 |

- **The two reasons are found again.** The two contracts on one function,
  in 16 of 24 parts as in the first run. And the missing approval, through
  the same step, with 8 of 8 answers. A second conflict of that report is
  close to it and comes from the question about two outcomes: the existing
  rule that taking a page down is guarded, against the change's example in
  which pages go down with no request for approval.
- **The check costs more than T40 showed.** It adds 7 conflicts over the
  four changes: the missing approval, and 6 artefacts (2, 3 and 1 on three
  of the changes).
- **Where it goes wrong.** It said yes to 35 steps (3, 10, 20 and 2), out
  of 2,768 questions. We read them all: 5 are wrong, by our reading.
  - Three have one shape: the rule applies in several cases, and the fact
    is about one of them. A rule "WHEN a call of this tool or of that tool
    is made", and the fact that a call of the second is made: 7 of 8
    answers "yes". A rule about four calls, and a fact about two of them in
    a kind of run. A rule "for any n from 1 to 60", and the fact that the
    request is for 3.
  - Two take one refusal for another: "the call is refused", "the job is
    refused", and the fact that the approver refused.
  - One wrong step gave 3 conflicts, all on one change that can be built.
    And one right step gave an artefact, as in T40.
- **`eval22/` has no case of that shape.** Its trap is a state from before
  the run. So E31 could not see it.
- **From run to run.** Without the facts of check 6 the four changes have
  8, 3, 2 and 3 conflicts here and had 6, 5, 3 and 1 in the first
  formalization (T38): the conflicts with a rule of another spec file are
  mostly different ones each time. The same in both: the two contracts in 16 of 24
  parts, nothing else in more than 3, and the missing approval.
- 4 of 131 parts were not formalized, as before; the limit of 40 left out
  1,755 of 4,523 questions.

**Decision.** Check 6 stays: it met the rule that was set for it, and on
the project it finds the reason it was built for, in two runs of two. Its
wrong steps on real specs are a limit, with their numbers in README.md.
What follows from them is the next step: the question has to be answered
"no" where the requirement applies in several cases and the fact is about
one of them. A new set first (`eval23/`).

---

## T42 — Development: a sentence about rules that apply in several cases (2026-11-27)

**Question.** T41 showed three wrong steps of one shape: the rule applies in
several cases, and the fact is about one of them. Does one sentence in the
prompt of check 6 stop them? The sentence, in its "no": "This is also the
answer when the requirement applies in several cases and B is the case in
only some of them (if it applies when it rains or when it snows, it need not
be snowing)". `eval23/` was written and committed first and is not read.

**How.** Check 6 was asked again with the sentence on saved runs: the runs
of `eval20/`, `eval21/` and `eval22/` (`T42_eval20`, `T42_eval21`,
`T42_eval22`), and the parts of the four changes of the real project from
T41. To ask it again, `--rescore ... --applies-base-url` now drops the
earlier answers of the check first.

- **On our sets nothing changes**: 24 of 24, 15 of 24 and 24 of 24 planted
  conflicts, and the same changes with a conflict as with the prompt of
  step 46.
- **On the project the wrong steps stay.** The rule about two calls and the
  fact about the second: 7 of 8 "yes" before, 7 of 8 with the sentence. The
  rule about four calls: 8 of 8 both times. Of the five wrong steps two
  went, both from 5 of 8 to 4 of 8. And the step that the check was built
  for, from "approved" to "requested", went from 8 of 8 to 6 of 8.
- **Why: the model reads the question backwards.** Its reasons for the
  rule about two calls all go one way: fact B says that the second tool is
  called; so, where the requirement is obeyed, the caller is the agent that
  the requirement names. It takes B as given, finds that the requirement
  then applies, and says yes. The prompt shows B as a fact
  marked TRUE, and asks "Is B then the case?". Where B is one of the cases
  in which the requirement applies, that reading gives a "yes". A sentence
  about several cases does not touch it.

**Decision.** The sentence is not kept: one try, as planned (plan.md 2.4).
What the reasons show is a different defect, with a different remedy: B
must be shown as a statement to judge, not as a given. That is step 48
(plan.md 2.5), and `eval23/`, still unread, is its test.

---

## T43 — Development: the fact as a statement to judge, not a given (2026-11-27)

**Question.** T42 showed that the model reads the question of check 6
backwards: it takes fact B as given and finds that the requirement then
applies. Step 48 (plan.md 2.5) says in the prompt that B is a statement
that is not given, asks "Must B be true there?", and defines "no" by a
counterexample: there can be such a situation in which B is false. Does that
stop the wrong steps, and keep the right ones? `eval23/` is not read.

**How.** As in T42: check 6 asked again on the saved runs of `eval20/`,
`eval21/` and `eval22/` (`T43_eval20`, `T43_eval21`, `T43_eval22`), and on
the parts of the four changes of the real project from T41.

- **On our sets nothing changes**: 24 of 24, 15 of 24 and 24 of 24 planted
  conflicts, and the same changes with a conflict as before.
- **On the project the three wrong steps of one shape are gone**, with no
  vote left:

  | The step | Form of step 46 | New form |
  |---|---|---|
  | a rule about two calls, and the fact that the second is called | 7 of 8 | 0 of 8 |
  | a rule about four calls, and a fact about two of them in a kind of run | 8 of 8 | 0 of 8 |
  | a rule "for any n from 1 to 60", and the fact that the request is for 3 | 5 of 8 | 0 of 8 |
  | from "approved" to "requested", the step the check was built for | 8 of 8 | 8 of 8 |

- **The conflicts that are not doubtful**, on the same parts, against the
  application's specs:

  | Change | Without check 6 | Form of step 46 | New form |
  |---|---|---|---|
  | cannot be built | 8 | 11 | 9 |
  | can be built | 3 | 6 | 3 |
  | can be built | 2 | 3 | 3 |
  | can be built | 3 | 3 | 3 |

  The question now adds 2 conflicts over the four changes, where it added
  7: the missing approval, and one artefact that rests on a right step.
- **What stays wrong.** The two steps that take one refusal for another (5
  and 6 of 8). And one new wrong step, of a kind of its own: a part marked
  FALSE. The requirement says that the plan was written; B is "FALSE: the
  run has a plan". The reasons say that the run has a plan, "making the
  assertion that it is FALSE incorrect", and the answer is "yes": 3 of 8
  before, 7 of 8 now. Parts marked FALSE are rare, 61 of the 2,768
  questions; 2 of them are answered yes, one rightly ("the approver
  refuses", and "FALSE: the approval was granted"). The wrong one adds no
  conflict here: its two rules already clash through a link.
- The steps said yes to: 30, where they were 35 (2, 8, 18 and 2 for the
  four changes).

**Decision.** The form is frozen as planned, for the held-out test on
`eval23/`. The part marked FALSE is written down as a limit: one try.

---

## E32 — Held-out `eval23/`: the fact as a statement to judge (2026-11-27)

**Question.** Does the form of step 48 (T43) stop the wrong step where a
rule applies in several cases, on specs it was not built on, and keep the
chains and the examples?

**The set** (`eval23/`, written and committed before step 47 and not read
until now). Four more projects about an assistant that calls tools: a
veterinary practice, a moving company, a caterer, a credit union. Each has
the rule that a call needs an earlier approved call ("WHEN a call of
`admit_animal` succeeds in a run with a plan THEN an earlier call of
`ask_vet` in the run was approved"), and a rule whose condition names two
calls: "WHEN a call of `ask_vet` or `order_medicine` is made THEN the agent
making it is the reception agent". Three changes each:

| Change | What it adds | Expected |
|---|---|---|
| chain | as in `eval22/`: "WHEN a call of `ask_vet` is made THEN the run is not an emergency run", and a rule about an admission in such a run | the conflict between the first rule and the new one; and the rule about two calls must not be set against the new rule |
| breaks | as in `eval22/`: an example that breaks the first rule by what it demands itself | that conflict, not doubtful |
| several | "WHEN a call of `order_medicine` is made THEN the run is not a check-up run", and a rule about `ask_vet` in such a run. The rule about two calls applies when either is made, so it does not say that `order_medicine` is called | nothing |

**The rule, set before the build** (plan.md 2.5). With doubtful conflicts set
aside, the same runs asked with the form of step 46 and with the new one:
the "several" changes have a conflict about them less often, and the "chain"
and "breaks" conflicts are found no less often. And on the saved runs of
`eval20/`, `eval21/` and `eval22/` no planted conflict is lost and no change
that should give nothing gets a conflict (met in T43).

**Result.** 12 changes, 3 runs each, with the code before step 48
(`E32_eval23_before`); then check 6 asked again on the same runs with the
new form (`E32_eval23`). 25 of the 36 runs finished. Doubtful conflicts are
set aside.

| | Form of step 46 | Form of step 48 |
|---|---|---|
| "several" changes with a conflict about them | 6 of 12 | 0 of 12 |
| "chain" conflicts found | 9 of 10 | 10 of 10 |
| "chain" runs that also set the rule about two calls against the new rule | 5 of 10 | 0 of 10 |
| "breaks" conflicts found | 3 of 3 | 3 of 3 |

- **The rule is met, on the runs that finished.** The set does test the
  change: with the form of step 46 the wrong step is taken in half of the
  runs.
- **The wrong step**, "a call of `ask_vet` or `order_medicine` is made →
  `order_medicine` is called": 2 to 7 of 8 "yes" with the form of step 46
  in the 12 "several" runs, more than half in 6 of them; 0 of 8 with the
  new form, in all 12. None of the 60 questions on those changes is
  answered yes now.
- **The right step stays**: "an earlier call of `ask_vet` was approved → a
  call of `ask_vet` is made" has 4 to 8 of 8 before and 6 to 8 of 8 after,
  in the 10 "chain" runs. The one chain that was missed before had 4 of 8.
- **11 of the 36 runs stopped at the read step**, the same in both columns:
  9 of the 12 "breaks" runs and 2 "chain" runs. In all of them the read
  step returned the rule about two calls as two rules with one label, one
  for each call, and a run whose labels are not kept is not scored
  (`change.changed_rules`). So "breaks" is tested on 3 runs here; on the
  saved runs of `eval21/` and `eval22/` it is 10 of 12 and 12 of 12, as
  before (T43). This has nothing to do with step 48, and it is new: no run
  of `eval20/` to `eval22/` stopped.

**Decision.** Step 48 stays. All twenty-three sets are development data
now. A scenario that the read step splits in two is the next thing to
repair, with `eval24/` first.

---

## T44 — TestingTheAgents with the form of step 48 (2026-11-27)

**Question.** What do the reports of the four changes say with the form
that passed `eval23/`?

**How.** Nothing was formalized again: check 6 was asked with the new form
on the parts of the run from scratch (T41), and the reports were worded
from them, against the application's specs (step 2 of the commands in
README.md).

| Change | Conflicts, not doubtful | The same without check 6 | With the form of step 46 (T41) | In the spec files of the change, with the parts that found each | With a rule of another spec file | Doubtful |
|---|---|---|---|---|---|---|
| `add-instant-bulk-takedown-workflow`, cannot be built | 9 | 8 | 11 | 2: in 16 and 1 of 24 parts | 7 | 19 |
| `add-licence-expiry-sweep-workflow`, can be built | 3 | 3 | 6 | 2: in 2 and 1 of 24 parts | 1 | 32 |
| `add-page-retirement-workflow`, can be built | 3 | 2 | 3 | 0 | 3 | 54 |
| `add-scheduled-batch-republish-workflow`, can be built | 3 | 3 | 3 | 0 | 3 | 19 |

- **The two reasons are in the first report**, as before: the two contracts
  on one function in 16 of 24 parts, and the missing approval, "if the
  assumed facts hold".
- **The question now adds 2 conflicts over the four changes**: the missing
  approval, and one on a change that can be built, which rests on a right
  step and holds under one reading of a rule that is ambiguous; the report
  says so. With the form of step 46 it added 7.
- Still wrong, among the 30 steps said yes to: the two that take one
  refusal for another, and one about a part marked FALSE (T43). None of
  the three adds a conflict in these reports.
- Still not found: the hand-over between two specialists and the batch size
  against the budgets.

**Decision.** The tables in README.md and GUIDE.md are brought up to date.

---

## T45 — Development: what the read step returns when a scenario names two calls (2026-11-27)

**Question.** 11 of the 36 runs of E32 stopped: "the read step did not keep
the scenario labels R2 (it returned the rules R1, R2, R2, R3, ...)". What are
the two rules that come back under one label?

**How.** The read step alone, on the documents of `eval20/` to `eval23/`,
which are all development data, each at three temperatures (0, 0.5 and
0.9): 156 reads. And every saved experiment was searched for a rule id that
came back twice.

- **`eval23/`: 13 of 36 reads have a label twice. `eval20/` to `eval22/`: 0
  of 120.**
- **In all 13 it is the same scenario, with the same words, once for each
  of its two calls.** Only the trigger differs:

  ```
  R2  trigger ask_chef_called      "WHEN a call of ask_chef or hire_waiters is made THEN the agent making it is the order agent"
  R2  trigger hire_waiters_called  "WHEN a call of ask_chef or hire_waiters is made THEN the agent making it is the order agent"
  ```

  So the model does not split the scenario. A rule has one field for the
  event it reacts to, this rule reacts to either of two, and the model says
  so in the only way the answer allows.
- It happens at every temperature: 4, 6 and 3 of 12 documents.
- In the 3,191 saved runs of all experiments an id came back twice only in
  those 11 runs.
- The trigger is used in two places. A conflict between two rules with two
  different triggers is doubted as two events at one moment, when a
  situation is a moment (not with `--whole-run`). And a gap is looked for
  once for each event; there the events in a rule's condition count as
  well. The translations are not shown it.

**Decision.** Step 49 (plan.md 2.6): rules that come back with one label and
the same words are one rule. `eval24/` first.

---

## E33 — Held-out `eval24/`: a rule that the read step returns twice is one rule (2026-11-27)

**Question.** Does step 49 (plan.md 2.6, T45) keep a run going when a
scenario comes back once for each of its events, on specs it was not built
on, and is that rule then in the checks?

**The set** (`eval24/`, written and committed before the code). Four more
projects about an assistant that calls tools: an optician, a zoo, a
self-storage site, a tutoring school. Each has the rule that a call needs an
earlier approved call, a rule whose condition names two calls ("WHEN a call
of `order_lenses` or `order_frame` is made THEN the run writes an audit
entry"), and one whose condition names three ("WHEN a call of
`send_reminder`, `send_offer` or `send_survey` is made THEN the customer has
agreed to messages"). Three changes each:

| Change | What it adds | Expected |
|---|---|---|
| direct | "WHEN a call of `order_frame` is made in a warranty run THEN the run writes no audit entry": the opposite of the rule about two calls, for its second call | that conflict. The rule about two calls must be in the checks, and for both calls |
| breaks | as in `eval22/` and `eval23/`: an example that breaks the first rule by what it demands itself | that conflict |
| quiet | "WHEN a call of `send_survey` is made THEN the run is not a complaint run", and a rule about the approving call in such a run | no conflict |

**The rule, set before the build** (plan.md 2.6). Fewer runs stop than with
the code before; the planted conflicts are found in more of the 24 runs that
have one, a run that stops counting as not found; and the "quiet" changes
have a conflict about them in no larger share of the runs that finish.

**Result.** 12 changes, 3 runs each, with the code before
(`E33_eval24_before`) and with the code of step 49 (`E33_eval24`): two runs
of the whole pipeline, since the read step comes first.

| | Code before | Step 49 |
|---|---|---|
| runs that finished | 25 of 36 | 36 of 36 |
| "direct" conflicts found | 8 of 12 | 12 of 12 |
| "breaks" conflicts found, and not doubtful | 6 of 12 | 11 of 12 |
| "quiet" changes with a conflict about them | 0 of 11 | 0 of 12 |
| other conflicts about a change | 0 | 0 |

- **The rule is met on every point.** With the code before, 11 runs stopped
  (6 "breaks", 4 "direct", 1 "quiet"), each time for both labels: the rule
  about two calls and the rule about three had come back more than once.
  Every planted conflict of a run that finished was found, with either
  code.
- **The rule that came back twice is in the checks for both calls.** From a
  run of the optician's "direct" change:

  ```
  R2  no trigger                   (or order_lenses_called order_frame_called) => audit_entry_written
  R5  trigger order_frame_called   (and order_frame_called run_is_warranty) => (not audit_entry_written)
  conflict R2, R5 in a warranty run in which order_frame is called, from the rules alone
  ```

  In 8 of the 36 new runs the saved model shows the repair: these two rules
  have no single trigger. In the others each came back once, or its copies
  named one event.
- All 12 "direct" conflicts are proven from the rules alone.
- The one "breaks" conflict that is doubtful: the example says "the plan is
  written once", the rule is about "a run with a plan", and the question of
  step 46 did not connect the two in that run (3 of 8 answers).
- **The "quiet" changes are not quiet for gaps, and that is the set's
  doing.** Their second rule, "WHEN a call of `ask_optician` is made in a
  complaint run THEN the answer names the optician", is the only rule that
  reacts to that call, so a call outside a complaint run is a gap by the
  tool's definition: reported about the change in 11 of 11 and 12 of 12
  runs. The "direct" changes get the same kind in every run, doubted by an
  assumed fact in all but 2. `eval22/` and `eval23/` did not have this,
  because there another rule covered the call. The set said "nothing may
  be reported"; that held for conflicts only.
- A change costs 61 requests on these projects.

**Decision.** Step 49 stays. All twenty-four sets are development data now.
On the real project it changes nothing: the 4 parts that could not be
formalized there lost their labels altogether, not for a rule that came
back twice (T41).

---

## T46 — Development: what the wrong answers about two outcomes say (2026-11-27)

**Question.** In the reports of the real project every change has 1 to 6
conflicts with a rule of another spec file that are artefacts (T41, T44),
and most rest on the question about two outcomes (check 4). What do those
answers say?

**How.** No model was asked. The reports of T44 and the parts they were
made from were read: for each conflict that is not doubtful, the assumed
facts it rests on; and for the facts of check 4, the two statements that
the model was shown and the sentence it gave.

- **Half of the conflicts rest on check 4.** The four reports have 18
  conflicts that are not doubtful. 9 of them rest on a fact of check 4, all
  9 with a rule of another spec file; 6 are proven from the rules alone, 1
  rests on the question of step 46 (the missing approval), 1 on a link and
  1 on a voted fact.
- Over the parts of the four changes check 4 was asked 5,052 times and
  called 185 pairs impossible. (Its limit of 40 pairs for a document left
  out 25,980 more.)
- **The wrong answers have two shapes**, by the sentences the model gave:
  1. *How a system works.* A hand-over that succeeds "implies a system
     state change"; a request that is refused "generates an audit event, so
     the audit log cannot be empty"; a tool "cannot be called if the module
     containing it was not imported"; a page "cannot be published if the
     write call to publish it has not succeeded". None of these is in the
     words of the two statements. The second of them does not even need
     the other statement: the model calls one statement impossible by
     itself.
  2. *Two things taken for one.* A limit of 40 tool calls and "no tool was
     called": "a run cannot have zero tool calls if the maximum ... is 40".
     "Every problem is reported for every live page" and "pages without a
     date are left out of the batch". A count of versions after a rollback
     and the list of what a page holds after a replacement. Two examples
     about two pages.
- The right ones are of the kind the check was built for: "a page cannot be
  both republished and in a draft status", "a single call cannot be both
  successful and refused", "never called, and a call that is refused".
- The prompt says "judge only by what the facts mean" and that "possible"
  holds "even if a system would rarely do both". It does not say, as the
  prompts of checks 5 and 6 do, that how a system works is no reason.

**Decision.** Step 50 (plan.md 2.7): the prompt of check 4 is told what does
not count. `eval25/` first.

---

## T47 — Development: the question about two outcomes, told what does not count (2026-11-27)

**Question.** Does the new prompt of check 4 (plan.md 2.7) stop the wrong
answers of T46, and does it keep the right ones? `eval25/` is not read.

**The prompt.** "possible" is also the answer when one statement would
usually cause, need or leave a trace of the other, or of its opposite ("do
not assume how the system works, or that anything succeeds or is written
down"); and when the two can be about two different things ("two objects, a
limit and what happened, all of one kind and some of another"). One
statement that alone looks like something no system would do is no reason.

**How.** Checks 4, 5 and 6 were asked again on saved runs with
`--rescore ... --outcomes-again-base-url` (files `T47_*`), and on the parts
of the four changes of the real project (T44). The three go together: check
5 and check 6 choose their pairs with the facts of check 4. For `eval12/`,
whose saved runs are older than check 6, the three were also asked again
with the old prompt (`T47_eval12_old`).

**The real project**, each change against the application's specs, the same
parts:

| Change | Conflicts, not doubtful: old prompt → new | With a rule of another spec file | Doubtful |
|---|---|---|---|
| cannot be built | 9 → 5 | 7 → 3 | 19 → 9 |
| can be built | 3 → 2 | 1 → 0 | 32 → 21 |
| can be built | 3 → 2 | 3 → 1 | 54 → 35 |
| can be built | 3 → 1 | 3 → 1 | 19 → 7 |

- **The 9 conflicts that rested on an answer of check 4 are all gone.**
  Check 4 calls 98 pairs impossible, where it called 185 (of 5,052).
- **The two reasons of the authors stay**: the two contracts on one function
  (16 of 24 parts) and the missing approval (its step has 7 of 8 answers).
- One of the 9 was close to the missing approval: an existing rule that a
  takedown is guarded, against an example in which pages go down with no
  request for approval. The model had called the two impossible because "a
  tool that requires approval cannot execute without a call to the approval
  mechanism", which is how a system works. It is not reported any more.
- What is left with a rule of another spec file, 5 conflicts over the four
  changes: the missing approval; two that are proven from the rules alone
  and set a property of one call against a property of another; one through
  a link; one that holds under one reading of an ambiguous rule.

**Our sets**, the same runs:

| Set | Planted conflicts found: before → new prompt | Changes or clean specs with a conflict that should have none |
|---|---|---|
| `eval12/` | 34 of 36 as saved, 33 with the old prompt asked again → 32 | 4 of 18 as saved, 3 asked again → 3; conflicts that nobody planted 25, 18 → 12 |
| `eval20/` | 24 of 24 → 24 | 0 of 24 → 0 |
| `eval21/` | 15 of 24 → 15 | 0 of 12 → 0 |
| `eval22/` | 24 of 24 → 22 | 1 of 12 → 0 |
| `eval23/` | 13 of 13 → 12 | 0 of 12 → 0 |
| `eval24/` | 23 of 24 → 24 | 0 of 12 → 0 |

- **What the new prompt loses is one case, the limit we know**: "deletes the
  employee's payslips" against "keep every payslip for ten years", where
  the second rule had become a number, `payslip_retention_years = 10`. The
  old prompt called the two impossible with 5 of 8 answers in two runs (3
  of 8 in one of them when asked again). The new one says "possible" with 8
  and 7 of 8: a setting and what happened are two things. That is right for
  the two statements as they are written, and the rule's own words are
  lost in the translation.
- **No planted conflict that rests on check 4 is lost in `eval20/` to
  `eval24/`**: their facts have 8 of 8 answers before and after.
- **The changes in `eval22/`, `eval23/` and `eval24/` come from check 6, not
  from the new prompt.** None of those conflicts uses a fact of check 4.
  The question of step 48, asked a second time on the same runs with the
  same words, gave the step from "approved" to "called" 3 and 4 of 8
  answers in two runs where it had 8 and 7, and gave another step 6 of 8
  where it had 3. Its answers: some reason rightly ("for a call to be
  approved, it must have been made") and then say "no"; some look for a
  situation in which the requirement does not apply ("if the call does not
  succeed, the requirement imposes no constraints"). So a majority of 8
  answers of that question is not stable. This was not seen before because
  the question had been asked once for each run.

**Decision.** The second half of the rule of plan.md 2.7 is not met as it
was written: on `eval12/` one planted conflict fewer is found (32 against
33, the old prompt asked again), and on `eval22/` and `eval23/` fewer are
found for a reason that is not the change. The prompt is frozen all the
same, for the held-out test on `eval25/`: on the real project 9 conflicts
that rest on wrong answers go and the two right reasons stay, against one
planted conflict that was found on a vote of 5 to 3 from a translation that
had lost the rule. The instability of the question of step 48 is a finding
of its own, and the next thing to repair.

---

## E34 — Held-out `eval25/`: what does not count in the question about two outcomes (2026-11-27)

**Question.** Does the prompt of step 50 (T47) stop the wrong answers of
check 4 on specs it was not built on, and still find a contradiction that is
said in other words?

**The set** (`eval25/`, written and committed before the prompt). Four more
projects about an assistant that calls tools: a plant nursery, a cheese
dairy, a city archive, a radio station. Each has three rules about three
happenings, and three changes that add one rule each:

| Change | The existing rule demands | The new rule demands | Expected |
|---|---|---|---|
| words | "the customer was sent a confirmation in the run" | "no message is sent to any customer in the run" | the conflict: the two exclude each other by the meaning of the words |
| works | "every batch in the cellar is listed as turned at the end of the run" | "`turn_batch` is never called in the run" | no conflict: a working system would not do both, but the words allow it (the batches can have been turned before) |
| other | "every bed of the east house is watered in the run" | "no bed of the west house is watered in the run" | no conflict: two different things |

**The rule, set before the build** (plan.md 2.7). With doubtful conflicts set
aside, the same runs asked with the old prompt and with the new one: the
"works" and "other" changes have a conflict about them less often, and the
"words" conflicts are found no less often. And on the saved runs of
`eval12/` and `eval20/` to `eval24/` no fewer planted conflicts are found
and no more changes or clean specs get a conflict (T47: not met as written,
one planted conflict fewer on `eval12/`).

**Result.** 12 changes, 3 runs each, with the old prompt
(`E34_eval25_before`); checks 4 to 6 asked again on the same runs with the
new one (`E34_eval25`); and a run of the whole pipeline with the new code
(`E34_eval25_full`). Doubtful conflicts are set aside.

| | Old prompt | The same runs, new prompt | A full run, new code |
|---|---|---|---|
| "words" conflicts found | 12 of 12 | 12 of 12 | 12 of 12 |
| "works" changes with a conflict | 3 of 12 | 1 of 12 | 2 of 12 |
| "other" changes with a conflict | 2 of 12 | 2 of 12 | 1 of 12 |
| pairs of a "works" or "other" change that check 4 calls impossible | 7 | 2 | 2 |

- **The first half of the rule is met**: the changes that should give no
  conflict have one in 5 of 24 runs with the old prompt and in 3 with the
  new one, and all 12 planted conflicts are found. The set does test the
  change: the old prompt gives the wrong answers that it was written for.
- **What goes.** "Every batch is listed as turned" and "`turn_batch` is
  never called": impossible with 8 of 8 answers before ("batches cannot be
  marked as turned if the function responsible for turning them is never
  called"), possible now, in 2 runs of 2.
- **What stays.** In the third run of that change the conflict comes from
  a link, not from check 4: "if `close_cellar` succeeds, `turn_batch` must
  have been invoked". The link step makes the same guess, and its prompt
  is not the one that changed. And "no batch is moved in the run" against
  "the run writes one release record that names the batch": 8 of 8 before,
  6 and 5 of 8 now, so still a fact. The model holds that a batch that is
  released was moved.
- **The planted pairs keep their votes**: 8 of 8 in the runs where check 4
  was asked about them, once 7 of 7, and once 7 of 8 in the full run. The
  other runs find the conflict through a shared name or a link.
- In the full run one more guess of the link step shows: "if a price list
  is built, `send_mail` must not have been invoked", from "the code that
  builds it does not import the mail module" (5 of 8).

**Decision.** Step 50 stays. Its rule is met on `eval25/` and not met as
written on the saved runs (T47); the gain is larger than the loss, and both
are in the documents. All twenty-five sets are development data now. Open
after it: the link step guesses how a system works too, and the question of
step 48 does not give the same majority twice (T47).

---

## T48 — Development: which situations count in the question of step 46, in two rounds (2026-11-27)

**Question.** T47 showed that check 6 does not give the same majority twice,
because some answers read "a situation in which the requirement applies" as
any run of a system that has the rule. Does a prompt that says which
situations count (plan.md 2.8) make the answers steady, and what else does
it change? `eval26/` is not read.

**How.** Check 6 alone was asked again on the saved runs of `eval22/`,
`eval23/` and `eval24/`, three times with each form (`T48_<set>_old1` to
`old3`, `new1` to `new3`, `final1` to `final3`), and once with each new form
on the parts of the four changes of the real project. "Steps" below are the
questions between the two rules of a planted conflict, 110 in the three
sets.

**Round 1: the wording.** "Only some situations count: those in which the
condition of the requirement is the case (what comes after WHEN, WHILE or
IF) and in which the system has done everything the requirement demands. A
situation in which the condition is not the case does not count."

| Over three askings, three sets | Old words | Round 1 | Round 2 |
|---|---|---|---|
| planted conflicts found, of 183 askings of a run that has one | 177 | 181 | 182 |
| changes that should give no conflict, with one, of 108 | 0 | 1 | 0 |
| steps with the same vote in all three askings, of 110 | 55 | 95 | 92 |
| steps whose votes differ by 3 or more between askings | 12 | 2 | 1 |

- **The answers are steady.** With the old words half of the steps got
  another vote in another asking, and one went from 8 of 8 to 2. With the
  new words 95 of 110 get the same vote three times.
- **On the real project the model now also says yes where the condition of
  a rule gives the statement.** "WHEN a call of the approval tool returns a
  refusal THEN no step is delegated after it", and the statement "a call of
  the approval tool is made": 0 of 8 with the old words, 8 of 8 now. The
  new answer is the right one. With the old words the model said no for the
  wrong reason: a run in which no call is refused.
- **And the fact that came of it was wrong in its form.** Check 6 wrote
  "where the rule applies and is obeyed, a call is made". The change has a
  rule "WHEN a call of the approval tool is made THEN the run is not an
  emergency run". An emergency run in which a call is refused is a
  situation that this rule forbids by itself, and the search sets such
  situations aside (5.2). But with the demand of the first rule in the fact,
  the solver needs that rule to see it, and reported the two as a conflict:
  2 more conflicts on the change that cannot be built (7, where 5).
- One wrong yes on our sets, in 1 of 36 askings: the rule about two calls
  and the statement that the second is called, 5 of 8. The model read "the
  condition is the case" as "the second call is made".

**Round 2: a yes says what makes the statement true.** The answer got one
more field, "by": "condition" if the statement is true as soon as the
condition of the requirement is the case, whatever the system then does;
"demand" if it takes what the requirement demands. If more of the yes
answers say "condition", the fact is "condition of a => B", without the
demand of a.

- **On the project the 2 conflicts are gone again**: 5, 2, 1 and 1
  conflicts that are not doubtful for the four changes, where 5, 2, 2 and 1
  before step 51. The two steps from a refusal and from a success of the
  approval call are yes with 8 of 8, "condition" with 6 of 8. The step of
  the missing approval is yes with 8 of 8, "demand" with 8 of 8.
- **On our sets** (the last column above): 182 of 183, no change that should
  give no conflict has one, and the votes are as steady as in round 1.
- The wrong yes about a rule with two calls is still given now and then (2
  of 300 askings on `eval23/`, and once on the project, 6 of 8). Each time
  most answers call it "condition", so the fact is about the condition, and
  the situation is one that the other rule forbids by itself: no conflict
  comes of it. The fact is still wrong.

**Decision.** The form of round 2 is frozen for the held-out test on
`eval26/`. The plan said one try; the trial took two rounds, because the
first made the model answer rightly a kind of question whose answer the
code then put into the wrong form. Both rounds are before the freeze, on
development data.

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
