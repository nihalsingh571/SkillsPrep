# Chapter 6: The DOM & Events — Complete Mastery Guide

> **"The DOM is the bridge between your HTML and JavaScript. Events are the heartbeat of every interactive web application."**

---

## Table of Contents

1. [The DOM (Document Object Model)](#1-the-dom)
2. [DOM Selection Methods](#2-dom-selection-methods)
3. [DOM Traversal](#3-dom-traversal)
4. [DOM Manipulation](#4-dom-manipulation)
5. [Events](#5-events)
6. [Event Bubbling](#6-event-bubbling)
7. [Event Capturing](#7-event-capturing)
8. [Event Delegation](#8-event-delegation)
9. [Custom Events](#9-custom-events)
10. [Form Events & Validation](#10-form-events--validation)
11. [Intersection Observer API](#11-intersection-observer-api)
12. [Mutation Observer](#12-mutation-observer)
13. [Resize Observer](#13-resize-observer)
14. [Performance Considerations](#14-performance-considerations)
15. [Chapter Summary & Master Review](#15-chapter-summary--master-review)

---

# 1. The DOM

## 1.1 What is the DOM?

**Definition:**  
The **Document Object Model (DOM)** is a programming interface for web documents. It represents the page as a **tree of objects** (nodes), allowing JavaScript to read and manipulate the structure, style, and content of a web page.

**Why does it exist?**  
HTML is just static markup — a text file. The browser needs a living, in-memory representation that JavaScript can interact with. The DOM is that representation. Without the DOM, JavaScript would have no way to "see" or "touch" the web page.

**Real-World Analogy:**  
Imagine a restaurant menu (HTML file). The menu itself is just paper — you can read it, but you can't change it. Now imagine that menu is entered into a computer system (the DOM). The computer system lets the waiter (JavaScript):
- **Read** what items are available
- **Add** new daily specials
- **Remove** sold-out items
- **Update** prices in real time

The computer system is the DOM — a live, interactive representation of the original document.

---

## 1.2 DOM Tree Structure

When a browser parses HTML, it builds a **tree structure** in memory. Every HTML element, text, attribute, and comment becomes a **node** in this tree.

```
HTML Source Code:
-----------------
<!DOCTYPE html>
<html>
  <head>
    <title>My Page</title>
  </head>
  <body>
    <h1 id="heading">Hello World</h1>
    <p class="intro">Welcome!</p>
    <!-- A comment -->
  </body>
</html>

DOM Tree (ASCII Diagram):
--------------------------

          [Document]
               |
          [html]  ← Element Node (root)
         /      \
      [head]   [body]
        |       /    \       \
    [title] [h1]    [p]   [Comment]
        |     |  \    |  \
    "My   [id]  "Hello" [class] "Welcome!"
    Page" attr  World"  attr
              (text node)    (text node)
```

**Detailed Node Type Diagram:**

```
┌─────────────────────────────────────────────────────────┐
│                    Node Types                           │
├──────────────────┬──────────────────────────────────────┤
│ Node Type        │ Example                              │
├──────────────────┼──────────────────────────────────────┤
│ Element Node     │ <div>, <p>, <h1>, <span>             │
│ Text Node        │ "Hello World" (text inside elements) │
│ Attribute Node   │ id="heading", class="intro"          │
│ Comment Node     │ <!-- This is a comment -->           │
│ Document Node    │ The root document object             │
│ DocumentFragment │ Lightweight container (no parent)    │
└──────────────────┴──────────────────────────────────────┘
```

---

## 1.3 Node Types Explained

### Element Nodes
The most common node type. Every HTML tag creates an element node.
```javascript
// <div class="box"> creates an Element Node
// nodeType === 1
console.log(document.body.nodeType); // 1 (Element)
```

### Text Nodes
Any text content inside an element. Even whitespace (spaces, newlines) creates text nodes.
```javascript
// "Hello" inside <p>Hello</p> is a Text Node
// nodeType === 3
const p = document.querySelector('p');
console.log(p.firstChild.nodeType); // 3 (Text)
```

### Comment Nodes
HTML comments become nodes in the DOM.
```javascript
// <!-- comment --> is a Comment Node
// nodeType === 8
```

### Attribute Nodes
In modern DOM (Level 2+), attributes are accessible via Element methods, not as separate traversable nodes.

---

## 1.4 The `document` Object

**What is it?**  
`document` is the entry point to the DOM. It represents the entire HTML page and is a property of `window`. Every DOM operation starts from `document`.

```javascript
// document properties
console.log(document.title);         // "My Page" - page title
console.log(document.URL);           // full URL of the page
console.log(document.domain);        // domain name
console.log(document.documentElement); // <html> element
console.log(document.head);          // <head> element
console.log(document.body);          // <body> element
console.log(document.cookie);        // cookies
console.log(document.readyState);    // "loading", "interactive", "complete"
console.log(document.characterSet);  // "UTF-8"
console.log(document.forms);         // all forms in document
console.log(document.images);        // all images in document
console.log(document.links);         // all anchor elements with href
```

---

## 1.5 The `window` Object

**What is it?**  
`window` is the global object in the browser. It represents the browser window/tab. The `document` object is a property of `window`.

```
window
  ├── document  ← the DOM
  ├── console
  ├── location  ← URL control
  ├── history   ← browser history
  ├── navigator ← browser/device info
  ├── localStorage
  ├── sessionStorage
  ├── setTimeout / setInterval
  ├── fetch
  └── alert / confirm / prompt
```

```javascript
// window methods
window.alert("Hello!");            // alert dialog
window.confirm("Are you sure?");   // confirmation dialog (returns true/false)
window.prompt("Enter name:");      // input dialog

// window properties
console.log(window.innerWidth);   // viewport width in pixels
console.log(window.innerHeight);  // viewport height in pixels
console.log(window.outerWidth);   // total window width
console.log(window.scrollX);      // horizontal scroll position
console.log(window.scrollY);      // vertical scroll position

// Note: In browser, window is global — these are equivalent:
alert("Hi");           // same as window.alert("Hi")
document.body;         // same as window.document.body
```

---

## 1.6 Relationship: HTML → Parser → DOM Tree

```
┌──────────────────────────────────────────────────────────────┐
│                  Browser Rendering Pipeline                  │
│                                                              │
│  HTML File                                                   │
│  ─────────────────────────────────────────────────────────  │
│  <html><body><h1>Hello</h1></body></html>                   │
│         │                                                    │
│         ▼                                                    │
│  [HTML Parser]  ←── encounters tags one by one              │
│         │                                                    │
│         ▼                                                    │
│  [DOM Tree in Memory]                                        │
│   Document                                                   │
│   └── html                                                   │
│       └── body                                               │
│           └── h1                                             │
│               └── "Hello" (text node)                        │
│         │                                                    │
│         ▼                                                    │
│  [CSSOM - CSS Object Model]  ←── from CSS files             │
│         │                                                    │
│         ▼                                                    │
│  [Render Tree] = DOM + CSSOM                                 │
│         │                                                    │
│         ▼                                                    │
│  [Layout] ─── calculate positions                           │
│         │                                                    │
│         ▼                                                    │
│  [Paint] ─── draw pixels on screen                          │
└──────────────────────────────────────────────────────────────┘
```

**Key point:** JavaScript can run during parsing and modify the DOM. This is why `<script>` tags at the bottom of `<body>` (or using `defer`) is best practice — the DOM is fully built before JS runs.

---

## 1.7 Live DOM vs Static NodeList

This is a critically important distinction often missed by developers.

| Feature | Live Collection | Static Collection |
|---------|----------------|-------------------|
| Return type | `HTMLCollection` | `NodeList` (from querySelectorAll) |
| Auto-updates | ✅ Yes — reflects DOM changes | ❌ No — snapshot at time of call |
| Methods that return it | `getElementsByClassName`, `getElementsByTagName`, `children` | `querySelectorAll`, `childNodes` |
| Performance | Slightly slower (must re-evaluate) | Slightly faster (cached snapshot) |

```javascript
// LIVE collection example
const liveList = document.getElementsByClassName('item'); // HTMLCollection
console.log(liveList.length); // 2

// Add a new element with class "item"
const newEl = document.createElement('div');
newEl.className = 'item';
document.body.appendChild(newEl);

console.log(liveList.length); // 3 ← automatically updated! (LIVE)

// STATIC collection example
const staticList = document.querySelectorAll('.item'); // NodeList
console.log(staticList.length); // 3

const another = document.createElement('div');
another.className = 'item';
document.body.appendChild(another);

console.log(staticList.length); // still 3 ← NOT updated (STATIC)
```

> **⚠️ Common Mistake:** Modifying a live collection while iterating it can cause infinite loops or skipped elements. Always convert to Array first: `Array.from(liveList)`.

---

### Interview Questions — Section 1

**Basic:**
1. What is the DOM?
2. What is the difference between `document` and `window`?
3. What are the different types of nodes in the DOM?

**Intermediate:**
4. What is the difference between a live HTMLCollection and a static NodeList?
5. Explain the browser rendering pipeline from HTML to pixels.
6. What does `document.readyState` tell you?

**Advanced:**
7. Why does modifying a live HTMLCollection during iteration cause bugs?
8. How does the parser build the DOM differently when it encounters a `<script>` tag?
9. What is the difference between the render tree and the DOM tree?

**Tricky:**
10. Is `childNodes` live or static? What about `children`?
    - Answer: Both `childNodes` (NodeList) and `children` (HTMLCollection) are **LIVE** in this case. `querySelectorAll` returns a static NodeList.

**MCQ:**
1. What is the `nodeType` of an Element node?
   - a) 1 ✅  b) 2  c) 3  d) 8

2. Which is a live collection?
   - a) `querySelectorAll()` b) `getElementsByTagName()` ✅ c) Array.from() result d) NodeList

---

# 2. DOM Selection Methods

## 2.1 `document.getElementById()`

**What is it?**  
Selects a single element by its unique `id` attribute. Fastest DOM selector.

**Real-World Analogy:** Finding a person by their unique passport number — guaranteed to find exactly one person (or none).

```javascript
// HTML: <div id="hero-section">Welcome!</div>

const hero = document.getElementById('hero-section');
// Returns: the Element node, or null if not found

console.log(hero);              // <div id="hero-section">Welcome!</div>
console.log(hero.id);          // "hero-section"
console.log(hero.tagName);     // "DIV"
console.log(hero.textContent); // "Welcome!"

// If not found:
const missing = document.getElementById('nonexistent');
console.log(missing); // null

// Always check for null before using:
if (hero) {
  hero.style.color = 'blue';
}
```

---

## 2.2 `document.getElementsByClassName()`

**What is it?**  
Returns a **live HTMLCollection** of all elements that have a given CSS class name.

```javascript
// HTML:
// <p class="note highlight">First</p>
// <p class="note">Second</p>
// <span class="note">Third</span>

// Single class
const notes = document.getElementsByClassName('note');
console.log(notes.length); // 3
console.log(notes[0]);     // first <p>

// Multiple classes (elements must have BOTH classes)
const highlighted = document.getElementsByClassName('note highlight');
console.log(highlighted.length); // 1

// Iterate safely (convert to array first for safety)
Array.from(notes).forEach(el => {
  el.style.border = '1px solid red';
});
```

---

## 2.3 `document.getElementsByTagName()`

**What is it?**  
Returns a **live HTMLCollection** of all elements with the specified tag name.

```javascript
// Get all paragraphs
const paragraphs = document.getElementsByTagName('p');
console.log(paragraphs.length);

// Get ALL elements (wildcard)
const allElements = document.getElementsByTagName('*');
console.log(allElements.length); // every element on page

// Case-insensitive for HTML (but case-sensitive for SVG/XML)
const divs = document.getElementsByTagName('div');
const DIVS = document.getElementsByTagName('DIV');
// Both work in HTML documents

// Scope to a subtree:
const container = document.getElementById('myContainer');
const innerPs = container.getElementsByTagName('p'); // only inside container
```

---

## 2.4 `document.querySelector()`

**What is it?**  
Returns the **first** Element that matches any valid CSS selector. Returns `null` if not found.

**Real-World Analogy:** A powerful search engine that understands complex queries (like CSS selectors) but only returns the first result.

```javascript
// By ID (equivalent to getElementById but less performant)
const byId = document.querySelector('#hero');

// By class
const byClass = document.querySelector('.note');     // first .note

// By tag
const byTag = document.querySelector('p');           // first <p>

// Combined selectors (CSS selector syntax)
const complex = document.querySelector('div.card > p.title'); // p.title direct child of div.card

// Attribute selectors
const input = document.querySelector('input[type="email"]');
const link = document.querySelector('a[href^="https"]');  // href starts with https

// Pseudo-selectors
const firstItem = document.querySelector('li:first-child');
const lastItem = document.querySelector('li:last-child');
const oddItems = document.querySelector('li:nth-child(odd)');

// Scoped queries (search within an element)
const container = document.querySelector('.container');
const innerBtn = container.querySelector('button'); // only inside .container
```

---

## 2.5 `document.querySelectorAll()`

**What is it?**  
Returns a **static NodeList** of ALL elements matching the CSS selector.

```javascript
// Get all list items
const items = document.querySelectorAll('li');

// items is a NodeList — iterable but NOT an Array
console.log(items instanceof NodeList); // true
console.log(items instanceof Array);    // false

// NodeList supports forEach directly (unlike HTMLCollection)
items.forEach((item, index) => {
  console.log(`Item ${index}: ${item.textContent}`);
});

// Convert to array for full Array methods (map, filter, reduce, etc.)
const itemArray = Array.from(items);
// OR:
const itemArray2 = [...items]; // spread operator

// Complex selectors
const highlights = document.querySelectorAll('.card:not(.disabled) > .title');
const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');

// Multiple selectors (comma-separated — like CSS)
const headings = document.querySelectorAll('h1, h2, h3'); // all headings
```

---

## 2.6 Comparison Table

```
┌─────────────────────────────────┬──────────────────┬─────────────┬──────────────────┐
│ Method                          │ Returns          │ Live?       │ Selector Type    │
├─────────────────────────────────┼──────────────────┼─────────────┼──────────────────┤
│ getElementById('id')            │ Element or null  │ N/A         │ ID only          │
│ getElementsByClassName('cls')   │ HTMLCollection   │ ✅ LIVE     │ Class only       │
│ getElementsByTagName('tag')     │ HTMLCollection   │ ✅ LIVE     │ Tag name only    │
│ querySelector('selector')       │ Element or null  │ N/A         │ Any CSS selector │
│ querySelectorAll('selector')    │ NodeList         │ ❌ STATIC   │ Any CSS selector │
└─────────────────────────────────┴──────────────────┴─────────────┴──────────────────┘

Performance Ranking (fastest to slowest):
1. getElementById       — O(1), direct hash lookup
2. getElementsByTagName — O(n), browser-optimized
3. getElementsByClassName — O(n), browser-optimized
4. querySelector        — O(n), CSS engine traversal
5. querySelectorAll     — O(n*m), most flexible but slowest
```

---

## 2.7 CSS Selector Syntax in querySelector

```javascript
// ─────────────── BASIC SELECTORS ───────────────
document.querySelector('p')           // tag name
document.querySelector('#myId')       // ID
document.querySelector('.myClass')    // class
document.querySelector('*')           // any element

// ─────────────── COMBINATOR SELECTORS ───────────────
document.querySelector('div p')       // descendant (any level deep)
document.querySelector('div > p')     // direct child only
document.querySelector('h2 + p')      // immediately adjacent sibling
document.querySelector('h2 ~ p')      // any subsequent sibling

// ─────────────── ATTRIBUTE SELECTORS ───────────────
document.querySelector('[href]')              // has href attribute
document.querySelector('[href="url"]')        // exact value
document.querySelector('[href^="https"]')     // starts with
document.querySelector('[href$=".pdf"]')      // ends with
document.querySelector('[href*="google"]')    // contains

// ─────────────── PSEUDO-CLASS SELECTORS ───────────────
document.querySelector('li:first-child')
document.querySelector('li:last-child')
document.querySelector('li:nth-child(2)')
document.querySelector('li:nth-child(even)')
document.querySelector('p:not(.special)')
document.querySelector('input:focus')
document.querySelector('input:checked')
document.querySelector('input:disabled')
document.querySelector(':hover')  // currently hovered element
```

---

### Interview Questions — Section 2

**Basic:**
1. What does `querySelector` return if no match is found?
2. What is the difference between `querySelector` and `querySelectorAll`?

**Intermediate:**
3. Why is `getElementById` the fastest DOM selector?
4. How does querySelectorAll differ from getElementsByClassName in terms of live/static?
5. Can you call `querySelector` on a specific element (not just document)?

**Advanced:**
6. Write a CSS selector to select all checked checkboxes inside a form with class "settings".
   ```javascript
   document.querySelectorAll('form.settings input[type="checkbox"]:checked');
   ```
7. What is the performance implication of using `querySelectorAll('*')` in a large DOM?

**Tricky Output Question:**
```javascript
// HTML: <div id="box" class="box"></div>

const a = document.getElementById('box');
const b = document.querySelector('#box');
const c = document.querySelector('.box');

console.log(a === b); // true — same DOM node
console.log(b === c); // true — same DOM node
console.log(a === c); // true — same DOM node
```
What is the output? **All true** — they all reference the same object in memory.

**MCQ:**
1. Which method returns a static NodeList?
   - a) getElementsByClassName  b) getElementsByTagName  c) querySelectorAll ✅  d) children

2. `document.querySelector('.menu li:nth-child(3)')` selects:
   - a) The 3rd .menu element  b) The 3rd li anywhere  c) The 3rd li inside .menu ✅  d) Error

