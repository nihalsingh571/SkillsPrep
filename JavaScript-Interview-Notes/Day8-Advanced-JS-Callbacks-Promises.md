# Day 8 — ADVANCED JS, CALLBACKS, COPYING, ERRORS & PROMISES

## 1. DAY OBJECTIVE
The objective of today's revision is to master advanced JavaScript concepts that are heavily tested in interviews. We will conquer asynchronous JavaScript starting from callback hell, moving into Error Handling, and ending with Promises. Additionally, we will deeply explore how JavaScript manages memory (Shallow vs Deep copying) and uncover the mysteries of the `this` keyword in different execution contexts.

---

## 2. COMPLETE CONCEPT NOTES

### Callback Hell
Before Promises and `async/await`, asynchronous logic was handled entirely by passing callback functions. When multiple asynchronous tasks depend on each other, you nest callbacks inside callbacks. This creates a "pyramid of doom" known as Callback Hell.

```js
// Example of Callback Hell
getUser(123, function(user) {
  getOrders(user.id, function(orders) {
    getDetails(orders[0].id, function(details) {
      calculateTotal(details, function(total) {
        console.log('Total is:', total);
        // We are 5 levels deep...
      });
    });
  });
});
```
**Problems with Callback Hell:**
1. **Unreadable:** Code grows horizontally, making it difficult to read and maintain.
2. **Error Handling is difficult:** You have to handle errors at every single level.
3. **Inversion of Control:** You hand over your callback to a third-party function, trusting they will call it at the right time and only once. (Promises fix this!).

---

### Shallow vs Deep Copy — CRITICAL
In JavaScript, primitives (strings, numbers, booleans) are passed by value. Objects and Arrays are passed by reference. When you "copy" an object simply by assigning it (`const a = b`), you are only copying the memory address.

**Shallow Copy:**
Copies the top-level properties of an object. However, if the property is another object or array, it only copies the reference to that nested object.
```js
const original = { name: 'John', address: { city: 'NY' } };

// Ways to shallow copy:
const copy1 = { ...original };           // Spread operator
const copy2 = Object.assign({}, original); // Object.assign
const arrCopy = [...arr];
const arrCopy2 = arr.slice();

// The problem with shallow copy:
copy1.name = 'Jane';           // original.name stays 'John'
copy1.address.city = 'LA';     // original.address.city becomes 'LA'! They share reference.
```

**Deep Copy:**
A deep copy completely duplicates every level of the object, creating entirely independent memory addresses.
```js
// 1. The classic (but flawed) way:
const deep1 = JSON.parse(JSON.stringify(original));
// Flaws of JSON method: 
// - Ignores undefined properties
// - Removes functions
// - Converts Dates to strings
// - Fails on circular references

// 2. The Modern Standard (ES2022+):
const deep2 = structuredClone(original);
// Handles Maps, Sets, Dates, nested objects, and circular references.
// Note: Still cannot copy functions or DOM nodes.

// 3. Lodash library
// const deep3 = _.cloneDeep(original);
```

**Comparison Table:**

| Method | Type | Handles nested? | Handles Date/Function? |
|---|---|---|---|
| Spread `{...obj}` | Shallow | No | Yes (copied as reference) |
| `Object.assign` | Shallow | No | Yes |
| JSON parse/stringify | Deep | Yes | No (Date→string, fn→lost) |
| `structuredClone` | Deep | Yes | Partial (no functions, yes Dates) |

---

### Error Handling
Errors in JS crash the application if unhandled. `try...catch` blocks allow us to gracefully handle these errors.

```js
try {
  // Code that might throw an error
  const data = JSON.parse('{"bad": json}'); // Throws SyntaxError
} catch (error) {
  // Executes if an error is thrown in the try block
  console.error('Error occurred:', error.message);
  console.error('Error name:', error.name);
} finally {
  // Executes unconditionally, whether try succeeds or catch runs
  console.log('Cleanup code goes here (e.g., closing loaders)');
}
```

**Error Types:** `Error`, `SyntaxError`, `ReferenceError`, `TypeError`, `RangeError`.

