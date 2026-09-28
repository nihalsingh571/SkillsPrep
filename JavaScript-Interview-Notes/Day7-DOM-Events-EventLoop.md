# Day 7 — DOM, EVENTS & EVENT LOOP

## 1. DAY OBJECTIVE
The objective of today's revision is to master the interaction between JavaScript and the browser. You will learn how to select, manipulate, and modify the Document Object Model (DOM), handle user interactions via DOM events, and understand the critical concept of the JavaScript Event Loop. We will also touch upon the basics of the Fetch API to make network requests. By the end of this day, you should be perfectly comfortable answering interview questions related to `NodeList` vs `HTMLCollection`, event bubbling, and predicting the exact execution order of synchronous and asynchronous JavaScript code.

---

## 2. COMPLETE CONCEPT NOTES

### DOM (Document Object Model)
The DOM is a structural, tree-like representation of the HTML document stored in memory by the browser. 
- Every HTML tag becomes a "node" in this tree.
- The `document` object is the global entry point to this tree.
- JavaScript can interact with this tree to read, change, add, or delete elements dynamically.

**Selecting Elements:**
```js
// Selects the first element with the given ID. Returns null if not found.
const title = document.getElementById('main-title');

// Selects the first element matching the CSS selector. Returns null if not found.
const firstButton = document.querySelector('.btn-primary');

// Selects ALL elements matching the CSS selector. 
// Returns a NodeList (static in this case).
const allButtons = document.querySelectorAll('button');

// Selects all elements with a specific class name.
// Returns an HTMLCollection (live).
const activeItems = document.getElementsByClassName('active');

// Selects all elements with a specific tag name.
// Returns an HTMLCollection (live).
const allDivs = document.getElementsByTagName('div');
```

**Difference: NodeList vs HTMLCollection vs Array:**
- **HTMLCollection:** It is "live", meaning if the DOM changes, the collection updates automatically. It does NOT have built-in array methods like `forEach()`, `map()`, or `filter()`.
- **NodeList:** It can be static (returned by `querySelectorAll`) or live (returned by `childNodes`). It comes with a `forEach()` method built-in.
- **Array:** Neither NodeList nor HTMLCollection are true arrays. To use methods like `map` or `filter`, you must convert them:
```js
// Converting to an Array
const nodeArray = Array.from(allButtons);
const nodeArray2 = [...allButtons]; // spread operator works too!
```

**Manipulating DOM Elements:**
Once you have selected an element, you can manipulate its content, styling, and attributes.
```js
const el = document.querySelector('#btn');

// Changing Text & Content
el.textContent = 'Click me';  // Safest. Returns/sets raw text.
el.innerText = 'Visible text';  // Respects CSS (doesn't show hidden text).
el.innerHTML = '<b>Bold</b>';  // Parses HTML strings — Warning: XSS risk!

// Changing Styles (Inline styles)
el.style.color = 'red';
el.style.backgroundColor = 'blue'; // Notice camelCase for CSS properties

// Manipulating Classes
el.classList.add('active', 'highlight');
el.classList.remove('active');
el.classList.toggle('active'); // Adds if missing, removes if present
const hasClass = el.classList.contains('active');  // returns boolean true/false

// Manipulating Attributes
el.setAttribute('disabled', 'true');
const idValue = el.getAttribute('data-id');
el.removeAttribute('disabled');
```

**Creating, Appending, and Removing Elements:**
```js
// 1. Create a new element in memory
const div = document.createElement('div');
div.textContent = 'Hello World';
div.classList.add('greeting');

// 2. Add it to the DOM
document.body.appendChild(div); // Appends as the last child
document.body.append(div, 'Some text', document.createElement('span')); // Can append multiple and strings

document.body.prepend(div); // Appends as the first child

// Insert before a specific element
const parent = document.getElementById('container');
const newEl = document.createElement('p');
const referenceEl = document.getElementById('reference');
parent.insertBefore(newEl, referenceEl);

// 3. Removing elements
newEl.remove(); // Removes itself (modern approach)
parent.removeChild(div); // Older approach, requires parent reference
```

---

### DOM Events
Events are actions or occurrences that happen in the system you are programming, which the system tells you about so you can respond to them.

