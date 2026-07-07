## MODIFIED Requirements

### Requirement: Embedding-Based Query Retrieval
The system SHALL embed user natural language queries and perform kNN vector search across SQL templates, schema descriptions, and business context indices using the OpenSearch vector database.

#### Scenario: Multi-index retrieval
- **WHEN** a user query is submitted
- **THEN** the retriever SHALL search all three OpenSearch indices and return combined top-K results from the OpenSearch service.
