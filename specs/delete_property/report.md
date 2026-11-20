# Requirements analysis: delete_property

5 requirements analysed: 1 conflict(s) (1 doubtful), 1 gap(s), 1 ambiguity(ies), 2 scenario(s) to confirm.

## 1. Ambiguity: Ambiguous scope of soft deletion

Requirement D4 is unclear about when the platform must keep property records in the database and hide them from the user interface. One reading says this must happen only after a property has been successfully deleted, while the other says the platform must always keep records in the database and hide them from the user interface, regardless of whether a deletion has occurred. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the platform must retain property records in the database and hide them from the user interface only after a property deletion is successfully completed.
- **B) Change:** Reword the requirement to state that the platform must always retain property records in the database and hide them from the user interface, regardless of whether a deletion has occurred.

*Proven:* Requirement D4 has no single clear meaning (independent translations split 3/3/1/1).
Reading 1: When a property deletion is successfully completed, the property record must be retained in the database and hidden from the user interface. [in logic: property_deleted => (and property_record_retained_in_db property_hidden_from_ui)]
Reading 2: The Platform must implement a mechanism where property records are retained in the database while being hidden from the user interface. [in logic: true => (and property_record_retained_in_db property_hidden_from_ui)]
The readings differ in this situation:
- FALSE: property_deleted (The Property has been successfully deleted)
- FALSE: property_hidden_from_ui (The Property is hidden from the user interface)
- FALSE: property_record_retained_in_db (The Property record is retained in the database)
It was left out of the conflict and gap checks and should be rewritten.

## 2. Conflict (if the assumed facts hold, doubtful: needs two events at the same moment): Conflict between deletion confirmation and ownership check

The requirements create a conflict because D2 requires the Platform to remove the Property record once deletion is confirmed, while D5 requires the Platform to deny deletion if the Property does not belong to the User Account. This conflict appears in the situation where a Property Owner initiates and confirms the deletion of a Property that is not associated with their User Account. This finding depends on the assumption that D5 requires the Platform to prevent the logical removal of the Property record in this specific case. However, this situation requires the initiation and confirmation of the deletion to happen at the same moment, which the requirements are probably not meant for, so the conflict may be a false alarm.

- **A) Keep as-is:** Keeping the requirements as written means the Platform must remove the Property record upon confirmation even if the Property does not belong to the User Account, which violates the authorization rule in D5.
- **B) Change:** Propose a change to D2 to state that the Platform SHALL remove the Property record only if the Property belongs to the User Account of the Property Owner, ensuring the ownership check in D5 is respected before removal.

*Proven:* Requirements D2, D5 cannot all be obeyed in this situation:
- TRUE: deletion_confirmed (A Property Owner has confirmed the deletion)
- TRUE: deletion_initiated (A Property Owner has initiated the property deletion process)
- FALSE: property_owned_by_user (The Property belongs to the User Account of the Property Owner)
This depends on assumptions that are not stated in the requirements:
- F1: What D5 demands, in the terms of the other requirements: If a Property Owner initiates the deletion process for a Property that is not associated with their User Account, the Platform must prevent the logical removal of the Property record.
But this situation needs these events to happen at the same moment: deletion_confirmed, deletion_initiated. The requirements are probably not meant for that, so the conflict may be a false alarm.

## 3. Gap (no event happens): Idle System State

The requirements define actions only for specific triggers, such as initiating or confirming a deletion. In the situation where none of these actions have occurred, the system is simply in a waiting state. This finding indicates that no specific behavior is mandated for this idle state, which is typically expected for a system at rest.

- **A) Keep as-is:** Keeping the requirements as written means the system performs no specific action when no deletion process has been started or confirmed.
- **B) Change:** No change is necessary, as the system is expected to remain in its default state until a user initiates an action.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_confirmed (A Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- FALSE: property_deleted (The Property has been successfully deleted)
No event happens in this situation, so this may only mean that the system waits.

## 4. Scenario, allowed: Deletion without confirmation

Requirement D2 explicitly states that the Platform SHALL remove the Property record only WHEN a Property Owner confirms deletion. The fact that the record is removed while the confirmation status is false directly violates the condition set by D2. This defeats the purpose of the confirmation prompt in D1, which is to prevent accidental or unauthorized deletions.

- **A) Keep as-is:** Keep the requirements, accepting that the system might delete properties without user confirmation.
- **B) Change:** Refine Requirement D2 to explicitly state that the Property record SHALL NOT be removed unless the deletion has been confirmed by the Property Owner.

*Proven:* The requirements allow this behaviour:
- FALSE: deletion_confirmed (A Property Owner has confirmed the deletion)
- TRUE: property_record_removed (The Property record is removed from the Platform (logically deleted))
Requirement D2 does not apply in it, and yet what D2 demands is the case.

## 5. Scenario, allowed: False success message on failed deletion

The requirements allow the system to show a success message and redirect the user even when the property deletion has not actually occurred. This is likely not intended because D3 links the confirmation message to the event of a property being deleted, implying the message should only appear after a successful deletion, not when it fails.

- **A) Keep as-is:** Keep the requirements, allowing the platform to display a success message and redirect even if the deletion did not succeed.
- **B) Change:** Modify D3 to explicitly state that the confirmation message and redirect SHALL only occur if the property deletion is successful.

*Proven:* The requirements allow this behaviour:
- TRUE: confirmation_message_displayed (The Platform displays a confirmation message indicating successful deletion)
- FALSE: property_deleted (The Property has been successfully deleted)
- TRUE: redirected_to_properties_list (The Platform redirects the user to the properties list)
Requirement D3 does not apply in it, and yet what D3 demands is the case.
