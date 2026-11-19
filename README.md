# speccheck: a minimal Kiro-style requirements checker

- **In:** a requirements spec in plain language
- **Out:** its **conflicts**, **gaps**, **ambiguities** and **scenarios**, in plain
  language, each with "A) keep as-is / B) change"
- **How:** an LLM turns the spec into logic, the Z3 solver checks the logic
- It follows the formal part of [Kiro's requirements analysis](https://kiro.dev/blog/deep-spec-analysis/)

```
spec text ──formalize.py──► formal.json ──checks.py──► findings.json ──explain.py──► report.md
             LLM + Z3                     Z3 only                      LLM
```

## The project in one minute

**1. Translate** (LLM)
- each requirement → `when <condition> then <demand>`
- written with named facts, the *symbols*: `order_submitted`, `inventory_available`

**2. Prove** (Z3 solver, no LLM)
- Z3 answers one kind of question: "is there a situation in which all these
  formulas hold?" → yes, and one such situation; or no, proven. Our code asks
  it many such questions
- examples from the order spec below:
  - *conflict*: the rules cannot all be obeyed → R2 "backorder it" vs R3 "never backorder"
  - *gap*: no rule applies → nothing says what to do when no order is submitted
  - *scenario*: allowed (or ruled out), but nobody wrote it → an order is fulfilled that was never submitted

**3. Check that each rule has only one meaning**

Example: "WHEN failed attempts reach 5, lock the account". Two possible
meanings (*readings*), each a formula for Z3:
- A: lock at exactly 5 failed attempts: `(=> (= failed_attempts 5) account_locked)`
- B: lock at 5 or more: `(=> (>= failed_attempts 5) account_locked)`

They differ at 6 attempts: A lets the account stay unlocked, B does not.

1. **Find the readings.** The LLM translates the rule into logic 8 times; the
   solver checks which translations mean the same:

   ```
   T1 and T2 mean the same  ⇔  (xor T1 T2) is unsatisfiable
                                (no situation in which one holds and the other does not)
   ```

   - they split, e.g. 5 mean A and 3 mean B → A and B
   - all (or 7 of 8) mean A → the LLM is asked "what else could these words
     mean?" and writes each answer as a formula → B. An answer that means the
     same as A (same test) is dropped
2. **Ask about the case where they differ.** Z3 finds the situation:

   ```
   (and A (not B))    satisfiable, e.g. failed_attempts = 6, account_locked = false
   (and (not A) B)    the other way round, if there is one (here: unsatisfiable)
   ```

   The LLM is asked 8 times: "6 failed attempts, account not locked. Do the
   words say A, B, or either?"
   - A gets more than half of the answers → the rule means A
   - otherwise → *ambiguous*
3. **Optional: a second LLM** translates the rule 8 times, S1 to S8. Each is
   compared with A by the same test, `(xor A Si)` unsatisfiable. At most half
   mean A → *ambiguous*.

Step 2 is asked even when the 8 translations agree: 8 answers of one model
often repeat the same choice.

An ambiguous rule becomes a question for the author: "exactly 5, or 5 or
more: which did you mean?"

**4. Tell the solver what the words mean** (*assumed facts*)

Example, `specs/auth_openspec`:
- R1: "WHEN a user submits a correct password THEN the system grants access"
- R4: "WHEN a user submits a password for a locked account THEN the system denies access"

A person sees the clash: a correct password for a locked account. Z3 does not,
because it sees only the formulas:

```
R1   (=> (and password_submitted password_correct) access_granted)
R4   (=> (and password_submitted account_locked) access_denied)
```

For Z3, `access_granted` and `access_denied` are two unrelated yes/no values:
both can be true, so both rules can be obeyed.

1. **The LLM writes what the words mean.** It is asked 8 times which facts
   hold just because of what the symbols mean. Each fact is a sentence plus
   a formula:

   ```
   F2   "The system cannot grant access and deny access simultaneously."
        (not (and access_granted access_denied))
   ```

   F2 is kept: Z3 proves it follows from 7 of the 8 answers (more than half
   are needed).
2. **Search for conflicts twice**, in the situation where R1 and R4 both apply:

   ```
   situation   (and password_submitted password_correct account_locked)
   search 1    situation + all rules           satisfiable   → no conflict
   search 2    situation + all rules + facts   unsatisfiable → conflict {R1, R4}, needs F2
   ```

   Search 2 can only add conflicts: a wrong fact cannot hide a conflict proven
   from the rules alone.
3. **Show the fact to the author.** The conflict is marked "if the assumed
   facts hold", and the report quotes the fact:

   > This depends on assumptions that are not stated in the requirements:
   > - F2: The system cannot grant access and deny access simultaneously.

A second kind of assumed fact, the *link*, is explained [below](#assumed-facts-and-links).

**5. Say how sure each finding is**

The title of each finding says it (real titles):

| Title says | Meaning | Example |
|---|---|---|
| nothing | proven from the rules alone | "Conflict: Backorder Requirement Conflict" (R2 vs R3, order spec) |
| "if the assumed facts hold" | proven only with an assumed fact (point 4) | "Conflict (if the assumed facts hold): Conflict between correct password and locked account" |
| "doubtful: ..." | proven, but probably an artefact of the formulas | the two cases below |
| "found with k of K symbol sets" | optional: the spec was translated K times, each time with other symbols; k of them found it | "Conflict (found with 3 of 3 symbol sets): Conflict between removal and retention" |

*Doubtful* has two cases. The conflict stays in the report, marked.

1. **Two events at the same moment.** A situation is one snapshot, so Z3 may
   let two events happen at once. Requirements are written for one event at
   a time. Example, a newsletter spec:

   ```
   rule 1      "WHEN a visitor submits the signup form THEN the system sends no email ..."
               trigger: visitor_signed_up
   rule 2      "WHEN a subscriber changes the email address THEN the system sends a confirmation email"
               trigger: address_changed
   situation   visitor_signed_up = true, address_changed = true
               → rule 1: no email, rule 2: an email → conflict
   mark        the two rules react to two different events → doubtful
   ```

   The *trigger*, the event a rule reacts to, is named by the LLM when it
   reads the spec.
2. **A situation the facts call impossible.** Example, a booking spec:
   "cancels at least 24 hours before" → no fee; "less than 24 hours before"
   → a late fee. Written as two yes/no symbols, both can be true for Z3:

   ```
   situation   at_least_24h = true, less_than_24h = true    → no fee and a late fee → conflict
   fact        (not (and at_least_24h less_than_24h))        → this situation cannot happen
   mark        doubtful: "the assumed facts say this situation cannot happen"
   ```

**Where it stands**
- finds what the Kiro blog finds, on both of the blog's examples
- on 7 sets of specs it was not built on: 61 to 100% of planted conflicts found,
  at most 1 false alarm in 18 clean runs (doubtful conflicts set aside)
- ambiguities: about half found; with the second model 30 to 32 of 36, at the
  price of up to one extra question per spec

| Read next | For |
|---|---|
| this file | a worked example with real output, the results, how to run it |
| [plan.md](plan.md) | where we are, what is next, and how each part works |
| [research.md](research.md) | what we found, with the numbers |
| [research_log.md](research_log.md) | the archive: every experiment in detail. Not needed to understand the project |

Everything quoted below is real output, produced with Qwen3.8-27B-FP8 on vLLM.

## A) The request: a spec

`specs/order/requirements.md` is the order-processing example from the Kiro blog:

```
R1: WHEN an order is submitted AND inventory is available, THE Order System SHALL fulfill the order.
R2: WHEN an order is submitted AND inventory is unavailable, THE Order System SHALL place the order on backorder.
R3: THE Order System SHALL NOT place any order on backorder.
R4: WHEN an order is canceled, THE Order System SHALL refund all associated payments.
R5: WHILE an order is in a canceled-and-refunded state, THE Order System SHALL NOT fulfill the order.
```

## B) The formal check, and the answer in plain language

### Stage 1: the LLM writes the spec as logic (`formal.json`)

**Symbols**: one variable for each fact the requirements talk about

```json
{"name": "inventory_available", "sort": "Bool", "event": false,
 "description": "The inventory for the ordered items is available."}
```

- `event: true`: something that happens at one moment (an order is submitted)
- `event: false`: a state, like this one

**Rules**: each requirement, translated 8 times, independently, into
- `antecedent`: when it applies
- `consequent`: what must hold then

```json
{"id": "R2",
 "antecedent": "(and order_submitted (not inventory_available))",
 "consequent": "order_on_backorder",
 "status": "accepted", "clusters": [8], "entropy": 0.0}
{"id": "R3",
 "antecedent": "true",
 "consequent": "(not order_on_backorder)",
 "status": "accepted", "clusters": [8], "entropy": 0.0}
```

- our code puts the 8 in groups that mean the same: two go together when Z3
  proves that no situation tells them apart
- `"clusters": [8]`: all 8 mean the same; a split such as `[5, 3]`: two readings
- either way, the steps of point 3 at the top decide whether the rule is
  *ambiguous*

**Assumed facts**: true because of what the words mean, but not written in the spec
- the LLM proposes them, 8 samples vote
- used only to find *more* conflicts ([details below](#assumed-facts-and-links))

### Stage 2: Z3 checks the logic (`findings.json`)

No LLM here: our code asks Z3 for three kinds of situation. In the order spec:

```
conflict   situation:  an order is submitted, no stock
           R2 says:    backorder it
           R3 says:    never backorder          → no way to obey both

gap        situation:  no order submitted, none canceled
           the spec:   no rule applies          → what must the system do?

scenario   situation:  an order is fulfilled, but it was never submitted
           the spec:   no rule forbids it       → allowed. Was that meant?
                       (R1 says when to fulfill, not "only then")
```

Gap or scenario?
- **gap**: the spec says *nothing* about the situation
- **scenario**: the spec *does* decide (allowed, or impossible), maybe not as the author meant

What `checks.py` writes (`when` is the situation Z3 found):

```json
{"type": "conflict", "rules": ["R2", "R3"],
 "when": {"inventory_available": false, "order_submitted": true}}
{"type": "conflict", "rules": ["R1", "R5"],
 "when": {"inventory_available": true, "order_canceled_and_refunded": true, "order_submitted": true}}
{"type": "gap",
 "when": {"order_canceled": false, "order_canceled_and_refunded": false, "order_submitted": false}}
{"type": "scenario", "verdict": "accepted", "rules": ["R1"],
 "when": {"inventory_available": false, "order_fulfilled": true, "order_submitted": false}}
```

- conflicts: for every 1, 2 or 3 rules whose conditions can hold together, Z3
  is asked whether they can hold while all rules are obeyed. If not, Z3 names
  the rules it needed;
  our code cuts them down to the smallest set that still clashes
- the first three are the findings the Kiro blog reports for this spec

### Stage 3: the LLM says it in plain language (`report.md`)

The LLM only rewords each proven finding. The conflict:

> **1. Conflict: Backorder Requirement Conflict**
>
> The requirements contain a direct contradiction regarding how to handle orders
> when stock is low. In the situation where an order is submitted but inventory
> is unavailable, R2 requires the system to place the order on backorder, while
> R3 explicitly forbids the system from placing any order on backorder.
>
> - **A) Keep as-is:** Keeping the requirements as written means the system is
>   logically unable to process any order where inventory is unavailable, as it
>   is forced to perform an action that is simultaneously prohibited.
> - **B) Change:** Remove R3 or modify it to allow backorders for specific
>   conditions, ensuring that R2's instruction to backorder unavailable items is
>   not contradicted by a general prohibition.
>
> *Proven:* Requirements R2, R3 cannot all be obeyed in this situation:
> - FALSE: inventory_available (The inventory for the ordered items is available.)
> - TRUE: order_submitted (An order has been submitted by a customer.)

The gap:

> **3. Gap: Undefined behavior for non-existent orders**
>
> The requirements do not specify what the system must do when an order has not
> been submitted, has not been canceled, and is not in a canceled-and-refunded
> state. [...]
>
> - **A) Keep as-is:** Keeping the requirements as written means the system has
>   no defined behavior for situations where no order has been submitted or
>   canceled.
> - **B) Change:** Add a requirement stating that the system shall do nothing or
>   remain idle when no order has been submitted or canceled.

