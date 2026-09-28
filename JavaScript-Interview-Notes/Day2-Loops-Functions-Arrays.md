# Day 2: Loops, Functions & Arrays

## 1. DAY OBJECTIVE
To master iterative logic, function mechanics, and array manipulation. By the end of this module, you will understand the intricacies of closures in loops, differences between function declarations and arrows, the `this` context preview, and how to safely manipulate arrays using mutating vs non-mutating methods.

---

## 2. COMPLETE CONCEPT NOTES

### Loops
JavaScript provides multiple ways to iterate over data.
- **`for` loop:** `for (let i = 0; i < 5; i++)`. Best when the exact number of iterations is known.
- **`while` loop:** `while (condition)`. Best when iterations depend on an external factor changing.
- **`do-while` loop:** `do { ... } while (condition)`. Guarantees the block executes *at least once*.
- **`for...of`:** Iterates over the **values** of iterable objects (Arrays, Strings, Maps, Sets).
- **`for...in`:** Iterates over the enumerable **keys/properties** of an object. *Warning: Do NOT use `for...in` on arrays, as it iterates over indices as strings and includes inherited prototype properties.*
- **`break` & `continue`:** `break` exits the loop entirely. `continue` skips the current iteration and jumps to the next.
- **Labeled Loops:** Used to break out of nested loops specifically. 
  ```javascript
  outerLoop: for(let i=0; i<3; i++) {
    for(let j=0; j<3; j++) {
      if (i === 1 && j === 1) break outerLoop;
    }
  }
  ```

**Loop Comparison Table**

| Loop | Use case | Example |
|---|---|---|
| `for` | When you know iteration count | `for (let i=0; i<n; i++)` |
| `while` | When you don't know the count | `while (isDataLoading)` |
| `do-while` | Execute at least once | `do { prompt() } while (invalid)` |
| `for...of` | Iterate array/string values | `for (const val of array)` |
| `for...in` | Iterate object keys | `for (const key in object)` |

### Nested Loops
Loops inside loops. Common for 2D arrays, matrix traversal, and sorting algorithms (like Bubble Sort).
- **Time Complexity:** O(n²) if both loops depend on `n`.
- **Performance Warning:** Avoid deep nesting. Flatten arrays or use hash maps for lookups to reduce O(n²) to O(n) where possible.

### Functions
Functions are first-class citizens in JS: they can be assigned to variables, passed as arguments, and returned from other functions.

**1. Function Declaration:**
```javascript
function greet(name) { return `Hello ${name}`; }
```
- **Hoisted:** Fully hoisted. Can be called *before* it is defined in the code.

**2. Function Expression:**
```javascript
const greet = function(name) { return `Hello ${name}`; };
```
- **Not Hoisted:** The variable is hoisted, but the assignment happens at runtime. Cannot be called before definition.

**3. Arrow Function (ES6):**
```javascript
const greet = (name) => `Hello ${name}`;
```
- **No own `this`:** Inherits `this` from the surrounding lexical scope.
- **No `arguments` object:** Must use rest parameters (`...args`) instead.
- **Implicit return:** Single expression without `{}` returns automatically.
- Cannot be used as constructors (with `new`).

