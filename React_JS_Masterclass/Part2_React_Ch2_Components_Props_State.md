# Part 2 — React.js Mastery
# Chapter 2: Components, Props, State & Rendering

> **"Components let you split the UI into independent, reusable pieces, and think about each piece in isolation."** — React Docs

---

## Table of Contents

1. Functional Components
2. Class Components & All Lifecycle Methods
3. Props — Complete Guide
4. State — useState Complete Guide
5. Rendering in React — When and Why
6. Conditional Rendering
7. Lists and Keys
8. Fragments
9. Portals
10. Refs
11. Forms — Controlled vs Uncontrolled
12. Chapter Summary
13. Top 25 Interview Questions
14. Output/Render Exercises
15. Coding Exercises
16. MCQs

---

# 1. Functional Components

## 1.1 — What is a Functional Component?

A **Functional Component** is a JavaScript **function** that:
1. Accepts a single argument — **props** (an object)
2. Returns **React elements** (JSX) or `null`

That's it. That's all a functional component is — a function.

```jsx
// MINIMUM valid functional component:
function Hello() {
  return <h1>Hello, World!</h1>;
}

// Arrow function form (equally valid):
const Hello = () => <h1>Hello, World!</h1>;

// With props:
function Greeting(props) {
  return <h1>Hello, {props.name}!</h1>;
}

// With destructured props (preferred):
function Greeting({ name, age }) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
    </div>
  );
}
```

---

## 1.2 — Returning JSX vs null

```jsx
// Returning JSX — renders UI
function Banner({ message }) {
  return (
    <div className="banner">
      <p>{message}</p>
    </div>
  );
}

// Returning null — renders NOTHING (no DOM node, no error)
function ConditionalBanner({ show, message }) {
  if (!show) return null; // Completely removes from DOM
  return (
    <div className="banner">
      <p>{message}</p>
    </div>
  );
}

// Returning false, undefined — also renders nothing
// But returning null is the idiomatic way to render nothing
```

---

## 1.3 — Component Identity and When React "Calls" Your Function

