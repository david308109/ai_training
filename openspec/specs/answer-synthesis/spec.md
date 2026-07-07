## Purpose

TBD - Automatically synced from data-agent-text-to-sql

## Requirements

### Requirement: Natural Language Answer Generation
The system SHALL use an LLM to convert SQL query results and the original user question into a clear, natural language answer. This skill SHALL be invoked as a fallback or for complex analytical queries.

#### Scenario: Successful answer synthesis
- **WHEN** the SQL query returns results for "Who has the highest deposit?"
- **THEN** the skill SHALL generate a natural language response like "The customer with the highest deposit is [name] with a total deposit of [amount]."

#### Scenario: Fallback synthesis
- **WHEN** local template formatting fails for a simple query
- **THEN** the system SHALL invoke this skill to produce the final answer

#### Scenario: Empty result handling
- **WHEN** the SQL query returns no rows
- **THEN** the skill SHALL generate a natural language response indicating no matching data was found

#### Scenario: Error result handling
- **WHEN** the SQL execution failed
- **THEN** the skill SHALL generate a natural language response explaining the error in user-friendly terms
