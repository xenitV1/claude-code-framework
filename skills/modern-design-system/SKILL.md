---
name: modern-design-system
description: 2025 UI design trends and patterns including glassmorphism, bento grids, micro-animations, and modern aesthetics. Essential for creating visually stunning, premium web interfaces.
---

# Modern Design System - 2025 UI Trends

> Comprehensive guide for premium, aesthetic, dynamic designs

---

## 🎨 2025 Visual Styles

### 1. Glassmorphism (Frosted Glass UI)

```css
/* Core Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

/* Dark mode glass */
.glass-dark {
  background: rgba(17, 25, 40, 0.75);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.125);
}

/* Colorful glass */
.glass-gradient {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
  backdrop-filter: blur(20px);
}
```

```tsx
// React Glassmorphism Component
interface GlassCardProps {
  children: React.ReactNode;
  blur?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function GlassCard({ children, blur = 'md', className }: GlassCardProps) {
  const blurValues = { sm: 'blur-sm', md: 'blur-md', lg: 'blur-xl' };
  
  return (
    <div
      className={cn(
        'bg-white/10 backdrop-blur-md border border-white/20',
        'rounded-2xl shadow-xl',
        'hover:bg-white/15 transition-all duration-300',
        className
      )}
    >
      {children}
    </div>
  );
}
```

---

### 2. Bento Grid Layout

```tsx
// Bento Grid with CSS Grid
export function BentoGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-4 gap-4 p-4">
      {children}
    </div>
  );
}

// Grid item with span options
interface BentoItemProps {
  children: React.ReactNode;
  colSpan?: 1 | 2 | 3 | 4;
  rowSpan?: 1 | 2;
}

export function BentoItem({ children, colSpan = 1, rowSpan = 1 }: BentoItemProps) {
  const colClasses = {
    1: 'col-span-1',
    2: 'col-span-2',
    3: 'col-span-3',
    4: 'col-span-4',
  };
  
  const rowClasses = {
    1: 'row-span-1',
    2: 'row-span-2',
  };
  
  return (
    <div
      className={cn(
        colClasses[colSpan],
        rowClasses[rowSpan],
        'bg-gradient-to-br from-slate-800 to-slate-900',
        'rounded-3xl p-6 border border-slate-700',
        'hover:border-slate-600 transition-all duration-300',
        'group'
      )}
    >
      {children}
    </div>
  );
}

// Usage Example
<BentoGrid>
  <BentoItem colSpan={2} rowSpan={2}>
    <FeatureCard title="Hero Feature" />
  </BentoItem>
  <BentoItem>
    <StatCard number="100K+" label="Users" />
  </BentoItem>
  <BentoItem>
    <StatCard number="99.9%" label="Uptime" />
  </BentoItem>
  <BentoItem colSpan={2}>
    <IntegrationList />
  </BentoItem>
</BentoGrid>
```

---

### 3. Micro-Animations & Motion

```tsx
// Framer Motion Patterns
import { motion, useInView } from 'framer-motion';

// Fade up on scroll
export function FadeUp({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.6, delay, ease: [0.25, 0.1, 0.25, 1] }}
    >
      {children}
    </motion.div>
  );
}

// Stagger children animation
export const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

export const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut' }
  },
};

// Hover scale with spring
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>

// Smooth counter animation
function AnimatedCounter({ value }: { value: number }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (v) => Math.round(v));
  
  useEffect(() => {
    const controls = animate(count, value, { duration: 2 });
    return controls.stop;
  }, [value]);
  
  return <motion.span>{rounded}</motion.span>;
}
```

---

### 4. Modern Color Palettes

```css
:root {
  /* ═══════════════════════════════════════════════════════════
     DARK THEME - Slate/Zinc based (Premium feel)
     ═══════════════════════════════════════════════════════════ */
  --bg-primary: #0a0a0a;
  --bg-secondary: #111111;
  --bg-tertiary: #1a1a1a;
  --bg-elevated: #262626;
  
  --text-primary: #fafafa;
  --text-secondary: #a3a3a3;
  --text-muted: #737373;
  
  /* Accent gradients */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-warm: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --gradient-cool: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --gradient-sunset: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  
  /* Glow effects */
  --glow-primary: 0 0 40px rgba(139, 92, 246, 0.3);
  --glow-success: 0 0 40px rgba(34, 197, 94, 0.3);
  --glow-warning: 0 0 40px rgba(234, 179, 8, 0.3);
  
  /* ═══════════════════════════════════════════════════════════
     VIBRANT ACCENTS
     ═══════════════════════════════════════════════════════════ */
  --accent-violet: #8b5cf6;
  --accent-fuchsia: #d946ef;
  --accent-cyan: #06b6d4;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;
}

/* Aurora/Mesh Gradient Background */
.aurora-bg {
  background: 
    radial-gradient(ellipse at 20% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 40% 40%, rgba(244, 63, 94, 0.1) 0%, transparent 50%),
    #0a0a0a;
}
```

---

### 5. Premium Typography