React calls your function component on every re-render. The component is re-called when:
- Its own state changes (via `useState` or `useReducer`)
- Its parent re-renders (even if props didn't change, unless memoized)
- Context it subscribes to changes

```jsx
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Click: {count}</button>
      <Child />  {/* Child re-renders every time Parent re-renders! */}
    </div>
  );
}

function Child() {
  console.log('Child rendered!'); // Logs on every parent render
  return <p>I am a child</p>;
}
// Solution: React.memo(Child) to skip re-render if props unchanged
```

---

## 1.4 — Component Identity Rules

```jsx
// ✅ RULE 1: Component name MUST start with uppercase
function userCard() { ... }  // ❌ treated as HTML element
function UserCard() { ... }  // ✅ treated as React component

// ✅ RULE 2: Components must be PURE (same input → same output)
// ❌ IMPURE — reads external mutable variable
let globalCount = 0;
function Counter() {
  globalCount++; // Side effect in render!
  return <div>{globalCount}</div>;
}

// ✅ PURE — same props always → same JSX
function Counter({ count }) {
  return <div>{count}</div>;
}

// ✅ RULE 3: Components cannot call other components as functions
// ❌ WRONG — treats UserCard as a plain function call
function App() {
  return UserCard({ name: 'Alice' }); // Bypasses React's component system!
}

// ✅ CORRECT — use JSX syntax
function App() {
  return <UserCard name="Alice" />; // React manages the component
}
```

---

# 2. Class Components

## 2.1 — What is a Class Component?

Before Hooks (React 16.8, February 2019), class components were the ONLY way to have state and lifecycle methods in React.

```jsx
import React, { Component } from 'react';

class Counter extends Component {
  // Constructor: called once when component is created
  constructor(props) {
    super(props); // MUST call super(props) first!
    // Initialize state
    this.state = {
      count: 0,
    };
    // Bind event handlers (old way — before class fields)
    this.handleIncrement = this.handleIncrement.bind(this);
  }

  // Event handler method
  handleIncrement() {
    this.setState({ count: this.state.count + 1 });
  }

  // The render method — returns JSX (equivalent to function component body)
  render() {
    return (
      <div>
        <h1>Count: {this.state.count}</h1>
        <p>Name: {this.props.name}</p>
        <button onClick={this.handleIncrement}>Increment</button>
      </div>
    );
  }
}

// Modern class component (class fields — no bind needed):
class Counter extends Component {
  state = { count: 0 }; // Class field (no constructor needed)

  // Arrow function as class field — auto-bound to instance
  handleIncrement = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <h1>Count: {this.state.count}</h1>
        <button onClick={this.handleIncrement}>Increment</button>
      </div>
    );
  }
}

export default Counter;
```

---

## 2.2 — this.setState — The Async Nature

`this.setState` is **asynchronous** — it does NOT immediately update `this.state`.

```jsx
class BugDemo extends Component {
  state = { count: 0 };

  handleClick = () => {
    // ❌ BUG: Reading state immediately after setState
    this.setState({ count: this.state.count + 1 });
    console.log(this.state.count); // Still 0! setState is async

    // ❌ BUG: Multiple setState calls with same state reference
    this.setState({ count: this.state.count + 1 }); // count = 0 + 1 = 1
    this.setState({ count: this.state.count + 1 }); // count = 0 + 1 = 1 (still reads old state!)
    this.setState({ count: this.state.count + 1 }); // count = 0 + 1 = 1
    // Result: count = 1, not 3!

    // ✅ FIX: Use functional form of setState
    this.setState(prevState => ({ count: prevState.count + 1 }));
    this.setState(prevState => ({ count: prevState.count + 1 }));
    this.setState(prevState => ({ count: prevState.count + 1 }));
    // Result: count = 3 ✅

    // ✅ Reading state after update: use setState callback
    this.setState({ count: this.state.count + 1 }, () => {
      console.log(this.state.count); // Now shows updated value
    });
  };

  render() {
    return <button onClick={this.handleClick}>{this.state.count}</button>;
  }
}
```

---

## 2.3 — All Lifecycle Methods — Complete Reference

```
┌────────────────────────────────────────────────────────────────────────┐
│                 CLASS COMPONENT LIFECYCLE                              │
│                                                                        │
│  ┌─────────────────── MOUNTING ──────────────────────┐                 │
│  │                                                   │                 │
│  │  constructor(props)                               │                 │
│  │       ↓                                           │                 │
│  │  static getDerivedStateFromProps(props, state)    │                 │
│  │       ↓                                           │                 │
│  │  render()                                         │                 │
│  │       ↓                                           │                 │
│  │  [DOM updates]                                    │                 │
│  │       ↓                                           │                 │
│  │  componentDidMount()  ← side effects here         │                 │
│  └───────────────────────────────────────────────────┘                 │
│                                                                        │
│  ┌─────────────────── UPDATING ──────────────────────┐                 │
│  │                                                   │                 │
│  │  static getDerivedStateFromProps(props, state)    │                 │
│  │       ↓                                           │                 │
│  │  shouldComponentUpdate(nextProps, nextState)      │                 │
│  │    → return false to SKIP re-render               │                 │
│  │       ↓ (if true)                                 │                 │
│  │  render()                                         │                 │
│  │       ↓                                           │                 │
│  │  getSnapshotBeforeUpdate(prevProps, prevState)    │                 │
│  │       ↓                                           │                 │
│  │  [DOM updates]                                    │                 │
│  │       ↓                                           │                 │
│  │  componentDidUpdate(prevProps, prevState, snap)   │                 │
│  └───────────────────────────────────────────────────┘                 │
│                                                                        │
│  ┌─────────────────── UNMOUNTING ────────────────────┐                 │
│  │                                                   │                 │
│  │  componentWillUnmount()  ← cleanup here           │                 │
│  └───────────────────────────────────────────────────┘                 │
│                                                                        │
│  ┌─────────────────── ERROR BOUNDARY ────────────────┐                 │
│  │                                                   │                 │
│  │  static getDerivedStateFromError(error)           │                 │
│  │  componentDidCatch(error, info)                   │                 │
│  └───────────────────────────────────────────────────┘                 │
└────────────────────────────────────────────────────────────────────────┘
```

### constructor(props)

```jsx
class MyComponent extends Component {
  constructor(props) {
    super(props);  // MUST call this first — sets up this.props
    // Initialize state here
    this.state = {
      count: props.initialCount || 0, // Can use props to init state
    };
    // Bind methods (old pattern)
    this.handleClick = this.handleClick.bind(this);
  }
}
// When to use constructor:
// - Initializing state
// - Binding event handlers (without class fields)
// - Creating refs (this.myRef = React.createRef())
// NOT for: side effects, subscriptions (use componentDidMount)
```

### static getDerivedStateFromProps(props, state)

```jsx
class AnimatedComponent extends Component {
  state = { prevColor: null, animating: false };

  // Called on EVERY render (both mount and update)
  // Returns: object to merge into state, OR null to update nothing
  static getDerivedStateFromProps(nextProps, prevState) {
    // When color prop changes, trigger animation
    if (nextProps.color !== prevState.prevColor) {
      return {
        prevColor: nextProps.color,
        animating: true, // Start animation
      };
    }
    return null; // No state update
  }
  // ⚠️ Rarely needed. Usually better to derive values in render.
  // ⚠️ Cannot access 'this' (it's static)
  // ⚠️ Called even when parent re-renders with same props
}
```

### render()

```jsx
class MyComponent extends Component {
  render() {
    // MUST be a pure function!
    // - Don't call setState() here
    // - Don't make HTTP requests here
    // - Don't start subscriptions here
    // ONLY return JSX (or null, string, number, array, fragment, portal)
    return (
      <div>
        <h1>{this.props.title}</h1>
        <p>{this.state.count}</p>
      </div>
    );
  }
}
```

### componentDidMount()

```jsx
class DataFetcher extends Component {
  state = { data: null, loading: true, error: null };

  componentDidMount() {
    // Called ONCE after component is first mounted to DOM
    // Perfect for:
    // - API calls / data fetching
    // - Setting up subscriptions
    // - Initializing third-party libraries (charts, maps)
    // - Setting up timers

    fetch('/api/data')
      .then(res => res.json())
      .then(data => this.setState({ data, loading: false }))
      .catch(err => this.setState({ error: err.message, loading: false }));

    // Example: subscribe to a data stream
    this.subscription = dataStream.subscribe(data => {
      this.setState({ data });
    });
  }

  componentWillUnmount() {
    // Always clean up what you set up in componentDidMount!
    this.subscription.unsubscribe(); // Prevent memory leak
  }

  render() {
    if (this.state.loading) return <Spinner />;
    if (this.state.error) return <ErrorMessage msg={this.state.error} />;
    return <DataDisplay data={this.state.data} />;
  }
}
```

### shouldComponentUpdate(nextProps, nextState)

```jsx
class OptimizedComponent extends Component {
  state = { count: 0, name: 'Alice' };

  shouldComponentUpdate(nextProps, nextState) {
    // Return true → allow re-render
    // Return false → SKIP re-render (performance optimization)

    // Only re-render if count changed (ignore name changes)
    if (nextState.count !== this.state.count) return true;
    if (nextProps.title !== this.props.title) return true;
    return false; // Don't re-render

    // Equivalent to: React.PureComponent (shallow comparison)
    // Or: React.memo() for functional components
  }

  render() {
    return <div>{this.state.count}</div>;
  }
}
```

### getSnapshotBeforeUpdate(prevProps, prevState)

```jsx
class ScrollingList extends Component {
  listRef = React.createRef();

  getSnapshotBeforeUpdate(prevProps, prevState) {
    // Called RIGHT BEFORE DOM is updated
    // Return value is passed as 3rd arg to componentDidUpdate
    // USE CASE: capture scroll position before re-render
    if (prevProps.messages.length < this.props.messages.length) {
      const list = this.listRef.current;
      return list.scrollHeight - list.scrollTop; // Capture scroll info
    }
    return null;
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    // 'snapshot' = return value of getSnapshotBeforeUpdate
    if (snapshot !== null) {
      const list = this.listRef.current;
      list.scrollTop = list.scrollHeight - snapshot; // Restore scroll
    }
  }

  render() {
    return (
      <div ref={this.listRef} style={{ height: '400px', overflow: 'auto' }}>
        {this.props.messages.map(msg => <div key={msg.id}>{msg.text}</div>)}
      </div>
    );
  }
}
```

### componentDidUpdate(prevProps, prevState, snapshot)

```jsx
class SearchComponent extends Component {
  state = { results: [] };

  componentDidUpdate(prevProps, prevState, snapshot) {
    // Called after every update EXCEPT initial mount
    // ALWAYS compare with previous values to avoid infinite loop!

    if (prevProps.searchTerm !== this.props.searchTerm) {
      // searchTerm prop changed → fetch new results
      fetch(`/api/search?q=${this.props.searchTerm}`)
        .then(res => res.json())
        .then(results => this.setState({ results }));
    }
    // ⚠️ WARNING: If you call setState without a condition,
    // you will cause an infinite loop:
    // setState → re-render → componentDidUpdate → setState → ...
  }

  render() {
    return <ResultsList results={this.state.results} />;
  }
}
```

### componentWillUnmount()

```jsx
class TimerComponent extends Component {
  componentDidMount() {
    // Set up timer
    this.timerID = setInterval(() => {
      this.setState(state => ({ seconds: state.seconds + 1 }));
    }, 1000);
  }

  componentWillUnmount() {
    // ALWAYS clean up!
    clearInterval(this.timerID);  // Prevent memory leak

    // Other cleanup examples:
    // this.subscription.unsubscribe();
    // this.abortController.abort();
    // document.removeEventListener('keydown', this.handleKeyDown);
    // this.socket.close();
  }

  render() {
    return <div>Seconds: {this.state.seconds}</div>;
  }
}
```

### componentDidCatch(error, info) — Error Boundaries

```jsx
class ErrorBoundary extends Component {
  state = { hasError: false, error: null };

  // getDerivedStateFromError: called during render phase to show fallback UI
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  // componentDidCatch: called in commit phase to log error
  componentDidCatch(error, errorInfo) {
    // errorInfo.componentStack: component call stack
    console.error('Error:', error);
    console.error('Component Stack:', errorInfo.componentStack);
    // Log to error monitoring service:
    logErrorToSentry(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong.</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage:
<ErrorBoundary>
  <ComponentThatMightCrash />
</ErrorBoundary>
```

> **Note:** Error boundaries only work as class components. As of 2024, there's no functional component equivalent (though proposals exist).

---

## 2.4 — Class vs Functional Components Comparison

| Feature | Class Component | Functional Component |
|---|---|---|
| **Syntax** | `class X extends Component` | `function X()` or `const X = () =>` |
| **State** | `this.state` + `this.setState` | `useState` hook |
| **Lifecycle** | Explicit methods | `useEffect` (maps to all) |
| **`this` keyword** | Required for state/props | Not needed |
| **Performance** | Slightly more overhead | Lighter |
| **Code length** | More verbose | More concise |
| **Error Boundaries** | ✅ Supported | ❌ Not supported |
| **Reusability** | Mixins (deprecated) | Custom Hooks (powerful) |
| **Testability** | Harder | Easier |
| **Learning curve** | Steeper (`this` binding) | Gentler |
| **Team preference** | Legacy codebases | Modern React (2019+) |
| **Future** | Maintained, no new features | Active development |

---

# 3. Props — Complete Guide

## 3.1 — What are Props?

**Props** (short for "properties") are the mechanism for passing data from a parent component to a child component. They are **read-only** — a component cannot modify its own props.

```
DATA FLOW:

Parent Component
    │
    │  <Child name="Alice" age={30} isAdmin={true} />
    │
    ▼
Child Component receives: { name: "Alice", age: 30, isAdmin: true }
Child CANNOT change these values
Child can DISPLAY them, PASS them further, USE them for logic
```

**Analogy:** Props are like **function arguments**. When you call `Math.max(3, 7)`, you pass arguments that the function uses but cannot change. Props work the same way.

---

## 3.2 — Passing All Types of Data via Props

```jsx
function Demo() {
  const userData = { name: 'Alice', age: 30 };
  const handleClick = (event) => console.log('Clicked!', event);

  return (
    <ComplexChild
      // String (no braces needed, but both work)
      title="Hello World"
      title2={'Hello World'}

      // Number (braces required)
      count={42}

      // Boolean (true shorthand)
      isActive       {/* = isActive={true} */}
      isDisabled={false}

      // Object
      user={userData}

      // Array
      items={['apple', 'banana', 'cherry']}

      // Function
      onClick={handleClick}
      onSubmit={(data) => console.log(data)}

      // JSX as prop (render prop pattern)
      header={<h1>Custom Header</h1>}

      // null / undefined
      optionalValue={null}

      // Template literals (computed)
      greeting={`Hello, ${userData.name}!`}
    />
  );
}
```

---

## 3.3 — Destructuring Props

```jsx
// Without destructuring:
function UserCard(props) {
  return (
    <div>
      <h2>{props.name}</h2>
      <p>{props.email}</p>
      <p>Admin: {props.isAdmin ? 'Yes' : 'No'}</p>
    </div>
  );
}

// With destructuring (cleaner — preferred):
function UserCard({ name, email, isAdmin }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>{email}</p>
      <p>Admin: {isAdmin ? 'Yes' : 'No'}</p>
    </div>
  );
}

// With default values in destructuring:
function UserCard({ name, email, isAdmin = false, role = 'User' }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>{email}</p>
      <p>Role: {role} {isAdmin ? '(Admin)' : ''}</p>
    </div>
  );
}

// With rest props:
function Button({ label, variant = 'primary', ...rest }) {
  // 'rest' contains any other props (onClick, className, disabled, etc.)
  return (
    <button className={`btn btn-${variant}`} {...rest}>
      {label}
    </button>
  );
}

// Usage:
<Button label="Submit" variant="success" onClick={handleSubmit} disabled={isLoading} />
// variant → used by Button
// onClick, disabled → spread onto <button> via ...rest
```

---

## 3.4 — defaultProps

```jsx
// Method 1: defaultProps (class and functional)
function Greeting({ name, greeting }) {
  return <h1>{greeting}, {name}!</h1>;
}

Greeting.defaultProps = {
  name: 'World',
  greeting: 'Hello',
};

// Method 2: Default parameter values in destructuring (preferred for functions)
function Greeting({ name = 'World', greeting = 'Hello' }) {
  return <h1>{greeting}, {name}!</h1>;
}

// Usage — missing props get defaults:
<Greeting />           // → "Hello, World!"
<Greeting name="Alice" />  // → "Hello, Alice!"
<Greeting greeting="Hi" name="Bob" />  // → "Hi, Bob!"
```

---

## 3.5 — PropTypes (Runtime Type Checking)

```jsx
import PropTypes from 'prop-types';

function UserProfile({ name, age, email, role, tags, onUpdate, children }) {
  return (
    <div>
      <h2>{name}</h2>
      {children}
    </div>
  );
}

UserProfile.propTypes = {
  name: PropTypes.string.isRequired,          // Required string
  age: PropTypes.number,                       // Optional number
  email: PropTypes.string.isRequired,          // Required string
  role: PropTypes.oneOf(['user', 'admin', 'moderator']),  // Enum
  tags: PropTypes.arrayOf(PropTypes.string),   // Array of strings
  onUpdate: PropTypes.func,                    // Function prop
  children: PropTypes.node,                    // Any renderable content

  // Shape for objects:
  address: PropTypes.shape({
    street: PropTypes.string,
    city: PropTypes.string.isRequired,
    zip: PropTypes.string,
  }),

  // Custom validator:
  evenNumber: function(props, propName, componentName) {
    if (props[propName] % 2 !== 0) {
      return new Error(`${propName} in ${componentName} must be even`);
    }
  },
};

// ⚠️ PropTypes only run in development mode (stripped in production)
// For production type safety: use TypeScript
```

---

## 3.6 — The children Prop

The `children` prop is special — it contains whatever JSX you put between a component's opening and closing tags.

```jsx
// Defining a component that accepts children:
function Card({ title, children }) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>{title}</h3>
      </div>
      <div className="card-body">
        {children}  {/* Renders whatever is passed between <Card> tags */}
      </div>
    </div>
  );
}

// Using it with children:
function App() {
  return (
    <Card title="My Card">
      {/* Everything here becomes 'children' */}
      <p>This is the card content.</p>
      <button>Click me</button>
      <ul>
        <li>Item 1</li>
        <li>Item 2</li>
      </ul>
    </Card>
  );
}
```

---

## 3.7 — Render Props Pattern

A **render prop** is a prop whose value is a function that returns JSX. This is a pattern for sharing logic between components.

```jsx
// Component that tracks mouse position and shares it via render prop
function MouseTracker({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (event) => {
    setPosition({ x: event.clientX, y: event.clientY });
  };

  return (
    <div onMouseMove={handleMouseMove} style={{ height: '100vh' }}>
      {/* Call the render prop function with shared data */}
      {render(position)}
    </div>
  );
}

// Usage — caller decides what to render with the position data:
function App() {
  return (
    <MouseTracker
      render={({ x, y }) => (
        <div>
          <p>Mouse at: {x}, {y}</p>
          <div
            style={{
              position: 'fixed',
              left: x,
              top: y,
              width: '10px',
              height: '10px',
              background: 'red',
              borderRadius: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          />
        </div>
      )}
    />
  );
}
```

> **Modern note:** Render props are largely replaced by **Custom Hooks** in modern React. But you'll see them in legacy codebases and interviews test them.

---

## 3.8 — Spread Props

```jsx
// Spread operator to pass all props at once:
function Parent() {
  const buttonProps = {
    variant: 'primary',
    size: 'large',
    disabled: false,
    onClick: () => console.log('clicked'),
  };

  return <Button {...buttonProps} label="Click me" />;
  // Equivalent to:
  // <Button variant="primary" size="large" disabled={false} onClick={...} label="Click me" />
}

// Useful for HOCs (Higher-Order Components) and wrapper components:
function StyledButton(props) {
  const { className, ...rest } = props; // Extract specific props
  return (
    <button
      className={`styled-btn ${className || ''}`}
      {...rest}  // Pass through all remaining props
    />
  );
}
```

---

## 3.9 — Prop Drilling Problem

**Prop drilling** occurs when you need to pass data through many layers of components that don't use it, just to reach a deeply nested component that does.

```
PROP DRILLING PROBLEM:

App (has 'user' state)
  ↓ passes user as prop
Dashboard
  ↓ passes user as prop (Dashboard doesn't need it!)
Sidebar
  ↓ passes user as prop (Sidebar doesn't need it!)
UserWidget
  ↓ passes user as prop (UserWidget doesn't need it!)
UserAvatar  ← THIS is the only one that actually needs 'user'

// Every intermediate component must accept and pass 'user' prop
// Changes to 'user' shape require updating every component in the chain!
```

**Solutions:**
1. **React Context** — global state accessible anywhere in the tree (Chapter 3)
2. **State management** — Redux, Zustand, Jotai
3. **Component composition** — rearrange components to avoid deep drilling

---

## 3.10 — Props vs State

| Aspect | Props | State |
|---|---|---|
| **Owner** | Parent component (passed down) | The component itself |
| **Mutable?** | No (read-only) | Yes (via setState/useState) |
| **Who sets it?** | Parent | The component itself |
| **Causes re-render?** | Yes (when parent re-renders with new props) | Yes (when updated) |
| **Initial value** | Passed from parent | Set in useState/constructor |
| **Passed to children?** | Yes | Can be, as props |
| **Default value?** | defaultProps | useState(defaultValue) |
| **Analogy** | Function argument | Function local variable |

---

# 4. State — useState Complete Guide

## 4.1 — What is State?

**State** is data that a component **owns and manages** — data that can change over time and when changed, causes the component to re-render.

**Analogy:** State is like a component's memory. Just as a person remembers their name (doesn't change) vs their current mood (can change), components have props (don't change from inside) and state (can change internally).

```jsx
// State example: A light switch
function LightSwitch() {
  // useState returns: [current value, function to update it]
  const [isOn, setIsOn] = useState(false);
  // 'false' = initial state

  return (
    <div>
      <p>Light is: {isOn ? 'ON' : 'OFF'}</p>
      <button onClick={() => setIsOn(prev => !prev)}>
        Toggle
      </button>
    </div>
  );
}
```

---

## 4.2 — useState Complete Syntax

```jsx
// Full syntax:
const [state, setState] = useState(initialValue);

// 'state' = the current value (read-only within this render)
// 'setState' = function to update state (triggers re-render)
// 'initialValue' = starting value (used ONLY on first render)

// Examples of different state types:
const [count, setCount] = useState(0);           // number
const [name, setName] = useState('Alice');        // string
const [isOpen, setIsOpen] = useState(false);      // boolean
const [items, setItems] = useState([]);           // array
const [user, setUser] = useState(null);           // null
const [data, setData] = useState({               // object
  name: '',
  email: '',
  age: 0,
});
```

---

## 4.3 — Lazy Initialization

When the initial state value is expensive to compute, use **lazy initialization** — pass a function instead of a value.

```jsx
// ❌ Expensive computation runs on EVERY render (wasteful!):
const [data, setData] = useState(expensiveComputation()); // Called every time!

// ✅ Lazy initialization — function called only ONCE (on mount):
const [data, setData] = useState(() => expensiveComputation());
// React only calls this function once — on initial render.
// On re-renders, the function is NOT called.

// Real example — reading from localStorage:
const [theme, setTheme] = useState(() => {
  // This runs only ONCE — initializes from localStorage
  const saved = localStorage.getItem('theme');
  return saved || 'light';
});
// On re-renders, useState completely ignores this function!
```

---

## 4.4 — Async Updates and State Snapshots

State updates are **asynchronous** — React doesn't update state immediately. It schedules the update and processes it before the next render.

**Critical concept:** Each render has its OWN snapshot of state. The `count` variable you use inside your component's render is a "snapshot" for that render.

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  const handleClick = () => {
    // All these read from the SAME snapshot (count = 0)
    setCount(count + 1); // Schedules: set to 0 + 1 = 1
    setCount(count + 1); // Schedules: set to 0 + 1 = 1 (still reads count = 0!)
    setCount(count + 1); // Schedules: set to 0 + 1 = 1

    console.log(count); // 0 (snapshot hasn't changed yet!)

    // After handleClick: count = 1 (not 3!) — last one wins for same state key
  };

  return <button onClick={handleClick}>{count}</button>;
}
```

---

## 4.5 — Functional Update Form (CRITICAL!)

Use the functional form of `setState` when the new state **depends on the previous state**:

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  const handleClick = () => {
    // ✅ CORRECT: Functional form — always reads the LATEST state
    setCount(prevCount => prevCount + 1); // prev = latest value React has
    setCount(prevCount => prevCount + 1); // prev = latest (previous result)
    setCount(prevCount => prevCount + 1); // prev = latest again
    // Result: count becomes 3 ✅

    // vs ❌ WRONG: Direct form — reads stale snapshot
    setCount(count + 1); // Schedules: 0 + 1 = 1
    setCount(count + 1); // Schedules: 0 + 1 = 1 (same count!)
    setCount(count + 1); // Schedules: 0 + 1 = 1
    // Result: count becomes 1 ❌
  };

  return <button onClick={handleClick}>{count}</button>;
}

// WHEN TO ALWAYS USE FUNCTIONAL FORM:
// 1. When new state depends on old state
// 2. When setState is called in closures (setTimeout, async code)
// 3. When calling setState multiple times in one event handler

// Example with async code (stale closure bug!):
function StaleClosureDemo() {
  const [count, setCount] = useState(0);

  const handleAsync = () => {
    setTimeout(() => {
      // ❌ 'count' is captured from the render when button was clicked
      // If count has changed since then, this is stale!
      setCount(count + 1); // Bug: always uses count from when button was clicked

      // ✅ Functional form reads the CURRENT latest count
      setCount(prev => prev + 1); // Always correct
    }, 3000);
  };

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={handleAsync}>Delayed Increment (+3s)</button>
    </div>
  );
}
```

