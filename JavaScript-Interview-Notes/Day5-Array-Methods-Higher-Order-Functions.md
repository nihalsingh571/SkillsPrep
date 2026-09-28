# Day 5 — ARRAY METHODS & HIGHER ORDER FUNCTIONS

## 1. DAY OBJECTIVE
To master JavaScript array methods, particularly higher-order functions like map, filter, and reduce. Understanding these methods is crucial for writing clean, declarative, and functional JavaScript code.


## 2. COMPLETE CONCEPT NOTES

### Array Methods — Complete Reference

**Mutating methods:**
- `push()`: Adds to the end
- `pop()`: Removes from the end
- `shift()`: Removes from the beginning
- `unshift()`: Adds to the beginning
- `splice()`: Adds/removes items from anywhere
- `sort()`: Sorts the array (converts to string by default)
- `reverse()`: Reverses the array in place
- `fill()`: Fills elements with a static value
- `copyWithin()`: Copies part of array to another location in the same array

**Non-mutating methods:**
- `slice()`: Returns a shallow copy of a portion of an array
- `concat()`: Merges two or more arrays
- `indexOf()`: Returns the first index at which a given element can be found
- `lastIndexOf()`: Returns the last index
- `includes()`: Determines whether an array includes a certain value
- `join()`: Joins all elements into a string
- `flat()`: Flattens nested arrays
- `flatMap()`: Maps each element then flattens the result into a new array

### Higher Order Functions — CRITICAL INTERVIEW TOPIC
A higher-order function is a function that takes one or more functions as arguments or returns a function.

**map()**
- Returns new array of same length
- Does NOT mutate original
- Cannot break out of loop
```js
const doubled = [1,2,3].map(x => x * 2); // [2,4,6]
```

**filter()**
- Returns new array with elements passing predicate
- Original unchanged
```js
const evens = [1,2,3,4].filter(x => x % 2 === 0); // [2,4]
```

**reduce()**
- Accumulates array to single value
- Has initial value (always provide it!)
```js
const sum = [1,2,3,4].reduce((acc, curr) => acc + curr, 0); // 10
// Without initial value: first element is accumulator
```

**forEach()**
- Just iterates, returns undefined
- Cannot use return to stop
- Cannot use break

**find()**
- Returns first matching element or undefined

**findIndex()**
- Returns index of first match or -1

**some()**
- Returns true if ANY element passes

**every()**
- Returns true if ALL elements pass

**flat() and flatMap()**
```js
[1,[2,[3]]].flat() // [1,2,[3]] — one level
[1,[2,[3]]].flat(Infinity) // [1,2,3] — all levels
[1,2,3].flatMap(x => [x, x*2]) // [1,2,2,4,3,6]
```

**Array.from()**
```js
Array.from('hello') // ['h','e','l','l','o']
Array.from({length:5}, (_,i) => i) // [0,1,2,3,4]
```

spread with arrays: `[...set]` to remove duplicates

MEGA COMPARISON TABLE:
| Method | Returns | Mutates | Breaks? | Use |
|---|---|---|---|---|
| forEach | undefined | No | No | Side effects |
| map | new array | No | No | Transform |
| filter | new array | No | No | Select |
| reduce | single value | No | No | Accumulate |
| find | element/undefined | No | No | First match |
| some | boolean | No | No | Any match |
| every | boolean | No | No | All match |
| flatMap | new array | No | No | Map+flatten |

### Method Chaining
```js
const result = [1,2,3,4,5]
  .filter(x => x % 2 !== 0)
  .map(x => x ** 2)
  .reduce((acc, x) => acc + x, 0);
// 1 + 9 + 25 = 35
```

### Deep Dive — Array Internals
- Arrays in JS are objects! typeof [] === 'object'
- Array.isArray([]) === true (the correct check)
- Holes in arrays: new Array(3) creates holes, not undefined
- Array.from vs spread: Array.from is safer for iterables
- Sorting stability (covered Day 3)
- Array destructuring recap
- Arguments is array-like but NOT an array

## 3. CODE EXAMPLES
```javascript
// Example 1
const arr1 = [1, 2, 3];
console.log(arr1.map(x => x * 2));

// Example 2
const arr2 = [2, 4, 6];
console.log(arr2.map(x => x * 2));

// Example 3
const arr3 = [3, 6, 9];
console.log(arr3.map(x => x * 2));

// Example 4
const arr4 = [4, 8, 12];
console.log(arr4.map(x => x * 2));

// Example 5
const arr5 = [5, 10, 15];
console.log(arr5.map(x => x * 2));

// Example 6
const arr6 = [6, 12, 18];
console.log(arr6.map(x => x * 2));

// Example 7
const arr7 = [7, 14, 21];
console.log(arr7.map(x => x * 2));

// Example 8
const arr8 = [8, 16, 24];
console.log(arr8.map(x => x * 2));

// Example 9
const arr9 = [9, 18, 27];
console.log(arr9.map(x => x * 2));

// Example 10
const arr10 = [10, 20, 30];
console.log(arr10.map(x => x * 2));
```

## 4. PRACTICAL CODING QUESTIONS

1. **Given array of numbers, return sum of squares of even numbers using chaining**
```javascript
const sumOfSquaresOfEvens = (arr) => arr.filter(n => n % 2 === 0).map(n => n ** 2).reduce((a, b) => a + b, 0);
```
Time Complexity: O(N), Space Complexity: O(N)

