# Requirements analysis: auth_openspec

5 requirements analysed: 2 conflict(s), 3 gap(s), 1 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity: Ambiguity in lock threshold

Requirement R3 is unclear about whether the account should be locked when the failed attempt count is exactly 5 or when it is 5 or more. In the situation where the count is 6 and the account is not locked, the two interpretations lead to different conclusions about whether the system has failed to meet the requirement. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying that the account is only required to be locked when the count is exactly 5, so a count of 6 does not necessarily trigger a lock.
- **B) Change:** Reword R3 to state that the system locks the account when the number of failed attempts reaches or exceeds 5, ensuring that a count of 6 always results in a locked account.

*Proven:* Requirement R3 has no single clear meaning. Shown both readings and the situation below, and asked whether the words decide between them, the answers were: 1 for reading 1, 6 for reading 2, 0 'either'.
Reading 1: If the number of consecutive failed login attempts for an account equals 5, the system must place the account in a locked state. [in logic: (= failed_attempts_count 5) => account_locked]
Reading 2: If the number of consecutive failed login attempts for an account is at least 5, the system must place the account in a locked state. [in logic: (>= failed_attempts_count 5) => account_locked]
The readings differ in this situation:
- FALSE: account_locked (The account is currently in a locked state)
- failed_attempts_count = 6 (The number of consecutive failed login attempts for the account)

## 2. Conflict: Administrator Account Lock Conflict

There is a direct contradiction between the rule that locks accounts after five failed attempts and the rule that prevents administrator accounts from being locked. In the situation where an administrator's account has reached five failed attempts, the system is required to both lock the account and not lock the account, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail to operate correctly when an administrator makes five failed login attempts, as it cannot simultaneously satisfy the locking and non-locking conditions.
- **B) Change:** Modify R3 to explicitly exclude administrator accounts from the locking rule, or modify R5 to specify that administrators are subject to a different security measure instead of being exempt from locking.

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

## 4. Gap: Undefined state after lockout

The requirements define what happens when the failed attempt count reaches 5 (R3) and what happens when a password is submitted to a locked account (R4). However, they do not specify the system's behavior or state when the failed attempt count is 6 and no new password is currently being submitted. This leaves a gap in the specification for the state of the account after it has already been locked.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific state is undefined, potentially leading to inconsistent implementation or unexpected behavior.
- **B) Change:** Add a requirement stating that once an account is locked, it remains in a locked state until an administrator manually unlocks it, regardless of the current failed attempt count.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 6 (The number of consecutive failed login attempts for the account)
- FALSE: password_submitted (A user has submitted a password for login)

## 5. Gap: Undefined System Behavior

The requirements do not specify what the system must do when a user has not submitted a password, the account is not an administrator, and there are no failed attempts. This gap appears in the situation where no password is submitted, the account is not an administrator, and the failed attempt count is zero.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific state is undefined and not governed by any rule.
- **B) Change:** Add a requirement stating that when no password is submitted, the system shall remain in its current state or display a login prompt.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 0 (The number of consecutive failed login attempts for the account)
- FALSE: password_submitted (A user has submitted a password for login)

## 6. Gap: Undefined behavior for negative attempt count

The requirements do not specify what the system must do when the number of consecutive failed login attempts is negative. This situation arises when the account is not an administrator, the failed attempt count is -1, and no password has been submitted.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior is undefined if the failed attempt count ever becomes negative.
- **B) Change:** Add a requirement stating that the system must reset the failed attempt count to zero if it is ever detected to be negative.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = -1 (The number of consecutive failed login attempts for the account)
- FALSE: password_submitted (A user has submitted a password for login)

## 7. Scenario, allowed: Access granted with wrong password

The requirements allow the system to grant access even when the submitted password is incorrect. This directly defeats the purpose of password authentication, which is to ensure that only users with the correct credentials can log in.

- **A) Keep as-is:** Keep the requirements, so the behaviour of granting access with an incorrect password remains allowed.
- **B) Change:** Modify the requirements to explicitly state that the system SHALL deny access whenever the submitted password is incorrect, regardless of other conditions.

*Proven:* The requirements allow this behaviour:
- TRUE: access_granted (The system grants access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- TRUE: password_submitted (A user has submitted a password for login)
Requirement R1 does not apply in it, and yet what R1 demands is the case.

## 8. Scenario, allowed: Denial without login attempt

The requirements allow the system to deny access even when no password has been submitted and the password is not correct. This is odd because the login requirement (R2) specifically ties denial to the submission of an incorrect password, implying that denial should only occur in the context of a login attempt.

- **A) Keep as-is:** Keep the requirements, allowing the system to deny access even without a password submission.
- **B) Change:** Modify R2 to explicitly state that access is denied only when a user submits an incorrect password, ensuring denial is tied to a login attempt.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R2 does not apply in it, and yet what R2 demands is the case.

## 9. Scenario, allowed: Denial without login attempt

The requirements allow the system to deny access even when no password has been submitted and the account is not locked. This is likely not intended because access denial is specified as a response to specific login events (incorrect password or locked account), not as a default state or an action taken without user interaction.

- **A) Keep as-is:** Keep the requirements, allowing the system to deny access in states where no password was submitted and the account is not locked.
- **B) Change:** Add a requirement stating that the system SHALL NOT deny access unless a password has been submitted or the account is locked.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: account_locked (The account is currently in a locked state)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R4 does not apply in it, and yet what R4 demands is the case.
