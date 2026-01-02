---
name: game-design
description: Game design fundamentals, GDD templates, player psychology, game balancing, and progression systems. Use when designing game mechanics, writing design documents, or balancing gameplay.
---

# Game Design Fundamentals

> Design theory, documentation, and player psychology for compelling games

## Game Design Document (GDD)

### One-Page GDD Template
```markdown
# [Game Title]

**Genre**: [e.g., Roguelike Deckbuilder]
**Platform**: [e.g., PC, Mobile, Web]
**Target Audience**: [e.g., Casual puzzle fans, 18-35]

## Core Loop
[Action] → [Challenge] → [Reward] → [Progress]

## Unique Selling Point
What makes this different from similar games?

## Key Mechanics
1. [Primary mechanic]
2. [Secondary mechanic]
3. [Meta progression]

## Mood & Tone
[Art style, music, overall feel]

## Success Metrics
- Retention Day 1: 40%
- Retention Day 7: 20%
- Session length: 10-15 min
```

### Full GDD Structure
```
1. Overview
   - Concept, genre, target audience
   - Platform, business model
   
2. Gameplay
   - Core mechanics
   - Controls
   - Game modes
   
3. Progression
   - Level structure
   - Unlocks
   - Difficulty curve
   
4. Story & World
   - Narrative
   - Characters
   - Lore
   
5. Art & Audio
   - Visual style
   - Music direction
   - SFX approach
   
6. Technical
   - Engine
   - Requirements
   - Multiplayer architecture
   
7. Monetization
   - Business model
   - IAP strategy
   
8. Timeline
   - Milestones
   - Release schedule
```

---

## Core Loop Design

### The Engagement Cycle
```
    ┌──────────────────────────────────────┐
    │                                      │
    ▼                                      │
[Action] ──→ [Challenge] ──→ [Reward] ──→ [Progress]
    │
    └── Player performs primary action
```

### Examples
| Game Type | Action | Challenge | Reward |
|-----------|--------|-----------|--------|
| Match-3 | Swap gems | Clear board | Points, stars |
| Roguelike | Move, attack | Enemies, traps | Items, gold |
| Builder | Place objects | Resources, space | Unlocks, beauty |

---

## Player Psychology

### Motivation Types (Self-Determination Theory)
```
Autonomy:   Let players make meaningful choices
Competence: Skill growth, mastery feeling
Relatedness: Social features, shared experiences
```

### Flow State
```
        Difficulty
            │
   Anxiety  │   ╱ FLOW ZONE
            │ ╱
            │╱
    ────────┼──────── Skill
            │╲
            │  ╲ Boredom
            │

Goal: Keep players in the flow zone
- Too easy → Boredom
- Too hard → Anxiety/Frustration
```

### Reward Psychology
```
Variable rewards > Fixed rewards (for engagement)
Immediate feedback > Delayed feedback
Earned rewards > Given rewards

Diminishing returns:
- 1st reward: 100% excitement
- 2nd same reward: 80%
- 3rd same reward: 60%
Solution: Rotate reward types
```

---

## Game Balancing

### Dynamic Difficulty Adjustment (DDA)
```typescript
// Track player performance
const metrics = {
    deathRate: deaths / attempts,
    completionTime: avgTime,
    hitRate: hits / attempts
};

// Adjust difficulty
if (metrics.deathRate > 0.5) {
    enemyHealth *= 0.9;
    playerDamage *= 1.1;
} else if (metrics.deathRate < 0.1) {
    enemyHealth *= 1.1;
}
```

### Balancing Formulas
```
Power curve:
  power = base * (1 + level * 0.1)

XP requirements:
  xpNeeded = baseXP * (level ^ 1.5)

Damage formula:
  damage = attack * (100 / (100 + defense))

Economy:
  Sink = Source (coins earned = coins spent over time)
```

### Testing Approach
```
1. Start slightly overpowered → More fun data
2. Run simulations (AI plays 10,000 games)
3. Playtest with real users
4. Iterate based on metrics
5. Balance for average, accommodate extremes
```

---

## Progression Systems

### Horizontal vs Vertical
```
Vertical: Power increases (levels, stats)
Horizontal: Options increase (unlocks, sidegrades)

Healthy games: Mix of both
Avoid: Endless vertical (power creep)
```

### Progression Types
| Type | Example | Feeling |
|------|---------|---------|
| Character | XP, levels | Growth |
| Collection | Cards, items | Discovery |
| Story | Chapters, endings | Narrative |
| Cosmetic | Skins, titles | Expression |
| Mastery | Achievements, ranks | Skill proof |

### Unlock Pacing
```
Early game: Fast unlocks (hook)
  - New thing every 2-5 minutes
  
Mid game: Steady unlocks
  - New thing every session
  
Late game: Mastery unlocks
  - Exclusive rewards for dedication
```

---

## Monetization Ethics

### Ethical F2P Principles
```
✅ Cosmetics only (no pay-to-win)
✅ Fair grind (achievable without paying)
✅ Clear pricing (no dark patterns)
✅ Battle pass (value over time)
✅ One-time "remove ads"

❌ Loot boxes with real money
❌ Energy systems that block play
❌ Aggressive FOMO tactics
❌ Hidden costs / currency obfuscation
❌ Targeting vulnerable players
```

---

## Accessibility

### WCAG for Games
```
Visual:
- Colorblind modes (8% of males)
- Scalable UI
- High contrast options
- Screen reader support (menus)

Motor:
- Remappable controls
- One-handed modes
- Auto-aim assist
- Adjustable timing

Cognitive:
- Tutorials
- Difficulty options
- Save anywhere
- Clear objectives
```

### Accessibility Checklist
```
[ ] Colorblind simulation tested
[ ] Remappable controls
[ ] Subtitle options
[ ] Adjustable text size
[ ] Screen shake toggle
[ ] Difficulty presets
[ ] Skip tutorial option
```

---

## Localization

### Planning for L10n
```
- String externalization from day 1
- UI flexible for text expansion (+30% for German)
- Cultural sensitivity review
- Right-to-left (Arabic, Hebrew) support if needed
- Date/time/number formatting
```

### Priority Markets
```
1. English (global)
2. Simplified Chinese (huge market)
3. Japanese (high ARPU)
4. Korean (competitive games)
5. German/French/Spanish (Europe)
6. Portuguese (Brazil)
```
