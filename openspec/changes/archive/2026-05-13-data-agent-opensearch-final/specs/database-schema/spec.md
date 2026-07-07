## ADDED Requirements

### Requirement: Banking Database Schema
The system SHALL provide a SQLite database with banking-domain tables: `customers`, `deposits`, `branches`, and `relationship_managers` with appropriate foreign key relationships.

#### Scenario: Database initialization
- **WHEN** the application starts for the first time
- **THEN** the SQLite database SHALL be created with all tables and seed data (~50 records across tables)

#### Scenario: Schema includes all required columns
- **WHEN** the database schema is inspected
- **THEN** the `deposits` table SHALL include `customer_id`, `customer_name`, `total_deposit`, `branch`, and `relationship_manager` columns (or equivalent via joins)

### Requirement: Human-Readable Schema Description
The system SHALL maintain a text-based description of the database schema that is optimized for LLM consumption.

#### Scenario: Schema description generation
- **WHEN** the schema description is retrieved
- **THEN** it SHALL include table names, column names, data types, relationships, and business meaning for each column

### Requirement: Seed Data Realism
The system SHALL populate seed data with realistic banking values (proper customer names, deposit amounts in reasonable ranges, branch names, RM names).

#### Scenario: Seed data validation
- **WHEN** the database is seeded
- **THEN** deposit amounts SHALL range from 10,000 to 10,000,000 and branch names SHALL represent plausible bank branch locations
