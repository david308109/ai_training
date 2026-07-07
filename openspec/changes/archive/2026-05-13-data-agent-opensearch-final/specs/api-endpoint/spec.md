## ADDED Requirements

### Requirement: POST /query Endpoint
The system SHALL expose a FastAPI endpoint `POST /query` that accepts a JSON body with `query` (string) and returns `answer` (string), `generated_sql` (string), and optionally `query_result` (object).

#### Scenario: Successful query flow
- **WHEN** a POST request is sent to `/query` with `{"query": "Who has the highest deposit?"}`
- **THEN** the response SHALL include `answer` (natural language), `generated_sql` (the SQL used), and `query_result` (the raw data)

#### Scenario: Invalid request body
- **WHEN** a POST request is sent without a `query` field
- **THEN** the endpoint SHALL return HTTP 422 with validation error details

### Requirement: Pipeline Orchestration
The system SHALL orchestrate the full pipeline: retrieve context → generate SQL → execute SQL → synthesize answer, passing data between steps.

#### Scenario: End-to-end flow
- **WHEN** a user submits a natural language query
- **THEN** the system SHALL execute retrieval, SQL generation, SQL execution, and answer synthesis in sequence, returning the final result

#### Scenario: Partial failure handling
- **WHEN** SQL execution fails but SQL generation succeeded
- **THEN** the response SHALL still include `generated_sql` and an error message in `answer`
