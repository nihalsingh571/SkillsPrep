# Chapter 1: How JavaScript Works — The Complete Deep Dive

> **"To master JavaScript, you must first understand what JavaScript IS — not just how to write it, but how it lives, breathes, and executes inside your computer."**

---

## Table of Contents

1. [Introduction to JavaScript](#introduction)
2. [History of JavaScript](#history)
3. [How JavaScript Works — The Big Picture](#big-picture)
4. [Browser Architecture](#browser-architecture)
5. [JavaScript Engine Deep Dive](#js-engine)
6. [V8 Engine Internals](#v8)
7. [JavaScript Runtime Environment](#runtime)
8. [Execution Context](#execution-context)
9. [Call Stack](#call-stack)
10. [Memory: Heap vs Stack](#memory)
11. [Garbage Collection](#garbage-collection)
12. [Event Loop](#event-loop)
13. [Web APIs](#web-apis)
14. [Microtask vs Macrotask Queue](#queues)
15. [Chapter Summary & Interview Prep](#summary)

---

## 1. Introduction to JavaScript {#introduction}

### What is JavaScript?

JavaScript is a **high-level, interpreted, single-threaded, dynamically-typed, prototype-based, multi-paradigm programming language**.

Let's break that down word by word:

| Term | What it means |
|------|--------------|
| **High-level** | You don't manage memory manually (like in C/C++). The language handles memory for you. |
| **Interpreted** | Code is executed line by line, not compiled to machine code beforehand (though modern JS engines do JIT compile — more on this later). |
| **Single-threaded** | JS has ONE call stack. It can do ONE thing at a time. |
| **Dynamically-typed** | Variables don't have fixed types. `let x = 5; x = "hello";` is valid. |
| **Prototype-based** | Objects inherit from other objects via prototype chains (not classical class-based inheritance, though ES6 classes are syntactic sugar over this). |
| **Multi-paradigm** | You can write in **procedural**, **object-oriented**, OR **functional** style. |

### What Can JavaScript Do?

**In the Browser (Client-Side):**
- Manipulate HTML/CSS dynamically (DOM manipulation)
- Handle user interactions (clicks, form input, keyboard)
- Make API calls (fetch data without page reload)
- Create animations and games
- Build complete Single Page Applications (SPAs)

**On the Server (Node.js):**
- Build REST APIs and web servers
- Handle file system operations
- Interact with databases
- Run scripts and automation

**Everywhere Else:**
- Mobile apps (React Native)
- Desktop apps (Electron)
- IoT devices
- Machine Learning (TensorFlow.js)

### JavaScript vs Java

These are **completely different languages** despite the similar name. The name was a marketing decision in 1995.

| Feature | JavaScript | Java |
|---------|-----------|------|
| **Type System** | Dynamic (types checked at runtime) | Static (types checked at compile time) |
| **Compilation** | Interpreted + JIT compiled | Compiled to bytecode, run on JVM |
| **Threading** | Single-threaded | Multi-threaded |
| **Memory** | Automatic GC | Automatic GC |
| **Typing** | Weakly typed | Strongly typed |
| **Paradigm** | Multi-paradigm | Primarily OOP |
| **Running Environment** | Browser, Node.js | JVM (Java Virtual Machine) |
| **Syntax Origin** | C, Java (influenced by) | C++, Simula |
| **Objects** | Prototype-based | Class-based |
| **`null` type** | `typeof null === 'object'` (bug!) | null is a reference type |

---

## 2. History of JavaScript {#history}

Understanding history explains WHY JavaScript is the way it is — including its quirks and design decisions.

### Timeline

```
1994 — Netscape Navigator browser launches, dominates the web
1995 — Brendan Eich at Netscape creates JavaScript in 10 DAYS
         ↓ Originally called "Mocha", then "LiveScript", then "JavaScript"
         ↓ The Java name was a marketing move (Java was trendy in 1995)
1996 — Microsoft creates JScript (reverse-engineered JS) for IE
         ↓ The "Browser Wars" begin
1997 — JavaScript standardized as ECMAScript (ES1) by ECMA International
         ↓ TC39 committee formed to govern future development
1998 — ES2 (minor updates)
1999 — ES3 (regex, try/catch — the foundation everyone coded on for years)
2009 — ES5 (strict mode, JSON, Array methods like forEach/map/filter)
2009 — Node.js created by Ryan Dahl — JS on the server!
2015 — ES6 / ES2015 — THE BIG LEAP
         ↓ let/const, arrow functions, classes, modules, promises, template literals
         ↓ Destructuring, spread operator, generators, Symbol
2016 — ES7: Array.includes(), exponentiation operator (**)
2017 — ES8: async/await, Object.entries/values, SharedArrayBuffer
2018 — ES9: Rest/Spread for objects, Promise.finally(), async iteration
2019 — ES10: Array.flat(), flatMap(), Object.fromEntries(), optional catch
2020 — ES11: Optional chaining (?.), nullish coalescing (??), BigInt, Promise.allSettled
2021 — ES12: String.replaceAll(), Promise.any(), logical assignment operators
2022 — ES13: Array.at(), Object.hasOwn(), top-level await, class fields
2023 — ES14: Array.toSorted(), toReversed(), toSpliced(), findLast()
2024 — ES15: Promise.withResolvers(), Object.groupBy(), Map.groupBy()
```

### Why JavaScript Was Created in 10 Days

In 1995, web pages were **static HTML**. There was no way to make the page respond to user actions without a full server round-trip. Netscape wanted a simple scripting language for the browser.

Brendan Eich was hired to create it. He was given **10 days**. This explains many of JavaScript's quirks:
- `typeof null === 'object'` — a bug from the original implementation
- `NaN === NaN` is `false` — follows IEEE 754 float spec but surprises everyone
- Automatic Semicolon Insertion (ASI) — controversial but baked in

Despite these quirks, JavaScript became the **language of the web** — and today it's the most used programming language in the world.

---

## 3. How JavaScript Works — The Big Picture {#big-picture}

Before diving into details, understand the 10,000-foot view:

```
┌─────────────────────────────────────────────────────────┐
│                    Your JavaScript Code                  │
│              const x = 5; console.log(x);               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   JavaScript Engine                      │
│   (V8 in Chrome/Node.js, SpiderMonkey in Firefox,       │
│    JavaScriptCore in Safari)                             │
│                                                          │
│  ┌─────────┐    ┌─────────┐    ┌──────────────────────┐ │
│  │  Parser │───▶│   AST   │───▶│  Interpreter/JIT     │ │
│  └─────────┘    └─────────┘    └──────────────────────┘ │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              JavaScript Runtime Environment              │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Call Stack │  │  Web APIs    │  │ Callback Queue │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│                          ▲                               │
│                          │                               │
│                   ┌──────────────┐                       │
│                   │  Event Loop  │                       │
│                   └──────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### Compiled vs Interpreted Languages

**Real-world analogy:**
- **Compiled language** = Translate an entire book from English to French FIRST, then read the French version. (C, C++, Rust)
- **Interpreted language** = Read the English book aloud while translating word-by-word in real time. (Traditional JavaScript, Python)
- **JIT (Just-In-Time) compiled** = Translate the most popular chapters first, cache them, then read those. If a chapter is rarely read, just translate on the fly. (Modern JavaScript)

```
COMPILED (C/C++):
Source Code → Compiler → Machine Code → Execute
    (once)                              (fast)

INTERPRETED (Traditional):
Source Code → Interpreter → Execute line by line
                            (slow — re-translates every time)

JIT COMPILED (Modern JS):
Source Code → Parser → AST → Interpreter (fast start)
                              ↓
                         Hot Code detected
                              ↓
                         JIT Compiler → Optimized Machine Code (fast execution)
```

---

## 4. Browser Architecture {#browser-architecture}

Your browser is not just a window to the web. It's a complex multi-component system.

```
┌────────────────────────────────────────────────────────────────┐
│                         BROWSER                                │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    USER INTERFACE                        │  │
│  │   (Address bar, Back/Forward buttons, Bookmarks, etc.)   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    BROWSER ENGINE                        │  │
│  │         (Coordinates UI and Rendering Engine)            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  RENDERING ENGINE                        │  │
│  │   (Parses HTML/CSS, builds DOM/CSSOM, layouts, paints)   │  │
│  │   Blink (Chrome/Edge), Gecko (Firefox), WebKit (Safari)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─────────────────────┐  ┌──────────────────────────────┐    │
│  │   JAVASCRIPT ENGINE │  │      NETWORKING              │    │
│  │   V8 / SpiderMonkey │  │  (HTTP/HTTPS, WebSockets)    │    │
│  │   / JavaScriptCore  │  └──────────────────────────────┘    │
│  └─────────────────────┘                                       │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   DATA STORAGE                           │  │
│  │    localStorage, sessionStorage, cookies, IndexedDB      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Key Browser Components Explained

**User Interface (UI Layer):**
Everything you see EXCEPT the webpage content. The address bar, reload button, developer tools toggle — all part of the UI layer.

**Browser Engine:**
Coordinates between the UI layer and the rendering engine. It initiates loading of the URL, passes the HTML to the rendering engine, etc.

**Rendering Engine:**
This is where your HTML and CSS comes to life:
1. Parses HTML → builds DOM tree
2. Parses CSS → builds CSSOM tree
3. Combines DOM + CSSOM → Render Tree
4. Layout phase (calculates positions and sizes)
5. Paint phase (fills pixels)
6. Composite phase (layers are combined and displayed)

**JavaScript Engine:**
This is our main focus. It executes your JavaScript code. Different browsers use different engines:

| Browser | JS Engine | Made By |
|---------|-----------|---------|
| Chrome | V8 | Google |
| Edge | V8 | Microsoft (uses Chromium) |
| Firefox | SpiderMonkey | Mozilla |
| Safari | JavaScriptCore (Nitro) | Apple |
| Node.js | V8 | Google |
| Deno | V8 | Ryan Dahl |

---

## 5. JavaScript Engine Deep Dive {#js-engine}

A JavaScript engine is a program that executes JavaScript code. Let's understand what happens when the engine receives your code.

### The General Flow (All Engines)

```
JavaScript Source Code
        │
        ▼
┌───────────────┐
│    PARSER     │  ← Reads your code character by character
│               │    Checks for syntax errors
│               │    Builds tokens (like words from letters)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  AST Builder  │  ← Creates Abstract Syntax Tree
│               │    Tree structure representing your code
│               │    Each node = one operation
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ INTERPRETER   │  ← Reads AST, generates BYTECODE
│  (Ignition    │    Starts executing immediately (fast startup)
│   in V8)      │    Monitors which code runs frequently ("hot code")
└───────┬───────┘
        │
        │ (hot code detected)
        ▼
┌───────────────┐
│ JIT COMPILER  │  ← Takes hot bytecode, compiles to optimized
│  (TurboFan    │    machine code specific to your CPU
│   in V8)      │    Caches the compiled code
└───────┬───────┘
        │
        ▼
  Machine Code Execution
  (Runs directly on CPU — very fast!)
```

### What is an AST?

AST = Abstract Syntax Tree. It's a tree representation of the structure of your code.

Example: `const x = 5 + 3;`

```
Program
  └── VariableDeclaration (kind: "const")
        └── VariableDeclarator
              ├── Identifier (name: "x")
              └── BinaryExpression (operator: "+")
                    ├── NumericLiteral (value: 5)
                    └── NumericLiteral (value: 3)
```

The engine doesn't understand your source code directly — it understands this tree. Tools like Babel (which transforms modern JS to older JS) also work on the AST level.

---

## 6. V8 Engine Internals {#v8}

V8 is Google's open-source JavaScript engine, written in C++. It powers Chrome and Node.js.

```
┌─────────────────────────────────────────────────────────────┐
│                        V8 ENGINE                            │
│                                                             │
│  Source Code                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐                                                │
│  │  Parser │ ← Tokenizer + Parser                          │
│  └────┬────┘   Syntax errors caught here                   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐                                                │
│  │   AST   │ ← Abstract Syntax Tree created                │
│  └────┬────┘                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────┐                                           │
│  │   IGNITION   │ ← Interpreter                            │
│  │  (Bytecode)  │   Fast startup, generates bytecode       │
│  └──────┬───────┘   Collects type feedback (profiling)     │
│         │                                                   │
│         │ (hot code — runs many times)                     │
│         ▼                                                   │
│  ┌──────────────┐                                           │
│  │   TURBOFAN   │ ← Optimizing JIT Compiler                │
│  │  (Machine    │   Takes bytecode + type feedback         │
│  │   Code)      │   Generates highly optimized machine code│
│  └──────┬───────┘                                          │
│         │                                                   │
│         │ (type changes — DEOPTIMIZATION)                  │
│         ▼                                                   │
│  Back to Ignition (deoptimize, re-profile)                 │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │                  MEMORY                            │    │
│  │   ┌────────────┐    ┌──────────────────────────┐   │    │
│  │   │   STACK    │    │          HEAP            │   │    │
│  │   │ (Call Stack│    │  (Object store, GC-mgd)  │   │    │
│  │   │  + Local   │    │  ┌────────┐ ┌─────────┐  │   │    │
│  │   │  Variables)│    │  │New Space│ │Old Space│  │   │    │
│  │   └────────────┘    │  └────────┘ └─────────┘  │   │    │
│  │                     └──────────────────────────┘   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### JIT Compilation — The Magic

**Real-world analogy:**
Imagine you're a live interpreter at the United Nations. 

- **Naive interpreter**: You translate every sentence from scratch, even if the same phrase appears 1000 times.
- **JIT compiler**: You notice "Good morning" is said 500 times a day. So you memorize the translation. Next time you hear it, you instantly say it without thinking.

JIT = Just-In-Time. Code is compiled to machine code JUST IN TIME before it runs (not ahead of time, not interpreted line by line — somewhere in between).

### Inline Caching

V8 optimizes property lookups using **Inline Caching (IC)**:

```javascript
function getAge(person) {
  return person.age;  // V8 remembers the "shape" of person objects
}

const alice = { name: "Alice", age: 25 };
const bob = { name: "Bob", age: 30 };

getAge(alice);  // First call: V8 learns "objects with name+age have age at offset X"
getAge(bob);    // Second call: V8 uses cached knowledge — super fast!
```

If suddenly you call `getAge({ age: 25 })` (different shape — no `name`), V8 has to deoptimize.

### Hidden Classes

V8 creates **hidden classes** (also called "shapes" or "maps") to track object structure:

```javascript
// GOOD — same hidden class (V8 optimizes this)
function Point(x, y) {
  this.x = x;  // Always add properties in same order
  this.y = y;
}
const p1 = new Point(1, 2);
const p2 = new Point(3, 4);

// BAD — different hidden classes (V8 can't optimize)
const obj1 = {};
obj1.x = 1;  // Hidden class A (just x)
obj1.y = 2;  // Hidden class B (x and y)

const obj2 = {};
obj2.y = 2;  // Hidden class C (just y) — different from A!
obj2.x = 1;  // Hidden class D (y and x) — different from B!
```

**Interview insight:** This is why you should always initialize object properties in the same order and in constructors.

### Deoptimization

When V8's assumptions are violated, it **deoptimizes** — goes back to interpreted mode:

```javascript
function add(a, b) {
  return a + b;
}

add(1, 2);     // V8: "These are integers, I'll optimize for integers"
add(3, 4);     // Fast — using optimized integer code
add("a", "b"); // DEOPTIMIZE — assumption broken, back to bytecode
```

**Interview tip:** This is why dynamic typing in performance-critical code can be slow.

---

## 7. JavaScript Runtime Environment {#runtime}

The JavaScript ENGINE (V8) is just one part of the runtime. The **Runtime Environment** is the full package:

```
┌─────────────────────────────────────────────────────────────────┐
│                 JAVASCRIPT RUNTIME ENVIRONMENT                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   JavaScript Engine (V8)                 │   │
│  │                                                          │   │
│  │   ┌──────────────┐          ┌──────────────────────┐    │   │
│  │   │  CALL STACK  │          │      HEAP MEMORY      │    │   │
│  │   │              │          │   (Objects, Closures)  │    │   │
│  │   │  main()      │          └──────────────────────┘    │   │
│  │   │  foo()       │                                       │   │
│  │   │  bar()       │                                       │   │
│  │   └──────────────┘                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                       WEB APIs                           │   │
│  │   (PROVIDED BY BROWSER — NOT PART OF JS ENGINE!)        │   │
│  │                                                          │   │
│  │   setTimeout()   fetch()   DOM APIs   Geolocation       │   │
│  │   localStorage   WebSockets  requestAnimationFrame       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────┐     ┌────────────────────┐                 │
│  │  MICROTASK QUEUE│     │   CALLBACK QUEUE    │                 │
│  │                 │     │   (Macrotask Queue) │                 │
│  │  Promise.then() │     │                     │                 │
│  │  queueMicrotask │     │   setTimeout CB     │                 │
│  │  MutationObserv │     │   setInterval CB    │                 │
│  └────────┬────────┘     │   fetch CB          │                 │
│           │              │   DOM event CB      │                 │
│           │              └──────────┬──────────┘                 │
│           │                         │                            │
│           └─────────────┬───────────┘                            │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                             │
│              │     EVENT LOOP      │                             │
│              │                     │                             │
│              │  Checks if stack    │                             │
│              │  is empty, then     │                             │
│              │  moves tasks to     │                             │
│              │  the call stack     │                             │
│              └─────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### Browser Runtime vs Node.js Runtime

| Feature | Browser Runtime | Node.js Runtime |
|---------|----------------|----------------|
| **Web APIs** | setTimeout, fetch, DOM, localStorage | Built-in modules (fs, http, path) |
| **Global object** | `window` | `global` (or `globalThis`) |
| **Module system** | ES Modules (native) | CommonJS + ES Modules |
| **Event loop** | libevent / platform-specific | libuv |
| **Access to** | DOM, CSSOM, BOM | File system, Network, OS |
| **setTimeout** | Web API | libuv timer |

---

## 8. Execution Context {#execution-context}

This is one of the **most important concepts** in JavaScript. Every interviewer at every company will ask about this.

### What is an Execution Context?

**Real-world analogy:**
Imagine you're managing a construction project. An **execution context** is like a **job site office**. When a new sub-project starts (like "install plumbing"), a new temporary office is set up. Inside that office, you have:
- A list of all variables and functions for that job (Memory Component)
- The workers executing the job (Code Component)

When the sub-project finishes, the temporary office is dismantled.

An **execution context** is the environment in which JavaScript code is evaluated and executed. It contains:
1. **Variable Environment (Memory)**: stores variables, functions, arguments
2. **Scope Chain**: reference to outer environments
3. **`this` binding**: what `this` refers to

### Types of Execution Context

```
1. Global Execution Context (GEC)
   - Created when the JS file first loads
   - Only ONE GEC per program
   - Creates: global object (window/global) and `this` = global object

2. Function Execution Context (FEC)
   - Created EVERY TIME a function is CALLED (not defined)
   - A new FEC is created for each function call
   - Has access to its own variables + outer scope

3. Eval Execution Context
   - Created by eval() function
   - Rarely used, avoid in production
```

### The Two Phases of Execution Context

This is the core of understanding hoisting. Every execution context has TWO phases:

#### Phase 1: Memory Creation Phase (Hoisting Phase)

JS engine scans through the code BEFORE executing anything:

```
For var declarations:     → allocated memory, initialized to undefined
For let/const declarations: → allocated memory, NOT initialized (TDZ)
For function declarations: → entire function stored in memory
For function expressions: → treated as var (undefined initially)
```

#### Phase 2: Code Execution Phase

JS engine executes the code line by line.

### Complete Example with Diagrams

```javascript
var name = "Alice";
var age = 25;

function greet() {
  var message = "Hello";
  console.log(message + " " + name);
}

greet();
console.log(age);
```

**Phase 1 — Memory Creation (GEC):**

```
GLOBAL EXECUTION CONTEXT
┌─────────────────────────────────────────┐
│ MEMORY (Variable Environment)           │
│                                         │
│  name    →  undefined  (var hoisted)    │
│  age     →  undefined  (var hoisted)    │
│  greet   →  function() {...}  (hoisted) │
│                                         │
│ CODE                                    │
│  (not yet executed)                     │
└─────────────────────────────────────────┘
```

**Phase 2 — Code Execution (GEC):**

```
Line 1: name = "Alice"
        GEC Memory: name → "Alice"

Line 2: age = 25
        GEC Memory: age → 25

Line 3-7: greet function definition — already in memory, skip

Line 9: greet() is called
        → NEW Function Execution Context created for greet()

FUNCTION EXECUTION CONTEXT (greet)
┌─────────────────────────────────────────┐
│ MEMORY (Variable Environment)           │
│  message  →  undefined  (hoisted)       │
│                                         │
│ CODE EXECUTION:                         │
│  message = "Hello"                      │
│  console.log("Hello Alice")            │
│                                         │
│ (greet FEC DELETED when function ends) │
└─────────────────────────────────────────┘

Back to GEC:
Line 10: console.log(25)
```

---

## 9. Call Stack {#call-stack}

### What is the Call Stack?

**Real-world analogy:**
Imagine a stack of plates. You can only add a plate on TOP and only remove a plate from the TOP. This is **LIFO** — Last In, First Out.

The Call Stack is how JavaScript keeps track of WHERE it is in the program — which function is currently running and which functions called it.

```
CALL STACK (LIFO — Last In, First Out)

When function is CALLED → PUSHED onto stack
When function RETURNS  → POPPED off stack
```

### Call Stack in Action

```javascript
function multiply(a, b) {
  return a * b;        // Line 2
}

function square(n) {
  return multiply(n, n);  // Line 6
}

function printSquare(n) {
  const result = square(n);  // Line 10
  console.log(result);       // Line 11
}

printSquare(5);  // Line 14
```

**Step-by-step Call Stack:**

```
INITIAL STATE:
┌──────────────┐
│   (empty)    │
└──────────────┘

STEP 1: printSquare(5) is called (Line 14)
┌──────────────┐
│ printSquare  │ ← TOP
└──────────────┘

STEP 2: Inside printSquare, square(5) is called (Line 10)
┌──────────────┐
│    square    │ ← TOP
│ printSquare  │
└──────────────┘

STEP 3: Inside square, multiply(5, 5) is called (Line 6)
┌──────────────┐
│   multiply   │ ← TOP
│    square    │
│ printSquare  │
└──────────────┘

STEP 4: multiply returns 25 → POPPED
┌──────────────┐
│    square    │ ← TOP (receives 25, returns 25)
│ printSquare  │
└──────────────┘

STEP 5: square returns 25 → POPPED
┌──────────────┐
│ printSquare  │ ← TOP (result = 25, then console.log)
└──────────────┘

STEP 6: printSquare finishes → POPPED
┌──────────────┐
│   (empty)    │
└──────────────┘
```

### Stack Overflow

The Call Stack has a **size limit**. If you add too many frames (infinite recursion), you get a **Stack Overflow**:

```javascript
function infiniteRecursion() {
  return infiniteRecursion();  // Calls itself forever
}

infiniteRecursion();
// RangeError: Maximum call stack size exceeded
```

**Real-world analogy:** Trying to stack plates forever — eventually the stack tips over!

The stack size limit depends on the browser/Node.js version, but typically it's **~10,000-15,000** frames.

### Stack Frames

Each entry on the call stack is a **Stack Frame**. It contains:
- The function being called
- Arguments passed to the function
- Local variables of the function
- The return address (where to go back after the function finishes)

---

## 10. Memory: Heap vs Stack {#memory}

JavaScript manages two types of memory: **Stack** and **Heap**.

### Stack Memory

```
┌─────────────────────────────────────────────────────────┐
│                      STACK MEMORY                       │
│                                                         │
│  Characteristics:                                       │
│  • Fixed size (allocated at compile time)               │
│  • LIFO structure                                       │
│  • Very fast access                                     │
│  • Automatic management (no GC needed)                  │
│  • Stores: primitive values, function call frames       │
│                                                         │
│  Frame for main():                                      │
│  ┌─────────────────────────────────────┐                │
│  │  let a = 5;    → a: 5              │                │
│  │  let b = "hi"; → b: "hi"           │                │
│  │  let c = true; → c: true           │                │
│  └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

**What goes on the Stack:**
- Primitive values: number, string, boolean, null, undefined, Symbol, BigInt
- Function call frames (execution contexts)
- References (pointers) to heap objects

### Heap Memory

```
┌─────────────────────────────────────────────────────────┐
│                      HEAP MEMORY                        │
│                                                         │
│  Characteristics:                                       │
│  • Dynamic size (grows as needed)                       │
│  • No particular order (scattered)                      │
│  • Slower access than stack                             │
│  • Managed by Garbage Collector                         │
│  • Stores: Objects, Arrays, Functions, Closures         │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────────────┐    │
│  │  {name: "Alice", │  │  [1, 2, 3, 4, 5]         │    │
│  │   age: 25}       │  │                          │    │
│  │  Address: 0x1a4  │  │  Address: 0x2b8          │    │
│  └──────────────────┘  └──────────────────────────┘    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  function greet() { ... }                        │  │
│  │  Address: 0x3c2                                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Pass by Value vs Pass by Reference

This is a CRITICAL concept for interviews:

```javascript
// PRIMITIVES — Pass by VALUE (copy of value is passed)
let a = 5;
let b = a;   // b gets a COPY of 5
b = 10;      // Only b changes
console.log(a); // 5 (a is unchanged)
console.log(b); // 10

// OBJECTS — Pass by REFERENCE (copy of reference/pointer)
let obj1 = { x: 5 };
let obj2 = obj1;    // obj2 gets a copy of the POINTER to the same object
obj2.x = 10;        // Modifies the SHARED object
console.log(obj1.x); // 10 (obj1 is CHANGED!)
console.log(obj2.x); // 10
```

**Memory diagram for objects:**

```
Stack                      Heap
┌──────────────┐          ┌──────────────────────┐
│ obj1: 0x1a4  │────────▶ │  { x: 5 }            │
│ obj2: 0x1a4  │────────▶ │  Address: 0x1a4      │
└──────────────┘          └──────────────────────┘

Both obj1 and obj2 POINT to the same object in heap!
When you do obj2.x = 10, you're modifying the object at 0x1a4
So obj1.x is also 10!
```

**Common interview question:**

```javascript
function changeValue(obj) {
  obj.name = "Bob";    // Modifies the ORIGINAL object
  obj = { name: "Charlie" };  // Now obj points to a NEW object
}

const person = { name: "Alice" };
changeValue(person);
console.log(person.name); // ???
```

**Answer:** `"Bob"` — because reassigning `obj` inside the function only changes the local copy of the reference. The first line `obj.name = "Bob"` modifies the original object before reassignment.

---

## 11. Garbage Collection {#garbage-collection}

### What is Garbage Collection?

**Real-world analogy:**
Imagine you're renting storage units. When you're done using your stuff, you give back the key. A facility manager (garbage collector) periodically checks which units have no keys assigned to them, and clears them out to make room for new renters.

In JavaScript, the **Garbage Collector (GC)** automatically frees memory that is no longer needed (i.e., no longer reachable from your code).

### Memory Lifecycle

```
1. ALLOCATE  → Memory is allocated when you create variables/objects
2. USE       → Memory is used while you reference the data
3. RELEASE   → Memory is freed when data is no longer reachable
```

### Mark and Sweep Algorithm

The most common GC algorithm. Used by V8 (with many optimizations).

**Step 1: Mark phase** — GC starts from "roots" (global variables, call stack variables) and marks everything REACHABLE.

**Step 2: Sweep phase** — Everything NOT marked is garbage. GC frees that memory.

```
ROOTS (Global scope + Call Stack)
    │
    ├── globalVar → { value: 42 }      ← REACHABLE (marked)
    │                    │
    │                    └── nested → { x: 1 }  ← REACHABLE (marked)
    │
    └── localVar → { data: "hi" }      ← REACHABLE (marked)

UNREACHABLE OBJECTS (will be swept):
    { orphaned: true }   ← No reference from any root
    { abandoned: "yes" } ← No reference from any root
```

### Memory Leaks — What Causes Them

A **memory leak** is when your program holds references to objects that are no longer needed, preventing GC from freeing them.

**Common causes:**

```javascript
// 1. GLOBAL VARIABLES (accidentally creating globals)
function badFunction() {
  leakedVar = "I'm global!";  // No var/let/const → becomes global!
}

// 2. FORGOTTEN INTERVALS
const intervalId = setInterval(() => {
  // This holds a reference to everything in its closure FOREVER
  doSomethingWithBigData(bigData);
}, 1000);
// FIX: clearInterval(intervalId) when done

// 3. EVENT LISTENERS NOT REMOVED
const button = document.getElementById('btn');
function handleClick() { /* does something */ }
button.addEventListener('click', handleClick);
// DOM element removed but listener still references handleClick
// FIX: button.removeEventListener('click', handleClick)

// 4. CLOSURES HOLDING LARGE DATA
function createLeak() {
  const hugeArray = new Array(1000000).fill('data');
  return function() {
    console.log(hugeArray[0]);  // hugeArray is captured by closure
    // Even if we only need hugeArray[0], the WHOLE array is kept in memory
  };
}

// 5. DETACHED DOM NODES
let button = document.getElementById('btn');
document.body.removeChild(button);  // Removed from DOM
// BUT if button variable still exists, the node is NOT garbage collected!
button = null;  // FIX: set to null to allow GC
```

### WeakRef and FinalizationRegistry (Modern JS)

ES2021 introduced `WeakRef` for holding weak references (don't prevent GC):

```javascript
let bigObject = { data: new Array(1000000).fill('x') };

// WeakRef doesn't prevent garbage collection
const weakRef = new WeakRef(bigObject);

bigObject = null;  // Now bigObject can be GC'd

// Later...
const obj = weakRef.deref();  // May return undefined if GC'd
if (obj) {
  console.log(obj.data.length);
}
```

---

## 12. Event Loop {#event-loop}

The Event Loop is the **most important concept** in JavaScript. It's what makes JavaScript non-blocking despite being single-threaded.

### The Problem: Single-Threaded + Blocking Operations

```javascript
// Without event loop, this would FREEZE the browser for 5 seconds:
const data = fetchDataFromServer();  // Takes 5 seconds
console.log("This would be stuck waiting...");
console.log("User can't click anything!");
```

JavaScript is single-threaded — it can only do ONE thing at a time. So how can it handle:
- Network requests that take seconds
- Timers
- User interactions
...without freezing?

**Answer: The Event Loop.**

### The Complete Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        JAVASCRIPT RUNTIME                        │
│                                                                  │
│  ┌────────────────────┐                                          │
│  │     CALL STACK     │                                          │
│  │                    │  ← JS Engine executes code here         │
│  │   (currently       │                                          │
│  │    running code)   │                                          │
│  └─────────┬──────────┘                                          │
│            │                                                     │
│            │ async operation → sent to Web API                  │
│            ▼                                                     │
│  ┌────────────────────┐                                          │
│  │      WEB APIs      │                                          │
│  │                    │  ← Browser handles async stuff here     │
│  │  setTimeout timer  │    (Not JS engine!)                     │
│  │  fetch HTTP req    │                                          │
│  │  DOM events        │                                          │
│  └──────┬─────────────┘                                          │
│         │ (when done, callback registered)                       │
│         │                                                        │
│         ├──────────────────────┐                                 │
│         ▼                      ▼                                 │
│  ┌─────────────┐    ┌────────────────────┐                       │
│  │  MICROTASK  │    │   CALLBACK QUEUE   │                       │
│  │    QUEUE    │    │  (Macrotask Queue) │                       │
│  │             │    │                    │                       │
│  │ Promise.then│    │  setTimeout CB     │                       │
│  │ queueMicro  │    │  setInterval CB    │                       │
│  │ MutationObs │    │  fetch CB          │                       │
│  └──────┬──────┘    └────────┬───────────┘                       │
│         │                    │                                   │
│         └────────┬───────────┘                                   │
│                  │                                               │
│                  ▼                                               │
│         ┌────────────────┐                                       │
│         │   EVENT LOOP   │                                       │
│         │                │                                       │
│         │  CHECK:        │                                       │
│         │  Is call stack │                                       │
│         │  empty?        │                                       │
│         │  → YES: move   │                                       │
│         │    microtasks  │                                       │
│         │    first, then │                                       │
│         │    macrotasks  │                                       │
│         └────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Event Loop Step-by-Step Example

```javascript
console.log("1 — Start");          // Synchronous

setTimeout(() => {
  console.log("2 — setTimeout");   // Macrotask
}, 0);

Promise.resolve().then(() => {
  console.log("3 — Promise");      // Microtask
});

console.log("4 — End");            // Synchronous
```

**Execution trace:**

```
STEP 1: console.log("1 — Start")
  Call Stack: [console.log]
  Output: "1 — Start"
  Call Stack: []

STEP 2: setTimeout(callback, 0)
  Call Stack: [setTimeout]
  → setTimeout handed to Web API
  → Timer starts (0ms) → immediately registered in Callback Queue
  Call Stack: []

STEP 3: Promise.resolve().then(callback)
  Call Stack: [Promise.then]
  → Promise resolved immediately
  → .then callback added to MICROTASK QUEUE
  Call Stack: []

STEP 4: console.log("4 — End")
  Call Stack: [console.log]
  Output: "4 — End"
  Call Stack: []

STEP 5: Call Stack is EMPTY! Event Loop activates.
  Check Microtask Queue: Promise callback is there
  → Move Promise callback to Call Stack
  → Execute: console.log("3 — Promise")
  Output: "3 — Promise"
  → Microtask Queue is now empty

STEP 6: Call Stack is EMPTY! Event Loop checks again.
  Microtask Queue: empty
  Callback Queue (Macrotask): setTimeout callback
  → Move setTimeout callback to Call Stack
  → Execute: console.log("2 — setTimeout")
  Output: "2 — setTimeout"

FINAL OUTPUT ORDER:
"1 — Start"
"4 — End"
"3 — Promise"
"2 — setTimeout"
```

**KEY INSIGHT:** Microtasks (Promises) ALWAYS run before Macrotasks (setTimeout), even if the setTimeout delay is 0.

---

## 13. Web APIs {#web-apis}

### What Are Web APIs?

Web APIs are **provided by the browser** (NOT by the JavaScript engine). They give JavaScript the ability to:
- Set timers (`setTimeout`, `setInterval`)
- Make network requests (`fetch`, `XMLHttpRequest`)
- Manipulate the DOM
- Access device features (Camera, Geolocation, Notifications)
- Store data (`localStorage`, `sessionStorage`)

**Critical point:** These are NOT part of JavaScript itself. If you run plain V8 (without a browser), `setTimeout` and `fetch` don't exist!

```
Browser = V8 (JavaScript engine) + Web APIs + Event Loop + Queues
Node.js = V8 (JavaScript engine) + Node APIs + Event Loop + Queues
```

### Common Web APIs

| API | Purpose | Example |
|-----|---------|---------|
| `setTimeout` | Run code after delay | `setTimeout(fn, 1000)` |
| `setInterval` | Run code repeatedly | `setInterval(fn, 1000)` |
| `fetch` | HTTP requests | `fetch('https://api.com/data')` |
| `XMLHttpRequest` | Legacy HTTP requests | `new XMLHttpRequest()` |
| `DOM APIs` | HTML manipulation | `document.getElementById()` |
| `localStorage` | Persistent storage | `localStorage.setItem('key', 'val')` |
| `Geolocation` | User's location | `navigator.geolocation.getCurrentPosition()` |
| `WebSockets` | Real-time communication | `new WebSocket('ws://...')` |
| `requestAnimationFrame` | Smooth animations | `requestAnimationFrame(fn)` |
| `Canvas API` | 2D/3D graphics | `canvas.getContext('2d')` |
| `Notifications` | Browser notifications | `new Notification('Hello!')` |
| `Clipboard` | Copy/paste | `navigator.clipboard.writeText('text')` |

### How Web APIs Integrate with the Event Loop

```javascript
console.log("Start");

// setTimeout is a Web API — not JS itself
setTimeout(function callback() {
  console.log("Timer done!");  
}, 2000);

console.log("End");

// What happens:
// 1. "Start" logged
// 2. setTimeout() called — Web API registers 2000ms timer
//    JS doesn't wait! It continues immediately
// 3. "End" logged
// 4. [2 seconds pass in the browser/OS, not in JS]
// 5. Timer fires — callback added to Callback Queue
// 6. Event Loop sees stack is empty → moves callback to stack
// 7. "Timer done!" logged
```

---

## 14. Microtask vs Macrotask Queue {#queues}

### Two Queues, Different Priorities

```
MICROTASK QUEUE (HIGH PRIORITY)          MACROTASK QUEUE (NORMAL PRIORITY)
─────────────────────────────────        ──────────────────────────────────
Promise .then() callbacks                setTimeout callbacks
Promise .catch() callbacks               setInterval callbacks
Promise .finally() callbacks             setImmediate callbacks (Node.js)
queueMicrotask() callbacks               MessageChannel callbacks
MutationObserver callbacks               I/O callbacks
                                         requestAnimationFrame (sort of)

RULE: ALL microtasks run before the NEXT macrotask.
```

### Detailed Execution Order

```javascript
console.log("1");

setTimeout(() => console.log("2 — setTimeout"), 0);

Promise.resolve()
  .then(() => console.log("3 — Promise 1"))
  .then(() => console.log("4 — Promise 2"));  // Chained promise!

queueMicrotask(() => console.log("5 — queueMicrotask"));

setTimeout(() => console.log("6 — setTimeout 2"), 0);

console.log("7");
```

**Execution trace:**

```
Synchronous execution:
  → "1" logged
  → setTimeout callback added to Macrotask Queue (slot 1)
  → Promise chain: "3" callback added to Microtask Queue
     (Note: "4" is chained — added to Microtask Queue AFTER "3" runs)
  → "5" added to Microtask Queue
  → setTimeout callback added to Macrotask Queue (slot 2)
  → "7" logged

Stack is empty! Process all microtasks:
  → "3 — Promise 1" logged
  → "4 — Promise 2" now added (chained promise scheduled)
  → "5 — queueMicrotask" logged
  → "4 — Promise 2" logged (was added during microtask processing)
  → Microtask queue empty

Process next macrotask:
  → "2 — setTimeout" logged

Process all microtasks (none):
  → nothing

Process next macrotask:
  → "6 — setTimeout 2" logged

OUTPUT:
1
7
3 — Promise 1
5 — queueMicrotask
4 — Promise 2
2 — setTimeout
6 — setTimeout 2
```

### Why Microtasks Before Macrotasks?

The design decision: **Promises (microtasks) represent immediate async completions** — they should resolve as soon as possible. Macrotasks (setTimeout) represent events from the external world that can be delayed.

Keeping microtasks high-priority ensures Promise chains execute completely before control returns to the browser (for painting, etc.), which leads to more predictable behavior.

### requestAnimationFrame — Special Case

`requestAnimationFrame` runs **after microtasks but before the next paint**. It's not exactly in either queue:

```
Order within one "tick":
1. Call Stack (synchronous code)
2. Microtask Queue (all microtasks)
3. requestAnimationFrame callbacks
4. Browser Paint
5. Macrotask Queue (one macrotask)
6. Repeat
```

---

## 15. Chapter Summary & Interview Prep {#summary}

### Chapter Revision Notes

```
KEY POINTS TO REMEMBER:

✅ JavaScript is single-threaded, interpreted (+ JIT compiled)
✅ V8: Parser → AST → Ignition (bytecode) → TurboFan (machine code)
✅ Runtime = Engine + Web APIs + Event Loop + Queues
✅ Global Execution Context (GEC): created once when script loads
✅ Function Execution Context (FEC): created on EACH function call
✅ Two phases: Memory Creation (hoisting) → Code Execution
✅ Call Stack: LIFO, tracks execution, stack overflow = infinite recursion
✅ Stack: primitives, function frames (fast, fixed size, auto-managed)
✅ Heap: objects, functions, closures (dynamic, GC-managed)
✅ Primitives: pass by VALUE. Objects: pass by REFERENCE (actually by sharing)
✅ GC: Mark and Sweep — marks reachable objects, sweeps the rest
✅ Memory leaks: globals, forgotten intervals, not removing event listeners
✅ Event Loop: watches call stack; when empty, moves tasks from queue to stack
✅ Microtasks (Promises) run BEFORE Macrotasks (setTimeout)
✅ Web APIs are NOT part of JS engine — provided by browser/Node.js
```

### Interview Cheat Sheet

```
One-liners for rapid review:

• "JS is single-threaded with a non-blocking event loop"
• "V8 uses JIT compilation: Ignition for bytecode, TurboFan for optimization"
• "GEC is created once; FEC is created for every function call"
• "Hoisting: var → undefined, let/const → TDZ, function → fully hoisted"
• "Primitives on stack; Objects on heap; references are on stack"
• "typeof null === 'object' is a historical bug in JS"
• "Microtask queue (Promises) always drains before macrotask queue (setTimeout)"
• "Memory leak causes: forgotten timers, global vars, stale DOM refs, closures"
• "Pass by value for primitives; pass by reference (sharing) for objects"
• "Stack overflow = infinite recursion exceeding call stack limit"
```

---

## Top 20 Interview Questions — Chapter 1

**Q1. Explain how JavaScript works under the hood.**
*Answer:* JavaScript source code is fed to the JavaScript engine (e.g., V8). The engine parses the code, builds an AST, then the interpreter (Ignition) converts it to bytecode. For frequently-executed code ("hot code"), the JIT compiler (TurboFan) compiles it to optimized machine code. The runtime environment also provides Web APIs, an event loop, and task queues that enable asynchronous behavior despite JS being single-threaded.

**Q2. What is the Event Loop and why does JavaScript need it?**
*Answer:* The Event Loop is a mechanism that continuously checks if the call stack is empty. If it is, it moves callbacks from the task queues to the call stack for execution. JS needs it because it's single-threaded — it can only run one thing at a time. The Event Loop enables non-blocking async behavior by offloading I/O operations to Web APIs (browser) or Node APIs, and then executing callbacks when the stack is free.

**Q3. What is the difference between the Microtask Queue and the Macrotask Queue?**
*Answer:* Microtask queue contains callbacks from Promises (.then, .catch, .finally), queueMicrotask(), and MutationObserver. Macrotask queue contains setTimeout, setInterval, I/O callbacks. The key difference is priority: ALL pending microtasks are processed before the next macrotask. This means Promise chains fully resolve before any setTimeout callback runs.

**Q4. What happens when you call a function in JavaScript?**
*Answer:* A new Function Execution Context (FEC) is created and pushed onto the call stack. The FEC goes through two phases: Memory Creation Phase (variables hoisted, set to undefined; functions fully stored) and Code Execution Phase (code runs line by line). When the function returns, its FEC is popped off the call stack and its memory is eligible for garbage collection.

**Q5. What is the difference between Stack Memory and Heap Memory?**
*Answer:* Stack memory stores primitive values and function call frames. It's fixed-size, LIFO, fast, and automatically managed. Heap memory stores objects, arrays, and functions. It's dynamically sized, not ordered, slower to access, and managed by the garbage collector. When you create a variable with an object, the reference (pointer) is on the stack but the actual object data is on the heap.

**Q6. Explain the Mark and Sweep garbage collection algorithm.**
*Answer:* GC starts from "roots" (global scope, current call stack). It traverses all reachable objects and "marks" them. In the sweep phase, anything NOT marked is considered garbage and its memory is freed. V8 enhances this with generational GC: new objects in "young generation" are collected frequently; objects that survive multiple GC cycles move to "old generation" and are collected less frequently.

**Q7. What are Web APIs? Are they part of JavaScript?**
*Answer:* No, Web APIs are NOT part of the JavaScript engine. They are provided by the browser (or Node.js runtime). Examples include setTimeout, fetch, DOM APIs, localStorage, Geolocation. The JavaScript engine has no knowledge of these — they are bridge points between JS code and the browser's capabilities.

**Q8. What is JIT compilation? How does V8 use it?**
*Answer:* JIT (Just-In-Time) compilation means code is compiled to native machine code right before it executes, not beforehand (AOT) or interpreted line by line. V8 first uses Ignition (interpreter) to generate bytecode quickly, enabling fast startup. It profiles which code runs frequently ("hot code"). TurboFan (the JIT compiler) then compiles hot bytecode into highly optimized machine code, using information about types gathered during profiling.

**Q9. What causes a stack overflow?**
*Answer:* A stack overflow occurs when the call stack exceeds its size limit. The most common cause is infinite recursion — a function calling itself without a proper base case. Each function call adds a frame to the stack; when the stack is full, you get `RangeError: Maximum call stack size exceeded`.

**Q10. What is the difference between `null` and `undefined`?**
*Answer:* `undefined` means a variable has been declared but no value assigned, or a function returns no value. `null` is an explicitly assigned value meaning "intentionally empty/no value." `typeof undefined === 'undefined'`, `typeof null === 'object'` (a historical bug). `null == undefined` is `true` (loose equality), but `null === undefined` is `false`.

**Q11. Predict the output:**
```javascript
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
```
*Answer:* `1, 4, 3, 2` — Synchronous first (1, 4), then microtask (3), then macrotask (2).

**Q12. What is a Hidden Class in V8?**
*Answer:* V8 creates "hidden classes" (also called shapes/maps) to track the structure of objects. When objects have the same properties in the same order, they share a hidden class, and property access is extremely fast (direct offset lookup). If you add properties in different orders or delete properties, different hidden classes are created, preventing this optimization.

**Q13. Why does `typeof null === 'object'`?**
*Answer:* This is a bug from JavaScript's original implementation in 1995. In the original implementation, values were stored as 32-bit units where the first bits indicated the type. The type tag for objects was `000`. null was represented as a null pointer (all zeros), so the first bits were also `000`, causing it to be identified as an object. This bug was never fixed for backward compatibility reasons.

**Q14. What are memory leaks in JavaScript and how do you prevent them?**
*Answer:* Memory leaks occur when memory that's no longer needed isn't released because references still exist. Common causes: (1) Accidental global variables, (2) Forgotten setInterval/setTimeout, (3) Event listeners not removed, (4) Closures capturing large data unintentionally, (5) Detached DOM nodes with JavaScript references. Prevention: Use `let`/`const`, clear intervals, remove event listeners, use WeakMap/WeakRef for cache-like structures, null out references when done.

**Q15. Explain the two phases of an Execution Context.**
*Answer:* Phase 1 - Memory Creation: JS scans the code, allocates memory for variables (var → undefined, let/const → uninitialized TDZ), and stores full function declarations. Phase 2 - Code Execution: JS executes code line by line, assigning values, calling functions (which creates new execution contexts), etc.

---

## 5 Output Prediction Exercises

### Exercise 1
```javascript
var x = 1;
function foo() {
  console.log(x);
  var x = 2;
  console.log(x);
}
foo();
console.log(x);
```
**Answer:** `undefined`, `2`, `1`
**Explanation:** Inside `foo()`, `var x` is hoisted to top of the function scope (initialized to `undefined`). So the first `console.log(x)` sees the local `x` which is `undefined`. Then `x = 2` assigns the value. The global `x` is never touched.

### Exercise 2
```javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
new Promise((resolve) => {
  console.log("C");
  resolve();
}).then(() => console.log("D"));
console.log("E");
```
**Answer:** `A`, `C`, `E`, `D`, `B`
**Explanation:** A (sync) → Promise executor runs synchronously so C (sync) → E (sync) → D (microtask) → B (macrotask)

### Exercise 3
```javascript
let a = { value: 1 };
let b = a;
b.value = 2;
b = { value: 3 };
console.log(a.value);
console.log(b.value);
```
**Answer:** `2`, `3`
**Explanation:** `b = a` makes b point to the same object. `b.value = 2` modifies the shared object (so a.value is also 2). `b = { value: 3 }` makes b point to a NEW object. a still points to the original object with value 2.

### Exercise 4
```javascript
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    getValue: () => count
  };
}
const c1 = createCounter();
const c2 = createCounter();
c1.increment();
c1.increment();
c2.increment();
console.log(c1.getValue());
console.log(c2.getValue());
```
**Answer:** `2`, `1`
**Explanation:** Each call to `createCounter()` creates a NEW closure with its own `count` variable. c1 and c2 have independent counts.

### Exercise 5
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
```
**Answer:** `3`, `3`, `3`
**Explanation:** `var i` is function-scoped (or global if no surrounding function). By the time the setTimeout callbacks run, the for loop has finished and `i` is 3. All three callbacks reference the same `i` variable. (Fix with `let` which creates a new binding per iteration.)

---

## 5 Coding Exercises

### Exercise 1: Implement a simple event loop simulator
```javascript
// Create a simple simulation that shows the concept of event loop
// Your code should demonstrate: sync code → microtasks → macrotasks

function simulateEventLoop() {
  const callStack = [];
  const microtaskQueue = [];
  const macrotaskQueue = [];
  
  // ... implement a simulation
}
```

### Exercise 2: Find and fix the memory leak
```javascript
// This code has a memory leak. Find it and fix it.
function setupSearch() {
  const searchHistory = [];
  const input = document.getElementById('search');
  
  input.addEventListener('keyup', function search(e) {
    searchHistory.push(e.target.value);
    console.log('History:', searchHistory);
  });
  
  // Function called many times to "reset" search
  // But leak exists! Find it.
}
// Called many times
for (let i = 0; i < 100; i++) {
  setupSearch();
}
```

### Exercise 3: Predict and explain output
```javascript
async function first() {
  console.log("first start");
  await second();
  console.log("first end");
}

async function second() {
  console.log("second");
}

console.log("main start");
first();
console.log("main end");
```

### Exercise 4: Implement your own setTimeout (conceptually)
Write pseudocode or actual code showing how you would implement a basic version of setTimeout using the concept of event loop and queues.

### Exercise 5: Debug the stack overflow
```javascript
// Fix this function to avoid stack overflow
function sumTo(n) {
  if (n === 0) return 0;
  return n + sumTo(n - 1);
}

// This works but crashes for large n
console.log(sumTo(100000)); // RangeError: Maximum call stack size exceeded
// Implement a version that handles large n
```

---

## 10 MCQs

**Q1.** Which of the following is NOT part of the JavaScript engine?
- A) Parser
- B) Call Stack  
- C) setTimeout
- D) Heap Memory

**Answer: C** — `setTimeout` is a Web API provided by the browser, not part of the JS engine.

---

**Q2.** What is the output order?
```javascript
setTimeout(() => console.log('A'), 0);
Promise.resolve().then(() => console.log('B'));
console.log('C');
```
- A) A, B, C
- B) C, A, B
- C) C, B, A
- D) B, C, A

**Answer: C** — Sync first (C), then microtask (B), then macrotask (A).

---

**Q3.** What does the Mark and Sweep algorithm do?
- A) Marks all variables and sweeps unused syntax
- B) Marks reachable objects and frees unreachable ones
- C) Marks hot code and sweeps cold code
- D) Marks compiled code and sweeps interpreted code

**Answer: B**

---

**Q4.** Which memory area stores objects in JavaScript?
- A) Stack
- B) Queue
- C) Heap
- D) Cache

**Answer: C**

---

**Q5.** What is a "hidden class" in V8?
- A) A private class in JavaScript
- B) A class created by the class keyword that's not exported
- C) An internal data structure V8 uses to optimize property access
- D) A class that's garbage collected immediately

**Answer: C**

---

**Q6.** The Event Loop checks for pending tasks when:
- A) A timer fires
- B) The call stack becomes empty
- C) A Promise is resolved
- D) A DOM event occurs

**Answer: B**

---

**Q7.** What is "JIT" in JIT compilation?
- A) JavaScript Internal Translation
- B) Just-In-Time
- C) JavaScript Integrated Translation
- D) Just Interpreted Translation

**Answer: B**

---

**Q8.** Which statement about pass by reference in JavaScript is TRUE?
- A) All values are passed by reference
- B) Primitives are passed by reference, objects by value
- C) Objects are passed by reference (by sharing), primitives by value
- D) JavaScript always copies everything

**Answer: C** — More precisely, objects are passed "by sharing": the reference is copied, but both copies point to the same object.

---

**Q9.** What causes the error "Maximum call stack size exceeded"?
- A) Using too many global variables
- B) Infinite recursion without a base case
- C) Too many setTimeout calls
- D) Memory running out on the heap

**Answer: B**

---

**Q10.** Which of these creates a potential memory leak?
- A) `let x = 5;`
- B) `const arr = [1, 2, 3];`
- C) `setInterval(() => update(), 1000);` (without storing the ID or clearing it)
- D) `function foo() { return 42; }`

**Answer: C** — setInterval keeps running and holds a reference to the callback and its closure forever unless explicitly cleared.

---

*End of Chapter 1 — You now have a deep understanding of how JavaScript truly works under the hood. Every concept in the chapters ahead builds on this foundation.*
