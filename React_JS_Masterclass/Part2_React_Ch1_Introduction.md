# Part 2 — React.js Mastery
# Chapter 1: Introduction to React — Foundation & Core Concepts

> **"React makes it painless to create interactive UIs."** — React Official Docs

---

## Table of Contents

1. What is React?
2. Problems React Solves
3. Virtual DOM
4. Reconciliation & Diffing Algorithm
5. React Fiber Architecture
6. SPA vs MPA
7. Component-Based Architecture
8. Setting Up React (Vite + CRA)
9. JSX Deep Dive
10. React Elements vs Components
11. React 18 Features
12. Chapter Summary
13. Top 25 Interview Questions
14. Output/Render Prediction Exercises
15. Coding Exercises
16. MCQs

---

# 1. What is React?

## 1.1 — Definition

React is an **open-source JavaScript library** (not a framework!) created by **Jordan Walke** at **Facebook** (now Meta), first deployed on Facebook's News Feed in **2011** and open-sourced at **JSConf US** in **May 2013**.

React's single, focused job is:

> **Building user interfaces — specifically, the "View" layer of an application.**

React does not prescribe how you handle routing, data fetching, or state management at the application level. You choose those tools yourself. This is by design — React is intentionally unopinionated about everything except rendering UI.

---

## 1.2 — Library vs Framework

This distinction is one of the most commonly asked interview questions.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LIBRARY vs FRAMEWORK                             │
│                                                                     │
│  LIBRARY                           FRAMEWORK                        │
│  ┌─────────────────────┐           ┌─────────────────────┐          │
│  │  Your Code          │           │  Framework          │          │
│  │  ┌────────────────┐ │           │  ┌────────────────┐ │          │
│  │  │                │ │           │  │  ┌──────────┐  │ │          │
│  │  │   calls →      │ │           │  │  │Your Code │  │ │          │
│  │  │   Library      │ │           │  │  └──────────┘  │ │          │
│  │  │   functions    │ │           │  │   calls ↑      │ │          │
│  │  └────────────────┘ │           │  └────────────────┘ │          │
│  └─────────────────────┘           └─────────────────────┘          │
│                                                                     │
│  YOU are in control.               FRAMEWORK is in control.         │
│  You call the library.             Framework calls your code.       │
│  (Hollywood Principle reversed)    (IoC — Inversion of Control)     │
│                                                                     │
│  Example: React, Lodash,           Example: Angular, Next.js,       │
│           Axios, jQuery            Nest.js, Ruby on Rails           │
└─────────────────────────────────────────────────────────────────────┘
```

**Real-World Analogy:**
- A **library** is like a **hardware store**. You walk in, pick the tools you need (hammer, drill, nails), and build whatever you want, however you want.
- A **framework** is like a **prefabricated house kit**. It gives you a blueprint and structure. You fill in the rooms, but you must follow the plan.

React is a **library** — you bring your own router (React Router), your own state manager (Redux, Zustand), your own HTTP client (Axios, fetch). You are in control.

---

## 1.3 — Core Philosophy of React

React is built on **three foundational philosophies**:

### Philosophy 1: Declarative

```
IMPERATIVE (old way — jQuery/vanilla JS):
"Go to the DOM, find element with id 'counter',
 read its text, parse it as number, add 1 to it,
 convert back to string, set the text content."

DECLARATIVE (React way):
"The UI should show this count value. React, figure out
 how to make the DOM look like that."
```

**Code Comparison:**

```javascript
// IMPERATIVE — Vanilla JS / jQuery
// You describe HOW to do it, step by step
const btn = document.querySelector('#increment');
btn.addEventListener('click', () => {
  const display = document.querySelector('#count');
  const currentValue = parseInt(display.textContent, 10);
  display.textContent = String(currentValue + 1);
});

