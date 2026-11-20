# Requirements analysis: auth_openspec

5 requirements analysed: 2 conflict(s), 1 gap(s), 1 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity: Ambiguity in lock threshold

Requirement R3 states that the system locks an account when the number of failed attempts reaches 5, but it is unclear if this applies only when the count is exactly 5 or whenever it is 5 or more. In the situation where an account has 6 failed attempts but is not locked, the two interpretations lead to different conclusions about whether the requirement is being met. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying that the account is only required to be locked when the failed attempt count is exactly 5.
- **B) Change:** Reword R3 to explicitly state that the system locks the account when the number of failed attempts is 5 or more.

*Proven:* Requirement R3 has no single clear meaning. Shown both readings and the situation below, and asked whether the words decide between them, the answers were: 1 for reading 1, 6 for reading 2, 0 'either'.
Reading 1: If the number of consecutive failed login attempts for an account equals 5, the system must place the account in a locked state. [in logic: (= failed_attempts_count 5) => account_locked]
Reading 2: If the number of consecutive failed login attempts for an account is at least 5, the system must place the account in a locked state. [in logic: (>= failed_attempts_count 5) => account_locked]
The readings differ in this situation:
- FALSE: account_locked (The account is currently in a locked state)
- failed_attempts_count = 6 (The number of consecutive failed login attempts for the account)
With reading 2 instead of reading 1: a requirement applies in 1 of the gaps reported below.

## 2. Conflict: Administrator Account Lock Conflict

There is a direct contradiction between the rule that locks an account after five failed attempts and the rule that prevents administrator accounts from being locked. In the situation where an administrator's account has reached five failed attempts, the system is required to both lock the account and keep it unlocked, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail to operate correctly when an administrator makes five failed login attempts, as it cannot simultaneously satisfy the locking and non-locking conditions.
- **B) Change:** Modify R3 to explicitly exclude administrator accounts from the locking rule, stating that the system locks the account only if the number of failed attempts reaches 5 and the account does not belong to an administrator.

*Proven:* Requirements R3, R5 cannot all be obeyed in this situation:
- TRUE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 5 (The number of consecutive failed login attempts for the account)

## 3. Conflict (if the assumed facts hold): Conflict between correct password and locked account

The requirements create a contradiction when a user enters the correct password for an account that is already locked. Requirement R1 states that the system must grant access when a correct password is submitted, while Requirement R4 states that the system must deny access when a password is submitted for a locked account. This conflict relies on the assumption that the system cannot grant and deny access at the same time.

- **A) Keep as-is:** Keeping the requirements as written means the system is forced to both grant and deny access simultaneously when a correct password is entered for a locked account, which is logically impossible.
- **B) Change:** Modify Requirement R4 to state that the system denies access only if the submitted password is incorrect, or modify Requirement R1 to state that access is granted only if the account is not locked.

*Proven:* Requirements R1, R4 cannot all be obeyed in this situation:
- TRUE: account_locked (The account is currently in a locked state)
- TRUE: password_correct (The submitted password matches the stored password for the account)
- TRUE: password_submitted (A user has submitted a password for login)
This depends on assumptions that are not stated in the requirements:
- F2: The system cannot grant access and deny access simultaneously.

## 4. Gap (no event happens, depends on the reading of R3): Ambiguous Locking Threshold

Requirement R3 is ambiguous regarding when an account is locked. One reading is that the system locks the account only when the number of failed attempts reaches exactly 5, while the other reading is that the system must lock the account whenever the number of failed attempts is at least 5. In the situation where the count is 6, the second reading requires the account to be locked, whereas the first reading leaves the system's state undefined because the count is no longer exactly 5. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying the account is locked only when the count is exactly 5, leaving the state undefined for counts greater than 5.
- **B) Change:** Reword R3 to state that the system locks the account when the number of failed attempts is 5 or more.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 6 (The number of consecutive failed login attempts for the account)
- FALSE: password_submitted (A user has submitted a password for login)
No event happens in this situation, so this may only mean that the system waits.
But R3 is ambiguous (see its finding). With its other reading a requirement applies in this situation. That reading: If the number of consecutive failed login attempts for an account is at least 5, the system must place the account in a locked state.

## 5. Scenario, allowed: Access granted with wrong password

The requirements state that the system must deny access when a user submits an incorrect password (R2). However, the logic allows a situation where the password is incorrect, yet access is still granted. This directly defeats the purpose of password authentication and account security.

- **A) Keep as-is:** Keep the requirements, accepting that the system might grant access even when the password is wrong.
- **B) Change:** Add a requirement stating that the system SHALL NOT grant access unless the submitted password matches the stored password.

*Proven:* The requirements allow this behaviour:
- TRUE: access_granted (The system grants access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- TRUE: password_submitted (A user has submitted a password for login)
Requirement R1 does not apply in it, and yet what R1 demands is the case.

## 6. Scenario, allowed: Denial without login attempt

The requirements allow the system to deny access even when no password has been submitted and the password is not correct. This is odd because the login requirement (R2) only mandates denial when an incorrect password is submitted, yet the system can deny access in a state where no submission occurred, which may defeat the purpose of a clear login flow.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement that the system only denies access when a password has been submitted, to forbid denial without a login attempt.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R2 does not apply in it, and yet what R2 demands is the case.

## 7. Scenario, allowed: Denial without login attempt

The requirements state that access is denied when a user submits an incorrect password (R2) or when submitting a password for a locked account (R4). However, the logic allows for a state where access is denied even though no password was submitted and the account is not locked. This defeats the purpose of the login specification, which implies that access decisions are tied to authentication attempts or lockout status, not arbitrary denials.

- **A) Keep as-is:** Keep the requirements, allowing the system to deny access for reasons not explicitly defined in the login or lockout scenarios.
- **B) Change:** Add a requirement stating that the system SHALL grant access if no password has been submitted and the account is not locked, or clarify that access denial only occurs in response to a submitted password.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: account_locked (The account is currently in a locked state)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R4 does not apply in it, and yet what R4 demands is the case.
