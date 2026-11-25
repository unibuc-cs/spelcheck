# Requirements analysis: rules-for-next-season

41 requirements analysed: 3 conflict(s), 3 gap(s), 0 ambiguity(ies), 3 scenario(s) to confirm.

Change `rules-for-next-season`, checked against the specs that exist: 5 scenario(s) added, 2 modified, 3 removed (requirements removed: registration/Registration when full, registration/Transfers).

Shown are the findings that involve an added or modified rule (N1, N2, N3, N4, N5, N6, N7), and the gaps that a removed rule (R12, R16, R19) leaves open. 7 other finding(s), among the existing requirements alone, are in findings.json.

## 1. Conflict: Conflict between bib handout and unpaid fee

Requirement R1 states that when a runner collects the bib and is cleared to start, the system must hand out the bib and the timing chip. However, Requirement N6 states that when the entry fee is unpaid, the system must not hand out any bib. In the situation where a runner has collected the bib, is cleared to start, but has not paid the entry fee, the system is forced to both hand out the bib and not hand out the bib, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will encounter a logical error and fail to function correctly whenever a cleared runner with an unpaid fee attempts to collect their bib.
- **B) Change:** Modify Requirement R1 to include the condition that the entry fee is paid, so that the bib is only handed out when the fee is settled, or modify Requirement N6 to specify that the bib is withheld only if the fee is unpaid at the moment of collection, resolving the direct contradiction.

*Proven:* Requirements R1, N6 cannot all be obeyed in this situation:
- TRUE: bib_collected (A runner has collected the bib)
- TRUE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- TRUE: runner_cleared_to_start (The runner is cleared to start)

## 2. Conflict: Conflict between heat warning and start gate

The requirements contain a direct contradiction regarding the start gate. Requirement R3 states that when a start wave is called and the runner belongs to that wave, the system must open the start gate for the runner. However, requirement N1 states that when a heat warning is in force, the system must not open any start gate. In the situation where a heat warning is active and a runner from the called wave is present, the system is required to both open and not open the gate, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail or behave unpredictably when a heat warning is active during a start wave, as it cannot simultaneously satisfy the command to open the gate and the prohibition against opening it.
- **B) Change:** Modify requirement R3 to include an exception, such as: 'WHEN a start wave is called AND the runner belongs to the wave AND no heat warning is in force THEN the system opens the start gate for the runner'.

*Proven:* Requirements R3, N1 cannot all be obeyed in this situation:
- TRUE: heat_warning_in_force (A heat warning is in force)
- TRUE: runner_belongs_to_wave (The runner belongs to the called start wave)
- TRUE: start_wave_called (A start wave has been called)

## 3. Conflict (if the assumed facts hold): Conflicting refund policies

The requirements contain a direct contradiction regarding what happens to the entry fee when a runner withdraws. Requirement R17 states that the system must refund the entry fee, while Requirement N5 states that the system must keep the entry fee. This conflict appears in the situation where a runner has withdrawn from the race, as the system cannot simultaneously refund and keep the same fee. This finding depends on the assumption that Requirement N5's instruction to "keep the entry fee" is interpreted as a prohibition against refunding it, which is the logical opposite of the action required by R17.

- **A) Keep as-is:** Keeping the requirements as written means the system is logically unable to process a withdrawal because it is instructed to perform two mutually exclusive actions with the same money.
- **B) Change:** Remove Requirement N5 to allow Requirement R17 to stand alone, ensuring that the entry fee is refunded when a runner withdraws.

*Proven:* Requirements R17, N5 cannot all be obeyed in this situation:
- TRUE: runner_withdrew (A runner has withdrawn from the race)
This depends on assumptions that are not stated in the requirements:
- F12: What N5 demands, in the terms of the other requirements: When a runner withdraws from the race, the system must not refund the entry fee.

## 4. Gap (opened by removing R16): Missing rule for rejected payment

The requirements do not specify what the system must do when a runner pays the entry fee but the payment is not accepted. This gap appears in the situation where the entry fee is paid but the payment is not accepted, and no other conditions like missed deadlines or unpaid fees apply.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for handling a rejected payment, leaving the runner without guidance on how to proceed.
- **B) Change:** Add a requirement stating that when a runner pays the entry fee and the payment is not accepted, the system asks for another payment method.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner has collected the bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner has asked for a certificate)
- FALSE: charity_place_requested (A runner has asked for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner has passed a checkpoint)
- TRUE: entry_fee_paid (A runner has paid the entry fee)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner has crossed the finish line)
- FALSE: finish_photo_requested (A runner has asked for the finish photo)
- FALSE: finish_time_below_course_record (The finish time of a runner is below the course record)
- FALSE: finish_time_corrected (A referee has corrected a finish time)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: medical_certificate_uploaded (A runner has uploaded a medical certificate)
- FALSE: pacer_requested (A runner has asked for a pacer)
- FALSE: payment_accepted (The payment is accepted)
- payment_deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: referee_warning_received (A runner has received a warning from a referee)
- FALSE: runner_dropped_out (A runner has dropped out)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- FALSE: runner_registered (A runner has registered)
- FALSE: runner_withdrew (A runner has withdrawn from the race)
- FALSE: shift_finished (A volunteer has finished a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave has been called)
- timing_chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- FALSE: tshirt_requested (A volunteer has asked for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer has checked in)
- FALSE: volunteer_signed_up (A volunteer has signed up for a shift)
Before the change a requirement covered this situation, and the change removes it:
- R16: WHEN a runner pays the entry fee AND the payment is not accepted THEN the system asks for another payment method

