# Requirements analysis: auth_split_symbols

5 requirements analysed: 2 conflict(s), 3 gap(s), 1 ambiguity(ies).

Assumed domain facts. The model proposed them from the meaning of the words; the requirements do not state them. They are used only to look for more conflicts, and a conflict that depends on one says so.

- F1: The failed attempt count cannot be negative. (8/8 samples agree)
- F2: Access cannot be both granted and denied. (8/8 samples agree)
- F3: A password cannot be both correct and incorrect. (8/8 samples agree)

## 1. Ambiguity: Ambiguity in Locking Threshold

Requirement R3 is ambiguous because it is unclear whether the account should be locked when the failed attempt count is exactly 5 or when it is 5 or more. In the situation where the count is 6 and the account is not locked, the two interpretations of the requirement lead to different conclusions about whether the system is behaving correctly. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying that the account is only required to be locked when the count is exactly 5, which would allow the account to remain unlocked at 6 attempts.
- **B) Change:** Reword R3 to state that the system locks the account when the number of failed attempts reaches or exceeds 5, ensuring the account is locked at 6 attempts.

*Proven:* Requirement R3 has no single clear meaning (independent translations split 5/3).
Reading 1: If the number of consecutive failed login attempts on an account reaches 5, the system must lock that account. [in logic: (= failed_attempt_count 5) => account_locked]
Reading 2: If the total number of consecutive failed login attempts for an account reaches 5, the account must be in a locked state. [in logic: (>= failed_attempt_count 5) => account_locked]
The readings differ in this situation:
- FALSE: account_locked (The account is currently in a locked state)
- failed_attempt_count = 6 (The total number of consecutive failed login attempts for the account)

## 2. Conflict: Conflict between lockout and admin exemption

Requirement R3 states that the system must lock the account when the number of failed attempts reaches 5. However, Requirement R5 states that the system must not lock the account if it belongs to an administrator. In the situation where an administrator account has exactly 5 failed attempts, the system is forced to both lock and not lock the account, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail to operate correctly for administrator accounts that reach the failure limit, as it cannot simultaneously satisfy the lockout rule and the exemption rule.
- **B) Change:** Modify Requirement R3 to explicitly exclude administrator accounts from the lockout condition, or modify Requirement R5 to specify that administrators are subject to a different security action instead of a lock.

*Proven:* Requirements R3, R5 cannot all be obeyed in this situation:
- TRUE: account_is_admin (The account has the administrator role)
- failed_attempt_count = 5 (The total number of consecutive failed login attempts for the account)

## 3. Conflict (if the assumed facts hold): Conflict between correct password and locked account

The requirements create a contradiction when a user enters the correct password for an account that is already locked. Requirement R1 states that the system must grant access when a correct password is submitted, while Requirement R4 states that the system must deny access when a password is submitted for a locked account. This conflict relies on the assumption that the system cannot both grant and deny access at the same time.

- **A) Keep as-is:** Keeping the requirements as written means the system is forced to perform two mutually exclusive actions simultaneously: granting access because the password is correct and denying access because the account is locked.
- **B) Change:** Modify Requirement R1 to state that the system grants access only if the password is correct AND the account is not locked, or modify Requirement R4 to specify that a correct password on a locked account should still result in denial, thereby establishing a clear priority.

*Proven:* Requirements R1, R4 cannot all be obeyed in this situation:
- TRUE: account_locked (The account is currently in a locked state)
- TRUE: password_is_correct (The submitted password matches the account's stored password)
- TRUE: user_submits_password (A user has submitted a password for login)
This depends on assumptions that are not stated in the requirements:
- F2: Access cannot be both granted and denied.

## 4. Gap: Undefined behavior for non-admin locked accounts

The requirements specify that an account is locked when failed attempts reach 5 (R3) and that access is denied if a password is submitted for a locked account (R4). However, there is no requirement stating what the system must do when a non-administrator account has more than 5 failed attempts but no new password submission is currently occurring. This leaves the system's state or action undefined in this specific scenario.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior is unspecified when a non-administrator account has exceeded the failure limit without an active login attempt.
- **B) Change:** Add a requirement stating that the system maintains the locked status of a non-administrator account as long as the failed attempt count is 5 or higher, regardless of whether a new password is submitted.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account has the administrator role)
- failed_attempt_count = 6 (The total number of consecutive failed login attempts for the account)
- FALSE: user_submits_password (A user has submitted a password for login)

## 5. Gap: Missing behavior for idle non-admin account

The requirements do not specify what the system must do when a non-administrator account has zero failed attempts and no password submission is occurring. This gap appears in the situation where the account is not an administrator, the failed attempt count is zero, and no password has been submitted.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific idle state is undefined and not constrained by any rule.
- **B) Change:** Add a requirement stating that when no password is submitted and the failed attempt count is zero, the system remains in a neutral state without granting or denying access.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account has the administrator role)
- failed_attempt_count = 0 (The total number of consecutive failed login attempts for the account)
- FALSE: user_submits_password (A user has submitted a password for login)

## 6. Gap: Undefined behavior for low failed attempts

The requirements do not specify what the system must do when an account has exactly one failed attempt and no password is currently being submitted. This gap appears in the situation where the account is not an administrator, the failed attempt count is 1, and no user has submitted a password.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific state is undefined and may vary or be untested.
- **B) Change:** Add a requirement stating that the system maintains the current failed attempt count and does not change the account status when no password is submitted and the failed attempt count is less than 5.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: account_is_admin (The account has the administrator role)
- failed_attempt_count = 1 (The total number of consecutive failed login attempts for the account)
- FALSE: user_submits_password (A user has submitted a password for login)
