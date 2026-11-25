# Requirements analysis: topup_reading

4 requirements analysed: 0 conflict(s), 4 gap(s), 1 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity: Ambiguity in PIN lock trigger

Requirement R4 is ambiguous because it is unclear whether the account must be locked for exactly 24 hours only when the third wrong PIN is entered, or whenever the count of consecutive wrong PINs is three or more. In the situation where a customer has entered a wrong PIN for the fourth time and the account is locked for 25 hours, the two readings of R4 differ in whether the requirement applies. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the system must lock the account for 24 hours specifically when the count of consecutive wrong PIN entries reaches three.
- **B) Change:** Reword the requirement to state that the system must lock the account for 24 hours whenever the count of consecutive wrong PIN entries is at least three.

*Proven:* Requirement R4 has no single clear meaning. Shown both readings and the situation below, and asked whether the words decide between them, the answers were: 3 for reading 1, 4 for reading 2, 1 'either'.
Reading 1: If the customer enters a wrong PIN and the count of consecutive wrong entries reaches three, the system must lock the account and set the lock duration to 24 hours. [in logic: (and wrong_pin_entered (= wrong_pin_count 3)) => (and account_locked (= lock_duration_hours 24))]
Reading 2: The system locks the account for 24 hours if the customer enters a wrong PIN and the count of consecutive wrong entries is at least three. [in logic: (and wrong_pin_entered (>= wrong_pin_count 3)) => (and account_locked (= lock_duration_hours 24))]
The readings differ in this situation:
- TRUE: account_locked (The customer's account is locked)
- lock_duration_hours = 25 (The duration in hours for which the account is locked)
- wrong_pin_count = 4 (The number of consecutive wrong PIN entries by the customer)
- TRUE: wrong_pin_entered (A customer enters an incorrect PIN)
With reading 2 instead of reading 1: a requirement applies in 1 of the gaps reported below.

## 2. Gap: Missing rule for failed credit purchase

The requirements do not specify what the system must do when a customer attempts to buy credit but the payment is not accepted. This gap appears in the situation where the balance is 2 euros, a credit purchase is initiated, the payment is rejected, and no wrong PIN is entered.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for handling a failed credit purchase, leaving the outcome of the transaction and any user feedback unspecified.
- **B) Change:** Add a requirement stating that when a customer buys credit and the payment is not accepted, the system must notify the customer of the failure and not alter the balance.

*Proven:* No requirement says what the system must do in this situation:
- balance = 2 (The current credit balance of the customer in euros)
- TRUE: customer_buys_credit (A customer initiates a purchase of credit)
- FALSE: payment_accepted (The payment for the credit purchase is accepted)
- FALSE: wrong_pin_entered (A customer enters an incorrect PIN)

## 3. Gap: Unspecified behavior for accepted payment without purchase

The requirements do not specify what the system must do when a payment for credit is accepted but no customer is actually buying credit. This gap appears in the situation where the balance is 2 euros, no purchase is initiated, yet the payment is accepted, and no wrong PIN has been entered.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific scenario is undefined and may vary or fail unpredictably.
- **B) Change:** Add a requirement stating that if a payment is accepted but no credit purchase is initiated, the system must reject the payment or notify the customer of the error.

*Proven:* No requirement says what the system must do in this situation:
- balance = 2 (The current credit balance of the customer in euros)
- FALSE: customer_buys_credit (A customer initiates a purchase of credit)
- TRUE: payment_accepted (The payment for the credit purchase is accepted)
- FALSE: wrong_pin_entered (A customer enters an incorrect PIN)

## 4. Gap (depends on the reading of R4): Unclear PIN lock trigger

The requirements do not specify what the system must do when a customer enters a wrong PIN for the fourth time. This gap exists only if R4 is read to mean the account locks strictly when the count reaches three; the other reading is that the account locks whenever a wrong PIN is entered and the count of consecutive wrong entries is at least three.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined action for the fourth wrong PIN entry, leaving the account state undefined in this scenario.
- **B) Change:** Change R4 to state that the system locks the account for 24 hours whenever a customer enters a wrong PIN and the count of consecutive wrong entries is three or more.

