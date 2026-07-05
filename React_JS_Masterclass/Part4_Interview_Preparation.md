# Part 4: Complete Interview Preparation Guide
## React.js + JavaScript Master Handbook — The Ultimate Interview Resource

> **Target:** This document is your single reference for every JavaScript and React interview question — from entry-level to FAANG Staff Engineer. Every question includes: the answer, what interviewers are really testing, follow-up questions, and common mistakes.

---

## Table of Contents

- [SECTION 1: JavaScript Interview Questions](#section-1-javascript-interview-questions)
  - [Basic JS (30 Questions)](#basic-js-questions)
  - [Intermediate JS (30 Questions)](#intermediate-js-questions)
  - [Advanced JS (20 Questions)](#advanced-js-questions)
  - [JavaScript Output Questions (25)](#javascript-output-questions)
  - [JS Machine Coding (15 Solutions)](#js-machine-coding-questions)
- [SECTION 2: React Interview Questions](#section-2-react-interview-questions)
  - [Basic React (30 Questions)](#basic-react-questions)
  - [Intermediate React (30 Questions)](#intermediate-react-questions)
  - [Advanced React (20 Questions)](#advanced-react-questions)
  - [React Machine Coding (12 Solutions)](#react-machine-coding-questions)
- [SECTION 3: Company-Specific Questions](#section-3-company-specific-questions)
- [SECTION 4: Behavioral Questions](#section-4-behavioral-questions)
- [SECTION 5: Interview Cheat Sheets](#section-5-interview-cheat-sheets)

---

# SECTION 1: JavaScript Interview Questions

---

# Basic JS Questions

---

## Q1. What is the Event Loop?

**What they're testing:** Do you understand JavaScript's concurrency model?

**Answer:**
JavaScript is single-threaded — it can only execute one thing at a time. The event loop is the mechanism that allows JavaScript to be non-blocking (asynchronous) despite being single-threaded.

```
┌───────────────────────────────────────────────────────────┐
│                  JavaScript Runtime                        │
│                                                           │
│  ┌─────────────────────┐    ┌──────────────────────────┐ │
│  │    Call Stack        │    │    Web APIs              │ │
│  │  (LIFO — sync code)  │    │  (setTimeout, fetch,     │ │
│  │                      │    │   DOM events, etc.)       │ │
│  │  [main()]            │    │                          │ │
│  │  [console.log()]     │    └──────────┬───────────────┘ │
│  └──────────┬───────────┘               │                  │
│             │                    Callback                  │
│             ↓                    registered               │
│  ┌──────────────────────┐               │                  │
│  │    Event Loop         │               ↓                  │
│  │  (constantly checks)  │    ┌──────────────────────────┐ │
│  │                       │    │   Callback/Task Queue    │ │
│  │  If stack is EMPTY   ←────┤   (Macrotasks)            │ │
│  │  → move from queue   │    │   setTimeout callbacks    │ │
│  │    to stack           │    │   setInterval             │ │
│  └───────────────────────┘    │   DOM event handlers     │ │
│                               └──────────────────────────┘ │
│                                                             │
│                               ┌──────────────────────────┐ │
│                               │   Microtask Queue        │ │
│                               │   (Priority!)            │ │
│                               │   Promise.then()         │ │
│                               │   queueMicrotask()       │ │
│                               │   MutationObserver       │ │
│                               └──────────────────────────┘ │
└───────────────────────────────────────────────────────────┘

EVENT LOOP ORDER:
1. Run ALL synchronous code (clear the stack)
2. Run ALL microtasks (Promise callbacks, queueMicrotask)
3. Render (if in browser)
4. Run ONE macrotask (setTimeout, setInterval, fetch callback)
5. Go back to step 2
```

**Code Example:**
```javascript
console.log('1');                         // Sync → runs first

setTimeout(() => console.log('2'), 0);   // Macrotask → runs last

Promise.resolve().then(() => console.log('3')); // Microtask → runs before macrotask

console.log('4');                         // Sync → runs second

// Output: 1, 4, 3, 2
```

**Follow-up questions interviewers ask:**
- What is the difference between microtask and macrotask queue?
- Why does `Promise.then` run before `setTimeout(fn, 0)`?
- Can you starve the event loop with too many microtasks?

**Common mistakes:**
- Saying JS is multi-threaded (it is not — Web Workers are separate)
- Not knowing that microtasks run BETWEEN macrotasks (not just once at the end)

---

## Q2. What is Hoisting?

**Answer:** Hoisting is JavaScript's default behavior of moving variable and function **declarations** (not initializations) to the top of their scope during the compilation phase, before code executes.

```javascript
// What you write:
console.log(name);    // undefined (not ReferenceError!)
var name = 'Alice';
greet();              // Works!

function greet() {
  console.log('Hello');
}

// What JS actually does (conceptually):
var name;             // Declaration hoisted to top
function greet() {    // Function declarations fully hoisted
  console.log('Hello');
}

console.log(name);    // undefined — declared but not yet assigned
name = 'Alice';
greet();
```

**Key differences:**
```javascript
// var — hoisted AND initialized to undefined
console.log(x); // undefined
var x = 5;

// let/const — hoisted but NOT initialized (Temporal Dead Zone)
console.log(y); // ReferenceError: Cannot access 'y' before initialization
let y = 5;

// Function declaration — fully hoisted (declaration + body)
greet();  // Works!
function greet() { }

// Function expression — only the var is hoisted
sayHi(); // TypeError: sayHi is not a function
var sayHi = function() { };
```

---

## Q3. Difference Between == and ===

**Answer:**
- `==` (Abstract Equality): Performs **type coercion** before comparing. JavaScript tries to convert both values to the same type.
- `===` (Strict Equality): Compares **value AND type**. No coercion.

```javascript
// == with type coercion
1 == '1'          // true (string '1' coerced to number 1)
0 == false        // true (false coerced to 0)
null == undefined // true (special case)
null == 0         // false (null only == undefined)
'' == false       // true (both coerced to 0)
[] == false       // true ([] → '' → 0, false → 0)
[] == ![]         // true (bizarre — both coerce to 0)

// === no coercion
1 === '1'         // false (different types)
0 === false       // false (different types)
null === undefined// false (different types)
```

**Rule of thumb:** Always use `===`. The only exception is checking for `null || undefined` in one step: `value == null` catches both.

---

## Q4. What is a Closure?

**Answer:** A closure is a function that **remembers the variables from its outer lexical scope**, even after the outer function has finished executing.

**Analogy:** Imagine a function is like a backpack. When a function is created inside another function, it packs the outer scope's variables into its backpack. Even after leaving the outer function's "room," it still carries those variables in its backpack.

```javascript
function makeCounter(startValue = 0) {
  let count = startValue;  // This lives in the closure's backpack
  
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
    reset: () => { count = startValue; },
  };
}

const counter = makeCounter(10);

console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter.decrement()); // 11
console.log(counter.getCount());  // 11

// Each call to makeCounter creates a SEPARATE closure
const counter2 = makeCounter(0);
counter2.increment();             // 1 — independent from counter
console.log(counter.getCount());  // 11 — counter unchanged
```

**Real-world uses:**
```javascript
// 1. Data encapsulation (private variables)
function createUser(name) {
  let _loginCount = 0;  // "private" — not accessible outside
  
  return {
    login: () => ++_loginCount,
    getLoginCount: () => _loginCount,
    name,
  };
}

// 2. Function factories
function multiply(factor) {
  return (number) => number * factor;
}
const double = multiply(2);
const triple = multiply(3);
double(5); // 10
triple(5); // 15

// 3. Memoization (caching computed results)
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
```

**Common Closure Gotcha — Closure in Loops:**
```javascript
// ❌ BUG: All functions share the same 'i' (var is function-scoped)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3

// ✅ FIX 1: Use let (block-scoped — each iteration gets its own i)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2

// ✅ FIX 2: Create closure with IIFE
for (var i = 0; i < 3; i++) {
  (function(j) {
    setTimeout(() => console.log(j), 100);
  })(i);
}
// Output: 0, 1, 2
```

---

## Q5. What is the `this` Keyword?

**Answer:** `this` refers to the **execution context** — the object that is currently calling the function. Its value is determined at **call time**, not definition time (except for arrow functions).

```javascript
// 1. Global context
console.log(this); // window (browser) or {} (Node.js strict mode)

// 2. Object method — this = the object before the dot
const user = {
  name: 'Alice',
  greet() {
    console.log(`Hello, ${this.name}`);
  }
};
user.greet(); // "Hello, Alice" — this = user

// 3. Function call — this = undefined (strict mode) or window
function greet() {
  console.log(this.name);
}
greet(); // undefined (strict) or window.name (sloppy)

// 4. Arrow functions — inherit 'this' from enclosing scope (lexical this)
const obj = {
  name: 'Bob',
  // Arrow function: this = whatever 'this' is where arrow was defined
  greet: () => console.log(this.name), // 'this' is NOT obj here!
  
  // Regular function: this = obj
  greetRegular() {
    const inner = () => console.log(this.name); // Arrow: inherits this from greetRegular
    inner(); // "Bob"
  }
};
obj.greet();        // undefined (this is window/module, not obj)
obj.greetRegular(); // "Bob"

// 5. new — this = newly created object
function Person(name) {
  this.name = name; // this is the new object
}
const alice = new Person('Alice'); // alice.name = 'Alice'

// 6. call/apply/bind — explicit this
function greetWith(greeting) {
  console.log(`${greeting}, ${this.name}`);
}
greetWith.call({ name: 'Alice' }, 'Hello');   // "Hello, Alice"
greetWith.apply({ name: 'Bob' }, ['Hi']);     // "Hi, Bob"
const greetBound = greetWith.bind({ name: 'Charlie' });
greetBound('Hey');                            // "Hey, Charlie"
```

---

## Q6. What is the Difference Between null and undefined?

| Aspect         | undefined                                | null                                   |
|----------------|------------------------------------------|----------------------------------------|
| Meaning        | Variable declared but not assigned       | Intentional absence of value           |
| Who sets it?   | JavaScript engine (automatic)            | Developer (intentional)                |
| typeof         | `"undefined"`                            | `"object"` ← famous bug               |
| == comparison  | `null == undefined` → `true`             | `null == undefined` → `true`           |
| === comparison | `null === undefined` → `false`           | `null === undefined` → `false`         |
| Use case       | Uninitialized, missing params, missing properties | Explicit "no value" / reset value  |

```javascript
let x;
console.log(x);          // undefined (declared, not assigned)
console.log(typeof x);   // "undefined"

let y = null;
console.log(y);          // null (intentionally empty)
console.log(typeof y);   // "object" ← historical bug in JS spec
```

---

## Q7. What are Falsy Values?

**Answer:** Values that coerce to `false` in a boolean context. There are exactly **8 falsy values** in JavaScript:

```javascript
// The 8 falsy values:
false
0
-0
0n          // BigInt zero
""          // empty string
''          // empty string (single quotes)
``          // empty string (template literal)
null
undefined
NaN

// Everything else is truthy, including:
"0"         // "0" is a non-empty string → TRUTHY
[]          // empty array → TRUTHY
{}          // empty object → TRUTHY
-1          // non-zero number → TRUTHY
```

---

## Q8. What is `typeof null`?

**Answer:** `typeof null` returns `"object"`. This is a **bug** in JavaScript that has existed since 1995 and cannot be fixed without breaking the web.

```javascript
typeof null        // "object" — BUG
typeof undefined   // "undefined"
typeof 42          // "number"
typeof "hello"     // "string"
typeof true        // "boolean"
typeof Symbol()    // "symbol"
typeof 42n         // "bigint"
typeof function(){} // "function"
typeof {}          // "object"
typeof []          // "object" — arrays are objects

// Correct null check:
value === null      // Use strict equality, not typeof
```

---

## Q9. Difference Between var, let, and const

| Feature            | var              | let              | const            |
|--------------------|------------------|------------------|------------------|
| Scope              | Function-scoped  | Block-scoped     | Block-scoped     |
| Hoisting           | Yes (undefined)  | Yes (TDZ)        | Yes (TDZ)        |
| Re-declaration     | ✅ Yes            | ❌ No             | ❌ No             |
| Re-assignment      | ✅ Yes            | ✅ Yes            | ❌ No             |
| Global object prop | ✅ (browser)      | ❌ No             | ❌ No             |
| Use in 2024        | ❌ Avoid          | ✅ For variables  | ✅ Default choice |

```javascript
// var — function scoped
function testVar() {
  if (true) {
    var x = 5;
  }
  console.log(x); // 5 — escapes the if block!
}

// let — block scoped
function testLet() {
  if (true) {
    let y = 5;
  }
  console.log(y); // ReferenceError — block scoped
}

// const — cannot be reassigned (but properties can be mutated)
const user = { name: 'Alice' };
user.name = 'Bob';  // ✅ — mutating property is fine
user = {};          // ❌ TypeError — cannot reassign

const arr = [1, 2, 3];
arr.push(4);        // ✅ — mutating array is fine
arr = [];           // ❌ TypeError
```

---

## Q10. What is the Temporal Dead Zone (TDZ)?

**Answer:** The Temporal Dead Zone is the period between the **start of the block scope** and the **actual declaration** of a `let` or `const` variable. Accessing the variable in this period throws a `ReferenceError`.

```javascript
{
  // TDZ starts here for 'x'
  console.log(x); // ❌ ReferenceError: Cannot access 'x' before initialization
  
  let x = 5;      // TDZ ends here — x is initialized
  
  console.log(x); // ✅ 5
}

// Why TDZ exists:
// It prevents bugs where code relies on a variable before it's been set.
// With var, accessing before assignment silently gives undefined — hard to debug.
// TDZ makes the bug loud and obvious.
```

---

## Q11. What is the Prototype Chain?

**Answer:** Every JavaScript object has a hidden `[[Prototype]]` link to another object. When you access a property that doesn't exist on the object, JavaScript walks up this chain until it either finds the property or reaches `null`.

```javascript
// Prototype chain visualization:
const animal = {
  breathes: true,
  eat() { return 'nom nom'; }
};

const dog = Object.create(animal); // dog's prototype IS animal
dog.bark = function() { return 'woof'; };

const rex = Object.create(dog); // rex's prototype IS dog
rex.name = 'Rex';

// Property lookup chain:
rex.name;      // Found on rex directly
rex.bark();    // Not on rex → look at dog → found! "woof"
rex.eat();     // Not on rex, not on dog → look at animal → found! "nom nom"
rex.breathes;  // Not on rex, not on dog → found on animal → true
rex.unknown;   // Not found anywhere → undefined

// The chain: rex → dog → animal → Object.prototype → null

// Object.prototype is at the top of ALL chains:
animal.hasOwnProperty;  // Found on Object.prototype
animal.toString;        // Found on Object.prototype
```

---

## Q12. How Does Garbage Collection Work?

**Answer:** JavaScript uses **automatic garbage collection** — memory is automatically freed when it's no longer reachable. The main algorithm is **Mark-and-Sweep**.

```
Mark-and-Sweep Algorithm:

1. Start from "roots" (global variables, currently executing functions)
2. MARK all objects reachable from roots
3. SWEEP (delete) all unmarked objects — they're unreachable = garbage

Example:
  let user = { name: 'Alice' };  // Object is reachable via 'user'
  user = null;                   // Object no longer reachable → GC will collect it

  // Circular references are handled by mark-and-sweep:
  let a = {};
  let b = { ref: a };
  a.ref = b;
  // Even though a and b reference each other, if nothing else references them...
  a = null;
  b = null;
  // ...they become unreachable from roots → both are collected ✅
```

**Memory leaks in JavaScript:**
```javascript
// 1. Forgotten event listeners
const button = document.getElementById('btn');
function handler() { /* closes over big data */ }
button.addEventListener('click', handler);
// Fix: button.removeEventListener('click', handler) when done

// 2. Detached DOM nodes
let detachedDiv = document.createElement('div');
document.body.appendChild(detachedDiv);
document.body.removeChild(detachedDiv); // Removed from DOM
// But 'detachedDiv' variable still holds reference — GC can't collect it
detachedDiv = null; // Fix: clear the reference

// 3. Growing closures
function createBigClosure() {
  const bigData = new Array(1000000).fill('data'); // Big array
  return function() {
    return bigData.length; // bigData lives as long as this closure lives
  };
}

// 4. setInterval not cleared
const interval = setInterval(() => {/* work */}, 1000);
// Fix: clearInterval(interval) when component unmounts
```

---

## Q13. What is call / apply / bind?

**Answer:** All three methods let you **explicitly set `this`** when calling a function.

```javascript
function introduce(greeting, punctuation) {
  console.log(`${greeting}, I'm ${this.name}${punctuation}`);
}

const person = { name: 'Alice' };

// .call(thisArg, arg1, arg2, ...) — arguments passed one by one
introduce.call(person, 'Hello', '!');    // "Hello, I'm Alice!"

// .apply(thisArg, [arg1, arg2]) — arguments passed as array
introduce.apply(person, ['Hi', '?']);   // "Hi, I'm Alice?"

// .bind(thisArg, arg1, ...) — returns NEW function with bound this
const boundIntroduce = introduce.bind(person, 'Hey');
boundIntroduce('.');   // "Hey, I'm Alice."
boundIntroduce('!');   // "Hey, I'm Alice!" (first arg is baked in)
```

**Memory Aid:**
- `call` → Comma-separated args
- `apply` → Array args
- `bind` → Bakes args in, returns function

---

## Q14. Pure Function vs Impure Function

| Feature         | Pure                             | Impure                                    |
|-----------------|----------------------------------|-------------------------------------------|
| Same input      | Always same output               | May produce different output              |
| Side effects    | None                             | May have (API calls, DOM, logs, state)    |
| External state  | Does not read/modify             | Reads/modifies external state             |
| Testable        | Extremely easy                   | Harder (needs mocks)                      |
| Predictable     | Completely                       | Not guaranteed                            |

```javascript
// Pure functions
const add = (a, b) => a + b;                    // Same input → same output
const formatDate = (date) => date.toISOString(); // No side effects

// Impure functions
let count = 0;
function increment() { count++; }    // Modifies external state

function getTime() { return new Date(); } // Different output each call

function fetchUser(id) {
  return fetch(`/api/users/${id}`); // Side effect: network call
}
```

---

## Q15. What is Memoization?

**Answer:** Memoization is an optimization technique that **caches** the results of expensive function calls and returns the cached result when the same inputs occur again.

```javascript
function memoize(fn) {
  const cache = new Map();
  
  return function(...args) {
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      console.log('Cache hit!');
      return cache.get(key);
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Expensive Fibonacci without memoization — O(2^n) time
function fib(n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

// With memoization — O(n) time
const memoFib = memoize(function fib(n) {
  if (n <= 1) return n;
  return memoFib(n - 1) + memoFib(n - 2);
});

memoFib(40); // Fast!
memoFib(40); // Instant — cached
```

---

## Q16. What are Promises?

**Answer:** A Promise is an object representing the eventual completion or failure of an asynchronous operation. It has three states: `pending`, `fulfilled`, `rejected`.

```javascript
// Creating a Promise
const fetchUser = (id) => new Promise((resolve, reject) => {
  if (!id) {
    reject(new Error('ID is required'));  // Triggers .catch()
    return;
  }
  
  setTimeout(() => {
    resolve({ id, name: 'Alice' });       // Triggers .then()
  }, 1000);
});

// Consuming with .then/.catch/.finally
fetchUser(1)
  .then(user => console.log(user))         // { id: 1, name: 'Alice' }
  .catch(error => console.error(error))
  .finally(() => console.log('Done'));     // Always runs

// Consuming with async/await (syntactic sugar over Promises)
async function loadUser(id) {
  try {
    const user = await fetchUser(id);
    console.log(user);
  } catch (error) {
    console.error(error);
  }
}
```

---

## Q17. What is async/await?

**Answer:** `async/await` is syntactic sugar over Promises that makes asynchronous code look and behave like synchronous code.

```javascript
// With Promises:
function loadUserData(userId) {
  return fetchUser(userId)
    .then(user => fetchPosts(user.id))
    .then(posts => fetchComments(posts[0].id))
    .then(comments => ({ user, posts, comments }))
    .catch(handleError);
}

// With async/await (same thing, more readable):
async function loadUserData(userId) {
  try {
    const user = await fetchUser(userId);       // Wait for user
    const posts = await fetchPosts(user.id);    // Then wait for posts
    const comments = await fetchComments(posts[0].id); // Then wait for comments
    return { user, posts, comments };
  } catch (error) {
    handleError(error);
  }
}

// Parallel execution (don't await one by one if independent!)
async function loadAll(userId) {
  // ❌ Sequential (slow — 3s total if each takes 1s)
  const user = await fetchUser(userId);
  const settings = await fetchSettings(userId);
  const notifications = await fetchNotifications(userId);
  
  // ✅ Parallel (fast — 1s total)
  const [user, settings, notifications] = await Promise.all([
    fetchUser(userId),
    fetchSettings(userId),
    fetchNotifications(userId),
  ]);
}
```

---

## Q18. What are Arrow Functions? How are they different from regular functions?

```javascript
// Regular function syntax
function add(a, b) { return a + b; }
const add2 = function(a, b) { return a + b; };

// Arrow function syntax
const add3 = (a, b) => a + b;         // Implicit return
const greet = name => `Hello, ${name}`; // Single param — no parens needed
const getObj = () => ({ key: 'value' }); // Return object — wrap in parens

// Key differences:
// 1. NO own 'this' — inherits from enclosing scope
const obj = {
  name: 'Alice',
  sayHi: function() {
    // Regular: 'this' = obj
    setTimeout(function() {
      console.log(this.name); // undefined — 'this' is window/undefined
    }, 100);
    
    // Arrow: 'this' = obj (inherited)
    setTimeout(() => {
      console.log(this.name); // "Alice" ✅
    }, 100);
  }
};

// 2. NO 'arguments' object
function regular() { console.log(arguments); } // [1, 2, 3]
const arrow = () => { console.log(arguments); }; // ReferenceError!

// 3. Cannot be used as constructors
const Person = (name) => { this.name = name; };
new Person('Alice'); // TypeError: Person is not a constructor

// 4. No .prototype property
console.log(regular.prototype); // {}
console.log(arrow.prototype);   // undefined
```

---

## Q19. What is the Spread Operator vs Rest Parameters?

```javascript
// SPREAD (...) — expands an iterable into individual elements
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2]; // [1, 2, 3, 4, 5, 6]

// Spread in function calls
Math.max(...arr1);  // Same as Math.max(1, 2, 3) → 3

// Shallow clone
const original = { a: 1, b: { c: 2 } };
const clone = { ...original };        // Shallow — b.c is still shared

// REST (...) — collects multiple arguments into an array
function sum(...numbers) {  // numbers = [1, 2, 3, 4, 5]
  return numbers.reduce((total, n) => total + n, 0);
}
sum(1, 2, 3, 4, 5); // 15

// Rest must be the LAST parameter
function first(a, b, ...rest) { // rest = everything after a and b
  return { a, b, rest };
}
first(1, 2, 3, 4, 5); // { a: 1, b: 2, rest: [3, 4, 5] }
```

---

## Q20. What is Destructuring?

```javascript
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Skip elements
const [,, third] = [1, 2, 3]; // third = 3

// Default values
const [a = 10, b = 20] = [5]; // a = 5, b = 20

// Swap variables
let x = 1, y = 2;
[x, y] = [y, x]; // x = 2, y = 1

// Object destructuring
const { name, age, city = 'Unknown' } = { name: 'Alice', age: 30 };
// name = 'Alice', age = 30, city = 'Unknown' (default)

// Rename while destructuring
const { name: userName, age: userAge } = { name: 'Bob', age: 25 };
// userName = 'Bob', userAge = 25

// Nested destructuring
const { address: { street, city: town } } = {
  address: { street: '123 Main St', city: 'NYC' }
};

// In function parameters
function renderUser({ name, email, role = 'user' }) {
  return `${name} (${email}) — ${role}`;
}
```

---

## Q21. What is `Array.prototype.map`?

```javascript
// map — transforms each element, returns NEW array
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);         // [2, 4, 6, 8, 10]
const strings = numbers.map(n => `Item ${n}`);  // ['Item 1', 'Item 2', ...]
const objects = numbers.map((n, i) => ({ id: i, value: n }));

// map vs forEach:
// map — returns new array ✅, don't mutate
// forEach — returns undefined, used for side effects

// Common mistake: using map when you need filter
const evens = numbers.map(n => n % 2 === 0);    // [false, true, false, true, false] ❌
const evens2 = numbers.filter(n => n % 2 === 0); // [2, 4] ✅
```

---

## Q22. Explain filter, reduce, find, some, every

```javascript
const products = [
  { id: 1, name: 'Shoes', price: 100, inStock: true },
  { id: 2, name: 'Hat', price: 25, inStock: false },
  { id: 3, name: 'Shirt', price: 50, inStock: true },
];

// filter — returns subset that passes the test
const available = products.filter(p => p.inStock);
// [{ id: 1... }, { id: 3... }]

// reduce — boils down to a single value
const totalPrice = products.reduce((sum, p) => sum + p.price, 0);
// 175

// Build object from array with reduce:
const byId = products.reduce((acc, p) => {
  acc[p.id] = p;
  return acc;
}, {});
// { 1: {...}, 2: {...}, 3: {...} }

// find — returns FIRST item that matches (or undefined)
const shirt = products.find(p => p.name === 'Shirt');

// findIndex — returns INDEX of first match (or -1)
const shirtIdx = products.findIndex(p => p.name === 'Shirt'); // 2

// some — true if AT LEAST ONE passes
const hasOutOfStock = products.some(p => !p.inStock); // true

// every — true if ALL pass
const allInStock = products.every(p => p.inStock);    // false

// flat — flatten nested arrays
[[1, 2], [3, [4, 5]]].flat();   // [1, 2, 3, [4, 5]]
[[1, 2], [3, [4, 5]]].flat(Infinity); // [1, 2, 3, 4, 5]

// flatMap — map + flat(1) in one step
const sentences = ['Hello World', 'Foo Bar'];
sentences.flatMap(s => s.split(' ')); // ['Hello', 'World', 'Foo', 'Bar']
```

---

## Q23. What is Optional Chaining (?.) and Nullish Coalescing (??)?

```javascript
// Optional chaining (?.) — safely access nested properties
const user = null;

// Before optional chaining — verbose
const city = user && user.address && user.address.city;

// With optional chaining
const city = user?.address?.city;  // undefined (no error!)

// Also works with methods and bracket notation
const firstPost = user?.posts?.[0];        // Array access
const name = user?.getName?.();            // Method call (only if method exists)

// Nullish coalescing (??) — default value when null or undefined
// Unlike ||, it ONLY triggers for null/undefined (not 0, '', false)
const score = 0;
const display1 = score || 'No score'; // 'No score' — WRONG! 0 is falsy
const display2 = score ?? 'No score'; // 0 — correct! 0 is not null/undefined

const config = {
  timeout: 0,
  debug: false,
  name: '',
};
const timeout = config.timeout ?? 3000;  // 0 (not 3000)
const debug = config.debug ?? true;      // false (not true)
const name = config.name ?? 'Default';  // '' (not 'Default')
```

---

## Q24. What are Symbols?

```javascript
// Symbol — unique, immutable primitive value
const id1 = Symbol('id');
const id2 = Symbol('id');
id1 === id2;  // false — every Symbol is unique

// Use case: unique property keys (avoid name collisions)
const ID = Symbol('userId');
const user = {
  name: 'Alice',
  [ID]: 42,              // Hidden from for...in, Object.keys, JSON.stringify
};

console.log(user[ID]); // 42
console.log(user.ID);  // undefined — must use bracket notation

// Well-known Symbols — customize JS behavior
class CustomArray {
  [Symbol.iterator]() {   // Makes it iterable with for...of
    let index = 0;
    return {
      next: () => ({ value: index++, done: index > 3 })
    };
  }
}

// Symbol.toPrimitive — customize type conversion
class Money {
  constructor(amount, currency) {
    this.amount = amount;
    this.currency = currency;
  }
  
  [Symbol.toPrimitive](hint) {
    if (hint === 'number') return this.amount;
    if (hint === 'string') return `${this.amount} ${this.currency}`;
    return this.amount;
  }
}

const price = new Money(100, 'USD');
+price;         // 100 (number hint)
`${price}`;    // "100 USD" (string hint)
```

---

## Q25. What is the Difference Between Object.freeze, Object.seal, Object.assign?

```javascript
// Object.freeze — deeply immutable (no add, remove, or modify)
const config = Object.freeze({ api: 'https://api.example.com', timeout: 5000 });
config.api = 'other';   // Silently fails (TypeError in strict mode)
config.newProp = 'val'; // Silently fails
delete config.timeout;  // Silently fails

// BUT: freeze is SHALLOW — nested objects are still mutable
const state = Object.freeze({ user: { name: 'Alice' } });
state.user.name = 'Bob'; // ✅ Works! nested object is not frozen

// Object.seal — can modify existing props, but can't add/remove
const obj = Object.seal({ x: 1, y: 2 });
obj.x = 10;      // ✅ Can modify existing
obj.z = 3;       // ❌ Can't add new
delete obj.x;    // ❌ Can't delete

// Object.assign — shallow merge/copy
const target = { a: 1, b: 2 };
const source = { b: 3, c: 4 };
Object.assign(target, source); // target = { a: 1, b: 3, c: 4 }

// Object.assign for cloning (shallow)
const clone = Object.assign({}, original);
// Same as spread: const clone = { ...original };
```

---

## Q26. What is the Difference Between for...in and for...of?

```javascript
// for...in — iterates over KEYS (enumerable properties)
const obj = { a: 1, b: 2, c: 3 };
for (const key in obj) {
  console.log(key);     // 'a', 'b', 'c' (keys)
  console.log(obj[key]); // 1, 2, 3 (values)
}

// ⚠️ for...in also iterates inherited properties
function Animal(name) { this.name = name; }
Animal.prototype.breathe = function() {};
const dog = new Animal('Rex');

for (const key in dog) {
  console.log(key); // 'name', 'breathe' (includes inherited!)
}
// Fix: use hasOwnProperty
for (const key in dog) {
  if (dog.hasOwnProperty(key)) {
    console.log(key); // 'name' only
  }
}

// for...of — iterates over VALUES of iterables (arrays, strings, Maps, Sets)
const arr = [10, 20, 30];
for (const value of arr) {
  console.log(value); // 10, 20, 30 (values, not indices)
}

for (const char of 'hello') {
  console.log(char); // 'h', 'e', 'l', 'l', 'o'
}

// for...of with Map
const map = new Map([['a', 1], ['b', 2]]);
for (const [key, value] of map) {
  console.log(key, value); // 'a' 1, 'b' 2
}
```

---

## Q27. What are Map and Set?

```javascript
// Map — key-value pairs where keys can be ANY type (not just strings)
const map = new Map();
const objKey = { id: 1 };

map.set('string', 'value');
map.set(42, 'number key');
map.set(objKey, 'object key');
map.set(true, 'boolean key');

map.get(objKey);   // 'object key'
map.size;          // 4
map.has('string'); // true
map.delete('string');

// Iterating Map
for (const [key, value] of map) { /* ... */ }
map.forEach((value, key) => { /* ... */ });

// Map vs Object:
// ✅ Map: any key type, maintains insertion order, has .size, iterable
// ✅ Object: better for static structure, JSON serializable, prototype methods

// Set — collection of UNIQUE values (no duplicates)
const set = new Set([1, 2, 3, 2, 1]); // Duplicates removed
set.size; // 3 — {1, 2, 3}

set.add(4);
set.has(2);    // true
set.delete(1);

// Use case: remove duplicates from array
const arr = [1, 2, 2, 3, 3, 4];
const unique = [...new Set(arr)]; // [1, 2, 3, 4]
```

---

## Q28. What is Event Delegation?

**Answer:** Instead of adding event listeners to each child element, add ONE listener on a parent. The event **bubbles up** from the target to the parent.

```javascript
// ❌ Without delegation — N listeners for N buttons
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', handleClick);
});

// ✅ With delegation — ONE listener, handles all current AND future buttons
document.getElementById('button-container').addEventListener('click', (event) => {
  // event.target is the actual clicked element
  if (event.target.matches('.btn')) {
    handleClick(event);
  }
  
  if (event.target.closest('.delete-btn')) { // closest() for nested elements
    handleDelete(event);
  }
});
```

**Benefits:**
- Better memory usage (fewer listeners)
- Works for dynamically added elements
- Simpler cleanup (remove one listener)

---

## Q29. What is the difference between `==` and `Object.is()`?

```javascript
// == uses coercion, === is strict, Object.is() handles edge cases

// Edge cases where === gives surprising results:
NaN === NaN;    // false (NaN is not equal to itself!)
+0 === -0;      // true (they're "equal" in ===)

// Object.is() — most precise equality
Object.is(NaN, NaN);  // true ✅
Object.is(+0, -0);    // false ✅
Object.is(1, 1);      // true
Object.is(null, null); // true

// React uses Object.is() internally for state comparison
// useState/useMemo/useEffect dependency comparison all use Object.is()
```

---

## Q30. What is IIFE?

**Answer:** An Immediately Invoked Function Expression — a function that runs the moment it's defined.

```javascript
// IIFE syntax
(function() {
  const private = 'I am private'; // Not accessible outside
  console.log('IIFE ran!');
})();

// Arrow IIFE
(() => {
  console.log('Arrow IIFE');
})();

// With parameters
(function(name) {
  console.log(`Hello, ${name}`);
})('Alice');

// Use cases:
// 1. Create a private scope (before let/const existed)
// 2. Avoid polluting global scope
// 3. Execute async code at module level
(async () => {
  const data = await fetch('/api/data').then(r => r.json());
  console.log(data);
})();
```

---

# Intermediate JS Questions

---

## Q31. How Does the Event Loop Handle Promises vs setTimeout?

```javascript
console.log('A');

setTimeout(() => console.log('B'), 0);

Promise.resolve()
  .then(() => console.log('C'))
  .then(() => console.log('D'));

console.log('E');

// EXECUTION ORDER:
// 1. Call stack runs sync code: A, then E
// 2. Call stack is empty → check microtask queue
// 3. Microtasks run: C, then D (each .then is a separate microtask)
// 4. Microtask queue empty → check macrotask queue
// 5. Macrotask: B

// Output: A E C D B
```

**Why Promises run before setTimeout:**
- Promises use the **microtask queue** (checked after every task)
- setTimeout uses the **macrotask queue** (checked after microtasks are empty)
- The event loop processes ALL microtasks before picking the next macrotask

```javascript
// Microtask starvation (advanced)
function starve() {
  Promise.resolve().then(starve); // Infinite microtasks
}
starve();
// setTimeout(() => console.log('Never runs'), 0); // NEVER executes
// Microtasks keep the macrotask from running — the event loop is starved
```

---

## Q32. What is a Generator Function?

**Answer:** A function that can be **paused and resumed**, yielding multiple values lazily one at a time.

```javascript
function* fibonacci() {
  let [prev, curr] = [0, 1];
  
  while (true) {              // Infinite sequence — but lazy!
    yield curr;               // Pause here, return curr
    [prev, curr] = [curr, prev + curr];
  }
}

const fib = fibonacci();
fib.next(); // { value: 1, done: false }
fib.next(); // { value: 1, done: false }
fib.next(); // { value: 2, done: false }
fib.next(); // { value: 3, done: false }
fib.next(); // { value: 5, done: false }

// Using for...of (automatically stops when done: true)
function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}

for (const n of range(0, 10, 2)) {
  console.log(n); // 0, 2, 4, 6, 8
}

// Generators as coroutines — send values back in
function* chat() {
  const name = yield 'What is your name?';
  const age = yield `Hello ${name}! How old are you?`;
  yield `${name} is ${age} years old.`;
}

const conv = chat();
conv.next();               // { value: 'What is your name?', done: false }
conv.next('Alice');        // { value: 'Hello Alice! How old are you?', done: false }
conv.next(30);             // { value: 'Alice is 30 years old.', done: false }
```

---

## Q33. Explain Microtask vs Macrotask Queue

| Queue         | Type        | Examples                                              | Priority |
|---------------|-------------|-------------------------------------------------------|----------|
| Microtask     | Microtask   | Promise.then, Promise.catch, queueMicrotask, MutationObserver | High — runs between tasks |
| Macrotask     | Macrotask   | setTimeout, setInterval, setImmediate (Node), I/O, UI paint | Low — one per event loop tick |

```javascript
// Complex execution order example
console.log('1');

setTimeout(() => console.log('2'), 0);          // Macrotask 1

Promise.resolve().then(() => {
  console.log('3');
  setTimeout(() => console.log('4'), 0);        // Macrotask 2 (scheduled from microtask)
  Promise.resolve().then(() => console.log('5')); // Another microtask
});

setTimeout(() => console.log('6'), 0);          // Macrotask 3

console.log('7');

// ANSWER: 1, 7, 3, 5, 2, 6, 4
// Sync: 1, 7
// Microtasks (after sync): 3, then schedule M2 and new microtask → 5
// Macrotask 1 (M1): 2
// (microtask queue now empty before each macrotask)
// Macrotask 3 (M3, because M2 was added after M1 was queued, but after M1 itself): 6
// Macrotask 2 (M2): 4
```

---

## Q34. What are WeakMap and WeakSet?

**Answer:** WeakMap and WeakSet hold **weak references** — they don't prevent garbage collection of their keys/values.

```javascript
// WeakMap — keys must be objects, values can be anything
const cache = new WeakMap();

function processElement(element) {
  if (cache.has(element)) {
    return cache.get(element); // Cached result
  }
  
  const result = expensiveCalculation(element);
  cache.set(element, result);
  return result;
}

// When 'element' (a DOM node) is removed from DOM:
// The WeakMap's reference is weak → GC can collect it
// Regular Map would prevent GC → memory leak!

// Key differences from Map:
// - Keys must be objects (not primitives)
// - Not iterable (can't loop or get .size)
// - GC can collect keys (weak references)

// WeakSet — stores objects, prevents GC retention
const seen = new WeakSet();

function markAsSeen(obj) {
  seen.add(obj);
}

function hasSeen(obj) {
  return seen.has(obj);
}
// When obj is no longer referenced elsewhere → WeakSet entry is collected

// Use cases:
// 1. Associate metadata with DOM elements without preventing GC
// 2. Track visited objects without memory leaks
// 3. Private data per instance (before private class fields)
```

---

## Q35. Implement Debounce from Scratch

**What:** Delay execution of a function until after a specified time has passed since the last call. Used for search input, resize handlers.

```javascript
/**
 * debounce — delays fn execution until after 'delay' ms of inactivity
 * @param {Function} fn - The function to debounce
 * @param {number} delay - Delay in milliseconds
 * @param {boolean} immediate - If true, call fn on leading edge instead of trailing
 */
function debounce(fn, delay, immediate = false) {
  let timeoutId = null;
  
  function debounced(...args) {
    const callNow = immediate && !timeoutId;
    
    // Clear existing timeout
    clearTimeout(timeoutId);
    
    // Set new timeout
    timeoutId = setTimeout(() => {
      timeoutId = null;
      if (!immediate) {
        fn.apply(this, args);
      }
    }, delay);
    
    // Call immediately on first call (leading edge)
    if (callNow) {
      fn.apply(this, args);
    }
  }
  
  // Cancel method to cancel pending execution
  debounced.cancel = () => {
    clearTimeout(timeoutId);
    timeoutId = null;
  };
  
  return debounced;
}

// Usage:
const handleSearch = debounce((query) => {
  console.log('Searching for:', query);
  // API call here
}, 300);

// User types rapidly — only the LAST call within 300ms fires
handleSearch('r');
handleSearch('re');
handleSearch('rea');
handleSearch('reac');
handleSearch('react');  // Only this fires (after 300ms of no typing)
```

---

## Q36. Implement Throttle from Scratch

**What:** Ensure a function is called at most once per specified time period. Used for scroll handlers, resize events, button rapid clicks.

```javascript
/**
 * throttle — ensures fn is called at most once per 'limit' ms
 */
function throttle(fn, limit) {
  let lastRan = null;
  let timeoutId = null;
  
  return function(...args) {
    const now = Date.now();
    
    if (lastRan === null) {
      // First call — run immediately
      fn.apply(this, args);
      lastRan = now;
    } else {
      const elapsed = now - lastRan;
      clearTimeout(timeoutId);
      
      // Schedule to run after remaining time
      timeoutId = setTimeout(() => {
        fn.apply(this, args);
        lastRan = Date.now();
      }, limit - elapsed);
    }
  };
}

// Alternative (simpler — trailing edge only):
function throttleSimple(fn, limit) {
  let isThrottled = false;
  
  return function(...args) {
    if (isThrottled) return; // Skip if throttled
    
    fn.apply(this, args);
    isThrottled = true;
    
    setTimeout(() => {
      isThrottled = false;
    }, limit);
  };
}

// Usage:
const handleScroll = throttle(() => {
  console.log('Scroll position:', window.scrollY);
}, 100); // At most once per 100ms

window.addEventListener('scroll', handleScroll);
```

**Debounce vs Throttle:**
```
Debounce: "Wait until you stop calling me, THEN execute"
          ████░░░░░░░░░░░░░░░░░░░░████░░░░░░░░░░░░░░███
          (Multiple rapid calls → one execution after pause)

Throttle: "Execute at most once per period, no matter how many calls"
          ██░░██░░██░░██░░██░░██
          (Periodic execution during rapid calls)
```

---

## Q37. Implement Custom Promise.all

```javascript
function promiseAll(promises) {
  // Return a new Promise
  return new Promise((resolve, reject) => {
    // Handle empty array
    if (promises.length === 0) {
      resolve([]);
      return;
    }
    
    const results = new Array(promises.length);
    let resolvedCount = 0;
    
    promises.forEach((promise, index) => {
      // Wrap in Promise.resolve in case it's not a Promise
      Promise.resolve(promise)
        .then((value) => {
          results[index] = value;   // Maintain order (not by completion time)
          resolvedCount++;
          
          // Resolve only when ALL promises resolved
          if (resolvedCount === promises.length) {
            resolve(results);
          }
        })
        .catch((error) => {
          reject(error);            // Reject immediately on ANY failure
        });
    });
  });
}

// Test:
promiseAll([
  Promise.resolve(1),
  Promise.resolve(2),
  Promise.resolve(3),
]).then(console.log); // [1, 2, 3]

promiseAll([
  Promise.resolve(1),
  Promise.reject('Error!'),
  Promise.resolve(3),
]).catch(console.error); // "Error!"
```

---

## Q38. Implement Memoize Function

```javascript
function memoize(fn) {
  const cache = new Map();
  
  return function(...args) {
    // Create cache key from arguments
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// With WeakMap for object arguments (allows GC):
function memoizeWeak(fn) {
  const cache = new WeakMap();
  
  return function(arg) {
    if (typeof arg === 'object' && arg !== null) {
      if (cache.has(arg)) return cache.get(arg);
      const result = fn(arg);
      cache.set(arg, result);
      return result;
    }
    return fn(arg); // Non-object args — no caching
  };
}

// With max size (LRU cache):
function memoizeWithLimit(fn, maxSize = 100) {
  const cache = new Map();
  
  return function(...args) {
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      // Move to end (most recently used)
      const value = cache.get(key);
      cache.delete(key);
      cache.set(key, value);
      return value;
    }
    
    const result = fn.apply(this, args);
    
    if (cache.size >= maxSize) {
      // Delete oldest (first item in Map — insertion order)
      const firstKey = cache.keys().next().value;
      cache.delete(firstKey);
    }
    
    cache.set(key, result);
    return result;
  };
}
```

---

## Q39. Implement Deep Clone

```javascript
function deepClone(value, seen = new WeakMap()) {
  // Handle primitives and null
  if (value === null || typeof value !== 'object') return value;
  
  // Handle circular references
  if (seen.has(value)) return seen.get(value);
  
  // Handle Date
  if (value instanceof Date) return new Date(value.getTime());
  
  // Handle RegExp
  if (value instanceof RegExp) return new RegExp(value.source, value.flags);
  
  // Handle Array
  if (Array.isArray(value)) {
    const clone = [];
    seen.set(value, clone);
    for (let i = 0; i < value.length; i++) {
      clone[i] = deepClone(value[i], seen);
    }
    return clone;
  }
  
  // Handle Map
  if (value instanceof Map) {
    const clone = new Map();
    seen.set(value, clone);
    for (const [k, v] of value) {
      clone.set(deepClone(k, seen), deepClone(v, seen));
    }
    return clone;
  }
  
  // Handle Set
  if (value instanceof Set) {
    const clone = new Set();
    seen.set(value, clone);
    for (const item of value) {
      clone.add(deepClone(item, seen));
    }
    return clone;
  }
  
  // Handle plain object
  const clone = Object.create(Object.getPrototypeOf(value));
  seen.set(value, clone);
  
  for (const key of Object.keys(value)) {
    clone[key] = deepClone(value[key], seen);
  }
  
  // Handle Symbol keys
  for (const sym of Object.getOwnPropertySymbols(value)) {
    clone[sym] = deepClone(value[sym], seen);
  }
  
  return clone;
}

// Test:
const obj = {
  a: 1,
  b: { c: [1, 2, 3] },
  d: new Date(),
  e: /regex/gi,
};
const clone = deepClone(obj);
clone.b.c.push(4);
console.log(obj.b.c.length);   // 3 — original unchanged
console.log(clone.b.c.length); // 4
```

---

## Q40. What is `Promise.allSettled`, `Promise.race`, `Promise.any`?

```javascript
// Promise.allSettled — waits for ALL to settle (no rejection on failure)
Promise.allSettled([
  Promise.resolve(1),
  Promise.reject('Error'),
  Promise.resolve(3),
]).then(results => {
  results.forEach(result => {
    if (result.status === 'fulfilled') console.log('OK:', result.value);
    if (result.status === 'rejected') console.log('ERR:', result.reason);
  });
});
// OK: 1, ERR: Error, OK: 3

// Promise.race — resolves/rejects with FIRST settled promise
Promise.race([
  new Promise(resolve => setTimeout(() => resolve('slow'), 1000)),
  new Promise(resolve => setTimeout(() => resolve('fast'), 100)),
]).then(console.log); // 'fast'

// Use case: timeout
const withTimeout = (promise, ms) => Promise.race([
  promise,
  new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), ms)),
]);

// Promise.any — resolves with FIRST successful, rejects only if ALL fail
Promise.any([
  Promise.reject('err1'),
  Promise.resolve('success!'),
  Promise.resolve('also ok'),
]).then(console.log); // 'success!'
```

---

# Advanced JS Questions

---

## Q41. How Does V8 JIT Compilation Work?

**Answer:** V8 (Chrome/Node.js JS engine) uses **Just-In-Time compilation** to optimize code at runtime.

```
Source Code
     │
     ↓
  Parser
     │
     ↓
  AST (Abstract Syntax Tree)
     │
     ↓
  Ignition (Interpreter)     ← Fast startup, generates bytecode
     │
     │ Collects profiling data
     │ Identifies "hot" (frequently executed) code
     ↓
  TurboFan (Optimizing Compiler) ← Compiles hot code to machine code
     │
     │ If assumptions break (type changes) → deoptimization
     ↓
  Optimized Machine Code    ← ~10-100x faster than interpreted
```

**How to write V8-friendly code:**
```javascript
// ✅ Consistent types — V8 can optimize with hidden classes
function Point(x, y) {
  this.x = x;
  this.y = y;
}

const p1 = new Point(1, 2); // Hidden class A: {x, y}
const p2 = new Point(3, 4); // Same hidden class A — optimized!

// ❌ Inconsistent property assignment order — different hidden classes
function BadPoint(x, y, flip) {
  if (flip) {
    this.y = y;
    this.x = x;
  } else {
    this.x = x;
    this.y = y;
  }
  // V8 creates TWO different hidden classes — deoptimizes!
}

// ✅ Monomorphic functions (always called with same types) — fast
function add(a, b) { return a + b; }
add(1, 2);    // number + number → V8 optimizes
add(3, 4);    // Same types → uses optimized version

// ❌ Polymorphic functions (different types) — slower
add('hello', ' world'); // Now V8 must handle both number and string cases
```

---

## Q42. What Are Hidden Classes in V8?

**Answer:** V8 creates internal "hidden classes" (similar to C++ struct layouts) for objects to speed up property access. Objects with the same properties added in the same order share hidden classes and benefit from optimized property access.

```javascript
// These two objects share a hidden class → fast property access
const obj1 = {};
obj1.x = 1;
obj1.y = 2;

const obj2 = {};
obj2.x = 10;
obj2.y = 20;

// ❌ Different property addition order → different hidden classes → slower
const obj3 = {};
obj3.y = 2;    // y first
obj3.x = 1;   // then x — different hidden class than obj1!

// ❌ Deleting properties → degrades hidden class
delete obj1.x; // obj1 goes to a "dictionary mode" object — slow!

// Best practice: initialize all properties in constructor in consistent order
function createUser(name, age) {
  return {
    name,  // Always in this order
    age,
    role: 'user',
  };
}
```

---

## Q43. Implement Custom bind()

```javascript
Function.prototype.myBind = function(thisArg, ...boundArgs) {
  // 'this' here is the function being bound
  const fn = this;
  
  return function(...callArgs) {
    // Merge bound args with call-time args
    return fn.apply(thisArg, [...boundArgs, ...callArgs]);
  };
};

// Test:
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const boundGreet = greet.myBind({ name: 'Alice' }, 'Hello');
console.log(boundGreet('!')); // "Hello, Alice!"
console.log(boundGreet('?')); // "Hello, Alice?"
```

---

## Q44. Implement Custom Array.prototype.map()

```javascript
Array.prototype.myMap = function(callbackFn, thisArg) {
  // Validate callback
  if (typeof callbackFn !== 'function') {
    throw new TypeError(callbackFn + ' is not a function');
  }
  
  const result = new Array(this.length);
  
  for (let i = 0; i < this.length; i++) {
    // Skip holes in sparse arrays (like native map does)
    if (i in this) {
      result[i] = callbackFn.call(thisArg, this[i], i, this);
    }
  }
  
  return result;
};

// Test:
[1, 2, 3].myMap(x => x * 2); // [2, 4, 6]
```

---

## Q45. Implement Curry Function

**What:** Currying transforms a function with multiple args into a sequence of functions, each accepting one argument.

```javascript
function curry(fn) {
  return function curried(...args) {
    // If enough arguments provided, call fn
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    
    // Otherwise, return new function that remembers current args
    return function(...moreArgs) {
      return curried.apply(this, [...args, ...moreArgs]);
    };
  };
}

// Usage:
function add(a, b, c) {
  return a + b + c;
}

const curriedAdd = curry(add);

curriedAdd(1)(2)(3);    // 6 — one arg at a time
curriedAdd(1, 2)(3);   // 6 — two args, then one
curriedAdd(1)(2, 3);   // 6 — one, then two
curriedAdd(1, 2, 3);   // 6 — all at once

// Real use case:
const add10 = curriedAdd(10);    // Partially applied
const add10And5 = add10(5);      // Further applied
add10And5(3);                    // 18

// Functional programming style:
const users = [{ name: 'Alice', role: 'admin' }, { name: 'Bob', role: 'user' }];
const getProp = curry((prop, obj) => obj[prop]);
const getName = getProp('name');
users.map(getName); // ['Alice', 'Bob']
```

---

## Q46. Implement pipe() and compose()

```javascript
// pipe — left to right: pipe(f, g, h)(x) = h(g(f(x)))
function pipe(...fns) {
  return function(value) {
    return fns.reduce((acc, fn) => fn(acc), value);
  };
}

// compose — right to left: compose(f, g, h)(x) = f(g(h(x)))
function compose(...fns) {
  return function(value) {
    return fns.reduceRight((acc, fn) => fn(acc), value);
  };
}

// Usage:
const double = x => x * 2;
const addOne = x => x + 1;
const square = x => x ** 2;

const transform = pipe(double, addOne, square);
transform(3); // pipe: double(3)=6 → addOne(6)=7 → square(7) = 49

const transform2 = compose(square, addOne, double);
transform2(3); // compose: double(3)=6 → addOne(6)=7 → square(7) = 49
// Same result! compose(f,g,h) = pipe(h,g,f)

// Real-world data transformation pipeline:
const processUser = pipe(
  user => ({ ...user, name: user.name.trim() }),
  user => ({ ...user, email: user.email.toLowerCase() }),
  user => ({ ...user, displayName: `${user.name} (${user.role})` }),
  user => ({ ...user, createdAt: new Date() }),
);
```

---

## Q47. What is Tail Call Optimization?

**Answer:** TCO is when the engine reuses the current stack frame for a recursive call in "tail position" (the very last action), preventing stack overflow.

```javascript
// Regular recursion — creates N stack frames (may stack overflow for large N)
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1); // NOT tail position — multiply happens after call
}

// Tail-recursive — call is the LAST thing (accumulator pattern)
function factorialTail(n, acc = 1) {
  if (n <= 1) return acc;
  return factorialTail(n - 1, n * acc); // Tail call — can reuse stack frame
}

// In practice — JS engines (V8) don't reliably implement TCO
// Alternative: use trampolining or iteration
function factorialIterative(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}
```

---

## Q48. Advanced: Implement an Observable/Event Emitter

```javascript
class EventEmitter {
  constructor() {
    this._events = new Map(); // eventName → Set of listeners
  }
  
  on(event, listener) {
    if (!this._events.has(event)) {
      this._events.set(event, new Set());
    }
    this._events.get(event).add(listener);
    return this; // Chainable
  }
  
  once(event, listener) {
    // Wrapper that removes itself after first call
    const wrapper = (...args) => {
      listener.apply(this, args);
      this.off(event, wrapper);
    };
    wrapper._originalListener = listener; // For removal
    return this.on(event, wrapper);
  }
  
  off(event, listener) {
    if (!this._events.has(event)) return this;
    
    const listeners = this._events.get(event);
    for (const l of listeners) {
      if (l === listener || l._originalListener === listener) {
        listeners.delete(l);
        break;
      }
    }
    
    if (listeners.size === 0) this._events.delete(event);
    return this;
  }
  
  emit(event, ...args) {
    if (!this._events.has(event)) return false;
    
    for (const listener of [...this._events.get(event)]) { // Copy to avoid mutation
      listener.apply(this, args);
    }
    return true;
  }
  
  removeAllListeners(event) {
    if (event) {
      this._events.delete(event);
    } else {
      this._events.clear();
    }
    return this;
  }
  
  listenerCount(event) {
    return this._events.has(event) ? this._events.get(event).size : 0;
  }
}

// Usage:
const emitter = new EventEmitter();

emitter.on('data', (payload) => console.log('Received:', payload));
emitter.once('connect', () => console.log('Connected!'));

emitter.emit('connect');         // "Connected!"
emitter.emit('connect');         // Nothing — once only fires once
emitter.emit('data', { id: 1 }); // "Received: { id: 1 }"
```

---

# JavaScript Output Questions

---

## OQ1 — var Hoisting in Functions

```javascript
var x = 1;

function test() {
  console.log(x);  // What prints?
  var x = 2;
  console.log(x);  // What prints?
}

test();
console.log(x);    // What prints?
```

**Answer:** `undefined`, `2`, `1`

**Explanation:**
- Inside `test()`, `var x` is hoisted to the top of the function scope → `x` is `undefined` at the first log
- After `var x = 2`, `x` is `2` → second log prints `2`
- The outer `x = 1` is unchanged → last log prints `1`

---

## OQ2 — Closure in Loop

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i);
  }, i * 1000);
}
```

**Answer:** `3`, `3`, `3` (printed at 0s, 1s, 2s intervals)

**Explanation:**
- `var` is function-scoped — there is ONE `i` shared by all closures
- When setTimeout callbacks run, the loop is done → `i` is `3`
- All three callbacks reference the SAME `i`

**Fix:**
```javascript
for (let i = 0; i < 3; i++) { // let creates new binding per iteration
  setTimeout(() => console.log(i), i * 1000);
}
// Output: 0, 1, 2
```

---

## OQ3 — Event Loop Order

```javascript
async function main() {
  console.log('A');
  
  await Promise.resolve();
  
  console.log('B');
}

main();
console.log('C');
```

**Answer:** `A`, `C`, `B`

**Explanation:**
- `main()` runs: prints `A`
- `await` suspends `main()` — schedules continuation as microtask
- Control returns to caller: prints `C`
- Microtask runs: prints `B`

---

## OQ4 — Promise Chaining Order

```javascript
Promise.resolve(1)
  .then(x => { console.log(x); return x + 1; })
  .then(x => { console.log(x); return x + 1; })
  .then(x => console.log(x));

Promise.resolve(10)
  .then(x => console.log(x));
```

**Answer:** `1`, `10`, `2`, `3`

**Explanation:**
- `.then()` callbacks are microtasks, scheduled in order
- After sync code: queue has `[then(1→2), then(10)]`
- Run `then(1→2)`: prints `1`, schedules `then(2→3)`
- Queue: `[then(10), then(2→3)]`
- Run `then(10)`: prints `10`
- Queue: `[then(2→3)]`
- Run `then(2→3)`: prints `2`, schedules last `then(3)`
- Run last then: prints `3`

---

## OQ5 — typeof Tricky Cases

```javascript
console.log(typeof undefined);     // ?
console.log(typeof null);          // ?
console.log(typeof []);            // ?
console.log(typeof {});            // ?
console.log(typeof function(){}); // ?
console.log(typeof class{});       // ?
console.log(typeof NaN);           // ?
console.log(typeof 42n);           // ?
```

**Answers:**
```
"undefined"
"object"      ← bug
"object"      ← arrays are objects
"object"
"function"    ← functions are callable objects
"function"    ← classes are functions
"number"      ← NaN is "Not a Number" but type is number!
"bigint"
```

---

## OQ6 — Equality Coercion

```javascript
console.log(0 == false);           // ?
console.log("" == false);          // ?
console.log(null == undefined);    // ?
console.log(null == false);        // ?
console.log([] == false);          // ?
console.log([] == ![]);            // ?
```

**Answers:**
```
true   // false → 0, then 0 == 0
true   // "" → 0, false → 0, then 0 == 0
true   // Special case in spec
false  // null only == undefined (not false, 0, etc.)
true   // [] → "" → 0, false → 0, then 0 == 0
true   // [] → 0, ![] = false → 0, then 0 == 0
```

---

## OQ7 — this in Different Contexts

```javascript
const obj = {
  name: 'Alice',
  
  regularFunc: function() {
    return this.name;
  },
  
  arrowFunc: () => {
    return this.name;
  },
  
  nestedRegular: function() {
    function inner() {
      return this.name;
    }
    return inner();
  },
  
  nestedArrow: function() {
    const inner = () => this.name;
    return inner();
  },
};

console.log(obj.regularFunc());  // ?
console.log(obj.arrowFunc());    // ?
console.log(obj.nestedRegular()); // ?
console.log(obj.nestedArrow());  // ?
```

**Answers:**
```
'Alice'     // 'this' = obj
undefined   // Arrow: 'this' = outer scope (module = {})
undefined   // inner() called without context → this = window/undefined (strict)
'Alice'     // Arrow inherits 'this' from nestedArrow → obj
```

---

## OQ8 — Short-Circuit Evaluation

```javascript
let a = 0;
const result1 = a || 'default';
const result2 = a ?? 'default';
const result3 = a && 'value';

console.log(result1); // ?
console.log(result2); // ?
console.log(result3); // ?

let x = null;
const result4 = x?.foo?.bar ?? 'fallback';
console.log(result4); // ?
```

**Answers:**
```
'default'   // 0 is falsy → || returns right side
0           // 0 is NOT null/undefined → ?? returns left side
0           // 0 is falsy → && returns left side (short-circuits)
'fallback'  // x?.foo → undefined → undefined?.bar → undefined ?? 'fallback'
```

---

## OQ9 — Prototype Chain

```javascript
function Animal(name) {
  this.name = name;
}
Animal.prototype.speak = function() {
  return `${this.name} makes a sound`;
};

function Dog(name) {
  Animal.call(this, name);
}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.bark = function() {
  return `${this.name} barks`;
};

const dog = new Dog('Rex');

console.log(dog instanceof Dog);         // ?
console.log(dog instanceof Animal);      // ?
console.log(dog.constructor === Dog);    // ?
console.log(dog.hasOwnProperty('name')); // ?
console.log(dog.hasOwnProperty('bark')); // ?
```

**Answers:**
```
true    // dog's chain includes Dog.prototype
true    // dog's chain includes Animal.prototype
true    // We manually fixed constructor
true    // 'name' is set directly on the instance
false   // 'bark' is on Dog.prototype, not the instance itself
```

---

## OQ10 — Closure Counter

```javascript
function makeAdder(x) {
  return function(y) {
    return x + y;
  };
}

const add5 = makeAdder(5);
const add10 = makeAdder(10);

console.log(add5(3));          // ?
console.log(add10(3));         // ?
console.log(add5(add10(2)));   // ?
```

**Answers:** `8`, `13`, `17`

---

## OQ11 — Promise Resolution

```javascript
const p = new Promise((resolve, reject) => {
  resolve(1);
  reject(2);       // What happens to this?
  resolve(3);      // And this?
});

p.then(console.log).catch(console.error);
```

**Answer:** `1`

**Explanation:** A Promise can only settle once. Once `resolve(1)` is called, the Promise is settled as fulfilled. Subsequent calls to `resolve` or `reject` are silently ignored.

---

## OQ12 — Async/Await Error Handling

```javascript
async function failing() {
  throw new Error('oops');
}

async function main() {
  const result = await failing().catch(err => 'recovered: ' + err.message);
  console.log(result);
}

main();
```

**Answer:** `"recovered: oops"`

**Explanation:** `async` functions always return a Promise. `throw` inside async function → rejected Promise. `.catch()` on the promise returns a resolved Promise with the return value of the catch handler.

---

## OQ13 — Spread and Rest

```javascript
function test(a, b, ...rest) {
  console.log(a, b, rest);
}

const arr = [1, 2, 3, 4, 5];
test(...arr);
```

**Answer:** `1  2  [3, 4, 5]`

---

## OQ14 — Object Property Shorthand

```javascript
const x = 1;
const y = 2;

const obj = { x, y, z: x + y };
console.log(obj);
```

**Answer:** `{ x: 1, y: 2, z: 3 }`

---

## OQ15 — Destructuring Default Values

```javascript
const { a = 1, b = 2, c = 3 } = { a: 10, b: undefined, c: null };

console.log(a, b, c);
```

**Answer:** `10  2  null`

**Explanation:**
- `a = 10` — value exists and is not undefined → `10`
- `b = 2` — value is `undefined` → use default → `2`
- `c = null` — value is `null` (NOT undefined) → `null` (default NOT applied!)

---

## OQ16-25 — Additional Output Questions

**OQ16:**
```javascript
console.log(1 + '2' + 3);   // '123' (left to right, + with string = concat)
console.log(1 + 2 + '3');   // '33' (1+2=3, then 3+'3'='33')
console.log('3' - 1);       // 2 (- triggers numeric coercion)
console.log('3' * '4');     // 12 (both coerced to numbers)
```

**OQ17:**
```javascript
let a = { val: 1 };
let b = a;
b.val = 2;
console.log(a.val); // 2 — objects are reference types
```

**OQ18:**
```javascript
console.log([] + []);  // "" (both convert to "")
console.log([] + {});  // "[object Object]" ([] → "", {} → "[object Object]")
console.log({} + []); // In eval: "[object Object]"  In console: 0 (ambiguity!)
```

**OQ19:**
```javascript
const arr = [1, 2, 3];
console.log(arr[10]);   // undefined (no ReferenceError for arrays)
console.log(10 in arr); // false
console.log(2 in arr);  // true
```

**OQ20:**
```javascript
async function a() { return 1; }
async function b() { return Promise.resolve(2); }

a().then(console.log); // 1
b().then(console.log); // 2
```

**OQ21 — Generator:**
```javascript
function* gen() {
  yield 1;
  yield 2;
  return 3;
  yield 4; // Never reached
}

const g = gen();
console.log(g.next()); // { value: 1, done: false }
console.log(g.next()); // { value: 2, done: false }
console.log(g.next()); // { value: 3, done: true }
console.log(g.next()); // { value: undefined, done: true }
```

**OQ22 — Map vs Object:**
```javascript
const map = new Map();
map.set('a', 1);
map.set('b', 2);

for (const [key, val] of map) {
  console.log(key, val); // 'a' 1, 'b' 2
}
console.log(map.size); // 2
```

**OQ23 — Nullish:**
```javascript
const value = 0;
console.log(value || 'default');  // 'default'
console.log(value ?? 'default');  // 0
console.log(value?.toString());   // '0'
```

**OQ24 — WeakRef:**
```javascript
const obj = { name: 'Alice' };
const ref = new WeakRef(obj);
console.log(ref.deref()?.name); // 'Alice'
// If GC has not collected obj yet
```

**OQ25 — Symbol:**
```javascript
const s1 = Symbol('test');
const s2 = Symbol('test');
console.log(s1 === s2);         // false — every Symbol is unique
console.log(typeof s1);         // 'symbol'
console.log(s1.toString());     // 'Symbol(test)'
console.log(s1.description);    // 'test'
```

---

# JS Machine Coding Questions

---

## MC1. Implement LRU Cache

```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map(); // Maintains insertion order
  }
  
  get(key) {
    if (!this.cache.has(key)) return -1;
    
    // Move to most recently used (delete + re-insert = move to end)
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }
  
  put(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key); // Remove to re-insert at end
    } else if (this.cache.size >= this.capacity) {
      // Delete least recently used (first item — Map maintains insertion order)
      const lruKey = this.cache.keys().next().value;
      this.cache.delete(lruKey);
    }
    
    this.cache.set(key, value);
  }
}

// Test:
const lru = new LRUCache(3);
lru.put('a', 1); // cache: [a]
lru.put('b', 2); // cache: [a, b]
lru.put('c', 3); // cache: [a, b, c]
lru.get('a');    // cache: [b, c, a] — a moved to end
lru.put('d', 4); // cache: [c, a, d] — b evicted (least recently used)
console.log(lru.get('b')); // -1 — b was evicted
```

---

## MC2. Implement Custom EventEmitter

*(Covered in Q48 above — production-quality implementation)*

---

## MC3. Retry Function with Delay

```javascript
async function retry(fn, options = {}) {
  const {
    maxAttempts = 3,
    delay = 1000,
    backoff = 2,           // Exponential backoff factor
    onRetry = (err, attempt) => console.warn(`Attempt ${attempt} failed:`, err),
  } = options;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      
      onRetry(error, attempt);
      
      const waitTime = delay * Math.pow(backoff, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
}

// Usage:
const data = await retry(
  () => fetch('/api/data').then(r => r.json()),
  { maxAttempts: 3, delay: 500, backoff: 2 }
);
// Retry at 500ms, 1000ms, 2000ms if needed
```

---

## MC4. Flatten Nested Array

```javascript
// Recursive approach
function flatten(arr, depth = Infinity) {
  return arr.reduce((acc, item) => {
    if (Array.isArray(item) && depth > 0) {
      acc.push(...flatten(item, depth - 1));
    } else {
      acc.push(item);
    }
    return acc;
  }, []);
}

// Stack-based (iterative — no stack overflow for huge arrays)
function flattenIterative(arr) {
  const stack = [...arr];
  const result = [];
  
  while (stack.length) {
    const item = stack.pop();
    if (Array.isArray(item)) {
      stack.push(...item); // Expand array back to stack
    } else {
      result.unshift(item); // Add to front (maintaining order)
    }
  }
  
  return result;
}

// Test:
flatten([1, [2, [3, [4]]]]); // [1, 2, 3, 4]
flatten([1, [2, [3, [4]]]], 1); // [1, 2, [3, [4]]]
```

---

## MC5. GroupBy Function

```javascript
function groupBy(arr, keyFn) {
  return arr.reduce((groups, item) => {
    const key = typeof keyFn === 'function' ? keyFn(item) : item[keyFn];
    (groups[key] = groups[key] || []).push(item);
    return groups;
  }, {});
}

// Usage:
const people = [
  { name: 'Alice', dept: 'Engineering' },
  { name: 'Bob', dept: 'Design' },
  { name: 'Charlie', dept: 'Engineering' },
];

groupBy(people, 'dept');
// { Engineering: [{Alice}, {Charlie}], Design: [{Bob}] }

groupBy([1, 2, 3, 4, 5], n => n % 2 === 0 ? 'even' : 'odd');
// { odd: [1, 3, 5], even: [2, 4] }
```

---

## MC6. once() Function

```javascript
function once(fn) {
  let called = false;
  let result;
  
  return function(...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result; // Return same result on subsequent calls
  };
}

// Usage:
const initialize = once(() => {
  console.log('Initialized!');
  return { status: 'ready' };
});

initialize(); // "Initialized!" → { status: 'ready' }
initialize(); // → { status: 'ready' } (no log)
initialize(); // → { status: 'ready' } (no log)
```

---

## MC7. chunk() Function

```javascript
function chunk(arr, size) {
  if (size <= 0) throw new Error('Size must be positive');
  
  const result = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

chunk([1, 2, 3, 4, 5, 6, 7], 3); // [[1,2,3], [4,5,6], [7]]
chunk([1, 2, 3], 1);              // [[1], [2], [3]]
chunk([1, 2, 3], 10);             // [[1, 2, 3]]
```

---

## MC8. Deep Equal Check

```javascript
function deepEqual(a, b) {
  // Primitive check (includes null)
  if (a === b) return true;
  
  // Type check
  if (typeof a !== typeof b) return false;
  if (typeof a !== 'object') return false;
  
  // Null check (typeof null === 'object')
  if (a === null || b === null) return false;
  
  // Date
  if (a instanceof Date && b instanceof Date) {
    return a.getTime() === b.getTime();
  }
  
  // Array
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  
  if (Array.isArray(a)) {
    if (a.length !== b.length) return false;
    return a.every((item, i) => deepEqual(item, b[i]));
  }
  
  // Object
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  
  if (keysA.length !== keysB.length) return false;
  
  return keysA.every(key => 
    Object.prototype.hasOwnProperty.call(b, key) && deepEqual(a[key], b[key])
  );
}

deepEqual({ a: 1, b: [2, 3] }, { a: 1, b: [2, 3] }); // true
deepEqual({ a: 1, b: [2, 3] }, { a: 1, b: [2, 4] }); // false
```

---

## MC9. Implement Promise.allSettled from Scratch

```javascript
function allSettled(promises) {
  return Promise.all(
    promises.map(promise =>
      Promise.resolve(promise)
        .then(value => ({ status: 'fulfilled', value }))
        .catch(reason => ({ status: 'rejected', reason }))
    )
  );
}

// Test:
allSettled([
  Promise.resolve(1),
  Promise.reject('error'),
  Promise.resolve(3),
]).then(results => {
  console.log(results);
  // [
  //   { status: 'fulfilled', value: 1 },
  //   { status: 'rejected', reason: 'error' },
  //   { status: 'fulfilled', value: 3 },
  // ]
});
```

---

## MC10. Pipe with Async Functions

```javascript
function asyncPipe(...fns) {
  return async function(value) {
    return fns.reduce(
      async (acc, fn) => fn(await acc),
      Promise.resolve(value)
    );
  };
}

// Usage:
const processOrder = asyncPipe(
  async (order) => ({ ...order, validated: await validateOrder(order) }),
  async (order) => ({ ...order, priced: await calculatePrice(order) }),
  async (order) => ({ ...order, confirmed: await confirmOrder(order) }),
);

const result = await processOrder({ items: [...] });
```

---

## MC11. Implement setTimeout using requestAnimationFrame

```javascript
function setTimeoutRAF(callback, delay) {
  const start = performance.now();
  let handle;
  
  function tick(timestamp) {
    if (timestamp - start >= delay) {
      callback();
    } else {
      handle = requestAnimationFrame(tick);
    }
  }
  
  handle = requestAnimationFrame(tick);
  
  return {
    cancel: () => cancelAnimationFrame(handle)
  };
}
```

---

## MC12. Implement Intersection of Two Arrays

```javascript
function intersection(arr1, arr2) {
  const set = new Set(arr2);
  return [...new Set(arr1.filter(item => set.has(item)))];
}

intersection([1, 2, 3, 4], [2, 4, 6]); // [2, 4]
intersection([1, 1, 2, 3], [1, 3, 5]); // [1, 3] — unique values
```

---

## MC13. Implement Promisify

```javascript
function promisify(fn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (error, result) => {
        if (error) reject(error);
        else resolve(result);
      });
    });
  };
}

// Usage:
const fs = require('fs');
const readFile = promisify(fs.readFile);

const content = await readFile('./file.txt', 'utf-8');
```

---

## MC14. Implement an Observable (simple)

```javascript
class Observable {
  constructor(subscriberFn) {
    this._subscriberFn = subscriberFn;
  }
  
  subscribe(observer) {
    // Normalize observer
    if (typeof observer === 'function') {
      observer = { next: observer };
    }
    
    const safeObserver = {
      next: (val) => observer.next && observer.next(val),
      error: (err) => observer.error ? observer.error(err) : null,
      complete: () => observer.complete && observer.complete(),
    };
    
    const cleanup = this._subscriberFn(safeObserver);
    return { unsubscribe: () => cleanup && cleanup() };
  }
  
  // Operators (chainable)
  map(fn) {
    return new Observable(observer => {
      return this.subscribe({
        next: value => observer.next(fn(value)),
        error: err => observer.error(err),
        complete: () => observer.complete(),
      }).unsubscribe;
    });
  }
  
  filter(predicate) {
    return new Observable(observer => {
      return this.subscribe({
        next: value => predicate(value) && observer.next(value),
        error: err => observer.error(err),
        complete: () => observer.complete(),
      }).unsubscribe;
    });
  }
}

// Usage:
const obs = new Observable(observer => {
  [1, 2, 3, 4, 5].forEach(n => observer.next(n));
  observer.complete();
});

obs
  .filter(n => n % 2 === 0)
  .map(n => n * 10)
  .subscribe(console.log); // 20, 40
```

---

## MC15. Implement String.prototype.trim() from scratch

```javascript
String.prototype.myTrim = function() {
  // Start from left — find first non-whitespace
  let start = 0;
  while (start < this.length && /\s/.test(this[start])) start++;
  
  // Start from right — find last non-whitespace
  let end = this.length - 1;
  while (end > start && /\s/.test(this[end])) end--;
  
  return this.slice(start, end + 1);
};

'  hello world  '.myTrim(); // 'hello world'
```

---

# SECTION 2: React Interview Questions

---

# Basic React Questions

---

## RQ1. What is React? What is the Virtual DOM?

**Answer:**

**React** is a JavaScript library (not a framework) for building user interfaces. Key characteristics:
- **Component-based:** UI is built from independent, reusable pieces
- **Declarative:** Describe WHAT the UI should look like, React figures out HOW to update it
- **One-way data flow:** Data flows from parent to child via props

**Virtual DOM:**
```
┌───────────────────────────────────────────────────────────────┐
│                   Virtual DOM Process                         │
│                                                               │
│  1. State/Props Change                                        │
│         │                                                     │
│         ↓                                                     │
│  2. React creates new Virtual DOM tree (a JS object tree)     │
│         │                                                     │
│         ↓                                                     │
│  3. Diffing: Compare new Virtual DOM with previous snapshot   │
│     (O(n) algorithm — not O(n³) like naive tree comparison)  │
│         │                                                     │
│         ↓                                                     │
│  4. Reconciliation: Compute minimal set of DOM operations     │
│         │                                                     │
│         ↓                                                     │
│  5. Batch update the real DOM                                 │
│                                                               │
│  Result: Only changed parts of the DOM are updated            │
└───────────────────────────────────────────────────────────────┘
```

**Why is Virtual DOM faster than direct DOM manipulation?**
- Direct DOM manipulation: every change triggers layout, paint, composite
- Virtual DOM: batch all changes → calculate minimum diff → ONE DOM update
- DOM operations are expensive (touching the "live" DOM causes reflows)

---

## RQ2. Functional vs Class Components

| Feature               | Class Component              | Functional Component         |
|-----------------------|------------------------------|------------------------------|
| Syntax                | `class Foo extends Component`| `function Foo() {}`          |
| State                 | `this.state`, `setState()`   | `useState()` hook            |
| Lifecycle             | `componentDidMount`, etc.    | `useEffect()` hook           |
| `this` usage          | Required for state/props     | Not used                     |
| Code size             | Verbose                      | Concise                      |
| Performance           | Slightly heavier (class instance) | Lighter              |
| Can use Hooks?        | ❌ No                         | ✅ Yes                        |
| Industry standard     | Legacy code                  | ✅ Modern standard            |

```jsx
// Class Component
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }
  
  componentDidMount() { document.title = `Count: ${this.state.count}`; }
  componentDidUpdate() { document.title = `Count: ${this.state.count}`; }
  
  render() {
    return (
      <button onClick={() => this.setState({ count: this.state.count + 1 })}>
        Count: {this.state.count}
      </button>
    );
  }
}

// Functional Component — same behavior, less code
function Counter() {
  const [count, setCount] = React.useState(0);
  
  React.useEffect(() => {
    document.title = `Count: ${count}`;
  });
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

---

## RQ3. What are Props?

**Answer:** Props (short for "properties") are how parent components pass data to child components. Props are **read-only** — a component must never modify its own props.

```jsx
// Parent passes props
function App() {
  return (
    <UserCard 
      name="Alice"
      age={30}
      isAdmin={true}
      onEdit={(id) => handleEdit(id)}
      tags={['react', 'js']}
    />
  );
}

// Child receives props (cannot modify them)
function UserCard({ name, age, isAdmin, onEdit, tags }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>Age: {age}</p>
      {isAdmin && <Badge>Admin</Badge>}
      <button onClick={() => onEdit(name)}>Edit</button>
      {tags.map(tag => <span key={tag}>{tag}</span>)}
    </div>
  );
}
```

---

## RQ4. What is State?

**Answer:** State is mutable data **owned and managed by the component itself**. When state changes, the component re-renders.

```jsx
function ToggleButton() {
  const [isOn, setIsOn] = React.useState(false); // isOn = state
  
  return (
    <button 
      onClick={() => setIsOn(prev => !prev)}
      style={{ background: isOn ? 'green' : 'gray' }}
    >
      {isOn ? 'ON' : 'OFF'}
    </button>
  );
}
```

**When to use State:**
- Data that changes over time
- Data specific to this component instance
- When changes should cause a re-render

**When NOT to use State:**
- Derived data (compute it from existing state/props, don't store it)
- Data that doesn't affect rendering (use a ref)
- Server data that should be cached (use React Query)

---

## RQ5. What is JSX?

**Answer:** JSX (JavaScript XML) is a syntax extension that lets you write HTML-like code inside JavaScript. It gets compiled by Babel into `React.createElement()` calls.

```jsx
// JSX
const element = <h1 className="title">Hello, {name}!</h1>;

// What Babel compiles it to:
const element = React.createElement(
  'h1',
  { className: 'title' },
  'Hello, ',
  name,
  '!'
);

// JSX Rules:
// 1. Must have one root element (or use Fragment)
// ✅ return <div><h1>Title</h1><p>Body</p></div>
// ✅ return <><h1>Title</h1><p>Body</p></>  (Fragment)
// ❌ return <h1>Title</h1><p>Body</p>  (two root elements)

// 2. Use className instead of class
// ✅ <div className="card">
// ❌ <div class="card">

// 3. Self-close tags that have no children
// ✅ <Input />  <br />  <img src="..." />

// 4. JS expressions in curly braces
// ✅ <p>{2 + 2}</p>  <p>{user.name}</p>  <p>{isAdmin ? 'Admin' : 'User'}</p>
```

---

## RQ6. Why Do We Need Keys in Lists?

**Answer:** Keys help React identify which items in a list have changed, been added, or removed. They are used during reconciliation to match elements between renders.

```jsx
// ❌ Without keys — React re-renders ALL items on every change
{items.map(item => <Item item={item} />)}

// ✅ With keys — React only re-renders changed items
{items.map(item => <Item key={item.id} item={item} />)}
```

**Key rules:**
1. Keys must be **unique among siblings** (not globally unique)
2. Keys must be **stable** (don't use array index if items can be reordered)
3. Use a unique ID from your data, not `Math.random()` or index

```jsx
// ❌ BAD — index as key (breaks when items are reordered or deleted)
{items.map((item, index) => <Item key={index} item={item} />)}

// ❌ WORSE — random key (new key every render = complete re-mount)
{items.map(item => <Item key={Math.random()} item={item} />)}

// ✅ GOOD — stable ID from data
{items.map(item => <Item key={item.id} item={item} />)}
```

---

## RQ7. What is Lifting State Up?

**Answer:** When multiple components need to share the same state, move ("lift") that state up to their closest common ancestor, and pass it down as props.

```jsx
// ❌ Each child tracks its own temperature — they can't stay in sync
function TemperatureInput() {
  const [temp, setTemp] = useState(0);
  return <input value={temp} onChange={e => setTemp(e.target.value)} />;
}

// ✅ Parent owns the state — passes down as props
function TempConverter() {
  const [celsius, setCelsius] = useState(0);
  
  const fahrenheit = (celsius * 9/5) + 32;
  
  return (
    <>
      <TempInput value={celsius} onChange={setCelsius} scale="C" />
      <TempInput value={fahrenheit} onChange={v => setCelsius((v - 32) * 5/9)} scale="F" />
    </>
  );
}
```

---

## RQ8. Controlled vs Uncontrolled Components

| Feature             | Controlled                              | Uncontrolled                         |
|---------------------|-----------------------------------------|--------------------------------------|
| Data stored in      | React state                             | DOM (via ref)                        |
| Read value via      | State variable                          | `ref.current.value`                  |
| Validation          | Real-time, on every keystroke           | Only when needed (on submit)         |
| Code amount         | More                                    | Less                                 |
| Use case            | Dynamic forms, validation, masking      | Simple forms, file inputs            |

```jsx
// Controlled — React is the "source of truth"
function ControlledInput() {
  const [value, setValue] = useState('');
  
  return (
    <input
      value={value}                     // React controls the value
      onChange={e => setValue(e.target.value)}
    />
  );
}

// Uncontrolled — DOM is the "source of truth"
function UncontrolledInput() {
  const inputRef = useRef(null);
  
  const handleSubmit = () => {
    console.log(inputRef.current.value); // Read from DOM when needed
  };
  
  return (
    <>
      <input ref={inputRef} defaultValue="initial" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

---

## RQ9. What is the children Prop?

```jsx
// children — whatever is between the component's opening and closing tags
function Card({ children, title }) {
  return (
    <div className="card">
      <h2 className="card__title">{title}</h2>
      <div className="card__body">{children}</div>
    </div>
  );
}

// Usage:
<Card title="Profile">
  <Avatar src={user.avatar} />
  <p>{user.bio}</p>
  <Button>Follow</Button>
</Card>
// Everything between <Card> and </Card> is the 'children' prop
```

---

## RQ10-30. Additional Basic React Questions (Condensed)

**RQ10: What is React.Fragment?**
```jsx
// Avoids adding extra DOM nodes
<React.Fragment>
  <h1>Title</h1>
  <p>Body</p>
</React.Fragment>

// Shorthand (no key support)
<>
  <h1>Title</h1>
  <p>Body</p>
</>

// Use <React.Fragment key={...}> when mapping (need key)
{items.map(item => (
  <React.Fragment key={item.id}>
    <dt>{item.term}</dt>
    <dd>{item.def}</dd>
  </React.Fragment>
))}
```

**RQ11: What is React.StrictMode?**
```jsx
// Identifies potential problems, double-invokes functions to detect side effects
<React.StrictMode>
  <App />
</React.StrictMode>
// Effects: warns about unsafe lifecycle methods, deprecated APIs
// In dev only — no production impact
```

**RQ12: What are React Portals?**
```jsx
// Render a child into a different DOM node than its parent
function Modal({ children }) {
  return ReactDOM.createPortal(
    children,
    document.getElementById('modal-root') // Outside the main app root
  );
}
// Use case: modals, tooltips, popovers — render outside overflow:hidden parents
```

**RQ13: What is React.memo?**
```jsx
// Memoize a component — only re-renders if props changed
const MemoizedCard = React.memo(UserCard);
const MemoizedCard2 = React.memo(UserCard, (prevProps, nextProps) => {
  return prevProps.userId === nextProps.userId; // Custom comparison
});
```

**RQ14-30 covered in intermediate/advanced sections below...**

---

# Intermediate React Questions

---

## IRQ1. Explain useState Deeply — The Stale Closure Problem

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  
  // ❌ STALE CLOSURE BUG
  const increment = () => {
    // This 'count' is captured at the time this function was created
    setTimeout(() => {
      setCount(count + 1); // 'count' is stale — always 0!
    }, 1000);
  };
  
  // ✅ FIX: Use functional update — React passes the CURRENT state
  const increment = () => {
    setTimeout(() => {
      setCount(prevCount => prevCount + 1); // Always has current state
    }, 1000);
  };
  
  return <button onClick={increment}>{count}</button>;
}
```

**Rules of useState:**
1. State updates are **asynchronous** — `count` doesn't change immediately
2. State updates are **batched** (React 18 batches even in setTimeout)
3. Setting state with the same value (by `Object.is`) → NO re-render
4. State updates trigger a **full component re-render** (and children)

---

## IRQ2. What Does useEffect Do? The Three Forms?

```jsx
// Form 1: No dependency array — runs after EVERY render
useEffect(() => {
  document.title = `Count: ${count}`;
}); // ← No []

// Form 2: Empty dependency array — runs ONCE after mount
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe(); // Cleanup on unmount
}, []); // ← []

// Form 3: Dependency array — runs when deps change
useEffect(() => {
  fetchUser(userId);
}, [userId]); // ← [userId] — runs when userId changes

// The cleanup function:
useEffect(() => {
  const timer = setInterval(() => console.log('tick'), 1000);
  
  return () => {
    clearInterval(timer); // Called before next effect OR on unmount
  };
}, []);
```

**Memory Leak Prevention with useEffect:**
```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    let isCancelled = false;  // Flag to prevent state update after unmount
    
    fetchUser(userId).then(data => {
      if (!isCancelled) {     // Only update if still mounted
        setUser(data);
      }
    });
    
    return () => {
      isCancelled = true;     // Mark as cancelled when component unmounts
    };
  }, [userId]);
  
  return user ? <div>{user.name}</div> : <Spinner />;
}
```

---

## IRQ3. useRef vs useState — When to Use Which?

| Aspect         | useState                          | useRef                            |
|----------------|-----------------------------------|-----------------------------------|
| Causes re-render | ✅ Yes, on change               | ❌ No, never                      |
| Value persists | ✅ Yes, across renders             | ✅ Yes, across renders             |
| Readable in JSX | ✅ Yes                            | Need `.current`                   |
| Use for        | UI data that affects rendering    | DOM refs, timers, previous values |

```jsx
function Stopwatch() {
  const [time, setTime] = useState(0);     // Causes re-render ← we WANT this
  const timerRef = useRef(null);           // Does NOT cause re-render ← we want this for the timer ID
  const countRef = useRef(0);             // Does NOT cause re-render
  
  const start = () => {
    timerRef.current = setInterval(() => {
      countRef.current += 1;
      setTime(countRef.current); // Only setTime triggers re-render
    }, 1000);
  };
  
  const stop = () => clearInterval(timerRef.current);
  
  return (
    <div>
      <p>Time: {time}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// useRef for previous value
function usePrevious(value) {
  const ref = useRef();
  useEffect(() => {
    ref.current = value; // Set after render
  });
  return ref.current; // Returns PREVIOUS value
}
```

---

## IRQ4. useMemo vs useCallback

```jsx
// useMemo — memoize a COMPUTED VALUE
const sortedList = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]); // Only re-compute when 'items' changes

// useCallback — memoize a FUNCTION REFERENCE
const handleSubmit = useCallback((data) => {
  onSubmit({ ...data, userId: user.id });
}, [user.id, onSubmit]); // Only new reference when deps change

// Why does it matter?
// If handleSubmit is a prop to a React.memo child:
// Without useCallback → new function reference every render → child re-renders
// With useCallback → same reference → React.memo prevents child re-render

function SearchBox({ onSearch }) {
  // ...
}
const MemoizedSearchBox = React.memo(SearchBox);

function Parent() {
  // ❌ New function reference every render → MemoizedSearchBox always re-renders
  const handleSearch = (query) => search(query);
  
  // ✅ Stable reference → MemoizedSearchBox skips re-render when Parent re-renders
  const handleSearch = useCallback((query) => search(query), []);
  
  return <MemoizedSearchBox onSearch={handleSearch} />;
}
```

**When NOT to memoize:**
- Don't memoize cheap computations (creates overhead for no benefit)
- Don't memoize if the component is cheap to render anyway
- Memoize only when you have a measured performance problem

---

## IRQ5. How Does React.memo Work?

```jsx
// React.memo — wrap component to skip re-render if props haven't changed
const UserCard = React.memo(function UserCard({ user, onEdit }) {
  console.log('UserCard rendered');
  return (
    <div>
      <p>{user.name}</p>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
});

// React.memo uses Object.is() for comparison (shallow)
// Objects/arrays: {} !== {} even if contents are same
// Functions: () => {} !== () => {} (new reference each render)

// When React.memo doesn't help:
function Parent() {
  const user = { name: 'Alice' }; // New object reference every render!
  const handleEdit = (id) => {};  // New function reference every render!
  
  return <UserCard user={user} onEdit={handleEdit} />; // Always re-renders!
}

// Fix:
function Parent() {
  const [userData, setUserData] = useState({ name: 'Alice' }); // Stable reference
  const handleEdit = useCallback((id) => {/* ... */}, []);      // Stable reference
  
  return <UserCard user={userData} onEdit={handleEdit} />;      // Skips re-render!
}
```

---

## IRQ6. What is Context API?

```jsx
// 1. Create context
const ThemeContext = React.createContext('light'); // default value

// 2. Provide context value
function App() {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Toolbar />
    </ThemeContext.Provider>
  );
}

// 3. Consume context (any depth in tree)
function Button() {
  const { theme, setTheme } = useContext(ThemeContext);
  
  return (
    <button
      onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}
      className={`btn btn--${theme}`}
    >
      Toggle
    </button>
  );
}

// IMPORTANT: When does Context re-render consumers?
// ALL consumers re-render when the Provider's VALUE changes (by Object.is)
// To prevent unnecessary re-renders, memoize the context value:
const value = useMemo(() => ({ theme, setTheme }), [theme]);
return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
```

---

## IRQ7. useReducer — When to Use Instead of useState?

**Use useReducer when:**
- State logic is complex (multiple sub-values)
- Next state depends on the previous state in complex ways
- Multiple pieces of state are related and change together
- You want to extract state logic for testing

```jsx
// Initial state
const initialState = {
  items: [],
  isLoading: false,
  error: null,
  searchQuery: '',
};

// Reducer — pure function
function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      const existingItem = state.items.find(i => i.id === action.payload.id);
      if (existingItem) {
        return {
          ...state,
          items: state.items.map(i =>
            i.id === action.payload.id
              ? { ...i, quantity: i.quantity + 1 }
              : i
          ),
        };
      }
      return { ...state, items: [...state.items, { ...action.payload, quantity: 1 }] };
    
    case 'REMOVE_ITEM':
      return { ...state, items: state.items.filter(i => i.id !== action.payload) };
    
    case 'CLEAR_CART':
      return { ...state, items: [] };
    
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    
    default:
      return state;
  }
}

