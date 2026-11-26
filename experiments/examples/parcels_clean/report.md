# Requirements analysis: add-returns

11 requirements analysed: 2 conflict(s) (2 doubtful), 1 gap(s), 0 ambiguity(ies), 2 scenario(s) to confirm.

Change `add-returns`, checked against the specs that exist: 4 scenario(s) added, 0 modified, 0 removed.

Shown are the findings that involve an added or modified rule (R8, R9, R10, R11). 2 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict (if the assumed facts hold, doubtful: the situation says more than the example does): Conflicting Requests for Same Parcel

The requirements state that if Dana asks to ship parcel k7 and the address has no postcode, the system must not call the shipping function (R5). However, if Dana asks to return parcel k7 and it was delivered, the system must call the return booking function (R8). The finding indicates that these two requirements cannot be obeyed simultaneously in a single run where both a ship request and a return request are received for the same parcel. This conflict may be a false alarm because it relies on the unstated assumption that a single run cannot be both a ship request and a return request; if the system processes these as separate, distinct runs, the conflict does not exist.

- **A) Keep as-is:** Keep the requirements as written, accepting that the system must handle ship and return requests as separate, non-overlapping runs to avoid the conflict.
- **B) Change:** Add a requirement stating that a single run cannot contain both a ship request and a return request for the same parcel, or clarify that R5 and R8 apply to mutually exclusive request types.

*Proven:* Requirements R5, R8 cannot all be obeyed in this situation:
- TRUE: parcel_delivered (The requested parcel was delivered)
- parcel_id = k7 (The identifier of the parcel in the request)
- TRUE: postcode_missing (The address of the requested parcel has no postcode)
- TRUE: return_request_received (Dana asks to return a parcel)
- TRUE: ship_request_received (Dana asks to ship a parcel)
This depends on assumptions that are not stated in the requirements:
- F7: What R5 and R8 demand cannot both be the case: A single run cannot be both a ship request and a return request.
But R5, R8 are examples, one concrete case each, and what each describes does not make the other requirement(s) apply: this situation says more than they do. So the conflict may be a false alarm.

## 2. Conflict (if the assumed facts hold, doubtful: the situation says more than the example does): Conflicting return rules

The requirements state that if a parcel is still in the warehouse, the return booking function is never called, but they also state that if the customer cancels the return, the return booking function is called once. This creates a contradiction because the system cannot both never call the function and call it once in the same scenario. This finding may be a false alarm because the requirements describe specific, separate cases that might not be intended to apply simultaneously to a single request.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail or behave unpredictably if a customer cancels a return for a parcel that is still in the warehouse.
- **B) Change:** Modify R10 to specify that the return booking function is only called if the parcel has been delivered, or clarify that the cancellation rule only applies after a successful return booking.

*Proven:* Requirements R9, R10 cannot all be obeyed in this situation:
- TRUE: customer_cancels_return (The customer cancels the return)
- parcel_id = k7 (The identifier of the parcel in the request)
- TRUE: parcel_in_warehouse (The requested parcel is still in the warehouse)
- TRUE: return_request_received (Dana asks to return a parcel)
This depends on assumptions that are not stated in the requirements:
- F8: What R9 and R10 demand cannot both be the case: The system cannot both not call book_return and have a book_return call count of 1.
But R9, R10 are examples, one concrete case each, and what each describes does not make the other requirement(s) apply: this situation says more than they do. So the conflict may be a false alarm.

## 3. Gap: Missing rule for returning other parcels

The requirements only specify what happens when Dana asks to return parcel k7. They do not state what the system must do when Dana asks to return any other parcel. This gap appears in the situation where Dana asks to return a parcel that is not k7, while no other specific conditions are met.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for return requests involving parcels other than k7.
- **B) Change:** Add a requirement stating that when Dana asks to return any parcel other than k7, the system must call book_return once and provide a return label.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: book_return_succeeded (A call to book_return has succeeded)
- FALSE: configuration_checked (The system is checking the configuration)
- FALSE: customer_cancels_return (The customer cancels the return)
- FALSE: find_parcel_succeeded (A call to find_parcel has succeeded)
- parcel_id = other (The identifier of the parcel in the request)
- TRUE: return_request_received (Dana asks to return a parcel)
- FALSE: ship_parcel_succeeded (A call to ship_parcel has succeeded)
- FALSE: signoff_refused (A call to request_signoff returned a refusal)

## 4. Scenario, allowed: Return label without request

The requirements allow a scenario where a return label is provided and a return is booked, even though Dana never asked for a return and the parcel was not delivered. This defeats the purpose of Requirement R8, which is to handle return requests only when they are explicitly made by the user for delivered parcels.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement that a return label is only provided and a return is only booked if Dana explicitly asks to return a delivered parcel.

*Proven:* The requirements allow this behaviour:
- TRUE: answer_gives_return_label (The answer to the return request gives the return label)
- book_return_call_count = 1 (The number of times book_return is called for the requested parcel)
- FALSE: parcel_delivered (The requested parcel was delivered)
- parcel_id = other (The identifier of the parcel in the request)
- FALSE: return_request_received (Dana asks to return a parcel)
Requirement R8 does not apply in it, and yet what R8 demands is the case.

## 5. Scenario, allowed: Spurious return cancellation

Requirement R10 specifies that a return should be booked and then cancelled only when the customer cancels the return. However, the requirements allow the system to perform both the booking and the cancellation even when the customer has not cancelled, which defeats the purpose of the cancellation logic and creates an inconsistent state where a return is processed and immediately voided without user intent.

- **A) Keep as-is:** Keep the requirements, allowing the system to book and cancel returns even when the customer has not explicitly cancelled.
- **B) Change:** Modify Requirement R10 to explicitly state that `cancel_return` SHALL NOT be called unless the customer cancels the return, or add a requirement that `cancel_return` is only called in response to a customer cancellation.

*Proven:* The requirements allow this behaviour:
- book_return_call_count = 1 (The number of times book_return is called for the requested parcel)
- cancel_return_call_count = 1 (The number of times cancel_return is called)
- FALSE: customer_cancels_return (The customer cancels the return)
Requirement R10 does not apply in it, and yet what R10 demands is the case.

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | shipping | Parcel limit | The parcel limit is configured |  |
| R2 | shipping | Sign-off before shipping | No shipping in a plan without a sign-off |  |
| R3 | shipping | Refusal | A refusal stops the plan |  |
| R4 | shipping | Requests | Example: a parcel with a complete address |  |
| R5 | shipping | Requests | Example: the postcode is missing |  |
| R6 | shipping-audit | Audit | Every shipment is audited |  |
| R7 | shipping-audit | Lookups | A lookup changes nothing |  |
| R8 | shipping-audit | Returns | Example: a return is booked | **added** |
| R9 | shipping-audit | Returns | Example: the parcel was never delivered | **added** |
| R10 | shipping-audit | Returns | Example: the customer cancels | **added** |
| R11 | shipping-audit | Return audit | Every return is audited | **added** |
