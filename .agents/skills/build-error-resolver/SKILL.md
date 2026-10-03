---
name: build-error-resolver
description: >-
  Systematic debugger for resolving TypeScript compilation errors, build failures, bundling issues, and syntax bugs.
  Use whenever a build, npm/cargo run build, or typecheck command fails with errors.
---

# Antigravity Build Error Resolver

Diagnostic guide for resolving build failures systematically.

## Resolution Workflow

1. **Capture & Parse Errors**:
   - Read the exact error stack, file paths, line numbers, and error codes (e.g., TS2322, TS2345).
   - Group related compiler errors caused by shared type definitions.

2. **Root Cause Analysis**:
   - Distinguish between missing types, breaking API changes, or incorrect imports.
   - Avoid blind patching or indiscriminate use of `any` / `@ts-ignore`.

3. **Incremental Fix & Validation**:
   - Fix foundational type contracts first.
   - Run typecheck/build command immediately to verify resolution.