// DECLARATIVE — React
// You describe WHAT the UI should look like given state
function Counter() {
  const [count, setCount] = React.useState(0);
  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

In the declarative approach, you don't touch the DOM at all. You just say: "given `count`, show this JSX." React handles all DOM updates.

### Philosophy 2: Component-Based

Everything in React is a **component** — a self-contained, reusable piece of UI that manages its own appearance and behavior.

```
Your Entire App
├── Header
│   ├── Logo
│   ├── NavBar
│   │   ├── NavItem
│   │   ├── NavItem
│   │   └── NavItem (with Dropdown)
│   └── UserAvatar
├── MainContent
│   ├── Sidebar
│   │   └── FilterPanel
│   └── ArticleList
│       ├── ArticleCard
│       ├── ArticleCard
│       └── ArticleCard
└── Footer
    ├── FooterLinks
    └── Copyright
```

Each component is like a **LEGO brick** — small, reusable, combinable.

### Philosophy 3: Learn Once, Write Anywhere

React skills transfer across:
- **React DOM** → web browsers
- **React Native** → iOS and Android apps
- **React 360** → VR experiences
- **React TV** → Smart TV apps
- **Ink** → Terminal/CLI interfaces
- **Next.js** → Server-side rendered web apps

You learn React once; the rendering target can change.

---

## 1.4 — React vs Angular vs Vue Comparison

| Feature | React | Angular | Vue |
|---|---|---|---|
| **Type** | Library (View only) | Full Framework | Progressive Framework |
| **Created by** | Meta (Facebook) | Google | Evan You (ex-Google) |
| **Released** | 2013 | 2016 (Angular 2+) | 2014 |
| **Language** | JavaScript / JSX | TypeScript (enforced) | JavaScript / TypeScript |
| **Learning Curve** | Medium | Steep | Gentle |
| **Architecture** | Component-based | MVC + Component-based | Component-based |
| **Data Binding** | One-way | Two-way | Two-way |
| **DOM** | Virtual DOM | Real DOM + Change Detection | Virtual DOM |
| **State Mgmt** | External (Redux, Zustand) | Built-in (Services) | Vuex / Pinia |
| **Routing** | React Router (external) | Built-in (@angular/router) | Vue Router (external) |
| **Bundle Size** | ~42KB (gzipped) | ~130KB (gzipped) | ~33KB (gzipped) |
| **Performance** | Excellent | Good | Excellent |
| **Community** | Largest | Large | Large |
| **Flexibility** | Maximum | Minimum (opinionated) | Medium |
| **Testing** | Jest + RTL | Jasmine + Karma | Vue Test Utils |
| **Mobile** | React Native | Ionic | NativeScript |
| **Job Market** | Highest demand | High demand | Growing demand |

**When to choose which:**
- **React** → Maximum flexibility, large talent pool, complex SPAs, when you want to choose your stack
- **Angular** → Enterprise, TypeScript-first teams, when you want everything provided
- **Vue** → Gentle learning curve, rapid prototyping, smaller teams, PHP/Laravel integration

---

## 1.5 — Companies Using React

React is trusted by some of the largest companies in the world:

| Company | React Usage |
|---|---|
| **Meta (Facebook)** | Created it — used everywhere |
| **Instagram** | Entire web app |
| **Netflix** | UI components |
| **Airbnb** | Main web application |
| **Uber** | Driver/Rider apps |
| **Twitter/X** | Web application |
| **Dropbox** | Web app + desktop |
| **WhatsApp Web** | Built with React |
| **Pinterest** | Main application |
| **Atlassian** | Jira, Confluence, Trello |
| **Microsoft** | Xbox, Teams, Outlook |
| **Amazon** | AWS Console |
| **Shopify** | Storefront components |
| **Khan Academy** | Education platform |
| **Notion** | Productivity app |

---

# 2. Problems React Solves

## 2.1 — The Dark Ages: jQuery and Vanilla JS Problems

Before React, building complex UIs meant directly manipulating the DOM. This led to several serious problems:

### Problem 1: Spaghetti Code — The Callback Hell of UI

```javascript
// VANILLA JS — Building a "Like" button with update count
// This is what developers had to write:

document.addEventListener('DOMContentLoaded', function() {
  var likeBtn = document.getElementById('likeBtn');
  var likeCount = document.getElementById('likeCount');
  var liked = false;
  var count = parseInt(likeCount.textContent) || 0;

  likeBtn.addEventListener('click', function() {
    if (!liked) {
      liked = true;
      count++;
      likeBtn.style.color = 'red';
      likeBtn.textContent = 'Unlike';
      likeCount.textContent = count + ' Likes';
      // Also need to update other places where count is shown...
      document.getElementById('totalEngagement').textContent =
        'Total: ' + (count + parseInt(document.getElementById('commentCount').textContent));
      // And the profile page shows like count...
      // And the notification badge...
      // And if there's a live feed elsewhere on the page...
      // Every single DOM element must be updated MANUALLY
    } else {
      // Reverse everything...
    }
  });
});
```

**Problems with this code:**
1. You must manually track every DOM element that displays `count`
2. Updating one piece of data requires updating multiple DOM nodes
3. As the app grows, these update chains become unmaintainable
4. State (the actual data) is scattered across DOM attributes and JavaScript variables
5. No single source of truth

### Problem 2: State Synchronization Nightmare

```
VANILLA JS STATE PROBLEM:

User data: name = "Alice", age = 30, likes = 42

WHERE IS THIS DATA?
├── In a JS variable: let userData = { name: "Alice", ... }
├── In DOM: <h1>Alice</h1> — stored as text content
├── In DOM: <span>30</span> — stored as text content  
├── In DOM: <div class="likes">42</div> — stored as text
├── In localStorage? Maybe.
├── In a cookie? Perhaps.
└── In a data-* attribute? Possibly.

When userData.likes changes to 43:
→ Must manually update ALL DOM occurrences
→ Miss one? The UI is inconsistent
→ Race conditions? Good luck debugging.
```

### Problem 3: Performance — Direct DOM Manipulation is Expensive

The DOM is a tree of objects living in C++ (in the browser engine). Every time JavaScript touches it:

```
JS Engine (V8) ←→ Bridge ←→ DOM Engine (C++)

Each DOM operation crosses this bridge. Crossing is expensive.

// BAD: Multiple DOM reads/writes (causes layout thrashing)
for (let i = 0; i < 1000; i++) {
  const el = document.getElementById('item-' + i);
  el.style.width = el.offsetWidth + 10 + 'px';  // READ then WRITE
  // Each iteration: read → browser recalculates layout → write → repeat
  // 1000 layout recalculations!
}
```

### Problem 4: No Reusability

In jQuery, creating a "card" component meant copying HTML + initializing jQuery plugins each time. There was no clean component model.

---

## 2.2 — The Facebook Chat Bug That Led to React

This is a famous story in software engineering history.

**The Year:** 2011
**The Problem:** Facebook's chat system had a maddening bug.

```
SCENARIO:
1. User opens Facebook
2. Chat notification badge shows "1" new message
3. User clicks it → reads the message
4. Badge updates to "0" — all good
5. User navigates to Timeline
6. Badge shows "1" again! ← BUG
7. User clicks → no new messages
8. Badge goes back to "0"
9. Navigate again → "1" appears AGAIN
```

**Root Cause Analysis:**

Facebook's chat state was stored in **multiple places**:
- The notification count in the nav bar
- The message store
- The chat pane state
- The unread indicator in the conversation list

When you "read" a message, you had to update **all of these**, and the update order was fragile. A cascade of events would sometimes reset the unread count incorrectly.

```
STATE SCATTERED ACROSS MULTIPLE "MODELS":

NavBar Controller     ChatPane Controller    MessageStore
     |                       |                    |
  count = 1              isRead = false       messages = [...]
     |                       |                    |
     └──────── User clicks ──┘                    |
                    ↓                             |
          Update NavBar count = 0                 |
                    ↓                             |
          Update MessageStore.read = true         |
                    ↓                             |
          ChatPane doesn't know about this        |
          still shows unread indicator            |
                    ↓                             |
          User navigates → other event fires      |
                    ↓                             |
          ChatPane re-emits "unread" event        |
                    ↓                             |
          NavBar picks it up: count = 1 again!    |
```

**The Solution — Flux Architecture (led to React):**

Jordan Walke and the Facebook team realized: **you cannot reliably synchronize state across multiple models with two-way event chains.**

The solution:
1. **Single Source of Truth**: One store for state
2. **One-Way Data Flow**: Data flows down, events flow up
3. **Re-render the entire view when state changes** (but do it efficiently with Virtual DOM)

This insight became React.

```
REACT'S SOLUTION:

Single State/Store
       ↓
   React renders UI from this state
       ↓
   User interacts
       ↓
   Action dispatched
       ↓
   State updates
       ↓
   React re-renders UI (only changed parts, via VDOM)
       ↓
   UI always reflects current state — GUARANTEED
```

---

## 2.3 — Two-Way Data Binding Issues (Angular 1.x)

Angular 1's two-way data binding (`ng-model`) was magical but problematic at scale:

```
TWO-WAY BINDING:

Model ←→ View

If Model changes → View updates
If View changes → Model updates
If Model changes because View changed → View updates again?
Potential infinite loop!

Angular 1's "digest cycle":
Model changes → Angular checks all watchers → 
If any changed → run again → repeat until stable

With 2000+ watchers on a complex page:
Performance degrades significantly (>2-3 second freezes)
```

React's **one-way data flow** avoids this:

```
DATA FLOWS ONE WAY:

State/Props → JSX (render) → DOM
                              ↑
User Event → Handler → setState → triggers re-render
```

No infinite loops. No digest cycles. Predictable.

---

# 3. Virtual DOM

## 3.1 — What is the Virtual DOM?

The **Virtual DOM (VDOM)** is a **lightweight JavaScript object representation** of the actual browser DOM.

**Analogy:**
Think of building a house. Before calling the construction crew (expensive, real work), an architect creates a **blueprint** (cheap, fast, on paper). The architect compares new blueprints with old ones, marks only the changes, and tells the crew exactly what to modify.

- **Real DOM** = The actual house (expensive to change)
- **Virtual DOM** = The blueprint (cheap JavaScript objects)
- **Reconciliation** = Comparing blueprints
- **React DOM patch** = Construction crew making targeted changes

```
VIRTUAL DOM REPRESENTATION:

// What you write in JSX:
<div className="container">
  <h1>Hello, World</h1>
  <p>Welcome to React</p>
</div>

// What React creates internally (simplified):
{
  type: 'div',
  props: {
    className: 'container',
    children: [
      {
        type: 'h1',
        props: {
          children: 'Hello, World'
        }
      },
      {
        type: 'p',
        props: {
          children: 'Welcome to React'
        }
      }
    ]
  }
}
```

This is just a **plain JavaScript object** — no browser APIs, no C++ engine, no painting pixels. Creating and comparing these objects is extremely fast.

---

## 3.2 — VDOM vs Real DOM Comparison Table

| Aspect | Real DOM | Virtual DOM |
|---|---|---|
| **Nature** | Browser API (C++ objects) | Plain JavaScript objects |
| **Memory** | High (each node is a full C++ object) | Low (simple JS objects) |
| **Create speed** | Slow | Very Fast |
| **Update speed** | Slow (triggers layout + paint) | Fast (just JS operations) |
| **Can be printed** | No | Yes (just a JS object) |
| **Accessible in Node.js** | No | Yes (React runs on Node for SSR) |
| **Triggers repaint?** | Yes, on every change | No (just object manipulation) |
| **React controls it?** | Yes (via ReactDOM) | Yes (React creates it) |

---

## 3.3 — How React Uses the Virtual DOM

```
┌──────────────────────────────────────────────────────────────────────┐
│                    REACT RENDERING PIPELINE                          │
│                                                                      │
│  1. Initial Render:                                                  │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐                  │
│  │  JSX Code  │───▶│  VDOM (v1) │───▶│  Real DOM  │                  │
│  │  App()     │    │  (created) │    │  (painted) │                  │
│  └────────────┘    └────────────┘    └────────────┘                  │
│                                                                      │
│  2. State Changes:                                                   │
│  ┌────────────┐    ┌────────────┐                                    │
│  │  setState  │───▶│  VDOM (v2) │ (new virtual tree created)         │
│  │  called    │    │  (new)     │                                    │
│  └────────────┘    └─────┬──────┘                                    │
│                          │                                           │
│                    ┌─────▼──────┐                                    │
│                    │  DIFFING   │ (v1 vs v2)                         │
│                    │  Algorithm │                                    │
│                    └─────┬──────┘                                    │
│                          │                                           │
│                    ┌─────▼──────┐    ┌────────────┐                  │
│                    │   Patch    │───▶│  Real DOM  │                  │
│                    │ (minimal   │    │  (updated  │                  │
│                    │  changes)  │    │  minimally)│                  │
│                    └────────────┘    └────────────┘                  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3.4 — THE MYTH: Is Virtual DOM Always Faster?

**No!** This is a critical misconception, and senior interviewers love testing this.

> **"The Virtual DOM is not inherently faster than direct DOM manipulation. It's a performance optimization over a naive re-render approach, but expert manual DOM manipulation is faster."**
>
> — Rich Harris (creator of Svelte)

```
PERFORMANCE SPECTRUM:

Slowest ◄──────────────────────────────────────────► Fastest

Naive full       Virtual DOM     Expert manual        Svelte
re-render    │     (React)    │   DOM updates     │ (compile-time)
(clear + repaint)│ (smart updates) │ (Facebook engineers)│ (no VDOM overhead)
```

**What Virtual DOM actually does:**
- Avoids **naive** re-renders (don't throw away and rebuild everything)
- Makes **good enough** performance accessible to **average developers**
- Provides a **clean programming model** (declarative) while maintaining **reasonable performance**

**When React VDOM is SLOWER:**
- Simple apps with few DOM nodes (overhead of VDOM isn't worth it)
- When you would have done fewer DOM updates manually anyway
- Svelte/SolidJS (no VDOM) outperform React in benchmarks

**React's real value proposition is not pure speed — it's:**
1. Predictable rendering (declarative)
2. Component reusability
3. Developer experience
4. Ecosystem

---

# 4. Reconciliation & Diffing Algorithm

## 4.1 — What is Reconciliation?

**Reconciliation** is the process by which React updates the DOM to match the current state of your component tree.

When state or props change, React:
1. Creates a **new Virtual DOM tree**
2. **Compares** (diffs) it against the **previous Virtual DOM tree**
3. Calculates the **minimum set of changes** needed
4. **Applies those changes** to the real DOM

> "Reconciliation is the algorithm behind what is popularly understood as the 'virtual DOM'." — React Docs

---

## 4.2 — The Naive Algorithm vs React's O(n) Algorithm

The most general algorithm for comparing two trees has a complexity of **O(n³)**:

```
NAIVE TREE COMPARISON — O(n³):
For a tree with 1000 nodes:
1000³ = 1,000,000,000 comparisons
At 60fps: 1 billion comparisons per second needed
IMPOSSIBLE for real-time UI!

REACT'S ALGORITHM — O(n):
For a tree with 1000 nodes:
1000 comparisons
At 60fps: perfectly feasible
```

**How does React achieve O(n)?** By making **two heuristic assumptions:**

---

## 4.3 — React's Two Key Assumptions

### Assumption 1: Elements of Different Types Produce Different Trees

```javascript
// CASE 1: Element type changes
// Previous render:          New render:
<div>                        <span>
  <Counter />                  <Counter />
</div>                       </span>

// React sees: div → span (different type)
// React's decision: TEAR DOWN the entire div subtree.
//                   BUILD an entirely new span subtree.
// Even though Counter is the same, it gets UNMOUNTED and REMOUNTED
// because its parent type changed!
```

This seems wasteful, but it's a safe heuristic. In practice, when you change a container's type, you almost always intend a completely different subtree.

### Assumption 2: Keys Signal Stable Identity Across Renders

```javascript
// Without keys — React compares by position:
// Previous:         New (item added at beginning):
<ul>                  <ul>
  <li>Alice</li>        <li>Bob</li>    ← React thinks: position 0 was Alice,
  <li>Bob</li>          <li>Alice</li>     now it's Bob → UPDATE
</ul>                   <li>Carol</li>  ← React thinks: position 2 is new → INSERT
                    </ul>
// React updates ALL existing elements + inserts one.
// Inefficient!

// With keys — React tracks identity:
<ul>
  <li key="alice">Alice</li>
  <li key="bob">Bob</li>
</ul>

// New:
<ul>
  <li key="bob">Bob</li>     ← React knows: bob moved, just reorder DOM
  <li key="alice">Alice</li> ← React knows: alice moved, just reorder DOM
  <li key="carol">Carol</li> ← React knows: carol is new → INSERT only
</ul>
// React just moves existing DOM nodes + inserts one. Efficient!
```

---

## 4.4 — How Diffing Works Step-by-Step

```
STATE CHANGE → NEW VDOM → DIFF → PATCH DOM
```

### Step 1: Compare Root Element Types

```
OLD TREE:    NEW TREE:    RESULT:
<div>        <div>        Same type → compare attributes/children
<span>       <div>        Different type → destroy old, build new
```

### Step 2: Compare Attributes (same type elements)

```javascript
// Old VDOM node:
{ type: 'div', props: { className: 'old', id: 'box', style: { color: 'red' } } }

// New VDOM node:
{ type: 'div', props: { className: 'new', id: 'box', style: { color: 'blue' } } }

// React computes diff:
// - className: 'old' → 'new'  →  UPDATE className
// - id: 'box' → 'box'         →  NO CHANGE
// - style.color: 'red' → 'blue' → UPDATE style.color
// Only the minimal attributes are changed in the real DOM!
```

### Step 3: Recurse on Children

```
Old:           New:
<ul>           <ul>
  <li>A</li>     <li>A</li>    ← Same, no change
  <li>B</li>     <li>B</li>    ← Same, no change
               <li>C</li>    ← New! INSERT into DOM
```

### Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│              RECONCILIATION FLOW DIAGRAM                            │
│                                                                     │
│  User triggers state change                                         │
│           │                                                         │
│           ▼                                                         │
│  React calls render() / function component                          │
│           │                                                         │
│           ▼                                                         │
│  New Virtual DOM Tree created                                       │
│           │                                                         │
│           ▼                                                         │
│  ┌────────────────────────┐                                         │
│  │  Is this initial mount?│                                         │
│  └────────┬───────────────┘                                         │
│           │ YES                    NO                               │
│           ▼                        ▼                                │
│  Mount to Real DOM         Compare with previous VDOM               │
│           │                        │                                │
│           │                 ┌──────▼──────────────────┐            │
│           │                 │ Walk tree node by node   │            │
│           │                 │ Compare element types    │            │
│           │                 │ Compare props/attributes │            │
│           │                 │ Compare children + keys  │            │
│           │                 └──────┬──────────────────┘            │
│           │                        │                                │
│           │                 ┌──────▼──────────────────┐            │
│           │                 │ Calculate minimal patch  │            │
│           │                 │ (list of DOM operations) │            │
│           │                 └──────┬──────────────────┘            │
│           │                        │                                │
│           └────────────────────────┤                                │
│                                    ▼                                │
│                        Apply changes to Real DOM                    │
│                        (batch for efficiency)                       │
│                                    │                                │
│                                    ▼                                │
│                        Browser repaints changed pixels              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4.5 — When Does React Re-Render?

React re-renders a component when:

1. **setState is called** (the component's own state changes)
2. **Props change** (parent passes new prop values)
3. **Parent re-renders** (even if props haven't changed — unless optimized with React.memo)
4. **Context changes** (any Context the component subscribes to changes)
5. **useReducer dispatch** (equivalent to setState)

```javascript
function Parent() {
  const [count, setCount] = useState(0);
  // When count changes, Parent re-renders
  // AND Child also re-renders (even though it receives no props)!
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>+</button>
      <Child />  {/* Re-renders whenever Parent does! */}
    </div>
  );
}

