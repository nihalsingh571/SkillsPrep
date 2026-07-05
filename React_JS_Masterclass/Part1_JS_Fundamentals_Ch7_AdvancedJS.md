# Chapter 7: Advanced JavaScript Concepts

> **"To become a true JavaScript expert, you must look beyond the basics and understand the advanced structures and patterns that power modern architectures."**

---

## Table of Contents

1. [Modules (ES Modules)](#modules)
2. [Map & Set](#map-set)
3. [Iterators & Iterables](#iterators)
4. [Generators (Deep Dive)](#generators)
5. [Symbol](#symbol)
6. [BigInt](#bigint)
7. [Optional Chaining (?.)](#optional-chaining)
8. [Nullish Coalescing (??)](#nullish-coalescing)
9. [Logical Assignment Operators](#logical-assignment)
10. [Functional Programming Concepts](#functional-programming)
11. [Design Patterns in JavaScript](#design-patterns)
12. [ES6 Proxy & Reflect](#proxy-reflect)
13. [SOLID Principles in JavaScript](#solid)
14. [Performance & JavaScript Internals Deep Dive](#internals)
15. [Chapter Summary & Interview Prep](#summary)

---

## 1. Modules (ES Modules) {#modules}

### What are Modules? Why do they exist?
A module is just a JavaScript file. Before modules, JavaScript relied on `<script>` tags, which caused global scope pollution and dependency hell (scripts had to be loaded in the exact right order). 

**ES Modules (ESM)** introduced an official way to share and encapsulate code using `import` and `export`.

### Named Exports vs Default Exports

```javascript
// math.js
export const PI = 3.14159;              // Named export
export function add(a, b) { return a + b; } // Named export

export default function multiply(a, b) { // Default export (only ONE per file)
  return a * b;
}

// app.js
// Importing default (can be named anything) and named exports (must match name)
import multiply, { PI, add } from './math.js';

// Renaming named exports
import { add as sum } from './math.js';

// Importing everything as an object
import * as MathUtils from './math.js';
console.log(MathUtils.PI);
```

### Dynamic Imports
`import()` allows you to load a module asynchronously, returning a Promise. Critical for **Code Splitting** in React!

```javascript
button.addEventListener('click', async () => {
  // Only load heavy.js when the button is clicked!
  const module = await import('./heavy.js');
  module.doHeavyLifting();
});
```

### Module Scope & Tree Shaking
- **Module Scope:** Variables declared in a module are NOT global. They are scoped to the module.
- **Tree Shaking:** Modern bundlers (Webpack, Vite) analyze your `import` statements and remove unused exported code from the final bundle to reduce file size.

---

## 2. Map & Set {#map-set}

### Map
A `Map` is a collection of keyed data items, similar to an `Object`. But the main difference is that `Map` allows keys of ANY type (even objects!).

```javascript
const map = new Map();

// Keys can be anything!
const objKey = { id: 1 };
map.set('name', 'Alice'); // String key
map.set(123, 'Number');   // Number key
map.set(objKey, 'User');  // Object key!

console.log(map.get(objKey)); // 'User'
console.log(map.size);        // 3
console.log(map.has('name')); // true

// Iteration (Maps remember insertion order!)
for (const [key, value] of map) {
  console.log(key, value);
}
```
*Why use Map over Object?* Use Map when keys are unknown until runtime, when keys need to be objects, or when you need guaranteed order and size.

### Set
A `Set` is a collection of values where each value may occur only ONCE.

```javascript
const set = new Set([1, 2, 2, 3, 3, 3]);
console.log(set); // Set(3) { 1, 2, 3 } - Duplicates removed!

set.add(4);
set.delete(1);
console.log(set.has(2)); // true

// Array deduplication trick:
const numbers = [1, 1, 2, 3, 3];
const unique = [...new Set(numbers)]; // [1, 2, 3]
```

### WeakMap & WeakSet
Similar to Map/Set, but keys MUST be objects. If there are no other references to the object key, it is **garbage collected**. Prevents memory leaks! (Commonly used for caching or private data).

---

## 3. Iterators & Iterables {#iterators}

- **Iterable:** An object that implements the `Symbol.iterator` method (Arrays, Strings, Maps, Sets).
- **Iterator:** An object with a `next()` method that returns `{ value: any, done: boolean }`.

```javascript
// How for...of works under the hood:
const arr = ["a", "b"];
const iterator = arr[Symbol.iterator]();

console.log(iterator.next()); // { value: 'a', done: false }
console.log(iterator.next()); // { value: 'b', done: false }
console.log(iterator.next()); // { value: undefined, done: true }

// Making a custom iterable:
const range = {
  from: 1, to: 3,
  [Symbol.iterator]() {
    let current = this.from;
    let last = this.to;
    return {
      next() {
        if (current <= last) return { done: false, value: current++ };
        else return { done: true };
      }
    };
  }
};

for (const num of range) console.log(num); // 1, 2, 3
```

---

## 4. Generators (Deep Dive) {#generators}

Generators are functions that can be paused and resumed using the `yield` keyword. They return a Generator object, which is both an iterator and an iterable.

```javascript
function* idGenerator() {
  let id = 1;
  while (true) { // Infinite sequence!
    yield id++;
  }
}

const gen = idGenerator();
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
```

Generators can also receive data back via `next(value)`:
```javascript
function* chat() {
  const answer = yield "What's your name?";
  yield `Hello, ${answer}!`;
}
const c = chat();
console.log(c.next().value); // "What's your name?"
console.log(c.next("Alice").value); // "Hello, Alice!"
```

---

## 5. Symbol {#symbol}

A `Symbol` is a unique and immutable primitive value. Often used for hidden object properties.

```javascript
const id1 = Symbol("id");
const id2 = Symbol("id");
console.log(id1 === id2); // false! Every symbol is unique.

const user = {
  name: "Alice",
  [id1]: 12345 // Property keyed by a symbol
};

// Symbols are hidden from for...in and Object.keys!
console.log(Object.keys(user)); // ["name"]
```

---

## 6. BigInt {#bigint}

JavaScript Numbers have a limit (`Number.MAX_SAFE_INTEGER`, which is $2^{53} - 1$). `BigInt` solves this.

```javascript
const huge = 9007199254740991n; // Append 'n' to make it a BigInt
const alsoHuge = BigInt("9007199254740991");

console.log(huge + 2n); // 9007199254740993n

// WARNING: You cannot mix BigInt and Number without explicit conversion!
// huge + 1; // TypeError
huge + BigInt(1); // OK
```

---

## 7. Optional Chaining (?.) {#optional-chaining}

Safely access deeply nested properties without throwing a `TypeError` if a reference is null/undefined.

```javascript
const user = { name: "Alice", address: { city: "NYC" } };

// Old way:
const zip = user && user.address && user.address.zipcode;

// Modern way:
const zip2 = user?.address?.zipcode; // returns undefined, no error!

// Works with arrays and functions:
user.hobbies?.[0]; 
user.getAvatar?.(); // only calls if getAvatar exists
```

---

## 8. Nullish Coalescing (??) {#nullish-coalescing}

Provides a default value ONLY if the left side is `null` or `undefined`.
(Unlike `||`, which triggers for *any* falsy value like `0` or `""`).

```javascript
const count = 0;

console.log(count || 10); // 10 (Bug! 0 is falsy)
console.log(count ?? 10); // 0  (Correct! 0 is not null/undefined)
```

---

## 9. Logical Assignment Operators {#logical-assignment}

```javascript
let a = 1;
let b = 0;
let c = null;

a &&= 5; // a = a && 5; (a becomes 5 because it was truthy)
b ||= 5; // b = b || 5; (b becomes 5 because it was falsy)
c ??= 5; // c = c ?? 5; (c becomes 5 because it was null)
```

---

## 10. Functional Programming Concepts {#functional-programming}

- **Pure Functions:** Same input always yields same output. No side effects.
- **Immutability:** Never mutate data; return new copies (e.g., `[...arr, newItem]`).
- **First-Class Functions:** Functions are values (can be passed as args).
- **Higher-Order Functions:** Take functions as args, or return functions (e.g., `map`, `filter`).

```javascript
// Compose: f(g(x)) - executing right to left
const compose = (f, g) => x => f(g(x));

const double = x => x * 2;
const addOne = x => x + 1;

const doubleThenAddOne = compose(addOne, double);
console.log(doubleThenAddOne(5)); // 11
```

---

## 11. Design Patterns in JavaScript {#design-patterns}

- **Singleton:** Ensure a class has only one instance (e.g., a Database connection).
- **Factory:** A function that creates objects (useful instead of classes).
- **Observer (Pub/Sub):** Objects subscribe to events and get notified (e.g., DOM Event Listeners, Redux).
- **Module:** Encapsulating private variables/functions (using closures or ES Modules).

---

## 12. ES6 Proxy & Reflect {#proxy-reflect}

A `Proxy` lets you intercept and redefine fundamental operations for an object (getting, setting, defining properties). (Vue 3 uses this for reactivity).

```javascript
const target = { message: "Hello" };

const handler = {
  get(obj, prop) {
    console.log(`Reading property: ${prop}`);
    return prop in obj ? obj[prop] : "Not Found";
  },
  set(obj, prop, value) {
    console.log(`Setting property: ${prop} to ${value}`);
    obj[prop] = value;
    return true;
  }
};

const proxy = new Proxy(target, handler);
console.log(proxy.message); // Logs: Reading property... -> "Hello"
console.log(proxy.age);     // Logs: Reading property... -> "Not Found"
proxy.age = 25;             // Logs: Setting property...
```

---

## 13. SOLID Principles in JavaScript {#solid}

1. **S**ingle Responsibility: A function/component should do ONE thing.
2. **O**pen/Closed: Open for extension (props, inheritance), closed for modification.
3. **L**iskov Substitution: Subclasses should be replaceable for their base classes.
4. **I**nterface Segregation: Don't force components to depend on props they don't use.
5. **D**ependency Inversion: High-level modules shouldn't depend on low-level modules; both should depend on abstractions (Context API / Dependency Injection).

---

## 14. Performance & JavaScript Internals Deep Dive {#internals}

### V8 Engine (Chrome/Node) Internals
- **Hidden Classes (Shapes):** V8 optimizes object property access by creating hidden classes. If two objects have the same properties added in the *exact same order*, they share a hidden class.
  - *Best Practice:* Initialize all object properties in the constructor. Don't add/delete properties dynamically if performance is critical.
- **Inline Caching:** V8 remembers the hidden class of objects passed to a function. If the same type of object is passed again, it bypasses the property lookup. (Monomorphic is fast, Megamorphic is slow).
- **Deoptimization:** If you pass different types of arguments to a function that V8 previously optimized for Numbers, V8 has to throw away the optimized machine code and fall back to bytecode.

---

## 15. Chapter Summary & Interview Prep {#summary}

### Interview Cheat Sheet
- **ES Modules:** `import`/`export`. `default` (one per file) vs `named` (many). Statically analyzed, enabling tree-shaking.
- **Map vs Object:** Maps allow any key type, maintain order, have `.size`.
- **Set:** Collection of unique values. Great for removing array duplicates `[...new Set(arr)]`.
- **?. and ??:** Optional chaining prevents `TypeError` on null accesses. Nullish coalescing (`??`) checks ONLY for null/undefined, unlike `||`.
- **Proxy:** Intercepts object operations. Used heavily in modern reactive frameworks.

### Top Interview Questions

**Q1. What is the difference between `==` and `===`? (Trick context)**
*Follow up: How does `??` differ from `||`?*
*Answer:* `||` returns the RHS for *any* falsy LHS (`0`, `""`, `false`). `??` returns the RHS *only* if LHS is `null` or `undefined`.

**Q2. How do you remove duplicates from an array?**
*Answer:* `const unique = [...new Set(array)];`

**Q3. What is a WeakMap?**
*Answer:* A Map where keys must be objects. Keys are weakly referenced, meaning if no other reference exists to the object, it gets garbage collected, preventing memory leaks.

**Q4. What is the output of `console.log(1 + 2 + '3')`?**
*Answer:* `'33'`. Left to right: `1 + 2` is `3`, then `3 + '3'` concatenates to `'33'`.

**Q5. Explain the Observer pattern.**
*Answer:* A publisher object maintains a list of subscribers. When a state change occurs, the publisher notifies all subscribers. Examples: `addEventListener`, Redux.

---

## Output Prediction Exercises

**Exercise 1**
```javascript
const map = new Map();
map.set({}, 'a');
map.set({}, 'b');
console.log(map.size);
```
*Answer:* `2`. The two empty objects are different references in memory, so they are treated as two distinct keys.

**Exercise 2**
```javascript
let count = 0;
console.log(count || 10);
console.log(count ?? 10);
```
*Answer:* `10`, `0`.

**Exercise 3**
```javascript
const sym1 = Symbol('a');
const sym2 = Symbol('a');
console.log(sym1 === sym2);
```
*Answer:* `false`. Every Symbol is strictly unique.

**Exercise 4**
```javascript
const user = { name: "Alice" };
const { name: userName = "Bob", age = 25 } = user;
console.log(userName, age);
```
*Answer:* `"Alice"`, `25`. Destructuring with renaming and defaults.

**Exercise 5**
```javascript
console.log(typeof BigInt(1) === typeof 1n);
```
*Answer:* `true`. Both evaluate to `"bigint"`.

---
*End of Chapter 7 — You've conquered advanced JavaScript! Next stop: React.*