// Component
function Cart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  
  return (
    <div>
      {state.items.map(item => (
        <CartItem
          key={item.id}
          item={item}
          onRemove={() => dispatch({ type: 'REMOVE_ITEM', payload: item.id })}
        />
      ))}
      <button onClick={() => dispatch({ type: 'CLEAR_CART' })}>Clear</button>
    </div>
  );
}
```

---

## IRQ8. Implement useLocalStorage Custom Hook

```jsx
function useLocalStorage(key, initialValue) {
  // Initialize from localStorage or use initialValue
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });
  
  // Wrapper around setState that also saves to localStorage
  const setValue = useCallback((value) => {
    try {
      // Allow value to be a function (same API as useState)
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);
  
  // Remove from localStorage
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.warn(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);
  
  // Sync across tabs
  useEffect(() => {
    const handleStorageChange = (event) => {
      if (event.key === key && event.newValue !== null) {
        setStoredValue(JSON.parse(event.newValue));
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);
  
  return [storedValue, setValue, removeValue];
}

// Usage:
function App() {
  const [theme, setTheme, removeTheme] = useLocalStorage('theme', 'light');
  
  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  );
}
```

---

## IRQ9. Custom Hook: useFetch

```jsx
function useFetch(url, options = {}) {
  const [state, setState] = useState({
    data: null,
    isLoading: true,
    error: null,
  });
  
  const abortControllerRef = useRef(null);
  
  useEffect(() => {
    if (!url) {
      setState({ data: null, isLoading: false, error: null });
      return;
    }
    
    // Cancel previous request
    abortControllerRef.current?.abort();
    abortControllerRef.current = new AbortController();
    
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    fetch(url, {
      ...options,
      signal: abortControllerRef.current.signal,
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => setState({ data, isLoading: false, error: null }))
      .catch(error => {
        if (error.name === 'AbortError') return; // Request was cancelled
        setState({ data: null, isLoading: false, error });
      });
    
    return () => abortControllerRef.current?.abort();
  }, [url]);
  
  return state;
}

// Usage:
function UserProfile({ userId }) {
  const { data: user, isLoading, error } = useFetch(`/api/users/${userId}`);
  
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage message={error.message} />;
  return <UserCard user={user} />;
}
```

---

## IRQ10. Custom Hook: useDebounce

```jsx
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(timeout);
  }, [value, delay]);
  
  return debouncedValue;
}

// Usage:
function SearchBox() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  
  // Only fires when user stops typing for 300ms
  useEffect(() => {
    if (debouncedQuery) {
      search(debouncedQuery);
    }
  }, [debouncedQuery]);
  
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

---

## IRQ11-30. Additional Intermediate Topics (Key Answers)

**IRQ11: What is useImperativeHandle?**
```jsx
// Customize what value is exposed via ref to parent
const FancyInput = forwardRef(function FancyInput(props, ref) {
  const inputRef = useRef(null);
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; },
    // Don't expose the raw DOM node — expose controlled API
  }));
  
  return <input ref={inputRef} {...props} />;
});
```

**IRQ12: What is the difference between useEffect and useLayoutEffect?**
```
useEffect      → runs AFTER browser paints (non-blocking, async)
useLayoutEffect → runs BEFORE browser paints (synchronous, like componentDidMount)

Use useLayoutEffect when:
- Reading DOM layout (getBoundingClientRect)
- Preventing flash of unstyled content
- Updating DOM before user sees it (tooltip positioning)
```

**IRQ13: What is React.lazy and Suspense?**
```jsx
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <LazyComponent />
    </Suspense>
  );
}
```

**IRQ14: What is forwardRef?**
```jsx
// Allows parent to get ref to a child's DOM element
const Input = React.forwardRef(function Input({ label, ...props }, ref) {
  return (
    <label>
      {label}
      <input ref={ref} {...props} />
    </label>
  );
});

// Parent:
const inputRef = useRef(null);
<Input ref={inputRef} label="Name" />
inputRef.current.focus(); // Works!
```

**IRQ15: What is key prop's role in resetting state?**
```jsx
// Changing key forces a component to COMPLETELY remount (reset state)
function App() {
  const [userId, setUserId] = useState(1);
  
  return (
    <UserProfile
      key={userId}     // When userId changes, UserProfile fully remounts
      userId={userId}  // Old state is gone, new fresh instance
    />
  );
}
```

---

# Advanced React Questions

---

## ARQ1. React Fiber Architecture

**What:** React Fiber is the complete rewrite of React's core algorithm (released in React 16). It enables **incremental rendering** — breaking rendering work into chunks and spreading it over multiple frames.

```
React 15 (Stack Reconciler):
  Once started rendering → cannot stop → browser frames are blocked
  User: "Why is my app janky?"

React 16+ (Fiber Reconciler):
  Rendering work = units of "fiber" nodes
  Can pause, resume, abort work between frames
  High-priority updates (user input) can interrupt low-priority work
  
  Fiber Work Loop:
  ┌─────────────────────────────────────────────────────┐
  │  1. beginWork(fiber) — work on this fiber           │
  │  2. completeWork(fiber) — finish fiber              │
  │  3. commitWork(fiber) — commit to real DOM          │
  │                                                     │
  │  Between steps 1 and 2: can be interrupted!        │
  │  Step 3 (commit): CANNOT be interrupted            │
  └─────────────────────────────────────────────────────┘
```

**Two phases:**
1. **Render phase** (interruptible): Build fiber tree, determine what changed
2. **Commit phase** (synchronous, uninterruptible): Apply changes to DOM

---

## ARQ2. How Does React's Reconciliation/Diffing Work?

React uses a heuristic O(n) algorithm based on two assumptions:

**Assumption 1: Elements of different types produce different trees**
```jsx
// Type changes → React destroys old tree, creates new tree
// Old: <div><Counter /></div>
// New: <span><Counter /></span>
// → Counter is DESTROYED and re-created (state lost!)
```

**Assumption 2: Keys tell React which items are stable**
```jsx
// Without keys → React re-renders all items on any change
// With stable keys → React can identify moved/removed items
```

**Diffing rules:**
```
1. Different element type → destroy + create new (state lost)
2. Same element type + same position → update (state preserved)
3. Keys → stable identity regardless of position
4. Children are diffed linearly (O(n))
```

---

## ARQ3. What is Concurrent Mode?

**What:** A new rendering mode (React 18) that allows React to prepare multiple versions of the UI simultaneously, interrupting and resuming work.

```jsx
// Enable Concurrent Mode (React 18+)
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

// New concurrent features:
// 1. useTransition — mark updates as non-urgent
const [isPending, startTransition] = useTransition();

function handleSearch(query) {
  // Urgent: show user what they typed immediately
  setSearchQuery(query);
  
  // Non-urgent: search results can be deferred
  startTransition(() => {
    setSearchResults(filterResults(query)); // Can be interrupted
  });
}

// 2. useDeferredValue — defer updating a value
const deferredQuery = useDeferredValue(searchQuery); // Stale while updating

// 3. Suspense for data (experimental)
// Component "suspends" while data is loading
```

---

## ARQ4. React 18's Automatic Batching

**What:** In React 18, ALL state updates are automatically batched — even in setTimeout, promises, and native event handlers.

```jsx
// Before React 18:
setTimeout(() => {
  setCount(c => c + 1);  // Re-render 1
  setFlag(f => !f);       // Re-render 2
  // 2 renders! No batching outside React events
}, 1000);

// React 18 (with createRoot):
setTimeout(() => {
  setCount(c => c + 1);  // Batched
  setFlag(f => !f);       // Batched
  // Only 1 render! Automatic batching everywhere
}, 1000);

// Opt-out of batching when needed:
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1);  // Forces immediate re-render
});
setFlag(f => !f);         // Another re-render
```

---

## ARQ5. How Does React Internally Store Hook State?

**The Fiber Node:**
Each React component has a corresponding Fiber node that stores:
- `memoizedState`: Linked list of hook states

```
Fiber Node for MyComponent:
  memoizedState → [Hook1] → [Hook2] → [Hook3] → null

Hook1 (useState): { memoizedState: 0, queue: [...], next: Hook2 }
Hook2 (useEffect): { create: fn, deps: [], next: Hook3 }
Hook3 (useRef): { memoizedState: { current: null }, next: null }

This is why:
❌ RULE: Hooks must be called in the SAME ORDER every render
   React identifies hooks by their position in the linked list
   If you conditionally call a hook → list order changes → wrong state!
```

---

## ARQ6. What is Streaming SSR?

**What:** Instead of waiting for the entire page to render on the server before sending HTML, React 18 can stream HTML in chunks as components are ready.

```
Traditional SSR:
  Server renders EVERYTHING → sends 1 big HTML → browser parses → hydrate
  User waits for slowest component before seeing anything!

Streaming SSR:
  Server sends shell HTML immediately → browser shows something!
  Server keeps streaming as Suspense boundaries resolve
  Browser progressively displays content
  
  Example:
  <Suspense fallback={<Shell />}>
    <FastComponent />      ← Streamed first
    <Suspense fallback={<ProductSkeleton />}>
      <SlowProductList />  ← Streamed when ready
    </Suspense>
  </Suspense>
```

---

## ARQ7. Server Components vs Client Components

```
Server Components (React Server Components / RSC):
  ✅ Run ONLY on server — never sent to client
  ✅ Can access database, filesystem directly
  ✅ Zero bundle impact (code stays on server)
  ✅ Can pass serializable data to Client Components
  ❌ Cannot use useState, useEffect, event handlers
  ❌ Cannot be interactive

Client Components ('use client'):
  ✅ Interactive (state, effects, events)
  ✅ Access browser APIs
  ❌ Sent to client (increases bundle)
  ❌ Cannot be async components

// RSC (in Next.js App Router):
// app/products/page.jsx
async function ProductsPage() {          // Server Component (default)
  const products = await db.query('SELECT * FROM products'); // Direct DB access!
  
  return (
    <main>
      <ProductGrid products={products} /> {/* Server Component */}
      <SearchBox />                       {/* Must be Client Component */}
    </main>
  );
}

// components/SearchBox.jsx
'use client'; // Mark as Client Component

function SearchBox() {
  const [query, setQuery] = useState(''); // useState works here
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

---

## ARQ8. What is React's Tearing Problem?

**What:** In concurrent mode, React can interrupt rendering. If external state (outside React) changes during interruption, different parts of the UI might show different "snapshots" of the state — a "tear."

```
Example (without useSyncExternalStore):
  Frame 1: Header reads store → value = 'dark'
  Interrupt! External store updates to 'light'
  Frame 2: Footer reads store → value = 'light'
  Result: Header shows 'dark', Footer shows 'light' — inconsistent!

Solution: useSyncExternalStore (React 18)
  Forces synchronous rendering to prevent tearing

// Correct way to subscribe to external stores in React 18:
function useExternalStore(store) {
  return useSyncExternalStore(
    store.subscribe,          // Subscribe function
    store.getSnapshot,        // Get current value (client)
    store.getServerSnapshot,  // Get current value (server)
  );
}
```

---

# React Machine Coding Questions

---

## RMC1. Search with Debouncing and API Integration

```jsx
import { useState, useEffect, useCallback } from 'react';

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
}