---

# 3. DOM Traversal

## 3.1 Why DOM Traversal?

Instead of always selecting elements from scratch using `getElementById` or `querySelector`, we can **navigate the DOM tree** relative to an already-selected element. This is faster and more maintainable.

**Real-World Analogy:** You're at the library. Instead of going back to the entrance and searching the entire catalog for the next book, you just reach to the shelf next to you.

---

## 3.2 Parent Traversal

```javascript
const child = document.querySelector('.child');

// parentNode — returns the parent Node (could be any node type)
const parent1 = child.parentNode;

// parentElement — returns the parent Element (only if parent is Element)
const parent2 = child.parentElement;

// They are almost always the same, except:
// document.documentElement.parentNode === document (Document node)
// document.documentElement.parentElement === null (Document is not an Element)

console.log(document.documentElement.parentNode);    // #document
console.log(document.documentElement.parentElement); // null ← key difference
```

---

## 3.3 Children Traversal

```javascript
// HTML:
// <ul id="list">
//   text node (whitespace)
//   <li>Item 1</li>
//   text node (whitespace)
//   <li>Item 2</li>
//   text node (whitespace)
// </ul>

const list = document.getElementById('list');

// childNodes — ALL child nodes including text nodes and comments
console.log(list.childNodes);
// NodeList [text, li, text, li, text] — length 5 (includes whitespace text nodes!)

// children — ONLY Element children (no text, no comment nodes)
console.log(list.children);
// HTMLCollection [li, li] — length 2 ✅ what you usually want

// firstChild — first node (might be text node with whitespace)
console.log(list.firstChild);          // #text (whitespace) ← tricky!

// firstElementChild — first ELEMENT child (ignores text/comment nodes)
console.log(list.firstElementChild);   // <li>Item 1</li> ✅

// lastChild — last node (might be text node with whitespace)
console.log(list.lastChild);           // #text (whitespace) ← tricky!

// lastElementChild — last ELEMENT child
console.log(list.lastElementChild);    // <li>Item 2</li> ✅

// childElementCount — number of element children
console.log(list.childElementCount);   // 2
```

> **⚠️ Common Mistake:** Using `firstChild` expecting to get the first element, but getting a whitespace text node instead. **Always prefer `firstElementChild`** unless you specifically need text nodes.

---

## 3.4 Sibling Traversal

```javascript
// HTML:
// <nav>
//   <a href="#">Home</a>
//   <a href="#" class="active">About</a>
//   <a href="#">Contact</a>
// </nav>

const activeLink = document.querySelector('.active');

// nextSibling — next node (includes text nodes!)
console.log(activeLink.nextSibling);          // #text (whitespace)

// nextElementSibling — next ELEMENT sibling
console.log(activeLink.nextElementSibling);   // <a href="#">Contact</a> ✅

// previousSibling — previous node (includes text nodes!)
console.log(activeLink.previousSibling);       // #text (whitespace)

// previousElementSibling — previous ELEMENT sibling
console.log(activeLink.previousElementSibling); // <a href="#">Home</a> ✅
```

---

## 3.5 `closest()` Method

**What is it?**  
Traverses **upward** through parent chain and returns the first ancestor matching the CSS selector.

**Real-World Analogy:** You're inside a nested set of boxes. `closest()` checks each box you're inside — starting from yourself and going outward — until it finds one painted the color you want.

```javascript
// HTML structure:
// <table>
//   <tbody>
//     <tr>
//       <td><button class="delete-btn">Delete</button></td>
//     </tr>
//   </tbody>
// </table>

const btn = document.querySelector('.delete-btn');

// Find the nearest ancestor <tr>
const row = btn.closest('tr');
console.log(row); // <tr>...</tr>

// Find the nearest ancestor that has class "card"
const card = btn.closest('.card');

// Returns null if no match found going up
const form = btn.closest('form'); // null (no form is ancestor)

// The element itself is also checked first
const self = btn.closest('button'); // returns btn itself!

// Practical use: event delegation
document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-action="delete"]');
  if (btn) {
    // User clicked something inside a delete button
    const item = btn.closest('.list-item');
    item.remove();
  }
});
```

---

## 3.6 `matches()` Method

**What is it?**  
Tests if an element matches a CSS selector. Returns `true` or `false`.

```javascript
const el = document.querySelector('p');

console.log(el.matches('p'));           // true
console.log(el.matches('.highlight'));  // true if has class highlight
console.log(el.matches('div'));         // false

// Practical use in event delegation:
document.addEventListener('click', function(e) {
  if (e.target.matches('button.submit')) {
    // Only runs if clicked element is a <button class="submit">
    handleSubmit();
  }
});
```

---

## 3.7 `contains()` Method

**What is it?**  
Tests if a node is a descendant (at any depth) of another node.

```javascript
const parent = document.querySelector('.container');
const child = document.querySelector('.item');

console.log(parent.contains(child));    // true if child is inside parent
console.log(child.contains(parent));    // false
console.log(parent.contains(parent));   // true (a node contains itself!)

// Use case: click outside to close a dropdown
document.addEventListener('click', function(e) {
  const dropdown = document.querySelector('.dropdown');
  if (!dropdown.contains(e.target)) {
    // Clicked outside the dropdown — close it
    dropdown.classList.remove('open');
  }
});
```

---

### Traversal Cheat Sheet

```
                    parentNode / parentElement
                           ↑
                         [ul]
                      ↙        ↘
[li] ←previousElementSibling→ [li] ←nextElementSibling→ [li]
  ↕ children / childNodes / firstElementChild / lastElementChild
[text content inside li]
```

---

# 4. DOM Manipulation

## 4.1 Creating Elements

```javascript
// Step 1: Create the element
const newDiv = document.createElement('div');
// Creates a <div> element NOT yet attached to the document

// Step 2: Configure it
newDiv.id = 'myNewDiv';
newDiv.className = 'card featured';
newDiv.textContent = 'Hello, I am new!';

// Step 3: Attach to document (see inserting methods below)
document.body.appendChild(newDiv);

// Creating multiple elements
function createCard(title, description) {
  const card = document.createElement('div');      // wrapper
  card.className = 'card';

  const h2 = document.createElement('h2');         // title
  h2.textContent = title;

  const p = document.createElement('p');           // description
  p.textContent = description;

  card.appendChild(h2);  // add title to card
  card.appendChild(p);   // add description to card

  return card; // return completed card
}

const myCard = createCard('React Fundamentals', 'Learn React from scratch!');
document.querySelector('.cards-container').appendChild(myCard);
```

---

## 4.2 Setting Content: innerHTML vs innerText vs textContent

**This is a critical distinction — especially for security.**

```javascript
const div = document.querySelector('#output');

// ─────────────── innerHTML ───────────────
// Gets/sets HTML markup as a string
// PARSES the string as HTML — creates real DOM nodes
div.innerHTML = '<strong>Bold text</strong> and <em>italic</em>';
// Result: The string is rendered as formatted HTML ✅

// ⚠️ SECURITY RISK: innerHTML with user input = XSS attack!
const userInput = '<img src="x" onerror="alert(\'HACKED!\')">'; // malicious
div.innerHTML = userInput; // DANGEROUS — executes the onerror script!

// ─────────────── innerText ───────────────
// Gets/sets the VISIBLE text (respects CSS)
// Triggers reflow (reads layout info)
div.innerText = '<strong>Bold text</strong>';
// Result: displays literal string "<strong>Bold text</strong>" as text

// innerText reads only VISIBLE text (hidden elements excluded)
// Normalizes whitespace like the browser would display it

// ─────────────── textContent ───────────────
// Gets/sets ALL text content (ignores HTML tags, ignores CSS)
// Does NOT trigger reflow — faster for reading
div.textContent = '<strong>Bold text</strong>';
// Result: displays literal string (same as innerText for SETTING)

// Key differences when READING:
// <div style="display:none">hidden</div>
// textContent: returns "hidden" (includes hidden text)
// innerText: returns "" (respects CSS visibility)

// <div>Line 1<br>Line 2</div>
// textContent: "Line 1Line 2" (no line breaks — raw text only)
// innerText: "Line 1\nLine 2" (respects visual line breaks)
```

