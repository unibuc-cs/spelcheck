# Requirements analysis: delete_property_links

5 requirements analysed with 3 symbol sets: 1 conflict(s), 2 gap(s), 2 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity (found with 3 of 3 symbol sets): Ambiguous Scope of Soft Deletion

Requirement D4 is ambiguous because it is unclear whether the platform must retain records and hide them from the interface only after a deletion is completed, or if it must always retain records and hide them from the interface regardless of the deletion status. This difference appears in the situation where no deletion has occurred, the property is visible, and the record is not in the database. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying that the platform only needs to ensure records are retained and hidden from the interface once a property deletion is completed.
- **B) Change:** Reword the requirement to state that the platform must always retain property records in the database and hide them from the user interface to support audit purposes, regardless of whether a deletion has been initiated or completed.

*Proven:* Requirement D4 has no single clear meaning (independent translations split 5/3).
Reading 1: The platform must implement soft deletion by ensuring that when a property deletion is completed, the property record remains present in the database and is not visible in the user interface. [in logic: property_deleted => (and property_record_retained_in_db property_hidden_from_ui)]
Reading 2: The system must retain property records in the database and hide them from the user interface to implement soft deletion for audit purposes. [in logic: true => (and property_record_retained_in_db property_hidden_from_ui)]
The readings differ in this situation:
- FALSE: property_deleted (The deletion process for the Property has been completed)
- FALSE: property_hidden_from_ui (The Property is not visible in the user interface)
- FALSE: property_record_retained_in_db (The Property record remains present in the database)

## 2. Ambiguity (found with 1 of 3 symbol sets): Ambiguity in Deletion Definition

Requirement D2 is unclear about what "remove the Property record" means. One reading requires that the record be physically erased from the database, while the other only requires that the property be considered deleted (which, per D4, allows the record to remain in the database). Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, implying that confirming deletion must physically erase the record from the database.
- **B) Change:** Reword D2 to state that the Platform must mark the Property as deleted, allowing the record to remain in the database for audit purposes.

*Proven:* Requirement D2 has no single clear meaning (independent translations split 4/4).
Reading 1: If a Property Owner confirms the deletion of a property, the platform must remove the property record from the platform. [in logic: deletion_confirmed => (not property_record_in_database)]
Reading 2: When a Property Owner confirms the deletion of a property, the Platform must ensure that the property is successfully deleted. [in logic: deletion_confirmed => property_deleted]
The readings differ in this situation:
- TRUE: deletion_confirmed (The Property Owner has confirmed the deletion)
- TRUE: property_deleted (The Property has been successfully deleted from the Platform)
- TRUE: property_record_in_database (The Property record is retained in the database)

## 3. Conflict (found with 3 of 3 symbol sets): Conflict between removal and retention

Requirement D2 states that the Platform must remove the Property record from the Platform once deletion is confirmed. However, Requirement D4 mandates that the Platform must retain Property records in the database for audit purposes. These two requirements cannot be satisfied simultaneously because a record cannot be both removed and retained in the same state.

- **A) Keep as-is:** Keeping the requirements as written means the system is logically impossible to build because it must both delete and keep the same data.
- **B) Change:** Change Requirement D2 to state that the Platform shall mark the Property as deleted rather than removing the record, aligning it with the soft deletion strategy in D4.

*Proven:* Requirements D2, D4 cannot all be obeyed in this situation:
- TRUE: deletion_confirmed (The Property Owner has confirmed the deletion)
- TRUE: property_deleted (The Property has been successfully deleted from the Platform)

## 4. Gap: Missing behavior for non-deletion state