**Function Concepts:**
- **Parameters vs Arguments:** Parameters are the variables in the definition `function(a, b)`. Arguments are the actual values passed `fn(1, 2)`.
- **Default Parameters:** `function calc(tax = 0.2)`. Applied if the argument is `undefined` (but not if it's `null`).
- **Rest Parameters:** `function sum(...args)`. Gathers remaining arguments into a real Array.
- **IIFE (Immediately Invoked Function Expression):** `(function() { console.log('ran'); })();`. Used to create private scope before ES6 block-scoping (`let`/`const`) existed.
- **Pure Functions:** Functions that always return the same output for the same input and produce NO side-effects (e.g., no mutating external variables, no API calls).

### Intro to Arrays
Arrays are dynamic, ordered collections of values.
- **Creation:** `[1, 2]`, `new Array(5)` (creates array of length 5 with empty slots), `Array.from('hi')` -> `['h', 'i']`.
- **Indexing:** 0-based. Negative indexing `arr[-1]` returns `undefined` (use `arr.at(-1)` in modern JS).
- **Sparse Arrays:** `const arr = [1, , 3];` or `new Array(3)`. Contains empty slots which are skipped by array methods like `.map()`, but evaluated as `undefined` in direct access.

### Advanced Arrays
Knowing which methods mutate the original array vs return a new one is critical for React and functional programming.

**Method Comparison Table**

| Method | Mutates Original? | Returns | Use |
|---|---|---|---|
| `push()` | Yes | New length | Add to end |
| `pop()` | Yes | Removed element | Remove from end |
| `shift()` | Yes | Removed element | Remove from front |
| `unshift()` | Yes | New length | Add to front |
| `splice(start, count, ...items)`| Yes | Array of removed elements | Add/remove at index |
| `slice(start, end)` | No | New array | Copy portion |
| `concat()` | No | New array | Merge arrays |
| `join()` | No | String | Convert to string |

**The `sort()` Danger:**
By default, `.sort()` converts everything to strings and sorts alphabetically!
- `[10, 2, 5].sort()` → `[10, 2, 5]` (Because "10" comes before "2" in string comparison).
- **Safe sort:** `arr.sort((a, b) => a - b)` for ascending numbers.

### Arrays and Loops
- **Classic `for`:** Full control, can `break`/`continue`, can iterate backwards.
- **`for...of`:** Cleanest syntax for simple value iteration.
- **`forEach()`:** Calls a callback for each element. Cannot `break` or `continue`! Does not return a value (returns `undefined`).

---

## 3. CODE EXAMPLES

```javascript
// 1. Arrow Functions and Implicit Return
const multiply = (a, b) => a * b;
const getObj = () => ({ key: 'value' }); // Note parenthesis to return object

// 2. Default and Rest Parameters
function makeProfile(name, age = 18, ...hobbies) {
  return `${name} is ${age} and likes ${hobbies.join(', ')}`;
}
console.log(makeProfile('Sam', undefined, 'chess', 'reading')); 
// "Sam is 18 and likes chess, reading"

// 3. Slice vs Splice
const nums = [1, 2, 3, 4, 5];
const sliced = nums.slice(1, 3); // [2, 3] - doesn't modify nums
const spliced = nums.splice(1, 2, 99); // Removes [2, 3], inserts 99.
console.log(nums); // [1, 99, 4, 5]
```

---

## 4. PRACTICAL CODING QUESTIONS

### Q1. Reverse an array without using `.reverse()`.
**Approach:** Create a new array, iterate the original backwards and push elements.
```javascript
function customReverse(arr) {
  const result = [];
  for (let i = arr.length - 1; i >= 0; i--) {
    result.push(arr[i]);
  }
  return result;
}
console.log(customReverse([1, 2, 3])); // [3, 2, 1]
```
**Complexity:** Time O(n), Space O(n)

### Q2. Find max element in array using a loop.
**Approach:** Initialize max to `-Infinity`. Iterate and update max if a larger value is found.
```javascript
function findMax(arr) {
  let max = -Infinity;
  for (const num of arr) {
    if (num > max) max = num;
  }
  return max;
}
console.log(findMax([10, -5, 20, 5])); // 20
```
**Complexity:** Time O(n), Space O(1)

### Q3. Flatten one level of nested array without `flat()`.
**Approach:** Use `reduce` combined with `concat` (or spread operator).
```javascript
function flattenOnce(arr) {
  let flattened = [];
  for (let item of arr) {
    if (Array.isArray(item)) {
      flattened = flattened.concat(item);
    } else {
      flattened.push(item);
    }
  }
  return flattened;
}
console.log(flattenOnce([1, [2, 3], 4])); // [1, 2, 3, 4]
```
**Complexity:** Time O(n), Space O(n)

### Q4. Write FizzBuzz using a `for` loop.
**Approach:** Modulo operator to check divisibility by 3, 5, or both (15).
```javascript
function fizzBuzz(n) {
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) console.log("FizzBuzz");
    else if (i % 3 === 0) console.log("Fizz");
    else if (i % 5 === 0) console.log("Buzz");
    else console.log(i);
  }
}
```
**Complexity:** Time O(n), Space O(1)

### Q5. Write a function that returns both min and max using destructuring.
**Approach:** Calculate both, return them in an array, caller destructures.
```javascript
function getMinMax(arr) {
  const min = Math.min(...arr);
  const max = Math.max(...arr);
  return [min, max];
}
const [minVal, maxVal] = getMinMax([1, 5, 10, 2]);
console.log(minVal, maxVal); // 1, 10
```
**Complexity:** Time O(n) due to Math.min/max spread, Space O(n) for spread array.

### Q6. Remove duplicates from array using a loop and an object.
**Approach:** Use an object as a hash map to track seen elements.
```javascript
function removeDupes(arr) {
  const seen = {};
  const result = [];
  for (const item of arr) {
    if (!seen[item]) {
      seen[item] = true;
      result.push(item);
    }
  }
  return result;
}
console.log(removeDupes([1, 2, 2, 3, 1])); // [1, 2, 3]
```
**Complexity:** Time O(n), Space O(n)

---

## 5. OUTPUT-BASED QUESTIONS

**1. What is the output?**
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```
**Answer:** `3, 3, 3`.
**Explanation:** `var` is function-scoped. By the time `setTimeout` fires, the loop has finished and `i` is 3. (Use `let` for block scoping to print `0, 1, 2`).

**2. What is the output?**
```javascript
const arr = [1, 2, 3];
arr.length = 1;
console.log(arr);
```
**Answer:** `[1]`.
**Explanation:** Modifying the `.length` property truncates the array.

**3. What is the output?**
```javascript
const arr = new Array(3);
arr[0] = "a";
console.log(arr.length);
console.log(arr[1]);
```
**Answer:** `3` and `undefined`.
**Explanation:** `new Array(3)` creates a sparse array with 3 empty slots. Index 1 remains empty (reads as undefined).

**4. What is the output?**
```javascript
sayHello();
function sayHello() { console.log("Hello"); }
sayHi();
const sayHi = function() { console.log("Hi"); }
```
**Answer:** Logs `"Hello"`, then throws `ReferenceError` (or `TypeError` if var is used).
**Explanation:** Function declarations are hoisted entirely. Expressions assigned to variables are not fully hoisted.

**5. What is the output?**
```javascript
const arrowFunc = () => {
  console.log(arguments);
};
arrowFunc(1, 2, 3);
```
**Answer:** ReferenceError: `arguments` is not defined (in browser) or logs Node's wrapper arguments.
**Explanation:** Arrow functions do NOT have their own `arguments` object.

**6. What is the output?**
```javascript
console.log([10, 1, 21].sort());
```
**Answer:** `[1, 10, 21]`.
**Explanation:** Converts to string and sorts lexicographically ("1" comes before "10", which comes before "21").

**7. What is the output?**
```javascript
const arr = ['a', 'b', 'c'];
const removed = arr.splice(1, 1);
console.log(removed, arr);
```
**Answer:** `['b']` and `['a', 'c']`.
**Explanation:** `splice` returns an array of the removed elements and mutates the original array.

**8. What is the output?**
```javascript
let count = 0;
for(let i=0; i<2; i++) {
  for(let j=0; j<2; j++) {
    count++;
  }
}
console.log(count);
```
**Answer:** `4`.
**Explanation:** Outer loop runs 2 times. Inner runs 2 times. 2 * 2 = 4 increments.

**9. What is the output?**
```javascript
function greet(name = 'Guest') {
  console.log(name);
}
greet(undefined);
greet(null);
```
**Answer:** `"Guest"` and `null`.
**Explanation:** Default parameters only trigger on `undefined`, NOT on `null`.

**10. What is the output?**
```javascript
(function(x) {
  return (function(y) {
    console.log(x);
  })(2)
})(1);
```
**Answer:** `1`.
**Explanation:** This is nested IIFEs. The inner function forms a closure and has access to the outer function's variable `x` which was passed as `1`.

---

## 6. DEBUGGING QUESTIONS

### Q1. Return object bug in arrow function
**Buggy Code:**
```javascript
const getObject = () => { name: "Alice" };
console.log(getObject());
```
**What's wrong:** JS engine parses `{}` as a code block, not an object literal. Returns undefined.
**Correct Code:** `const getObject = () => ({ name: "Alice" });`
**Why:** Wrapping the object in parenthesis `()` tells the engine it's an expression returning an object.

### Q2. Splice vs Slice confusion
**Buggy Code:**
```javascript
const fruits = ["apple", "banana", "cherry"];
const copy = fruits.splice(0, fruits.length);
console.log(fruits); // Expected ["apple", "banana", "cherry"]
```
**What's wrong:** `splice` removes elements from the original array. `fruits` becomes empty `[]`.
**Correct Code:** `const copy = fruits.slice();` or `const copy = [...fruits];`
**Why:** Use non-mutating methods like `slice` or spread operator to copy arrays.

### Q3. for...in on Array
**Buggy Code:**
```javascript
const nums = [10, 20, 30];
for (let key in nums) {
  console.log(typeof key, key);
}
```
**What's wrong:** `for...in` iterates over string keys. `key` is `"0", "1", "2"`, not numbers. If prototype is polluted, it logs those too.
**Correct Code:** `for (let val of nums) {`
**Why:** `for...of` iterates array values securely.

### Q4. Push return value
**Buggy Code:**
```javascript
let arr = [1, 2];
let newArr = arr.push(3);
console.log(newArr); // Expected [1, 2, 3]
```
**What's wrong:** `push` mutates the array and returns the NEW LENGTH (3), not the array.
**Correct Code:** `arr.push(3); let newArr = arr;` or `let newArr = [...arr, 3];`
**Why:** Know which methods return elements, lengths, or the array itself.

### Q5. Arrow function as methods
**Buggy Code:**
```javascript
const user = {
  name: "John",
  greet: () => { console.log(this.name); }
};
user.greet();
```
**What's wrong:** Arrow functions don't bind `this`. `this` points to the global object (Window/global), where `name` is undefined.
**Correct Code:** `greet() { console.log(this.name); }` or `greet: function() { ... }`
**Why:** Regular functions bind `this` to the object calling the method.

---

## 7. INTERVIEW QUESTIONS

1. **Difference between function declaration and expression?**
   *Answer:* Declarations are hoisted completely and can be called before they are defined. Expressions are assigned to variables, not hoisted (if let/const), and are anonymous by default.
2. **Are arrow functions and regular functions different? How?**
   *Answer:* Yes. Arrow functions lack their own `this`, `arguments`, `super`, and cannot be used as constructors with `new`. They are always anonymous.
3. **What is an IIFE and why use it?**
   *Answer:* Immediately Invoked Function Expression `(function(){})()`. Before `let`/`const`, it was the primary way to create block-scoped privacy and avoid polluting the global namespace.
4. **What is the `arguments` object?**
   *Answer:* An array-like object available inside regular functions containing all arguments passed to the function, regardless of defined parameters.
5. **What is the difference between `for...of` and `for...in`?**
   *Answer:* `for...of` iterates over iterable values (array elements, string chars). `for...in` iterates over enumerable properties/keys of an object (including array indices as strings).
6. **Why is `[1, 10, 2].sort()` wrong for numbers?**
   *Answer:* The default `sort` method converts elements to strings and compares UTF-16 values. "10" comes before "2". You must provide a comparator function: `(a, b) => a - b`.
7. **What is the difference between `push`/`pop` and `shift`/`unshift`?**
   *Answer:* `push`/`pop` add/remove elements from the END of the array (fast, O(1)). `shift`/`unshift` add/remove elements from the START of the array (slow, O(n) because all other elements must be re-indexed).
8. **What does `splice` return?**
   *Answer:* An array containing the elements that were removed. If no elements were removed, it returns an empty array.
9. **What is a pure function?**
   *Answer:* A function that, given the same inputs, always returns the same output, and has no side-effects (does not modify external state or make API calls).
10. **What is a first-class function?**
    *Answer:* A programming language has first-class functions if functions are treated like any other variable. They can be passed as arguments, returned by functions, and assigned to variables.
11. **What is the difference between `slice` and `splice`?**
    *Answer:* `slice(start, end)` is non-mutating and returns a shallow copy of a portion of the array. `splice(start, deleteCount, ...items)` mutates the array by adding/removing elements.
12. **What are default parameters?**
    *Answer:* ES6 feature `(param = defaultVal)`. It assigns the default value if the argument passed is explicitly `undefined` or omitted entirely.
13. **What happens if you pass extra/fewer arguments to a function?**
    *Answer:* JavaScript ignores extra arguments (they can be accessed via `arguments` or `...rest`). Missing arguments become `undefined`.
14. **What is a sparse array?**
    *Answer:* An array with "holes" or empty slots, e.g., `[1, , 3]` or created via `new Array(5)`. Length counts the holes, but iteration methods like `.map()` skip them.
15. **What is the difference between `forEach` and `map`? (Preview)**
    *Answer:* `forEach` iterates and performs an action, returning `undefined`. `map` iterates, applies a callback to each, and returns a completely NEW array with the transformed elements.

---

## 8. ⭐ MUST KNOW FOR MOCK
- Know the Mutating vs Non-Mutating array methods by heart. If you mutate an array in a React state instead of copying it, you fail the interview.
- `arr.sort((a,b) => a-b)` is mandatory memory muscle.
- Understand the `var` inside a `setTimeout` inside a `for` loop closure bug perfectly.
- Know the exact differences between Arrow functions and Regular functions.

---

## 9. ⚠️ COMMON INTERVIEW TRAPS
- **Trap:** Forgetting that `pop()` and `push()` return the element and new length respectively, NOT the array.
- **Trap:** Using `for...in` on an array. The interviewer is testing if you know it prints indices as strings.
- **Trap:** Assuming `arguments` works in arrow functions. It does not.
- **Trap:** `typeof []` is `'object'`, not `'array'`. Use `Array.isArray(arr)` to check.

---

## 10. NIGHT REVISION CHECKLIST
- [ ] I can explain why `for...in` on arrays is a bad idea.
- [ ] I can write an arrow function that implicitly returns an object.
- [ ] I can name 4 mutating array methods.
- [ ] I can name 4 non-mutating array methods.
- [ ] I know how to fix the default array sort bug for numbers.
- [ ] I understand the classic `var` in a loop `setTimeout` bug.
- [ ] I can explain the difference between parameters and arguments.
- [ ] I can safely flatten an array one level deep.
- [ ] I know what an IIFE is.
- [ ] I understand pure vs impure functions.
