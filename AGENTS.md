# Agent guidance (Codex)

- Always follow TDD: write/modify pytest tests first, then implement.
- Keep functions small and well-documented.
- Do not change project structure without asking.
- If tests fail, fix tests or code until `pytest` passes locally.
- Prefer clear error handling (ValueError with good messages).