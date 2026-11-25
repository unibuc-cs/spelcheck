# Requirements analysis: rules-for-next-season

41 requirements analysed: 4 conflict(s), 3 gap(s), 0 ambiguity(ies), 3 scenario(s) to confirm.

Change `rules-for-next-season`, checked against the specs that exist: 5 scenario(s) added, 2 modified, 3 removed (requirements removed: registration/Registration when full, registration/Transfers).

Shown are the findings that involve an added or modified rule (R7, R11, R19, R20, R21, R22, R25), and the gaps that a removed rule (X1, X2, X3) leaves open. 6 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict: Conflict between bib handout and payment status

The requirements contain a direct contradiction regarding what happens when a runner collects a bib while their entry fee is unpaid. Requirement R1 states that if a runner collects a bib and is cleared to start, the system must hand out the bib and timing chip. However, Requirement R22 states that if the entry fee is unpaid, the system must not hand out any bib. In the situation where a cleared runner with an unpaid fee collects a bib, the system is forced to both hand out the bib and not hand out the bib, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will encounter a logical error and fail to determine whether to hand out the bib or not when a cleared runner with an unpaid fee attempts to collect it.
- **B) Change:** Modify Requirement R1 to include a condition that the entry fee must be paid, or modify Requirement R22 to specify that the bib is withheld only if the runner is not cleared to start, thereby resolving the conflict.

*Proven:* Requirements R1, R22 cannot all be obeyed in this situation:
- TRUE: bib_collected (A runner is collecting a bib)
- TRUE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- TRUE: runner_cleared_to_start (The runner is cleared to start the race)

## 2. Conflict: Conflict between heat warning and start gate

Requirement R7 states that when a heat warning is in force, the system must not open any start gate. However, Requirement R3 states that when a start wave is called and the runner belongs to that wave, the system must open the start gate for the runner. In the situation where a heat warning is active and a runner from the called wave is present, the system is forced to both open and not open the gate, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail or behave unpredictably whenever a heat warning is active during a start wave, as it cannot simultaneously satisfy both R3 and R7.
- **B) Change:** Modify Requirement R3 to state that the system opens the start gate only if no heat warning is in force, or modify Requirement R7 to specify that it overrides R3, thereby resolving the conflict.

*Proven:* Requirements R3, R7 cannot all be obeyed in this situation:
- TRUE: heat_warning_in_force (A heat warning is in force)
- TRUE: runner_belongs_to_wave (The runner belongs to the called start wave)
- TRUE: start_wave_called (A start wave is called)

## 3. Conflict (if the assumed facts hold): Conflicting refund policies

The requirements contain a direct contradiction regarding what happens to the entry fee when a runner withdraws. Requirement R16 states that the system must refund the entry fee, while Requirement R21 states that the system must keep the entry fee. This conflict appears in the situation where a runner withdraws from the race, as the system cannot simultaneously refund and keep the same fee. This finding depends on the assumption that R21's instruction to keep the fee is interpreted as a prohibition against refunding it, which is the logical opposite of R16's instruction.

- **A) Keep as-is:** Keeping the requirements as written means the system is logically unable to determine whether to refund or keep the entry fee when a runner withdraws, leading to undefined behavior.
- **B) Change:** Remove Requirement R21 to ensure that the system consistently refunds the entry fee when a runner withdraws, as specified in Requirement R16.

*Proven:* Requirements R16, R21 cannot all be obeyed in this situation:
- TRUE: runner_withdrew (A runner withdraws from the race)
This depends on assumptions that are not stated in the requirements:
- F6: What R21 demands, in the terms of the other requirements: When a runner withdraws from the race, the system must not refund the entry fee.

## 4. Conflict (if the assumed facts hold): Registration vs. Unpaid Fee Conflict

The requirements contain a conflict that exists only if R12 is read as implying that the system hands out the bib upon registration. R12 states that when a runner registers and places are left, the system confirms the registration and assigns a bib number. However, R22 states that when the entry fee is unpaid, the system does not hand out any bib. In the situation where a runner registers with places available but has not yet paid, R12 requires the system to assign a bib number (which implies handing out the bib), while R22 forbids handing out the bib. This creates a direct contradiction in the system's required actions.

- **A) Keep as-is:** Keeping the requirements as written means the system is forced to both assign a bib number and refuse to hand out the bib simultaneously when a runner registers without paying, which is logically impossible to execute.
- **B) Change:** Modify R12 to state that the system confirms the registration and assigns a bib number only after the entry fee has been paid, or clarify that assigning a bib number is distinct from handing out the physical bib.

*Proven:* Requirements R12, R22 cannot all be obeyed in this situation:
- TRUE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- TRUE: places_left (Places are left for the race)
- TRUE: runner_registered (A runner registers for the race)
This depends on assumptions that are not stated in the requirements:
- F4: What R12 demands, in the terms of the other requirements: If a runner registers while places are still available, the system must confirm the registration for the new runner and hand out the bib.

