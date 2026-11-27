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

It also checks an OpenSpec *change* against the specs that already exist, and
reports what the change breaks
([Checking a change against existing specs](#checking-a-change-against-existing-specs)).

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
| the list of symbols has several for one thing, or none for what a rule demands | translations that differ only in their symbols vote; a rule that could not be written is read a second time, for the symbols it lacks | [Ambiguities](#ambiguities) |
| two rules say opposite things in different words | it lets the model propose *assumed facts* ("access cannot be both granted and denied"), and asks it directly whether the outcomes of two rules can both hold. It keeps what a majority of answers agree on, and uses it only to find more conflicts | [Assumed facts and links](#assumed-facts-and-links) |
| a contradiction is a chain of three rules: what one rule demands is, in other words, what makes another rule apply | it asks the model whether the words of the first rule say that a part of the other rule's condition is the case | [Specs about the runs of an agent](#specs-about-the-runs-of-an-agent) |
| the logic has no time, and the solver lets two conditions hold together that exclude each other, so some proven conflicts are not real | it marks them *doubtful* instead of hiding them. For two rules that clash, it asks the model whether their conditions can hold together | [How sure is a finding](#how-sure-is-a-finding) |
| the findings depend on the symbols the model chose | it can formalize the spec several times and say how often each finding came up | [Several symbol sets](#several-symbol-sets) |
| the spec is about the runs of an agent that calls tools: its rules are about a whole run, it mixes rules with examples, and it has hundreds of scenarios | two options say so (`--whole-run`, `--examples`), and a project with more than 100 scenarios is checked in parts | [Specs about the runs of an agent](#specs-about-the-runs-of-an-agent) |

Where the project stands:

- it finds what the Kiro blog finds, on both of the blog's examples. One of
  the three findings of the first example, R1 against R5, is marked
  doubtful in a run made today ([Known limits](#known-limits));
- on 10 sets of specs it was not built on, it found 61 to 100% of the
  conflicts we had planted, with at most 1 false alarm in 18 clean runs
  (doubtful conflicts set aside);
- on an eleventh set, where every planted conflict says the opposite outcome
  in other words, it found 34 of 36. That is with a newer step, the questions
  about two outcomes, which also reports more conflicts that nobody planted
  (3 of 18 clean runs);
- it found 71 of the 72 planted gaps on the four sets that have them, and
  reported a gap that is not one in 0 to 5 of 18 clean runs;
- it finds about half of the planted ambiguities, and 30 to 32 of 36 with a
  second model, at the price of up to one extra question per spec;
- for a change to specs that already exist, it found all 180 conflicts and
  125 of the 126 gaps we had planted in 138 changes it was not built on, among
  them every gap that a removed requirement opens. A cheaper way to check a
  change, the option `--incremental`, is off by default: it costs a sixth to a
  seventh. On one test set it found 50 conflicts where the full way found 54,
  on the next one all 72
  ([The two ways to check a change](#the-two-ways-to-check-a-change));
- for the specs of an agent system, whose rules are about whole runs and
  stand next to examples, there are two options and a second question about
  links. On a set it was not built on, with doubtful conflicts set aside:
  the conflicts between rules about two calls of one run are found in 12 of
  12 runs, where all 12 were doubtful before, and of 24 runs on changes that
  should give nothing, none has a conflict about the change, where 17 had
  one. Since then the model is also asked whether what one rule demands
  makes another rule apply. On a third set a contradiction that is a chain
  of three rules is found in 12 of 12 runs, and in 2 without that question;
  an example that breaks a rule by its own words in 12 of 12, and in none.
  On a fourth set, with a rule that applies in several cases, that question
  gave a wrong conflict in 6 of 12 runs until it was put as a statement to
  judge, and in none since. 11 of that set's 36 runs stopped before the
  checks: the model had listed a rule about two calls twice. Such copies
  are one rule now, and on a fifth set all 36 runs finish, where 25 did
  ([Specs about the runs of an agent](#specs-about-the-runs-of-an-agent));
- all of that is on specs we wrote. On 69 changes of a real project it does
  worse. What we planted in 21 of them is found: 46 of 52 conflicts with a
  copied condition, 10 of 16 with a condition of their own. But one rule in
  six to one in four gives the checks nothing to work with, the more the
  longer the spec, and of 20 reported conflicts that nobody planted, which
  we read, none is a real contradiction: 12 are artefacts and 7 set a
  general rule against its own exception. A question about the two
  conditions now marks one such conflict in six to nine as doubtful, and
  one in three to six says in its title that it is a rule against a special
  case of it; about half are still reported with no mark
  ([How reliable is it](#how-reliable-is-it));
- a second real project is of an agent system:
  [TestingTheAgents](https://github.com/unibuc-cs/TestingTheAgents), with 33
  spec files, 465 scenarios and four open changes, one of which its authors
  say cannot be built, for four reasons. Each change is checked in 32 or 33
  parts. Two of the reasons are in its report: a contradiction between two
  rules of the change, found in 16 of the 24 parts of the application's
  specs, and an approval that an existing rule demands and the change
  forbids, a chain of three rules. In the spec files of the other three
  changes no conflict is found in more than 3 parts. The other two reasons
  are not found, and every report also has 1 to 6 conflicts with a rule of
  another spec file that are artefacts, mostly other ones in each run ([A real project of that kind](#a-real-project-of-that-kind-testingtheagents)).

| Read next | For |
|---|---|
| [GUIDE.md](GUIDE.md) | a guided tour for a first reading: every idea from an example, in small steps |
| [commands.md](commands.md) | the commands on one page: set up, start the model, check a spec or a change, run an evaluation, run it on TestingTheAgents |
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

A gap is looked for once for each event the rules react to: "is there a
situation in which an order is submitted and no rule applies?" Here every
event is covered. The only gap left is the one in which nothing happens at
all. That one is rarely something to fix, because a system normally just waits
then, and the report marks it "no event happens".

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

These files were saved before the model was asked about the conditions of
two rules that clash ([How sure is a finding](#how-sure-is-a-finding)). A
run made today finds the same, and marks the second conflict, R1 against R5,
as doubtful: the model holds that an order which is canceled and refunded
cannot be one that is being submitted ([Known limits](#known-limits)).

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

Not every split is two readings. On real specs the eight translations often
differ only in which symbols they use: three say `success_message_displayed`,
two say that and `spec_summary_displayed`. Such translations vote, and the
rule is accepted with the strongest translation that more than half of them
entail, here the first. A split between translations that use the same
symbols, like A and B above, is never settled that way. The price is that a
voted rule can say less than its words: here the summary of the specs is not
in the formula.

Some rules cannot be written at all, because the list has no symbol for what
they demand. "WHEN file write fails THEN let the error bubble up naturally
with file path" came out as `file_write_failed => true`: a rule that demands
nothing. Such rules are read a second time, alone, with the symbols so far,
and the model is told that a symbol is missing. Here it added
`error_bubbles_up_with_path`, and all eight new translations said
`file_write_failed => error_bubbles_up_with_path`. A rule takes its new
translation only if it is accepted now (the eight agree, or the vote above
settles them), and a new symbol is kept only if such a translation uses it.

Until the author answers, the checks use reading A, and some findings may
exist only because of that choice. So each ambiguous rule is tried once more
with its other reading, by the solver alone. A conflict or a gap that is gone
with the other reading says so in its title, and the ambiguity lists what its
other reading changes. In a spec for topping up a phone
(`experiments/examples/topup_reading`), R4 is "WHEN a customer enters a wrong
PIN for the third time THEN the system locks the account for 24 hours". It was
read as "exactly the third time", and the gap at the fourth wrong PIN exists
only with that reading:

> **4. Gap (depends on the reading of R4): Unclear PIN lock trigger**
>
> The requirements do not specify what the system must do when a customer
> enters a wrong PIN for the fourth time. This gap exists only if R4 is read
> to mean the account locks strictly when the count reaches three; the other
> reading is that the account locks whenever a wrong PIN is entered and the
> count of consecutive wrong entries is at least three.
>
> *Proven:* No requirement says what the system must do in this situation: [...]
> But R4 is ambiguous (see its finding). With its other reading a requirement
> applies in this situation. That reading: The system locks the account for
> 24 hours if the customer enters a wrong PIN and the count of consecutive
> wrong entries is at least three.

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

**Voted facts.** The LLM is asked 8 times to list the facts that hold "purely
because of what the symbols mean". It is shown only the symbols with their
meaning (`access_granted`: "The system grants access to the user"), not the
requirements. Each answer is a list of facts, and each fact is a sentence and
a formula:

```
F2   "The system cannot grant access and deny access simultaneously."
     (not (and access_granted access_denied))
```

Then the 8 answers vote on every fact that any of them proposed. They word the
same fact differently, for example `(=> access_granted (not access_denied))`,
so an answer votes for a fact when Z3 proves that the fact follows from that
answer's own facts:

```
(and <facts of answer k> (not F2))    unsatisfiable  →  answer k votes for F2
```

F2 has 7 of the 8 votes. More than half are needed, so it is kept.

**Links.** Sometimes a rule uses a symbol that no other rule uses, and then
nothing can clash with it. This happens in the Kiro blog's other spec,
`specs/delete_property/requirements.md`:

```
D2: WHEN a Property Owner confirms deletion, THE Platform SHALL remove the Property record from the Platform
D4: THE Platform SHALL implement soft deletion to retain Property records in the database for audit purposes while hiding them from the user interface
```

The LLM writes D2 with a symbol of its own, `property_record_removed`, and D4
with `property_record_retained_in_db`. For Z3 the two are unrelated, so a
record can be removed and retained at once. So D2 is translated 8 more times,
and this time the LLM may not use D2's own symbol. It may use only the symbols
with which the *other* rules say what they demand. For D2, 8 of 8 answers say
"not retained in the database", and that becomes the *link*:

```json
{"id": "F1", "restates": "D2", "support": "8/8",
 "text": "What D2 demands, in the terms of the other requirements: When a property owner confirms the deletion of a property, the platform must remove the property record from the database.",
 "formula": "(=> (and deletion_confirmed property_record_removed) (not property_record_retained_in_db))"}
```

A link is tested before it is used. The LLM is asked 8 times whether the
record could still be in the database in a system that does everything D2
demands, and more than half of the answers must say "impossible". With this
link, Z3 proves the conflict between D2 and D4.

That test does not show the rule's own symbol, so it passes a link that only
moves a rule's demand to another symbol of the same kind. Such a link is
asked about a second time, with both symbols in view; the example is under
[Specs about the runs of an agent](#specs-about-the-runs-of-an-agent).

**Questions about two outcomes.** The voted facts come from an open question,
and the answers often leave out the pair that matters. In a canteen spec
(`experiments/sets/eval7/canteen_overlap`), "take the price from the balance"
became `payment_taken` and "refuse all payments" became `payment_refused`. No
voted fact connected the two, so the conflict between these rules was missed
in 3 of 3 runs. Now our code picks every pair of rules that can apply together
and whose outcomes share no symbol, and the LLM is asked 8 times about the two
outcomes alone, without the requirements:

```
Statement A:   TRUE: payment_taken (The system has deducted the meal price from the card balance)
Statement B:   TRUE: payment_refused (The system has declined the payment request)
Question:      can A and B both hold in the same snapshot?    → 8 of 8 answers: impossible
New fact:      (not (and payment_taken payment_refused))
               "A payment cannot be successfully taken and refused at the same time."
```

With this fact Z3 proves the conflict. The steps of all three are in
[GUIDE.md, section 3.2](GUIDE.md#32-telling-the-solver-what-the-words-mean).

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
| "doubtful: ..." | proven, but probably an artefact of the formulas | the cases below |
| "depends on the reading of R4" | proven with the first reading of R4, which is ambiguous; gone with its other reading | "Gap (depends on the reading of R4): Unclear PIN lock trigger", the gap at the fourth wrong PIN in the top-up spec ([Ambiguities](#ambiguities)) |
| "found with k of K symbol sets" | optional: the spec was translated K times, each time with other symbols, and k of them found it | "Conflict (found with 3 of 3 symbol sets): Conflict between removal and retention" |
| "found in k of K parts" | only for a project that is checked in parts: K parts hold all the rules of this finding, and k of them found it as it is shown | "Conflict (found in 18 of 32 parts, R479 is a special case of R477)", for two contracts of one function, in a change to a real project of 479 scenarios ([below](#a-real-project-of-that-kind-testingtheagents)) |
| "Not checked: ..." | not a finding about the spec: the requirement could not be written in logic, because no symbol stands for what it demands, and it took no part in the checks | "Not checked: Uncheckable Success Message Requirement", for a rule that demands a message with three prompts in it (a real project, below) |
| "opened by removing X1" | only when a change is checked: a rule that the change removes used to cover this situation | "Gap (opened by removing X1): Missing rule for unauthorized check-in" ([Checking a change](#checking-a-change-against-existing-specs)) |
| "R2 is a special case of R1" | only for a conflict between two rules: R2 applies only where R1 does, which the solver proves. Not a doubt. If R2 is meant as the exception, R1 does not say so | "Conflict (if the assumed facts hold, R2 is a special case of R1)", for "`createChange(...)` is called: create the directory" against "... and the directory already exists: throw an error" (a real project) |

A conflict is marked *doubtful* in three cases, and a gap in the second one.
A marked finding stays in the report. The third case, a situation that says
more than an example does, needs the option `--examples` and is shown under
[Specs about the runs of an agent](#specs-about-the-runs-of-an-agent).

The first case is two events at the same moment. A situation is one snapshot,
so Z3 may let two events happen at once, while requirements are written for
one event at a time. (With `--whole-run` a situation is a whole run, and this
mark is not given.) In a newsletter spec:

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

The facts rarely say such a thing by themselves. So for two rules that clash
under two different conditions, the model is asked directly, eight times,
whether the two conditions can hold together. In a real spec:

```
R5         "WHEN agent reads tasks.md AND incomplete tasks are found THEN display warning ..."
R7         "WHEN tasks.md does not exist THEN proceed without task-related warning"
situation  tasks_md_read = true, tasks_md_exists = false     → a warning and no warning → conflict
asked      A: tasks_md_read is TRUE, all_tasks_complete is FALSE.   B: tasks_md_exists is FALSE.
answers    6 of 8 "impossible": "A file cannot be read if it does not exist."
mark       doubtful, with that sentence quoted
```

The model sees only the two conditions, not the requirements, and is told
that "impossible" means excluded by the meaning of the words, not prevented
by a system that behaves. Two rules with the same condition, or a rule and a
special case of it, are not asked about.

For a gap, the two symbols are both false. In a laundry spec, "the slot is
free" and "the slot is taken" each have a rule:

```
situation   resident_books_slot = true, slot_is_free = false, slot_is_taken = false    → no rule applies: a gap
fact        (or slot_is_free slot_is_taken)                                            → this situation cannot happen
mark        doubtful: "the assumed facts say this situation cannot happen"
```

The model rarely proposes a fact like this one, so most such gaps stay
unmarked ([Known limits](#known-limits)).

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

## Checking a change against existing specs

In an OpenSpec project the specs say what the system does today, and new work
arrives as a *change*, a folder that holds only the difference.
`specs/auth_change` is the login spec laid out that way:

```
openspec/specs/auth/spec.md                               what exists: 4 scenarios, one of them
    "WHEN the number of failed attempts on an account reaches 5 THEN the system locks the account"

openspec/changes/admin-never-locked/specs/auth/spec.md    the change
    ## ADDED Requirements
    "WHEN the account belongs to an administrator THEN the system does not lock the account"
```

Neither file has a conflict on its own. With `--change`, speccheck first
applies the change to the specs, as OpenSpec does when a change is archived,
and writes the result as one document in which every scenario has a label
(R1 to R5 here). That document goes through the three stages like any spec.
Then our code keeps the findings that involve a rule the change added or
modified. This is the top of the report:

> Change `admin-never-locked`, checked against the specs that exist: 1
> scenario(s) added, 0 modified, 0 removed.
>
> Shown are the findings that involve an added or modified rule (R5). 3 other
> finding(s), among the existing requirements alone, are in findings.json.
>
> **1. Conflict: Administrator Account Lock Conflict**
>
> Requirement R3 states that the system must lock an account when the number
> of failed attempts reaches 5. However, Requirement R5 states that the system
> must not lock an account if it belongs to an administrator. In the situation
> where an administrator's account has reached 5 failed attempts, the system
> is forced to both lock and not lock the account, which is impossible.

The 3 findings that are not shown were there before the change: R1 against R4
(the conflict of [Assumed facts and links](#assumed-facts-and-links)), the
ambiguity of R3, and the gap in which no event happens. The report ends with
a table that says, for each rule, which spec file and requirement it comes
from.

A change can also remove a rule, and leave a case open. The scenarios that a
change removes stay in the merged document under labels of their own (X1,
X2, ...), so that they get the same symbols as the rest. They are taken out
before the checks, and Z3 is asked one more question for each: is the
situation this rule was written for still covered? In a spec for hospital
visitors, a change drops the scenario for a visitor who is not on the
patient's list (`experiments/examples/visitors_removed`):

> **1. Gap (opened by removing X1): Missing rule for unauthorized check-in**
>
> The requirements do not specify what the system must do when a visitor who
> is not on the patient's visitor list attempts to check in. This gap exists
> because the previous rule that handled this specific scenario was removed.

### The two ways to check a change

There are two ways to run the check. The default is the full run. The option
`--incremental` is cheaper. On one of the two sets it was tested on, it found
less than the full run, so it is off unless you ask for it.

| | Default: `--change DIR` | Option: `--change DIR --incremental` |
|---|---|---|
| What the LLM formalizes for a change | all the specs, with the change applied | only the scenarios that the change adds or rewords (labels N1, N2, ...) |
| How old and new rules get the same symbols | they are read together, in one document | the specs were formalized once before; the read step is shown those symbols and told to use them |
| Requests to the LLM for one change (measured on `eval14/` and `eval15/`) | 68 | 9 and 11; none for a change that only removes |
| Cost that comes once | none | one full run of the specs that exist, about 60 requests |
| Planted conflicts found on `eval14/` (36 changes, both ways) | 54 of 54 | 50 of 54 |
| Planted conflicts found on `eval15/` (36 changes, both ways, after a change to the read prompt) | 72 of 72 | 72 of 72 |
| Planted gaps found (`eval14/`, `eval15/`) | 36 of 36, 18 of 18 | 36 of 36, 18 of 18 |
| Clean changes with something reported about them | 0 of 18 on each set | 0 of 18 on each set |
| Files written | `merged.md`, `formal.json`, `findings.json`, `report.md` | `new.md` in place of `merged.md`, and the saved model, `openspec/.speccheck/base.json` |
| Cannot be combined with | | `--symbol-sets`, `--second-base-url`, `--review` |

What to know before using `--incremental`:

- **The saved model.** The first run formalizes the specs under
  `openspec/specs` and saves their formal model in
  `openspec/.speccheck/base.json`. Later runs use that file, and say so on the
  error stream ("using the saved model of the specs").
- **When it is made again.** The file records what it was made from: a
  fingerprint of the text of the specs, and the name of the model. If either
  is different, the specs are formalized again, by one full run. That happens
  after you edit a spec, after a change is archived into the specs, and when
  you ask another model. To force it, delete the file.
- **So it pays off** when several changes are checked against the same specs,
  or when one change is checked again and again while it is written. A single
  check after every archived change costs a full run each time, as the
  default does.
- **What it misses.** In the first test (`eval14/`) the 4 conflicts it missed
  were two new rules that were rejected because their translations disagreed.
  One was "WHEN a person is younger than 17 THEN the system does not create
  any learner file": shown only the saved symbols, the LLM tied it to the
  saved event "a person registers", which the rule does not name. The read
  prompt was changed for that case, and in the second test (`eval15/`)
  nothing was missed. The cause is not gone: the LLM still ties some new
  rules to a saved event, and such a rule is reported as ambiguous more
  often. A finding it does report is as sure as one of the full run.
- **Keep the file out of version control** if the specs are edited by several
  people; it is a cache. This repository ignores `.speccheck/`.

A saved run of the option is in `experiments/examples/auth_incremental`.

The steps are in [GUIDE.md, part 5](GUIDE.md#5-checking-a-change-against-the-specs-that-exist),
with the message to the model and the questions to Z3 written out for both
examples.

### Specs about the runs of an agent

Some specs do not say what a system does at one moment. They say what a
whole run of an assistant that calls tools may contain, and they mix rules
with examples. Two options tell speccheck so. The examples are three changes
to one project of ours, a dispatcher that ships parcels
(`experiments/sets/eval20/parcels_*`); the saved runs are in
`experiments/examples/parcels_cross`, `parcels_clean` and `parcels_twins`.

**`--whole-run`: a situation is a whole run.** The first change adds R6:

```
R2   "WHEN a call of `ship_parcel` succeeds in a run with a plan
      THEN an earlier call of `request_signoff` in the run was approved"
R6   "WHEN an express request is handled in a run THEN `request_signoff` is not called in the run"
```

The two react to two different happenings, and both can be in one run. Read
as moments, their conflict is marked doubtful, as two events at once. With
the option it is a conflict like any other, and the question about two
outcomes ([Assumed facts and links](#assumed-facts-and-links)) is asked of
such pairs too:

> **1. Conflict (if the assumed facts hold): Express requests and signoff conflict**
>
> The requirements state that if an express request is handled, no signoff
> request is made (R6), but if a parcel ships successfully in a run with a
> plan, a signoff must have been approved earlier (R2). In the situation
> described, an express request is handled in a run with a plan where a
> parcel ships successfully, which creates a contradiction because the
> successful shipment requires a prior signoff that the express handling
> forbids.

**`--examples PATTERN`: some scenarios are examples.** The second change
adds three cases of one request:

```
R8    "Example: a return is booked"              WHEN dana asks to return parcel k7 AND k7 was delivered
                                                 THEN `book_return` is called once ...
R9    "Example: the parcel was never delivered"  WHEN the same request runs while k7 is still in the warehouse
                                                 THEN `book_return` is never called ...
R10   "Example: the customer cancels"            WHEN the same request runs and the customer cancels the return
                                                 THEN `book_return` is called once ...
```

Read as rules for all cases, R9 and R10 clash for a parcel that is still in
the warehouse while the customer cancels. Neither example says that: each is
about its own case. The pattern is a regular expression, looked for in the
name of a scenario and in the lines below it; here the name of every example
starts with "Example:". Then:

1. Our code marks the rules of those scenarios as examples.
2. For each example in a conflict, Z3 is asked whether its own case, its
   condition and what it demands, makes the other rules of the conflict
   apply. R9's case is a parcel in the warehouse; it does not say that the
   customer cancels.
3. If one example fails that test, the conflict is marked:

> **2. Conflict (if the assumed facts hold, doubtful: the situation says more than the example does): Conflicting return rules**
>
> *Proven:* Requirements R9, R10 cannot all be obeyed in this situation: ...
> But R9, R10 are examples, one concrete case each, and what each describes
> does not make the other requirement(s) apply: this situation says more
> than they do. So the conflict may be a false alarm.

A conflict stays as it is when every example in it passes: an example in
which `ship_parcel` succeeds and nobody signs off, against R2; or two
examples with the same condition and opposite outcomes. An example and a
variant of it ("WHEN the same request runs while ...") are two cases: the
first does not say what the variant adds.

**No option: a setting named like another.** The third change adds a
second limit, R6 in its own document:

```
R1   "... `shipping.max_parcels` is the integer 20"          (= max_parcels 20)
R6   "... `shipping.max_batch_parcels` is the integer 50"    (= max_batch_parcels 50)
link of R6, 8 answers of 8:  "The system's configured maximum number of parcels must be 50 ..."    (= max_parcels 50)
test of the link:            8 of 8 "impossible"  → the link would be used, and R1 would clash with R6
```

The test shows the requirement and a situation in which `max_parcels` is 51,
and the model takes that setting for the one in the requirement. So a link
that only moves a demand to another symbol is asked about once more, with
both symbols and their descriptions:

```
Statement A:   max_batch_parcels = 50 (The configured maximum number of parcels in a batch)
Statement B:   max_parcels = 51 (The configured maximum number of parcels)
Question:      can A and B both hold?    → 8 of 8 answers: possible
```

The link is used only if most answers say "impossible", so it is left out,
and the report of that change has no finding. The same question confirms the
link that the first example needs: "an earlier call of `request_signoff` was
approved" and "`request_signoff` is not called" got 8 of 8 "impossible".

**No option: a chain of three rules.** In another project of ours, the front
desk of a hotel (`experiments/sets/eval22/hotel_chain`; the saved run is
`experiments/examples/hotel_chain`), a change adds R4 and R5:

```
R1   "WHEN a call of `check_in_guest` succeeds in a run with a plan
      THEN an earlier call of `ask_manager` in the run was approved"
     (=> (and check_in_guest_succeeded run_has_plan) ask_manager_approved)
R4   "WHEN a call of `ask_manager` is made THEN the run is not a late-arrival run"
     (=> ask_manager_called (not run_is_late_arrival))
R5   "WHEN a call of `check_in_guest` succeeds in a late-arrival run THEN the answer gives the night code"
```

A late arrival who is checked in in a run with a plan needs the manager's
approval (R1), and in such a run the manager is not asked (R4). But no two
of these rules clash by themselves: R4 applies only where `ask_manager` is
called, and nothing says that an approved call is a call that was made. So:

1. Z3 picks the pairs. In a late-arrival run with a plan in which a
   check-in succeeds, R1 and R5 apply, and R4 cannot apply as well: it
   forbids the call there. So the question is whether what R1 demands makes
   R4 apply.
2. The model gets the words of R1 and one statement B, and is asked eight
   times: B is not given; must it be true wherever the requirement applies
   and is obeyed?

   ```
   Requirement:   WHEN a call of `check_in_guest` succeeds in a run with a plan THEN an earlier call of `ask_manager` in the run was approved
   Statement B:   TRUE: ask_manager_called (A call to ask_manager is made in the current run)
   answers:       8 of 8 "yes".  For R2, R3, R5 and R6, asked the same about that statement: 8 of 8 "no"
   ```

3. More than half "yes" is an assumed fact: where R1 applies and is obeyed,
   `ask_manager_called` holds. With it Z3 proves the conflict:

> **1. Conflict (if the assumed facts hold): Conflict between manager approval and late-arrival rules**
>
> - **A) Keep as-is:** Keeping the requirements as written means that a
>   successful check-in in a planned, late-arrival run is impossible because
>   it would require both an approved manager request and the absence of
>   any manager request.
>
> *Proven:* Requirements R1, R4 cannot all be obeyed in this situation: ...
> This depends on assumptions that are not stated in the requirements:
> - F1: Where R1 applies and is obeyed, a part of the condition of R4 holds:
>   If an earlier call to ask_manager was approved, then a call to
>   ask_manager was made in the run.

The model is shown the words of the rule, not its symbols, and the one
statement alone. Its prompt says two more things, each learned from a form
of the question that failed:

- What a system would merely need does not count: "to give the return label
  it must have found the parcel" is a "no".
- B is not given. Shown B as a fact marked TRUE, the model took it as given
  wherever B is one of the cases in which the rule applies. In another
  project of ours, R2 is "WHEN a call of `ask_vet` or `order_medicine` is
  made THEN the agent making it is the reception agent". Asked whether
  `order_medicine` is then called, up to 7 answers of 8 said yes: the fact
  says that it is called, so the rule applies. The rule applies when
  `ask_vet` is called too, so the answer is no. Asked "must B be true?", 8
  of 8 say no, in all 12 runs.

In the hotel project, "the guest's card was verified at check-in" does not
say that `verify_card` is called in this run: no "yes" in 10 of 12 runs, at
most 4 of 8 in the others, and nothing is reported.

The same question lifts a doubt from an example. "... THEN the plan is
written once AND `check_in_guest` succeeds once AND `ask_manager` is never
called" breaks R1, but "succeeds once" became a count and R1 is about "a
call succeeds", so the example did not make R1 apply and its conflict was
marked doubtful. Asked with the example's words, the model says that it
does. The question is asked at most 40 times for a document, and for a
change only of pairs with one of its rules.

**No option: a scenario that reacts to either of two calls.** In an
optician's project of ours (`experiments/sets/eval24/optician_direct`):

```
R2   "WHEN a call of `order_lenses` or `order_frame` is made THEN the run writes an audit entry"

the read step returns    R2, trigger order_lenses_called, with those words
                         R2, trigger order_frame_called, with the same words
```

1. A rule has one trigger, the event it reacts to. This rule reacts to
   either of two, so the model lists it once for each.
2. The check of a change tells the rules of the change from the others by
   their labels. Two rules with one label used to stop the run.
3. Now copies with one label and the same words are one rule, with no
   trigger of its own. The translations do not see the trigger; R2 becomes
   `(or order_lenses_called order_frame_called) => audit_entry_written`.

A change that adds "WHEN a call of `order_frame` is made in a warranty run
THEN the run writes no audit entry" then gets its conflict with R2, proven
from the rules alone.

### A project too large for one document

A change is read together with the specs, in one document. That works up to
about 100 scenarios. A larger project is checked in parts, without an
option:

1. Our code writes one document for each spec file that the change does not
   touch. It holds that file and the files the change touches, with the
   change applied. Every scenario keeps the label it has in the whole
   project, so a rule of the change is the same rule in every part.
2. The parts are formalized at the same time and checked one by one.
3. Our code puts the findings together. A finding among the rules of the
   change can show up in every part, and says in how many it was found as
   it is shown: "found in 18 of 32 parts". A finding with a rule of another
   spec file shows up in the part of that file. What is not doubtful comes
   first.

The rules of the change are translated once for each part, each time with
other symbols, so that count says how far a finding depends on the symbols,
as [several symbol sets](#several-symbol-sets) do. `--against PATTERN` checks
the change only against the spec files whose name matches (`"billing-*"`).
What this way cannot find is a conflict that needs rules of three spec
files. A part that cannot be formalized is left out and named in the report.

### A real project of that kind: TestingTheAgents

[TestingTheAgents](https://github.com/unibuc-cs/TestingTheAgents) is a testbed for the
tests of an agent system. Its folder `trace-eval/openspec` has 33 spec files
with 465 scenarios: 24 about the application, an orchestrator and specialist
agents that call tools (`fs-*`), and 9 about the test harness (`testbed-*`).
Four open changes each add a workflow, and `openspec/changes/README.md` says
which of them can be built: three can, and
`add-instant-bulk-takedown-workflow` cannot, for four reasons. In these specs
an example is a scenario whose clause says `use: scenario`.

To run speccheck on it again (in bash; the numbers in this README are from
its commit `f6cb12b`):

```
git clone https://github.com/unibuc-cs/TestingTheAgents ../TestingTheAgents
T=../TestingTheAgents/trace-eval/openspec/changes

# 1. every change against all 33 spec files, in parts: 30 to 60 minutes each on two GPUs
for change in $T/add-*; do
    python -m speccheck --change $change --whole-run --examples "^use: scenario$" \
        --base-url http://localhost:18200/v1 --out out/agents_all/$(basename $change)
done

# 2. the same against the 24 spec files of the application, from the saved parts:
#    the model is asked for the wording only (without --base-url, not at all)
for change in $T/add-*; do
    python -m speccheck --change $change --examples "^use: scenario$" --against "fs-*" \
        --formal "out/agents_all/$(basename $change)/parts/formal_*.json" \
        --base-url http://localhost:18200/v1 --out out/agents/$(basename $change)
done

# 3. one table for the four changes
python -m experiments.agents.tally $T out/agents
python -m experiments.agents.tally $T out/agents_all
```

Each `out/.../<change>` folder then holds `report.md`, `findings.json` and
`merged.md`, and after step 1 also `parts/`, the document and the formal
model of every part. Step 2 can be repeated with any `--against`, and after
a change to the checks, without formalizing again. What the reports say is
under [How reliable is it](#how-reliable-is-it).

## Run it

```
uv sync          # on a "hardlink" error: set UV_LINK_MODE=copy and retry
```

Then, inside the project's `.venv`.

**Without a GPU.** This runs the solver only, on a saved `formal.json`. The
report has the proven facts, without wording and without scenarios.

```
python -m speccheck specs/order/requirements.md --formal specs/order/formal.json --out out
python -m speccheck --change specs/auth_change/openspec/changes/admin-never-locked --formal specs/auth_change/formal.json --out out
python -m speccheck --change experiments/sets/eval20/parcels_cross/openspec/changes/add-express-shipping --examples "^Example:" --formal experiments/examples/parcels_cross/formal.json --out out
python -m speccheck --change experiments/sets/eval22/hotel_chain/openspec/changes/add-late-arrivals --examples "^Example:" --formal experiments/examples/hotel_chain/formal.json --out out
python -m pytest tests
```

**With the LLM.** Any OpenAI-compatible server will do.

```
# on the cluster, in ~/speccheck:   sbatch --time=00:30:00 serve.sbatch     (ready in about 3 minutes)
ssh -N -L 18200:hpc-nodegpu01:18200 <user>@hpc-ctrl01.acc-ub.local
export OPENAI_API_KEY=<content of ~/speccheck/api_key on the cluster>
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1
python -m speccheck path/to/your_spec.md --base-url http://localhost:18200/v1 --symbol-sets 3
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --incremental   # the cheaper way, see "The two ways to check a change"
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --whole-run --examples "^Example:"   # specs about the runs of an agent
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --whole-run --against "billing-*"   # only against the spec files whose name matches
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
| `merged.md` | only with `--change`: the specs with the change applied, every scenario labelled. What the change removes is still in it, under the labels X1, X2, ...; the checks leave it out. The output goes into the change's folder |
| `new.md`, `openspec/.speccheck/base.json` | only with `--change --incremental`: the new scenarios of the change, which is all that is formalized for it; and the saved formal model of the specs that exist |
| `parts/merged_01.md`, `parts/formal_01.json`, ... | only for a project that is checked in parts: the document and the formal model of each part. To run the solver again on them: `--formal out/parts/formal_*.json` |

A 5-rule spec takes under a minute, and about a minute with 3 symbol sets. A
spec of 100 requirements took about 10 minutes; the read step has room for
about 140 requirements (`READ_MAX_TOKENS` in `formalize.py`). A change to a
project of 479 scenarios, checked in 33 parts, took about 40 minutes on two
GPUs.
When you are done, cancel the server job: it holds the account's two GPUs.

## It works on any spec

Nothing in the code or in the prompts is about orders.

| Specs | Format | Used for |
|---|---|---|
| `specs/order`, `specs/delete_property` | Kiro EARS | the two examples of the Kiro blog |
| `specs/auth_openspec` | OpenSpec (`### Requirement` / `#### Scenario`) | another format; two conflicts we planted |
| `experiments/sets/`: `eval` to `eval10`, `eval12` | both | 66 specs in new domains. Each has a clean version and versions with one planted defect, 297 versions in all. Each set was written before it was used, as a test the prompts had not seen |
| `specs/auth_change`, `experiments/sets/eval11`, `eval13`, `eval14`, `eval15` | OpenSpec projects: specs that exist, and a change | the login example as a change, and 24 projects in new domains with 5 or 6 changes each |
| `experiments/sets/mixed` | one larger OpenSpec project (39 scenarios, four spec files) | one change that adds, rewrites, removes and renames at once |
| `experiments/sets/eval16`, `eval17`, `eval18` | OpenSpec format, written like real tool specs: scenarios with two or three outcomes, and states, codes and commands in quotes | eighteen specs, each clean and with a planted conflict or gap; those of `eval18` also with two planted ambiguities |
| `experiments/sets/real1`, `real2`, `real3` | a real project: the OpenSpec tool's own specs (MIT licence, see the README in each folder) | 48 of its archived changes, each with the spec files it touches as they were before it. Nothing is planted, so there is no known answer |
| `experiments/sets/real4` | the same project: 13 more of its changes, each of which creates a new spec | each change as it is, and once more with one scenario of ours that clashes with one of its own: a known answer on real text |
| `experiments/sets/eval19`, `real5` | six specs of our own whose clean versions hold two scenarios with conditions that exclude each other by their meaning; and the last 8 unused changes of the real project, each also with a conflict planted under a condition of its own | the test of the question whether the conditions of two rules that clash can hold together |
| `experiments/sets/eval20`, `eval21` | eight OpenSpec projects of our own about an assistant that calls tools: rules about whole runs, settings, and scenarios that are examples; four and three changes each | the tests of the options for specs about the runs of an agent |
| `experiments/sets/eval22` | four more such projects, each with a rule that a call needs an earlier approved call, and three changes: a contradiction that is a chain of three rules, an example that breaks the rule, and a chain that only looks like one | the test of the question whether what one rule demands makes another rule apply |
| `experiments/sets/eval23` | four more, each also with a rule whose condition names two calls, and three changes: a chain, an example that breaks a rule, and a rule about the second of the two calls, where nothing may be reported | the test of that question put as a statement to judge |
| `experiments/sets/eval24` | four more, each with a rule whose condition names two calls and one whose condition names three, and three changes: a rule that says the opposite of the first of these for one call, an example that breaks a rule, and a rule that should give no conflict | the test of a scenario that the model lists once for each of its events |

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
| `eval9/` (E15), doubtful conflicts set aside | 18 of 18 | 2 of 18, a real conflict we wrote by mistake | 18 of 36 |
| `eval10/` (E16) | 18 of 18 | 0 of 18, even counting doubtful conflicts | 7 of 36 |
| `eval12/` (E18), conflicts said in other words; with the questions about two outcomes | 34 of 36 (27 without them) | 3 of 18 (0 without them) | 16 of 36 |

Some notes on these numbers:

- Assumed facts and links carry a large part of the result. Without them,
  `eval3/` gives 10 of 21.
- The questions about two outcomes were added late, and `eval12/` is the
  first set tested with them. Asked on the saved runs of `eval3/` to
  `eval10/`, they raise the planted conflicts found there from 129 to 142 of
  153. They also report conflicts that nobody planted: the clean runs with
  one go from 3 to 13 of 144 on those runs, and from 0 to 3 of 18 on
  `eval12/`. Some of these are fair findings (two rules that can apply
  together, with nothing saying which one wins), and some are artefacts of
  the single snapshot. Each one says "if the assumed facts hold" and quotes
  the fact. We kept the step on, because it gains more than it costs
  (research.md 3.13 and 4.6).
- On `eval3/` and `eval4/`, every doubtful conflict was a false alarm. On
  `eval5/` one planted conflict was marked too ("WHEN a member is suspended"
  was read as an event), so with doubtful conflicts counted, E10 finds 14 of 18.
- The second model finds about twice as many ambiguities, and raises about
  twice as many flags on clean specs (7 → 15 on `eval4/`, 5 → 9 on `eval7/`,
  in 18 runs).
- `delete_property`, the blog's second example, was found in 3 of the last 3
  runs. It was missed in 4 of 7 earlier runs, 3 times because of a wrong voted
  fact (research.md 4.3).
- Gaps are measured from `eval8/` on. A clean spec there has two
  complementary requirements, such as "... AND the slot is free" and
  "... AND the slot is taken", and its gap version has only one of them. On
  `eval8/`, `eval9/` and `eval10/` all 18 planted gaps were found, and 17 of
  18 on `eval12/`. On the clean specs, where both cases are covered, 4, 3, 5
  and 0 of 18 runs still reported a gap.
  Each time the model had made two symbols, `slot_is_free` and
  `slot_is_taken`, and for Z3 a slot can then be neither. The doubtful mark
  caught 2 of 13 such gaps in the runs made with it (research.md 4.2).
- All these specs have at most six requirements. To see what a longer document
  does, we wrote one spec of 30 requirements (`experiments/sets/size`) and one
  of 100 (`experiments/sets/size2`), each with three defect versions. Both
  went as well as the small ones: the planted conflicts were found in 6 of 6
  runs and the planted gap in 3 of 3. The clean version of the long one gave
  one false alarm in 3 runs, and its solver stage takes 35 seconds instead of
  under one. The optional second model, tried once on the long one, flagged
  9 of the 100 rules of the clean version as ambiguous, where the main model
  alone flags 2 (research.md 4.4). Two documents are a first sign, not a
  measurement.
- The samples are drawn at temperature 0.7. At 0.3 and 0.5, on `eval8/`, the
  conflicts and gaps did not change, and fewer ambiguities of "only" were
  found (T17), so 0.7 stays.
- The check of a change was tested on `eval11/` (E17): six OpenSpec projects,
  each with five changes. One change is harmless, two clash with an existing
  scenario (a new requirement, and a rewritten one), and two leave a case
  open (a new requirement with one of its two cases, and a rewritten one that
  lost a scenario). In 90 runs all 36 planted conflicts and all 36 planted
  gaps were found, and nothing was reported about the harmless changes. The
  reports left out 174 findings about the existing requirements alone. The
  planted conflicts were worded to be easy to find ("opens the gate" against
  "does not open the gate"), because this set tests the merge and the
  selection of findings; one of them was marked doubtful in 3 of 3 runs.
- What a change removes was tested on `eval13/` (E19): six more projects with
  six changes each. A change that removes the requirement for one of two
  cases got its gap, reported as opened by the change, in 18 of 18 runs. A
  change that removes the only requirement for an event got none, in 18 of
  18. Every project also has one conflict from before any change: it was
  found in all 108 runs and shown as the change's in none. Of the 54 runs on
  changes about which nothing should be reported, 2 showed a conflict.
- The two ways to check a change were compared on `eval14/` (E20): six more
  projects, 36 changes, each checked both ways. The full way found 54 of 54
  planted conflicts and 36 of 36 gaps, with 68 requests to the LLM for a
  change. On a saved model of the specs (`--incremental`) a change took 9
  requests, after one full run for the specs of the project. That way found
  the same 36 gaps and 50 of the 54 conflicts: two new rules were rejected
  because their translations disagreed. So `--incremental` is the cheaper
  way, and the full run is the default.
- The read prompt of `--incremental` was then changed for the rule it had
  lost (a new rule is to be read by its own words), and the two ways were
  compared again on `eval15/` (E21): six more projects and 36 changes, 12 of
  which add a rule about a property of the person or thing that an existing
  event is about. The full way found 72 of 72 planted conflicts and 18 of 18
  gaps, and so did `--incremental`, with 11 requests for a change against 68.
  With the old prompt it found 71 of 72 there. So the new prompt cost nothing
  and gained little, and the LLM still tied some new rules to a saved event.
- All those projects have 7 to 9 scenarios, and each change does one thing.
  `mixed/` (E22) is one larger project, a city marathon with 39 scenarios in
  four spec files, and one change that adds four requirements, rewrites
  three, removes two and renames one. We planted 3 conflicts and 3 gaps in
  it; its other parts must give nothing. In 3 runs each way, the full run and
  `--incremental` both found all of them and reported nothing else about the
  change (346 requests to the LLM for a run, 83 with `--incremental`). The
  report of one run is in `experiments/examples/marathon_mixed`; that run
  shows one conflict more, from a wrong link that the report quotes.
- A real project (E23, a first batch). The OpenSpec tool keeps its own specs
  in this format: 44 spec files and 108 archived changes. That is too large
  to check as one document, so each change was checked against the spec
  files it touches, as they were before it. Of 16 changes, run once:
  - 5 runs stopped: 3 because our parser read the example in a code block as
    a scenario (fixed since), 2 because the LLM made a symbol with a name
    that is not a word (".claude");
  - 147 of the 366 rules got no agreed translation (79 ambiguous, 68
    rejected). On our sets that is about 3%. The cause is the list of symbols
    that the first step makes for the whole document. A real rule demands two
    or three things, and the list does not fit: for 73 of the 147 it has
    several overlapping symbols for one outcome and the eight translations
    pick different ones; for 50 it has none, and some translations then
    demand nothing (`... => true`);
  - 45 more rules were accepted with a translation that demands nothing,
    because all eight agreed on it. So about half of the real rules gave the
    checks nothing to work with;
  - 29 conflicts were reported about a change, in 3 of the 11 changes. 26 of
    them rest on a question about two outcomes, and the 4 we read set a
    general rule against its own special case ("the legacy list command
    works as before" against "when no active changes exist, display 'No
    active changes found.'");
  - the other 3 are proven from the rules alone, and they look real: "WHEN
    `$SHELL` contains `bash` ... detect shell as `bash`" and "WHEN
    `$PSModulePath` ... is present ... detect shell as `powershell`" can both
    apply, and nothing says which wins.

  So on a real project the tool was not usable as it stood. The points
  below are what was done about it. The scripts are in `experiments/real/`,
  and the cases in `experiments/sets/real1`.
- Two remedies for that, tested on a second batch of 16 real changes
  (`real2/`) and on `eval16/`, six specs of our own written like real ones,
  each with the code before and after (E24):
  - a rule whose translation demands nothing is rejected, and the report
    lists it as "Not checked". This stays: no such rule is accepted any more;
  - a long document was read in pieces, each with the symbols so far. It gave
    the real rules their symbols, but 44% of the rules were still of no use
    to the checks, against 57% and 47% in two runs without it. More runs
    stopped (3 of 16 against 1 and 2), and our own long documents got
    conflicts that nobody planted. It was taken out again;
  - on `eval16/` what we planted is found either way (19 of 22 and 19 of 20
    conflicts, 10 of 10 gaps). 6 and 8 of its 48 runs stopped, each because
    the LLM made a value that is not a word (the status `timed out`, the
    status 201). And 96% of its rules get an agreed translation: specs we
    write are easier than real ones, also when we try to write them alike.
- A run no longer stops for such a value (E25). The LLM keeps the spelling of
  what a document gives in quotes, and our code used to refuse a symbol list
  with a name that is not a word. Now it repairs the list (`timed out`
  becomes `timed_out`, 201 becomes `answer_status_201`), without any change
  to a prompt. On `eval17/`, six more specs full of such values, 7 of 48 runs
  finished with the old code and 48 of 48 with the new one, and 22 of the 24
  planted conflicts and 10 of the 12 planted gaps were found. On the second
  real batch 16 of 16 runs finish (14 and 15 before).
- The translations of a rule now vote when they differ only in the symbols
  they use ([Ambiguities](#ambiguities)). Tested with the code before and
  after on data it was not built on (E26):
  - a third batch of 16 real changes (`real3/`), run twice each way: 54% and
    62% of the rules were of no use to the checks before, 28% and 36% after.
    The author is asked about a rule of the change half as often (45
    questions against 83);
  - half of what is left are rules for whose outcome the first step listed
    no symbol (179 of 341), which a vote cannot help;
  - with more rules in the checks, more conflicts are reported about the
    changes: 30 that are not doubtful, 23 before. Those we read set a rule
    for the normal case against a rule for a failure that can happen at the
    same time. Nothing is planted in real specs, so we cannot say how many
    are findings;
  - `eval18/`, six specs of our own with planted ambiguities, to see the
    cost: 18 of 18 planted conflicts, 18 of 18 planted gaps and 11 of 36
    planted ambiguities, the same both ways. The vote took 5 of the 36
    planted rules, and one of them was still reported. A limit worded
    "reaches 90 days" was found in none of 18 runs, either way;
  - three of the six clean specs of `eval18/` have a rule that cuts across
    the others ("WHEN the configuration names a rule that does not exist
    ... exits with code 2"), as `eval16/` had. They report a conflict in
    every clean run, with either code.
- A rule without a symbol for what it demands is read a second time
  ([Ambiguities](#ambiguities)). Tested on 13 real changes that create a
  new spec (`real4/`), each also with one conflict we planted, twice with
  the code before and after (E27):
  - the planted conflicts are found: 24 of 26 before, 22 of 26 after, and
    15 and 14 without the assumed facts and links. The two that the new code
    lost are one case, and neither of its two rules was read again;
  - the second read does little on these specs: 16% and 14% of the rules
    are of no use to the checks, against 17% and 16%, which is what two
    runs differ by. They have 14 to 31 scenarios, and only one rule in
    twenty lacked a symbol. On the longer documents it was developed on (30
    to 60 scenarios) it brings back 5 to 17 points within a run;
  - so the test we had set for it was not passed. It is kept because it
    gains within every run, no loss could be traced to it, and a second
    read that helps no rule leaves the run exactly as it was.
- What are the conflicts that nobody planted? We read 20 of the 40 that 13
  real specs got in one run (T32). None is a contradiction that the author
  would not have meant. 12 are artefacts, 8 of them in a situation that
  cannot happen: "tasks.md is read" together with "tasks.md does not
  exist", which the solver allows. 7 set a general rule against its own
  exception, which is how these specs are written. 1 is a fair question:
  two failures at once, and nothing says which error is thrown. The reading
  was done by the assistant that works on this project, not by a person.
- Since then the model is asked whether the conditions of two rules that
  clash can hold together ([How sure is a finding](#how-sure-is-a-finding)).
  Tested on six specs of ours that hold such pairs (`eval19/`) and on the
  last 8 unused real changes, each also with a conflict planted under a
  condition of its own (`real5/`); every run is scored with and without the
  answers (E28):
  - `eval19/`: clean runs with a conflict 0 of 18, against 11 without the
    question; conflicts that nobody planted 19 against 97; planted conflicts
    48 of 54 and planted gaps 18 of 18, the same both ways;
  - `real5/`: conflicts that nobody planted 56 against 63. Of the 10 pairs
    it called impossible, 7 are right ("all artifacts are completed" with
    "an artifact is blocked") and 3 are two flags of one command that a user
    can give together ("--default" and "--no-default"), which is a fair
    question and is now marked doubtful;
  - no planted conflict was called impossible, in either set;
  - a conflict planted in a real spec under a condition of its own is found
    in 10 of 16 runs, where one with a copied condition is found in 46 of
    52. Four of the 10 are marked doubtful, because the planted mode ("the
    loader runs in lenient mode") was read as an event.
- A conflict between a rule and a special case of it now says so in its
  title (T35). The solver proves the form, and no count changes. On those
  real changes it is on 22 of the 56 conflicts that nobody planted and that
  are not doubtful, mostly a command and its fallback ("... without
  arguments THEN prompt user" against "GIVEN stdin is not a TTY ... THEN do
  not prompt"). None of the conflicts in our own sets has the form. So of
  63 conflicts that a reader of those real reports had to sort, 7 are
  doubtful now, 22 carry this remark, and 34 are left as they were.
- Specs about the runs of an agent
  ([above](#specs-about-the-runs-of-an-agent)). Tested on four projects of
  ours about an assistant that calls tools, with four changes each
  (`eval20/`), twice: with the code before, and with `--whole-run
  --examples "^Example:"`. Doubtful conflicts are set aside (E29):
  - a conflict between two rules that react to two calls of one run: found
    in 0 of 12 runs before, 12 of 12 after. Before, all 12 were found and
    marked as two events at the same moment;
  - a direct conflict between two rules about one function: 12 of 12 both
    times;
  - a change that only adds examples: a conflict about it in 6 of 12 runs
    before, 0 after. With the examples read as rules it is 11 of 12;
  - a change that adds a setting named like an existing one: a conflict in
    11 of 12 runs before, 0 after. Without the second question about the
    link it is 9 of 12;
  - the price: with a whole run as the situation the question about two
    outcomes is asked of 1,530 pairs, not 74, and a change costs 87
    requests to the model, not 55.
- The tool was then run on the project of an agent system named above, and
  one of its reports showed a case that the first set did not have: an
  existing example and a new variant of it ("the same case, while one more
  thing is true"), reported as a conflict in 21 of 32 parts. Since then
  every example of a conflict must describe its situation, not one of them.
  Tested on four more projects of ours, whose changes all add examples
  (`eval21/`), each run scored both ways (E30):
  - a change that adds two variants of an existing example: a conflict
    about it in 3 of 12 runs when one example is enough, 0 of 12 now;
  - two examples of one case with opposite outcomes: found in 5 of 12 runs,
    either way. In the 7 misses "called once" and "never called" became a
    count and "the call did not succeed", which can hold together;
  - an example that breaks a rule by what it demands itself: found in 10 of
    12 runs, and plain in 4 either way. In 6 it is marked doubtful: the
    example says "succeeds once", which became a count, and the rule is
    about "a call succeeds".
- One of the reasons why a change of that project cannot be built is a
  chain of three rules, which no pair of rules shows. Since then the model
  is asked whether what one rule demands makes another rule apply. The form
  of the question was chosen on saved runs, in four rounds (T39). Tested on
  four more projects of ours with three changes each (`eval22/`), the same
  runs scored with and without the facts of that question, doubtful
  conflicts set aside (E31):
  - a contradiction that is a chain of three rules: found in 12 of 12 runs,
    and in 2 of 12 without;
  - an example that breaks a rule by what it demands itself: 12 of 12, and
    0 of 12 without. On `eval21/`, asked on its saved runs: 10 of 12, where
    it was 4;
  - a change where the demand only looks like the condition ("the card was
    verified at check-in", and a rule about calls of `verify_card`): a
    conflict about it in 1 of 12 runs either way. None of the 59 questions
    asked there was answered yes;
  - asked on the saved runs of `eval20/`, no change that should give
    nothing gets a conflict, and no planted conflict is lost.
- A run of the real project from scratch then showed a wrong step that
  none of those sets has (T41): a rule that applies in several cases ("WHEN
  a call of this tool or of that tool is made"), and the fact that the
  second is called. Of the 7 conflicts that the question added over four
  changes, 6 were artefacts. One sentence about such rules in the prompt
  changed nothing (T42). The model's reasons showed why: it took the fact
  as given and found that the rule then applies. Since then the fact is
  shown as a statement to judge. Tested on four more projects of ours that
  have such a rule (`eval23/`), the same runs asked in both forms,
  doubtful conflicts set aside (E32):
  - a change where the rule about two calls must not be taken for a rule
    about one: a conflict about it in 6 of 12 runs before, 0 of 12 after;
  - a contradiction that is a chain of three rules: found in 9 of 10 runs
    before, 10 of 10 after. In 5 of the 10 the rule about two calls was
    also set against the new rule before, in none after;
  - an example that breaks a rule: 3 of 3 both times;
  - 11 of the 36 runs stopped before the checks, the same in both forms: 9
    of the 12 runs with such an example, and 2 with a chain. The read step
    had returned the rule about two calls as two rules with one label.
- What came back in those runs is the same scenario with the same words,
  once for each of its two calls (T45). Such copies are one rule now
  ([above](#specs-about-the-runs-of-an-agent)). Tested on four more
  projects of ours, each with a rule about two calls and a rule about three
  (`eval24/`), every change run three times with the code before and after
  (E33):
  - runs that finish: 25 of 36 before, 36 of 36 after;
  - a rule that says the opposite of the rule about two calls, for its
    second call: the conflict is found in 8 of 12 runs before, 12 of 12
    after;
  - an example that breaks a rule: found and not doubtful in 6 of 12 runs
    before, 11 of 12 after;
  - a change that should give no conflict: none, either way. Each of these
    changes gets a gap about it, with either code: its second rule is the
    only one about its call, and covers one kind of run. That is how we
    wrote the set.
- That project, TestingTheAgents, each change against the 24 spec files of
  the application: the run from scratch by the commands
  [above](#a-real-project-of-that-kind-testingtheagents), with the question
  asked in its final form (T44). In brackets: the same run without the
  facts of that question.

  | Change | Conflicts, not doubtful | In the spec files of the change, with the parts that found each | With a rule of another spec file | Doubtful |
  |---|---|---|---|---|
  | `add-instant-bulk-takedown-workflow`, cannot be built | 9 (8) | 2: in 16 and 1 of 24 parts | 7 (6) | 19 |
  | `add-licence-expiry-sweep-workflow`, can be built | 3 (3) | 2: in 2 and 1 of 24 parts | 1 (1) | 32 |
  | `add-page-retirement-workflow`, can be built | 3 (2) | 0 | 3 (2) | 54 |
  | `add-scheduled-batch-republish-workflow`, can be built | 3 (3) | 0 | 3 (3) | 19 |

  - Two of the authors' four reasons are in the first report. The conflict
    found in 16 parts is the contradiction between two rules of the change.
    One of the 7 with a rule of another spec file is the missing approval:
    the existing rule that nothing goes live or down in a plan without an
    approval, against the change's rule that such a run asks nobody, "if
    the assumed facts hold", through the fact that an approved request is a
    request that was made. The question found it in two formalizations of
    two.
  - The question adds 2 conflicts over the four changes: the missing
    approval, and one on a change that can be built, which holds under one
    reading of an ambiguous rule; the report says so. Before it was put as
    a statement to judge it added 7.
  - The number of conflicts does not tell the changes apart; the number of
    parts does. The other conflicts with a rule of another spec file are
    artefacts, those we read: a wrong assumed fact between two unrelated
    happenings of one run, or an attribute of one call taken for an
    attribute of the run. They are mostly other ones in each run: the
    earlier run had 6, 5, 3 and 1 conflicts without the new question.
    Against all 33 spec files, the 9 of the project's test harness add up
    to 9 more. The doubtful ones are all marked for an example.
  - The authors' other two reasons are not found: one needs rules of three
    spec files, and one is arithmetic over the steps of a run.
- The numbers are small: the specs were written by us, there is one main
  model, and the real changes are those of one project. The details are in
  [research.md](research.md).

## Known limits

| Limit | What it means |
|---|---|
| A finding is a proof about `formal.json`, not about your intent | if the LLM mistranslates a rule, the solver proves something about the wrong formula |
| One model finds about half of the ambiguities | it is confident about readings a person would ask about. A second model finds most, and flags about one more clear rule per spec |
| An assumed fact or link can be wrong, even with a majority | the report quotes every one a conflict depends on, so you can judge |
| Some proven conflicts are artefacts of the model | two events at the same moment ("a visitor signs up" while "a subscriber changes the address"); "at least 24 hours" and "less than 24 hours" as two symbols, both true. These are marked *doubtful* |
| The *doubtful* mark needs the LLM to name the event each rule reacts to | a state taken for an event ("WHEN a member is suspended") marks a real conflict too |
| "Remove" against "keep" is still missed when "keep for N years" becomes only a number | "delete the listing" becomes a yes/no symbol, `listing_deleted`, and "keep every listing for seven years" becomes a number of years. For Z3 nothing connects the two, and the question about the two outcomes is answered "possible" as often as not (GUIDE.md, section 6.4) |
| The questions about two outcomes also report conflicts that nobody planted | "release the coat when the guest shows the token" against "list a coat as unclaimed after 30 days": in one snapshot a coat collected late falls under both. No mark catches this kind yet. On a long spec only the first 40 pairs of rules are asked about |
| Gaps depend on the symbols, and on the events the LLM marks | "free" and "taken" as two symbols give a false gap, and it is rarely marked doubtful. The gap in which no event happens, which almost every spec has, is marked as such and is rarely something to fix |
| One snapshot, no time | "then", "after" and "until" are not modelled |
| A reworded scenario is the change's, whatever its new words are | if its old words gave the same finding, the finding is still shown as the change's |
| Real specs are harder than the ones we wrote | on real changes one rule in six to one in four gets no agreed translation or one that demands nothing, the more the longer the document, because the symbols of the first step do not fit rules that demand several things. A whole real project is also too large to check at once: a change is checked against the spec files it touches |
| On real specs, most conflicts that nobody planted are not contradictions | of 20 that we read, 8 are in a situation that cannot happen (two conditions that exclude each other by their meaning, which the solver lets hold together), 4 are other artefacts, 7 set a general rule against its own exception, and 1 is a fair question. The question about two conditions marks one conflict in six to nine as doubtful, and one in three to six says that it is a rule against a special case of it; about half are still reported with no mark |
| The question about two conditions also doubts real conflicts | in the order example above, a run made today marks R1 against R5 as doubtful: "An order that has been canceled and refunded cannot currently be an active submitted order with available inventory." The Kiro blog reports that conflict. And it calls two flags of one command impossible ("--default" and "--no-default"), where what the tool does with both is a fair question. A doubtful conflict stays in the report, with the sentence it is doubted for |
| The second read adds symbols that are about one rule | `openspec_dir_created` next to `openspec_dir_exists`. The rule can be written then, but it clashes with another rule only through the assumed facts. A rule with no usable translation at all is not read again |
| A voted translation can say less than the rule | when the eight translations differ only in their symbols, the rule is kept with what more than half of them entail. "Display success message with archived name and list of updated specs" became "the success message is displayed". `formal.json` marks such a rule (`"voted": "7/7"`), the report does not. A split that the vote settles is no longer a question to the author: on `eval18/` that happened to 5 of 36 planted ambiguities, and 1 was still found |
| With `--whole-run`, the question about two outcomes is asked of many more pairs, and errs more | it is asked of rules that react to two different happenings too. A wrong answer ("A run cannot have a maximum tool call count of 40 if no tools were called") gives a conflict between two unrelated rules. On TestingTheAgents every change got 1 to 6 such conflicts against the application's specs, each in one part, and mostly other ones in each run. In a document of 30 rules the limit of 40 pairs cuts off most of about 175 |
| The question whether a rule applies is asked 40 times for a document at most | on our sets that is enough. In a project in parts it is not: on the four changes of TestingTheAgents, 2,008 of 5,004 questions were left out. A chain of three rules is found only if its pair is among those asked about, and only across the spec files of one part |
| On real specs the question whether a rule applies still takes wrong steps | 3 of the 30 it said yes to on TestingTheAgents. Two take one refusal for another: "the job is refused", and the statement that the approver refused. One is about a statement marked FALSE: the model says that the fact is true, and then answers "yes". None of the three adds a conflict there. None on our own sets |
| A rule that reacts to either of two events has no trigger | "WHEN a call of `order_lenses` or `order_frame` is made THEN ...": the model lists it once for each event, and the copies are kept as one rule without a trigger. Where a situation is one moment, a conflict between it and a rule about another event is then not marked as two events at once. A label that comes back twice with two different texts still stops the run; that was not seen in 3,191 saved runs |
| A step from one rule to another can be right and its conflict still an artefact | "a call that is refused was made" is right. The conflict it gave on the real project has a call that succeeds in its situation, which the example excludes in words and the formulas do not: "refused" and "succeeds" are two symbols |
| Two examples of one case with opposite outcomes are missed in 7 of 12 runs | "called once" and "never called" became a count and "the call did not succeed", which can hold together (E30) |
| An attribute of one call becomes an attribute of the whole run | "the token the call was made with", "the agent that made it", "the file the function is in": two rules about two different calls then clash |
| A project in parts is checked against one other spec file at a time | a conflict that needs rules of three spec files is not found; scenarios are not looked for; a part that the model cannot read is left out (4 of 131 on the real project, all named in the reports) |
| The cheaper way to check a change reads a new rule with little around it | by default the specs are formalized again for each change, so that old and new rules share their symbols. `--incremental` avoids that. Shown only the saved symbols, the LLM sometimes ties a new rule to a saved event that the rule does not name. That cost 4 of 54 planted conflicts on `eval14/`, and none of 72 on `eval15/`, where one such rule was ambiguous in 3 of 3 runs. Either way, a project is bounded by the read step's room, about 140 scenarios |

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
| `speccheck/formalize.py` | stage 1: read, sample, cluster, vote, facts, links; several symbol sets; adding new rules to a saved formal model |
| `speccheck/probe.py` | stage 1, step 6: questions about concrete situations, about the outcomes of two rules, about the conditions of two rules that clash, and whether what one rule demands makes another apply |
| `speccheck/checks.py` | stage 2: conflicts, gaps, scenarios; which findings depend on a reading; merging several symbol sets |
| `speccheck/explain.py` | stage 3: wording, the scenario judge, the Markdown report |
| `speccheck/cli.py` | runs the three stages |
| `speccheck/change.py` | for `--change`: applies an OpenSpec change to the specs, labels the scenarios, sets apart what the change removes, selects the findings about the change; splits a large project into parts and puts their findings together |
| `speccheck/refine.py` | optional LLM review, off by default |
| `experiments/slurm/serve.sbatch`, `experiments/slurm/serve_second.sbatch` | start the vLLM servers on the cluster: the main model, the second model |
| `experiments/slurm/serve_direct.sh` | the same server for the main model, started directly on a machine with free GPUs, without the queue |
| `tests/` | 130 tests of everything that needs no LLM |
| `experiments/sets/`, `experiments/make_eval.py` | the evaluation sets `eval` to `eval10`, `eval12`, `eval16` to `eval19`, `size` and `size2`; for the change check `eval11`, `eval13`, `eval14`, `eval15`, `eval20` to `eval24`, `mixed` and `change_dev`; and the script that writes them. `real1` to `real5` are not written by it (`experiments/real/`) |
| `experiments/results/` | every experiment: the raw data (`.json`) and its tables (`.md`) |
| `experiments/evaluate.py` | runs and scores the evaluation; re-scores saved runs without a GPU |
| `experiments/real/` | the trial on a real OpenSpec project: each archived change next to the specs before it, from the git history; and the real changes with a conflict planted in them |
| `experiments/agents/` | speccheck on a real project of an agent system, TestingTheAgents: how it is run, and the script that puts its reports into one table |
| `experiments/stability.py`, `fact_threshold.py` | the earlier experiments |
| `experiments/examples/` | saved runs referred to above and in research_log.md |
| `docs/management/` | a paper and a slide deck about the project, with their LaTeX sources, the evidence files behind their numbers, two snapshots of the source they describe, and the packaged editions (`speccheck-management-*.zip`, about 60 MB each). Start with its own README |
