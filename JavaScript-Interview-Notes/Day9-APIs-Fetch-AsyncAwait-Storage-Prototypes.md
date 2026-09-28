# Day 9 — APIs, FETCH, ASYNC/AWAIT, STORAGE & PROTOTYPES

## 1. DAY OBJECTIVE
Master asynchronous JavaScript requests, browser storage mechanisms, and the prototype chain. These are fundamental for any frontend or full-stack interview.

## 2. COMPLETE CONCEPT NOTES

### Intro to APIs
An Application Programming Interface (API) allows different software applications to communicate with each other. In web development, we often deal with Web APIs that return JSON data.

### Fetch API Deep Dive
The Fetch API provides a JavaScript interface for accessing and manipulating parts of the protocol, such as requests and responses. It also provides a global etch() method that provides an easy, logical way to fetch resources asynchronously across the network.

**GET request:**
`js
const fetchUser = async () => {
  try {
    const res = await fetch('https://api.github.com/users/octocat');
    if (!res.ok) throw new Error(HTTP );
    const data = await res.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
};
`

**POST request:**
`js
const createUser = async () => {
  try {
    const res = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Alice', age: 25 })
    });
    const data = await res.json();
  } catch (error) {
    console.error(error);
  }
};
`
* etch does NOT reject on HTTP errors (404, 500). Must check 
es.ok or 
es.status.
* etch rejects ONLY on network failure.
* Response methods: 
es.json(), 
es.text(), 
es.blob(), 
es.arrayBuffer() — all return Promises.
* Common headers: Authorization, Content-Type, Accept.

### Promise Methods — ALL FOUR

1. **Promise.all([p1, p2, p3])**:
   - Runs in parallel
   - Resolves when ALL resolve
   - Rejects immediately if ANY rejects
   - Returns array of results

2. **Promise.allSettled([p1, p2, p3])**:
   - Runs in parallel
   - Waits for ALL to settle (fulfill or reject)
   - NEVER rejects
   - Returns array of {status: 'fulfilled', value} or {status: 'rejected', reason}

3. **Promise.race([p1, p2, p3])**:
   - Returns result of FIRST to settle (either fulfill or reject)
   - Used for timeouts

4. **Promise.any([p1, p2, p3])**:
   - Returns FIRST fulfilled
   - Rejects only if ALL reject (AggregateError)
   - Opposite of Promise.race for failures

**Comparison Table:**

| Method | Resolves when | Rejects when | Use |
|---|---|---|---|
| all | ALL fulfill | ANY rejects | Parallel, need all results |
| allSettled | ALL settle | Never | Need all, regardless of failure |
| race | FIRST settles | FIRST rejects | Timeout, fastest |
| any | FIRST fulfills | ALL reject | Try multiple, need first success |

### Async/Await — SYNTACTIC SUGAR OVER PROMISES
Async functions allow you to write promise-based code as if it were synchronous, but without blocking the execution thread.

`js
async function fetchUser(id) {
  try {
    const res = await fetch(/api/users/);
    if (!res.ok) throw new Error(HTTP );
    const user = await res.json();
    return user;
  } catch (err) {
    console.error('Error:', err);
    throw err;  // re-throw to propagate
  }
}
`

**Key rules:**
- sync function ALWAYS returns a Promise.
- wait pauses execution of current async function only (not whole thread!).
- wait can only be used inside async functions (or top-level module).
- Errors in async functions should use 	ry/catch.

**Sequential vs Parallel:**
`js
// Sequential (slower):
const user = await fetchUser();
const posts = await fetchPosts();

// Parallel (faster):
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
`

### Web Storage
**localStorage:**
- Persists until manually cleared
- Per origin (protocol + domain + port)
- ~5MB limit
- String only — must JSON.stringify/JSON.parse

`js
localStorage.setItem('user', JSON.stringify({name: 'Alice'}));
const user = JSON.parse(localStorage.getItem('user'));
localStorage.removeItem('user');
localStorage.clear();
`

