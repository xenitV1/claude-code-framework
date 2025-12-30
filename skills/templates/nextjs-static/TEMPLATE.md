---
name: nextjs-static
description: Static site template with Next.js, perfect for landing pages, portfolios, and marketing sites.
---

# Next.js Static Site Template

## Tech Stack

- **Framework:** Next.js 14 (Static Export)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **SEO:** Next SEO

---

## Directory Structure

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Home/Landing
│   │   ├── about/
│   │   │   └── page.tsx
│   │   ├── contact/
│   │   │   └── page.tsx
│   │   └── blog/
│   │       ├── page.tsx          # Blog list
│   │       └── [slug]/
│   │           └── page.tsx      # Blog post
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── sections/
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── Pricing.tsx
│   │   │   └── CTA.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       └── Container.tsx
│   ├── lib/
│   │   ├── utils.ts
│   │   └── content.ts            # Static content/data
│   └── styles/
│       └── globals.css
├── content/                      # Markdown content
│   └── blog/
│       └── first-post.md
├── public/
│   ├── images/
│   └── favicon.ico
├── next.config.js
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "export": "next build",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.330.0",
    "next-seo": "^6.4.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0"
  }
}
```

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
};

module.exports = nextConfig;
```

### src/app/layout.tsx

```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '{{PROJECT_NAME}} - Your Tagline Here',
  description: 'A brief description of your product or service.',
  openGraph: {
    title: '{{PROJECT_NAME}}',
    description: 'A brief description of your product or service.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

### src/components/sections/Hero.tsx

```tsx
'use client';

import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/Button';

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-slate-900 to-slate-800 py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-2xl text-center"
        >
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">
            Build something{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              amazing
            </span>
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-300">
            Create stunning websites with our modern template. 
            Fast, responsive, and SEO-optimized out of the box.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Button size="lg">
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" size="lg">
              Learn More
            </Button>
          </div>
        </motion.div>
      </div>
      
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/2 top-0 -translate-x-1/2 blur-3xl">
          <div
            className="aspect-[1155/678] w-[72rem] bg-gradient-to-tr from-blue-500 to-purple-500 opacity-20"
            style={{
              clipPath:
                'polygon(74% 44%, 100% 61%, 97% 26%, 85% 0%, 80% 2%, 72% 32%, 60% 62%, 52% 68%, 47% 58%, 45% 34%, 27% 76%, 0% 64%, 17% 100%, 27% 76%, 76% 97%, 74% 44%)',
            }}
          />
        </div>
      </div>
    </section>
  );
}
```

### src/components/ui/Button.tsx

```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={twMerge(
        clsx(
          'inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-200',
          {
            'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
            'bg-slate-700 text-white hover:bg-slate-600': variant === 'secondary',
            'border-2 border-white/20 text-white hover:bg-white/10': variant === 'outline',
            'px-3 py-1.5 text-sm': size === 'sm',
            'px-4 py-2 text-base': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

### src/components/sections/Features.tsx

```tsx
'use client';

import { motion } from 'framer-motion';
import { Zap, Shield, Palette, Rocket } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Optimized for speed with static generation and edge caching.',
  },
  {
    icon: Shield,
    title: 'Secure by Default',
    description: 'Built with security best practices and no server vulnerabilities.',
  },
  {
    icon: Palette,
    title: 'Beautiful Design',
    description: 'Modern, responsive design that looks great on all devices.',
  },
  {
    icon: Rocket,
    title: 'Easy to Deploy',
    description: 'Deploy anywhere: Vercel, Netlify, GitHub Pages, or any static host.',
  },
];

export function Features() {
  return (
    <section className="py-24 bg-white">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            A complete toolkit for building modern static websites.
          </p>
        </div>
        
        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              viewport={{ once: true }}
              className="relative rounded-2xl border border-gray-200 p-8 hover:shadow-lg transition-shadow"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600">
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">
                {feature.title}
              </h3>
              <p className="mt-2 text-gray-600">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## Deployment

### Static Export

```bash
npm run build
# Output in 'out' directory
```

### Deploy Options

| Platform | Command |
|----------|---------|
| Vercel | `vercel --prod` |
| Netlify | Drag & drop `out` folder |
| GitHub Pages | Push `out` to `gh-pages` branch |
| Any static host | Upload `out` folder |

---

## Setup Steps

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. `cd {{name}}`
3. Install: `npm install framer-motion lucide-react next-seo clsx tailwind-merge`
4. Update `next.config.js` for static export
5. Copy template components
6. `npm run dev`