## 5. Gap: Missing rule for unavailable pacer

The requirements specify what happens when a runner asks for a pacer and one is available (N2), but they do not state what the system must do when a runner asks for a pacer and no pacer for the target time is free. This gap appears in the situation where a runner has asked for a pacer, but a pacer for the target time is not free.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a runner who requests a pacer when none are available for their target time.
- **B) Change:** Add a requirement stating that when a runner asks for a pacer and a pacer for the target time is not free, the system informs the runner that no pacer is available or offers an alternative target time.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner has collected the bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner has asked for a certificate)
- FALSE: charity_place_requested (A runner has asked for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner has passed a checkpoint)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner has crossed the finish line)
- FALSE: finish_photo_requested (A runner has asked for the finish photo)
- FALSE: finish_time_below_course_record (The finish time of a runner is below the course record)
- FALSE: finish_time_corrected (A referee has corrected a finish time)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: medical_certificate_uploaded (A runner has uploaded a medical certificate)
- FALSE: pacer_free (A pacer for the target time is free)
- TRUE: pacer_requested (A runner has asked for a pacer)
- FALSE: payment_accepted (The payment is accepted)
- payment_deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: referee_warning_received (A runner has received a warning from a referee)
- FALSE: runner_dropped_out (A runner has dropped out)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- FALSE: runner_registered (A runner has registered)
- FALSE: runner_withdrew (A runner has withdrawn from the race)
- FALSE: shift_finished (A volunteer has finished a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave has been called)
- timing_chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- FALSE: tshirt_requested (A volunteer has asked for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer has checked in)
- FALSE: volunteer_signed_up (A volunteer has signed up for a shift)

## 6. Gap (opened by removing R12): Missing waiting list rule

The requirements do not specify what the system must do when a runner registers while no places are left. This gap appears in the situation where a runner has registered and no places are left, as the previous rule covering this scenario was removed.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for registering runners when the race is full.
- **B) Change:** Add a requirement stating that when a runner registers and no places are left, the system puts the runner on the waiting list.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: bib_collected (A runner has collected the bib)
- FALSE: briefing_started (The briefing of a shift has started)
- FALSE: certificate_requested (A runner has asked for a certificate)
- FALSE: charity_place_requested (A runner has asked for a charity place)
- FALSE: checkpoint_cutoff_passed (The cut-off time of a checkpoint has passed)
- FALSE: checkpoint_passed (A runner has passed a checkpoint)
- FALSE: entry_fee_unpaid (The entry fee of a runner is unpaid)
- FALSE: finish_line_crossed (A runner has crossed the finish line)
- FALSE: finish_photo_requested (A runner has asked for the finish photo)
- FALSE: finish_time_below_course_record (The finish time of a runner is below the course record)
- FALSE: finish_time_corrected (A referee has corrected a finish time)
- FALSE: heat_warning_in_force (A heat warning is in force)
- FALSE: medical_certificate_uploaded (A runner has uploaded a medical certificate)
- FALSE: pacer_requested (A runner has asked for a pacer)
- FALSE: payment_accepted (The payment is accepted)
- payment_deadline_missed_count = 0 (The number of times the runner has missed the payment deadline)
- FALSE: places_left (Places are left for the race)
- FALSE: protest_open (A protest against a result is open)
- FALSE: race_results_final (The results of the race are final)
- FALSE: referee_warning_received (A runner has received a warning from a referee)
- FALSE: runner_dropped_out (A runner has dropped out)
- FALSE: runner_is_club_member (The runner is a member of a running club)
- TRUE: runner_registered (A runner has registered)
- FALSE: runner_withdrew (A runner has withdrawn from the race)
- FALSE: shift_finished (A volunteer has finished a shift)
- shift_missed_count = 0 (The number of times the volunteer has missed a shift)
- FALSE: start_wave_called (A start wave has been called)
- timing_chip_lost_count = 0 (The number of times the runner has lost a timing chip)
- FALSE: tshirt_requested (A volunteer has asked for a T-shirt)
- FALSE: volunteer_checked_in (A volunteer has checked in)
- FALSE: volunteer_signed_up (A volunteer has signed up for a shift)
Before the change a requirement covered this situation, and the change removes it:
- R12: WHEN a runner registers AND no places are left THEN the system puts the runner on the waiting list

## 7. Scenario, allowed: Unrequested Pacer Assignment

Requirement N2 states that the system assigns a pacer only when a runner asks for one and a pacer is free. The logic allows the system to assign a pacer even when no request has been made, provided a pacer is available. This defeats the purpose of the requirement, which is to provide pacers based on runner demand, and could lead to unnecessary resource allocation or confusion for runners who did not request assistance.

