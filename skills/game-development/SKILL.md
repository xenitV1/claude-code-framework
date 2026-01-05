---
name: game-development
description: Core game development principles applicable to all platforms. Game loop, design patterns, optimization, and AI fundamentals.
---

# Game Development Fundamentals

> Core principles for game development across all platforms.
> **Learn to THINK, not memorize engine APIs.**

---

## 1. Game Loop Principles

### The Universal Pattern

```
Every game has:
1. INPUT → Read player actions
2. UPDATE → Process game logic (fixed timestep)
3. RENDER → Draw the frame (interpolated)
```

### Fixed Timestep Principle

- Physics/logic updates at fixed rate (e.g., 50Hz)
- Rendering runs as fast as possible
- Interpolate between states for smooth visuals

---

## 2. Design Pattern Selection

### When to Use Each Pattern

| Pattern | Use When | Example |
|---------|----------|---------|
| **State Machine** | Discrete states with transitions | Player: Idle→Walk→Jump→Attack |
| **Object Pooling** | Frequent create/destroy | Bullets, particles, enemies |
| **Observer/Events** | Decoupled communication | Health→UI, Death→Audio |
| **ECS** | Many similar entities | Thousands of units |
| **Command** | Replay, undo, networking | Input recording, multiplayer |
| **Behavior Tree** | Complex AI decisions | Enemy AI |

### Selection Principles

- Start simple (State Machine)
- Add ECS only if performance demands
- Use Events for cross-system communication
- Pool anything spawned frequently

---

## 3. Core Systems Design

### Input Abstraction

```
Abstract input into ACTIONS, not keys:
- "jump" → Space, Gamepad A, Touch tap
- "move" → WASD, Left stick, Virtual joystick

Benefits: Multi-platform, rebindable
```

### Collision Strategy

| Type | Best For |
|------|----------|
| **AABB** | Rectangles, fast |
| **Circle** | Round objects, cheap |
| **Spatial Hash** | Many objects, same size |
| **Quadtree** | Large worlds, varying sizes |

### Save System

| Platform | Storage |
|----------|---------|
| Web | LocalStorage, IndexedDB |
| Mobile | PlayerPrefs, FileAccess |
| PC | JSON/Binary files |

---

## 4. Performance Principles

### Frame Budget (60 FPS = 16.67ms)

| System | Budget |
|--------|--------|
| Input | 1ms |
| Physics | 3ms |
| AI | 2ms |
| Game Logic | 4ms |
| Rendering | 5ms |
| Buffer | 1.67ms |

### Optimization Priority

1. **Algorithm** - O(n²) to O(n log n)
2. **Batching** - Reduce draw calls
3. **Pooling** - Avoid GC spikes
4. **LOD** - Detail at distance
5. **Culling** - Don't render invisible

### Memory Management

- Pool frequently spawned objects
- Use sprite atlases
- Stream large assets
- Unload unused resources

---

## 5. AI Fundamentals

### Selection by Complexity

| AI Type | Complexity | Use Case |
|---------|------------|----------|
| **FSM** | Simple | 3-5 states, predictable |
| **Behavior Tree** | Medium | Modular, designer-friendly |
| **GOAP** | High | Emergent, planning |
| **Utility AI** | High | Scoring-based decisions |

### Common AI Behaviors

- Patrol → Move between waypoints
- Chase → Follow player
- Attack → Engage when in range
- Flee → Escape when low health

---

## 6. Audio Principles

### Audio Categories

| Category | Behavior |
|----------|----------|
| **Music** | Loop, crossfade |
| **SFX** | One-shot, 3D positioned |
| **UI** | Immediate, no 3D |
| **Voice** | Priority, ducking |

### Best Practices

- Pool audio sources
- 3D audio for immersion
- Duck music during dialogue
- Preload frequently used sounds

---

## 7. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Update everything every frame | Use events, dirty flags |
| Create objects in hot loops | Object pooling |
| SELECT * in game logic | Cache references |
| Optimize without profiling | Profile first |
| Mix input with logic | Abstract input layer |

---

## 8. Sub-Skills Reference

Platform-specific guidance:
- PC Games → Engine selection, Steam
- Web Games → Phaser, Three.js, WebGPU
- Mobile Games → Touch, battery, stores
- Game Design → GDD, balancing
- Multiplayer → Networking patterns
- VR/AR → Immersion, comfort
- 2D Games → Sprites, tilemaps
- 3D Games → Meshes, shaders

---

> **Remember:** Great games come from iteration, not perfection. Prototype fast, then polish.