**Throwing Custom Errors:**
```js
function divide(a, b) {
  if (b === 0) throw new Error('Cannot divide by zero');
  if (typeof a !== 'number') throw new TypeError('Expected a number');
  return a / b;
}

// Custom Error Class
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field; // custom property
  }
}
```

---

### THIS Keyword — TOP INTERVIEW TOPIC
`this` is a keyword that refers to an object. Which object it refers to depends strictly on **HOW** the function is invoked, not where it is defined (for regular functions).

**The 5 Rules of `this`:**
1. **Global context:** In the browser, `this` is the `window` object. In Node, it's `global`. In "strict mode", global `this` inside a function is `undefined`.
2. **Implicit Binding (Method context):** When a function is called as a property of an object, `this` refers to the object *before the dot*.
   ```js
   const user = { name: 'Alice', greet() { return this.name; } };
   user.greet(); // 'Alice'
   ```
3. **Explicit Binding:** Using `call()`, `apply()`, or `bind()`, you explicitly force `this` to be a specific object.
4. **New Binding:** When a function is invoked with the `new` keyword (constructors), `this` refers to the newly created, empty object.
5. **Lexical Binding (Arrow Functions):** Arrow functions do NOT have their own `this`. They inherit `this` from the outer (enclosing) lexical scope at the time they are defined.

**Common `this` traps:**
```js
const obj = {
  name: 'Bob',
  greet() {
    // 1. Loss of context when assigned to a variable
    const { greet } = this; // 'this' is lost
    
    // 2. setTimeout trap
    setTimeout(function() { 
      console.log(this.name); 
    }, 0);  // undefined! Regular function defaults to window
    
    // The fix: Arrow function
    setTimeout(() => { 
      console.log(this.name); 
    }, 0);  // 'Bob' — inherits 'this' from greet()
  }
};
```

---

### Promises — CRITICAL
A Promise is an object representing the eventual completion (or failure) of an asynchronous operation and its resulting value. It solves the "Inversion of Control" problem of callbacks.

**Promise States:**
1. `pending`: Initial state, neither fulfilled nor rejected.
2. `fulfilled`: Operation completed successfully.
3. `rejected`: Operation failed.
*(Once a promise is fulfilled or rejected, it is considered "settled" and cannot change state).*

**Creating a Promise:**
```js
const p = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = true;
    if (success) {
      resolve('Data fetched'); // Transitions to fulfilled
    } else {
      reject(new Error('Fetch failed')); // Transitions to rejected
    }
  }, 1000);
});
```

**Consuming a Promise:**
```js
p.then(value => {
  console.log(value); // Runs if resolved
})
.catch(err => {
  console.error(err); // Runs if rejected
})
.finally(() => {
  console.log('Done'); // Always runs
});
```

**Promise Chaining Rules:**
- `.then()` always returns a **NEW** promise.
- If the callback in `.then()` returns a normal value (e.g., `return 5`), the next `.then()` receives `5`.
- If the callback returns a Promise, the next `.then()` waits for it to settle.
- If an error is thrown anywhere in the chain, it skips all subsequent `.then()` blocks and goes straight to the nearest `.catch()`.

**Example:**
```js
fetch('/api/user')
  .then(res => res.json())
  .then(user => fetch(`/api/orders/${user.id}`))
  .then(res => res.json())
  .then(orders => console.log(orders))
  .catch(err => console.error('Caught error for ANY step:', err));
```

---

## 3. CODE EXAMPLES (runnable ES6+)

### Example 1: Recursive Deep Clone function
```js
function deepClone(obj) {
  // Handle null and non-objects (primitives)
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  
  // Handle Date
  if (obj instanceof Date) return new Date(obj.getTime());
  
  // Handle Array
  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item));
  }
  
  // Handle Object
  const clone = {};
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key]); // Recursive call
    }
  }
  return clone;
}

const original = { a: 1, b: { c: 2 }, d: new Date() };
const copied = deepClone(original);
```

