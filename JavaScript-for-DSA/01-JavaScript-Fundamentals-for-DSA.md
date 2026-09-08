# JavaScript Fundamentals for DSA: A Java Developer's Guide

Welcome to the comprehensive guide for transitioning from Java to JavaScript for Data Structures and Algorithms (DSA) and Competitive Programming (CP). 
If you are coming from Java, you already know how to think algorithmically. This guide will teach you how to translate that thinking into JavaScript effectively, highlighting the pitfalls and features unique to the language.

---

## 1. JavaScript Basics

### What is JavaScript?
Many developers think of JavaScript strictly as a language for the web browser, used for DOM manipulation and web development. However, for DSA, we use JavaScript in a completely different environment: **Node.js**.
Node.js is a runtime that allows you to execute JavaScript code on your machine, just like the Java Virtual Machine (JVM) runs Java code. You don't need HTML, CSS, or a browser.

### Running JavaScript
In Java, you compile and run your code like this:
```bash
javac Solution.java
java Solution
```

In JavaScript (via Node.js), there is no separate compilation step (it is interpreted/JIT-compiled). You run the file directly:
```bash
node solution.js
```

### Statements, Semicolons, and Comments
Like Java, JavaScript uses C-style syntax.

**Comments:**
```javascript
// This is a single-line comment (same as Java)

/*
 * This is a multi-line comment
 * (same as Java)
 */
```

**Semicolons:**
In Java, semicolons at the end of statements are mandatory. If you miss one, the code won't compile.
In JavaScript, semicolons are *optional* because of a feature called Automatic Semicolon Insertion (ASI). However, for DSA, **it is highly recommended to always use semicolons** to avoid subtle bugs, especially when minifying or running complex scripts.

```javascript
// Good practice
let x = 10;
let y = 20;

// ASI might misinterpret this if you omit semicolons in edge cases
```

### The Global Object
In Java, everything must be inside a class. 
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

In JavaScript, you can write code at the top level. There is no `main` method required.
```javascript
// solution.js
console.log("Hello"); // Executes immediately when run with node
```

---

## 2. Variables — let, const, var

In Java, you declare variables with explicit types (`int`, `double`, `String`, etc.). 
In JavaScript, variables are dynamically typed. You declare them using `let`, `const`, or `var`. The type is determined at runtime based on the value assigned.

### `let` - The Standard Variable
Use `let` for variables whose values will change (e.g., loop counters, accumulators).

```java
// Java
int x = 5;
x = 10;
```

```javascript
// JavaScript
let x = 5;
x = 10;
```

**Scope:** `let` is block-scoped, exactly like variables in Java.
```javascript
if (true) {
    let blockScoped = 5;
}
// console.log(blockScoped); // ReferenceError!
```

### `const` - The Constant
Use `const` for variables that should not be reassigned. This is the equivalent of `final` in Java.

```java
// Java
final int MAX_SIZE = 100;
// MAX_SIZE = 200; // Error
```

```javascript
// JavaScript
const MAX_SIZE = 100;
// MAX_SIZE = 200; // TypeError: Assignment to constant variable.
```

**Important Caveat for DSA:** `const` only prevents *reassignment* of the variable identifier. If the value is an object or array, the *contents* can still be mutated!

```javascript
const arr = [1, 2, 3];
arr.push(4); // Perfectly fine! arr is now [1, 2, 3, 4]
// arr = [5, 6]; // ERROR! Reassignment
```

### `var` - The Legacy Variable (AVOID)
Before modern JavaScript (ES6), `var` was the only way to declare variables. You should **never** use `var` for DSA because it introduces scope confusion.

**The Hoisting Gotcha:**
`var` is function-scoped, not block-scoped. Furthermore, its declaration is "hoisted" to the top of its scope.

```javascript
// Using let (Expected behavior)
console.log(a); // ReferenceError
let a = 5;

// Using var (Bizarre behavior)
console.log(b); // Prints 'undefined' (no error!)
var b = 5;
```

If you use `var` in a loop, it leaks outside the loop:
```javascript
for (var i = 0; i < 3; i++) {
    // ...
}
console.log(i); // Prints 3! The variable leaked out of the loop.
```
**Rule for DSA:** Always use `const` by default. If you know the value must change, use `let`. Never use `var`.

---

## 3. Data Types

