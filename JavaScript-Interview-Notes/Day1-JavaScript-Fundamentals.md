# Day 1: JavaScript Fundamentals

## 1. DAY OBJECTIVE
To build an unbreakable foundation in JavaScript fundamentals. By the end of this revision, you will master data types, type coercion, equality checks, modern ES6+ operators (spread, destructuring, nullish coalescing), and operator precedence. These topics form the core of 80% of introductory JavaScript interview questions and output-prediction challenges.

---

## 2. COMPLETE CONCEPT NOTES

### Introduction to JavaScript
**What is JavaScript?**
- **Interpreted / JIT Compiled:** JavaScript is typically compiled just-in-time (JIT) by engines like V8, unlike C++ which is pre-compiled.
- **Single-Threaded:** JS executes one command at a time in a single main thread (Call Stack).
- **High-Level:** Abstracts away memory management (has an automatic Garbage Collector).
- **Dynamically Typed:** Variable types are checked during execution, not at compilation. Variables can hold any type of data and change types dynamically.

**Execution Environment:**
- **Browser:** JS runs in browser engines (V8 in Chrome, SpiderMonkey in Firefox). It manipulates the DOM.
- **Node.js:** A runtime environment that allows JS to run on the server, providing access to file systems and network capabilities.

**JavaScript vs Java:**
- They are completely different languages. Java is a class-based, strictly typed, compiled language. JavaScript is a prototype-based, dynamically typed, interpreted/JIT language. "Java is to JavaScript what Car is to Carpet."

**ECMAScript Versions:**
- **ES5 (2009):** The old standard (var, strict mode, JSON support).
- **ES6 / ES2015:** The massive modern update (let/const, arrow functions, classes, promises, destructuring).
- **ES2020+:** Modern additions (optional chaining `?.`, nullish coalescing `??`, BigInt).

### Data Types & Variables
JavaScript values fall into two main categories: Primitives and References.

**Primitive Types (7 types):**
1. `Number`: Integer and floating-point numbers (e.g., `42`, `3.14`).
2. `String`: Text data (e.g., `'hello'`).
3. `Boolean`: `true` or `false`.
4. `Undefined`: A variable declared but not assigned a value.
5. `Null`: Intentional absence of any object value.
6. `Symbol`: Unique and immutable identifier (ES6).
7. `BigInt`: For numbers larger than the `Number` type can hold securely (ES2020).

**Reference Types:**
- `Object` (including Arrays, Functions, Dates, Regex)

**`typeof` Operator & Gotchas:**
- `typeof 42` === `'number'`
- `typeof 'hi'` === `'string'`
- `typeof undefined` === `'undefined'`
- `typeof function(){}` === `'function'` (Functions are objects, but `typeof` has a special return for them).
- `typeof null` === `'object'` ⚠️ **FAMOUS BUG**: This is a legacy bug from JS v1. Null is primitive, not an object!

**Difference Table: Primitive vs Reference**

| Feature | Primitive | Reference |
|---|---|---|
| **Stored in** | Stack (usually) | Heap (Stack holds the memory address pointer) |
| **Passed by** | Value (Copy of the actual value) | Reference (Copy of the memory address) |
| **Mutable?** | No (Immutable - cannot be changed in place) | Yes (Properties/elements can be modified) |

**Null vs Undefined Table**

| Feature | `undefined` | `null` |
|---|---|---|
| **Meaning** | Uninitialized / Not assigned yet | Intentionally empty / no value |
| **Type (`typeof`)** | `'undefined'` | `'object'` (Bug) |
| **Default in JS** | Yes, variables start as undefined | No, must be explicitly assigned |
| **Equality** | `null == undefined` is `true` | `null === undefined` is `false` |

**Variables Intro:**
- `var`: Function-scoped, hoisted with `undefined`, can be re-declared (Legacy).
- `let`: Block-scoped, hoisted but in Temporal Dead Zone (TDZ), cannot be re-declared.
- `const`: Block-scoped, must be initialized, cannot be re-assigned. (Deep dive in Day 4).