**Comparison Table:**

```
┌──────────────────┬───────────────────────┬──────────────────────────┬───────────────────┐
│ Property         │ Parses HTML?          │ CSS-aware?               │ XSS Risk?         │
├──────────────────┼───────────────────────┼──────────────────────────┼───────────────────┤
│ innerHTML        │ ✅ Yes                │ N/A (sets HTML)          │ ✅ HIGH RISK      │
│ innerText        │ ❌ No                 │ ✅ Yes (triggers reflow) │ ❌ Safe           │
│ textContent      │ ❌ No                 │ ❌ No (faster)           │ ❌ Safe           │
└──────────────────┴───────────────────────┴──────────────────────────┴───────────────────┘

Rule of thumb:
- Use textContent when inserting plain text (safest, fastest)
- Use innerHTML only for trusted/sanitized HTML templates
- Never use innerHTML with raw user input
```

---

## 4.3 Attributes

```javascript
const link = document.querySelector('a');

// getAttribute — reads any attribute (even non-standard)
const href = link.getAttribute('href');   // e.g., "/about"
const cls = link.getAttribute('class');   // "nav-link active"

// setAttribute — sets any attribute
link.setAttribute('href', 'https://example.com');
link.setAttribute('target', '_blank');
link.setAttribute('aria-label', 'Visit Example');

// removeAttribute — removes the attribute entirely
link.removeAttribute('target');

// hasAttribute — check if attribute exists
console.log(link.hasAttribute('href'));     // true
console.log(link.hasAttribute('disabled')); // false

// Direct property access (cleaner for standard attributes)
link.href = 'https://example.com'; // sets the resolved URL
link.id = 'myLink';
link.className = 'nav-link'; // replaces ALL classes

// Note: getAttribute('href') vs element.href
// <a href="/about"> 
// link.getAttribute('href') → "/about"   (raw attribute value)
// link.href               → "http://site.com/about" (absolute URL resolved)
```

---

## 4.4 Dataset (data-*) Attributes

**What is it?**  
HTML5 allows custom attributes prefixed with `data-`. JavaScript accesses these via the `dataset` property.

**Why:** Allows embedding data in HTML elements without polluting standard attributes or using hidden fields.

```javascript
// HTML: <div data-user-id="42" data-role="admin" data-is-active="true">...</div>

const div = document.querySelector('div');

// Reading — note: kebab-case becomes camelCase in JS
console.log(div.dataset.userId);    // "42" (string!)
console.log(div.dataset.role);      // "admin"
console.log(div.dataset.isActive);  // "true" (string, not boolean!)

// Writing
div.dataset.userId = '99';          // sets data-user-id="99" in HTML
div.dataset.newProp = 'hello';      // creates data-new-prop="hello"

// Deleting
delete div.dataset.role;            // removes data-role attribute

// Conversion needed for non-strings:
const id = parseInt(div.dataset.userId);    // convert to number
const active = div.dataset.isActive === 'true'; // convert to boolean

// Common use case: event delegation with data attributes
document.getElementById('product-list').addEventListener('click', function(e) {
  const card = e.target.closest('.product-card');
  if (card) {
    const productId = card.dataset.productId;
    const category = card.dataset.category;
    addToCart(productId, category);
  }
});
```

---

## 4.5 CSS Styles

### Direct Style Property
```javascript
const box = document.querySelector('.box');

// Setting individual CSS properties (camelCase for hyphenated names!)
box.style.color = 'red';
box.style.backgroundColor = 'blue';   // background-color → backgroundColor
box.style.fontSize = '18px';          // font-size → fontSize
box.style.marginTop = '20px';         // margin-top → marginTop
box.style.borderRadius = '8px';
box.style.display = 'flex';
box.style.transform = 'translateX(100px)';

// Reading computed styles (includes CSS file styles):
const computed = window.getComputedStyle(box);
console.log(computed.color);         // "rgb(255, 0, 0)"
console.log(computed.fontSize);      // "18px"
// getComputedStyle gives the ACTUAL applied value, not just inline styles

// Removing inline style:
box.style.color = '';  // empty string removes inline style
```

### classList API (Preferred Method)

```javascript
const el = document.querySelector('.alert');

// add — adds one or more classes
el.classList.add('active');
el.classList.add('visible', 'highlighted'); // multiple at once

// remove — removes one or more classes
el.classList.remove('active');
el.classList.remove('visible', 'highlighted');

// toggle — adds if absent, removes if present (returns boolean)
el.classList.toggle('open');          // toggles
el.classList.toggle('open', true);    // force add (never removes)
el.classList.toggle('open', false);   // force remove (never adds)

// contains — check if class exists (returns boolean)
console.log(el.classList.contains('active'));  // true or false

// replace — replace one class with another
el.classList.replace('alert-danger', 'alert-success');

// item — get class at index
console.log(el.classList.item(0)); // first class name

// spread to array
const classes = [...el.classList]; // ["alert", "active", ...]

// length
console.log(el.classList.length);
```

---

## 4.6 Inserting Elements

```javascript
const parent = document.querySelector('.container');
const newEl = document.createElement('p');
newEl.textContent = 'New paragraph';

// ─────────── CLASSIC METHODS ───────────

// appendChild — adds child at END of parent
parent.appendChild(newEl);

// insertBefore — inserts before a reference child
const reference = parent.querySelector('.existing');
parent.insertBefore(newEl, reference); // inserts newEl BEFORE reference
parent.insertBefore(newEl, parent.firstElementChild); // insert at beginning

// ─────────── MODERN METHODS (ES6+) ───────────

// append — like appendChild but:
//   1. Can append multiple nodes
//   2. Can append strings (auto-creates text nodes)
//   3. Returns undefined (not the appended node)
parent.append(newEl, 'some text', anotherEl);

// prepend — inserts at BEGINNING (before first child)
parent.prepend(newEl);
parent.prepend('Text at start', newEl);

// before — inserts BEFORE the element (as sibling)
reference.before(newEl);

// after — inserts AFTER the element (as sibling)
reference.after(newEl);
reference.after(newEl, 'text', anotherEl); // multiple items

// ─────────── insertAdjacentElement & insertAdjacentHTML ───────────

// insertAdjacentElement(position, element)
// position options:
// "beforebegin" — before the element itself (sibling)
// "afterbegin"  — first child of the element
// "beforeend"   — last child of the element
// "afterend"    — after the element itself (sibling)

/*
<!-- beforebegin -->
<div class="container">      ← target element
  <!-- afterbegin -->
  <p>existing content</p>
  <!-- beforeend -->
</div>
<!-- afterend -->
*/

parent.insertAdjacentElement('beforebegin', newEl);
parent.insertAdjacentElement('afterbegin', newEl);
parent.insertAdjacentElement('beforeend', newEl);
parent.insertAdjacentElement('afterend', newEl);

// insertAdjacentHTML — insert raw HTML string at position
parent.insertAdjacentHTML('beforeend', '<p class="new">Added via HTML string</p>');
// ⚠️ Same XSS risk as innerHTML — only use with trusted content
```

---

## 4.7 Removing Elements

```javascript
// Modern way (recommended — clean and simple)
const el = document.querySelector('.obsolete');
el.remove(); // removes itself from DOM

// Classic way (parent.removeChild)
const parent = document.querySelector('.container');
const child = document.querySelector('.child');
parent.removeChild(child);
// Note: child must be an actual direct child of parent or Error is thrown

// Removing all children
const list = document.querySelector('ul');
// Method 1: innerHTML (fast but not ideal — no cleanup of event listeners)
list.innerHTML = '';

// Method 2: while loop (best for complex elements — allows cleanup)
while (list.firstChild) {
  list.removeChild(list.firstChild);
}

// Method 3: replaceChildren (modern, cleanest)
list.replaceChildren(); // removes all children
```

---

## 4.8 Replacing and Cloning

```javascript
// replaceChild (classic)
const parent = document.querySelector('.container');
const oldChild = document.querySelector('.old');
const newChild = document.createElement('div');
newChild.textContent = 'I replaced the old element';
parent.replaceChild(newChild, oldChild); // (new, old)

// replaceWith (modern — element replaces itself)
const old = document.querySelector('.old');
const replacement = document.createElement('section');
old.replaceWith(replacement);
old.replaceWith('<p>Text content</p>'); // can pass strings too

// ─────────── cloneNode ───────────

const original = document.querySelector('.card');

// Shallow clone — copies only the element, NOT its children
const shallowCopy = original.cloneNode(false);

// Deep clone — copies element AND all descendants
const deepCopy = original.cloneNode(true);

// ⚠️ cloneNode does NOT clone event listeners attached via addEventListener!
// Data stored in dataset IS cloned (it's in HTML)
// IDs are also cloned — make sure to update them to avoid duplicate IDs

deepCopy.id = 'card-copy'; // change ID to keep uniqueness
document.body.appendChild(deepCopy);
```

---

## 4.9 DocumentFragment

**What is it?**  
A lightweight, in-memory container for holding DOM nodes. Changes to a fragment don't trigger reflows until the fragment is inserted into the document.

**Why:** Building and inserting many elements one by one triggers a reflow for each insertion. Using DocumentFragment batches all insertions into a single DOM operation.

```javascript
// ─── BAD PRACTICE: inserting in a loop (triggers reflow N times) ───
const ul = document.getElementById('list');
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  ul.appendChild(li); // ← DOM reflow triggered EACH iteration!
}

// ─── GOOD PRACTICE: using DocumentFragment ───
const fragment = document.createDocumentFragment();
// fragment is in memory — NOT part of the live document

for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li); // ← no reflow, just memory operation
}

ul.appendChild(fragment); // ← single DOM insertion, ONE reflow ✅

// Performance benefit:
// Without fragment: 1000 reflows
// With fragment:    1 reflow

// Also works with append, insertBefore, etc.
```

---

### Interview Questions — Section 4

**Basic:**
1. What is the difference between `innerHTML` and `textContent`?
2. How do you add a class to an element without removing existing classes?
3. What is `createElement` and how do you add it to the page?

**Intermediate:**
4. What is an XSS attack and how does `innerHTML` enable it?
5. When would you use `data-*` attributes instead of JavaScript variables?
6. What is the difference between `appendChild` and `append`?

**Advanced:**
7. Explain the performance benefit of `DocumentFragment`.
8. Why doesn't `cloneNode` copy event listeners?
9. What is the difference between `element.style.color` and `getComputedStyle(element).color`?

**Scenario-Based:**
10. You have a list of 500 products coming from an API. How do you render them to the DOM efficiently?

---

# 5. Events

## 5.1 What Are Events?

**Definition:**  
Events are signals fired by the browser when something happens — a user clicks, types, scrolls, the page loads, a timer fires, etc. JavaScript can **listen** for these signals and respond.

**Real-World Analogy:**  
Think of a doorbell (event) and a security system (event listener). The doorbell fires a signal when pressed. The security system is always listening — when it hears the signal, it records footage, sounds an alarm, or sends a notification. Multiple systems can listen to the same doorbell.

---

## 5.2 Event-Driven Programming Paradigm

```
Traditional (procedural):
  Step 1 → Step 2 → Step 3 → Done

Event-Driven:
  "Subscribe to events, wait for them to happen, react"

  Browser                     Your Code
  ─────────────────────       ─────────────────────
  User clicks button    →     click handler runs
  Key is pressed        →     keydown handler runs
  Network responds      →     fetch callback runs
  Timer expires         →     setTimeout callback runs
  Page finishes loading →     DOMContentLoaded fires
```

---

## 5.3 `addEventListener()` — Complete Syntax

```javascript
// Full syntax:
element.addEventListener(eventType, handlerFunction, options);

// Parameters:
// eventType   — string: 'click', 'keydown', etc.
// handler     — function to run when event occurs
// options     — optional: boolean (useCapture) OR options object

// ─── Basic Example ───
const btn = document.getElementById('myBtn');

btn.addEventListener('click', function(event) {
  // 'event' (or 'e') is the Event object — contains info about what happened
  console.log('Button clicked!');
  console.log(event.type);     // "click"
  console.log(event.target);   // the element that was clicked
});

// ─── Arrow function syntax ───
btn.addEventListener('click', (e) => {
  console.log('Clicked with arrow function');
});

// ─── Named function (allows removeEventListener later) ───
function handleClick(e) {
  console.log('Named handler clicked');
}
btn.addEventListener('click', handleClick);

// ─── Options object ───
btn.addEventListener('click', handleClick, {
  capture: false,  // use bubbling phase (default)
  once: true,      // remove listener after first trigger
  passive: true,   // listener never calls preventDefault() (performance hint)
  signal: controller.signal, // AbortController signal for cleanup
});
```

