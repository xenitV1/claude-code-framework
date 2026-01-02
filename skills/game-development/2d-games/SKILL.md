---
name: 2d-games
description: 2D game development patterns and techniques. Use when building platformers, top-down games, puzzle games, or any 2D game with sprites, tilemaps, and 2D physics.
---

# 2D Game Development

> Patterns and techniques for sprite-based 2D games

## 2D Game Types

| Genre | Camera | Physics |
|-------|--------|---------|
| **Platformer** | Side-scroll | Gravity, jump |
| **Top-down** | Overhead | 8-dir movement |
| **Puzzle** | Static/scroll | Match, logic |
| **Shmup** | Vertical/horizontal | Bullet patterns |
| **Fighting** | Side view | Hitboxes |

---

## Sprite Systems

### Sprite Sheets & Atlases
```
Benefits:
- Single draw call for multiple sprites
- Reduced texture swaps
- Better GPU memory usage

Tools:
- TexturePacker
- Unity Sprite Atlas
- Godot AtlasTexture
- Phaser Texture Packer integration
```

### Animation
```typescript
// Frame-based animation
interface Animation {
    name: string;
    frames: number[];    // indices in spritesheet
    frameRate: number;   // fps
    loop: boolean;
}

const animations = {
    idle: { frames: [0, 1, 2, 3], frameRate: 8, loop: true },
    run: { frames: [4, 5, 6, 7, 8, 9], frameRate: 12, loop: true },
    jump: { frames: [10, 11], frameRate: 10, loop: false },
    attack: { frames: [12, 13, 14, 15], frameRate: 15, loop: false }
};
```

---

## Tilemaps

### Tile-Based Levels
```
Grid types:
- Square (most common)
- Isometric (45° view)
- Hexagonal (strategy games)

Layers:
1. Background (non-interactive)
2. Collision (defines walkable)
3. Foreground (overlays player)
4. Objects (spawners, triggers)
```

### Autotiling
```
Bitmask autotiling:
- 4-bit (16 tiles): Basic corners
- 8-bit (47 tiles): Full blob tileset
- Wang tiles: Seamless variations

Tools:
- Tiled Map Editor (free, cross-platform)
- LDtk (modern, game-focused)
```

### Collision from Tiles
```gdscript
# Godot TileMap collision
func _ready():
    var tilemap = $TileMap
    for cell in tilemap.get_used_cells(0):  # layer 0
        var tile_data = tilemap.get_cell_tile_data(0, cell)
        if tile_data and tile_data.get_custom_data("solid"):
            # This tile is solid
            pass
```

---

## 2D Physics

### Platformer Physics
```typescript
// Responsive platformer movement
class PlatformerController {
    // Tuning constants
    gravity = 980;
    maxFallSpeed = 400;
    jumpForce = -350;
    coyoteTime = 0.1;  // seconds after leaving platform
    jumpBuffer = 0.1;  // seconds before landing
    
    // Variable jump height
    update(dt: number) {
        // Apply gravity
        this.velocity.y += this.gravity * dt;
        this.velocity.y = Math.min(this.velocity.y, this.maxFallSpeed);
        
        // Jump cut (release early = lower jump)
        if (!this.jumpHeld && this.velocity.y < 0) {
            this.velocity.y *= 0.5;
        }
        
        // Coyote time
        if (this.wasGrounded && !this.isGrounded) {
            this.coyoteTimer = this.coyoteTime;
        }
        
        // Jump buffer
        if (this.jumpPressed) {
            this.jumpBufferTimer = this.jumpBuffer;
        }
        
        // Execute jump
        if (this.jumpBufferTimer > 0 && (this.isGrounded || this.coyoteTimer > 0)) {
            this.velocity.y = this.jumpForce;
            this.jumpBufferTimer = 0;
            this.coyoteTimer = 0;
        }
    }
}
```