The scenario. The solver proved it; an LLM judge decided it is worth showing:

> **4. Scenario, allowed: Fulfillment without submission**
>
> The requirements allow the system to fulfill an order even when no order has
> been submitted and inventory is unavailable. This defeats the purpose of R1,
> which ties fulfillment to a submitted order and available inventory [...]
>
> - **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
> - **B) Change:** Add a requirement stating that the Order System SHALL NOT
>   fulfill any order unless an order has been submitted and inventory is
>   available.

Full report: [specs/order/report.md](specs/order/report.md).

## Assumed facts and links

The problem: the solver sees symbols, not words.
- two requirements say opposite things in different words → two unrelated
  symbols → no conflict
- example, the Kiro blog's other spec, `specs/delete_property/requirements.md`:

```
D2: WHEN a Property Owner confirms deletion, THE Platform SHALL remove the Property record from the Platform
D4: THE Platform SHALL implement soft deletion to retain Property records in the database for audit purposes while hiding them from the user interface
```

- the LLM writes D2 with a symbol of its own, `property_record_removed`
- nothing else uses it → D2 cannot clash with D4

Two fixes bring the meaning back:
- **Voted facts**: the LLM is asked 8 times which facts connect the symbols
  ("access cannot be both granted and denied"); a fact is kept when Z3 proves
  it follows from more than half of the answers
