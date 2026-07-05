# Chapter 2: Variables, Data Types, Operators & Control Flow

> **"Variables are the nouns of programming — they name the things your code works with. Understanding how JavaScript stores and manages these values is the key to writing bug-free code."**

---

## Table of Contents

1. [Variables: var, let, const](#variables)
2. [Scope](#scope)
3. [Hoisting](#hoisting)
4. [Temporal Dead Zone (TDZ)](#tdz)
5. [Data Types — Primitives](#primitive-types)
6. [Data Types — Non-Primitives](#non-primitive-types)
7. [typeof Operator](#typeof)
8. [Type Conversion & Coercion](#type-conversion)
9. [Truthy and Falsy Values](#truthy-falsy)
10. [Operators](#operators)
11. [Control Flow](#control-flow)
12. [Chapter Summary & Interview Prep](#summary)

---

## 1. Variables: var, let, const {#variables}

### What is a Variable?

**Real-world analogy:** A variable is like a labeled storage box. You give it a name, put something inside it, and later you can open it to get what you stored — or replace the contents.

```
Box labeled "age"     →     let age = 25;
Contents: 25          →     the value

Box labeled "name"    →     const name = "Alice";
Contents: "Alice"     →     cannot replace contents (const)
```

Before ES6 (2015), JavaScript had only `var`. ES6 introduced `let` and `const` to fix serious problems with `var`.

---

### `var` — The Original (and Problematic) Way

```javascript
// SYNTAX:
var variableName = value;

// Examples:
var greeting = "Hello";
var count = 0;
var isLoggedIn = false;
var data;  // Declaration without initialization → undefined
```

**Every keyword explained:**
- `var` — keyword that declares a variable
- `variableName` — identifier (name you choose for the box)
- `=` — assignment operator (put this value in the box)
- `value` — the data to store

**Characteristics of `var`:**

```javascript
// 1. FUNCTION-SCOPED (not block-scoped)
function demo() {
  if (true) {
    var x = 10;  // You'd expect x to only exist inside the if block
  }
  console.log(x);  // 10 — x "leaked" out of the if block!
}

// 2. CAN BE RE-DECLARED (no error)
var name = "Alice";
var name = "Bob";  // No error! Silently overwrites
console.log(name); // "Bob"

// 3. CAN BE RE-ASSIGNED
var count = 0;
count = 5;  // Fine
count = "five";  // Also fine (dynamic typing)

// 4. HOISTED (initialized to undefined)
console.log(value);  // undefined (not an error!)
var value = 42;
console.log(value);  // 42

// 5. ATTACHED TO GLOBAL OBJECT (in global scope)
var globalVar = "I'm global";
console.log(window.globalVar);  // "I'm global" (in browser)
```

**Why `var` is problematic:**

```javascript
// BUG with var in loops:
for (var i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i);  // Expected: 0, 1, 2
  }, 100);           // Actual: 3, 3, 3 !!
}
// WHY: var i is function-scoped (or global), not loop-scoped.
// By the time setTimeout runs, the loop has finished and i === 3.

// BUG with re-declaration:
var user = "Alice";
// ... 200 lines later ...
var user = "Bob";  // No error! You just silently broke your code.
```

---

### `let` — The Block-Scoped Variable (ES6)

```javascript
// SYNTAX:
let variableName = value;

// Examples:
let count = 0;
let message = "Hello";
let items = [];
```

**Characteristics of `let`:**

```javascript
// 1. BLOCK-SCOPED (exists only within its enclosing { })
function demo() {
  if (true) {
    let x = 10;  // x only exists inside this if block
  }
  console.log(x);  // ReferenceError: x is not defined
}

// 2. CANNOT BE RE-DECLARED in same scope
let name = "Alice";
let name = "Bob";  // SyntaxError: Identifier 'name' has already been declared

// 3. CAN BE RE-ASSIGNED
let count = 0;
count = 5;   // Fine
count++;     // Fine
count = "five";  // Fine (dynamic typing still applies)

// 4. HOISTED but NOT INITIALIZED (TDZ — covered next section)
console.log(value);  // ReferenceError: Cannot access 'value' before initialization
let value = 42;

// 5. NOT attached to global object
let globalLet = "not on window";
console.log(window.globalLet);  // undefined

// 6. WORKS CORRECTLY in loops
for (let i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i);  // 0, 1, 2 ✅ — each iteration has its own i
  }, 100);
}
```

**Why the loop fix works with `let`:**
`let` creates a NEW binding for `i` in each iteration. Each setTimeout closure captures its own copy of `i`. This is a key behavior that makes `let` far more predictable than `var`.

---

### `const` — The Immutable Reference (ES6)

```javascript
// SYNTAX:
const CONSTANT_NAME = value;  // Convention: UPPERCASE for true constants
const variableName = value;   // But camelCase is also common

// Examples:
const PI = 3.14159;
const MAX_RETRIES = 3;
const user = { name: "Alice", age: 25 };
const numbers = [1, 2, 3];
```

**Characteristics of `const`:**

```javascript
// 1. BLOCK-SCOPED (same as let)

// 2. CANNOT BE RE-DECLARED

// 3. CANNOT BE RE-ASSIGNED
const PI = 3.14159;
PI = 3.14;  // TypeError: Assignment to constant variable

// 4. BUT OBJECTS AND ARRAYS CAN BE MUTATED!
const user = { name: "Alice" };
user.name = "Bob";    // ✅ FINE — mutating the object
user.age = 25;        // ✅ FINE — adding property
user = { name: "Charlie" };  // ❌ TypeError — reassigning the variable

// WHY? const makes the BINDING (the reference) constant.
// The object itself is on the heap and can change.

const numbers = [1, 2, 3];
numbers.push(4);    // ✅ FINE — mutating the array
numbers[0] = 10;    // ✅ FINE
numbers = [4, 5, 6]; // ❌ TypeError — reassigning the variable

// 5. MUST BE INITIALIZED at declaration
const x;  // SyntaxError: Missing initializer in const declaration
const x = 5;  // ✅

// 6. HOISTED but in TDZ (like let)
```

**Making objects truly immutable:**

```javascript
// const doesn't make the object immutable!
const user = { name: "Alice" };

// To make it truly immutable:
const frozenUser = Object.freeze({ name: "Alice", age: 25 });
frozenUser.name = "Bob";  // Silently fails in strict mode, throws in strict
console.log(frozenUser.name);  // "Alice" — unchanged!

// Note: Object.freeze is SHALLOW — nested objects are still mutable!
const config = Object.freeze({
  server: { port: 3000 }  // This nested object is NOT frozen!
});
config.server.port = 8080;  // Works! (shallow freeze)
```

---

### The Complete Comparison Table

| Feature | `var` | `let` | `const` |
|---------|-------|-------|---------|
| **Scope** | Function/Global | Block | Block |
| **Hoisting** | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| **Re-declaration** | ✅ Allowed | ❌ SyntaxError | ❌ SyntaxError |
| **Re-assignment** | ✅ Allowed | ✅ Allowed | ❌ TypeError |
| **Must initialize** | No | No | Yes |
| **Global object property** | Yes (in global scope) | No | No |
| **Best for** | Legacy code | Mutable values | Constants, objects |
| **TDZ** | No | Yes | Yes |

### When to Use Which

```
Use const BY DEFAULT — for everything
Use let when you KNOW the value will change (loop counter, accumulators)
Avoid var — only in legacy code or very specific edge cases

// Good pattern:
const MAX = 100;           // Never changes
const user = {};           // Object reference doesn't change
let counter = 0;           // Will be incremented
let currentPage = 1;       // Will be updated
```

---

## 2. Scope {#scope}

### What is Scope?

**Real-world analogy:** Scope is like the visibility of a person in a building. People in a private office (inner scope) can see everything in their office AND the hallway (outer scope). But people in the hallway can't see inside the private offices.

Scope determines **where in your code** a variable is accessible.

### Types of Scope

#### Global Scope

Variables declared outside any function or block:

```javascript
// Global scope
const appName = "MyApp";  // Accessible everywhere

function greet() {
  console.log(appName);  // ✅ Can access global variable
}

if (true) {
  console.log(appName);  // ✅ Can access global variable
}
```

#### Function Scope

Variables declared with `var` inside a function:

```javascript
function outer() {
  var functionVar = "I'm function-scoped";
  let functionLet = "I'm also function-scoped";
  
  console.log(functionVar);  // ✅
  console.log(functionLet);  // ✅
}

console.log(functionVar);  // ❌ ReferenceError
console.log(functionLet);  // ❌ ReferenceError
```

#### Block Scope

Variables declared with `let` or `const` inside a block `{ }`:

```javascript
{
  let blockLet = "I'm block-scoped";
  const blockConst = "Me too";
  var blockVar = "I escape blocks!";
}

console.log(blockVar);   // ✅ (var ignores block scope)
console.log(blockLet);   // ❌ ReferenceError
console.log(blockConst); // ❌ ReferenceError
```

### Scope Chain

When JavaScript looks up a variable, it starts in the current scope and travels **outward** through parent scopes until it finds it (or reaches global scope and throws ReferenceError).

```javascript
const global = "global";

function outer() {
  const outerVar = "outer";
  
  function inner() {
    const innerVar = "inner";
    
    // inner can see: innerVar, outerVar, global
    console.log(innerVar);   // ✅ "inner"
    console.log(outerVar);   // ✅ "outer" (found in parent scope)
    console.log(global);     // ✅ "global" (found in grandparent scope)
  }
  
  // outer can see: outerVar, global
  // outer CANNOT see: innerVar
  console.log(outerVar);   // ✅
  console.log(innerVar);   // ❌ ReferenceError
  
  inner();
}

outer();
```

**ASCII Scope Chain Diagram:**

```
┌─────────────────────────────────────────────────────┐
│  GLOBAL SCOPE                                       │
│  global = "global"                                  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  outer() SCOPE                                │  │
│  │  outerVar = "outer"                           │  │
│  │                                               │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │  inner() SCOPE                          │  │  │
│  │  │  innerVar = "inner"                     │  │  │
│  │  │                                         │  │  │
│  │  │  Looking up "global":                   │  │  │
│  │  │  1. Check inner() scope → not found     │  │  │
│  │  │  2. Check outer() scope → not found     │  │  │
│  │  │  3. Check global scope → FOUND! ✅      │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘

Lookup direction: inner → outer → global
```

### Lexical Scope

JavaScript uses **lexical scoping** (also called static scoping). This means the scope of a variable is determined by where it was **written** in the code (at author time), NOT where it's called from (runtime).

```javascript
function createGreeter() {
  const greeting = "Hello";
  
  function greet(name) {
    // "greeting" is accessible because greet was DEFINED inside createGreeter
    // Not because of where greet is CALLED FROM
    console.log(greeting + " " + name);
  }
  
  return greet;
}

const greet = createGreeter();
greet("Alice");  // "Hello Alice" — greeting is accessible!
// Even though greet() is called outside createGreeter,
// it still has access to greeting because that's where it was DEFINED.
```

This is the foundation of **closures** — we'll cover them in Chapter 3.

---

## 3. Hoisting {#hoisting}

### What is Hoisting?

**Real-world analogy:** Before a movie crew starts filming, the director reads the entire script and writes down a list of all the characters needed. On filming day, all actors are "ready" from the start, even though their scenes haven't been filmed yet.

JavaScript's V8 engine does something similar: in the **Memory Creation Phase** (Phase 1 of execution context), it scans the entire scope and prepares space for all variables and functions — BEFORE executing any code (Phase 2).

This behavior is called **hoisting** — it's as if declarations are "hoisted" (lifted) to the top of their scope.

**IMPORTANT:** Only DECLARATIONS are hoisted, not INITIALIZATIONS.

### Hoisting Behavior by Declaration Type

#### `var` Hoisting

```javascript
// What you write:
console.log(name);  // Line 1
var name = "Alice"; // Line 2

// What JavaScript "sees" after hoisting (conceptually):
var name;           // Declaration hoisted to top, initialized to undefined
console.log(name);  // undefined (not an error!)
name = "Alice";     // Initialization stays in place

// OUTPUT: undefined
```

```javascript
// More examples:
function hoistingDemo() {
  console.log(x);  // undefined
  console.log(y);  // undefined  
  
  var x = 10;
  var y = 20;
  
  console.log(x);  // 10
  console.log(y);  // 20
}
```

#### `let` and `const` Hoisting — Temporal Dead Zone

```javascript
// What you write:
console.log(name);  // ReferenceError!
let name = "Alice";

// let IS hoisted (the variable is "known" to exist in memory),
// but it is NOT initialized. Accessing it before the line of declaration
// throws a ReferenceError. This period is called the TDZ.
```

#### Function Declaration Hoisting — Fully Hoisted!

```javascript
// You can call a function BEFORE it's declared:
greet("Alice");  // "Hello, Alice!" — works!

function greet(name) {
  console.log("Hello, " + name + "!");
}

// REASON: Function declarations are FULLY hoisted —
// the entire function body is stored in memory in Phase 1.
```

#### Function Expression Hoisting — NOT Fully Hoisted

```javascript
// Function expression is stored in a var — only var part is hoisted
greet("Alice");  // TypeError: greet is not a function

var greet = function(name) {
  console.log("Hello, " + name + "!");
};

// What hoisting does:
var greet;        // Declaration hoisted, initialized to undefined
greet("Alice");   // TypeError: undefined is not a function!
greet = function(name) { ... };  // Assignment stays
```

#### Arrow Function Hoisting

```javascript
// Arrow functions are NEVER fully hoisted (they're always expressions)
greet("Alice");  // TypeError or ReferenceError depending on declaration
const greet = (name) => `Hello, ${name}!`;
```

### Hoisting Summary Table

| Declaration Type | Hoisted? | Initial Value in Memory | Accessible Before Declaration? |
|-----------------|----------|------------------------|-------------------------------|
| `var` | ✅ Yes | `undefined` | ✅ Yes (but value is `undefined`) |
| `let` | ✅ Yes | Uninitialized (TDZ) | ❌ ReferenceError |
| `const` | ✅ Yes | Uninitialized (TDZ) | ❌ ReferenceError |
| Function declaration | ✅ Yes | Full function object | ✅ Yes (fully accessible) |
| Function expression (var) | ✅ Yes (var part) | `undefined` | ❌ TypeError (not a function) |
| Arrow function (const/let) | ✅ Yes | Uninitialized (TDZ) | ❌ ReferenceError |

### Memory Creation Phase Visualization

```javascript
var a = 5;
let b = 10;
const c = 15;
function foo() { return "hello"; }
var bar = function() { return "bar"; };

// Memory Creation Phase (what's in memory BEFORE any code runs):
// a       → undefined
// b       → <uninitialized> (TDZ)
// c       → <uninitialized> (TDZ)
// foo     → function() { return "hello"; }  (complete function!)
// bar     → undefined

// Code Execution Phase:
// a = 5        → a is now 5
// b = 10       → b exits TDZ, now 10
// c = 15       → c exits TDZ, now 15
// foo = ...    → already in memory, skip
// bar = fn     → bar is now the function
```

---

## 4. Temporal Dead Zone (TDZ) {#tdz}

### What is the TDZ?

The **Temporal Dead Zone** is the period between when a `let` or `const` variable is hoisted (JavaScript knows it exists) and when it is initialized (the line where you assigned it a value is reached).

During the TDZ, accessing the variable throws a `ReferenceError`.

**Real-world analogy:** You've ordered a package online (the variable is "known" to be coming), but it hasn't arrived yet (not initialized). If you try to open a package that isn't there, you get an error. You have to wait until it arrives (the line of code is reached).

```javascript
// The TDZ begins at the START of the block containing the declaration
{
  // TDZ for "x" starts here ↓
  console.log(x);  // ReferenceError: Cannot access 'x' before initialization
  
  let x = 5;  // TDZ ends here, x is initialized to 5
  
  console.log(x);  // 5 ✅
}
```

### Why TDZ Exists

The TDZ was introduced with `let` and `const` intentionally — to **catch bugs**!

With `var`, accessing a variable before its assignment silently returns `undefined`, which can lead to subtle, hard-to-debug bugs. The TDZ makes this an explicit error, helping you catch mistakes immediately.

```javascript
// With var — silent bug:
console.log(name);  // undefined (no error, might go unnoticed)
var name = "Alice";

// With let — explicit error:
console.log(name);  // ReferenceError: Cannot access 'name' before initialization
let name = "Alice";
// The error tells you EXACTLY what's wrong!
```

### TDZ in Different Situations

```javascript
// 1. TDZ in if blocks:
if (true) {
  // TDZ for myVar starts
  console.log(myVar);  // ReferenceError
  let myVar = 10;
  // TDZ ends
}

// 2. TDZ in function parameters (edge case):
function foo(a = b, b) {
  // 'b' is in TDZ when 'a' default is evaluated!
}
foo();  // ReferenceError

// 3. TDZ with classes:
const obj = new MyClass();  // ReferenceError
class MyClass {}  // Classes are also subject to TDZ

// 4. typeof no longer safe with let/const:
typeof undeclaredVar;  // "undefined" (safe, no error)
typeof tdzVar;         // ReferenceError! (if tdzVar is in TDZ)
let tdzVar = 5;
```

---

## 5. Data Types — Primitives {#primitive-types}

### What is a Data Type?

Data types define what **kind** of data a variable holds and what **operations** can be performed on it.

JavaScript has **8 data types** total: **7 primitives** and **1 non-primitive** (Object).

### The 7 Primitive Types

A **primitive** is an immutable, single value stored directly on the stack.

#### 1. `number`

```javascript
// JavaScript has ONLY ONE number type (no int vs float distinction)
let integer = 42;
let float = 3.14;
let negative = -100;
let exponential = 1e6;       // 1,000,000
let hex = 0xFF;              // 255
let octal = 0o17;            // 15
let binary = 0b1010;         // 10

// Special number values:
let notANumber = NaN;        // Result of invalid math
let infinite = Infinity;     // 1/0
let negInfinite = -Infinity; // -1/0

// Number limits:
console.log(Number.MAX_SAFE_INTEGER);  // 9007199254740991 (2^53 - 1)
console.log(Number.MIN_SAFE_INTEGER);  // -9007199254740991
console.log(Number.MAX_VALUE);         // ~1.7976 × 10^308
console.log(Number.EPSILON);           // 2.22e-16 (smallest difference)

// Floating point quirk (IEEE 754):
console.log(0.1 + 0.2);        // 0.30000000000000004 (NOT 0.3!)
console.log(0.1 + 0.2 === 0.3); // false!
// Fix: Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON

// NaN is special:
console.log(NaN === NaN);      // false! (NaN is not equal to itself)
console.log(Number.isNaN(NaN)); // true (correct way to check)
console.log(isNaN("hello"));   // true (coerces first, legacy)
console.log(Number.isNaN("hello")); // false (no coercion, safer)
```

#### 2. `string`

```javascript
// Three ways to create strings:
let single = 'Hello';
let double = "World";
let template = `Hello World`;  // Template literal (ES6)

// Strings are IMMUTABLE — you can't change individual characters
let str = "hello";
str[0] = "H";    // Silently fails in non-strict mode
console.log(str); // Still "hello"

// But you can CREATE new strings:
let newStr = str[0].toUpperCase() + str.slice(1);
console.log(newStr);  // "Hello"

// Template literals:
const name = "Alice";
const age = 25;
const greeting = `Hello, ${name}! You are ${age} years old.`;
// Supports expressions: `${2 + 2}` → "4"
// Supports multiline (without \n)
const multiline = `
  Line 1
  Line 2
  Line 3
`;

// String length:
console.log("hello".length);  // 5 (property, not method)

// String concatenation:
const a = "Hello" + " " + "World";  // "Hello World"
const b = "Number: " + 42;          // "Number: 42" (42 coerced to string)
```

#### 3. `boolean`

```javascript
let isTrue = true;
let isFalse = false;

// Booleans from comparisons:
const isAdult = age >= 18;  // true or false
const isLoggedIn = user !== null;  // true or false

// Boolean() coercion:
Boolean(1);         // true
Boolean(0);         // false
Boolean("");        // false
Boolean("hello");   // true
Boolean(null);      // false
Boolean(undefined); // false
Boolean({});        // true (even empty object!)
Boolean([]);        // true (even empty array!)
```

#### 4. `undefined`

```javascript
// undefined means "no value assigned yet"
let x;
console.log(x);  // undefined

// Automatically assigned when:
let a;                    // Declaration without initialization
function foo() {}
console.log(foo());       // undefined (function with no return)

function greet(name) {
  console.log(name);      // undefined if called as greet()
}

const obj = {};
console.log(obj.missing); // undefined (accessing non-existent property)

// typeof undefined:
console.log(typeof undefined); // "undefined"
console.log(typeof x);         // "undefined"
```

#### 5. `null`

```javascript
// null means "intentionally empty" — you explicitly set this
let user = null;  // No user logged in
let data = null;  // No data fetched yet

// null vs undefined:
// undefined = "I haven't been given a value"
// null = "I was intentionally given NO value"

// The typeof null bug:
console.log(typeof null);     // "object" ← BUG in JavaScript!
// This is a historical bug. null is NOT an object.

// Checking for null:
if (user === null) { /* user is null */ }    // Use strict equality
if (user == null) { /* user is null OR undefined */ }  // Loose equality

// null in arithmetic:
console.log(null + 1);   // 1 (null coerces to 0)
console.log(null + "");  // "null" (coerces to string)
```

#### 6. `symbol` (ES6)

```javascript
// Symbol creates a UNIQUE, immutable value
// Every Symbol() call creates a brand new unique symbol
const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log(sym1 === sym2);  // false! (each Symbol is unique)

// Symbols as unique object keys:
const ID = Symbol("id");
const user = {
  [ID]: 123,     // Symbol as computed property key
  name: "Alice"
};

console.log(user[ID]);     // 123
console.log(user.ID);      // undefined (different!)

// Symbols are not shown in for...in or Object.keys()
for (const key in user) {
  console.log(key);  // Only "name" — Symbol is hidden!
}

// Global symbols (shared across files):
const globalSym = Symbol.for("app.id");
const sameSym = Symbol.for("app.id");
console.log(globalSym === sameSym);  // true (same registry)

// Well-known Symbols (used by JS internally):
Symbol.iterator   // Defines how object is iterable (for...of)
Symbol.toPrimitive  // Custom type coercion
Symbol.hasInstance  // Customizes instanceof behavior
```

#### 7. `bigint` (ES2020)

```javascript
// For integers larger than Number.MAX_SAFE_INTEGER
const big = 9007199254740992n;  // n suffix makes it BigInt
const also = BigInt("9007199254740992");

console.log(9007199254740992 + 1);   // 9007199254740992 (loses precision!)
console.log(9007199254740992n + 1n); // 9007199254740993n (precise!)

// BigInt operations:
const a = 100n;
const b = 30n;
console.log(a + b);   // 130n
console.log(a * b);   // 3000n
console.log(a / b);   // 3n (integer division, truncates)
console.log(a ** 2n); // 10000n

// Cannot mix BigInt and Number:
100n + 100;  // TypeError: Cannot mix BigInt and other types

// Must convert explicitly:
Number(100n) + 100;  // 200
100n + BigInt(100);  // 200n
```

---

## 6. Data Types — Non-Primitives {#non-primitive-types}

There is ONE non-primitive type in JavaScript: **Object**. Arrays, functions, dates, regex — they are ALL objects.

#### Object

```javascript
// Object = collection of key-value pairs
const person = {
  name: "Alice",    // string value
  age: 25,          // number value
  hobbies: ["reading", "coding"],  // array value
  address: {        // nested object
    city: "New York"
  },
  greet: function() {  // method (function value)
    return `Hi, I'm ${this.name}`;
  }
};
```

#### Array (is an Object)

```javascript
const numbers = [1, 2, 3, 4, 5];
console.log(typeof numbers);  // "object" — arrays ARE objects!
console.log(Array.isArray(numbers));  // true (correct way to check)

// Arrays are objects with numeric keys:
// { '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, length: 5 }
```

#### Function (is an Object)

```javascript
function add(a, b) { return a + b; }
console.log(typeof add);  // "function" (special typeof result)
// But functions ARE objects — they can have properties:
add.description = "Adds two numbers";
console.log(add.description);  // "Adds two numbers"

// Functions are "first-class" objects — can be stored in variables,
// passed to functions, returned from functions
```

### Primitive vs Non-Primitive Comparison

| Feature | Primitive | Non-Primitive (Object) |
|---------|-----------|----------------------|
| **Stored as** | Value (on stack) | Reference pointer (stack) + data (heap) |
| **Comparison** | By value | By reference |
| **Mutability** | Immutable | Mutable |
| **Copying** | Value is copied | Reference is copied |
| **typeof** | Returns type name | Returns "object" (or "function") |
| **Examples** | number, string, boolean, null, undefined, symbol, bigint | Object, Array, Function, Date, RegExp, Map, Set |

---

## 7. typeof Operator {#typeof}

### Complete typeof Table

```javascript
typeof undefined       // "undefined"
typeof null            // "object"  ← BUG! null is NOT an object
typeof true            // "boolean"
typeof false           // "boolean"
typeof 42              // "number"
typeof 3.14            // "number"
typeof NaN             // "number"  ← NaN is a number type!
typeof "hello"         // "string"
typeof ''              // "string"
typeof Symbol()        // "symbol"
typeof 42n             // "bigint"
typeof {}              // "object"
typeof []              // "object"  ← arrays are objects
typeof function(){}    // "function"  ← special case!
typeof class{}         // "function"  ← classes are functions
typeof (() => {})      // "function"
typeof undeclaredVar   // "undefined" (no error for undeclared vars!)
```

### Checking Types Correctly

```javascript
// For null — use strict equality:
value === null

// For arrays — use Array.isArray():
Array.isArray([])   // true

// For objects (excluding null and arrays):
value !== null && typeof value === 'object' && !Array.isArray(value)

// Using Object.prototype.toString (most reliable):
Object.prototype.toString.call([])           // "[object Array]"
Object.prototype.toString.call({})           // "[object Object]"
Object.prototype.toString.call(null)         // "[object Null]"
Object.prototype.toString.call(undefined)    // "[object Undefined]"
Object.prototype.toString.call(new Date())   // "[object Date]"
Object.prototype.toString.call(/regex/)      // "[object RegExp]"
```

---

## 8. Type Conversion & Coercion {#type-conversion}

### Explicit Conversion (You Control It)

```javascript
// To Number:
Number("42")       // 42
Number("3.14")     // 3.14
Number("")         // 0
Number("hello")    // NaN
Number(true)       // 1
Number(false)      // 0
Number(null)       // 0
Number(undefined)  // NaN
Number([])         // 0  (surprising!)
Number([1])        // 1  (single element)
Number([1,2])      // NaN (multiple elements)

parseInt("42.9px")  // 42 (parses until non-numeric)
parseFloat("3.14abc")  // 3.14

// Unary + operator (converts to number):
+"42"      // 42
+""        // 0
+true      // 1
+null      // 0
+undefined // NaN

// To String:
String(42)         // "42"
String(null)       // "null"
String(undefined)  // "undefined"
String(true)       // "true"
(42).toString()    // "42"
(42).toString(2)   // "101010" (binary)
(42).toString(16)  // "2a" (hex)

// To Boolean:
Boolean(0)         // false
Boolean("")        // false
Boolean(null)      // false
Boolean(undefined) // false
Boolean(NaN)       // false
Boolean("0")       // true! (non-empty string)
Boolean([])        // true! (array, even empty)
Boolean({})        // true! (object, even empty)

// Double NOT operator !! (shorthand for Boolean()):
!!0       // false
!!""      // false
!!1       // true
!!"hi"    // true
!![]      // true
!!{}      // true
```

### Implicit Coercion (JavaScript Does It Automatically)

```javascript
// String coercion with +:
"5" + 2        // "52" (number 2 coerced to string)
"5" + 2 + 3    // "523" (left-to-right: "5"+2="52", "52"+3="523")
5 + 2 + "3"    // "73" (left-to-right: 5+2=7, 7+"3"="73")

// Numeric coercion with -, *, /, %:
"6" - 2        // 4 (string "6" coerced to number)
"6" * "2"      // 12
"6" / "2"      // 3
"6" - "a"      // NaN

// Boolean coercion in conditions:
if ("") { /* never runs */ }
if ("hello") { /* always runs */ }
if (0) { /* never runs */ }
if ([]) { /* always runs! */ }

// The == (loose equality) coercion rules:
null == undefined   // true (special rule)
null == 0           // false (null only == undefined)
"0" == 0            // true (string coerced to number)
"" == 0             // true
"" == false         // true
[] == 0             // true ([] → "" → 0)
[] == ""            // true ([] → "")
[] == false         // true
[1] == 1            // true
[1,2] == "1,2"      // true (array toString is "1,2")
NaN == NaN          // false (NaN is never equal to anything)
```

### The Abstract Equality Comparison (`==`) Rules

```
When a == b is evaluated:

1. If types are same → use strict equality (===)
2. null == undefined → true
3. null == (anything else) → false  
4. undefined == (anything else) → false
5. If one is number, one is string → convert string to number, compare
6. If one is boolean → convert boolean to number, compare
7. If one is object, one is primitive → convert object to primitive, compare
8. Otherwise → false
```

### Always Use `===` (Strict Equality)

```javascript
// === checks VALUE and TYPE — no coercion
"5" === 5    // false (different types)
null === undefined  // false (different types)
NaN === NaN  // false (NaN is never equal to anything)

// == vs === comparison:
0 == false    // true  (false coerced to 0)
0 === false   // false (different types)

"" == false   // true  (both coerce to 0)
"" === false  // false (different types)

// When == is acceptable:
value == null  // true for both null AND undefined (often useful)
// Equivalent to: value === null || value === undefined
```

---

## 9. Truthy and Falsy Values {#truthy-falsy}

### Falsy Values (ONLY 8 in JavaScript)

```javascript
// Memorize these — they are the ONLY falsy values:
false
0            // zero
-0           // negative zero
0n           // BigInt zero
""           // empty string (single quotes)
''           // empty string (double quotes)
``           // empty template literal
null
undefined
NaN

// Everything else is TRUTHY — including:
"0"          // Non-empty string! "0" is truthy!
"false"      // Non-empty string! "false" is truthy!
[]           // Empty array! Still truthy!
{}           // Empty object! Still truthy!
function(){} // Functions are truthy!
-1           // Any non-zero number is truthy!
Infinity     // Truthy!
```

### Practical Usage

```javascript
// Checking if a value exists:
if (user) {
  // user is not null, undefined, "", 0, or false
  console.log(user.name);
}

// Short-circuit evaluation:
const name = user && user.name;  // Only access user.name if user is truthy
// Better (modern): const name = user?.name;

// Default values with ||:
const displayName = username || "Anonymous";
// If username is empty/null/undefined, use "Anonymous"

// Problem with ||: 0 and "" are falsy!
const count = userCount || 10;  // If userCount is 0, you get 10! Bug!

// Solution — use ?? (nullish coalescing):
const count = userCount ?? 10;  // Only uses 10 if userCount is null/undefined
// 0 ?? 10 → 0 (correct!)
// null ?? 10 → 10 (correct!)
```

### Short-Circuit Evaluation

```javascript
// && (AND): returns first falsy value, or last value if all truthy
false && "anything"    // false (short-circuits at false)
null && "anything"     // null (short-circuits at null)
0 && "anything"        // 0 (short-circuits at 0)
"hello" && "world"     // "world" (all truthy, returns last)
"hello" && 42          // 42

// || (OR): returns first truthy value, or last value if all falsy
false || "default"     // "default" (false is falsy, returns next)
null || undefined      // undefined (both falsy, returns last)
0 || "fallback"        // "fallback"
"hello" || "default"   // "hello" (first truthy)

// ?? (Nullish Coalescing — ES2020):
null ?? "default"       // "default" (null → use default)
undefined ?? "default"  // "default" (undefined → use default)
0 ?? "default"          // 0 (0 is NOT null/undefined → use 0)
"" ?? "default"         // "" (empty string is NOT null/undefined)
false ?? "default"      // false
```

---

## 10. Operators {#operators}

### Arithmetic Operators

```javascript
// Basic:
5 + 3     // 8 (addition)
5 - 3     // 2 (subtraction)
5 * 3     // 15 (multiplication)
5 / 3     // 1.6666... (division, always float)
5 % 3     // 2 (modulo — remainder)
5 ** 3    // 125 (exponentiation — ES7)

// Increment/Decrement:
let x = 5;
x++;     // Post-increment: returns 5, THEN increments to 6
++x;     // Pre-increment: increments first, THEN returns 7
x--;     // Post-decrement: returns 7, THEN decrements to 6
--x;     // Pre-decrement: decrements first, THEN returns 5

// Important distinction:
let a = 5;
let b = a++;  // b = 5, a = 6 (post: assign then increment)
let c = ++a;  // c = 7, a = 7 (pre: increment then assign)
```

### Assignment Operators

```javascript
let x = 10;
x += 5;    // x = x + 5  → 15
x -= 3;    // x = x - 3  → 12
x *= 2;    // x = x * 2  → 24
x /= 4;    // x = x / 4  → 6
x %= 4;    // x = x % 4  → 2
x **= 3;   // x = x ** 3 → 8

// Logical assignment (ES2021):
x &&= 5;   // x = x && 5  (assign 5 only if x is truthy)
x ||= 5;   // x = x || 5  (assign 5 only if x is falsy)
x ??= 5;   // x = x ?? 5  (assign 5 only if x is null/undefined)
```

### Comparison Operators

```javascript
5 == "5"   // true  (loose — coerces types)
5 === "5"  // false (strict — no coercion)
5 != "5"   // false (loose not equal)
5 !== "5"  // true  (strict not equal)
5 > 3      // true
5 < 3      // false
5 >= 5     // true
5 <= 4     // false
```

### Ternary Operator

```javascript
// SYNTAX: condition ? valueIfTrue : valueIfFalse

const age = 20;
const status = age >= 18 ? "adult" : "minor";  // "adult"

// Chaining (but prefer if/else for readability):
const grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";

// Use for simple, clear conditions:
const message = isLoggedIn ? "Welcome back!" : "Please log in";
```

### Logical Operators

```javascript
// AND (&&): true only if BOTH are true
true && true    // true
true && false   // false
false && true   // false

// OR (||): true if AT LEAST ONE is true
true || false   // true
false || false  // false

// NOT (!): flips the boolean
!true   // false
!false  // true
!0      // true
!"hi"   // false

// Double NOT (!!): converts to boolean
!!1      // true
!!""     // false
!![]     // true
!!null   // false
```

### Special Operators

```javascript
// typeof — checks type:
typeof "hello"  // "string"
typeof 42       // "number"

// instanceof — checks prototype chain:
[] instanceof Array   // true
[] instanceof Object  // true (Array is Object)
{} instanceof Object  // true

// in — checks if property exists in object:
"name" in { name: "Alice" }  // true
"age" in { name: "Alice" }   // false
0 in [1, 2, 3]               // true (index 0 exists)

// delete — removes a property:
const obj = { a: 1, b: 2 };
delete obj.a;   // true (success)
console.log(obj);  // { b: 2 }

// void — returns undefined:
void 0        // undefined (common pattern: void(0) to return undefined)
void "hello"  // undefined

// Comma operator — evaluates both, returns last:
let x = (5, 10, 15);  // x = 15
```

### Operator Precedence (High to Low)

```
Priority | Operator
---------|----------------------------------
18       | () grouping
17       | . [] ?.  member access
16       | () function call, new
15       | new (without args)
14       | ++ -- (postfix)
13       | ! ~ + - ++ -- typeof void delete (unary, prefix)
12       | **
11       | * / %
10       | + -
9        | << >> >>>
8        | < > <= >= in instanceof
7        | == != === !==
6        | &
5        | ^
4        | |
3        | &&
2        | || ??
1        | ?: (ternary)
0        | = += -= ...= (assignment)
-1       | , (comma)
```

---

## 11. Control Flow {#control-flow}

### if / else if / else

```javascript
// SYNTAX:
if (condition) {
  // runs if condition is truthy
} else if (anotherCondition) {
  // runs if anotherCondition is truthy
} else {
  // runs if none of the above
}

// Example:
const score = 85;

if (score >= 90) {
  console.log("Grade: A");
} else if (score >= 80) {
  console.log("Grade: B");  // This runs!
} else if (score >= 70) {
  console.log("Grade: C");
} else {
  console.log("Grade: F");
}

// Single-line (no braces — use with caution):
if (isLoggedIn) console.log("Welcome!");  // OK for simple cases
// But ALWAYS use braces to avoid bugs:
// if (condition)
//   statement1;
//   statement2;  ← This ALWAYS runs, regardless of condition!
```

### switch Statement

```javascript
// SYNTAX:
switch (expression) {
  case value1:
    // code
    break;  // REQUIRED to prevent fallthrough!
  case value2:
    // code
    break;
  default:
    // code (optional, runs if no case matches)
}

// Example:
const day = "Monday";

switch (day) {
  case "Monday":
  case "Tuesday":
  case "Wednesday":
  case "Thursday":
  case "Friday":
    console.log("Weekday");  // Intentional fallthrough for grouping
    break;
  case "Saturday":
  case "Sunday":
    console.log("Weekend");
    break;
  default:
    console.log("Invalid day");
}

// IMPORTANT: Without break, code falls through to next case:
switch (1) {
  case 1:
    console.log("One");  // prints
    // No break! Falls through!
  case 2:
    console.log("Two");  // Also prints!
    // No break! Falls through!
  case 3:
    console.log("Three"); // Also prints!
    break;
}
// Output: "One", "Two", "Three"
```

### Loops

#### for loop

```javascript
// SYNTAX:
for (initialization; condition; update) {
  // body
}

// Example:
for (let i = 0; i < 5; i++) {
  console.log(i);  // 0, 1, 2, 3, 4
}

// Reverse loop:
for (let i = 4; i >= 0; i--) {
  console.log(i);  // 4, 3, 2, 1, 0
}

// Loop with array:
const fruits = ["apple", "banana", "cherry"];
for (let i = 0; i < fruits.length; i++) {
  console.log(fruits[i]);
}
```

#### while loop

```javascript
// Runs while condition is true
let count = 0;
while (count < 5) {
  console.log(count);  // 0, 1, 2, 3, 4
  count++;             // Don't forget to update, or infinite loop!
}

// When to use while vs for:
// Use for when you know the number of iterations
// Use while when you don't know how many iterations
let userInput;
while (userInput !== "quit") {
  userInput = prompt("Type 'quit' to exit:");
}
```

#### do-while loop

```javascript
// Executes body AT LEAST ONCE, then checks condition
let i = 0;
do {
  console.log(i);  // Runs at least once even if i is already 5!
  i++;
} while (i < 5);

// Use case: menu systems, input validation
do {
  const response = confirm("Do you want to continue?");
  if (!response) break;
  // ... do work
} while (true);
```

#### for...of (ES6) — Iterates over VALUES

```javascript
// Works with any ITERABLE: arrays, strings, Maps, Sets, generators
const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit);  // "apple", "banana", "cherry"
}

// With index (using entries()):
for (const [index, fruit] of fruits.entries()) {
  console.log(index, fruit);  // 0 "apple", 1 "banana", 2 "cherry"
}

// With string:
for (const char of "hello") {
  console.log(char);  // h, e, l, l, o
}

// With Map:
const map = new Map([["a", 1], ["b", 2]]);
for (const [key, value] of map) {
  console.log(key, value);
}

// With Set:
const set = new Set([1, 2, 3]);
for (const value of set) {
  console.log(value);
}
```

#### for...in — Iterates over KEYS (Object Properties)

```javascript
// Works with objects (and arrays, but NOT recommended for arrays!)
const person = { name: "Alice", age: 25, city: "NYC" };
for (const key in person) {
  console.log(key, person[key]);
  // "name" "Alice"
  // "age" 25
  // "city" "NYC"
}

// WARNING: for...in iterates over INHERITED properties too!
// Always check hasOwnProperty:
for (const key in person) {
  if (Object.hasOwn(person, key)) {  // Modern (ES2022)
    console.log(key, person[key]);
  }
}

// DON'T use for...in with arrays:
const arr = [1, 2, 3];
for (const index in arr) {
  console.log(index);  // "0", "1", "2" (strings, not numbers!)
  // Also iterates over any added properties!
}
// Use for...of instead!
```

### break and continue

```javascript
// break — exits the loop entirely
for (let i = 0; i < 10; i++) {
  if (i === 5) break;  // Stop at 5
  console.log(i);  // 0, 1, 2, 3, 4
}

// continue — skips current iteration, continues to next
for (let i = 0; i < 10; i++) {
  if (i % 2 === 0) continue;  // Skip even numbers
  console.log(i);  // 1, 3, 5, 7, 9
}

// Labeled loops (for nested loops):
outer: for (let i = 0; i < 3; i++) {
  inner: for (let j = 0; j < 3; j++) {
    if (i === 1 && j === 1) break outer;  // Breaks out of OUTER loop
    console.log(i, j);
  }
}
// Outputs: 0,0  0,1  0,2  1,0  (stops when i=1, j=1)
```

### Loop Comparison Table

| Loop | When to Use | Iterates Over |
|------|------------|---------------|
| `for` | Known number of iterations | Index-based |
| `while` | Unknown iterations, check first | Custom logic |
| `do-while` | At least once, then check | Custom logic |
| `for...of` | Arrays, strings, iterables | Values |
| `for...in` | Object properties | Keys (strings) |
| `Array.forEach()` | Array side effects | Values |
| `Array.map()` | Transform array | Values → new array |

---

## 12. Chapter Summary & Interview Prep {#summary}

### Revision Notes

```
VARIABLES:
✅ var: function-scoped, hoisted (undefined), re-declarable, re-assignable
✅ let: block-scoped, hoisted (TDZ), NOT re-declarable, re-assignable
✅ const: block-scoped, hoisted (TDZ), NOT re-declarable, NOT re-assignable
✅ const doesn't make objects immutable — use Object.freeze() for that
✅ Use const by default, let when value must change, avoid var

SCOPE:
✅ Global scope → accessible everywhere
✅ Function scope → accessible within function
✅ Block scope → accessible within { } (let/const only)
✅ Scope chain → looks outward through parent scopes
✅ Lexical scope → determined by where code is WRITTEN, not called

HOISTING:
✅ var → declaration hoisted, initialized to undefined
✅ let/const → declaration hoisted, but in TDZ (ReferenceError if accessed early)
✅ Function declarations → FULLY hoisted (can call before declaration)
✅ Function expressions → only var part hoisted (undefined)

DATA TYPES:
✅ 7 Primitives: number, string, boolean, null, undefined, symbol, bigint
✅ 1 Non-Primitive: Object (includes arrays, functions)
✅ Primitives are immutable, stored by value on stack
✅ Objects are mutable, stored by reference (pointer on stack, data on heap)
✅ typeof null === 'object' is a bug (null is NOT an object)
✅ typeof NaN === 'number' (NaN is a Number type value)
✅ NaN !== NaN (use Number.isNaN() to check)
✅ 0.1 + 0.2 !== 0.3 (floating point precision issue)

TYPE COERCION:
✅ + with string → string concatenation
✅ -, *, / → numeric coercion
✅ == performs type coercion (use === instead!)
✅ Always use === for comparison

FALSY VALUES (exactly 8):
✅ false, 0, -0, 0n, "", '', ``, null, undefined, NaN
✅ Everything else is truthy (including "0", [], {})
```

### Interview Cheat Sheet

```
"var is function-scoped, let/const are block-scoped"
"const prevents reassignment but NOT mutation of objects"
"TDZ: let/const are hoisted but not initialized — ReferenceError if accessed early"
"typeof null === 'object' is a historical bug in JavaScript"
"NaN !== NaN — use Number.isNaN() to check"
"0.1 + 0.2 !== 0.3 due to IEEE 754 floating point"
"8 falsy values: false, 0, -0, 0n, '', null, undefined, NaN"
"[] and {} are truthy — empty doesn't mean falsy for objects"
"== coerces types, === doesn't — always use ==="
"null == undefined is true (loose), null === undefined is false (strict)"
"Primitives pass by value, objects pass by reference"
```

---

## Top 20 Interview Questions — Chapter 2

**Q1. What is the difference between var, let, and const?**

*Answer:* `var` is function-scoped, is hoisted (initialized to `undefined`), can be re-declared and re-assigned, and creates properties on the global object. `let` is block-scoped, is hoisted but remains in the TDZ until the declaration line, cannot be re-declared in the same scope, and can be re-assigned. `const` is like `let` but cannot be re-assigned — however, if it holds an object or array, the contents can be mutated. Always prefer `const`, use `let` when you need to change the value, and avoid `var`.

**Q2. What is the Temporal Dead Zone?**

*Answer:* The TDZ is the period between when a `let` or `const` variable is hoisted (JS knows it exists) and when it's initialized (the line where you assigned it a value). Accessing a variable in its TDZ throws a `ReferenceError: Cannot access 'x' before initialization`. It was introduced to catch bugs — with `var`, accessing before assignment silently returns `undefined`, hiding bugs.

**Q3. What is the output?**
```javascript
console.log(foo);
console.log(bar);
var foo = "hello";
let bar = "world";
```
*Answer:* `undefined` then `ReferenceError`. `foo` is hoisted with `var` → `undefined`. `bar` is in TDZ → `ReferenceError`.

**Q4. What is hoisting?**

*Answer:* Hoisting is JavaScript's behavior of moving declarations to the top of their scope during the Memory Creation Phase. `var` declarations are initialized to `undefined`. `let`/`const` declarations are hoisted but remain in the TDZ. Function declarations are fully hoisted (entire function body available). Function expressions are only hoisted as `var` → `undefined`.

**Q5. Why is typeof null === 'object'?**

*Answer:* It's a bug from the original JavaScript implementation. Values were stored as 32-bit units where the first bits indicated type. The type tag for objects was `000`. `null` was represented as a null pointer (all zeros), so it matched the `000` object type tag. This bug was never fixed for backward compatibility.

**Q6. What are falsy values in JavaScript?**

*Answer:* The 8 falsy values are: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`. Everything else is truthy — including `"0"`, `[]`, `{}`, and functions. This surprises many developers: `if ([]) {}` runs even though the array is empty.

**Q7. What is the difference between == and ===?**

*Answer:* `===` (strict equality) checks both VALUE and TYPE — no type coercion. `==` (loose equality) allows type coercion: `"5" == 5` → `true`, `null == undefined` → `true`, `0 == false` → `true`. Always use `===` in production code. The only exception might be `value == null` (checks both null and undefined).

**Q8. What is the difference between null and undefined?**

*Answer:* `undefined` means a variable was declared but not assigned a value, or a function has no return value, or an object property doesn't exist. `null` is an explicitly assigned value meaning "intentionally empty." `typeof undefined === 'undefined'`, `typeof null === 'object'` (bug). `null == undefined` is `true` (loose), `null === undefined` is `false`.

**Q9. Explain the scope chain.**

*Answer:* When JS looks up a variable, it first checks the current scope. If not found, it moves to the outer scope, then the outer's outer scope, all the way to the global scope. If not found in global scope, it throws a `ReferenceError`. This chain of scopes is the scope chain. JavaScript uses lexical (static) scoping — the scope chain is determined by where code is written, not where it's called from.

**Q10. Predict the output:**
```javascript
let x = 10;
{
  let x = 20;
  console.log(x);
}
console.log(x);
```
*Answer:* `20`, then `10`. Each `let x` creates a separate binding in its block scope. They don't conflict.

**Q11. What is the difference between for...in and for...of?**

*Answer:* `for...in` iterates over **enumerable property KEYS** of an object (including inherited ones). It works with objects. `for...of` iterates over **VALUES** of an **iterable** (arrays, strings, Maps, Sets, generators). You should not use `for...in` with arrays because it iterates over indices as strings and also over any added properties.

**Q12. What happens when you mutate a `const` object?**

*Answer:* It works fine. `const` prevents re-assigning the variable (you can't point it to a new object), but it does NOT prevent mutating the existing object. The `const` binding is immutable, but the object itself (on the heap) is mutable. To prevent mutation, use `Object.freeze()`, though note that `freeze` is shallow — nested objects are still mutable.

**Q13. What is `NaN` and why does `NaN !== NaN`?**

*Answer:* `NaN` stands for "Not a Number." It's the result of invalid numeric operations like `"hello" / 2` or `Math.sqrt(-1)`. It has `typeof NaN === 'number'`. `NaN !== NaN` follows the IEEE 754 floating-point standard, which states that NaN is not equal to anything including itself. To check for NaN, use `Number.isNaN(value)` (not `isNaN()` which coerces first).

**Q14. Why does `0.1 + 0.2 !== 0.3`?**

*Answer:* JavaScript uses IEEE 754 double-precision floating-point. In this system, `0.1` and `0.2` cannot be represented exactly in binary — they have infinite repeating decimal expansions in binary. When you add their approximations, the result is `0.30000000000000004`, not exactly `0.3`. Fix: `Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON`.

**Q15. What is lexical scope?**

*Answer:* Lexical (or static) scope means the scope of a variable is determined by where it's **written in the source code** (the lexical environment at author time), NOT by where the function is called at runtime. This is what enables closures — a function has access to variables from its outer scope based on where it was defined, even when called elsewhere.

---

## 5 Output Prediction Exercises

### Exercise 1
```javascript
function test() {
  console.log(a);  // ?
  console.log(b);  // ?
  var a = 1;
  let b = 2;
}
test();
```
**Answer:** `undefined`, then `ReferenceError`

### Exercise 2
```javascript
var x = 1;
{
  var x = 2;
  console.log(x);  // ?
}
console.log(x);  // ?
```
**Answer:** `2`, `2` — `var` ignores block scope, both refer to the same `x`.

### Exercise 3
```javascript
console.log(typeof undeclaredVariable);  // ?
console.log(typeof null);               // ?
console.log(typeof []);                 // ?
console.log(typeof function(){});       // ?
```
**Answer:** `"undefined"`, `"object"`, `"object"`, `"function"`

### Exercise 4
```javascript
const obj = { a: 1 };
const copy = obj;
copy.a = 99;
console.log(obj.a);  // ?
```
**Answer:** `99` — both `obj` and `copy` point to the same object.

### Exercise 5
```javascript
console.log(1 + "2" + 3);   // ?
console.log(1 + 2 + "3");   // ?
console.log("5" - 3);       // ?
console.log(true + false);  // ?
console.log([] + []);       // ?
console.log({} + []);       // ?
```
**Answer:** `"123"`, `"33"`, `2`, `1`, `""`, `"[object Object]"`

---

## 10 MCQs

**Q1.** Which variable declaration creates a block-scoped variable that cannot be reassigned?
- A) var
- B) let
- C) const
- D) Both B and C

**Answer: C** — `const` is block-scoped AND prevents reassignment. `let` is block-scoped but allows reassignment.

---

**Q2.** What is the output of `console.log([] == false)`?
- A) false
- B) true
- C) TypeError
- D) undefined

**Answer: B** — `[]` → `""` (toString) → `0` (number), `false` → `0`. `0 == 0` → `true`.

---

**Q3.** Which of these is NOT a falsy value?
- A) `""`
- B) `"0"`
- C) `null`
- D) `0`