**addEventListener:**
```js
const btn = document.querySelector('button');

// syntax: element.addEventListener(event, handler, options)
btn.addEventListener('click', function(e) {
  console.log('Button clicked!');
}, { capture: false, once: true, passive: true });
```
- `once: true` -> The listener will automatically remove itself after firing once.
- `passive: true` -> Improves scrolling performance, promises you won't call `preventDefault()`.

**removeEventListener:**
CRITICAL: To remove an event listener, you MUST pass the exact same function reference in memory.
```js
const el = document.querySelector('#my-el');

const fn = () => console.log('clicked');
el.addEventListener('click', fn);
el.removeEventListener('click', fn);  // ✅ WORKS

// This DOES NOT WORK:
el.addEventListener('click', () => console.log('hi'));
el.removeEventListener('click', () => console.log('hi')); // ❌ Fails. Different function in memory!
```

**The Event Object (`e`):**
Passed automatically to your handler function.
- `e.target`: The actual element that triggered the event (the deepest element clicked).
- `e.currentTarget`: The element the event listener is attached to.
- `e.preventDefault()`: Stops the browser's default behavior (e.g., stops a form submission from refreshing the page, stops a link from navigating).
- `e.stopPropagation()`: Stops the event from bubbling further up the DOM tree.

**Event Bubbling vs Capturing:**
By default, events "bubble".
1. **Capturing Phase:** The event goes down from the `window` to the `document`, root element, and through ancestors down to the target.
2. **Target Phase:** The event hits the target element.
3. **Bubbling Phase:** The event bubbles back up from the target through its ancestors.

To listen in the capturing phase, pass `true` as the third argument:
```js
el.addEventListener('click', handler, true);
```

**Event Delegation:**
Instead of attaching 100 event listeners to 100 `<li>` items, attach ONE listener to the parent `<ul>` and use `e.target` to figure out which `<li>` was clicked.
```js
document.querySelector('#list').addEventListener('click', (e) => {
  if (e.target.matches('li')) {
    console.log('List item clicked:', e.target.textContent);
  }
});
```
*Advantages:* Saves memory (fewer listeners), works dynamically for items added later.

**DOMContentLoaded vs load:**
- `DOMContentLoaded`: Fires when the HTML is completely parsed and the DOM tree is built. Does NOT wait for stylesheets, images, or iframes to finish loading.
- `load`: Fires on the `window` object when the whole page has loaded, including all dependent resources like stylesheets and images.

---

### JavaScript Event Loop — CRITICAL INTERVIEW TOPIC
JavaScript is single-threaded. It has one Call Stack and can do one thing at a time. It doesn't wait around for slow things like network requests. It delegates them to the browser (Web APIs).

**The Components:**
1. **Call Stack:** Executes synchronous code. LIFO (Last In, First Out).
2. **Web APIs:** Browser features (DOM, setTimeout, fetch, setInterval). Not part of the V8 engine itself.
3. **Callback Queue (Macrotask Queue):** Where `setTimeout`, `setInterval`, and DOM event callbacks wait.
4. **Microtask Queue:** Where `Promise.then/catch/finally` and `queueMicrotask` wait. **Higher priority than the Callback Queue.**
5. **Event Loop:** The mechanism that constantly checks if the Call Stack is empty. If it is, it pushes the first task from the Microtask Queue to the Call Stack. If the Microtask Queue is empty, it pushes the first task from the Callback Queue.

**Execution Order Rule of Thumb:**
1. Execute all Synchronous code.
2. Check and drain the entire Microtask Queue (Promises). If microtasks add more microtasks, execute those too.
3. Execute ONE task from the Macrotask Queue (Callback Queue).
4. Render UI (if needed).
5. Repeat.

**Classic Example:**
```js
console.log('1. Sync Start');

setTimeout(() => {
  console.log('2. Macrotask (setTimeout)');
}, 0);

Promise.resolve().then(() => {
  console.log('3. Microtask (Promise)');
});

console.log('4. Sync End');

// Order of execution:
// 1. Sync Start
// 4. Sync End
// 3. Microtask (Promise)
// 2. Macrotask (setTimeout)
```

**Nested Promises vs setTimeout:**
```js
setTimeout(() => console.log('timeout'), 0);
Promise.resolve()
  .then(() => { 
    console.log('p1'); 
    return Promise.resolve(); 
  })
  .then(() => console.log('p2'));

// Output: p1, p2, timeout
// Explanation: The event loop drains the ENTIRE microtask queue before touching the macrotask queue.
```

