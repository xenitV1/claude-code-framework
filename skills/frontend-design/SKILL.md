---
name: frontend-design
description: Frontend design patterns that avoid AI slop and create polished, professional interfaces.
---

# Frontend Design

> Source: travisvn/awesome-claude-skills

## Overview
Patterns for creating professional frontend designs that avoid common AI-generated design pitfalls.

## Avoiding "AI Slop"

Common AI design mistakes to avoid:

❌ **Generic gradients** - Blue-purple gradients everywhere
❌ **Overused shadows** - Everything has box-shadow
❌ **Same layout** - Grid of cards on every page
❌ **Stock icons** - Using the same icons everywhere
❌ **No personality** - Generic, soulless design

## Mathematical Proportions & Spacing (2025)

### The 8-Point Grid System
All dimensions, padding, and margins must be multiples of 8 (or 4 for micro-spacing):
- **❌ DO NOT:** Use arbitrary values like `p-[13px]` or `m-7`.
- **✅ DO:** Use Tailwind spacing scale: `p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px).
- **Goal:** Perfect mathematical alignment across the entire UI.

### Golden Ratio & Visual Hierarchy
- Use the **Golden Ratio (1.618)** for component sizing and typography scales.
- Ensure consistent aspect ratios (e.g., `aspect-video`, `aspect-square`) for all media elements.
- Maintain "Optical Balance" - sometimes geometric center is not the visual center.

### 1. Intentional Color
```css
/* Don't: Generic blue gradient */
background: linear-gradient(to right, #3B82F6, #8B5CF6);

/* Do: Tailwind CSS v4 CSS-First Theme */
@theme {
  --color-primary: #0F766E;
  --color-accent: #F97316;
  --font-brand: "Inter", sans-serif;
}
```

### 2. Thoughtful Typography
```css
/* Don't: Default system font */
font-family: sans-serif;

/* Do: Intentional font pairing */
font-family: 'Inter', system-ui, sans-serif;
.heading { font-family: 'Cal Sans', serif; }
```

### 3. Container Queries (Micro-Layouts)
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card-content { display: grid; grid-template-columns: 1fr 2fr; }
}
```

### 4. View Transitions API
```javascript
// Native app-like navigation transitions
if (document.startViewTransition) {
  document.startViewTransition(() => {
    updateTheDOM();
  });
}
```

### 5. Subtle Animations
```css
/* Using Tailwind v4 3D utilities */
.card-hover {
  transition: transform 0.2s;
  &:hover { transform: rotateY(10deg) scale(1.02); }
}
```

### 6. Meaningful Spacing
```css
/* Use consistent spacing scale */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-4: 1rem;     /* 16px */
--space-8: 2rem;     /* 32px */
```

## Component Guidelines

```tsx
// Professional card design
<div className="
  bg-white rounded-xl p-6
  border border-gray-100
  hover:border-gray-200
  transition-colors duration-150
">
  {/* Content */}
</div>
```

<!-- Mobile-first approach -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on md, third on lg -->
</div>

## Mathematical Spacing (8-Point Grid)
Strictly follow the 8-point grid for visual consistency:
```html
<div class="space-y-4 p-8 m-auto"> <!-- 16px vertical gap, 32px padding -->
  <div class="h-16 w-16"></div> <!-- 64px square -->
</div>
```

## Checklist

- [ ] Colors serve a purpose (not just decoration)
- [ ] Typography has hierarchy
- [ ] Spacing is consistent
- [ ] Animations are subtle and quick
- [ ] Design has personality/brand
- [ ] Accessibility considered
