---
name: mobile-ux-patterns
description: Mobile UX patterns for touch gestures, haptic feedback, accessibility, and platform-native interactions. Essential for building truly mobile-friendly apps.
---

# Mobile UX Patterns

## Touch Gesture System

### React Native Gesture Handler

```tsx
import { Gesture, GestureDetector, GestureHandlerRootView } from 'react-native-gesture-handler';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring,
  runOnJS,
} from 'react-native-reanimated';

// ═══════════════════════════════════════════════════════════
// TAP GESTURE
// ═══════════════════════════════════════════════════════════
function TapExample() {
  const scale = useSharedValue(1);
  
  const tapGesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withSpring(0.95);
    })
    .onFinalize(() => {
      scale.value = withSpring(1);
    })
    .onEnd(() => {
      runOnJS(handleTap)();
    });
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  return (
    <GestureDetector gesture={tapGesture}>
      <Animated.View style={animatedStyle}>
        <Text>Tap me</Text>
      </Animated.View>
    </GestureDetector>
  );
}

// ═══════════════════════════════════════════════════════════
// LONG PRESS
// ═══════════════════════════════════════════════════════════
function LongPressExample({ onLongPress }: { onLongPress: () => void }) {
  const longPressGesture = Gesture.LongPress()
    .minDuration(500)
    .onStart(() => {
      // Haptic feedback
      runOnJS(Haptics.impactAsync)(Haptics.ImpactFeedbackStyle.Medium);
      runOnJS(onLongPress)();
    });
  
  return (
    <GestureDetector gesture={longPressGesture}>
      <View style={styles.card}>
        <Text>Long press for options</Text>
      </View>
    </GestureDetector>
  );
}

// ═══════════════════════════════════════════════════════════
// SWIPE TO DELETE
// ═══════════════════════════════════════════════════════════
function SwipeToDelete({ onDelete }: { onDelete: () => void }) {
  const translateX = useSharedValue(0);
  const DELETE_THRESHOLD = -100;
  
  const panGesture = Gesture.Pan()
    .activeOffsetX([-10, 10])
    .onUpdate((event) => {
      // Only allow left swipe
      translateX.value = Math.min(0, event.translationX);
    })
    .onEnd((event) => {
      if (translateX.value < DELETE_THRESHOLD) {
        translateX.value = withSpring(-300);
        runOnJS(onDelete)();
      } else {
        translateX.value = withSpring(0);
      }
    });
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));
  
  return (
    <View style={styles.container}>
      {/* Delete background */}
      <View style={styles.deleteBackground}>
        <Text style={styles.deleteText}>Delete</Text>
      </View>
      
      {/* Swipeable content */}
      <GestureDetector gesture={panGesture}>
        <Animated.View style={[styles.card, animatedStyle]}>
          <Text>Swipe left to delete</Text>
        </Animated.View>
      </GestureDetector>
    </View>
  );
}

// ═══════════════════════════════════════════════════════════
// PINCH TO ZOOM
// ═══════════════════════════════════════════════════════════
function PinchToZoom({ imageUri }: { imageUri: string }) {
  const scale = useSharedValue(1);
  const savedScale = useSharedValue(1);
  
  const pinchGesture = Gesture.Pinch()
    .onUpdate((event) => {
      scale.value = savedScale.value * event.scale;
    })
    .onEnd(() => {
      // Clamp scale between 1 and 4
      const finalScale = Math.min(Math.max(scale.value, 1), 4);
      scale.value = withSpring(finalScale);
      savedScale.value = finalScale;
    });
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  return (
    <GestureDetector gesture={pinchGesture}>
      <Animated.Image source={{ uri: imageUri }} style={[styles.image, animatedStyle]} />
    </GestureDetector>
  );
}

// ═══════════════════════════════════════════════════════════
// DRAG & DROP
// ═══════════════════════════════════════════════════════════
function DraggableCard() {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const isDragging = useSharedValue(false);
  
  const panGesture = Gesture.Pan()
    .onStart(() => {
      isDragging.value = true;
    })
    .onUpdate((event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;
    })
    .onEnd(() => {
      isDragging.value = false;
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
      { scale: isDragging.value ? 1.1 : 1 },
    ],
    zIndex: isDragging.value ? 100 : 1,
    shadowOpacity: isDragging.value ? 0.3 : 0.1,
  }));
  
  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        <Text>Drag me</Text>
      </Animated.View>
    </GestureDetector>
  );
}

// ═══════════════════════════════════════════════════════════
// DOUBLE TAP TO LIKE
// ═══════════════════════════════════════════════════════════
function DoubleTapToLike({ onLike }: { onLike: () => void }) {
  const scale = useSharedValue(0);
  
  const doubleTap = Gesture.Tap()
    .numberOfTaps(2)
    .onStart(() => {
      scale.value = withSpring(1, {}, () => {
        scale.value = withSpring(0);
      });
      runOnJS(Haptics.notificationAsync)(Haptics.NotificationFeedbackType.Success);
      runOnJS(onLike)();
    });
  
  const heartStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: scale.value,
  }));
  
  return (
    <GestureDetector gesture={doubleTap}>
      <View style={styles.imageContainer}>
        <Image source={require('./image.jpg')} style={styles.image} />
        <Animated.View style={[styles.heart, heartStyle]}>
          <Text style={styles.heartEmoji}>❤️</Text>
        </Animated.View>
      </View>
    </GestureDetector>
  );
}
```

