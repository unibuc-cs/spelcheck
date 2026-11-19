# Requirements analysis: delete_property

5 requirements analysed: 0 conflict(s), 2 gap(s), 1 ambiguity(ies). Review of the text: 2 note(s).

## 1. Ambiguity: Ambiguous Scope of Soft Deletion

Requirement D4 is unclear about when the platform must retain records and hide them from the interface. One reading suggests this is a general rule that always applies, while the other suggests it only applies after a deletion is finished. In the situation where no deletion has occurred, the property is visible, and the record is missing, these two interpretations lead to different conclusions about whether the requirement is violated. Which did you mean?

- **A) Keep as-is:** Keep the requirement as a general rule that Property records must always be retained in the database and hidden from the user interface, regardless of whether a deletion has occurred.
- **B) Change:** Reword the requirement to state that only after a Property deletion is completed must the record be retained in the database and hidden from the user interface.

*Proven:* Requirement D4 has no single clear meaning (independent translations split 4/4).
Reading 1: The Platform must ensure that Property records are retained in the database while being hidden from the user interface to support soft deletion for audit purposes. [in logic: true => (and property_record_retained_in_db property_hidden_from_ui)]
Reading 2: When the deletion process for a Property is completed, the Property record must remain in the database and be hidden from the user interface. [in logic: property_deleted => (and property_record_retained_in_db property_hidden_from_ui)]
The readings differ in this situation:
- FALSE: property_deleted (The deletion process for the Property has been completed)
- FALSE: property_hidden_from_ui (The Property is not visible in the user interface)
- FALSE: property_record_retained_in_db (The Property record remains present in the database)

## 2. Gap: Missing behavior for non-deletion state

The requirements only define the system's behavior when a deletion is initiated, confirmed, or completed. They do not specify what the Platform must do when none of these deletion actions have occurred, leaving the system's state undefined in this scenario.

- **A) Keep as-is:** Keeping the requirements as written means the Platform has no specified behavior or obligation when a Property Owner is not actively deleting a Property.
- **B) Change:** Add a requirement stating that the Platform SHALL display the standard properties list or dashboard when no deletion process is active.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_attempted (A Property Owner has attempted to delete a Property)
- FALSE: deletion_confirmed (The Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- FALSE: property_deleted (The deletion process for the Property has been completed)

## 3. Gap: Missing behavior for uninitiated deletion

The requirements define actions for when a deletion is initiated, confirmed, or completed, but they do not specify what the system must do when a property belongs to a user and no deletion process has been started or finished. This gap appears in the situation where the property is validly owned by the user, yet no deletion has been initiated, confirmed, or completed.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a user who has a valid property but has not yet started or finished deleting it, leaving the system's response undefined in this state.
- **B) Change:** Add a requirement stating that when a Property belongs to a User Account and no deletion process has been initiated, the Platform SHALL display the Property in the user interface and allow the Property Owner to initiate deletion.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_confirmed (The Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- TRUE: property_belongs_to_user (The Property being deleted is associated with the User Account of the actor)
- FALSE: property_deleted (The deletion process for the Property has been completed)

## Review of the text (not proven)

The model's reading of the requirements as written. These notes are a judgement, not a proof.

### 4. Review (contradiction): Removal vs Retention

D2 states the Platform SHALL "remove the Property record from the Platform", while D4 states the Platform SHALL "retain Property records in the database". These requirements demand incompatible outcomes for the same action: the record cannot be both removed and retained.

- **A) Keep as-is:** The system would fail to meet D4 because the record is removed, or fail D2 because the record is retained, making the requirement untestable as written.
- **B) Change:** Rewrite D2 as: "WHEN a Property Owner confirms deletion, THE Platform SHALL mark the Property as deleted so that it is no longer visible in the user interface"

*Review, not proven:* the reviewing model's reading of requirements D2, D4.

### 5. Review (wording): Implementation Prescribed

The requirement prescribes a specific implementation technique ("implement soft deletion") and internal storage state ("retain Property records in the database") rather than observable behavior. A tester cannot verify the internal database state or the specific technique used, only the visible effect.

- **A) Keep as-is:** The system could use hard deletion or a different retention mechanism and still pass the test if the tester only checks the UI, but the requirement explicitly demands a specific internal implementation that is not observable.
- **B) Change:** Rewrite D4 as: "WHEN a Property is deleted, THE Platform SHALL ensure the Property data is retained for audit purposes and is not visible in the user interface"

*Review, not proven:* the reviewing model's reading of requirements D4.