function SearchWithDebounce() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const debouncedQuery = useDebounce(query, 400);
  
  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setResults([]);
      return;
    }
    
    const controller = new AbortController();
    
    setIsLoading(true);
    setError(null);
    
    fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`, {
      signal: controller.signal,
    })
      .then(res => {
        if (!res.ok) throw new Error('Search failed');
        return res.json();
      })
      .then(data => {
        setResults(data.results);
        setIsLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError(err.message);
          setIsLoading(false);
        }
      });
    
    return () => controller.abort();
  }, [debouncedQuery]);
  
  return (
    <div className="search">
      <input
        type="search"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search..."
        aria-label="Search"
      />
      
      {isLoading && <div className="search__loading">Searching...</div>}
      {error && <div className="search__error">{error}</div>}
      
      {results.length > 0 && (
        <ul className="search__results" role="listbox">
          {results.map(result => (
            <li key={result.id} role="option">
              <a href={result.url}>{result.title}</a>
              <span>{result.description}</span>
            </li>
          ))}
        </ul>
      )}
      
      {!isLoading && debouncedQuery && results.length === 0 && (
        <p className="search__empty">No results for "{debouncedQuery}"</p>
      )}
    </div>
  );
}

export default SearchWithDebounce;
```

---

## RMC2. Accordion Component

