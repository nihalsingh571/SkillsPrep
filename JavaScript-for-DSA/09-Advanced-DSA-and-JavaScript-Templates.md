# Advanced DSA and JavaScript Templates

Welcome to the Advanced Data Structures and Algorithms guide tailored for JavaScript! This document bridges the gap between Java and JavaScript for DSA, providing complete implementations, reusable templates, cheat sheets, and performance optimizations.

## 1. Trie (Prefix Tree)

A Trie is an efficient information reTrieval data structure. Using Trie, search complexities can be brought to optimal limit (key length).

### Standard Trie Implementation
```javascript
class TrieNode {
    constructor() {
        this.children = {}; // Using an object as a hash map. Alternative: new Array(26).fill(null)
        this.isEnd = false;
    }
}

class Trie {
    constructor() { 
        this.root = new TrieNode(); 
    }
    
    insert(word) {
        let node = this.root;
        for(const c of word) {
            if(!node.children[c]) {
                node.children[c] = new TrieNode();
            }
            node = node.children[c];
        }
        node.isEnd = true;
    }
    
    search(word) {
        let node = this.root;
        for(const c of word) {
            if(!node.children[c]) return false;
            node = node.children[c];
        }
        return node.isEnd;
    }
    
    startsWith(prefix) {
        let node = this.root;
        for(const c of prefix) {
            if(!node.children[c]) return false;
            node = node.children[c];
        }
        return true;
    }
}
```

**Java Comparison:** Java uses `HashMap<Character, TrieNode>` or `TrieNode[] children = new TrieNode[26]`. In JavaScript, the plain object `{}` is highly optimized for key-value pairs (hash map). For purely alphabetic tries (a-z), an array of size 26 is also fine.

### Applications of Trie
- Word Dictionary with Wildcard
- Count Words with Prefix
- Longest Prefix Matching
- Autocomplete Systems

### XOR Trie (Maximum XOR of Two Numbers)
Used heavily in bitwise optimization problems.

```javascript
class XORTrieNode {
    constructor() { 
        this.children = [null, null]; // Only 0 and 1
    }
}

class XORTrie {
    constructor() { 
        this.root = new XORTrieNode(); 
    }
    
    insert(num) {
        let node = this.root;
        for(let i = 31; i >= 0; i--) {
            const bit = (num >> i) & 1;
            if(!node.children[bit]) {
                node.children[bit] = new XORTrieNode();
            }
            node = node.children[bit];
        }
    }
    
    maxXOR(num) {
        let node = this.root;
        let result = 0;
        for(let i = 31; i >= 0; i--) {
            const bit = (num >> i) & 1;
            const want = 1 - bit; // We want the opposite bit to maximize XOR
            
            if(node.children[want]) { 
                result |= (1 << i); 
                node = node.children[want]; 
            } else if (node.children[bit]) {
                node = node.children[bit];
            } else {
                break;
            }
        }
        return result;
    }
}
```

---

## 2. Fenwick Tree (Binary Indexed Tree)

A Fenwick tree is a data structure that can efficiently update elements and calculate prefix sums in a table of numbers.

```javascript
class FenwickTree {
    constructor(n) { 
        this.tree = new Array(n + 1).fill(0); 
        this.n = n; 
    }
    
    // Add delta to element at index i (1-indexed)
    update(i, delta) {  
        for(; i <= this.n; i += i & (-i)) {
            this.tree[i] += delta;
        }
    }
    
    // Get prefix sum from 1 to i
    query(i) {  
        let sum = 0;
        for(; i > 0; i -= i & (-i)) {
            sum += this.tree[i];
        }
        return sum;
    }
    
    // Get sum in range [l, r]
    rangeQuery(l, r) { 
        return this.query(r) - this.query(l - 1); 
    }
    
    // Build tree from array in O(n) instead of O(n log n)
    build(arr) {
        // Copy values to tree
        for(let i = 0; i < arr.length; i++) {
            this.tree[i + 1] = arr[i];
        }
        // Build prefix connections
        for(let i = 1; i <= this.n; i++) {
            const parent = i + (i & (-i));
            if(parent <= this.n) {
                this.tree[parent] += this.tree[i];
            }
        }
    }
}
```

**Explain:** `i & (-i)` extracts the lowest set bit. This is the core operation moving up the tree for updates, and moving down for queries. Both Java and JS need custom implementations.

**Applications:**
- Range Sum Queries
- Count Inversions
- Order Statistics Tree (Finding K-th smallest element dynamically)

