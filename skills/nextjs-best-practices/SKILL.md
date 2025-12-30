---
name: nextjs-best-practices
description: Next.js 14+ best practices with App Router, Server Components, and modern patterns.
---

# Next.js Best Practices

## App Router Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   └── page.tsx        # /dashboard
├── api/
│   └── users/
│       └── route.ts    # /api/users
└── components/
    └── Header.tsx
```

## Server vs Client Components

```tsx
// Server Component (default)
async function UserProfile({ userId }: { userId: string }) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return <div>{user.name}</div>;
}

// Client Component
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## Data Fetching

```tsx
// Server Component fetching
async function Posts() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 } // ISR: revalidate every 60s
  }).then(r => r.json());
  
  return <PostList posts={posts} />;
}
```

## API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

## Metadata

```tsx
// Static metadata
export const metadata = {
  title: 'My App',
  description: 'Welcome to my app'
};

// Dynamic metadata
export async function generateMetadata({ params }: Props) {
  const post = await getPost(params.id);
  return { title: post.title };
}
```

## Loading & Error States

```tsx
// loading.tsx
export default function Loading() {
  return <div className="animate-pulse">Loading...</div>;
}

// error.tsx
'use client';

export default function Error({ error, reset }: { 
  error: Error; 
  reset: () => void 
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Best Practices

1. **Server Components by default** - Only use 'use client' when needed
2. **Colocate files** - Keep related files together
3. **Use loading.tsx** - Better UX with loading states
4. **Optimize images** - Use next/image
5. **Route groups** - (marketing), (dashboard) for organization
