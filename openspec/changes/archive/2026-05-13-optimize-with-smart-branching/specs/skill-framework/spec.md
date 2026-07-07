## MODIFIED Requirements

### Requirement: Skill Abstract Base Class
The system SHALL define an abstract `Skill` class with `name`, `description` properties and an `execute(context: dict) -> dict` method. The class SHALL also support being used as a LangChain `Runnable`.

#### Scenario: Skill interface contract
- **WHEN** a new skill is created
- **THEN** it MUST implement the `execute` method accepting a context dict and returning a result dict

### Requirement: Extensibility
The system's skill architecture SHALL allow adding new skills without modifying existing orchestration code, and SHALL support chaining skills using LangChain Expression Language (LCEL).

#### Scenario: Chaining skills with LCEL
- **WHEN** multiple skills are defined as Runnables
- **THEN** they SHALL be chainable using the `|` operator in the orchestrator
