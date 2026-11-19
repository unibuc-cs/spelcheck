# Requirements analysis: delete_property_found

5 requirements analysed: 1 conflict(s), 2 gap(s), 1 ambiguity(ies).

Assumed domain facts. The model proposed them from the meaning of the words; the requirements do not state them. They are used only to look for more conflicts, and a conflict that depends on one says so.

- F1: A property record cannot be both removed and retained at the same time. (7/8 samples agree)

## 1. Ambiguity: Ambiguous soft deletion scope

Requirement D4 is ambiguous because it is unclear whether the system must retain property records for audit purposes only when soft deletion is implemented, or whenever a property is successfully deleted. In the situation where a property has not been successfully deleted and the record is not retained, the two interpretations of the requirement lead to different expectations for system behavior. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the system must ensure property records are retained for audit purposes specifically when implementing soft deletion, regardless of whether a deletion action has occurred.
- **B) Change:** Reword the requirement to state that the system must ensure property records are retained in the database for audit purposes whenever a property is successfully deleted.

*Proven:* Requirement D4 has no single clear meaning (independent translations split 4/4).
Reading 1: The system must ensure that property records are retained for audit purposes when implementing soft deletion. [in logic: true => property_record_retained]
Reading 2: The system must ensure that property records are retained in the database for audit purposes when a property is successfully deleted. [in logic: property_deleted => property_record_retained]
The readings differ in this situation:
- FALSE: property_deleted (The property has been successfully deleted from the system.)
- FALSE: property_record_retained (The property record still exists in the database for audit purposes.)

## 2. Conflict (if the assumed facts hold): Conflict between removal and retention

Requirement D2 states that the system must remove the Property record when the owner confirms deletion, while Requirement D4 states that the system must retain Property records for audit purposes. These two requirements cannot both be obeyed in the situation where the owner confirms the deletion, assuming that a property record cannot be both removed and retained at the same time.

- **A) Keep as-is:** Keeping the requirements as written means the system must simultaneously remove the record and retain it, which is impossible under the assumption that a record cannot be in both states at once.
- **B) Change:** Change Requirement D2 to state that the system shall mark the Property record as deleted rather than removing it, ensuring the record is retained for audit purposes as required by D4.

*Proven:* Requirements D2, D4 cannot all be obeyed in this situation:
- TRUE: deletion_confirmed (The user has confirmed the deletion action.)
- TRUE: user_is_owner (The user making the request is the owner of the property.)
This depends on assumptions that are not stated in the requirements:
- F1: A property record cannot be both removed and retained at the same time.

## 3. Gap: Missing behavior for non-owner without request

The requirements define actions for when a deletion is requested or attempted, but they do not specify what the system should do when a non-owner is interacting with a property without having submitted a deletion request. This gap appears in the situation where no deletion request exists, the property remains intact, and the user is not the owner.

- **A) Keep as-is:** Keeping the requirements as written means the system's behavior in this specific state is undefined and may vary or be unhandled.
- **B) Change:** Add a requirement stating that if a user who is not the owner views a property without requesting deletion, the system shall display the property details normally or restrict access based on standard viewing permissions.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_requested (The user has submitted a request to delete a property.)
- FALSE: property_deleted (The property has been successfully deleted from the system.)
- FALSE: user_is_owner (The user making the request is the owner of the property.)

## 4. Gap: Missing behavior for normal state

The requirements define specific actions for when a deletion is requested, confirmed, or completed, but they do not specify what the system should do when none of these events have occurred. This gap appears in the situation where no deletion request has been made, no confirmation has been given, and no property has been deleted.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for the standard state where no deletion process is active.
- **B) Change:** Add a requirement stating that the system shall display the standard property details or list view when no deletion request is active.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_confirmed (The user has confirmed the deletion action.)
- FALSE: deletion_requested (The user has submitted a request to delete a property.)
- FALSE: property_deleted (The property has been successfully deleted from the system.)
