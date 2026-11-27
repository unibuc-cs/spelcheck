# Research issues, with examples

This is the list of problems we ran into while building speccheck, written
for a paper or a talk. Each entry has the same five parts:

- **The problem**, in one or two sentences.
- **An example**, taken from a real run.
- **What we did.**
- **The result**, with numbers. "Found in 12 of 12 runs" means: the same spec
  was checked 12 times, and the tool found the planted contradiction every
  time.
- **Still open**, if something is.

Three words are used all through:

- A **rule** is one requirement of a spec: "WHEN this happens THEN the
  system does that".
- The **model** is the language model. It reads the rules and writes each
  one as a formula.
- The **solver** is Z3. It gets the formulas and proves that two rules
  contradict each other, or that no rule covers a case. It never guesses.

The solver is always right about the formulas. The formulas come from the
model, and the model makes mistakes. Almost every issue below is one kind of
such a mistake.

The code in brackets at the end of an entry (E18, T39, ...) is the
experiment in [research_log.md](research_log.md) that has the details. The
specs we wrote ourselves are in `experiments/sets/`.

---

## A. A rule is read wrongly

### 1. A sentence has two meanings

- **The problem.** The model picks one meaning and says nothing about the
  other.
- **Example.** "WHEN failed attempts reach 5, lock the account." Exactly 5,
  or 5 or more? At 6 attempts the two meanings differ.
- **What we did.** The model translates each rule 8 times. If the
  translations disagree, we have two meanings. If they agree, the model is
  asked what else the words could mean; the solver finds the case where the
  two meanings differ (6 attempts), and the model is asked 8 times which
  meaning the words support there. If neither wins, the tool asks the
  author: "exactly 5, or 5 or more?"
- **The result.** About half of the ambiguities we planted are found: 14 to
  20 of 36 on most test sets.
- **Still open.** Half are missed. The model is confident about readings
  that a person would ask about.

### 2. One model agrees with itself

- **The problem.** Eight answers of one model often repeat the same choice.
- **Example.** The same "reaches 5" rule: all 8 translations say "exactly
  5".
- **What we did.** A second model translates every rule too (an option). If
  most of its translations mean something else, the rule is ambiguous.
- **The result.** 30 and 32 of 36 planted ambiguities found, where one model
  found 14 and 17. The price: about twice as many questions about rules
  that are clear (15 against 7, and 9 against 5, in 18 runs) (E9, E12).

### 3. The translations differ only in the names they use

- **The problem.** On real specs the 8 translations of a rule often mean the
  same thing but use different names, so they look like a disagreement.
- **Example.** "Display success message with archived name and list of
  updated specs": three translations say `success_message_displayed`, two
  say that and `spec_summary_displayed`.
- **What we did.** Such translations vote. The rule is kept with what more
  than half of them say.
- **The result.** On real changes, the rules that gave the checks nothing
  went from 54% and 62% to 28% and 36% (E26).
- **Still open.** A voted rule can say less than its words: here the list of
  specs is not in the formula.

### 4. There is no name for what a rule demands

- **The problem.** The model first lists the names (symbols) for a whole
  document. For a long document it leaves some out, and a rule then demands
  nothing.
- **Example.** "WHEN file write fails THEN let the error bubble up naturally
  with file path" became `file_write_failed => true`.
- **What we did.** Such rules are read a second time, alone, and the model
  is told that a name is missing. Here it added `error_bubbles_up_with_path`.
- **The result.** On long documents it brings back 5 to 17 points of the
  rules. On the test set we had chosen for it, it did little (16% and 14%
  of rules of no use, against 17% and 16%). The test we had set was not
  passed; it is kept because it never makes a run worse (E27).

### 5. A finding exists only because of the meaning that was picked

- **The problem.** Until the author answers, the tool works with one meaning
  of an ambiguous rule. Some findings exist only with that meaning.
- **Example.** "WHEN a customer enters a wrong PIN for the third time THEN
  lock the account." Read as "exactly the third time", nothing covers the
  fourth wrong PIN: a gap. Read as "three or more", there is no gap.
