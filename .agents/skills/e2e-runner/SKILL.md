---
name: e2e-runner
description: >-
  End-to-End (E2E) testing specialist using Playwright or Cypress for browser automation and user journey validation.
  Use when writing, debugging, or running E2E browser tests, testing critical UI workflows, or validating user journeys.
---

# Antigravity E2E Runner

Playwright / Browser automation and E2E test execution.

## Core Guidelines

1. **User-Centric Locators**: Use accessible locators (`getByRole`, `getByText`, `getByLabel`, `getByPlaceholder`) rather than brittle CSS selectors.
2. **Deterministic Waiting**: Rely on Playwright auto-waiting. Avoid hardcoded `sleep` or fixed timeouts.
3. **Isolated Test State**: Ensure each test starts with clean state (independent auth sessions, seeded database records).
4. **Resilient Assertions**: Use web-first assertions (`await expect(locator).toBeVisible()`).
