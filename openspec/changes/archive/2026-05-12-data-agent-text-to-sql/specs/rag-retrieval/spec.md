## ADDED Requirements

### Requirement: Embedding-Based Query Retrieval
The system SHALL embed user natural language queries and perform kNN vector search across SQL templates, schema descriptions, and business context indices.

#### Scenario: Multi-index retrieval
- **WHEN** a user query is submitted
- **THEN** the retriever SHALL search all three OpenSearch indices and return combined top-K results

#### Scenario: Relevance ranking
- **WHEN** a user asks "Who has the highest deposit?"
- **THEN** the retriever SHALL return SQL templates related to deposit ranking as the top results

### Requirement: Configurable Top-K
The system SHALL allow configuration of the number of results retrieved per index (default: 3 per index).

#### Scenario: Top-K override
- **WHEN** the retrieval top_k is set to 5
- **THEN** the retriever SHALL return up to 5 results per index

### Requirement: Local Embedding Model
The system SHALL use a local sentence-transformers model (all-MiniLM-L6-v2) for embedding generation, requiring no external API calls for embeddings.

#### Scenario: Embedding generation
- **WHEN** a text string is submitted for embedding
- **THEN** the system SHALL return a dense vector using the local model without making external API calls