The requirements define specific actions only for scenarios where a deletion is initiated, confirmed, or completed. However, there is no requirement stating what the system must do when none of these deletion steps have occurred, leaving the system's behavior undefined for the standard state where no deletion is taking place.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior or obligation when a user is not actively trying to delete a property.
- **B) Change:** Add a requirement stating that the Platform SHALL display the standard property details or list view when no deletion process has been initiated.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_attempted (A Property Owner has attempted to delete a Property)
- FALSE: deletion_confirmed (A Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- FALSE: property_deleted (The deletion process for the Property has been completed)

## 5. Gap: Undefined state for owned property

The requirements define actions for initiating, confirming, or completing deletion, but they do not specify what the system must do when a property is owned by the user and no deletion action has been taken. This gap appears in the situation where the property belongs to the user, but the deletion process has not been initiated, confirmed, or completed.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a property that is owned by the user but is not currently undergoing a deletion process.
- **B) Change:** Add a requirement stating that the Platform SHALL display the property in the user's list and allow the user to view or edit it when no deletion process has been initiated.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_confirmed (A Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- TRUE: property_belongs_to_user (The Property being deleted belongs to the User Account of the Property Owner)
- FALSE: property_deleted (The deletion process for the Property has been completed)

## 6. Scenario, allowed (found with 3 of 3 symbol sets): Deletion without confirmation

Requirement D2 states that the Platform SHALL remove the Property record only WHEN a Property Owner confirms deletion. The consequence shows that the record is removed even though the confirmation did not happen. This directly violates the intent of D2 and D1, which require user confirmation before any removal occurs, making this a clear failure of the stated goal.

- **A) Keep as-is:** Keep the requirements as they are, accepting that the system might delete properties without user confirmation.
- **B) Change:** Modify Requirement D2 to explicitly state that the Property record SHALL NOT be removed unless the deletion has been confirmed by the Property Owner.

*Proven:* The requirements allow this behaviour:
- FALSE: deletion_confirmed (A Property Owner has confirmed the deletion)
- TRUE: property_record_removed (The Property record is removed from the Platform's active data set)
Requirement D2 does not apply in it, and yet what D2 demands is the case.

## 7. Scenario, allowed (found with 3 of 3 symbol sets): False Deletion Confirmation

The requirements allow the system to show a success message and redirect the user even though the property deletion has not actually finished. This is likely not intended because D3 requires these actions only when a Property is deleted, and showing a success message for a failed or incomplete operation would mislead the user into thinking the property was removed when it was not.

- **A) Keep as-is:** Keep the requirements, allowing the platform to display a confirmation and redirect even if the deletion process is not fully complete.
- **B) Change:** Modify D3 to explicitly state that the confirmation message and redirect SHALL only occur after the deletion process has been successfully completed.

*Proven:* The requirements allow this behaviour:
- TRUE: confirmation_message_displayed (The Platform displays a message confirming the deletion)
- FALSE: property_deleted (The deletion process for the Property has been completed)
- TRUE: redirected_to_properties_list (The Platform redirects the user to the properties list view)
Requirement D3 does not apply in it, and yet what D3 demands is the case.

## 8. Scenario, allowed (found with 3 of 3 symbol sets): Spurious Authorization Error

The requirements allow the system to deny a deletion and show an authorization error even when no deletion attempt has been made. This is likely not intended because D5 specifies that the error should only appear when a Property Owner attempts to delete a property that does not belong to them, implying a user action must trigger the check.

- **A) Keep as-is:** Keep the requirements, allowing the system to display authorization errors and deny deletions without a preceding user attempt.
- **B) Change:** Modify D5 to explicitly state that the authorization check and error display only occur after a valid deletion initiation by a Property Owner.

*Proven:* The requirements allow this behaviour:
- TRUE: authorization_error_displayed (The Platform displays an error message indicating an authorization failure)
- FALSE: deletion_attempted (A Property Owner has attempted to delete a Property)
- TRUE: deletion_denied (The Platform denies the deletion request)
- FALSE: property_belongs_to_user (The Property being deleted belongs to the User Account of the Property Owner)
Requirement D5 does not apply in it, and yet what D5 demands is the case.