---

## 4.6 — Batching in React 18

React 18 automatically batches ALL state updates into a single re-render:

```jsx
function BatchingDemo() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  const [c, setC] = useState(0);

  const handleClick = () => {
    setA(prev => prev + 1);  // ─┐
    setB(prev => prev + 1);  //  ├─ All batched → ONE re-render (React 18)
    setC(prev => prev + 1);  // ─┘
    console.log('After all setStates — still in handler, not re-rendered yet');
  };

  console.log('Rendered! a:', a, 'b:', b, 'c:', c);
  // This logs once per click (not 3 times!)

  return (
    <div>
      <p>A: {a}, B: {b}, C: {c}</p>
      <button onClick={handleClick}>Update All</button>
    </div>
  );
}
```

---

## 4.7 — State Immutability

**NEVER mutate state directly.** Always create a new object/array.

```jsx
function ImmutabilityDemo() {
  const [user, setUser] = useState({ name: 'Alice', age: 30, skills: ['React'] });

  // ❌ WRONG: Mutating state directly
  const addSkillWrong = (skill) => {
    user.skills.push(skill); // Mutates the existing array
    setUser(user);           // React sees same object reference → NO re-render!
    // React's Object.is() comparison: user === user → true → skips re-render
  };

  // ✅ CORRECT: Creating new objects
  const addSkillCorrect = (skill) => {
    setUser(prev => ({
      ...prev,            // Copy all existing properties
      skills: [...prev.skills, skill]  // Create new array with new skill
    }));
  };

  // ✅ Updating nested object property:
  const updateName = (newName) => {
    setUser(prev => ({ ...prev, name: newName }));
  };

  // ✅ Updating array items:
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React', done: false },
    { id: 2, text: 'Build Project', done: false },
  ]);

  const toggleTodo = (id) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id
          ? { ...todo, done: !todo.done }  // New object for changed item
          : todo                            // Same reference for unchanged items
      )
    );
  };

  const deleteTodo = (id) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
    // filter creates a new array — correct!
  };

  const addTodo = (text) => {
    setTodos(prev => [...prev, { id: Date.now(), text, done: false }]);
    // Spread + new item — correct!
  };

  return (
    <div>
      <p>Name: {user.name}</p>
      <p>Skills: {user.skills.join(', ')}</p>
      <button onClick={() => addSkillCorrect('TypeScript')}>Add TypeScript</button>
    </div>
  );
}
```