function Child() {
  console.log('Child rendered');  // Called every time Parent renders
  return <div>I am a child</div>;
}
```

---

# 5. React Fiber Architecture

## 5.1 — Why Fiber Was Needed (React 16, 2017)

Before React 16, React used a **stack reconciler** — a synchronous, recursive algorithm.

```
OLD STACK RECONCILER:

renderApp()
  └─ renderHeader()
       └─ renderNav()
            └─ renderNavItem() × 50
renderMain()
  └─ renderArticleList()
       └─ renderArticle() × 100
            └─ renderComments() × 20 each

Total recursive calls: potentially thousands
ALL SYNCHRONOUS — cannot be interrupted!
```

**The Problem:**

```
JavaScript is single-threaded!

┌─────────────────────────────────────────────────────────────────┐
│                  BROWSER MAIN THREAD                            │
│                                                                 │
│  [  React reconciliation (100ms)  ] [  User input?  ] [Paint]  │
│                                          ↑                      │
│                                   BLOCKED! Must wait            │
│                                   for React to finish           │
│                                                                 │
│  User types in input field → character appears 100ms later     │
│  User clicks button → click fires 100ms later                  │
│  Animation → JANK (dropped frames)                             │
└─────────────────────────────────────────────────────────────────┘
```

**The real-world symptom:**
- Facebook had a complex News Feed with animations + user interactions
- Whenever a large component tree re-rendered, animations would jank
- User input would appear delayed/frozen
- This was unacceptable for a modern web application

---

## 5.2 — What is React Fiber?

**Fiber** is React's **reimplemented reconciliation algorithm** (React 16+).

The core idea: **make rendering work interruptible**.

> "Fiber is the new reconciliation engine in React 16. Its main goal is to enable incremental rendering of the virtual DOM." — React Team

**Key innovation:** Instead of one huge recursive call stack, React Fiber represents each component as a **Fiber node** — a plain JavaScript object that contains all information needed to process that unit of work.

```
FIBER NODE (simplified):

{
  type: MyComponent,          // Component type
  key: null,                  // Key for reconciliation
  stateNode: null,            // DOM node or class instance
  child: FiberNode,           // First child
  sibling: FiberNode,         // Next sibling
  return: FiberNode,          // Parent fiber
  pendingProps: {},           // New props
  memoizedProps: {},          // Last rendered props
  memoizedState: {},          // Last rendered state
  effectTag: 0,               // What DOM changes are needed
  alternate: FiberNode,       // The previous fiber (for comparison)
  // Priority:
  lanes: 0,                   // Priority level (React 18)
}
```

---

## 5.3 — The Linked List Tree (How Fibers Connect)

React Fiber converts the component tree into a **linked list** instead of a call stack:

```
FIBER TREE (linked list structure):

          App
        /    \
    child    sibling ─ ...
      |
    Header
        \
      sibling → Main
                  |
                child
                  |
               ArticleList
                  |
                child
                  |
               Article ─ sibling → Article ─ sibling → ...

Each node has: child, sibling, return (parent) pointers
React can walk this tree ONE NODE AT A TIME
and PAUSE/RESUME between nodes!
```

---

## 5.4 — Two Phases of Fiber Work

Fiber divides rendering into two distinct phases:

### Phase 1: Render Phase (Interruptible)

```
RENDER PHASE:
- Can be PAUSED, ABORTED, or RESTARTED
- Pure computation — no side effects
- Determines what changes need to be made
- Runs "off-screen" (doesn't touch real DOM)
- May run multiple times if interrupted!

Work done in render phase:
├── Call function components (to get JSX)
├── Call class component render() methods
├── Run useState/useReducer logic
├── Perform VDOM diffing
└── Build list of DOM changes ("effects")
```

> **Critical implication:** Since render phase can run multiple times, it MUST be pure (no side effects). This is why React 18's Strict Mode double-invokes renders in development — to catch impure renders!

### Phase 2: Commit Phase (Synchronous, cannot be interrupted)

```
COMMIT PHASE:
- CANNOT be paused
- Runs synchronously from start to finish
- Actually modifies the real DOM
- Runs lifecycle methods / effects

Three sub-phases:
1. Before mutation  → getSnapshotBeforeUpdate, etc.
2. Mutation         → Insert/Update/Delete DOM nodes
3. Layout           → useLayoutEffect, componentDidMount/Update
```

---

## 5.5 — Priority Scheduling

Fiber assigns priorities to different types of updates:

```
PRIORITY LEVELS (highest to lowest):

┌────────────────────────────────────────────────────────┐
│ ImmediatePriority    → Synchronous, must complete now  │
│ (e.g., user input, discrete events)                    │
├────────────────────────────────────────────────────────┤
│ UserBlockingPriority → Must respond within 250ms       │
│ (e.g., hover, scrolling)                               │
├────────────────────────────────────────────────────────┤
│ NormalPriority       → No deadline (~5 seconds)        │
│ (e.g., data fetch results)                             │
├────────────────────────────────────────────────────────┤
│ LowPriority          → Can defer (~10 seconds)         │
│ (e.g., prefetching data)                               │
├────────────────────────────────────────────────────────┤
│ IdlePriority         → Do when browser is idle         │
│ (e.g., preloading off-screen content)                  │
└────────────────────────────────────────────────────────┘
```

**Example:** If React is reconciling a large list AND the user types in an input:
- React **pauses** the list reconciliation
- **Processes** the keystroke (high priority) first
- **Resumes** list reconciliation after

This is what makes React 18's **Concurrent Mode** possible.

---

## 5.6 — Concurrent Mode (React 18)

**Concurrent Mode** is built on top of Fiber's interruptible rendering:

```javascript
// React 17 (legacy): createRoot was ReactDOM.render()
// React 18: createRoot enables concurrent features
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);

// Now you can use concurrent features:
// useTransition — mark some state updates as non-urgent
// useDeferredValue — defer expensive re-renders
// Suspense — declarative loading states
```

```
CONCURRENT RENDERING ANALOGY:

OLD (synchronous):
Chef cooks entire meal from start to finish without stopping.
A fire alarm goes off → chef ignores it until done.

NEW (concurrent / Fiber):
Chef starts cooking meal.
Fire alarm goes off → chef PAUSES, handles emergency, RESUMES cooking.
More important task? INTERRUPT, handle it, come BACK.
```

---

# 6. SPA vs MPA

## 6.1 — Definitions

### Single Page Application (SPA)

An SPA loads **one HTML file** once. All navigation happens via **JavaScript** — the URL changes but no full page reload occurs. The server returns data (JSON), not new HTML pages.

```
SPA NAVIGATION FLOW:

1. User visits example.com
   → Server returns ONE index.html + JS bundle

2. User clicks "About" link
   → JavaScript intercepts click
   → Fetches JSON data from API
   → Updates only the changed portion of the DOM
   → Updates URL via History API (pushState)
   → No network request for new HTML!

3. User clicks "Products"
   → Same as above, milliseconds to "navigate"
```

**Examples:** Gmail, Google Maps, Twitter, Trello, any React/Angular/Vue app

### Multi Page Application (MPA)

An MPA loads a **new HTML file** from the server on every navigation.

```
MPA NAVIGATION FLOW:

1. User visits example.com/home
   → Server returns home.html

2. User clicks "About"
   → NEW HTTP request to server
   → Server returns about.html
   → Browser discards current page
   → Renders new page (full repaint, flash)

3. User clicks "Products"
   → NEW HTTP request for products.html
   → Repeat
```

**Examples:** Traditional WordPress sites, e-commerce product pages, news sites

---

## 6.2 — SPA vs MPA Comparison Table

| Feature | SPA | MPA |
|---|---|---|
| **Initial Load** | Slower (large JS bundle) | Faster (small HTML) |
| **Subsequent navigation** | Instantaneous | Slower (full page reload) |
| **User Experience** | App-like, smooth | Page flash on navigation |
| **SEO** | Harder (needs SSR/SSG) | Excellent (HTML is searchable) |
| **Server Load** | Less (API only) | More (renders full pages) |
| **JavaScript required** | Yes | No (graceful degradation) |
| **Caching** | Complex | Simpler |
| **Security (CSRF)** | More careful needed | Built-in browser protections |
| **Development** | More complex setup | Simpler for small sites |
| **Time to Interactive** | Slower initially | Faster initially |
| **Analytics** | Need special handling | Natural (each page = a request) |
| **Browser History** | Manual (History API) | Built-in |
| **Mobile Performance** | Can be heavy | Lighter |

---

## 6.3 — When to Choose Which

**Choose SPA when:**
- Building app-like experiences (dashboards, tools, productivity apps)
- Heavy user interaction (forms, real-time updates, complex state)
- Your users have reliable internet
- Team has strong JavaScript skills
- Examples: Admin dashboards, email clients, social feeds, games

**Choose MPA when:**
- SEO is critical (blogs, e-commerce, news)
- Content is mostly static
- Accessibility across diverse devices
- Simple content-focused sites
- Progressive enhancement is important
- Examples: Marketing sites, blogs, product catalogs, documentation

**The modern answer — SSR/SSG (Next.js, Remix):**
- Get the SEO benefits of MPA
- Get the UX benefits of SPA
- React renders on server → sends HTML → hydrates to SPA

---

# 7. Component-Based Architecture

## 7.1 — Why Components?

**The fundamental problem components solve:** Code reuse and separation of concerns in UI.

```
WITHOUT COMPONENTS (HTML duplication):