**Answer: B** — `"0"` is a non-empty string, so it's **truthy**!

---

**Q4.** What does `typeof null` return?
- A) "null"
- B) "undefined"
- C) "object"
- D) null

**Answer: C** — Due to a historical bug in JavaScript.

---

**Q5.** What is the output?
```javascript
let a = 1;
let b = 2;
let c = 3;
c = b;
b = a;
console.log(a, b, c);
```
- A) 1, 2, 3
- B) 1, 1, 2
- C) 2, 1, 2
- D) 1, 2, 2

**Answer: B** — c gets b's value (2), b gets a's value (1). a stays 1. So: 1, 1, 2.

---

**Q6.** What is the TDZ?
- A) A zone where variables have type undefined
- B) A zone where let/const are declared but not initialized, causing ReferenceError
- C) A zone where var declarations are hoisted
- D) A zone where functions cannot be called

**Answer: B**

---

**Q7.** `var` declared in a function is accessible:
- A) Globally
- B) Only within the same block { }
- C) Only within the function
- D) Everywhere in the file

**Answer: C** — var is function-scoped.

---

**Q8.** Which comparison returns `true`?
- A) `null === undefined`
- B) `null == undefined`
- C) `NaN === NaN`
- D) `[] === []`

**Answer: B** — `null == undefined` is a special case in the Abstract Equality Comparison algorithm.

---

**Q9.** What is the output?
```javascript
console.log(0.1 + 0.2 === 0.3);
```
- A) true
- B) false
- C) Error
- D) undefined

**Answer: B** — Due to IEEE 754 floating-point representation issues.

---

**Q10.** Which loop should be used to iterate over object properties?
- A) for...of
- B) for...in
- C) while
- D) do-while

**Answer: B** — `for...in` iterates over enumerable property keys of an object.

---

*End of Chapter 2 — You now have a solid understanding of variables, scope, hoisting, data types, and operators in JavaScript.*