## 5. Gap: Missing rule for unavailable pacer

The requirements specify what happens when a runner asks for a pacer and one is available (R11), but they do not state what the system must do when a runner asks for a pacer and no pacer for the target time is free. This gap appears in the situation where a runner requests a pacer while the specific pacer for their target time is not available.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a runner who requests a pacer when none is available for their target time.
- **B) Change:** Add a requirement stating that when a runner asks for a pacer and no pacer for the target time is free, the system informs the runner that no pacer is available or suggests an alternative target time.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner is collecting a bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner asks for a certificate)
- FALSE: certificate_uploaded (A runner uploads a medical certificate)
- FALSE: charity_place_requested (A runner asks for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner passes a checkpoint)
- chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner crosses the finish line)
- FALSE: finish_time_below_record (The finish time of a runner is below the course record)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: pacer_free (A pacer for the target time is free)
- TRUE: pacer_requested (A runner asks for a pacer)
- FALSE: payment_attempted (A runner pays the entry fee)
- FALSE: photo_requested (A runner asks for the finish photo)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: runner_dropped_out (A runner drops out of the race)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- FALSE: runner_registered (A runner registers for the race)
- FALSE: runner_withdrew (A runner withdraws from the race)
- FALSE: shift_finished (A volunteer finishes a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave is called)
- FALSE: time_corrected (A referee corrects a finish time)
- FALSE: tshirt_requested (A volunteer asks for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer checks in)
- FALSE: volunteer_signed_up (A volunteer signs up for a shift)
- FALSE: warning_received (A runner receives a warning from a referee)

## 6. Gap (opened by removing X2): Missing rule for rejected payment

The requirements do not specify what the system must do when a runner attempts to pay the entry fee and the payment is not accepted. This gap exists because a previous requirement that handled this specific scenario was removed.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for handling a rejected payment, leaving the runner without guidance or a next step.
- **B) Change:** Add a requirement stating that when a runner pays the entry fee and the payment is not accepted, the system asks for another payment method.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner is collecting a bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner asks for a certificate)
- FALSE: certificate_uploaded (A runner uploads a medical certificate)
- FALSE: charity_place_requested (A runner asks for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner passes a checkpoint)
- chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner crosses the finish line)
- FALSE: finish_time_below_record (The finish time of a runner is below the course record)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: pacer_requested (A runner asks for a pacer)
- FALSE: payment_accepted (The payment is accepted)
- TRUE: payment_attempted (A runner pays the entry fee)
- FALSE: photo_requested (A runner asks for the finish photo)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: runner_dropped_out (A runner drops out of the race)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- FALSE: runner_registered (A runner registers for the race)
- FALSE: runner_withdrew (A runner withdraws from the race)
- FALSE: shift_finished (A volunteer finishes a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave is called)
- FALSE: time_corrected (A referee corrects a finish time)
- FALSE: tshirt_requested (A volunteer asks for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer checks in)
- FALSE: volunteer_signed_up (A volunteer signs up for a shift)
- FALSE: warning_received (A runner receives a warning from a referee)
Before the change a requirement covered this situation, and the change removes it:
- X2: WHEN a runner pays the entry fee AND the payment is not accepted THEN the system asks for another payment method

## 7. Gap (opened by removing X1): Missing waiting list rule

The requirements do not specify what the system must do when a runner registers for the race and no places are left. This gap appears in the situation where a runner registers and no places are left, while all other race and volunteer events are not occurring.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for registering a runner when the race is full.
- **B) Change:** Add a requirement stating that when a runner registers and no places are left, the system puts the runner on the waiting list.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner is collecting a bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner asks for a certificate)
- FALSE: certificate_uploaded (A runner uploads a medical certificate)
- FALSE: charity_place_requested (A runner asks for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner passes a checkpoint)
- chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner crosses the finish line)
- FALSE: finish_time_below_record (The finish time of a runner is below the course record)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: pacer_requested (A runner asks for a pacer)
- FALSE: payment_attempted (A runner pays the entry fee)
- FALSE: photo_requested (A runner asks for the finish photo)
- FALSE: places_left (Places are left for the race)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: runner_dropped_out (A runner drops out of the race)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- TRUE: runner_registered (A runner registers for the race)
- FALSE: runner_withdrew (A runner withdraws from the race)
- FALSE: shift_finished (A volunteer finishes a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave is called)
- FALSE: time_corrected (A referee corrects a finish time)
- FALSE: tshirt_requested (A volunteer asks for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer checks in)
- FALSE: volunteer_signed_up (A volunteer signs up for a shift)
- FALSE: warning_received (A runner receives a warning from a referee)
Before the change a requirement covered this situation, and the change removes it:
- X1: WHEN a runner registers AND no places are left THEN the system puts the runner on the waiting list