---

## Flutter Gesture Patterns

```dart
// ═══════════════════════════════════════════════════════════
// TAP & LONG PRESS
// ═══════════════════════════════════════════════════════════
GestureDetector(
  onTap: () => print('Tapped'),
  onDoubleTap: () => print('Double tapped'),
  onLongPress: () {
    HapticFeedback.mediumImpact();
    showOptions();
  },
  child: Container(
    child: Text('Interactive'),
  ),
)

// ═══════════════════════════════════════════════════════════
// SWIPE / PAN
// ═══════════════════════════════════════════════════════════
class SwipeCard extends StatefulWidget {
  @override
  _SwipeCardState createState() => _SwipeCardState();
}

class _SwipeCardState extends State<SwipeCard> {
  double _offset = 0;
  
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onHorizontalDragUpdate: (details) {
        setState(() {
          _offset += details.delta.dx;
        });
      },
      onHorizontalDragEnd: (details) {
        if (_offset.abs() > 100) {
          // Swipe detected
          _handleSwipe(_offset > 0 ? 'right' : 'left');
        }
        setState(() => _offset = 0);
      },
      child: Transform.translate(
        offset: Offset(_offset, 0),
        child: Card(child: Text('Swipe me')),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════
// PINCH TO ZOOM
// ═══════════════════════════════════════════════════════════
InteractiveViewer(
  minScale: 0.5,
  maxScale: 4.0,
  child: Image.network('https://example.com/image.jpg'),
)

// ═══════════════════════════════════════════════════════════
// CUSTOM MULTI-GESTURE
// ═══════════════════════════════════════════════════════════
class MultiGestureWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RawGestureDetector(
      gestures: {
        AllowMultipleGestureRecognizer: GestureRecognizerFactoryWithHandlers<
            AllowMultipleGestureRecognizer>(
          () => AllowMultipleGestureRecognizer(),
          (AllowMultipleGestureRecognizer instance) {
            instance.onTap = () => print('Tap');
          },
        ),
      },
      child: Container(),
    );
  }
}
```

---

## Haptic Feedback

### React Native (Expo)

```tsx
import * as Haptics from 'expo-haptics';

// Light feedback for selections
Haptics.selectionAsync();

// Impact feedback (Light, Medium, Heavy)
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

// Notification feedback
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
```