---

## 5.4 `removeEventListener()`

```javascript
// IMPORTANT: You MUST use the exact same function reference to remove!

function handleClick(e) {
  console.log('Clicked');
}

const btn = document.getElementById('myBtn');

// Add listener
btn.addEventListener('click', handleClick);

// Remove listener — must pass the SAME function reference
btn.removeEventListener('click', handleClick); // ✅ works

// ─── This does NOT work (anonymous function — different reference each time) ───
btn.addEventListener('click', function() { console.log('clicked'); });
btn.removeEventListener('click', function() { console.log('clicked'); }); // ❌ fails!

// ─── Modern alternative: AbortController ───
const controller = new AbortController();

btn.addEventListener('click', handleClick, { signal: controller.signal });

// Later, to remove:
controller.abort(); // removes all listeners that used this signal ✅
```

---

## 5.5 The Event Object

When an event fires, the handler receives an **Event object** with rich information.

```javascript
element.addEventListener('click', function(event) {

  // ─── Universal Event Properties ───
  event.type          // "click" — the event type string
  event.target        // element that triggered the event (could be child)
  event.currentTarget // element the listener is attached to
  event.timeStamp     // milliseconds since page loaded
  event.bubbles       // true if event bubbles
  event.cancelable    // true if preventDefault() works
  event.defaultPrevented // true if preventDefault() was called

  // ─── Methods ───
  event.preventDefault()      // prevents default browser behavior
  event.stopPropagation()     // stops bubbling/capturing
  event.stopImmediatePropagation() // stops all other listeners too

});
```

---

## 5.6 Common Events Reference

```
┌─────────────────┬──────────────────────────────────────────────────────┐
│ Event           │ When it fires                                        │
├─────────────────┼──────────────────────────────────────────────────────┤
│ MOUSE EVENTS                                                           │
│ click           │ Mouse button pressed and released                    │
│ dblclick        │ Double click                                         │
│ mousedown       │ Mouse button pressed down                            │
│ mouseup         │ Mouse button released                                │
│ mouseover       │ Mouse enters element OR any descendant (bubbles)     │
│ mouseout        │ Mouse leaves element OR any descendant (bubbles)     │
│ mouseenter      │ Mouse enters element ONLY (does NOT bubble)          │
│ mouseleave      │ Mouse leaves element ONLY (does NOT bubble)          │
│ mousemove       │ Mouse moves over element                             │
│ contextmenu     │ Right-click                                          │
├─────────────────┼──────────────────────────────────────────────────────┤
│ KEYBOARD EVENTS                                                        │
│ keydown         │ Key pressed (fires first, fires repeatedly)          │
│ keypress        │ ⚠️ DEPRECATED — use keydown instead                 │
│ keyup           │ Key released                                         │
├─────────────────┼──────────────────────────────────────────────────────┤
│ FORM EVENTS                                                            │
│ submit          │ Form submitted                                       │
│ input           │ Value changes (fires on every keystroke)             │
│ change          │ Value changes AND element loses focus                │
│ focus           │ Element gains focus (does NOT bubble)                │
│ blur            │ Element loses focus (does NOT bubble)                │
│ focusin         │ Element gains focus (DOES bubble)                    │
│ focusout        │ Element loses focus (DOES bubble)                    │
│ reset           │ Form reset button clicked                            │
├─────────────────┼──────────────────────────────────────────────────────┤
│ DOCUMENT/WINDOW                                                        │
│ DOMContentLoaded│ HTML parsed, DOM ready (before images/CSS load)      │
│ load            │ Everything (images, CSS, scripts) fully loaded       │
│ beforeunload    │ User about to leave the page                         │
│ unload          │ User leaves the page                                 │
│ scroll          │ Element or page scrolled                             │
│ resize          │ Window resized                                       │
│ hashchange      │ URL hash (#) changed                                 │
│ popstate        │ Browser history changes (back/forward)               │
└─────────────────┴──────────────────────────────────────────────────────┘
```

---

## 5.7 Keyboard Events

```javascript
document.addEventListener('keydown', function(e) {
  // ─── Key identification ───
  console.log(e.key);      // "a", "Enter", "ArrowUp", " " (space), "Shift"
  console.log(e.code);     // "KeyA", "Enter", "ArrowUp", "Space", "ShiftLeft"
  console.log(e.keyCode);  // ⚠️ DEPRECATED — numeric code (65 for 'A')

  // ─── Modifier keys ───
  console.log(e.shiftKey); // true if Shift held
  console.log(e.ctrlKey);  // true if Ctrl held
  console.log(e.altKey);   // true if Alt held
  console.log(e.metaKey);  // true if Cmd (Mac) / Win key held

  // ─── Practical examples ───

  // Save with Ctrl+S:
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault(); // prevent browser save dialog
    saveDocument();
  }

  // Close modal with Escape:
  if (e.key === 'Escape') {
    closeModal();
  }

  // Arrow key navigation:
  if (e.key === 'ArrowUp')    moveFocusUp();
  if (e.key === 'ArrowDown')  moveFocusDown();
  if (e.key === 'Enter')      selectItem();
});

// key vs code distinction:
// e.key: what character the keypress produces (layout-dependent)
//        'A' vs 'a' depending on shift; varies by keyboard layout
// e.code: the physical key position (layout-independent)
//        Always "KeyA" regardless of shift or keyboard language
// Use e.key for character input, e.code for physical key shortcuts
```

---

## 5.8 Mouse Events

```javascript
document.addEventListener('mousemove', function(e) {
  // ─── Coordinate systems ───
  console.log(e.clientX, e.clientY); // relative to VIEWPORT (ignores scroll)
  console.log(e.pageX, e.pageY);     // relative to PAGE (includes scroll offset)
  console.log(e.screenX, e.screenY); // relative to SCREEN/MONITOR
  console.log(e.offsetX, e.offsetY); // relative to TARGET element's top-left corner
  console.log(e.movementX, e.movementY); // pixels moved since last event

  // ─── Button information ───
  console.log(e.button);  // 0=left, 1=middle, 2=right
  console.log(e.buttons); // bitmask of pressed buttons (can detect multiple)

  // ─── Target info ───
  console.log(e.target);         // element mouse is over
  console.log(e.relatedTarget);  // element mouse came FROM (mouseover) or TO (mouseout)
});

// Drag tracking example:
let isDragging = false;
let startX, startY;
const draggable = document.querySelector('.draggable');

draggable.addEventListener('mousedown', (e) => {
  isDragging = true;
  startX = e.clientX - draggable.offsetLeft;
  startY = e.clientY - draggable.offsetTop;
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  draggable.style.left = (e.clientX - startX) + 'px';
  draggable.style.top = (e.clientY - startY) + 'px';
});

document.addEventListener('mouseup', () => {
  isDragging = false;
});
```

---

# 6. Event Bubbling

## 6.1 What is Event Bubbling?

**Definition:**  
When an event fires on an element, it first runs handlers on that element, then on its **parent**, then its **grandparent**, all the way up to `document` and then `window`. The event "bubbles up" like a bubble rising through water.

**Real-World Analogy:**  
Imagine a company org chart. An employee (inner element) submits a report (event). The report first goes to their direct manager, then the manager's manager, then the CEO, then the board — traveling up the hierarchy.

```
ASCII Diagram — Bubbling:
─────────────────────────

HTML:
<div id="grandparent">         ← (3) fires 3rd
  <div id="parent">            ← (2) fires 2nd
    <button id="child">Click   ← (1) fires 1st (origin)
    </button>
  </div>
</div>

Event Flow (Bubbling):
            window
              ↑
           document
              ↑
            <html>
              ↑
            <body>
              ↑
     ┌──── grandparent ────┐ (3)
     │         ↑           │
     │  ┌── parent ──┐     │ (2)
     │  │     ↑      │     │
     │  │   child    │     │ (1) ← click happens here
     │  └────────────┘     │
     └─────────────────────┘
```

```javascript
// Setting up event bubbling demo
const grandparent = document.getElementById('grandparent');
const parent = document.getElementById('parent');
const child = document.getElementById('child');

grandparent.addEventListener('click', () => console.log('Grandparent clicked'));
parent.addEventListener('click', () => console.log('Parent clicked'));
child.addEventListener('click', () => console.log('Child clicked'));

// When you click the button:
// Output:
// "Child clicked"      ← fires first
// "Parent clicked"     ← bubbles to parent
// "Grandparent clicked" ← bubbles to grandparent
```

---

## 6.2 `event.target` vs `event.currentTarget`

This is one of the most important distinctions in DOM events.

```javascript
grandparent.addEventListener('click', function(e) {
  console.log(e.target);        // The element that was ACTUALLY clicked (the child)
  console.log(e.currentTarget); // The element THIS listener is attached to (grandparent)
  console.log(this);            // Same as currentTarget (inside regular function)
});

// If you click the child button:
// e.target        → <button id="child">  (where it started)
// e.currentTarget → <div id="grandparent"> (where this listener lives)

// Arrow functions and 'this':
grandparent.addEventListener('click', (e) => {
  console.log(this);            // undefined (or window in non-strict) — arrow functions!
  console.log(e.currentTarget); // <div id="grandparent"> ← use this instead
});
```

---

## 6.3 `stopPropagation()` and `stopImmediatePropagation()`

```javascript
// stopPropagation — stops the event from bubbling further UP
child.addEventListener('click', function(e) {
  e.stopPropagation(); // prevents event from reaching parent/grandparent
  console.log('Child handled, stopping bubble');
});

parent.addEventListener('click', () => {
  console.log('This will NOT run if child stopped propagation');
});

// stopImmediatePropagation — stops bubbling AND stops other listeners on SAME element
const btn = document.getElementById('btn');

btn.addEventListener('click', function(e) {
  e.stopImmediatePropagation();
  console.log('First handler — stopping everything');
});

btn.addEventListener('click', function(e) {
  console.log('Second handler — this will NOT run');
});

// ─── When to use stopPropagation ───
// - Dropdown menus: click inside doesn't close the dropdown
// - Nested clickable elements (card with a button inside)
// - Modal dialogs where outer click closes modal but inner doesn't

// ─── ⚠️ Warning ───
// Overusing stopPropagation breaks event delegation and is hard to debug
// Prefer checking e.target inside parent handlers instead
```

---

# 7. Event Capturing

## 7.1 What is Event Capturing?

**Definition:**  
The opposite of bubbling. Events travel **DOWN** the DOM tree from `window` to the target element BEFORE the target fires. This is called the **capture phase**.

```
Complete Event Phases:
─────────────────────
Phase 1: CAPTURING (top → down)
Phase 2: TARGET (at the element)
Phase 3: BUBBLING (bottom → up)

                     window
                 ↓ capture ↑ bubble
                  document
                 ↓ capture ↑ bubble
                   <html>
                 ↓ capture ↑ bubble
                   <body>
                 ↓ capture ↑ bubble
                    <div>
                 ↓ capture ↑ bubble
                   <button>  ← target phase
```

---

## 7.2 Enabling Capture Phase

```javascript
// Third parameter: true = capture phase, false = bubble phase (default)
element.addEventListener('click', handler, true);  // capture
element.addEventListener('click', handler, false); // bubble (default)

// Or with options object:
element.addEventListener('click', handler, { capture: true });

// Capture + Bubble demo:
const outer = document.querySelector('.outer');
const inner = document.querySelector('.inner');

// CAPTURE listeners
outer.addEventListener('click', () => console.log('Outer CAPTURE'), true);
inner.addEventListener('click', () => console.log('Inner CAPTURE'), true);

// BUBBLE listeners
inner.addEventListener('click', () => console.log('Inner BUBBLE'), false);
outer.addEventListener('click', () => console.log('Outer BUBBLE'), false);

// Click on inner element — output order:
// 1. "Outer CAPTURE"   ← capture phase, going down
// 2. "Inner CAPTURE"   ← at target (capture listener first)
// 3. "Inner BUBBLE"    ← at target (bubble listener second)
// 4. "Outer BUBBLE"    ← bubble phase, going up
```

---

## 7.3 When to Use Capturing

```javascript
// 1. Intercepting events before they reach the target
// Use case: access control / logging
document.addEventListener('click', function(e) {
  logEvent(e.target, 'click'); // log all clicks for analytics
}, { capture: true }); // runs before any bubble-phase handlers

// 2. Focus management (focus doesn't bubble, but focusin does)
// Some frameworks use capture for focus events

// 3. Rare: when you need to modify/cancel events before they reach targets
document.addEventListener('keydown', function(e) {
  if (appState.modalOpen && e.key === 'Tab') {
    e.preventDefault(); // trap focus inside modal
    cycleFocusInModal();
  }
}, { capture: true });
```

