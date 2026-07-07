## Purpose

TBD - Automatically synced from data-agent-text-to-sql

## Requirements

### Requirement: SQL Execution Against SQLite
The system SHALL execute LLM-generated SQL against the SQLite database and return structured results.

#### Scenario: Successful query execution
- **WHEN** a valid SELECT query is executed
- **THEN** the system SHALL return column names and row data as a structured result

#### Scenario: Read-only enforcement
- **WHEN** a generated SQL contains INSERT, UPDATE, DELETE, or DROP statements
- **THEN** the system SHALL reject the query and return an error

#### Scenario: Query timeout
- **WHEN** a query takes longer than 10 seconds
- **THEN** the system SHALL cancel the query and return a timeout error