---

### Fetch API (intro)
The modern way to make HTTP network requests in JS, replacing `XMLHttpRequest`.
```js
fetch('https://jsonplaceholder.typicode.com/users/1')
  .then(response => {
    // Check if response is successful
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // response.json() returns a PROMISE!
    return response.json(); 
  })
  .then(userData => {
    console.log('User data:', userData);
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
```
*Note:* A `fetch()` promise only rejects on network failure (like offline). It does NOT reject on HTTP errors like 404 or 500. You must manually check `response.ok`.

---

## 3. CODE EXAMPLES (runnable ES6+)

### Example 1: Robust Event Delegation
```js
// HTML assumed:
// <ul id="todo-list">
//   <li data-id="1">Buy groceries <button class="delete-btn">X</button></li>
//   <li data-id="2">Walk dog <button class="delete-btn">X</button></li>
// </ul>

const todoList = document.getElementById('todo-list');

todoList.addEventListener('click', (event) => {
  // Check if what we clicked is a delete button
  if (event.target.classList.contains('delete-btn')) {
    // e.target is the button. The parent node is the <li>
    const li = event.target.closest('li');
    const todoId = li.getAttribute('data-id');
    
    console.log(`Deleting todo with ID: ${todoId}`);
    li.remove(); // Remove from DOM
  }
  
  // Notice we used .closest('li') instead of parentNode
  // closest() goes up the DOM tree looking for a matching selector
});
```

### Example 2: Event Loop Complex Visualization
```js
console.log('A');

setTimeout(() => {
  console.log('B');
  Promise.resolve().then(() => console.log('C'));
}, 0);

Promise.resolve().then(() => {
  console.log('D');
  setTimeout(() => console.log('E'), 0);
});

console.log('F');

/* 
Execution trace:
1. Sync: log 'A'
2. Macrotask queued (B)
3. Microtask queued (D)
4. Sync: log 'F'
-- Stack Empty --
5. Drain Microtasks: run (D) -> logs 'D' -> Queues Macrotask (E)
-- Microtasks Empty --
6. Run 1 Macrotask: run (B) -> logs 'B' -> Queues Microtask (C)
-- Stack Empty --
7. Drain Microtasks: run (C) -> logs 'C'
-- Microtasks Empty --
8. Run 1 Macrotask: run (E) -> logs 'E'

Final Output: A, F, D, B, C, E
*/
```

---

## 4. PRACTICAL CODING QUESTIONS

### Q1. Implement event delegation for a dynamically generated list
**Approach:** Instead of adding listeners to new elements, add one listener to the parent container. Use `matches` or `classList.contains`.
**Solution:**
```js
const container = document.getElementById('container');
const btn = document.getElementById('add-btn');

// Adding dynamically
btn.addEventListener('click', () => {
  const div = document.createElement('div');
  div.className = 'dynamic-item';
  div.textContent = 'I am new!';
  container.appendChild(div);
});

// Event Delegation
container.addEventListener('click', (e) => {
  if (e.target.classList.contains('dynamic-item')) {
    console.log('Dynamic item clicked:', e.target.textContent);
    e.target.style.backgroundColor = 'yellow';
  }
});
```
**Time Complexity:** O(1) per click (excluding DOM traversal which is fast).
**Space Complexity:** O(1) memory for the single event listener.

### Q2. Create a debounce function using setTimeout
**Approach:** Debouncing limits the rate at which a function fires. It resets a timer every time the function is called.
**Solution:**
```js
function debounce(func, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId); // Clear the previous timer
    timerId = setTimeout(() => {
      func.apply(this, args); // Execute the function after delay
    }, delay);
  };
}

// Usage
const handleResize = debounce(() => {
  console.log('Resized window!');
}, 500);

window.addEventListener('resize', handleResize);
```
**Complexity:** O(1) Time, O(1) Space per invocation.

### Q3. Create a throttle function
**Approach:** Throttling ensures a function is called AT MOST once in a specified time period.
**Solution:**
```js
function throttle(func, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false; // Release the throttle lock after limit
      }, limit);
    }
  };
}

const handleScroll = throttle(() => {
  console.log('Scroll event processed!');
}, 1000);
window.addEventListener('scroll', handleScroll);
```

### Q4. Predict output of complex event loop code
(See Output-Based Questions section)