---

## 3. Segment Tree

A segment tree allows answering range queries over an array effectively, while still being flexible enough to allow modifying the array.

```javascript
class SegmentTree {
    constructor(arr) {
        this.n = arr.length;
        this.tree = new Array(4 * this.n).fill(0);
        if (this.n > 0) {
            this.build(arr, 0, 0, this.n - 1);
        }
    }
    
    build(arr, node, start, end) {
        if(start === end) { 
            this.tree[node] = arr[start]; 
            return; 
        }
        const mid = Math.floor((start + end) / 2);
        this.build(arr, 2 * node + 1, start, mid);
        this.build(arr, 2 * node + 2, mid + 1, end);
        this.tree[node] = this.tree[2 * node + 1] + this.tree[2 * node + 2];
    }
    
    update(node, start, end, idx, val) {
        if(start === end) { 
            this.tree[node] = val; 
            return; 
        }
        const mid = Math.floor((start + end) / 2);
        if(idx <= mid) {
            this.update(2 * node + 1, start, mid, idx, val);
        } else {
            this.update(2 * node + 2, mid + 1, end, idx, val);
        }
        this.tree[node] = this.tree[2 * node + 1] + this.tree[2 * node + 2];
    }
    
    query(node, start, end, l, r) {
        if(r < start || end < l) return 0; // Completely outside
        if(l <= start && end <= r) return this.tree[node]; // Completely inside
        
        const mid = Math.floor((start + end) / 2);
        return this.query(2 * node + 1, start, mid, l, r) + 
               this.query(2 * node + 2, mid + 1, end, l, r);
    }
    
    // Public API
    pointUpdate(idx, val) { 
        this.update(0, 0, this.n - 1, idx, val); 
    }
    
    rangeQuery(l, r) { 
        return this.query(0, 0, this.n - 1, l, r); 
    }
}
```

**Explain:** The segment tree has `4n` nodes max. The left child of a node is `2 * node + 1`, right is `2 * node + 2`. 
For lazy propagation (range updates), an additional `lazy` array of size `4n` is required to defer updates to children until explicitly queried.

---

## 4. Sparse Table (Range Minimum Query)

Sparse tables answer Range Minimum Queries in O(1) time after an O(N log N) preprocessing step.

```javascript
function buildSparseTable(arr) {
    const n = arr.length;
    const LOG = Math.floor(Math.log2(n)) + 1;
    
    // Initialize sparse table
    const sparse = Array.from({ length: LOG }, () => new Array(n).fill(0));
    
    // Base case: length 1 intervals
    sparse[0] = [...arr];
    
    // DP for intervals of length 2^j
    for(let j = 1; j < LOG; j++) {
        for(let i = 0; i + (1 << j) <= n; i++) {
            sparse[j][i] = Math.min(
                sparse[j - 1][i], 
                sparse[j - 1][i + (1 << (j - 1))]
            );
        }
    }
    return { sparse, LOG };
}

function queryMin(sparse, LOG, l, r) {
    const k = Math.floor(Math.log2(r - l + 1));
    return Math.min(
        sparse[k][l], 
        sparse[k][r - (1 << k) + 1]
    );
}
```
**Explain:** Preprocessing computes min for ranges of length 1, 2, 4, 8... For a query range, we take the overlapping bounds of the largest power of 2 that fits.

---

## 5. Monotonic Stack Template

A monotonic stack maintains values in a strictly increasing or decreasing order.

```javascript
// Next Greater Element to the right
function nextGreater(arr) {
    const n = arr.length;
    const result = new Array(n).fill(-1);
    const stack = []; // Stores indices
    
    for(let i = 0; i < n; i++) {
        while(stack.length > 0 && arr[stack[stack.length - 1]] < arr[i]) {
            result[stack.pop()] = arr[i];
        }
        stack.push(i);
    }
    return result;
}

// Next Smaller Element
function nextSmaller(arr) {
    const n = arr.length;
    const result = new Array(n).fill(-1);
    const stack = [];
    
    for(let i = 0; i < n; i++) {
        while(stack.length > 0 && arr[stack[stack.length - 1]] > arr[i]) {
            result[stack.pop()] = arr[i];
        }
        stack.push(i);
    }
    return result;
}

// Previous Greater Element (traverse right to left, or adapt logic)
function previousGreater(arr) {
    const n = arr.length;
    const result = new Array(n).fill(-1);
    const stack = [];
    
    for(let i = n - 1; i >= 0; i--) {
        while(stack.length > 0 && arr[stack[stack.length - 1]] < arr[i]) {
            result[stack.pop()] = arr[i];
        }
        stack.push(i);
    }
    return result;
}

// Trapping Rain Water using Monotonic Stack
function trap(height) {
    let ans = 0, current = 0, stack = [];
    while (current < height.length) {
        while (stack.length > 0 && height[current] > height[stack[stack.length - 1]]) {
            const top = stack.pop();
            if (stack.length === 0) break;
            const distance = current - stack[stack.length - 1] - 1;
            const bounded_height = Math.min(height[current], height[stack[stack.length - 1]]) - height[top];
            ans += distance * bounded_height;
        }
        stack.push(current++);
    }
    return ans;
}
```

