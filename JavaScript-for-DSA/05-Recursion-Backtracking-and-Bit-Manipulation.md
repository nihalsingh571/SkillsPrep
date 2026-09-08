# Recursion, Backtracking, and Bit Manipulation: Java to JavaScript

Welcome to this comprehensive guide on Recursion, Backtracking, and Bit Manipulation tailored specifically for developers transitioning from Java to JavaScript. As a Java developer, you are already familiar with the fundamental concepts of these topics. This guide will focus on translating that knowledge to JavaScript, highlighting syntax differences, engine-specific behaviors (like the call stack), and common pitfalls.

---

## 1. Recursion in JavaScript

Recursion in JavaScript fundamentally works the same way it does in Java. A function calls itself until it reaches a base case. The logic, structural patterns, and problem-solving approaches you learned in Java are entirely applicable here.

### Java vs JavaScript: Syntax Comparison

Let's start by looking at some basic examples to see how the syntax translates.

#### Example: Factorial

**Java:**
```java
public class Recursion {
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
```

**JavaScript:**
```javascript
// JavaScript recursion: same logic, slightly different syntax
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Arrow function syntax
const factorialArrow = (n) => {
    if (n <= 1) return 1;
    return n * factorialArrow(n - 1);
};
```

#### Example: Fibonacci

**Java:**
```java
public static int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

**JavaScript:**
```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

As you can see, the core logic is identical. The primary difference is the lack of explicit type declarations (`int`) and the use of the `function` keyword (or arrow functions) in JavaScript.

### The Call Stack and Recursion Depth Limits

One of the most critical differences between Java and JavaScript regarding recursion is how they handle the call stack and recursion depth limits.

#### Java Call Stack
In Java, the size of the call stack is configurable at runtime using the `-Xss` JVM flag (e.g., `java -Xss1m MyApp`). The default size is typically around 512KB to 1MB, depending on the platform and JVM version. This usually allows for several thousands of recursive calls before throwing a `StackOverflowError`.

#### JavaScript Call Stack
JavaScript environments (like Node.js or web browsers) have a hardcoded, engine-specific limit on the call stack size. You cannot easily configure this limit via a flag like you can in Java.

- **V8 Engine (Node.js, Chrome):** The limit is typically around 10,000 to 15,000 stack frames.
- **SpiderMonkey (Firefox):** Usually higher, sometimes up to 30,000 to 50,000 frames.
- **JavaScriptCore (Safari):** Typically around 40,000 to 50,000 frames.

When this limit is exceeded, JavaScript throws a `RangeError: Maximum call stack size exceeded`.

#### Handling Deep Recursion in JavaScript

Because of the relatively shallow call stack in V8 (the most common JS engine), you must be careful with deep recursion in JavaScript. If you anticipate a recursion depth of over 10,000, you should consider alternatives:

1.  **Iterative Conversion:** Rewrite the recursive algorithm using loops and an explicit stack or queue. This is the safest and most common approach.

2.  **Trampolining:** A technique to achieve tail-recursive-like behavior in engines that don't natively support Tail Call Optimization (TCO). A trampoline is a loop that iteratively invokes thunk-returning functions.

    ```javascript
    // Example of Trampolining
    function trampoline(fn) {
        return function(...args) {
            let result = fn(...args);
            while (typeof result === 'function') {
                result = result();
            }
            return result;
        };
    }

    // The recursive function returns a function (thunk) instead of making the call directly
    function factorialThunk(n, acc = 1) {
        if (n <= 1) return acc;
        return () => factorialThunk(n - 1, n * acc);
    }

    const safeFactorial = trampoline(factorialThunk);
    console.log(safeFactorial(100000)); // No RangeError! (Though it will return Infinity due to JS number limits)
    ```

