# Day 10 — CLOSURES, CALL/APPLY/BIND, ADVANCED FETCH

## 1. DAY OBJECTIVE
Master Closures (the most commonly asked JS topic), function borrowing with call/apply/bind, and complex fetch scenarios (retries, timeouts, AbortController).

## 2. COMPLETE CONCEPT NOTES

### Closures — ONE OF THE MOST ASKED JS CONCEPTS
**Definition:** A closure is a function that remembers its outer scope even after the outer function has returned.

`js
function makeCounter() {
  let count = 0;  // count is closed over
  return function() {
    count++;         // still has access to count
    return count;
  };
}
const counter = makeCounter();
console.log(counter());  // 1
console.log(counter());  // 2
console.log(counter());  // 3
// count is private — cannot access from outside!
`

**Why closures exist:** Lexical scoping — functions access variables where they are DEFINED, not where they are CALLED.

**Practical uses:**
1. **Data privacy / encapsulation:**
`js
function createBankAccount(initial) {
  let balance = initial;  // private
  return {
    deposit(amount) { balance += amount; },
    withdraw(amount) { 
      if (amount > balance) throw new Error('Insufficient');
      balance -= amount;
    },
    getBalance() { return balance; }
  };
}
`

2. **Function factories:**
`js
function multiplier(factor) {
  return (num) => num * factor;  // closes over factor
}
const double = multiplier(2);
const triple = multiplier(3);
`

3. **Memoization:**
`js
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
`

4. **Module pattern (before ES modules):**
`js
const myModule = (function() {
  let private = 'secret';
  return {
    getPrivate() { return private; }
  };
})();
`

**Classic closure bug in loops:**
`js
// BUG:
const fns = [];
for (var i = 0; i < 3; i++) {
  fns.push(function() { return i; });  // all close over same i
}
fns[0]();  // 3, not 0!

// Fix 1: use let
for (let i = 0; i < 3; i++) {
  fns.push(function() { return i; });  // each iteration has its own i
}

// Fix 2: IIFE
for (var i = 0; i < 3; i++) {
  fns.push((function(j) { return function() { return j; }; })(i));
}
`

### Call, Apply, Bind — CRITICAL
All three explicitly set 	his for a function.

**call(thisArg, arg1, arg2, ...):**
- Calls function immediately
- Arguments passed individually
`js
function greet(greeting, punct) {
  return ${greeting}, ;
}
const obj = { name: 'Alice' };
greet.call(obj, 'Hello', '!');  // 'Hello, Alice!'
`

**apply(thisArg, [argsArray]):**
- Calls function immediately
- Arguments as ARRAY
`js
greet.apply(obj, ['Hello', '!']);  // 'Hello, Alice!'
// Classic use: Math.max(...array) — old way: Math.max.apply(null, arr)
`

**bind(thisArg, arg1, ...):**
- Does NOT call immediately
- Returns NEW function with 'this' permanently bound
- Can partially apply arguments (partial application/currying)
`js
const boundGreet = greet.bind(obj, 'Hi');  // partial application
boundGreet('!');  // 'Hi, Alice!'
`

**Table: call vs apply vs bind**
| Feature | call | apply | bind |
|---|---|---|---|
| Invokes immediately | Yes | Yes | No |
| Args format | Individual | Array | Individual |
| Returns | Result | Result | New function |
| Main use | Borrow method | Array args | Fix this for later |

### Advanced Fetch — Error Handling & Retries

**Proper error handling:**
`js
async function safeFetch(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const error = new Error(HTTP Error: );
    error.status = res.status;
    throw error;
  }
  return res.json();
}
`

**Retry logic:**
`js
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      return await safeFetch(url);
    } catch (err) {
      if (attempt === retries) throw err;  // last attempt: give up
      console.log(Attempt  failed. Retrying in ms...);
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2;  // exponential backoff
    }
  }
}
`