<!-- product-list.html -->
<div class="product-card">
  <img src="shoe.jpg" alt="Shoe">
  <h3>Nike Air Max</h3>
  <p>$129.99</p>
  <button>Add to Cart</button>
</div>
<div class="product-card">
  <img src="shirt.jpg" alt="Shirt">
  <h3>Levi's T-Shirt</h3>
  <p>$39.99</p>
  <button>Add to Cart</button>
</div>
<!-- Repeat 50 more times... -->
<!-- Want to add a "wishlist" button? Update 52 places! -->

WITH COMPONENTS (React):
function ProductCard({ image, name, price }) {
  return (
    <div className="product-card">
      <img src={image} alt={name} />
      <h3>{name}</h3>
      <p>${price}</p>
      <button>Add to Cart</button>
      <button>Add to Wishlist</button>  {/* Added once → appears everywhere */}
    </div>
  );
}

{products.map(p => <ProductCard key={p.id} {...p} />)}
```

---

## 7.2 — Component Tree ASCII Diagram

```
┌─────────────────────── <App> ────────────────────────────┐
│                                                          │
│   ┌──────── <Header> ─────────────────────┐              │
│   │  <Logo />   <Nav>    <UserMenu>        │              │
│   │             ├─<NavItem>               │              │
│   │             ├─<NavItem>               │              │
│   │             └─<NavItem>               │              │
│   └───────────────────────────────────────┘              │
│                                                          │
│   ┌──────── <Main> ─────────────────────────────────┐    │
│   │  ┌─── <Sidebar> ────┐  ┌─── <Content> ────────┐ │    │
│   │  │  <FilterPanel>   │  │  <PostList>           │ │    │
│   │  │  <TagCloud>      │  │  ├─<PostCard>         │ │    │
│   │  └──────────────────┘  │  ├─<PostCard>         │ │    │
│   │                        │  └─<PostCard>         │ │    │
│   │                        │       ├─<AuthorBadge> │ │    │
│   │                        │       ├─<LikeButton>  │ │    │
│   │                        │       └─<CommentCount>│ │    │
│   │                        └──────────────────────┘ │    │
│   └────────────────────────────────────────────────-┘    │
│                                                          │
│   ┌──────── <Footer> ─────────────────────┐              │
│   │  <FooterLinks />   <Copyright />      │              │
│   └───────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

---

## 7.3 — Smart vs Dumb Components (Container vs Presentational)

This pattern was popularized by Dan Abramov:

| Aspect | Dumb (Presentational) | Smart (Container) |
|---|---|---|
| **Concern** | HOW it looks | WHAT it does |
| **Data** | From props only | Manages own state/fetches |
| **Side effects** | None | Yes (fetch, subscriptions) |
| **Reusability** | High | Low |
| **Examples** | Button, Card, Input | UserListContainer, AuthWrapper |
| **Testing** | Easy (pure function) | Needs mocks |

```javascript
// DUMB / PRESENTATIONAL Component
// Only cares about rendering props
function UserCard({ name, email, avatarUrl }) {
  return (
    <div className="user-card">
      <img src={avatarUrl} alt={name} />
      <h2>{name}</h2>
      <p>{email}</p>
    </div>
  );
}

// SMART / CONTAINER Component
// Fetches data, manages state, passes to dumb components
function UserCardContainer({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => { setUser(data); setLoading(false); });
  }, [userId]);

  if (loading) return <Spinner />;
  return <UserCard name={user.name} email={user.email} avatarUrl={user.avatar} />;
}
```

---

## 7.4 — Atomic Design

A popular methodology for organizing React components:

```
ATOMIC DESIGN HIERARCHY:

Pages
  └─ Templates (page layouts)
       └─ Organisms (complex UI sections, e.g., Header, ProductGrid)
            └─ Molecules (groups of atoms, e.g., SearchBar, ProductCard)
                 └─ Atoms (basic building blocks, e.g., Button, Input, Label)
```

```
atoms/
  Button.jsx
  Input.jsx
  Label.jsx
  Avatar.jsx

molecules/
  SearchBar.jsx   (Input + Button)
  ProductCard.jsx (Avatar + Button + Label)
  FormField.jsx   (Label + Input)

organisms/
  Header.jsx      (Logo + Nav + SearchBar + Avatar)
  ProductGrid.jsx (Grid of ProductCards)

templates/
  MainLayout.jsx  (Header + Sidebar + Content + Footer)

pages/
  HomePage.jsx
  ProductsPage.jsx
  UserProfilePage.jsx
```

---

# 8. Setting Up React

## 8.1 — Create React App (CRA) — Legacy

CRA was React's official starter for years. Now deprecated in favor of Vite.

```bash
# CRA — No longer recommended
npx create-react-app my-app
cd my-app
npm start
```

**Why CRA is now legacy:**
- Very slow development server (based on webpack)
- Large bundle of config files
- No easy way to eject and customize
- Maintained by community now, not Meta

---

## 8.2 — Vite (Current Recommended Approach)

Vite uses **native ES modules** in development (no bundling!) and **Rollup** for production builds.

```bash
# Step 1: Create project
npm create vite@latest my-react-app -- --template react

# Step 2: Navigate to project
cd my-react-app

# Step 3: Install dependencies
npm install

# Step 4: Start dev server
npm run dev

# Step 5: For TypeScript template:
npm create vite@latest my-react-app -- --template react-ts
```

**Why Vite is faster:**
```
CRA (Webpack):
- Bundles ALL your code before serving
- 30-60 second startup on large apps
- Full rebuild on each change (slow HMR)

VITE:
- No bundling in dev mode!
- Serves files as ES modules natively
- Browser fetches what it needs on demand
- <1 second startup always
- HMR updates individual module in milliseconds
```

---

## 8.3 — Complete Folder Structure Explained

```
my-react-app/
│
├── node_modules/          ← All npm packages (never edit, never commit)
│
├── public/                ← Static assets served as-is
│   └── vite.svg           ← Favicon/logo (can add robots.txt, images here)
│
├── src/                   ← Your application source code
│   ├── assets/            ← Images, fonts imported in components
│   │   └── react.svg
│   ├── App.css            ← Styles for App component
│   ├── App.jsx            ← Root component of your application
│   ├── index.css          ← Global styles (applied to entire app)
│   └── main.jsx           ← Entry point — mounts React to DOM
│
├── .eslintrc.cjs          ← ESLint configuration (code quality rules)
├── .gitignore             ← Files to not commit to Git
├── index.html             ← The ONE HTML file (the "single page")
├── package.json           ← Project metadata + dependencies + scripts
├── package-lock.json      ← Exact dependency versions (lock file)
└── vite.config.js         ← Vite configuration
```

---

## 8.4 — Every Key File Explained

### `index.html` — The Shell

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <!-- ↑ Character encoding for international characters -->

    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <!-- ↑ Browser tab favicon -->

    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- ↑ Makes app responsive on mobile devices -->

    <title>Vite + React</title>
    <!-- ↑ Browser tab title -->
  </head>
  <body>
    <div id="root"></div>
    <!-- ↑ THE CRITICAL ELEMENT: React mounts here.
          Initially empty — React fills it in.
          This is the "single page" in SPA. -->

    <script type="module" src="/src/main.jsx"></script>
    <!-- ↑ Entry point script. type="module" enables ES modules.
          Vite processes this and all imports. -->
  </body>
</html>
```

### `src/main.jsx` — The Entry Point

```jsx
// 1. Import React (not needed in React 17+ but good practice)
import React from 'react'

// 2. Import ReactDOM for web rendering
import ReactDOM from 'react-dom/client'

// 3. Import your root component
import App from './App.jsx'

// 4. Import global CSS styles
import './index.css'

// 5. Find the #root div in index.html
// 6. Create a React root (React 18 API)
// 7. Render your App into it
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* ↑ StrictMode: development-only wrapper that:
          - Double-invokes renders to find impure renders
          - Double-invokes effects to find missing cleanups
          - Warns about deprecated APIs
          - Does NOTHING in production */}
    <App />
    {/* ↑ Your entire application as one root component */}
  </React.StrictMode>,
)
```

### `src/App.jsx` — Root Component

```jsx
// Default Vite App.jsx (simplified for learning):
import { useState } from 'react'   // Import useState hook
import reactLogo from './assets/react.svg'   // Import SVG as URL
import './App.css'   // Import component-specific styles

function App() {
  // useState creates a piece of state: count starts at 0
  // setCount is the function to update count
  const [count, setCount] = useState(0)

  return (
    // JSX returned by functional component
    <div>
      <h1>Hello React!</h1>
      <p>Count: {count}</p>
      {/* ↑ {} renders JavaScript expressions */}
      <button onClick={() => setCount(count + 1)}>
        {/* ↑ Event handler as arrow function */}
        Increment
      </button>
    </div>
  )
}

// Must export default so other files can import it
export default App
```

### `package.json` — Project Configuration

```json
{
  "name": "my-react-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  // ↑ Enables ES modules (import/export syntax)

  "scripts": {
    "dev": "vite",
    // ↑ npm run dev → starts development server with HMR

    "build": "vite build",
    // ↑ npm run build → creates optimized production bundle in /dist

    "lint": "eslint . --ext js,jsx --report-unused-disable-directives",
    // ↑ npm run lint → runs ESLint to check code quality

    "preview": "vite preview"
    // ↑ npm run preview → locally preview the production build
  },

  "dependencies": {
    "react": "^18.2.0",
    // ↑ React core library (component logic, VDOM)

    "react-dom": "^18.2.0"
    // ↑ React's DOM renderer (connects React to browser DOM)
    // Note: react-native would be used for mobile instead
  },

  "devDependencies": {
    "@types/react": "^18.2.15",
    // ↑ TypeScript type definitions for React

    "@vitejs/plugin-react": "^4.0.3",
    // ↑ Vite plugin that enables React features (JSX transform, HMR)

    "eslint": "^8.45.0",
    // ↑ Code linting tool

    "vite": "^4.4.5"
    // ↑ Build tool and dev server
  }
}
```

---

## 8.5 — ReactDOM.createRoot() — React 17 vs React 18

```javascript
// REACT 17 (legacy API):
import ReactDOM from 'react-dom';
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
// Limitations:
// - Legacy (blocking) mode only
// - No concurrent features
// - Will show deprecation warnings

