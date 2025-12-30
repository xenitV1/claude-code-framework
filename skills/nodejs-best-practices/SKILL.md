---
name: nodejs-best-practices
description: Node.js best practices including error handling, async patterns, security, and project structure.
---

# Node.js Best Practices

## Project Structure

```
src/
├── controllers/    # HTTP request handlers
├── services/       # Business logic (Pure functions)
├── repositories/   # Data access (Drizzle/SQLite)
├── middleware/     # Hono/Fastify middleware
├── utils/          # AbortController & Stream helpers
├── config/         # Zod-validated configuration
└── index.ts        # Entry point (Native TS)
```

## Error Handling

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string
  ) {
    super(message);
  }
}

// Async error wrapper
const asyncHandler = (fn: RequestHandler) => (
  req: Request, res: Response, next: NextFunction
) => Promise.resolve(fn(req, res, next)).catch(next);

// Global error handler (RFC 7807 compliant)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  const statusCode = err instanceof AppError ? err.statusCode : 500;
  res.status(statusCode).json({
    type: "https://example.com/probs/" + (err instanceof AppError ? err.code : "internal-error"),
    title: err.message,
    status: statusCode
  });
});
```

## Modern Runtime Features (Node.js 23+)

### Native TypeScript (Strip Types)
Run TS files directly without transpile step:
```bash
node --experimental-strip-types src/index.ts
```

### Built-in Test Runner
```typescript
import { test, describe } from 'node:test';
import assert from 'node:assert';

test('business logic', async () => {
  assert.strictEqual(add(1, 2), 3);
});
```

### Native SQLite
```typescript
import { DatabaseSync } from 'node:sqlite';
const db = new DatabaseSync('local.db');
db.exec("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)");
```

## Async Patterns

```typescript
// Promise.all for parallel operations
const [users, posts] = await Promise.all([
  userRepo.findAll(),
  postRepo.findAll()
]);

// Promise.allSettled for non-critical failures
const results = await Promise.allSettled([
  sendEmail(user),
  updateAnalytics(user)
]);
```

## Environment Variables

```typescript
// Validate on startup
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing: ${envVar}`);
  }
}
```

## Security

```typescript
// Helmet for headers
app.use(helmet());

// Rate limiting
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// Input validation
const schema = z.object({ email: z.string().email() });
```
