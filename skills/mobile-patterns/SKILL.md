---
name: mobile-patterns
description: Cross-platform mobile development patterns for React Native and Flutter.
---

# Mobile Patterns

## React Native Patterns

### React 19 Actions in RN
```tsx
function SearchScreen() {
  const [error, submitAction, isPending] = useActionState(async (prev, formData) => {
    return await searchAPI(formData.get('query'));
  }, null);

  return (
    <View>
      <TextInput name="query" />
      <Button onPress={submitAction} title="Search" disabled={isPending} />
    </View>
  );
}
```

### React Server Components (Expo RSC)
```tsx
// server-component.tsx
export default async function DataList() {
  const data = await db.query('SELECT * FROM items'); // Direct DB access!
  return <View>{data.map(item => <Text>{item.name}</Text>)}</View>;
}
```

### Navigation
```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## Flutter Patterns (2025)

### Impeller & Dart 3 Patterns
```dart
// Destructuring with patterns
var (name, age) = ('Mehmet', 25);

// Impeller-ready Graphics
CustomPaint(
  painter: MyImpellerPainter(), // Optimized for Impeller renderer
)
```

## Best Practices

1. **Performance**: Use FlatList/ListView for long lists
2. **Offline**: Handle network failures gracefully
3. **Accessibility**: Always add accessibility labels
4. **Testing**: Test on real devices, not just emulators