// REACT 18 (new API):
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);
// Benefits:
// - Enables Concurrent Mode
// - useTransition, useDeferredValue work
// - Automatic batching of state updates
// - Better Suspense support
```

---

# 9. JSX Deep Dive

## 9.1 — What is JSX?

**JSX** stands for **JavaScript XML**. It is a **syntax extension** for JavaScript that allows you to write HTML-like code inside JavaScript files.

**Important:** JSX is NOT HTML. It is NOT a string. It compiles to plain JavaScript function calls.

```
JSX → (Babel/SWC transforms) → React.createElement() calls → JavaScript Object (VDOM node)
```

---

## 9.2 — JSX Compiles to React.createElement()

```jsx
// What you write (JSX):
const element = (
  <div className="greeting" id="main">
    <h1>Hello, World!</h1>
    <p>Welcome to React</p>
  </div>
);

// What Babel/SWC compiles it to (before React 17):
const element = React.createElement(
  'div',                           // type
  { className: 'greeting', id: 'main' },  // props
  React.createElement('h1', null, 'Hello, World!'), // children[0]
  React.createElement('p', null, 'Welcome to React')  // children[1]
);

// What React.createElement returns (the VDOM object):
{
  $$typeof: Symbol(react.element),   // Internal type marker
  type: 'div',
  key: null,
  ref: null,
  props: {
    className: 'greeting',
    id: 'main',
    children: [
      { type: 'h1', props: { children: 'Hello, World!' } },
      { type: 'p',  props: { children: 'Welcome to React' } }
    ]
  }
}
```

**React 17+ New JSX Transform:**

React 17 introduced a new JSX transform that auto-imports what's needed. You no longer need `import React from 'react'` at the top of every file.

```jsx
// React 17+ (new transform) — what Babel outputs:
import { jsx as _jsx, jsxs as _jsxs } from 'react/jsx-runtime';

const element = _jsxs('div', {
  className: 'greeting',
  id: 'main',
  children: [
    _jsx('h1', { children: 'Hello, World!' }),
    _jsx('p',  { children: 'Welcome to React' })
  ]
});
```

---

## 9.3 — JSX Rules (Comprehensive)

### Rule 1: Single Root Element

```jsx
// ❌ WRONG — Multiple root elements
function App() {
  return (
    <h1>Title</h1>
    <p>Paragraph</p>   // SyntaxError: Adjacent JSX elements must be wrapped
  );
}

// ✅ CORRECT — Wrapped in div
function App() {
  return (
    <div>
      <h1>Title</h1>
      <p>Paragraph</p>
    </div>
  );
}

// ✅ CORRECT — Fragment (no extra DOM node)
function App() {
  return (
    <>
      <h1>Title</h1>
      <p>Paragraph</p>
    </>
  );
}
```

**Why?** `React.createElement()` returns ONE object. You cannot return two values from a function call without wrapping them.

### Rule 2: className Instead of class

```jsx
// ❌ WRONG (class is a reserved word in JavaScript)
<div class="container">...</div>

// ✅ CORRECT
<div className="container">...</div>
```

### Rule 3: htmlFor Instead of for

```jsx
// ❌ WRONG (for is a reserved word in JavaScript — for loops)
<label for="email">Email:</label>

// ✅ CORRECT
<label htmlFor="email">Email:</label>
<input id="email" type="email" />
```

### Rule 4: All Tags Must Close

```jsx
// ❌ WRONG — HTML allows some unclosed tags
<img src="photo.jpg">
<input type="text">
<br>

// ✅ CORRECT — JSX requires self-closing
<img src="photo.jpg" />
<input type="text" />
<br />
```

### Rule 5: camelCase for HTML Attributes

```jsx
// HTML attribute  →  JSX prop
// class           →  className
// for             →  htmlFor
// onclick         →  onClick
// onchange        →  onChange
// tabindex        →  tabIndex
// crossorigin     →  crossOrigin
// maxlength       →  maxLength
// readonly        →  readOnly

// ❌ WRONG
<input tabindex="1" maxlength="100" />

// ✅ CORRECT
<input tabIndex={1} maxLength={100} />
```

### Rule 6: JavaScript Expressions in {} (Curly Braces)

```jsx
const name = 'Alice';
const age = 30;
const isAdmin = true;

function UserInfo() {
  return (
    <div>
      {/* String interpolation */}
      <h1>Hello, {name}!</h1>

      {/* Math expression */}
      <p>Age: {age}</p>
      <p>Next year: {age + 1}</p>

      {/* Ternary expression */}
      <p>Role: {isAdmin ? 'Administrator' : 'User'}</p>

      {/* Function call */}
      <p>Upper name: {name.toUpperCase()}</p>

      {/* JSX inside expression */}
      <div>{isAdmin && <AdminBadge />}</div>

      {/* ❌ These DON'T work in JSX (not expressions): */}
      {/* {if (isAdmin) { return <AdminBadge /> }}  — SYNTAX ERROR */}
      {/* {for (...) {...}}  — SYNTAX ERROR */}
      {/* Use ternary or && instead of if/for */}
    </div>
  );
}
```

### Rule 7: Comments in JSX

```jsx
function Component() {
  return (
    <div>
      {/* This is a JSX comment — correct way */}
      <p>Content</p>
      {/*
        Multi-line comment
        also works like this
      */}
    </div>
  );
}

// Outside JSX → normal JS comments:
// const x = 5; // This is fine
```

### Rule 8: Style is an Object, Not a String

```jsx
// ❌ WRONG — HTML style string
<div style="color: red; font-size: 16px">...</div>

// ✅ CORRECT — JSX style as JavaScript object
<div style={{ color: 'red', fontSize: '16px' }}>...</div>
// Note: Double curly braces {{}}
// Outer {} = JSX expression
// Inner {} = JavaScript object literal
// camelCase properties (fontSize not font-size)
```

---

## 9.4 — JSX Security: Auto-Escaping (XSS Prevention)

**JSX automatically escapes any values inserted into it.** This prevents Cross-Site Scripting (XSS) attacks by default.

```jsx
// ⚠️ What if user inputs malicious code?
const userInput = '<script>alert("XSS attack!")</script>';

function SafeComponent() {
  return (
    <div>
      {/* JSX ESCAPES this automatically — renders as TEXT, not HTML */}
      <p>{userInput}</p>
      {/* Browser displays: <script>alert("XSS attack!")</script> as text
          Script never executes! JSX converts < to &lt;, > to &gt;, etc. */}
    </div>
  );
}
```

**How React escapes values:**

```
String value:   '<script>alert("xss")</script>'
                        ↓
React converts: '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
                        ↓
Browser renders as: <script>alert("xss")</script>  (as visible text, not executed)
```

---

## 9.5 — dangerouslySetInnerHTML (Warning!)

If you MUST inject raw HTML, React provides a deliberately scary API:

```jsx
// ⚠️ DANGEROUS — only use with trusted, sanitized HTML!
function BlogPost({ content }) {
  // content is HTML string from your database
  // ONLY safe if you sanitized it server-side first!
  return (
    <div
      dangerouslySetInnerHTML={{ __html: content }}
      // Why the double {{ }}?
      // Outer {} = JSX expression
      // Inner {} = object with __html property
      // __html: the deliberate misspelling reminds you it's dangerous
    />
  );
}

// The SAFE way: Use a library like DOMPurify to sanitize first
import DOMPurify from 'dompurify';

function SafeBlogPost({ rawContent }) {
  const cleanContent = DOMPurify.sanitize(rawContent); // Remove scripts, event handlers
  return (
    <div dangerouslySetInnerHTML={{ __html: cleanContent }} />
  );
}
```

---

# 10. React Elements vs Components

## 10.1 — React Elements

A **React element** is a plain JavaScript object describing what you want to see on screen. It is the smallest building block in React.

```javascript
// React.createElement() creates a React ELEMENT:
const element = React.createElement('h1', { className: 'title' }, 'Hello');

// Same as JSX:
const element = <h1 className="title">Hello</h1>;

// Both produce this object:
{
  $$typeof: Symbol(react.element),
  type: 'h1',          // STRING for HTML elements
  props: {
    className: 'title',
    children: 'Hello'
  },
  key: null,
  ref: null
}
```

React elements are:
- **Immutable**: once created, you can't change their children or props
- **Cheap**: just objects, no DOM operations
- **Descriptions**: they describe what should be rendered, not the DOM itself

## 10.2 — React Components

A **React Component** is a **function** (or class) that **returns** React elements.

```javascript
// COMPONENT: A function/class
function Welcome(props) {
  // Returns a React ELEMENT:
  return <h1>Hello, {props.name}</h1>;
}

// ELEMENT: An instance/usage of a component:
const element = <Welcome name="Alice" />;

// What this creates:
{
  $$typeof: Symbol(react.element),
  type: Welcome,     // FUNCTION reference for components (vs string for HTML)
  props: {
    name: 'Alice'
  },
  key: null,
  ref: null
}
```

**The critical distinction:**

```
React ELEMENT:
- Plain JavaScript object
- type is a string ('div', 'h1') for HTML
- type is a function/class for components
- Immutable snapshot
- Created by JSX or React.createElement()

React COMPONENT:
- A function or class
- Accepts props → returns elements
- Can have state, lifecycle, side effects
- Can be reused (called multiple times → creates new elements)
- Type name MUST start with uppercase letter!
```

**Why uppercase component names?**

```jsx
// ❌ lowercase → React treats as HTML element (looks for <button> in HTML)
function button() { return <button>Click</button>; }
<button />  // React looks for HTML <button> element — not your component!

// ✅ Uppercase → React knows it's a custom component
function Button() { return <button>Click</button>; }
<Button />  // React calls your Button function
```

---

# 11. React 18 Features

## 11.1 — Overview of React 18 (Released March 2022)

React 18 was the biggest release since React 16 (Fiber). Core theme: **Concurrency**.

Key additions:
1. `createRoot` API (replaces `ReactDOM.render`)
2. Automatic Batching
3. Transitions (`useTransition`, `useDeferredValue`)
4. Suspense improvements
5. New hooks: `useId`, `useSyncExternalStore`
6. Concurrent Mode (stable)
7. Server Components (experimental at launch)

---

## 11.2 — createRoot API

```javascript
// OLD React 17:
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));