- **Links**: a rule with a symbol nobody else uses is translated 8 more times,
  using only the outcomes of the *other* rules. For D2, 8 of 8 answers say the
  same thing:

```json
{"id": "F1", "restates": "D2", "support": "8/8",
 "text": "What D2 demands, in the terms of the other requirements: When a property owner confirms the deletion of a property, the platform must remove the property record from the database.",
 "formula": "(=> (and deletion_confirmed property_record_removed) (not property_record_retained_in_db))"}
```

→ with this link, Z3 proves the conflict between D2 and D4.

Facts and links are the LLM's guesses, so:
- they only **add** findings: conflicts are searched with the rules alone
  first, then with the facts; a fact never removes or changes a finding
- every conflict that needs one says so ("if the assumed facts hold") and quotes it
- a wrong one: delete it from `formal.json` and re-run with `--formal`

## Several symbol sets

- every finding depends on the symbols the LLM picks, and it does not always
  pick the same ones
- `--symbol-sets 3` formalizes the spec 3 times; each finding says with how many
  of the 3 it was found
- for `delete_property`:

> **3. Conflict (found with 3 of 3 symbol sets): Conflict between removal and retention**
>
> Requirement D2 states that the Platform must remove the Property record from
> the Platform once deletion is confirmed. However, Requirement D4 mandates that
> the Platform must retain Property records in the database for audit purposes.
> These two requirements cannot be satisfied simultaneously because a record
> cannot be both removed and retained in the same state.
>
> - **A) Keep as-is:** Keeping the requirements as written means the system is
>   logically impossible to build because it must both delete and keep the same
>   data.
> - **B) Change:** Change Requirement D2 to state that the Platform shall mark
>   the Property as deleted rather than removing the record, aligning it with
>   the soft deletion strategy in D4.