## 8. Scenario, allowed: Unrequested charity reservation

Requirement R19 states that the system reserves a charity place only when a runner asks for one and the charity has places left. In this situation, the runner did not ask, and the charity had no places left, so the conditions for R19 were not met. However, the system still reserved a place, which directly contradicts the intent of the requirement to manage charity places based on explicit requests and availability.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement stating that the system SHALL NOT reserve a charity place unless a runner explicitly asks for it and the charity has places left.

*Proven:* The requirements allow this behaviour:
- FALSE: charity_place_requested (A runner asks for a charity place)
- TRUE: charity_place_reserved (The system reserves a charity place for the runner)
- FALSE: charity_places_left (The charity has places left)
Requirement R19 does not apply in it, and yet what R19 demands is the case.

## 9. Scenario, allowed: Warning shown without heat

Requirement R7 states that the system shows the warning at the start area only when a heat warning is in force. However, the requirements do not explicitly forbid showing the warning when no heat warning is in force. This allows the system to display a heat warning to runners even when the weather is safe, which could cause unnecessary confusion or alarm.

- **A) Keep as-is:** Keep the requirements, allowing the system to display the heat warning at the start area even when no heat warning is currently in force.
- **B) Change:** Add a requirement stating that the system SHALL NOT show the heat warning at the start area when a heat warning is not in force.

*Proven:* The requirements allow this behaviour:
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: start_gate_opened (The system opens the start gate for the runner)
- TRUE: warning_shown_at_start_area (The system shows the warning at the start area)
Requirement R7 does not apply in it, and yet what R7 demands is the case.

## 10. Scenario, allowed: Pacer assigned when none free

Requirement R11 states that the system assigns a pacer only when a pacer for the target time is free. The logic shows that the system can assign a pacer even when no pacer is free, which contradicts the condition set in the requirement. This defeats the purpose of managing pacer availability.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Change Requirement R11 to explicitly state that the system shall not assign a pacer if no pacer for the target time is free.

*Proven:* The requirements allow this behaviour:
- TRUE: pacer_assigned (The system assigns the pacer to the runner)
- FALSE: pacer_free (A pacer for the target time is free)
- TRUE: pacer_requested (A runner asks for a pacer)
Requirement R11 does not apply in it, and yet what R11 demands is the case.

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | race-day | Bib collection | Cleared to start |  |
| R2 | race-day | Bib collection | Not cleared to start |  |
| R3 | race-day | Start waves | Runner in the wave |  |
| R4 | race-day | Start waves | Runner in another wave |  |
| R5 | race-day | Checkpoints | Checkpoint passed |  |
| R6 | race-day | Cut-off | Cut-off time passed |  |
| R7 | race-day | Heat warning | Warning in force | **modified** |
| R8 | race-day | Drop-outs | Runner injured |  |
| R9 | race-day | Drop-outs | Runner not injured |  |
| R10 | race-day | Lost chips | Second lost chip |  |
| R11 | race-day | Pacers | Pacer free | **added** |
| R12 | registration | Registration with places left | Places left |  |
| X1 | registration | Registration when full | No places left | **removed** |
| R13 | registration | Medical certificate | Certificate valid |  |
| R14 | registration | Medical certificate | Certificate not valid |  |
| R15 | registration | Payment | Payment accepted |  |
| X2 | registration | Payment | Payment not accepted | **removed** |
| R16 | registration | Withdrawal | Runner withdraws |  |
| R17 | registration | Payment deadline | Second missed deadline |  |
| X3 | registration | Transfers | Registration transferred | **removed** |
| R18 | registration | Club discount | Club member |  |
| R19 | registration | Charity places | Charity place free | **added** |
| R20 | registration | Charity places | Charity full | **added** |
| R21 | registration | No refunds | Fee kept | **added** |
| R22 | registration | Unpaid fees | Fee unpaid | **added** |
| R23 | results | Finish times | Runner finishes |  |
| R24 | results | Protests | Protest open |  |
| R25 | results | Certificates | Result final | **modified** |
| R26 | results | Certificates | Result not final |  |
| R27 | results | Age groups | Results final |  |
| R28 | results | Disqualification | Third warning |  |
| R29 | results | Photos | Photo available |  |
| R30 | results | Photos | Photo not available |  |
| R31 | results | Records | Course record |  |
| R32 | results | Time corrections | Time corrected |  |
| R33 | volunteers | Sign-up | Shift has places |  |
| R34 | volunteers | Sign-up | Shift full |  |
| R35 | volunteers | Check-in | Shift today |  |
| R36 | volunteers | Check-in | No shift today |  |
| R37 | volunteers | No-shows | Second missed shift |  |
| R38 | volunteers | Meals | Shift finished |  |
| R39 | volunteers | Briefing | Briefing started |  |
| R40 | volunteers | T-shirts | Size in stock |  |
| R41 | volunteers | T-shirts | Size not in stock |  |