### Example 2: Promisifying a callback-based API
```js
// Legacy callback API
function fsReadFile(path, callback) {
  setTimeout(() => {
    if (path === 'file.txt') callback(null, 'File content');
    else callback(new Error('Not found'), null);
  }, 500);
}

// Convert to Promise
function readFileAsync(path) {
  return new Promise((resolve, reject) => {
    fsReadFile(path, (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// Usage
readFileAsync('file.txt')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

---

## 4. PRACTICAL CODING QUESTIONS

### Q1. Create a Promise-based delay function
**Approach:** Wrap `setTimeout` in a Promise.
**Solution:**
```js
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Usage
console.log('Start');
delay(2000).then(() => console.log('2 seconds passed'));
```
**Complexity:** O(1) time and space.

### Q2. Implement Promise.all manually
**Approach:** Create an array for results. Count how many promises have resolved. If count equals the array length, resolve the main promise. If any reject, reject the main promise.
**Solution:**
```js
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completedCount = 0;
    
    if (promises.length === 0) return resolve(results);
    
    promises.forEach((p, index) => {
      Promise.resolve(p) // Wrap in Promise.resolve in case a raw value is passed
        .then(value => {
          results[index] = value; // Maintain order
          completedCount++;
          if (completedCount === promises.length) {
            resolve(results);
          }
        })
        .catch(err => reject(err)); // Reject immediately on first error
    });
  });
}
```

### Q3. Fetch user data and handle errors properly
**Solution:**
```js
function getUserData(url) {
  return fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      return res.json();
    })
    .catch(err => {
      console.error('Fetch failed:', err.message);
      // Decide whether to throw it further or return fallback
      return null; 
    });
}
```

### Q4. Create a deep clone function using recursion
*(See Code Examples section)*

### Q5. Fix a 'this' binding problem in event listener
**Scenario:** A class method used as an event listener loses `this`.
**Solution:**
```js
class Counter {
  constructor() {
    this.count = 0;
    this.btn = document.getElementById('btn');
    
    // FIX 1: bind(this)
    // this.btn.addEventListener('click', this.increment.bind(this));
    
    // FIX 2: Arrow function wrapper
    this.btn.addEventListener('click', () => this.increment());
  }
  
  increment() {
    this.count++;
    console.log(this.count);
  }
}
```

### Q6. Convert callback-based function to Promise
*(See Code Examples section)*

---

## 5. OUTPUT-BASED QUESTIONS

**Q1. this in different calling contexts**
```js
const obj = {
  message: 'Hello',
  getMessage() { return this.message; }
};
const fn = obj.getMessage;
console.log(fn());
```
**Answer:** `undefined` (or throws TypeError in strict mode).
**Explanation:** `fn` is invoked as a bare function call (`fn()`), losing its connection to `obj`. The implicit binding is lost.

**Q2. Arrow function this vs regular function this**
```js
const user = {
  name: 'Dev',
  regular: function() { return this.name; },
  arrow: () => { return this.name; }
};
console.log(user.regular());
console.log(user.arrow());
```
**Answer:** `Dev`, `undefined`
**Explanation:** `regular` uses implicit binding (object before the dot). `arrow` functions don't have their own `this`; they inherit from the global scope (window), where `name` is undefined.

**Q3. Shallow copy mutation side effect**
```js
const user = { id: 1, profile: { age: 30 } };
const clone = { ...user };
clone.id = 2;
clone.profile.age = 40;
console.log(user.id, user.profile.age);
```
**Answer:** `1, 40`
**Explanation:** Spread creates a shallow copy. Primitives (`id`) are separate, but references (`profile`) are shared.

**Q4. JSON.parse(JSON.stringify()) with Date**
```js
const obj = { date: new Date() };
const clone = JSON.parse(JSON.stringify(obj));
console.log(typeof clone.date);
```
**Answer:** `"string"`
**Explanation:** `JSON.stringify` converts the Date object into an ISO string. `JSON.parse` does not know it was originally a Date, so it remains a string.

**Q5. Promise chain: what gets passed to each .then**
```js
Promise.resolve(2)
  .then(val => val * 2)
  .then(val => console.log(val));
