# Requirements: Campsite

## Requirement 1

**User Story:** As a camper, I want to book a pitch and use the services of the campsite with my booking card, so that my stay runs smoothly.

### Acceptance Criteria

- C1: WHEN a camper requests a pitch AND a pitch of the requested size is free for all requested nights, THE Campsite System SHALL reserve the pitch.
- C2: WHEN a camper requests a pitch AND no pitch of the requested size is free for all requested nights, THE Campsite System SHALL offer the nearest free dates.
- C3: WHEN a camper pays the deposit for a reserved pitch, THE Campsite System SHALL confirm the booking by email.
- C4: WHEN the deposit for a reserved pitch has been missing for more than 48 hours, THE Campsite System SHALL send the camper a reminder.
- C5: WHEN a camper cancels a booking more than 14 days before arrival, THE Campsite System SHALL refund the deposit.
- C6: WHEN a camper cancels a booking 14 days or less before arrival, THE Campsite System SHALL keep the deposit.
- C7: WHEN a camper arrives AND the booking is confirmed, THE Campsite System SHALL issue a booking card and show the way to the pitch.
- C8: WHEN a camper arrives AND the booking is not confirmed, THE Campsite System SHALL send the camper to the reception desk.
- C9: WHEN a camper holds a booking card to the barrier AND the card is valid, THE Campsite System SHALL open the barrier.
- C10: WHEN a camper holds a booking card to the barrier AND the card is not valid, THE Campsite System SHALL keep the barrier closed and show a message.
- C11: WHEN a vehicle has passed the barrier, THE Campsite System SHALL close the barrier.
- C12: WHEN a camper plugs a cable into the power post of the pitch AND the booking includes electricity, THE Campsite System SHALL switch on the power post.
- C13: WHEN a camper plugs a cable into the power post of the pitch AND the booking does not include electricity, THE Campsite System SHALL keep the power post off and offer the electricity option.
- C14: WHEN the power use of a pitch exceeds 10 amperes, THE Campsite System SHALL notify the camper and the site manager.
- C15: WHEN a camper buys shower tokens, THE Campsite System SHALL add the tokens to the booking card.
- C16: WHEN a camper holds a booking card to a shower AND the card has at least one token, THE Campsite System SHALL start the shower for five minutes and take one token.
- C17: WHEN a camper holds a booking card to a shower AND the card has no token, THE Campsite System SHALL show the price of a token.
- C18: WHEN a camper registers a dog, THE Campsite System SHALL add the dog fee to the bill.
- C19: WHEN a camper orders bread for the next morning before 18:00, THE Campsite System SHALL add the order to the bakery list.
- C20: WHEN a camper orders bread for the next morning at 18:00 or later, THE Campsite System SHALL refuse the order.
- C21: WHEN a camper reports a fault on the pitch, THE Campsite System SHALL create a task for the maintenance team.
- C22: WHEN a maintenance task has been open for more than 24 hours, THE Campsite System SHALL alert the site manager.
- C23: WHEN a camper asks to extend the stay AND the pitch is free for the extra nights, THE Campsite System SHALL extend the booking.
- C24: WHEN a camper asks to extend the stay AND the pitch is not free for the extra nights, THE Campsite System SHALL offer another pitch.
- C25: WHEN the departure day of a booking begins, THE Campsite System SHALL send the bill to the camper.
- C26: WHEN a camper pays the bill, THE Campsite System SHALL send a receipt and mark the booking as paid.
- C27: WHEN a camper leaves the campsite AND the bill is paid, THE Campsite System SHALL cancel the booking card.
- C28: WHEN a camper leaves the campsite AND the bill is not paid, THE Campsite System SHALL charge the open amount to the stored payment card.
- C29: WHEN a booking card is reported lost, THE Campsite System SHALL cancel the card and issue a new one.
- C30: WHEN a camper writes a review after the stay, THE Campsite System SHALL publish the review on the campsite page.
- C31: THE Campsite System SHALL NOT publish any review.