JavaScript has a simpler type system compared to Java. Because it is dynamically typed, a single variable can hold a number, then a string, then a boolean.

### Number
In Java, you have `byte`, `short`, `int`, `long`, `float`, and `double`.
In JavaScript, there is only **one** numeric type: `Number`.
Under the hood, all JavaScript numbers are double-precision 64-bit floating-point format (IEEE 754).

```java
// Java
int i = 5;
double d = 5.5;
```

```javascript
// JavaScript
let i = 5;    // Type is Number
let d = 5.5;  // Type is Number
```

Because they are floating-point, integer division behaves differently!
```javascript
// Java: 5 / 2 = 2
// JavaScript:
console.log(5 / 2); // 2.5
```
To get integer division in JS, you must use `Math.floor()` or bitwise operators:
```javascript
console.log(Math.floor(5 / 2)); // 2
console.log(Math.trunc(5 / 2)); // 2
console.log(~~(5 / 2)); // 2 (Bitwise double NOT trick for positive numbers)
```

### String
Strings in JavaScript can be enclosed in single quotes, double quotes, or backticks.

```javascript
let s1 = "Hello";
let s2 = 'World';
let s3 = `Hello ${s2}`; // Template literal (string interpolation)
```

### Boolean
Just like Java, `true` and `false` (lowercase).

### null and undefined
In Java, uninitialized objects are `null`.
In JavaScript, there are two distinct types for "nothing":
1. `undefined`: The variable has been declared but has not yet been assigned a value.
2. `null`: An intentional absence of any object value.

```javascript
let a;
console.log(a); // undefined

let b = null;
console.log(b); // null
```

### BigInt
Because JavaScript uses 64-bit floats for all numbers, the maximum safe integer is `2^53 - 1`.
If your CP problem involves numbers larger than `9,007,199,254,740,991` (often the case when dealing with modulo `10^9 + 7` arithmetic over long sequences, or 64-bit integer inputs), you must use `BigInt`.

```javascript
let bigNum = 123456789012345678901234567890n; // append 'n'
let anotherBig = BigInt("123456789012345678901234567890");

// Note: You cannot mix BigInt and Number!
// let res = bigNum + 5; // TypeError
let res = bigNum + 5n; // Correct
```

### The `typeof` Operator
You can check a variable's type at runtime:
```javascript
console.log(typeof 42); // "number"
console.log(typeof 'hi'); // "string"
console.log(typeof true); // "boolean"
console.log(typeof undefined); // "undefined"
console.log(typeof null); // "object" (This is a famous historical bug in JS!)
```

### Implicit Type Coercion Pitfalls
JavaScript tries very hard to run your code, even if it means changing types automatically. This is dangerous for DSA!

```javascript
console.log("5" + 2); // "52" (String concatenation)
console.log("5" - 2); // 3 (Numeric subtraction)
console.log("5" * 2); // 10
```
**Takeaway:** Always explicitly convert your inputs to Numbers using `Number()` or `parseInt()` before performing arithmetic!

---

## 4. Operators

JavaScript has mostly the same operators as Java: `+`, `-`, `*`, `/`, `%`, `++`, `--`, `+=`, `-=`, etc.

### Comparison: The == vs === Trap (VERY IMPORTANT)

In Java, `==` compares primitives by value, and objects by reference.
In JavaScript, you have two sets of equality operators:

1. **Loose Equality (`==` and `!=`)**: Performs type coercion before comparing.
2. **Strict Equality (`===` and `!==`)**: Compares both type AND value. No coercion.

**Example of why `==` is dangerous:**
```javascript
console.log(5 == "5");   // true (The string "5" is coerced to a number)
console.log(0 == false); // true
console.log("" == 0);    // true
console.log(null == undefined); // true
```

**Always use `===` for DSA:**
```javascript
console.log(5 === "5");   // false (Different types)
console.log(0 === false); // false
console.log("" === 0);    // false
console.log(null === undefined); // false
```
For inequality, always use `!==` instead of `!=`.

### Modulo with Negative Numbers
Both Java and JavaScript handle the `%` operator identically with negative numbers, which often isn't the true mathematical modulo you want in CP.

```javascript
console.log(-5 % 3); // -2
```
In many DSA problems (like circular arrays or modular arithmetic), you need a positive modulo.
**The Fix:**
```javascript
let mod = ((x % n) + n) % n; 
console.log(((-5 % 3) + 3) % 3); // 1
```

