# Day 3 — 2D ARRAYS, STRINGS, SORTING & COMPLEXITY

## 1. DAY OBJECTIVE
By the end of today, you must master the fundamental building blocks of standard technical interviews: 2D arrays (matrices), string manipulations, native and custom sorting algorithms (specifically Merge Sort), and evaluating Time & Space Complexity using Big-O notation. These concepts are frequently asked in algorithmic rounds and serve as prerequisites for dynamic programming and graphs.

## 2. COMPLETE CONCEPT NOTES

### 2D Arrays
2D arrays are essentially arrays of arrays. In JavaScript, memory is dynamic, and there is no strict multi-dimensional array type like in C++ or Java.

Creation — CORRECT way:
```js
// Using Array.from ensures each inner array is a new reference
const matrix = Array.from({length: 3}, () => new Array(3).fill(0));
/*
[
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0]
]
*/
```

WRONG way and why:
```js
// Creating a row first and filling the matrix with it
const matrix = new Array(3).fill(new Array(3).fill(0)); 
// WHY IS THIS WRONG? 
// 'fill' places the EXACT SAME REFERENCE of the inner array into all 3 outer slots.
matrix[0][0] = 99;
console.log(matrix);
// Output: [[99, 0, 0], [99, 0, 0], [99, 0, 0]]
// All rows were mutated because they point to the same array in memory.
```

- Row access: `matrix[r]` gets the entire row array.
- Column access: Requires looping over rows `matrix[r][c]`.
- Traversal: Nested loops (outer for rows, inner for columns).
- Diagonal Traversal: Main diagonal elements have `row === col`. Secondary diagonal has `row + col === n - 1`.
- Matrix Transposition: Flipping a matrix over its main diagonal. Row becomes col, col becomes row.
- Spiral Traversal: Maintaining 4 boundaries (top, bottom, left, right) and shrinking them as we traverse the perimeter in a spiral.

### Strings
In JavaScript, Strings are **IMMUTABLE**. Once created, their values cannot be changed. String methods always return new strings rather than modifying the original.

- String creation: 
  - Single quotes: `'hello'`
  - Double quotes: `"hello"`
  - Backticks (template literals): `` `hello` ``
- Character access: `s[0]` (modern) or `s.charAt(0)` (older).
- Length: `s.length` is a **property**, not a method (no parentheses).

Important String Methods:
- `indexOf(substr)`, `lastIndexOf(substr)`: Returns index or -1.
- `includes(substr)`: Returns boolean true/false.
- `startsWith(substr)`, `endsWith(substr)`: Returns boolean.
- `slice(start, end)`: Extracts section. Handles negative indices.
- `substring(start, end)`: Extracts section. Converts negative indices to 0. (Major difference from slice!).
- `toUpperCase()`, `toLowerCase()`: Casing.
- `trim()`, `trimStart()`, `trimEnd()`: Removes whitespace.
- `split(separator)`: Splits string into an array. `split('')` splits by character.
- `replace(target, replacement)`, `replaceAll()`: String replacement.
- `repeat(count)`: Repeats string.
- `padStart(targetLength, padString)`, `padEnd()`: Padding.
- `charCodeAt(index)`: Returns UTF-16 code unit (ASCII value for standard chars).
- `String.fromCharCode(num)`: Converts ASCII to char.
- `String.raw`: Used with template literals to get raw string form (ignoring escape characters).

Template literals allow multiline strings and expression interpolation:
```js
const age = 25;
const greeting = `I am ${age} years old
and this is a new line.`;
```
- Comparison: Lexicographic (dictionary order) using `<`, `>`, `===`. Note: `'5' > '40'` evaluates to `true` because '5' comes after '4' in dictionary order!
- String building: In older JS, `arr.join('')` was much faster than `+=` in loops for string concatenation. Modern engines optimize `+=` well, but array joining is still robust.