**Timeout with Promise.race:**
`js
function fetchWithTimeout(url, timeout = 5000) {
  const fetchPromise = fetch(url);
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Request timed out')), timeout)
  );
  return Promise.race([fetchPromise, timeoutPromise]);
}
`

**AbortController:**
`js
const controller = new AbortController();
const { signal } = controller;

fetch('/api/data', { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === 'AbortError') console.log('Request cancelled');
  });

controller.abort();  // cancel the request
`

## 3. CODE EXAMPLES (runnable ES6+)

`javascript
// Closures in Event Listeners
function attachEvent() {
    let count = 0;
    document.getElementById('btn').addEventListener('click', function() {
        console.log(Clicked  times);
    });
}

// Bind in React/Classes
class Widget {
    constructor() {
        this.value = 42;
        this.handleClick = this.handleClick.bind(this);
    }
    handleClick() {
        console.log(this.value);
    }
}
`

## 4. PRACTICAL CODING QUESTIONS

### Q1. Implement a memoize function using closure
**Approach**: Return function that maintains a cache object. Check cache before calling.
`javascript
function memoize(fn) {
    const cache = {};
    return function(...args) {
        const key = JSON.stringify(args);
        if (key in cache) return cache[key];
        const res = fn.apply(this, args);
        cache[key] = res;
        return res;
    }
}
`

### Q2. Implement Function.prototype.bind manually
**Approach**: Return function that calls apply.
`javascript
Function.prototype.myBind = function(context, ...args1) {
    const fn = this;
    return function(...args2) {
        return fn.apply(context, [...args1, ...args2]);
    }
}
`

### Q3. Create a counter with increment/decrement/reset using closure (no class)
**Approach**: IIFE or factory returning an object with methods.
`javascript
function createCounter() {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        reset: () => { count = 0; return count; }
    }
}
`

### Q4. Implement fetchWithRetry with exponential backoff
**Approach**: See Advanced Fetch notes.

### Q5. Implement curry function using closure
**Approach**: Recursively collect arguments until required length is met.
`javascript
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        } else {
            return function(...args2) {
                return curried.apply(this, args.concat(args2));
            }
        }
    }
}
`

### Q6. Implement partial application using bind
**Approach**: Bind args upfront.
`javascript
const add = (a, b) => a + b;
const addFive = add.bind(null, 5);
console.log(addFive(10)); // 15
`

## 5. OUTPUT-BASED QUESTIONS

**1. Classic closure loop bug (var vs let)**
`js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
`
**Answer**: 3, 3, 3
**Explanation**: ar is function-scoped. By the time timeout runs, i is 3.

**2. Counter closure: what does each call return**
`js
function counter() {
    let x = 0;
    return () => ++x;
}
const c1 = counter();
const c2 = counter();
console.log(c1(), c1(), c2());
`
**Answer**: 1, 2, 1
**Explanation**: Each counter() creates an independent closure environment.

**3. greet.call vs greet.apply**
`js
function sayHi(a, b) { console.log(this.name, a, b); }
sayHi.call({name: 'A'}, 1, 2);
sayHi.apply({name: 'B'}, [1, 2]);
`
**Answer**: A 1 2, B 1 2

**4. bind partial application**
`js
const f = (x, y) => x * y;
const f2 = f.bind(null, 2);
console.log(f2(5));
`
**Answer**: 10

**5. Closure data privacy**
Can you access private variable from outside? No.

**6. Memoized function**
How many times does fn run? Only once for unique inputs.

**7. What does bind return?**
A new function with bound context.

**8. Function borrowing with call**
`js
const args = [1,2,3];
console.log(Math.max.apply(null, args));
`
**Answer**: 3

**9. fetchWithRetry**
On 3 failures, fetch is called exactly 3 times.

**10. AbortController**
Throws a DOMException with 
ame as AbortError.

## 6. DEBUGGING QUESTIONS