- **A) Keep as-is:** Keep the requirements, allowing the system to assign pacers to runners even without a specific request if a pacer is free.
- **B) Change:** Modify Requirement N2 to explicitly state that the system SHALL NOT assign a pacer unless a runner has asked for one.

*Proven:* The requirements allow this behaviour:
- TRUE: pacer_assigned (The system has assigned the pacer to the runner)
- TRUE: pacer_free (A pacer for the target time is free)
- FALSE: pacer_requested (A runner has asked for a pacer)
Requirement N2 does not apply in it, and yet what N2 demands is the case.

## 8. Scenario, allowed: Unrequested charity reservation

The requirements allow the system to reserve a charity place for a runner even when the runner has not asked for one and the charity has no places left. This defeats the purpose of the charity place requirement, which is to offer places only when requested and available, and contradicts the logic that a reservation should only happen when places are left.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement that the system SHALL NOT reserve a charity place unless the runner has asked for it and the charity has places left.

*Proven:* The requirements allow this behaviour:
- FALSE: charity_place_requested (A runner has asked for a charity place)
- TRUE: charity_place_reserved (The system has reserved a charity place for the runner)
- FALSE: charity_places_left (The charity has places left)
Requirement N3 does not apply in it, and yet what N3 demands is the case.

## 9. Scenario, allowed: Unsolicited charity proposal

Requirement N4 states that the system should propose another charity only when a runner asks for a charity place and the current charity has no places left. In this situation, the system performs the action demanded by N4 (proposing another charity) even though the runner did not ask for a place. This suggests the system might be spamming runners with charity offers without their consent, which is likely not intended.

- **A) Keep as-is:** Keep the requirements, allowing the system to propose charities even if the runner did not explicitly ask for a place.
- **B) Change:** Modify Requirement N4 to explicitly state that the system shall not propose another charity unless the runner has actively requested a charity place.

*Proven:* The requirements allow this behaviour:
- TRUE: another_charity_proposed (The system has proposed another charity to the runner)
- FALSE: charity_place_requested (A runner has asked for a charity place)
- FALSE: charity_places_left (The charity has places left)
Requirement N4 does not apply in it, and yet what N4 demands is the case.

## The rules, by label

| Rule | Spec | Requirement | Scenario | |
|---|---|---|---|---|
| R1 | race-day | Bib collection | Cleared to start |  |
| R2 | race-day | Bib collection | Not cleared to start |  |
| R3 | race-day | Start waves | Runner in the wave |  |
| R4 | race-day | Start waves | Runner in another wave |  |
| R5 | race-day | Checkpoints | Checkpoint passed |  |
| R6 | race-day | Cut-off | Cut-off time passed |  |
| N1 | race-day | Heat warning | Warning in force | **modified** |
| R8 | race-day | Drop-outs | Runner injured |  |
| R9 | race-day | Drop-outs | Runner not injured |  |
| R10 | race-day | Lost chips | Second lost chip |  |
| N2 | race-day | Pacers | Pacer free | **added** |
| R11 | registration | Registration with places left | Places left |  |
| R12 | registration | Registration when full | No places left | **removed** |
| R13 | registration | Medical certificate | Certificate valid |  |
| R14 | registration | Medical certificate | Certificate not valid |  |
| R15 | registration | Payment | Payment accepted |  |
| R16 | registration | Payment | Payment not accepted | **removed** |
| R17 | registration | Withdrawal | Runner withdraws |  |
| R18 | registration | Payment deadline | Second missed deadline |  |
| R19 | registration | Transfers | Registration transferred | **removed** |
| R20 | registration | Club discount | Club member |  |
| N3 | registration | Charity places | Charity place free | **added** |
| N4 | registration | Charity places | Charity full | **added** |
| N5 | registration | No refunds | Fee kept | **added** |
| N6 | registration | Unpaid fees | Fee unpaid | **added** |
| R21 | results | Finish times | Runner finishes |  |
| R22 | results | Protests | Protest open |  |
| N7 | results | Certificates | Result final | **modified** |
| R24 | results | Certificates | Result not final |  |
| R25 | results | Age groups | Results final |  |
| R26 | results | Disqualification | Third warning |  |
| R27 | results | Photos | Photo available |  |
| R28 | results | Photos | Photo not available |  |
| R29 | results | Records | Course record |  |
| R30 | results | Time corrections | Time corrected |  |
| R31 | volunteers | Sign-up | Shift has places |  |
| R32 | volunteers | Sign-up | Shift full |  |
| R33 | volunteers | Check-in | Shift today |  |
| R34 | volunteers | Check-in | No shift today |  |
| R35 | volunteers | No-shows | Second missed shift |  |
| R36 | volunteers | Meals | Shift finished |  |
| R37 | volunteers | Briefing | Briefing started |  |
| R38 | volunteers | T-shirts | Size in stock |  |
| R39 | volunteers | T-shirts | Size not in stock |  |