```jsx
import { useState } from 'react';

function AccordionItem({ title, children, isOpen, onToggle }) {
  return (
    <div className="accordion-item">
      <button
        className="accordion-item__trigger"
        aria-expanded={isOpen}
        onClick={onToggle}
      >
        <span>{title}</span>
        <span
          className="accordion-item__icon"
          style={{ transform: isOpen ? 'rotate(180deg)' : 'none' }}
        >
          ▼
        </span>
      </button>
      
      <div
        className="accordion-item__content"
        hidden={!isOpen}
        aria-hidden={!isOpen}
      >
        <div className="accordion-item__body">{children}</div>
      </div>
    </div>
  );
}

// Controlled Accordion (allows multiple open)
function Accordion({ items, allowMultiple = false }) {
  const [openItems, setOpenItems] = useState(new Set());
  
  const toggleItem = (id) => {
    setOpenItems(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        if (!allowMultiple) next.clear(); // Close others if not allowing multiple
        next.add(id);
      }
      return next;
    });
  };
  
  return (
    <div className="accordion" role="list">
      {items.map(item => (
        <AccordionItem
          key={item.id}
          title={item.title}
          isOpen={openItems.has(item.id)}
          onToggle={() => toggleItem(item.id)}
        >
          {item.content}
        </AccordionItem>
      ))}
    </div>
  );
}

export default Accordion;
```