// NEW React 18:
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);

// The root object also has:
root.unmount(); // Unmount the React tree (replaces ReactDOM.unmountComponentAtNode)

// Why the change?
// ReactDOM.render was coupled to legacy (synchronous) rendering.
// createRoot opts into concurrent rendering → enables all React 18 features.
```

---

## 11.3 — Automatic Batching

**Batching** = grouping multiple state updates into a single re-render.

```javascript
// REACT 17: Only batched in React event handlers
// Outside (setTimeout, promises, native events) — each setState = one re-render

function handleClick() {
  setCount(c => c + 1); // In React 17: batched (1 re-render total)
  setFlag(f => !f);     // In React 17: batched (1 re-render total)
}

// But:
setTimeout(() => {
  setCount(c => c + 1); // REACT 17: re-render 1
  setFlag(f => !f);     // REACT 17: re-render 2 (not batched!)
}, 1000);

// REACT 18: Automatic batching EVERYWHERE:
setTimeout(() => {
  setCount(c => c + 1); // REACT 18: batched
  setFlag(f => !f);     // REACT 18: batched (only 1 re-render total!)
}, 1000);

fetch('/api/data').then(() => {
  setData(newData);     // REACT 18: batched
  setLoading(false);    // REACT 18: batched (1 re-render total)
});
```

**If you ever need to opt OUT of batching** (rare):

```javascript
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1); // Immediately triggers re-render
});
// DOM updated here
flushSync(() => {
  setFlag(f => !f);     // Another immediate re-render
});
```

---

## 11.4 — Transitions (useTransition, useDeferredValue)

**The problem:** Some updates are urgent (typing), some are non-urgent (filtering a huge list).

```javascript
// WITHOUT transitions:
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(allItems);

  function handleChange(e) {
    setQuery(e.target.value);         // Urgent: update input
    setResults(filterItems(e.target.value)); // Non-urgent: filter (expensive!)
    // Both run at same priority → typing feels laggy if filter is slow
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      <ResultsList results={results} />
    </>
  );
}
```

### useTransition

```javascript
import { useState, useTransition } from 'react';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(allItems);
  const [isPending, startTransition] = useTransition();
  // isPending: boolean — true while the transition is in progress
  // startTransition: function — wraps non-urgent updates

  function handleChange(e) {
    setQuery(e.target.value); // URGENT: happens immediately (keeps input responsive)

    startTransition(() => {
      // NON-URGENT: React can interrupt/defer this
      setResults(filterItems(e.target.value));
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}  {/* Show loading while transition runs */}
      <div style={{ opacity: isPending ? 0.5 : 1 }}>
        <ResultsList results={results} />
      </div>
    </>
  );
}
```

### useDeferredValue

```javascript
import { useState, useDeferredValue } from 'react';

function SearchPage() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  // deferredQuery: "lags behind" query
  // query updates immediately (urgent)
  // deferredQuery updates after React has time (non-urgent)
  // No isPending — use comparison for loading state

  const isStale = query !== deferredQuery; // True while deferred value is catching up

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        <ResultsList query={deferredQuery} />  {/* Uses stale value until caught up */}
      </div>
    </>
  );
}
```

**useTransition vs useDeferredValue:**
- `useTransition`: You control WHEN the transition happens (wrap the setter)
- `useDeferredValue`: You defer a VALUE (useful when you don't control the setter, e.g., from a prop)

---

## 11.5 — Suspense Improvements

```jsx
// React 18 enables Suspense for data fetching (with supported libraries)
// Previously Suspense only worked with React.lazy() for code splitting

// React.lazy() + Suspense (code splitting):
const HeavyChart = React.lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<Skeleton />}>
      {/* HeavyChart.js is NOT downloaded until this renders */}
      <HeavyChart />
    </Suspense>
  );
}

// React 18: Suspense + data fetching (with libraries like React Query, Relay):
function UserProfile({ userId }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserData userId={userId} />  {/* Suspends while fetching */}
    </Suspense>
  );
}

// Nested Suspense (waterfall vs parallel):
function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Header />
      <Suspense fallback={<ContentSkeleton />}>
        <Content />
        <Suspense fallback={<SidebarSkeleton />}>
          <Sidebar />
        </Suspense>
      </Suspense>
    </Suspense>
  );
}
```

---

## 11.6 — React 18 Strict Mode Double-Render

React 18 Strict Mode makes an important change:

```
REACT 18 STRICT MODE BEHAVIOR (Development only):

1. Component renders → checks for issues
2. Component renders AGAIN → verifies first render was pure
3. If state differs between renders → warns about impure render

EFFECT BEHAVIOR:
1. Component mounts
2. Effects run
3. Effects CLEANUP runs (simulating unmount)
4. Effects run AGAIN (simulating remount)
→ Tests that your cleanup properly undoes effects

WHY: Upcoming React feature (Offscreen API / Activity)
will mount/unmount components multiple times for performance.
Strict Mode ensures your code handles this correctly.
```

```javascript
// This code BREAKS in Strict Mode (reveals a bug):
let count = 0; // External mutable variable (bad!)

function Counter() {
  count++; // This runs TWICE in Strict Mode dev
  // After double render: count = 2, not 1!
  // Bug revealed: render must be pure (no side effects)
  return <div>{count}</div>;
}

// CORRECT: Use state, not external mutable variables
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      {count}
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  );
}
```

---

# 12. Chapter Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CHAPTER 1 SUMMARY                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WHAT IS REACT?                                                     │
│  ├─ JavaScript library (not framework) for building UIs             │
│  ├─ Created by Facebook (2011/2013), open source                    │
│  └─ Core: Declarative, Component-Based, Learn Once Write Anywhere   │
│                                                                     │
│  PROBLEMS REACT SOLVES                                              │
│  ├─ Eliminates manual DOM manipulation                              │
│  ├─ Single source of truth for state                                │
│  └─ One-way data flow prevents sync bugs                            │
│                                                                     │
│  VIRTUAL DOM                                                        │
│  ├─ Lightweight JS object representing real DOM                     │
│  ├─ Fast to create and compare                                      │
│  └─ MYTH: Not always faster than manual DOM (but more maintainable) │
│                                                                     │
│  RECONCILIATION                                                     │
│  ├─ O(n) diffing (not O(n³))                                        │
│  ├─ Two assumptions: type changes = rebuild, keys = identity        │
│  └─ State change → New VDOM → Diff → Patch                         │
│                                                                     │
│  FIBER                                                              │
│  ├─ Introduced React 16, enables interruptible rendering            │
│  ├─ Render phase (interruptible) + Commit phase (synchronous)       │
│  └─ Foundation for Concurrent Mode                                  │
│                                                                     │
│  JSX                                                                │
│  ├─ Compiles to React.createElement()                               │
│  ├─ Rules: single root, className, htmlFor, camelCase, self-close   │
│  └─ Auto-escapes values (XSS protection by default)                 │
│                                                                     │
│  REACT 18                                                           │
│  ├─ createRoot (concurrent mode)                                    │
│  ├─ Automatic batching everywhere                                   │
│  └─ Transitions (useTransition, useDeferredValue)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 13. Top 25 Interview Questions — Chapter 1

## Beginner Questions

**Q1: What is React? Is it a library or a framework?**

**Answer:** React is an open-source **JavaScript library** for building user interfaces, created by Facebook (Meta) in 2013. It is specifically a **library** (not a framework) because:
- React handles only the View layer (UI rendering)
- You choose your own routing, state management, HTTP client
- You call React's APIs; React doesn't dictate your app structure
- In contrast, Angular is a framework that provides routing, HTTP, forms — all built-in

---

**Q2: What is the Virtual DOM? How does it work?**

**Answer:** The Virtual DOM (VDOM) is a lightweight JavaScript object representation of the real browser DOM. It works in three steps:
1. When state/props change, React creates a **new VDOM tree**
2. React **compares** (diffs) the new VDOM with the previous VDOM
3. React **patches** only the changed parts into the real DOM

This is efficient because comparing JavaScript objects is much faster than comparing actual DOM nodes (which trigger layout, style recalculation, and painting).

---

**Q3: What is JSX? Why do we use it?**

**Answer:** JSX (JavaScript XML) is a syntax extension that lets you write HTML-like code in JavaScript. It compiles to `React.createElement()` calls via Babel/SWC. We use it because:
- It makes component structure visually clear (reads like HTML)
- It's more readable than raw `React.createElement()` calls
- It enables static analysis and IDE tooling
- Security: automatically escapes values, preventing XSS attacks

---

**Q4: What are the rules of JSX?**

**Answer:**
1. Must return a single root element (wrap in `<div>` or `<>`)
2. Use `className` instead of `class`
3. Use `htmlFor` instead of `for`
4. All tags must be self-closed (`<img />`, `<input />`)
5. Attributes use camelCase (`onClick`, `tabIndex`, `maxLength`)
6. Expressions in `{}` curly braces
7. Style is an object: `style={{ color: 'red', fontSize: '16px' }}`
8. Comments use `{/* ... */}` inside JSX

---

**Q5: What is reconciliation in React?**

**Answer:** Reconciliation is the algorithm React uses to determine how to update the real DOM when state or props change. It involves:
1. Creating a new Virtual DOM tree after state change
2. Comparing it with the previous VDOM (diffing)
3. Computing the minimum set of DOM operations
4. Applying those operations to the real DOM

React's diffing is O(n) (linear) rather than O(n³) (naive tree comparison) by using two heuristics: (1) different element types produce different trees, (2) keys help identify list element identity across renders.

---

## Intermediate Questions

**Q6: What is React Fiber? Why was it introduced?**

**Answer:** React Fiber is the complete reimplementation of React's reconciliation algorithm introduced in React 16. It was introduced to solve the problem of the **old stack reconciler** which was synchronous and couldn't be interrupted — causing dropped frames and laggy user interactions on complex apps.

Fiber makes rendering **interruptible** by representing each component as a "fiber node" (JavaScript object) in a linked list, rather than using the JavaScript call stack. This enables:
- Pausing and resuming rendering work
- Priority-based scheduling (urgent updates preempt non-urgent ones)
- Concurrent Mode (React 18)
- useTransition and useDeferredValue

---

**Q7: Explain the two phases of React Fiber's work.**

**Answer:**
1. **Render Phase (interruptible):** React traverses the component tree, calls function components, computes new VDOM, performs diffing. This phase can be paused, aborted, or restarted based on priority. It runs "off-screen" (no DOM mutations). Because it can run multiple times, it must be **pure** (no side effects).

2. **Commit Phase (synchronous):** React applies the computed changes to the real DOM. This phase cannot be interrupted and always runs to completion. It has three sub-phases: "before mutation," "mutation" (actual DOM changes), and "layout" (useLayoutEffect, lifecycle methods).

---

**Q8: Is the Virtual DOM always faster than the Real DOM? Explain.**

**Answer:** No — the Virtual DOM is not inherently always faster. Direct, expert manual DOM manipulation can be faster. The VDOM is an optimization over **naive full re-renders** (clear everything and rebuild), not over careful manual updates.

Rich Harris (Svelte creator) demonstrated that Svelte's approach (compile-time optimization, no VDOM) outperforms React in benchmarks. React's value is developer experience, declarative code, and "fast enough" performance for most applications — not maximum raw performance.

---

**Q9: What is the difference between SPA and MPA?**

**Answer:** 
- **SPA** (Single Page Application): One HTML file served once. Navigation handled by JavaScript — URL changes via History API but no full page reload. Great UX, hard SEO, slower initial load. Examples: Gmail, React apps.
- **MPA** (Multi Page Application): Each navigation is a new HTTP request returning a new HTML page. Great SEO, page flash on navigation, natural browser history. Examples: Traditional WordPress, news sites.

Modern solution: SSR/SSG (Next.js, Remix) — combine benefits of both.

---

**Q10: What did React 18 introduce?**

**Answer:** React 18 introduced:
1. **`createRoot` API** — enables Concurrent Mode
2. **Automatic Batching** — all state updates batch everywhere (not just React event handlers)
3. **`useTransition`** — mark updates as non-urgent to keep UI responsive
4. **`useDeferredValue`** — defer expensive renders
5. **`useId`** — stable, unique IDs for SSR hydration
6. **`useSyncExternalStore`** — safely read external stores in concurrent mode
7. **Suspense improvements** — better support for data fetching
8. **Strict Mode changes** — double-invokes effects to catch cleanup bugs

---

## Advanced Questions

**Q11: How does React's O(n) diffing algorithm work? What are the two assumptions?**

**Answer:** React achieves O(n) complexity through two heuristics:

1. **Different types produce different trees:** If the element type changes (e.g., `<div>` to `<span>`), React destroys the entire subtree and builds a new one. This avoids costly "can we reuse?" analysis.

2. **Keys signal stable identity:** In lists, keys tell React which elements are the same across renders. Without keys, React compares by position (inaccurate). With stable unique keys, React can correctly identify moved/added/removed items.

The algorithm walks both trees level-by-level (breadth-first), comparing nodes at the same depth. It never tries to match nodes across different levels (a valid optimization for most real-world UI structures).

---

**Q12: Why should you NOT use array indices as React keys?**

**Answer:** Using array indices as keys causes React to misidentify elements when the list order changes:

```javascript
// List: ['Alice', 'Bob', 'Carol'] → keys 0, 1, 2
// After removing 'Alice': ['Bob', 'Carol'] → keys 0, 1
// React thinks: "key 0 was Alice, now it's Bob" → updates Alice's DOM to show Bob
// React thinks: "key 1 was Bob, now it's Carol" → updates Bob's DOM to show Carol
// React thinks: "key 2 is gone" → removes Carol's DOM
// Result: unnecessary updates + potential state bugs

