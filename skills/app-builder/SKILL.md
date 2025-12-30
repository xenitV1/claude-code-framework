---
name: app-builder
description: Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. Use for creating new applications, scaffolding projects, or building features from scratch.
---

# App Builder - Application Building Orchestrator

## Purpose
Analyzes user's natural language requests, determines the appropriate tech stack, plans project structure, and coordinates expert agents to create a working application.

---

## 1. Project Type Detection

### 1.1 Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| api, backend, service, rest | API Service | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe, payment | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation, content | Documentation | astro-static |
| extension, plugin, chrome, browser | Browser Extension | chrome-extension |
| desktop, electron, windows, mac | Desktop App | electron-desktop |
| cli, command line, terminal, tool | CLI Tool | cli-tool |
| monorepo, workspace, multi-package | Monorepo | monorepo-turborepo |

### 1.2 Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → forward to conversation-manager
5. Suggest tech stack
```

---

## 2. Tech Stack Selection

### 2.1 Default Stack (Web App - 2025)

```yaml
Frontend:
  framework: Next.js 15 (Stable)
  language: TypeScript 5.7+
  styling: Tailwind CSS v4 (Alpha/Stable)
  state: React 19 Actions / Server Components
  bundler: Turbopack (Stable for Dev)

Backend:
  runtime: Node.js 23 (Native Test Runner)
  framework: Next.js API Routes / Hono (for Edge)
  validation: Zod / TypeBox

Database:
  primary: PostgreSQL
  orm: Prisma / Drizzle
  hosting: Supabase / Neon

Auth:
  provider: Auth.js (v5) / Clerk

Monorepo:
  tool: Turborepo 2.0 (New Terminal UI)
```

### 2.2 Alternative Options

| Need | Default | Alternative |
|------|---------|-------------|
| Real-time | - | Supabase Realtime, Socket.io |
| File storage | - | Cloudinary, S3 |
| Payment | Stripe | LemonSqueezy, Paddle |
| Email | - | Resend, SendGrid |
| Search | - | Algolia, Typesense |

---

## 3. Agent Coordination

### 3.1 Agent Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   APP BUILDER (Orchestrator)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PROJECT PLANNER                          │
│  • Task breakdown                                            │
│  • Dependency graph                                          │
│  • File structure planning                                   │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ DATABASE        │ │ BACKEND         │ │ FRONTEND        │
│ ARCHITECT       │ │ SPECIALIST      │ │ SPECIALIST      │
│                 │ │                 │ │                 │
│ • Schema design │ │ • API routes    │ │ • Components    │
│ • Migrations    │ │ • Controllers   │ │ • Pages         │
│ • Seed data     │ │ • Middleware    │ │ • Styling       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 PARALLEL PHASE (Optional)                    │
│  • Security Auditor → Vulnerability check                   │
│  • Test Engineer → Unit tests                               │
│  • Performance Optimizer → Bundle analysis                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DEVOPS ENGINEER                          │
│  • Environment setup                                         │
│  • Preview deployment                                        │
│  • Health check                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Execution Order

| Phase | Agent(s) | Parallel? | Prerequisite |
|-------|----------|-----------|--------------|
| 1 | Project Planner | ❌ | - |
| 2 | Database Architect | ❌ | Plan ready |
| 3 | Backend Specialist | ❌ | Schema ready |
| 4 | Frontend Specialist | ✅ | API ready (partial) |
| 5 | Security Auditor, Test Engineer | ✅ | Code ready |
| 6 | DevOps Engineer | ❌ | All code ready |

---

## 4. Project Scaffolding

### 4.1 Directory Structure (Next.js Full-Stack)

```
project-name/
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── api/
│   │   │   └── [resource]/
│   │   │       └── route.ts
│   │   └── [feature]/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   └── [feature]/
│   ├── lib/
│   │   ├── db.ts
│   │   ├── auth.ts
│   │   └── utils.ts
│   ├── hooks/
│   └── types/
├── public/
├── .env.example
├── .env.local
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

### 4.2 Core Files

Files automatically created for every project:
- `package.json` - Dependencies
- `tsconfig.json` - TypeScript config
- `tailwind.config.ts` - Tailwind config
- `.env.example` - Environment variables template
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules
- `prisma/schema.prisma` - Database schema

---

## 5. Feature Building

### 5.1 Feature Analysis

```
Request: "add payment system"

Analysis:
├── Required Changes:
│   ├── Database: orders, payments tables
│   ├── Backend: /api/checkout, /api/webhooks/stripe
│   ├── Frontend: CheckoutForm, PaymentSuccess
│   └── Config: Stripe API keys
│
├── Dependencies:
│   ├── stripe package
│   └── Existing user authentication
│
└── Estimated Time: 15-20 minutes
```

### 5.2 Iterative Enhancement

```
1. Analyze existing project
2. Create change plan
3. Present plan to user
4. Get approval
5. Apply changes
6. Test
7. Show preview
```

---

## 6. Context Management

### 6.1 Project State

```json
{
  "projectPath": "/path/to/project",
  "projectType": "nextjs-ecommerce",
  "techStack": {
    "frontend": "next.js",
    "database": "postgresql",
    "auth": "clerk"
  },
  "features": ["product-listing", "cart", "checkout"],
  "pendingFeatures": ["admin-panel"],
  "lastModified": "2025-12-30T08:00:00Z"
}
```

### 6.2 Context Loading

```
At session start:
1. Read current-project.json
2. Load project state
3. Restore conversation history
4. Present summary to user (optional)
```

---

## 7. Error Handling

### 7.1 Build Errors

```
Error Type → Solution Strategy:

TypeScript Error → Fix type, add missing import
Missing Dependency → Run npm install
Port Conflict → Suggest alternative port
Database Error → Check migration, validate connection string
```

### 7.2 Recovery Strategy

```
1. Detect error
2. Try automatic fix
3. If failed, report to user
4. Suggest alternative
5. Rollback if necessary
```

---

## 8. Integration Points

This skill integrates with the following skills and agents:

| Component | Role |
|-----------|------|
| `conversation-manager` | User communication, Q&A |
| `project-planner` agent | Task breakdown, dependency graph |
| `frontend-specialist` agent | UI components, pages |
| `backend-specialist` agent | API, business logic |
| `database-architect` agent | Schema, migrations |
| `devops-engineer` agent | Deployment, preview |
| `progress-reporter` script | Real-time status updates |

---

## 9. Usage Example

```
User: "Make an Instagram clone with photo sharing and likes"

App Builder Process:
1. Project type: Social Media App
2. Tech stack: Next.js + Prisma + Cloudinary + Clerk
3. 
   ┌─ Create plan
   ├─ Database schema (users, posts, likes, follows)
   ├─ API routes (12 endpoints)
   ├─ Pages (feed, profile, upload)
   └─ Components (PostCard, Feed, LikeButton)
4. Coordinate agents
5. Report progress
6. Start preview
7. Notify user when complete
```
