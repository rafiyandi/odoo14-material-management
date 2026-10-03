# Agent & Skill Orchestration

## Available Skills & Subagents

Located in `.agents/skills/` (and `.agents/rules/`):

| Skill / Subagent | Purpose | When to Use |
|---|---|---|
| **planner** | Implementation planning | Complex features, large-scale refactoring |
| **architect** | System design & ADR | Architectural decisions, technology choices |
| **tdd-workflow** / **tdd-guide** | Test-driven development | New features, bug fixes, API endpoints |
| **code-reviewer** | Code review & quality checks | After writing or modifying code |
| **security-reviewer** | Security & vulnerability analysis | Before committing or deploying |
| **build-error-resolver** | Fix compilation & build errors | When build, typecheck, or bundling fails |
| **e2e-runner** | Playwright E2E testing | Critical user flows, full stack testing |
| **refactor-cleaner** | Dead code cleanup & refactoring | Code maintenance, dependency cleanup |
| **doc-updater** | Documentation maintenance | Keeping READMEs, API docs, and code synced |

## Immediate Skill Usage

No explicit prompt needed from the user:
1. **Complex feature requests** $\rightarrow$ Activate **planner** skill
2. **Code just written or edited** $\rightarrow$ Activate **code-reviewer** skill
3. **Bug fix or new feature implementation** $\rightarrow$ Activate **tdd-workflow** / **tdd-guide** skill
4. **Architectural design or tech stack decision** $\rightarrow$ Activate **architect** skill

## Multi-Perspective Analysis

For complex architectural problems, evaluate through multiple perspectives:
- Senior Software Engineer (maintainability & clean code)
- Security Specialist (threat modeling & OWASP)
- Performance Engineer (latency, memory, token context)
- Test Engineer (testability & coverage)