**sessionStorage:**
- Cleared when tab/browser closed
- Per tab
- Same API as localStorage

### Cookies
`js
document.cookie = 'name=Alice; expires=Fri, 31 Dec 2025 23:59:59 GMT; path=/';
// Reading: document.cookie returns ALL cookies as string — must parse manually
`
Attributes: expires/max-age, path, domain, secure (HTTPS only), httpOnly (server-set, not accessible by JS), SameSite.

### Prototypes — CRITICAL INTERVIEW TOPIC
Every object in JS has an internal [[Prototype]] property (accessible via __proto__ or Object.getPrototypeOf).
Prototype chain: when property not found on object, JS looks up prototype chain.

`js
const arr = [1,2,3];
// arr → Array.prototype → Object.prototype → null

function Person(name) { this.name = name; }
Person.prototype.greet = function() { return Hi ; };
const p = new Person('Alice');
p.greet();  // found on Person.prototype, not on p itself
`

**Prototype chain lookup order:**
1. Own properties of the object
2. Object's prototype
3. Prototype's prototype
4. ... up to Object.prototype
5. null — end of chain

**Object.create(proto):**
`js
const animal = { breathe() { return 'breathing'; } };
const dog = Object.create(animal);
dog.bark = function() { return 'woof'; };
dog.breathe();  // found on animal (prototype)
`

**hasOwnProperty vs in operator:**
`js
const obj = { a: 1 };
'a' in obj;                    // true (own + inherited)
obj.hasOwnProperty('a');       // true (own only)
'toString' in obj;             // true (inherited from Object.prototype)
obj.hasOwnProperty('toString') // false
`

**instanceof:**
`js
p instanceof Person;  // true — checks prototype chain
`

**Class vs prototype:**
- ES6 classes are SYNTACTIC SUGAR over prototype-based inheritance.
- Methods defined in class body go on prototype.
- class instance properties go on the object itself.

## 3. CODE EXAMPLES (runnable ES6+)

`javascript
// Example 1: Parallel Fetching
const fetchMultiple = async () => {
    try {
        const [users, posts] = await Promise.all([
            fetch('https://jsonplaceholder.typicode.com/users').then(res => res.json()),
            fetch('https://jsonplaceholder.typicode.com/posts').then(res => res.json())
        ]);
        console.log(users.length, posts.length);
    } catch(err) {
        console.error('Failed fetching data');
    }
}
fetchMultiple();

// Example 2: Prototype implementation
function Animal(name) {
    this.name = name;
}
Animal.prototype.speak = function() {
    return ${this.name} makes a noise;
}

function Dog(name, breed) {
    Animal.call(this, name);
    this.breed = breed;
}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.speak = function() {
    return ${this.name} barks;
}
`

## 4. PRACTICAL CODING QUESTIONS

### Q1. Fetch from two endpoints in parallel using Promise.all
**Approach**: Define urls in array, map to fetch promises, pass to Promise.all.
`javascript
const urls = ['url1', 'url2'];
const promises = urls.map(url => fetch(url).then(r => r.json()));
Promise.all(promises).then(data => console.log(data));
`
**Time**: Max(T1, T2)
**Space**: O(N) where N is number of endpoints.

### Q2. Implement a timeout for fetch using Promise.race
**Approach**: Create a timeout promise that rejects after MS, race it against fetch.
`javascript
const fetchWithTimeout = (url, ms) => {
    const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), ms));
    return Promise.race([fetch(url), timeout]);
};
`

### Q3. Retry failed fetch up to 3 times using async/await
**Approach**: For loop, try block. Catch handles retry if not last iteration.
`javascript
const fetchRetry = async (url, retries = 3) => {
    for (let i=0; i<retries; i++) {
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error('Status not ok');
            return await res.json();
        } catch (err) {
            if (i === retries - 1) throw err;
        }
    }
}
`

