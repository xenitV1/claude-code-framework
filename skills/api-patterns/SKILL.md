---
name: api-patterns
description: REST API design patterns including resource naming, HTTP methods, status codes, versioning, pagination, and response formats. Use when designing or implementing APIs.
---

# API Patterns

## Overview
This skill covers REST API design best practices for building clean, consistent, and scalable APIs.

## Resource Naming

### URL Structure
```
✅ GOOD:
GET    /users              List all users
GET    /users/123          Get user 123
POST   /users              Create new user
PUT    /users/123          Update user 123
PATCH  /users/123          Partial update
DELETE /users/123          Delete user 123

GET    /users/123/posts    Get user's posts
POST   /users/123/posts    Create post for user

❌ BAD:
GET    /getUsers
GET    /user/list
POST   /createUser
GET    /getUserById/123
```

### Conventions
- Use nouns, not verbs (resources, not actions)
- Use plural forms (`/users` not `/user`)
- Use lowercase with hyphens (`/user-profiles`)
- Nest related resources (`/users/123/posts`)

## HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Replace resource | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove resource | Yes | No |

## Status Codes

### Success (2xx)
```
200 OK           - Success (GET, PUT, PATCH)
201 Created      - Resource created (POST)
204 No Content   - Success, no body (DELETE)
```

### Client Errors (4xx)
```
400 Bad Request  - Invalid input
401 Unauthorized - Missing/invalid auth
403 Forbidden    - Valid auth, no permission
404 Not Found    - Resource doesn't exist
409 Conflict     - Duplicate or conflict
422 Unprocessable- Validation failed
429 Too Many     - Rate limit exceeded
```

### Server Errors (5xx)
```
500 Internal     - Server error
502 Bad Gateway  - Upstream error
503 Unavailable  - Service down
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2025-01-01T12:00:00Z"
  }
}
```

### List Response with Pagination
```json
{
  "success": true,
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "prev": null,
    "first": "/users?page=1",
    "last": "/users?page=5"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "message": "Must be a positive number"
      }
    ]
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "requestId": "req_abc123"
}
```

## Versioning

### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
GET /users
Accept: application/vnd.api+json; version=1
```

## Pagination

### Offset Pagination
```
GET /users?page=2&limit=20
```

### Cursor Pagination (Better for large datasets)
```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

## Filtering & Sorting

```
GET /users?status=active&role=admin
GET /users?sort=-createdAt,name
GET /users?fields=id,name,email
GET /products?price[gte]=10&price[lte]=100
```

## Implementation Example

```typescript
// Express.js API implementation
import { Router } from 'express';

const router = Router();

// List with pagination
router.get('/users', async (req, res) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 20;
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    userRepository.findMany({ skip: offset, take: limit }),
    userRepository.count()
  ]);

  res.json({
    success: true,
    data: users,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
});

// Create
router.post('/users', async (req, res) => {
  const validation = userSchema.safeParse(req.body);
  if (!validation.success) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        details: validation.error.errors
      }
    });
  }

  const user = await userService.create(validation.data);
  res.status(201).json({ success: true, data: user });
});
```

## Best Practices

1. **Consistency**: Same patterns across all endpoints
2. **Documentation**: Use OpenAPI/Swagger
3. **Validation**: Validate all input
4. **Error Handling**: Consistent error format
5. **Rate Limiting**: Protect from abuse
6. **HATEOAS**: Include related links
