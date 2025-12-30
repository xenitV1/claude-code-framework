---
name: monorepo-turborepo
description: Monorepo template with Turborepo, pnpm workspaces, and shared packages.
---

# Turborepo Monorepo Template

## Tech Stack

- **Build System:** Turborepo
- **Package Manager:** pnpm
- **Apps:** Next.js, Express API
- **Packages:** Shared UI, Config, Types
- **Language:** TypeScript

---

## Directory Structure

```
project-name/
├── apps/
│   ├── web/                     # Next.js app
│   │   ├── src/
│   │   ├── package.json
│   │   └── next.config.js
│   ├── api/                     # Express API
│   │   ├── src/
│   │   └── package.json
│   └── docs/                    # Documentation site
│       └── package.json
├── packages/
│   ├── ui/                      # Shared UI components
│   │   ├── src/
│   │   │   ├── Button.tsx
│   │   │   └── index.ts
│   │   └── package.json
│   ├── config/                  # Shared configs
│   │   ├── eslint/
│   │   ├── typescript/
│   │   └── tailwind/
│   ├── types/                   # Shared TypeScript types
│   │   ├── src/
│   │   └── package.json
│   └── utils/                   # Shared utilities
│       ├── src/
│       └── package.json
├── turbo.json
├── pnpm-workspace.yaml
├── package.json
└── README.md
```

---

## Core Files

### package.json (root)

```json
{
  "name": "{{PROJECT_NAME}}",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "clean": "turbo clean && rm -rf node_modules",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "prettier": "^3.2.0",
    "turbo": "^2.0.0",
    "typescript": "^5.3.0"
  },
  "packageManager": "pnpm@8.15.0",
  "engines": {
    "node": ">=20.0.0"
  }
}
```

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    },
    "clean": {
      "cache": false
    }
  }
}
```

### apps/web/package.json

```json
{
  "name": "@{{PROJECT_NAME}}/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3000",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@{{PROJECT_NAME}}/ui": "workspace:*",
    "@{{PROJECT_NAME}}/utils": "workspace:*",
    "@{{PROJECT_NAME}}/types": "workspace:*"
  },
  "devDependencies": {
    "@{{PROJECT_NAME}}/config": "workspace:*",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0"
  }
}
```

### apps/api/package.json

```json
{
  "name": "@{{PROJECT_NAME}}/api",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "lint": "eslint src"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "@{{PROJECT_NAME}}/utils": "workspace:*",
    "@{{PROJECT_NAME}}/types": "workspace:*"
  },
  "devDependencies": {
    "@{{PROJECT_NAME}}/config": "workspace:*",
    "@types/express": "^4.17.0",
    "@types/cors": "^2.8.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  }
}
```

### packages/ui/package.json

```json
{
  "name": "@{{PROJECT_NAME}}/ui",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "lint": "eslint src"
  },
  "dependencies": {
    "react": "^18.2.0"
  },
  "devDependencies": {
    "@{{PROJECT_NAME}}/config": "workspace:*",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0"
  }
}
```

### packages/ui/src/Button.tsx

```tsx
import * as React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-colors';
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700',
    outline: 'border-2 border-gray-300 hover:bg-gray-100',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className || ''}`}
      {...props}
    >
      {children}
    </button>
  );
}
```

### packages/ui/src/index.ts

```typescript
export { Button } from './Button';
```

### packages/types/src/index.ts

```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export type { ButtonProps } from '@{{PROJECT_NAME}}/ui';
```

### packages/config/typescript/base.json

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

---

## Setup Steps

1. `mkdir {{name}} && cd {{name}}`
2. `pnpm init`
3. Copy template files
4. `pnpm install`
5. `pnpm dev` (runs all apps in parallel)

---

## Common Commands

```bash
# Run all apps
pnpm dev

# Build all
pnpm build

# Run specific app
pnpm --filter @{{PROJECT_NAME}}/web dev

# Add dependency to specific package
pnpm --filter @{{PROJECT_NAME}}/web add axios

# Add dependency to root
pnpm add -D -w prettier
```