### Q4. Create a simple prototype chain using Object.create
**Approach**: Define parent obj, create child with Object.create(parent).
`javascript
const parent = { type: 'Parent', show() { console.log(this.type) } };
const child = Object.create(parent);
child.type = 'Child';
`

### Q5. Implement Promise.all manually
**Approach**: Return new Promise, maintain count and results array. Resolve when count == length.
`javascript
function myPromiseAll(promises) {
    return new Promise((resolve, reject) => {
        let results = [];
        let completed = 0;
        if(promises.length === 0) resolve(results);
        promises.forEach((p, index) => {
            Promise.resolve(p).then(res => {
                results[index] = res;
                completed++;
                if (completed === promises.length) resolve(results);
            }).catch(reject);
        });
    });
}
`

### Q6. Create a storage wrapper class using localStorage
**Approach**: Class with getter, setter, remover methods integrating JSON parsing.
`javascript
class StorageWrapper {
    static get(key) { return JSON.parse(localStorage.getItem(key)); }
    static set(key, val) { localStorage.setItem(key, JSON.stringify(val)); }
    static remove(key) { localStorage.removeItem(key); }
}
`

## 5. OUTPUT-BASED QUESTIONS

**1. Promise.all with one rejection**
`js
Promise.all([Promise.resolve(1), Promise.reject(2), Promise.resolve(3)])
  .then(console.log)
  .catch(console.log);
`
**Answer**: 2
**Explanation**: Promise.all rejects immediately upon the first rejection.

**2. Promise.allSettled output format**
`js
Promise.allSettled([Promise.resolve(1), Promise.reject(2)])
  .then(console.log);
`
**Answer**: [{status: 'fulfilled', value: 1}, {status: 'rejected', reason: 2}]
**Explanation**: Waits for all, returns object format indicating status for each.

**3. async function return value**
`js
async function test() { return 1; }
console.log(test());
`
**Answer**: Promise {<fulfilled>: 1}
**Explanation**: Async functions always return a Promise, implicitly resolving returned value.

**4. Sequential vs parallel timing**
`js
async function run() {
  console.time('seq');
  await new Promise(r => setTimeout(r, 1000));
  await new Promise(r => setTimeout(r, 1000));
  console.timeEnd('seq');
}
`
**Answer**: seq: ~2000ms
**Explanation**: Sequential awaits pause execution one after the other.

**5. localStorage JSON parse for missing key**
`js
const data = JSON.parse(localStorage.getItem('missing_key'));
console.log(data);
`
**Answer**: null
**Explanation**: getItem returns null if key missing. JSON.parse(null) is null.

**6. Prototype chain lookup**
`js
const a = {};
const b = Object.create(a);
b.val = 1;
a.val = 2;
console.log(b.val);
`
**Answer**: 1
**Explanation**: Engine finds 'val' on 'b' directly before checking prototype 'a'.

**7. hasOwnProperty vs in operator**
`js
const p = { name: 'A' };
const c = Object.create(p);
console.log('name' in c, c.hasOwnProperty('name'));
`
**Answer**: true, false
**Explanation**: 'in' checks prototype chain, 'hasOwnProperty' only checks the object itself.

**8. instanceof check**
`js
function F() {}
const obj = new F();
console.log(obj instanceof F, obj instanceof Object);
`
**Answer**: true, true
**Explanation**: obj's prototype chain is F.prototype -> Object.prototype -> null.

**9. Object.create prototype chain**
`js
const a = Object.create(null);
console.log(a.toString);
`
**Answer**: undefined
**Explanation**: Object.create(null) creates an object with no prototype, not even Object.prototype, hence no toString.

**10. Promise.race first resolve vs reject**
`js
Promise.race([
  new Promise(r => setTimeout(r, 100, 'A')),
  new Promise((_, r) => setTimeout(r, 50, 'B'))
]).then(console.log).catch(console.error);
`
**Answer**: 'B' (logged as error)
**Explanation**: Rejects after 50ms, beating the resolve at 100ms.