### Q5. Add/remove items in a todo list using DOM manipulation only
**Solution:**
```js
const form = document.querySelector('#todo-form');
const input = document.querySelector('#todo-input');
const list = document.querySelector('#todo-list');

form.addEventListener('submit', (e) => {
  e.preventDefault(); // Prevent page reload
  
  const val = input.value.trim();
  if (!val) return;
  
  const li = document.createElement('li');
  li.textContent = val;
  
  const btn = document.createElement('button');
  btn.textContent = 'Remove';
  btn.addEventListener('click', () => {
    li.remove();
  });
  
  li.appendChild(btn);
  list.appendChild(li);
  
  input.value = ''; // clear input
});
```

### Q6. Attach and properly remove an event listener
**Solution:**
```js
const btn = document.querySelector('.btn');

// Define named function
function handleClick(e) {
  console.log('Clicked');
  // Remove itself after one click
  btn.removeEventListener('click', handleClick);
}

btn.addEventListener('click', handleClick);
```

---

## 5. OUTPUT-BASED QUESTIONS

**Q1. Event loop order: sync + promise + setTimeout**
```js
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
```
**Answer:** 1, 4, 3, 2
**Explanation:** `1` and `4` are synchronous. The `Promise.then` callback goes to the microtask queue (`3`). The `setTimeout` callback goes to the macrotask queue (`2`). Microtasks run before macrotasks.

**Q2. Nested promises execution order**
```js
Promise.resolve().then(() => console.log(1));
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => {
  console.log(3);
  Promise.resolve().then(() => console.log(4));
});
```
**Answer:** 1, 3, 4, 2
**Explanation:** Sync is empty. Microtasks: (log 1) and (log 3, queue 4). After logging 1 and 3, microtask queue gets a new task (log 4). The event loop processes it immediately. Finally, the macrotask (log 2) runs.

**Q3. setTimeout(fn,0) vs Promise.resolve().then(fn)**
They don't execute at the same time. Promises (microtasks) have higher priority and will always execute before timeouts (macrotasks) scheduled at the same time.

**Q4. e.target vs e.currentTarget**
```html
<div id="parent" onclick="console.log(event.target.id, event.currentTarget.id)">
  <button id="child">Click</button>
</div>
```
*Clicking the button:*
**Answer:** Logs: `child parent`
**Explanation:** `target` is the actual element clicked (the button). `currentTarget` is the element where the event listener is attached (the div).

**Q5. What does removeEventListener with anonymous function do?**
```js
btn.addEventListener('click', () => console.log('hi'));
btn.removeEventListener('click', () => console.log('hi'));
```
**Answer:** It does NOTHING.
**Explanation:** `removeEventListener` requires the exact same reference in memory. An anonymous arrow function creates a new reference. The listener remains attached.

**Q6. Multiple setTimeout(fn,0) order**
```js
setTimeout(() => console.log('A'), 0);
setTimeout(() => console.log('B'), 0);
```
**Answer:** A, B
**Explanation:** Macrotasks are executed in the order they are pushed into the queue (FIFO).

**Q7. DOMContentLoaded vs load which fires first**
**Answer:** `DOMContentLoaded` fires first.
**Explanation:** `DOMContentLoaded` fires as soon as the HTML is parsed. `load` waits for CSS, images, and iframes to finish downloading.

**Q8. NodeList vs HTMLCollection behavior**
```js
const list1 = document.getElementsByTagName('div'); // HTMLCollection
const list2 = document.querySelectorAll('div');     // NodeList
document.body.appendChild(document.createElement('div'));
console.log(list1.length === list2.length);
```
**Answer:** `false`
**Explanation:** HTMLCollection is live, so `list1` automatically updates its length. `querySelectorAll` returns a static NodeList, so `list2` remains the same length as when it was queried.

**Q9. innerHTML vs textContent XSS**
```js
el.innerHTML = '<script>alert("Hacked")</script>'; // Vulnerable?
el.textContent = '<script>alert("Hacked")</script>'; // Vulnerable?
```
**Answer:** `innerHTML` executes HTML (though modern HTML5 blocks direct script injection this way, `img onerror` still works for XSS). `textContent` safely renders it as literal text strings `<script>...` on the screen.

