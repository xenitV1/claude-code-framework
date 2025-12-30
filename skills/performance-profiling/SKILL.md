---
name: performance-profiling
description: Performance profiling techniques for web applications including Core Web Vitals, bundle analysis, and runtime profiling.
---

# Performance Profiling

## Core Web Vitals

### Targets
| Metric | Good | Poor |
|--------|------|------|
| LCP (Largest Contentful Paint) | < 2.5s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |

### Measurement Commands
```bash
# Lighthouse CLI
npx lighthouse https://example.com --output html

# Web Vitals library
npm install web-vitals
```

## Bundle Analysis

```bash
# Next.js bundle analyzer
ANALYZE=true npm run build

# Vite bundle analyzer
npx vite-bundle-visualizer

# General webpack analyzer
npx webpack-bundle-analyzer stats.json
```

## Runtime Profiling

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Chrome DevTools
# Performance tab → Record → Analyze flame chart
```

## Quick Wins

1. **Lazy load images**: Use `loading="lazy"`
2. **Code splitting**: Dynamic imports
3. **Compress assets**: Enable gzip/brotli
4. **Cache headers**: Set proper Cache-Control
5. **Optimize images**: Use WebP, proper sizing