```
**Answer:** Logs `4`.
**Explanation:** The return value of one `.then` becomes the input argument for the next `.then`.

**Q6. try/catch with return in finally**
```js
function test() {
  try {
    return 1;
  } finally {
    return 2;
  }
}
console.log(test());
```
**Answer:** `2`
**Explanation:** `finally` ALWAYS executes. If `finally` returns a value, it overrides any return value from `try` or `catch`.

**Q7. Detached method this problem**
```js
var length = 4;
function callback() { console.log(this.length); }
const obj = {
  length: 5,
  method(fn) { fn(); }
};
obj.method(callback);
```
**Answer:** `4`
**Explanation:** `fn()` is invoked without a dot. It defaults to the global window object. `var length = 4` is attached to window.

**Q8. Multiple .then chaining return values**
```js
Promise.resolve(1)
  .then(() => 2)
  .then(console.log);
```
**Answer:** `2`
**Explanation:** `console.log` receives the returned value `2` from the previous `.then()`.

**Q9. catch and re-throw pattern**
```js
Promise.reject(new Error('fail'))
  .catch(err => { console.log('caught'); throw err; })
  .then(() => console.log('success'))
  .catch(err => console.log('caught again'));
```
**Answer:** `caught`, `caught again`
**Explanation:** The first `catch` logs, then re-throws the error. This skips the `.then()` block and hits the final `.catch()`.

**Q10. Promise without return**
```js
Promise.resolve(1)
  .then(val => { val * 2 })
  .then(val => console.log(val));