---

## RMC3. Modal with Portal

```jsx
import { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';

function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  const modalRef = useRef(null);
  const previousFocusRef = useRef(null);
  
  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement;
      modalRef.current?.focus();
      document.body.style.overflow = 'hidden'; // Prevent background scroll
    } else {
      document.body.style.overflow = '';
      previousFocusRef.current?.focus(); // Restore focus on close
    }
    
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);
  
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);
  
  if (!isOpen) return null;
  
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={(e) => {
      if (e.target === e.currentTarget) onClose(); // Close on overlay click
    }}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        className={`modal modal--${size}`}
      >
        <div className="modal__header">
          <h2 id="modal-title" className="modal__title">{title}</h2>
          <button
            className="modal__close"
            onClick={onClose}
            aria-label="Close modal"
          >
            ✕
          </button>
        </div>
        
        <div className="modal__body">
          {children}
        </div>
      </div>
    </div>,
    document.getElementById('modal-root') // Portal target
  );
}

// Usage:
function App() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Modal</button>
      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Confirm Action"
      >
        <p>Are you sure you want to continue?</p>
        <button onClick={() => setIsOpen(false)}>Cancel</button>
        <button onClick={handleConfirm}>Confirm</button>
      </Modal>
    </>
  );
}
```

---

## RMC4. Pagination Component