---

## 4.8 — Lifting State Up

When two components need to share the same state, move it to their closest common ancestor.

```
WITHOUT LIFTING STATE:
┌── App ──────────────────┐
│  ┌── TemperatureInput ──┐│  ← Has its own state (celsius)
│  └─────────────────────┘│
│  ┌── TemperatureInput ──┐│  ← Has its own state (fahrenheit)
│  └─────────────────────┘│
│  (They can't sync!)     │
└─────────────────────────┘

WITH LIFTING STATE:
┌── Calculator (STATE HERE) ─┐  ← Single source of truth
│  ┌── TemperatureInput ────┐│  ← Receives state as prop
│  └────────────────────────┘│
│  ┌── TemperatureInput ────┐│  ← Receives state as prop
│  └────────────────────────┘│
└────────────────────────────┘
```

```jsx
// COMPLETE EXAMPLE: Temperature Converter (classic React exercise)

function TemperatureInput({ scale, temperature, onTemperatureChange }) {
  const scaleNames = { c: 'Celsius', f: 'Fahrenheit' };
  return (
    <fieldset>
      <legend>Enter temperature in {scaleNames[scale]}:</legend>
      <input
        type="number"
        value={temperature}
        onChange={e => onTemperatureChange(e.target.value)}
      />
    </fieldset>
  );
}

function toCelsius(fahrenheit) {
  return ((fahrenheit - 32) * 5) / 9;
}

function toFahrenheit(celsius) {
  return (celsius * 9) / 5 + 32;
}

// STATE IS LIFTED HERE:
function Calculator() {
  const [temperature, setTemperature] = useState('');
  const [scale, setScale] = useState('c');

  const handleCelsiusChange = (temp) => {
    setTemperature(temp);
    setScale('c');
  };

  const handleFahrenheitChange = (temp) => {
    setTemperature(temp);
    setScale('f');
  };

  // Derive display values from single state
  const celsius = scale === 'f' ? toCelsius(parseFloat(temperature)) : temperature;
  const fahrenheit = scale === 'c' ? toFahrenheit(parseFloat(temperature)) : temperature;

  return (
    <div>
      <TemperatureInput
        scale="c"
        temperature={celsius}
        onTemperatureChange={handleCelsiusChange}
      />
      <TemperatureInput
        scale="f"
        temperature={fahrenheit}
        onTemperatureChange={handleFahrenheitChange}
      />
      {parseFloat(celsius) >= 100 && (
        <p>The water would boil!</p>
      )}
    </div>
  );
}
```

---

# 5. Rendering in React — When and Why

## 5.1 — What Triggers a Render?

```
RENDER TRIGGERS:

┌─────────────────────────────────────────────────────┐
│  Trigger                │  Example                  │
├─────────────────────────┼───────────────────────────┤
│  Own state changes      │  setState / setCount()     │
│  Props change           │  Parent passes new values  │
│  Parent re-renders      │  Even with same props!     │
│  Context value changes  │  useContext() subscriber   │
│  forceUpdate() (class)  │  Rare class component use  │
└─────────────────────────┴───────────────────────────┘
```

---

## 5.2 — Render vs Commit Phase

```
RENDER PHASE (pure computation):
1. React calls your function component (or render() method)
2. You return JSX
3. React creates VDOM from JSX
4. React diffs new VDOM with previous VDOM
5. React computes list of DOM changes needed

COMMIT PHASE (apply changes):
1. React applies DOM changes (insert, update, delete nodes)
2. Calls useLayoutEffect cleanups and effects
3. Paints pixels to screen
4. Calls useEffect cleanups and effects
```

---

## 5.3 — Preventing Unnecessary Renders

```jsx
// Problem: Every time Parent renders, ALL children re-render
// Solution 1: React.memo (memoize component — skip re-render if props unchanged)

const ExpensiveChild = React.memo(function ExpensiveChild({ data }) {
  console.log('ExpensiveChild rendered'); // Only logs when data changes!
  return <div>{JSON.stringify(data)}</div>;
});

// Solution 2: useMemo (memoize calculated values)
// Solution 3: useCallback (memoize function references)
// Solution 4: Restructure to avoid re-renders (covered in Chapter 3)

// React.memo SHALLOW compares props:
// - Primitive values (string, number, boolean) → compares by value ✅
// - Objects/arrays → compares by REFERENCE ❌ (new object = different reference!)

function Parent() {
  const [count, setCount] = useState(0);

  // ❌ New object on every render → React.memo won't help!
  const config = { color: 'blue', size: 'large' };

  // ✅ Memoized → same reference unless deps change
  const config2 = useMemo(() => ({ color: 'blue', size: 'large' }), []);

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Click</button>
      <ExpensiveChild data={config2} />
    </>
  );
}
```

---

# 6. Conditional Rendering

## 6.1 — All Patterns

```jsx
function ConditionalPatterns({ isLoggedIn, user, items, score }) {
  // Pattern 1: if/else — for complex conditions
  if (!isLoggedIn) {
    return <LoginPage />;  // Early return — entire component is different
  }

  // Pattern 2: Element variable
  let badge;
  if (score >= 90) badge = <GoldBadge />;
  else if (score >= 70) badge = <SilverBadge />;
  else badge = <BronzeBadge />;

  return (
    <div>
      {/* Pattern 3: Ternary operator */}
      {user ? (
        <UserProfile user={user} />
      ) : (
        <GuestView />
      )}

      {/* Pattern 4: && (short-circuit) */}
      {user?.isAdmin && <AdminPanel />}

      {/* Pattern 5: || (OR — show fallback if left is falsy) */}
      {user?.displayName || 'Anonymous User'}

      {/* Pattern 6: ?? (Nullish coalescing — only null/undefined trigger fallback) */}
      {user?.bio ?? 'No bio provided'}
      {/* vs || which triggers for 0, '', false, NaN too */}

      {/* Pattern 7: Switch-like with IIFE */}
      {(() => {
        switch(user?.role) {
          case 'admin': return <AdminDashboard />;
          case 'moderator': return <ModeratorPanel />;
          default: return <UserDashboard />;
        }
      })()}

      {badge}

      {/* ⚠️ COMMON PITFALL: 0 renders as text! */}
      {items.length && <ItemList items={items} />}
      {/* If items.length = 0, renders "0" in the DOM! */}

      {/* ✅ FIX: Convert to boolean */}
      {items.length > 0 && <ItemList items={items} />}
      {!!items.length && <ItemList items={items} />}
      {Boolean(items.length) && <ItemList items={items} />}

      {/* Pattern 8: Returning null */}
      <StatusBanner status={user?.status} />
    </div>
  );
}

// Component that renders nothing based on condition:
function StatusBanner({ status }) {
  if (!status || status === 'normal') return null; // No DOM output
  return <div className={`banner-${status}`}>Status: {status}</div>;
}
```

---

# 7. Lists and Keys

## 7.1 — Rendering Lists

```jsx
function ProductList({ products }) {
  return (
    <ul>
      {products.map(product => (
        // key MUST be on the outermost element returned from map
        <li key={product.id}>
          <strong>{product.name}</strong> — ${product.price}
        </li>
      ))}
    </ul>
  );
}

// With a component:
function ProductItem({ product }) {
  return (
    <li>
      <strong>{product.name}</strong>
    </li>
  );
}

function ProductList({ products }) {
  return (
    <ul>
      {products.map(product => (
        // key goes on ProductItem (the outermost JSX in map), NOT on <li> inside ProductItem
        <ProductItem key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

---

## 7.2 — Why Keys are Required

```
WITHOUT KEYS (React compares by position):
Old list:  [A, B, C]
New list:  [X, A, B, C] (added at beginning)

React comparison:
Position 0: A → X  (different! UPDATE A to show X)
Position 1: B → A  (different! UPDATE B to show A)
Position 2: C → B  (different! UPDATE C to show B)
Position 3: –→ C   (new! INSERT C at position 3)

