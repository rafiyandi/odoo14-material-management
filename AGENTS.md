# Antigravity Agent Guidelines

This repository provides reusable guidelines, skills, and hooks for Google Antigravity.

## Instructions for Antigravity

1. **Adhere to Defined Rules**: Follow all rules in `.agents/rules/` and `GEMINI.md`.
2. **Use Specialized Skills**: Check `.agents/skills/` before executing complex workflows. Load relevant skills on-demand using progressive disclosure.
3. **Follow Verification Loops**: Always verify code changes by running tests, checking linting, and inspecting types.
4. **Clean Code & No Extraneous Files**: Do not generate random temporary markdown or log files in the project root.