---

# 8. Event Delegation

## 8.1 What is Event Delegation?

**Definition:**  
Instead of attaching event listeners to each individual element, attach **one listener to a common ancestor** and use `event.target` to determine which element was actually clicked.

**Real-World Analogy:**  
Instead of hiring a security guard for every single store in a mall, the mall management hires one CCTV operator who watches all stores at once. When an incident happens in any store, the operator identifies which store (event.target) and responds accordingly.

---

## 8.2 The Problem Without Delegation

```javascript
// ─── BAD: Listener on every element ───
// HTML: <ul id="list">
//         <li>Item 1</li>
//         <li>Item 2</li>
//         ...1000 items...
//       </ul>

const items = document.querySelectorAll('#list li');

items.forEach(item => {
  item.addEventListener('click', function() {
    console.log(this.textContent); // Each li has its own listener
  });
});

// Problems:
// 1. 1000 event listeners in memory — performance hit
// 2. New items added dynamically DON'T get listeners!
// 3. Hard to remove all listeners cleanly
```

## 8.3 Event Delegation Solution

```javascript
// ─── GOOD: One listener on parent ───
const list = document.getElementById('list');

list.addEventListener('click', function(e) {
  // e.target: the specific <li> that was clicked
  // e.currentTarget: the <ul> (where listener lives)

  // Make sure we clicked an li, not whitespace in the ul
  if (e.target.tagName === 'LI') {
    console.log(e.target.textContent);
    e.target.classList.toggle('selected');
  }
});

// ✅ Works for dynamically added items too!
setTimeout(() => {
  const newItem = document.createElement('li');
  newItem.textContent = 'Item 1001';
  list.appendChild(newItem);
  // This new item is AUTOMATICALLY covered by the parent listener!
}, 1000);
```

---

## 8.4 Using `closest()` for Robust Delegation

```javascript
// HTML structure:
// <ul id="task-list">
//   <li class="task" data-id="1">
//     <span class="task-name">Buy groceries</span>
//     <button class="delete">✕</button>
//   </li>
// </ul>

// PROBLEM: If user clicks the <span> or button INSIDE the <li>,
// e.target won't be the <li> itself

// SOLUTION: Use closest() to find the right ancestor

document.getElementById('task-list').addEventListener('click', function(e) {

  // Handle delete button click
  if (e.target.closest('.delete')) {
    const taskItem = e.target.closest('.task');
    const taskId = taskItem.dataset.id;
    deleteTask(taskId);
    taskItem.remove();
    return;
  }

  // Handle clicking the task item itself (for toggling completion)
  const task = e.target.closest('.task');
  if (task) {
    task.classList.toggle('completed');
  }
});
```

---

## 8.5 Real-World Example: Dynamic Table

```javascript
// Creating a dynamic table with delegation
const table = document.getElementById('data-table');

// One listener handles ALL rows — even rows added later
table.addEventListener('click', function(e) {
  const action = e.target.dataset.action; // data-action attribute on buttons

  if (!action) return; // clicked something without a data-action

  const row = e.target.closest('tr');
  const userId = row.dataset.userId;

  switch (action) {
    case 'edit':
      openEditModal(userId);
      break;
    case 'delete':
      if (confirm('Delete this user?')) {
        deleteUser(userId).then(() => row.remove());
      }
      break;
    case 'view':
      viewUserProfile(userId);
      break;
  }
});

// Function to add rows dynamically — they're automatically handled
function addUserRow(user) {
  const row = document.createElement('tr');
  row.dataset.userId = user.id;
  row.innerHTML = `
    <td>${user.name}</td>
    <td>${user.email}</td>
    <td>
      <button data-action="view">View</button>
      <button data-action="edit">Edit</button>
      <button data-action="delete">Delete</button>
    </td>
  `;
  table.querySelector('tbody').appendChild(row);
}
```

---

## 8.6 Performance Benefits

```
Memory comparison (1000 list items):
─────────────────────────────────────
Without delegation:
  1000 li × 1 listener each = 1000 listener objects in memory

With delegation:
  1 ul × 1 listener = 1 listener object in memory

Performance difference:
  - Page load: faster (no event binding loop)
  - Memory: ~99.9% reduction in listener objects
  - Dynamic elements: automatically handled (no code needed)
  - Cleanup: remove 1 listener instead of 1000
```

---

### Interview Questions — Sections 5-8

**Basic:**
1. What is the difference between `addEventListener` and the old `onclick` property?
2. What does `preventDefault()` do?
3. What is event bubbling?

**Intermediate:**
4. Explain event delegation and why it's better than attaching listeners to each element.
5. What is the difference between `event.target` and `event.currentTarget`?
6. What is the difference between `mouseover` and `mouseenter`?

**Advanced:**
7. How does event capturing work? Give a use case where you'd use it.
8. Why can't you remove an anonymous function added with `addEventListener`?
9. Explain the three phases of DOM events in order.

**Scenario-Based:**
10. You have a "load more" feature that adds 50 new cards to the page. Each card has edit/delete buttons. How do you handle events efficiently?

**Tricky Output Question:**
```javascript
const div = document.createElement('div');
const btn = document.createElement('button');
div.appendChild(btn);
document.body.appendChild(div);

div.addEventListener('click', () => console.log('div clicked'));
btn.addEventListener('click', (e) => {
  e.stopPropagation();
  console.log('btn clicked');
});

btn.click();
// What is the output?
// Answer: "btn clicked" only — stopPropagation prevents "div clicked"
```

---

# 9. Custom Events

## 9.1 What are Custom Events?

**Definition:**  
JavaScript lets you create your own events (beyond the built-in ones like 'click' or 'keydown') and dispatch them on any element. This enables a **pub/sub (publish-subscribe) communication pattern** between different parts of your application.

**Real-World Analogy:**  
A news agency publishes articles. Subscribers (event listeners) who signed up for particular topics automatically receive the news when it's published. You control what events exist, what data they carry, and when they fire.

---

## 9.2 Creating and Dispatching Custom Events

```javascript
// ─── Basic CustomEvent ───

// Step 1: Create the custom event
const myEvent = new CustomEvent('userLoggedIn', {
  bubbles: true,     // should event bubble up the DOM? (default: false)
  cancelable: true,  // can preventDefault() be called?
  detail: {          // ← key feature: pass custom DATA with the event
    userId: 42,
    username: 'nihal_singh',
    role: 'admin',
    loginTime: new Date()
  }
});

// Step 2: Listen for the custom event
document.addEventListener('userLoggedIn', function(e) {
  console.log('User logged in!');
  console.log(e.detail.username);  // "nihal_singh"
  console.log(e.detail.role);      // "admin"
  updateUIForUser(e.detail);
});

// Step 3: Dispatch (fire) the event from anywhere
// Usually from the element closest to the source of the change
document.dispatchEvent(myEvent);
```

---

## 9.3 Practical: Component Communication Without Frameworks

```javascript
// Real-world use: Decoupled components communicating via events

// ─── Cart Component ───
const cart = {
  items: [],

  addItem(item) {
    this.items.push(item);

    // Notify the rest of the app
    const event = new CustomEvent('cart:updated', {
      bubbles: true,
      detail: {
        items: this.items,
        count: this.items.length,
        total: this.items.reduce((sum, i) => sum + i.price, 0)
      }
    });
    document.dispatchEvent(event);
  }
};

// ─── Header Badge Component (listens independently) ───
document.addEventListener('cart:updated', function(e) {
  const badge = document.getElementById('cart-badge');
  badge.textContent = e.detail.count;  // update count display
});

// ─── Sidebar Summary Component (listens independently) ───
document.addEventListener('cart:updated', function(e) {
  document.getElementById('cart-total').textContent = `$${e.detail.total}`;
});

// Using the cart:
cart.addItem({ name: 'React Book', price: 39.99 });
// Both header badge AND sidebar automatically update!
```

---

## 9.4 Custom Event on Specific Element

```javascript
// Custom events can be dispatched on any element
const modal = document.getElementById('myModal');

// Listen on specific element
modal.addEventListener('modal:close', function(e) {
  console.log('Close reason:', e.detail.reason);
  modal.style.display = 'none';
});

// Dispatch on specific element
function closeModal(reason) {
  const event = new CustomEvent('modal:close', {
    detail: { reason }
  });
  modal.dispatchEvent(event); // fires on modal, bubbles up if bubbles:true
}

closeModal('user-dismissed');
```

---

# 10. Form Events & Validation

## 10.1 Form Events

```javascript
const form = document.getElementById('signup-form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');

// ─── submit event ───
form.addEventListener('submit', function(e) {
  e.preventDefault(); // CRITICAL: stops form from reloading the page

  // Collect form data
  const formData = new FormData(form);
  const data = {
    name: formData.get('name'),
    email: formData.get('email'),
    password: formData.get('password')
  };

  // Or get values directly:
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();

  if (validateForm(data)) {
    submitToServer(data);
  }
});

// ─── input event (fires on EVERY keystroke) ───
nameInput.addEventListener('input', function(e) {
  const value = e.target.value;
  const count = document.getElementById('char-count');
  count.textContent = `${value.length}/50 characters`;

  // Real-time validation
  if (value.length < 2) {
    showError(nameInput, 'Name must be at least 2 characters');
  } else {
    clearError(nameInput);
  }
});

// ─── change event (fires on change + blur) ───
emailInput.addEventListener('change', function(e) {
  // Only fires when user leaves the field after making a change
  validateEmail(e.target.value);
});

// ─── focus event (element receives focus) ───
nameInput.addEventListener('focus', function() {
  nameInput.parentElement.classList.add('focused'); // add highlight
});

// ─── blur event (element loses focus) ───
nameInput.addEventListener('blur', function() {
  nameInput.parentElement.classList.remove('focused');
  // Validate on blur (common UX pattern)
  if (!nameInput.value.trim()) {
    showError(nameInput, 'Name is required');
  }
});
```

---

## 10.2 Custom Form Validation

```javascript
// ─── HTML5 Constraint Validation API ───

// HTML: <input type="email" id="email" required minlength="5">

const input = document.getElementById('email');

// Check validity state
console.log(input.validity.valid);        // true/false overall
console.log(input.validity.valueMissing); // true if required but empty
console.log(input.validity.typeMismatch); // true if wrong type (e.g., bad email)
console.log(input.validity.tooShort);     // true if shorter than minlength
console.log(input.validity.tooLong);      // true if longer than maxlength
console.log(input.validity.patternMismatch); // true if pattern not matched
console.log(input.validity.rangeUnderflow);  // true if below min
console.log(input.validity.rangeOverflow);   // true if above max

// Get browser validation message
console.log(input.validationMessage); // "Please enter a valid email address"

// Trigger validation display
input.checkValidity(); // returns true/false; triggers 'invalid' event if false
form.reportValidity(); // returns true/false; shows browser error tooltips

// Set custom validation message
input.setCustomValidity('');             // clears custom error
input.setCustomValidity('Username taken!'); // marks as invalid with your message

// ─── Complete custom validation function ───
function validateForm(form) {
  let isValid = true;

  // Clear previous errors
  form.querySelectorAll('.error-msg').forEach(el => el.remove());
  form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

  // Name validation
  const name = form.querySelector('[name="name"]');
  if (name.value.trim().length < 2) {
    showFieldError(name, 'Name must be at least 2 characters');
    isValid = false;
  }

  // Email validation
  const email = form.querySelector('[name="email"]');
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    showFieldError(email, 'Please enter a valid email address');
    isValid = false;
  }

  // Password validation
  const password = form.querySelector('[name="password"]');
  if (password.value.length < 8) {
    showFieldError(password, 'Password must be at least 8 characters');
    isValid = false;
  }

  return isValid;
}

function showFieldError(input, message) {
  input.classList.add('error');
  const errorEl = document.createElement('span');
  errorEl.className = 'error-msg';
  errorEl.textContent = message;
  input.parentElement.appendChild(errorEl);
}
```

---

# 11. Intersection Observer API

## 11.1 What is the Intersection Observer API?

**Definition:**  
An API that lets you asynchronously observe when an element **enters or exits the viewport** (or another specified root element). It replaced the expensive practice of listening to scroll events and calling `getBoundingClientRect()`.

**Real-World Analogy:**  
Security cameras at a store entrance. Instead of a guard constantly watching every person in the store (scroll event + getBoundingClientRect), cameras only alert the guard when someone crosses the entrance line (element enters viewport).

**Use Cases:**
- Lazy loading images
- Infinite scroll / load more
- Animation triggers (animate when scrolled into view)
- Analytics (tracking ad visibility, reading time)
- Sticky headers

---

## 11.2 Basic Intersection Observer

