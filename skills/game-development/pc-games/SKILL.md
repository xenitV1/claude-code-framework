---
name: pc-games
description: PC and console game development with Unity 6, Godot 4.3+, and Unreal 5.4. Use when building desktop games, Steam integration, controller support, or engine-specific patterns.
---

# PC/Console Game Development

> Engine-specific patterns for desktop and console platforms

## Engine Selection Guide

| Engine | Best For | Language |
|--------|----------|----------|
| **Unity 6** | Cross-platform, mobile ports | C#, DOTS |
| **Godot 4.3+** | Indies, 2D games, open source | GDScript, C# |
| **Unreal 5.4** | AAA quality, realistic graphics | C++, Blueprint |

---

## Unity 6 (2024-2025)

### DOTS Architecture
```csharp
// Entity Component System
[GenerateAuthoringComponent]
public struct MoveSpeed : IComponentData {
    public float Value;
}

public partial class MovementSystem : SystemBase {
    protected override void OnUpdate() {
        float dt = SystemAPI.Time.DeltaTime;
        
        Entities.ForEach((ref Translation pos, in MoveSpeed speed) => {
            pos.Value.y += speed.Value * dt;
        }).ScheduleParallel();
    }
}
```

### Burst Compiler
```csharp
[BurstCompile]
public struct MyJob : IJobParallelFor {
    public NativeArray<float> data;
    
    public void Execute(int index) {
        data[index] *= 2f;
    }
}
```

### Key Unity 6 Features
- Native TypeScript support (experimental)
- WebGPU backend
- Enhanced UI Toolkit
- Improved Addressables

---

## Godot 4.3+

### GDScript 2.0 Patterns
```gdscript
class_name Player extends CharacterBody2D

@export var speed: float = 200.0
@export var jump_force: float = -400.0

@onready var sprite := $Sprite2D
@onready var anim := $AnimationPlayer

func _physics_process(delta: float) -> void:
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed
    velocity.y += gravity * delta
    
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_force
    
    move_and_slide()
```

### Signal-Based Communication
```gdscript
# Decouple with signals
signal health_changed(new_health: int)
signal died

func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health)
    if health <= 0:
        died.emit()
```

### Composition Over Inheritance
```gdscript
# StateMachine node as child
# HitboxComponent as child
# HealthComponent as child

func _ready() -> void:
    $HealthComponent.died.connect(_on_died)
```

---

## Unreal 5.4

### Nanite Virtualized Geometry
```
- Automatic LOD for high-poly meshes
- No manual LOD authoring needed
- Ideal for: large environments, detailed props
- Enable per-mesh in Static Mesh Editor
```

### Lumen Global Illumination
```
- Real-time GI without baking
- Dynamic lighting and reflections
- Cost: ~3-5ms on modern GPUs
- Settings: Project Settings → Rendering → Global Illumination
```

### World Partition
```
- Automatic level streaming
- Large open worlds
- Grid-based cell loading
- Enable: World Settings → World Partition
```

### Blueprint Best Practices
```
1. Keep graphs organized with comments
2. Use functions for repeated logic
3. Collapse to macros for reusability
4. C++ for performance-critical code
5. Blueprint-C++ hybrid for best results
```

---

## Steam Integration

### Steamworks Features
```
- Achievements
- Cloud saves
- Leaderboards
- Workshop (mods)
- Matchmaking
- Rich Presence
```

### Implementation
```csharp
// Unity - Steamworks.NET
SteamClient.Init(YOUR_APP_ID);
SteamUserStats.SetAchievement("FIRST_KILL");
SteamUserStats.StoreStats();
```

---

## Controller Support

### Input Mapping
```
Actions (abstract):
  jump, attack, interact, pause
  
Bindings (per-device):
  Keyboard: Space, X, E, Escape
  Xbox: A, X, Y, Start
  PlayStation: Cross, Square, Triangle, Options
```

### Haptic Feedback
```
- Light rumble: UI feedback
- Heavy rumble: Impacts
- Adaptive triggers (PS5): Tension for bowstrings, weapons
```

---

## Performance Optimization

### Profiling Tools
| Engine | Tool |
|--------|------|
| Unity | Profiler Window, Memory Profiler |
| Godot | Debugger → Profiler |
| Unreal | Unreal Insights, Stat commands |

### Common Bottlenecks
```
CPU:
- Too many Update() calls → Use events
- GC spikes → Object pooling
- Physics → Simplify colliders

GPU:
- Draw calls → Batching, atlases
- Overdraw → Culling
- Shader complexity → LOD shaders
```

### 60fps Target
```
Frame budget: 16.67ms
Reserve 2-3ms for system overhead
Profile early and often
```
