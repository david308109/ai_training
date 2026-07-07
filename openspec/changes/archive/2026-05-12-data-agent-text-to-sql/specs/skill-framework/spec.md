## ADDED Requirements

### Requirement: Skill Abstract Base Class
The system SHALL define an abstract `Skill` class with `name`, `description` properties and an `execute(context: dict) -> dict` method.

#### Scenario: Skill interface contract
- **WHEN** a new skill is created
- **THEN** it MUST implement the `execute` method accepting a context dict and returning a result dict

### Requirement: Skill Registry
The system SHALL maintain a `SkillRegistry` that maps skill names to skill instances, enabling dynamic lookup and invocation.

#### Scenario: Skill registration
- **WHEN** a skill is registered with name "sql_generation"
- **THEN** it SHALL be retrievable from the registry by that name

#### Scenario: Unknown skill lookup
- **WHEN** a non-existent skill name is looked up
- **THEN** the registry SHALL raise a `KeyError` with a descriptive message

### Requirement: Extensibility
The system's skill architecture SHALL allow adding new skills without modifying existing orchestration code.

#### Scenario: Adding a new skill
- **WHEN** a developer creates a new skill class implementing the Skill ABC and registers it
- **THEN** the orchestrator SHALL be able to invoke it without code changes to the orchestrator itself
