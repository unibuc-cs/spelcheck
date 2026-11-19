# Requirements: Transfer

## Requirement 1

**User Story:** As an account holder, I want to transfer money to other accounts, so that I can pay people.

### Acceptance Criteria

- T1: WHEN the account holder submits a transfer AND the balance covers the amount AND the amount is at most the daily limit, THE Banking System SHALL execute the transfer.
- T2: WHEN the account holder submits a transfer AND the balance does not cover the amount, THE Banking System SHALL reject the transfer and show an insufficient-funds message.
- T3: WHEN the account holder submits a transfer AND the amount is above the daily limit, THE Banking System SHALL reject the transfer and show a limit message.
- T4: WHEN a transfer is executed, THE Banking System SHALL send a receipt to the account holder.
- T5: WHEN the account holder submits a transfer to a payee that was never used before, THE Banking System SHALL ask for a one-time code.
- T6: WHILE the account is frozen, THE Banking System SHALL NOT execute any transfer.