- **What we did.** Each ambiguous rule is tried once more with its other
  meaning, by the solver alone. A finding that goes away says so in its
  title: "Gap (depends on the reading of R4)" (T15).

---

## B. Two rules say opposite things in different words

### 6. "Grant access" and "deny access" are two unrelated names

- **The problem.** The solver sees names, not words. Two names for opposite
  things can both be true for it.
- **Example.** "A correct password: grant access" and "a locked account:
  deny access". A correct password for a locked account? The solver sees no
  problem: `access_granted` and `access_denied` are both true.
- **What we did.** The model is asked 8 times which facts hold "purely
  because of what the names mean". A fact that more than half of the
  answers support is kept: "access cannot be both granted and denied".
- **The result.** With that fact the solver proves the contradiction. These
  facts carry a large part of all results: without them one test set gives
  10 of 21 found, with them 15 (E8).

### 7. A wrong fact hid a real contradiction

- **The problem.** The facts of entry 6 are guesses. At first we treated
  them as truths.
- **Example.** A wrong fact with 7 of 8 votes made the situation of a real
  contradiction "impossible", and the contradiction was not reported.
- **What we did.** A fact may now only add findings. The solver searches
  twice: with the rules alone, and with the facts added. What the first
  search finds is never taken away. A finding that needs a fact says "if
  the assumed facts hold" and quotes the fact, so the reader can judge it
  (T1).

### 8. A rule uses a name that no other rule uses

- **The problem.** Then nothing can contradict it.
- **Example.** From the Kiro blog: "remove the Property record from the
  Platform" and "retain Property records in the database for audit". The
  model wrote `property_record_removed` and
  `property_record_retained_in_db`: removed and retained at once is fine
  for the solver.
- **What we did.** The rule is translated again, and this time the model may
  only use the names of the other rules. 8 of 8 answers said "not retained
  in the database". That sentence, a *link*, is tested once more before it
  is used.
- **The result.** The blog's contradiction is found, in 3 of the last 3
  runs (T5, E5).

### 9. Opposite outcomes that no fact connected

- **The problem.** The open question of entry 6 often leaves out the pair
  that matters.
- **Example.** "Take the price from the balance" became `payment_taken`,
  "refuse all payments" became `payment_refused`. No fact connected them,
  and the contradiction was missed in 3 of 3 runs.
- **What we did.** For every two rules that can apply together, the model is
  asked directly, 8 times: "can these two outcomes both be true?"
- **The result.** On a test set where every contradiction is said in other
  words: 34 of 36 found, 27 without the question (E18).
- **Still open.** The question also adds contradictions that nobody planted:
  3 of 18 clean specs got one, none without it. Entry 30 is about that.

### 10. "Delete it" against "keep it for seven years"

- **The problem.** One rule is about a thing, the other became a number.
- **Example.** "Delete the listing" became `listing_deleted`. "Keep every
  listing for seven years" became `listing_retention_years = 7`. Nothing
  connects a yes/no fact about a listing with a number of years.