```jsx
function usePagination({ totalItems, itemsPerPage, currentPage }) {
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  
  // Generate page numbers with ellipsis
  const pages = useMemo(() => {
    const delta = 2; // Pages around current page to show
    const range = [];
    
    for (
      let i = Math.max(2, currentPage - delta);
      i <= Math.min(totalPages - 1, currentPage + delta);
      i++
    ) {
      range.push(i);
    }
    
    if (currentPage - delta > 2) range.unshift('...');
    if (currentPage + delta < totalPages - 1) range.push('...');
    
    return [1, ...range, totalPages];
  }, [currentPage, totalPages]);
  
  return { totalPages, pages };
}

function Pagination({ currentPage, totalItems, itemsPerPage, onPageChange }) {
  const { totalPages, pages } = usePagination({ totalItems, itemsPerPage, currentPage });
  
  if (totalPages <= 1) return null;
  
  return (
    <nav aria-label="Pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
      >
        ← Prev
      </button>
      
      {pages.map((page, index) =>
        page === '...' ? (
          <span key={`ellipsis-${index}`} className="pagination__ellipsis">...</span>
        ) : (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={page === currentPage ? 'active' : ''}
            aria-current={page === currentPage ? 'page' : undefined}
          >
            {page}
          </button>
        )
      )}
      
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
      >
        Next →
      </button>
    </nav>
  );
}
```

