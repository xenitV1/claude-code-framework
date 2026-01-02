---
name: mobile-games
description: Mobile game development for iOS and Android. Use when building touch-based games, optimizing battery, handling app store submissions, or implementing mobile-specific features like ads and in-app purchases.
---

# Mobile Game Development

> Platform-specific patterns for iOS and Android games

## Touch Controls

### Gesture Recognition
```typescript
// Touch input patterns
const gestures = {
    tap: { maxDuration: 200, maxDistance: 10 },
    longPress: { minDuration: 500 },
    swipe: { minDistance: 50, maxDuration: 300 },
    pinch: { fingers: 2 },
    drag: { fingers: 1 }
};

// Virtual joystick
class VirtualJoystick {
    private center: Vector2;
    private maxRadius: number = 50;
    
    getDirection(): Vector2 {
        const delta = touchPos.subtract(center);
        return delta.normalize().clampLength(1);
    }
}
```

### Touch-Friendly UI
```
Minimum touch target: 44x44 points (iOS) / 48x48 dp (Android)
Button spacing: 8-16 points minimum
Avoid: Small buttons, hover states, precise gestures
```

---

## Performance Optimization

### Battery Optimization
```
Target: 30-60 FPS (adaptive)
When battery low or thermal throttling:
- Reduce FPS to 30
- Lower particle counts
- Disable post-processing
- Reduce physics iterations
```

### Thermal Management
```typescript
// Unity - Adaptive Performance
AdaptivePerformance.DeviceThermalStateChanged += (state) => {
    switch(state) {
        case ThermalState.Throttling:
            QualitySettings.SetQualityLevel(0);
            Application.targetFrameRate = 30;
            break;
    }
};
```

### Memory Limits
| Device | Safe RAM | Max Textures |
|--------|----------|--------------|
| Low-end | 512MB | 1K-2K |
| Mid-range | 1GB | 2K |
| High-end | 2GB+ | 4K |

---

## Responsive UI

### Safe Areas
```typescript
// Handle notches/cutouts
const safeArea = Screen.safeArea;
canvas.style.padding = `${safeArea.top}px ${safeArea.right}px`;
```

### Adaptive Layouts
```
Portrait: Vertical stacking, thumb-friendly bottom controls
Landscape: Horizontal layout, dual thumbsticks
Tablet: Larger UI, more screen real estate
```

### Resolution Scaling
```typescript
// Dynamic resolution for performance
const dpr = Math.min(window.devicePixelRatio, 2);
renderer.setPixelRatio(dpr);
```

---

## App Store Guidelines

### iOS (App Store)
```
Required:
- Privacy policy
- App Tracking Transparency (ATT) for ads
- Sign in with Apple (if other social logins)
- Age rating questionnaire

Avoid:
- External payment links
- Mention of other platforms
- Beta/test in screenshots
```

### Android (Play Store)
```
Required:
- Content rating
- Privacy policy
- Data safety form
- Target API level (current year - 1)

Avoid:
- Deceptive ads
- Misleading screenshots
- Keyword stuffing
```

---

## Monetization

### In-App Purchases (Ethical)
```typescript
// Consumables: Coins, gems, lives
// Non-consumables: Remove ads, unlock levels
// Subscriptions: VIP pass, battle pass

// Always show real price, not just premium currency
const product = await store.getProduct("remove_ads");
showButton(`Remove Ads - ${product.localizedPrice}`);
```

### Ad Integration
```typescript
// Rewarded ads (preferred - user choice)
adManager.showRewarded({
    onReward: () => player.addCoins(100),
    onDismiss: () => resumeGame()
});

// Interstitials (sparingly)
// Show between levels, not mid-gameplay
// Frequency cap: Max every 3-5 minutes
```

### Ethical Guidelines
```
Do:
✅ Rewarded ads (optional)
✅ Cosmetics-only purchases
✅ Clear pricing
✅ No pay-to-win in multiplayer

Avoid:
❌ Loot boxes with real money
❌ Aggressive upsells
❌ Hidden costs
❌ Targeting children
```

---

## Push Notifications

### Engagement (Non-Annoying)
```typescript
// Good:
// - Daily reward available
// - Friend activity
// - Event starting

// Bad:
// - Come back! We miss you!
// - Buy now!
// - Constant reminders

const notification = {
    title: "Daily Reward Ready!",
    body: "Claim your free gems",
    schedule: { hour: 18, minute: 0 }
};
```

---

## Cross-Platform Considerations

### Unity Mobile
```csharp
// Platform-specific code
#if UNITY_IOS
    // iOS-specific
#elif UNITY_ANDROID
    // Android-specific
#endif

// Touch input
if (Input.touchCount > 0) {
    Touch touch = Input.GetTouch(0);
    if (touch.phase == TouchPhase.Began) {
        HandleTap(touch.position);
    }
}
```

### Godot Mobile Export
```gdscript
# Touch input
func _input(event: InputEvent) -> void:
    if event is InputEventScreenTouch:
        if event.pressed:
            handle_tap(event.position)
    elif event is InputEventScreenDrag:
        handle_drag(event.velocity)
```

---

## Testing

### Device Coverage
```
Test on:
- Low-end phone (2-3 years old)
- Current flagship
- Tablet
- Different aspect ratios (16:9, 19.5:9, 20:9)
```

### Checklist
```
[ ] Touch targets large enough
[ ] Works offline
[ ] Handles interruptions (calls, notifications)
[ ] Respects mute switch
[ ] Battery usage acceptable
[ ] Loads quickly (<5 seconds)
[ ] Handles background/foreground
```
