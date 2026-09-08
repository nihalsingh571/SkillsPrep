# Arrays, Strings, and Hashing in JavaScript for DSA

This is the most critical chapter for mastering DSA in JavaScript. Arrays and Strings are the foundation of 80% of all algorithmic problems, and Hashing (Maps/Sets) provides the necessary O(1) lookups to optimize them.

---

## 1. JavaScript Arrays vs Java Arrays

In Java, arrays are fixed in size and uniform in type. If you need a dynamic array, you use an `ArrayList`.
In JavaScript, there is only one Array object, and it acts like an `ArrayList` by default. It is dynamic, resizable, and can hold mixed types (though for DSA, you should keep types uniform).

### Initialization

**Java:**
```java
// Fixed size, initialized to 0
int[] arr = new int[5]; 

// Literals
int[] arr = {1, 2, 3};
```

**JavaScript:**
```javascript
// Dynamic array initialized with elements
let arr = [1, 2, 3];

// Initialize an array of a specific size, filled with a default value (e.g., 0)
let arr2 = new Array(5).fill(0); // [0, 0, 0, 0, 0]
```

*Important:* If you just do `new Array(5)`, it creates an array of 5 "empty slots" (which act like `undefined`), which can cause issues with mapping. Always chain `.fill()` when initializing sizes.

---

## 2. All Array Operations with Complexity

Here is the definitive guide to JavaScript array methods, their Java equivalents, and their Time Complexities.

### Adding / Removing Elements at the END (Fast)

- **`push(x)`**
  - **Purpose:** Adds element to the end.
  - **Java Equivalent:** `list.add(x)`
  - **Complexity:** O(1) amortized
  - **Example:** `arr.push(4);`

- **`pop()`**
  - **Purpose:** Removes and returns the last element.
  - **Java Equivalent:** `list.remove(list.size() - 1)`
  - **Complexity:** O(1)
  - **Example:** `let last = arr.pop();`

### Adding / Removing Elements at the BEGINNING (SLOW - AVOID!)

Unlike Java's `LinkedList`, a JS Array is backed by continuous memory. Modifying the front requires shifting all other elements.

- **`shift()`**
  - **Purpose:** Removes and returns the first element.
  - **Java Equivalent:** `list.remove(0)`
  - **Complexity:** **O(n) SLOW**
  - **Mistake:** Using `shift()` in a tight loop to simulate a Queue. It will cause TLE (Time Limit Exceeded). For a real queue in JS, you must build a custom linked list or use an index pointer.

- **`unshift(x)`**
  - **Purpose:** Adds element to the front.
  - **Java Equivalent:** `list.add(0, x)`
  - **Complexity:** **O(n) SLOW**

### Searching and Slicing

- **`indexOf(x)`**
  - **Purpose:** Returns the first index of `x`, or `-1` if not found.
  - **Java Equivalent:** `list.indexOf(x)`
  - **Complexity:** O(n)
  
- **`includes(x)`**
  - **Purpose:** Returns boolean true if `x` is in array.
  - **Java Equivalent:** `list.contains(x)`
  - **Complexity:** O(n)

- **`slice(start, end)`**
  - **Purpose:** Returns a shallow copy of a portion of an array (end not included).
  - **Java Equivalent:** `Arrays.copyOfRange(arr, start, end)`
  - **Complexity:** O(n) where n is the length of the slice.
  - **Example:** `let sub = arr.slice(1, 3);`

### Mutation and Reordering

- **`splice(start, deleteCount, ...items)`**
  - **Purpose:** Extremely powerful, highly dangerous. Adds/removes items *in place*.
  - **Complexity:** O(n) due to shifting elements.
  - **Example:** `arr.splice(2, 1)` (Removes 1 element at index 2).

- **`reverse()`**
  - **Purpose:** Reverses the array **IN PLACE**. It mutates the original array and returns it.
  - **Java Equivalent:** `Collections.reverse(list)`
  - **Complexity:** O(n)

- **`fill(val, start, end)`**
  - **Purpose:** Fills elements with a static value.
  - **Java Equivalent:** `Arrays.fill(arr, val)`
  - **Complexity:** O(n)

### Transformations

- **`join(separator)`**
  - **Purpose:** Joins elements into a single string.
  - **Java Equivalent:** `String.join(sep, list)`
  - **Complexity:** O(n)
  - **Example:** `[1, 2, 3].join('-')` // "1-2-3"

- **`concat(arr2)`**
  - **Purpose:** Merges arrays and returns a NEW array.
  - **Complexity:** O(n)

- **`flat()`**
  - **Purpose:** Flattens nested arrays.
  - **Complexity:** O(n)

- **`Array.from()`**
  - **Purpose:** Creates arrays from iterables or custom lengths.
  - **Example:** `Array.from({length: n}, (_, i) => i);` // Creates [0, 1, ..., n-1]

---

## 3. Array Copying — CRITICAL

In both Java and JS, arrays are Objects. Assigning an array to a new variable just copies the reference.

