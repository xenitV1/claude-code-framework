---
name: brainstorming
description: Structured brainstorming technique using Socratic dialogue to clarify problems, explore solutions, and refine ideas. Use when starting new projects, solving complex problems, or when direction is unclear.
---

# Brainstorming

> Source: obra/superpowers

## Overview
This skill provides a structured brainstorming approach using Socratic questioning to deeply understand problems before jumping to solutions.

## Socratic Discovery Protocol (2025)

Interactive questioning protocol used by agents to discover user intent:

1. **Assume Nothing:** Ask clarifying questions instead of making assumptions in ambiguous situations.
2. **Query the 'Why':** Ask "Why are we choosing this architecture?" before a technical decision.
3. **Think Beyond:** Analyze side effects by asking "How will this change affect the system 2 steps from now?".
4. **Human-in-the-loop:** Request approval/feedback via `notify_user` for critical decisions.

## The Socratic Approach

Instead of immediately providing solutions, ask clarifying questions:

### 1. Problem Clarification
```
"What specific problem are you trying to solve?"
"Who will be using this solution?"
"What happens if this problem isn't solved?"
"What have you already tried?"
```

### 2. Scope Definition
```
"What's the minimum viable version?"
"What features are must-haves vs nice-to-haves?"
"What are the constraints (time, budget, tech)?"
"What can we defer to a later phase?"
```

### 3. Success Criteria
```
"How will you know if this is successful?"
"What metrics matter?"
"What does 'done' look like?"
"Who needs to approve this?"
```

### 4. Risk Assessment
```
"What could go wrong?"
"What are the biggest unknowns?"
"What dependencies exist?"
"What's the rollback plan?"
```

## Brainstorming Session Structure

### Phase 1: Understand (15 min)
- Listen to the problem statement
- Ask clarifying questions
- Identify key stakeholders
- Map the current state

### Phase 2: Explore (20 min)
- Generate multiple solutions
- No criticism at this stage
- Build on ideas
- Consider unconventional approaches

### Phase 3: Evaluate (15 min)
- Review each option
- Identify pros/cons
- Consider feasibility
- Rank by impact vs effort

### Phase 4: Refine (10 min)
- Select top 1-3 approaches
- Detail implementation
- Identify first steps
- Assign ownership

## Question Templates

### For New Projects
```
1. "Describe what you're building in one sentence"
2. "Who is the primary user?"
3. "What's the #1 thing they need to accomplish?"
4. "What existing solutions are they using today?"
5. "Why isn't the current solution working?"
```

### For Bug Fixes
```
1. "What is the expected behavior?"
2. "What is the actual behavior?"
3. "When did this start happening?"
4. "Can you reproduce it consistently?"
5. "What changed recently?"
```

### For Architecture Decisions
```
1. "What are the key quality attributes? (performance, scalability, maintainability)"
2. "What's the expected load/scale?"
3. "What's the team's expertise?"
4. "What systems does this integrate with?"
5. "What's the 5-year vision?"
```

## Anti-Patterns to Avoid

❌ **Jumping to solutions** before understanding the problem
❌ **Assuming requirements** without asking
❌ **Over-engineering** the first version
❌ **Ignoring constraints** (time, budget, skills)
❌ **Solving the wrong problem** due to miscommunication

## Output Format

After brainstorming, summarize:

```markdown
## Problem Statement
[Clear, concise description of the problem]

## Key Constraints
- [Constraint 1]
- [Constraint 2]

## Proposed Solutions
1. **Option A**: [Description]
   - Pros: ...
   - Cons: ...
   - Effort: Low/Medium/High

2. **Option B**: [Description]
   - Pros: ...
   - Cons: ...
   - Effort: Low/Medium/High

## Recommendation
[Selected approach with reasoning]

## Next Steps
1. [Immediate action]
2. [Follow-up action]
```

## When to Use

- Starting a new project or feature
- Facing a complex technical decision
- When requirements are unclear
- Before writing code
- When stuck on a problem
