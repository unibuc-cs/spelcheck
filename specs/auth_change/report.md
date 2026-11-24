# Requirements analysis: admin-never-locked

5 requirements analysed: 1 conflict(s), 0 gap(s), 0 ambiguity(ies).

Change `admin-never-locked`, checked against the specs that exist: 1 scenario(s) added, 0 in modified requirements.

Only findings that involve an added or modified rule (R5) are shown. 3 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict: Administrator Account Lock Conflict

Requirement R3 states that the system must lock an account when the number of failed attempts reaches 5. However, Requirement R5 states that the system must not lock an account if it belongs to an administrator. In the situation where an administrator's account has reached 5 failed attempts, the system is forced to both lock and not lock the account, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail to operate correctly for administrator accounts that reach the failure limit, as it cannot simultaneously satisfy the lock and no-lock conditions.
- **B) Change:** Modify Requirement R3 to explicitly exclude administrator accounts from the locking mechanism, or modify Requirement R5 to specify that administrators are subject to a different security protocol instead of a simple lock.

*Proven:* Requirements R3, R5 cannot all be obeyed in this situation:
- failed_attempts_count = 5 (The number of consecutive failed login attempts for the account)
- TRUE: is_administrator (The account belongs to an administrator)

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | auth | Login | Valid credentials |  |
| R2 | auth | Login | Invalid credentials |  |
| R3 | auth | Account Lockout | Lockout threshold |  |
| R4 | auth | Account Lockout | Locked account |  |
| R5 | auth | Administrator Access | Administrators are never locked out | **added** |