```javascript
// ─── Step 1: Create the observer ───
const observer = new IntersectionObserver(callback, options);

// ─── The callback function ───
// Called when any observed element's visibility changes
function callback(entries, observer) {
  // entries: array of IntersectionObserverEntry objects
  entries.forEach(entry => {
    console.log(entry.target);          // the observed element
    console.log(entry.isIntersecting);  // true = in view, false = out of view
    console.log(entry.intersectionRatio); // 0.0 to 1.0 how much is visible
    console.log(entry.boundingClientRect); // element's DOMRect
    console.log(entry.intersectionRect);   // visible portion's DOMRect
    console.log(entry.rootBounds);         // root's DOMRect
    console.log(entry.time);               // timestamp of observation

    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}

// ─── Options ───
const options = {
  root: null,          // null = viewport; or specify an element as root
  rootMargin: '0px',   // margin around root ("100px 0px" = trigger 100px early)
  threshold: 0.5       // 0=any intersection, 1=fully visible, 0.5=50% visible
                       // Array: [0, 0.25, 0.5, 0.75, 1] for multiple triggers
};

// ─── Step 2: Observe elements ───
const targets = document.querySelectorAll('.lazy-section');
targets.forEach(target => observer.observe(target));

// ─── Step 3: Stop observing ───
observer.unobserve(entry.target); // stop observing ONE element
observer.disconnect();            // stop observing ALL elements
```

---

## 11.3 Practical: Lazy Loading Images

```javascript
// HTML: <img class="lazy" data-src="actual-image.jpg" src="placeholder.jpg">

const lazyImages = document.querySelectorAll('img.lazy');

const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;

      // Swap placeholder src with actual image
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      img.classList.add('loaded');

      // Stop observing this image (it's loaded!)
      imageObserver.unobserve(img);
    }
  });
}, {
  rootMargin: '200px 0px' // start loading 200px before it enters viewport
});

lazyImages.forEach(img => imageObserver.observe(img));
```

---

## 11.4 Practical: Animate on Scroll

```javascript
// Reveal elements as they scroll into view
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      // Optionally stop observing after first reveal
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.15 // trigger when 15% of element is visible
});

document.querySelectorAll('.reveal-on-scroll').forEach(el => {
  revealObserver.observe(el);
});

// CSS would be:
// .reveal-on-scroll { opacity: 0; transform: translateY(30px); transition: all 0.6s; }
// .reveal-on-scroll.revealed { opacity: 1; transform: translateY(0); }
```

---

## 11.5 Practical: Infinite Scroll

```javascript
// Add a sentinel element at the bottom of your list
// HTML: <div id="sentinel"></div>

const sentinel = document.getElementById('sentinel');
let page = 1;
let loading = false;

const scrollObserver = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && !loading) {
    loading = true;
    page++;

    const newItems = await fetchMoreItems(page); // your API call
    renderItems(newItems);

    loading = false;

    if (newItems.length === 0) {
      // No more items — stop observing
      scrollObserver.unobserve(sentinel);
    }
  }
});

scrollObserver.observe(sentinel);
```

---

# 12. Mutation Observer

## 12.1 What is MutationObserver?

**Definition:**  
An API for watching the DOM for changes — additions/removals of child nodes, attribute changes, or text content changes. The modern replacement for deprecated DOM Mutation Events.

**Real-World Analogy:**  
A foreman watching a construction site. Instead of constantly inspecting every inch of the site (polling with setInterval), the foreman only gets notified when workers make changes (mutations).

---

## 12.2 MutationObserver Setup

```javascript
// ─── Create observer ───
const observer = new MutationObserver(function(mutationsList, observer) {
  // mutationsList: array of MutationRecord objects
  mutationsList.forEach(mutation => {
    console.log('Mutation type:', mutation.type);

    if (mutation.type === 'childList') {
      // Child nodes were added or removed
      console.log('Added nodes:', mutation.addedNodes);
      console.log('Removed nodes:', mutation.removedNodes);
    }

    if (mutation.type === 'attributes') {
      // An attribute changed
      console.log('Changed attribute:', mutation.attributeName);
      console.log('Old value:', mutation.oldValue);
    }

    if (mutation.type === 'characterData') {
      // Text content changed
      console.log('Text changed to:', mutation.target.data);
    }
  });
});

// ─── Configuration options ───
const config = {
  childList: true,        // watch for child node additions/removals
  subtree: true,          // watch all descendants (not just direct children)
  attributes: true,       // watch attribute changes
  attributeOldValue: true, // record old attribute value
  characterData: true,    // watch text content changes
  characterDataOldValue: true, // record old text value
  attributeFilter: ['class', 'style'] // only watch specific attributes
};

// ─── Start observing ───
const targetNode = document.getElementById('watched-container');
observer.observe(targetNode, config);

// ─── Stop observing ───
observer.disconnect();

// ─── Read accumulated mutations ───
const pendingMutations = observer.takeRecords(); // and clears the queue
```

---

## 12.3 Practical Use Cases

```javascript
// Use case 1: Detect when a third-party script changes an element
const priceDisplay = document.querySelector('.price');
const priceObserver = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    if (mutation.type === 'characterData' || mutation.type === 'childList') {
      const newPrice = parseFloat(priceDisplay.textContent);
      if (newPrice !== lastKnownPrice) {
        onPriceChanged(newPrice);
      }
    }
  });
});
priceObserver.observe(priceDisplay, { childList: true, characterData: true, subtree: true });

// Use case 2: Auto-initialize components added dynamically
const bodyObserver = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    mutation.addedNodes.forEach(node => {
      if (node.nodeType === 1 && node.classList.contains('datepicker')) {
        initializeDatepicker(node); // auto-init any new datepickers
      }
    });
  });
});
bodyObserver.observe(document.body, { childList: true, subtree: true });
```

---

# 13. Resize Observer

## 13.1 What is ResizeObserver?

**Definition:**  
Watches for changes in the **size of an element** and notifies you whenever the element's content dimensions change.

**Why is this better than `window.addEventListener('resize')`?**
- `window resize` only fires when the WINDOW changes size
- Elements can resize due to: CSS changes, content changes, flexbox/grid reflow, parent container resize
- ResizeObserver is element-scoped, not window-scoped

---

## 13.2 ResizeObserver Usage

```javascript
const resizeObserver = new ResizeObserver(entries => {
  entries.forEach(entry => {
    const { width, height } = entry.contentRect;
    console.log('Element width:', width);
    console.log('Element height:', height);

    // Also available:
    entry.target;              // the element being observed
    entry.contentBoxSize;      // size as array of ResizeObserverSize
    entry.borderBoxSize;       // includes padding and border
    entry.devicePixelContentBoxSize; // size in device pixels
  });
});

// Observe an element
const box = document.querySelector('.resizable-box');
resizeObserver.observe(box);

// Stop observing
resizeObserver.unobserve(box);
resizeObserver.disconnect();

// Practical example: responsive chart
const chart = document.getElementById('chart-container');
const resizeChart = new ResizeObserver(entries => {
  const { width, height } = entries[0].contentRect;
  myChartInstance.resize(width, height); // re-render chart to fit
});
resizeChart.observe(chart);

// Responsive canvas
const canvas = document.getElementById('myCanvas');
const canvasObserver = new ResizeObserver(entries => {
  const { width, height } = entries[0].contentRect;
  canvas.width = width * window.devicePixelRatio;
  canvas.height = height * window.devicePixelRatio;
  redrawCanvas(); // re-render
});
canvasObserver.observe(canvas.parentElement);
```

---

# 14. Performance Considerations

## 14.1 Reflow and Repaint

**Definitions:**
- **Reflow (Layout):** Browser recalculates positions and sizes of elements. Expensive.
- **Repaint:** Browser redraws pixels without geometry changes (e.g., color change). Less expensive.
- **Compositing:** Browser moves pre-rendered layers. Very cheap (GPU-accelerated).

```
Cost:  Reflow > Repaint > Compositing

Properties that trigger REFLOW (avoid in hot code paths):
  - width, height, top, left, right, bottom
  - margin, padding, border
  - font-size, font-family
  - display, position
  - offsetWidth/Height, clientWidth/Height ← READING layout also triggers reflow!
  - getBoundingClientRect(), getComputedStyle()

Properties that trigger only REPAINT:
  - color, background-color
  - visibility, outline, border-radius, box-shadow

Properties that ONLY composite (GPU layer — very fast):
  - transform, opacity, filter (with will-change)
```

---

## 14.2 Layout Thrashing (Forced Synchronous Layout)

**This is one of the most common performance mistakes:**

```javascript
// ─── BAD: Layout Thrashing ───
// Alternating reads and writes forces the browser to recalculate layout each time

const boxes = document.querySelectorAll('.box');
boxes.forEach(box => {
  const width = box.offsetWidth;        // READ  → forces layout
  box.style.width = width / 2 + 'px';  // WRITE → invalidates layout
  const height = box.offsetHeight;      // READ  → forces layout AGAIN
  box.style.height = height / 2 + 'px'; // WRITE → invalidates layout AGAIN
});
// Each iteration: READ → layout → WRITE → invalidate → READ → layout ...

// ─── GOOD: Batch reads, then batch writes ───
const boxes = document.querySelectorAll('.box');
const dimensions = []; // Step 1: collect all reads

boxes.forEach(box => {
  dimensions.push({
    width: box.offsetWidth,   // READ all at once
    height: box.offsetHeight  // (browser does ONE layout calculation)
  });
});

boxes.forEach((box, i) => {
  box.style.width = dimensions[i].width / 2 + 'px';   // WRITE all at once
  box.style.height = dimensions[i].height / 2 + 'px'; // (browser paints ONCE)
});
```

---

## 14.3 requestAnimationFrame for Animations

```javascript
// ─── BAD: setInterval for animation ───
setInterval(() => {
  element.style.left = parseFloat(element.style.left) + 1 + 'px';
}, 16); // ~60fps... but not synchronized with screen refresh!

// ─── GOOD: requestAnimationFrame ───
// Synchronized with browser repaint cycle (typically 60fps = 16.67ms intervals)
// Automatically pauses when tab is not visible (saves battery/CPU)

let position = 0;
let animationId;

function animate(timestamp) {
  // timestamp: high-resolution timestamp provided by browser
  position += 2;
  element.style.transform = `translateX(${position}px)`; // use transform, not left!

  if (position < 500) {
    animationId = requestAnimationFrame(animate); // schedule next frame
  }
}

animationId = requestAnimationFrame(animate); // start animation

// Cancel animation
cancelAnimationFrame(animationId);

// ─── Smooth animation with delta time ───
let lastTime = 0;
const speed = 200; // pixels per second

function animateWithDelta(currentTime) {
  const deltaTime = (currentTime - lastTime) / 1000; // convert to seconds
  lastTime = currentTime;

  position += speed * deltaTime; // frame-rate independent movement
  element.style.transform = `translateX(${position}px)`;

  if (position < 500) {
    requestAnimationFrame(animateWithDelta);
  }
}
requestAnimationFrame(animateWithDelta);
```

---

## 14.4 `will-change` CSS Property

```css
/* Hints to browser to prepare a GPU layer for this element */
/* Use ONLY on elements that WILL animate — don't use globally! */

.animated-element {
  will-change: transform, opacity; /* promote to own compositor layer */
}

/* After animation completes — remove it: */
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto'; // clean up
});
```

```javascript
// Use will-change dynamically
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform';
});
element.addEventListener('mouseleave', () => {
  element.style.willChange = 'auto';
});
```

---

## 14.5 DocumentFragment (Revisited in Performance Context)

```javascript
// Benchmark comparison:
// Direct DOM insertion of 10,000 elements: ~150ms
// DocumentFragment approach: ~8ms (nearly 20x faster!)

function renderLargeList(items) {
  const fragment = document.createDocumentFragment();

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    li.dataset.id = item.id;
    fragment.appendChild(li); // in-memory, no reflow
  });

  document.getElementById('list').appendChild(fragment); // ONE DOM operation
}
```

---

## 14.6 Debouncing and Throttling Event Handlers

```javascript
// ─── PROBLEM: scroll/resize events fire hundreds of times per second ───
window.addEventListener('scroll', () => {
  doExpensiveCalculation(); // Called 60+ times per second! 😱
});

// ─── SOLUTION 1: Throttle — execute at most once per N milliseconds ───
function throttle(fn, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

window.addEventListener('scroll', throttle(() => {
  doExpensiveCalculation();
}, 100)); // at most once every 100ms ✅

// ─── SOLUTION 2: Debounce — execute ONLY after N ms of inactivity ───
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer); // reset timer on each call
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

// Search input — only search after user stops typing for 300ms
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce((e) => {
  performSearch(e.target.value); // called only once after user pauses typing
}, 300));

// Resize recalculation
window.addEventListener('resize', debounce(() => {
  recalculateLayout();
}, 200));
```