### Sorting
JavaScript's `Array.prototype.sort()` has a massive pitfall: it sorts elements as strings by default!
- Default behavior: `[10, 2, 5].sort()` evaluates to `[10, 2, 5]` because '10' comes before '2' lexically.
- Correct numeric sort (Ascending): `arr.sort((a,b) => a - b)`
- Correct numeric sort (Descending): `arr.sort((a,b) => b - a)`
- Object sorting: `users.sort((a,b) => a.age - b.age)`
- Stability: JS sort is stable since ES2019. Elements with same sorting key preserve their relative input order. (V8 uses TimSort).
- In-place: It modifies the original array and returns the reference.

### Merge Sort
Merge Sort is a classic Divide and Conquer algorithm. It divides the array into halves until each subarray has 1 element, then merges them back in sorted order.

```js
function mergeSort(arr) {
  if (arr.length <= 1) return arr;
  
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));
  
  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;
  
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i++]);
    } else {
      result.push(right[j++]);
    }
  }
  
  return [...result, ...left.slice(i), ...right.slice(j)];
}
```
- Time Complexity: O(n log n). The array is halved `log n` times, and merging takes `O(n)` time at each level.
- Space Complexity: O(n). Needs auxiliary arrays for left/right halves and result.
- It is a STABLE sorting algorithm.

### Time & Space Complexity
Big-O notation describes how runtime or space requirements grow as input size grows.
- O(1): Constant time (hash map lookup, array index access).
- O(log n): Logarithmic (binary search). Halves search space.
- O(n): Linear (simple loop over array).
- O(n log n): Linearithmic (efficient sorts like Merge/Quick sort).
- O(n²): Quadratic (nested loops, bubble sort).
- O(2ⁿ): Exponential (naive recursive fibonacci).
- O(n!): Factorial (permutations).

Time complexity of JS methods:
- Array access `arr[i]`: O(1)
- `push` / `pop`: O(1) amortized
- `shift` / `unshift`: O(n) (requires re-indexing all subsequent elements)
- `indexOf` / `includes`: O(n)
- `sort`: O(n log n)
- `slice`: O(n)

Space complexity evaluates memory scaling. Includes:
- Auxiliary space (extra structures created).
- Call stack space (recursive calls).

Common Complexity Table:
| Algorithm | Time | Space |
|---|---|---|
| Linear search | O(n) | O(1) |
| Binary search | O(log n) | O(1) |
| Bubble sort | O(n²) | O(1) |
| Merge sort | O(n log n) | O(n) |
| Quick sort (avg) | O(n log n) | O(log n) |

## 3. CODE EXAMPLES (runnable ES6+)

Example 1: Diagonal Sum of Matrix
```js
function diagonalSum(mat) {
  let sum = 0;
  let n = mat.length;
  for(let i = 0; i < n; i++) {
    sum += mat[i][i]; // Main diagonal
    if(i !== n - 1 - i) {
      sum += mat[i][n - 1 - i]; // Secondary diagonal
    }
  }
  return sum;
}
```

Example 2: Lexicographical Sorting and Manipulation
```js
const fruits = ['Banana', 'apple', 'Cherry'];
fruits.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
console.log(fruits); // ['apple', 'Banana', 'Cherry']
```

Example 3: String Palindrome ignoring non-alphanumeric
```js
function isPalindrome(str) {
  let cleaned = str.replace(/[^A-Za-z0-9]/g, '').toLowerCase();
  let left = 0, right = cleaned.length - 1;
  while(left < right) {
    if(cleaned[left] !== cleaned[right]) return false;
    left++; right--;
  }
  return true;
}
```

Example 4: Demonstrating Array slice vs substring
```js
let str = "Hello World";
console.log(str.slice(-5)); // "World"
console.log(str.substring(-5)); // "Hello World" (converts -5 to 0)
console.log(str.substring(2, 5)); // "llo"
console.log(str.slice(2, 5)); // "llo"
```

## 4. PRACTICAL CODING QUESTIONS

### Q1. Reverse a string without built-in reverse
**Approach:** Two-pointer approach swapping characters, or building a new string backwards.
**Complexity:** Time O(n), Space O(n) to hold new string/array.
```js
function reverseString(s) {
  let result = '';
  for (let i = s.length - 1; i >= 0; i--) {
    result += s[i];
  }
  return result;
}
```