### Logical Operators
`&&` (AND), `||` (OR), `!` (NOT).

JavaScript logical operators don't just return booleans; they return the actual values based on truthiness (short-circuit evaluation).
```javascript
let name = null;
// If name is falsy, assign "Guest"
let user = name || "Guest"; 
console.log(user); // "Guest"
```

---

## 5. Conditions

Control flow is virtually identical to Java.

```javascript
if (x > 10) {
    // ...
} else if (x === 10) {
    // ...
} else {
    // ...
}

// Switch statement (identical to Java)
switch (value) {
    case 1:
        break;
    default:
        break;
}
```

### Truthy and Falsy Values
In Java, an `if` statement requires a strict `boolean` expression (`if (x != 0)`).
In JavaScript, you can put ANY value in an `if` statement. It will be coerced to a boolean.

**Falsy Values (evaluate to `false`):**
1. `false`
2. `0`
3. `""` (empty string)
4. `null`
5. `undefined`
6. `NaN` (Not a Number)

**Truthy Values:**
Literally everything else.
- `"0"` (string with zero) is truthy!
- `[]` (empty array) is truthy!
- `{}` (empty object) is truthy!

```javascript
let arr = [];
if (arr) {
    console.log("This will print, because arrays are objects, and objects are truthy!");
}

// To check if an array is empty in JS:
if (arr.length === 0) {
    // Correct
}
```

---

## 6. Loops — VERY DETAILED

Loops in JavaScript look exactly like Java loops.

### The Classic `for` Loop
```java
// Java
for (int i = 0; i < n; i++) { ... }
```
```javascript
// JavaScript
for (let i = 0; i < n; i++) { ... }
```
*Crucial*: Always use `let` here. If you use `var`, the variable leaks. If you omit `let`, you create a global variable, which is a massive performance hit and scoping bug!

### `while` and `do-while`
Exactly the same as Java.
```javascript
let i = 0;
while (i < 10) {
    i++;
}
```

### The `for...of` Loop (For Arrays and Iterables)
This is the equivalent of Java's enhanced for loop (`for (int val : arr)`).
Use this when you need the values, but not the indices.

```javascript
const arr = [10, 20, 30];

// Java: for(int val : arr)
for (const val of arr) {
    console.log(val); // 10, 20, 30
}
```

### The `for...in` Loop (AVOID FOR ARRAYS)
`for...in` iterates over the *keys* (properties) of an object. If used on an array, it iterates over the string indices, which is terrible for performance and can include prototype properties!
```javascript
const arr = [10, 20, 30];

// BAD FOR ARRAYS!
for (const idx in arr) {
    console.log(idx); // Prints "0", "1", "2" as STRINGS!
    console.log(arr[idx]); // Works, but slower and risky.
}
```
**Rule:** Use `for...of` for arrays. Use `for...in` ONLY for plain objects.

### Loop Best Practices for DSA
- The classic `for (let i = 0; i < n; i++)` is usually the fastest execution-wise in V8 (the Node.js engine).
- Off-by-one errors are just as common. Always trace your boundaries.
- `break` and `continue` work exactly as they do in Java.

---

## 7. Functions

Functions in JavaScript are first-class citizens. You can pass them as arguments, return them, and assign them to variables.

### 1. Function Declaration (Classic)
This is most similar to a Java method. Function declarations are hoisted, meaning you can call them before they are defined in the file.

```javascript
// Hoisted: this works!
console.log(add(2, 3)); 

function add(a, b) {
    return a + b;
}
```

### 2. Arrow Functions (ES6)
Arrow functions are a more concise syntax. They are similar to Java's lambda expressions.
They are NOT hoisted. You must define them before you call them.

```javascript
const addArrow = (a, b) => {
    return a + b;
};

// Implicit return for single expressions:
const multiply = (a, b) => a * b;
```

**Which to use for DSA?**
Both are perfectly fine. Many CPers prefer standard function declarations for their main helper functions (like `dfs`, `binarySearch`) because hoisting allows you to put them at the bottom of the file out of the way. Arrow functions are highly preferred for passing inline callbacks (e.g., sorting).

### Default Parameters
```javascript
function greet(name = "Guest") {
    return `Hello ${name}`;
}
```

