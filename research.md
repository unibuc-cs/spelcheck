# What we found

The findings of the project, in reading order, each with its numbers. The full
record behind them (every experiment and trial, all tables, the exact prompts)
is in [research_log.md](research_log.md); the codes in brackets, like (E5),
point to its entries. How each mechanism works is in [plan.md](plan.md)
section 5; its terms are defined in section 3.

---

## 1. The setting

- **Models:** one local model does all the work, `Qwen/Qwen3.8-27B-FP8` on
  vLLM, 2 GPUs. Only the optional second reader (3.8) uses a second local
  model, `thelamapi/next-70b` (Llama architecture, 70B, run in 8 bits).
- **Development specs** (`specs/`): three small specs the prompts were developed on.

  | Spec | Format | Conflicts we expect |
  |---|---|---|
  | `order` | Kiro EARS | 2, both reported in the Kiro blog |
  | `auth_openspec` (login) | OpenSpec | 2, planted by us |
  | `delete_property` | Kiro EARS | 1, the Kiro blog's "remove the record" against "retain the record" |

- **Evaluation sets** (`experiments/sets/`): specs in new domains, each in a clean version and in
  versions with one planted defect, so the right answer is known. A set is
  *held-out* until its results are read to design something; after that it
  counts as development data, and a new set is written first.

  | Set | Specs | Planted | Held-out in | Since then |
  |---|---|---|---|---|
  | `eval/` | 6 domains, 21 versions | 16 conflicts, 3 ambiguities | E4, E5 | development data |
  | `eval2/` | 6 domains, 30 versions | 12 conflicts, 12 ambiguities | E7 | development data |
  | `eval3/` | 6 domains, 24 versions | 7 conflicts, 12 ambiguities | E8 | development data |
  | `eval4/` | 6 domains, 24 versions | 7 conflicts, 12 ambiguities | E9 | development data |
  | `eval5/` | 6 domains, 24 versions | 6 conflicts, 12 ambiguities | E10 | development data |
  | `eval6/` | 6 domains, 24 versions | 6 conflicts, 12 ambiguities | E11 | development data |
  | `eval7/` | 6 domains, 24 versions | 6 conflicts, 12 ambiguities | E12 | development data |

- **A run** = the pipeline once on one spec. The LLM gives different answers
  on different runs, so every number below is "in how many runs".

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

From E8 on, conflicts marked doubtful (3.7) are set aside. Counted, they give
false alarms in 9 (E8), 6 (E9), 11 (E10), 8 (E11) and 0 (E12) of 18 clean runs: those specs have
many events, and events cause the false alarms that the mark is for. In E10
the mark also hit a planted conflict (4.2); counted, E10 finds 14 of 18.

### 2.3 Both examples of the Kiro blog are found by the solver

The second blog example, `delete_property`, was the hard one. Kiro itself finds
it with an LLM stage, not with its solver (C1). Ours found it in 1 of 40 runs,
after the "links" step (3.3) in 8 of 8 (E5), then in 3 of 7 after a change to
the read prompt (4.3), and in 3 of 3 again in the last runs (T11).

---

## 3. What makes it work

The solver sees symbols, not words. Each mechanism below repairs one way in
which the LLM's translation into logic can go wrong, and each was measured.

### 3.1 Sampling each rule 8 times finds ambiguity, not conflicts (E1)

- Conflicts are found equally often with 1 translation per rule and with 8:
  all samples of a rule share one set of symbols, so they cannot repair it.
- What the 8 samples show is disagreement. "The number of failed attempts
  reaches 5" splits into "exactly 5" and "5 or more". Nobody planted that.

### 3.2 Assumed facts help, but only if they can never remove a finding (T1, E2)

- **As truths, a wrong fact hid a real conflict.** 7 of 8 samples agreed that
  "an order cannot be both fulfilled and canceled", a business rule, not a
  fact; with it, one of the order spec's conflicts disappeared (T1).
- **So facts are add-only:** in 240 runs no finding was lost and no wrong one
  added (E2).
- **The vote is needed too:** keeping every stated fact gives wrong conflicts
  in 9 of 90 runs (E2).

### 3.3 Links: a rule in the other rules' terms (T5, E5)

- Asked to say "remove the Property record" with the other rules' outcomes
  only, the model answers "not kept in the database" in 7 to 8 of 8 samples
  (T5). When the same model chose the symbols, it had described "removed" as
  "removed from the active data set", which agrees with keeping it, in 40 of
  40 runs (E3). **The question decides the reading.**