## 6. DEBUGGING QUESTIONS

**Bug 1: Unhandled fetch error**
`js
const getData = async () => {
    const res = await fetch('wrong-url');
    const data = await res.json();
    console.log(data);
}
`
**What's wrong**: etch only rejects on network errors. A 404/500 won't be caught by a standard catch block around it.
**Correct**:
`js
const getData = async () => {
    try {
        const res = await fetch('wrong-url');
        if (!res.ok) throw new Error('Bad response');
        const data = await res.json();
    } catch(err) { console.error(err); }
}
`

**Bug 2: Mutating Prototype incorrectly**
`js
function Car() {}
Car.prototype = { wheels: 4 };
const c = new Car();
console.log(c.constructor === Car); // false
`
**What's wrong**: Overwriting .prototype with a new object loses the .constructor property.
**Correct**:
`js
Car.prototype.wheels = 4;
// or
Car.prototype = { wheels: 4, constructor: Car };
`

## 7. INTERVIEW QUESTIONS

- **What is the difference between Promise.all and Promise.allSettled?**
  *Promise.all rejects immediately if one fails. Promise.allSettled waits for all to complete regardless of success or failure.*
- **What is Promise.any? When would you use it?**
  *Returns the first fulfilled promise. Useful when fetching from multiple identical endpoints and you just want the fastest successful one.*
- **What does async always return?**
  *A Promise.*
- **What does await do to the event loop?**
  *It pauses the execution of the async function and yields control back to the event loop to run other microtasks/macrotasks.*
- **How do you run multiple async operations in parallel with async/await?**
  *Wrap them in Promise.all() and await the result.*
- **When does fetch reject?**
  *Only on network errors or CORS failures, never on HTTP error statuses like 404 or 500.*
- **How do you handle HTTP errors with fetch?**
  *By checking the 
esponse.ok property and throwing an error if it is false.*
- **What is the difference between localStorage and sessionStorage?**
  *localStorage persists until manually cleared. sessionStorage clears when the tab is closed.*
- **What are cookies? What is httpOnly?**
  *Cookies are small data pieces sent with requests. httpOnly means they can't be accessed via client-side JavaScript, improving security.*
- **What is the prototype chain?**
  *A mechanism by which objects inherit properties and methods from other objects.*
- **What is the difference between __proto__ and prototype?**
  *prototype is a property on constructor functions used to build __proto__ of instances. __proto__ is the actual reference to the prototype on any object.*
- **What does Object.create do?**
  *Creates a new object using an existing object as the prototype of the newly created object.*
- **What is the difference between hasOwnProperty and the in operator?**
  *in checks the object and its prototype chain. hasOwnProperty checks only the object itself.*
- **How does instanceof work?**
  *It checks if the prototype property of a constructor appears anywhere in the prototype chain of an object.*
- **Why are classes in JavaScript called 'syntactic sugar'?**
  *Because under the hood, they still use the exact same prototype-based inheritance model that pre-ES6 constructor functions used.*

## 8. ⭐ MUST KNOW FOR MOCK
- Manually implementing Promise.all
- Writing robust etch calls with error handling
- Demonstrating the prototype chain inheritance visually

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Forgetting 
es.ok check in fetch
- Assuming wait blocks the main thread (it doesn't, just the async function scope)
- Confusing .prototype (on functions) with __proto__ (on instances)

## 10. NIGHT REVISION CHECKLIST
- [ ] Review Fetch API error handling
- [ ] Memorize Promise methods (all, allSettled, race, any)
- [ ] Understand async/await execution order
- [ ] Practice Storage methods
- [ ] Trace a prototype chain to 
ull
- [ ] Code manual Promise.all implementation





















































































































































































































































































































































































































































































































