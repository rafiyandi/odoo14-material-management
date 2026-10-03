# Everything Antigravity: Workspace Rules & Guidelines

Welcome to **Everything Antigravity** — the comprehensive productivity configuration suite for Google Antigravity, optimized for Gemini models (Gemini 3.7 Pro, Gemini 3.7 Flash).

## Core Principles & Coding Standards

1. **Immutability First**: Avoid in-place mutations. Use spread operators, pure functions, and immutable data structures.
2. **Modular & Small Functions**: Keep functions focused (<50 lines) and files compact (<800 lines). Avoid nesting deeper than 4 levels.
3. **Strict Validation**: Always validate user and external input using schema libraries (e.g., Zod) before processing.
4. **Test-Driven Development (TDD)**: Write tests first for new features and bug fixes. Maintain minimum 80% coverage (unit, integration, E2E).
5. **Zero Hardcoded Secrets**: Use environment variables for all sensitive configuration. Never commit API keys or private credentials.

## Antigravity Workflow & Skill Orchestration

- **Planning & Architecture**: For complex features or refactoring, activate the `planner` or `architect` skills before writing code.
- **TDD Flow**: Use `tdd-workflow` or `tdd-guide` to follow the RED -> GREEN -> REFACTOR cycle.
- **Code & Security Review**: Before completing tasks or proposing commits, execute `code-reviewer` and `security-reviewer` checks.
- **Build Troubleshooting**: If build errors occur, systematically analyze and resolve them using `build-error-resolver`.
- **E2E & Verification**: Validate critical user journeys with `e2e-runner` and `verification-loop`.

## Model Usage Guidance

- **Gemini 3.7 Flash**: Recommended for fast iterative code edits, running tests, single-file utilities, and routine tool execution.
- **Gemini 3.7 Pro / Flash Thinking**: Recommended for complex architecture design, planning mode, cross-cutting refactoring, and multi-file debugging.