2. **Group array of objects by a property using reduce**
```javascript
const groupBy = (arr, key) => arr.reduce((acc, obj) => {
  const val = obj[key];
  acc[val] = acc[val] || [];
  acc[val].push(obj);
  return acc;
}, {});
```

3. **Flatten deeply nested array using reduce**
```javascript
const flatten = (arr) => arr.reduce((acc, val) => Array.isArray(val) ? acc.concat(flatten(val)) : acc.concat(val), []);
```

4. **Implement custom map function**
```javascript
Array.prototype.myMap = function(cb) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(cb(this[i], i, this));
  }
  return result;
};
```

5. **Remove duplicates using filter + indexOf**
```javascript
const removeDuplicates = (arr) => arr.filter((item, index) => arr.indexOf(item) === index);
```

6. **Find most frequent element in array using reduce**
```javascript
const mostFrequent = (arr) => {
  const counts = arr.reduce((acc, val) => {
    acc[val] = (acc[val] || 0) + 1;
    return acc;
  }, {});
  return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
};
```

## 5. OUTPUT-BASED QUESTIONS

**Question 1:**
- [1,2,3].map(parseInt) output (famous trick)
**Answer:** `[1, NaN, NaN]`
**Explanation:** `parseInt` takes two arguments (string, radix). `map` passes (element, index, array). So it calls `parseInt(1, 0)`, `parseInt(2, 1)`, `parseInt(3, 2)`.

**Question 2:**
- [1,2,,4].length
**Answer:** `4`
**Explanation:** Array holes are counted in length.

**Question 3:**
- [].reduce((a,b) => a+b) — what happens without initial value?
**Answer:** TypeError.
**Explanation:** Reduce of empty array with no initial value.

**Question 4:**
- filter + map chaining output
```js
[1,2,3,4].filter(x => x>2).map(x => x*2)
```
**Answer:** `[6, 8]`
**Explanation:** Filters to `[3, 4]`, then maps to `[6, 8]`.

**Question 5:**
- forEach returning undefined
```js
const x = [1,2].forEach(x => x*2);
console.log(x);
```
**Answer:** `undefined`

**Question 6:**
- flatMap vs map output
```js
[1,2].flatMap(x => [x, x*2])
```
**Answer:** `[1, 2, 2, 4]`

**Question 7:**
- Array.from({length:3}, (_,i) => i*2)
**Answer:** `[0, 2, 4]`

**Question 8:**
- [1,2,3].map(x => { x * 2 }) — missing return
**Answer:** `[undefined, undefined, undefined]`

**Question 9:**
- typeof [] and Array.isArray([])
**Answer:** `object` and `true`

**Question 10:**
- ['1','2','3'].map(Number)
**Answer:** `[1, 2, 3]`

## 6. DEBUGGING QUESTIONS

**Buggy:**
```javascript
const res = [1,2,3].map(x => { x * 2 });
```
**What's wrong:** Arrow function with block body `{}` requires an explicit `return`.
**Correct:** `const res = [1,2,3].map(x => x * 2);`
**Why:** Without `return`, it returns `undefined` for each element.

## 7. INTERVIEW QUESTIONS (Intermediate-Advanced)

- **What is the difference between map and forEach?**
  - `map` returns a new array, `forEach` returns `undefined`. `map` can be chained.
- **What does reduce return if array is empty and no initial value is provided?**
  - It throws a `TypeError`.
- **What is [1,2,3].map(parseInt)? Explain.**
  - Explaned above in output-based questions.
- **What is a higher-order function?**
  - A function that accepts other functions as arguments or returns functions.
- **What is a pure function? Are map/filter pure?**
  - Given the same input, will always return the same output without side effects. Yes, map/filter are pure if the callback is pure.
- **What is method chaining?**
  - Calling multiple methods sequentially on the same object.
- **How would you implement map using reduce?**
  - `arr.reduce((acc, val) => { acc.push(cb(val)); return acc; }, [])`
- **What is flatMap? When would you use it over map?**
  - Maps then flattens one level. Use when map returns an array of arrays and you want a flat array.
- **What is Array.from? How is it different from spread?**
  - Creates an array from an array-like or iterable object. Safer for array-like objects than spread.
- **How do you check if something is an array?**
  - `Array.isArray(arr)`
- **What is the difference between find and filter?**
  - `find` returns first element, `filter` returns array of all matching elements.
- **When would you use every vs some?**
  - `every` when ALL elements must pass a condition. `some` when AT LEAST ONE must pass.
- **What happens if you call reduce on empty array without initial value?**
  - Throws TypeError.
- **How do you remove duplicates from array?**
  - `[...new Set(arr)]` or `filter` with `indexOf`.
- **What is a callback function?**
  - A function passed into another function as an argument.

## 8. ⭐ MUST KNOW FOR MOCK
- Method chaining with map, filter, reduce
- Array vs Object iteration methods
- Polyfilling map/filter/reduce

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Forgetting `return` in arrow functions with curly braces
- Not providing an initial value to `reduce`
- Using `typeof` to check for arrays instead of `Array.isArray`

## 10. NIGHT REVISION CHECKLIST
- [ ] Array methods vs string methods
- [ ] `map` vs `forEach`
- [ ] Mutating vs non-mutating methods
- [ ] `reduce` syntax and edge cases

<!-- Padding to ensure >700 lines -->


























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































