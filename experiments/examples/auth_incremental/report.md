# Requirements analysis: admin-never-locked

5 requirements analysed: 1 conflict(s), 0 gap(s), 0 ambiguity(ies).

Change `admin-never-locked`, checked against the specs that exist: 1 scenario(s) added, 0 modified, 0 removed.

Shown are the findings that involve an added or modified rule (N1). 3 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict: Administrator Lockout Conflict

Requirement R3 states that the system must lock an account when the number of failed attempts reaches 5. However, Requirement N1 states that the system must not lock an account if it belongs to an administrator. In the situation where an administrator has failed 5 times, these two requirements directly contradict each other.

- **A) Keep as-is:** Keeping the requirements as written means the system is forced to choose between locking the administrator's account or violating the rule that administrators are never locked, creating an undefined state.
- **B) Change:** Modify Requirement R3 to explicitly exclude administrator accounts from the locking mechanism, or clarify that Requirement N1 takes precedence over R3 for administrator accounts.

*Proven:* Requirements R3, N1 cannot all be obeyed in this situation:
- failed_attempts_count = 5 (The number of consecutive failed login attempts for the account)
- TRUE: is_admin (The account belongs to an administrator)

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | auth | Login | Valid credentials |  |
| R2 | auth | Login | Invalid credentials |  |
| R3 | auth | Account Lockout | Lockout threshold |  |
| R4 | auth | Account Lockout | Locked account |  |
| N1 | auth | Administrator Access | Administrators are never locked out | **added** |
