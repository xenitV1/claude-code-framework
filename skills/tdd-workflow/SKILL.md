---
name: tdd-workflow
description: Test-Driven Development workflow with RED-GREEN-REFACTOR cycle. Use when writing new features or fixing bugs to ensure code quality and test coverage.
---

# TDD Workflow

> Source: obra/superpowers

## Overview
This skill provides a structured Test-Driven Development workflow following the RED-GREEN-REFACTOR cycle.

## The TDD Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   🔴 RED                             │
│   Write a failing test               │
│                                      │
│            ↓                         │
│                                      │
│   🟢 GREEN                           │
│   Write minimal code to pass         │
│                                      │
│            ↓                         │
│                                      │
│   🔵 REFACTOR                        │
│   Improve code, keep tests passing   │
│                                      │
│            ↓                         │
│                                      │
│   Repeat...                          │
│                                      │
└──────────────────────────────────────┘
```

## Step-by-Step Process

### Step 1: 🔴 RED - Write Failing Test

Write a test for the behavior you want to implement.

```typescript
// calculator.test.ts
describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      const calc = new Calculator();
      expect(calc.add(2, 3)).toBe(5);
    });
  });
});
```

Run the test - it should FAIL:
```bash
npm test
# ❌ ReferenceError: Calculator is not defined
```

### Step 2: 🟢 GREEN - Make Test Pass

Write the **minimum** code to make the test pass.

```typescript
// calculator.ts
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
```

Run the test - it should PASS:
```bash
npm test
# ✅ 1 test passed
```

### Step 3: 🔵 REFACTOR - Improve Code

Improve the code while keeping tests green.

```typescript
// Maybe no refactoring needed for simple code
// Or refactor if complexity grows
```

### Step 4: Repeat

Add more tests for edge cases:

```typescript
it('should handle negative numbers', () => {
  expect(calc.add(-5, 3)).toBe(-2);
});

it('should handle zero', () => {
  expect(calc.add(0, 5)).toBe(5);
});

it('should handle decimal numbers', () => {
  expect(calc.add(1.5, 2.5)).toBe(4);
});
```

## Complete Example: User Registration

### RED: Write Tests First

```typescript
// userService.test.ts
describe('UserService', () => {
  describe('register', () => {
    it('should create user with hashed password', async () => {
      const service = new UserService();
      const result = await service.register({
        email: 'test@example.com',
        password: 'SecurePass123!'
      });
      
      expect(result.id).toBeDefined();
      expect(result.email).toBe('test@example.com');
      expect(result.password).toBeUndefined(); // Not returned
    });

    it('should throw if email already exists', async () => {
      const service = new UserService();
      await service.register({ email: 'test@example.com', password: 'pass' });
      
      await expect(
        service.register({ email: 'test@example.com', password: 'pass' })
      ).rejects.toThrow('Email already exists');
    });

    it('should throw if password too weak', async () => {
      const service = new UserService();
      
      await expect(
        service.register({ email: 'test@example.com', password: '123' })
      ).rejects.toThrow('Password too weak');
    });
  });
});
```

### GREEN: Implement

```typescript
// userService.ts
class UserService {
  private users: User[] = [];

  async register(data: RegisterInput): Promise<UserResponse> {
    // Validate password strength
    if (data.password.length < 8) {
      throw new Error('Password too weak');
    }

    // Check duplicate email
    if (this.users.find(u => u.email === data.email)) {
      throw new Error('Email already exists');
    }

    // Create user
    const user: User = {
      id: crypto.randomUUID(),
      email: data.email,
      passwordHash: await bcrypt.hash(data.password, 12)
    };

    this.users.push(user);

    // Return without password
    return { id: user.id, email: user.email };
  }
}
```

### REFACTOR: Improve

```typescript
// Extract validation
private validatePassword(password: string): void {
  if (password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }
  if (!/[A-Z]/.test(password)) {
    throw new ValidationError('Password must contain uppercase');
  }
  // More validations...
}

// Use repository pattern
constructor(private userRepo: UserRepository) {}

async register(data: RegisterInput): Promise<UserResponse> {
  this.validatePassword(data.password);
  
  const existing = await this.userRepo.findByEmail(data.email);
  if (existing) {
    throw new ConflictError('Email already exists');
  }
  
  const user = await this.userRepo.create({
    email: data.email,
    passwordHash: await bcrypt.hash(data.password, 12)
  });
  
  return this.toResponse(user);
}
```

## TDD Rules

### The Three Laws of TDD

1. **Write production code only to make a failing test pass**
2. **Write only enough of a test to demonstrate failure**
3. **Write only enough production code to make the test pass**

### Best Practices

✅ **DO:**
- Write test first
- Run tests frequently
- Keep tests fast
- Test behavior, not implementation
- Refactor with confidence

❌ **DON'T:**
- Skip the RED phase
- Write tests after code
- Test private methods directly
- Over-engineer initial solution
- Refactor without tests passing

## When to Use TDD

**Great for:**
- New features
- Bug fixes (write test that reproduces bug first)
- API design
- Complex business logic

## AI-Augmented TDD (2025)

Collaborative loop between human and AI agents:
1. **Human/Agent A (RED):** Defines the interface and writes failing tests.
2. **Agent B (GREEN):** Implements the minimum code to pass.
3. **Agent C (REFACTOR):** Optimizes for performance and best practices.

## Property-Based Testing
Use `fast-check` to find edge cases automatically:
```typescript
import fc from 'fast-check';

test('add is commutative', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (a, b) => {
      return add(a, b) === add(b, a);
    })
  );
});
```
