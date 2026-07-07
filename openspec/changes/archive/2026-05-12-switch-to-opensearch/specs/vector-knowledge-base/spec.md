## MODIFIED Requirements

### Requirement: OpenSearch Vector Indexing
The system SHALL index SQL templates, schema descriptions, and business context into separate OpenSearch indices with vector embeddings.

#### Scenario: Index creation
- **WHEN** the indexer runs
- **THEN** three OpenSearch indices SHALL be created: `sql_templates`, `schema_descriptions`, and `business_context`, each with kNN vector fields using the Lucene/HNSW engine.

## ADDED Requirements

### Requirement: OpenSearch Authentication
The system SHALL support connecting to OpenSearch using HTTP Basic Authentication (username and password) to support both local and cloud-managed instances.

#### Scenario: Authenticated connection
- **WHEN** OpenSearch credentials (username/password) are provided in configuration
- **THEN** the system SHALL successfully authenticate and connect to the OpenSearch service.