### Recursion
Recursion works exactly the same.
```javascript
function fib(n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
```
Note: JavaScript does not typically have tail-call optimization guaranteed in all engines, so deep recursion (e.g., depth > 10,000) will throw a "Maximum call stack size exceeded" error (StackOverflow in Java).

---

## 8. Input / Output for Competitive Programming (CRITICAL)

In Java, you usually use `Scanner` or `BufferedReader`.
In Node.js, I/O is completely different. The most robust way for CP platforms (Codeforces, LeetCode, HackerRank) is to read the entire input from standard input at once into a string, then parse it.

### The Standard Template
Save this template. You will use it for every CP problem.

```javascript
const fs = require('fs');

function solve() {
    // 1. Read all input from standard input (file descriptor 0)
    // .trim() removes trailing newlines
    // .split(/\s+/) splits by any whitespace (newlines, spaces, tabs)
    const input = fs.readFileSync(0, 'utf-8').trim().split(/\s+/);
    
    if (input.length === 0 || input[0] === "") return;

    let ptr = 0;
    
    // Helper function to get next token as a string
    function next() {
        return input[ptr++];
    }
    
    // Helper function to get next token as a number
    function nextInt() {
        return parseInt(input[ptr++], 10);
    }

    // --- YOUR LOGIC HERE ---
    
    // Example: Read T test cases
    const T = nextInt();
    for (let t = 0; t < T; t++) {
        const n = nextInt();
        const m = nextInt();
        
        // Read array of size n
        const arr = new Array(n);
        for (let i = 0; i < n; i++) {
            arr[i] = nextInt();
        }
        
        // Print output
        console.log(`Test case ${t+1}: n=${n}, m=${m}`);
    }
}

solve();
```

### Handling LeetCode vs HackerRank/Codeforces
- **LeetCode:** You only need to write the function signature (e.g., `function twoSum(nums, target)`). You `return` the answer. You do NOT use `fs.readFileSync` or `console.log` for output.
- **HackerRank / Codeforces:** You must read from `stdin` and print to `stdout` using `console.log()`.

### Performance Tip for Massive Output
Calling `console.log()` inside a tight loop is very slow! If you have to print 100,000 lines, build an array and join it, or build a string, then print once.

```javascript
// SLOW
for (let i = 0; i < 100000; i++) {
    console.log(i); 
}

// FAST
let out = [];
for (let i = 0; i < 100000; i++) {
    out.push(i);
}
console.log(out.join('\n'));
```

---

## 9. Math and Number Handling

JavaScript's `Math` object provides static methods, identical in purpose to Java's `java.lang.Math`.

### Common Math Functions
- `Math.abs(x)`
- `Math.max(a, b)`
- `Math.min(a, b)`
- `Math.floor(x)`: Round down (essential for JS integer division).
- `Math.ceil(x)`: Round up.
- `Math.round(x)`: Round to nearest integer.
- `Math.sqrt(x)`
- `Math.pow(base, exp)` or use the `**` operator (`base ** exp`).

### Finding Max/Min of an Array
In Java, you must loop. In JavaScript, you can use the spread operator (`...`), which unpacks the array into arguments.

```javascript
const arr = [5, 1, 9, 3];
const maxVal = Math.max(...arr); // Equivalent to Math.max(5, 1, 9, 3)
```
*Warning:* Do not use `Math.max(...arr)` if the array has millions of elements. It will exceed the maximum number of function arguments and crash. For huge arrays, use a loop.

### Numeric Limits
Java has `Integer.MAX_VALUE` and `Integer.MIN_VALUE`.
JavaScript has:
- `Number.MAX_SAFE_INTEGER` (2^53 - 1)
- `Number.MIN_SAFE_INTEGER` -(2^53 - 1)

For infinity sentinels (e.g., initializing a min variable):
```javascript
let minFound = Infinity;     // Greater than any other number
let maxFound = -Infinity;    // Less than any other number
```

### NaN (Not a Number)
`NaN` is a special numeric value that represents an invalid calculation (e.g., `0 / 0` or `parseInt("hello")`).
**The Trap:** `NaN === NaN` is `false`!
To check for NaN, use `Number.isNaN()`:
```javascript
let val = parseInt("hello");
console.log(val === NaN); // false!
console.log(Number.isNaN(val)); // true!
```

---

## 10. Classes for DSA

