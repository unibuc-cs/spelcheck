# Requirements analysis: auth_openspec

5 requirements analysed: 2 conflict(s), 1 gap(s), 1 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity: Ambiguity in lock threshold

Requirement R3 is ambiguous because it is unclear whether the account should be locked when the number of failed attempts is exactly 5 or when it is 5 or more. In the situation where an account has 6 failed attempts but is not locked, the two readings lead to different conclusions: one reading requires the account to be locked, while the other does not. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the account is locked only when the number of failed attempts is exactly 5.
- **B) Change:** Reword the requirement to state that the account is locked when the number of failed attempts is 5 or more.

*Proven:* Requirement R3 has no single clear meaning. Shown both readings and the situation below, and asked whether the words decide between them, the answers were: 1 for reading 1, 6 for reading 2, 0 'either'.
Reading 1: If the number of consecutive failed login attempts for an account equals 5, the system must place the account in a locked state. [in logic: (= failed_attempts_count 5) => account_locked]
Reading 2: If the number of consecutive failed login attempts for an account is at least 5, the system must place the account in a locked state. [in logic: (>= failed_attempts_count 5) => account_locked]
The readings differ in this situation:
- FALSE: account_locked (The account is currently in a locked state)
- failed_attempts_count = 6 (The number of consecutive failed login attempts for the account)
Choosing reading 2 instead of reading 1 changes no conflict and no gap.

## 2. Conflict: Conflict between lockout and admin exemption

Requirement R3 states that the system must lock the account when failed attempts reach 5. However, Requirement R5 states that the system must not lock the account if it belongs to an administrator. In the situation where an administrator's account has reached 5 failed attempts, these two requirements directly contradict each other, making it impossible to satisfy both simultaneously.

- **A) Keep as-is:** Keeping the requirements as written means the system is in a state of logical conflict and cannot determine whether to lock the administrator's account or not.
- **B) Change:** Modify Requirement R3 to explicitly exclude administrator accounts from the lockout rule, or modify Requirement R5 to specify that administrators are subject to lockout after a different, higher number of attempts.

*Proven:* Requirements R3, R5 cannot all be obeyed in this situation:
- TRUE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 5 (The number of consecutive failed login attempts for the account)

## 3. Conflict (if the assumed facts hold): Conflict between correct password and locked account

The requirements create a contradiction when a user enters the correct password for an account that is already locked. Requirement R1 states that the system must grant access when a correct password is submitted, while Requirement R4 states that the system must deny access when a password is submitted for a locked account. This problem exists only if it is assumed that the system cannot grant and deny access at the same time, which is a standard operational constraint not explicitly written in the requirements.

- **A) Keep as-is:** Keeping the requirements as written means the system is forced to both grant and deny access simultaneously when a correct password is entered for a locked account, which is logically impossible under standard system behavior.
- **B) Change:** Modify Requirement R4 to state that the system denies access only if the submitted password is incorrect, or modify Requirement R1 to state that access is granted only if the account is not locked.

*Proven:* Requirements R1, R4 cannot all be obeyed in this situation:
- TRUE: account_locked (The account is currently in a locked state)
- TRUE: password_correct (The submitted password matches the stored password for the account)
- TRUE: password_submitted (A user has submitted a password for login)
This depends on assumptions that are not stated in the requirements:
- F2: The system cannot grant access and deny access simultaneously.

## 4. Gap (no event happens): Idle System State

The requirements do not specify any action for the system when it is not processing a login attempt. This situation describes a state where the account is not an administrator account, there are no failed attempts recorded, and no password has been submitted. Since no event occurs in this situation, this may only mean that the system waits.

- **A) Keep as-is:** Keeping the requirements as written implies that the system takes no specific action and remains in its current state when no login attempt is made.
- **B) Change:** Add a requirement stating that the system remains in an idle state and performs no actions when no password is submitted.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account belongs to an administrator)
- failed_attempts_count = 0 (The number of consecutive failed login attempts for the account)
- FALSE: password_submitted (A user has submitted a password for login)
No event happens in this situation, so this may only mean that the system waits.

## 5. Scenario, allowed: Access granted with wrong password

The requirements state that the system must deny access when a user submits an incorrect password (R2). However, the logic allows a situation where the password is incorrect, yet access is still granted. This directly defeats the purpose of password authentication and security.

- **A) Keep as-is:** Keep the requirements, accepting that the system might grant access even when the password is wrong.
- **B) Change:** Add a requirement stating that the system SHALL NOT grant access if the submitted password is incorrect.

*Proven:* The requirements allow this behaviour:
- TRUE: access_granted (The system grants access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- TRUE: password_submitted (A user has submitted a password for login)
Requirement R1 does not apply in it, and yet what R1 demands is the case.

## 6. Scenario, allowed: Denial without login attempt

The requirements allow the system to deny access even when no password has been submitted and the password is not correct. This is odd because the login requirement (R2) only mandates denial when an incorrect password is submitted, implying that denial should be a response to a login attempt, not a state that can exist without one.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement stating that the system SHALL NOT deny access unless a user has submitted a password for login.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: password_correct (The submitted password matches the stored password for the account)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R2 does not apply in it, and yet what R2 demands is the case.

## 7. Scenario, allowed: Denial without login attempt

The requirements state that access is denied when a user submits an incorrect password (R2) or when submitting a password for a locked account (R4). However, the logic allows for a state where access is denied even though no password was submitted and the account is not locked. This defeats the purpose of the login specification, which implies that access decisions are tied to the act of submitting credentials.

- **A) Keep as-is:** Keep the requirements, accepting that the system may deny access for reasons not explicitly defined in the login scenarios.
- **B) Change:** Add a requirement stating that the system SHALL grant access if no password has been submitted and the account is not locked, or clarify that access denial only occurs in response to a submitted password.

*Proven:* The requirements allow this behaviour:
- TRUE: access_denied (The system denies access to the user)
- FALSE: account_locked (The account is currently in a locked state)
- FALSE: password_submitted (A user has submitted a password for login)
Requirement R4 does not apply in it, and yet what R4 demands is the case.
