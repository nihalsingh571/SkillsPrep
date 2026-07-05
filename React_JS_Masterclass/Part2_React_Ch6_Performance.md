# Chapter 6: Performance Optimization

> **"React is fast out of the box. But as applications grow, poorly managed renders and massive bundle sizes will kill your framerate. Performance optimization is a senior-level requirement."**

---

## Table of Contents

1. [How React Renders (The Render Phase vs Commit Phase)](#rendering)
2. [When Does React Re-Render?](#when-rerender)
3. [React.memo()](#react-memo)
4. [useMemo() & useCallback() in Depth](#usememo-usecallback)
5. [Code Splitting & Lazy Loading (React.lazy)](#lazy-loading)
6. [Virtualization (Windowing) for Large Lists](#virtualization)
7. [Debouncing & Throttling in React](#debouncing)
8. [Optimizing Context API](#context-optimization)
9. [Bundle Size Optimization](#bundle-size)
10. [Core Web Vitals & Monitoring](#web-vitals)
11. [Chapter Summary & Interview Prep](#summary)

---

## 1. How React Renders (Render vs Commit) {#rendering}

A "Render" in React does NOT mean updating the DOM. 

1. **Render Phase:** React calls your functional component. It figures out what the UI *should* look like (creates a new Virtual DOM tree) and diffs it against the old one to find the changes. **This phase must be pure and fast.**
2. **Commit Phase:** React applies the calculated changes to the actual browser DOM (using APIs like `document.createElement`).

*Performance Rule #1:* React rendering is cheap. Committing to the real DOM is expensive. We want to avoid both if possible, but avoiding unnecessary Commit phases is the most critical.

---

## 2. When Does React Re-Render? {#when-rerender}

A component re-renders if:
1. Its **State** changes.
2. It consumes a **Context** that changed.
3. Its **Parent** re-renders! (This is the most common cause of wasted renders).

*Important:* React does NOT care if your `props` changed by default. If a parent re-renders, ALL its children re-render recursively, regardless of whether their props changed or not.

---

## 3. React.memo() {#react-memo}

`React.memo` is a Higher Order Component (HOC). It wraps a functional component and tells React: "Only re-render this child if its `props` have explicitly changed."

### Basic Usage

```javascript
import { memo, useState } from 'react';

// Wrap the component in memo()
const ExpensiveChild = memo(({ text }) => {
  console.log("ExpensiveChild rendered!");
  return <div>{text}</div>;
});

function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      
      {/* 
        Even though Parent re-renders when count changes, 
        ExpensiveChild will NOT re-render because its 'text' prop didn't change!
      */}
      <ExpensiveChild text="Hello" />
    </div>
  );
}
```

### The Referential Equality Problem (Why memo fails)

If you pass an **object, array, or function** as a prop, `React.memo` will fail to stop the re-render. Why? Because on every parent render, a *new* object/function reference is created in memory.

```javascript
function Parent() {
  const [count, setCount] = useState(0);
  
  // A NEW object reference is created on every render!
  const user = { name: "Alice" }; 
  
  // memo() sees: prevProps.user !== nextProps.user
  // It fails and re-renders the child anyway!
  return <ExpensiveChild user={user} />;
}
```
**The Fix:** Wrap the object in `useMemo`, or the function in `useCallback`.

---

## 4. useMemo() & useCallback() in Depth {#usememo-usecallback}

### When to use useMemo
1. To cache an expensive calculation (looping through 10,000 items).
2. To keep an object/array reference stable so it doesn't break `React.memo` on child components.
3. To keep a reference stable so it doesn't cause a `useEffect` infinite loop.

```javascript
// Stabilizing an object for a memoized child
const user = useMemo(() => ({ name: "Alice" }), []);
<ExpensiveChild user={user} />
```

### When to use useCallback
To keep a function reference stable so it doesn't break `React.memo` or trigger `useEffect`.

```javascript
// Stabilizing a function
const handleClick = useCallback(() => {
  console.log("Clicked");
}, []);
<ExpensiveChild onClick={handleClick} />
```

### When NOT to use them (The Cost of Memoization)
Memoization is not free. Creating the cache array, comparing dependencies, and storing the result takes memory and CPU time. 
*Do not wrap every function in `useCallback` or every component in `memo`.* Only use them on deeply nested trees, heavy calculations, or interactive graphs/tables.

---

## 5. Code Splitting & Lazy Loading (React.lazy) {#lazy-loading}

By default, bundlers like Webpack package your entire React app into one giant JavaScript file (e.g., `bundle.js`). If this file is 5MB, the user sees a blank screen for 10 seconds.

**Code Splitting** breaks the bundle into smaller chunks. 
**Lazy Loading** loads those chunks only when the user needs them.

### Route-Based Code Splitting

```javascript
import { Suspense, lazy } from 'react';
import { Routes, Route } from 'react-router-dom';

// 1. DO NOT import components normally
// import Dashboard from './Dashboard'; 

// 2. Import dynamically using React.lazy
const Home = lazy(() => import('./Home'));
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    // 3. Wrap Routes in Suspense to show a fallback UI while downloading the chunk
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* The Dashboard code is ONLY downloaded when the user visits /dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}
```

---

## 6. Virtualization (Windowing) for Large Lists {#virtualization}

If you render 10,000 rows in a table, the browser will create 10,000 DOM nodes. The DOM will grind to a halt.

**Virtualization** (or Windowing) only renders the DOM nodes that are currently visible on the screen (plus a few padding nodes). As the user scrolls, it reuses those same DOM nodes, swapping out the data.

Libraries to use: `react-window` or `react-virtualized`.

```javascript
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }) => (
  <div style={style}>Row {index}</div>
);

function HugeList() {
  return (
    // Renders 100,000 items, but only ~15 DOM nodes ever exist!
    <List
      height={400}
      itemCount={100000}
      itemSize={35}
      width={300}
    >
      {Row}
    </List>
  );
}
```

---

## 7. Debouncing & Throttling in React {#debouncing}

If you have a search input that fetches data, you don't want to make an API call on every keystroke. You must debounce it.

### The Pitfall: Defining debounce inside the component
If you use a standard `lodash.debounce` inside a component, it gets recreated on every render, losing its timer!

### The Solution: useCallback or Custom Hook

```javascript
import { useState, useCallback } from 'react';
import debounce from 'lodash.debounce';

function Search() {
  const [query, setQuery] = useState("");

  // 1. Wrap the debounced function in useCallback with empty dependencies
  const debouncedFetch = useCallback(
    debounce((searchTerm) => {
      fetchAPI(searchTerm);
    }, 500),
    [] // Keep reference stable forever
  );

  const handleChange = (e) => {
    const val = e.target.value;
    setQuery(val); // Update input UI instantly
    debouncedFetch(val); // Trigger debounced API call
  };

  return <input value={query} onChange={handleChange} />;
}
```

---

## 8. Optimizing Context API {#context-optimization}

Context is notorious for causing massive render cascades.

**Problem:**
```javascript
<AppContext.Provider value={{ user, theme, toggleTheme }}>
```
If `user` changes, ANY component using `useContext(AppContext)` will re-render, even if they only needed the `theme`.

**Solutions:**
1. **Split Contexts:** Create separate `UserContext` and `ThemeContext`.
2. **Memoize the Provider Value:**
```javascript
const value = useMemo(() => ({ user, theme }), [user, theme]);
<AppContext.Provider value={value}>
```
3. **Push State Down:** Don't use Context if passing props one level down works.
4. **Use Zustand/Redux:** They solve this using Selectors.

---

## 9. Bundle Size Optimization {#bundle-size}

How to keep your JavaScript payload small:
1. **Analyze your bundle:** Use `source-map-explorer` or `webpack-bundle-analyzer` to see what dependencies are taking up space.
2. **Import specifically:** 
   - BAD: `import { omit } from 'lodash';` (Might bundle all of lodash)
   - GOOD: `import omit from 'lodash/omit';`
3. **Remove Moment.js:** It is gigantic and not tree-shakeable. Use `date-fns` or `dayjs` instead.
4. **Tree Shaking:** Ensure you are using ES modules (`import/export`) so Vite/Webpack can remove dead code.

---

## 10. Core Web Vitals & Monitoring {#web-vitals}

Google ranks websites based on three Core Web Vitals:
1. **LCP (Largest Contentful Paint):** How long until the main content loads? (Optimize: Server-Side Rendering, Image optimization, lazy loading below-fold).
2. **FID (First Input Delay) / INP (Interaction to Next Paint):** How fast does the site respond when clicked? (Optimize: Break up long JS tasks, use `useTransition`).
3. **CLS (Cumulative Layout Shift):** Does the UI jump around while loading? (Optimize: Give images explicit height/width, use Skeleton loaders).

---

## 11. Chapter Summary & Interview Prep {#summary}

### Top 25 Interview Questions

**Q1. What causes a component to re-render in React?**
*Answer:* 1) Local state change via useState/useReducer. 2) A change in consumed Context. 3) The component's parent re-renders. (Note: Props changing is technically a symptom of the parent re-rendering, not the primary cause).

**Q2. How does React.memo work and when should you use it?**
*Answer:* It's a HOC that prevents a component from re-rendering if its props haven't changed (uses shallow equality check). Use it on heavy, complex child components, or when a component renders frequently with the same props.

**Q3. Why is it bad to use inline object/function props on a memoized component?**
*Answer:* `style={{ color: 'red' }}` creates a new object reference in memory on every render. `React.memo` will see `prevProps.style !== nextProps.style` and re-render the component anyway, defeating the purpose of memo. You must wrap the object in `useMemo` or function in `useCallback`.

**Q4. What is Code Splitting?**
*Answer:* Breaking the final JavaScript bundle into smaller chunks that are loaded on demand (Lazy Loading). We achieve this in React using `React.lazy()` and `<Suspense>`, typically splitting by Route. It drastically improves initial load time (LCP).

**Q5. How do you render a list of 10,000 items without freezing the browser?**
*Answer:* Use Windowing/Virtualization (e.g., `react-window`). It only renders the DOM nodes visible in the viewport and recycles them as the user scrolls, keeping DOM nodes low and memory usage stable.

**Q6. What is the difference between useMemo and useCallback?**
*Answer:* `useMemo` caches the *result* of a function. `useCallback` caches the *function definition itself*.

**Q7. Explain the difference between Render phase and Commit phase.**
*Answer:* Render phase is React calling components to figure out what the UI should look like (VDOM diffing). It is pure and interruptible in React 18. Commit phase is React actually applying those changes to the real browser DOM.

**Q8. Why use `date-fns` instead of `moment.js`?**
*Answer:* `moment.js` is heavily object-oriented and mutable, meaning it cannot be tree-shaken by modern bundlers resulting in massive bundle sizes. `date-fns` uses pure functions, allowing bundlers to only include the specific functions you import.

**Q9. How do you implement debounce for a search input in React?**
*Answer:* You cannot simply define `debounce` inside the render body, as it will be recreated. You must wrap the debounced function in `useCallback` with an empty dependency array, or use a custom `useDebounce` hook.

**Q10. What are Core Web Vitals?**
*Answer:* Google's performance metrics: LCP (Largest Contentful Paint - load speed), INP/FID (Interaction to Next Paint - interactivity speed), and CLS (Cumulative Layout Shift - visual stability).

---

## 5 Output Prediction Exercises

**Exercise 1**
```javascript
const Child = React.memo(({ onClick }) => console.log("Child Rendered"));
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Update</button>
      <Child onClick={() => console.log('Click')} />
    </>
  );
}
// User clicks "Update". Does Child render?
```
*Answer:* Yes. `() => console.log('Click')` creates a new function reference every render, breaking the memoization.

**Exercise 2**
```javascript
const Child = React.memo(({ data }) => console.log("Child Rendered"));
function Parent() {
  const [count, setCount] = useState(0);
  const data = useMemo(() => [1, 2, 3], []);
  return <Child data={data} />;
}
// Count state updates. Does Child render?
```
*Answer:* No. `useMemo` keeps the array reference stable.

**Exercise 3**
```javascript
function List({ items }) {
  return items.map((item, index) => <div key={index}>{item.name}</div>);
}
// Why is using index as key a performance/bug risk here?
```
*Answer:* If items are added, removed, or reordered at the start/middle of the array, the indexes shift. React will misidentify which items changed, causing complete re-renders of the DOM nodes instead of moving them, and can map the wrong local state to the wrong item.

**Exercise 4**
```javascript
const expensive = useMemo(() => {
  console.log("Calculating...");
  return 100 * 100;
});
// Notice anything missing?
```
*Answer:* There is no dependency array! `useMemo` without an array recalculates on EVERY render, defeating its purpose. It should be `useMemo(..., [])`.

**Exercise 5**
```javascript
import Dashboard from './Dashboard';
// Later in JSX:
<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
// Will Dashboard be code-split?
```
*Answer:* No. Because it was statically imported at the top, it is bundled into the main chunk. It must be imported using `const Dashboard = React.lazy(() => import('./Dashboard'))`.

---
*End of Chapter 6 — Performance Optimization.*