**WRONG: Reference Copy**
```javascript
let a = [1, 2, 3];
let b = a;  // b points to the SAME array in memory!
b[0] = 99;
console.log(a[0]); // 99 (a was modified!)
```

**CORRECT: Shallow Copy**
There are three common ways to safely shallow copy an array:
```javascript
let a = [1, 2, 3];

let b = [...a];          // 1. Spread operator (Most modern/preferred)
let c = a.slice();       // 2. Slice with no arguments
let d = Array.from(a);   // 3. Array.from
```

**Deep Copy for 2D Arrays:**
Shallow copies only copy the first level. For matrices, use map:
```javascript
let copy = matrix.map(row => [...row]);
```

---

## 4. 2D Arrays — VERY IMPORTANT

Creating matrices correctly is one of the most common pitfalls for Java developers moving to JS.

In Java: `int[][] matrix = new int[rows][cols];`

In JavaScript, **DO NOT do this (WRONG WAY):**
```javascript
// BUG! Creates an array of n elements, but fills them all with a REFERENCE to the SAME inner array.
const matrix = Array(n).fill(new Array(m).fill(0));

matrix[0][0] = 1;
console.log(matrix[1][0]); // 1! Modifying row 0 modified ALL rows!
```

**CORRECT WAY:**
You must instantiate a new array for every single row. The cleanest way is using `Array.from`:
```javascript
// Array.from takes a length, and a mapping function to execute for each element.
const matrix = Array.from({length: n}, () => new Array(m).fill(0));
```

### Matrix Traversal
```javascript
for (let r = 0; r < matrix.length; r++) {
    for (let c = 0; c < matrix[0].length; c++) {
        console.log(matrix[r][c]);
    }
}
```

---

## 5. Strings

Strings in JavaScript are **immutable**, exactly like Java. Any string manipulation method returns a NEW string.

### Accessing Characters
```javascript
// Java
char c = s.charAt(i);
int len = s.length();

// JavaScript
const c1 = s[i];       // Bracket notation is preferred
const c2 = s.charAt(i);
const len = s.length;  // Property, NO parentheses!
```

### Important String Methods

- **`.split(separator)`**
  - Extremely useful for turning a string into an array of characters.
  - `s.split('')` // "hello" -> ['h', 'e', 'l', 'l', 'o']
- **`.join(separator)`** (Array method used with strings)
  - Turns char array back to string.
  - `arr.join('')`
- **`.slice(start, end)`** / **`.substring(start, end)`**
  - Equivalent to Java's `substring`. Extracts a part of a string.
- **`.includes(sub)`**
  - O(n). Returns boolean.
- **`.indexOf(sub)`**
  - O(n). Returns starting index or -1.
- **`.toLowerCase()`** / **`.toUpperCase()`**
- **`.trim()`**
  - Removes leading/trailing whitespace.
- **`.replace(old, new)`**
  - Replaces ONLY the first occurrence!
- **`.replaceAll(old, new)`**
  - Replaces all occurrences.

### String Building Pattern (Performance Critical)
In Java, you use `StringBuilder` to avoid O(n^2) concatenation in a loop.
In JavaScript, modern V8 engines are highly optimized for `+=` string concatenation, BUT the safest and most standard pattern for large concatenations is to push to an array and `join`.

```javascript
// Safe and Fast String Building
const parts = [];
for (let c of arr) {
    parts.push(c);
}
const result = parts.join(''); // O(n)
```

### Common DSA String Patterns

**Palindrome Check (Two Pointers):**
```javascript
function isPalindrome(s) {
    let l = 0, r = s.length - 1;
    while (l < r) {
        if (s[l] !== s[r]) return false;
        l++;
        r--;
    }
    return true;
}
```

**String Reversal (Using Array Methods):**
```javascript
const reversed = s.split('').reverse().join('');
```

---

## 6. JavaScript Map (HashMap equivalent)

In Java, you rely heavily on `HashMap`. In JS, the exact equivalent is `Map`.

**Initialization:**
```java
// Java
HashMap<Integer, Integer> map = new HashMap<>();
```
```javascript
// JavaScript
const map = new Map();
```

### Map Methods vs Java

- **`new Map()`** — Java: `new HashMap<>()`
- **`.set(key, val)`** — Java: `.put(key, val)`
- **`.get(key)`** — Returns the value, or `undefined` if missing (Java: returns `null`).
- **`.has(key)`** — Java: `.containsKey(key)`. Returns boolean.
- **`.delete(key)`** — Java: `.remove(key)`
- **`.size`** — Java: `.size()` (Note: property, no parentheses)
- **`.clear()`** — Java: `.clear()`

### Idiomatic Counting (The `getOrDefault` Equivalent)
In Java:
```java
map.put(x, map.getOrDefault(x, 0) + 1);
```
In JavaScript:
```javascript
map.set(x, (map.get(x) || 0) + 1);
```
*How it works:* If `map.get(x)` is undefined (falsy), the `||` operator falls back to `0`. Then we add `1`.