Result: 3 updates + 1 insert = 4 DOM operations
AND: components lose their state (X gets A's state!)

WITH KEYS:
Old list:  [A(key=a), B(key=b), C(key=c)]
New list:  [X(key=x), A(key=a), B(key=b), C(key=c)]

React uses key map:
key=x: not in old → INSERT X
key=a: was at 0, now at 1 → MOVE
key=b: was at 1, now at 2 → MOVE
key=c: was at 2, now at 3 → MOVE

Result: 1 insert + 3 moves = 4 DOM operations
BUT: each component's state is preserved! ✅
```

---

## 7.3 — When Index is NOT OK as Key

```jsx
// ❌ BAD: Index as key when list can change order
function SortableList({ items }) {
  const [sorted, setSorted] = useState(false);
  const displayItems = sorted ? [...items].sort() : items;

  return (
    <ul>
      {displayItems.map((item, index) => (
        // Key is index — when sorted, keys don't match components
        <li key={index}>
          <input defaultValue={item} />  {/* Has state! */}
        </li>
      ))}
    </ul>
  );
  // Problem: After sorting, each index still has the old input value!
  // "Apple" was at index 0, "Banana" at 1
  // After sort: "Apple" is still at index 0, "Banana" at 1
  // But if user typed in input at index 0, that stays at index 0!
  // The input content doesn't move with the item!
}

// ✅ CORRECT: Stable unique ID
function SortableList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>  {/* Stable ID — moves with the item */}
          <input defaultValue={item.name} />
        </li>
      ))}
    </ul>
  );
}
```

**When index IS OK:**
- List is static and never reorders
- Items have no stateful children (pure display)
- Items are never filtered or reversed
- Performance benchmark shows it's acceptable

---

## 7.4 — Nested Lists with Keys

```jsx
function CategoryList({ categories }) {
  return (
    <div>
      {categories.map(category => (
        <div key={category.id}>  {/* Key on outer element */}
          <h2>{category.name}</h2>
          <ul>
            {category.items.map(item => (
              <li key={item.id}>  {/* Key is unique WITHIN its list scope */}
                {item.name}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
// Keys only need to be unique among siblings (same level in same array)
// Keys don't need to be globally unique
```

---

# 8. Fragments

## 8.1 — Why Fragments?

**Problem:** React requires a single root element, but adding extra `<div>` wrappers can break:
- CSS Flexbox/Grid layouts (extra nodes disrupt direct child relationships)
- HTML table structure (`<tr>` requires `<td>` as direct children)
- Semantic HTML

```jsx
// ❌ Without Fragment — extra div breaks table layout
function TableRow({ data }) {
  return (
    <div>  {/* <div> inside <tr> → invalid HTML! */}
      <td>{data.name}</td>
      <td>{data.age}</td>
    </div>
  );
}

// ✅ With Fragment — no extra DOM node
function TableRow({ data }) {
  return (
    <>
      <td>{data.name}</td>
      <td>{data.age}</td>
    </>
  );
}
// <></> is shorthand for <React.Fragment></React.Fragment>
// No extra DOM node created!

// ✅ Long-form with key (required when using key prop):
function ListItems({ items }) {
  return (
    <>
      {items.map(item => (
        // Must use React.Fragment (not <>) when you need key prop!
        <React.Fragment key={item.id}>
          <dt>{item.term}</dt>
          <dd>{item.description}</dd>
        </React.Fragment>
      ))}
    </>
  );
}
```

---

## 8.2 — Fragment vs div

```
DOM STRUCTURE COMPARISON:

Using <div>:
<div>     ← rendered in DOM
  <h1>Title</h1>
  <p>Content</p>
</div>

Using <>...</>:
(nothing)  ← no wrapper element in DOM!
<h1>Title</h1>
<p>Content</p>
```

---

# 9. Portals

## 9.1 — What is a Portal?

A **Portal** allows you to render a component's output into a different DOM node than its parent in the React tree.

**Use case:** Modals, tooltips, dropdown menus — elements that need to "escape" their parent's overflow/z-index constraints.

```
PORTAL CONCEPT:

React Component Tree:      Real DOM Tree:
<App>                      <body>
  <Modal>                    <div id="root">    ← Normal React output
    content                    <App's DOM>
  </Modal>                   </div>
</App>                       <div id="modal-root">  ← Portal output
                               <Modal's DOM>    ← Rendered here!
                             </div>
                           </body>

Even though Modal is inside App in React tree,
its DOM is rendered in #modal-root, outside #root!
```

```jsx
// index.html — add portal root:
// <div id="root"></div>
// <div id="modal-root"></div>  ← Add this

import { createPortal } from 'react-dom';

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return createPortal(
    // What to render:
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        {children}
      </div>
    </div>,
    // Where to render (DOM node):
    document.getElementById('modal-root')
  );
}

// Usage:
function App() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div style={{ overflow: 'hidden' }}>  {/* overflow:hidden won't trap Modal! */}
      <button onClick={() => setShowModal(true)}>Open Modal</button>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
        <h2>Modal Title</h2>
        <p>Modal content here...</p>
      </Modal>
    </div>
  );
}
```

---

## 9.2 — Portal Event Bubbling

**Key insight:** Events from a portal bubble through the React component tree (not the real DOM tree).

```jsx
function Parent() {
  const [clicked, setClicked] = useState(false);

  // This onClick fires even when the child Portal's button is clicked!
  // Because in React's component tree, PortalChild is INSIDE Parent
  return (
    <div onClick={() => setClicked(true)}>
      <p>Clicked: {String(clicked)}</p>
      <PortalChild />  {/* Even though DOM is elsewhere, events still bubble to here */}
    </div>
  );
}

function PortalChild() {
  return createPortal(
    <button>Click me (in portal)</button>,
    document.body  // Rendered at body level in DOM
  );
}
// Clicking the button → event bubbles through React tree → reaches Parent's div onClick
// This is intentional — allows proper event delegation in React
```

---

# 10. Refs

## 10.1 — What is useRef?

`useRef` returns a mutable object (`{ current: initialValue }`) that persists across renders. Changing `ref.current` does **NOT trigger a re-render**.

**Two use cases:**

```
USE CASE 1: Access DOM elements directly
USE CASE 2: Store a mutable value that persists across renders
            (like an instance variable, without causing re-renders)
```

---

## 10.2 — useRef for DOM Access

```jsx
import { useRef, useEffect } from 'react';

function AutoFocusInput() {
  const inputRef = useRef(null); // Create ref, initially null

  useEffect(() => {
    // After component mounts, inputRef.current = the actual <input> DOM element
    inputRef.current.focus(); // Focus the input on mount
  }, []);

  return (
    <input
      ref={inputRef}  // Attach ref to DOM element
      type="text"
      placeholder="I'm focused on mount!"
    />
  );
}

// More DOM operations with refs:
function VideoPlayer({ src }) {
  const videoRef = useRef(null);

  const play = () => videoRef.current.play();
  const pause = () => videoRef.current.pause();
  const setVolume = (v) => { videoRef.current.volume = v; };

  return (
    <div>
      <video ref={videoRef} src={src} />
      <button onClick={play}>Play</button>
      <button onClick={pause}>Pause</button>
    </div>
  );
}
```

---

## 10.3 — useRef for Mutable Values (No Re-render)

```jsx
function StopwatchWithRef() {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef(null); // Store interval ID — doesn't need to cause re-render

  const start = () => {
    if (intervalRef.current) return; // Already running
    setIsRunning(true);
    intervalRef.current = setInterval(() => {
      setTime(t => t + 1); // This updates time (re-renders)
    }, 1000);
  };

  const stop = () => {
    clearInterval(intervalRef.current);
    intervalRef.current = null; // Clear the ref
    setIsRunning(false);
  };

  const reset = () => {
    stop();
    setTime(0);
  };

  // Why not useState for intervalRef?
  // setIntervalId would trigger a re-render every time interval starts/stops
  // We don't need to display intervalId, so no re-render needed → useRef!

  return (
    <div>
      <p>{time}s</p>
      <button onClick={start} disabled={isRunning}>Start</button>
      <button onClick={stop} disabled={!isRunning}>Stop</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

---

## 10.4 — Storing Previous Values

```jsx
function usePrevious(value) {
  const prevRef = useRef(undefined);

  useEffect(() => {
    // After render, update ref to current value
    prevRef.current = value;
  }); // No deps array = runs after every render

  return prevRef.current; // Returns the PREVIOUS value (before this render)
}

// Usage:
function PriceTracker({ price }) {
  const prevPrice = usePrevious(price);

  return (
    <div>
      <p>Current: ${price}</p>
      <p>Previous: ${prevPrice}</p>
      <p style={{ color: price > prevPrice ? 'green' : 'red' }}>
        {price > prevPrice ? '↑ Up' : '↓ Down'}
      </p>
    </div>
  );
}
```

---

## 10.5 — forwardRef and useImperativeHandle

```jsx
// forwardRef — allows parent to pass a ref into a child component's DOM element
const FancyInput = React.forwardRef(function FancyInput(props, ref) {
  // ref is the second argument (after props)
  return (
    <div className="fancy-input-wrapper">
      <input ref={ref} {...props} className="fancy-input" />
    </div>
  );
});

// Parent can now access the inner <input> DOM element:
function Form() {
  const inputRef = useRef(null);

  const handleSubmit = () => {
    inputRef.current.focus(); // Focus the actual input
    console.log('Value:', inputRef.current.value);
  };

  return (
    <>
      <FancyInput ref={inputRef} placeholder="Type here" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}

// useImperativeHandle — expose a custom API instead of raw DOM element
const VideoPlayer = React.forwardRef(function VideoPlayer({ src }, ref) {
  const videoRef = useRef(null);

  // Expose only specific methods to parent — not the whole DOM element
  useImperativeHandle(ref, () => ({
    play: () => videoRef.current.play(),
    pause: () => videoRef.current.pause(),
    seek: (time) => { videoRef.current.currentTime = time; },
    // Parent cannot directly access videoRef.current (only these methods)
  }));

  return <video ref={videoRef} src={src} />;
});

// Parent usage:
function App() {
  const playerRef = useRef(null);

  return (
    <>
      <VideoPlayer ref={playerRef} src="/video.mp4" />
      <button onClick={() => playerRef.current.play()}>Play</button>
      <button onClick={() => playerRef.current.seek(30)}>Skip to 30s</button>
    </>
  );
}
```

---

## 10.6 — useRef vs useState Comparison

| Aspect | useRef | useState |
|---|---|---|
| **Triggers re-render?** | No | Yes |
| **Value persists?** | Yes (across renders) | Yes (across renders) |
| **Access pattern** | `ref.current` | Direct value + setter |
| **Mutable?** | Yes (direct mutation OK) | No (use setter function) |
| **Use for display?** | No (won't update UI) | Yes |
| **Use for DOM?** | Yes | No |
| **Common uses** | DOM refs, timers, prev values | UI data, form values |

---

# 11. Forms — Controlled vs Uncontrolled

## 11.1 — Controlled Components

In a **controlled component**, React state is the single source of truth. Every form input's value is controlled by React.

```jsx
import { useState } from 'react';

function LoginForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
    role: 'user',
    country: 'US',
  });
  const [errors, setErrors] = useState({});

  // Generic handler for all inputs:
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.email.includes('@')) newErrors.email = 'Invalid email';
    if (formData.password.length < 6) newErrors.password = 'Too short (min 6 chars)';
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent browser's default form submission (page reload)
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    console.log('Submitting:', formData);
    // Send to server, navigate, etc.
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Text Input */}
      <div>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"           // Must match formData key
          value={formData.email} // React controls value
          onChange={handleChange}
        />
        {errors.email && <span style={{ color: 'red' }}>{errors.email}</span>}
      </div>

      {/* Password Input */}
      <div>
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />
        {errors.password && <span style={{ color: 'red' }}>{errors.password}</span>}
      </div>

      {/* Checkbox */}
      <div>
        <label>
          <input
            type="checkbox"
            name="rememberMe"
            checked={formData.rememberMe}  // Use 'checked' for checkboxes!
            onChange={handleChange}
          />
          Remember Me
        </label>
      </div>

      {/* Radio Buttons */}
      <div>
        <label>
          <input
            type="radio"
            name="role"
            value="user"
            checked={formData.role === 'user'}
            onChange={handleChange}
          />
          User
        </label>
        <label>
          <input
            type="radio"
            name="role"
            value="admin"
            checked={formData.role === 'admin'}
            onChange={handleChange}
          />
          Admin
        </label>
      </div>

      {/* Select (Dropdown) */}
      <div>
        <label htmlFor="country">Country</label>
        <select
          id="country"
          name="country"
          value={formData.country}
          onChange={handleChange}
        >
          <option value="US">United States</option>
          <option value="UK">United Kingdom</option>
          <option value="IN">India</option>
          <option value="CA">Canada</option>
        </select>
      </div>

      {/* Textarea */}
      <div>
        <label htmlFor="bio">Bio</label>
        <textarea
          id="bio"
          name="bio"
          value={formData.bio || ''}
          onChange={handleChange}
          rows={4}
        />
      </div>

      <button type="submit">Login</button>
    </form>
  );
}
```

---

## 11.2 — Uncontrolled Components

In an **uncontrolled component**, the DOM handles form data. You read values when needed using refs.

```jsx
function UncontrolledForm() {
  const nameRef = useRef(null);
  const emailRef = useRef(null);
  const fileRef = useRef(null);  // File inputs are always uncontrolled!

  const handleSubmit = (e) => {
    e.preventDefault();
    const name = nameRef.current.value;
    const email = emailRef.current.value;
    const file = fileRef.current.files[0];
    console.log({ name, email, file });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        ref={nameRef}
        type="text"
        defaultValue="Alice"  // Set initial value (NOT value — that would be controlled)
        // defaultValue sets initial state but DOM then owns the value
      />
      <input
        ref={emailRef}
        type="email"
      />
      {/* File input is ALWAYS uncontrolled — you cannot set its value programmatically */}
      <input ref={fileRef} type="file" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## 11.3 — Controlled vs Uncontrolled Comparison

| Aspect | Controlled | Uncontrolled |
|---|---|---|
| **Source of truth** | React state | DOM |
| **Value access** | `state.value` | `ref.current.value` |
| **Re-renders on change?** | Yes (every keystroke) | No |
| **Validation** | Immediate (on each change) | On submit only |
| **Dynamic fields** | Easy | Complex |
| **Programmatic reset** | Easy (`setState('')`) | `ref.current.value = ''` |
| **React philosophy** | Preferred (declarative) | Escape hatch |
| **File inputs** | Not possible | Required |
| **Performance** | Can be slower (many re-renders) | Faster for large forms |

---

# 12. Chapter Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│              CHAPTER 2 SUMMARY — COMPONENTS, PROPS, STATE           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FUNCTIONAL COMPONENTS                                              │
│  ├─ Function returning JSX                                          │
│  ├─ Must start with uppercase                                       │
│  └─ Must be pure (same props → same output)                         │
│                                                                     │
│  CLASS COMPONENTS                                                   │
│  ├─ Lifecycle: constructor→getDerivedStateFromProps→render→         │
│  │  componentDidMount→shouldComponentUpdate→render→                 │
│  │  getSnapshotBeforeUpdate→componentDidUpdate→componentWillUnmount │
│  └─ Error boundaries require class components                       │
│                                                                     │
│  PROPS                                                              │
│  ├─ Read-only data from parent                                      │
│  ├─ children prop, spread props, render props                       │
│  └─ Prop drilling problem → solved by Context or restructuring      │
│                                                                     │
│  STATE (useState)                                                   │
│  ├─ Use functional form when new state depends on old state         │
│  ├─ Never mutate state — always create new objects/arrays           │
│  ├─ Lazy initialization with function argument                      │
│  └─ Lift state to common ancestor when sharing between siblings     │
│                                                                     │
│  CONDITIONAL RENDERING                                              │
│  └─ WARNING: 0 && <Comp> renders "0" — use count > 0 && <Comp>     │
│                                                                     │
│  LISTS AND KEYS                                                     │
│  ├─ Always provide stable unique keys (not array index)            │
│  └─ Keys help React identify item identity for efficient updates    │
│                                                                     │
│  REFS                                                               │
│  ├─ DOM access + mutable value storage without re-render           │
│  └─ forwardRef to pass refs to child components                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 13. Top 25 Interview Questions — Chapter 2

**Q1: What is the difference between state and props?**

**Answer:** 
- **Props**: Read-only data passed from parent to child. The parent owns and can change props (from its perspective). The child cannot modify them.
- **State**: Data owned and managed by the component itself. The component can update state via `setState`/`useState`. State is private to the component.

Analogy: Props are like function parameters (read-only from function's perspective). State is like local variables inside the function (can be changed).

---

**Q2: Why should you never mutate state directly in React?**

**Answer:** React uses **Object.is()** (reference equality) to detect state changes. If you mutate an existing object and pass the same reference, React doesn't know the state changed and skips re-rendering.

```javascript
// Bug: React sees same reference → no re-render
state.items.push(newItem);  // Mutated existing array
setState(state.items);       // Same reference → React ignores!

// Correct: New reference → React detects change → re-renders
setState(prev => [...prev.items, newItem]);  // New array reference ✅
```

---

**Q3: What is the functional form of useState's setter and when must you use it?**

**Answer:** The functional form `setState(prevState => newState)` receives the LATEST state value. You MUST use it when:
1. New state depends on previous state
2. Multiple setState calls in one event handler
3. setState called from async callbacks/closures (where direct state value could be stale)

```javascript
// These both increment count by 3:
// ❌ Wrong (batched, all read count = 0):
setCount(count + 1); setCount(count + 1); setCount(count + 1); // → 1

// ✅ Correct (each gets latest):
setCount(p => p + 1); setCount(p => p + 1); setCount(p => p + 1); // → 3
```

---

**Q4: What are all the lifecycle methods in a React class component?**

**Answer:**
**Mounting:** `constructor` → `getDerivedStateFromProps` → `render` → `componentDidMount`
**Updating:** `getDerivedStateFromProps` → `shouldComponentUpdate` → `render` → `getSnapshotBeforeUpdate` → `componentDidUpdate`
**Unmounting:** `componentWillUnmount`
**Error handling:** `getDerivedStateFromError` → `componentDidCatch`

---

**Q5: Why do we need the `key` prop in lists?**

**Answer:** React uses keys to match components between renders during reconciliation. Without keys, React compares list items by position — if you add an item at the beginning, React thinks every item changed. With unique stable keys, React can correctly identify which items were added, removed, or moved, minimizing DOM updates and preserving component state.

---

**Q6: When should you use useRef vs useState?**

**Answer:**
- **useState**: When the value needs to cause a UI re-render when it changes. For values that are displayed in JSX.
- **useRef**: When you need to:
  - Access a DOM element directly
  - Store a mutable value that should NOT trigger re-renders (timer IDs, previous values, subscribers)
  - Maintain a reference to any mutable value across renders

Key distinction: `useRef` doesn't trigger re-renders; `useState` does.

---

**Q7: What is prop drilling and how do you solve it?**

**Answer:** Prop drilling is passing data through multiple layers of components that don't need it, just to reach a deeply nested component that does.

Solutions:
1. **React Context** — create global state accessible anywhere in the component tree
2. **State management libraries** — Redux, Zustand, Jotai
3. **Component composition** — restructure so the component needing data is closer to its source
4. **Render props / children as function** — let the top-level component render the child that needs the data

---

**Q8: What is the `children` prop?**

**Answer:** `children` is a special prop that contains whatever JSX is nested between a component's opening and closing tags. It enables component composition — building wrapper/layout components that accept arbitrary content.

```jsx
<Modal>
  <h1>Title</h1>  {/* These become props.children */}
  <p>Content</p>
</Modal>
```

---

**Q9: What is the difference between controlled and uncontrolled components?**

**Answer:**
- **Controlled**: React state drives the form value (`value={state}` + `onChange`). React is the source of truth. Allows immediate validation, programmatic control.
- **Uncontrolled**: DOM manages the value. React reads it via refs when needed (on submit). Simpler, less re-renders, required for file inputs.

---

**Q10: What is lifting state up?**

**Answer:** When two sibling components need to share state, you remove the state from both and move it to their closest common ancestor (parent). The parent passes the state as props and provides callback functions for siblings to request state changes.

---

**Q11: How does `forwardRef` work?**

**Answer:** `React.forwardRef` allows a parent component to pass a ref to a child component's DOM element. Without it, refs only work on native DOM elements; functional components don't accept the `ref` prop by default.

```jsx
const Input = React.forwardRef((props, ref) => (
  <input ref={ref} {...props} />
));
// Now: <Input ref={myRef} /> → myRef.current = <input> DOM node
```

---

**Q12: What is the difference between `defaultValue` and `value` in a form input?**

**Answer:**
- `value` — controlled: React fully controls the input. Must provide `onChange` or input is read-only.
- `defaultValue` — uncontrolled: Sets initial value but DOM controls it afterwards. Used with refs to read values later.

```jsx
<input value={state} onChange={...} />     // Controlled
<input defaultValue="initial" ref={ref} /> // Uncontrolled
```

---

**Q13: What is a React Portal and why would you use it?**

**Answer:** A Portal renders a component's output into a different DOM node than its parent component. Created with `ReactDOM.createPortal(jsx, domNode)`.

Use cases: Modals, tooltips, dropdown menus — components that need to visually "escape" their parent's CSS constraints (overflow:hidden, z-index stacking context) while remaining logically inside the React component tree (for event bubbling purposes).

---

**Q14: What are render props?**

**Answer:** A render prop is a prop whose value is a function that returns JSX. It's a pattern for sharing logic between components — the parent holds the logic (data/state) and the child decides how to render it via the render prop function.

```jsx
<DataProvider render={data => <Chart data={data} />} />
// or using children as a function:
<DataProvider>{data => <Chart data={data} />}</DataProvider>
```

This pattern is largely replaced by Custom Hooks in modern React.

---

**Q15: Why is `super(props)` required in class component constructors?**

**Answer:** `super(props)` calls the `Component` base class's constructor, which sets up `this.props`. Without it, accessing `this.props` inside the constructor would be `undefined` (though it works in lifecycle methods and render, which is why this bug is subtle). Also, in JavaScript, you cannot use `this` before calling `super()` in a derived class.

---

**Q16: What is `shouldComponentUpdate` and what does React.PureComponent do?**

**Answer:** `shouldComponentUpdate(nextProps, nextState)` is a lifecycle method that returns `true` (re-render) or `false` (skip re-render). You implement it for performance optimization.

`React.PureComponent` automatically implements `shouldComponentUpdate` with a **shallow comparison** of props and state — if nothing changed shallowly, it skips re-rendering. The functional component equivalent is `React.memo()`.

---

**Q17: When would you use `getSnapshotBeforeUpdate`?**

**Answer:** `getSnapshotBeforeUpdate` runs after render but before DOM updates are applied. You can read DOM properties (like scroll position) before the update. The return value is passed as the third argument to `componentDidUpdate`.

Classic use case: A chat window that should scroll to show new messages while preserving the user's scroll position if they've scrolled up to read old messages.

---

**Q18: What is the difference between `getDerivedStateFromError` and `componentDidCatch`?**

**Answer:**
- `getDerivedStateFromError(error)`: Called during the **render phase** to derive state from the error. Used to set `hasError: true` so the fallback UI renders. Returns the state update object.
- `componentDidCatch(error, info)`: Called during the **commit phase** for side effects like logging the error to an error monitoring service (Sentry, Datadog). Has access to `this` (unlike the static getDerivedStateFromError).

---

**Q19: Can you give an example where using array index as key causes a bug?**

**Answer:** Consider a list with text inputs where each input has user-typed content. If you use index as key and delete the first item, React shifts all indices — each component gets the key that was previously the NEXT item's key. React sees these as the same components (same key) and doesn't re-mount them. But the shifted items now display the wrong content because the state (user-typed text) was tied to the old index/key, not the item identity.

---

**Q20: What is lazy initialization in useState?**

**Answer:** Passing a function to `useState` instead of a value. The function is called ONCE (on initial mount) to compute the initial state. Use it when initial state computation is expensive (reading localStorage, complex calculation):

```javascript
// ❌ Runs on every render (wasteful):
const [data, setData] = useState(localStorage.getItem('data'));

// ✅ Runs only once (lazy):
const [data, setData] = useState(() => localStorage.getItem('data'));
```

---

**Q21: Why does React re-render a child even if its props didn't change?**

**Answer:** By default, whenever a parent component re-renders, ALL of its children re-render too, regardless of whether props changed. This is because React re-calls your function component, and you get fresh JSX. React's default behavior is "re-render everything and let the VDOM diffing handle it."

To prevent this, use `React.memo()` which skips re-rendering a child if its props are shallowly equal to previous props.

---

**Q22: What happens if you forget `e.preventDefault()` in a form's onSubmit?**

**Answer:** The browser performs its default form submission behavior — it sends an HTTP GET (or POST) request to the page URL (or form's `action` attribute), causing a full page reload. All React state is lost. In SPAs, this is almost always wrong. `e.preventDefault()` stops the default browser action, letting React handle the submission.

---

**Q23: Explain the PropTypes library and its limitations.**

**Answer:** PropTypes provides runtime type checking for React props. You define expected types on a component's `propTypes` property, and React logs warnings in development if wrong types are passed.

Limitations:
1. Only runs in **development** (stripped in production — no performance cost but no protection)
2. Only **warns**, doesn't throw errors — silently fails in production
3. **Runtime** only — no compile-time safety
4. Limited expressiveness vs TypeScript's type system
5. Bundle size overhead (though removable with babel plugin)

Modern alternative: **TypeScript** for compile-time type checking.

---

**Q24: What is `useImperativeHandle` and when would you use it?**

**Answer:** `useImperativeHandle` (used with `forwardRef`) lets you customize the interface exposed to parents via refs. Instead of exposing the entire DOM node, you expose only specific methods.

Use case: A complex `VideoPlayer` component that exposes only `play()`, `pause()`, `seek()` methods to parents — not the entire `<video>` DOM element (which would let parents do anything to it, breaking encapsulation).

---

**Q25: What is the difference between `null` and `undefined` when rendered in JSX?**

**Answer:** Both `null` and `undefined` render nothing (no DOM output) when used as JSX children. However:
- Returning `null` from a component is the idiomatic way to render nothing
- Returning `undefined` causes a React warning/error (components should return null, not undefined)
- `{null}` in JSX → renders nothing ✅
- `{undefined}` in JSX → renders nothing ✅
- `{false}` in JSX → renders nothing ✅
- `{0}` in JSX → renders the number "0" ⚠️ (common bug!)
- `{NaN}` in JSX → renders "NaN" ⚠️

---

# 14. Output/Render Exercises

**Exercise 1: What does this render?**

```jsx
function App() {
  const [count, setCount] = useState(3);
  return (
    <div>
      {count && <p>Count: {count}</p>}
    </div>
  );
}
```

**Answer:** Renders `<div><p>Count: 3</p></div>`.
When count = 3 (truthy), `3 && <p>Count: 3</p>` evaluates to `<p>Count: 3</p>`.
BUT: If count was 0, it would render `<div>0</div>`! Bug!

---

**Exercise 2: How many times does this render?**

```jsx
function Parent() {
  const [x, setX] = useState(0);

  return (
    <div>
      <button onClick={() => setX(x)}>Click</button>
      <Child />
    </div>
  );
}

const Child = React.memo(() => {
  console.log('Child rendered');
  return <p>Hello</p>;
});
```

**Answer:**
- Initial render: `Child rendered` → 1 time
- After clicking the button: `setX(x)` sets the same value. React uses `Object.is(0, 0)` = true → **skips re-render**. `Child rendered` does NOT log again.

Note: If `Child` was NOT wrapped in `React.memo`, clicking would re-render `Child` (even though `x` didn't change) because `Parent` re-renders. But React's optimization for class components and `React.memo` skips the child when parent's state update results in same value.

---

**Exercise 3: What does this class component do?**

```jsx
class BadComponent extends Component {
  state = { count: 0 };

  componentDidUpdate() {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return <div>{this.state.count}</div>;
  }
}
```

**Answer:** **Infinite loop!**

`componentDidUpdate` calls `setState` unconditionally → triggers re-render → `componentDidUpdate` runs again → `setState` again → infinite loop. React will crash with "Maximum update depth exceeded."

Fix: Add a condition: `if (someCondition) this.setState(...)`.

---

**Exercise 4: What does this output?**

```jsx
function App() {
  const ref = useRef(0);

  const handleClick = () => {
    ref.current += 1;
    console.log('ref.current:', ref.current);
  };

  return (
    <div>
      <p>Ref value: {ref.current}</p>
      <button onClick={handleClick}>Increment Ref</button>
    </div>
  );
}
```

**Answer:** 
- Display always shows **"Ref value: 0"** — it never updates in the UI, because changing `ref.current` doesn't trigger a re-render.
- `console.log` shows 1, 2, 3, ... on each click — the ref IS incrementing, but the UI doesn't know.
- To see it in UI: use `useState` instead.

---

**Exercise 5: What is wrong with this key usage?**

```jsx
function List({ items }) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i}>
          <input placeholder={item.label} />
        </li>
      ))}
    </ul>
  );
}

// Test: items = [{ label: 'A' }, { label: 'B' }, { label: 'C' }]
// User types "hello" in input A
// items is filtered to remove first element: [{ label: 'B' }, { label: 'C' }]
```

**Answer:** Bug! After filtering:
- Index 0 was "A" (user typed "hello"), now it's "B"
- React sees key=0 → same component → keeps existing input's state
- Input at index 0 still shows "hello" (typed for A), but label says "B"
- User's typed text has "moved" to the wrong item

Fix: Use stable unique IDs as keys: `key={item.id}`.

---

# 15. Coding Exercises

## Exercise 1: Complete Class Component Lifecycle Demo

```jsx
import React, { Component } from 'react';

class LifecycleDemo extends Component {
  constructor(props) {
    super(props);
    console.log('1. constructor');
    this.state = {
      data: null,
      loading: true,
      count: 0,
    };
  }

  static getDerivedStateFromProps(props, state) {
    console.log('2. getDerivedStateFromProps');
    return null; // No state update
  }

  componentDidMount() {
    console.log('4. componentDidMount');
    // Simulate API call
    setTimeout(() => {
      this.setState({ data: 'Fetched Data!', loading: false });
    }, 1000);
  }

  shouldComponentUpdate(nextProps, nextState) {
    console.log('5. shouldComponentUpdate');
    // Skip re-render if only loading changed but count is the same
    return true; // Allow all updates for demo
  }

  getSnapshotBeforeUpdate(prevProps, prevState) {
    console.log('6. getSnapshotBeforeUpdate');
    return `Snapshot: count was ${prevState.count}`;
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    console.log('7. componentDidUpdate, snapshot:', snapshot);
  }

  componentWillUnmount() {
    console.log('8. componentWillUnmount');
  }

  render() {
    console.log('3. render');
    if (this.state.loading) return <div>Loading...</div>;
    return (
      <div>
        <h2>{this.state.data}</h2>
        <p>Count: {this.state.count}</p>
        <button onClick={() => this.setState(s => ({ count: s.count + 1 }))}>
          Increment
        </button>
      </div>
    );
  }
}

export default LifecycleDemo;
```

---

## Exercise 2: Custom Form Hook

```jsx
// Custom hook for form management
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setValues(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleBlur = (e) => {
    setTouched(prev => ({ ...prev, [e.target.name]: true }));
  };

  const resetForm = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return { values, errors, touched, setErrors, handleChange, handleBlur, resetForm };
}

// Usage:
function RegistrationForm() {
  const { values, errors, touched, setErrors, handleChange, handleBlur, resetForm } = useForm({
    username: '',
    email: '',
    password: '',
    agreeToTerms: false,
  });

  const validate = (vals) => {
    const errs = {};
    if (vals.username.length < 3) errs.username = 'Min 3 characters';
    if (!vals.email.includes('@')) errs.email = 'Invalid email';
    if (vals.password.length < 8) errs.password = 'Min 8 characters';
    if (!vals.agreeToTerms) errs.agreeToTerms = 'Must agree to terms';
    return errs;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate(values);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    console.log('Registered:', values);
    resetForm();
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '400px' }}>
      <div>
        <input
          name="username"
          placeholder="Username"
          value={values.username}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        {touched.username && errors.username && (
          <span style={{ color: 'red', fontSize: '12px' }}>{errors.username}</span>
        )}
      </div>
      <div>
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={values.email}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        {touched.email && errors.email && (
          <span style={{ color: 'red', fontSize: '12px' }}>{errors.email}</span>
        )}
      </div>
      <div>
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={values.password}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        {touched.password && errors.password && (
          <span style={{ color: 'red', fontSize: '12px' }}>{errors.password}</span>
        )}
      </div>
      <label>
        <input
          name="agreeToTerms"
          type="checkbox"
          checked={values.agreeToTerms}
          onChange={handleChange}
        />
        I agree to the Terms of Service
      </label>
      {errors.agreeToTerms && (
        <span style={{ color: 'red', fontSize: '12px' }}>{errors.agreeToTerms}</span>
      )}
      <button type="submit">Register</button>
      <button type="button" onClick={resetForm}>Reset</button>
    </form>
  );
}