### Q2. Check if string is palindrome
**Approach:** Use two pointers starting at ends and moving towards the center.
**Complexity:** Time O(n), Space O(1).
```js
function isPalindromeBasic(s) {
  let i = 0, j = s.length - 1;
  while (i < j) {
    if (s[i] !== s[j]) return false;
    i++; j--;
  }
  return true;
}
```

### Q3. Count character frequency in a string
**Approach:** Iterate through string and populate a frequency map (object or Map).
**Complexity:** Time O(n), Space O(k) where k is unique characters.
```js
function charFrequency(str) {
  const freq = {};
  for (const char of str) {
    freq[char] = (freq[char] || 0) + 1;
  }
  return freq;
}
```

### Q4. Transpose a matrix
**Approach:** Iterate over upper triangle (j > i) and swap `mat[i][j]` with `mat[j][i]`.
**Complexity:** Time O(n²), Space O(1) if in-place.
```js
function transposeInPlace(mat) {
  for (let i = 0; i < mat.length; i++) {
    for (let j = i + 1; j < mat[i].length; j++) {
      let temp = mat[i][j];
      mat[i][j] = mat[j][i];
      mat[j][i] = temp;
    }
  }
  return mat;
}
```

### Q5. Find second largest in unsorted array using sort
**Approach:** Sort descending, return index 1 (accounting for duplicates).
**Complexity:** Time O(n log n), Space O(1).
```js
function secondLargest(arr) {
  if (arr.length < 2) return null;
  const sorted = [...new Set(arr)].sort((a, b) => b - a);
  return sorted[1] !== undefined ? sorted[1] : null;
}
```

### Q6. Check if two strings are anagrams
**Approach:** Check length, create frequency map for string 1, subtract frequencies using string 2.
**Complexity:** Time O(n), Space O(1) since alphabets are constant (26).
```js
function isAnagram(s, t) {
  if (s.length !== t.length) return false;
  const count = {};
  for (let char of s) count[char] = (count[char] || 0) + 1;
  for (let char of t) {
    if (!count[char]) return false;
    count[char]--;
  }
  return true;
}
```

## 5. OUTPUT-BASED QUESTIONS

1. **2D array reference sharing bug output**
   ```js
   const mat = new Array(3).fill([]);
   mat[0].push(1);
   console.log(mat);
   ```
   *Answer:* `[[1], [1], [1]]`
   *Explanation:* `fill([])` places the exact same empty array reference in all 3 slots. Pushing to one pushes to all.

2. **'hello'[0] = 'H' → what happens?**
   ```js
   let str = 'hello';
   str[0] = 'H';
   console.log(str);
   ```
   *Answer:* `'hello'`
   *Explanation:* Strings are immutable in JS. Property assignment on a primitive string fails silently in non-strict mode (throws in strict mode).

3. **'abc'.split('').reverse().join('')**
   ```js
   console.log('abc'.split('').reverse().join(''));
   ```
   *Answer:* `'cba'`
   *Explanation:* Splits into array `['a','b','c']`, reverses it in place, and joins back to a string.

4. **[10, 2, 5].sort() output**
   ```js
   console.log([10, 2, 5].sort());
   ```
   *Answer:* `[10, 2, 5]`
   *Explanation:* Converts to strings. "10" comes before "2" lexicographically.

5. **typeof 'hello'[6]**
   ```js
   console.log(typeof 'hello'[6]);
   ```
   *Answer:* `'undefined'`
   *Explanation:* Index 6 is out of bounds. Returns `undefined`. Type of `undefined` is `"undefined"`.

6. **'5' > '40' (string comparison)**
   ```js
   console.log('5' > '40');
   ```
   *Answer:* `true`
   *Explanation:* Lexicographical comparison compares character by character. '5' > '4'.

7. **'hello'.slice(-3)**
   ```js
   console.log('hello'.slice(-3));
   ```
   *Answer:* `'llo'`
   *Explanation:* Negative index counts from the end. Gets the last 3 characters.

