# Chapter 3: Functions — The Complete Deep Dive

> **"Functions are the building blocks of JavaScript. Master functions — closures, higher-order functions, `this`, and all the patterns — and you master JavaScript itself."**

---

## Table of Contents

1. [Why Functions Exist](#why-functions)
2. [Function Declarations](#declarations)
3. [Function Expressions](#expressions)
4. [Arrow Functions](#arrow-functions)
5. [Callbacks & Higher-Order Functions](#hof)
6. [IIFE (Immediately Invoked Function Expressions)](#iife)
7. [Closures — The Deep Dive](#closures)
8. [The `this` Keyword — Complete Guide](#this)
9. [call(), apply(), bind()](#call-apply-bind)
10. [Default Parameters](#default-params)
11. [Rest Parameters & Arguments Object](#rest-params)
12. [Pure Functions & Side Effects](#pure-functions)
13. [Currying & Partial Application](#currying)
14. [Function Composition](#composition)
15. [Memoization](#memoization)
16. [Recursion](#recursion)
17. [Generator Functions](#generators)
18. [Async Functions (Preview)](#async-functions)
19. [Chapter Summary & Interview Prep](#summary)

---

## 1. Why Functions Exist {#why-functions}

### The Problem Functions Solve

Without functions, every piece of logic would need to be written repeatedly:

```javascript
// WITHOUT functions — imagine calculating area 5 times:
const width1 = 5, height1 = 10;
const area1 = width1 * height1;
console.log(area1);

const width2 = 3, height2 = 7;
const area2 = width2 * height2;
console.log(area2);

// ... repeat 3 more times — horrible! Code duplication everywhere!

// WITH functions — write once, use many times:
function calculateArea(width, height) {
  return width * height;
}

console.log(calculateArea(5, 10));  // 50
console.log(calculateArea(3, 7));   // 21
console.log(calculateArea(8, 4));   // 32
```

### Functions Enable:

| Benefit | Explanation |
|---------|-------------|
| **Reusability** | Write once, call many times |
| **Abstraction** | Hide complexity behind a simple name |
| **DRY Principle** | Don't Repeat Yourself |
| **Modularity** | Break complex programs into small pieces |
| **Testability** | Test each function independently |
| **Readability** | `calculateTax(income)` is clearer than the raw formula |

### Functions as First-Class Citizens

In JavaScript, functions are **first-class objects**. This means:

```javascript
// 1. Functions can be stored in variables:
const greet = function(name) { return `Hello, ${name}`; };

// 2. Functions can be stored in arrays:
const operations = [
  function(a, b) { return a + b; },
  function(a, b) { return a - b; }
];

// 3. Functions can be stored in object properties (methods):
const calculator = {
  add: function(a, b) { return a + b; },
  subtract: function(a, b) { return a - b; }
};

// 4. Functions can be passed as arguments to other functions:
setTimeout(function() { console.log("delayed!"); }, 1000);

// 5. Functions can be returned from other functions:
function multiplier(factor) {
  return function(number) {
    return number * factor;
  };
}
const double = multiplier(2);
const triple = multiplier(3);
console.log(double(5));   // 10
console.log(triple(5));   // 15

// 6. Functions have properties (they're objects!):
function greet(name) { return `Hello, ${name}`; }
console.log(greet.name);    // "greet"
console.log(greet.length);  // 1 (number of parameters)
greet.description = "A greeting function";
```

---

## 2. Function Declarations {#declarations}

### Syntax (Every Part Explained)

```javascript
function functionName(param1, param2) {
  // function body
  return value;
}

// Breaking it down:
// function   → keyword that declares a function
// functionName → identifier (name of the function)
// (param1, param2) → parameters: local variable names for inputs
// { } → function body: code that runs when called
// return → exits the function and specifies what value to give back
// value → the return value (optional; undefined if omitted)
```

### Examples

```javascript
// Basic function:
function add(a, b) {
  return a + b;
}
console.log(add(3, 4));  // 7

// Function with no parameters:
function sayHello() {
  console.log("Hello!");
}
sayHello();  // "Hello!"

// Function with no return value (returns undefined):
function logMessage(msg) {
  console.log(msg);
  // No return statement → implicitly returns undefined
}
const result = logMessage("test");  // logs "test"
console.log(result);                // undefined

// Multiple return paths:
function getGrade(score) {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  return "F";  // Default case
}

// Function calling itself (recursion — covered later):
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

### Key Characteristic: Hoisting

```javascript
// Function declarations are FULLY HOISTED
// You can call them BEFORE they're defined!
greet("Alice");  // "Hello, Alice!" — works!

function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

**Why this works:** In the Memory Creation Phase, the entire function body is stored in memory. So by the time `greet("Alice")` executes, the function already exists.

---

## 3. Function Expressions {#expressions}

### What is a Function Expression?

A function expression stores a function in a variable. The function itself has no name (anonymous) or has a name only visible inside itself (named function expression).

```javascript
// Anonymous function expression:
const add = function(a, b) {
  return a + b;
};

// Named function expression (name only visible INSIDE the function):
const factorial = function computeFactorial(n) {
  if (n <= 1) return 1;
  return n * computeFactorial(n - 1);  // Can use computeFactorial here!
};

// computeFactorial(5);  // ReferenceError — not visible outside!
factorial(5);  // 120 ✅
```

### Key Difference: NOT Hoisted

```javascript
// This fails with function expressions:
greet("Alice");  // TypeError: greet is not a function

const greet = function(name) {
  console.log(`Hello, ${name}!`);
};

// What JavaScript sees after hoisting:
// var greet = undefined;  (if var was used)
// const greet = TDZ;      (if const was used)
// greet("Alice");  → TypeError or ReferenceError
```

### Why Use Function Expressions?

```javascript
// 1. Conditional function definition:
let greet;
if (isFormal) {
  greet = function(name) { return `Good day, ${name}.`; };
} else {
  greet = function(name) { return `Hey, ${name}!`; };
}

// 2. As callback arguments:
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(function(n) {
  return n * 2;
});

// 3. As object methods:
const person = {
  name: "Alice",
  greet: function() {
    return `Hi, I'm ${this.name}`;
  }
};
```

### Declaration vs Expression Comparison

| Feature | Function Declaration | Function Expression |
|---------|---------------------|---------------------|
| **Hoisting** | Fully hoisted (can call before) | Not fully hoisted (TDZ or undefined) |
| **Syntax** | `function name() {}` | `const name = function() {}` |
| **Name** | Required | Optional |
| **Use as callback** | Yes (but awkward) | Yes (common pattern) |
| **Conditional definition** | No (hoisted regardless) | Yes |

---

## 4. Arrow Functions {#arrow-functions}

### What Are Arrow Functions?

Introduced in ES6, arrow functions provide a **shorter syntax** for writing function expressions. But more importantly, they have a **different `this` binding** — they don't have their own `this`.

### Syntax Variations (All Forms)

```javascript
// Full syntax:
const add = (a, b) => {
  return a + b;
};

// Implicit return (single expression, no curly braces):
const add = (a, b) => a + b;

// Single parameter (no parentheses needed):
const double = n => n * 2;

// No parameters (parentheses required):
const greet = () => "Hello!";

// Returning an object literal (wrap in parentheses to avoid confusion with block):
const makeUser = (name, age) => ({ name, age });
// Without parens: (name, age) => { name, age } — this is a BLOCK with labels, not object!

// Multi-line body:
const processUser = (user) => {
  const name = user.name.toUpperCase();
  const age = user.age + 1;
  return { name, age };
};
```

### The `this` Difference — The Critical Part

Arrow functions do NOT have their own `this`. They **inherit `this` from their surrounding lexical scope**.

```javascript
// PROBLEM with regular functions in class/object methods:
const timer = {
  seconds: 0,
  start: function() {
    // 'this' here = timer object (correct)
    setInterval(function() {
      // 'this' here = ??? (global/undefined in strict mode!)
      // Regular function's 'this' is determined by HOW it's called
      // setInterval calls the callback as a plain function → global this
      this.seconds++;  // BUG! 'this' is not timer
    }, 1000);
  }
};

// FIX 1: Store reference to 'this'
start: function() {
  const self = this;  // Old way
  setInterval(function() {
    self.seconds++;  // ✅ self is always the timer object
  }, 1000);
}

// FIX 2: Use arrow function (modern way):
start: function() {
  setInterval(() => {
    this.seconds++;  // ✅ Arrow function inherits 'this' from start()
    // 'this' in start() is the timer object, so arrow function's 'this' is too!
  }, 1000);
}
```

### What Arrow Functions DON'T Have

```javascript
// 1. No own 'this' (lexical this from outer scope)
// 2. No 'arguments' object:
const arrowFunc = () => {
  console.log(arguments);  // ReferenceError! No arguments object
};

// Regular function HAS arguments:
function regularFunc() {
  console.log(arguments);  // Arguments { 0: 1, 1: 2, 2: 3 }
}
regularFunc(1, 2, 3);

// 3. Cannot be used as constructors:
const Foo = () => {};
new Foo();  // TypeError: Foo is not a constructor

// 4. No 'prototype' property:
console.log((() => {}).prototype);  // undefined

// 5. Cannot be generator functions:
const gen = *() => {};  // SyntaxError
```

### When to Use vs When NOT to Use Arrow Functions

| Use Arrow Functions | Don't Use Arrow Functions |
|--------------------|--------------------------|
| Callbacks (map, filter, forEach) | Object methods (need `this`) |
| Short utility functions | Constructor functions |
| When you want lexical `this` | Event handlers (if you need `this` = element) |
| Promise chains (.then(() => ...)) | Prototype methods |
| React functional components | Generator functions |

```javascript
// ✅ Great for callbacks:
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);

// ❌ Bad for object methods:
const person = {
  name: "Alice",
  greet: () => {
    // 'this' is NOT person — it's the outer scope (global/window)!
    return `Hi, I'm ${this.name}`;  // this.name is undefined!
  }
};

// ✅ Good for object methods:
const person = {
  name: "Alice",
  greet: function() {
    return `Hi, I'm ${this.name}`;  // this = person ✅
  }
};
```

---

## 5. Callbacks & Higher-Order Functions {#hof}

### What is a Callback?

**Real-world analogy:** You call a restaurant to order pizza. You say "Call me back when it's ready." The restaurant calls you (the "callback") when the pizza is done. You (the function) are passed to the restaurant (another function) to be called later.

A **callback** is a function passed as an argument to another function, to be called at some later point.

```javascript
// Simplest callback:
function doSomething(callback) {
  console.log("Doing something...");
  callback();  // Call the callback function!
}

function done() {
  console.log("I'm the callback — I was called!");
}

doSomething(done);
// Output:
// "Doing something..."
// "I'm the callback — I was called!"
```

### Synchronous Callbacks

```javascript
// Array methods use synchronous callbacks:
const numbers = [1, 2, 3, 4, 5];

// forEach callback — called synchronously for each element:
numbers.forEach(function(num) {
  console.log(num * 2);  // Called right now, in order
});

// map callback:
const doubled = numbers.map(num => num * 2);

// filter callback:
const evens = numbers.filter(num => num % 2 === 0);

// sort callback:
const sorted = numbers.sort((a, b) => a - b);
```

### Asynchronous Callbacks

```javascript
// setTimeout uses async callback:
console.log("Before");

setTimeout(function() {
  console.log("This runs after delay");  // Called later by Web API
}, 1000);

console.log("After");

// Output:
// "Before"
// "After"
// (1 second later)
// "This runs after delay"
```

### Callback Hell (The Problem)

When you nest many async callbacks, code becomes deeply nested and hard to read:

```javascript
// Callback Hell — "Pyramid of Doom":
getUserFromDB(userId, function(user) {
  getUserPosts(user.id, function(posts) {
    getPostComments(posts[0].id, function(comments) {
      getCommentAuthor(comments[0].authorId, function(author) {
        getAuthorProfile(author.id, function(profile) {
          // FINALLY! But this is deeply nested!
          console.log(profile);
          // Error handling at every level is a nightmare!
        }, function(error) {
          handleError(error);
        });
      }, function(error) {
        handleError(error);
      });
    }, function(error) {
      handleError(error);
    });
  }, function(error) {
    handleError(error);
  });
}, function(error) {
  handleError(error);
});
```

**Problems with callback hell:**
1. Hard to read (deep nesting)
2. Hard to maintain
3. Error handling is repetitive
4. Hard to debug
5. Inversion of control (you trust the library to call your callback correctly)

**Solution:** Promises and async/await (covered in Chapter 5).

---

### Higher-Order Functions (HOF)

A **Higher-Order Function** is a function that:
1. Takes one or more functions as arguments, AND/OR
2. Returns a function

```javascript
// HOF that takes a function:
function repeat(n, action) {
  for (let i = 0; i < n; i++) {
    action(i);
  }
}

repeat(3, console.log);  // 0, 1, 2

// HOF that returns a function:
function multiplier(factor) {
  return function(number) {
    return number * factor;
  };
}
const double = multiplier(2);
const triple = multiplier(3);
console.log(double(5));  // 10
console.log(triple(4));  // 12
```

### Built-in HOFs: map, filter, reduce

#### `Array.map()` — Transform Elements

```javascript
// map: creates NEW array by applying function to each element
// Original array is NOT modified
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
// [2, 4, 6, 8, 10]

// More realistic example:
const users = [
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 }
];

const names = users.map(user => user.name);
// ["Alice", "Bob"]

const ageLabels = users.map(user => `${user.name} is ${user.age}`);
// ["Alice is 25", "Bob is 30"]

// Implementing map from scratch:
Array.prototype.myMap = function(callback) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    // callback(currentValue, index, originalArray)
    result.push(callback(this[i], i, this));
  }
  return result;
};
```

#### `Array.filter()` — Select Elements

```javascript
// filter: creates NEW array with elements that pass the test (callback returns true)
const numbers = [1, 2, 3, 4, 5, 6];
const evens = numbers.filter(n => n % 2 === 0);
// [2, 4, 6]

const adults = users.filter(user => user.age >= 18);

// Implementing filter from scratch:
Array.prototype.myFilter = function(callback) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    if (callback(this[i], i, this)) {
      result.push(this[i]);
    }
  }
  return result;
};
```

#### `Array.reduce()` — Reduce to Single Value

```javascript
// reduce: accumulates array to a single value
// SYNTAX: array.reduce(callback, initialValue)
// callback receives: (accumulator, currentValue, index, array)

const numbers = [1, 2, 3, 4, 5];

// Sum:
const sum = numbers.reduce((acc, curr) => acc + curr, 0);
// Step: acc=0, curr=1 → 1
// Step: acc=1, curr=2 → 3
// Step: acc=3, curr=3 → 6
// Step: acc=6, curr=4 → 10
// Step: acc=10, curr=5 → 15
// Result: 15

// Product:
const product = numbers.reduce((acc, curr) => acc * curr, 1);
// 120

// Max value:
const max = numbers.reduce((acc, curr) => Math.max(acc, curr), -Infinity);
// 5

// Flatten array:
const nested = [[1, 2], [3, 4], [5, 6]];
const flat = nested.reduce((acc, curr) => acc.concat(curr), []);
// [1, 2, 3, 4, 5, 6]

// Count occurrences:
const words = ["apple", "banana", "apple", "cherry", "banana", "apple"];
const counts = words.reduce((acc, word) => {
  acc[word] = (acc[word] || 0) + 1;
  return acc;
}, {});
// { apple: 3, banana: 2, cherry: 1 }

// Group by:
const people = [
  { name: "Alice", city: "NY" },
  { name: "Bob", city: "LA" },
  { name: "Carol", city: "NY" }
];
const byCity = people.reduce((acc, person) => {
  const city = person.city;
  if (!acc[city]) acc[city] = [];
  acc[city].push(person);
  return acc;
}, {});
// { NY: [Alice, Carol], LA: [Bob] }

// Implementing reduce from scratch:
Array.prototype.myReduce = function(callback, initialValue) {
  let acc = initialValue !== undefined ? initialValue : this[0];
  let startIndex = initialValue !== undefined ? 0 : 1;
  
  for (let i = startIndex; i < this.length; i++) {
    acc = callback(acc, this[i], i, this);
  }
  return acc;
};
```

### Chaining HOFs

```javascript
const students = [
  { name: "Alice", grade: 85, passed: true },
  { name: "Bob", grade: 42, passed: false },
  { name: "Carol", grade: 92, passed: true },
  { name: "Dave", grade: 55, passed: false }
];

// Chain filter → map → reduce:
const avgPassingGrade = students
  .filter(s => s.passed)           // [Alice(85), Carol(92)]
  .map(s => s.grade)               // [85, 92]
  .reduce((sum, grade, _, arr) => sum + grade / arr.length, 0);
// 88.5
```

---

## 6. IIFE — Immediately Invoked Function Expressions {#iife}

### What is an IIFE?

An IIFE is a function that is **defined and immediately called**. It runs once and then is gone.

```javascript
// SYNTAX 1 (most common):
(function() {
  console.log("I run immediately!");
})();

// SYNTAX 2 (alternative grouping):
(function() {
  console.log("Also runs immediately!");
}());

// Arrow IIFE:
(() => {
  console.log("Arrow IIFE!");
})();

// IIFE with parameters:
(function(name) {
  console.log(`Hello, ${name}!`);
})("Alice");  // "Hello, Alice!"

// IIFE with return value:
const result = (function() {
  return 42;
})();
console.log(result);  // 42
```

### Why Use IIFEs?

```javascript
// 1. AVOID POLLUTING GLOBAL SCOPE:
// Without IIFE — these variables are global!
var counter = 0;
var increment = function() { counter++; };

// With IIFE — these variables are private!
const { counter, increment } = (function() {
  let count = 0;
  return {
    counter: () => count,
    increment: () => ++count
  };
})();

// 2. CREATE PRIVATE SCOPE (Module Pattern):
const BankAccount = (function() {
  let balance = 0;  // PRIVATE — not accessible from outside
  
  return {
    deposit: function(amount) { balance += amount; },
    withdraw: function(amount) {
      if (amount <= balance) balance -= amount;
    },
    getBalance: function() { return balance; }
  };
})();

BankAccount.deposit(100);
BankAccount.withdraw(30);
console.log(BankAccount.getBalance());  // 70
console.log(BankAccount.balance);       // undefined (private!)

// 3. IIFE in FOR LOOP (old way to capture var — now use let instead):
for (var i = 0; i < 3; i++) {
  (function(index) {
    setTimeout(() => console.log(index), 100);
  })(i);
}
// 0, 1, 2 (correct!) — each IIFE captures its own 'index'
```

---

## 7. Closures — The Deep Dive {#closures}

### What is a Closure?

**Real-world analogy:** A closure is like a backpack. When you leave a room (function), you carry your backpack (closure) with you. Inside the backpack is everything that was in the room when you left. Even though the room is gone, you still have access to everything you packed.

Technically: **A closure is a function that remembers and has access to its outer scope even after the outer function has returned.**

```javascript
function outer() {
  const message = "Hello!";  // outer's local variable
  
  function inner() {
    // inner can access 'message' even after outer() returns!
    console.log(message);
  }
  
  return inner;
}

const myFunction = outer();
// outer() has finished executing — message should be gone!
// But...
myFunction();  // "Hello!" — message is still accessible!
```

### How Closures Work Internally

```
MEMORY DIAGRAM:

When outer() runs, an Execution Context is created:
┌─────────────────────────────────────────┐
│  outer() Execution Context              │
│  message: "Hello!"                      │
│  inner: [Function: inner]               │
│         ↑                               │
│         inner's [[Environment]] links   │
│         back to this scope             │
└─────────────────────────────────────────┘

When outer() returns and its EC is removed,
NORMALLY the memory would be freed.

But inner still has a REFERENCE to outer's scope!
So outer's scope is NOT garbage collected:

┌─────────────────────────────────────────┐
│  HEAP (persisted in memory)             │
│  [Closure Scope of outer]               │
│  message: "Hello!"   ← still alive!    │
└─────────────────────────────────────────┘

myFunction (= inner) has a hidden property
[[Environment]] → pointing to that scope

So when myFunction() is called, it can access 'message'!
```

### Closure Examples

#### The Classic Counter

```javascript
function createCounter() {
  let count = 0;  // Private variable — only accessible via the returned functions
  
  return {
    increment: function() { count++; },
    decrement: function() { count--; },
    getCount: function() { return count; },
    reset: function() { count = 0; }
  };
}

const counter = createCounter();
counter.increment();  // count = 1
counter.increment();  // count = 2
counter.increment();  // count = 3
counter.decrement();  // count = 2
console.log(counter.getCount());  // 2
console.log(counter.count);       // undefined (private!)

// Each call to createCounter creates INDEPENDENT counters:
const counter1 = createCounter();
const counter2 = createCounter();
counter1.increment();
counter1.increment();
counter2.increment();
console.log(counter1.getCount()); // 2
console.log(counter2.getCount()); // 1 (independent!)
```

#### Closure Bug with `var` in Loops

```javascript
// CLASSIC INTERVIEW QUESTION:
const functions = [];

for (var i = 0; i < 3; i++) {
  functions.push(function() {
    console.log(i);  // All print 3!
  });
}

functions[0]();  // 3 (expected 0)
functions[1]();  // 3 (expected 1)
functions[2]();  // 3 (expected 2)

// WHY? All three functions share the SAME 'i' (var is function-scoped).
// By the time they're called, the loop has ended and i === 3.

// FIX 1: Use let (each iteration gets its own 'i'):
for (let i = 0; i < 3; i++) {
  functions.push(function() {
    console.log(i);  // 0, 1, 2 ✅
  });
}

// FIX 2: IIFE to capture current value:
for (var i = 0; i < 3; i++) {
  (function(index) {  // 'index' is a new binding for each iteration
    functions.push(function() {
      console.log(index);  // 0, 1, 2 ✅
    });
  })(i);
}
```

### Practical Closure Use Cases

#### 1. Data Privacy (Encapsulation)

```javascript
function createUser(name, email) {
  let _balance = 0;  // Private — convention: underscore prefix
  const _email = email;  // Private
  
  return {
    getName: () => name,
    getBalance: () => _balance,
    
    deposit(amount) {
      if (amount > 0) {
        _balance += amount;
        console.log(`Deposited ${amount}. New balance: ${_balance}`);
      }
    },
    
    withdraw(amount) {
      if (amount > 0 && amount <= _balance) {
        _balance -= amount;
        console.log(`Withdrew ${amount}. New balance: ${_balance}`);
      } else {
        console.log("Insufficient funds");
      }
    }
  };
}

const user = createUser("Alice", "alice@example.com");
user.deposit(1000);    // "Deposited 1000. New balance: 1000"
user.withdraw(200);    // "Withdrew 200. New balance: 800"
console.log(user._balance);  // undefined (private!)
```

#### 2. Memoization (Caching)

```javascript
function memoize(fn) {
  const cache = {};  // Closed over — persists between calls
  
  return function(...args) {
    const key = JSON.stringify(args);
    
    if (cache[key] !== undefined) {
      console.log("Cache hit!");
      return cache[key];
    }
    
    console.log("Computing...");
    const result = fn(...args);
    cache[key] = result;
    return result;
  };
}

function expensiveAdd(a, b) {
  // Imagine this takes 2 seconds...
  return a + b;
}

const memoizedAdd = memoize(expensiveAdd);
console.log(memoizedAdd(1, 2));  // "Computing..." then 3
console.log(memoizedAdd(1, 2));  // "Cache hit!" then 3 (instant!)
console.log(memoizedAdd(3, 4));  // "Computing..." then 7
```

#### 3. Partial Application

```javascript
function multiply(a, b) {
  return a * b;
}

// Partial application: pre-fill some arguments
function partial(fn, ...presetArgs) {
  return function(...laterArgs) {
    return fn(...presetArgs, ...laterArgs);
  };
}

const double = partial(multiply, 2);
const triple = partial(multiply, 3);

console.log(double(5));   // 10
console.log(triple(5));   // 15
console.log(double(10));  // 20
```

#### 4. Event Handlers with State

```javascript
function createButton(label) {
  let clickCount = 0;  // Private to each button
  
  const button = document.createElement('button');
  button.textContent = label;
  
  button.addEventListener('click', function() {
    clickCount++;
    console.log(`${label} clicked ${clickCount} times`);
    button.textContent = `${label} (${clickCount})`;
  });
  
  return button;
}

const btn1 = createButton("Save");
const btn2 = createButton("Cancel");
// Each button has its own private clickCount!
document.body.append(btn1, btn2);
```

### Memory Implications of Closures

```javascript
// POTENTIAL MEMORY LEAK:
function createLeak() {
  const bigData = new Array(1000000).fill('x');  // 1MB of data
  
  return function() {
    // This function only uses bigData[0], but the ENTIRE bigData
    // array is kept in memory because the closure references bigData!
    return bigData[0];
  };
}

const leakyFn = createLeak();
// bigData is still in memory even though we only need index 0!

// FIX:
function createNoLeak() {
  const bigData = new Array(1000000).fill('x');
  const onlyWhatWeNeed = bigData[0];  // Extract what we need
  // bigData can now be garbage collected after the function returns!
  
  return function() {
    return onlyWhatWeNeed;
  };
}
```

---

## 8. The `this` Keyword — Complete Guide {#this}

### What is `this`?

`this` is a special keyword that refers to the **context** in which a function is called. It's NOT about where the function is defined — it's about HOW and WHERE the function is called.

**Real-world analogy:** When you say "I work here," the word "I" means different things depending on who says it. Similarly, `this` means different things depending on the context.

### Rule 1: Global Context

```javascript
// In a browser (non-strict mode):
console.log(this);  // Window object (the global object)

// In strict mode:
"use strict";
console.log(this);  // undefined (inside functions)

// In Node.js (module scope):
console.log(this);  // {} (module's exports object)
```

### Rule 2: Regular Function — `this` is Dynamic (depends on call site)

```javascript
function showThis() {
  console.log(this);
}

// Called as a plain function:
showThis();  // Window (non-strict) or undefined (strict mode)

// Called as object method:
const obj = { name: "Alice", show: showThis };
obj.show();  // obj — {name: "Alice", show: f}

// Called with new:
const instance = new showThis();  // new creates a new object; this = new object
```

### Rule 3: Object Methods

```javascript
const person = {
  name: "Alice",
  
  greet: function() {
    console.log(this.name);  // 'this' = person (the object the method is called on)
  },
  
  // Arrow function — inherits this from outer scope (usually wrong for methods!)
  greetArrow: () => {
    console.log(this.name);  // 'this' = Window (NOT person!)
  }
};

person.greet();       // "Alice" ✅
person.greetArrow();  // undefined ❌

// Method extraction — loses 'this':
const greet = person.greet;
greet();  // undefined (called as plain function now, 'this' = global)
```

### Rule 4: Arrow Functions — Lexical `this`

```javascript
function Timer() {
  this.seconds = 0;
  
  // Arrow function inherits 'this' from Timer constructor:
  setInterval(() => {
    this.seconds++;  // 'this' = Timer instance ✅
    console.log(this.seconds);
  }, 1000);
}

const timer = new Timer();  // Works correctly!

// vs Regular function (broken):
function TimerBroken() {
  this.seconds = 0;
  
  setInterval(function() {
    this.seconds++;  // 'this' = Window (undefined in strict) ❌
  }, 1000);
}
```

### Rule 5: Event Listeners

```javascript
const button = document.querySelector('button');

// Regular function — 'this' = the element that triggered the event:
button.addEventListener('click', function() {
  console.log(this);          // button element
  this.textContent = "Clicked!";  // Works!
});

// Arrow function — 'this' = outer scope (usually Window):
button.addEventListener('click', () => {
  console.log(this);  // Window (NOT the button!)
  this.textContent = "Clicked!";  // Doesn't work as expected
});
```

### Rule 6: `new` Keyword

```javascript
function Person(name, age) {
  // When called with 'new', 'this' refers to the newly created object
  this.name = name;
  this.age = age;
  // Implicitly returns 'this' (the new object)
}

const alice = new Person("Alice", 25);
console.log(alice.name);  // "Alice"
console.log(alice.age);   // 25
```

### Priority Order of `this` Binding

```
1. new binding (highest priority): new Foo() → this = new object
2. Explicit binding: call/apply/bind → this = specified object
3. Implicit binding: obj.method() → this = obj
4. Default binding: func() → this = global (or undefined in strict)
```

---

## 9. call(), apply(), bind() {#call-apply-bind}

These three methods let you **explicitly set `this`** when calling a function.

### `call()` — Call with explicit `this`, individual args

```javascript
// SYNTAX: function.call(thisArg, arg1, arg2, ...)

function introduce(greeting, punctuation) {
  console.log(`${greeting}, I'm ${this.name}${punctuation}`);
}

const alice = { name: "Alice" };
const bob = { name: "Bob" };

introduce.call(alice, "Hello", "!");  // "Hello, I'm Alice!"
introduce.call(bob, "Hi", ".");       // "Hi, I'm Bob."

// Borrowing methods:
const person = {
  name: "Alice",
  greet: function() {
    return `Hi, I'm ${this.name}`;
  }
};

const user = { name: "Bob" };
console.log(person.greet.call(user));  // "Hi, I'm Bob" (borrowed!)
```

### `apply()` — Call with explicit `this`, args as array

```javascript
// SYNTAX: function.apply(thisArg, [arg1, arg2, ...])
// Same as call, but arguments passed as an ARRAY

introduce.apply(alice, ["Hello", "!"]);  // "Hello, I'm Alice!"

// Practical use — spreading an array into Math.max:
const numbers = [3, 1, 4, 1, 5, 9, 2, 6];
const max = Math.max.apply(null, numbers);  // 9
// Modern: Math.max(...numbers)

// Finding array max before spread operator existed:
const max2 = Math.max.apply(Math, numbers);  // 9
```

### `bind()` — Create a new function with fixed `this`

```javascript
// SYNTAX: const boundFn = function.bind(thisArg, arg1, arg2, ...)
// Returns a NEW function with 'this' permanently bound
// Does NOT call the function immediately!

const alice = { name: "Alice" };
function greet(greeting) {
  return `${greeting}, I'm ${this.name}`;
}

const aliceGreet = greet.bind(alice);        // Creates new function
const aliceHello = greet.bind(alice, "Hello"); // Also pre-fills args!

console.log(aliceGreet("Hi"));     // "Hi, I'm Alice"
console.log(aliceHello());         // "Hello, I'm Alice"

// Common use: preserving 'this' in event handlers
class Button {
  constructor(label) {
    this.label = label;
    this.clickCount = 0;
    
    // Without bind:
    // document.querySelector('btn').addEventListener('click', this.handleClick);
    // this.handleClick would have 'this' = the button element (wrong!)
    
    // With bind:
    this.handleClick = this.handleClick.bind(this);  // Now 'this' always = Button instance
  }
  
  handleClick() {
    this.clickCount++;
    console.log(`${this.label} clicked ${this.clickCount} times`);
  }
}
```

### Implementing bind() from Scratch (Interview Question!)

```javascript
Function.prototype.myBind = function(context, ...presetArgs) {
  const originalFn = this;  // 'this' here is the function being bound
  
  return function(...laterArgs) {
    return originalFn.call(context, ...presetArgs, ...laterArgs);
  };
};

// Test:
function multiply(a, b) { return a * b; }
const double = multiply.myBind(null, 2);
console.log(double(5));  // 10 ✅
```

### call vs apply vs bind Comparison

| Method | Invokes immediately? | Arguments | Use Case |
|--------|---------------------|-----------|---------|
| `call` | Yes | Individual args | Borrow methods, set this once |
| `apply` | Yes | Array of args | When args are already in array |
| `bind` | No (returns new fn) | Individual args | Create pre-configured function |

---

## 10. Default Parameters {#default-params}

```javascript
// OLD WAY (before ES6):
function greet(name) {
  name = name || "Guest";  // Problem: what if name = "" or 0?
  return `Hello, ${name}!`;
}

// ES6 Default Parameters:
function greet(name = "Guest") {  // Only used if name is undefined
  return `Hello, ${name}!`;
}

greet();           // "Hello, Guest!"
greet("Alice");    // "Hello, Alice!"
greet(undefined);  // "Hello, Guest!" (undefined triggers default)
greet(null);       // "Hello, null!" (null does NOT trigger default!)
greet("");         // "Hello, !" (empty string does NOT trigger default!)

// Default values can be expressions:
function createUser(name, role = "user", createdAt = new Date()) {
  return { name, role, createdAt };
}

// Default values can reference previous parameters:
function makeBox(width, height = width) {  // Square by default
  return { width, height, area: width * height };
}
makeBox(5);      // { width: 5, height: 5, area: 25 }
makeBox(5, 10);  // { width: 5, height: 10, area: 50 }

// Default values can call functions:
function getDefaultName() {
  return "Anonymous_" + Math.random().toString(36).slice(2);
}

function createProfile(name = getDefaultName()) {
  return { name };
}
// getDefaultName() is called each time name is not provided
```

---

## 11. Rest Parameters & Arguments Object {#rest-params}

### Rest Parameters (ES6)

```javascript
// SYNTAX: ...paramName (collects remaining args into array)
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

console.log(sum(1, 2, 3));       // 6
console.log(sum(1, 2, 3, 4, 5)); // 15

// Rest with fixed parameters before it:
function log(level, ...messages) {
  messages.forEach(msg => console.log(`[${level}]: ${msg}`));
}

log("INFO", "Starting app", "Loading config", "Ready");
// [INFO]: Starting app
// [INFO]: Loading config
// [INFO]: Ready

// Rules:
// 1. Rest must be LAST parameter: function foo(a, b, ...rest) ✅
// 2. Only ONE rest parameter per function
// 3. function foo(...rest, a) ❌ SyntaxError!
```

### The `arguments` Object (Old Way)

```javascript
// Regular functions have an implicit 'arguments' object
// NOT available in arrow functions!
function sum() {
  console.log(arguments);  // Arguments [1, 2, 3]
  
  let total = 0;
  for (let i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}
sum(1, 2, 3);  // 6

// arguments is array-LIKE but NOT an actual array:
// No .map(), .filter() etc.
// Convert to array:
function sum() {
  const args = Array.from(arguments);  // or [...arguments]
  return args.reduce((a, b) => a + b, 0);
}

// Arrow functions do NOT have arguments:
const sum = () => {
  console.log(arguments);  // ReferenceError!
};

// Use rest params instead (preferred):
const sum = (...args) => args.reduce((a, b) => a + b, 0);
```

---

## 12. Pure Functions & Side Effects {#pure-functions}

### What is a Pure Function?

A **pure function**:
1. Given the same inputs, ALWAYS returns the same output
2. Has NO side effects (doesn't modify anything outside itself)

```javascript
// PURE:
function add(a, b) {
  return a + b;  // Same inputs → always same output
}

// IMPURE — reads external variable:
let tax = 0.1;
function addTax(price) {
  return price + price * tax;  // Depends on external 'tax'!
  // If tax changes, same input gives different output!
}

// IMPURE — modifies external state:
let total = 0;
function addToTotal(n) {
  total += n;  // Side effect: modifies external variable!
  return total;
}

// IMPURE — modifies argument:
function double(arr) {
  for (let i = 0; i < arr.length; i++) {
    arr[i] *= 2;  // Modifies the original array!
  }
  return arr;
}

// PURE version:
function double(arr) {
  return arr.map(n => n * 2);  // Returns new array, original unchanged
}
```

### Why Pure Functions Matter

| Benefit | Explanation |
|---------|-------------|
| **Testability** | Easy to test: given X, expect Y. No mocking needed. |
| **Predictability** | No hidden state changes. Easier to reason about. |
| **Memoization** | Same input → same output, so results can be cached! |
| **Concurrency** | No shared mutable state → safe to run in parallel. |
| **Debugging** | No hidden side effects to hunt down. |

---

## 13. Currying & Partial Application {#currying}

### What is Currying?

**Currying** transforms a function with multiple arguments into a sequence of functions, each accepting ONE argument.

```javascript
// Normal function:
function add(a, b) {
  return a + b;
}
add(2, 3);  // 5

// Curried version:
function curriedAdd(a) {
  return function(b) {
    return a + b;
  };
}

curriedAdd(2)(3);  // 5
const add2 = curriedAdd(2);  // Partial application!
add2(3);  // 5
add2(10); // 12

// Arrow function curried:
const curriedAdd = a => b => a + b;
```

### Why Currying?

```javascript
// Real-world use case: Creating specialized functions from generic ones

// Generic function:
const multiply = (a, b) => a * b;

// Curried:
const curriedMultiply = a => b => a * b;

// Specialized versions:
const double = curriedMultiply(2);
const triple = curriedMultiply(3);
const tenTimes = curriedMultiply(10);

// Now use them:
[1, 2, 3, 4, 5].map(double);    // [2, 4, 6, 8, 10]
[1, 2, 3, 4, 5].map(triple);   // [3, 6, 9, 12, 15]
[1, 2, 3, 4, 5].map(tenTimes); // [10, 20, 30, 40, 50]
```

### General Curry Function (Interview Question!)

```javascript
// Converts any function to curried form:
function curry(fn) {
  return function curried(...args) {
    // If we have enough arguments, call the original function:
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    
    // Otherwise, return a new function expecting more args:
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}

// Test:
function add(a, b, c) {
  return a + b + c;
}

const curriedAdd = curry(add);

curriedAdd(1)(2)(3);    // 6 (one at a time)
curriedAdd(1, 2)(3);    // 6 (mixed)
curriedAdd(1)(2, 3);    // 6 (mixed)
curriedAdd(1, 2, 3);    // 6 (all at once)
```

---

## 14. Function Composition {#composition}

### What is Composition?

Combining small, focused functions to create more complex functionality.

```javascript
// Math analogy: f(g(x))
// Apply g first, then f on the result

const double = x => x * 2;
const addOne = x => x + 1;
const square = x => x * x;

// Without composition:
const result = square(addOne(double(3)));  // double(3)=6, addOne(6)=7, square(7)=49

// compose: applies functions right-to-left (mathematical order)
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

const transform = compose(square, addOne, double);
transform(3);  // 49 — applies: double → addOne → square

// pipe: applies functions left-to-right (more intuitive reading order)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const transform = pipe(double, addOne, square);
transform(3);  // 49 — same result, but more readable: "first double, then addOne, then square"
```

### Real-World Composition

```javascript
// Data processing pipeline:
const processUsers = pipe(
  users => users.filter(u => u.active),              // Filter active users
  users => users.map(u => ({ ...u, name: u.name.toUpperCase() })),  // Uppercase names
  users => users.sort((a, b) => a.name.localeCompare(b.name)),  // Sort alphabetically
  users => users.slice(0, 10)                         // Take first 10
);

const result = processUsers(allUsers);
```

---

## 15. Memoization {#memoization}

### What is Memoization?

**Memoization** is an optimization technique where you cache the results of expensive function calls. If the function is called again with the same arguments, return the cached result instead of recomputing.

```javascript
// Without memoization:
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
// fibonacci(40) makes ~2 billion calls! Terrible performance!

// With memoization:
function memoize(fn) {
  const cache = new Map();
  
  return function(...args) {
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const memoFib = memoize(function fib(n) {
  if (n <= 1) return n;
  return memoFib(n - 1) + memoFib(n - 2);
});

console.log(memoFib(40));  // Almost instant! (vs seconds without memoization)

// Time complexity:
// Without memo: O(2^n) — exponential!
// With memo: O(n) — linear!
```

### useMemo in React (Preview)

```javascript
// React's useMemo works on the same principle:
const expensiveResult = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);  // Only recomputes when a or b changes
```

---

## 16. Recursion {#recursion}

### What is Recursion?

**Recursion** is when a function calls itself. Every recursive function needs:
1. **Base case** — when to STOP recursing
2. **Recursive case** — how to break the problem into smaller problems

**Real-world analogy:** Russian nesting dolls. To get to the smallest doll, you open each doll until you find the one that doesn't open (base case).

```javascript
// Factorial: n! = n × (n-1) × (n-2) × ... × 1
function factorial(n) {
  // Base case: stop condition
  if (n <= 1) return 1;
  
  // Recursive case: call with smaller n
  return n * factorial(n - 1);
}

// Trace: factorial(4)
// = 4 * factorial(3)
// = 4 * (3 * factorial(2))
// = 4 * (3 * (2 * factorial(1)))
// = 4 * (3 * (2 * 1))
// = 4 * (3 * 2)
// = 4 * 6
// = 24
```

### Recursion vs Iteration

```javascript
// Fibonacci:
// Iterative (better performance):
function fibIterative(n) {
  if (n <= 1) return n;
  let prev = 0, curr = 1;
  for (let i = 2; i <= n; i++) {
    [prev, curr] = [curr, prev + curr];
  }
  return curr;
}

// Recursive (elegant but slow without memoization):
function fibRecursive(n) {
  if (n <= 1) return n;
  return fibRecursive(n - 1) + fibRecursive(n - 2);
}

// Flatten nested array — recursion shines here:
function flatten(arr) {
  return arr.reduce((flat, item) => {
    return Array.isArray(item)
      ? flat.concat(flatten(item))  // Recursive call!
      : flat.concat(item);
  }, []);
}

flatten([1, [2, [3, [4, [5]]]]]);  // [1, 2, 3, 4, 5]

// Deep clone object:
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(deepClone);  // Recursive!
  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [key, deepClone(value)])  // Recursive!
  );
}
```

### Tail Call Optimization (TCO)

```javascript
// Regular recursion — EACH CALL adds a frame to call stack (stack overflow risk):
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);  // Needs to wait for recursive call before multiplying
}

// Tail call — recursive call is the LAST operation (can be optimized):
function factorial(n, accumulator = 1) {
  if (n <= 1) return accumulator;
  return factorial(n - 1, n * accumulator);  // Tail call — no pending operation
}
// Note: TCO is only supported in strict mode in some environments
```

---

## 17. Generator Functions {#generators}

### What are Generators?

Generators are special functions that can **pause** and **resume** execution, yielding multiple values over time.

```javascript
// SYNTAX: function* (note the asterisk)
function* simpleGenerator() {
  yield 1;  // pause, return 1
  yield 2;  // pause, return 2
  yield 3;  // pause, return 3
  // return; (implicit)
}

const gen = simpleGenerator();

console.log(gen.next());  // { value: 1, done: false }
console.log(gen.next());  // { value: 2, done: false }
console.log(gen.next());  // { value: 3, done: false }
console.log(gen.next());  // { value: undefined, done: true }

// Generators are iterable:
for (const value of simpleGenerator()) {
  console.log(value);  // 1, 2, 3
}

[...simpleGenerator()]  // [1, 2, 3]
```

### Infinite Sequences

```javascript
// Generate infinite sequence of IDs:
function* idGenerator() {
  let id = 1;
  while (true) {  // Infinite loop is OK in generators!
    yield id++;
  }
}

const getId = idGenerator();
console.log(getId.next().value);  // 1
console.log(getId.next().value);  // 2
console.log(getId.next().value);  // 3
// ... generates IDs on demand, no memory issues!
```

---

## 18. Async Functions (Preview) {#async-functions}

```javascript
// async functions ALWAYS return a Promise
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    // await "pauses" the function until the Promise resolves
    // OTHER code continues running while we wait!
    const user = await response.json();
    return user;  // This is wrapped in a resolved Promise automatically
  } catch (error) {
    console.error("Failed to fetch user:", error);
    throw error;  // Re-throws (wrapped in rejected Promise)
  }
}

// Usage:
fetchUser(1).then(user => console.log(user));

// Or in another async function:
async function main() {
  const user = await fetchUser(1);
  console.log(user);
}
```

---

## 19. Chapter Summary & Interview Prep {#summary}

### Revision Notes

```
FUNCTION TYPES:
✅ Declaration: hoisted, named, can be called before definition
✅ Expression: NOT hoisted, often anonymous, stored in variable
✅ Arrow: shorter syntax, lexical 'this', no 'arguments', can't be constructor
✅ IIFE: self-invoking, creates private scope, runs once

CLOSURES:
✅ Inner function has access to outer function's variables after outer returns
✅ Each function call creates a NEW closure (independent state)
✅ Use for: data privacy, memoization, factories, module pattern
✅ var in loops: all closures share same variable! Fix with let or IIFE

THIS KEYWORD:
✅ Regular function: 'this' depends on how function is CALLED
✅ Arrow function: 'this' is inherited from outer lexical scope (never changes)
✅ Method call: obj.method() → this = obj
✅ Plain call: func() → this = global (undefined in strict)
✅ new keyword: this = new object
✅ call/apply/bind: explicitly set this

CALL/APPLY/BIND:
✅ call(thisArg, arg1, arg2) → calls immediately, args individually
✅ apply(thisArg, [arg1, arg2]) → calls immediately, args as array
✅ bind(thisArg, ...args) → returns new function with bound this (NOT called)

HIGHER-ORDER FUNCTIONS:
✅ map: transform each element → new array (pure)
✅ filter: keep elements that pass test → new array (pure)
✅ reduce: accumulate array to single value
✅ forEach: side effects (no return value)

CLOSURES INTERVIEW GOLD:
✅ Counter with private state
✅ var in loop bug → use let or IIFE to fix
✅ Module pattern
✅ Memoization pattern
```

### Interview Cheat Sheet

```
"Arrow functions have lexical 'this' — they inherit 'this' from where they're DEFINED"
"Closure: inner function retains access to outer scope after outer function returns"
"call and apply call immediately; bind returns a new bound function"
"Pure function: same input → same output, no side effects"
"Currying converts f(a,b,c) to f(a)(b)(c)"
"Memoization caches expensive function results by argument"
"Generator function* uses yield to pause and resume execution"
"async function always returns a Promise; await pauses without blocking thread"
"IIFE creates a private scope immediately — used before modules"
"var in loops creates ONE shared variable; let creates per-iteration binding"
"HOF: takes functions as args OR returns functions (map, filter, reduce)"
```

---

## Top 25 Interview Questions — Chapter 3

**Q1. What is a closure? Give a practical example.**

*Answer:* A closure is created when an inner function retains access to its outer function's variables even after the outer function has returned. This happens because the inner function maintains a reference to its outer lexical environment. Practical example: a counter factory that returns increment/decrement functions that all share the same private `count` variable.

**Q2. What is the output of this code?**
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
```
*Answer:* `3, 3, 3`. All three arrow functions share the same `i` (var is function-scoped). By the time setTimeout runs, `i` is already 3. Fix with `let` (block-scoped, per-iteration binding).

**Q3. Explain the difference between arrow functions and regular functions.**

*Answer:* Key differences: (1) Arrow functions have lexical `this` (inherited from outer scope), regular functions have dynamic `this` (based on call site). (2) Arrow functions have no `arguments` object. (3) Arrow functions cannot be used as constructors (no `new`). (4) Arrow functions have no `prototype` property. (5) Shorter syntax. Use regular functions for object methods and constructors; use arrow functions for callbacks and when you want lexical `this`.

**Q4. What is the difference between call(), apply(), and bind()?**

*Answer:* All three let you explicitly set `this`. `call(thisArg, arg1, arg2)` calls the function immediately with individual arguments. `apply(thisArg, [args])` calls immediately with an array of arguments. `bind(thisArg, ...args)` returns a NEW function with permanently bound `this` (and optionally pre-filled args) without calling it immediately.

**Q5. What is a higher-order function?**

*Answer:* A function that takes one or more functions as arguments AND/OR returns a function. Examples: `Array.map`, `Array.filter`, `Array.reduce`, `setTimeout`, `addEventListener`. HOFs are a cornerstone of functional programming.

**Q6. Implement debounce from scratch.**

```javascript
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```

**Q7. What is currying and why is it useful?**

*Answer:* Currying transforms `f(a, b, c)` into `f(a)(b)(c)` — a sequence of functions each taking one argument. It's useful for: creating specialized functions from general ones (e.g., `multiply(2)` gives `double`), partial application, and function composition. It promotes code reuse and more declarative programming.

**Q8. What is the difference between function declaration and function expression?**

*Answer:* Function declarations are fully hoisted (can be called before they appear in code). Function expressions are not fully hoisted (only the variable declaration is hoisted). Declarations always have names; expressions can be anonymous. Use declarations for main utility functions; use expressions when you need conditional definition or when passing as callbacks.

**Q9. Explain `this` in arrow functions.**

*Answer:* Arrow functions don't have their own `this`. They capture `this` from their surrounding lexical scope at the time they're **defined** (not when called). This means `this` in an arrow function never changes regardless of how or where the function is called. This makes them ideal for callbacks in methods (where you want to preserve the outer `this`), but bad for object methods themselves (where `this` should be the object).

**Q10. What is memoization?**

*Answer:* Memoization is a performance optimization technique where function results are cached based on their inputs. If the function is called again with the same arguments, the cached result is returned immediately instead of recomputing. It's most effective for pure functions with expensive computations (like Fibonacci) and only works correctly when the same inputs always produce the same output.

---

## 5 Output Prediction Exercises

### Exercise 1
```javascript
const person = {
  name: "Alice",
  greet: function() {
    return `Hi from ${this.name}`;
  },
  greetArrow: () => {
    return `Hi from ${this.name}`;
  }
};

console.log(person.greet());       // ?
console.log(person.greetArrow());  // ?

const fn = person.greet;
console.log(fn());                 // ?
```
**Answer:** `"Hi from Alice"`, `"Hi from undefined"` (arrow uses Window.name = ""), `"Hi from undefined"` or TypeError in strict mode.

### Exercise 2
```javascript
function outer() {
  var x = 10;
  function inner() {
    console.log(x);
  }
  x = 20;
  return inner;
}
outer()();  // ?
```
**Answer:** `20` — The closure captures a REFERENCE to `x`, not a snapshot. By the time `inner()` runs, `x` has been updated to 20.

### Exercise 3
```javascript
const add = x => y => x + y;
const add5 = add(5);
console.log(add5(3));   // ?
console.log(add(2)(4)); // ?
```
**Answer:** `8`, `6`

### Exercise 4
```javascript
function makeCounter() {
  let n = 0;
  return {
    count: () => ++n,
    reset: () => n = 0
  };
}

const c = makeCounter();
console.log(c.count());  // ?
console.log(c.count());  // ?
c.reset();
console.log(c.count());  // ?
```
**Answer:** `1`, `2`, `1`

### Exercise 5
```javascript
function foo(a, b = a * 2) {
  return a + b;
}
console.log(foo(3));     // ?
console.log(foo(3, 4));  // ?
```
**Answer:** `9` (3 + 3*2 = 9), `7` (3 + 4 = 7)

---

## 10 MCQs

**Q1.** What does `bind()` return?
- A) The result of calling the function
- B) A new function with bound `this`
- C) A Promise
- D) undefined

**Answer: B**

---

**Q2.** Which of the following has its own `this`?
- A) Arrow function
- B) Regular function
- C) Both
- D) Neither

