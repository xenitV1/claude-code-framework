---
name: tailwind-patterns
description: Tailwind CSS patterns including responsive design, custom components, and dark mode.
---

# Tailwind Patterns

## Responsive Design

```html
<!-- Mobile-first approach -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on md, third on lg -->
</div>

<!-- Hide/show based on breakpoint -->
<div class="hidden md:block">Desktop only</div>
<div class="block md:hidden">Mobile only</div>
```

## Component Patterns

```tsx
// Button variants
const buttonVariants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white",
  secondary: "bg-gray-200 hover:bg-gray-300 text-gray-800",
  danger: "bg-red-600 hover:bg-red-700 text-white"
};

function Button({ variant = "primary", children, ...props }) {
  return (
    <button 
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${buttonVariants[variant]}`}
      {...props}
    >
      {children}
    </button>
  );
}
```

## Dark Mode

```html
<!-- With dark: prefix -->
<div class="bg-white dark:bg-gray-900">
  <p class="text-gray-900 dark:text-white">Content</p>
</div>
```

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  // ...
}
```

## Common Patterns

```html
<!-- Card -->
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-lg font-semibold mb-2">Title</h3>
  <p class="text-gray-600">Content</p>
</div>

<!-- Flex center -->
<div class="flex items-center justify-center h-screen">
  Centered content
</div>

<!-- Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Tailwind CSS v4 (Oxide)
V4 is CSS-first. Design tokens are defined using `@theme`:

```css
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --font-display: "Satoshi", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

### Breaking Changes 2025
- No more `tailwind.config.js` by default.
- Modern CSS variables are generated for all tokens.
- Native CSS nesting supported (no plugin needed).
- `border` defaults to `currentColor` (previously `gray-200`).
