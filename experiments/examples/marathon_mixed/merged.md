# race-day Specification

## Purpose

The start, the course and the finish on the day of the race.

## Requirements

### Requirement: Bib collection

The system SHALL hand out bibs before the race.

#### Scenario R1: Cleared to start

- **WHEN** a runner collects the bib
- **AND** the runner is cleared to start
- **THEN** the system hands out the bib and the timing chip

#### Scenario R2: Not cleared to start

- **WHEN** a runner collects the bib
- **AND** the runner is not cleared to start
- **THEN** the system sends the runner to the medical desk

### Requirement: Start waves

The system SHALL start the runners in waves.

#### Scenario R3: Runner in the wave

- **WHEN** a start wave is called
- **AND** the runner belongs to the wave
- **THEN** the system opens the start gate for the runner

#### Scenario R4: Runner in another wave

- **WHEN** a start wave is called
- **AND** the runner does not belong to the wave
- **THEN** the system shows the runner the right wave

### Requirement: Checkpoints

The system SHALL time the runners on the course.

#### Scenario R5: Checkpoint passed

- **WHEN** a runner passes a checkpoint
- **THEN** the system records the split time of the runner

### Requirement: Cut-off

The system SHALL close the checkpoints in time.

#### Scenario R6: Cut-off time passed

- **WHEN** the cut-off time of a checkpoint has passed
- **THEN** the system closes the checkpoint

### Requirement: Heat warning

The system SHALL warn the runners of heat.

#### Scenario R7: Warning in force

- **WHEN** a heat warning is in force
- **THEN** the system shows the warning at the start area and does not open any start gate

### Requirement: Drop-outs

The system SHALL look after runners who drop out.

#### Scenario R8: Runner injured

- **WHEN** a runner drops out
- **AND** the runner is injured
- **THEN** the system calls the medical team

#### Scenario R9: Runner not injured

- **WHEN** a runner drops out
- **AND** the runner is not injured
- **THEN** the system sends the sweep bus

### Requirement: Lost chips

The system SHALL act on lost timing chips.

#### Scenario R10: Second lost chip

- **WHEN** a runner loses a timing chip for the second time
- **THEN** the system charges the runner for the chip

### Requirement: Pacers

The system SHALL give runners a pacer for their target time.

#### Scenario R11: Pacer free

- **WHEN** a runner asks for a pacer
- **AND** a pacer for the target time is free
- **THEN** the system assigns the pacer to the runner

# registration Specification

## Purpose

Runners register for a city marathon and pay the entry fee.

## Requirements

### Requirement: Registration with places left

The system SHALL register a runner while places are left.

#### Scenario R12: Places left

- **WHEN** a runner registers
- **AND** places are left
- **THEN** the system confirms the registration and assigns a bib number

### Requirement: Registration when full

The system SHALL keep a waiting list when the race is full.

#### Scenario X1: No places left

- **WHEN** a runner registers
- **AND** no places are left
- **THEN** the system puts the runner on the waiting list

### Requirement: Medical certificate

The system SHALL check the medical certificate of a runner.

#### Scenario R13: Certificate valid

- **WHEN** a runner uploads a medical certificate
- **AND** the certificate is valid
- **THEN** the system marks the runner as cleared to start

#### Scenario R14: Certificate not valid

- **WHEN** a runner uploads a medical certificate
- **AND** the certificate is not valid
- **THEN** the system asks the runner for a new certificate

### Requirement: Payment

The system SHALL take the entry fee.

#### Scenario R15: Payment accepted

- **WHEN** a runner pays the entry fee
- **AND** the payment is accepted
- **THEN** the system sends the runner a receipt

#### Scenario X2: Payment not accepted

- **WHEN** a runner pays the entry fee
- **AND** the payment is not accepted
- **THEN** the system asks for another payment method

### Requirement: Withdrawal

The system SHALL let runners withdraw.

#### Scenario R16: Runner withdraws

- **WHEN** a runner withdraws from the race
- **THEN** the system refunds the entry fee

### Requirement: Payment deadline

The system SHALL act on runners who do not pay in time.

#### Scenario R17: Second missed deadline

- **WHEN** a runner misses the payment deadline for the second time
- **THEN** the system cancels the registration of the runner

### Requirement: Transfers

The system SHALL let a runner pass the registration on.

#### Scenario X3: Registration transferred

- **WHEN** a runner transfers the registration to another runner
- **THEN** the system sends the new runner a confirmation

### Requirement: Club discount

The system SHALL give a discount to the members of running clubs.

#### Scenario R18: Club member

- **WHEN** a runner is a member of a running club
- **THEN** the system applies the club discount to the entry fee

### Requirement: Charity places