### Operators
**Arithmetic:**
- `+`, `-`, `*`, `/`, `%` (modulo), `**` (exponentiation).
- **String + Number Coercion:** The `+` operator prefers strings. `'5' + 2` = `'52'`. However, `-`, `*`, `/` prefer numbers. `'5' - 2` = `3`.

**Unary Operators:**
- `+` (converts to number: `+'5' === 5`)
- `-` (converts to number and negates)
- `!` (logical NOT, converts to boolean and negates)
- `typeof`

**Equality: `==` vs `===` (VERY IMPORTANT)**
- `==` (Loose Equality): Performs **Type Coercion** before comparing.
- `===` (Strict Equality): Checks BOTH **Value** and **Type**. No coercion.
- `!=` (Loose Inequality) vs `!==` (Strict Inequality).

| Expression | `==` result | `===` result | Why? |
|---|---|---|---|
| `5 == '5'` | `true` | `false` | `==` coerces `'5'` to a number. |
| `null == undefined` | `true` | `false` | Special rule in JS: they loosely equal each other. |
| `0 == false` | `true` | `false` | `false` becomes `0`. `0 == 0` is true. |
| `NaN == NaN` | `false` | `false` | `NaN` is never equal to anything, not even itself. |

**Relational:** `<`, `>`, `<=`, `>=`
**Logical:** `&&` (AND), `||` (OR), `!` (NOT) with short-circuit evaluation.
- Short-circuit `||`: Returns the first truthy value. `0 || 'hello' // 'hello'`
- Short-circuit `&&`: Returns the first falsy value. `1 && 'hello' // 'hello'`

**Nullish Coalescing (`??`):**
Returns the right-hand side ONLY if the left side is `null` or `undefined`.
- `0 ?? 'default'` returns `0` (unlike `||` which would return `'default'`).

**Optional Chaining (`?.`):**
Safely reads nested object properties without throwing an error if a reference is nullish.
- `user?.address?.zipCode` returns `undefined` instead of crashing if `address` is missing.

### Operator Precedence
Order of operations dictates how expressions are evaluated.
**Order (Highest to Lowest):**
1. Grouping: `()`
2. Logical NOT, Unary plus/minus, typeof: `!`, `+`, `-`, `typeof`
3. Exponentiation: `**`
4. Multiplication/Division/Modulo: `*`, `/`, `%`
5. Addition/Subtraction: `+`, `-`
6. Relational: `<`, `>`, `<=`, `>=`
7. Equality: `==`, `===`, `!=`, `!==`
8. Logical AND: `&&`
9. Logical OR, Nullish Coalescing: `||`, `??`
10. Assignment: `=`, `+=`, etc.

*Example:* `2 + 3 * 4` = `14` (Multiplication has higher precedence than addition).

### Destructuring & Spread Operator
**Array Destructuring:** Extract values from arrays based on position.
```javascript
const [a, b, c] = [10, 20, 30]; // a=10, b=20, c=30
const [first, , third] = [1, 2, 3]; // Skip elements
const [x, ...rest] = [1, 2, 3, 4]; // rest = [2, 3, 4]
```

**Object Destructuring:** Extract values from objects based on key names.
```javascript
const user = { name: 'Alice', age: 25, role: 'Dev' };
const { name, age } = user;
const { name: fullName } = user; // Renaming variable to fullName
const { salary = 50000 } = user; // Default values
```

**Spread Operator (`...`):** Expands iterables into individual elements.
- Copy arrays: `const clone = [...arr];`
- Merge arrays: `const merged = [...arr1, ...arr2];`
- Copy objects: `const objClone = { ...obj };`
- Merge objects: `const mergedObj = { ...obj1, ...obj2 };`

**Rest Parameters (`...`):** Collects multiple elements and condenses them into a single array. Used in function definitions.
```javascript
function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }
// Difference: Spread EXPANDS elements, Rest COLLECTS elements.
```