### Top-Down Movement
```typescript
// 8-direction movement with smoothing
class TopDownController {
    maxSpeed = 200;
    acceleration = 800;
    friction = 600;
    
    update(dt: number, inputDir: Vector2) {
        if (inputDir.length() > 0) {
            inputDir = inputDir.normalized();
            this.velocity.x += inputDir.x * this.acceleration * dt;
            this.velocity.y += inputDir.y * this.acceleration * dt;
        } else {
            // Apply friction
            const frictionAmount = this.friction * dt;
            if (this.velocity.length() < frictionAmount) {
                this.velocity = Vector2.ZERO;
            } else {
                this.velocity -= this.velocity.normalized() * frictionAmount;
            }
        }
        
        // Clamp to max speed
        if (this.velocity.length() > this.maxSpeed) {
            this.velocity = this.velocity.normalized() * this.maxSpeed;
        }
    }
}
```

---

## Collision Detection

### AABB (Axis-Aligned Bounding Box)
```typescript
function aabbCollision(a: Rect, b: Rect): boolean {
    return a.x < b.x + b.width &&
           a.x + a.width > b.x &&
           a.y < b.y + b.height &&
           a.y + a.height > b.y;
}
```

### Circle Collision
```typescript
function circleCollision(a: Circle, b: Circle): boolean {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < a.radius + b.radius;
}
```

### Hitboxes & Hurtboxes
```
Hitbox: Deals damage (attack)
Hurtbox: Receives damage (body)

Separate from collision box for gameplay tuning
Active frames: Hitbox only active during attack animation frames
```

---

## Camera Systems

### Follow Camera
```typescript
// Smooth follow with look-ahead
class Camera2D {
    smoothing = 5;
    lookAhead = 50;
    
    update(dt: number, target: Vector2, velocity: Vector2) {
        // Look ahead in movement direction
        const ahead = velocity.normalized() * this.lookAhead;
        const targetPos = target + ahead;
        
        // Smooth interpolation
        this.position = Vector2.lerp(
            this.position, 
            targetPos, 
            this.smoothing * dt
        );
    }
}
```

### Screen Shake
```typescript
function screenShake(intensity: number, duration: number) {
    const startTime = performance.now();
    
    function shake() {
        const elapsed = performance.now() - startTime;
        if (elapsed < duration) {
            const remaining = 1 - (elapsed / duration);
            const offset = {
                x: (Math.random() - 0.5) * intensity * remaining,
                y: (Math.random() - 0.5) * intensity * remaining
            };
            camera.offset = offset;
            requestAnimationFrame(shake);
        } else {
            camera.offset = { x: 0, y: 0 };
        }
    }
    shake();
}
```

---

## Parallax Backgrounds

```typescript
// Multi-layer parallax
const layers = [
    { sprite: 'sky', speedFactor: 0.1 },
    { sprite: 'mountains', speedFactor: 0.3 },
    { sprite: 'trees', speedFactor: 0.6 },
    { sprite: 'ground', speedFactor: 1.0 }
];

function updateParallax(cameraX: number) {
    for (const layer of layers) {
        layer.x = -cameraX * layer.speedFactor;
        // Wrap for infinite scrolling
        layer.x = layer.x % layer.width;
    }
}
```

---

## Particle Systems

### Common 2D Effects
```
Dust: Jump/land, running
Sparks: Hit effects, metal
Smoke: Explosions, fire
Trail: Projectiles, movement
Sparkle: Pickups, magic
```

### Implementation
```typescript
// Emitter configuration
const dustEmitter = {
    lifetime: { min: 0.3, max: 0.5 },
    speed: { min: 20, max: 50 },
    angle: { min: -30, max: 30 },
    scale: { start: 0.5, end: 0 },
    alpha: { start: 0.8, end: 0 },
    color: 0xDDCCAA,
    count: { min: 3, max: 5 }
};
```

---

## Best Practices

### Pixel Art Games
```
- Use nearest-neighbor filtering (no blur)
- Integer scaling (1x, 2x, 3x, not 1.5x)
- Consistent pixel density
- Limit color palette per sprite
```

### Performance
```
- Use sprite batching
- Object pool for particles, bullets
- Cull off-screen sprites
- Optimize tilemap rendering (chunks)
```
