## ADDED Requirements

### Requirement: Test Dataset
The system SHALL include a test dataset of at least 15 natural language queries with corresponding ground truth SQL statements.

#### Scenario: Test dataset structure
- **WHEN** the test dataset is loaded
- **THEN** each entry SHALL contain a `question` (string) and `expected_sql` (string)

#### Scenario: Query diversity
- **WHEN** the test dataset is inspected
- **THEN** it SHALL include queries covering: single-table lookups, aggregations (SUM, AVG, COUNT), sorting (ORDER BY), filtering (WHERE), joins, and GROUP BY operations

### Requirement: Automated Evaluation Script
The system SHALL provide a Python script that runs all test queries against the API and compares generated SQL with ground truth.

#### Scenario: Batch evaluation
- **WHEN** the evaluation script is executed
- **THEN** it SHALL call `POST /query` for each test case, log the generated SQL vs expected SQL, and compute accuracy metrics

#### Scenario: Result comparison
- **WHEN** generated SQL and expected SQL produce the same result set
- **THEN** the evaluation SHALL mark the test case as "result-equivalent" even if SQL syntax differs

### Requirement: Acceptance Test Script
The system SHALL include a simple Python script that demonstrates a single query against the running API.

#### Scenario: Acceptance test execution
- **WHEN** the acceptance test script is run with the API server active
- **THEN** it SHALL POST a query and print the JSON response including `answer`, `generated_sql`, and `query_result`
