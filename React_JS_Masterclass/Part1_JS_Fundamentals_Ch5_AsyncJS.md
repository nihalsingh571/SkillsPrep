# Chapter 5: Asynchronous JavaScript

> **"Mastering asynchronous JavaScript is the barrier between a junior and a senior developer. It's the engine that powers modern, non-blocking web applications."**

---

## Table of Contents

1. [Synchronous vs Asynchronous JavaScript](#sync-vs-async)
2. [Callbacks Deep Dive](#callbacks)
3. [Promises](#promises)
4. [Promise Static Methods](#promise-methods)
5. [Async/Await](#async-await)
6. [Error Handling](#error-handling)
7. [Fetch API](#fetch-api)
8. [AJAX & XMLHttpRequest (legacy)](#ajax)
9. [WebSockets](#websockets)
10. [Timers and Scheduling](#timers)
11. [Debouncing](#debouncing)
12. [Throttling](#throttling)
13. [Web Storage](#web-storage)
14. [JSON](#json)
15. [Chapter Summary & Interview Prep](#summary)

---

## 1. Synchronous vs Asynchronous JavaScript {#sync-vs-async}

### What is Sync Code? Problems with Blocking

By default, JavaScript is **synchronous** and **single-threaded**. This means it executes code one line at a time, top to bottom. If one line takes a long time (like fetching data), everything else is blocked.

**Real-world analogy:** A restaurant with one waiter (single thread). If the waiter stands by your table waiting 20 minutes for your food to cook (synchronous/blocking), no other tables get served. 

```javascript
// Synchronous (Blocking) Code:
console.log("Start");

// Imagine this takes 3 seconds...
const data = fetchSyncData(); // Blocks the entire page! UI freezes!

console.log("End");
```

### What is Async Code? Why it's needed

Asynchronous code allows JavaScript to start a long-running task and move on to the next line of code without waiting for the task to finish. When the task is done, JavaScript is notified and handles the result.

**Real-world analogy:** The waiter takes your order, gives it to the kitchen, and immediately goes to serve other tables (asynchronous/non-blocking). When the kitchen rings the bell (callback), the waiter brings your food.

```javascript
// Asynchronous (Non-Blocking) Code:
console.log("Start");

setTimeout(() => {
  console.log("Timer finished!"); // Runs after 2 seconds
}, 2000);

console.log("End");

// Output:
// "Start"
// "End"
// "Timer finished!" (after 2 seconds)
```

### How JS Handles Async (Single Thread + Event Loop)

JavaScript's main thread runs inside the JS Engine (like V8), which only does synchronous code. Async tasks (like timers, network requests, DOM events) are handed off to **Web APIs** (provided by the browser). 

When Web APIs finish the task, they push a callback function to the **Callback Queue**. The **Event Loop** constantly checks: "Is the Call Stack empty? If yes, take the first callback from the queue and put it on the stack."

---

## 2. Callbacks Deep Dive {#callbacks}

### The Callback Pattern

A callback is simply a function passed as an argument to another function, to be executed later.

```javascript
function greet(name, callback) {
  console.log(`Hello, ${name}!`);
  callback();
}

function sayGoodbye() {
  console.log("Goodbye!");
}

greet("Alice", sayGoodbye); 
// "Hello, Alice!" 
// "Goodbye!"
```

### Synchronous vs Asynchronous Callbacks

**Synchronous Callbacks:** Executed immediately, blocking the thread.
```javascript
const numbers = [1, 2, 3];
// The callback in forEach runs synchronously
numbers.forEach(num => console.log(num)); 
console.log("Done");
// Output: 1, 2, 3, "Done"
```

**Asynchronous Callbacks:** Executed later, via the Event Loop.
```javascript
console.log("Start");
setTimeout(() => console.log("Timeout"), 0);
console.log("End");
// Output: "Start", "End", "Timeout"
```

### Callback Hell (The Pyramid of Doom)

When you need to execute multiple async operations sequentially, callbacks lead to deeply nested, unreadable code.

```javascript
// Callback Hell example (getting user, then their posts, then comments):
getUser(1, function(user) {
  getPosts(user.id, function(posts) {
    getComments(posts[0].id, function(comments) {
      getAuthor(comments[0].authorId, function(author) {
        console.log("Finally got author:", author);
      }, function(error) {
        console.error(error); // Error handling repeated!
      });
    }, function(error) {
      console.error(error);
    });
  }, function(error) {
    console.error(error);
  });
}, function(error) {
  console.error(error);
});
```

**Problems with Callbacks:**
1. **Inversion of Control:** You hand your callback to a third-party library and trust them to call it correctly (not too early, not too late, not multiple times).
2. **Poor Readability:** Nested code is hard to follow.
3. **Complex Error Handling:** You must handle errors at every level.

---

## 3. Promises {#promises}

### What is a Promise?

A Promise is an object representing the eventual completion (or failure) of an asynchronous operation. 

**Real-world analogy:** A buzzer at a restaurant. You place an order and get a buzzer (a Promise). You can go talk to your friends (non-blocking). The buzzer will eventually ring green (fulfilled/resolved) or red (rejected, out of food).

### Promise States
1. **Pending:** Initial state, neither fulfilled nor rejected.
2. **Fulfilled (Resolved):** Operation completed successfully.
3. **Rejected:** Operation failed.
*(Once a Promise settles—fulfilled or rejected—its state cannot change.)*

### Creating a Promise (Executor Function)

```javascript
// SYNTAX: new Promise((resolve, reject) => { ... })

const myPromise = new Promise((resolve, reject) => {
  // Executor runs immediately!
  console.log("Executor running...");
  
  setTimeout(() => {
    const success = true;
    if (success) {
      resolve("Data fetched successfully!"); // Changes state to Fulfilled
    } else {
      reject("Failed to fetch data.");       // Changes state to Rejected
    }
  }, 1000);
});
```

### Consuming Promises (.then, .catch, .finally)

```javascript
myPromise
  .then(data => {
    // Runs if resolved
    console.log(data); 
  })
  .catch(error => {
    // Runs if rejected
    console.error(error);
  })
  .finally(() => {
    // Runs regardless of success/failure (useful for hiding loaders)
    console.log("Operation finished.");
  });
```

### Promise Chaining (Solving Callback Hell)

Every `.then()` returns a **new Promise**, allowing us to chain them flatly instead of nesting!

```javascript
getUser(1)
  .then(user => getPosts(user.id))       // returns a Promise
  .then(posts => getComments(posts[0].id)) // returns a Promise
  .then(comments => console.log(comments))
  .catch(error => console.error("Caught any error in the chain:", error));
  // A single catch handles errors for the ENTIRE chain!
```

### Returning Values from .then()

```javascript
Promise.resolve(10)
  .then(num => num * 2)    // Returns 20 (wrapped in a Promise automatically)
  .then(num => num + 5)    // Returns 25
  .then(num => {
    console.log(num);      // 25
    return Promise.resolve(100); // Explicitly returning a Promise
  })
  .then(console.log);      // 100
```

### Promisifying Callbacks

Converting old callback-based APIs to Promises:

```javascript
// Old callback style (Node.js fs)
const fs = require('fs');
fs.readFile('data.txt', 'utf8', (err, data) => { ... });

// Promisified version:
function readFilePromisified(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

readFilePromisified('data.txt').then(console.log).catch(console.error);
```

---

## 4. Promise Static Methods {#promise-methods}

JavaScript provides built-in methods to handle multiple promises concurrently.

### Promise.all() — "All or Nothing"
Waits for ALL promises to fulfill. If even ONE rejects, the entire `Promise.all` immediately rejects.

```javascript
const p1 = Promise.resolve("A");
const p2 = new Promise(res => setTimeout(() => res("B"), 1000));
const p3 = Promise.resolve("C");

Promise.all([p1, p2, p3])
  .then(results => console.log(results)) // ["A", "B", "C"] (Order is preserved!)
  .catch(err => console.error(err));

// If p2 rejected instead, .catch() would run immediately, ignoring A and C.
```

### Promise.allSettled() — "Wait for everything, good or bad" (ES2020)
Waits for all promises to finish (either fulfill or reject). Never rejects.

```javascript
const p1 = Promise.resolve("Success");
const p2 = Promise.reject("Failed");

Promise.allSettled([p1, p2])
  .then(results => {
    console.log(results);
    // [
    //   { status: "fulfilled", value: "Success" },
    //   { status: "rejected", reason: "Failed" }
    // ]
  });
```

### Promise.race() — "First to settle wins"
Returns the result/error of the FIRST promise to finish (fulfill or reject).

```javascript
const slow = new Promise(res => setTimeout(() => res("Slow"), 2000));
const fast = new Promise(res => setTimeout(() => res("Fast"), 1000));

Promise.race([slow, fast]).then(console.log); // "Fast"
```

### Promise.any() — "First to succeed wins" (ES2021)
Returns the FIRST fulfilled promise. Ignores rejections unless ALL reject.

```javascript
const p1 = Promise.reject("Fail 1");
const p2 = new Promise(res => setTimeout(() => res("Success!"), 1000));

Promise.any([p1, p2]).then(console.log); // "Success!" (Ignores p1)
// If all reject, throws an AggregateError.
```

### Comparison Table

| Method | Behavior | Short-circuits when? | Use Case |
|--------|----------|----------------------|----------|
| `all()` | Returns array of all values | 1st Rejection | Fetching dependent data, all needed |
| `allSettled()`| Returns array of statuses | Never | Batch operations, UI updates for all |
| `race()` | Returns first settled value | 1st Settle (Resolve/Reject) | Timeout mechanism for fetch |
| `any()` | Returns first resolved value | 1st Resolve | Fetching from multiple mirrors, need fastest |

---

## 5. Async/Await {#async-await}

### What is async/await? (ES2017)

`async/await` is syntactic sugar over Promises. It makes asynchronous code look and behave like synchronous code, improving readability.

1. **`async`** keyword: Placed before a function. It ensures the function ALWAYS returns a Promise.
2. **`await`** keyword: Can only be used inside an `async` function. It pauses the function execution until the Promise settles.

```javascript
// Promise .then() syntax:
function getUserData() {
  fetch('/api/user')
    .then(res => res.json())
    .then(user => console.log(user))
    .catch(err => console.error(err));
}

// Async/Await syntax (Cleaner!):
async function getUserDataAsync() {
  try {
    const res = await fetch('/api/user'); // Pauses here
    const user = await res.json();        // Pauses here
    console.log(user);
  } catch (err) {
    console.error(err);
  }
}
```

### Sequential vs Parallel Async Operations

**COMMON MISTAKE:** Running independent promises sequentially (slow!).

```javascript
// SLOW (Sequential): Takes 3 seconds total
async function getDashboardData() {
  // Waits 1s
  const users = await fetchUsers();     
  // Waits 2s
  const posts = await fetchPosts();     
  return { users, posts };
}

// FAST (Parallel): Takes 2 seconds total!
async function getDashboardDataFast() {
  // Start both immediately
  const usersPromise = fetchUsers();
  const postsPromise = fetchPosts();
  
  // Wait for both to finish concurrently
  const [users, posts] = await Promise.all([usersPromise, postsPromise]);
  return { users, posts };
}
```

### async/await with Loops

**For loop (Sequential):**
```javascript
async function processSequentially(ids) {
  for (const id of ids) {
    const data = await fetchItem(id); // Pauses loop!
    console.log(data);
  }
}
```

**Array.map (Parallel):**
```javascript
async function processInParallel(ids) {
  // Creates array of pending promises
  const promises = ids.map(id => fetchItem(id)); 
  // Waits for all to resolve
  const results = await Promise.all(promises); 
  console.log(results);
}
```
**Warning:** `forEach` does NOT wait for promises! Never use `await` inside a `.forEach()`.

---

## 6. Error Handling {#error-handling}

### try/catch/finally

The standard way to handle errors in async/await.

```javascript
async function fetchData() {
  try {
    // 1. Try to run this
    const data = await riskyOperation();
    console.log("Success:", data);
  } catch (error) {
    // 2. Catch errors (network failure, syntax errors, thrown errors)
    console.error("Caught an error:", error.message);
  } finally {
    // 3. Always runs, success or fail (cleanup, hide spinners)
    hideLoadingSpinner();
  }
}
```

### Error Types in JS

- **SyntaxError:** Typo in code (e.g., `let a = ;`)
- **TypeError:** Operation on wrong type (e.g., `null.method()`, `const x=1; x=2;`)
- **ReferenceError:** Accessing undeclared variable (e.g., `console.log(doesNotExist)`)
- **RangeError:** Value out of allowed range (e.g., array length < 0, Call stack overflow)

### Custom Errors

```javascript
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

function validateAge(age) {
  if (age < 0) throw new ValidationError("Age cannot be negative");
  return true;
}

try {
  validateAge(-5);
} catch (err) {
  if (err instanceof ValidationError) {
    console.log("Validation failed:", err.message);
  } else {
    console.log("Unknown error:", err);
  }
}
```

### Unhandled Promise Rejections

If a Promise rejects and there is no `.catch()` or `try/catch` block, it causes an "Unhandled Promise Rejection".

```javascript
// Node.js global handler:
process.on('unhandledRejection', (reason, promise) => {
  console.log('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Browser global handler:
window.addEventListener('unhandledrejection', event => {
  console.log('Unhandled Rejection:', event.reason);
});
```

---

## 7. Fetch API {#fetch-api}

### What is Fetch?

`fetch()` is a modern, Promise-based Web API for making HTTP requests. It replaces the legacy `XMLHttpRequest`.

### Syntax and Response Methods

```javascript
// GET Request
fetch('https://api.example.com/data')
  .then(response => {
    console.log(response.status); // 200, 404, 500, etc.
    console.log(response.ok);     // true if status is 200-299
    
    // You MUST parse the body!
    return response.json();       // parses JSON (returns Promise)
    // OR: return response.text(); (for plain text/HTML)
    // OR: return response.blob(); (for images/files)
  })
  .then(data => console.log(data));
```

### IMPORTANT MISTAKE: Fetch doesn't reject on HTTP errors!

Fetch only rejects on **network failures** (like no internet). If the server returns a 404 or 500 error, the Promise STILL RESOLVES. You must manually check `response.ok`.

```javascript
async function safeFetch(url) {
  const res = await fetch(url);
  
  if (!res.ok) { // Check if 4xx or 5xx
    throw new Error(`HTTP Error! Status: ${res.status}`);
  }
  
  return await res.json();
}
```

### POST Requests

```javascript
async function createPost(postData) {
  const response = await fetch('https://api.example.com/posts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Tell server it's JSON
      'Authorization': 'Bearer YOUR_TOKEN' // Auth token
    },
    body: JSON.stringify(postData) // Convert object to JSON string
  });
  return await response.json();
}
```

### Aborting Requests (AbortController)

Prevent race conditions or cancel long requests if the user navigates away.

```javascript
const controller = new AbortController();
const signal = controller.signal;

// Start request with signal
fetch('/api/data', { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === 'AbortError') {
      console.log('Fetch aborted completely');
    }
  });

// Later: Abort the request!
controller.abort(); 
```

---

## 8. AJAX & XMLHttpRequest (legacy) {#ajax}

*Note: Rarely written from scratch today, but appears in interviews.*

**AJAX (Asynchronous JavaScript and XML):** The concept of updating parts of a web page without reloading it.

```javascript
// The old way (Pre-Fetch):
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/data");

xhr.onreadystatechange = function() {
  // readyState 4 means request finished and response is ready
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      console.log(JSON.parse(xhr.responseText));
    } else {
      console.error("Error", xhr.status);
    }
  }
};

xhr.send();
```
*Why Fetch is better:* No nested callbacks, uses Promises natively, cleaner syntax.

---

## 9. WebSockets {#websockets}

### HTTP vs WebSockets

- **HTTP:** Half-duplex. Client asks, Server answers. Server *cannot* initiate contact.
- **WebSocket:** Full-duplex. Persistent, two-way connection. Server can push data to client anytime (chat apps, stock tickers, gaming).

### Implementation

```javascript
// 1. Connect (ws:// or wss:// for secure)
const socket = new WebSocket('wss://example.com/chat');

// 2. Event Listeners
socket.addEventListener('open', (event) => {
  console.log('Connected to server!');
  
  // 3. Send data
  socket.send(JSON.stringify({ type: 'hello', msg: 'Hi Server!' }));
});

// 4. Receive data
socket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('Message from server:', data);
});

socket.addEventListener('close', () => console.log('Disconnected'));
socket.addEventListener('error', (err) => console.error('WS Error:', err));
```

---

## 10. Timers and Scheduling {#timers}

### setTimeout & setInterval

```javascript
// setTimeout: Execute ONCE after delay
const timeoutId = setTimeout(() => console.log("Done"), 1000);
clearTimeout(timeoutId); // Cancels it

// setInterval: Execute REPEATEDLY every delay
let count = 0;
const intervalId = setInterval(() => {
  console.log(++count);
  if (count === 5) clearInterval(intervalId); // Stop after 5 times
}, 1000);
```

### The `setTimeout(fn, 0)` Trick

Why use a 0ms delay? Because it pushes the callback to the **Macrotask Queue**, forcing it to run *after* all currently executing synchronous code finishes.

```javascript
console.log("A");
setTimeout(() => console.log("B"), 0); 
console.log("C");
// Output: A, C, B
```

### Execution Order: Microtasks vs Macrotasks

- **Microtasks** (High Priority): Promises (`.then`, `.catch`), `queueMicrotask`, `MutationObserver`.
- **Macrotasks** (Low Priority): `setTimeout`, `setInterval`, DOM Events, network callbacks.

**Rule:** After every synchronous execution, the Event Loop empties the ENTIRE Microtask queue before taking ONE task from the Macrotask queue.

```javascript
console.log("1. Sync");

setTimeout(() => console.log("5. Macrotask (Timeout)"), 0);

Promise.resolve().then(() => console.log("3. Microtask (Promise 1)"));
queueMicrotask(() => console.log("4. Microtask (queueMicrotask)"));

console.log("2. Sync");

// OUTPUT:
// 1. Sync
// 2. Sync
// 3. Microtask (Promise 1)
// 4. Microtask (queueMicrotask)
// 5. Macrotask (Timeout)
```

---

## 11. Debouncing {#debouncing}

### What is Debouncing?

**Debouncing** ensures that a function is not called again until a certain amount of time has passed without it being called.

**Real-world analogy:** An elevator door. Every time someone steps in, the "close door" timer resets to 3 seconds. The door only closes when 3 seconds pass with NO ONE stepping in.

**Use cases:** Search bar autosuggestion (don't fetch API on every keystroke, wait until user stops typing for 500ms). Window resizing.

### Implementation from Scratch (Interview Favorite!)

```javascript
function debounce(func, delay) {
  let timeoutId; // Closure variable holds the timer
  
  return function(...args) {
    // 1. Clear previous timer if called again
    clearTimeout(timeoutId);
    
    // 2. Set new timer
    timeoutId = setTimeout(() => {
      func.apply(this, args); // Execute function with correct context
    }, delay);
  };
}

// Usage:
const searchAPI = (query) => console.log("Fetching for:", query);
const debouncedSearch = debounce(searchAPI, 500);

// User types rapidly: 'c', 'ca', 'cat' (takes < 500ms total)
debouncedSearch('c');   // Timer starts
debouncedSearch('ca');  // Timer clears, new timer starts
debouncedSearch('cat'); // Timer clears, new timer starts
// ... 500ms passes ...
// Output: "Fetching for: cat" (API called ONCE!)
```

---

## 12. Throttling {#throttling}

### What is Throttling?

**Throttling** ensures a function is called *at most* once in a specified time period, no matter how many times it's triggered.

**Real-world analogy:** A machine gun that can only fire 1 bullet per second. No matter how many times you pull the trigger, it enforces the 1-second limit.

**Use cases:** Scroll event listeners, window resize events, API rate limiting, button click spam prevention.

### Implementation from Scratch

```javascript
function throttle(func, limit) {
  let inThrottle = false; // Flag to track state
  
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args); // Execute immediately
      inThrottle = true;      // Lock it
      
      setTimeout(() => {
        inThrottle = false;   // Unlock after limit
      }, limit);
    }
  };
}

// Usage:
const logScroll = () => console.log("Scrolled!");
const throttledScroll = throttle(logScroll, 1000);

// Triggered 100 times in 3 seconds by scrolling:
window.addEventListener('scroll', throttledScroll);
// Output: "Scrolled!" logs exactly 3 times (once per second).
```

### Debounce vs Throttle Summary

| Technique | Behavior | Example |
|-----------|----------|---------|
| **Debounce** | Groups multiple sequential calls into a single call. Waits for a pause. | Search input API calls |
| **Throttle** | Guarantees a constant rate of execution. Enforces a maximum frequency. | Scroll tracking |

---

## 13. Web Storage {#web-storage}

APIs to store key-value pairs in the browser.

| Feature | `localStorage` | `sessionStorage` | Cookies | IndexedDB |
|---------|----------------|------------------|---------|-----------|
| **Lifespan** | Persistent (until cleared manually) | Until tab/window is closed | Defined expiry date | Persistent |
| **Capacity** | ~5MB | ~5MB | 4KB | 50MB+ |
| **Sent with HTTP?** | No | No | Yes (every request) | No |
| **Use case** | Theme preference, auth token (debatable) | Form data during checkout | Server-side sessions | Offline web apps, large data |

### localStorage & sessionStorage Syntax (Identical)

```javascript
// Storage only holds STRINGS!

// Save
localStorage.setItem('theme', 'dark');
localStorage.setItem('user', JSON.stringify({ name: 'Alice' })); // Serialize objects!

// Read
const theme = localStorage.getItem('theme');
const user = JSON.parse(localStorage.getItem('user')); // Parse objects!

// Remove
localStorage.removeItem('theme');

// Clear all
localStorage.clear();
```

---

## 14. JSON {#json}

### What is JSON?

JavaScript Object Notation. It's a text format for storing and transporting data. It looks like JS objects, but keys MUST be wrapped in double quotes.

### JSON.stringify()

Converts a JS object into a JSON string.

```javascript
const obj = { name: "Alice", age: 25, active: true };
const str = JSON.stringify(obj); 
// '{"name":"Alice","age":25,"active":true}'

// Formatting (Space parameter):
const prettyStr = JSON.stringify(obj, null, 2); // Indents with 2 spaces
```

### JSON.parse()

Converts a JSON string back into a JS object.

```javascript
const jsonStr = '{"name":"Alice","age":25}';
const newObj = JSON.parse(jsonStr);
```

### Limitations (Important for Deep Cloning!)

JSON cannot serialize:
- Functions
- `undefined`
- Symbols
- Circular references (throws TypeError)
- Dates are converted to strings, but `JSON.parse` won't convert them back to Date objects automatically.

```javascript
const tricky = { 
  a: undefined, 
  b: function(){}, 
  c: Symbol("id") 
};
console.log(JSON.stringify(tricky)); // "{}" (They are completely stripped out!)
```

---

## 15. Chapter Summary & Interview Prep {#summary}

### Revision Notes
- **Event Loop:** Single-threaded JS uses Web APIs for async tasks. Callbacks go to the Microtask queue (Promises) or Macrotask queue (Timers/Events). Microtasks run first.
- **Promises:** Solve callback hell. States: Pending, Fulfilled, Rejected. Chain flatly with `.then()`. Catch errors cleanly.
- **Promise.all:** Rejects immediately if ONE rejects.
- **async/await:** Syntactic sugar over Promises. Makes async code look sync. Use `try/catch`. Don't use `await` sequentially if tasks are independent (use `Promise.all`).
- **Fetch:** Returns a Promise. Does NOT reject on 404/500 errors; must check `response.ok`.
- **Debounce:** Waits for you to stop triggering before executing.
- **Throttle:** Executes at a steady, limited rate regardless of triggers.

### Cheat Sheet
```javascript
// Fetch boilerplate
const res = await fetch(url);
if (!res.ok) throw new Error("HTTP error");
const data = await res.json();

// Parallel execution
const [a, b] = await Promise.all([promiseA, promiseB]);

// Debounce concept
Wait for pause -> Execute
// Throttle concept
Execute -> Wait limit -> Ready to execute again
```

---

## Top 25 Interview Questions — Chapter 5

**Q1. Explain the Event Loop.**
*Answer:* JavaScript is single-threaded. When async code (like setTimeout or fetch) runs, it's handed off to browser Web APIs. When finished, callbacks are pushed to queues. The Event Loop constantly checks if the Call Stack is empty. If it is, it pushes tasks from the Microtask queue (Promises) until empty, then takes one task from the Macrotask queue (Timers/Events), and repeats.

**Q2. What is the difference between Microtasks and Macrotasks?**
*Answer:* Microtasks have higher priority. Promises (`.then`, `.catch`) and `queueMicrotask` create microtasks. `setTimeout`, `setInterval`, and DOM events create macrotasks. The event loop completely empties the microtask queue before running the next macrotask.

**Q3. Predict the output:**
```javascript
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);
```
*Answer:* `1, 4, 3, 2`. Sync code runs first (1, 4). Microtask queue runs next (3). Macrotask runs last (2).

**Q4. What is a Promise and what are its states?**
*Answer:* An object representing the eventual completion/failure of an async operation. States are Pending, Fulfilled, and Rejected.

**Q5. Why does fetch() not reject on a 404 error?**
*Answer:* `fetch()` only rejects on network failures (e.g., DNS lookup failure, no internet). If the server responds (even with a 500 or 404), the request completed successfully at the network level, so it resolves. You must manually check `if (!response.ok)` to throw an error.

**Q6. What is the difference between Promise.all() and Promise.allSettled()?**
*Answer:* `Promise.all()` short-circuits and rejects immediately if *any* promise rejects. `Promise.allSettled()` waits for *all* promises to finish, regardless of success or failure, returning an array of objects detailing the status of each.

**Q7. Explain Debouncing vs Throttling.**
*Answer:* Debouncing delays function execution until a certain period of inactivity has passed (e.g., wait 500ms after user stops typing to search). Throttling limits function execution to a maximum frequency (e.g., allow scroll handler to run only once every 100ms).

**Q8. What is wrong with this code and how do you fix it?**
```javascript
async function getData() {
  const users = await fetchUsers();
  const posts = await fetchPosts();
  return { users, posts };
}
```
*Answer:* It suffers from sequential blocking. `fetchPosts` doesn't start until `fetchUsers` finishes, even though they are independent. Fix using `Promise.all`: `const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);`

**Q9. Can you use `await` inside a `.forEach()` loop?**
*Answer:* No, `forEach` is not promise-aware and executes synchronously. The loop will finish before the awaited tasks complete. Instead, use a `for...of` loop for sequential execution, or `Promise.all(array.map(async () => {}))` for parallel execution.

**Q10. What happens if you don't catch a Promise rejection?**
*Answer:* It results in an "Unhandled Promise Rejection". In modern Node.js, this crashes the process. In browsers, it throws an error in the console.

---

## 5 Output Prediction Exercises

### Exercise 1
```javascript
setTimeout(() => console.log('A'), 0);
Promise.resolve().then(() => console.log('B'));
Promise.resolve().then(() => setTimeout(() => console.log('C'), 0));
console.log('D');
```
**Answer:** `D, B, A, C`. (Sync D -> Microtask B -> Macrotask A -> Macrotask C added by B runs last).

### Exercise 2
```javascript
async function test() {
  console.log(1);
  await null;
  console.log(2);
}
console.log(3);
test();
console.log(4);
```
**Answer:** `3, 1, 4, 2`. `test()` is called synchronously up to the first `await`. The code after `await` is queued as a microtask. 

### Exercise 3
```javascript
const p = new Promise((res, rej) => {
  console.log('A');
  res('B');
  console.log('C');
});
p.then(console.log);
```
**Answer:** `A, C, B`. The executor function in a Promise runs synchronously.

### Exercise 4
```javascript
Promise.resolve(1)
  .then(val => { console.log(val); return val + 1; })
  .then(val => { throw new Error('Fail'); })
  .catch(err => { console.log('Caught'); return 10; })
  .then(val => console.log(val));
```
**Answer:** `1, Caught, 10`. The chain continues after a `catch` block resolves successfully.

### Exercise 5
```javascript
let count = 0;
const interval = setInterval(() => {
  count++;
  if (count === 2) clearInterval(interval);
  console.log(count);
}, 100);
```
**Answer:** `1`, `2` (Logs 1 and 2, then stops).

---

## 5 Coding Exercises

1. **Implement `debounce` from scratch.**
2. **Implement `throttle` from scratch.**
3. **Write a function `sleep(ms)` that pauses async execution using Promises.**
   *(Solution: `const sleep = ms => new Promise(res => setTimeout(res, ms));`)*
4. **Implement your own version of `Promise.all` using standard Promises.**
5. **Fetch data from two APIs, but abort both if neither finishes within 3 seconds using `Promise.race` and `AbortController`.**

---

## 10 MCQs

**Q1.** Which queue has higher priority in the Event Loop?
- A) Macrotask Queue
- B) Microtask Queue
- C) Render Queue
- D) Call Stack

**Answer: B**

**Q2.** What keyword is used to handle rejected promises in async/await?
- A) .catch()
- B) try/catch
- C) error()
- D) throw

**Answer: B**

**Q3.** What does `Promise.race()` return?
- A) An array of results
- B) The first promise to resolve (ignoring rejections)
- C) The first promise to settle (resolve or reject)
- D) The last promise to finish

**Answer: C**

**Q4.** Why doesn't `setTimeout(fn, 0)` execute instantly?
- A) 0 is interpreted as 1000ms
- B) The Event Loop must empty the Call Stack and Microtask Queue first
- C) The browser throttles it
- D) Syntax error

**Answer: B**

**Q5.** Which Web Storage option persists data after the browser is closed?
- A) sessionStorage
- B) localStorage
- C) applicationStorage
- D) window.store

**Answer: B**

*End of Chapter 5 — Async JS is the key to performant web apps.*
