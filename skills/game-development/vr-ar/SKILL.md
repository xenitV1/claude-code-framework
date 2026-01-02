---
name: vr-ar
description: Virtual Reality and Augmented Reality game development. Use when building VR/AR experiences, XR interactions, motion controls, or immersive gameplay with Unity XR, Unreal VR, or WebXR.
---

# VR/AR Game Development

> Immersive experience design for Virtual and Augmented Reality

## Platform Overview

| Platform | SDK | Headsets |
|----------|-----|----------|
| **Meta Quest** | Meta XR SDK | Quest 2, 3, Pro |
| **SteamVR** | OpenXR | Valve Index, Vive, etc |
| **Apple Vision Pro** | RealityKit | Vision Pro |
| **WebXR** | WebXR API | Browser-based |
| **ARKit** | ARKit | iPhone, iPad |
| **ARCore** | ARCore | Android devices |

---

## Performance Requirements

### VR Frame Targets
| Headset | Refresh Rate | Frame Budget |
|---------|-------------|--------------|
| Quest 2 | 72-120 Hz | 8.3-13.9ms |
| Quest 3 | 90-120 Hz | 8.3-11.1ms |
| Vision Pro | 90 Hz | 11.1ms |
| PC VR | 90-144 Hz | 6.9-11.1ms |

**Critical**: Missed frames → motion sickness

### Optimization Priorities
```
1. 90 FPS minimum (no exceptions for VR)
2. Fixed foveated rendering
3. Single-pass stereo rendering
4. LOD aggressive usage
5. Occlusion culling
6. GPU instancing
```

---

## Unity XR

### XR Interaction Toolkit
```csharp
using UnityEngine.XR.Interaction.Toolkit;

public class Grabbable : XRGrabInteractable
{
    protected override void OnSelectEntered(SelectEnterEventArgs args)
    {
        base.OnSelectEntered(args);
        // Picked up
        audioSource.PlayOneShot(grabSound);
    }
    
    protected override void OnSelectExited(SelectExitEventArgs args)
    {
        base.OnSelectExited(args);
        // Released
    }
}
```

### Hand Tracking
```csharp
using UnityEngine.XR.Hands;

void Update()
{
    if (XRHandSubsystem.TryGetHand(XRHandedness.Right, out XRHand hand))
    {
        if (hand.GetJoint(XRHandJointID.IndexTip).TryGetPose(out Pose pose))
        {
            indexTipPosition = pose.position;
        }
        
        // Pinch gesture
        if (hand.GetFingerPinchStrength(XRHandFingerID.Index) > 0.9f)
        {
            OnPinch();
        }
    }
}
```

---

## Unreal VR

### VR Template Setup
```cpp
// Motion controller input
void AVRPawn::SetupPlayerInputComponent(UInputComponent* Input)
{
    Input->BindAction("GrabLeft", IE_Pressed, this, &AVRPawn::GrabLeft);
    Input->BindAction("GrabRight", IE_Pressed, this, &AVRPawn::GrabRight);
    Input->BindAction("Teleport", IE_Pressed, this, &AVRPawn::StartTeleport);
    Input->BindAction("Teleport", IE_Released, this, &AVRPawn::ExecuteTeleport);
}

// Haptic feedback
void AVRPawn::TriggerHaptic(EControllerHand Hand, float Intensity)
{
    APlayerController* PC = Cast<APlayerController>(GetController());
    PC->PlayHapticEffect(HapticEffect, Hand, Intensity);
}
```

---

## WebXR

### Browser-Based VR/AR
```typescript
// Check WebXR support
if (navigator.xr) {
    const isVRSupported = await navigator.xr.isSessionSupported('immersive-vr');
    const isARSupported = await navigator.xr.isSessionSupported('immersive-ar');
}

// Start VR session
async function enterVR() {
    const session = await navigator.xr.requestSession('immersive-vr', {
        requiredFeatures: ['local-floor'],
        optionalFeatures: ['hand-tracking']
    });
    
    renderer.xr.setSession(session);
}
```