export default RegistrationForm;
```

---

## Exercise 3: Portal Modal Component

```jsx
import { createPortal } from 'react-dom';
import { useState, useEffect } from 'react';

function Modal({ isOpen, onClose, title, children }) {
  // Close on Escape key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      document.body.style.overflow = 'hidden'; // Prevent background scroll
    }
    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div
      style={{
        position: 'fixed', inset: 0,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'white', borderRadius: '8px',
          padding: '24px', maxWidth: '500px', width: '90%',
          position: 'relative',
        }}
        onClick={e => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
          <h2 style={{ margin: 0 }}>{title}</h2>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        {children}
      </div>
    </div>,
    document.body
  );
}

function App() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div style={{ padding: '40px' }}>
      <h1>Portal Modal Demo</h1>
      <button onClick={() => setModalOpen(true)}>Open Modal</button>
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Hello, Portal!"
      >
        <p>This modal is rendered in document.body via a Portal!</p>
        <p>Click outside or press Escape to close.</p>
        <button onClick={() => setModalOpen(false)}>Close</button>
      </Modal>
    </div>
  );
}

export default App;
```

---

## Exercise 4: Lifted State — Shopping Cart

```jsx
import { useState } from 'react';

// Product catalog data
const PRODUCTS = [
  { id: 1, name: 'React T-Shirt', price: 29.99 },
  { id: 2, name: 'JavaScript Mug', price: 14.99 },
  { id: 3, name: 'TypeScript Hoodie', price: 59.99 },
];

