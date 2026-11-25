# What we found

The findings of the project, each with its numbers. The full record (every
experiment and trial, all tables, the exact prompts) is in
[research_log.md](research_log.md); the codes in brackets, like (E5), point to
its entries. How each mechanism works is in [plan.md](plan.md), section 5.

---

## 1. The setting

- **Models.** One local model does all the work: `Qwen/Qwen3.8-27B-FP8` on
  vLLM, on 2 GPUs. Only the optional second reader (3.8) uses a second local
  model, `thelamapi/next-70b` (Llama architecture, 70B, run in 8 bits).
- **Development specs** (`specs/`). The prompts were developed on three small
  specs: `order` (Kiro EARS, the blog's 2 conflicts), `auth_openspec` (a login
  spec in OpenSpec format, 2 conflicts planted by us) and `delete_property`
  (Kiro EARS, the blog's "remove the record" against "retain the record").
- **Evaluation sets** (`experiments/sets/`). Each set has 6 specs in new
  domains, each in a clean version and in versions with one planted defect, so
  the right answer is known. A set was written before a design change and used
  once as a held-out test. After its results were read it became development
  data, and all of them are development data now.

  | Set | Versions | Planted | Held-out in |
  |---|---|---|---|
  | `eval/` | 21 | 16 conflicts, 3 ambiguities | E4, E5 |
  | `eval2/` | 30 | 12 conflicts, 12 ambiguities | E7 |
  | `eval3/` to `eval7/` | 24 each | 6 or 7 conflicts and 12 ambiguities each | E8 to E12 |
  | `eval8/` | 30 | 7 conflicts, 12 ambiguities, 6 gaps | E13 |
  | `eval9/` | 30 | 6 conflicts, 12 ambiguities, 6 gaps | E15 |
  | `eval10/` | 30 | 6 conflicts, 12 ambiguities, 6 gaps | E16 |
  | `eval11/` | 30 changes on 6 OpenSpec projects (2.4) | 12 conflicts, 12 gaps | E17 |
  | `eval12/` | 36 | 12 conflicts said in other words, 12 ambiguities, 6 gaps | E18 |
  | `eval13/` | 36 changes on 6 OpenSpec projects, with removals (2.4) | 6 conflicts, 12 gaps; 1 old conflict in each project | E19 |
  | `eval14/` | 36 changes on 6 OpenSpec projects, run both ways (2.4) | 18 conflicts, 12 gaps | E20 |
  | `eval15/` | 36 changes on 6 OpenSpec projects, run both ways; new rules about a property of what an existing event is about (2.4) | 24 conflicts, 6 gaps | E21 |
  | `size/` | 4 versions of one spec of 30 requirements | 2 conflicts, 1 gap | E13 |
  | `size2/` | 4 versions of one spec of 100 requirements | 2 conflicts, 1 gap | E14 (not held-out: no design was tuned on it) |

- **A run** is the pipeline once on one spec version. The LLM answers
  differently each time, so every version is run 3 times, and every number
  below counts runs.

---

## 2. What works

### 2.1 It reproduces Kiro's solver findings on Kiro's own example

The order spec gives the blog's two conflicts and its gap in every run we made
(190 of 190, E1 to E3, E5, T8, T10 to T12).

### 2.2 It finds planted conflicts on specs it was not built on

| Held-out test | Planted conflicts found | Clean runs with a false alarm |
|---|---|---|
| E5, `eval/` | 44 of 48 (92%) | 0 of 18 |
| E7, `eval2/` | 31 of 36 (86%) | 0 of 18 |
| E8, `eval3/` | 15 of 21 (71%) | 1 of 18 |
| E9, `eval4/` | 21 of 21 (100%) | 0 of 18 |
| E10, `eval5/` | 11 of 18 (61%) | 0 of 18 |
| E11, `eval6/` | 15 of 18 (83%) | 0 of 18 |
| E12, `eval7/` | 13 of 18 (72%) | 0 of 18 |
| E13, `eval8/` | 18 of 21 (86%) | 0 of 18 |
| E15, `eval9/` | 18 of 18 (100%) | 2 of 18, a real conflict we wrote by mistake |
| E16, `eval10/` | 18 of 18 (100%) | 0 of 18 |
| E18, `eval12/`, all conflicts said in other words; with the questions about outcomes (3.13) | 34 of 36 (94%) | 3 of 18 |

From E8 on, conflicts marked doubtful (3.7) are set aside. Counted, they give
false alarms in 9, 6, 11, 8, 0, 4, 5 and 0 of 18 clean runs (E8 to E13, E15, E16). In
E10 the mark also hit a planted conflict (4.2); counted, E10 finds 14 of 18.
The 2 runs of E15 found a conflict in `shelter_clean` that is real: an animal
adopted after 90 days in the shelter must be removed from the website and
featured on its home page.

Since E18 the pipeline also asks about pairs of outcomes (3.13). Added to the
saved runs of E8 to E16, that check raises their sum from 129 to 142 of 153
planted conflicts, and the clean runs with a false alarm from 3 to 13 of 144
(T22, 4.6).

### 2.3 Both examples of the Kiro blog are found by the solver

Kiro finds `delete_property` with an LLM stage, not with its solver (C1). Ours
found it in 1 of 40 runs, then in 8 of 8 after the links step (3.3, E5), in 3
of 7 after a change to the read prompt (4.3), and in 3 of 3 in the last runs
(T11).

### 2.4 It checks a change against the specs that already exist (T21, E17, T23, E19, T24, E20, T25, E21)

In an OpenSpec project the specs say what the system does today, and a
*change* holds only what is added, modified or removed. With `--change`, our
code applies the change to the specs and labels every scenario in the merged
document; the pipeline formalizes that document as it is, with no change to
the prompts; and our code keeps the findings that involve an added or
modified rule (plan.md 5.10). What the change removes stays in that document
under labels of its own, is taken out before the checks, and serves one more
question to Z3: is the situation this removed rule was written for still
covered?

On the held-out `eval11/`, six projects with five changes each (E17):

| | Found |
|---|---|
| planted conflicts, an added requirement against an existing scenario | 18 of 18 |
| planted conflicts, a rewritten requirement against a scenario in another spec file | 18 of 18 (15 with doubtful ones set aside) |
| planted gaps, an added requirement that covers one of two cases | 18 of 18 |
| planted gaps, a requirement rewritten without one of its two scenarios | 18 of 18 |
| clean changes with a conflict or a false gap reported about them | 0 of 18 |

- **The labels came back as rule ids in every run**, 159 of 159 (T21, E17).
  The check depends on that, and it needed no new prompt: the read prompt
  already said to use a document's own labels.
- **Everything shown was planted.** Of 246 findings in the 90 runs, 72 were
  about the change, and they are the 72 planted ones. The 174 others (171
  gaps and 3 ambiguities among the existing requirements) were left out.
- **It is not a harder test of finding conflicts.** The planted conflicts
  negate an existing outcome in its own words, on purpose: the set tests the
  merge and the selection. What 4.2 says about the choice of symbols holds
  for changes too. One planted conflict was marked doubtful in 3 of 3 runs,
  because "WHEN the projector of a hall is out of order" was read as an
  event (4.2).
- **On old specs turned into changes** (development data, T21): 12 of 12
  planted conflicts, 18 of 18 gaps, 13 of 36 ambiguities.

On the held-out `eval13/`, six projects with six changes each, and one
conflict that every project has before any change (E19):

| | Result |
|---|---|
| planted gaps, the requirement for one of two cases is removed | 18 of 18, each reported as opened by the change |
| planted gaps, one of two scenarios is dropped from a rewritten requirement | 17 of 18 |
| a change that removes the only requirement for an event: gaps reported | 0 of 18 |
| planted conflicts, a rewritten requirement against a scenario in the other spec file | 18 of 18 (15 with doubtful ones set aside) |
| the old conflict, shown as the change's | 0 of 108 |
| the old conflict, found and left out | 108 of 108 |
| changes about which nothing may be reported: with a gap, with a conflict | 0 of 54, 2 of 54 |

- **A gap that a removal opens is now the change's.** Before, it was found
  and left among the other findings.
- **An old conflict is not blamed on a change that rewrites a neighbouring
  scenario.** Inside a rewritten requirement, a scenario with the same words
  counts as existing (T21 had shown such a conflict in 2 runs).
- **The 2 conflicts on quiet changes** come from a question about two
  outcomes (3.13) on a scenario whose words did change; the one missed gap
  is a translation that lost a condition (E19).

**A change can be checked without formalizing all the specs again** (T24,
E20, T25, E21). With `--incremental` the specs that exist are formalized once
and the model is saved; for a change only its new scenarios are formalized,
and the read step is shown the saved symbols and told to use them. It was
compared with the full run on two held-out sets, 36 changes each:

| | `eval14/`: the full run | `eval14/`: on a saved model | `eval15/`: the full run | `eval15/`: on a saved model |
|---|---|---|---|---|
| planted conflicts found | 54 of 54 | 50 of 54 | 72 of 72 | 72 of 72 |
| planted gaps found | 36 of 36 | 36 of 36 | 18 of 18 | 18 of 18 |
| clean changes with a finding about them | 0 of 18 | 0 of 18 | 0 of 18 | 0 of 18 |
| requests to the LLM for a change, on average | 68 | 9 | 68 | 11 |
| tokens read / written for a change | 32,431 / 28,806 | 4,934 / 3,816 | 31,516 / 27,972 | 5,791 / 4,604 |

- **It costs a sixth to a seventh for a change**, after one full run for the
  specs of the project (about 60 requests). A change that only removes asks
  the LLM nothing.
- **On `eval14/` it found less**, 50 of 54. No miss came from a new symbol
  where an old one was meant. Three misses were one rule: shown the saved
  symbols, the read step tied "WHEN a person is younger than 17 THEN ..." to
  the saved event "a person registers", as its trigger and in the description
  of its new symbol ("the age of the person attempting to register"). The
  translations then disagreed on whether the event belongs to the condition,
  and the rule was rejected.
- **One change to the read prompt** followed (T25): a rule is read by its own
  words, a listed event is its trigger only when the rule names it, and a new
  symbol is described by the fact alone. On the development sets the
  saved-model way then found 54 of 54 (`eval14/`) and 36 of 36 (`eval11/`,
  35 before).
- **On `eval15/`**, written for this case and run after the change, it found
  what the full run found. With the old sentence it found 71 of 72 there, so
  the change gained one conflict and lost nothing, and it stays. It did not
  remove the cause: the read step tied a new rule to a saved event as often
  with it as without (4.5).
- It is still an option. On one held-out set it found less than the full
  run, on the other the same.

---

## 3. What makes it work

The solver sees symbols, not words. Each mechanism below repairs one way in
which the LLM's translation into logic can go wrong, and each was measured.

### 3.1 Sampling each rule 8 times finds ambiguity, not conflicts (E1, T17)

Conflicts are found as often with 1 translation per rule as with 8, because
all samples of a rule use the same symbols. What the 8 samples show is
disagreement: "the number of failed attempts reaches 5" split into "exactly 5"
and "5 or more", which nobody had planted.

The samples are drawn at temperature 0.7. On `eval8/` at 0.3, 0.5 and 0.7,
conflicts (18 of 21), gaps (18 of 18) and false alarms (none, doubtful ones
set aside) did not change at all (T17). Planted ambiguities were 13, 14 and 14
of 36, but two runs at 0.7 gave 14 and 20, so most of that is noise. The one
clear effect: ambiguities of "only", which show up when the 8 translations
split, fell from 8 of 9 at 0.7 to 3 of 9 at 0.3. The temperature stays 0.7.

### 3.2 Assumed facts help, but only if they can never remove a finding (T1, E2)

- Used as truths, a wrong fact hid a real conflict: 7 of 8 samples agreed that
  "an order cannot be both fulfilled and canceled", which is a business rule,
  and one of the order spec's conflicts disappeared (T1).
- Used only to add findings, in 240 runs no finding was lost and no wrong one
  added (E2).
- The vote is needed: keeping every stated fact gives wrong conflicts in 9 of
  90 runs (E2).

### 3.3 Links: a rule in the other rules' terms (T5, E5)

Asked to say "remove the Property record" with only the symbols of the other
rules, the model answers "not kept in the database" in 7 to 8 of 8 samples
(T5). When the same model chose the symbols, it had described "removed" as
"removed from the active data set", which agrees with keeping the record, in
40 of 40 runs (E3). The question decides the reading. `delete_property` went
from 1 of 40 runs to 8 of 8 (E5).

### 3.4 Facts and links carry a large part of the result (E5, E7 to E9, E12, E13)

The same runs, scored without and with them: 27 → 44 of 48 (`eval/`),
18 → 31 of 36 (`eval2/`), 10 → 15 of 21 (`eval3/`), 18 → 21 of 21 (`eval4/`),
3 → 13 of 18 (`eval7/`), 9 → 18 of 21 (`eval8/`).

### 3.5 Several symbol sets tell how sure a finding is (E4, E5)

With 3 symbol sets on `eval/`, what most sets found was never wrong (43 of 48,
no unexpected conflict), and what any set found missed nothing (48 of 48),
with a few false alarms.

### 3.6 Questions about one concrete situation (T6, T7, E7 to E9)

- Checking links rejected 15 of 60 links on `eval2/`: unexpected conflicts
  6 → 3, at the cost of one planted conflict (32 → 31) (E7).
- Checking readings is a dial, not a fix: it halves the flags on clear rules
  and finds fewer ambiguities (4.1).

### 3.7 Doubtful conflicts are marked, not removed (E6, E8, E9, E10)

- **Two events at the same moment.** The mark went on 48 conflicts on `eval3/`
  and 28 on `eval4/`, all false alarms, and on no planted conflict (E8, E9).
- **It needs to know the event each rule reacts to.** Since the read step names
  each rule's trigger, counted failures ("a PIN check fails for the third
  time") get their event in 72 of 72 runs, and all their false conflicts are
  marked (E10).
- **A situation the assumed facts call impossible** gave 12 more marks on
  `eval3/`, all on false alarms (E8). On `eval/` it also hit 2 planted
  conflicts (E6), which is why doubtful conflicts are marked and not dropped.

### 3.8 A second reader finds most ambiguities (T9, E9, T13, E12)

A model of another family translates every rule 8 times too, and the
translation stands only if more than half of its answers mean the same.

- **Held-out:** 14 → 30 of 36 planted ambiguities on `eval4/` (E9), 17 → 32 of
  36 on `eval7/` (E12).
- **Why it works:** on ambiguous words its own 8 answers split. They had no
  majority on 15 of 33 planted ambiguous rules, and on 34 of 321 other rules
  (T9).
- **Its price:** flags on clean specs went from 7 to 15 (E9) and from 5 to 9
  (E12), in 18 runs.
- **Fewer flags, same finds (T13).** Comparing the two readings only where the
  events of the rule's condition happen cut the clean-spec flags on the saved
  E9 runs from 21 to 15, and lost nothing.

### 3.9 A finding says when it depends on an ambiguous rule (T15)

Each ambiguous rule is tried once more with its other reading, by the solver
alone, and a conflict or gap that is gone with it says so. On the saved runs of
`eval2/` to `eval7/`, of 186 flags with two readings, the other reading changes
a conflict in 15, only a gap in 48, and nothing in 123. No finding is added or
removed.

### 3.10 Gaps are asked once for each event (D8, E13)

A search over all situations returns variations of "nothing happens". Asked
once for each event instead, on the same runs of `eval8/`:

- **Planted gaps:** 0 of 18 found before, 18 of 18 after. The gap planted in
  the 30-requirement spec: 0 of 3 and 3 of 3.
- **False gaps:** 4 of 18 clean runs, when "the slot is free" and "the slot is
  taken" became two symbols (4.2). Since T20 a gap that the assumed facts rule
  out is marked doubtful, as conflicts are, but that rarely happens (4.2).
- **Other gaps on clean specs:** 21 in 18 runs, all cases that the specs do
  leave open. 6 of them were cases we had left out without noticing.

### 3.11 Rules that share no symbol are not tried together (D8, E13)

Such rules cannot contradict each other, so the conflict search skips them.
The 1054 conflicts of the saved models do not change. The 30-requirement spec
falls into 16 to 18 families of rules, and its solver stage went from 26 to 34
s down to 0.4 to 0.9 s. It also gave 6 of 6 planted conflicts, no conflict on
the clean version (doubtful ones set aside), and the right number of
requirements in every run. One spec is thin evidence: in a document whose rules
all meet in a few symbols, nothing is saved.

### 3.12 A document of 100 requirements works, with a longer read answer (E14)

The read step writes every requirement and every symbol into one answer. For
100 requirements that answer is 16,799 tokens, about 170 per requirement, and
with the old limit of 8192 it was cut off, so every run would have failed.
With a limit of 24576 (room for about 140 requirements in the server's window
of 32,768 tokens), all 12 runs read the right number of requirements, with
about 206 symbols:

- planted conflicts 6 of 6, the planted gap 3 of 3, no false gap on the 20
  covered events;
- one false alarm in 3 clean runs, not marked doubtful: "reserve a seat"
  against "release a seat unpaid for 30 minutes", one seat symbol for all
  seats in one snapshot;
- one rule rejected in every run, a sentence we wrote unclearly ("has not
  checked in 30 minutes before departure");
- the solver stage takes 35 s per model, a full run with the wording about 10
  minutes.

### 3.13 A question about two outcomes finds conflicts said in other words (T22, E18)

Of the 153 planted conflicts of E8 to E16, 21 were missed. In 13 of them the
two rules demand opposite things with two different symbols ("take the price"
as `payment_taken`, "refuse all payments" as `payment_refused`), and no
assumed fact connects the two. The open question of step 4, "which facts
connect these symbols?", often does not mention the pair that matters.

Check 4 of step 6 asks about exactly those pairs. For two rules that can
apply together, do not react to two different events, and demand things that
share no symbol, the model is asked 8 times whether both outcomes can hold in
one snapshot. It sees the two outcomes only, not the requirements. If more
than half of the answers say "impossible", that is one more assumed fact, and
Z3 proves the conflict with it.

| | Without the check | With it |
|---|---|---|
| the saved runs of E8 to E16, doubtful conflicts set aside (T22) | 129 of 153 | 142 of 153 |
| held-out `eval12/`, all 12 conflicts said in other words (E18) | 27 of 36 | 34 of 36 |

- **What it recovers:** 13 of the 21 old misses and 7 of the 9 on `eval12/`,
  among them retention periods ("delete the token record" against "keep
  every token record for two years").
- **What it asks:** 2 to 4 pairs for a spec of six rules; 9% (T22) and 14%
  (E18) of the pairs were called impossible.
- **Its price** is more conflicts that nobody planted (4.6).

---

## 4. What does not work yet

### 4.1 Ambiguity: finding them costs flags on clear rules (E4 to E9, T7, T9, T13)

Planted ambiguities on the held-out `eval4/` (E9), 9 per kind:

| | Sampling only | Questions (default) | Questions, 7 of 8 | Second reader (with T13) |
|---|---|---|---|---|
| a boundary ("after", "three times") | 2 | 3 | 3 | 6 |
| what an "and" / "or" covers | 4 | 4 | 6 | 6 |
| what an "only" covers | 9 | 5 | 5 | 9 |
| what an "if" covers | 4 | 2 | 2 | 9 |
| **all, of 36** | **19** | **14** | **16** | **30** |
| flags on rules of clean specs (18 runs) | 12 | 7 | 18 | 15 |
| flags on other rules where nothing was planted | 44 | 22 | 62 | 59 |

- **One model is confident** where a reader is not, whatever it is asked (T7).
- **A second model** finds most planted ambiguities, at about one flag per clean
  spec. Some of those flags may be real ambiguities that nobody planted; there
  is no ground truth for them.
- **A setting tuned on development data did not hold:** "7 of 8" gave 27 of 36
  there (T8), and 16 of 36 here.
- **It depends on the set.** One model found 14 to 20 of 36 on `eval4/` to
  `eval9/`, but 7 of 36 on `eval10/` (E16), where the 8 translations agreed on
  all 9 planted "if" rules.

### 4.2 The choice of symbols is still the fragile step (E1 to E3, E10 to E13, E16, E18, T10, T12, T14, T20, T22)

- With symbols drawn again on every run, the login spec's conflicts are found
  in 3 to 9 of 10 runs instead of 10 of 10 (E1 to E3).
- **A state can be read as an event.** "WHEN a member is suspended" got the
  event `member_suspended`, so its planted conflict looked like two events at
  once and was marked doubtful in 3 of 3 runs (E10). A prompt sentence did not
  change that (T12). It was the exception: on `eval6/`, four other states
  after WHEN were read as states in 12 of 12 runs (E11).
- **A prompt change can break an old result.** Two changes to the read prompt
  broke `delete_property` (4.3, T10), so the development specs are now run
  after every prompt change.
- **Two symbols for one thing.** "Take the price" (`payment_taken`) against
  "refuse all payments" (`payment_refused`) was missed in 3 of 3 runs (E12).
  The questions about outcomes now find it, in 3 of 3 of the same runs (3.13).
- **Two symbols for two complementary conditions give false gaps** ("the
  slot is free" / "taken", "the car passes" / "fails"): in 3 to 5 of 18 clean
  runs per set (E13, E15, E16). To Z3 the slot can be neither. A gap that the
  facts rule out is marked doubtful, but the model rarely votes the fact that
  one of the two always holds: 2 of the 13 false gaps in T20 and E16 were
  marked. For some pairs it is right not to (a payment can also be pending).
  Left as a known limit.
- **"Remove" against "keep" is found in 10 of 21 runs** (E10 to E13): 3 of 3 in
  `backup`, `lab` and `skipass`, 1 of 3 in `photos`, 0 of 3 in `messages`,
  `auctions` and `clinic`. When it is missed, the link read "remove" in
  another way that the words allow ("removes the message" as "not
  delivered", E10); or "keep for seven years" became a number,
  `listing_retention_years = 7`, that nothing clashes with (E11, E12); or the
  translations of the "keep" rule scattered and it was rejected (E13). A
  prompt sentence calling "remove" and "keep" opposites made it worse and was
  dropped (T14). With the questions about outcomes it is 13 of 21 on the same
  runs (T22), and 4 of 6 runs for the two retention conflicts of `eval12/`
  (E18). A retention period that became only a number is still hit or miss:
  "the payslips are deleted" together with `payslip_retention_years = 10` was
  called impossible by 8 of 8 answers in one run and by 4 of 8 in another.

### 4.3 Wrong facts and links exist (T6, T8, T10, E9)

- A majority can agree on something wrong: a wrong link passed 7 to 1 in a
  development run (T6).
- **A wrong fact can hide a conflict, although facts are add-only.** In
  `delete_property`, "a deleted property has its record removed" made D4
  impossible to obey, and a conflict needs two rules, not one rule against the
  facts. The conflict was found in 3 of 7 runs (T8). Facts that make a
  requirement impossible to obey are now checked against its words; on the
  three saved failing runs this recovered the conflict once (T10).
- A wrong fact can also make a conflict (`printing_overlap`, E9).

### 4.4 Not measured

- **Scenarios** have no ground truth. **Gaps** have one only since `eval8/`,
  for one kind of planted gap.
- **Conflicts of three rules** are searched, but the one planted case is also
  found through a pair.
- **The plain-language wording** was checked by hand only (L9). On a long
  spec it buries a gap: each lists every other event as FALSE, about 70 lines
  at 100 requirements (E14).
- **The second reader on a long spec** was run once (T26). It could not run
  in E14, because every request kept 4,096 tokens for an answer that needs
  about 200; with 1,024 it fits its server's window. On one run of each
  version of the spec of 100 requirements it raised 9 ambiguity flags on the
  clean version, where the main model alone raises 2, and none of the 100
  rules has a planted ambiguity.

### 4.5 The limits of the change check (T21, E17, T23, E19, E20, E21)

- **By default every change is a full run.** The merged spec is formalized
  again each time, so that old and new rules share their symbols. The saved
  model of `--incremental` avoids that. It found 4 of 54 conflicts less than
  the full run on `eval14/`, and the same 72 of 72 on `eval15/` (2.4).
- **A new rule read next to the saved symbols is tied to a saved event more
  often than its words justify.** The sentences added to the read prompt
  (T25) cured the case they were written on and no other. On `eval15/`, with
  them as without (E21):
  - a saved event became the trigger of a rule about a state in 6 of 36
    cases ("WHEN an observing session is held in the lecture room THEN ..."
    got "a guide starts an observing session");
  - a new symbol was described through a saved event in 3 of 3 runs of one
    case ("the number of items in the order being collected"; the full run
    wrote "the number of items in the order"). The translations of that rule
    then split, and it was ambiguous in 3 of 3 runs, against 1 of 3 in the
    full run.

  No conflict was lost to this on `eval15/`. On `eval14/` it cost 3 (E20).
- **The specs of a project must fit one read answer**, about 140 scenarios
  (3.12), also for the saved model.
- **The saved model lasts until the specs change.** Archiving a change
  changes them, and the next check then pays one full run again. So
  `--incremental` saves work for several changes against the same specs, or
  for one change checked many times, not for a single check after every
  archive. Carrying the model of the archived change over is not built.
- **A scenario with new words is the change's, whatever the words are.** If
  its old words gave the same finding, the finding is still shown as the
  change's (2 runs of E19).
- **Removed rules are asked about, not compared.** For a removed rule Z3 is
  asked whether its own situation is still covered. A removed rule that was
  rejected (its translations scattered) cannot be asked about, and removing
  a rule that reacted to no event (a state) is never reported.
- **No real project.** The 12 projects are small and written by us.

### 4.6 The questions about outcomes also report conflicts that nobody planted (T22, E18)

With check 4 (3.13), the clean runs with a conflict that was not planted went
from 3 to 13 of 144 on the saved runs of E8 to E16, and from 0 to 3 of 18 on
`eval12/` (doubtful conflicts set aside). Over all versions such conflicts
went from 32 to 88, and from 1 to 28. They are of three kinds:

- **Two rules that really can apply together, with nothing saying which one
  wins.** "Start the selected program" against "stop all brushes" when the
  emergency button is pressed. 7 of the 10 new clean runs of T22 are of this
  kind; the tool is right, and the spec is not as clean as we thought.
- **The planted rule also clashes with a third rule.** "Refuse all payments"
  clashes with "take the price", as planted, and with "add the top-up to the
  balance" too (20 of the 56 added conflicts of T22).
- **Artefacts of the one snapshot.** "Release the coat when the guest shows
  the token" against "add a coat to the list of unclaimed coats after 30
  days": a coat collected late falls under both, and 8 of 8 answers say that
  a coat cannot be released and on that list at once. Over time there is no
  clash. This one pair gives 24 of the 27 added conflicts of `eval12/`, and
  all 3 of its clean runs with a conflict.

Each of these conflicts says "if the assumed facts hold" and quotes the fact,
so a reader can judge it. Two more limits: an outcome that is not one definite
state ("a payslip younger than ten years is retained") is not asked about;
and at most 40 pairs are asked about, while the specs of 30 and 100
requirements have several hundred.

### 4.7 The evaluation is small

Eleven sets with 66 base specs (297 versions), two longer specs and twenty-four OpenSpec
projects with 138 changes, all written by us; 63 to 90 runs per experiment; one main model. One leak is known: an
example in the read prompt came from the domain of an `eval3/` spec (D4). And
one clean spec, `shelter_clean` in `eval9/`, has a conflict we did not plan
(E15).

The runs of one spec mostly agree, so the numbers rest on fewer cases than
they seem to: of the 79 planted conflicts of the ten held-out tests, 64 were
found in all 3 of their runs, 7 in none, and only 8 in some (T15, E13, E15,
E16).

---

## 5. What we tried and dropped

| Tried | What happened | Entry |
|---|---|---|
| Facts as hard truths | a wrong fact with 7 of 8 votes hid a real conflict | T1 |
| The model's "thinking" mode for choosing symbols | one call spent 109 s and all its tokens on reasoning and never answered | T2 |
| Telling the model to read each requirement literally | the symbol descriptions did not change | T3 |
| Keeping facts that only a few samples state | wrong conflicts in up to 10 of 30 runs | E3 |
| Asking "could a developer take the words the other way?" | the model said yes to nearly every reading: flags on every clean run | T7 |
| Read-prompt sentences about events and states | each moved something else: a planted conflict lost (T8), the blog's conflict marked doubtful (T10), or no change (T12) | T8, T10, T12 |
| A read-prompt sentence: "remove" and "keep" are opposites | the "keep" rules' translations scattered and were rejected in 6 of 6 runs; nothing found | T14 |
| Other thresholds for the second reader | they only trade flags for finds | T9, T13 |
| Setting aside wrong facts in other ways | at most 1 of 7 runs recovered, with 9 to 12 more unexpected conflicts on `eval3/` | T10 |
| An LLM review of the text (Kiro's "refinement") | finds `delete_property` in 40 of 40 runs, misses two conflicts the solver finds. Built, then switched off by decision: the project is about the formal check | T4, E3, D1 |

---

## 6. The experiments

Every experiment file in `experiments/results/` holds the formalizations and
the prompts, so it can be scored again without a GPU.

| | What | Size | Main result |
|---|---|---|---|
| E1 | The same spec many times, 4 settings | 120 runs | Sampling finds ambiguity, not conflicts (3.1) |
| E2 | Add-only facts (two rounds) | 240 runs | No finding lost, none wrong (3.2) |
| E3 | The solver next to an LLM review | 120 runs | Each misses what the other finds (5) |
| E4 | `eval/`, before links | 63 runs | 35 of 48 conflicts, no false alarm on clean specs |
| E5 | `eval/` and the development specs, with links | 87 runs | 44 of 48; `delete_property` 8 of 8 (2.2, 3.3) |
| E6 | `eval/` with questions | 63 runs | Ambiguities 2 → 5 of 9 |
| E7 | `eval2/`, held-out | 90 runs | 31 of 36 conflicts, 0 false alarms on clean specs (2.2) |
| E8 | `eval3/`, held-out | 72 runs | 15 of 21 conflicts; the two-event mark (3.7) |
| E9 | `eval4/`, held-out, with counted events and the second reader | 72 runs | 21 of 21 conflicts, 0 false alarms; ambiguities 14 → 30 of 36 with the second reader (3.8) |
| E10 | `eval5/`, held-out, with triggers and check 3 | 72 runs | 11 of 18 conflicts (14 counting doubtful ones); counted failures are events in 72 of 72 runs (3.7, 4.2) |
| E11 | `eval6/`, held-out, the design of E10 again | 72 runs | 15 of 18 conflicts; the 3 misses are "remove" against "keep" (4.2) |
| E12 | `eval7/`, held-out, with the comparison of T13 | 72 runs | 13 of 18 conflicts; ambiguities 17 → 32 of 36 with the second reader (3.8) |
| E13 | `eval8/`, held-out, with gaps asked for each event; and one spec of 30 requirements | 90 + 12 runs | 18 of 21 conflicts; planted gaps 0 → 18 of 18; the long spec 6 of 6 conflicts, solver stage 30 s → under 1 s (3.10, 3.11) |
| E14 | one spec of 100 requirements, read answer up to 24576 tokens | 12 runs | read answer 16,799 tokens; 6 of 6 conflicts, the gap 3 of 3; solver stage 35 s (3.12) |
| E15 | `eval9/`, held-out, with the parentheses repair of the facts vote (T19) | 90 runs | 18 of 18 conflicts, planted gaps 18 of 18; the repair added 17 facts, all bounds, and changed no finding (on the saved runs: 3 planted conflicts gained in one run) (2.2) |
| E16 | `eval10/`, held-out, with the doubtful mark on gaps (T20) | 90 runs | 18 of 18 conflicts and no other conflict at all; planted gaps 18 of 18; the mark set aside none of the 5 false gaps (4.2) |
| E17 | `eval11/`, held-out: 30 changes on 6 OpenSpec projects, checked against the specs that exist (T21) | 90 runs | 36 of 36 planted conflicts, 36 of 36 planted gaps, nothing else reported about a change; labels kept in 90 of 90 runs (2.4) |
| E18 | `eval12/`, held-out: conflicts said in other words, with the questions about pairs of outcomes (T22) | 108 runs | 34 of 36 conflicts (27 without the questions); 3 of 18 clean runs with a conflict that was not planted (0 without) (3.13, 4.6) |
| E19 | `eval13/`, held-out: 36 changes on 6 OpenSpec projects, with removals and an old conflict (T23) | 108 runs | gaps opened by a removal 18 of 18; the old conflict never shown as the change's; 18 of 18 conflicts, 17 of 18 gaps of a dropped scenario (2.4) |
| E20 | `eval14/`, held-out: 36 changes on 6 OpenSpec projects, each checked the full way and on a saved model of the specs (T24) | 108 + 108 runs | conflicts 54 of 54 against 50 of 54, gaps 36 of 36 both; a change costs 68 requests against 9 (2.4) |
| E21 | `eval15/`, held-out: 36 changes on 6 OpenSpec projects, checked the full way, and on a saved model with the read prompt before and after T25 | 3 x 108 runs | conflicts 72 of 72 (full), 71 and 72 of 72 (saved model, before and after); gaps 18 of 18 in all three; a change costs 68 requests against 11 (2.4) |

The trials (T1 to T26) were run on development data between these
experiments. Among the last: T17 compared temperatures 0.3, 0.5 and 0.7 (3.1);
T18 found that the first read answer, at temperature 0, was usable for all
204 specs, so the read step's retry is never needed on them; T19 found that
5.4% of the sampled facts are dropped before the vote, nearly all for a slip
in the formula (mostly missing outer parentheses) and almost never for an
invented symbol. The vote now repairs the parentheses (E15). T20 added the
typical case "one of two things is always the case" to the facts prompt and a
doubtful mark on gaps that the facts rule out (4.2, E16). T21 built the check
of an OpenSpec change on old specs turned into projects (2.4). T22 sorted the
21 conflicts missed in E8 to E16 by cause, and added the questions about
pairs of outcomes to the saved runs (3.13). T23 kept what a change removes in
the merged document, to see which gap the removal opens (2.4). T24 formalized
only the new scenarios of a change, on a saved model of the specs (2.4). T25
found why that way lost a conflict in E20, and changed the read prompt
addition (2.4, 4.5). T26 ran the second model on the spec of 100 requirements
(4.4).
research_log.md
has them in order, together with the bugs that
changed results before they were fixed (L1 to L10) and the open threats to
validity. To score a saved run again: `python -m experiments.evaluate --rescore
experiments/results/E9_eval4.json` (E4 to E14), or `python -m
experiments.stability --rescore experiments/results/E3_refine.json` (E1 to E3).