### Three.js XR
```typescript
import { VRButton } from 'three/addons/webxr/VRButton.js';
import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';

// Enable XR
renderer.xr.enabled = true;
document.body.appendChild(VRButton.createButton(renderer));

// Controller models
const controllerModelFactory = new XRControllerModelFactory();
const controller1 = renderer.xr.getController(0);
const controllerGrip1 = renderer.xr.getControllerGrip(0);
controllerGrip1.add(controllerModelFactory.createControllerModel(controllerGrip1));
scene.add(controllerGrip1);

// Controller events
controller1.addEventListener('selectstart', onSelectStart);
controller1.addEventListener('selectend', onSelectEnd);
```

---

## Locomotion

### Movement Types
| Type | Comfort | Use Case |
|------|---------|----------|
| **Teleportation** | High | Most users |
| **Smooth locomotion** | Medium | VR veterans |
| **Arm swinging** | Medium | Active games |
| **Snap turning** | High | Comfort option |
| **Vehicle/cockpit** | High | Racing, flight |

### Teleportation Implementation
```csharp
public class TeleportProvider : MonoBehaviour
{
    [SerializeField] private LineRenderer arc;
    [SerializeField] private Transform reticle;
    
    void Update()
    {
        if (isTeleportActive)
        {
            // Parabolic arc
            Vector3 velocity = controller.forward * teleportSpeed;
            DrawArc(controller.position, velocity);
            
            if (Physics.Raycast(arcEnd, Vector3.down, out RaycastHit hit))
            {
                if (IsValidTeleportTarget(hit))
                {
                    reticle.position = hit.point;
                    reticle.gameObject.SetActive(true);
                }
            }
        }
    }
}
```

---

## Interaction Design

### Grab Mechanics
```
Direct grab: Hand touches object
Ray grab: Point and grab distant objects
Force grab: Pull objects to hand

Best practice:
- Visual feedback on hover
- Haptic feedback on grab
- Natural release physics
```

### UI in VR
```
Do:
- World-space UI (not screen-space)
- Curved panels for readability
- Large touch targets (min 6cm)
- Laser pointer interaction
- Gaze + dwell as fallback

Don't:
- Small text
- Fast-moving UI
- UI too close (<0.5m)
- Forced head movement
```

---

## AR Development

### ARKit (iOS)
```swift
// Plane detection
let configuration = ARWorldTrackingConfiguration()
configuration.planeDetection = [.horizontal, .vertical]
arSession.run(configuration)

// Place object on plane
func placeObject(at anchor: ARAnchor) {
    let node = SCNNode(geometry: myModel)
    node.position = SCNVector3(anchor.transform.columns.3.x,
                               anchor.transform.columns.3.y,
                               anchor.transform.columns.3.z)
    sceneView.scene.rootNode.addChildNode(node)
}
```

### ARCore (Android)
```kotlin
// Plane detection
val config = Config(session)
config.planeFindingMode = Config.PlaneFindingMode.HORIZONTAL_AND_VERTICAL
session.configure(config)

// Hit test
val hitResults = frame.hitTest(motionEvent)
for (hit in hitResults) {
    if (hit.trackable is Plane) {
        placeObject(hit.createAnchor())
        break
    }
}
```

---

## Comfort & Safety

### Motion Sickness Prevention
```
1. Maintain 90 FPS (no drops)
2. Avoid camera shake/rotation forced
3. Fixed reference points (cockpit, nose)
4. Vignette during movement
5. Snap turning option
6. Comfort mode presets
```

### Health Warnings
```
- Breaks every 30 minutes
- Age restrictions (varies by platform)
- Seizure warnings
- Clear play area
- Guardian/boundary system
```

---

## Testing Checklist

```
[ ] 90 FPS on target hardware
[ ] No judder or frame drops
[ ] Comfortable locomotion options
[ ] Readable UI at all distances
[ ] Controller haptics working
[ ] Hand tracking fallback (if applicable)
[ ] Guardian/boundary integration
[ ] Audio spatialization
[ ] Comfort settings accessible
[ ] Works seated and standing
```
