# speccheck: how it works, and where we are

speccheck reads a requirements document written in natural language and
reports what is wrong with it. It follows the formal part of
[Kiro's requirements analysis](https://kiro.dev/blog/deep-spec-analysis/): an
LLM turns the text into logic, the Z3 solver checks the logic, and the results
come back in plain language, each with "A) keep as-is / B) change". It can
also check a *change* against the specs that already exist, as OpenSpec
projects have them (5.10).

| File | Read it for |
|---|---|
| [GUIDE.md](GUIDE.md) | a first reading: a guided tour, every idea from an example, in small steps |
| [README.md](README.md) | the idea, a worked example with real output, how to run it |
| `plan.md` (this file) | where we are, what is next, and how each part works |
| [research.md](research.md) | what we found, with the numbers |
| [research_log.md](research_log.md) | the archive: every experiment and trial in detail. Not needed to understand the project |

---

## 1. Where we are

| Goal | Status |
|---|---|
| **G1** A minimal working prototype of Kiro's formal analysis: spec, formal check, answer in plain language | **Done.** Conflicts, gaps, ambiguities and scenarios, as in Kiro's formal part. Gaps are asked once for each event, and all 18 planted gaps of `eval8/` were found. Both Kiro blog examples found by the solver (`delete_property`: 3 of 3 in the last runs; a wrong voted fact can still hide it). Ambiguities: about half with one model; with the optional second reader 30 and 32 of 36 (held-out `eval4/`, `eval7/`), at up to one extra question per spec |
| **G2** Data-driven: any spec, any format | **Done for the prototype.** 63 base specs in two formats (Kiro EARS, OpenSpec), no change to code or prompts; specs of 30 and of 100 requirements went as well as the small ones (E13, E14), and the read step has room for about 140. An OpenSpec *change* is checked against the specs that exist (`--change`, 5.10): on held-out `eval11/`, 36 of 36 planted conflicts and 36 of 36 planted gaps, and nothing else reported about a change (E17). A gap that a removal opens is reported as the change's, 18 of 18 on held-out `eval13/`, and a conflict the specs had before is never blamed on the change (E19). With `--incremental` a change is checked on a saved model of the specs, for about a seventh of the cost, and finds a little less: 50 against 54 of 54 conflicts on held-out `eval14/` (E20). Not tried: a real OpenSpec project |
| **G3** Code and documents a person can read | **Done** for the current state. GUIDE.md and README.md were revised after a point-by-point review (2026-11-22): each mechanism is a short list of steps on one real example |
| **G4** Research for a paper, on the local model | **Well under way.** 12 held-out tests (E5, E7 to E13, E15 to E18). On the 10 before the questions about outcomes: 61 to 100% of planted conflicts found; with doubtful conflicts set aside, at most 1 false alarm in 18 clean runs, apart from a real conflict we wrote into an `eval9/` clean spec by mistake (2 runs, E15). With those questions (E18, conflicts said in other words): 34 of 36, and 3 of 18 clean runs with a conflict that was not planted. Planted gaps 18 of 18 in each of the last three sets (E13, E15, E16). Still small: one main model, specs written by us |
| **G5** Only the formal part | **Done.** An LLM review of the text was built, measured, and switched off |

In short: the pipeline works end to end, finds what Kiro's blog finds, and
holds up on specs it was not built on. Conflicts that are likely artefacts
(two events at once, or a situation the facts call impossible) are marked
*doubtful*, and with those set aside almost no false alarms are left. The mark
depends on knowing which event each rule reacts to, and the read step names it.

Conflicts said in other words ("take the price" against "refuse all
payments") were the main misses. Since step 32 the model is asked about such
pairs of outcomes, which finds most of them and also reports more conflicts
that nobody planted (5.7, research.md 3.13 and 4.6). What is still missed is
mostly a retention period that became only a number.
A second local model, used as an independent reader,
finds most of the ambiguities, at the cost of more questions to the author.
A finding that holds with only one reading of an ambiguous rule now says so,
and each ambiguity says what its other reading would change (5.9).
A change to specs that already exist, as OpenSpec projects have them, can be
checked too: the report shows what the change breaks (5.10).

---

## 2. What is next

The check of an OpenSpec change is built (step 31, 5.10), and so are the
questions about pairs of outcomes (step 32, 5.7). Three candidates follow, in
this order:

1. **A larger evaluation** (G4): another main model, the second reader on
   more sets, specs we did not write, and results counted per planted
   conflict (the runs of one spec mostly agree, so more specs help more than
   more runs). For the change check: a real OpenSpec project with its
   history of changes. All fourteen sets have been read (`eval14/` in E20), so
   a new design needs `eval15/`, written first.
2. **The change check, further** (G2). The gap that a removal opens is done
   (step 33), and so is a way to check a change on a saved model of the
   specs (step 34, `--incremental`). What is left:
   - the saved-model way misses a few conflicts that the full run finds (4
     of 54 on `eval14/`): a new rule read on its own can get an event of the
     saved model as its trigger and then be rejected (research.md 4.5);
   - the specs of a project must still fit one read answer, about 140
     scenarios. The same step that adds a change to a saved model could add
     the spec files one by one, which would lift that bound. Not tried.
3. **The choice of symbols** (G1), which is where the remaining misses and
   false alarms come from:
   - two symbols for one outcome ("take the price", "refuse all payments").
     Done in step 32: the questions about pairs of outcomes find 13 of the 21
     conflicts that were missed on `eval3/` to `eval10/`, and 34 of 36 on
     `eval12/` (T22, E18). What is left: a retention period that became only
     a number ("keep for ten years" as `payslip_retention_years = 10`) is
     found in some runs and not in others; and on a long spec only the first
     40 pairs are asked about, of several hundred.
   - the price of step 32: more conflicts that nobody planted, among them
     artefacts of the one snapshot ("release the coat" against "list the
     coat as unclaimed after 30 days"; research.md 4.6). A mark for them, as
     for two events at once, has not been tried.
   - two symbols for complementary conditions ("the slot is free", "the slot
     is taken"). They give doubtful conflicts, and since step 26 also the
     false alarms of the gap search (3 to 5 of 18 clean runs per set). Tried
     once (step 30): a gap the assumed facts rule out is marked doubtful, but
     the facts rarely say that one of the two always holds, so only 2 of 13
     were marked (T20, E16). This is a known limit now.

Small things that are open:

- **The wording of a finding that depends on a reading** (E13). The model now
  names the two readings correctly, but in the one report we looked at it
  wrote the gap as if it were the ambiguity, and ended with "Which did you
  mean?". One sentence in the wording prompt would probably settle it; it
  needs a run with the LLM to check.
- **Long documents** (E14). A spec of 100 requirements works: its read answer
  is 16,799 tokens, which the new limit of 24576 holds (about 140
  requirements; the server's window of 32,768 tokens is the real bound). Three
  things do not scale yet. The second reader cannot run: a translation prompt
  with 206 symbols has 4,234 tokens, and its server allows 6,144 for prompt
  and answer with 4,096 kept for the answer; the answers are about 60 tokens,
  so a lower answer limit for translations would make room. A gap in the
  report lists every other event as FALSE, about 70 lines at this size. And
  the solver stage takes 35 s per model instead of under 1 s.

Decided on 2026-11-22: **the samples stay at temperature 0.7** (T17). On
`eval8/`, 0.3 and 0.5 changed nothing for conflicts, gaps or false alarms;
two runs at 0.7 differed more in ambiguities (14 and 20 of 36) than the
temperatures did; and at 0.3 the ambiguities of "only" fell from 8 of 9 to 3.
The read step's retry temperatures (now 0 → 0.3 → 0.9) are never reached at
temperature 0: the first answer was usable for all 204 specs (T18).

Decided on 2026-11-23: **the facts vote adds missing outer parentheses**
(`>= x 0` becomes `(>= x 0)`, the most common slip, T19). On the saved runs
it recovered one planted conflict (3 runs) and lost nothing; on held-out
`eval9/` it added 17 facts, all bounds, and changed no finding (E15).

Decided on 2026-11-24: **a gap that the assumed facts rule out is marked
doubtful, and the facts prompt names the case "one of two things is always
the case"** (T20). It broke nothing: on held-out `eval10/`, 18 of 18 planted
conflicts, no other conflict at all, 18 of 18 planted gaps (E16). It also
helps little, because the model rarely votes such a fact: none of the 5
false gaps of `eval10/` was marked. The false gaps from two complementary
symbols stay, as a known limit, and are not tried again.

Decided on 2026-11-24: **the questions about pairs of outcomes stay on by
default** (step 32, 5.7). On the saved runs of `eval3/` to `eval10/` they
raise the planted conflicts found from 132 to 145 of 153, and the clean runs
with a conflict that was not planted from 3 to 13 of 144 (T22). On held-out
`eval12/`: 27 to 34 of 36, and 0 to 3 of 18 (E18). The gain is larger than the
loss, and each added conflict quotes the fact it rests on. The rule for such
decisions from now on: when the gains are larger than the losses, the new
version becomes the default, and the loss is written down as a limit.

Decided on 2026-11-24: **checking a change on a saved model of the specs is
an option, `--incremental`; the full run stays the default** (step 34, 5.10).
The rule was set before the test: the new way becomes the default only if it
finds as much. On held-out `eval14/` it found 50 of the 54 planted conflicts
against 54, and the same 36 of 36 gaps, for 9 requests to the LLM for a change
against 68 (E20). It is the cheaper way, not the better one.

Decided on 2026-11-24: **what a change removes stays in the merged document,
apart** (step 33, 5.10). The removed scenarios are formalized with the rest
and taken out before the checks; for each, Z3 is asked whether its own
situation is still covered. On held-out `eval13/` the gap of a removed
requirement was reported as the change's in 18 of 18 runs, and the conflict
that the specs had before in 0 of 108 (E19). Nothing was lost on `eval11/`
(T23). Inside a rewritten requirement, a scenario with the same words now
counts as existing.

Decided on 2026-11-24: **an OpenSpec change is checked by merging it into the
specs and running the pipeline as it is** (5.10). The prompts did not change:
the scenario labels that our code writes into the merged document came back
as rule ids in 159 of 159 runs (T21, E17). Kept simple on purpose: every
scenario of a modified requirement counts as changed, nothing is cached, and
a gap opened by a removed requirement is not attributed to the change.

Time ("then", "after", "until") is not planned. The model is one snapshot.

---

## 3. Terms

Every term used later is defined here.

| Term | Meaning |
|---|---|
| **requirement**, **rule** | One statement of what the system shall do, and when. It has an id such as `R2`. The code says "rule". |
| **symbol** | A named variable for one observable fact, e.g. `inventory_available`. Its sort is Bool, Int, Real or Enum. |
| **situation** | One value for every symbol: a snapshot of the system. There is no time, only one snapshot. |
| **formula** | A logical expression over symbols, written in SMT-LIB: `(and order_submitted (not inventory_available))`. |
| **antecedent**, **consequent** | The two halves of a rule in logic: *when* it applies, and *what* must hold then. The rule means `antecedent => consequent`. |
| **translation** | One LLM answer that turns one rule into an antecedent and a consequent. |
| **sample** | One of N independent LLM answers to the same question. N is 8 by default. |
| **solver** | Z3. Given formulas, it answers "satisfiable" (and gives a situation) or "unsatisfiable" (no such situation exists). |
| **witness** | A concrete situation shown to the user as evidence. Stored as `when`, e.g. `{"order_submitted": true}`. |
| **assumed fact** | A statement that is true because of what the words mean: "access cannot be both granted and denied". The LLM proposes it; the spec does not state it. So it is an *assumption*, and it may only add findings, never remove one. |
| **link** | An assumed fact of one kind: what one requirement demands, said with the outcomes of the other requirements ("removing the record means it is not retained"). |
| **formal model** | One `formal.json`: the symbols, the assumed facts and the rules in logic. |
| **symbol set** | The symbols of one formal model. The same document can be formalized several times, each time with its own symbol set. |
| **question** | A concrete situation, chosen by Z3, about which the LLM is asked what ONE requirement says. Used to test translations and links (step 6, 5.7). |
| **second reader** | Optional: a second local model, of another family, that translates every rule again; where its reading differs from the translation, the rule is reported as ambiguous (step 7, 5.8). |
| **event** | A yes/no symbol for something that happens at one moment (a request, a click, an arrival). The read step marks each symbol as an event or not. |
| **trigger** | The event a rule reacts to, named by the read step: "WHEN a visitor signs up ..." reacts to `visitor_signed_up`. A rule that reacts to a state ("WHILE ...") has none. |
| **doubtful** | A mark on a proven conflict or gap that is likely an artefact of the model (5.2, 5.4). Doubtful findings are reported, marked, never removed. |
| **finding** | One thing reported to the author. There are four types: |

| Finding type | It says | Who decides |
|---|---|---|
| **conflict** | some requirements cannot all be obeyed in a situation | the solver |
| **gap** | in a situation, no requirement applies | the solver |
| **ambiguity** | one requirement has two readings | LLM samples (and, optionally, a second model's), compared by the solver; or the LLM's answers to questions |
| **scenario** | a behaviour the requirements allow, or a situation they rule out, that the author may not have intended | the solver proves it; an LLM judge decides whether it is worth showing |

---

## 4. The pipeline

```
 requirements document      any format: Kiro EARS, OpenSpec, plain text
        │
        ▼
┌───────────────── formalize.py ─────────────────────────┐
│ 1 read     LLM x1          → rules, triggers, symbols  │──► llm.py ──► model server
│ 2 sample   LLM xN per rule → antecedent / consequent   │
│ 3 cluster  group the N samples by meaning              │──► logic.py (Z3)
│            (Z3: does any situation tell two apart?)    │
│            → accepted / ambiguous / rejected           │
│ 4 facts    LLM xN          → domain facts              │
│            keep the facts most of the N answers imply  │
│            (Z3: does an answer imply the fact?)        │
│ 5 links    LLM xN per rule with a private outcome      │
│            → that rule in the other rules' terms       │
│ 6 probe    Z3 picks situations, LLM x8 per question    │──► probe.py
│            → do the words decide between two readings? │
│            → do the words demand what a link says?     │
│            → does a requirement agree with the facts   │
│              that make it impossible to obey?          │
│ 7 second   optional: a second model xN per rule        │──► second model server
│            Z3: same meaning as the translation?        │
└───────────────┬────────────────────────────────────────┘
                ▼
          formal.json        the ONLY input of the checks; readable, editable
                │            (with --symbol-sets K: K of them, one per symbol set)
                ▼
┌───────────────── checks.py (Z3 only, no LLM) ──────────┐
│ ambiguity : samples split, step 6 answers say the      │──► logic.py (Z3)
│             words do not decide, or the second model   │
│             reads it otherwise (settled)               │
│ conflict  : force 1, 2 or 3 rules to apply,            │
│             smallest clashing set                      │
│             run 1: rules alone        (proven)         │
│             run 2: + assumed facts    (adds only)      │
│             marked doubtful: needs two events at once, │
│             or the facts rule the situation out        │
│ gap       : for each event, a situation where no rule  │
│             applies; then one with no event            │
│ scenario  : behaviours the rules allow or rule out     │
│ readings  : each ambiguous rule once more, with its    │
│             other reading: which findings change?      │
│ combine   : K formal models → "found with k of K"      │
└───────────────┬────────────────────────────────────────┘
                ▼
          findings           rule ids + a witness situation
                │
                ▼
┌───────────────── explain.py ───────────────────────────┐
│ explain  LLM x1 per defect → explanation, A) and B)    │──► llm.py
│ judge    LLM x1 per scenario → keep the surprising     │
│ render   → findings.json, report.md                    │
└────────────────────────────────────────────────────────┘
```

The code, in the order to read it:

| File | Lines | Job | Uses |
|---|---|---|---|
| `speccheck/llm.py` | 80 | One function: prompt + JSON schema in, N parsed answers out | the model server |
| `speccheck/logic.py` | 250 | Symbols to Z3 variables; parses formulas; asks the solver, including the test "do these two rules mean the same?" | Z3 |
| `speccheck/formalize.py` | 790 | Stage 1: text to `formal.json` (steps 1 to 5, then 6 and 7); `formalize_sets` for K symbol sets; with `base`, adds new rules to a formal model that exists | `llm`, `logic`, `probe` |
| `speccheck/probe.py` | 600 | Stage 1, step 6: four checks by simple questions, three about one requirement and one about the outcomes of two | `llm`, `logic` |
| `speccheck/checks.py` | 750 | Stage 2: `formal.json` to findings; which findings depend on a reading; scenarios; `combine` for K formal models | `logic` |
| `speccheck/explain.py` | 370 | Stage 3: findings to plain words; the scenario judge; builds `report.md` | `llm` |
| `speccheck/cli.py` | 180 | Runs the three stages, writes the files; with `--change`, on the specs of an OpenSpec project with a change applied | all |
| `speccheck/change.py` | 440 | For `--change`: applies an OpenSpec change to the specs that exist, labels the scenarios, and says which findings involve the change (5.10) | `logic` |

About half of each file is comments, docstrings and prompts.

Around the package:

| File | Job |
|---|---|
| `tests/` | 42 tests of everything that needs no LLM |
| `experiments/make_eval.py` | writes the evaluation sets `eval` to `eval11`, `size` and `size2` into `experiments/sets/` (clean specs and planted defects) |
| `experiments/results/` | every experiment: the raw data (`.json`) and its tables (`.md`) |
| `experiments/evaluate.py` | runs the pipeline on a set of specs and scores it against the planted defects; adds the second reader to saved runs; re-scores saved runs without a GPU |
| `experiments/slurm/serve.sbatch`, `experiments/slurm/serve_second.sbatch` | start the main model and the second model on the cluster (section 8) |
| `experiments/stability.py` | the earlier experiments E1 to E3: the same spec many times under several settings |
| `experiments/fact_threshold.py` | redoes the vote on facts with other thresholds, on saved runs |
| `speccheck/refine.py` | optional LLM review of the text, off by default (section 9) |

**Who decides what**
- the LLM: translates, proposes facts and links (stage 1); words the result,
  scores how surprising a scenario is (stage 3)
- Z3 alone: every conflict, gap and scenario (stage 2)
- so a finding is a proof *about `formal.json`*. Whether `formal.json` says
  what the author meant: the ambiguity check, the support counts and the
  listed assumptions help to judge

---

## 5. How each decision is made

Each rule *i* is `A_i => C_i` (antecedent, consequent).

### 5.1 Is a requirement ambiguous? (`formalize.py`, steps 2 and 3)

- the rule is translated N times
- two translations *a* and *b* mean the same when no situation is allowed by
  one and forbidden by the other:

```
(A_a => C_a)  differs from  (A_b => C_b)      unsatisfiable?
```

- our code puts the N translations in groups: each one joins the first group
  whose first member Z3 proves it means the same as, or starts a new group
- the spread of the groups (entropy) decides the status. With 8 samples:

| Split | Status | Effect |
|---|---|---|
| 8, or 7/1 | accepted | the largest group is used |
| 6/2, 5/3 | ambiguous | used; the second group is the other reading, and the question of 5.7 decides |
| 4/2/2 and wider | rejected | left out of the checks; must be rewritten |

- this finds where the model is unsure
- a split is not final: the question of 5.7 decides between the two groups
  (a split can be noise). Only a split no question could be built for is
  reported as it is (`found_by: samples`)
- it finds nothing where all 8 samples agree on one reading of ambiguous
  words. That is what the other two ways are for: the questions (5.7) and the
  second reader (5.8)

### 5.2 Do requirements conflict? (`checks.py`)

- "can all rules hold together?" is useless: every implication holds when
  nothing applies
- so the check forces rules to apply. For every single rule, every pair and
  every triple of rules `G`:

```
1. A_G                  satisfiable?    the situation can happen
2. A_G and all rules    unsatisfiable?  nothing the system does would obey them all
```

- when both hold, Z3 names the rules it needed for the contradiction (the
  "unsat core", shrunk until no rule can be dropped), and a situation of
  step 1 is the witness
- not a conflict: one rule alone forbids the situation (forcing "account
  locked" for an administrator, against "never lock administrators")
- dropped: a conflict that contains a smaller reported conflict
- not tried together: rules that share no symbol, directly or through other
  rules and the facts. They cannot contradict each other, so forcing them to
  apply together could only find again what each shows alone. In a document
  about one subject this changes nothing; in a document made of unrelated
  parts it saves most of the work (research.md 3.11)

**Doubtful**: two marks. A marked conflict stays in the report.

- **Two events at the same moment**
  - one snapshot lets any events coincide: "a visitor signs up" and "a
    subscriber changes the address", with "send no email" against "send a
    confirmation email"
  - requirements are written for one event at a time, so a conflict between
    rules that react to two different events is marked
  - the read step names, for each rule, the event it reacts to (its *trigger*):
    ```
    N1  "WHEN a visitor signs up ..."                 trigger: visitor_signed_up
    N5  "WHEN a subscriber changes the address ..."   trigger: address_changed
    conflict {N1, N5}: two different triggers  → doubtful
    ```
  - the trigger counts even when the translation leaves the event out: "the
    doors fail to close for the third time" is often translated as the count
    alone, `(= door_close_failures 3)`, which looks like a state (E9)
  - a rule that reacts to a state ("WHILE ...") has no trigger
  - formal models made before triggers were named: the events in the
    antecedents are used instead
- **A situation the facts call impossible**
  - "at least 24 hours" and "less than 24 hours" as two yes/no symbols: both
    can be true for the solver
  - an assumed fact (5.3) says they exclude each other

Result on the held-out `eval3/`: every marked conflict was a false alarm;
setting them aside cut false alarms on clean runs from 9 to 1 of 18 (E8).

### 5.3 Which facts are assumed, and how are they used?

- two requirements can demand opposite things in different words: with "grant
  access" and "deny access" as two symbols, the solver sees no clash
- an assumed fact connects them:

```
R1:  password_correct => access_granted   ─┐
R4:  account_locked   => access_denied    ─┼─► unsatisfiable when both apply
F2:  not (access_granted and              ─┘   → conflict {R1, R4}, depends on F2
          access_denied)
```

**Choosing the facts** (`formalize.py`, step 4)
- the LLM is asked N times for facts that hold "purely because of what the
  symbols mean"
- it sees the symbols only, not the requirements
- every fact in every answer is a candidate, and the N answers vote on it:
  answer k votes for a candidate when the candidate follows from answer k's
  own facts
- a formula that does not parse is dropped, except that missing outer
  parentheses are added back (`>= x 0`, 3.4% of all facts, T19, E15)

```
facts of answer k  and  not candidate      unsatisfiable?     answer k votes for it
```

- a candidate with the votes of more than half of the N answers is kept

- so "a and b exclude each other" and "a implies not b" count as the same vote

**Using the facts** (`checks.py`): facts are guesses, so they may only add:

```
run 1   conflict search with the rules alone   → proven findings
run 2   the same search with the facts added   → keep only conflicts that need a
                                                 fact and are not explained by run 1
```

- a fact never removes or changes a finding of run 1
- a conflict of run 2 names the facts it needed
- one rule against the facts is not reported, only two or more rules (with
  one snapshot, "WHEN the door is open, close it" contradicts "a closed door
  is not open" by design)
- a fact never removes a gap either; it can only mark one as doubtful (5.4)

**Links: a second source of facts** (`formalize.py`, step 5)
- a symbol that only one rule uses hides meaning: "the record is removed", as
  a symbol of its own, cannot clash with "the record is retained"
- such a rule is translated N more times, and this time the model may use only
  the rule's own condition and the *outcomes of the other rules*:

```
rule D2          confirmed => record_removed             (record_removed is private)
asked again      "remove the Property record", with the other rules' outcomes
8 of 8 answers   confirmed => (not record_retained)         (experiments/examples/delete_property_links)
link (a fact)    (confirmed and record_removed) => (not record_retained)
```

- when more than half of the answers agree on one meaning, it becomes an
  assumed fact with its support, used like the others: add-only, and named by
  every conflict that needs it
- "cannot be expressed" is a valid answer, and counts against a link
- why this works where the read step does not: choosing symbols, the model
  describes "removed" so that it fits the soft-deletion rule; asked to say D2
  with the other rules' outcomes, it takes the words literally
- a link can still be wrong ("a confirmation message" taken for "a
  confirmation prompt"), so each link is checked by a question (5.7) before it
  is used
- a link is kept even when the voted facts already imply it: a fact may be
  rejected later (check 3)

**Questions about pairs of outcomes: a third source of facts** (`probe.py`,
step 6, check 4)
- for two rules that can apply together and demand things with no symbol in
  common, the model is asked whether both outcomes can hold; "impossible"
  from more than half of the answers is an assumed fact (5.7)

**Facts that contradict a requirement** (check 3, 5.7)
- voted facts can be wrong in a way that hides conflicts: with "a deleted
  property has its record removed" and "a removed record is not retained", D4
  (soft deletion: retain the records) is impossible to obey wherever it applies
- a conflict needs two rules that clash, not one rule against the facts, so
  every conflict of D4 disappears
- so such facts are put to the LLM with the requirement's words

### 5.4 Is a situation uncovered? (`checks.py`)

```
not A_1 and ... and not A_n      satisfiable?
```

Nearly every spec has a gap in which nothing happens at all. No rule applies
there because nothing happened, and a system normally just waits, so this gap
is rarely something to fix. The gaps worth reading are those in which
something happens. So when the rules
react to events, the question is asked once for each event, with no other
event at the same moment (requirements are written for one event at a time):

```
rules    "WHEN a courier scans a parcel AND a compartment is free THEN ..."
         (the rule for "no compartment is free" is missing)
event    parcel_scanned
ask      parcel_scanned and no other event, and no rule applies:   satisfiable?
gap      parcel_scanned TRUE, compartment_free FALSE
```

- at most one gap for each event some rule reacts to: the event named as a
  rule's trigger, or used in a rule's condition
- then one gap in which no event happens, marked "no event happens". For the
  order spec this is the gap of the Kiro blog: "no order submitted, none
  canceled"
- the situation found is trimmed to the symbols that matter; the event stays
- rules that always apply, like "SHALL NOT backorder", do not count as coverage
- without events to go by (a formal model made before they were marked, or
  rules that react to states only), the search is as it was: over all
  situations, with the gap found excluded and the question asked again, at
  most 3 gaps
- the assumed facts only mark a gap: when they rule out every uncovered
  situation for an event, the gap is still reported, marked doubtful, with
  the facts that rule it out (`doubted_by`). In the laundry spec,
  `slot_is_free` and `slot_is_taken` are two symbols, so "books a slot"
  with neither is uncovered; the fact `(or slot_is_free slot_is_taken)`
  rules that out. The model rarely votes such a fact (T20, E16)

### 5.5 What do the requirements allow or rule out? (`checks.py`, `explain.py`)

- a scenario is not a defect: it is a consequence of the rules that the
  author may not have intended
- gap or scenario? A gap is a situation no rule speaks about. A scenario is
  something the rules do decide (allowed, or impossible), maybe not as meant:
  in the order spec, "an order fulfilled that was never submitted" is allowed
- the solver proves two kinds:

```
allowed     all rules  and  not A_i  and  C_i            satisfiable?
            what rule i demands may also happen when rule i does not apply
            ("the order is fulfilled although it was never submitted")

ruled out   A_q and A_r  satisfiable,  but  A_q and A_r and C_r  unsatisfiable
            rule q would apply in a situation that rule r alone makes impossible
            ("a locked administrator account")
```

- one candidate per rule or pair; most are unremarkable
- an LLM judge reads each one next to the document's goal and keeps the
  surprising ones
- the scenario itself is proven; the judge only decides whether to show it

### 5.6 Does a finding depend on the choice of symbols? (`formalize.py`, `checks.py`)

- the read step chooses the symbols, and everything follows from that choice
- `--symbol-sets K`: the document is formalized K times, once as usual and
  K-1 times with the read step at a higher temperature, so that it picks
  other symbols
- all K formal models must list the same rules

```
formal model 1 ─► findings ─┐
formal model 2 ─► findings ─┼─► combine ─► each finding with "found with k of K"
formal model K ─► findings ─┘
```

- findings are matched by what they are about: a conflict by its set of
  rules, an ambiguity by its rule, a scenario by its kind and rules
- gaps cannot be matched (a gap is a situation over one model's own symbols):
  the gaps of the first model are kept

### 5.7 Four checks by questions (`probe.py`, step 6)

- all 8 samples can agree and still be wrong: one model tends to make the same
  choice every time
- so step 6 does not ask for more translations. The LLM gets ONE requirement,
  on its own, and ONE concrete situation that Z3 picks, or one statement, and
  says what the words of the requirement decide about it
- each question is asked 8 times; the answers are counted

**Check 1: is the translation the only reading of the words?**

```
rule           "WHEN the number of failed attempts reaches 5 THEN lock the account"
translation    (= failed_attempts 5) => account_locked     step 3: 8 of 8 samples
other reading  (>= failed_attempts 5) => account_locked    proposed by the LLM
situation      failed_attempts = 6, account_locked FALSE   picked by Z3
               translation says: obeyed     other reading says: broken
question       Do the words decide which reading is meant?  A / B / either
```

- 8 answers, half of them with the two readings swapped
- the translation stands when it gets more than half of them; otherwise the
  rule is reported as ambiguous
- when the samples of step 3 split, their second group is the other reading
- the experiments also score the stricter "7 of 8" (research.md 4.1)

**Check 2: does the rule demand what its link says?**

```
link of D2     (confirmed and record_removed) => (not record_retained)      (5.3)
situation      confirmed TRUE, record_retained TRUE
               picked by Z3: D2 applies, and the link's claim is false
question       D2, fully obeyed: could this situation still be true?
               possible / impossible / unclear
verdict        more than half say "impossible" → the link is used; otherwise not
```

**Check 3: does a requirement agree with the facts that contradict it?**

```
requirement    D4 "retain Property records in the database for audit purposes"
voted facts    "a deleted property has its record removed"
               "a removed record is not retained"
               proven by Z3: together they make D4 impossible to obey
question       for each of these facts: does D4 agree with it?
               agrees / contradicts / unclear
verdict        more than half say "contradicts" → the fact is left out
```

- for each requirement, Z3 is asked whether the voted facts make it impossible
  to obey; if so, our code cuts the facts down to the smallest set that still
  does it
- "more than half" against a voted fact: it already has a majority behind it

**Check 4: can what two requirements demand both be the case?**

The first three checks are about one requirement. This one is about two, and
it adds assumed facts. From `experiments/sets/eval7/canteen_overlap`:

```
C1   "WHEN a student taps the card at the till AND the card balance covers the meal,
      THE Canteen System SHALL take the price from the balance."
     (and card_tapped (>= card_balance meal_price)) => payment_taken
C6   "WHILE the canteen is closed for holidays, THE Canteen System SHALL refuse all payments."
     canteen_closed_for_holidays => payment_refused

pair        C1 and C6 can apply together; payment_taken and payment_refused
            are two symbols, so to Z3 both can be true: no conflict
question    Statement A: TRUE: payment_taken (The system has deducted the meal price ...)
            Statement B: TRUE: payment_refused (The system has declined the payment request)
            Can A and B both hold in the same snapshot?  possible / impossible / unclear
answers     8 of 8 "impossible"
fact        (not (and payment_taken payment_refused))
            "A payment cannot be successfully taken and refused at the same time."
conflict    C1 and C6, "if the assumed facts hold"                    (5.3, run 2)
```

- our code and Z3 pick the pairs. A pair is asked about when both rules can
  apply in one situation that the facts allow; they do not react to two
  different events (that conflict would be doubtful anyway); what they demand
  shares no symbol, and no fact already excludes the two; and what each
  demands is one definite state of its symbols (not "x or y")
- the model sees the two outcomes only, as facts with their descriptions. It
  does not see the requirements: as in step 4, it is asked what the symbols
  mean, not what the system should do
- more than half of the 8 answers "impossible" → an assumed fact, used like
  the others: add-only, and quoted by every conflict that needs it
- in this spec 4 pairs were asked about. "Refuse all payments" was also
  called impossible together with "add the top-up to the balance" (C3), a
  conflict nobody planted, and possible together with the other two
- at most 40 pairs are asked about, the first ones in the document
  (`MAX_PAIRS`). A spec of six rules has 2 to 5; one of 100 requirements has
  several hundred
- what it finds and what it costs: research.md 3.13 and 4.6

### 5.8 A second reader (`formalize.py`, step 7, optional)

- one model's 8 samples can agree with each other even on a rule that two
  people would read in two ways, because they all come from the same model
- a second model, of another family, is an independent reader
- it gets exactly the prompt of step 2 and answers 8 times; for each answer,
  Z3 is asked whether it means the same as the translation, and our code
  counts the ones that do:

```
rule           "WHEN a comment has been reported three times THEN hide it"
translation    (= report_count 3) => comment_hidden     main model, 8 of 8 samples
second model   (>= report_count 3) => comment_hidden    5 of its 8 answers
               (= report_count 3) => comment_hidden     3 of its 8 answers
verdict        3 of 8 mean the same: not more than half → ambiguous
```

- the translation stands only if more than half of the second model's answers
  mean the same (the majority rule of facts, links and questions)
- otherwise the rule is reported as ambiguous, with the second model's most
  common other reading
- the two readings are compared only where the events that the translation's
  condition requires happen: one model may write "the delivery fails for the
  second time" with the event `delivery_failed`, the other with the count
  alone, and that is not another reading (T13)
- held-out sets (E9, E12): 30 and 32 of 36 planted ambiguities found instead
  of 14 and 17; 15 and 9 rules of clean specs flagged instead of 7 and 5
- off by default: `--second-base-url`

### 5.9 Which findings depend on the reading of an ambiguous rule? (`checks.py`)

An ambiguous rule has two readings, and the checks use the first one. Which
one the author meant is exactly what is not known, so a conflict or a gap may
exist only because of that choice. The report has to say so, in the same way
as it says "if the assumed facts hold".

After the checks, each ambiguous rule is tried once more with its other
reading, one rule at a time, with all the other rules as they are. Z3 only:

```
R3          "WHEN the number of failed attempts reaches 5 THEN lock the account"
reading 1   (= failed_attempts 5)    used by the checks
reading 2   (>= failed_attempts 5)

gap         "6 failed attempts, no password submitted": no rule applies
            with reading 2, R3 applies there
            → the gap is reported as "depends on the reading of R3"
```

- a conflict that is not found with the other reading, and a gap in which a
  rule applies with the other reading, are marked with the rule's id
- the ambiguity itself lists what its other reading changes: the conflicts
  that are gone, the conflicts that appear, and the number of gaps covered
- ambiguities whose answer changes another finding are shown first. The
  others say "changes no conflict and no gap", so the author can see that the
  question is less urgent
- nothing is removed and no finding is added, so the counts of the evaluation
  are the same with and without this step
- not covered: a finding that needs the other reading of two rules at once

On the saved runs of `eval2/` to `eval7/`: research.md 3.9.

### 5.10 Does a change fit the specs that exist? (`change.py`, `cli.py --change`)

In an OpenSpec project the specs say what the system does today, and new work
arrives as a *change*, a folder that holds only the difference. The question
is what the change breaks in the specs that exist.

```
openspec/specs/auth/spec.md                        existing
    "WHEN the number of failed attempts on an account reaches 5 THEN the system locks the account"
openspec/changes/admin-never-locked/specs/auth/spec.md      the change
    ## ADDED Requirements
    "WHEN the account belongs to an administrator THEN the system does not lock the account"
```

Neither file has a conflict on its own. Together they do. Run on
`specs/auth_change`:

| Step | Who | What |
|---|---|---|
| 1 merge | our code (`change.merge`) | applies the change to the specs: RENAMED, then REMOVED, MODIFIED, ADDED, matched by the requirement's name. Writes all spec files into one document, `merged.md`, with a label in every scenario header (`#### Scenario R3: Lockout threshold`), and notes that R5 is added. What the change removes stays in the document, labelled X1, X2, ... |
| 2 formalize | the LLM and Z3 | `merged.md` goes through stage 1 like any spec. The read step uses the labels as rule ids. Prompts and `formalize.py` know nothing about changes |
| 3 set apart | our code (`change.after_model`) | takes the removed rules (X...) out of the formal model, with the links and outcome facts that came from them, and keeps them under `removed_rules` |
| 4 check | Z3 (`checks.py`) | as always, on the rules that are left. One more question for each removed rule: is the situation it was written for still covered? |
| 5 select | our code (`change.about_change`) | of 2 conflicts, 1 ambiguity and 1 gap, keeps the conflict of R3 with R5. The other three involve existing rules only; they are counted in the report and stay in `findings.json` |
| 6 word | the LLM | as always. The report ends with a table: each rule, its spec file, requirement and scenario, and whether the change added, modified or removed it |

**The state of a scenario.** Requirements are matched by name, and inside a
MODIFIED requirement the scenarios by theirs:

| State | When |
|---|---|
| existing | it was there, and its words are the same (also inside a requirement that the change rewrites) |
| modified | it was there, with other words |
| added | it is new |
| removed | its requirement is REMOVED, or the new text of its MODIFIED requirement has no scenario of that name |

**A finding is about the change when:**
- a conflict or a scenario has an added or modified rule;
- an ambiguity is about such a rule;
- a gap is for an event that such a rule reacts to (its trigger, or an event
  in its condition); or a removed rule covered its situation.

**The gap that a removal opens** (`checks.find_gaps`, `lost`). From
`experiments/examples/visitors_removed`:

```
stays     R1  "WHEN a visitor checks in at a ward AND the visitor is on the patient's visitor list THEN ..."
removed   X1  "WHEN a visitor checks in at a ward AND the visitor is not on the patient's visitor list THEN ..."
ask Z3    X1's own situation: visitor_checks_in and no other event, visitor_on_list FALSE.
          Does any remaining rule apply there?       no
gap       "Gap (opened by removing X1)", with the text of X1 under it
```

- the removed rules take no part in any other check: they cannot cause or
  hide a finding
- the situation is the removed rule's own, with all of its events. When the
  model reads "the payment is refused" as an event, the removed rule needs
  "buys credit" and "payment refused" together, and a search that lets one
  event happen at a time never reaches it (T23)
- a removed rule whose events no remaining rule reacts to gives no gap:
  nothing reacts to that event any more, by decision
- a removed rule that was rejected (its translations scattered) cannot be
  asked about

**Without formalizing everything again** (`--incremental`; `formalize` with
`base`). By default the merged spec is formalized again for every change, so
that all rules share one set of symbols, and a change costs one normal run.
With `--incremental`:

| Step | Who | What |
|---|---|---|
| 1 base | the LLM and Z3, once | the specs that exist are formalized as one labelled document (`change.base_document`). The model is kept in `openspec/.speccheck/base.json` with a fingerprint of the specs, and made again only when they change |
| 2 new part | our code (`change.merge(on_base=True)`) | writes the added and reworded scenarios of the change as a document of their own, `new.md`, labelled N1, N2, ... The scenarios that stay keep the labels of the base, the removed ones too; the old rule of a reworded scenario is "replaced" and dropped |
| 3 formalize the new part | the LLM and Z3 (`formalize(base=...)`) | the read step sees the symbols of the base before the document and is told to use them where they fit (`READ_MORE`). Translations, links and the questions of step 6 are asked for the new rules only; the question about two outcomes for the pairs with a new rule; the facts question again only if a symbol was added |
| 4 as before | Z3, our code, the LLM | removed rules set apart, the checks, the selection, the wording |

- a change that only removes asks the LLM nothing before the wording
- the second reader (5.8) and several symbol sets (5.6) are not used this way
- what it finds and what it costs, next to the full run: research.md 2.4

**Kept simple:**
- if a label does not come back as a rule id, the tool stops: it could not
  tell the change's rules from the others (`change.changed_rules`)
- the read step may take a requirement's SHALL sentence for a rule of its
  own, without a label. It counts as changed when it is the sentence of an
  added requirement or the new sentence of a modified one, and as removed
  when it is the sentence of a removed requirement
- a delta that names a requirement which is not there, or adds one that is,
  is refused, as `openspec archive` refuses it

---

## 6. The data between the pieces

### `formal.json`: the spec as logic

```json
{
  "symbols": [
    {"name": "inventory_available", "sort": "Bool", "values": [],
     "description": "The required inventory for the order is available."}
  ],
  "background": [
    {"id": "F2", "text": "Access cannot be both granted and denied.",
     "formula": "(not (and access_granted access_denied))", "support": "8/8"}
  ],
  "rules": [
    {"id": "R2",
     "text": "WHEN an order is submitted AND inventory is unavailable, THE Order System SHALL place the order on backorder.",
     "reading": "a submitted order with no stock must be backordered",
     "antecedent": "(and order_submitted (not inventory_available))",
     "consequent": "order_on_backorder",
     "status": "accepted", "clusters": [8], "entropy": 0.0}
  ]
}
```

| Field | Meaning |
|---|---|
| `symbols[].sort` | `Bool`, `Int`, `Real` or `Enum`; `values` lists the members of an Enum |
| `background` | the assumed facts; `support` = how many samples agree. A fact with `restates` is a link (step 5): it says what that rule demands in the other rules' terms; its `check` holds the answers of step 6. Editable by hand |
| `rules[].status` | `accepted` (samples agree), `ambiguous` (two readings; the rule also carries `alternative` and `differs_when`), `rejected` (no stable reading; left out of the checks) |
| `rules[].clusters` | how the samples split by meaning, e.g. `[5, 3]` |
| `symbols[].event` | true for something that happens at one moment (5.2) |
| `rules[].trigger` | the event the rule reacts to (5.2), or empty |
| `rules[].probes` | step 6: each other reading, the situations asked about, and the answers |
| `outcome_pairs` | step 6, check 4: each pair of rules asked about, and the count of its answers. A fact that came from one has `between`: the ids of the two rules |
| `rules[].second` | step 7, if it ran: the second model's reading, its support ("7/8"), and whether it means the same as the translation |

It is the only input of `checks.py`, so the solver stage can be re-run without a GPU.

### `findings.json`: one entry per finding

```json
[
  {"type": "conflict", "rules": ["R2", "R3"],
   "when": {"order_submitted": true, "inventory_available": false}},
  {"type": "conflict", "rules": ["R1", "R4"], "facts": ["F2"],
   "when": {"account_locked": true, "password_is_correct": true}},
  {"type": "gap",
   "when": {"order_submitted": false, "order_canceled": false}},
  {"type": "ambiguity", "rule": "R3", "status": "ambiguous", "split": [5, 3],
   "readings": ["... [in logic: (= failed_attempts 5) => account_locked]",
                "... [in logic: (>= failed_attempts 5) => account_locked]"],
   "differs_when": {"account_locked": false, "failed_attempts": 6}}
]
```

- A conflict with a `facts` list holds only if those assumed facts are true. A
  conflict without one is proven from the rules alone. It is doubtful when it
  has `simultaneous_events` (the events it needs at once) or `doubted_by` (the
  facts that say its situation cannot happen).
- An ambiguity has `found_by`: `samples` (5.1), `questions` (5.7) or `models` (5.8).
- A scenario looks like `{"type": "scenario", "verdict": "accepted", "rules": ["R1"], "when": {...}}`
  (`"rejected"` for a situation the rules rule out).
- With several symbol sets every finding also has `support` ("3/5": found with 3
  of 5 sets) and `model` (which formal model its witness is written in).
- A conflict or gap with `depends_on_reading` (rule id → that rule's other
  reading, in words) is gone with the other reading of those ambiguous rules. An ambiguity with two
  readings has `other_reading`: `{"removes": [[rule ids]], "adds": [[rule ids]],
  "covers_gaps": 1}`, what its other reading changes (5.9).
- A gap has `event` (the event that happens in it) or `quiet: true` (no event
  happens); a gap found by the search over all situations has neither (5.4).
  It is doubtful when it has `doubted_by`, as a conflict is.
- After stage 3 every finding also has `title`, `explanation`, `option_a`,
  `option_b`.
- With `--change`, every finding has `about_change` (5.10). Those with
  `false` come last and are not worded.

### `report.md`

```
# Requirements analysis: <name>
5 requirements analysed: 2 conflict(s) (1 doubtful), 1 gap(s), 0 ambiguity(ies), 1 scenario(s) to confirm.

 ## 1. Conflict (if the assumed facts hold, found with 3 of 3 symbol sets): <title>
    explanation
    A) Keep as-is: ...     B) Change: ...
    *Proven:* the exact fact: rule ids, the witness situation, the assumed facts it needs
```

The remarks in brackets appear only when they apply; a doubtful conflict says
"doubtful: needs two events at the same moment" or "doubtful: the assumed facts
say this situation cannot happen", and a doubtful gap says the latter. A conflict or gap that is gone with the
other reading of an ambiguous rule says "depends on the reading of R3".

With `--change`, the output goes into the change's folder, together with
`merged.md` (the specs with the change applied, every scenario labelled). The
report shows only the findings about the change. Under its first line it says
what the change adds, modifies and removes, and how many other findings were
left out; it ends with a table of the rules: label, spec file, requirement,
scenario, and "added" or "modified".

---

## 7. How far to trust a finding

| Finding | Trust it as |
|---|---|
| conflict, gap | a proof about `formal.json`. Wrong only if the translation is wrong |
| gap marked "no event happens" | a proof, but it may only mean that the system waits. Nearly every spec has one |
| conflict "if the assumed facts hold" | a proof that also needs the listed facts or links. Judge them |
| conflict marked "doubtful" | a proof, but likely an artefact of the model (two events at once, or a situation the facts rule out). On `eval3/`, all 60 marked conflicts were false alarms |
| gap marked "doubtful" | a proof, but the assumed facts say its situation cannot happen; usually two symbols for one yes/no question ("free", "taken"). Rare: most such false gaps are not marked |
| ambiguity | a real question: the model's own translations disagree, the words did not decide between two readings it was shown, or a second model reads it otherwise. Expect about half of the real ambiguities to be found; with the second reader most, with about one extra question per spec |
| scenario | a proven consequence of the rules. Which scenarios are shown is chosen by an LLM judge; whether one is a problem is for the author to decide |
| conflict or gap marked "depends on the reading of R3" | a proof that holds with the first reading of R3 only. R3 is ambiguous: answer its question first |
| "found with k of K symbol sets" | the higher k, the less the finding depends on how the text was modelled. In the evaluation, findings with most sets were never wrong |

---

## 8. Where the model runs

```
Windows:  python -m speccheck spec.md --base-url http://localhost:18200/v1
              │  ssh -L 18200:hpc-nodegpu01:18200 hpc-ctrl01
              ▼
SLURM:    experiments/slurm/serve.sbatch → vllm serve Qwen/Qwen3.8-27B-FP8   (2 GPUs)
```

- **One local model for the pipeline:** `Qwen/Qwen3.8-27B-FP8` on vLLM. Only the
  optional second reader (step 7) calls another local model,
  `thelamapi/next-70b`, which was already in the cluster's model cache. It
  needs both GPUs, so it runs in its own job (`experiments/slurm/serve_second.sbatch`,
  port 18201), after Qwen's, and the experiments add its answers to saved runs.
- **2 GPUs:** the account's limit, for all its jobs together: a second job
  waits with `QOSGrpGRES` (seen 2026-11-22). `--data-parallel-size 2` gives
  two replicas behind one address, so the Python code needs no load balancing.
  For E14 and T17 a second server with the same model and flags ran on two
  free GPUs of the lab workstation; `serve.sbatch` takes `PORT`, so that two
  servers can also share one node when the quota allows it.
- **Shared quota:** other jobs of the account use the same 2 GPUs. Start the
  server with a short limit (`sbatch --time=00:30:00 serve.sbatch`) and cancel it when done.
- **Key:** a random API key is written to `~/speccheck/api_key` at each start;
  the client reads it from `OPENAI_API_KEY`.
- **Thinking mode off:** Qwen can write out its reasoning before answering. The
  one call tried with it never reached an answer (research_log.md, T2).
- **Startup switches:** the node's CUDA compiler is too old for kernels vLLM
  compiles at startup; `serve.sbatch` switches those off and explains each one.
- **Threads:** only LLM calls run in threads. Z3 is not thread-safe, so all
  solver work happens in one thread per process.
- **Not repeatable at temperature 0:** the batched server gives slightly
  different answers to the same prompt (research_log.md, L10).

---

## 9. Compared with Kiro

| Kiro | Here |
|---|---|
| Formal model: schema, implications, background assertions | the same three parts: symbols, rules, assumed facts |
| Ambiguity from the entropy of sampled formalizations | the same |
| Conflicts as minimal rule sets | the same, for conflicts triggered by up to three rules |
| Background assertions kept by a frequency threshold | kept by majority vote, and only allowed to add findings; plus links (step 5) and facts from questions about pairs of outcomes (step 6) |
| Completeness gaps | the same idea, asked once for each event, plus one gap with no event |
| Surprising accepted / rejected scenarios, picked by an LLM judge | the same; at most 3 are shown |
| (not stated) | several symbol sets: each finding says with how many it was found |
| (not stated) | optional second reader: a model of another family must confirm each translation |
| Refinement: an LLM rewrites the criteria before formalization | not part of the pipeline. An optional review exists, off by default (below) |
| Reads one `requirements.md` | reads one document, or an OpenSpec change together with the specs that exist: only the findings that involve the change are reported (5.10) |
| (not stated) | one snapshot, no time: "then", "after", "until" are not modelled |

**The optional review**
- Kiro finds one of its two blog examples (the `delete_property`
  contradiction) with its LLM refinement stage, not with the solver
- a version of that stage: `speccheck/refine.py`, runs only with `--review`;
  nothing else needs it
- what we measured with it: research.md, section 5

---

## TODO

Legend: `[x]` done and verified, `[~]` in progress, `[ ]` not started.

- [x] **Step 1 — formal layer, no GPU**: `logic.py`, `checks.py`, hand-written tests
- [x] **Step 2 — model serving**: `experiments/slurm/serve.sbatch`, `llm.py`
- [x] **Step 3 — formalization**: `formalize.py` (read, sample, cluster)
- [x] **Step 4 — report**: `explain.py`, `cli.py`, README with real output
- [x] **Step 5 — batch experiments**: `experiments/stability.py`, third spec (OpenSpec format)
- [x] **Step 6 — assumed domain facts**: sampled, voted, add-only; `experiments/fact_threshold.py`
- [x] **Step 7 — LLM review of the text ("refinement")**: built and measured (E3),
      then switched off by default: the focus is the formal part
- [x] **Documentation pass**: README, plan and research log rewritten for reading
- [x] **Step 8 — evaluation set the prompts have not seen**: `eval/` (21 specs from
      `experiments/make_eval.py`), `experiments/evaluate.py`, experiment E4
- [x] **Step 9 — several symbol sets**: `--symbol-sets K`; every finding says
      "found with k of K"
- [x] **Step 10 — the rest of Kiro's formal part**: conflicts of three rules;
      scenarios with an LLM judge
- [x] **Step 11 — the charitable choice of symbols**: links (formalize step 5).
      `delete_property` 8 of 8; held-out recall 73% to 92% (E5)
- [ ] **Step 12 (recommended next; postponed by decision) — check a change against the specs that already exist**
  - [ ] a small OpenSpec project as test data: existing specs plus a change that
        clashes with them
  - [ ] read the project: `openspec/specs/<domain>/spec.md` and the ADDED /
        MODIFIED / REMOVED delta of the change
  - [ ] apply the delta, formalize the merged spec (existing requirements cached)
  - [ ] report only findings that involve a new or modified requirement
- [ ] **Step 13 — a larger evaluation**: more base specs, more runs, another main model
- [x] **Step 14 — better ambiguity detection**: questions about concrete situations
      (step 6, `probe.py`); held-out `eval2/` (E7)
- [x] **Step 15 — two repairs**: conflicts marked doubtful; links checked by a question
- [x] **Step 16 — two events at once, and ambiguity revisited**: events marked by the
      read step, conflicts needing two events marked doubtful; the reading question
      rebuilt (A / B / either); held-out `eval3/` (E8)
- [x] **Step 17 — events written as states**: a counted happening gets an event symbol
      and a count; the translation keeps the event (T8); held-out `eval4/` (E9)
- [x] **Step 18 — a second reader for ambiguity**: optional step 7, a second local
      model (`--second-base-url`); measured on `eval3/` (T9) and `eval4/` (E9)
- [x] **Step 19 — repair `delete_property`**: facts that make a requirement impossible
      to obey are checked against its words (check 3); links kept (T10)
- [x] **Step 20 — failures as events**: the read step names each rule's trigger; the
      two-event mark uses the triggers of the clashing rules (T11); held-out `eval5/` (E10)
- [x] **Step 21 — states read as events**: a prompt sentence was tried and dropped
      (T12); on `eval6/` states after WHEN were read as states in 12 of 12 runs (E11)
- [x] **Step 22 — "remove" against "keep"**: decided to leave it as a known limit (D6);
      measured again in E11
- [x] **Step 23 — "remove" against "keep", one prompt sentence**: tried and dropped (T14);
      measured again in E12 (10 of 18 runs found over E10 to E12)
- [x] **Step 24 — fewer flags from the second reader**: compared only where the required
      events happen (T13); held-out `eval7/` (E12)
- [x] **Step 25 — findings that depend on a reading**: each ambiguous rule is tried
      once more with its other reading (Z3 only); conflicts and gaps that are gone say
      so, each ambiguity lists what changes (5.9); measured on the saved runs (T15)
- [x] **Step 26 — gaps that say something, and size**: `eval8/` (with planted gaps) and a
      30-requirement spec written first; a gap is looked for once for each event; conflicts
      are searched only among rules that share symbols (D8); held-out `eval8/`: planted gaps
      0 → 18 of 18, conflicts 18 of 21, the long spec 6 of 6 (E13)
- [x] **Step 27 — long documents**: read answer limit 8192 → 24576 tokens; a
      100-requirement spec (`size2/`) written first; E14: 6 of 6 conflicts, the
      gap 3 of 3, read answer 16,799 tokens; the second reader does not fit yet
- [x] **Step 28 — the temperature of the samples**: `evaluate.py --temperature`;
      T17 on `eval8/` at 0.3, 0.5 and 0.7: no gain, 0.7 kept. T18: the read
      step's retry is never needed at temperature 0 (0 of 204)
- [x] **Step 29 — facts lost to a slip in the formula**: T19 counted the drops
      (5.4%, mostly missing outer parentheses); `eval9/` written first; the
      vote repairs the parentheses; held-out `eval9/` (E15): 18 of 18
      conflicts, the repair changes no finding there
- [x] **Step 30 — false gaps from two complementary symbols**: `eval10/`
      written first; the facts prompt names "one of two things is always the
      case"; a gap the facts rule out is marked doubtful (T20); held-out
      `eval10/` (E16): 18 of 18 conflicts, no other conflict, 18 of 18 planted
      gaps, but none of the 5 false gaps marked. Kept, and the false gaps
      recorded as a known limit
- [x] **Step 31 — check an OpenSpec change against the existing specs**:
      `eval11/` (30 changes on 6 projects) written first; `change.py` and
      `--change` (5.10); development run on old specs as projects and on
      `specs/auth_change` (T21); held-out `eval11/` (E17): 36 of 36 planted
      conflicts, 36 of 36 planted gaps, nothing else reported about a change
- [x] **Step 32 — conflicts said in other words**: the 21 misses of `eval3/`
      to `eval10/` sorted by cause (T22); `eval12/` written first; probe
      check 4 asks whether the outcomes of two rules can both hold; on the
      saved runs 132 → 145 of 153 conflicts, clean runs with an unplanted
      conflict 3 → 13 of 144; held-out `eval12/` (E18): 27 → 34 of 36, and
      0 → 3 of 18. Kept on by default
- [x] **Step 33 — what a change removes**: `eval13/` written first; removed
      scenarios stay in the merged document (labels X1, X2, ...) and apart in
      the formal model; Z3 is asked whether each one's situation is still
      covered; a scenario with the same words inside a rewritten requirement
      counts as existing (T23); held-out `eval13/` (E19): gaps opened by a
      removal 18 of 18, the old conflict shown as the change's 0 of 108
- [x] **Step 34 — a change without formalizing everything again**: `eval14/`
      written first; the specs formalized once and saved, a change's new
      scenarios formalized on top with the saved symbols (`--incremental`;
      T24); held-out `eval14/` both ways (E20): conflicts 54 of 54 against 50
      of 54, gaps 36 of 36 both, 68 requests for a change against 9. Kept as
      an option; the full run stays the default
- [x] **Documentation pass 2**: GUIDE.md reviewed point by point and rewritten (a new
      2.4 on gaps and scenarios; the ambiguity check, voted facts and links as steps on
      one real example), then shortened from 1112 to 893 lines; README.md reworded in the
      same places; plan.md 5.3, 5.4, 5.7, 5.8 and 7 in the same words

Section 2 says why, and in which order.