---

## 6. Monotonic Queue (Sliding Window Max)

Maintains a deque of useful elements for sliding window problems.

```javascript
function maxSlidingWindow(nums, k) {
    const deque = []; // Stores indices
    const result = [];
    
    for(let i = 0; i < nums.length; i++) {
        // 1. Remove elements out of window
        while(deque.length > 0 && deque[0] < i - k + 1) {
            deque.shift(); 
            // Note: in pure JS, array shift is O(n), but for sliding window the amortized 
            // cost is minimal because elements are processed once. 
            // For strict O(1), use a custom deque or a front pointer.
        }
        
        // 2. Remove smaller elements as they are useless
        while(deque.length > 0 && nums[deque[deque.length - 1]] < nums[i]) {
            deque.pop();
        }
        
        // 3. Add current element
        deque.push(i);
        
        // 4. Output max for current window
        if(i >= k - 1) {
            result.push(nums[deque[0]]);
        }
    }
    return result;
}
```

---

## 7. LRU Cache

Least Recently Used Cache implementation.

```javascript
class LRUCache {
    constructor(capacity) {
        this.capacity = capacity;
        this.map = new Map();  // Map maintains insertion order in JS!
    }
    
    get(key) {
        if(!this.map.has(key)) return -1;
        
        // Refresh the key by deleting and re-inserting
        const val = this.map.get(key);
        this.map.delete(key);
        this.map.set(key, val);  // Moves to end (most recently used)
        return val;
    }
    
    put(key, value) {
        // If it exists, remove it so we can update and move to end
        if(this.map.has(key)) {
            this.map.delete(key);
        } else if(this.map.size >= this.capacity) {
            // Delete oldest (the first item in the Map iterator)
            const oldestKey = this.map.keys().next().value;
            this.map.delete(oldestKey);
        }
        
        // Insert new item at the end
        this.map.set(key, value);
    }
}
```

**Key insight:** JavaScript's `Map` object maintains insertion order — this is guaranteed by the ES6 spec! This allows us to implement LRU cache in O(1) time without needing a custom Doubly-Linked List + Hash Map (which Java requires unless using `LinkedHashMap`).

---

## 8. Complete Template Library (copy-paste ready)

