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

From E8 on, conflicts marked doubtful (3.7) are set aside. Counted, they give
false alarms in 9, 6, 11, 8, 0 and 4 of 18 clean runs (E8 to E13). In E10 the
mark also hit a planted conflict (4.2); counted, E10 finds 14 of 18.

### 2.3 Both examples of the Kiro blog are found by the solver

Kiro finds `delete_property` with an LLM stage, not with its solver (C1). Ours
found it in 1 of 40 runs, then in 8 of 8 after the links step (3.3, E5), in 3
of 7 after a change to the read prompt (4.3), and in 3 of 3 in the last runs
(T11).

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
  taken" became two symbols (4.2).
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

### 4.2 The choice of symbols is still the fragile step (E1 to E3, E10 to E13, T10, T12, T14)

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
  "The slot is free" and "the slot is taken" give false gaps (3.10).
- **"Remove" against "keep" is found in 10 of 21 runs** (E10 to E13): 3 of 3 in
  `backup`, `lab` and `skipass`, 1 of 3 in `photos`, 0 of 3 in `messages`,
  `auctions` and `clinic`. When it is missed, the link read "remove" in
  another way that the words allow ("removes the message" as "not
  delivered", E10); or "keep for seven years" became a number,
  `listing_retention_years = 7`, that nothing clashes with (E11, E12); or the
  translations of the "keep" rule scattered and it was rejected (E13). A
  prompt sentence calling "remove" and "keep" opposites made it worse and was
  dropped (T14).

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
- **The second reader on a long spec** cannot run as it is: with 206 symbols
  a translation prompt has 4,234 tokens, and its server allows 6,144 for
  prompt and answer, with 4,096 kept for the answer (E14).

### 4.5 The evaluation is small

Eight sets with 48 base specs (201 versions) and two longer specs, all written
by us; 63 to 90 runs per experiment; one main model. One leak is known: an
example in the read prompt came from the domain of an `eval3/` spec (D4).

The runs of one spec mostly agree, so the numbers rest on fewer cases than
they seem to: of the 67 planted conflicts of the eight held-out tests, 52 were
found in all 3 of their runs, 7 in none, and only 8 in some (T15, E13).

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

The trials (T1 to T18) were run on development data between these
experiments. Among the last: T17 compared temperatures 0.3, 0.5 and 0.7 (3.1);
T18 found that the first read answer, at temperature 0, was usable for all
204 specs, so the read step's retry is never needed on them. research_log.md
has them in order, together with the bugs that
changed results before they were fixed (L1 to L10) and the open threats to
validity. To score a saved run again: `python -m experiments.evaluate --rescore
experiments/results/E9_eval4.json` (E4 to E14), or `python -m
experiments.stability --rescore experiments/results/E3_refine.json` (E1 to E3).