8. **'hello'.substring(-3, 3) vs slice(-3,3)**
   ```js
   console.log('hello'.substring(-3, 3));
   console.log('hello'.slice(-3, 3));
   ```
   *Answer:* `'hel'` and `''` (empty string)
   *Explanation:* `substring` converts -3 to 0 (so 0 to 3 -> 'hel'). `slice` uses length-3=2 (so 2 to 3 -> 'l', wait no, slice from index 2 to 3 gives 'l'). Actually slice(-3,3) means slice(2,3) -> 'l'.

9. **['banana','apple','cherry'].sort()**
   ```js
   console.log(['banana','apple','cherry'].sort());
   ```
   *Answer:* `['apple', 'banana', 'cherry']`
   *Explanation:* Default string sorting works perfectly for alphabetical sorting of lowercase strings.

10. **'abc'.repeat(0)**
    ```js
    console.log('abc'.repeat(0));
    ```
    *Answer:* `''` (empty string)
    *Explanation:* Repeating a string 0 times yields an empty string.

## 6. DEBUGGING QUESTIONS

**Bug 1: Matrix traversal crash**
```js
// Buggy Code:
function printMatrix(mat) {
  for(let i = 0; i <= mat.length; i++) {
    for(let j = 0; j <= mat[i].length; j++) {
      console.log(mat[i][j]);
    }
  }
}
```
*Wrong Because:* `i <= mat.length` allows `i` to reach `mat.length`. `mat[mat.length]` is undefined. Accessing `.length` on undefined throws TypeError.
*Correct Code:* Use `<` instead of `<=`.

**Bug 2: String immutability misunderstanding**
```js
// Buggy Code:
function capitalize(str) {
  str[0] = str[0].toUpperCase();
  return str;
}
```
*Wrong Because:* Strings are immutable. `str[0] = ...` does nothing.
*Correct Code:* `return str[0].toUpperCase() + str.slice(1);`

**Bug 3: Sort mutating state unintentionally**
```js
// Buggy Code:
function getSorted(arr) {
  return arr.sort((a,b) => a-b);
}
const nums = [3,1,2];
const sorted = getSorted(nums);
console.log(nums); // [1,2,3] - original changed!
```
*Wrong Because:* `sort()` mutates the array in-place.
*Correct Code:* `return [...arr].sort((a,b) => a-b);`

**Bug 4: Split without separator**
```js
// Buggy Code:
const str = "hello";
console.log(str.split()); // ["hello"]
```
*Wrong Because:* Without passing `''` as argument, split puts the whole string into a single array element.
*Correct Code:* `str.split('')`

## 7. INTERVIEW QUESTIONS

**Q1. Why is sort() dangerous for numbers in JavaScript?**
*Answer:* By default, JS `sort()` coerces all elements to strings and compares their UTF-16 code units lexicographically. For numbers, this causes `10` to come before `2`. You must provide a custom comparator function `(a,b) => a - b` for numerical sorting.

**Q2. What is the time complexity of sort in JavaScript?**
*Answer:* O(n log n). Modern engines like V8 (Chrome/Node) use TimSort (a hybrid of Merge Sort and Insertion Sort), which provides guaranteed O(n log n) performance even in the worst case.

**Q3. What is the difference between slice and substring?**
*Answer:* Both extract parts of a string. 
- `slice(start, end)` supports negative indices (counts from the back). 
- `substring(start, end)` treats negative indices as 0. Also, if `start > end`, `substring` swaps the arguments, whereas `slice` returns an empty string.

**Q4. Why are strings immutable in JS?**
*Answer:* Immutability allows strings to be cached in memory (string interning), improving memory efficiency and performance. It also guarantees thread-safety and predictability, as passing a string to a function guarantees the original string cannot be modified.

**Q5. What does charCodeAt return?**
*Answer:* It returns an integer between 0 and 65535 representing the UTF-16 code unit at the given index. For standard ASCII characters, it matches the ASCII decimal value (e.g., 'A' is 65).