ES6 introduced the `class` keyword. Under the hood, it's syntactic sugar over JavaScript's prototype-based inheritance, but syntactically it looks very similar to Java.

```java
// Java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}
```

```javascript
// JavaScript
class ListNode {
    // The constructor is explicitly named 'constructor'
    constructor(val = 0, next = null) {
        this.val = val;      // Must use 'this' to assign properties
        this.next = next;
    }
}

// Instantiating
let head = new ListNode(5);
head.next = new ListNode(10);
```

You will use classes frequently for defining Tree nodes, Graph edges, Tries, and Custom Data Structures (like Heaps).
Unlike Java, you do not declare the fields before the constructor. You simply attach them to `this` inside the constructor.

---

## 11. Java → JavaScript Quick Reference Table

| Concept | Java | JavaScript | Note |
| :--- | :--- | :--- | :--- |
| **Print** | `System.out.println(x);` | `console.log(x);` | |
| **Integer Var** | `int x = 5;` | `let x = 5;` | JS uses 64-bit floats |
| **Constant** | `final int X = 5;` | `const X = 5;` | |
| **Max Int** | `Integer.MAX_VALUE` | `Number.MAX_SAFE_INTEGER` | JS limits at 2^53-1 |
| **Infinity** | *No direct equivalent* | `Infinity` | Useful for DP/Graphs |
| **Parse Int** | `Integer.parseInt(s)` | `parseInt(s, 10)` | Always provide radix 10 |
| **Int Division**| `a / b` | `Math.floor(a / b)` | JS `/` gives decimals |
| **String Len** | `s.length()` | `s.length` | Property, not a method |
| **Char at idx** | `s.charAt(i)` | `s[i]` | Bracket notation is preferred |
| **Null pointer**| `null` | `null` or `undefined` | |
| **Class Inst** | `new Node()` | `new Node()` | Identical |
| **Construct** | `Node(int v) { this.v = v; }`| `constructor(v) { this.v = v; }` | |
| **Equals** | `a.equals(b)` | `a === b` | Primitives only! (Objects compare by ref) |
| **Array len** | `arr.length` | `arr.length` | |
| **List add** | `list.add(x)` | `arr.push(x)` | |
| **List get** | `list.get(i)` | `arr[i]` | |

---

## 12. JavaScript Fundamentals Traps (DSA-specific)

Before moving to the next chapter, review these common bugs that trip up Java developers.

1. **`==` vs `===` Bugs**
   Never use `==`. It will coerce types and cause unpredictable truth evaluation. Always use `===`.

2. **String + Number Concatenation (`"5" + 2`)**
   If you accidentally try to sum an integer with a string, JS will convert the integer to a string and concatenate. Use `parseInt()` or `Number()` on string inputs first.

3. **`var` Hoisting**
   Using `var i = 0` inside a loop pollutes the global scope. Multiple loops using `var i` can interfere with each other if not enclosed in functions. Always use `let i = 0`.

4. **`const` Arrays and Objects**
   `const arr = []` means you cannot assign `arr` to a new array. It DOES NOT mean the array is immutable. `arr.push(1)` works fine.

5. **`NaN` Comparisons**
   If your parsed number results in `NaN`, checking `if (val === NaN)` fails. Use `Number.isNaN(val)`.

6. **Negative Modulo**
   `-5 % 3` evaluates to `-2`. Use `((x % m) + m) % m` to get `1`.

7. **`parseInt` Radix Issue**
   `parseInt("08")` used to parse as octal in older JS engines, returning `0`. Modern JS defaults to base 10, but to be completely safe in all environments, always specify the radix: `parseInt(s, 10)`.

8. **Missing Semicolons with IIFEs**
   If you omit semicolons, lines starting with `(` or `[` can merge with the previous line, causing fatal runtime errors. Just use semicolons.

9. **Integer Division**
   Forgetting `Math.floor()` when calculating the mid-point in Binary Search.
   ```javascript
   // WRONG! mid will be a decimal like 2.5
   let mid = (left + right) / 2; 

   // CORRECT!
   let mid = Math.floor((left + right) / 2);
   ```

10. **Global Variables in LeetCode**
    If you declare a global variable outside the main function in LeetCode, it persists across test cases! Always initialize your variables *inside* the function.

---
*End of Chapter 1. Please proceed to Chapter 2 for Data Structures.*