// If 'Alice' had a text input with typed content, and we remove Alice,
// Bob's component would inherit Alice's input state!
```

Use stable, unique IDs (database IDs, UUID) as keys. Index is OK only if: list never reorders, never filters, items have no state.

---

**Q13: What is Concurrent Mode and how does React 18 enable it?**

**Answer:** Concurrent Mode is React's ability to work on multiple versions of the UI simultaneously — preparing new renders "in the background" while keeping the current UI responsive.

Before Concurrent Mode, React rendered synchronously: once it started, it couldn't stop until the entire tree was processed. With Concurrent Mode:
- Rendering work can be interrupted by more urgent updates
- React can discard half-finished work if it becomes stale
- React can "pre-render" future UI states in the background

React 18 enables Concurrent Mode by using `createRoot()` instead of `ReactDOM.render()`. The concurrent features (`useTransition`, `useDeferredValue`, Suspense) all require `createRoot`.

---

## Tricky/Scenario Questions

**Q14: What will happen if you write `<component />` (lowercase) vs `<Component />` (uppercase) in JSX?**

**Answer:** 
- `<component />` — React treats this as an **HTML element** named "component." Since no such HTML element exists, it renders as `<component></component>` in the DOM (a custom HTML element). Your function is never called.
- `<Component />` — React treats this as a **custom component** and calls your `Component` function/class.

This is why React component names MUST start with uppercase.

---

**Q15: In React 18 Strict Mode, why do effects run twice in development?**

**Answer:** React 18 Strict Mode intentionally:
1. Mounts the component
2. Runs effects
3. Runs cleanup functions (simulating unmount)
4. Runs effects again (simulating remount)

This behavior was introduced to prepare for the upcoming **Offscreen API** (a.k.a. Activity), where React will unmount and remount components to preserve UI state while hiding them off-screen (for performance). By double-running effects in development, React ensures that your cleanup function properly reverses the effect. If your effect relies on "running only once," that's a bug the double-invocation will expose.

---

**Q16: Can you render `false`, `null`, `undefined`, or `0` in JSX? What actually shows?**

**Answer:**
```jsx
<div>{false}</div>   → renders nothing (falsy, React ignores)
<div>{null}</div>    → renders nothing (React ignores)
<div>{undefined}</div> → renders nothing (React ignores)
<div>{0}</div>       → renders the NUMBER 0 (0 is falsy but React renders it!)
<div>{''}</div>      → renders nothing (empty string)
<div>{NaN}</div>     → renders "NaN" (a string)

COMMON BUG:
{count && <Component />}
// If count = 0, renders "0" not nothing!
// Fix: {count > 0 && <Component />}
// Or:  {!!count && <Component />}
// Or:  {count ? <Component /> : null}
```

---

**Q17: What is `dangerouslySetInnerHTML` and when is it necessary?**

**Answer:** `dangerouslySetInnerHTML` is React's replacement for DOM's `innerHTML` property. It allows injecting raw HTML strings into a component.

Use cases:
- Rendering rich text content from a CMS (with HTML formatting)
- Displaying sanitized content from a WYSIWYG editor
- Rendering HTML email previews

Why it's "dangerous": It bypasses React's XSS protection. Any script tags in the HTML string will execute. You MUST sanitize the HTML first using a library like DOMPurify.

Never use it with untrusted user input without sanitization.

---

**Q18: What is automatic batching in React 18? Give an example.**

**Answer:** Automatic batching groups multiple `setState` calls into a single re-render. In React 17, this only worked inside React event handlers. React 18 extends batching to ALL contexts: setTimeout, Promise `.then()`, native DOM events, etc.

```javascript
// React 18 — only ONE re-render happens:
setTimeout(() => {
  setA(1); // Batched
  setB(2); // Batched → 1 re-render total
}, 0);

fetch('/api').then(() => {
  setData(d);   // Batched
  setLoading(false); // Batched → 1 re-render total
});
```

Use `flushSync` from 'react-dom' to opt out of batching when needed (rare).

---

## Conceptual/Why Questions

**Q19: Why is React's data flow one-directional? What problem does it solve?**

**Answer:** One-directional data flow means data flows from parent to child via props, and events flow up from child to parent via callbacks. This solves:

1. **Predictability:** The cause of any UI change can always be traced to a single `setState` call
2. **Debuggability:** With two-way binding, a state change in A triggers B, which updates C, which triggers A again — circular chains are impossible to debug
3. **The Facebook chat bug:** Two-way binding between multiple models caused unsynchronized state

---

**Q20: Why does React use `className` instead of `class`?**

**Answer:** JSX is compiled to JavaScript. In JavaScript, `class` is a reserved keyword (used for defining classes). If JSX used `class`, it would conflict syntactically. Therefore, React uses `className` (which is actually the DOM property name for the element's CSS class — `element.className`). This is consistent: JSX attribute names follow the DOM property names, not HTML attribute names.

---

**Q21: What happens internally when you call `setState`?**

**Answer:**
1. React marks the component as needing re-render (schedules work)
2. React does NOT immediately update state — it queues the update
3. During the render phase, React calls the function component
4. The new state value is computed from the update queue
5. React re-renders the component with the new state
6. The new VDOM is compared with the previous (diffing)
7. Only changed DOM nodes are updated (commit phase)

This is why state changes are "asynchronous" — `console.log(count)` after `setCount(count + 1)` will show the OLD value.

---

**Q22: What are React Fragments and why do we need them?**

**Answer:** React requires components to return a single root element. Fragments allow returning multiple elements without adding an extra DOM node.

Without Fragments: `<div>` wrappers pollute the DOM tree (breaks flexbox layouts, CSS selectors, etc.)

With Fragments:
```jsx
return (
  <>
    <td>Name</td>
    <td>Age</td>
  </>
);
// vs wrong:
return (
  <div>  ← inserts <div> inside <tr>, breaking HTML table structure!
    <td>Name</td>
    <td>Age</td>
  </div>
);
```

Long-form `<React.Fragment key={id}>` is needed when using keys on Fragment lists.

---

**Q23: How does React's `key` prop help with reconciliation?**

**Answer:** The `key` prop gives React a stable identity for elements in a list. Without keys, React identifies list items by position. With keys, React can:
- Match items by key across renders
- Know when an item moved vs. was replaced
- Avoid unnecessary DOM mutations (just reorder existing nodes)
- Preserve component state correctly

React uses an internal map (key → fiber node) to look up existing elements. When a key is found in the new list, React updates that existing fiber instead of creating a new one.

---

**Q24: What is the difference between React Elements and React Components?**

**Answer:**
- **React Element:** A plain JavaScript object (created by JSX or `React.createElement`) describing what to render. Immutable. Has `type` (string for HTML, function for components), `props`, `key`, `ref`.
- **React Component:** A JavaScript function or class that accepts props and returns React elements. It has its own lifecycle, can maintain state, and can produce side effects.

An element is like a "blueprint instance" — it says "render a Button with these props." The component (Button) is the blueprint itself — the definition of how to render.

---

**Q25: Explain `useTransition` with a real-world use case.**

**Answer:** `useTransition` is used when you have a state update that's non-urgent and could make the UI feel laggy if it blocks rendering.

Real-world: Search-as-you-type with a large dataset.

```javascript
const [isPending, startTransition] = useTransition();

