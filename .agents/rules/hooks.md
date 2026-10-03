# Antigravity Hooks System

## Supported Lifecycle Events

Antigravity supports 5 lifecycle hook events configured in `.agents/hooks.json`:

- **PreToolUse**: Executes before a tool step runs (can allow, deny, or ask confirmation).
- **PostToolUse**: Executes after a tool step completes (auto-formatting, linting, analysis).
- **PreInvocation**: Executes before the model is called (injecting context/reminders).
- **PostInvocation**: Inspects model outputs and can force continuation.
- **Stop**: Executes when the agent loop is about to terminate (ensures tests passed, no console.logs left).

## Configured Workspace Hooks

### PreToolUse
- **tmux reminder**: Suggests tmux or background task execution for long-running processes (npm, pnpm, cargo, etc.).
- **doc blocker**: Blocks generation of unneeded `.md`/`.txt` files outside standard documentation files (`README.md`, `GEMINI.md`, `AGENTS.md`).

### PostToolUse
- **Prettier / Formatter**: Auto-formats modified JS/TS/JSON files after tool edits (`replace_file_content` / `multi_replace_file_content`).
- **TypeScript Typecheck**: Verifies type safety after editing `.ts` / `.tsx` files.
- **console.log Warning**: Detects and warns about leftover `console.log` statements in source files.

### Stop
- **Audit Checklist**: Confirms test coverage and absence of debugging statements before session completion.