### Type Conversion & Coercion
**Explicit Conversion (Type Casting):** You force the conversion.
- `Number('42')` → `42`, `Number('')` → `0`, `Number('abc')` → `NaN`
- `Number(true)` → `1`, `Number(null)` → `0`, `Number(undefined)` → `NaN`
- `String(42)` → `'42'`, `String(null)` → `'null'`
- `Boolean(0)` → `false`, `Boolean(1)` → `true`
- `parseInt('42px')` → `42`, `parseFloat('3.14rem')` → `3.14`

**Implicit Coercion (The Dangerous One):** JavaScript automatically converts types.
- `+` with string: Concatenation. `1 + '2'` → `'12'`
- `-`, `*`, `/`: Numeric conversion. `'5' * 2` → `10`, `'5' - '2'` → `3`
- `==`: Triggers type coercion.
- `if (value)`: Converts `value` to a boolean.

**Falsy Values:** There are exactly 6 falsy values in JS:
1. `0`
2. `""` (Empty string)
3. `null`
4. `undefined`
5. `NaN`
6. `false`
*(Note: `-0` and `0n` (BigInt zero) are also falsy).*

**Truthy Values:** EVERYTHING ELSE IS TRUTHY.
- `'0'` (String with zero)
- `[]` (Empty array)
- `{}` (Empty object)
- `-1` (Negative numbers)
- `function(){}`

### Conditionals
- **if / else if / else**: Standard branching.
- **Switch-case**: Uses strict equality (`===`) for matching. Beware of "fall-through" if you forget `break`.
- **Ternary Operator**: `condition ? exprIfTrue : exprIfFalse`
- **Short-circuiting (`||`)**: `let user = name || "Anonymous";` (If name is falsy, defaults to "Anonymous").
- **Nullish Coalescing (`??`)**: `let count = value ?? 0;` (Only defaults to 0 if value is `null` or `undefined`. If value is `0` or `""`, it keeps it!).

---

## 3. CODE EXAMPLES

```javascript
// 1. Primitive vs Reference mutation
let a = 10;
let b = a; // Pass by value
b = 20;
console.log(a); // 10

let obj1 = { name: 'Alice' };
let obj2 = obj1; // Pass by reference
obj2.name = 'Bob';
console.log(obj1.name); // 'Bob'

// 2. Destructuring with Default Values and Renaming
const person = { firstName: 'John', location: { city: 'NY' } };
const { 
  firstName: fName, 
  lastName = 'Doe', 
  location: { city } 
} = person;
console.log(fName, lastName, city); // "John", "Doe", "NY"

// 3. Optional Chaining and Nullish Coalescing
const response = { data: null };
// If data is null, .user would throw error. ?. prevents it.
const username = response.data?.user?.name ?? 'Guest';
console.log(username); // 'Guest'
```

---

## 4. PRACTICAL CODING QUESTIONS

### Q1. Write a function using destructuring to swap two variables.
**Approach:** Create an array with the two variables and instantly destructure it into the swapped variables. No temp variable needed.
```javascript
function swap(a, b) {
  [a, b] = [b, a];
  return [a, b];
}
console.log(swap(5, 10)); // [10, 5]
```
**Complexity:** Time O(1), Space O(1)

### Q2. Sum all arguments using rest parameters.
**Approach:** Use `...args` in the function parameter to gather all arguments into an array, then use `.reduce()` to sum them.
```javascript
function sumAll(...numbers) {
  return numbers.reduce((acc, curr) => acc + curr, 0);
}
console.log(sumAll(1, 2, 3, 4, 5)); // 15
```
**Complexity:** Time O(n), Space O(n) for the rest array.

### Q3. Merge two objects using spread, ensuring the second overrides the first.
**Approach:** Use `{...obj1, ...obj2}`. Keys in `obj2` will overwrite keys in `obj1`.
```javascript
const objA = { x: 1, y: 2, color: 'red' };
const objB = { y: 99, z: 3, color: 'blue' };

function mergeObjects(o1, o2) {
  return { ...o1, ...o2 };
}
console.log(mergeObjects(objA, objB)); 
// { x: 1, y: 99, color: 'blue', z: 3 }
```
**Complexity:** Time O(n+m), Space O(n+m) where n, m are object keys.