### Flutter (WASM)
- **Near-Native Web:** Flutter Web apps compiled to WASM for 2x faster performance.
- **Energy Efficiency:** 20-30% lower battery usage compared to JS.

---

## Mobile WASM (2025)
For background processing or heavy logic (Encryption, AI inference):
```typescript
// Load WASM module in Mobile WebView or Node-like environment
const wasmModule = await WebAssembly.instantiateStreaming(
  fetch('module.wasm')
);
const result = wasmModule.instance.exports.heavy_logic();
```

---

## Touch Target Guidelines

| Element | Minimum Size | Recommended |
|---------|--------------|-------------|
| Buttons | 44x44 pt | 48x48 pt |
| Icons | 24x24 pt | 32x32 pt |
| List items | 44pt height | 48-56pt height |
| Touch spacing | 8pt between | 12pt between |

```tsx
// Good touch target
const styles = StyleSheet.create({
  button: {
    minHeight: 48,
    minWidth: 48,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  iconButton: {
    width: 48,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listItem: {
    minHeight: 56,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
});
```

---

## Accessibility Gestures

```tsx
import { AccessibilityInfo, View, Text } from 'react-native';

function AccessibleButton({ onPress, label }) {
  return (
    <View
      accessible={true}
      accessibilityLabel={label}
      accessibilityRole="button"
      accessibilityHint="Double tap to activate"
      accessibilityActions={[
        { name: 'activate', label: 'Activate' },
        { name: 'magicTap', label: 'Magic Tap' },
      ]}
      onAccessibilityAction={(event) => {
        if (event.nativeEvent.actionName === 'activate') {
          onPress();
        }
      }}
    >
      <Text>{label}</Text>
    </View>
  );
}

// Check if screen reader is enabled
const [screenReaderEnabled, setScreenReaderEnabled] = useState(false);

useEffect(() => {
  AccessibilityInfo.isScreenReaderEnabled().then(setScreenReaderEnabled);
  const subscription = AccessibilityInfo.addEventListener(
    'screenReaderChanged',
    setScreenReaderEnabled
  );
  return () => subscription.remove();
}, []);
```

---

## Pull to Refresh

```tsx
import { RefreshControl, ScrollView } from 'react-native';

function PullToRefresh() {
  const [refreshing, setRefreshing] = useState(false);
  
  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  }, []);
  
  return (
    <ScrollView
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor="#007AFF"
          title="Yenileniyor..."
          titleColor="#666"
        />
      }
    >
      {/* Content */}
    </ScrollView>
  );
}
```

---

## Best Practices Checklist

```markdown
## Touch UX Checklist

### Gestures
- [ ] All interactive elements are at least 44x44pt
- [ ] Touch targets have adequate spacing (8pt+)
- [ ] Gestures have visual feedback (scale, opacity)
- [ ] Haptic feedback for important actions
- [ ] Swipe gestures have clear visual cues

### Performance
- [ ] Animations run at 60fps
- [ ] Using native driver for animations
- [ ] No blocking operations on gesture thread
- [ ] Optimized re-renders (memo, useCallback)

### Accessibility
- [ ] All elements have accessibility labels
- [ ] Gestures have alternative actions
- [ ] Screen reader announcements work
- [ ] Magic tap gesture supported
- [ ] Reduced motion option respected

### Platform Conventions
- [ ] iOS: Right-edge swipe for back navigation
- [ ] Android: Back button/gesture works
- [ ] Platform-specific haptic patterns
- [ ] Native scroll physics
```

---

## Common Mistakes to Avoid

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Small touch targets (< 44pt) | Min 44x44pt touch area |
| No gesture feedback | Visual + haptic feedback |
| Blocking JS during gesture | Use worklets/native driver |
| Ignoring accessibility | Full a11y support |
| Same haptics everywhere | Context-appropriate haptics |
| Conflicting gestures | Proper gesture composition |
