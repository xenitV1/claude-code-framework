---
name: 3d-games
description: 3D game development patterns and techniques. Use when building 3D games with meshes, shaders, lighting, physics, and camera systems across Unity, Godot, Unreal, or Three.js.
---

# 3D Game Development

> Patterns and techniques for 3D rendering, physics, and gameplay

## 3D Pipelines

| Engine | Rendering | Shading Language |
|--------|-----------|------------------|
| **Unity** | URP, HDRP | HLSL, ShaderGraph |
| **Unreal** | Forward+, Deferred | HLSL, Materials |
| **Godot** | Forward+, Mobile | GLSL, VisualShader |
| **Three.js** | WebGL, WebGPU | GLSL, WGSL |

---

## 3D Math Essentials

### Vectors
```typescript
// Common operations
dot(a, b)     // Alignment (-1 to 1)
cross(a, b)   // Perpendicular vector
normalize(v)  // Unit vector (length 1)
lerp(a, b, t) // Linear interpolation
slerp(a, b, t) // Spherical interpolation (rotations)
```

### Matrices
```
Model Matrix: Object → World space
View Matrix: World → Camera space
Projection Matrix: Camera → Screen space

MVP = Projection * View * Model
```

### Quaternions
```typescript
// Rotation without gimbal lock
const rotation = Quaternion.fromEuler(pitch, yaw, roll);
const combined = Quaternion.multiply(a, b);
const interpolated = Quaternion.slerp(from, to, t);

// Look at target
const lookRotation = Quaternion.lookRotation(targetDir, Vector3.UP);
```

---

## Rendering Techniques

### Lighting Types
| Type | Use Case | Cost |
|------|----------|------|
| **Directional** | Sun, moon | Low |
| **Point** | Lamps, fires | Medium |
| **Spot** | Flashlights | Medium |
| **Area** | Soft shadows | High |

### Shadows
```
Shadow mapping:
1. Render depth from light's view
2. Compare fragment depth to shadow map
3. If deeper, in shadow

Techniques:
- Cascaded Shadow Maps (CSM) for directional
- Point light cubemap shadows
- Soft shadows (PCF, PCSS)
```

### PBR (Physically Based Rendering)
```
Material properties:
- Albedo (base color)
- Metallic (0 = dielectric, 1 = metal)
- Roughness (0 = smooth, 1 = rough)
- Normal (surface detail)
- Ambient Occlusion (self-shadowing)
- Emission (glowing)
```

---

## Shaders

### Basic Vertex/Fragment
```glsl
// Vertex shader
#version 330 core
layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

out vec3 vNormal;
out vec2 vTexCoord;

void main() {
    gl_Position = uProjection * uView * uModel * vec4(aPosition, 1.0);
    vNormal = mat3(transpose(inverse(uModel))) * aNormal;
    vTexCoord = aTexCoord;
}

// Fragment shader
#version 330 core
in vec3 vNormal;
in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec3 uLightDir;

out vec4 fragColor;

void main() {
    vec3 normal = normalize(vNormal);
    float diffuse = max(dot(normal, -uLightDir), 0.0);
    vec3 color = texture(uTexture, vTexCoord).rgb;
    fragColor = vec4(color * (0.3 + 0.7 * diffuse), 1.0);
}
```

### Common Effects
```
Dissolve: Noise threshold for disappearing
Outline: Inverted hull or post-process edge
Toon/Cel: Stepped lighting
Hologram: Scanlines + fresnel + emission
Water: Sine displacement + reflection + refraction
```

---

## 3D Physics

### Rigid Body Types
| Type | Use Case |
|------|----------|
| **Dynamic** | Player, enemies, physics objects |
| **Kinematic** | Platforms, doors (scripted movement) |
| **Static** | Environment, walls |

