---
name: tdd-guide
description: >-
  Test-Driven Development (TDD) guide for enforcing the Red-Green-Refactor cycle and 80%+ test coverage.
  Use when implementing new features, creating API endpoints, fixing bugs, or refactoring code.
---

# Antigravity TDD Guide

Test-Driven Development methodology and best practices.

## TDD Cycle: RED $\rightarrow$ GREEN $\rightarrow$ REFACTOR

1. **RED**: Write failing tests specifying desired behavior and edge cases first.
2. **GREEN**: Write minimal code necessary to make all tests pass.
3. **REFACTOR**: Improve code quality, maintainability, and readability without breaking tests.

## Coverage Standards

- **Target**: Minimum 80% coverage (unit, integration, and critical E2E).
- **Edge Cases**: Empty lists, null/undefined values, boundary conditions, rate limits, network timeouts.
- **Fast Execution**: Keep unit test suites running in <5 seconds.