```javascript
// === INPUT TEMPLATE ===
const fs = require('fs');
// Handles competitive programming inputs via stdin
const lines = fs.readFileSync(0, 'utf8').trim().split(/\s+/);
let idx = 0;
const nextString = () => lines[idx++];
const nextInt = () => parseInt(nextString(), 10);
const nextInts = (n) => {
    let arr = [];
    for (let i = 0; i < n; i++) arr.push(nextInt());
    return arr;
};

// === BINARY SEARCH TEMPLATE ===
function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        if (arr[mid] === target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// === TWO POINTERS TEMPLATE ===
function twoPointers(arr, target) {
    let left = 0, right = arr.length - 1;
    while(left < right) {
        const sum = arr[left] + arr[right];
        if(sum === target) return [left, right];
        if(sum < target) left++;
        else right--;
    }
    return [-1, -1];
}

// === SLIDING WINDOW TEMPLATE ===
function slidingWindow(arr, k) {
    let sum = 0, maxSum = 0;
    for(let i = 0; i < arr.length; i++) {
        sum += arr[i];
        if(i >= k - 1) {
            maxSum = Math.max(maxSum, sum);
            sum -= arr[i - (k - 1)]; // Remove leftmost
        }
    }
    return maxSum;
}

// === PREFIX SUM TEMPLATE ===
function prefixSum(arr) {
    const n = arr.length;
    const prefix = new Array(n + 1).fill(0);
    for(let i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    return prefix;
    // sum(l, r) = prefix[r + 1] - prefix[l]
}

// === EFFICIENT QUEUE TEMPLATE ===
class Queue {
    constructor() {
        this.items = [];
        this.front = 0;
    }
    push(val) { this.items.push(val); }
    pop() { return this.front < this.items.length ? this.items[this.front++] : undefined; }
    peek() { return this.front < this.items.length ? this.items[this.front] : undefined; }
    isEmpty() { return this.front >= this.items.length; }
    size() { return this.items.length - this.front; }
}

// === BFS TEMPLATE ===
function bfs(startNode) {
    const q = new Queue();
    const visited = new Set();
    
    q.push(startNode);
    visited.add(startNode);
    
    let steps = 0;
    while(!q.isEmpty()) {
        const size = q.size();
        for(let i = 0; i < size; i++) {
            const node = q.pop();
            // Process node
            for(const neighbor of getNeighbors(node)) {
                if(!visited.has(neighbor)) {
                    visited.add(neighbor);
                    q.push(neighbor);
                }
            }
        }
        steps++;
    }
}

// === DFS TEMPLATE ===
function dfs(node, visited = new Set()) {
    if(visited.has(node)) return;
    visited.add(node);
    
    // Process node
    for(const neighbor of getNeighbors(node)) {
        dfs(neighbor, visited);
    }
}

// === DIJKSTRA TEMPLATE ===
// Note: Requires a priority queue. Here is a simplified greedy approach for dense graphs.
// For sparse graphs, implement a MinHeap class.
function dijkstra(n, edges, start) {
    const graph = Array.from({length: n}, () => []);
    for(const [u, v, w] of edges) graph[u].push([v, w]);
    
    const dist = new Array(n).fill(Infinity);
    const visited = new Array(n).fill(false);
    dist[start] = 0;
    
    for(let i = 0; i < n; i++) {
        let u = -1;
        for(let j = 0; j < n; j++) {
            if(!visited[j] && (u === -1 || dist[j] < dist[u])) u = j;
        }
        if(dist[u] === Infinity) break;
        visited[u] = true;
        
        for(const [v, w] of graph[u]) {
            if(dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    return dist;
}

// === DSU (DISJOINT SET) TEMPLATE ===
class DSU {
    constructor(n) {
        this.parent = Array.from({length: n}, (_, i) => i);
        this.rank = new Array(n).fill(1);
    }
    
    find(i) {
        if(this.parent[i] === i) return i;
        return this.parent[i] = this.find(this.parent[i]); // Path compression
    }
    
    union(i, j) {
        const rootI = this.find(i);
        const rootJ = this.find(j);
        if(rootI === rootJ) return false;
        
        if(this.rank[rootI] < this.rank[rootJ]) {
            this.parent[rootI] = rootJ;
        } else if(this.rank[rootI] > this.rank[rootJ]) {
            this.parent[rootJ] = rootI;
        } else {
            this.parent[rootJ] = rootI;
            this.rank[rootI]++;
        }
        return true;
    }
}

// === HEAP (MINHEAP) TEMPLATE ===
class MinHeap {
    constructor(compareFunc = (a, b) => a - b) {
        this.heap = [];
        this.compare = compareFunc;
    }
    
    push(val) {
        this.heap.push(val);
        this._siftUp();
    }
    
    pop() {
        if (this.size() === 0) return null;
        if (this.size() === 1) return this.heap.pop();
        
        const top = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._siftDown();
        return top;
    }
    
    peek() { return this.size() > 0 ? this.heap[0] : null; }
    size() { return this.heap.length; }
    isEmpty() { return this.heap.length === 0; }
    
    _siftUp() {
        let nodeIdx = this.heap.length - 1;
        while(nodeIdx > 0) {
            const parentIdx = Math.floor((nodeIdx - 1) / 2);
            if (this.compare(this.heap[nodeIdx], this.heap[parentIdx]) >= 0) break;
            
            [this.heap[nodeIdx], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[nodeIdx]];
            nodeIdx = parentIdx;
        }
    }
    
    _siftDown() {
        let nodeIdx = 0;
        const length = this.heap.length;
        
        while(true) {
            const leftChildIdx = 2 * nodeIdx + 1;
            const rightChildIdx = 2 * nodeIdx + 2;
            let smallestIdx = nodeIdx;
            
            if(leftChildIdx < length && this.compare(this.heap[leftChildIdx], this.heap[smallestIdx]) < 0) {
                smallestIdx = leftChildIdx;
            }
            if(rightChildIdx < length && this.compare(this.heap[rightChildIdx], this.heap[smallestIdx]) < 0) {
                smallestIdx = rightChildIdx;
            }
            if(smallestIdx === nodeIdx) break;
            
            [this.heap[nodeIdx], this.heap[smallestIdx]] = [this.heap[smallestIdx], this.heap[nodeIdx]];
            nodeIdx = smallestIdx;
        }
    }
}

// === BACKTRACKING TEMPLATE ===
function backtrack(arr) {
    const result = [];
    
    function dfs(path, options) {
        // Base case
        if(path.length === arr.length) {
            result.push([...path]); // Push a copy
            return;
        }
        
        // Explore choices
        for(let i = 0; i < options.length; i++) {
            // Choose
            path.push(options[i]);
            
            // Explore (exclude chosen element if needed)
            const nextOptions = options.slice(0, i).concat(options.slice(i + 1));
            dfs(path, nextOptions);
            
            // Un-choose (Backtrack)
            path.pop();
        }
    }
    
    dfs([], arr);
    return result;
}

// === 1D DP TEMPLATE ===
function dp1d(n) {
    const dp = new Array(n + 1).fill(0);
    dp[0] = 1; // Base case
    dp[1] = 1;
    for(let i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2]; // Transition
    }
    return dp[n];
}

// === 2D DP TEMPLATE ===
function dp2d(m, n) {
    const dp = Array.from({length: m}, () => new Array(n).fill(0));
    dp[0][0] = 1; // Base case
    
    for(let i = 0; i < m; i++) {
        for(let j = 0; j < n; j++) {
            if(i > 0) dp[i][j] += dp[i - 1][j];
            if(j > 0) dp[i][j] += dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}

// === KNAPSACK TEMPLATE ===
function knapsack(weights, values, capacity) {
    const n = weights.length;
    const dp = Array.from({length: n + 1}, () => new Array(capacity + 1).fill(0));
    
    for(let i = 1; i <= n; i++) {
        const w = weights[i - 1];
        const v = values[i - 1];
        for(let j = 0; j <= capacity; j++) {
            if(w <= j) {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i - 1][j - w] + v);
            } else {
                dp[i][j] = dp[i - 1][j];
            }
        }
    }
    return dp[n][capacity];
}
```