---

## RMC5. Star Rating Component

```jsx
import { useState } from 'react';

function StarRating({ value = 0, onChange, max = 5, readOnly = false }) {
  const [hovered, setHovered] = useState(0);
  
  const displayValue = readOnly ? value : (hovered || value);
  
  return (
    <div
      className="star-rating"
      role={readOnly ? 'img' : 'radiogroup'}
      aria-label={`Rating: ${value} out of ${max}`}
    >
      {Array.from({ length: max }, (_, i) => {
        const starValue = i + 1;
        const isFilled = starValue <= displayValue;
        
        if (readOnly) {
          return (
            <span
              key={starValue}
              className={`star ${isFilled ? 'star--filled' : 'star--empty'}`}
            >
              ★
            </span>
          );
        }
        
        return (
          <button
            key={starValue}
            type="button"
            role="radio"
            aria-checked={value === starValue}
            aria-label={`${starValue} star${starValue > 1 ? 's' : ''}`}
            className={`star ${isFilled ? 'star--filled' : 'star--empty'}`}
            onClick={() => onChange?.(starValue)}
            onMouseEnter={() => setHovered(starValue)}
            onMouseLeave={() => setHovered(0)}
          >
            ★
          </button>
        );
      })}
      
      {!readOnly && value > 0 && (
        <button
          className="star-rating__clear"
          onClick={() => onChange?.(0)}
          aria-label="Clear rating"
        >
          Clear
        </button>
      )}
    </div>
  );
}

export default StarRating;
```

