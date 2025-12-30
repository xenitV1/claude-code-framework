---
name: parallel-agents
description: Concurrent subagent workflows for parallel task execution. Use when multiple independent tasks can run simultaneously.
---

# Parallel Agents

> Source: obra/superpowers

## Overview
This skill enables executing multiple independent tasks in parallel using subagents.

## When to Use Parallel Agents

✅ **Good for:**
- Independent tasks (no dependencies)
- Code analysis from multiple perspectives
- Generating multiple alternatives
- Parallel file processing

❌ **Not for:**
- Sequential dependencies
- Tasks that share state
- When one task's output is another's input

## 2-Stage Pattern

### Stage 1: Parallel Execution
Spawn multiple agents working independently.

```markdown
## Parallel Tasks
| Agent | Task | Status |
|-------|------|--------|
| Agent 1 | Core Architecture Review | ⏳ |
| Agent 2 | Frontend (React/UI) | ⏳ |
| Agent 3 | Backend (API/Logic) | ⏳ |
| Agent 4 | Database & Schema | ⏳ |
| Agent 5 | Security & Auth | ⏳ |
| Agent 6 | DevOps & Deployment | ⏳ |
| Agent 7 | Performance Audit | ⏳ |
| Agent 8 | Test Coverage | ⏳ |
| Agent 9 | Documentation Audit | ⏳ |
| Agent 10 | Mobile UX/Patterns | ⏳ |
| Agent 11 | Debugging & Root Cause | ⏳ |
| Agent 12 | Project Planning | ⏳ |
| Agent 13 | Orchestration Check | ⏳ |
| Agent 14 | Research & Discovery | ⏳ |
```

### Stage 2: Synthesis
Combine results into coherent output.

```markdown
## Combined Results
- Finding from Agent 1
- Finding from Agent 2
- Finding from Agent 3

## Final Recommendation
[Synthesized conclusion]
```

## Task Distribution

```markdown
## Project Analysis (Parallel)

### Agent 1: Architecture Review
Focus: System design, scalability
Files: Entire codebase

### Agent 2: Frontend Review
Focus: React components, UI/UX
Files: src/components/**

### Agent 3: Backend Review
Focus: API endpoints, business logic
Files: src/api/**, src/services/**

### Agent 4: Database Architect
Focus: Schema design, Prisma, migrations
Files: prisma/**, src/db/**

### Agent 5: Security Auditor
Focus: Auth, input validation, vulnerabilities
Files: All security-sensitive code

### Agent 6: DevOps Review
Focus: CI/CD, deployment config, PM2
Files: .github/**, ecosystem.config.js

### Agent 7: Performance Review
Focus: Bundle size, query optimization
Files: src/**

### Agent 8: Test Engineer
Focus: Test coverage, edge cases
Files: tests/**, **/*.test.ts

### Agent 9: Doc Writer
Focus: READMEs, API docs, code comments
Files: **/*.md, src/**

### Agent 10: Mobile Review
Focus: React Native patterns, Expo
Files: apps/mobile/**

### Agent 11: Debugger
Focus: Root cause analysis of known issues
Files: Source code, logs

### Agent 12: Project Planner
Focus: Task breakdown, milestones
Files: CLAUDE.md, plan.md

### Agent 13: Orchestrator
Focus: Multi-agent coordination and synergy
Files: System-wide

### Agent 14: Explorer Agent
Focus: Dependency graph, tech stack research, codebase mapping
Files: Entire codebase
```

## Result Aggregation

```markdown
## Aggregated Findings

### High Priority (All agents agree)
1. [Finding]
2. [Finding]

### Medium Priority (Some agents found)
1. [Finding]

### Low Priority (Single agent)
1. [Finding]
```

## Multi-Agent Orchestration (2025)

### Swarm Architecture
A decentralized model where agents "hand off" tasks dynamically:
- **Agent A (Researcher)** → Finds documentation.
- **Agent B (Architect)** → Designs the plan based on A's findings.
- **Agent C (Executor)** → Implements the plan.

### Agentic Consensus (Synthesis)
When parallel agents disagree, use a "Critic" agent:
1. Agents 1-3 provide independent solutions.
2. Agent 4 (Critic) evaluates all three for:
   - Security compliance.
   - Performance impact.
   - Code style consistency.
3. Final output is the consensus or the best-evaluated path.

## Best Practices

1. **Clear scope** - Define exactly what each agent does
2. **Independent tasks** - No dependencies between agents
3. **Consistent format** - All agents report in same format
4. **Synthesis step** - Always combine/review results
5. **Time boxing** - Set max time per agent
