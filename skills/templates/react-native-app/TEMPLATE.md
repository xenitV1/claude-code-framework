---
name: react-native-app
description: React Native mobile app template with Expo, TypeScript, navigation, and state management.
---

# React Native App Template

## Tech Stack

- **Framework:** React Native with Expo
- **Language:** TypeScript
- **Navigation:** React Navigation 6
- **State:** Zustand + React Query
- **Styling:** NativeWind (Tailwind for RN)
- **Testing:** Jest + React Native Testing Library

---

## Directory Structure

```
project-name/
├── app/                        # Expo Router (file-based routing)
│   ├── _layout.tsx             # Root layout
│   ├── index.tsx               # Home screen
│   ├── (tabs)/                 # Tab navigation
│   │   ├── _layout.tsx
│   │   ├── home.tsx
│   │   ├── profile.tsx
│   │   └── settings.tsx
│   └── [id].tsx                # Dynamic route
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Loading.tsx
│   └── features/               # Feature-specific components
├── hooks/
│   ├── useAuth.ts
│   └── useApi.ts
├── lib/
│   ├── api.ts                  # API client
│   ├── storage.ts              # AsyncStorage helpers
│   └── utils.ts
├── store/
│   └── useStore.ts             # Zustand store
├── types/
│   └── index.ts
├── constants/
│   ├── Colors.ts
│   └── Layout.ts
├── assets/
│   ├── images/
│   └── fonts/
├── app.json
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── README.md
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {
    "expo": "~50.0.0",
    "expo-router": "~3.4.0",
    "expo-status-bar": "~1.11.0",
    "react": "18.2.0",
    "react-native": "0.73.0",
    "@react-navigation/native": "^6.1.0",
    "react-native-safe-area-context": "4.8.0",
    "react-native-screens": "~3.29.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.0.0",
    "nativewind": "^2.0.0",
    "expo-secure-store": "~12.8.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@types/react": "~18.2.0",
    "typescript": "^5.3.0",
    "tailwindcss": "3.3.2",
    "jest": "^29.0.0",
    "@testing-library/react-native": "^12.0.0",
    "eslint": "^8.0.0"
  }
}
```

### app/_layout.tsx

```tsx
import { Stack } from 'expo-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <Stack
          screenOptions={{
            headerStyle: { backgroundColor: '#1a1a1a' },
            headerTintColor: '#fff',
            headerTitleStyle: { fontWeight: 'bold' },
          }}
        />
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}
```

### components/ui/Button.tsx

```tsx
import { TouchableOpacity, Text, ActivityIndicator, StyleSheet } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  loading?: boolean;
  disabled?: boolean;
}

export function Button({
  title,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
}: ButtonProps) {
  return (
    <TouchableOpacity
      style={[
        styles.button,
        styles[variant],
        (disabled || loading) && styles.disabled,
      ]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color={variant === 'outline' ? '#007AFF' : '#fff'} />
      ) : (
        <Text style={[styles.text, variant === 'outline' && styles.outlineText]}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 48,
  },
  primary: {
    backgroundColor: '#007AFF',
  },
  secondary: {
    backgroundColor: '#5856D6',
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#007AFF',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  outlineText: {
    color: '#007AFF',
  },
});
```

### store/useStore.ts

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  user: { id: string; email: string } | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: { id: string; email: string }, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) =>
        set({ user, token, isAuthenticated: true }),
      logout: () =>
        set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### hooks/useApi.ts

```tsx
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuthStore } from '../store/useStore';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000/api';

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = useAuthStore.getState().token;
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

export function useApiQuery<T>(key: string[], endpoint: string) {
  return useQuery<T>({
    queryKey: key,
    queryFn: () => fetchWithAuth(endpoint),
  });
}

export function useApiMutation<T, V>(endpoint: string, method = 'POST') {
  return useMutation<T, Error, V>({
    mutationFn: (data) =>
      fetchWithAuth(endpoint, {
        method,
        body: JSON.stringify(data),
      }),
  });
}
```

---

## app.json

```json
{
  "expo": {
    "name": "{{PROJECT_NAME}}",
    "slug": "{{PROJECT_SLUG}}",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#1a1a1a"
    },
    "updates": {
      "fallbackToCacheTimeout": 0
    },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.{{BUNDLE_ID}}"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#1a1a1a"
      },
      "package": "com.{{BUNDLE_ID}}"
    },
    "plugins": ["expo-router", "expo-secure-store"]
  }
}
```

---

## Setup Steps

1. `npx create-expo-app {{name}} -t expo-template-blank-typescript`
2. `cd {{name}}`
3. `npx expo install expo-router react-native-safe-area-context react-native-screens`
4. Copy template files
5. `npm install`
6. `npx expo start`

---

## Best Practices

1. **Use Expo Router** for file-based navigation
2. **Zustand for local state**, React Query for server state
3. **NativeWind** for consistent styling with Tailwind classes
4. **Expo SecureStore** for sensitive data (tokens)
5. **Test on both iOS and Android** regularly