**Q10. Event bubbling order: child click on nested structure**
```html
<div id="grandparent">
  <div id="parent">
    <button id="child">Click</button>
  </div>
</div>
<!-- All have click listeners logging their ID -->
```
**Answer:** `child`, `parent`, `grandparent`
**Explanation:** Events bubble upwards from the deepest nested element (target) to the outermost ancestors.

---

## 6. DEBUGGING QUESTIONS

**Q1. Why is this event listener not removing?**
*Buggy Code:*
```js
const el = document.getElementById('my-el');
el.addEventListener('scroll', function() { console.log('scrolling'); });
// later
el.removeEventListener('scroll', function() { console.log('scrolling'); });
```
*Wrong:* The listener keeps firing.
*Correct:* Extract the function to a variable.
```js
const handleScroll = () => console.log('scrolling');
el.addEventListener('scroll', handleScroll);
el.removeEventListener('scroll', handleScroll);
```
*Why:* Functions are reference types. Two identical-looking inline functions point to different memory addresses.

**Q2. Why is innerHTML destroying my event listeners?**
*Buggy Code:*
```js
container.innerHTML += '<div>New item</div>';
```
*Wrong:* All previously existing elements inside `container` that had event listeners lose them!
*Correct:* Use `container.insertAdjacentHTML('beforeend', '<div>New item</div>');` OR `appendChild`.
*Why:* `innerHTML +=` serializes the DOM to a string, adds the new string, and re-parses EVERYTHING, creating entirely new DOM nodes and destroying old ones (and their attached listeners).

**Q3. Array methods failing on NodeList**
*Buggy Code:*
```js
const divs = document.querySelectorAll('div');
const mappedDivs = divs.map(div => div.textContent);
```
*Wrong:* TypeError: divs.map is not a function.
*Correct:* `const mappedDivs = Array.from(divs).map(div => div.textContent);`
*Why:* NodeLists are array-like, but they don't inherit from `Array.prototype`.

**Q4. e.preventDefault() not working for passive scroll listeners**
*Buggy Code:*
```js
window.addEventListener('touchstart', (e) => {
  e.preventDefault(); // Console throws an error
}, { passive: true });
```
*Wrong:* Cannot prevent default inside a passive event listener.
*Correct:* Remove `{ passive: true }` if you absolutely must prevent default.
*Why:* `passive: true` is a performance optimization where you promise the browser you WON'T call `preventDefault`, allowing the browser to scroll immediately without waiting for JS.

---

## 7. INTERVIEW QUESTIONS

**1. What is the DOM? (Basic)**
The Document Object Model (DOM) is an object-oriented, hierarchical tree representation of an HTML document. The browser creates this structure so that programming languages like JavaScript can interact with, read, and manipulate the page structure, style, and content dynamically.

**2. What is the event loop? (Frequently Asked)**
JavaScript is single-threaded, meaning it can only execute one task at a time on the Call Stack. The Event Loop is a continuous process that monitors the Call Stack and the task queues (Microtask and Macrotask). If the Call Stack is empty, it pushes the first available task from the Microtask Queue to the Call Stack. Once the Microtask queue is empty, it processes tasks from the Macrotask Queue. This is what enables asynchronous, non-blocking behavior in JS.

**3. What is the difference between the microtask queue and the callback queue (macrotask)? (Advanced)**
The microtask queue has higher priority. It holds callbacks from Promises (e.g., `.then`, `.catch`, `.finally`), `MutationObserver`, and `queueMicrotask`. The macrotask (callback) queue holds callbacks from `setTimeout`, `setInterval`, `setImmediate`, and DOM events. The event loop drains the *entire* microtask queue before it moves on to process even a *single* macrotask.

**4. Why do Promise callbacks run before setTimeout callbacks? (Intermediate)**
Because Promises are added to the Microtask queue, while `setTimeout` callbacks go to the Macrotask queue. The Event Loop specification dictates that the microtask queue is completely drained before moving to the next macrotask.

**5. What is event bubbling and capturing? (Intermediate)**
They are phases of event propagation in the DOM. Capturing (Trickling) happens first: the event travels from the `window` down through ancestors to the target element. Bubbling happens next: the event travels from the target element back up through its ancestors. By default, `addEventListener` listens in the bubbling phase.

**6. What is event delegation? Why is it useful? (Frequently Asked)**
Event delegation is a pattern where a single event listener is attached to a parent element to handle events triggered by its children, taking advantage of event bubbling. 
*Why useful:* It drastically reduces memory usage (one listener instead of thousands) and gracefully handles elements dynamically added to the DOM after page load.

