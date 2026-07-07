## ADDED Requirements

### Requirement: LLM-Based SQL Generation
The system SHALL use LangChain with an LLM (via OpenRouter) to generate executable SQL from a user's natural language query combined with retrieved context (SQL templates, schema, business context).

#### Scenario: Successful SQL generation
- **WHEN** the user asks "Who has the highest deposit?"
- **THEN** the skill SHALL generate a valid SQL query equivalent to `SELECT * FROM deposits ORDER BY total_deposit DESC LIMIT 1`

#### Scenario: Context-aware generation
- **WHEN** the user asks a question and retrieved context includes relevant SQL templates
- **THEN** the generated SQL SHALL leverage the template patterns rather than generating from scratch

### Requirement: SQL Output Extraction
The system SHALL extract clean SQL from LLM responses, stripping any markdown formatting or explanation text.

#### Scenario: Markdown SQL extraction
- **WHEN** the LLM returns SQL wrapped in ```sql code blocks
- **THEN** the system SHALL extract only the SQL statement

### Requirement: Error Handling for Invalid SQL
The system SHALL handle cases where the LLM generates invalid or non-executable SQL.

#### Scenario: Invalid SQL fallback
- **WHEN** the generated SQL fails to parse or execute
- **THEN** the system SHALL return an error message explaining the failure rather than crashing
