---
name: database-design
description: Database design patterns including normalization, indexing, query optimization, and PostgreSQL best practices. Use when designing schemas, optimizing queries, or planning migrations.
---

# Database Design

## Overview
This skill covers database design principles, PostgreSQL best practices, and query optimization techniques.

## Normalization

### First Normal Form (1NF)
- Atomic values (no arrays or nested objects in columns)
- No repeating groups

```sql
-- ❌ BAD: Repeating groups
CREATE TABLE orders (
    id INT PRIMARY KEY,
    item1 VARCHAR(100),
    item2 VARCHAR(100),
    item3 VARCHAR(100)
);

-- ✅ GOOD: Separate table
CREATE TABLE orders (id INT PRIMARY KEY);
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    item VARCHAR(100)
);
```

### Second Normal Form (2NF)
- 1NF + No partial dependencies
- All non-key columns depend on entire primary key

### Third Normal Form (3NF)
- 2NF + No transitive dependencies
- Non-key columns depend only on primary key

## Schema Design

### Well-Designed Schema
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' 
        CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for email lookups
CREATE INDEX idx_users_email ON users(email);

-- Posts table
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    content TEXT,
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMPTZ,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Composite index for user's published posts
CREATE INDEX idx_posts_user_published ON posts(user_id, published, created_at DESC);

-- Tags table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE
);

-- Many-to-many junction table
CREATE TABLE post_tags (
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

## Indexing Strategy

### When to Index
- Columns used in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY
- Foreign key columns

### Index Types
```sql
-- B-tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (multi-column)
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at DESC);

-- Partial index (conditional)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- GIN index (for JSONB, arrays, full-text)
CREATE INDEX idx_posts_metadata ON posts USING GIN(metadata);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

## Query Optimization

### EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE 
SELECT * FROM posts 
WHERE user_id = '123' AND published = true 
ORDER BY created_at DESC 
LIMIT 10;
```

### Common Optimizations
```sql
-- ❌ BAD: SELECT * (fetches all columns)
SELECT * FROM users WHERE id = '123';

-- ✅ GOOD: Select only needed columns
SELECT id, name, email FROM users WHERE id = '123';

-- ❌ BAD: LIKE with leading wildcard (no index)
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- ✅ GOOD: Use reverse index or full-text search
SELECT * FROM users WHERE email LIKE 'user%';

-- ❌ BAD: OR conditions (may skip index)
SELECT * FROM posts WHERE user_id = '1' OR user_id = '2';

-- ✅ GOOD: Use IN
SELECT * FROM posts WHERE user_id IN ('1', '2');
```

### N+1 Problem
```sql
-- ❌ BAD: N+1 queries
-- 1: SELECT * FROM posts
-- N: SELECT * FROM users WHERE id = ?

-- ✅ GOOD: Single JOIN
SELECT p.*, u.name as author_name
FROM posts p
JOIN users u ON p.user_id = u.id;
```

## Migrations

### Safe Migration Pattern
```sql
-- Step 1: Add column as nullable (non-blocking)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill in batches
UPDATE users SET phone = '' WHERE phone IS NULL LIMIT 1000;

-- Step 3: Add NOT NULL after backfill
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- Step 4: Add index concurrently (non-blocking)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);
```

## Modern Database Patterns (2025)

### Drizzle ORM (Edge-Ready)
```typescript
// schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  fullName: text('full_name'),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});

// Implementation (Neon / Turso)
const db = drizzle(client);
const result = await db.select().from(users).where(eq(users.id, 1));
```

### Vector Indexing (AI Support)
```sql
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Add vector column (1536 dimensions for OpenAI)
ALTER TABLE documents ADD COLUMN embedding vector(1536);

-- HNSW Index for fast similarity search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Querying with Cosine Similarity
SELECT content FROM documents 
ORDER BY embedding <=> '[0.1, 0.2, ...]' 
LIMIT 5;
```

### Edge Capabilities
- **LibSQL (Turso):** Optimized for low-latency edge nodes.
- **Neon:** Serverless Postgres with instant branching for dev environments.

## PostgreSQL Features

### JSONB
```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    data JSONB NOT NULL
);

-- Query JSONB
SELECT * FROM events WHERE data->>'type' = 'click';
SELECT * FROM events WHERE data @> '{"type": "click"}';

-- Index JSONB
CREATE INDEX idx_events_data ON events USING GIN(data);
```

### Common Table Expressions (CTE)
```sql
WITH active_users AS (
    SELECT id, name FROM users WHERE status = 'active'
),
user_posts AS (
    SELECT user_id, COUNT(*) as post_count
    FROM posts
    GROUP BY user_id
)
SELECT au.name, COALESCE(up.post_count, 0) as posts
FROM active_users au
LEFT JOIN user_posts up ON au.id = up.user_id;
```

## Best Practices

1. **Use UUIDs** for primary keys (better for distributed systems)
2. **Always add timestamps** (created_at, updated_at)
3. **Use constraints** (NOT NULL, CHECK, UNIQUE)
4. **Index foreign keys** for JOIN performance
5. **Use appropriate types** (TIMESTAMPTZ, not VARCHAR for dates)
6. **Document schema** with comments
