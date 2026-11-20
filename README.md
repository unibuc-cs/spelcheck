# speccheck: a minimal Kiro-style requirements checker

**New here? Read [GUIDE.md](GUIDE.md) first.** It explains the same ideas one
at a time, each from an example, with diagrams.

speccheck reads a requirements document written in plain language and reports
what is wrong with it: requirements that contradict each other (*conflicts*),
situations that no requirement covers (*gaps*), sentences that can be read in
two ways (*ambiguities*), and consequences the author may not have intended
(*scenarios*). Every finding is given in plain language, with two choices:
"A) keep as-is" or "B) change".

It follows the formal part of
[Kiro's requirements analysis](https://kiro.dev/blog/deep-spec-analysis/). A
language model turns the spec into logic, the Z3 solver checks the logic, and
the model puts the results back into words:

```
spec text ──formalize.py──► formal.json ──checks.py──► findings.json ──explain.py──► report.md
             LLM + Z3                     Z3 only                      LLM
```

## The project in one minute

The model rewrites each requirement as "when *condition* then *demand*", using
named facts such as `order_submitted` and `inventory_available`. These names
are the *symbols*.

Z3 then does the proving, and no language model is involved in that. Z3 can
answer one kind of question: "is there a situation in which all these formulas
hold?" Either it shows such a situation, or it proves that none exists. Our
code asks that question many times, looking for three kinds of situation. In
the order spec used below:

| Finding | What it means | Example |
|---|---|---|
| conflict | the rules cannot all be obeyed | R2 "backorder it" against R3 "never backorder" |
| gap | no rule applies | nothing says what to do when no order is submitted |
| scenario | allowed (or ruled out), though nobody wrote it down | an order is fulfilled that was never submitted |

A proof is only as good as the translation it starts from, so most of the
project deals with what can go wrong there:

| What goes wrong | What speccheck does about it | More |
|---|---|---|
| a sentence has two meanings, and the model picks one | it looks for a second reading and, if the words do not decide between them, reports an *ambiguity*: a question to the author | [Ambiguities](#ambiguities) |
| two rules say opposite things in different words | it lets the model propose *assumed facts* ("access cannot be both granted and denied"), keeps those that a majority of answers agree on, and uses them only to find more conflicts | [Assumed facts and links](#assumed-facts-and-links) |
| the logic has no time, so some proven conflicts are not real | it marks them *doubtful* instead of hiding them | [How sure is a finding](#how-sure-is-a-finding) |
| the findings depend on the symbols the model chose | it can formalize the spec several times and say how often each finding came up | [Several symbol sets](#several-symbol-sets) |

Where the project stands:

- it finds what the Kiro blog finds, on both of the blog's examples;
- on 8 sets of specs it was not built on, it found 61 to 100% of the conflicts
  we had planted, with at most 1 false alarm in 18 clean runs (doubtful
  conflicts set aside);
- it finds about half of the planted ambiguities, and 30 to 32 of 36 with a
  second model, at the price of up to one extra question per spec.

| Read next | For |
|---|---|
| [GUIDE.md](GUIDE.md) | a guided tour for a first reading: every idea from an example, in small steps |
| this file | a worked example with real output, the results, how to run it |
| [plan.md](plan.md) | where we are, what is next, and the exact rule behind each decision |
| [research.md](research.md) | what we found, with the numbers |
| [research_log.md](research_log.md) | the archive: every experiment in detail. Not needed to understand the project |

Everything quoted below is real output, produced with Qwen3.8-27B-FP8 on vLLM.

## A worked example

### The spec

`specs/order/requirements.md` is the order-processing example from the Kiro blog:

```
R1: WHEN an order is submitted AND inventory is available, THE Order System SHALL fulfill the order.
R2: WHEN an order is submitted AND inventory is unavailable, THE Order System SHALL place the order on backorder.
R3: THE Order System SHALL NOT place any order on backorder.
R4: WHEN an order is canceled, THE Order System SHALL refund all associated payments.
R5: WHILE an order is in a canceled-and-refunded state, THE Order System SHALL NOT fulfill the order.
```

### Stage 1: the LLM writes the spec as logic (`formal.json`)

First come the symbols, one variable for each fact the requirements talk about:

```json
{"name": "inventory_available", "sort": "Bool", "event": false,
 "description": "The inventory for the ordered items is available."}
```

`event` says whether the symbol is something that happens at one moment (an
order is submitted) or a state, like this one.

Then come the rules. Each requirement is translated 8 times, independently,
into an `antecedent` (when it applies) and a `consequent` (what must hold then):

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

Our code puts the 8 translations into groups that mean the same. Two go into
the same group when Z3 proves that no situation tells them apart.
`"clusters": [8]` says that all 8 mean the same; a split such as `[5, 3]`
would show two readings (see [Ambiguities](#ambiguities)).

The file also holds the assumed facts, which have
[a section of their own](#assumed-facts-and-links).

### Stage 2: Z3 checks the logic (`findings.json`)

There is no LLM in this stage. Our code asks Z3 for three kinds of situation.
In the order spec:

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

A gap is looked for once for each event the rules react to ("an order is
submitted and no rule applies"); here every event is covered, so the only gap
is the one in which no event happens, and the report marks it as such.

A gap and a scenario are not the same thing. In a gap, the spec says nothing
about the situation. In a scenario, the spec does decide (the situation is
allowed, or it is impossible), perhaps not as the author meant.

This is what `checks.py` writes. The field `when` is the situation Z3 found:

```json
{"type": "conflict", "rules": ["R2", "R3"],
 "when": {"inventory_available": false, "order_submitted": true}}
{"type": "conflict", "rules": ["R1", "R5"],
 "when": {"inventory_available": true, "order_canceled_and_refunded": true, "order_submitted": true}}
{"type": "gap", "quiet": true,
 "when": {"order_canceled": false, "order_canceled_and_refunded": false, "order_submitted": false}}
{"type": "scenario", "verdict": "accepted", "rules": ["R1"],
 "when": {"inventory_available": false, "order_fulfilled": true, "order_submitted": false}}
```

To find conflicts, the check takes every rule, every pair and every group of
three rules whose conditions can hold together, and asks Z3 whether all rules
can be obeyed while those conditions hold. If they cannot, Z3 names the rules
it needed for the contradiction, and our code cuts that list down to the
smallest set that still clashes. The first three findings above are the ones
the Kiro blog reports for this spec.

### Stage 3: the LLM says it in plain language (`report.md`)

The model only rewords each proven finding. This is the conflict:

> **1. Conflict: Backorder Requirement Conflict**
>
> The requirements contain a direct contradiction regarding how to handle
> orders when stock is low. In the situation where an order is submitted but
> inventory is unavailable, R2 requires the system to place the order on
> backorder, while R3 explicitly forbids the system from placing any order on
> backorder.
>
> - **A) Keep as-is:** Keeping the requirements as written means the system is
>   logically trapped and cannot legally process any order where inventory is
>   unavailable, as it must simultaneously do and not do the same action.
> - **B) Change:** Remove R3 entirely, or modify R3 to state that the system
>   shall not place orders on backorder only under specific conditions that do
>   not overlap with the scenario in R2.
>
> *Proven:* Requirements R2, R3 cannot all be obeyed in this situation:
> - FALSE: inventory_available (The inventory for the ordered items is available.)
> - TRUE: order_submitted (An order has been submitted by a customer.)

The gap. No event happens in it, and the title says so:

> **3. Gap (no event happens): Undefined System Behavior**
>
> The requirements do not specify what the Order System must do when no order
> has been submitted, canceled, or refunded. This gap appears in the situation
> where none of these events have occurred, leaving the system's behavior
> undefined.
>
> - **A) Keep as-is:** Keeping the requirements as written means the system has
>   no defined action to take when no orders are submitted, canceled, or
>   refunded.
> - **B) Change:** Add a requirement stating that the Order System SHALL remain
>   in an idle state when no orders are submitted, canceled, or refunded.

And the scenario. The solver proved it, and an LLM judge decided that it is
worth showing:

> **4. Scenario, allowed: Fulfillment without submission**
>
> The requirements allow the system to fulfill an order even when no order has
> been submitted and inventory is unavailable. This defeats the purpose of R1,
> which ties fulfillment to a submitted order and available inventory, and
> contradicts the user story's expectation that processing follows submission.
>
> - **A) Keep as-is:** Keep the requirements, allowing the system to fulfill
>   orders without a prior submission or available inventory.
> - **B) Change:** Add a requirement stating that the Order System SHALL NOT
>   fulfill any order unless an order has been submitted and inventory is
>   available.

The full report is in [specs/order/report.md](specs/order/report.md).

## Ambiguities

Take the rule "WHEN failed attempts reach 5, lock the account". It has two
possible meanings, or *readings*, and each is a formula for Z3:

```
A   lock at exactly 5 failed attempts    (=> (= failed_attempts 5) account_locked)
B   lock at 5 or more                    (=> (>= failed_attempts 5) account_locked)
```

They differ at 6 attempts: A lets the account stay unlocked, B does not.
speccheck has three ways to notice that a rule has two readings.

1. **The translations split.** The LLM translates the rule 8 times, and our
   code checks with Z3 which translations mean the same: T1 and T2 mean the
   same when `(xor T1 T2)` is unsatisfiable, that is, when no situation makes
   one hold and the other not. If 5 mean A and 3 mean B, we have both readings.
2. **The words do not decide.** If all 8 (or 7 of 8) mean A, the LLM is asked
   what else the words could mean, and writes each answer as a formula; that
   gives B. Z3 then finds the situation where the two differ, here
   `failed_attempts = 6, account_locked = false`, and the LLM is asked 8
   times: "6 failed attempts, account not locked. Do the words say A, B, or
   either?" If A gets more than half of the answers, the rule means A.
   Otherwise it is ambiguous. This question is asked even when the 8
   translations agree, because 8 answers of one model often repeat the same choice.
3. **A second model reads it otherwise** (optional). A second LLM translates
   the rule 8 times, and each translation is compared with A by the same test.
   If at most half mean A, the rule is ambiguous.

An ambiguous rule becomes a question for the author: "exactly 5, or 5 or more:
which did you mean?" The guide goes through this with a diagram
([GUIDE.md, section 3.1](GUIDE.md#31-does-a-rule-have-only-one-meaning)).

Until the author answers, the checks use reading A, and some findings may
exist only because of that choice. So each ambiguous rule is tried once more
with its other reading, by the solver alone. A conflict or a gap that is gone
with the other reading says so in its title, and the ambiguity lists what its
other reading changes. In the login spec, the gap "6 failed attempts, no
password submitted" exists only if R3 means "exactly 5":

> *Proven:* No requirement says what the system must do in this situation: [...]
> But R3 is ambiguous (see its finding). With its other reading a requirement
> applies in this situation. That reading: If the number of consecutive failed
> login attempts for an account is at least 5, the system must place the
> account in a locked state.

## Assumed facts and links

The solver sees symbols, not words. Here are two rules of `specs/auth_openspec`:

```
R1   "WHEN a user submits a correct password THEN the system grants access"
     (=> (and password_submitted password_correct) access_granted)

R4   "WHEN a user submits a password for a locked account THEN the system denies access"
     (=> (and password_submitted account_locked) access_denied)
```

A person sees the clash at once: a correct password for a locked account. Z3
does not, because for Z3 `access_granted` and `access_denied` are two
unrelated yes/no values. Both can be true, so both rules can be obeyed. Two
repairs bring the meaning back.

**Voted facts.** The LLM is shown only the symbols with their meaning
(`access_granted`: "The system grants access to the user"), not the
requirements, and it lists facts that hold "purely because of what the symbols
mean". It does this 8 times. Each fact is a sentence and a formula:

```
F2   "The system cannot grant access and deny access simultaneously."
     (not (and access_granted access_denied))
```

The 8 answers word the same fact differently, for example
`(=> access_granted (not access_denied))`. So an answer counts as agreeing
with a fact when Z3 proves that the fact follows from that answer's facts:

```
(and <facts of answer k> (not F2))    unsatisfiable  →  answer k agrees
```

F2 has 7 of the 8 answers behind it. More than half are needed, so it is kept.

**Links.** Sometimes a rule uses a symbol that no other rule uses, and then
nothing can clash with it. This happens in the Kiro blog's other spec,
`specs/delete_property/requirements.md`:

```
D2: WHEN a Property Owner confirms deletion, THE Platform SHALL remove the Property record from the Platform
D4: THE Platform SHALL implement soft deletion to retain Property records in the database for audit purposes while hiding them from the user interface
```

The LLM writes D2 with a symbol of its own, `property_record_removed`. Such a
rule is translated 8 more times, using only the outcomes of the *other* rules.
For D2, 8 of 8 answers say the same thing:

```json
{"id": "F1", "restates": "D2", "support": "8/8",
 "text": "What D2 demands, in the terms of the other requirements: When a property owner confirms the deletion of a property, the platform must remove the property record from the database.",
 "formula": "(=> (and deletion_confirmed property_record_removed) (not property_record_retained_in_db))"}
```

With this link, Z3 proves the conflict between D2 and D4.

Facts and links are the LLM's guesses, so they are handled with care:

- **They only add findings.** Conflicts are searched twice: with the rules
  alone, and then with the facts added. A fact never removes or changes a
  finding of the first search, so a wrong fact cannot hide a conflict that is
  proven from the rules alone.

  ```
  situation   (and password_submitted password_correct account_locked)
  search 1    situation + all rules           satisfiable   → no conflict
  search 2    situation + all rules + facts   unsatisfiable → conflict {R1, R4}, needs F2
  ```

- **A conflict that needs one says so** ("if the assumed facts hold"), and the
  report quotes the fact:

  > This depends on assumptions that are not stated in the requirements:
  > - F2: The system cannot grant access and deny access simultaneously.

- **A wrong one is easy to remove:** delete it from `formal.json` and run
  again with `--formal`.

## How sure is a finding

The title of each finding says how far to trust it. These are real titles:

| The title says | Meaning | Example |
|---|---|---|
| nothing more | proven from the rules alone | "Conflict: Backorder Requirement Conflict" (R2 against R3, order spec) |
| "if the assumed facts hold" | proven only with an assumed fact | "Conflict (if the assumed facts hold): Conflict between correct password and locked account" |
| "doubtful: ..." | proven, but probably an artefact of the formulas | the two cases below |
| "depends on the reading of R3" | proven with the first reading of R3, which is ambiguous; gone with its other reading | "Gap (no event happens, depends on the reading of R3)", the gap at 6 failed attempts in the login spec ([Ambiguities](#ambiguities)) |
| "found with k of K symbol sets" | optional: the spec was translated K times, each time with other symbols, and k of them found it | "Conflict (found with 3 of 3 symbol sets): Conflict between removal and retention" |

A conflict is marked *doubtful* in two cases. It stays in the report, marked.

The first case is two events at the same moment. A situation is one snapshot,
so Z3 may let two events happen at once, while requirements are written for
one event at a time. In a newsletter spec:

```
rule 1      "WHEN a visitor submits the signup form THEN the system sends no email ..."
            trigger: visitor_signed_up
rule 2      "WHEN a subscriber changes the email address THEN the system sends a confirmation email"
            trigger: address_changed
situation   visitor_signed_up = true, address_changed = true
            → rule 1: no email, rule 2: an email → conflict
mark        the two rules react to two different events → doubtful
```

The *trigger* is the event a rule reacts to. The LLM names it when it reads the spec.

The second case is a situation that the assumed facts call impossible. In a
booking spec, "cancels at least 24 hours before" means no fee, and "less than
24 hours before" means a late fee. Written as two yes/no symbols, both can be
true for Z3:

```
situation   at_least_24h = true, less_than_24h = true    → no fee and a late fee → conflict
fact        (not (and at_least_24h less_than_24h))        → this situation cannot happen
mark        doubtful: "the assumed facts say this situation cannot happen"
```

## Several symbol sets

Every finding depends on the symbols the LLM picks, and it does not always
pick the same ones. With `--symbol-sets 3` the spec is formalized 3 times, and
each finding says with how many of the 3 it was found. For `delete_property`:

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

One of the 3 symbol sets also split on D2 itself, 4 against 4. That gives the
question the Kiro blog shows for this spec:

> **2. Ambiguity (found with 1 of 3 symbol sets): Ambiguity in Deletion Definition**
>
> Requirement D2 is unclear about what "remove the Property record" means. One
> reading requires that the record be physically erased from the database, while
> the other only requires that the property be considered deleted (which, per D4,
> allows the record to remain in the database). Which did you mean?

The saved run is in
[experiments/examples/delete_property_links](experiments/examples/delete_property_links).

## Run it

```
uv sync          # on a "hardlink" error: set UV_LINK_MODE=copy and retry
```

Then, inside the project's `.venv`.

**Without a GPU.** This runs the solver only, on a saved `formal.json`. The
report has the proven facts, without wording and without scenarios.

```
python -m speccheck specs/order/requirements.md --formal specs/order/formal.json --out out
python -m pytest tests
```

**With the LLM.** Any OpenAI-compatible server will do.

```
# on the cluster, in ~/speccheck:   sbatch --time=00:30:00 serve.sbatch     (ready in about 3 minutes)
ssh -N -L 18200:hpc-nodegpu01:18200 <user>@hpc-ctrl01.acc-ub.local
export OPENAI_API_KEY=<content of ~/speccheck/api_key on the cluster>
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1 --symbol-sets 3
```

**With the second model.** It is optional and finds more ambiguities. It needs
the same 2 GPUs, so it runs as its own job after the first one (plan.md,
section 8). With more GPUs both servers can run at once, and you add
`--second-base-url http://localhost:18201/v1` to the command above.

```
# on the cluster:   sbatch --time=00:40:00 serve_second.sbatch
ssh -N -L 18201:hpc-nodegpu01:18201 <user>@hpc-ctrl01.acc-ub.local
python -m experiments.evaluate --rescore experiments/results/<run>.json --second-base-url http://localhost:18201/v1
```

The output is written next to the spec, or into `--out`:

| File | Content |
|---|---|
| `formal.json` | the spec as logic: symbols, assumed facts, rules (`formal_2.json` ... with `--symbol-sets`) |
| `findings.json` | what the solver proved, with its wording |
| `report.md` | the same, in plain language (also printed) |

A 5-rule spec takes under a minute, and about a minute with 3 symbol sets.
When you are done, cancel the server job: it holds the account's two GPUs.

## It works on any spec

Nothing in the code or in the prompts is about orders.

| Specs | Format | Used for |
|---|---|---|
| `specs/order`, `specs/delete_property` | Kiro EARS | the two examples of the Kiro blog |
| `specs/auth_openspec` | OpenSpec (`### Requirement` / `#### Scenario`) | another format; two conflicts we planted |
| `experiments/sets/`: `eval` to `eval8` (201 specs) | both | 48 specs in new domains, each clean and with planted defects. Each set was written before it was used, as a test the prompts had not seen |

## How reliable is it

Each line is a test on specs the prompts had not seen, with 3 runs per spec:

| Test | Planted conflicts found | Clean runs with a false alarm | Planted ambiguities found |
|---|---|---|---|
| `eval/` (E5) | 44 of 48 | 0 of 18 | 2 of 9 |
| `eval2/` (E7) | 31 of 36 | 0 of 18 | 17 of 36 |
| `eval3/` (E8), doubtful conflicts set aside | 15 of 21 | 1 of 18 | 14 of 36 |
| `eval4/` (E9), doubtful conflicts set aside | 21 of 21 | 0 of 18 | 14 of 36; 30 of 36 with the second model |
| `eval5/` (E10), doubtful conflicts set aside | 11 of 18 | 0 of 18 | 15 of 36 |
| `eval6/` (E11), doubtful conflicts set aside | 15 of 18 | 0 of 18 | 19 of 36 |
| `eval7/` (E12), doubtful conflicts set aside | 13 of 18 | 0 of 18 | 17 of 36; 32 of 36 with the second model |
| `eval8/` (E13), doubtful conflicts set aside | 18 of 21 | 0 of 18 | 20 of 36 |

Some notes on these numbers:

- Assumed facts and links carry a large part of the result. Without them,
  `eval3/` gives 10 of 21.
- On `eval3/` and `eval4/`, every doubtful conflict was a false alarm. On
  `eval5/` one planted conflict was marked too ("WHEN a member is suspended"
  was read as an event), so with doubtful conflicts counted, E10 finds 14 of 18.
- The second model finds about twice as many ambiguities, and raises about
  twice as many flags on clean specs (7 → 15 on `eval4/`, 5 → 9 on `eval7/`,
  in 18 runs).
- `delete_property`, the blog's second example, was found in 3 of the last 3
  runs. It was missed in 4 of 7 earlier runs, 3 times because of a wrong voted
  fact (research.md 4.3).
- Gaps were measured for the first time on `eval8/`, where one of two
  complementary requirements was removed: all 18 planted gaps were found. On
  the clean specs, 4 of 18 runs reported a gap that is not one, each time
  because two complementary conditions had become two symbols ("the slot is
  free", "the slot is taken").
- One spec of 30 requirements (`experiments/sets/size`) went as well as the
  small ones: 6 of 6 planted conflicts, none on the clean version, and under
  a second in the solver stage. That is one spec, not a study of size.
- The numbers are small: the specs were written by us, and there is one main
  model. The details are in [research.md](research.md).

## Known limits

| Limit | What it means |
|---|---|
| A finding is a proof about `formal.json`, not about your intent | the LLM mistranslates → the solver proves the wrong thing |
| One model finds about half of the ambiguities | it is confident about readings a person would ask about. A second model finds most, and flags about one more clear rule per spec |
| An assumed fact or link can be wrong, even with a majority | the report quotes every one a conflict depends on, so you can judge |
| Some proven conflicts are artefacts of the model | two events at the same moment ("a visitor signs up" while "a subscriber changes the address"); "at least 24 hours" and "less than 24 hours" as two symbols, both true. These are marked *doubtful* |
| The *doubtful* mark needs the LLM to name the event each rule reacts to | a state taken for an event ("WHEN a member is suspended") marks a real conflict too |
| "Remove" against "keep" is missed in about half of the cases | "delete the listing" vs "keep every listing for seven years" become unrelated symbols, or a number, and nothing connects them. The main cause of missed conflicts |
| Gaps depend on the symbols, and on the events the LLM marks | a gap is looked for once for each event; the gap in which no event happens, which almost every spec has, is marked as such |
| One snapshot, no time | "then", "after" and "until" are not modelled |
| One document | checking a change against specs that already exist is the next step (plan.md) |

## Optional: an LLM review of the text (off by default)

This project is the formal check only. Kiro also has an LLM stage that reads
the text itself, which it calls "refinement". A version of it exists here in
`speccheck/refine.py`, and it runs only with `--review`. What it found is in
research.md, section 5.

## Files

| File | What it does |
|---|---|
| `speccheck/llm.py` | the one place that calls the model (answers forced into a JSON schema) |
| `speccheck/logic.py` | symbols to Z3 variables, formula parsing, solver questions |
| `speccheck/formalize.py` | stage 1: read, sample, cluster, facts, links; several symbol sets |
| `speccheck/probe.py` | stage 1, step 6: questions about concrete situations |
| `speccheck/checks.py` | stage 2: conflicts, gaps, scenarios; which findings depend on a reading; merging several symbol sets |
| `speccheck/explain.py` | stage 3: wording, the scenario judge, the Markdown report |
| `speccheck/cli.py` | runs the three stages |
| `speccheck/refine.py` | optional LLM review, off by default |
| `experiments/slurm/serve.sbatch`, `experiments/slurm/serve_second.sbatch` | start the vLLM servers on the cluster: the main model, the second model |
| `tests/` | 42 tests of everything that needs no LLM |
| `experiments/sets/`, `experiments/make_eval.py` | the evaluation sets `eval` to `eval8` and `size`, and the script that writes them |
| `experiments/results/` | every experiment: the raw data (`.json`) and its tables (`.md`) |
| `experiments/evaluate.py` | runs and scores the evaluation; re-scores saved runs without a GPU |
| `experiments/stability.py`, `fact_threshold.py` | the earlier experiments |
| `experiments/examples/` | saved runs referred to above and in research_log.md |