*Proven:* No requirement says what the system must do in this situation:
- balance = 2 (The current credit balance of the customer in euros)
- FALSE: payment_accepted (The payment for the credit purchase is accepted)
- wrong_pin_count = 4 (The number of consecutive wrong PIN entries by the customer)
- TRUE: wrong_pin_entered (A customer enters an incorrect PIN)
But R4 is ambiguous (see its finding). With its other reading a requirement applies in this situation. That reading: The system locks the account for 24 hours if the customer enters a wrong PIN and the count of consecutive wrong entries is at least three.

## 5. Gap (no event happens): Undefined behavior at 2 euro balance

The requirements do not specify what the system must do when the balance is exactly 2 euros and no other triggering events are occurring. This gap appears in the situation where the balance is 2 euros, no credit purchase is happening, and no wrong PIN has been entered. This finding may be a false alarm because no event happens in this situation, so it likely just means the system waits.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined action to take when the balance is exactly 2 euros and no other events are occurring.
- **B) Change:** Add a requirement stating that the system does nothing when the balance is exactly 2 euros and no other triggering events are occurring.

*Proven:* No requirement says what the system must do in this situation:
- balance = 2 (The current credit balance of the customer in euros)
- FALSE: customer_buys_credit (A customer initiates a purchase of credit)
- FALSE: payment_accepted (The payment for the credit purchase is accepted)
- FALSE: wrong_pin_entered (A customer enters an incorrect PIN)
No event happens in this situation, so this may only mean that the system waits.

## 6. Scenario, allowed: Credit added without customer purchase

The requirements allow the system to add credit to a balance and send a confirmation text even when the customer has not initiated a purchase, provided the payment is accepted. This defeats the purpose of the top-up process, which is to add credit only when a customer actively buys it, and could lead to unauthorized or erroneous credit additions.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Modify R1 to explicitly state that the system adds credit and sends a text message only when a customer initiates a purchase and the payment is accepted.

*Proven:* The requirements allow this behaviour:
- TRUE: credit_added_to_balance (The system adds the purchased credit to the customer's balance)
- FALSE: customer_buys_credit (A customer initiates a purchase of credit)
- TRUE: payment_accepted (The payment for the credit purchase is accepted)
- TRUE: text_message_sent (The system sends a text message to the customer)
Requirement R1 does not apply in it, and yet what R1 demands is the case.

## 7. Scenario, allowed: Call ended without active call

Requirement R3 states that the system ends a call only when the balance reaches zero during a call. In this situation, the balance is 1.50 euros (not zero) and no call is in progress, yet the system ends a call. This behavior is not required by R3 and contradicts the condition that a call must be in progress and the balance must be zero for the call to be ended.

- **A) Keep as-is:** Keep the requirements as they are, allowing the system to end a call even when no call is in progress and the balance is not zero.
- **B) Change:** Modify Requirement R3 to explicitly state that the system shall not end a call unless a call is currently in progress and the balance has reached zero.

*Proven:* The requirements allow this behaviour:
- balance = 1/2 (The current credit balance of the customer in euros)
- TRUE: call_ended (The system ends the current call)
- FALSE: call_in_progress (A call is currently in progress for the customer)
Requirement R3 does not apply in it, and yet what R3 demands is the case.

## 8. Scenario, allowed: Lock without wrong PIN entry

The requirements state that the account is locked for 24 hours only when a customer enters a wrong PIN for the third time. However, the logic allows a state where the account is locked for 24 hours with a wrong PIN count of 3, even though no incorrect PIN was actually entered in that specific instance. This contradicts the causal link intended by the security requirement, as the lock should be a direct result of the wrong entry.

- **A) Keep as-is:** Keep the requirements, accepting that the account can be locked for 24 hours with a wrong PIN count of 3 even if no incorrect PIN is currently being entered.
- **B) Change:** Modify Requirement R4 to explicitly state that the account is locked only if the third wrong PIN entry has just occurred, or clarify that the lock state persists only as a direct consequence of the third wrong entry.

*Proven:* The requirements allow this behaviour:
- TRUE: account_locked (The customer's account is locked)
- lock_duration_hours = 24 (The duration in hours for which the account is locked)
- wrong_pin_count = 3 (The number of consecutive wrong PIN entries by the customer)
- FALSE: wrong_pin_entered (A customer enters an incorrect PIN)
Requirement R4 does not apply in it, and yet what R4 demands is the case.
