## MODIFIED Requirements

### Requirement: Structured SQL and Metadata Generation
The system SHALL use LangChain with an LLM to generate a structured JSON response containing the executable SQL query, a complexity classification, and a response template.

#### Scenario: Simple query metadata
- **WHEN** the user asks "What is my balance?"
- **THEN** the skill SHALL return a JSON object with `sql`, `complexity`: "simple", and a `template` string.

#### Scenario: Complex query metadata
- **WHEN** the user asks for a multi-row analytical summary
- **THEN** the skill SHALL return a JSON object with `sql` and `complexity`: "complex".

### Requirement: LLM-Based SQL Generation
The system SHALL use LangChain with an LLM (via OpenRouter) to generate executable SQL from a user's natural language query combined with retrieved context (SQL templates, schema, business context).

#### Scenario: Successful SQL generation
- **WHEN** the user asks "Who has the highest deposit?"
- **THEN** the skill SHALL generate a valid SQL query equivalent to `SELECT * FROM deposits ORDER BY total_deposit DESC LIMIT 1`

#### Scenario: Context-aware generation
- **WHEN** the user asks a question and retrieved context includes relevant SQL templates
- **THEN** the generated SQL SHALL leverage the template patterns rather than generating from scratch