// Dumb component — only renders data from props
function ProductItem({ product, quantity, onAdd, onRemove }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', border: '1px solid #ddd', marginBottom: '8px', borderRadius: '4px' }}>
      <div>
        <strong>{product.name}</strong>
        <p style={{ margin: '4px 0', color: '#666' }}>${product.price}</p>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button onClick={() => onRemove(product.id)}>-</button>
        <span>{quantity}</span>
        <button onClick={() => onAdd(product.id)}>+</button>
      </div>
    </div>
  );
}

// Cart summary — also dumb
function CartSummary({ items, products }) {
  const total = items.reduce((sum, item) => {
    const product = products.find(p => p.id === item.productId);
    return sum + (product.price * item.quantity);
  }, 0);

  return (
    <div style={{ marginTop: '20px', padding: '16px', background: '#f5f5f5', borderRadius: '4px' }}>
      <h3>Cart Summary</h3>
      {items.filter(i => i.quantity > 0).map(item => {
        const product = products.find(p => p.id === item.productId);
        return (
          <p key={item.productId}>
            {product.name} × {item.quantity} = ${(product.price * item.quantity).toFixed(2)}
          </p>
        );
      })}
      <hr />
      <strong>Total: ${total.toFixed(2)}</strong>
    </div>
  );
}