**Answer: B**

---

**Q3.** What is output?
```javascript
const greet = function(name) {
  return `Hello, ${name}`;
};
console.log(greet.name);
```
- A) undefined
- B) "greet"
- C) "name"
- D) ""

**Answer: B** — Named function expressions capture the variable name.

---

**Q4.** Which is NOT a feature of arrow functions?
- A) Shorter syntax
- B) Lexical `this`
- C) `arguments` object
- D) Implicit return for single expression

**Answer: C** — Arrow functions do NOT have the `arguments` object.

---

**Q5.** What does this output?
```javascript
function outer() {
  let count = 0;
  return () => ++count;
}
const inc = outer();
inc(); inc(); console.log(inc());
```
- A) 1
- B) 2
- C) 3
- D) 0

**Answer: C** — The arrow function closes over `count`. Each `inc()` call increments it.

---

**Q6.** Pure functions are:
- A) Functions with no parameters
- B) Functions that always return the same output for same input and have no side effects
- C) Functions with only one line
- D) Functions that don't use closures

**Answer: B**

---

**Q7.** What is memoization most useful for?
- A) Functions with side effects
- B) Impure functions
- C) Expensive pure functions called with repeated arguments
- D) Async functions

**Answer: C**

---

**Q8.** `Array.prototype.reduce` is classified as a:
- A) Pure function
- B) Higher-order function
- C) Constructor function
- D) Generator function

**Answer: B** — It takes a callback function as an argument.

---

**Q9.** What happens if a recursive function has no base case?
- A) It returns undefined
- B) It throws a TypeError
- C) Stack overflow (Maximum call stack size exceeded)
- D) It runs forever without error

**Answer: C**

---

**Q10.** What is the difference between rest parameters and the arguments object?
- A) Rest parameters work in arrow functions; arguments doesn't
- B) Rest is an actual Array; arguments is array-like
- C) Both A and B are correct
- D) There is no difference

**Answer: C** — Rest parameters work in arrow functions AND are true Arrays (with all Array methods). The `arguments` object only works in regular functions and is array-like (no Array methods).

---

*End of Chapter 3 — Functions are the heart of JavaScript. Every advanced concept builds on what you've learned here.*