The system SHALL offer places that are sold through a charity.

#### Scenario R19: Charity place free

- **WHEN** a runner asks for a charity place
- **AND** the charity has places left
- **THEN** the system reserves a charity place for the runner

#### Scenario R20: Charity full

- **WHEN** a runner asks for a charity place
- **AND** the charity has no places left
- **THEN** the system proposes another charity to the runner

### Requirement: No refunds

The system SHALL keep the fees of runners who withdraw.

#### Scenario R21: Fee kept

- **WHEN** a runner withdraws from the race
- **THEN** the system keeps the entry fee

### Requirement: Unpaid fees

The system SHALL hold back the bibs of runners who have not paid.

#### Scenario R22: Fee unpaid

- **WHEN** the entry fee of a runner is unpaid
- **THEN** the system does not hand out any bib

# results Specification

## Purpose

Times, rankings and certificates after the race.

## Requirements

### Requirement: Finish times

The system SHALL publish the times of the runners.

#### Scenario R23: Runner finishes

- **WHEN** a runner crosses the finish line
- **THEN** the system publishes the finish time of the runner

### Requirement: Protests

The system SHALL hold back results that are under protest.

#### Scenario R24: Protest open

- **WHEN** a protest against a result is open
- **THEN** the system does not publish any finish time

### Requirement: Certificates

The system SHALL send certificates to runners.

#### Scenario R25: Result final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is final
- **THEN** the system sends the certificate by email and adds the split times

#### Scenario R26: Result not final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is not final
- **THEN** the system tells the runner the date of the final results

### Requirement: Age groups

The system SHALL rank the runners.

#### Scenario R27: Results final

- **WHEN** the results of the race are final
- **THEN** the system ranks the runners in their age groups

### Requirement: Disqualification

The system SHALL act on the warnings of the referees.

#### Scenario R28: Third warning

- **WHEN** a runner receives a warning from a referee for the third time
- **THEN** the system disqualifies the runner

### Requirement: Photos

The system SHALL give runners their finish photo.

#### Scenario R29: Photo available

- **WHEN** a runner asks for the finish photo
- **AND** the photo is available
- **THEN** the system sends the runner a link to the photo

#### Scenario R30: Photo not available

- **WHEN** a runner asks for the finish photo
- **AND** the photo is not available
- **THEN** the system tells the runner when the photos will be ready

### Requirement: Records

The system SHALL announce records.

#### Scenario R31: Course record

- **WHEN** the finish time of a runner is below the course record
- **THEN** the system announces a new course record

### Requirement: Time corrections

The system SHALL tell runners when their time is corrected.

#### Scenario R32: Time corrected

- **WHEN** a referee corrects a finish time
- **THEN** the system informs the runner of the new time

# volunteers Specification

## Purpose

Volunteers sign up for shifts and work at the race.

## Requirements

### Requirement: Sign-up

The system SHALL assign volunteers to shifts.

#### Scenario R33: Shift has places

- **WHEN** a volunteer signs up for a shift
- **AND** the shift has places left
- **THEN** the system assigns the volunteer to the shift

#### Scenario R34: Shift full

- **WHEN** a volunteer signs up for a shift
- **AND** the shift has no places left
- **THEN** the system offers the volunteer another shift

### Requirement: Check-in

The system SHALL check volunteers in.

#### Scenario R35: Shift today

- **WHEN** a volunteer checks in
- **AND** the volunteer has a shift on that day
- **THEN** the system prints the volunteer badge

#### Scenario R36: No shift today

- **WHEN** a volunteer checks in
- **AND** the volunteer has no shift on that day
- **THEN** the system shows the volunteer the date of the next shift

### Requirement: No-shows

The system SHALL act on volunteers who do not turn up.

#### Scenario R37: Second missed shift

- **WHEN** a volunteer misses a shift for the second time
- **THEN** the system removes the volunteer from the remaining shifts

### Requirement: Meals

The system SHALL feed the volunteers.

#### Scenario R38: Shift finished

- **WHEN** a volunteer finishes a shift
- **THEN** the system issues a meal voucher

### Requirement: Briefing

The system SHALL guide volunteers to their briefing.

#### Scenario R39: Briefing started

- **WHEN** the briefing of a shift has started
- **THEN** the system shows the briefing room on the volunteer screens

### Requirement: T-shirts

The system SHALL give every volunteer a T-shirt.

#### Scenario R40: Size in stock

- **WHEN** a volunteer asks for a T-shirt
- **AND** the size is in stock
- **THEN** the system hands out the T-shirt

#### Scenario R41: Size not in stock

- **WHEN** a volunteer asks for a T-shirt
- **AND** the size is not in stock
- **THEN** the system notes the size for the next delivery
