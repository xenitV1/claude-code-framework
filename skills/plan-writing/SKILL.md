---
name: plan-writing
description: Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work.
---

# Plan Writing

> Source: obra/superpowers

## Overview
This skill provides a framework for breaking down work into clear, actionable tasks with verification criteria.

## Task Breakdown Principles

### 1. Small, Focused Tasks
- Each task should take 2-5 minutes
- One clear outcome per task
- Independently verifiable

### 2. Clear Verification
- How do you know it's done?
- What can you check/test?
- What's the expected output?

### 3. Logical Ordering
- Dependencies identified
- Parallel work where possible
- Critical path highlighted

## Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Overview
[Brief description of what we're building]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Prerequisites
- [x] [Already completed prereq]
- [ ] [Pending prereq]

## Tasks

### Phase 1: Setup
- [ ] **Task 1.1**: [Description]
  - Files: `path/to/file.ts`
  - Verify: [How to verify]
  
- [ ] **Task 1.2**: [Description]
  - Files: `path/to/file.ts`
  - Depends on: Task 1.1
  - Verify: [How to verify]

### Phase 2: Implementation
- [ ] **Task 2.1**: [Description]
  - Files: `path/to/file.ts`
  - Verify: [How to verify]

### Phase 3: Testing
- [ ] **Task 3.1**: Write unit tests
  - Files: `path/to/file.test.ts`
  - Verify: All tests pass

### Phase 4: Cleanup
- [ ] **Task 4.1**: Code review
- [ ] **Task 4.2**: Documentation update

## Notes
[Any important considerations]
```

## Task Description Format

Good task descriptions include:

```markdown
- [ ] **Create UserService class**
  - Files: `src/services/UserService.ts`
  - Actions:
    - Create new file
    - Add constructor with UserRepository dependency
    - Implement findById method
    - Implement create method
  - Verify: TypeScript compiles, unit tests pass
  - Time: ~5 min
```

## Example: API Endpoint Implementation

```markdown
# Implementation Plan: Add User Profile Endpoint

## Overview
Add GET /api/users/:id/profile endpoint to return user profile data.

## Success Criteria
- [ ] Endpoint returns 200 with profile data for valid user
- [ ] Endpoint returns 404 for non-existent user
- [ ] Endpoint requires authentication
- [ ] Response matches API specification

## Tasks

### Phase 1: Schema & Types
- [ ] **1.1**: Define ProfileResponse type
  - Files: `src/types/profile.ts`
  - Verify: TypeScript compiles

- [ ] **1.2**: Add profile fields to User model if needed
  - Files: `prisma/schema.prisma`
  - Verify: `npx prisma validate`

### Phase 2: Service Layer
- [ ] **2.1**: Add getProfile method to UserService
  - Files: `src/services/UserService.ts`
  - Verify: Unit test passes

- [ ] **2.2**: Write unit test for getProfile
  - Files: `src/services/UserService.test.ts`
  - Verify: Test runs and passes

### Phase 3: API Layer
- [ ] **3.1**: Create profile route handler
  - Files: `src/routes/users.ts`
  - Verify: Endpoint accessible

- [ ] **3.2**: Add authentication middleware
  - Files: `src/routes/users.ts`
  - Verify: Returns 401 without token

- [ ] **3.3**: Write integration test
  - Files: `src/routes/users.test.ts`
  - Verify: All scenarios covered

### Phase 4: Documentation
- [ ] **4.1**: Update OpenAPI spec
  - Files: `docs/openapi.yaml`
  - Verify: Swagger UI shows endpoint

## Estimated Time
Total: ~30 minutes
```

## Verification Methods

### Code Verification
```bash
# TypeScript compiles
npm run typecheck

# Tests pass
npm test

# Lint passes
npm run lint

# Build succeeds
npm run build
```

### Runtime Verification
```bash
# Endpoint responds
curl http://localhost:3000/api/users/1/profile

# Manual testing
# Open browser, test functionality
```

## Best Practices

1. **Start with the end** - Define success criteria first
2. **Think in phases** - Group related tasks
3. **Include verification** - Every task should be checkable
4. **Note dependencies** - Identify blockers
5. **Keep it visible** - Update as you progress
6. **Timebox tasks** - 2-5 min per task ideal

---

## Technical Design & RFC (2025)
For complex changes, use an RFC (Request for Comments) structure:
1. **Background:** Why is this change needed?
2. **Proposal:** High-level architectural decision.
3. **Trade-offs:** What are the alternatives?
4. **Security:** Prompt injection risks, data privacy.
5. **AI Risks:** Hallucimation mitigation, model drift considerations.

## When to Use

- Before starting any feature
- When refactoring code
- During sprint planning
- When onboarding others
- When work seems overwhelming