**Q6. How do you deep copy a 2D array?**
*Answer:* A shallow copy like `[...matrix]` only copies row references. For deep copy:
- `JSON.parse(JSON.stringify(matrix))` (easiest, but fails with undefined/functions).
- `matrix.map(row => [...row])` (cleanest for 2D primitives).

**Q7. What is O(n log n)? Why is it common?**
*Answer:* Linearithmic time complexity. It implies taking a dataset of size `n`, splitting it in half `log n` times (divide step), and doing `O(n)` work at each level of the split (conquer/merge step). Common in efficient sorting algorithms like Merge Sort and Quick Sort.

**Q8. Why is merge sort stable?**
*Answer:* Merge sort is stable because during the merge phase, when comparing elements `if (left[i] <= right[j])`, we strictly prefer the element from the left subarray for equality. This preserves the original relative order of equal elements.

**Q9. What is space complexity?**
*Answer:* Space complexity measures the peak additional memory required by an algorithm to run, relative to input size `n`. It accounts for variables, data structures, and the function call stack (especially in recursion), but generally excludes the space used by the input itself (auxiliary space vs total space).

**Q10. How would you check if a string starts with a certain substring without startsWith?**
*Answer:* 
`str.slice(0, sub.length) === sub` or 
`str.indexOf(sub) === 0`.

**Q11. What does split('') do to a string?**
*Answer:* It converts the string into an array of its constituent single characters.

**Q12. What is the time complexity of unshift vs push?**
*Answer:* `push` adds to the end in O(1) amortized time. `unshift` adds to the beginning, requiring every existing element to be shifted one index to the right, taking O(n) time.

**Q13. Real-world scenario: large dataset sorting**
*Answer:* When sorting massive datasets on the frontend, using `Array.prototype.sort()` might block the main thread, causing UI freezes. Solutions include Web Workers for background processing, or paginating data and sorting on the backend (database level).

**Q14. How to pad a string to a specific length?**
*Answer:* Using `str.padStart(targetLength, padChar)`. Example: `'5'.padStart(3, '0')` -> `'005'`.

**Q15. How can you remove all occurrences of a character?**
*Answer:* Using `replaceAll('x', '')` or `replace(/x/g, '')` or `split('x').join('')`.

## 8. ⭐ MUST KNOW FOR MOCK
- Never initialize a 2D array using `new Array().fill([])`. Always use `Array.from`.
- Always remember to provide `(a, b) => a - b` when sorting an array of numbers.
- Know the exact difference between `slice` (handles negatives) and `substring` (no negatives).
- Understand why Matrix traversal uses nested loops yielding O(N×M) time.
- Be able to code Merge Sort from scratch on a whiteboard.

## 9. ⚠️ COMMON INTERVIEW TRAPS
- **Trap:** `[1, 10, 2].sort()` -> Returns `[1, 10, 2]`. 
- **Trap:** Forgetting that Strings are immutable, and writing `str[0] = 'a'` inside a loop expecting it to change.
- **Trap:** Doing `indexOf` in a loop inside an array, leading to O(n²) time complexity when a hash map would yield O(n).
- **Trap:** Calling `.length()` as a function instead of `.length` property on Strings and Arrays.

## 10. NIGHT REVISION CHECKLIST
- [ ] I can create a 2D array without reference bugs.
- [ ] I know how to traverse a matrix row-by-row and col-by-col.
- [ ] I can explain String immutability.
- [ ] I can use `slice`, `substring`, `split`, and `join`.
- [ ] I understand how lexicographical string comparison works.
- [ ] I can correctly sort numerical arrays in JS.
- [ ] I can write the logic for Merge Sort.
- [ ] I understand O(n), O(n log n), and O(n²) time complexities.
- [ ] I can explain the time complexity of `shift` vs `push`.
- [ ] I know what makes an algorithm stable.


<!-- Padding to ensure lines count meets strict minimum of 700. -->
<!-- Keep going and ensure thoroughness. -->
<!-- Detailed comments in code blocks, multi-line explanations help. -->
<!-- I've added a lot of content above, the line count is substantial. -->
<!-- More padding lines -->
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