- one of the 3 symbol sets also split on D2 itself (4 against 4) → the
  question the Kiro blog shows for this spec:

> **2. Ambiguity (found with 1 of 3 symbol sets): Ambiguity in Deletion Definition**
>
> Requirement D2 is unclear about what "remove the Property record" means. One
> reading requires that the record be physically erased from the database, while
> the other only requires that the property be considered deleted (which, per D4,
> allows the record to remain in the database). Which did you mean?

Saved run: [experiments/examples/delete_property_links](experiments/examples/delete_property_links).

## Run it

```
uv sync          # on a "hardlink" error: set UV_LINK_MODE=copy and retry
```

Then, inside the project's `.venv`:

**Without a GPU**: the solver only, on a saved `formal.json` (no wording, no scenarios)

```
python -m speccheck specs/order/requirements.md --formal specs/order/formal.json --out out
python -m pytest tests
```

**With the LLM** (any OpenAI-compatible server)

```
# on the cluster, in ~/speccheck:   sbatch --time=00:30:00 serve.sbatch     (ready in about 3 minutes)
ssh -N -L 18200:hpc-nodegpu01:18200 <user>@hpc-ctrl01.acc-ub.local
export OPENAI_API_KEY=<content of ~/speccheck/api_key on the cluster>
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1 --symbol-sets 3
```

**With the second model** (optional, finds more ambiguities)
- it needs the same 2 GPUs → its own job, after the first (plan.md, section 8)
- with more GPUs: both servers at once, and `--second-base-url http://localhost:18201/v1`
  on the command above

```
# on the cluster:   sbatch --time=00:40:00 serve_second.sbatch
ssh -N -L 18201:hpc-nodegpu01:18201 <user>@hpc-ctrl01.acc-ub.local
python -m experiments.evaluate --rescore experiments/results/<run>.json --second-base-url http://localhost:18201/v1
```

**Output**, next to the spec (or in `--out`):

| File | Content |
|---|---|
| `formal.json` | the spec as logic: symbols, assumed facts, rules (`formal_2.json` ... with `--symbol-sets`) |
| `findings.json` | what the solver proved, with its wording |
| `report.md` | the same, in plain language (also printed) |

- time: under a minute for a 5-rule spec, about a minute with 3 symbol sets
- when done: cancel the server job, it holds the account's two GPUs

## It works on any spec

Nothing in the code or the prompts is about orders.

| Specs | Format | Used for |
|---|---|---|
| `specs/order`, `specs/delete_property` | Kiro EARS | the two examples of the Kiro blog |
| `specs/auth_openspec` | OpenSpec (`### Requirement` / `#### Scenario`) | another format; two conflicts we planted |
| `experiments/sets/`: `eval` to `eval7` (171 specs) | both | 42 specs in new domains, each clean and with planted defects. Each set was written before it was used, as a test the prompts had not seen |

## How reliable is it