- **What we did.** We tried one more sentence in the prompt ("removing and
  keeping are opposites"). Nothing was gained, and a rule was lost: its
  translations scattered. The sentence was taken out (T14).
- **Still open.** Found in 13 of 21 runs. The stricter question of entry 30
  finds it less often: a setting and what happened are two things.

---

## C. A finding is proven, but it is not real

### 11. Two things happen at the same moment

- **The problem.** For the solver a situation is one snapshot, and two
  events can be in it. Rules are written for one event at a time.
- **Example.** "A visitor signs up: send no email" and "a subscriber changes
  the address: send a confirmation". Both at the same instant: an email and
  no email.
- **What we did.** The model names the event each rule reacts to. A
  contradiction between rules that react to two different events is marked
  *doubtful*. It stays in the report.
- **The result.** On two test sets every doubtful contradiction was a false
  alarm (E8, E9).
- **Still open.** A state taken for an event ("WHEN a member is suspended")
  marks a real contradiction too (E10).

### 12. A situation that cannot happen

- **The problem.** The solver lets two conditions be true together that
  exclude each other by their meaning.
- **Example.** In a real spec: "WHEN agent reads tasks.md AND incomplete
  tasks are found THEN display warning" and "WHEN tasks.md does not exist
  THEN proceed without warning". The solver's situation: the file is read,
  and it does not exist.
- **What we did.** For two rules that contradict each other, the model is
  asked 8 times whether their two conditions can be true together. Here 6
  of 8 said no: "a file cannot be read if it does not exist". The finding
  is marked doubtful, with that sentence.
- **The result.** On specs of ours built for this: clean specs with a
  contradiction 0 of 18, against 11 without the question. On real changes:
  56 contradictions that nobody planted, against 63 (E28).
- **Still open.** It also doubts a real one: in the Kiro blog's order
  example the model holds that a canceled order cannot be a submitted
  order.

### 13. A general rule against its own exception

- **The problem.** Real specs are written as "the general case" plus "the
  special case". The solver reports the pair as a contradiction.
- **Example.** "`createChange(...)` is called: create the directory" and
  "... and the directory already exists: throw an error".
- **What we did.** The solver proves that one rule applies only where the
  other does. The title then says so: "R2 is a special case of R1". It is a
  remark, not a doubt.
- **The result.** On real changes the remark is on 22 of 56 contradictions
  that nobody planted (T35).

### 14. A case that no rule covers, which is not a real gap

- **The problem.** Almost every spec has the gap "nothing happens at all".
  And two names for "free" and "taken" let a slot be neither.
- **Example.** A laundry spec has a rule for "the slot is free" and one for
  "the slot is taken". The model made two names; for the solver a slot can
  be neither, so a booking of such a slot is a gap.
- **What we did.** The gap in which no event happens is marked as such. A
  gap that the assumed facts exclude is marked doubtful.
- **The result.** 71 of 72 planted gaps found. Clean specs still got a false
  gap in 0 to 5 of 18 runs; the mark caught 2 of 13 of them (E13, E16).

### 15. The findings depend on the names the model chose

- **The problem.** Another run picks other names, and finds something else.
- **Example.** The blog's remove/retain contradiction was missed in 4 of 7
  early runs.
- **What we did.** An option formalizes the spec several times. Each finding
  says how often it came up: "found with 3 of 3 symbol sets" (E4).

---

## D. Checking a change against specs that exist

### 16. A change that contradicts an existing rule

- **The problem.** Neither the specs nor the change has a contradiction by
  itself.
- **Example.** The specs: "at 5 failed attempts the account is locked". The
  change adds: "an administrator's account is not locked".
- **What we did.** The tool applies the change to the specs, checks the
  whole, and shows only the findings that involve a rule of the change.
- **The result.** On 138 changes we wrote: all 180 planted contradictions
  and 125 of 126 planted gaps found (E17, E19 to E21).

### 17. A change removes a rule, and a case is left open

- **Example.** A change drops the rule for "a visitor who is not on the
  patient's list".
- **What we did.** The removed rule stays in the document under a label of
  its own, so that it gets the same names. For each one the solver is asked
  whether its case is still covered.
- **The result.** The gap is reported as "opened by removing X1" in 18 of 18
  runs (E19).

### 18. The cheap way of checking a change loses rules

- **The problem.** Formalizing all specs again for each change costs 68
  requests. Formalizing only the new rules costs 9 to 11, but the model
  then sees little around a new rule.
- **Example.** "WHEN a person is younger than 17 THEN the system does not
  create any learner file." Shown only the saved names, the model tied it
  to the saved event "a person registers", which the rule does not name.
- **The result.** 50 of 54 contradictions found the cheap way, where the
  full way found 54. After a change to the prompt: 72 of 72 on the next
  set. The cheap way is an option, not the default (E20, E21).

---

## E. Real specs are harder than the ones we wrote

### 19. Half of the real rules gave the checks nothing

- **The problem.** A real rule demands two or three things. The list of
  names does not fit it.
- **Example.** On 16 changes of a real project (the OpenSpec tool's own
  specs): 147 of 366 rules got no agreed translation, and 45 more were
  accepted with a translation that demands nothing. On our own specs that
  is about 3%.
- **What we did.** Entries 3 and 4, and a rule that demands nothing is now
  reported as "Not checked".
- **The result.** Now one real rule in six to one in four is of no use, the
  more the longer the document (E23 to E27).

### 20. A value that is not a word stopped the run

- **Example.** The status `timed out`, the status 201, the folder `.claude`.
- **What we did.** The code repairs such names (`timed_out`,
  `answer_status_201`). No prompt changed.
- **The result.** 48 of 48 runs finish, where 7 of 48 did (E25).

### 21. Reading a long document in pieces (tried and dropped)

- **What we tried.** Cut a long document at its headings, and let the model
  read a few rules at a time.
- **What happened.** The rules got their names, but no more of them got an
  agreed translation (44% of no use, against 57% and 47% in two runs
  without it). More runs stopped. And a state was read as an event in a
  later piece, so a real contradiction was marked doubtful in 3 of 3 runs.
  It was taken out (T28, E24).

### 22. On real specs, most contradictions that nobody planted are not real

- **Example.** We read 20 of the 40 that 13 real specs got in one run.
- **The result.** None is a contradiction the author would not have meant.
  12 are artefacts (8 of them in a situation that cannot happen, entry 12),
  7 set a general rule against its exception (entry 13), 1 is a fair
  question. The reading was done by the assistant that works on this
  project, not by a person (T32).

---

## F. Specs about an agent that calls tools

The real target is a project of an agent system,
[TestingTheAgents](https://github.com/unibuc-cs/TestingTheAgents): 33 spec
files, 465 scenarios, four open changes. Its authors say that one change
cannot be built, for four reasons.

### 23. The rules are about a whole run, not about one moment

- **Example.** "WHEN a call of `ship_parcel` succeeds in a run with a plan
  THEN an earlier call of `request_signoff` in the run was approved" and
  "WHEN an express request is handled in a run THEN `request_signoff` is
  not called in the run". Two different events, both in one run.
- **The problem.** By entry 11 this real contradiction was marked doubtful,
  as two events at one moment: found in 12 of 12 runs, marked in all 12.
- **What we did.** An option, `--whole-run`, says that a situation is a
  whole run.
- **The result.** 12 of 12 found and not doubtful (E29).

### 24. Examples were read as rules

- **Example.** Three examples of one request: "the parcel was delivered",
  "the parcel is still in the warehouse", "the customer cancels". Read as
  rules for all cases, the second and third contradict each other for a
  parcel in the warehouse whose customer cancels. Neither example says
  that.
- **What we did.** An option, `--examples`, says which scenarios are
  examples. A contradiction with an example is marked doubtful unless the
  example's own case is the whole situation.
- **The result.** Changes that only add examples: a contradiction in 6 of
  12 runs before, 0 after. Then the real project showed a case we had not
  thought of, an example and a variant of it, reported in 21 of 32 parts.
  After a second repair: 3 of 12 before, 0 of 12 after (E29, E30).

### 25. A setting named like another setting

- **Example.** `shipping.max_parcels` is 20. A change adds
  `shipping.max_batch_parcels` is 50. The model's link said that the first
  setting must be 50.
- **What we did.** A link that only moves a demand to another name is asked
  about once more, with both names in view.
- **The result.** A false contradiction in 11 of 12 runs before, 0 after
  (E29).

### 26. The project is too large to read at once

- **The problem.** One document holds about 100 scenarios before the
  translations get worse. The project has 465.
- **What we did.** A change is checked in parts: one document for each spec
  file it does not touch, next to the files it does. A finding says in how
  many parts it was found.
- **The result.** The first of the authors' four reasons, two rules of the
  change that contradict each other, is "found in 16 of 24 parts". Nothing
  else is found in more than 3 parts. That count tells the changes apart;
  the number of contradictions does not (T38, T41).
- **Still open.** 4 of 131 parts cannot be read. A contradiction that needs
  rules of three spec files is not found.

### 27. A contradiction that needs three rules

- **The problem.** No two of the rules contradict each other. One step is
  missing, and nobody wrote it down.
- **Example.** "WHEN a check-in succeeds in a run with a plan THEN an
  earlier call of `ask_manager` was approved." "WHEN a call of `ask_manager`
  is made THEN the run is not a late-arrival run." A late arrival is
  checked in: the first rule demands an approval, the second forbids the
  call. But the second rule applies only when the call is made, and nothing
  says that an approved call is a call that was made.
- **What we did.** The model is asked: where the first rule applies and is
  obeyed, must the call have been made? 8 of 8 said yes. With that the
  solver proves the contradiction.
- **The result.** Found in 12 of 12 runs, and in 2 without the question. On
  the real project the second of the authors' four reasons, a missing
  approval, is now reported (E31, T40).
- **Tried and dropped.** Three other forms of the question. One example: the
  model said that "to give the return label, the system must have found the
  parcel". That is how a system works, not what the words say (T39).

### 28. The model read the question backwards

- **Example.** The rule: "WHEN a call of `ask_vet` or `order_medicine` is
  made THEN the agent making it is the reception agent." The question:
  where this rule applies, is `order_medicine` called? Up to 7 of 8 answers
  said yes. The right answer is no: the rule applies when `ask_vet` is
  called, too.
- **The problem.** The model took the fact as given ("it says that
  `order_medicine` is called") and checked that the rule then applies.
- **What we did.** First, one more sentence in the prompt about rules that
  apply in several cases. It changed nothing: 7 of 8 before and after. Then
  we read the model's own reasons, saw the real defect, and changed the
  question: "this statement is not given. Must it be true?"
- **The result.** 0 of 8 say yes now. A false contradiction in 6 of 12 runs
  before, 0 of 12 after. On the real project that question now adds 2
  contradictions over four changes, where it added 7 (6 of them false)
  (T42, T43, E32, T44).
- **The lesson.** Read the model's reasons before choosing the repair.

### 29. A rule about two calls stopped the run

- **Example.** "WHEN a call of `order_lenses` or `order_frame` is made THEN
  the run writes an audit entry." The model listed this rule twice, with
  the same words: once for each call.
- **The problem.** Our format has room for one event per rule, and this
  rule reacts to either of two. The tool tells the rules of a change from
  the others by their labels, and stopped at two rules with one label: 11
  of 36 runs.
- **What we did.** We first guessed that the model splits the rule in two.
  A look at what it really returns showed the same words twice. Such copies
  are now one rule. Ten lines of code, no prompt changed.
- **The result.** 36 of 36 runs finish, where 25 did. Planted
  contradictions found in 23 of 24 runs, where 14 (T45, E33).

### 30. The model guesses how the system works

- **The problem.** The question of entry 9, "can these two outcomes both be
  true?", is answered "no" too often on the real project.
- **Example.** One rule demands that a request is refused and that nothing
  is written to the audit log. The model: impossible, because "a refused
  request generates an audit event". Nobody wrote that. A second shape: a
  limit of 40 tool calls, and "no tool was called": the model says a run
  cannot have zero calls if the maximum is 40. These are two different
  things.
- **How large it is.** In the reports of the four changes, 9 of the 18
  contradictions that are not doubtful rest on such an answer (T46).
- **What we did.** The question now says what does not count: how a system
  usually works, and two statements that can be about two different
  things.
- **The result.** On the real project all 9 are gone: the four reports have
  5, 2, 2 and 1 contradictions, where they had 9, 3, 3 and 3, and the two
  real reasons that were found are still there. On 12 new examples of ours:
  the 4 real contradictions are found in 12 of 12 runs before and after;
  the 8 that only look like one are reported in 5 of 24 runs before, 3
  after (T47, E34).
- **What it cost.** On an older test set one planted contradiction is no
  longer found (entry 10: "delete the payslips" against "keep every payslip
  for ten years"). We had set the rule "nothing may be lost"; it was not
  met, and we kept the change because it gains more than it loses.
- **Still open.** The step of entry 8 makes the same kind of guess: "every
  batch is listed as turned" became "if the cellar is closed, the turning
  tool must have been called".

### 31. The same question, asked twice, gives two answers

- **The problem.** Every question is asked 8 times and the majority
  decides. We had assumed that a second round of 8 gives the same majority.
- **Example.** The question of entry 27: "where this rule applies and is
  obeyed, must the call have been made?" The right answer is yes. Asked
  once: 8 of 8 yes. Asked again on the same run, with the same words: 3 of
  8.
- **Why.** The model's own reasons show it. The question says "take a
  situation in which the requirement applies". Some answers read that as
  "any run of a system that has this rule", also a run in which the rule's
  condition is not met, and then say no: "if the call does not succeed, the
  requirement imposes no constraints". One answer says in so many words:
  "This phrasing is ambiguous."
- **How large it is.** In one round, a real contradiction was not found in
  2 of 12 runs for that reason (T47).
- **What we did.** The question now says which situations count: those in
  which the WHEN part of the rule is true.
- **The result.** On 16 new examples, each run asked three times: 39 of 46
  right steps get the same vote all three times, where 22 did. Real
  contradictions found in 60 of 72 askings, where 58; on three earlier
  sets 182 of 183, where 177. No false one added (T48, E35).
- **The lesson.** Ask a question twice before trusting its majority.

### 32. A right answer, written down in the wrong form

- **The problem.** The clearer question of entry 31 made the model answer
  one kind of case rightly for the first time, and our code then drew a
  wrong conclusion from the right answer.
- **Example.** A rule begins "WHEN an approval request is refused ...".
  Question: must a request have been made? The model, rightly: yes. Our
  code wrote that down as "where this rule is *obeyed*, a request was
  made". Another rule says "in an emergency run no approval request is
  made". An emergency run in which a request is refused simply breaks that
  second rule. But because of the word "obeyed", the logic part needed the
  first rule to see it, and reported the two rules as contradicting each
  other: 2 more false contradictions on the real project.
- **What we did.** The model now also says whether the statement follows
  from the rule's WHEN part alone or from what the rule demands, and the
  fact is written accordingly.
- **The result.** The 2 false contradictions are gone. The four reports of
  the real project have 9 contradictions in all (5, 2, 1 and 1), with the
  two real reasons among them (T48).
- **The lesson.** A better answer from the model can break code that relied
  on the worse one. Check the real project after every change to a
  question, not only the test sets.

### 33. In a spec about whole runs, a name is still described as a moment

- **The problem.** When the model lists the names, it describes each as a
  fact about one moment. For a spec about whole runs that is the wrong
  tense.
- **Example.** The name `ask_astronomer_made` got the description "a call
  to ask_astronomer is being made". Question: if an earlier call was
  approved, must this be true? The model: no, "a past approved call does
  not imply that a call is currently in progress". So the chain of entry 27
  is not found.
- **How large it is.** 3 of 12 runs with such a chain in the last test
  (E35).
- **What we did.** Nothing yet. This is the next step.

---

## G. Not solved

| Issue | Example |
|---|---|
| Two of the four reasons of the real project are not found | one needs rules of three spec files; one is arithmetic: the size of a batch against two budgets of steps |
| A property of one call becomes a property of the whole run | "the token the call was made with": two rules about two different calls then contradict each other |
| The questions are asked 40 times for a document at most | in a large project that leaves out most pairs |
| There is no time in the logic | "then", "after" and "until" are not modelled |
| "Delete" against "keep for N years" | entry 10 |
| Half of the ambiguities are missed with one model | entry 1 |
| The evaluation is small | the specs with known answers were written by us; one main model; two real projects |
