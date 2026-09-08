# DSA Patterns, Cheat Sheets, and Practice Roadmap

This is your ultimate revision manual. It contains everything you need to transition your Java DSA knowledge to JavaScript, avoid common JS traps, recognize algorithmic patterns, and follow a structured roadmap.

---

## SECTION 1: Comprehensive Java → JavaScript DSA Cheat Sheet

| Java | JavaScript | Notes |
|---|---|---|
| `int x = 5;` | `let x = 5;` | JavaScript is dynamically typed. |
| `final int X = 5;` | `const X = 5;` | `const` protects the binding, not the object. |
| `long x = 5L;` | `let x = 5;` or `5n` | For integers > $2^{53}-1$, use BigInt (e.g. `123456789n`). |
| `boolean` | `boolean` | Uses `true` and `false`. |
| `String s = "hi";` | `const s = 'hi';` or `"hi";` | Backticks `` `hi` `` allow template literals. |
| `char c = 'a';` | `const c = 'a';` | JS has no `char` type, only strings of length 1. |
| `int[] arr = new int[n];` | `const arr = new Array(n).fill(0);` | Highly recommended to fill initialization. |
| `int[] arr = {1, 2, 3};` | `const arr = [1, 2, 3];` | Array literals. |
| `arr.length` | `arr.length` | Property, no parentheses. |
| `String s = s.length();` | `s.length` | Property in JS, not a method! |
| `Arrays.sort(arr)` | `arr.sort((a,b)=>a-b)` | **CRITICAL:** Without comparator, JS sorts lexicographically! |
| `Collections.sort(list)` | `arr.sort((a,b)=>a-b)` | Works on the array in-place. |
| `ArrayList<Integer> l = new ArrayList<>()` | `const arr = [];` | Arrays in JS are inherently dynamic. |
| `list.add(x)` | `arr.push(x)` | |
| `list.get(i)` | `arr[i]` | |
| `list.size()` | `arr.length` | |
| `list.remove(list.size()-1)` | `arr.pop()` | |
| `list.remove(0)` | `arr.shift()` | **[O(n) time!]** Use front pointer instead. |
| `HashMap<K,V> map = new HashMap<>()` | `const map = new Map();` | Use `Map`, not `{}` for optimal DSA performance. |
| `map.put(k,v)` | `map.set(k,v)` | |
| `map.get(k)` | `map.get(k)` | Returns `undefined` if key does not exist. |
| `map.containsKey(k)` | `map.has(k)` | |
| `map.getOrDefault(k,0)` | `map.get(k) || 0` | Easy fallback using logical OR. |
| `map.remove(k)` | `map.delete(k)` | |
| `map.size()` | `map.size` | Property, no parentheses. |
| `HashSet<T> set = new HashSet<>()` | `const set = new Set();` | |
| `set.add(x)` | `set.add(x)` | |
| `set.contains(x)` | `set.has(x)` | |
| `set.remove(x)` | `set.delete(x)` | |
| `Stack<T> stack = new Stack<>()` | `const stack = [];` | Native arrays act as stacks. |
| `stack.push(x)` | `stack.push(x)` | |
| `stack.pop()` | `stack.pop()` | |
| `stack.peek()` | `stack[stack.length-1]` | |
| `stack.isEmpty()` | `stack.length === 0` | |
| `Queue<T> q = new LinkedList<>()` | `const q=[]; let front=0;` | Avoid `shift()`. Use a pointer. |
| `q.offer(x)` | `q.push(x)` | |
| `q.poll()` | `q[front++]` | Lazy deletion. |
| `q.peek()` | `q[front]` | |
| `q.isEmpty()` | `front >= q.length` | |
| `PriorityQueue<T> pq = new PriorityQueue<>()` | `class MinHeap {...}` | **Custom implementation required in JS.** |
| `StringBuilder sb = new StringBuilder()` | `const parts = [];` | Arrays are best for string building. |
| `sb.append(x)` | `parts.push(x)` | |
| `sb.toString()` | `parts.join('')` | High performance string joining. |
| `Integer.MAX_VALUE` | `Infinity` or `Number.MAX_SAFE_INTEGER` | |
| `Integer.MIN_VALUE` | `-Infinity` or `Number.MIN_SAFE_INTEGER`| |
| `Integer.parseInt(s)` | `parseInt(s)` or `Number(s)` | |
| `String.valueOf(x)` | `String(x)` or `${x}` | |
| `(char)(c + 1)` | `String.fromCharCode(c.charCodeAt(0)+1)`| |
| `c - 'a'` | `s.charCodeAt(i) - 97` | JS strings don't subtract directly. |
| `Math.max(a,b)` | `Math.max(a,b)` | |
| `Math.min(a,b)` | `Math.min(a,b)` | |
| `Math.abs(x)` | `Math.abs(x)` | |
| `Math.sqrt(x)` | `Math.sqrt(x)` | |
| `Math.pow(a,b)` | `Math.pow(a,b)` or `a**b` | |
| `Math.floor(x)` | `Math.floor(x)` | |
| `Math.ceil(x)` | `Math.ceil(x)` | |
| `System.out.println(x)` | `console.log(x)` | |
| `Arrays.fill(arr, val)` | `arr.fill(val)` | |
| `Arrays.copyOf(arr, n)` | `arr.slice(0, n)` | |
| `Collections.reverse(list)` | `arr.reverse()` | **In-place mutation!** |
| `Collections.max(list)` | `Math.max(...arr)` | Warning: stack overflow for n > 100k. Use reduce. |
| `for(int x : arr)` | `for(const x of arr)` | |
| `null` | `null` | |
| `Scanner sc = new Scanner(System.in)` | `fs.readFileSync(0,'utf8')` | |

