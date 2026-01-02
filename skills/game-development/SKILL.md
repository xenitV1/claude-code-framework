---
name: game-development
description: Core game development patterns and fundamentals applicable to all platforms. Use when working on game architecture, game loops, design patterns, or general game programming concepts.
---

# Game Development Fundamentals

> Core patterns and principles for game development across all platforms

## Game Loop Architecture

### Fixed Timestep Pattern
```
accumulator = 0
while game_running:
    accumulator += delta_time
    
    while accumulator >= FIXED_TIMESTEP:
        update_physics(FIXED_TIMESTEP)
        accumulator -= FIXED_TIMESTEP
    
    interpolation = accumulator / FIXED_TIMESTEP
    render(interpolation)
```

**FIXED_TIMESTEP**: Usually 1/60 (16.67ms) or 1/50 (20ms)

---

## Design Patterns

### 1. Entity Component System (ECS)
```
Entity: Just an ID
Component: Data only (Position, Velocity, Sprite)
System: Logic that processes components

Example:
- MovementSystem processes entities with Position + Velocity
- RenderSystem processes entities with Position + Sprite
```

**Benefits**: Cache-friendly, scalable, decoupled

### 2. State Machine
```
States: Idle, Walking, Jumping, Attacking
Transitions: Input/conditions trigger state changes

Each state handles:
- Enter(): Setup when entering state
- Update(): Per-frame logic
- Exit(): Cleanup when leaving state
```

### 3. Object Pooling
```
Pre-allocate objects (bullets, particles, enemies)
Instead of: new/destroy
Use: pool.get() / pool.release()
```

**Critical for**: Mobile, WebGL, frequent spawning

### 4. Observer Pattern
```
EventBus.emit("player_died", {score: 1000})
EventBus.on("player_died", updateUI)
EventBus.on("player_died", playSound)
```

### 5. Command Pattern
```
Commands are objects that encapsulate actions
Use for: Input replay, undo/redo, network sync

InputCommand { execute(), undo() }
```

---

## Core Systems

### Input Handling
```
Abstract input into actions:
  "jump": [Keyboard.SPACE, Gamepad.A, Touch.TAP]
  "move": [Keyboard.WASD, Gamepad.LEFT_STICK, Touch.JOYSTICK]

Process input at start of frame, before update
```

### Collision Detection
| Type | Use Case |
|------|----------|
| AABB | Rectangles, fast |
| Circle | Round objects, cheap |
| SAT | Complex polygons |
| Spatial Hash | Many objects |
| Quadtree | Large worlds |

### Save System
```
Serialize game state to JSON/binary
Store: player progress, settings, unlocks
Platforms: LocalStorage (web), PlayerPrefs (Unity), FileAccess (Godot)
```

---

## Performance Guidelines

### Frame Budget (60 FPS = 16.67ms)
```
Input:     1ms
Physics:   3ms
AI:        2ms
Update:    4ms
Render:    5ms
Buffer:    1.67ms
```

### Memory Management
- Pool frequently created/destroyed objects
- Use sprite atlases/texture packing
- Stream large assets
- Unload unused resources

### Rendering Optimization
- Batch draw calls
- Use frustum culling
- Implement LOD for 3D
- Minimize state changes

---

## AI Fundamentals

### Behavior Trees
```
Selector: Try children until one succeeds
Sequence: Run children until one fails
Decorator: Modify child behavior

Common nodes:
- Wait, MoveTo, Attack, Patrol, Chase
```

### Finite State Machine (FSM)
```
Simple AI: 3-5 states
Complex AI: Hierarchical FSM (HFSM)

States: Patrol → Alert → Chase → Attack → Flee
```

### Goal-Oriented Action Planning (GOAP)
```
AI has goals and actions with preconditions/effects
Planner finds action sequence to achieve goal

Example goal: "EnemyDead"
Actions: GetWeapon → MoveTo → Attack
```

---

## Audio System

```
Categories: Music, SFX, UI, Voice
Features:
- 3D positional audio
- Audio pooling
- Fade in/out
- Ducking (lower music during dialogue)
```

---

## Sub-Skills Reference

For platform-specific patterns:
- [PC Games](./pc-games/SKILL.md) - Unity, Godot, Unreal
- [Web Games](./web-games/SKILL.md) - Phaser, Three.js, Babylon.js
- [Mobile Games](./mobile-games/SKILL.md) - Touch, battery, stores
- [Game Design](./game-design/SKILL.md) - GDD, balancing, psychology
- [Multiplayer](./multiplayer/SKILL.md) - Networking patterns
- [VR/AR](./vr-ar/SKILL.md) - Immersive experiences
- [2D Games](./2d-games/SKILL.md) - Sprites, tilemaps, platformers
- [3D Games](./3d-games/SKILL.md) - Meshes, shaders, 3D physics

