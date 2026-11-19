# Requirements analysis: delete_property

5 requirements analysed: 0 conflict(s), 2 gap(s), 0 ambiguity(ies). Review of the text: 1 note(s).

## 1. Gap: Missing behavior for non-deletion states

The requirements only define system actions when a deletion is initiated, confirmed, or completed. They do not specify what the system must do when none of these deletion steps have occurred, leaving the system's behavior undefined in this state.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior or obligation when a Property Owner is not in the process of deleting a Property.
- **B) Change:** Add a requirement stating that when a Property Owner is not attempting to delete a Property, the system shall display the standard property details or list view without any deletion prompts or errors.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_attempted (A Property Owner has attempted to delete a Property)
- FALSE: deletion_confirmed (The Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- FALSE: property_deleted (The Property has been successfully deleted)

## 2. Gap: Missing behavior for uninitiated deletion

The requirements define actions for when a deletion is initiated, confirmed, or attempted on a property that does not belong to the owner. However, they do not specify what the system must do when a property belongs to the owner but the deletion process has not been started or confirmed. This gap means the system's behavior in this specific state is undefined.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined obligation to perform any specific action when a property belongs to the owner but no deletion has been initiated or confirmed.
- **B) Change:** Add a requirement stating that when a property belongs to the owner and no deletion has been initiated, the system shall display the property in the user interface and allow the owner to initiate the deletion process.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: deletion_confirmed (The Property Owner has confirmed the deletion)
- FALSE: deletion_initiated (A Property Owner has initiated the property deletion process)
- TRUE: property_belongs_to_owner (The Property belongs to the User Account of the Property Owner attempting the deletion)
- FALSE: property_deleted (The Property has been successfully deleted)

## Review of the text (not proven)

The model's reading of the requirements as written. These notes are a judgement, not a proof.

### 3. Review (wording): Vague audit retention

The requirement states that data is "retained for audit purposes" but does not define what this means observably. A tester cannot verify if the data is actually retained or how long, nor can they distinguish between soft deletion and hard deletion based on this text alone.

- **A) Keep as-is:** Keep as written, accepting that "retained for audit purposes" is a non-testable design goal rather than a specific behavioral constraint.
- **B) Change:** Rewrite D4 as: "WHEN a Property is deleted, THE Platform SHALL retain the Property record in the database with a status indicating deletion, ensuring it is not visible in the user interface but remains accessible to authorized audit roles."

*Review, not proven:* the reviewing model's reading of requirements D4.