---

## SECTION 2: JavaScript DSA Traps Checklist

1. **`sort()` without comparator**
   - *Problem:* `[10, 2, 1].sort()` results in `[1, 10, 2]`. Lexicographic by default.
   - *Fix:* `arr.sort((a, b) => a - b)`.

2. **`shift()` in tight loop**
   - *Problem:* Using `shift()` for a queue processing $N$ items takes $O(N^2)$ time.
   - *Fix:* Use `let front = 0; q[front++]` instead.

3. **`Array.fill()` with reference**
   - *Problem:* `new Array(3).fill([])` creates a 3-element array pointing to the *same* inner array.
   - *Fix:* `Array.from({length: 3}, () => [])`.

4. **`==` vs `===`**
   - *Problem:* `0 == "0"` is true. Type coercion can hide bugs.
   - *Fix:* Always use strict equality `===` and `!==`.

5. **Number precision**
   - *Problem:* `0.1 + 0.2 === 0.3` is `false`. Floating point precision errors.
   - *Fix:* `Math.abs(a - b) < Number.EPSILON` or work with integers.

6. **BigInt + Number**
   - *Problem:* `10n + 5` throws `TypeError: Cannot mix BigInt and other types`.
   - *Fix:* Explicit conversion: `10n + BigInt(5)`.

7. **String Concatenation in Math**
   - *Problem:* `'5' + 2` is `'52'`.
   - *Fix:* Use `Number('5') + 2`.

8. **`parseInt` vs `Number`**
   - *Problem:* `parseInt('')` is `NaN`, `Number('')` is `0`.
   - *Fix:* Know the difference. Usually `Number(x)` is stricter and safer.

9. **Object References**
   - *Problem:* `let b = a` copies the reference, not the array/object. Modifying `b` modifies `a`.
   - *Fix:* Shallow copy: `let b = [...a]`. Deep copy: `structuredClone(a)`.

10. **`const` Mutability**
    - *Problem:* `const arr = []; arr.push(1);` is perfectly legal. `const` prevents reassignment, not mutation.
    - *Fix:* Understand `const` limits.

11. **`Math.max(...largeArr)`**
    - *Problem:* Destructuring `...` puts elements on the call stack. Throws error for $N > 100,000$.
    - *Fix:* `largeArr.reduce((a,b) => Math.max(a,b), -Infinity)`.

12. **Negative modulo**
    - *Problem:* `-5 % 3` is `-2` in JavaScript, not `1`.
    - *Fix:* `((x % n) + n) % n`.

13. **Bitwise on large numbers**
    - *Problem:* Bitwise operators operate on 32-bit signed integers. They break on numbers > $2^{31}-1$.
    - *Fix:* Use Math operations or BigInt for large masks.

14. **NaN comparisons**
    - *Problem:* `NaN === NaN` is `false`.
    - *Fix:* Use `Number.isNaN(x)`.

15. **Recursion depth**
    - *Problem:* JS engine stack size is around 10,000. Deep DFS can throw stack overflow.
    - *Fix:* Use iterative DFS with a stack for very deep graphs.

16. **Pushing Arrays in Backtracking**
    - *Problem:* `result.push(current)` pushes the reference. All answers will look identical later.
    - *Fix:* `result.push([...current])`.

17. **`for...in` on arrays**
    - *Problem:* Iterates over keys (indices as strings), not values!
    - *Fix:* Use `for...of` for arrays.

18. **Infinity arithmetic**
    - *Problem:* `Infinity - Infinity` is `NaN`.
    - *Fix:* Be careful initializing distances in DP/Graphs.