---

## 14.7 Virtual Scroll for Long Lists

```javascript
// When rendering thousands of items, only render what's VISIBLE
// This is "windowing" or "virtual scrolling"

class VirtualScroller {
  constructor(container, items, itemHeight) {
    this.container = container;
    this.items = items;
    this.itemHeight = itemHeight;
    this.totalHeight = items.length * itemHeight;
    this.visibleCount = Math.ceil(container.clientHeight / itemHeight) + 2; // buffer

    this.setup();
  }

  setup() {
    // Create a spacer to maintain correct scrollbar
    this.spacer = document.createElement('div');
    this.spacer.style.height = this.totalHeight + 'px';
    this.container.appendChild(this.spacer);

    // The actual visible items wrapper
    this.viewport = document.createElement('div');
    this.viewport.style.position = 'absolute';
    this.viewport.style.top = '0';
    this.viewport.style.width = '100%';
    this.container.appendChild(this.viewport);

    this.container.style.position = 'relative';
    this.container.style.overflow = 'auto';

    this.container.addEventListener('scroll', () => this.render());
    this.render();
  }

  render() {
    const scrollTop = this.container.scrollTop;
    const startIndex = Math.floor(scrollTop / this.itemHeight);
    const endIndex = Math.min(startIndex + this.visibleCount, this.items.length);

    this.viewport.style.transform = `translateY(${startIndex * this.itemHeight}px)`;
    this.viewport.innerHTML = '';

    // Only render visible slice
    const fragment = document.createDocumentFragment();
    for (let i = startIndex; i < endIndex; i++) {
      const el = document.createElement('div');
      el.style.height = this.itemHeight + 'px';
      el.textContent = this.items[i];
      fragment.appendChild(el);
    }
    this.viewport.appendChild(fragment);
  }
}

// Usage:
const items = Array.from({ length: 100000 }, (_, i) => `Item ${i + 1}`);
const scroller = new VirtualScroller(document.getElementById('list'), items, 40);
// Renders only ~20 items at a time instead of 100,000!
```

---

## 14.8 Passive Event Listeners

```javascript
// ─── PROBLEM: scroll/touch listeners that never call preventDefault()
// still block the main thread while browser WAITS to find out
// if you're going to call preventDefault()

// ─── SOLUTION: { passive: true } tells browser to not wait ───
window.addEventListener('scroll', handleScroll, { passive: true });
// Browser can immediately start scrolling without waiting for JS to run!

document.addEventListener('touchstart', handleTouch, { passive: true });
document.addEventListener('touchmove', handleTouch, { passive: true });
// Massive improvement for scroll performance on mobile devices!

// ⚠️ Only use passive: true if you NEVER call e.preventDefault()
// Calling preventDefault() in a passive listener throws a warning and is ignored
```

---

# 15. Chapter Summary & Master Review

## Chapter Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CHAPTER 6 SUMMARY                               │
├──────────────────┬──────────────────────────────────────────────────┤
│ Topic            │ Key Takeaway                                      │
├──────────────────┼──────────────────────────────────────────────────┤
│ DOM              │ In-memory tree representation of HTML             │
│ Selection        │ querySelector is most flexible; getElementById    │
│                  │ is fastest                                        │
│ Live vs Static   │ HTMLCollection = live; querySelectorAll = static  │
│ Traversal        │ Use *ElementChild/Sibling to avoid text nodes     │
│ closest()        │ Find nearest matching ancestor (traverse up)      │
│ createElement    │ Create → Configure → Insert                       │
│ innerHTML        │ XSS risk with user input; use textContent instead │
│ dataset          │ Access data-* attributes safely via element.dataset│
│ classList        │ add/remove/toggle/contains/replace                │
│ DocumentFragment │ Batch DOM insertions for performance              │
│ addEventListener │ Preferred over onclick; supports multiple handlers │
│ Bubbling         │ Events travel UP the DOM tree by default          │
│ Capturing        │ Events travel DOWN (set { capture: true })        │
│ Delegation       │ One parent listener for many children             │
│ Custom Events    │ new CustomEvent + dispatchEvent for pub/sub       │
│ preventDefault   │ Stop default browser behavior (form submit, links)│
│ IntersectionObs  │ Lazy loading, infinite scroll, scroll animations  │
│ MutationObserver │ Watch DOM changes (third-party code, auto-init)   │
│ ResizeObserver   │ Element-level resize detection                    │
│ Reflow/Repaint   │ Batch reads then writes; avoid layout thrashing   │
│ rAF              │ Use requestAnimationFrame for smooth animations    │
│ Debounce/Throttle│ Limit rate of scroll/resize/input handlers        │
│ Virtual Scroll   │ Only render visible items for large lists         │
└──────────────────┴──────────────────────────────────────────────────┘
```

---

## Top 25 Interview Questions

### Basic Level
1. **What is the DOM?** — In-memory tree object representation of the HTML document that JavaScript can interact with.

2. **What is the difference between `querySelector` and `getElementById`?** — `querySelector` accepts any CSS selector and returns the first match; `getElementById` only accepts an ID and is faster (O(1) hash lookup).

3. **What does `preventDefault()` do?** — Prevents the browser's default action for an event (e.g., stops a form submission reloading the page, stops a link from navigating).

4. **What is the difference between `innerHTML` and `textContent`?** — `innerHTML` parses HTML and can cause XSS. `textContent` treats input as plain text — safe and faster.

5. **What is event bubbling?** — After an event fires on the target element, it propagates up through all ancestor elements.

### Intermediate Level
6. **What is event delegation and why is it better?** — Attaching one listener to a parent instead of multiple listeners to children. Better for performance and handles dynamic elements automatically.

7. **Explain the difference between `event.target` and `event.currentTarget`.** — `target` is where the event originated; `currentTarget` is the element with the listener.

8. **What is the difference between a live HTMLCollection and a static NodeList?** — HTMLCollection auto-updates when DOM changes; static NodeList (from querySelectorAll) is a snapshot.

9. **What is `closest()` and when would you use it?** — Traverses upward through ancestors to find first match of a CSS selector. Used in event delegation to find the relevant container element.

10. **What is the difference between `mouseover` and `mouseenter`?** — `mouseover` bubbles and fires when entering child elements; `mouseenter` doesn't bubble and only fires when the mouse enters the element itself.

### Advanced Level
11. **Explain the three phases of DOM event propagation.** — Capture (top→down), Target (at element), Bubble (bottom→up).

12. **What is layout thrashing and how do you prevent it?** — Alternating reads (offsetWidth) and writes (style changes) forces repeated synchronous reflows. Prevent by batching all reads first, then all writes.

13. **How does `DocumentFragment` improve performance?** — It's an in-memory node container not attached to the DOM. Building nodes in it then inserting all at once triggers one reflow instead of N.

14. **What is `requestAnimationFrame` and why prefer it over `setInterval` for animations?** — rAF syncs with the browser's repaint cycle (60fps), automatically pauses when tab is hidden, and provides a high-res timestamp.

15. **Explain Intersection Observer vs scroll event.** — Scroll events fire continuously (60+/sec); IntersectionObserver fires only when intersection state changes. Much more performant and avoids synchronous layout reads.

### Senior/Tricky Level
16. **Why can't you remove an anonymous function added via addEventListener?** — `removeEventListener` requires the exact same function reference. Anonymous functions create new references each time.

17. **What happens if you iterate over a live HTMLCollection while modifying the DOM?** — Items can be skipped or infinite loops can occur since the collection updates in real time. Convert to array first.

18. **In event delegation, a user clicks a `<span>` inside an `<li>`. How do you get the `<li>`?** — Use `e.target.closest('li')` to traverse upward to find the li.

19. **What is the difference between `stopPropagation` and `stopImmediatePropagation`?** — Both stop event bubbling, but `stopImmediatePropagation` also prevents other handlers on the SAME element from running.

20. **When would you use event capturing over bubbling?** — For intercepting events before they reach the target (logging, access control, focus trapping in modals).

### React-Relevant Questions
21. **React uses synthetic events. How are they different from native DOM events?** — React wraps native events in SyntheticEvent objects for cross-browser consistency. They're pooled for performance (in older React) and have the same interface as native events.

22. **Why doesn't React use event delegation on every element?** — React attaches a single event listener at the root container, using its own internal event delegation system.

23. **Can you use `addEventListener` alongside React's `onClick`?** — Yes, but be careful about conflicts. React's events are in the bubble phase at the root. Manual listeners closer to the target fire first.

24. **What is the equivalent of DOMContentLoaded in React?** — `useEffect(() => { /* ... */ }, [])` — runs after component mounts (DOM is ready).

25. **How would you implement the IntersectionObserver pattern in React?** — Use a custom hook with `useEffect` to create the observer on mount and `disconnect` it on cleanup (return function from useEffect).

---

## 5 Output Exercises

### Exercise 1 — Bubbling
```javascript
// HTML:
// <div id="A">
//   <div id="B">
//     <div id="C"></div>
//   </div>
// </div>

document.getElementById('A').addEventListener('click', () => console.log('A'));
document.getElementById('B').addEventListener('click', () => console.log('B'));
document.getElementById('C').addEventListener('click', (e) => {
  console.log('C');
  e.stopPropagation();
});

document.getElementById('A').click(); // What is the output?
document.getElementById('C').click(); // What is the output?
```
**Answer:**
- `A.click()` → `"A"` (no bubbling siblings)
- `C.click()` → `"C"` only (stopPropagation prevents B and A)

---

### Exercise 2 — Live vs Static
```javascript
const live = document.getElementsByClassName('box');
const static_ = document.querySelectorAll('.box');

console.log(live.length);    // 2
console.log(static_.length); // 2

const newDiv = document.createElement('div');
newDiv.className = 'box';
document.body.appendChild(newDiv);

console.log(live.length);    // ?
console.log(static_.length); // ?
```
**Answer:** `live.length` → `3` | `static_.length` → `2`

---

### Exercise 3 — Event Object
```javascript
document.body.addEventListener('click', function(e) {
  console.log(e.target === e.currentTarget);
});

document.querySelector('p').addEventListener('click', function(e) {
  console.log(e.target === e.currentTarget);
});
```
**If you click the `<p>` element:**
- First output: `false` (target=p, currentTarget=body)
- Second output: `true` (target=p, currentTarget=p)

---

### Exercise 4 — classList
```javascript
const el = document.createElement('div');
el.className = 'foo bar';

el.classList.add('baz');
el.classList.remove('foo');
el.classList.toggle('bar');
el.classList.toggle('new');

console.log(el.className);
```
**Answer:** `"baz new"` (bar was removed by toggle, new was added by toggle, foo was removed)

---

### Exercise 5 — Custom Event
```javascript
let count = 0;

document.addEventListener('increment', (e) => {
  count += e.detail.amount;
  console.log('Count:', count);
});

document.dispatchEvent(new CustomEvent('increment', { detail: { amount: 5 } }));
document.dispatchEvent(new CustomEvent('increment', { detail: { amount: 3 } }));
document.dispatchEvent(new CustomEvent('increment', { detail: { amount: -2 } }));

console.log('Final:', count);
```
**Output:**
```
Count: 5
Count: 8
Count: 6
Final: 6
```

---

## 5 Coding Exercises

### Coding Exercise 1 — Build a Todo App with Event Delegation
**Task:** Build a functional todo list:
- Add items via input + button
- Delete individual items (event delegation)
- Toggle completion state on click
- Count shows remaining items

```javascript
// Solution:
(function() {
  const input = document.getElementById('todo-input');
  const addBtn = document.getElementById('add-btn');
  const list = document.getElementById('todo-list');
  const countEl = document.getElementById('remaining-count');
  let todos = [];

  function updateCount() {
    const remaining = todos.filter(t => !t.done).length;
    countEl.textContent = `${remaining} item(s) remaining`;
  }

  function renderTodo(todo) {
    const li = document.createElement('li');
    li.dataset.id = todo.id;
    li.className = todo.done ? 'done' : '';
    li.innerHTML = `
      <span class="text">${todo.text}</span>
      <button class="delete" data-action="delete">✕</button>
    `;
    list.appendChild(li);
  }

  addBtn.addEventListener('click', () => {
    const text = input.value.trim();
    if (!text) return;
    const todo = { id: Date.now(), text, done: false };
    todos.push(todo);
    renderTodo(todo);
    input.value = '';
    updateCount();
  });

  list.addEventListener('click', (e) => {
    const li = e.target.closest('li');
    if (!li) return;
    const id = Number(li.dataset.id);

    if (e.target.matches('[data-action="delete"]')) {
      todos = todos.filter(t => t.id !== id);
      li.remove();
    } else if (e.target.matches('.text')) {
      const todo = todos.find(t => t.id === id);
      todo.done = !todo.done;
      li.classList.toggle('done');
    }
    updateCount();
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addBtn.click();
  });
})();
```

---

### Coding Exercise 2 — Implement Infinite Scroll with IntersectionObserver
**Task:** Fetch paginated data when the user scrolls near the bottom.

```javascript
async function initInfiniteScroll() {
  let page = 1;
  let isLoading = false;
  const container = document.getElementById('content');
  const sentinel = document.getElementById('scroll-sentinel');

  async function loadPage(pageNum) {
    const response = await fetch(`/api/posts?page=${pageNum}&limit=10`);
    return response.json();
  }

  function renderPosts(posts) {
    posts.forEach(post => {
      const card = document.createElement('article');
      card.className = 'post-card';
      card.innerHTML = `<h3>${post.title}</h3><p>${post.body}</p>`;
      container.insertBefore(card, sentinel);
    });
  }

  const observer = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isLoading) {
      isLoading = true;
      sentinel.textContent = 'Loading...';

      const posts = await loadPage(page);

      if (posts.length === 0) {
        sentinel.textContent = 'No more posts.';
        observer.disconnect();
        return;
      }

      renderPosts(posts);
      page++;
      sentinel.textContent = '';
      isLoading = false;
    }
  }, { rootMargin: '200px' });

  observer.observe(sentinel);
}