```css
/* Font imports */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cal+Sans&display=swap');

:root {
  /* Type scale (modular scale 1.25) */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 4rem;        /* 64px */
  
  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-black: 800;
  
  /* Line heights */
  --leading-tight: 1.1;
  --leading-snug: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Letter spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.05em;
}

/* Hero heading */
.hero-heading {
  font-family: 'Cal Sans', 'Inter', sans-serif;
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #fff 0%, #a3a3a3 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

### 6. Premium Button Styles

```tsx
// Button variants with modern aesthetics
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'gradient' | 'glow';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({ variant = 'primary', size = 'md', className, children, ...props }: ButtonProps) {
  const variants = {
    primary: 'bg-white text-black hover:bg-gray-100',
    secondary: 'bg-white/10 text-white border border-white/20 hover:bg-white/20',
    ghost: 'text-white hover:bg-white/10',
    gradient: 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white hover:opacity-90',
    glow: `
      bg-violet-600 text-white
      shadow-[0_0_20px_rgba(139,92,246,0.5)]
      hover:shadow-[0_0_30px_rgba(139,92,246,0.7)]
    `,
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm rounded-lg',
    md: 'px-4 py-2.5 text-sm rounded-xl',
    lg: 'px-6 py-3 text-base rounded-xl',
  };
  
  return (
    <button
      className={cn(
        'font-medium transition-all duration-200',
        'focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-black',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

---

### 7. Card Patterns

```tsx
// Feature Card with hover effects
export function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={cn(
        'group relative p-6 rounded-2xl',
        'bg-gradient-to-br from-slate-800/50 to-slate-900/50',
        'border border-slate-700/50',
        'hover:border-violet-500/50 hover:shadow-[0_0_30px_rgba(139,92,246,0.1)]',
        'transition-all duration-300'
      )}
    >
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-violet-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <div className="relative z-10">
        <div className="w-12 h-12 rounded-xl bg-violet-600/20 flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
        <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
      </div>
    </motion.div>
  );
}

// Stat Card with animated number
export function StatCard({ value, label, suffix = '' }: StatCardProps) {
  return (
    <div className="p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
      <div className="text-4xl font-bold text-white mb-1">
        <AnimatedCounter value={parseInt(value)} />{suffix}
      </div>
      <div className="text-sm text-gray-400">{label}</div>
    </div>
  );
}
```

---

### 8. Section Layouts

```tsx
// Hero Section
export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Aurora background */}
      <div className="absolute inset-0 aurora-bg" />
      
      {/* Grid pattern */}
      <div 
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px',
        }}
      />
      
      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        <FadeUp>
          <span className="inline-block px-4 py-1.5 rounded-full bg-violet-600/20 text-violet-400 text-sm font-medium mb-6">
            ✨ Introducing v2.0
          </span>
        </FadeUp>
        
        <FadeUp delay={0.1}>
          <h1 className="hero-heading mb-6">
            Build something<br />
            <span className="gradient-text">extraordinary</span>
          </h1>
        </FadeUp>
        
        <FadeUp delay={0.2}>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10">
            The modern platform for building beautiful, performant web applications.
          </p>
        </FadeUp>
        
        <FadeUp delay={0.3}>
          <div className="flex gap-4 justify-center">
            <Button variant="gradient" size="lg">Get Started</Button>
            <Button variant="secondary" size="lg">Learn More</Button>
          </div>
        </FadeUp>
      </div>
    </section>
  );
}
```

---

## 📋 Design Quality Checklist

```markdown
## Visual Excellence Checklist

### Colors & Theming
- [ ] Custom color palette (not generic Tailwind defaults)
- [ ] Gradient accents used purposefully
- [ ] Dark mode with proper contrast ratios
- [ ] Glow effects for emphasis

### Typography
- [ ] Custom font stack (Inter, Cal Sans, etc.)
- [ ] Clear type hierarchy (6+ sizes)
- [ ] Gradient text for headlines
- [ ] Proper line-height & letter-spacing

### Layout
- [ ] Bento grid for complex content
- [ ] Generous whitespace (not cramped)
- [ ] Consistent spacing scale (8pt grid)
- [ ] Hero section with visual impact

### Motion & Interaction
- [ ] Micro-animations on buttons
- [ ] Scroll-triggered reveals
- [ ] Hover states with depth (y-translation)
- [ ] Page transitions

### Components
- [ ] Glassmorphism cards where appropriate
- [ ] Gradient buttons
- [ ] Animated counters
- [ ] Loading skeletons

### Premium Touches
- [ ] Subtle noise/grain texture
- [ ] Grid/dot patterns in backgrounds
- [ ] Cursor effects (optional)
- [ ] Easter eggs
```

---

## ❌ Avoid: AI Slop Design

| ❌ Avoid | ✅ Instead |
|----------|-----------|
| Generic blue-purple gradient | Custom brand gradient |
| `box-shadow: 0 4px 6px` everywhere | Subtle, context-aware shadows |
| Same card layout on every page | Varied layouts (bento, masonry) |
| Default system fonts | Custom font pairing |
| Static, lifeless UI | Micro-animations |
| Stock Heroicons everywhere | Mix of custom + curated icons |
| White background everywhere | Subtle gradients/patterns |