- `delete_property`: 1 of 40 runs before, 8 of 8 after (E5).

### 3.4 Facts and links carry a large part of the result (E5, E7 to E9, E12)

The same runs, scored without and with them: 27 → 44 of 48 (`eval/`),
18 → 31 of 36 (`eval2/`), 10 → 15 of 21 (`eval3/`), 18 → 21 of 21 (`eval4/`),
3 → 13 of 18 (`eval7/`).

### 3.5 Several symbol sets tell how sure a finding is (E4, E5)

With 3 symbol sets on `eval/`: what most sets found was never wrong (43 of 48,
no unexpected conflict); what any set found missed nothing (48 of 48), with a
few false alarms.

### 3.6 Questions about one concrete situation (T6, T7, E7 to E9)

- **Links are checked.** On `eval2/` this rejected 15 of 60 links: unexpected
  conflicts 6 → 3, at the cost of one planted conflict (32 → 31) (E7).
- **Readings are checked.** This is a dial, not a fix: it halves the flags on
  clear rules and finds fewer ambiguities (4.1).

### 3.7 Doubtful conflicts are marked, not removed (E6, E8, T8, E9)

- **Two events at the same moment.** One snapshot lets "a badge is presented"
  and "the receptionist presses the remote button" happen together. The mark
  went on 48 conflicts on `eval3/` and 28 on `eval4/`, all false alarms, and
  on no planted conflict (E8, E9).