---

## 9. JavaScript Performance Guide for DSA

When transitioning from Java to JavaScript for Competitive Programming or LeetCode, keep these performance tips in mind:

1. **Operations Limit:** O(n) is perfectly fine up to $10^8$ operations. Modern V8 engines can comfortably execute around $10^8$ basic operations per second.
2. **Loops vs Methods:** Prefer standard `for` loops over higher-order functions like `.map()`, `.filter()`, or `.reduce()` in highly performance-critical code. Function calls have overhead.
3. **Queue Implementations:** Using `Array.prototype.shift()` is $O(N)$ because it reindexes the array. In a BFS loop, this causes $O(N^2)$ complexity. ALWAYS use a front pointer `q[front++]` as shown in the template.
4. **String Operations:** String concatenation (`str += char`) inside a loop creates many intermediate strings and can degrade to $O(N^2)$. Instead, push to an array and use `arr.join('')` at the end.
5. **Math.max() Overflow:** `Math.max(...arr)` will throw a Maximum Call Stack Size Exceeded error for arrays larger than ~100,000 elements. Use `arr.reduce((a, b) => Math.max(a, b), -Infinity)` or a manual loop instead.
6. **Object vs Map vs Array:** 
   - Fixed size small arrays are very fast.
   - For associative arrays, use `new Map()` instead of `{}` if keys are added/removed frequently, as `Map` is optimized for this and maintains order.
   - Lookups are generally $O(1)$ amortized for Map/Set.
7. **Sorting:** The built-in `Array.prototype.sort()` is well optimized (usually TimSort or QuickSort, $O(N \log N)$), but **YOU MUST** provide a comparator `(a, b) => a - b` for numbers, otherwise it sorts them as strings (e.g., `10` comes before `2`).
8. **Memory Allocation:** Avoid creating arrays inside tight loops if possible. Reuse variables or preallocate arrays with `new Array(size)` rather than pushing repeatedly if the exact size is known.

---

*This concludes the Advanced DSA and JavaScript Templates guide. Use these implementations as a reference when solving complex algorithmic problems.*