**7. What is the difference between e.target and e.currentTarget? (Basic)**
`e.target` refers to the exact DOM element that triggered the event (the one the user actually clicked). `e.currentTarget` refers to the element that the event listener is actively attached to.

**8. What is preventDefault and stopPropagation? (Intermediate)**
`e.preventDefault()` prevents the browser's native default behavior for an event (e.g., stopping a form from submitting/refreshing the page). `e.stopPropagation()` stops the event from continuing to bubble up or trickle down the DOM tree, preventing ancestors/descendants from receiving the event.

**9. How do you remove an event listener correctly? (Basic)**
By using `removeEventListener` and passing the exact same event type and the *exact same function reference* that was passed to `addEventListener`.

**10. What is innerHTML vs textContent vs innerText? (Scenario-based)**
- `innerHTML`: Returns/sets the HTML markup inside an element. Vulnerable to XSS.
- `textContent`: Returns/sets the raw text content of an element and all descendants. It ignores CSS (returns hidden text). Fast and safe.
- `innerText`: Returns/sets the visible text content. It triggers a reflow to calculate CSS and won't return text hidden via `display: none`. Slower but useful for reading exactly what the user sees.

**11. What is DOMContentLoaded vs load? (Intermediate)**
`DOMContentLoaded` triggers when the initial HTML document has been completely loaded and parsed, without waiting for stylesheets, images, and subframes. `load` triggers when the entire page and all its dependent resources (images, CSS) have finished loading.

**12. What is debouncing vs throttling? (Advanced)**
Both are techniques to limit the rate at which a function is executed.
- *Debouncing:* Delays function execution until after a certain period of inactivity. If the event fires again before the period ends, the timer resets. (e.g., Search autocomplete).
- *Throttling:* Ensures the function executes at a regular interval, executing at most once every *X* milliseconds, regardless of how many times the event fires. (e.g., Window resizing, scrolling).

**13. What does fetch return? (Basic)**
`fetch` returns a Promise that resolves to a `Response` object representing the response to the request.

**14. Does fetch reject on 404? Why not? (Frequently Asked)**
No, a `fetch()` promise does *not* reject on HTTP error statuses (like 404 or 500). It only rejects on network failures (e.g., loss of internet connectivity, CORS errors). To handle HTTP errors, you must manually check the `response.ok` property or the `response.status` code.

**15. What is the call stack? (Basic)**
The call stack is a LIFO (Last In, First Out) data structure used by the JavaScript engine to keep track of function execution. When a function is called, it's pushed onto the stack. When it returns, it's popped off the stack.

---

## 8. ⭐ MUST KNOW FOR MOCK
- Draw out the Event Loop architecture (Call stack, Web API, Queues).
- Write a Debounce function from memory.
- Explain the output of mixed `setTimeout` and `Promise` chaining clearly.
- Write a perfect event delegation implementation.

---

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Assuming `HTMLCollection` and `NodeList` are Arrays and calling `.map()` on them directly.
- Trying to remove an event listener that used an inline anonymous arrow function.
- Saying `fetch()` throws an error on `404 Not Found`. (It doesn't!).
- Thinking `setTimeout(fn, 0)` executes immediately. (It yields to the call stack and microtasks first).

---

## 10. NIGHT REVISION CHECKLIST
- [ ] Can I define the DOM and its core methods?
- [ ] Do I understand the difference between `querySelector` and `getElementsByClassName`?
- [ ] Do I know how to convert a `NodeList` to an Array?
- [ ] Can I explain `textContent` vs `innerText` vs `innerHTML`?
- [ ] Can I dynamically create, append, and remove elements?
- [ ] Do I understand capturing vs bubbling phases?
- [ ] Can I write an Event Delegation script?
- [ ] Do I know the difference between `e.target` and `e.currentTarget`?
- [ ] Can I explain the Event Loop to a 5-year-old?
- [ ] Can I differentiate between the Microtask Queue and Macrotask Queue?
- [ ] Do I know the exact execution order of sync code, Promises, and timeouts?
- [ ] Can I write a `fetch` request handling `response.ok`?
- [ ] Can I code Debounce from scratch?
- [ ] Can I code Throttle from scratch?
- [ ] Have I reviewed the common traps section?
