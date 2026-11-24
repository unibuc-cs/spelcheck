# Requirements analysis: visitors-gap

4 requirements analysed: 0 conflict(s), 1 gap(s), 0 ambiguity(ies).

Change `visitors-gap`, checked against the specs that exist: 0 scenario(s) added, 0 modified, 1 removed.

Shown are the findings that involve an added or modified rule, and the gaps that a removed rule (X1) leaves open. 2 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Gap (opened by removing X1): Missing rule for unauthorized check-in

The requirements do not specify what the system must do when a visitor who is not on the patient's visitor list attempts to check in. This gap exists because the previous rule that handled this specific scenario was removed.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a visitor who is not on the list and attempts to check in.
- **B) Change:** Add a requirement stating that when a visitor checks in at a ward and is not on the patient's visitor list, the system keeps the ward door closed and calls a nurse.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: visiting_time_ends (The scheduled visiting time period has ended)
- TRUE: visitor_checks_in (A visitor initiates a check-in process at a ward)
- FALSE: visitor_leaves_without_badge (A visitor leaves the ward without returning their badge)
- FALSE: visitor_on_list (The checking-in visitor is present on the patient's visitor list)
- visitor_stay_duration = 2 (The amount of time a visitor has stayed in the ward, in hours)
Before the change a requirement covered this situation, and the change removes it:
- X1: WHEN a visitor checks in at a ward AND the visitor is not on the patient's visitor list THEN the system keeps the ward door closed and calls a nurse

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | visitors | Check-in | Listed visitor |  |
| X1 | visitors | Check-in | Unlisted visitor | **removed** |
| R2 | visitors | Hours | End of visiting time |  |
| R3 | visitors | Hours | Long visit |  |
| R4 | visitors | Safety | Badge not returned |  |
