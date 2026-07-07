## ADDED Requirements

### Requirement: SQL Template Knowledge Base
The system SHALL maintain a collection of at least 15 SQL templates, each with a corresponding business description explaining what the query represents.

#### Scenario: Template structure
- **WHEN** a SQL template is defined
- **THEN** it SHALL include the SQL query string, a business description, and a list of referenced tables

#### Scenario: Template coverage
- **WHEN** the template collection is inspected
- **THEN** it SHALL cover common banking queries including: top depositors, branch aggregations, RM portfolio analysis, deposit range filtering, and customer lookups

### Requirement: Business Context Documents
The system SHALL maintain business context documents that describe domain-level concepts (e.g., what a Relationship Manager does, how deposits work, branch hierarchy).

#### Scenario: Business context structure
- **WHEN** a business context document is defined
- **THEN** it SHALL include a topic identifier and descriptive content about the banking domain concept

### Requirement: OpenSearch Vector Indexing
The system SHALL index SQL templates, schema descriptions, and business context into separate OpenSearch indices with vector embeddings.

#### Scenario: Index creation
- **WHEN** the indexer runs
- **THEN** three OpenSearch indices SHALL be created: `sql_templates`, `schema_descriptions`, and `business_context`, each with kNN vector fields

#### Scenario: Re-indexing idempotency
- **WHEN** the indexer runs multiple times
- **THEN** it SHALL delete and recreate indices to ensure clean state
