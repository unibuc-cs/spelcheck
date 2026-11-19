# Refined requirements: delete_property

The requirements of the analysed document with the proposals of the review applied.
Amended: D4. Added: none.

- D1: WHEN a Property Owner initiates property deletion, THE Platform SHALL prompt for confirmation before proceeding
- D2: WHEN a Property Owner confirms deletion, THE Platform SHALL mark the Property as deleted so that it is no longer visible in the user interface
- D3: WHEN a Property is deleted, THE Platform SHALL display a confirmation message and redirect to the properties list
- D4: WHEN a Property is deleted, THE Platform SHALL retain the Property record in the database with a status indicating deletion, ensuring it is not visible in the user interface but remains accessible to authorized audit roles.
- D5: WHEN a Property Owner attempts to delete a Property that does not belong to their User Account, THE Platform SHALL deny the deletion and display an authorization error message
