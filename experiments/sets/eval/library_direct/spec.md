# Requirements: Library

## Requirement 1

**User Story:** As a library member, I want to borrow and return books, so that I can read them at home.

### Acceptance Criteria

- L1: WHEN a member requests to borrow a book AND the book is available AND the member has no unpaid fines, THE Library System SHALL lend the book to the member.
- L2: WHEN a member requests to borrow a book AND the book is not available AND the member has no unpaid fines, THE Library System SHALL add the member to the waiting list for the book.
- L3: WHEN a member requests to borrow a book AND the member has unpaid fines, THE Library System SHALL refuse the request.
- L4: WHEN a member returns a book, THE Library System SHALL mark the book as available.
- L5: WHEN a member returns a book more than 14 days after borrowing it, THE Library System SHALL add a fine to the member's account.
- L6: THE Library System SHALL NOT add any member to a waiting list.