```
**Answer:** `undefined`
**Explanation:** The first `.then()` has curly braces but no `return` keyword, so it implicitly returns `undefined`.

---

## 6. DEBUGGING QUESTIONS

**Q1. Unhandled Promise Rejection**
*Buggy Code:*
```js
function doWork() { Promise.reject('Failed!'); }
doWork();
```
*Wrong:* Triggers an UnhandledPromiseRejection error.
*Correct:* `doWork().catch(err => console.error(err));` or wrap inside a `.catch()` if `doWork` returned the promise.
*Why:* Rejected promises MUST be caught somewhere in the application, otherwise it's a fatal error in Node and a warning in browsers.

**Q2. This is undefined in React/Classes**
*Buggy Code:*
```js
class UI {
  constructor() { this.name = 'UI'; }
  handleClick() { console.log(this.name); }
}
const ui = new UI();
document.body.addEventListener('click', ui.handleClick);
```
*Wrong:* Logs `undefined`.
*Correct:* `document.body.addEventListener('click', () => ui.handleClick());`
*Why:* The browser calls the handler with `this` set to the DOM element (`document.body`), losing the class context.

**Q3. Forgetting to return a Promise**
*Buggy Code:*
```js
function fetchData() {
  fetch('/api').then(res => res.json()); // No return!
}
fetchData().then(data => console.log(data)); // Error: undefined has no .then
```
*Correct:* `return fetch('/api')...`
*Why:* If you don't return the promise from your function, the caller gets `undefined` and cannot chain `.then()`.

**Q4. Shallow copy array side effects**
*Buggy Code:*
```js
const matrix = [[1], [2]];
const copy = [...matrix];
copy[0].push(99); // Modifies original matrix too!
```
*Correct:* `const copy = structuredClone(matrix);`
*Why:* Spread only copies one level deep. Arrays inside arrays are still passed by reference.

---

## 7. INTERVIEW QUESTIONS

**1. What is the difference between shallow and deep copy? (Advanced)**
A shallow copy creates a new object, but inserts references into it to the nested objects found in the original. If you mutate a nested property in the copy, it affects the original. A deep copy creates a completely new independent clone, recursively duplicating all nested objects and properties.

**2. What is structuredClone? (Basic)**
`structuredClone()` is a modern built-in JavaScript function used to create deep copies of objects. Unlike `JSON.parse(JSON.stringify())`, it supports circular references, Dates, Maps, Sets, and Arrays natively.

**3. What are the limitations of JSON.parse/stringify for copying? (Intermediate)**
It ignores properties with `undefined` values. It strips out functions. It converts `Date` objects into ISO strings. It throws a TypeError if the object contains circular references.

**4. What are the states of a Promise? (Basic)**
`pending` (initial state), `fulfilled` (completed successfully), and `rejected` (failed).

**5. What does .then() return? (Intermediate)**
`.then()` always returns a brand new Promise. This is what allows Promise chaining to work. If the `.then()` handler returns a value, the new Promise resolves with that value.

**6. How does Promise chaining work? (Intermediate)**
Because every `.then()` returns a new Promise, you can attach another `.then()` to it. The return value of one `.then()` callback is passed as the argument to the next `.then()` callback.

**7. Where does .catch() in a chain catch errors? (Intermediate)**
A `.catch()` block catches errors generated by *any* preceding Promise in the chain that has not already been caught. It acts as a safety net for the entire chain above it.

**8. What is the difference between a resolved and settled Promise? (Advanced)**
A "settled" promise is one that is no longer pending (it is either fulfilled OR rejected). A "resolved" promise generally implies successful fulfillment, but technically means it is locked in to match the state of another promise (which could eventually reject).

**9. Explain 'this' in 5 different contexts (Advanced)**
1. Global scope: points to `window`/`global`.
2. Method call: points to the object the method is called on.
3. Constructor (`new`): points to the newly instantiated object.
4. Explicit binding (`call/apply/bind`): points to the specifically provided object argument.
5. Arrow functions: has no own `this`, inherits it lexically from the surrounding scope.

**10. Why does 'this' differ between arrow functions and regular functions? (Frequently Asked)**
Regular functions determine `this` dynamically based on how they are invoked at runtime. Arrow functions determine `this` lexically based on where they are written in the code. Arrow functions cannot be bound to a new `this` using `.bind()`.

**11. What is the common 'this' bug in setTimeout? (Scenario)**
When passing an object method directly to `setTimeout` (e.g., `setTimeout(obj.method, 1000)`), the method loses its context and defaults to the global `window` object. This is fixed by wrapping it in an arrow function or using `.bind()`.

**12. What is try/catch/finally? Does finally always run? (Basic)**
It's a block used for handling synchronous errors (and `await` async errors). The `try` block contains risky code. `catch` handles the error. `finally` executes cleanup code. Yes, `finally` always runs, even if a `return` statement is inside the `try` or `catch`.

**13. What is callback hell and how do Promises solve it? (Frequently Asked)**
Callback hell is deeply nested callbacks that become unreadable. Promises solve this by flattening the asynchronous code structure using `.then()` chains, centralizing error handling with `.catch()`, and restoring "Inversion of Control" since the API returns a Promise object you control rather than you passing a callback.

**14. What are the built-in Error types? (Intermediate)**
`Error` (generic), `SyntaxError` (invalid JS code syntax), `ReferenceError` (using an undeclared variable), `TypeError` (value is not of the expected type, e.g., calling a non-function), `RangeError` (number outside allowable range).

**15. What is an unhandled promise rejection? (Intermediate)**
It occurs when a Promise transitions to a `rejected` state, but there is no `.catch()` block attached to handle the error. In Node.js, this traditionally caused the process to crash (or warn).

---

## 8. ⭐ MUST KNOW FOR MOCK
- Be prepared to trace `this` bindings through complex code blocks containing nested functions and arrow functions.
- Write a recursive `deepClone` function.
- Write `Promise.all` from scratch.
- Master how to flatten callback hell into a clean Promise chain.

---

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Forgetting that `.then()` returns a NEW promise, not the same one.
- Using `JSON.parse(JSON.stringify())` without mentioning its flaws regarding Dates and functions.
- Claiming arrow functions bind `this` to the window (they bind lexically, which *might* be window, but not always).
- Putting `return` inside `finally` and wondering why the function output changed.

---

## 10. NIGHT REVISION CHECKLIST
- [ ] Do I understand the Pyramid of Doom (Callback Hell)?
- [ ] Can I explain passing by value vs passing by reference?
- [ ] Can I write a deep copy using `structuredClone`?
- [ ] Do I know the limitations of JSON stringify cloning?
- [ ] Can I write a custom Error class?
- [ ] Do I understand what `finally` does?
- [ ] Can I recite the 5 rules of `this`?
- [ ] Do I know why arrow functions are good for callbacks inside methods?
- [ ] Can I explain the three states of a Promise?
- [ ] Do I know how to chain Promises and pass values?
- [ ] Can I implement `Promise.all` manually?
- [ ] Do I know how to catch errors properly in a Promise chain?
- [ ] Have I reviewed the `setTimeout` contextual `this` loss problem?
- [ ] Can I explain the difference between a TypeError and a ReferenceError?
- [ ] Have I completed the Mock interview checklist?
