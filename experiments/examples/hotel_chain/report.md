# Requirements analysis: add-late-arrivals

6 requirements analysed: 1 conflict(s), 0 gap(s), 0 ambiguity(ies).

Change `add-late-arrivals`, checked against the specs that exist: 2 scenario(s) added, 0 modified, 0 removed.

Shown are the findings that involve an added or modified rule (R4, R5). 1 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict (if the assumed facts hold): Conflict between manager approval and late-arrival rules

The requirements cannot all be obeyed in this situation because R1 requires that an earlier call to ask_manager was approved, while R4 forbids any call to ask_manager in a late-arrival run. This problem appears in the situation where a check-in succeeds in a run that is both planned and a late-arrival. This finding depends on the assumption that if an earlier call to ask_manager was approved, then a call to ask_manager was made in the run.

- **A) Keep as-is:** Keeping the requirements as written means that a successful check-in in a planned, late-arrival run is impossible because it would require both an approved manager request and the absence of any manager request.
- **B) Change:** Change R4 to allow calls to ask_manager in late-arrival runs, or change R1 to not require an approved manager request when the run is a late-arrival run.

*Proven:* Requirements R1, R4 cannot all be obeyed in this situation:
- TRUE: check_in_guest_succeeded (A call to check_in_guest has succeeded in the current run)
- TRUE: run_has_plan (The current run is a planned run)
- TRUE: run_is_late_arrival (The current run is a late-arrival run)
This depends on assumptions that are not stated in the requirements:
- F1: Where R1 applies and is obeyed, a part of the condition of R4 holds: If an earlier call to ask_manager was approved, then a call to ask_manager was made in the run.

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | stays | Manager before a check-in | No check-in in a plan without the manager |  |
| R2 | stays | Refunds | A refund goes to a verified card |  |
| R3 | stays | Requests | Example: a guest is checked in |  |
| R4 | stays | Late arrivals | A late-arrival run asks nobody | **added** |
| R5 | stays | Late arrivals | A late arrival gets the night code | **added** |
| R6 | stays-records | Stay records | Every check-in is recorded |  |