function handleSearch(query) {
  // URGENT: Update input (must feel instant)
  setInputValue(query);

  // NON-URGENT: Filter 10,000 items (can lag slightly)
  startTransition(() => {
    setFilteredResults(expensiveFilter(query));
  });
}
```

`isPending` is `true` while the transition is processing — you can show a loading indicator or dim the results. The input feels responsive because it's not blocked by the expensive filtering operation.

---

# 14. Output/Render Prediction Exercises

**Exercise 1: What does this render?**

```jsx
function App() {
  const items = [];
  return (
    <div>
      {items.length && <ul><li>Item</li></ul>}
    </div>
  );
}
```

**Answer:** Renders `<div>0</div>` — displays the number **0** in the browser!

`items.length` = 0. `0 && <ul>...</ul>` = 0 (falsy short-circuit returns the left operand). React renders 0 as text. Fix: `{items.length > 0 && <ul>...</ul>}` or `{!!items.length && <ul>...</ul>}`.

---

**Exercise 2: How many times does this component render on button click?**

```jsx
function Counter() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);

  const handleClick = () => {
    setA(a + 1);
    setB(b + 1);
  };

  console.log('Counter rendered');

  return <button onClick={handleClick}>Click</button>;
}
```

**Answer (React 18):** `Counter rendered` logs **1 time** per click.

React 18 automatic batching groups both `setA` and `setB` into a single re-render, even though they're called sequentially. In React 17, inside a React event handler, they would also batch (1 render). In React 17 in a `setTimeout`, they would trigger 2 renders.

---

**Exercise 3: What happens in Strict Mode?**

```jsx
// StrictMode is enabled (default in Vite template)
function Counter() {
  const [count, setCount] = useState(0);
  console.log('Render: count =', count);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

**Answer (Development mode, React 18 Strict Mode):**

Initial render: `Render: count = 0` logs **twice** (Strict Mode double-invokes renders).

After clicking: `Render: count = 1` logs **twice**.

In production: Each logs **once** (Strict Mode is dev-only).

---

**Exercise 4: What is the output of the following key change?**

```jsx
function App() {
  const [swap, setSwap] = useState(false);
  return (
    <div>
      {swap ? <input key="b" placeholder="B" /> : <input key="a" placeholder="A" />}
      <button onClick={() => setSwap(s => !s)}>Swap</button>
    </div>
  );
}
```

**Answer:** When "Swap" is clicked:
- The `key` changes from `"a"` to `"b"` (or vice versa)
- React sees a different key → **destroys the old input** (loses any typed text) → **creates a new input**
- If you type "hello" in input A, click Swap, the text is gone
- Keys are used to **reset** component state intentionally (key change = fresh mount)

---

**Exercise 5: What does this JSX compile to?**

```jsx
const el = <MyButton color="blue" onClick={handleClick}>Click me</MyButton>;
```

**Answer:**

```javascript
const el = React.createElement(
  MyButton,             // type = function reference (uppercase → component)
  {
    color: 'blue',      // props
    onClick: handleClick
  },
  'Click me'           // children prop
);
// Result: { type: MyButton, props: { color: 'blue', onClick: handleClick, children: 'Click me' }, key: null, ref: null }
```

---

# 15. Coding Exercises

## Exercise 1: Build a Simple Counter (Covers: useState, JSX, events)

```jsx
// Build a counter with: increment, decrement, reset buttons
// Constraint: Count cannot go below 0

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Counter: {count}</h1>
      <button
        onClick={() => setCount(c => c + 1)}
        style={{ margin: '0 10px' }}
      >
        +1
      </button>
      <button
        onClick={() => setCount(c => Math.max(0, c - 1))}
        style={{ margin: '0 10px' }}
      >
        -1
      </button>
      <button
        onClick={() => setCount(0)}
        style={{ margin: '0 10px' }}
      >
        Reset
      </button>
      {count >= 10 && <p style={{ color: 'green' }}>Count is 10 or more!</p>}
    </div>
  );
}

export default Counter;
```

---

## Exercise 2: Explain the Virtual DOM Concept in Code

```jsx
// Demonstrate how VDOM enables targeted updates
// Run this and check the Chrome DevTools "Elements" tab
// Only the changed span should flash/update

import { useState } from 'react';

function VDOMDemo() {
  const [count, setCount] = useState(0);

  // React only updates the <span> containing count
  // The h1, p, and button elements do NOT get re-created in the DOM
  return (
    <div>
      <h1>Virtual DOM Demo</h1>
      <p>This paragraph never changes — React knows not to update it</p>
      <p>Count: <span style={{ fontWeight: 'bold', color: 'red' }}>{count}</span></p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment (only the count span updates in DOM!)
      </button>
    </div>
  );
}

export default VDOMDemo;
```

---

## Exercise 3: Create a Component Tree

```jsx
// Build a blog layout using component tree architecture

// Atom
function Tag({ label }) {
  return (
    <span style={{
      background: '#e0f0ff',
      padding: '2px 8px',
      borderRadius: '4px',
      fontSize: '12px',
      marginRight: '4px'
    }}>
      {label}
    </span>
  );
}

// Molecule
function ArticleCard({ title, excerpt, tags, date }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
      <h2 style={{ margin: '0 0 8px' }}>{title}</h2>
      <p style={{ color: '#666' }}>{excerpt}</p>
      <div>
        {tags.map(tag => <Tag key={tag} label={tag} />)}
      </div>
      <small style={{ color: '#999' }}>{date}</small>
    </div>
  );
}

// Organism
function ArticleList({ articles }) {
  return (
    <div>
      {articles.map(article => (
        <ArticleCard key={article.id} {...article} />
      ))}
    </div>
  );
}

// Page
function BlogPage() {
  const articles = [
    { id: 1, title: 'React 18 Features', excerpt: 'Concurrent mode, transitions...', tags: ['React', 'JavaScript'], date: 'Jan 1, 2024' },
    { id: 2, title: 'Virtual DOM Explained', excerpt: 'How React renders efficiently...', tags: ['React', 'Performance'], date: 'Jan 5, 2024' },
  ];

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Blog</h1>
      <ArticleList articles={articles} />
    </div>
  );
}

export default BlogPage;
```

---

## Exercise 4: JSX Conditional Rendering Patterns

```jsx
// Demonstrate all conditional rendering patterns

import { useState } from 'react';

function ConditionalDemo() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [count, setCount] = useState(0);
  const [items] = useState(['Apple', 'Banana', 'Cherry']);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Conditional Rendering Patterns</h2>

      {/* Pattern 1: if/else with element variable */}
      {(() => {
        if (isLoggedIn) {
          return <p style={{ color: 'green' }}>✓ Welcome, User!</p>;
        } else {
          return <p style={{ color: 'red' }}>✗ Please log in</p>;
        }
      })()}

      {/* Pattern 2: Ternary */}
      <button onClick={() => setIsLoggedIn(l => !l)}>
        {isLoggedIn ? 'Log Out' : 'Log In'}
      </button>

      {/* Pattern 3: && operator */}
      {isLoggedIn && <p>This only shows when logged in</p>}

      {/* Pattern 4: Common PITFALL with 0 */}
      <p>Count: {count}</p>
      {/* BUG: renders "0" when count is 0 */}
      <p>Bug: {count && <strong>Count is non-zero</strong>}</p>
      {/* FIX: use boolean coercion */}
      <p>Fix: {count > 0 && <strong>Count is non-zero</strong>}</p>

      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset to 0</button>

      {/* Pattern 5: Nullish coalescing */}
      <p>Items: {items.length ?? 'No items'}</p>
    </div>
  );
}

export default ConditionalDemo;
```

---

## Exercise 5: JSX List Rendering with Keys

```jsx
// Demonstrate proper key usage and why it matters

import { useState } from 'react';

function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React', done: false },
    { id: 2, text: 'Build Projects', done: false },
    { id: 3, text: 'Get a Job', done: false },
  ]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (input.trim()) {
      setTodos(prev => [
        { id: Date.now(), text: input, done: false },
        ...prev  // Add at beginning — demonstrates key importance!
      ]);
      setInput('');
    }
  };

  const toggleTodo = (id) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  };

  const deleteTodo = (id) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>Todo List (with proper keys)</h2>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addTodo()}
          placeholder="Add todo..."
          style={{ flex: 1, padding: '8px' }}
        />
        <button onClick={addTodo}>Add</button>
      </div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map(todo => (
          // key = stable unique ID (not index!)
          // If we used index, deleting from beginning would
          // reassign keys and cause state bugs
          <li key={todo.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.done ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => deleteTodo(todo.id)} style={{ marginLeft: 'auto' }}>×</button>
          </li>
        ))}
      </ul>
      <p>{todos.filter(t => !t.done).length} remaining</p>
    </div>
  );
}

export default TodoList;
```

---

# 16. Multiple Choice Questions (MCQs)

**Q1:** What does JSX compile to?
- A) HTML
- B) `React.createElement()` calls ✅
- C) JSON
- D) TypeScript

---

**Q2:** Which of the following is NOT a valid reason React uses `className` instead of `class`?
- A) `class` is a reserved word in JavaScript
- B) DOM property is `className`, not `class`
- C) HTML requires `class` ✅ (HTML uses `class`, but JSX follows DOM APIs)
- D) To distinguish JSX from HTML

**Explanation:** Actually, `class` IS the HTML attribute. JSX uses `className` because in JavaScript, `class` is reserved for ES6 classes, and the DOM property is `element.className`. Options A, B, and D are all valid reasons.

---

**Q3:** React Fiber was introduced in which version?
- A) React 14
- B) React 15
- C) React 16 ✅
- D) React 18

---

**Q4:** Which of the following CORRECTLY describes the Virtual DOM?
- A) A faster version of the real DOM provided by browsers
- B) A JavaScript object representation of the real DOM ✅
- C) A shadow DOM implementation
- D) A cached version of the real DOM

---

**Q5:** In React 18, automatic batching applies to:
- A) Only React event handlers
- B) React event handlers and setTimeout
- C) All state updates everywhere ✅
- D) Only async functions

---

**Q6:** What is the complexity of React's diffing algorithm?
- A) O(n³)
- B) O(n²)
- C) O(n log n)
- D) O(n) ✅

---

**Q7:** What does `<React.StrictMode>` do in production?
- A) Enables additional safety checks
- B) Doubles all renders
- C) Nothing — it's development-only ✅
- D) Enables concurrent mode

---

**Q8:** Which of the following would cause a COMPLETE re-mount (destroy and recreate) of a component?
- A) A prop value changes
- B) State updates
- C) The component's `key` prop changes ✅
- D) Context value changes

---

**Q9:** What will `{0 && <Component />}` render?
- A) Nothing (0 is falsy)
- B) `<Component />`
- C) The number `0` ✅
- D) `false`

---

**Q10:** Which React 18 API replaces `ReactDOM.render()`?
- A) `ReactDOM.createRoot().render()` ✅
- B) `React.createRoot()`
- C) `ReactDOM.hydrateRoot()`
- D) `ReactDOM.mount()`

---

> **End of Chapter 1 — React Introduction**

---

*Next Chapter: Components, Props, State & Rendering →*

---
**Chapter Word Count:** ~8,500 words | **Code Examples:** 60+ | **Interview Questions:** 25 | **MCQs:** 10 | **Exercises:** 5+
