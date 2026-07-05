# Chapter 3: React Hooks — The Complete Guide

> **"Hooks completely changed how we write React. Mastering Hooks means understanding the React rendering cycle, closures, and side effects. This is the most important chapter for any React interview."**

---

## Table of Contents

1. [Introduction to Hooks](#intro)
2. [useState](#usestate)
3. [useEffect](#useeffect)
4. [useRef](#useref)
5. [useMemo](#usememo)
6. [useCallback](#usecallback)
7. [useContext](#usecontext)
8. [useReducer](#usereducer)
9. [Custom Hooks](#custom-hooks)
10. [useLayoutEffect](#uselayouteffect)
11. [React 18 Hooks Overview](#react-18-hooks)
12. [Hook Internals (How they work under the hood)](#hook-internals)
13. [Chapter Summary & Interview Prep](#summary)

---

## 1. Introduction to Hooks {#intro}

### What are Hooks?
Introduced in React 16.8 (2019), Hooks are functions that let you "hook into" React state and lifecycle features from **functional components**. Before hooks, state and lifecycles were only available in Class components.

### Why were Hooks created?
1. **Wrapper Hell:** Patterns like Higher-Order Components (HOCs) and Render Props created deeply nested component trees.
2. **Giant Components:** Class `componentDidMount` and `componentDidUpdate` often contained mixed, unrelated logic (fetching data + setting up event listeners). Hooks let you split logic based on *what it does* rather than lifecycle methods.
3. **Confusing Classes:** `this` in JavaScript is confusing. Classes don't minify well and make hot reloading flaky.

### The Two Rules of Hooks
1. **Only call Hooks at the top level.** Don't call them inside loops, conditions, or nested functions.
2. **Only call Hooks from React function components** (or custom hooks).

*Why?* React relies on the **order** in which Hooks are called to associate state with the correct `useState` call. If a hook is inside an `if` statement, the order might change between renders, breaking the app!

---

## 2. useState {#usestate}

### What is it?
Allows you to add state variables to functional components. State represents data that changes over time and should cause the UI to re-render when updated.

### Syntax
```javascript
const [state, setState] = useState(initialState);
```

### Basic Example
```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

### Deep Dive: State is a Snapshot!
When React renders a component, it calls your function. The `count` variable inside that specific render is a constant. Setting state does *not* change the existing variable; it triggers a *new render* with a new value.

```javascript
function SnapshotDemo() {
  const [number, setNumber] = useState(0);

  const handleClick = () => {
    setNumber(number + 1);
    setNumber(number + 1);
    setNumber(number + 1);
    // WHAT HAPPENS? The number will only increase by 1!
    // Because in THIS render, 'number' is 0. 
    // It evaluates to: setNumber(0+1), setNumber(0+1), setNumber(0+1).
  };
}
```

### Functional Update Form (Solving the Snapshot Problem)
If your new state depends on the previous state, pass a **callback function** to the setter.

```javascript
  const handleClickFix = () => {
    setNumber(prev => prev + 1);
    setNumber(prev => prev + 1);
    setNumber(prev => prev + 1);
    // Increases by 3! React queues these updates.
  };
```

### Lazy Initialization
If your initial state requires an expensive computation, pass a *function* to `useState`. It will only execute on the *first* render.

```javascript
// BAD: Runs on EVERY render
const [data, setData] = useState(heavyComputation()); 

// GOOD: Runs ONLY on initial mount
const [data, setData] = useState(() => heavyComputation()); 
```

### Working with Objects and Arrays
**Rule:** NEVER mutate state directly! Always create a new object/array.

```javascript
const [user, setUser] = useState({ name: "Alice", age: 25 });

// BAD MUTATION (React won't re-render!):
// user.age = 26; setUser(user);

// GOOD (Spread operator):
setUser(prevUser => ({ ...prevUser, age: 26 }));

// ARRAYS:
const [items, setItems] = useState([1, 2]);
// Add: setItems([...items, 3]);
// Remove: setItems(items.filter(i => i !== 2));
```

### Batching (React 18)
In React 18, all state updates inside a single event handler (even inside async timeouts or promises) are **batched** together into a single re-render for performance.

---

## 3. useEffect {#useeffect}

### What is it?
Lets you perform **side effects** in function components. Side effects are anything that interacts with the outside world: fetching data, manually mutating the DOM, setting up subscriptions, or timers.

### Syntax
```javascript
useEffect(() => {
  // 1. Setup code (the effect)
  
  return () => {
    // 2. Cleanup code (optional)
  };
}, [dependencyArray]); // 3. When to run
```

### The 3 Forms of useEffect

**1. No dependency array:** Runs after EVERY render. (Dangerous, often leads to infinite loops).
```javascript
useEffect(() => {
  console.log("I run after every render!");
});
```

**2. Empty array `[]`:** Runs exactly ONCE after the initial render (Mounting).
```javascript
useEffect(() => {
  console.log("I run once when component mounts.");
}, []);
```

**3. Array with dependencies `[x, y]`:** Runs on mount, AND whenever `x` or `y` changes.
```javascript
useEffect(() => {
  document.title = `Clicked ${count} times`;
}, [count]); // Only re-runs if 'count' changes
```

### The Cleanup Function (Unmounting & Re-running)
If your effect creates subscriptions or timers, you MUST clean them up to prevent memory leaks. The cleanup function runs:
1. Before the component unmounts.
2. *Before the effect runs again* (on subsequent re-renders).

```javascript
useEffect(() => {
  const timer = setInterval(() => console.log('Tick'), 1000);
  
  // Cleanup:
  return () => clearInterval(timer);
}, []);
```

### Strict Mode Double-Effect (React 18)
In development, React 18 mounts, unmounts, and re-mounts components to help you find bugs in your cleanup logic. If you see APIs fetching twice, it's Strict Mode doing its job! Don't turn it off; ensure your cleanup logic handles it.

### Fetching Data inside useEffect (Race Conditions)
When fetching data, network responses can arrive out of order. We must handle this using an `AbortController` or a cleanup boolean flag.

```javascript
useEffect(() => {
  const controller = new AbortController();
  
  async function fetchData() {
    try {
      const response = await fetch(`/api/user/${userId}`, { signal: controller.signal });
      const data = await response.json();
      setUser(data);
    } catch (err) {
      if (err.name !== 'AbortError') console.error(err);
    }
  }
  
  fetchData();
  
  // Cleanup: If userId changes before fetch finishes, abort the old request!
  return () => controller.abort();
}, [userId]);
```

### Infinite Loop Pitfall (Objects/Arrays in Dependencies)
```javascript
function BadComponent() {
  const [data, setData] = useState([]);
  
  // A new object is created on EVERY render!
  const options = { active: true }; 
  
  useEffect(() => {
    fetchData(options); // Uses options
  }, [options]); // Because 'options' is a new reference every render, this loops infinitely!
}
```
**Fix:** Move `options` outside the component, or memoize it with `useMemo`.

---

## 4. useRef {#useref}

### What is it?
`useRef` is a "box" that can hold a mutable value. Crucially, **changing a ref does NOT trigger a re-render** (unlike state).

### Use Case 1: Accessing DOM Elements
```javascript
function TextInputWithFocusButton() {
  const inputEl = useRef(null);

  const onButtonClick = () => {
    // Access the actual DOM node
    inputEl.current.focus(); 
  };

  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}
```

### Use Case 2: Storing Mutable Values (Instance variables)
Need to keep track of a timer ID or a previous value without causing the screen to flash/re-render? Use a ref.

```javascript
function Timer() {
  const [count, setCount] = useState(0);
  const timerId = useRef(null);

  const start = () => {
    timerId.current = setInterval(() => setCount(c => c + 1), 1000);
  };

  const stop = () => {
    clearInterval(timerId.current);
  };

  return <button onClick={start}>Start</button>;
}
```

### State vs Ref Summary
| | `useState` | `useRef` |
|---|---|---|
| Mutability | Immutable (use setter) | Mutable (`.current = value`) |
| Re-render | **Triggers** a re-render | Does **NOT** trigger re-render |
| Usage | UI Data | DOM nodes, Timers, Interval IDs |

---

## 5. useMemo {#usememo}

### What is it?
Memoizes (caches) the **result of a calculation** between renders. It only recalculates when its dependencies change.

### Syntax
```javascript
const cachedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

### Why use it? (Performance Optimization)
React components re-render often. If you have a loop that processes 10,000 items, you don't want to run that loop on every keystroke in a unrelated text input.

```javascript
function Dashboard({ users, filterText }) {
  // Only re-filters if 'users' array or 'filterText' changes.
  // Typing in a completely unrelated input won't trigger this heavy calculation.
  const filteredUsers = useMemo(() => {
    console.log("Filtering users..."); // Heavy logic
    return users.filter(u => u.name.includes(filterText));
  }, [users, filterText]);
  
  return <div>...</div>;
}
```

### Reference Stability (The Hidden Superpower)
`useMemo` is also used to keep object/array references stable to prevent `useEffect` infinite loops or to prevent `React.memo` child components from needlessly re-rendering.

---

## 6. useCallback {#usecallback}

### What is it?
Memoizes a **function definition** between renders. (It is literally just `useMemo` but specifically for functions).

### Why do we need it?
In React, whenever a component re-renders, every function inside it is recreated (a new memory address). If you pass these functions as props to child components, the child will think the prop changed and re-render unnecessarily!

```javascript
// A child component wrapped in React.memo (only re-renders if props change)
const Child = React.memo(({ onClick }) => {
  console.log("Child rendered!");
  return <button onClick={onClick}>Click Me</button>;
});

function Parent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // BAD: New function created on every render. Child will re-render when 'text' changes!
  // const handleClick = () => setCount(c => c + 1);

  // GOOD: Function reference is cached. Child will NOT re-render when 'text' changes!
  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <Child onClick={handleClick} />
    </div>
  );
}
```
*Note: Do NOT use `useCallback` everywhere. It has a performance cost. Only use it when passing functions to optimized child components (`React.memo`) or when a function is a dependency in a `useEffect`.*

---

## 7. useContext {#usecontext}

### What is it?
Allows you to read and subscribe to context from your component. It solves **Prop Drilling** (passing props down 5 levels of components just to get data to the bottom).

### Implementation Steps
1. Create Context (`createContext`)
2. Wrap App in Provider (`<Context.Provider value={...}>`)
3. Consume Context (`useContext(Context)`)

```javascript
// 1. Create
const ThemeContext = createContext('light');

function App() {
  // 2. Provide
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  return <ThemedButton />;
}

function ThemedButton() {
  // 3. Consume (No prop drilling!)
  const theme = useContext(ThemeContext);
  return <button className={theme}>I am styled by context!</button>;
}
```

### The Performance Gotcha!
When a Provider's `value` changes, **EVERY single component that calls `useContext` will re-render**, regardless of `React.memo`. 
*Optimization:* If context holds `{ user, theme }`, and `theme` changes, components only using `user` will still re-render. Split contexts into `UserContext` and `ThemeContext`!

---

## 8. useReducer {#usereducer}

### What is it?
An alternative to `useState` for managing complex state logic that involves multiple sub-values or when the next state depends on the previous one. (It works exactly like Redux).

### Syntax
```javascript
const [state, dispatch] = useReducer(reducer, initialState);
```

### Complete Example
```javascript
const initialState = { count: 0 };

// Reducer: pure function that takes (state, action) and returns new state
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return { count: 0 };
    default:
      throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </>
  );
}
```
*Why use it?* It centralizes state logic. Instead of calling `setLoading`, `setData`, and `setError` separately, you dispatch one action: `dispatch({ type: 'FETCH_SUCCESS', payload: data })`.

---

## 9. Custom Hooks {#custom-hooks}

### What are they?
You can extract component logic into reusable functions. Custom hooks MUST start with the word `use` (so React's linter knows to enforce the Rules of Hooks inside them).

### Example: `useLocalStorage`

```javascript
import { useState, useEffect } from "react";

function useLocalStorage(key, initialValue) {
  // Lazy init state from localStorage
  const [value, setValue] = useState(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  // Update localStorage when state changes
  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue]; // Return tuple like useState
}

// Usage in any component:
// const [name, setName] = useLocalStorage("username", "Guest");
```

---

## 10. useLayoutEffect {#uselayouteffect}

### Difference from useEffect
- `useEffect`: Runs **asynchronously** AFTER the browser paints the screen. (Good for 99% of cases).
- `useLayoutEffect`: Runs **synchronously** immediately after DOM mutations, but BEFORE the browser paints.

### When to use it?
Only use it when you need to read DOM measurements (like scroll position, or element width) and instantly mutate the DOM based on that measurement, *before* the user sees it. If you use `useEffect` for this, the user will see a visible "flicker" as the screen paints, then quickly re-paints.

---

## 11. React 18 Hooks Overview {#react-18-hooks}

- **useTransition:** Lets you mark state updates as "non-urgent" (transitions). Keeps the UI responsive during heavy renders.
  ```javascript
  const [isPending, startTransition] = useTransition();
  startTransition(() => {
    setSearchQuery(input); // Marked as low-priority
  });
  ```
- **useDeferredValue:** Lets you defer updating a part of the UI.
- **useId:** Generates unique IDs for accessibility attributes (stable across server and client rendering).

---

## 12. Hook Internals (How they work) {#hook-internals}

### The Linked List
How does React know which state belongs to which `useState` call when there are 5 of them in a component?
React stores Hooks as a **Linked List** attached to the component's internal Fiber node. 

1. First render: React pushes hooks onto the list.
2. Next renders: React traverses the list in the exact same order.

If you put a hook in an `if` statement, and that `if` evaluates to `false` on the second render, React will pull the *wrong* hook state from the linked list for all subsequent hooks. **This is why the Rules of Hooks exist!**

---

## 13. Chapter Summary & Interview Prep {#summary}

### Cheat Sheet
- **useState:** UI State. Use functional updates if relying on previous state.
- **useEffect:** Side effects. `[]` = mount only. Return function = cleanup.
- **useRef:** Mutable box that bypasses renders. Good for DOM nodes & timers.
- **useMemo:** Caches computed values.
- **useCallback:** Caches function definitions.
- **useContext:** Avoids prop drilling.
- **useReducer:** Complex state logic management.

### Top 25 Interview Questions

**Q1. What are the Rules of Hooks?**
*Answer:* Only call hooks at the top level (never in loops, conditions, or nested functions). Only call hooks from React function components or custom hooks.

**Q2. Explain the stale closure problem in useEffect.**
*Answer:* If an effect uses a state variable but doesn't include it in the dependency array, the effect is "trapped" in the closure of the render where it was created, seeing the old state forever. Fix by adding it to dependencies, or using the functional update form of `useState`.

**Q3. When should you use useMemo and useCallback?**
*Answer:* Do not use them blindly. Use `useMemo` for computationally expensive operations, or to maintain referential equality of objects/arrays passed as dependencies. Use `useCallback` when passing functions to highly optimized child components (like those wrapped in `React.memo`) to prevent unnecessary child re-renders.

**Q4. What is the difference between useEffect and useLayoutEffect?**
*Answer:* `useEffect` runs asynchronously after the browser paints, meaning it won't block the visual update. `useLayoutEffect` runs synchronously after DOM mutations but before the paint. Use it only when measuring DOM elements to prevent visual flickering.

**Q5. Why do we need a cleanup function in useEffect?**
*Answer:* To prevent memory leaks. If you set up an event listener, a WebSocket, or a setInterval on mount, you must clean them up when the component unmounts. Cleanup also runs before the effect re-runs on updates.

**Q6. Can you force a component to re-render without changing state?**
*Answer:* While anti-pattern, you can by updating a dummy state variable. e.g., `const [, forceRender] = useState(0); forceRender(x => x + 1);`

**Q7. How does React handle multiple setState calls in the same function?**
*Answer:* In React 18, it automatically batches them. If you call `setA(1)`, `setB(2)`, `setC(3)` in an event handler, React will only trigger ONE re-render, improving performance.

**Q8. What happens if you update state with the exact same value?**
*Answer:* React uses `Object.is` to compare. If it's the exact same primitive value, or the exact same object reference, React will bail out and NOT re-render the component.

**Q9. How do you fetch data with hooks and handle race conditions?**
*Answer:* Fetch in a `useEffect`. Handle race conditions by creating a local boolean variable (`let isMounted = true`) and checking it before calling setState in the `.then`, OR better, use the native `AbortController` API and call `.abort()` in the useEffect cleanup function.

**Q10. How does useContext impact performance?**
*Answer:* Any component that calls `useContext` will re-render whenever the Provider's value changes. If the value is an object `value={{a, b}}`, and only `a` changes, a component consuming only `b` will STILL re-render. You must split contexts or memoize the provider value to optimize.

---

## 5 Output Prediction Exercises

**Exercise 1**
```javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  const handleTriple = () => {
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
  };
  // User clicks once. What is the new count?
}
```
*Answer:* `1`. State is a snapshot. In that render cycle, `count` is 0.

**Exercise 2**
```javascript
useEffect(() => {
  console.log("A");
  return () => console.log("B");
}, [count]);
// Component mounts, then count changes once. What is logged?
```
*Answer:* Mounts: `A`. Count changes: `B` (cleanup of old), `A` (new effect).

**Exercise 3**
```javascript
const obj1 = { id: 1 };
const [data, setData] = useState(obj1);
setData(obj1); // Will the component re-render?
```
*Answer:* No. React uses `Object.is`. The reference is identical.

**Exercise 4**
```javascript
const renderCount = useRef(0);
renderCount.current++;
console.log(renderCount.current);
// Will updating the ref cause a re-render?
```
*Answer:* No. Mutations to `ref.current` never trigger a re-render.

**Exercise 5**
```javascript
useEffect(() => {
  setInterval(() => console.log(count), 1000);
}, []); // Empty deps
// Count updates to 5. What does the interval log?
```
*Answer:* It logs `0` forever (stale closure).

---
*End of Chapter 3 — Hooks are the heart of modern React.*
