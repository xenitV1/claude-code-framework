---
name: web-games
description: Web browser game development with Phaser 4, Three.js, Babylon.js 7, and WebGPU. Use when building HTML5 games, canvas optimization, or browser-based gaming experiences.
---

# Web Browser Game Development

> Modern web game frameworks with WebGPU support (73% browser coverage in 2025)

## Framework Selection

| Framework | Type | Best For |
|-----------|------|----------|
| **Phaser 4** | 2D | Arcade, platformers, puzzle |
| **Three.js** | 3D | 3D experiences, visualizations |
| **Babylon.js 7** | 3D | Full game engine, XR support |
| **PixiJS 8** | 2D | UI-heavy, rendering performance |
| **PlayCanvas** | 3D | Visual editor, collaboration |

---

## Phaser 4 (2025)

### New Beam Renderer
```typescript
// Phaser 4 - Enhanced WebGL rendering
const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.WEBGL,
    width: 1280,
    height: 720,
    scene: MainScene,
    physics: {
        default: 'arcade',
        arcade: { gravity: { y: 300 } }
    }
};

const game = new Phaser.Game(config);
```

### Scene Structure
```typescript
class MainScene extends Phaser.Scene {
    private player!: Phaser.Physics.Arcade.Sprite;
    
    preload(): void {
        this.load.spritesheet('player', 'player.png', {
            frameWidth: 32,
            frameHeight: 32
        });
    }
    
    create(): void {
        this.player = this.physics.add.sprite(100, 100, 'player');
        this.player.setCollideWorldBounds(true);
        
        this.cursors = this.input.keyboard.createCursorKeys();
    }
    
    update(): void {
        if (this.cursors.left.isDown) {
            this.player.setVelocityX(-160);
        } else if (this.cursors.right.isDown) {
            this.player.setVelocityX(160);
        } else {
            this.player.setVelocityX(0);
        }
    }
}
```

---

## Three.js + WebGPU

### WebGPU Renderer
```typescript
import * as THREE from 'three';
import WebGPURenderer from 'three/addons/renderers/webgpu/WebGPURenderer.js';

const renderer = new WebGPURenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();
```

### Performance Tips
```typescript
// Geometry merging
const mergedGeometry = BufferGeometryUtils.mergeGeometries(geometries);

// Instancing for repeated objects
const mesh = new THREE.InstancedMesh(geometry, material, count);

// Frustum culling (enabled by default)
mesh.frustumCulled = true;
```

---

## Babylon.js 7

### WebGPU with WGSL Shaders
```typescript
const engine = new BABYLON.WebGPUEngine(canvas);
await engine.initAsync();

const scene = new BABYLON.Scene(engine);
const camera = new BABYLON.ArcRotateCamera(
    "camera", 0, Math.PI/3, 10, BABYLON.Vector3.Zero(), scene
);

// Native WebGPU shaders
const material = new BABYLON.ShaderMaterial("shader", scene, {
    vertexSource: vertexShaderWGSL,
    fragmentSource: fragmentShaderWGSL
}, { shaderLanguage: BABYLON.ShaderLanguage.WGSL });
```

### Physics with Havok
```typescript
const havokInstance = await HavokPhysics();
const hk = new BABYLON.HavokPlugin(true, havokInstance);
scene.enablePhysics(new BABYLON.Vector3(0, -9.81, 0), hk);

const sphere = BABYLON.MeshBuilder.CreateSphere("sphere", {}, scene);
const sphereBody = new BABYLON.PhysicsBody(sphere, 
    BABYLON.PhysicsMotionType.DYNAMIC, false, scene);
```

---

## WebGPU Essentials

### Feature Detection
```typescript
if (navigator.gpu) {
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    // WebGPU available
} else {
    // Fallback to WebGL
}
```

### Browser Support (2025)
| Browser | WebGPU | Notes |
|---------|--------|-------|
| Chrome | ✅ | Since v113 |
| Edge | ✅ | Since v113 |
| Firefox | ✅ | Since v131 |
| Safari | ✅ | Since 18.0 (2025) |
| **Total** | **73%** | Global users |

---

## Asset Loading

### Progressive Loading
```typescript
// Lazy load non-critical assets
const loader = new BABYLON.AssetsManager(scene);

const textureTask = loader.addTextureTask("tex", "large-texture.jpg");
textureTask.onSuccess = (task) => {
    material.diffuseTexture = task.texture;
};

loader.load();
```

### Compression
```
Textures: KTX2 with Basis Universal
Audio: MP3 (fallback), WebM/Opus (preferred)
Models: glTF with Draco/Meshopt compression
```

---

## PWA Support

### Offline Gaming
```javascript
// service-worker.js
const CACHE_NAME = 'game-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/game.js',
    '/assets/sprites.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});
```

### Web App Manifest
```json
{
    "name": "My Game",
    "short_name": "Game",
    "start_url": "/",
    "display": "fullscreen",
    "orientation": "landscape",
    "icons": [{ "src": "icon-512.png", "sizes": "512x512" }]
}
```

---

## Audio Context

### User Interaction Required
```typescript
document.addEventListener('click', () => {
    const audioContext = new AudioContext();
    audioContext.resume();
}, { once: true });
```

### Howler.js Integration
```typescript
const sound = new Howl({
    src: ['sound.webm', 'sound.mp3'],
    volume: 0.5,
    loop: false
});
sound.play();
```
</Parameter>
<parameter name="Complexity">7
