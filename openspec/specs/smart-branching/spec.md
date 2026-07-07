## Purpose

TBD - Automatically synced from optimize-with-smart-branching

## Requirements

### Requirement: Conditional Response Routing
The system SHALL route the response generation process through a conditional branch based on query complexity.

#### Scenario: Routing to local formatter
- **WHEN** a query is classified as `simple` AND local formatting is successful
- **THEN** the system SHALL skip the AI Answer Synthesis step and return the locally formatted answer.

#### Scenario: Routing to AI Synthesis
- **WHEN** a query is classified as `complex` OR local formatting fails
- **THEN** the system SHALL invoke the AI Answer Synthesis skill to generate the final response.

### Requirement: Local Template Formatting
The system SHALL support populating natural language templates with SQL query results using Python's standard formatting logic.

#### Scenario: Successful template population
- **WHEN** a template "Balance is {amount}" is provided with data `{"amount": 1000}`
- **THEN** the system SHALL produce the string "Balance is 1000".

### Requirement: Automatic Fallback
The system SHALL automatically fallback to AI Answer Synthesis if local formatting encounters an error.

#### Scenario: Key mismatch fallback
- **WHEN** a template contains a key `{total}` but the SQL result only has `{sum}`
- **THEN** the system SHALL catch the error and invoke the AI Answer Synthesis skill.
