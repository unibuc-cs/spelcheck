# Requirements: Streaming

## Requirement 1

**User Story:** As a parent, I want each profile of our streaming account to show suitable films, so that the children see what they may see.

### Acceptance Criteria

- S1: WHEN an adult profile starts a film AND the subscription is active, THE Streaming Service SHALL play the film.
- S2: WHEN a profile starts a film AND the subscription has expired, THE Streaming Service SHALL show the renewal page.
- S3: WHEN a child profile starts a film AND the film is rated 16 or higher, THE Streaming Service SHALL block the film.
- S4: WHEN a child profile starts a film AND the film is rated below 16 AND the subscription is active, THE Streaming Service SHALL play the film.
- S5: WHEN a parent enters the correct PIN, THE Streaming Service SHALL unlock the child profile for one film.
- S6: WHEN a child profile starts a film, THE Streaming Service SHALL play the film.