// Smart parent — owns the STATE (lifted up)
function ShoppingCart() {
  const [cartItems, setCartItems] = useState(
    PRODUCTS.map(p => ({ productId: p.id, quantity: 0 }))
  );

  const addItem = (productId) => {
    setCartItems(prev =>
      prev.map(item =>
        item.productId === productId
          ? { ...item, quantity: item.quantity + 1 }
          : item
      )
    );
  };

  const removeItem = (productId) => {
    setCartItems(prev =>
      prev.map(item =>
        item.productId === productId
          ? { ...item, quantity: Math.max(0, item.quantity - 1) }
          : item
      )
    );
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h1>Shopping Cart</h1>
      {PRODUCTS.map(product => (
        <ProductItem
          key={product.id}
          product={product}
          quantity={cartItems.find(i => i.productId === product.id).quantity}
          onAdd={addItem}
          onRemove={removeItem}
        />
      ))}
      <CartSummary items={cartItems} products={PRODUCTS} />
    </div>
  );
}

export default ShoppingCart;
```

---

## Exercise 5: Error Boundary with Reset

```jsx
import { Component } from 'react';

class ErrorBoundary extends Component {
  state = { hasError: false, error: null, errorInfo: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    // In production: logErrorToMonitoringService(error, errorInfo);
    console.error('Caught an error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', background: '#fff3f3', border: '1px solid #ffcccc', borderRadius: '8px' }}>
          <h2>⚠️ Something went wrong</h2>
          <p><strong>Error:</strong> {this.state.error?.message}</p>
          {process.env.NODE_ENV === 'development' && (
            <details style={{ marginTop: '10px' }}>
              <summary>Error details (dev only)</summary>
              <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                {this.state.errorInfo?.componentStack}
              </pre>
            </details>
          )}
          <button
            onClick={this.handleReset}
            style={{ marginTop: '12px', padding: '8px 16px' }}
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Component that throws an error:
function BuggyComponent({ shouldError }) {
  if (shouldError) {
    throw new Error('I crashed!');
  }
  return <p style={{ color: 'green' }}>✓ Everything is working!</p>;
}

function App() {
  const [crash, setCrash] = useState(false);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h1>Error Boundary Demo</h1>
      <button onClick={() => setCrash(true)} style={{ marginBottom: '12px' }}>
        Crash the component
      </button>
      <ErrorBoundary>
        <BuggyComponent shouldError={crash} />
      </ErrorBoundary>
    </div>
  );
}

export default App;
```

---

# 16. MCQs

**Q1:** Which lifecycle method is called ONLY once, after the first render?
- A) `getDerivedStateFromProps`
- B) `componentDidUpdate`
- C) `componentDidMount` ✅
- D) `render`

---

**Q2:** What does `React.memo` do?
- A) Memoizes expensive computations inside a component
- B) Prevents a component from re-rendering if its props are shallowly equal ✅
- C) Caches the result of an API call
- D) Makes a component lazy-load

---

**Q3:** When using `useRef`, what happens when you change `ref.current`?
- A) The component re-renders
- B) An error is thrown
- C) Nothing — no re-render occurs ✅
- D) The parent re-renders

---

**Q4:** Which is the CORRECT way to update an array in React state?
- A) `state.items.push(newItem); setState(state);`
- B) `setState({ items: state.items.push(newItem) });`
- C) `setState(prev => ({ items: [...prev.items, newItem] }));` ✅
- D) `setState({ items: state.items });`

---

**Q5:** What is the output of `{0 && <div>Hello</div>}` in JSX?
- A) Nothing is rendered
- B) `<div>Hello</div>` is rendered
- C) The number `0` is rendered ✅
- D) An error is thrown

---

**Q6:** Which of the following is TRUE about Error Boundaries?
- A) They can be functional components
- B) They must be class components ✅
- C) They catch errors in event handlers
- D) They catch asynchronous errors

---

**Q7:** What does `e.preventDefault()` do in a form's `onSubmit` handler?
- A) Stops the event from bubbling up
- B) Prevents the browser's default form submission (page reload) ✅
- C) Prevents React's re-render
- D) Clears the form fields

---

**Q8:** When is `getSnapshotBeforeUpdate` called?
- A) Before the component renders
- B) After the DOM has been updated
- C) After render, but before the DOM updates are applied ✅
- D) When an error occurs

---

**Q9:** Which prop would you use to give a `<label>` its `for` attribute in JSX?
- A) `for`
- B) `forLabel`
- C) `htmlFor` ✅
- D) `labelFor`

---

**Q10:** What is the main benefit of lifting state up?
- A) Better performance
- B) Smaller bundle size
- C) A single source of truth shared between sibling components ✅
- D) Prevents prop drilling

---

> **End of Chapter 2 — Components, Props, State & Rendering**

---

*Next Chapter: React Hooks — The Complete Guide →*

---
**Chapter Word Count:** ~9,500 words | **Code Examples:** 70+ | **Interview Questions:** 25 | **MCQs:** 10 | **Exercises:** 5+
