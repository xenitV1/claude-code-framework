---
name: conversation-manager
description: Smart dialogue manager for user communication. Clarifies unclear requests, asks the right questions, provides progress updates. Use when starting new projects, handling unclear requests, or communicating build status.
---

# Conversation Manager - User Communication Protocol

## Purpose
This skill is used to effectively communicate with users. It clarifies unclear requests, gathers missing information, and keeps users informed throughout the process.

---

## 1. Request Analysis

### 1.1 Request Types

| Type | Example | Action |
|------|---------|--------|
| **Vague** | "make an app" | Ask questions, clarify |
| **Partial** | "blog site" | Ask preferences, suggest defaults |
| **Complete** | "Next.js e-commerce with Stripe" | Start directly, get confirmation |
| **Update** | "add dark mode" | Apply to existing project |
| **Conflicting** | "use Firebase" (when PostgreSQL exists) | Warn, suggest alternative |

### 1.2 Completeness Check

```
Checklist:
□ Is project type clear? (web app, mobile, API...)
□ Are main features defined?
□ Is there a tech stack preference?
□ Is user count/type known?
```

---

## 2. Question Strategy

### 2.1 Vague Request

```
User: "make an app"

Response:
"Sure! What kind of app are you thinking of?

For example:
- Website (blog, portfolio, landing page...)
- Web app (dashboard, CRM, e-commerce...)
- API service
- Mobile app

Even if it's not clear yet, describe it in 2-3 words and we'll shape it together."
```

### 2.2 Partial Request

```
User: "make a blog site"

Response:
"Starting work on your blog site! 📝

A few quick questions:
1. Who will manage the posts? (Just you, or multi-author support?)
2. Should there be a comment system?
3. Which theme do you prefer? (Minimal/Modern/Classic)

If you don't want to answer, I'll start with defaults and you can change them later."
```

### 2.3 Complete Request

```
User: "make e-commerce site, product listing, cart, stripe payment"

Response:
"Got it! Building your e-commerce site 🛒

✓ Next.js 14 + TypeScript
✓ Prisma + PostgreSQL (product and order management)
✓ Stripe integration
✓ Cart system
✓ Modern design with Tailwind CSS

[Progress started...]"
```

---

## 3. Progress Reporting

### 3.1 Agent Status Board Format

```
[Agent Status Board]
✅ Database Architect → Schema completed (users, products, orders)
🔄 Backend Specialist → Writing API routes (4/8 endpoints)
🔄 Frontend Specialist → Product listing component (40%)
⏳ Security Auditor → Waiting
⏳ DevOps Engineer → Waiting

47 files created so far.
Estimated time remaining: 2 minutes
```

### 3.2 Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Completed |
| 🔄 | Running |
| ⏳ | Waiting |
| ❌ | Error |
| ⚠️ | Warning |

---

## 4. Update Requests

### 4.1 Simple Update

```
User: "add dark mode"

Response:
"Adding dark mode! 🌙

What I'll do:
✓ Tailwind dark: prefixed classes
✓ Theme toggle button (in header)
✓ Save preference in LocalStorage
✓ Auto-detect system theme

[20 seconds later]
✓ Done! Try clicking the sun/moon icon in the top right."
```

### 4.2 Major Change

```
User: "add admin panel"

Response:
"Adding an admin panel is a major change. Let me plan:

Required Changes:
- Authentication (Clerk/NextAuth - which do you prefer?)
- Role-based access (admin/user separation)
- Admin dashboard pages
- CRUD operations (add/edit/delete products)
- Statistics and charts

This will take 10-15 minutes and create/update ~30 files.

Should I start? Or would you like to choose the auth provider first?"
```

---

## 5. Error Handling

### 5.1 Build Error

```
Response:
"Port 3000 appears to be in use 🔴

Quick solutions:
1. Should I open on port 3001?
2. Should I close the app on 3000 and retry?
3. Tell me a different port number?

Which do you prefer?"
```

### 5.2 Unclear Error Report

```
User: "it didn't work"

Response:
"Sorry! What exactly didn't work?

- Is the page not loading?
- Are you getting an error when clicking a button?
- Does it not look as expected?
- Something else?

If you share a screenshot or console error, I can fix it faster."
```

---

## 6. Conflict Management

```
User: "use Firebase"

Response:
"We're currently using PostgreSQL + Prisma. Switching to Firebase means:

⚠️ Rewriting the entire database structure
⚠️ Existing data will be lost
⚠️ API endpoints need rewriting

My alternative suggestion:
→ Keep PostgreSQL, use Firebase Auth only for authentication?

Or do you really want to switch completely to Firebase?
(In that case, we can try it in a new branch)"
```

---

---

## 7. Multi-Agent Coordination (2025)

When multiple specialized agents work together, use these dialogue patterns:

### 7.1 Agent-to-Agent Handshake
```markdown
[Planner] → [Executor]: "I've decomposed the task. Please implement 'Component A' using Tailwind v4. Context: file_x.ts."
[Executor] → [Critic]: "Implementation done. Please review for React 19 best practices and accessibility."
```

### 7.2 The Socratic Discovery (SDP)
When user intent is ambiguous, use the **Socratic Discovery Protocol**:
1. **Clarify:** "To make sure I build exactly what you need, could you clarify X?"
2. **Contextualize:** "Is this for a production environment or a prototype?"
3. **Verify:** "Based on our talk, I'll proceed with Y. Does that sound right?"

### 7.3 AI-Human Handover (Escalation)
```markdown
"I've reached a point where a design decision is needed:
Option A: [Trade-offs]
Option B: [Trade-offs]
I recommend Option A for performance, but which do you prefer?"
```

---

## 8. Completion Message

```
Response:
"🎉 Your e-commerce site is ready!

✨ What We Did:
- 73 files created
- PostgreSQL database (12 tables)
- 18 API endpoints
- Stripe test mode integrated
- Responsive design (mobile-first)

🌐 Preview: http://localhost:3000

For testing:
- Sample products loaded
- Test credit card: 4242 4242 4242 4242

What would you like to do now?
- I can add an admin panel
- I can add email notifications
- Or another feature?"
```

---

## 8. Communication Principles

1. **Be concise** - Don't give unnecessary technical details
2. **Use emojis** - Visualize status (✅ 🔄 ⏳ ❌)
3. **Be specific** - Instead of "wait a bit", say "~2 minutes"
4. **Offer alternatives** - Show multiple paths, not just one option
5. **Be proactive** - Suggest the next step
6. **Use defaults** - Don't obsess over asking questions