19. **Object key coercion**
    - *Problem:* `obj[1] === obj['1']`. All object keys become strings.
    - *Fix:* Use `Map` if you need true integer or object keys.

20. **`undefined` vs `null`**
    - *Problem:* `map.get(missing)` returns `undefined`. If you check `if (map.get(k))`, it fails on values that are `0` or `false`.
    - *Fix:* Use `map.has(k)` or `map.get(k) !== undefined`.

---

## SECTION 3: Pattern Recognition Table

| Problem Signal | Algorithm/Pattern | Time Complexity |
|---|---|---|
| Find pair with target sum | Two Pointers (sorted) / HashMap | O(n) / O(n) |
| Contiguous subarray | Sliding Window / Prefix Sum | O(n) |
| Sorted array search | Binary Search | O(log n) |
| Next greater element | Monotonic Stack | O(n) |
| Shortest path unweighted | BFS | O(V+E) |
| Shortest path weighted (non-neg) | Dijkstra | O(E log V) |
| Shortest path (negative weights) | Bellman-Ford | O(VE) |
| All pairs shortest path | Floyd-Warshall | O(V³) |
| Dependencies / ordering | Topological Sort | O(V+E) |
| Connected components | DFS/BFS/DSU | O(V+E) |
| Repeated min/max queries | Heap | O(log n) per query |
| All combinations/subsets | Backtracking | O(2^n) |
| Overlapping subproblems | DP | varies |
| Prefix string matching | Trie | O(L) |
| Range sum queries | Prefix Sum / Fenwick / Segment Tree | O(1)/O(log n) |
| Range min/max queries (static) | Sparse Table | O(1) query |
| String pattern matching | KMP / Z-algorithm | O(n+m) |
| Island counting | BFS/DFS on grid | O(rows×cols) |
| Cycle detection | Floyd's / DFS with color | O(n) |
| Minimum spanning tree | Kruskal / Prim | O(E log V) |
| Dynamic connectivity | DSU | O(α(n)) per op |
| Frequency count | HashMap / Array | O(n) |
| Sliding window max/min | Monotonic Deque | O(n) |
| Merge intervals | Sort + greedy | O(n log n) |
| K-th largest/smallest | Heap / QuickSelect | O(n log k) / O(n) avg |
| Median of stream | Two Heaps | O(log n) per insert |
| Binary string XOR maximize | XOR Trie | O(n × bits) |
| Graph coloring (2-color) | Bipartite BFS | O(V+E) |
| Maximum flow | Ford-Fulkerson / Dinic | O(V×E²) |
| Inversion count | Merge Sort / BIT | O(n log n) |
| Longest subsequence | DP / Patience Sort | O(n²) / O(n log n) |
| Permutations of string/array | Backtracking | O(n!) |
| Matrix rotation/spiral | Simulation | O(n²) |
| Balanced parentheses | Stack | O(n) |
| Expression evaluation | Stack | O(n) |
| Sum of subsets = target | Backtracking / DP | O(2^n) / O(n×target) |

---

## SECTION 4: Problem-Solving Framework

Follow these 12 steps consistently to structure your thinking:

1. **Read carefully** — What is asked exactly? Do not skim.
2. **Input/output** — Understand types, formats, and guarantees.
3. **Constraints** — Is $N$ up to $100$? (O(n³)). Up to $10^5$? (O(n log n)).
4. **Create 2-3 examples manually** — Walk through simple edge cases.
5. **Edge cases** — Empty arrays, single elements, negatives, huge numbers, duplicates.
6. **Brute force** — What's the simplest, most naïve working solution?
7. **Complexity of brute force** — Will it Time Limit Exceed (TLE)?
8. **Optimize** — Find bottlenecks. Can a HashMap, Heap, or Binary Search help?
9. **Identify pattern** — Check the Pattern Recognition Table.
10. **Write pseudocode first** — Do not write code immediately.
11. **Convert to JavaScript carefully** — Watch out for JS traps!
12. **Test all edge cases** — Dry run the code manually.

---

## SECTION 5: Edge Case Checklist

Before submitting, check your code against these inputs:

- **Array:** Empty `[]`, single `[x]`, all duplicates `[5,5,5,5]`, sorted asc/desc, negatives, zeroes.
- **Math/Numbers:** Integer overflow (use BigInt if needed), precision, dividing by zero.
- **Hash/Maps:** Duplicate keys, zero as value, empty maps.
- **Strings:** Empty string `""`, length 1 `"a"`, all same chars `"aaaa"`, spaces, special chars.
- **Trees:** `null` root, single node, skewed tree (linked list behavior).
- **Graphs:** Disconnected components, self-loops, multiple edges, isolated nodes.
- **Constraints Constraints:** Test the minimum and maximum possible inputs.