**Bug 1: Losing context**
`js
const user = {
    name: 'Alice',
    greet() { console.log(this.name); }
};
setTimeout(user.greet, 100); // logs undefined
`
**Correct**: setTimeout(user.greet.bind(user), 100); or setTimeout(() => user.greet(), 100);

## 7. INTERVIEW QUESTIONS

- **What is a closure? Give a real-world example.**
  *A function plus its lexical environment. Example: Data privacy like bank balance.*
- **How does a closure maintain access to outer scope after function returns?**
  *Through a hidden [[Environment]] reference to the lexical scope in memory, preventing garbage collection.*
- **What is the classic closure bug with var in loops? How do you fix it?**
  *Callbacks inside loops with ar read the final iterated value. Fix: use let or an IIFE.*
- **What are practical use cases for closures?**
  *Memoization, data privacy, currying, module pattern.*
- **What is the module pattern and how does closure enable it?**
  *IIFE returning public methods that close over private variables.*
- **What is the difference between call, apply, and bind?**
  *call passes comma-separated args, pply passes an array, ind returns a new function.*
- **What does bind return?**
  *A newly bound function.*
- **How would you implement bind manually?**
  *Return a closure that invokes the original function via pply with the bound context and args.*
- **What is partial application? How does bind enable it?**
  *Applying some arguments to a function beforehand. ind lets you pass these preset args.*
- **How do you borrow a method from one object and use it on another?**
  *Using .call() or .apply().*
- **What is the difference between call and apply? When would you prefer apply?**
  *Prefer pply when you already have an array of arguments.*
- **How do you handle HTTP errors in fetch?**
  *Checking 
esponse.ok.*
- **What is exponential backoff?**
  *Increasing delay multiplicatively between retries to prevent overwhelming a failing server.*
- **What is AbortController and when would you use it?**
  *To cancel pending etch requests, e.g., when a user navigates away from a page before data loads.*
- **How do you implement a timeout for a fetch request?**
  *Racing it against a setTimeout Promise.*
- **What is the difference between retry and timeout?**
  *Retry attempts request again. Timeout cancels it if taking too long.*
- **What is memoization? Implement it.**
  *Caching function results.*
- **What is currying? How is it related to closures?**
  *Translating (a,b) to (a)(b). Closures store the previously passed arguments.*
- **If you use bind in a class method as an event listener, what does it solve?**
  *Keeps 	his pointing to the class instance instead of the DOM element.*
- **What is Function.prototype.call.bind used for?**
  *Creates a standalone version of .call() that can be invoked safely.*

## 8. ⭐ MUST KNOW FOR MOCK
- Explaining closures with code.
- Manually implementing bind.

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Confusing arrow functions' 	his behavior (they ignore call/apply/bind).
- Forgetting to handle AbortError uniquely.

## 10. NIGHT REVISION CHECKLIST
- [ ] Understand Closure scope chains
- [ ] Memorize call vs apply vs bind differences
- [ ] Fix loop closure bugs
- [ ] Code a polyfill for bind
- [ ] Write a retry fetch wrapper

## 🎯 COMPLETE JAVASCRIPT INTERVIEW MASTER CHECKLIST

### Top 10 Must-Know Concepts for ANY JavaScript Interview:
1. Closures (definition + examples + loop bug)
2. 	his keyword (5 rules)
3. Promises + async/await + event loop
4. Prototype chain
5. var/let/const + hoisting + TDZ
6. == vs === + type coercion
7. call/apply/bind
8. Event loop + microtask vs macrotask queue
9. Shallow vs deep copy
10. Array HOFs (map, filter, reduce)

### Output Questions You WILL See in Any Interview:
- setTimeout order with promises
- var in for loop closure bug
- typeof null
- [] + [] and [] + {}
- [1,2,3].map(parseInt)
- 	his in various contexts

### Questions Guaranteed for MERN/Frontend Interviews:
- Explain the event loop
- What are closures?
- Promise vs async/await
- Explain 'this'
- What is prototype?
- How does fetch work? How do you handle errors?

























































































































































































































































































































































































































































































































































































































