## 1. Skill Framework Refactor

- [ ] 1.1 Update `app/skills/base.py` to make `Skill` inherit from `Runnable`.
- [ ] 1.2 Ensure `execute` method is compatible with LangChain's `ainvoke`.

## 2. SQL Generation Enhancement

- [ ] 2.1 Update `SQL_GENERATION_PROMPT` in `app/skills/sql_generation.py` to require JSON output.
- [ ] 2.2 Add `complexity` and `response_template` instructions to the prompt.
- [ ] 2.3 Update `_extract_sql` and `execute` to parse the new JSON format.

## 3. Smart Branching Implementation

- [ ] 3.1 Create a local response formatter utility in `app/skills/` (or within orchestrator).
- [ ] 3.2 Implement the formatting logic with a try-except fallback flag.
- [ ] 3.3 Implement `RunnableBranch` logic in the orchestrator.

## 4. Orchestrator LCEL Refactor

- [ ] 4.1 Refactor `app/agent/orchestrator.py` to use LangChain LCEL pipe (`|`) syntax.
- [ ] 4.2 Replace the manual sequential flow with a unified `Chain`.
- [ ] 4.3 Integrate the `RunnableBranch` into the new Chain.

## 5. Verification & Testing

- [ ] 5.1 Run `python tests/test_acceptance.py` to ensure the new flow works.
- [ ] 5.2 Manually verify "simple" queries only trigger 1 AI call (via logs).
- [ ] 5.3 Verify "complex" queries still trigger 2 AI calls.