---

## RMC6. Todo App with Full CRUD

```jsx
import { useState, useCallback } from 'react';

const FILTERS = { ALL: 'all', ACTIVE: 'active', COMPLETED: 'completed' };

function useTodos() {
  const [todos, setTodos] = useState([]);
  
  const addTodo = useCallback((text) => {
    setTodos(prev => [...prev, {
      id: Date.now(),
      text: text.trim(),
      completed: false,
      createdAt: new Date().toISOString(),
    }]);
  }, []);
  
  const toggleTodo = useCallback((id) => {
    setTodos(prev => prev.map(t =>
      t.id === id ? { ...t, completed: !t.completed } : t
    ));
  }, []);
  
  const deleteTodo = useCallback((id) => {
    setTodos(prev => prev.filter(t => t.id !== id));
  }, []);
  
  const editTodo = useCallback((id, newText) => {
    setTodos(prev => prev.map(t =>
      t.id === id ? { ...t, text: newText.trim() } : t
    ));
  }, []);
  
  const clearCompleted = useCallback(() => {
    setTodos(prev => prev.filter(t => !t.completed));
  }, []);
  
  const toggleAll = useCallback(() => {
    const allCompleted = todos.every(t => t.completed);
    setTodos(prev => prev.map(t => ({ ...t, completed: !allCompleted })));
  }, [todos]);
  
  return { todos, addTodo, toggleTodo, deleteTodo, editTodo, clearCompleted, toggleAll };
}

function TodoApp() {
  const { todos, addTodo, toggleTodo, deleteTodo, editTodo, clearCompleted, toggleAll } = useTodos();
  const [filter, setFilter] = useState(FILTERS.ALL);
  const [inputValue, setInputValue] = useState('');
  
  const filteredTodos = todos.filter(todo => {
    if (filter === FILTERS.ACTIVE) return !todo.completed;
    if (filter === FILTERS.COMPLETED) return todo.completed;
    return true;
  });
  
  const activeCount = todos.filter(t => !t.completed).length;
  const completedCount = todos.filter(t => t.completed).length;
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      addTodo(inputValue);
      setInputValue('');
    }
  };
  
  return (
    <div className="todo-app">
      <h1>Todo App</h1>
      
      <form onSubmit={handleSubmit}>
        <input
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder="What needs to be done?"
          aria-label="New todo"
        />
        <button type="submit">Add</button>
      </form>
      
      {todos.length > 0 && (
        <div>
          <button onClick={toggleAll}>
            {todos.every(t => t.completed) ? 'Uncheck All' : 'Check All'}
          </button>
        </div>
      )}
      
      <ul className="todo-list">
        {filteredTodos.map(todo => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={() => toggleTodo(todo.id)}
            onDelete={() => deleteTodo(todo.id)}
            onEdit={(text) => editTodo(todo.id, text)}
          />
        ))}
      </ul>
      
      <div className="todo-footer">
        <span>{activeCount} items left</span>
        
        <div className="filters" role="group" aria-label="Filter todos">
          {Object.values(FILTERS).map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={filter === f ? 'active' : ''}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
        
        {completedCount > 0 && (
          <button onClick={clearCompleted}>Clear completed</button>
        )}
      </div>
    </div>
  );
}

function TodoItem({ todo, onToggle, onDelete, onEdit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  
  const handleEditSubmit = () => {
    if (editText.trim()) {
      onEdit(editText);
      setIsEditing(false);
    }
  };
  
  return (
    <li className={`todo-item ${todo.completed ? 'todo-item--completed' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={onToggle}
        aria-label={`Mark "${todo.text}" as ${todo.completed ? 'incomplete' : 'complete'}`}
      />
      
      {isEditing ? (
        <input
          value={editText}
          onChange={e => setEditText(e.target.value)}
          onBlur={handleEditSubmit}
          onKeyDown={e => {
            if (e.key === 'Enter') handleEditSubmit();
            if (e.key === 'Escape') { setEditText(todo.text); setIsEditing(false); }
          }}
          autoFocus
        />
      ) : (
        <span onDoubleClick={() => setIsEditing(true)}>{todo.text}</span>
      )}
      
      <button onClick={onDelete} aria-label={`Delete "${todo.text}"`}>✕</button>
    </li>
  );
}

export default TodoApp;
```

---

# SECTION 3: Company-Specific Questions

---

## Google/Meta Level Questions

### Technical Internals

**Q: Explain how React's reconciliation algorithm handles list updates.**
- Uses keys to identify elements across renders
- Without keys: linear O(n) comparison (position-based) — inefficient for insertions
- With keys: can match elements by identity — efficient
- Keys must be stable and unique among siblings

**Q: How would you implement a virtualized list from scratch?**
- Calculate which items are visible (scrollTop / itemHeight = startIndex)
- Only render visible items + a small buffer (overscan)
- Position items absolutely using CSS top property
- Set container height to totalItems * itemHeight (creates scrollbar)
- Listen to scroll events to update visible range

**Q: How does React handle batching in different scenarios (React 17 vs 18)?**
- React 17: Batched in React event handlers only
- React 18: Batched everywhere (setTimeout, Promises, native events)
- Opt-out: `flushSync()` for immediate DOM updates

---

## Microsoft/Amazon Questions

**STAR Method Behavioral:**
"Tell me about a time you improved performance significantly."

**Framework Answer:**
- **Situation:** Our product listing page had a 6s LCP on mobile
- **Task:** Reduce to under 2.5s (Core Web Vitals threshold)
- **Action:** Profiled with Lighthouse, found 3 root causes: (1) 450KB unoptimized images, (2) 180KB third-party scripts blocking render, (3) no code splitting — entire bundle loaded upfront. Fixed with WebP images + srcset, deferred analytics scripts, route-based code splitting.
- **Result:** LCP dropped from 6s to 1.8s. 22% increase in conversion rate.

---

## Indian Product Companies (Flipkart/Swiggy/Zomato)

**Common focus areas:**
1. Performance on low-end Android devices and 3G networks
2. Optimistic UI for actions like "Add to Cart"
3. Offline support for previously loaded content
4. PWA features (installability, push notifications)

**Q: How would you optimize a product listing page for users on 3G networks?**
- Server-side rendering for initial HTML (no JS needed to show products)
- Skeleton screens (not spinner) — show layout while loading
- Critical CSS inlined in `<head>`
- Images: WebP with AVIF fallback, lazy load, correct dimensions to prevent CLS
- `preconnect` to API domain and image CDN
- Service worker to cache static assets
- Infinite scroll instead of loading all at once
- Abort slow requests after 5s, show error state

---

# SECTION 4: Behavioral Questions

---

## Q: Tell Me About Yourself

**Framework (P.A.S.T):**
```
Present:   Current role and key responsibilities
           "I'm currently a senior frontend engineer at X, where I lead..."

Accomplishment: Most impressive recent achievement
                "Most recently, I reduced our checkout funnel's load time by 40%..."

Skills:    Technologies relevant to THIS role
           "I specialize in React, TypeScript, and performance optimization..."

Transition: Why you want THIS job
            "I'm looking for a role where I can work on..."
```

**Example Answer:**
*"I'm a frontend engineer with 5 years of experience, currently at Flipkart where I work on our search and discovery platform. My biggest recent win was redesigning our search results page to use virtualization and progressive image loading — it improved our LCP from 4.2s to 1.6s, which contributed to a 15% increase in search-to-purchase conversion. My strength is building performant, accessible React applications at scale. I'm looking for a role where I can take on system-level ownership, which is why I'm excited about this staff engineer position."*

---

## Q: The STAR Method

**Structure:**
- **S**ituation: Set the scene (brief, 1-2 sentences)
- **T**ask: What was your specific responsibility?
- **A**ction: What did YOU specifically do? (Most important)
- **R**esult: Quantified outcome + what you learned

**Example: "Describe a conflict with a team member"**

*"Situation: A backend engineer wanted to put all business logic in the API layer, making our frontend a 'dumb display.' I disagreed — I felt the frontend needed more flexibility for UX requirements.*

*Task: I needed to resolve this disagreement without damaging the relationship or slowing development.*

*Action: Instead of arguing my position, I scheduled a meeting and asked him to walk me through his concerns. He worried about business logic duplication across our web and mobile apps. I showed him how we could put truly shared logic in an API schema (with OpenAPI), while keeping UX-specific decisions client-side. We wrote down the principles we agreed on.*

*Result: We reached a documented agreement that both teams followed. The mobile team later thanked us because they could reuse the API schemas while still having flexibility in their UX layer."*

---

## Q: Why React/Frontend?

**Strong answer elements:**
1. Immediate user feedback (you can see your work's impact instantly)
2. Intersection of design and engineering (rare combination)
3. Performance directly affects business metrics you can measure
4. The accessibility challenge — building for everyone
5. Evolving ecosystem keeps it intellectually stimulating

---

# SECTION 5: Interview Cheat Sheets

---

## JavaScript One-Pager Cheat Sheet

```
TYPES:          string, number, boolean, null, undefined, symbol, bigint, object

TYPE COERCION:  + with string → concatenation
                - * / with string → numeric coercion
                == → coercion, === → no coercion

SCOPE CHAIN:    variable lookup: current → parent → ... → global

HOISTING:       var: declared + undefined, let/const: TDZ, function decl: full

CLOSURES:       inner function accesses outer variables after outer returns

THIS:           global → window, method → object, new → instance, arrow → lexical

PROTOTYPE:      obj.__proto__ links to Animal.prototype links to Object.prototype

EVENT LOOP:     sync → microtasks (Promises) → macrotask (setTimeout)

ASYNC:          callback hell → Promises → async/await

ARRAY METHODS:
  map()         transform each item, returns new array
  filter()      subset of items, returns new array
  reduce()      single value from array
  find()        first match
  some()        any match?
  every()       all match?
  flat/flatMap  flatten nested arrays

OBJECT:
  Object.keys()    → ['a', 'b']
  Object.values()  → [1, 2]
  Object.entries() → [['a', 1], ['b', 2]]
  Object.assign()  → shallow merge
  { ...spread }    → shallow clone/merge

DESTRUCTURING:
  const { a, b = 2 } = obj        // with default
  const [first, ...rest] = arr    // rest
  const { a: renamed } = obj      // rename

NULLISH:
  ??    only triggers for null/undefined (not 0, '', false)
  ?.    safe property access, returns undefined instead of error
```

---

## React Hooks Cheat Sheet

```
useState(initialValue)
  → [state, setState]
  → setState(newValue) or setState(fn => newValue)

useEffect(fn, deps)
  → no deps:    run after every render
  → []:         run once after mount
  → [a, b]:     run when a or b changes
  → return fn:  cleanup (called before next effect or unmount)

useContext(Context)
  → reads context value, re-renders when value changes

useRef(initialValue)
  → { current: value }
  → does NOT cause re-render
  → use for: DOM refs, timers, previous values, instance variables

useMemo(fn, deps)
  → memoizes computed VALUE
  → recalculates only when deps change

useCallback(fn, deps)
  → memoizes FUNCTION REFERENCE
  → new reference only when deps change

useReducer(reducer, initialState)
  → [state, dispatch]
  → for complex state logic

useLayoutEffect(fn, deps)
  → like useEffect but synchronous (before paint)
  → use for: reading DOM layout, preventing flicker

useId()
  → generates unique stable ID (for accessibility)

useTransition()
  → [isPending, startTransition]
  → marks updates as non-urgent

useDeferredValue(value)
  → returns deferred copy of value
  → stale while updating (like debounce for rendering)

forwardRef(fn)
  → allow ref to inner DOM element

useImperativeHandle(ref, fn, deps)
  → customize exposed ref API
```

---

## Event Loop Execution Order Cheat Sheet

```
1. ALL synchronous code in call stack
2. ALL microtasks:
   - Promise.then / .catch / .finally
   - queueMicrotask()
   - async function continuations (after await)
   - MutationObserver callbacks
3. Browser renders (if needed)
4. ONE macrotask:
   - setTimeout
   - setInterval
   - setImmediate (Node.js)
   - I/O callbacks
   - UI events (click, keypress)
5. Return to step 2

IMPORTANT:
- Microtasks run BETWEEN every macrotask (and after sync)
- Microtasks can add more microtasks (all run before next macrotask)
- Too many microtasks → starve the event loop

QUICK TEST: What order?
setTimeout(()=> log('A'), 0)
Promise.resolve().then(()=> log('B'))
queueMicrotask(()=> log('C'))
log('D')

Answer: D, B, C, A
(D = sync, B and C = microtasks in order, A = macrotask)
```

---

## State Management Decision Cheat Sheet

```
Is it LOCAL to one component?
  YES → useState / useReducer

Is it SERVER DATA (from API)?
  YES → React Query / SWR / RTK Query

Should it be in the URL (shareable)?
  YES → URL search params (useSearchParams)

Is it shared between DISTANT components?
  YES → Context API (few consumers, simple data)
        OR Zustand (simpler than Redux)
        OR Redux Toolkit (large app, complex state, team familiarity)

Does it need to PERSIST?
  YES → localStorage + sync with state (useLocalStorage hook)
        OR IndexedDB (large amounts of data)
        OR Cookie (with expiry, accessible server-side)

LIBRARY SELECTION:
  Small app:    useState + Context
  Medium app:   Zustand + React Query
  Large app:    Redux Toolkit + RTK Query
  SSR/Next.js:  Jotai / Zustand + Server State (server components)
```

---

## Performance Optimization Cheat Sheet

```
RENDERING:
  ✅ React.memo for expensive components with stable props
  ✅ useMemo for expensive computations
  ✅ useCallback for stable function references
  ✅ useTransition for non-urgent updates
  ❌ Don't memoize everything — only measured bottlenecks

BUNDLE:
  ✅ Code split at routes (React.lazy)
  ✅ Dynamic import for heavy components (charts, editors)
  ✅ Tree shaking (import specific functions, not whole libraries)
  ✅ Bundle analysis (webpack-bundle-analyzer)

IMAGES:
  ✅ WebP/AVIF format
  ✅ Correct dimensions + responsive srcset
  ✅ loading="lazy" for below-fold images
  ✅ Blur placeholder while loading (blurhash)
  ✅ CDN for image serving + resizing

DATA FETCHING:
  ✅ React Query (caching, deduplication, background refetch)
  ✅ Prefetch on hover/route change
  ✅ Optimistic updates for user actions
  ✅ Abort stale requests (AbortController)
  ✅ Pagination/infinite scroll (not "load all")

LISTS:
  ✅ Virtualize lists > 100 items (react-window/react-virtual)
  ✅ Stable keys from data

NETWORK:
  ✅ HTTP/2 for parallel requests
  ✅ CDN for static assets
  ✅ preconnect to critical origins
  ✅ Service worker for offline + cache

METRICS:
  ✅ LCP < 2.5s
  ✅ FID < 100ms
  ✅ CLS < 0.1
  ✅ Bundle initial JS < 200KB
```

---

*End of Part 4 — Complete Interview Preparation Guide*
*Next: Part 5 — Projects Guide*
