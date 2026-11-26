# Requirements analysis: add-express-shipping

9 requirements analysed: 3 conflict(s) (2 doubtful), 1 gap(s), 0 ambiguity(ies).

Change `add-express-shipping`, checked against the specs that exist: 2 scenario(s) added, 0 modified, 0 removed.

Shown are the findings that involve an added or modified rule (R6, R7). 3 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict (if the assumed facts hold): Express requests and signoff conflict

The requirements state that if an express request is handled, no signoff request is made (R6), but if a parcel ships successfully in a run with a plan, a signoff must have been approved earlier (R2). In the situation described, an express request is handled in a run with a plan where a parcel ships successfully, which creates a contradiction because the successful shipment requires a prior signoff that the express handling forbids. This conflict depends on the assumption that the successful shipment in a planned run strictly requires a prior approved signoff as defined by R2.

- **A) Keep as-is:** Keeping the requirements as written means that it is impossible to successfully ship a parcel in a run with a plan if that run also handles an express request.
- **B) Change:** Modify R6 to state that when an express request is handled, request_signoff is not called only if no parcel shipping call succeeds in the run, or modify R2 to exclude runs where express requests are handled from the signoff requirement.

*Proven:* Requirements R2, R6 cannot all be obeyed in this situation:
- TRUE: express_request_handled (An express request is handled in the run)
- TRUE: run_has_plan (The current run has a plan)
- TRUE: ship_parcel_succeeded (A call to ship_parcel has succeeded)
This depends on assumptions that are not stated in the requirements:
- F5: What R2 demands, in the terms of the other requirements: If a parcel shipping call succeeds during a run that has a plan, it implies that a request for signoff was previously made and approved within that run.

## 2. Conflict (if the assumed facts hold, doubtful: the situation says more than the example does): Conflicting shipping instructions

The requirements state that when Dana asks to ship parcel k7 with a complete address, the system must call the shipping function once for that parcel. However, when Dana sends an express request for parcels k1, k2, and k3, the system must make the shipping function succeed three times. This conflict appears in the situation where Dana sends an express request for k1, k2, and k3, and the address for k7 is complete. This finding may be a false alarm because the requirements are examples of specific cases, and the situation described includes details that do not necessarily trigger both requirements simultaneously.

- **A) Keep as-is:** Keeping the requirements as written means that if Dana sends an express request for k1, k2, and k3 while the address for k7 is complete, the system faces a contradiction between calling the shipping function once for k7 and making it succeed three times for the group.
- **B) Change:** Modify R4 to specify that it applies only when the request is not part of an express batch, or modify R7 to clarify how individual parcel addresses are handled within an express request to ensure the shipping function is called the correct number of times.

*Proven:* Requirements R4, R7 cannot all be obeyed in this situation:
- TRUE: address_complete (The address of the parcel is complete)
- TRUE: express_request_received (An express request is received)
- parcel_id = k7 (The identifier of the parcel in the request)
- request_parcel_ids = k1_k2_k3 (The set of parcel identifiers in the express request)
- TRUE: requester_is_dana (The requester is dana)
- TRUE: ship_request_received (A request to ship a parcel is received)
This depends on assumptions that are not stated in the requirements:
- F8: What R4 and R7 demand cannot both be the case: A function cannot succeed three times if it is called only once.
But R4, R7 are examples, one concrete case each, and what each describes does not make the other requirement(s) apply: this situation says more than they do. So the conflict may be a false alarm.

## 3. Conflict (if the assumed facts hold, doubtful: the situation says more than the example does): Conflict between express shipment and state stability

The requirements state that when dana sends an express request for parcels k1, k2, and k3, the shipment must succeed (R7), and that when a parcel is found, its state must not change during that call (R9). This conflict appears in the situation where dana sends an express request for those specific parcels and a parcel lookup succeeds. This finding depends on the unstated assumption that a successful parcel shipment necessarily involves a change in the parcel's state. However, because R7 describes a specific example case rather than a general rule, and the situation described does not explicitly force the other requirements to apply in a way that creates a logical impossibility, this conflict may be a false alarm.

- **A) Keep as-is:** Keep the requirements as written, accepting that the specific scenario in R7 might not trigger the state-change prohibition in R9 if the shipment process is distinct from the find_parcel call.
- **B) Change:** Clarify R9 to specify that the state prohibition applies only to the find_parcel call itself and not to subsequent actions like shipping, or clarify R7 to ensure the shipment process does not rely on state changes that would violate R9.

*Proven:* Requirements R7, R9 cannot all be obeyed in this situation:
- TRUE: express_request_received (An express request is received)
- TRUE: find_parcel_succeeded (A call to find_parcel has succeeded)
- request_parcel_ids = k1_k2_k3 (The set of parcel identifiers in the express request)
- TRUE: requester_is_dana (The requester is dana)
This depends on assumptions that are not stated in the requirements:
- F9: What R7 and R9 demand cannot both be the case: A successful parcel shipment necessarily involves a change in the parcel's state.
But R7 is an example, one concrete case, and what it describes does not make the other requirement(s) apply: this situation says more than it does. So the conflict may be a false alarm.

## 4. Gap: Unspecified behavior for received express request

The requirements do not specify what the system must do when an express request is received but is not yet being handled in a run. This gap appears in the situation where an express request is received, but no express request is handled, and no other specific actions like shipping or signoff have occurred.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior for a received express request that is not yet handled is undefined and may vary.
- **B) Change:** Add a requirement stating that when an express request is received, the system must immediately begin handling it in a run or provide a specific acknowledgment response.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: configuration_checked (The system is checking the configuration)
- FALSE: express_request_handled (An express request is handled in the run)
- TRUE: express_request_received (An express request is received)
- FALSE: find_parcel_succeeded (A call to find_parcel has succeeded)
- FALSE: request_signoff_refused (A call to request_signoff returned a refusal)
- FALSE: requester_is_dana (The requester is dana)
- FALSE: ship_parcel_succeeded (A call to ship_parcel has succeeded)
- FALSE: ship_request_received (A request to ship a parcel is received)

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | shipping | Parcel limit | The parcel limit is configured |  |
| R2 | shipping | Sign-off before shipping | No shipping in a plan without a sign-off |  |
| R3 | shipping | Refusal | A refusal stops the plan |  |
| R4 | shipping | Requests | Example: a parcel with a complete address |  |
| R5 | shipping | Requests | Example: the postcode is missing |  |
| R6 | shipping | Express shipping | An express run asks nobody | **added** |
| R7 | shipping | Express shipping | Example: three express parcels | **added** |
| R8 | shipping-audit | Audit | Every shipment is audited |  |
| R9 | shipping-audit | Lookups | A lookup changes nothing |  |