### Iterating over a Map
Use `for...of` with array destructuring:
```javascript
for (const [key, val] of map) {
    console.log(`Key: ${key}, Value: ${val}`);
}
```

### Map vs Object for DSA
Before ES6, JS developers used plain Objects `{}` as hashmaps. You will still see this, but `Map` is strictly better for algorithmic problems.

| Feature | `Map` | `Object {}` |
| :--- | :--- | :--- |
| **Key Type** | ANY type (numbers, nodes, etc.) | Strings or Symbols ONLY |
| **Order** | Preserves insertion order | Iteration order not guaranteed |
| **Size checking** | `map.size` (O(1)) | `Object.keys(obj).length` (O(n)) |
| **Add/Remove Perf** | Highly optimized for dynamic usage | Slower for frequent additions/deletions |
| **DSA Verdict** | **Always use Map for non-string keys** | Okay for quick string-frequency counting |

---

## 7. JavaScript Set (HashSet equivalent)

Used for keeping track of unique elements or visited nodes.

```java
// Java
HashSet<Integer> set = new HashSet<>();
```
```javascript
// JavaScript
const set = new Set();
```

### Set Methods

- **`new Set()`** / **`new Set(iterable)`**
- **`.add(val)`** — Java: `.add()`
- **`.has(val)`** — Java: `.contains()`
- **`.delete(val)`** — Java: `.remove()`
- **`.size`** — Java: `.size()`
- **`.clear()`**

### Powerful Set Patterns

**Remove Duplicates from an Array:**
```javascript
const arr = [1, 2, 2, 3];
const uniqueArr = [...new Set(arr)]; // [1, 2, 3]
```

**Set Operations:**
JavaScript does not have built-in set operations (union, intersection) yet (though they are coming in newer ES standards). For now, use arrays and filters:

```javascript
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);

// Intersection
const intersection = new Set([...a].filter(x => b.has(x)));

// Union
const union = new Set([...a, ...b]);

// Difference (A - B)
const difference = new Set([...a].filter(x => !b.has(x)));
```

---

## 8. Objects for DSA

While `Map` is preferred, plain objects are still highly prevalent for character counting because they are syntactically shorter to write.

```javascript
// Character frequency counter using an Object
const freq = {};
for (const char of s) {
    freq[char] = (freq[char] || 0) + 1;
}

// Iterating over Object keys/values
for (const key in freq) {
    console.log(`${key} appears ${freq[key]} times`);
}
```

*Rule of thumb:* If keys are characters or strings, `{}` is fine. If keys are integers, arrays, or objects, use `Map`.

---

## 9. Higher-Order Functions for DSA

JavaScript arrays come with functional methods that take callbacks. They are elegant, but be cautious: a simple `for` loop is often faster. Use these when performance is not the ultimate bottleneck, or for clean code.

- **`arr.map(fn)`**: Transforms every element, returns a NEW array. O(n).
  ```javascript
  const doubled = arr.map(x => x * 2);
  ```
- **`arr.filter(fn)`**: Keeps elements that return true, returns NEW array. O(n).
  ```javascript
  const positives = arr.filter(x => x > 0);
  ```
- **`arr.reduce(fn, initialVal)`**: Accumulates a value. O(n).
  ```javascript
  const sum = arr.reduce((acc, curr) => acc + curr, 0);
  ```
- **`arr.find(fn)`**: Returns the FIRST element that matches, or undefined.
- **`arr.findIndex(fn)`**: Returns FIRST index, or -1.
- **`arr.some(fn)`**: Returns true if AT LEAST ONE element matches.
- **`arr.every(fn)`**: Returns true if ALL elements match.

---

## 10. Destructuring and Spread for DSA

These syntactical features make JS highly expressive for swapping and merging.

**Array Destructuring:**
```javascript
const arr = [10, 20];
const [a, b] = arr; // a = 10, b = 20

// Skipping elements
const [first, , third] = [1, 2, 3];
```

**Swapping Variables (No Temp Needed!):**
In Java, swapping requires a `temp` variable. In JS:
```javascript
let i = 0, j = 1;
[arr[i], arr[j]] = [arr[j], arr[i]];
```

**Spread Operator (`...`):**
Expands an array into individual elements.
```javascript
const merged = [...arr1, ...arr2]; // Better than concat!
const copy = [...arr1];
```

---

## 11. Complete Chapter Practice Problems

To solidify your understanding of Arrays, Strings, and Hashing in JavaScript, practice these standard patterns on LeetCode/HackerRank:

1. Two Sum (Using Map)
2. Valid Anagram (Using frequency Object/Array)
3. Group Anagrams (Map + String Sorting)
4. Top K Frequent Elements (Map + Bucket Sort)
5. Valid Palindrome (Two Pointers + String methods)
6. Longest Consecutive Sequence (Using Set)
7. Subarray Sum Equals K (Prefix Sum + Map)
8. Longest Substring Without Repeating Characters (Sliding Window + Set)
9. Product of Array Except Self (Prefix/Suffix Arrays)
10. Spiral Matrix (2D Array Traversal)

*End of Chapter 2.*
