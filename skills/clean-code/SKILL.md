---
name: clean-code
description: Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---

# Clean Code - Pragmatic AI Coding Standards

> **CRITICAL SKILL** - Be **concise, direct, and solution-focused**.

---

## Core Principles

| Principle | Rule |
|-----------|------|
| **SRP** | Single Responsibility - each function/class does ONE thing |
| **DRY** | Don't Repeat Yourself - extract duplicates, reuse |
| **KISS** | Keep It Simple - simplest solution that works |
| **YAGNI** | You Aren't Gonna Need It - don't build unused features |
| **Boy Scout** | Leave code cleaner than you found it |

---

## Naming Rules

| Element | Convention |
|---------|------------|
| **Variables** | Reveal intent: `userCount` not `n` |
| **Functions** | Verb + noun: `getUserById()` not `user()` |
| **Booleans** | Question form: `isActive`, `hasPermission`, `canEdit` |
| **Constants** | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |

> **Rule:** If you need a comment to explain a name, rename it.

---

## Function Rules

| Rule | Description |
|------|-------------|
| **Small** | Max 20 lines, ideally 5-10 |
| **One Thing** | Does one thing, does it well |
| **One Level** | One level of abstraction per function |
| **Few Args** | Max 3 arguments, prefer 0-2 |
| **No Side Effects** | Don't mutate inputs unexpectedly |

---

## Code Structure

| Pattern | Apply |
|---------|-------|
| **Guard Clauses** | Early returns for edge cases |
| **Flat > Nested** | Avoid deep nesting (max 2 levels) |
| **Composition** | Small functions composed together |
| **Colocation** | Keep related code close |

---

## AI Coding Style

| Situation | Action |
|-----------|--------|
| User asks for feature | Write it directly |
| User reports bug | Fix it, don't explain |
| No clear requirement | Ask, don't assume |

---

## Anti-Patterns (DON'T)

| ❌ Pattern | ✅ Fix |
|-----------|-------|
| Comment every line | Delete obvious comments |
| Helper for one-liner | Inline the code |
| Factory for 2 objects | Direct instantiation |
| utils.ts with 1 function | Put code where used |
| "First we import..." | Just write code |
| Deep nesting | Guard clauses |
| Magic numbers | Named constants |
| God functions | Split by responsibility |

---

## Summary

| Do | Don't |
|----|-------|
| Write code directly | Write tutorials |
| Let code self-document | Add obvious comments |
| Fix bugs immediately | Explain the fix first |
| Inline small things | Create unnecessary files |
| Name things clearly | Use abbreviations |
| Keep functions small | Write 100+ line functions |

> **Remember: The user wants working code, not a programming lesson.**

---

## Verification Scripts (MANDATORY)

> 🔴 **CRITICAL:** Before completing ANY coding task, run the appropriate verification scripts.

### Available Scripts

| Script | When to Use | Command |
|--------|-------------|---------|
| **Security Scan** | After ANY code changes | `python ~/.claude/skills/vulnerability-scanner/scripts/security_scan.py .` |
| **Lint Check** | After writing code | `python ~/.claude/skills/lint-and-validate/scripts/lint_runner.py .` |
| **Type Coverage** | TypeScript/Python types | `python ~/.claude/skills/lint-and-validate/scripts/type_coverage.py .` |
| **API Validator** | After API/endpoint work | `python ~/.claude/skills/api-patterns/scripts/api_validator.py .` |
| **UX Audit** | After frontend work | `python ~/.claude/skills/frontend-design/scripts/ux_audit.py .` |
| **A11y Check** | After UI components | `python ~/.claude/skills/frontend-design/scripts/accessibility_checker.py .` |
| **SEO Check** | After page creation | `python ~/.claude/skills/seo-fundamentals/scripts/seo_checker.py .` |
| **GEO Check** | AI citation readiness | `python ~/.claude/skills/geo-fundamentals/scripts/geo_checker.py .` |
| **Mobile Audit** | After mobile/responsive | `python ~/.claude/skills/mobile-design/scripts/mobile_audit.py .` |
| **Schema Validate** | After DB changes | `python ~/.claude/skills/database-design/scripts/schema_validator.py .` |
| **Test Runner** | After any feature | `python ~/.claude/skills/testing-patterns/scripts/test_runner.py .` |
| **Lighthouse** | Web performance | `python ~/.claude/skills/performance-profiling/scripts/lighthouse_audit.py <url>` |
| **Playwright** | E2E testing | `python ~/.claude/skills/webapp-testing/scripts/playwright_runner.py <url>` |
| **i18n Check** | Hardcoded strings & translations | `python ~/.claude/skills/i18n-localization/scripts/i18n_checker.py .` |

### Usage Rules

1. **Frontend work?** → Run: `ux_audit.py`, `accessibility_checker.py`
2. **API/Backend?** → Run: `security_scan.py`, `lint_runner.py`, `api_validator.py`
3. **Database changes?** → Run: `schema_validator.py`
4. **Any code?** → Run: `security_scan.py` (always)
5. **Multi-language app?** → Run: `i18n_checker.py`
6. **Web project complete?** → Run: `lighthouse_audit.py`, `playwright_runner.py`

### Script Output Handling

- ✅ **Pass** → Continue with next task
- ❌ **Fail** → Fix issues before proceeding
- ⚠️ **Warning** → Document in PLAN.md, fix if time permits

> 🔴 **EXIT GATE:** Do NOT mark any coding task complete without running at least `security_scan.py`.