initInfiniteScroll();
```

---

### Coding Exercise 3 — Modal with Focus Trap and Keyboard Support
**Task:** A fully accessible modal that:
- Opens on button click
- Closes on Escape or overlay click
- Traps focus inside when open

```javascript
function createModal() {
  const modal = document.getElementById('modal');
  const overlay = document.getElementById('overlay');
  const openBtn = document.getElementById('open-modal');
  const closeBtn = document.getElementById('close-modal');

  const focusableSelectors = 'button, input, select, textarea, a[href], [tabindex]:not([tabindex="-1"])';

  function openModal() {
    modal.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // prevent background scroll

    // Focus first focusable element
    const first = modal.querySelector(focusableSelectors);
    if (first) first.focus();

    // Trap focus with keyboard listener
    modal.addEventListener('keydown', trapFocus);
    document.addEventListener('keydown', handleEscape);
  }

  function closeModal() {
    modal.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    modal.removeEventListener('keydown', trapFocus);
    document.removeEventListener('keydown', handleEscape);
    openBtn.focus(); // return focus to trigger
  }

  function trapFocus(e) {
    if (e.key !== 'Tab') return;
    const focusables = [...modal.querySelectorAll(focusableSelectors)];
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus(); // wrap to end
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus(); // wrap to beginning
    }
  }

  function handleEscape(e) {
    if (e.key === 'Escape') closeModal();
  }

  openBtn.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
}

createModal();
```

---

### Coding Exercise 4 — Drag and Drop (Pure JS)
**Task:** Implement drag and drop reordering of list items.

```javascript
function initDragDrop() {
  const list = document.getElementById('sortable-list');
  let draggedItem = null;

  list.addEventListener('dragstart', (e) => {
    draggedItem = e.target.closest('li');
    draggedItem.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
  });

  list.addEventListener('dragend', () => {
    draggedItem.classList.remove('dragging');
    draggedItem = null;
    list.querySelectorAll('li').forEach(li => li.classList.remove('drag-over'));
  });

  list.addEventListener('dragover', (e) => {
    e.preventDefault(); // allow dropping
    const target = e.target.closest('li');
    if (!target || target === draggedItem) return;

    list.querySelectorAll('li').forEach(li => li.classList.remove('drag-over'));
    target.classList.add('drag-over');

    // Calculate if dragging to before or after target
    const rect = target.getBoundingClientRect();
    const midY = rect.top + rect.height / 2;
    if (e.clientY < midY) {
      list.insertBefore(draggedItem, target);
    } else {
      list.insertBefore(draggedItem, target.nextSibling);
    }
  });

  list.addEventListener('drop', (e) => {
    e.preventDefault();
  });
}

initDragDrop();
```

---

### Coding Exercise 5 — Real-Time Search Filter with Debounce
**Task:** Filter a list of items as user types, with debounce.

```javascript
function initSearch() {
  const searchInput = document.getElementById('search-input');
  const itemList = document.getElementById('item-list');
  const items = [...itemList.querySelectorAll('li')]; // static snapshot

  function debounce(fn, delay) {
    let timer;
    return function(...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  function filterItems(query) {
    const lower = query.toLowerCase().trim();

    items.forEach(item => {
      const text = item.textContent.toLowerCase();
      const matches = text.includes(lower);
      item.style.display = matches ? '' : 'none';
      // Highlight matching text
      if (lower && matches) {
        item.innerHTML = item.textContent.replace(
          new RegExp(`(${lower})`, 'gi'),
          '<mark>$1</mark>'
        );
      } else {
        item.textContent = item.textContent; // remove marks
      }
    });

    const visible = items.filter(i => i.style.display !== 'none').length;
    document.getElementById('result-count').textContent =
      `Showing ${visible} of ${items.length} items`;
  }

  searchInput.addEventListener('input', debounce((e) => {
    filterItems(e.target.value);
  }, 250));
}

initSearch();
```

---

## 10 Multiple Choice Questions (MCQs)

**1.** Which method returns a LIVE HTMLCollection?
- a) `document.querySelectorAll('.item')`
- b) `document.getElementsByClassName('item')` ✅
- c) `Array.from(document.querySelectorAll('.item'))`
- d) `[...document.querySelectorAll('.item')]`

**2.** What is the correct order of DOM event phases?
- a) Target → Capture → Bubble
- b) Bubble → Target → Capture
- c) Capture → Target → Bubble ✅
- d) Capture → Bubble → Target

**3.** Which property gives you the element that HAS the event listener (not the element that was clicked)?
- a) `event.target`
- b) `event.currentTarget` ✅
- c) `event.relatedTarget`
- d) `event.srcElement`

**4.** What does `element.closest('.parent')` do?
- a) Finds the first `.parent` descendant
- b) Finds the first `.parent` sibling
- c) Traverses UP the DOM and returns first `.parent` ancestor ✅
- d) Searches the entire document for `.parent`

**5.** Which approach causes layout thrashing?
- a) Reading all widths first, then setting all widths
- b) Using `requestAnimationFrame`
- c) Alternating reads (`offsetWidth`) and writes (`style.width`) ✅
- d) Using `DocumentFragment`

**6.** What is the `detail` property of a `CustomEvent`?
- a) A description of the event type
- b) Custom data passed with the event ✅
- c) A boolean indicating if the event bubbles
- d) The DOM level of the event

**7.** Why is `{ passive: true }` useful for scroll event listeners?
- a) It makes the listener fire faster
- b) It prevents the default scroll behavior
- c) It tells the browser the listener won't call preventDefault(), allowing smoother scrolling ✅
- d) It makes the event fire only once

**8.** What does `e.stopImmediatePropagation()` do differently from `e.stopPropagation()`?
- a) Nothing — they're identical
- b) It also prevents other handlers on the SAME element from running ✅
- c) It prevents the event from reaching the target
- d) It cancels the event completely

**9.** IntersectionObserver's `rootMargin` property allows you to:
- a) Set the margin of the element being observed
- b) Expand or shrink the effective viewport boundary for triggering ✅
- c) Set the minimum percentage of intersection
- d) Define the root element's CSS margin

**10.** Which of these triggers a browser REFLOW (layout recalculation)?
- a) `element.style.color = 'red'`
- b) `element.style.opacity = '0.5'`
- c) `element.style.transform = 'scale(2)'`
- d) `element.offsetWidth` ← reading geometry property ✅

---

## Revision Notes & Interview Cheat Sheet

```
╔══════════════════════════════════════════════════════════════════╗
║           CHAPTER 6 — DOM & EVENTS CHEAT SHEET                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  SELECTION:                                                      ║
║  getElementById    → fastest, ID only, returns Element/null      ║
║  querySelector     → first match, any CSS selector               ║
║  querySelectorAll  → all matches, static NodeList                ║
║  getElementsBy*    → live HTMLCollection                         ║
║                                                                  ║
║  CONTENT:                                                        ║
║  textContent  → safe, fast, no HTML parsing                      ║
║  innerText    → CSS-aware, triggers reflow                       ║
║  innerHTML    → parses HTML, XSS risk with user input            ║
║                                                                  ║
║  CLASSES:                                                        ║
║  classList.add/remove/toggle/contains/replace                    ║
║                                                                  ║
║  TRAVERSAL (use Element versions to skip text nodes):            ║
║  firstElementChild, lastElementChild                             ║
║  nextElementSibling, previousElementSibling                      ║
║  parentElement                                                   ║
║  closest(selector) — searches upward                             ║
║  matches(selector) — tests current element                       ║
║  contains(node)    — checks if descendant                        ║
║                                                                  ║
║  INSERTION (modern methods):                                     ║
║  append, prepend, before, after, replaceWith, remove             ║
║  insertAdjacentElement/HTML (beforebegin/afterbegin/             ║
║                              beforeend/afterend)                 ║
║                                                                  ║
║  EVENTS — KEY RULES:                                             ║
║  • Bubbling: inner→outer (default)                               ║
║  • Capturing: outer→inner ({ capture: true })                    ║
║  • target = origin; currentTarget = listener owner              ║
║  • stopPropagation → stops bubbling                              ║
║  • stopImmediatePropagation → stops bubbling + same-el handlers  ║
║  • preventDefault → stops browser default action                 ║
║                                                                  ║
║  DELEGATION:                                                     ║
║  • Listen on parent, use e.target.closest() to identify          ║
║  • Handles dynamic elements automatically                        ║
║  • Use data-action attributes for clean routing                  ║
║                                                                  ║
║  PERFORMANCE:                                                    ║
║  • Read → Write (never alternate)                                ║
║  • DocumentFragment for bulk insertions                          ║
║  • requestAnimationFrame for animations                          ║
║  • IntersectionObserver for scroll-based features                ║
║  • Debounce for input; Throttle for scroll/resize                ║
║  • passive: true for scroll/touch listeners                      ║
║  • Virtual scroll for 1000+ items                                ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Bad Practices to NEVER Do

```javascript
// ❌ 1. Using innerHTML with user input (XSS)
div.innerHTML = userInput; // NEVER!

// ❌ 2. Attaching event listeners in a loop to every element
items.forEach(item => item.addEventListener('click', handler)); // use delegation

// ❌ 3. Not checking for null after querySelector
const el = document.querySelector('.maybe-exists');
el.style.color = 'red'; // TypeError if el is null! Always check first.

// ❌ 4. Using anonymous functions with removeEventListener
el.addEventListener('click', () => doSomething());
el.removeEventListener('click', () => doSomething()); // FAILS — different ref

// ❌ 5. Reading layout in animation loops
function animate() {
  const height = el.offsetHeight; // forces layout EVERY frame!
  el.style.top = height + 'px';
  requestAnimationFrame(animate);
}

// ❌ 6. Not using passive for scroll listeners
window.addEventListener('scroll', heavyHandler); // blocks scroll thread

// ❌ 7. Not disconnecting observers
// Always disconnect IntersectionObserver, MutationObserver, ResizeObserver
// when the component/page section is done — prevents memory leaks

// ❌ 8. Querying the DOM inside a loop
for (let i = 0; i < 1000; i++) {
  document.querySelector('#list').appendChild(el); // queries DOM 1000 times!
}
// Cache it: const list = document.querySelector('#list');
```

---

## Best Practices Summary

```javascript
// ✅ 1. Cache DOM queries
const btn = document.getElementById('myBtn'); // cache once

// ✅ 2. Use textContent for safe text insertion
el.textContent = userInput; // safe from XSS

// ✅ 3. Use DocumentFragment for bulk insertions
const frag = document.createDocumentFragment();

// ✅ 4. Use event delegation for lists
parent.addEventListener('click', (e) => {
  const item = e.target.closest('.item');
  if (item) handleItem(item);
});

// ✅ 5. Named functions for removable listeners
el.addEventListener('click', handleClick);
// ... later:
el.removeEventListener('click', handleClick);

// ✅ 6. Passive scroll listeners
window.addEventListener('scroll', handler, { passive: true });

// ✅ 7. Use IntersectionObserver instead of scroll events for visibility
// ✅ 8. Debounce search input; Throttle scroll/resize
// ✅ 9. Use CSS transforms/opacity for animations (GPU-accelerated)
// ✅ 10. Disconnect observers on cleanup
observer.disconnect();
```

---

*End of Chapter 6 — The DOM & Events*

> **Next Chapter Preview → Chapter 7: Asynchronous JavaScript — Callbacks, Promises, async/await, Fetch API, Error Handling, and more.**
