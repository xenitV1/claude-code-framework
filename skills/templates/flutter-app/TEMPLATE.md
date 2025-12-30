---
name: flutter-app
description: Flutter mobile app template with Riverpod state management, Go Router, and clean architecture.
---

# Flutter App Template

## Tech Stack

- **Framework:** Flutter 3.x
- **Language:** Dart 3.x
- **State Management:** Riverpod 2.0
- **Navigation:** Go Router
- **HTTP:** Dio
- **Storage:** Hive

---

## Directory Structure

```
project_name/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants/
│   │   │   ├── app_colors.dart
│   │   │   └── app_strings.dart
│   │   ├── theme/
│   │   │   └── app_theme.dart
│   │   ├── router/
│   │   │   └── app_router.dart
│   │   └── utils/
│   │       └── extensions.dart
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   │   ├── repositories/
│   │   │   │   └── models/
│   │   │   ├── domain/
│   │   │   │   └── entities/
│   │   │   └── presentation/
│   │   │       ├── screens/
│   │   │       ├── widgets/
│   │   │       └── providers/
│   │   └── home/
│   │       └── ...
│   ├── shared/
│   │   ├── widgets/
│   │   │   ├── app_button.dart
│   │   │   └── app_text_field.dart
│   │   └── providers/
│   │       └── shared_providers.dart
│   └── services/
│       ├── api/
│       │   └── api_client.dart
│       └── storage/
│           └── storage_service.dart
├── test/
├── pubspec.yaml
└── README.md
```

---

## Core Files

### pubspec.yaml

```yaml
name: {{PROJECT_NAME}}
description: {{PROJECT_DESCRIPTION}}
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0
  
  # Navigation
  go_router: ^13.0.0
  
  # Network
  dio: ^5.4.0
  
  # Storage
  hive: ^2.2.0
  hive_flutter: ^1.1.0
  
  # Utils
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0
  
  # UI
  flutter_svg: ^2.0.0
  cached_network_image: ^3.3.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  riverpod_generator: ^2.3.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  hive_generator: ^2.0.0
```

### lib/main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  runApp(
    const ProviderScope(
      child: App(),
    ),
  );
}
```

### lib/app.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';

class App extends ConsumerWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: '{{PROJECT_NAME}}',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

### lib/core/router/app_router.dart

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/home/presentation/screens/home_screen.dart';

part 'app_router.g.dart';

@riverpod
GoRouter router(RouterRef ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Page not found: ${state.uri}'),
      ),
    ),
  );
}
```

### lib/core/theme/app_theme.dart

```dart
import 'package:flutter/material.dart';

class AppTheme {
  static final light = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.light,
    ),
    appBarTheme: const AppBarTheme(
      centerTitle: true,
      elevation: 0,
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      filled: true,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(double.infinity, 48),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    ),
  );

  static final dark = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.dark,
    ),
    appBarTheme: const AppBarTheme(
      centerTitle: true,
      elevation: 0,
    ),
  );
}
```

### lib/services/api/api_client.dart

```dart
import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'api_client.g.dart';

@riverpod
Dio dio(DioRef ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) {
        // Add auth token
        // final token = ref.read(authTokenProvider);
        // options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
      onError: (error, handler) {
        // Handle errors globally
        handler.next(error);
      },
    ),
  );

  return dio;
}

@riverpod
class ApiClient extends _$ApiClient {
  @override
  Dio build() => ref.watch(dioProvider);

  Future<T> get<T>(String path) async {
    final response = await state.get(path);
    return response.data as T;
  }

  Future<T> post<T>(String path, {dynamic data}) async {
    final response = await state.post(path, data: data);
    return response.data as T;
  }
}
```

### lib/shared/widgets/app_button.dart

```dart
import 'package:flutter/material.dart';

class AppButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final ButtonStyle? style;

  const AppButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.style,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: style,
      child: isLoading
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Text(text),
    );
  }
}
```

---

## Setup Steps

1. `flutter create {{name}} --org com.{{BUNDLE_ID}}`
2. `cd {{name}}`
3. Replace `pubspec.yaml`
4. `flutter pub get`
5. Copy template files
6. `dart run build_runner build`
7. `flutter run`

---

## Useful Commands

```bash
# Generate code
dart run build_runner build --delete-conflicting-outputs

# Watch mode
dart run build_runner watch

# Run on specific device
flutter run -d chrome
flutter run -d ios
flutter run -d android

# Build release
flutter build apk --release
flutter build ios --release
```