- **It needs to know which event each rule reacts to.** In E8, "a comment
  receives its third report" became a counter, so the mark could not see the
  event, and 25 false conflicts were left. Now the read step names each rule's
  event (its trigger), and a conflict is doubtful when its clashing rules react
  to two different events. On `eval5/`, counted failures ("a PIN check fails
  for the third time") have their event in 72 of 72 runs, and all of their
  false conflicts are marked: none is left (E10).
- **A situation the assumed facts call impossible** gives 12 more marks on
  `eval3/`, all on false alarms (E8). On `eval/` it also hit 2 planted
  conflicts (E6), which is why doubtful conflicts are marked, not dropped.

### 3.8 A second reader finds most ambiguities (T9, E9, T13, E12)

One model's 8 samples agree where a reader would hesitate (4.1). A second
model, of another family, translates every rule 8 times too, and the
translation stands only if more than half of its answers mean the same
(plan.md 5.8).

- **Held-out: 14 → 30 of 36 planted ambiguities on `eval4/` (E9), 17 → 32 of
  36 on `eval7/` (E12).** "If" goes to 9 of 9 in both. On the development
  data: 18 → 28 of 36 (T9).
- **Why it works:** where the words are ambiguous, the second model
  hesitates. Its answers had no majority on 15 of 33 planted ambiguous rules,
  on 34 of 321 other rules (T9).
- **Its price:** flags on clean specs 7 → 15 (E9) and 5 → 9 (E12) in 18 runs.
- **Fewer flags, same finds (T13).** About a third of its flags on clean specs
  came from a detail: one model writes the event into a counted happening,
  the other only the count. The two readings are now compared only where the
  events the condition requires happen. On the saved E9 runs: clean-spec flags
  21 → 15, other flags 80 → 59, nothing lost. On `eval7/` the pattern did not
  occur, and nothing changed (E12).
- **A first rule** flagged only when the second model's majority reading
  differs. It added 2 of 36 (T9): it ignored exactly that hesitation.

---

## 4. What does not work yet

### 4.1 Ambiguity: finding them costs flags on clear rules (E4 to E9, T7, T9)

Planted ambiguities on the held-out `eval4/` (E9), 9 per kind:

| | Sampling only | Questions (default) | Questions, 7 of 8 | Second reader |
|---|---|---|---|---|
| a boundary ("after", "three times") | 2 | 3 | 3 | 6 |
| what an "and" / "or" covers | 4 | 4 | 6 | 6 |
| what an "only" covers | 9 | 5 | 5 | 9 |
| what an "if" covers | 4 | 2 | 2 | 9 |
| **all, of 36** | **19** | **14** | **16** | **30** |
| flags on rules of clean specs (18 runs) | 12 | 7 | 18 | 15 |
| flags on other rules where nothing was planted | 44 | 22 | 62 | 59 |

- **One model is confident** where a reader is not, whatever it is asked
  (T7). Its questions trade one error for the other.
- **A second model** finds most planted ambiguities, at about one flag per
  clean spec. Some of those flags may be real ambiguities nobody planted;
  there is no ground truth for them.
- **"7 of 8" looked best on development data** (27 of 36, T8) and gave 16 of
  36 here: a setting tuned on development data that did not hold.
- **"And" / "or"** is the weakest kind with the second reader (6 of 9 in E9,
  5 of 9 in E12).
- The second reader's flags in this table are with the comparison of T13;
  before it, 21 and 80.

### 4.2 The choice of symbols is still the fragile step (E1 to E3, T7 to T11, E9, E10)

- With symbols re-drawn on every run, the login spec's conflicts are found in
  3 to 9 of 10 runs instead of 10 of 10 (E1 to E3).
- **Events and states are read by the model, and it can err both ways.** A
  counted happening read as a state hid false alarms from the mark (E8, E9);
  that is fixed (E10, 72 of 72). The other way round is new: "WHEN a member is
  suspended THEN ... counts no vote" got the event `member_suspended`, so the
  planted conflict with "WHEN a member casts a vote" looked like two events at
  once and was marked doubtful in 3 of 3 runs (E10); a prompt sentence did not
  change that (T12). It was the exception: on `eval6/`, four other states
  after WHEN ("WHEN the station is out of order") were read as states in 12 of
  12 runs (E11). "Is recorded as late for the third time" became an event in
  5 of 12 runs (T11).
- **A prompt change can break an old result.** Each change to the read prompt
  shifted how `delete_property` is described: one made the voted facts wrong
  (4.3), another marked "the property is deleted" as an event, which made the
  blog's conflict look like two events (T10). The development specs are now
  run after every prompt change.
- **Two symbols for one outcome are not always linked:** "take the price"
  (`payment_taken`) against "refuse all payments" (`payment_refused`) was
  missed in 3 of 3 runs (E12), as "unlocks all doors" against "keeps the door
  locked" was in E8.
- A restriction can disappear inside a symbol name:
  `issue_sent_to_active_subscribers_only`, although the prompt forbids it (T7).
- Telling the model to "read literally" changed nothing (T3).

### 4.3 Wrong facts and links exist (E2, T6, T8, T10, E9, E10)

- A majority of samples can agree on something wrong. Links are checked
  (3.6), but a wrong one passed 7 to 1 in a development run (T6).
- **A wrong fact can hide a conflict, although facts are add-only.** In
  `delete_property`, "a deleted property has its record removed" made D4
  impossible to obey, and a conflict needs two rules that clash, not one rule
  against the facts: found in 3 of 7 runs (T8). Facts that make a requirement
  impossible to obey are now checked against its words (check 3). On the three
  saved failing runs it rejected the wrong fact twice, but once also a right
  one, and it kept a wrong one worded with a hedge; it recovered the conflict
  in one (T10). In E10 it never fired.
- **"Remove" against "keep" is found in 10 of 18 runs** (E10 to E12): 3 of 3
  in `backup`, `lab` and `skipass`, 1 of 3 in `photos`, 0 of 3 in `messages`
  and `auctions`. When it is missed, either the link read "remove" otherwise
  ("removes the message" as "not delivered", which the words allow, E10), or
  "keep for seven years" became a number, `listing_retention_years = 7`,
  with nothing to clash with "deleted" (E11, E12). A prompt sentence calling
  "remove" and "keep" opposites made it worse and was dropped (T14).
- A wrong fact can also make a conflict (`printing_overlap`, E9).

### 4.4 Not measured

- **Scenarios** and **gaps** have no ground truth. Scenarios read sensibly on
  the development specs ("the order is fulfilled although it was never submitted").
- **Conflicts that need three rules** are searched; the one planted case
  (`eval2/` discounts) is also found through a pair whose situation triggers
  the third rule.
- **The plain-language wording** was checked by hand only. It once described a
  situation as its opposite; making it restate the proven situation first
  fixed all 8 cases we then checked (L9).

### 4.5 The evaluation is small

Seven evaluation sets with 42 base specs (171 versions), written by us; 63
to 90 runs per experiment; one main model. Each held-out set was used once. One
leak is known: a read-prompt example came from the domain of an `eval3/` spec
(D4).

---

## 5. What we tried and dropped

| Tried | What happened | Entry |
|---|---|---|
| Facts as hard truths | A wrong fact with 7 of 8 votes hid a real conflict | T1 |
| The model's "thinking" mode for choosing symbols | One call spent 109 s and all its tokens on reasoning and never answered | T2 |
| Instructing the model to read each requirement literally | The symbol descriptions did not change | T3 |
| Keeping facts that only a few samples state | Wrong conflicts in up to 10 of 30 runs | E3 offline |
| Choosing symbols for each requirement in isolation | Withdrawn before building: it would lose the shared symbols everything else depends on | C1 |
| Asking "could a developer take the words the other way?" | The model said yes to nearly every reading: flags on every clean run | T7 |
| Replacing the translation when the answers prefer the other reading | Dropped: a 5-to-3 answer is weak evidence; the author is asked instead | T7 |
| Telling the translation step to keep the event "also when a count or a state is given" | It moved conditions into the antecedent, and a planted conflict was lost; narrowed to counts | T8 |
| Second reader: flag only when its majority reading differs | 2 more of 36; it ignores the second model's hesitation | T9 |
| For wrong facts: let the one-rule filter use only the facts of the proof | No conflict recovered; 12 more unexpected conflicts on `eval3/` | T10 |
| For wrong facts: set aside every fact that makes a rule impossible to obey | 1 run of 7 recovered; 9 more unexpected conflicts on `eval3/` | T10 |
| Naming "an attempt fails" as a happening in the read prompt | Failures got their event in 2 of 12 runs, and "the property is deleted" became an event, marking the blog's conflict doubtful | T10 |
| Two-event test on the triggers of the rule group that found the situation | A third rule in that group reacted to another event; it must be the rules that clash | T11 |
| A read-prompt sentence: a state written after WHEN has no trigger | "WHEN a member is suspended" kept its trigger in 3 of 3 runs; nothing else changed | T12 |
| A read-prompt sentence: "remove" and "keep" are opposites about one fact | The keep rules' translations scattered and were rejected in 6 of 6 runs; nothing found | T14 |
| Second reader: flag only when at most k of its 8 answers confirm | Only trades flags for finds (k = 2: 26 of 36 with 15 clean flags, against 30 with 21) | T13 |
| An LLM review of the text (Kiro's "refinement") | Finds `delete_property` in 40 of 40 runs, misses two conflicts the solver finds. **Built, then switched off by decision:** the project is about the formal check | T4, E3, D1 |

---

## 6. The experiments

Every experiment file in `experiments/results/` holds the formalizations and the
prompts, so it can be scored again without a GPU.

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
| E10 | `eval5/`, held-out, with triggers and check 3 | 72 runs | Counted failures are events in 72 of 72 runs; 0 false alarms; 11 of 18 conflicts (14 counting doubtful ones) (3.7, 4.2, 4.3) |
| E11 | `eval6/`, held-out, the design of E10 again | 72 runs | 15 of 18 conflicts, none marked; 0 false alarms; the 3 misses are "remove" against "keep" (4.3) |
| E12 | `eval7/`, held-out, with the second reader's comparison of T13 | 72 runs | 13 of 18 conflicts; 0 false alarms; ambiguities 17 → 32 of 36 with the second reader (3.8) |

The trials on development data are T8 (counted events) and T9 (the second
reader) before E9, T10 and T11 (wrong facts, triggers) before E10, T12
(dropped) before E11, and T13 (offline) and T14 (dropped) before E12. Commands: `python -m experiments.evaluate --rescore
experiments/results/E9_eval4.json` (E4 to E9) and `python -m experiments.stability
--rescore experiments/results/E3_refine.json` (E1 to E3).

---

## 7. Lessons from bugs

Each of these changed results before it was fixed.

| | What happened | Fix |
|---|---|---|
| L1 | An enum with one value made every condition on it silently true; the findings looked right by accident | Enums need two values |
| L2 | Forcing "admin and locked" contradicted "never lock administrators" alone and was reported as a conflict | A situation one rule forbids is not a conflict |
| L3 | `A => C` and `true => (A => C)` counted as two readings | Translations are compared as whole formulas |
| L4, L9 | The wording model described a FALSE fact as true | Facts are marked TRUE / FALSE; the model restates the situation first |
| L6 | Scoring by rule id failed: the model renumbers unlabelled rules | Scoring by position |
| L7 | Z3 called from several threads killed the process silently | Only LLM calls run in threads |
| L8 | With one snapshot and no time, a single rule can contradict a fact by design | A conflict that needs facts must involve two rules |
| L10 | Temperature 0 is not repeatable on a batched server | None; reported as it is |
