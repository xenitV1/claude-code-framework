---
name: react-patterns
description: Modern React patterns including hooks, component composition, performance optimization, and TypeScript best practices. Use when building React components, implementing state management, or optimizing React applications.
---

# React Patterns

## Overview
This skill provides comprehensive React patterns and best practices for building production-ready applications.

## Core Patterns

### 1. Custom Hooks
Extract reusable logic into custom hooks.

```tsx
// useLocalStorage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value;
    setStoredValue(valueToStore);
    window.localStorage.setItem(key, JSON.stringify(valueToStore));
  };

  return [storedValue, setValue] as const;
}

// useDebounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// useActionState (React 19 Form Management)
function SignupForm() {
  const [error, submitAction, isPending] = useActionState(async (previousState, formData) => {
    const error = await signupUser(formData);
    if (error) return error;
    redirect("/dashboard");
    return null;
  }, null);

  return (
    <form action={submitAction}>
      <input type="email" name="email" />
      <button disabled={isPending}>Sign Up</button>
      {error && <p>{error}</p>}
    </form>
  );
}

// useOptimistic (React 19 Zero Latency UI)
function Chat({ messages, sendMessage }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { text: newMessage, sending: true }]
  );

  return (
    <div>
      {optimisticMessages.map(m => <p key={m.id}>{m.text}</p>)}
      <button onClick={() => addOptimisticMessage("Hello!")}>Send</button>
    </div>
  );
}
```

### 2. Compound Components
Components that work together to share state.

```tsx
// Compound component pattern
interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');
  
  return (
    <button
      className={context.activeTab === id ? 'active' : ''}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');
  
  if (context.activeTab !== id) return null;
  return <div className="tab-panel">{children}</div>;
}

// Usage
<Tabs defaultTab="tab1">
  <TabList>
    <Tab id="tab1">Tab 1</Tab>
    <Tab id="tab2">Tab 2</Tab>
  </TabList>
  <TabPanel id="tab1">Content 1</TabPanel>
  <TabPanel id="tab2">Content 2</TabPanel>
</Tabs>
```

### 3. React Compiler & Memoization (2025)
React 19's Compiler automates memoization. Avoid manual optimization unless necessary:
- **❌ DO NOT:** Proactively wrap every context or component in `memo` or `useMemo`.
- **✅ DO:** Maintain pure functional components and let the compiler optimize the build.
- **✅ DO:** Use `useCallback` only when stability is required for specific dependencies (e.g., custom hooks).

### 4. Error Boundary

```tsx
class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Error caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

### 5. Form Handling Pattern

```tsx
// Controlled form with validation
function useForm<T extends Record<string, any>>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = (name: keyof T) => (
    e: ChangeEvent<HTMLInputElement>
  ) => {
    setValues(prev => ({ ...prev, [name]: e.target.value }));
  };

  const handleBlur = (name: keyof T) => () => {
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const validate = (validationFn: (values: T) => Partial<Record<keyof T, string>>) => {
    const newErrors = validationFn(values);
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  return { values, errors, touched, handleChange, handleBlur, validate, setValues };
}
```

## Best Practices

1. **Component Organization**: Keep components small and focused
2. **Type Safety**: Always use TypeScript interfaces for props
3. **Key Prop**: Always use stable, unique keys in lists
4. **Cleanup**: Clean up effects (subscriptions, timers)
5. **Error Handling**: Use error boundaries for graceful failures
6. **Accessibility**: Include ARIA labels and semantic HTML