### Collision Shapes
```
Sphere: Fastest, rolling objects
Box: Buildings, crates
Capsule: Character controllers
Mesh: Static environment only
Convex Hull: Dynamic with complex shape
Compound: Multiple primitives
```

### Character Controller
```csharp
// Unity CharacterController
[RequireComponent(typeof(CharacterController))]
public class PlayerMovement : MonoBehaviour
{
    public float speed = 5f;
    public float gravity = -9.81f;
    public float jumpHeight = 1.5f;
    
    private CharacterController controller;
    private Vector3 velocity;
    
    void Update()
    {
        bool isGrounded = controller.isGrounded;
        if (isGrounded && velocity.y < 0)
            velocity.y = -2f;
        
        Vector3 move = transform.right * Input.GetAxis("Horizontal") +
                       transform.forward * Input.GetAxis("Vertical");
        controller.Move(move * speed * Time.deltaTime);
        
        if (Input.GetButtonDown("Jump") && isGrounded)
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
        
        velocity.y += gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);
    }
}
```

---

## Camera Systems

### Third-Person Camera
```typescript
class ThirdPersonCamera {
    distance = 5;
    height = 2;
    smoothing = 10;
    
    update(dt: number, target: Vector3) {
        // Calculate desired position
        const yaw = this.yawInput;
        const pitch = this.pitchInput;
        
        const offset = new Vector3(
            Math.sin(yaw) * Math.cos(pitch) * this.distance,
            Math.sin(pitch) * this.distance + this.height,
            Math.cos(yaw) * Math.cos(pitch) * this.distance
        );
        
        const desiredPos = target.add(offset);
        
        // Collision avoidance
        const ray = new Ray(target, offset.normalized());
        if (Physics.raycast(ray, this.distance, out hit)) {
            desiredPos = hit.point - offset.normalized() * 0.2;
        }
        
        // Smooth follow
        this.position = Vector3.lerp(this.position, desiredPos, dt * this.smoothing);
        this.lookAt(target);
    }
}
```

### First-Person Camera
```typescript
class FirstPersonCamera {
    sensitivity = 0.2;
    pitch = 0;
    yaw = 0;
    
    update(mouseX: number, mouseY: number) {
        this.yaw += mouseX * this.sensitivity;
        this.pitch -= mouseY * this.sensitivity;
        this.pitch = clamp(this.pitch, -89, 89);
        
        const front = new Vector3(
            Math.cos(toRad(this.yaw)) * Math.cos(toRad(this.pitch)),
            Math.sin(toRad(this.pitch)),
            Math.sin(toRad(this.yaw)) * Math.cos(toRad(this.pitch))
        );
        
        this.forward = front.normalized();
    }
}
```

---

## Level of Detail (LOD)

### Implementation
```
LOD 0: Full detail (close)
LOD 1: 50% triangles (medium)
LOD 2: 25% triangles (far)
LOD 3: Billboard/imposter (very far)

Transition distances based on screen size
Use dithering or cross-fade for smooth transitions
```

---

## Optimization

### Draw Call Reduction
```
- Batching (combine meshes)
- Instancing (same mesh, different transforms)
- Atlasing (single material)
- GPU culling
```

### Culling
```
Frustum culling: Only render visible objects
Occlusion culling: Skip objects behind walls
Distance culling: Skip far objects
LOD: Reduce distant object complexity
```

### Performance Budget
```
Target: 16.67ms (60fps)

Typical breakdown:
- CPU gameplay: 4ms
- CPU rendering: 2ms
- GPU draw: 8ms
- Buffer: 2.67ms

Profile with:
- Unity Profiler
- RenderDoc
- Unreal Insights
- Chrome DevTools (WebGL)
```

---

## Best Practices

```
1. Use static batching for environment
2. Bake lighting where possible
3. Compress textures (BCn, ASTC)
4. Keep materials simple for mobile
5. Use imposters for distant vegetation
6. Pool dynamic objects
7. Limit real-time shadows
8. Profile early and often
```