### Q4. Find the type of each value in an array using `typeof`.
**Approach:** Map over the array and return the `typeof` evaluated on each element.
```javascript
const mixedData = [1, 'hello', true, null, undefined, {}, [], function(){}];

function getTypes(arr) {
  return arr.map(item => typeof item);
}
console.log(getTypes(mixedData)); 
// ['number', 'string', 'boolean', 'object', 'undefined', 'object', 'object', 'function']
// Notice how null, {}, and [] all return 'object'!
```
**Complexity:** Time O(n), Space O(n)

### Q5. Write a function that returns a default greeting using `??`.
**Approach:** Accept a name. Use `??` to provide a fallback only if the name is strictly null or undefined, preserving empty strings if provided.
```javascript
function greet(name) {
  const finalName = name ?? 'Stranger';
  return `Hello, ${finalName}!`;
}
console.log(greet('Alice')); // "Hello, Alice!"
console.log(greet(null));    // "Hello, Stranger!"
console.log(greet(''));      // "Hello, !" (Preserves empty string, || would replace it)
```
**Complexity:** Time O(1), Space O(1)

---

## 5. OUTPUT-BASED QUESTIONS

**1. What is the output?**
```javascript
console.log(typeof null);
```
**Answer:** `'object'`. 
**Explanation:** This is a known, legacy bug in JavaScript's engine.

**2. What is the output?**
```javascript
console.log('5' + 2 + 3);
console.log(2 + 3 + '5');
```
**Answer:** `'523'` and `'55'`.
**Explanation:** Evaluates left to right. `'5'+2` becomes `'52'`, then `'52'+3` is `'523'`. For the second, `2+3` is `5` (numbers), then `5+'5'` becomes `'55'`.

**3. What is the output?**
```javascript
console.log(null == undefined);
console.log(null === undefined);
```
**Answer:** `true` and `false`.
**Explanation:** `==` coerces them and they are defined to be loosely equal. `===` checks types; `null` is object (technically), `undefined` is undefined, so they differ.

**4. What is the output?**
```javascript
console.log(Boolean([]));
console.log(Boolean({}));
```
**Answer:** `true` and `true`.
**Explanation:** Arrays and objects are reference types. Even if empty, their memory reference exists. They are NOT falsy values.

**5. What is the output?**
```javascript
console.log(0 || 'hello');
console.log(0 ?? 'hello');
```
**Answer:** `'hello'` and `0`.
**Explanation:** `||` checks for falsy values (`0` is falsy, so it moves to right). `??` checks ONLY for null/undefined (`0` is not nullish, so it returns `0`).

**6. What is the output?**
```javascript
console.log(NaN === NaN);
```
**Answer:** `false`.
**Explanation:** `NaN` represents an invalid mathematical operation. By IEEE 754 spec, `NaN` is not equal to anything, including itself. Use `Number.isNaN()` to check.

**7. What is the output?**
```javascript
console.log(undefined + 1);
```
**Answer:** `NaN`.
**Explanation:** JavaScript tries to coerce `undefined` to a number, which results in `NaN`. `NaN + 1` remains `NaN`.

**8. What is the output?**
```javascript
console.log([] + []);
console.log([] + {});
```
**Answer:** `""` (empty string) and `"[object Object]"`.
**Explanation:** The `+` operator forces `toString()`. `[].toString()` is `""`. `"" + ""` is `""`. For the second, `{}.toString()` is `"[object Object]"`, so `"" + "[object Object]"` yields `"[object Object]"`.

**9. What is the output?**
```javascript
console.log(+true);
console.log(+false);
console.log(+null);
console.log(+undefined);
console.log(+"");
```
**Answer:** `1, 0, 0, NaN, 0`.
**Explanation:** The unary `+` explicitly coerces to a Number. `Number(true)` is `1`. `Number(null)` is `0`. `Number(undefined)` is `NaN`. `Number("")` is `0`.

