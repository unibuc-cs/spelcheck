## ADDED Requirements

### Requirement: New labels

A relabelled folder SHALL carry only its new label.

#### Scenario: A relabel replaces the label

- **WHEN** a relabel request is handled in a run
- **THEN** the folder carries the new label and not the old one at the end of the run