---

## SECTION 6: TLE Prevention Guide

If you get "Time Limit Exceeded", check constraints against safe time complexities:
- $O(N)$ is safe for $N \le 10^7$
- $O(N \log N)$ is safe for $N \le 10^6$
- $O(N^2)$ is safe for $N \le 5000$
- $O(N^3)$ is safe for $N \le 500$
- $O(2^N)$ is safe for $N \le 20$
- $O(N!)$ is safe for $N \le 11$

**JavaScript specific TLE causes:**
- Calling `.shift()` repeatedly.
- String concatenation `s += c` inside a loop.
- `.map().filter().reduce()` chains (creates multiple arrays, huge overhead).
- `.indexOf()` inside a loop (makes it $O(N^2)$).
- Sorting repeatedly.

---

## SECTION 7: Practice Roadmap (LeetCode-focused)

For mastery, complete these in order:

1. **Arrays & Hashing:** Two Sum, Valid Anagram, Contains Duplicate, Group Anagrams, Top K Frequent Elements.
2. **Two Pointers:** Valid Palindrome, 3Sum, Container With Most Water, Trapping Rain Water.
3. **Sliding Window:** Best Time to Buy/Sell, Longest Substring Without Repeats, Minimum Window Substring.
4. **Stack:** Valid Parentheses, Min Stack, Daily Temperatures, Largest Rectangle in Histogram.
5. **Binary Search:** Binary Search, Search 2D Matrix, Koko Eating Bananas, Search in Rotated Array.
6. **Linked List:** Reverse List, Merge Two Lists, Reorder List, Remove Nth Node, LRU Cache.
7. **Trees:** Maximum Depth, Invert Tree, Lowest Common Ancestor, Validate BST, Serialize/Deserialize.
8. **Tries:** Implement Trie, Design Add/Search Word, Word Search II.
9. **Heaps:** Kth Largest, Last Stone Weight, Find Median from Data Stream.
10. **Backtracking:** Subsets, Combination Sum, Permutations, N-Queens.
11. **Graphs:** Number of Islands, Clone Graph, Pacific Atlantic Water Flow, Course Schedule, Word Ladder.
12. **Advanced Graphs:** Network Delay Time (Dijkstra), Cheapest Flights (Bellman-Ford), Min Cost to Connect Points (Prim/Kruskal).
13. **1D DP:** Climbing Stairs, House Robber, Word Break, Coin Change.
14. **2D DP:** Unique Paths, Longest Common Subsequence, Edit Distance.

---

## SECTION 8: Final Interview Checklist

1. Did I clarify assumptions?
2. Are variable names descriptive?
3. Did I mention Space and Time complexities loudly and clearly?
4. Are my base cases correct?
5. Have I DRY-run the code with a small example?
6. Did I handle empty inputs?
7. Is my JavaScript idiomatic?
8. Did I avoid global variables?
9. Are there any unnecessary copies or loops?
10. Is the code modular?

---

## SECTION 9: ONE-PAGE JavaScript DSA Cheat Sheet

Print this or keep it on your second monitor during coding!

```javascript
VARIABLES: let x=5; const arr=[]; const MAP=new Map(); const SET=new Set();
LOOPS: for(let i=0;i<n;i++) | for(const x of arr) | while(cond) {}
FUNCTION: function f(a,b){return a+b;} | const f=(a,b)=>a+b;
ARRAY: push/pop O(1) | shift/unshift O(n) | slice/indexOf/includes O(n)
SORT: arr.sort((a,b)=>a-b) [ALWAYS use comparator for numbers!]
STRING: s.length [no()] | s[i] | s.split('') | arr.join('')
MAP: new Map() | .set(k,v) | .get(k) | .has(k) | .delete(k) | .size
SET: new Set() | .add(x) | .has(x) | .delete(x) | .size
STACK: let s=[]; s.push(x); s.pop(); s[s.length-1]; [peek]
QUEUE: let q=[], f=0; q.push(x); q[f++]; [dequeue]
HEAP: class MinHeap{} [custom — NO built-in!]
BINARY SEARCH: left + Math.floor((right-left)/2)
MATH: Math.max/min/abs/floor/ceil/sqrt/pow | Infinity | -Infinity
INPUT: fs.readFileSync(0,'utf8').trim().split('\n')
OUTPUT: console.log(result) | console.log(arr.join(' '))
NUMBERS: Number.MAX_SAFE_INTEGER=2^53-1 | BigInt for larger
TRAPS: sort()→lexicographic | shift()→O(n) | fill([])→shared ref | === not ==
```
