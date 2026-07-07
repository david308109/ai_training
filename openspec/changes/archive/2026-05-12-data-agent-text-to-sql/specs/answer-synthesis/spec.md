## ADDED Requirements

### Requirement: Natural Language Answer Generation
The system SHALL use an LLM to convert SQL query results and the original user question into a clear, natural language answer.

#### Scenario: Successful answer synthesis
- **WHEN** the SQL query returns results for "Who has the highest deposit?"
- **THEN** the skill SHALL generate a natural language response like "The customer with the highest deposit is [name] with a total deposit of [amount]."

#### Scenario: Empty result handling
- **WHEN** the SQL query returns no rows
- **THEN** the skill SHALL generate a natural language response indicating no matching data was found

#### Scenario: Error result handling
- **WHEN** the SQL execution failed
- **THEN** the skill SHALL generate a natural language response explaining the error in user-friendly terms