3.  **Tail Call Optimization (TCO):** While the ES6 standard includes TCO, **most modern JavaScript engines (including V8/Node.js) do NOT implement it** (Safari's JavaScriptCore is a notable exception). Therefore, you cannot rely on tail-recursive functions preventing stack overflows in standard JS development.

### Return Value Pattern

When writing recursive functions that search or compute a value, ensure you are correctly returning the result up the call stack.

```javascript
// Generic search/compute pattern
function solve(n) {
    // 1. Base Case(s)
    if (baseCaseCondition(n)) {
        return baseCaseValue;
    }

    // 2. Recursive Step
    // Compute the subproblem
    const subResult = solve(subproblemCondition(n));

    // 3. Return the result up the stack
    return processResult(subResult);
}
```

### Memoization Template

Memoization is a technique used to speed up recursive algorithms by caching the results of expensive function calls. In Java, you might use a `HashMap` or an array. In JavaScript, `Map`, `Set`, or plain objects (`{}`) are used.

#### Using a Higher-Order Function (The Functional Way)

JavaScript's first-class functions allow us to create a generic memoization wrapper.

```javascript
/**
 * A generic memoization function.
 * @param {Function} fn - The function to memoize.
 * @returns {Function} - The memoized version of the function.
 */
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        // Stringify arguments to use as a cache key.
        // Note: JSON.stringify is simple but has edge cases (e.g., circular references, object key order).
        // For complex arguments, a custom hashing function might be needed.
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            return cache.get(key); // Cache hit
        }
        
        // Cache miss: compute the result
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

// Usage:
const memoizedFib = memoize(function fib(n) {
    if (n <= 1) return n;
    return memoizedFib(n - 1) + memoizedFib(n - 2);
});

console.log(memoizedFib(50)); // Very fast!
```

#### Using an Explicit Cache Map (The DSA Way)

For most algorithmic problems on platforms like LeetCode, it's often simpler to pass an explicit cache or use closure variables.

```javascript
// Using closure scope for the cache
const memo = new Map();

function fibDP(n) {
    // Base cases
    if (n <= 1) return n;
    
    // Check cache
    if (memo.has(n)) return memo.get(n);
    
    // Compute recursive relation
    const result = fibDP(n - 1) + fibDP(n - 2);
    
    // Store in cache and return
    memo.set(n, result);
    return result;
}
```
**Complexity of Memoized Fibonacci:**
- **Time Complexity:** O(N) because we compute each state only once.
- **Space Complexity:** O(N) for the call stack and O(N) for the `Map` cache.

---

## 2. Backtracking Templates

Backtracking is a systematic way to iterate through all the possible configurations of a search space. These configurations may represent arrangements of objects, subsets of a set, paths in a graph, etc.

### General Backtracking Template

The core logic is: **Make a choice, recurse, undo the choice.**

```javascript
/**
 * Generic Backtracking Template
 * 
 * @param {Array} result - The array accumulating all valid solutions.
 * @param {Array} current - The current state/path being explored.
 * @param {...any} params - Other state variables (e.g., index, remaining target).
 */
function backtrack(result, current, ...params) {
    // 1. Base Case: Have we reached a valid solution?
    if (isBaseCase(params)) {
        // IMPORTANT: We MUST create a copy of 'current'.
        // If we push 'current' directly, we are pushing a reference.
        // Subsequent modifications to 'current' will modify the result array!
        result.push([...current]); 
        return;
    }

    // 2. Iterate through all possible choices at the current state
    for (const choice of getChoices(params)) {
        
        // Optimization: Pruning (if applicable)
        if (!isValid(choice)) continue;

        // 3. Make the choice (Add to current state)
        current.push(choice);

        // 4. Explore further down this path (Recursive call)
        backtrack(result, current, updateParams(params, choice));

        // 5. Undo the choice (Backtrack)
        current.pop(); 
    }
}
```

### VERY IMPORTANT JavaScript Pitfall: Array Copying

In Java, if you do `result.add(new ArrayList<>(current))`, you create a new list.
In JavaScript, the equivalent is `result.push([...current])`.

**Do NOT do this:**
```javascript
if (baseCase) {
    result.push(current); // BUG! Pushes the reference.
    return;
}
```
If you push the reference, when `current.pop()` is called later in the recursive tree, it will mutate the arrays that have already been saved in your `result` array. All elements in `result` will end up empty or in an incorrect state.

**Always use the spread operator (`...`) or `Array.from()` to copy:**
```javascript
if (baseCase) {
    result.push([...current]); // Correct! Pushes a shallow copy.
    // OR: result.push(Array.from(current));
    // OR: result.push(current.slice());
    return;
}
```

---

### Complete Implementations of Classic Backtracking Problems

#### 1. Subsets / Power Set (LeetCode 78)

Given an integer array `nums` of **unique** elements, return all possible subsets (the power set).

```javascript
/**
 * @param {number[]} nums
 * @return {number[][]}
 */
function subsets(nums) {
    const result = [];
    
    function backtrack(start, current) {
        // In subsets, every state is a valid subset, so we add it immediately.
        result.push([...current]);
        
        // Iterate from 'start' to avoid duplicate permutations (like [1,2] and [2,1])
        for (let i = start; i < nums.length; i++) {
            // Make choice
            current.push(nums[i]);
            // Recurse (move start pointer forward to only pick elements after i)
            backtrack(i + 1, current);
            // Undo choice
            current.pop();
        }
    }
    
    backtrack(0, []);
    return result;
}
```
**Complexity:**
- **Time:** O(N * 2^N) to generate all subsets and copy them.
- **Space:** O(N) for the recursion stack and `current` array.

#### 2. Subsets II (With Duplicates) (LeetCode 90)

Given an integer array `nums` that may contain duplicates, return all possible subsets. The solution set must not contain duplicate subsets.

```javascript
function subsetsWithDup(nums) {
    const result = [];
    // Sort to handle duplicates efficiently
    nums.sort((a, b) => a - b);
    
    function backtrack(start, current) {
        result.push([...current]);
        
        for (let i = start; i < nums.length; i++) {
            // Pruning: Skip duplicates at the same level of the recursion tree
            if (i > start && nums[i] === nums[i - 1]) {
                continue;
            }
            current.push(nums[i]);
            backtrack(i + 1, current);
            current.pop();
        }
    }
    
    backtrack(0, []);
    return result;
}
```

#### 3. Permutations (LeetCode 46)

Given an array `nums` of distinct integers, return all the possible permutations.

```javascript
/**
 * @param {number[]} nums
 * @return {number[][]}
 */
function permutations(nums) {
    const result = [];
    
    function backtrack(current, remaining) {
        // Base case: If no elements remaining to pick, we have a complete permutation
        if (remaining.length === 0) { 
            result.push([...current]); 
            return; 
        }
        
        // Iterate through all remaining elements
        for (let i = 0; i < remaining.length; i++) {
            // Make choice
            current.push(remaining[i]);
            
            // Create a new remaining array without the chosen element
            const newRemaining = [
                ...remaining.slice(0, i), 
                ...remaining.slice(i + 1)
            ];
            
            // Recurse
            backtrack(current, newRemaining);
            
            // Undo choice
            current.pop();
        }
    }
    
    backtrack([], nums);
    return result;
}

// Alternative approach using a 'visited' array (often faster in JS than slicing arrays)
function permutationsVisited(nums) {
    const result = [];
    const visited = new Array(nums.length).fill(false);
    
    function backtrack(current) {
        if (current.length === nums.length) {
            result.push([...current]);
            return;
        }
        
        for (let i = 0; i < nums.length; i++) {
            if (visited[i]) continue; // Skip if already used
            
            visited[i] = true;
            current.push(nums[i]);
            
            backtrack(current);
            
            current.pop();
            visited[i] = false;
        }
    }
    backtrack([]);
    return result;
}
```
**Complexity:**
- **Time:** O(N * N!)
- **Space:** O(N)

#### 4. Combination Sum (Duplicates Allowed) (LeetCode 39)

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all unique combinations where the chosen numbers sum to `target`. The same number may be chosen unlimited number of times.

```javascript
/**
 * @param {number[]} candidates
 * @param {number} target
 * @return {number[][]}
 */
function combinationSum(candidates, target) {
    const result = [];
    // Sorting helps with pruning
    candidates.sort((a, b) => a - b);
    
    function backtrack(start, current, remaining) {
        // Base case: found a valid combination
        if (remaining === 0) { 
            result.push([...current]); 
            return; 
        }
        
        for (let i = start; i < candidates.length; i++) {
            // Pruning: if the candidate exceeds the remaining target, stop looking
            // (Requires the array to be sorted)
            if (candidates[i] > remaining) break;
            
            // Make choice
            current.push(candidates[i]);
            
            // Recurse. Note that 'start' is passed as 'i' (not i+1) because we can reuse elements
            backtrack(i, current, remaining - candidates[i]);
            
            // Undo choice
            current.pop();
        }
    }
    
    backtrack(0, [], target);
    return result;
}
```

#### 5. N-Queens (LeetCode 51)

The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

```javascript
/**
 * @param {number} n
 * @return {string[][]}
 */
function solveNQueens(n) {
    const result = [];
    
    // Sets to keep track of columns and diagonals under attack
    const cols = new Set();
    const diag1 = new Set(); // row - col = constant
    const diag2 = new Set(); // row + col = constant
    
    // Initialize the board with empty spaces
    const board = Array.from({ length: n }, () => '.'.repeat(n));
    
    function backtrack(row) {
        // Base case: All n queens placed successfully
        if (row === n) { 
            result.push([...board]); 
            return; 
        }
        
        // Try placing a queen in each column of the current row
        for (let col = 0; col < n; col++) {
            // Check if the current square is under attack
            if (cols.has(col) || diag1.has(row - col) || diag2.has(row + col)) {
                continue; // Prune
            }
            
            // Make choice: Place Queen
            cols.add(col); 
            diag1.add(row - col); 
            diag2.add(row + col);
            // In JS strings are immutable, we recreate the string for that row
            board[row] = '.'.repeat(col) + 'Q' + '.'.repeat(n - col - 1);
            
            // Recurse to next row
            backtrack(row + 1);
            
            // Undo choice: Remove Queen
            cols.delete(col); 
            diag1.delete(row - col); 
            diag2.delete(row + col);
            board[row] = '.'.repeat(n);
        }
    }
    
    backtrack(0);
    return result;
}
```
**Notes on N-Queens in JS:** String manipulation for the board representation can be slow. An alternative is to use an array of strings or an array of numbers representing column indices and convert it to string format only when adding to the result.

#### 6. Word Search (2D Grid Backtracking / DFS) (LeetCode 79)

Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.

```javascript
/**
 * @param {character[][]} board
 * @param {string} word
 * @return {boolean}
 */
function exist(board, word) {
    const rows = board.length;
    const cols = board[0].length;
    
    function dfs(r, c, idx) {
        // Base case: All characters matched
        if (idx === word.length) return true;
        
        // Out of bounds or character mismatch
        if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== word[idx]) {
            return false;
        }
        
        // Mark as visited by mutating the board temporarily
        const temp = board[r][c];
        board[r][c] = '#'; 
        
        // Explore all 4 adjacent directions
        const found = 
            dfs(r + 1, c, idx + 1) || // Down
            dfs(r - 1, c, idx + 1) || // Up
            dfs(r, c + 1, idx + 1) || // Right
            dfs(r, c - 1, idx + 1);   // Left
            
        // Undo choice (backtrack)
        board[r][c] = temp; 
        
        return found;
    }
    
    // Start DFS from every possible cell
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (dfs(r, c, 0)) {
                return true;
            }
        }
    }
    return false;
}
```

#### 7. Sudoku Solver (LeetCode 37)

Write a program to solve a Sudoku puzzle by filling the empty cells.

```javascript
/**
 * @param {character[][]} board
 * @return {void} Do not return anything, modify board in-place instead.
 */
function solveSudoku(board) {
    
    function isValid(board, r, c, char) {
        for (let i = 0; i < 9; i++) {
            // Check row
            if (board[r][i] === char) return false;
            // Check column
            if (board[i][c] === char) return false;
            // Check 3x3 box
            const boxRow = 3 * Math.floor(r / 3) + Math.floor(i / 3);
            const boxCol = 3 * Math.floor(c / 3) + i % 3;
            if (board[boxRow][boxCol] === char) return false;
        }
        return true;
    }
    
    function backtrack() {
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                if (board[r][c] === '.') {
                    for (let char of ['1','2','3','4','5','6','7','8','9']) {
                        if (isValid(board, r, c, char)) {
                            board[r][c] = char; // Make choice
                            
                            if (backtrack()) return true; // Found solution, propagate true up
                            
                            board[r][c] = '.'; // Backtrack
                        }
                    }
                    return false; // Exhausted all options for this cell, trigger backtrack
                }
            }
        }
        return true; // No empty cells left, puzzle solved
    }
    
    backtrack();
}
```

#### 8. Rat in a Maze (Classic GFG Problem)

Given an `N x N` matrix representing a maze, find all paths from (0, 0) to (N-1, N-1). 1 represents open paths, 0 represents walls.

```javascript
function findPath(m, n) {
    const result = [];
    const visited = Array.from({ length: n }, () => new Array(n).fill(false));
    
    // Check if start or end is blocked
    if (m[0][0] === 0 || m[n-1][n-1] === 0) return result;
    
    function isSafe(r, c) {
        return r >= 0 && r < n && c >= 0 && c < n && m[r][c] === 1 && !visited[r][c];
    }
    
    function backtrack(r, c, path) {
        if (r === n - 1 && c === n - 1) {
            result.push(path);
            return;
        }
        
        visited[r][c] = true;
        
        // Lexicographical order: D, L, R, U
        
        // Down
        if (isSafe(r + 1, c)) backtrack(r + 1, c, path + 'D');
        // Left
        if (isSafe(r, c - 1)) backtrack(r, c - 1, path + 'L');
        // Right
        if (isSafe(r, c + 1)) backtrack(r, c + 1, path + 'R');
        // Up
        if (isSafe(r - 1, c)) backtrack(r - 1, c, path + 'U');
        
        visited[r][c] = false; // Backtrack
    }
    
    backtrack(0, 0, "");
    return result;
}
```

---

## 3. Bit Manipulation in JavaScript

Bit manipulation is an area where JavaScript differs significantly from Java, and these differences can easily lead to bugs if you aren't careful.

### Java vs JavaScript Bitwise: CRITICAL DIFFERENCES

**Java:**
- `int` is a 32-bit signed integer.
- `long` is a 64-bit signed integer.
- Bitwise operators on `int` work on 32 bits, and on `long` they work on 64 bits.

**JavaScript:**
- Internally, all numbers in standard JavaScript (excluding `BigInt`) are stored as **64-bit floating-point numbers** (IEEE 754 double precision).
- **CRITICAL:** However, when you perform a bitwise operation in JavaScript, the engine converts the number to a **32-bit SIGNED integer**, performs the operation, and then converts the result back to a 64-bit float.

**Consequences:**
1.  **32-Bit Limit:** Bitwise operations in standard JS are strictly limited to 32 bits. If you try to use bitwise operations on numbers larger than `2^31 - 1`, the upper bits will be discarded, leading to incorrect results.
2.  **Signed Results:** Because it converts to a *signed* 32-bit integer, operations can result in negative numbers if the 31st bit (sign bit) is set.
3.  **Unsigned Right Shift (`>>>`):** JavaScript introduces a new operator `>>>` which performs a right shift but fills the leftmost bits with zeros, regardless of the sign. This effectively treats the 32-bit integer as unsigned. **Java does not have an equivalent operator for `int` (though it exists, it behaves differently).**

### JavaScript Bitwise Operators

```javascript
let a = 5;  // 00000000 00000000 00000000 00000101
let b = 3;  // 00000000 00000000 00000000 00000011

// 1. AND (&): Sets bit if both are 1
console.log(a & b); // 1  (00000000 ... 00000001)

// 2. OR (|): Sets bit if either is 1
console.log(a | b); // 7  (00000000 ... 00000111)

// 3. XOR (^): Sets bit if they differ
console.log(a ^ b); // 6  (00000000 ... 00000110)

// 4. NOT (~): Inverts all bits (Two's Complement)
console.log(~a);    // -6
// Note: ~x is equivalent to -(x + 1) in Two's complement

// 5. Left Shift (<<): Shifts bits left, fills right with 0s. Equivalent to multiplying by 2^n
console.log(a << 1); // 10 (5 * 2^1)

// 6. Sign-Propagating Right Shift (>>): Shifts bits right, preserves sign bit. Equivalent to integer division by 2^n
let neg = -5;
console.log(neg >> 1); // -3

// 7. Zero-Fill Right Shift (>>>): Shifts bits right, fills left with 0s. 
// treats the number as an unsigned 32-bit integer.
console.log(neg >>> 1); // 2147483645 (Massive positive number)
```

### The `>>> 0` Trick (Unsigned Conversion)

Because JS bitwise ops result in signed integers, sometimes you need to interpret the 32 bits as an unsigned integer. You can do this by applying `>>> 0`.

```javascript
let x = -1; // 11111111 11111111 11111111 11111111 (as 32-bit signed)
console.log(x); // -1

// Convert to unsigned representation
let unsignedX = x >>> 0;
console.log(unsignedX); // 4294967295 (2^32 - 1)
```

### Common Bit Tricks and Recipes

These tricks are identical in logic to Java, but you must keep the 32-bit limit in mind.

```javascript
// 1. Check if a number is Even or Odd
function isEven(x) {
    return (x & 1) === 0;
}
function isOdd(x) {
    return (x & 1) === 1;
}

// 2. Check if a number is a Power of 2
// Explanation: A power of 2 has only one bit set (e.g., 4 is 100).
// x-1 flips all bits after that bit (3 is 011).
// ANDing them gives 0.
function isPowerOfTwo(x) {
    return x > 0 && (x & (x - 1)) === 0;
}

// 3. Get the i-th bit (0-indexed from right)
function getBit(x, i) {
    return (x >> i) & 1;
}

// 4. Set the i-th bit to 1
function setBit(x, i) {
    return x | (1 << i);
}

// 5. Clear the i-th bit (set to 0)
function clearBit(x, i) {
    const mask = ~(1 << i);
    return x & mask;
}

// 6. Toggle the i-th bit
function toggleBit(x, i) {
    return x ^ (1 << i);
}

// 7. Clear the lowest set bit (removes the rightmost 1)
function clearLowestSetBit(x) {
    return x & (x - 1);
}
```

### Counting Set Bits (Hamming Weight)

**Brian Kernighan's Algorithm:**
Instead of checking every bit, this algorithm clears the lowest set bit in each iteration.

```javascript
/**
 * @param {number} n - a positive integer
 * @return {number}
 */
function hammingWeight(n) {
    let count = 0;
    while (n !== 0) {
        n = n & (n - 1); // Clears the lowest set bit
        count++;
    }
    return count;
}
```
*Time Complexity: O(k), where k is the number of set bits.*

### XOR Tricks

XOR (`^`) has unique properties that make it highly useful in DSA:
1.  `a ^ a = 0` (XORing a number with itself is 0)
2.  `a ^ 0 = a` (XORing with 0 preserves the number)
3.  XOR is commutative and associative: `a ^ b ^ c = a ^ c ^ b`

#### Find Single Number (LeetCode 136)
Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

```javascript
function singleNumber(nums) {
    // We can use reduce for a clean functional approach
    return nums.reduce((acc, current) => acc ^ current, 0);
    
    /* Imperative equivalent:
    let result = 0;
    for (let num of nums) {
        result ^= num;
    }
    return result;
    */
}
```

### Generating Subsets using Bitmasks

Instead of backtracking, we can use a bitmask to generate all subsets. For an array of size `N`, there are `2^N` subsets. We can represent each subset with a binary number from `0` to `2^N - 1`. If the `i-th` bit is set, include `nums[i]` in the subset.

```javascript
function generateSubsetsBitmask(nums) {
    const n = nums.length;
    const result = [];
    const totalSubsets = 1 << n; // 2^n
    
    // JS Limit Warning: '1 << n' works correctly up to n=30.
    // If n=31, 1<<31 becomes a negative number (-2147483648) in JS!
    // For n >= 31, you must use BigInt or Math.pow(2, n)
    
    for (let mask = 0; mask < totalSubsets; mask++) {
        const currentSubset = [];
        for (let i = 0; i < n; i++) {
            // Check if the i-th bit of mask is set
            if ((mask >> i) & 1) {
            // Alternative: if (mask & (1 << i))
                currentSubset.push(nums[i]);
            }
        }
        result.push(currentSubset);
    }
    
    return result;
}
```

### Bitmask Dynamic Programming (Bitmask DP)

In advanced DP problems, a state often needs to keep track of a set of visited/used items. If the number of items is small (e.g., `<= 20`), an integer bitmask is highly efficient.

```javascript
// Example usage snippet in Bitmask DP
let state = 0; // Represents no items used
// Add item i
state = state | (1 << i);
// Remove item i
state = state & ~(1 << i);
// Check if item i is used
let isUsed = (state >> i) & 1;
```

---

## 4. Practice Problems

Here is a curated list of problems to reinforce these concepts. Try solving them in JavaScript.

**Recursion & Backtracking:**
1.  **Letter Combinations of a Phone Number** (LeetCode 17) - Map building and standard string backtracking.
2.  **Generate Parentheses** (LeetCode 22) - Track open/close counts.
3.  **Combination Sum II** (LeetCode 40) - Handling duplicates in combination generation.
4.  **Palindrome Partitioning** (LeetCode 131) - Backtracking + string palindrome checking.
5.  **Restore IP Addresses** (LeetCode 93) - Segmenting a string.
6.  **Matchsticks to Square** (LeetCode 473) - Array partitioning into 4 equal sum subsets.
7.  **Find Unique Binary String** (LeetCode 1980) - Cantor's diagonal argument or standard backtracking.

**Bit Manipulation:**
8.  **Missing Number** (LeetCode 268) - Using XOR trick.
9.  **Counting Bits** (LeetCode 338) - DP + Bit Manipulation relation (`dp[i] = dp[i >> 1] + (i & 1)`).
10. **Reverse Bits** (LeetCode 190) - Must handle unsigned 32-bit correctly in JS.
11. **Number of 1 Bits** (LeetCode 191) - Brian Kernighan's.
12. **Bitwise AND of Numbers Range** (LeetCode 201) - Find common prefix.
13. **Maximum Product of Word Lengths** (LeetCode 318) - Using bitmasks to represent characters in a string.
14. **Subsets** (LeetCode 78) - Solve it again using the bitmask approach.
15. **Single Number III** (LeetCode 260) - Advanced XOR trick to separate numbers based on a differing bit.