**10. What is the output?**
```javascript
console.log(typeof typeof 42);
```
**Answer:** `'string'`.
**Explanation:** Evaluates right to left. `typeof 42` is `'number'` (which is a string). Then `typeof 'number'` is `'string'`.

---

## 6. DEBUGGING QUESTIONS

### Q1. Destructuring bug
**Buggy Code:**
```javascript
const user = { name: 'John', address: { city: 'Paris' } };
const { city } = user;
```
**What's wrong:** Trying to directly extract `city` from the top level of `user`, but it's nested inside `address`. `city` will be undefined.
**Correct Code:**
```javascript
const { address: { city } } = user;
```
**Why:** You must mirror the object structure to destructure nested properties.

### Q2. Unintended Global
**Buggy Code:**
```javascript
function setAge() {
  age = 25; 
}
setAge();
console.log(age); 
```
**What's wrong:** Variable `age` is assigned without `let`, `const`, or `var`. In non-strict mode, this creates a global variable.
**Correct Code:**
```javascript
function setAge() {
  let age = 25; 
}
```
**Why:** Always declare variables to prevent polluting the global scope. Use `"use strict";` to catch this automatically.

### Q3. Spread syntax error
**Buggy Code:**
```javascript
const arr1 = [1, 2];
const arr2 = [3, 4];
const combined = [arr1, ...arr2];
```
**What's wrong:** `arr1` is not spread. `combined` becomes `[[1, 2], 3, 4]`.
**Correct Code:**
```javascript
const combined = [...arr1, ...arr2];
```
**Why:** You must use the `...` operator on both arrays to flatten their elements into the new array.

### Q4. Equality Trap
**Buggy Code:**
```javascript
if (score = 100) {
  console.log("Perfect score!");
}
```
**What's wrong:** Used single `=` (assignment) instead of `===` (equality check). This assigns `100` to `score` and evaluates to truthy.
**Correct Code:**
```javascript
if (score === 100) {
```
**Why:** Single equals assigns a value; the if-statement then evaluates the truthiness of the assigned value.

### Q5. Coercion Bug
**Buggy Code:**
```javascript
function addPrices(price1, price2) {
  return price1 + price2;
}
console.log(addPrices('10', '20')); // Returns "1020", not 30
```
**What's wrong:** Inputting strings results in concatenation instead of addition.
**Correct Code:**
```javascript
function addPrices(price1, price2) {
  return Number(price1) + Number(price2); // or +price1 + +price2
}
```
**Why:** Explicit coercion to numbers ensures mathematical addition rather than string concatenation.

---

## 7. INTERVIEW QUESTIONS

1. **What is the difference between `null` and `undefined`?**
   *Answer:* `undefined` means a variable has been declared but not assigned a value. `null` is an intentional assignment representing "no value" or "empty". `typeof undefined` is `'undefined'`, while `typeof null` is `'object'`.
2. **Why does `typeof null` return `'object'`?**
   *Answer:* It's a historical bug from the first version of JavaScript. Values were stored in 32-bit units, and the type tag for objects was `000`. `null` was represented as the NULL pointer (all zeros), so it matched the object type tag. It was never fixed to avoid breaking legacy code.
3. **What are falsy values in JS?**
   *Answer:* There are exactly 6: `0`, `""` (empty string), `null`, `undefined`, `NaN`, and `false`.
4. **Difference between `==` and `===`**
   *Answer:* `==` (loose equality) performs type coercion before comparing values. `===` (strict equality) checks both the value and the exact data type without converting. Always prefer `===`.
5. **What is type coercion? Give an example.**
   *Answer:* Type coercion is JavaScript's automatic or implicit conversion of values from one data type to another. For example, `'5' - 1` results in the number `4` because JS coerces the string `'5'` to a number for subtraction.
6. **What is the difference between spread and rest?**
   *Answer:* Spread (`...`) *expands* an iterable (array/object) into individual elements (e.g., copying arrays). Rest (`...`) *collects* multiple elements and condenses them into a single array (e.g., gathering function arguments).
