---
name: testing-patterns
description: Testing patterns and best practices including unit tests, integration tests, mocking, and test organization. Use when writing tests or setting up testing infrastructure.
---

# Testing Patterns

## Overview
This skill covers testing best practices, patterns, and strategies for reliable test suites.

## Testing Pyramid

```
        /\        E2E (Few)
       /  \       - Critical user flows
      /----\      
     /      \     Integration (Some)
    /--------\    - API endpoints, DB queries
   /          \   
  /------------\  Unit (Many)
                  - Individual functions
```

## AAA Pattern

Every test follows **Arrange-Act-Assert**:

```typescript
describe('Calculator', () => {
  it('should add two numbers', () => {
    // Arrange
    const calculator = new Calculator();
    const a = 5;
    const b = 3;

    // Act
    const result = calculator.add(a, b);

    // Assert
    expect(result).toBe(8);
  });
});
```

## Unit Testing

### Vitest 2.0 Example
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks(); // Use 'vi' instead of 'jest'
  });

  it('should find user', async () => {
    const mockUser = { id: '1', name: 'Mehmet' };
    vi.mock('./repository', () => ({ find: vi.fn().mockResolvedValue(mockUser) }));
    // ...
  });
});
```

## Contract Testing (MSW 2.0)
Mock network at the protocol level for integration tests:
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/user', () => {
    return HttpResponse.json({ id: '1', name: 'John' });
  })
);
```

### Pytest Example
```python
# test_user_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.user_service import UserService

class TestUserService:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        return UserService(repository=mock_repository)

    def test_find_by_id_returns_user(self, service, mock_repository):
        # Arrange
        mock_user = {"id": "123", "name": "John"}
        mock_repository.find_by_id.return_value = mock_user

        # Act
        result = service.find_by_id("123")

        # Assert
        assert result == mock_user
        mock_repository.find_by_id.assert_called_once_with("123")

    def test_find_by_id_raises_when_not_found(self, service, mock_repository):
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundError):
            service.find_by_id("999")
```

## Integration Testing

### API Integration Test
```typescript
// users.integration.test.ts
import request from 'supertest';
import { app } from '../app';
import { db } from '../database';
import { createTestUser } from './factories';

describe('Users API', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear('users');
  });

  describe('POST /users', () => {
    it('should create user and return 201', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/users')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.email).toBe(userData.email);
      expect(response.body.data).not.toHaveProperty('password');
    });

    it('should reject invalid email and return 400', async () => {
      const response = await request(app)
        .post('/users')
        .send({ email: 'invalid', name: 'Test', password: 'pass' })
        .expect(400);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('GET /users/:id', () => {
    it('should return user by id', async () => {
      const user = await createTestUser();

      const response = await request(app)
        .get(`/users/${user.id}`)
        .expect(200);

      expect(response.body.data.id).toBe(user.id);
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/users/non-existent-id')
        .expect(404);
    });
  });
});
```

## Mocking

### Mock Functions
```typescript
// Simple mock
const mockFn = jest.fn();
mockFn.mockReturnValue(42);

// Async mock
mockFn.mockResolvedValue({ data: 'async result' });
mockFn.mockRejectedValue(new Error('Failed'));

// Implementation mock
mockFn.mockImplementation((x) => x * 2);
```

### Mock Modules
```typescript
// Mock entire module
jest.mock('./emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue({ sent: true })
}));

// Partial mock
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  fetchData: jest.fn()
}));
```

## Test Factories

```typescript
// factories/user.factory.ts
import { faker } from '@faker-js/faker';

export function createUserData(overrides = {}) {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    password: faker.internet.password({ length: 12 }),
    ...overrides
  };
}

export async function createTestUser(overrides = {}) {
  const data = createUserData(overrides);
  return await db.user.create({ data });
}
```

## Best Practices

1. **Descriptive Names**: `should return error when email is invalid`
2. **One Assert Per Test**: Focus on single behavior
3. **Independent Tests**: No test dependencies
4. **Clean Up**: Reset state between tests
5. **Fast Tests**: Unit tests < 100ms
6. **Avoid Implementation Details**: Test behavior
7. **Use Factories**: Consistent test data
8. **CI Integration**: Run tests automatically
