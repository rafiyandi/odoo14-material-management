# Performance & Model Optimization

## Model Selection Strategy

Antigravity operates with Google's state-of-the-art Gemini models:

- **Gemini 3.7 Flash** (Fast, responsive, cost-effective):
  - Routine code editing, test execution, shell commands, and quick utility tasks.
  - Subagent worker tasks and iterative code generation.

- **Gemini 3.7 Pro / Flash Thinking** (Deep reasoning, complex orchestration):
  - Complex architectural decisions, planning mode, and full-stack design.
  - Deep debugging, multi-file refactoring, and root cause analysis.

## Context Window & Token Efficiency

- **Progressive Disclosure**: Keep core rules lightweight and rely on on-demand skills (`SKILL.md`) for detailed workflows to avoid polluting token context.
- **Selective Tool Use**: Minimize redundant tool invocations. Combine file reads or searches where appropriate.
- **MCP Server Management**: Only enable MCP servers relevant to the active project to preserve context window capacity.

## Troubleshooting & Failure Recovery

If a build, typecheck, or test fails:
1. Activate the `build-error-resolver` skill.
2. Read the full error stack without making blind guesses.
3. Apply focused, incremental fixes and verify immediately.