7. **What is short-circuit evaluation?**
   *Answer:* It's when logical operators (`&&`, `||`) evaluate from left to right and stop as soon as the outcome is determined. `A || B` stops at `A` if `A` is truthy. `A && B` stops at `A` if `A` is falsy.
8. **What is nullish coalescing and how does it differ from `||`?**
   *Answer:* Nullish coalescing (`??`) returns the right operand only if the left operand is strictly `null` or `undefined`. `||` returns the right operand for ANY falsy value (`0`, `""`, `false`), which can accidentally override valid falsy inputs.
9. **What are primitive vs reference types?**
   *Answer:* Primitives (Number, String, Boolean, Null, Undefined, Symbol, BigInt) are immutable and stored by value. References (Objects, Arrays, Functions) are mutable and stored by reference (pointer to a heap memory location).
10. **How does pass-by-value vs pass-by-reference work?**
    *Answer:* Passing a primitive assigns a copy of the actual value. Changing the copy doesn't affect the original. Passing a reference assigns a copy of the memory address. Changing properties on the copied reference affects the original object.
11. **What is `NaN` and how do you check for it correctly?**
    *Answer:* `NaN` stands for Not-a-Number, resulting from invalid math operations (e.g., `"a" / 2`). `NaN === NaN` is false. Check for it using `Number.isNaN(value)`.
12. **What does `+'5'` give? Why?**
    *Answer:* It gives the number `5`. The unary plus operator forces an explicit type conversion to a Number.
13. **Explain operator precedence.**
    *Answer:* It determines the order in which operators are evaluated in an expression. For instance, multiplication has higher precedence than addition, so `2 + 3 * 4` evaluates to `14`, not `20`.
14. **What is destructuring? Give examples.**
    *Answer:* A syntax that unpacks values from arrays, or properties from objects, into distinct variables. Example: `const { name, age } = user;` or `const [first, second] = arr;`.
15. **What is the temporal dead zone? (Preview)**
    *Answer:* The TDZ is the period between entering scope and the actual declaration of a `let` or `const` variable, during which they cannot be accessed. (Deep dive Day 4).

---

## 8. ⭐ MUST KNOW FOR MOCK
- Know the 6 falsy values intimately. If it's not one of those 6, it is TRUTHY (`[]`, `{}`, `'0'`).
- The `typeof` outcomes for all types, especially `typeof null` and `typeof undefined`.
- How `+` behaves with strings vs how `- * /` behave.
- The distinction between Spread (expanding) and Rest (collecting in functions).
- `null == undefined` is true, but `null === undefined` is false.

---

## 9. ⚠️ COMMON INTERVIEW TRAPS
- **Trap:** Assuming `0` will trigger a fallback with `??`. `0 ?? 5` is `0`.
- **Trap:** Assuming empty arrays `[]` or empty objects `{}` are falsy. They are objects, hence truthy! `if ([]) console.log("yes")` prints "yes".
- **Trap:** `typeof NaN` is `'number'`. Yes, "Not-a-Number" is a type of Number.
- **Trap:** Thinking `Object.assign` is a deep clone. The spread operator `{...obj}` is also only a SHALLOW clone.
- **Trap:** Modifying a `const` object. `const` prevents reassignment of the variable binding, NOT mutation of the object properties.

---

## 10. NIGHT REVISION CHECKLIST
- [ ] I can list all 7 primitive types.
- [ ] I can explain the `typeof null` bug.
- [ ] I understand primitive (value) vs reference (memory address) behavior.
- [ ] I know why `0 == false` but `0 !== false`.
- [ ] I can successfully predict string vs number coercion (`+` vs `-`).
- [ ] I can explain why `NaN === NaN` is false.
- [ ] I understand `||` vs `??`.
- [ ] I can write array and object destructuring logic blindfolded.
- [ ] I can use the spread operator to shallow copy objects.
- [ ] I can use rest parameters in a function signature.