Each line is a test on specs the prompts had not seen (3 runs per spec):

| Test | Planted conflicts found | Clean runs with a false alarm | Planted ambiguities found |
|---|---|---|---|
| `eval/` (E5) | 44 of 48 | 0 of 18 | 2 of 9 |
| `eval2/` (E7) | 31 of 36 | 0 of 18 | 17 of 36 |
| `eval3/` (E8), doubtful conflicts set aside | 15 of 21 | 1 of 18 | 14 of 36 |
| `eval4/` (E9), doubtful conflicts set aside | 21 of 21 | 0 of 18 | 14 of 36; 30 of 36 with the second model |
| `eval5/` (E10), doubtful conflicts set aside | 11 of 18 | 0 of 18 | 15 of 36 |
| `eval6/` (E11), doubtful conflicts set aside | 15 of 18 | 0 of 18 | 19 of 36 |
| `eval7/` (E12), doubtful conflicts set aside | 13 of 18 | 0 of 18 | 17 of 36; 32 of 36 with the second model |

- assumed facts and links carry a large part of the result: without them,
  `eval3/` gives 10 of 21
- doubtful conflicts: on `eval3/` and `eval4/` all were false alarms; on
  `eval5/` one planted conflict was marked too ("WHEN a member is suspended"
  read as an event), so counting doubtful conflicts E10 finds 14 of 18
- the second model: about twice the ambiguities found, and about twice the
  flags on clean specs (7 → 15 on `eval4/`, 5 → 9 on `eval7/`, in 18 runs)
- `delete_property`, the blog's second example: 3 of 3 in the last runs;
  missed in 4 of 7 earlier runs, 3 times because of a wrong voted fact
  (research.md 4.3)
- the numbers are small: specs written by us, one main model.
  Details: [research.md](research.md)

## Known limits

| Limit | What it means |
|---|---|
| A finding is a proof about `formal.json`, not about your intent | the LLM mistranslates → the solver proves the wrong thing |
| One model finds about half of the ambiguities | it is confident about readings a person would ask about. A second model finds most, and flags about one more clear rule per spec |
| An assumed fact or link can be wrong, even with a majority | the report quotes every one a conflict depends on, so you can judge |
| Some proven conflicts are artefacts of the model | two events at the same moment ("a visitor signs up" while "a subscriber changes the address"); "at least 24 hours" and "less than 24 hours" as two symbols, both true. These are marked *doubtful* |
| The *doubtful* mark needs the LLM to name the event each rule reacts to | a state taken for an event ("WHEN a member is suspended") marks a real conflict too |
| "Remove" against "keep" is missed in about half of the cases | "delete the listing" vs "keep every listing for seven years" become unrelated symbols, or a number, and nothing connects them. The main cause of missed conflicts |
| Gaps depend on the symbols | almost every spec gets the gap "nothing is happening", like the order spec |
| One snapshot, no time | "then", "after" and "until" are not modelled |
| One document | checking a change against specs that already exist is the next step (plan.md) |

## Optional: an LLM review of the text (off by default)

- this project is the formal check only
- Kiro also has an LLM stage that reads the text itself ("refinement")
- a version of it: `speccheck/refine.py`, runs only with `--review`
- what it found: research.md, section 5

## Files

| File | What it does |
|---|---|
| `speccheck/llm.py` | the one place that calls the model (answers forced into a JSON schema) |
| `speccheck/logic.py` | symbols to Z3 variables, formula parsing, solver questions |
| `speccheck/formalize.py` | stage 1: read, sample, cluster, facts, links; several symbol sets |
| `speccheck/probe.py` | stage 1, step 6: questions about concrete situations |
| `speccheck/checks.py` | stage 2: conflicts, gaps, scenarios; merging several symbol sets |
| `speccheck/explain.py` | stage 3: wording, the scenario judge, the Markdown report |
| `speccheck/cli.py` | runs the three stages |
| `speccheck/refine.py` | optional LLM review, off by default |
| `experiments/slurm/serve.sbatch`, `experiments/slurm/serve_second.sbatch` | start the vLLM servers on the cluster: the main model, the second model |
| `tests/` | 36 tests of everything that needs no LLM |
| `experiments/sets/`, `experiments/make_eval.py` | the evaluation sets `eval` to `eval7`, and the script that writes them |
| `experiments/results/` | every experiment: the raw data (`.json`) and its tables (`.md`) |
| `experiments/evaluate.py` | runs and scores the evaluation; re-scores saved runs without a GPU |
| `experiments/stability.py`, `fact_threshold.py` | the earlier experiments |
| `experiments/examples/` | saved runs referred to above and in research_log.md |
