# Trees, Binary Search Trees, and Heaps: Java to JavaScript

Welcome to the guide on non-linear data structures: Trees and Heaps. As a Java developer, you know that Java provides robust standard libraries (like `PriorityQueue`, `TreeMap`, `TreeSet`). In JavaScript, the standard library is notoriously bare-bones. You will often have to build these structures from scratch or rely on external packages. For DSA interviews in JS, you **must** know how to implement a Heap from scratch.

---

## 1. Binary Tree Node Representation

In Java, you define a class with member variables. In modern JavaScript (ES6+), the class syntax is very similar, though dynamically typed.

**Java:**
```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode(int x) { val = x; }
}
```

**JavaScript:**
```javascript
class TreeNode {
    // We can use default parameters in JS for cleaner constructors
    constructor(val = 0, left = null, right = null) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```
*Note: In JS, `null` is generally used to represent the absence of a child node, corresponding to Java's `null`.*

---

## 2. Tree Traversals

Traversals are the foundation of solving most tree problems. You must be comfortable with both recursive and iterative approaches.

### Depth-First Search (DFS)

#### A. Inorder Traversal (Left - Root - Right)

In a Binary Search Tree, Inorder traversal retrieves elements in sorted order.

**Recursive:**
```javascript
/**
 * @param {TreeNode} root
 * @return {number[]}
 */
function inorder(root) {
    if (!root) return [];
    // Using spread operator for functional style (though less memory efficient)
    return [...inorder(root.left), root.val, ...inorder(root.right)];
    
    /* More memory efficient approach (Standard):
    const result = [];
    function traverse(node) {
        if (!node) return;
        traverse(node.left);
        result.push(node.val);
        traverse(node.right);
    }
    traverse(root);
    return result;
    */
}
```

**Iterative:**
Iterative Inorder uses a manual stack.
```javascript
function inorderIterative(root) {
    const result = [];
    const stack = [];
    let curr = root;
    
    while (curr !== null || stack.length > 0) {
        // Go as far left as possible
        while (curr !== null) {
            stack.push(curr);
            curr = curr.left;
        }
        
        // Pop and process
        curr = stack.pop();
        result.push(curr.val);
        
        // Visit right subtree
        curr = curr.right;
    }
    
    return result;
}
```

#### B. Preorder Traversal (Root - Left - Right)

Useful for creating a copy of the tree or serializing it.

**Recursive:**
```javascript
function preorder(root) {
    const result = [];
    function traverse(node) {
        if (!node) return;
        result.push(node.val);
        traverse(node.left);
        traverse(node.right);
    }
    traverse(root);
    return result;
}
```

**Iterative:**
```javascript
function preorderIterative(root) {
    if (!root) return [];
    const result = [];
    const stack = [root];
    
    while (stack.length > 0) {
        const curr = stack.pop();
        result.push(curr.val);
        
        // Push RIGHT child first so LEFT is popped first (LIFO)
        if (curr.right) stack.push(curr.right);
        if (curr.left) stack.push(curr.left);
    }
    return result;
}
```

#### C. Postorder Traversal (Left - Right - Root)

Useful when you need data from children before processing the parent (e.g., deleting a tree, calculating height).

**Recursive:**
```javascript
function postorder(root) {
    const result = [];
    function traverse(node) {
        if (!node) return;
        traverse(node.left);
        traverse(node.right);
        result.push(node.val);
    }
    traverse(root);
    return result;
}
```

**Iterative (Two Stacks - easier to remember):**
```javascript
function postorderIterative(root) {
    if (!root) return [];
    const result = [];
    const stack1 = [root];
    const stack2 = [];
    
    while (stack1.length > 0) {
        const curr = stack1.pop();
        stack2.push(curr);
        
        if (curr.left) stack1.push(curr.left);
        if (curr.right) stack1.push(curr.right);
    }
    
    while (stack2.length > 0) {
        result.push(stack2.pop().val);
    }
    return result;
}
```

### Breadth-First Search (BFS) / Level Order

BFS is implemented using a Queue.
**Crucial JS Detail:** JavaScript Arrays do not have O(1) `shift()` (dequeue) operations. Calling `queue.shift()` is O(N) because it requires re-indexing the entire array.
For LeetCode, simulating a queue by keeping a `front` pointer is often necessary to avoid Time Limit Exceeded (TLE) errors on large datasets.

```javascript
/**
 * Level Order Traversal returning array of arrays
 * @param {TreeNode} root
 * @return {number[][]}
 */
function levelOrder(root) {
    if (!root) return [];
    
    const result = [];
    const queue = [root];
    let front = 0; // Pointer to simulate O(1) dequeue
    
    while (front < queue.length) {
        // Number of nodes in the current level
        const levelSize = queue.length - front;
        const currentLevel = [];
        
        for (let i = 0; i < levelSize; i++) {
            // Dequeue equivalent O(1)
            const node = queue[front++]; 
            
            currentLevel.push(node.val);
            
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
        
        result.push(currentLevel);
    }
    
    return result;
}
```

---

## 3. Common Tree Problems

Here are the templates for the most fundamental tree algorithms.

#### 1. Height / Maximum Depth of Binary Tree (LeetCode 104)

```javascript
function maxDepth(root) {
    if (!root) return 0;
    const leftDepth = maxDepth(root.left);
    const rightDepth = maxDepth(root.right);
    return 1 + Math.max(leftDepth, rightDepth);
}
```

#### 2. Diameter of Binary Tree (LeetCode 543)

The diameter is the length of the longest path between any two nodes. The path may or may not pass through the root.

```javascript
function diameterOfBinaryTree(root) {
    let maxDiam = 0;
    
    function depth(node) {
        if (!node) return 0;
        
        const left = depth(node.left);
        const right = depth(node.right);
        
        // Update global max diameter found so far
        maxDiam = Math.max(maxDiam, left + right);
        
        // Return height of current node
        return 1 + Math.max(left, right);
    }
    
    depth(root);
    return maxDiam;
}
```

#### 3. Balanced Binary Tree (LeetCode 110)

A height-balanced binary tree is defined as a binary tree in which the left and right subtrees of every node differ in height by no more than 1.

```javascript
function isBalanced(root) {
    // Returns -1 if unbalanced, otherwise returns height
    function checkHeight(node) {
        if (!node) return 0;
        
        const left = checkHeight(node.left);
        if (left === -1) return -1; // Propagate failure
        
        const right = checkHeight(node.right);
        if (right === -1) return -1; // Propagate failure
        
        if (Math.abs(left - right) > 1) {
            return -1; // Unbalanced at this node
        }
        
        return 1 + Math.max(left, right);
    }
    
    return checkHeight(root) !== -1;
}
```

#### 4. Lowest Common Ancestor (LCA) of a Binary Tree (LeetCode 236)

```javascript
function lca(root, p, q) {
    // Base cases: if root is null, or matches p or q
    if (!root || root === p || root === q) return root;
    
    const left = lca(root.left, p, q);
    const right = lca(root.right, p, q);
    
    // If both left and right return a node, root is the LCA
    if (left && right) return root;
    
    // Otherwise, propagate the found node upwards
    return left ? left : right;
}
```

#### 5. Binary Tree Right Side View (LeetCode 199)

Return the values of the nodes you can see ordered from top to bottom when looking from the right side.

```javascript
// Approach: BFS, take the last element of each level
function rightSideView(root) {
    if (!root) return [];
    const result = [];
    const queue = [root];
    let front = 0;
    
    while (front < queue.length) {
        const levelSize = queue.length - front;
        for (let i = 0; i < levelSize; i++) {
            const node = queue[front++];
            // If it's the last node in this level, add to result
            if (i === levelSize - 1) result.push(node.val);
            
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
    }
    return result;
}
```

#### 6. Serialize and Deserialize Binary Tree (LeetCode 297)

Convert tree to string, and string back to tree. We use Preorder traversal with marker `#` for nulls.

```javascript
/**
 * Encodes a tree to a single string.
 */
function serialize(root) {
    const data = [];
    function buildString(node) {
        if (!node) {
            data.push('#');
            return;
        }
        data.push(node.val);
        buildString(node.left);
        buildString(node.right);
    }
    buildString(root);
    return data.join(',');
}

/**
 * Decodes your encoded data to tree.
 */
function deserialize(data) {
    const nodes = data.split(',');
    let index = 0;
    
    function buildTree() {
        const val = nodes[index++];
        if (val === '#' || val === undefined) return null;
        
        const node = new TreeNode(parseInt(val, 10));
        node.left = buildTree();
        node.right = buildTree();
        return node;
    }
    
    return buildTree();
}
```

---

## 4. Binary Search Tree (BST) Operations

A BST has the property: `Left child < Root < Right child`.

#### Search in a BST (LeetCode 700)

```javascript
// Recursive
function searchBST(root, val) {
    if (!root) return null;
    if (root.val === val) return root;
    return val < root.val ? searchBST(root.left, val) : searchBST(root.right, val);
}

// Iterative (Often preferred for O(1) space)
function searchBSTIterative(root, val) {
    let curr = root;
    while (curr) {
        if (curr.val === val) return curr;
        if (val < curr.val) curr = curr.left;
        else curr = curr.right;
    }
    return null;
}
```

#### Insert into a BST (LeetCode 701)

```javascript
function insertBST(root, val) {
    if (!root) return new TreeNode(val);
    
    if (val < root.val) {
        root.left = insertBST(root.left, val);
    } else {
        root.right = insertBST(root.right, val);
    }
    
    return root;
}
```

#### Validate Binary Search Tree (LeetCode 98)

Determine if a valid BST. Must check against an acceptable range, not just immediate children.

```javascript
function isValidBST(root) {
    function validate(node, min, max) {
        if (!node) return true;
        
        if (node.val <= min || node.val >= max) {
            return false;
        }
        
        return validate(node.left, min, node.val) && 
               validate(node.right, node.val, max);
    }
    
    // JS Numbers range from -Infinity to Infinity
    return validate(root, -Infinity, Infinity);
}
```

#### Kth Smallest Element in a BST (LeetCode 230)

Since Inorder traversal of a BST gives sorted order, we traverse Inorder and stop at `k`.

```javascript
function kthSmallest(root, k) {
    let count = 0;
    let result = null;
    
    function inorder(node) {
        if (!node || result !== null) return;
        
        inorder(node.left);
        
        count++;
        if (count === k) {
            result = node.val;
            return;
        }
        
        inorder(node.right);
    }
    
    inorder(root);
    return result;
}
```

---

## 5. Heaps and Priority Queues in JavaScript

**CRITICAL:** JavaScript does **NOT** have a built-in Priority Queue or Heap data structure.
In Java, you just do `PriorityQueue<Integer> pq = new PriorityQueue<>();`.
In a JS interview, you have two options:
1. Ask the interviewer if you can assume a `MinHeap` or `PriorityQueue` class exists and stub its methods.
2. Quickly implement a Heap yourself. You **must** memorize how to build one.

### Implementing a MinHeap in JavaScript

A Heap is usually implemented as an array.
- For node at index `i`:
    - Left Child: `2 * i + 1`
    - Right Child: `2 * i + 2`
    - Parent: `Math.floor((i - 1) / 2)`

```javascript
class MinHeap {
    constructor() {
        this.heap = [];
    }
    
    size() {
        return this.heap.length;
    }
    
    peek() {
        return this.heap.length > 0 ? this.heap[0] : null;
    }
    
    push(val) {
        // Add to end and bubble up
        this.heap.push(val);
        this._bubbleUp(this.heap.length - 1);
    }
    
    pop() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();
        
        // Save the min (root), put the last element at root, and sink down
        const min = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._sinkDown(0);
        return min;
    }
    
    _bubbleUp(i) {
        while (i > 0) {
            const parent = Math.floor((i - 1) / 2);
            // If parent is smaller or equal, we are done
            if (this.heap[parent] <= this.heap[i]) break;
            
            // Swap
            [this.heap[parent], this.heap[i]] = [this.heap[i], this.heap[parent]];
            i = parent;
        }
    }
    
    _sinkDown(i) {
        const n = this.heap.length;
        while (true) {
            let smallest = i;
            const left = 2 * i + 1;
            const right = 2 * i + 2;
            
            if (left < n && this.heap[left] < this.heap[smallest]) {
                smallest = left;
            }
            if (right < n && this.heap[right] < this.heap[smallest]) {
                smallest = right;
            }
            
            if (smallest === i) break; // Heap property satisfied
            
            // Swap
            [this.heap[smallest], this.heap[i]] = [this.heap[i], this.heap[smallest]];
            i = smallest;
        }
    }
}
```

### Generic Custom Comparator Heap

In Java: `new PriorityQueue<>((a, b) -> b.val - a.val)`
In JavaScript, we can modify our Heap class to take a comparator function to handle objects or max heaps.

```javascript
/**
 * Generic Heap class.
 * MinHeap: new Heap((a,b) => a - b)
 * MaxHeap: new Heap((a,b) => b - a)
 */
class Heap {
    constructor(compareFn = (a, b) => a - b) {
        this.heap = [];
        // compareFn(a, b) returns < 0 if a has higher priority than b
        this.compare = compareFn;
    }
    
    size() { return this.heap.length; }
    peek() { return this.heap[0]; }
    
    push(val) {
        this.heap.push(val);
        this._bubbleUp(this.heap.length - 1);
    }
    
    pop() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();
        const top = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._sinkDown(0);
        return top;
    }
    
    _bubbleUp(i) {
        while (i > 0) {
            const parent = Math.floor((i - 1) / 2);
            // If compare(parent, child) <= 0, parent has priority, heap is valid
            if (this.compare(this.heap[parent], this.heap[i]) <= 0) break;
            
            [this.heap[parent], this.heap[i]] = [this.heap[i], this.heap[parent]];
            i = parent;
        }
    }
    
    _sinkDown(i) {
        const n = this.heap.length;
        while (true) {
            let priorityIdx = i;
            const left = 2 * i + 1;
            const right = 2 * i + 2;
            
            if (left < n && this.compare(this.heap[left], this.heap[priorityIdx]) < 0) {
                priorityIdx = left;
            }
            if (right < n && this.compare(this.heap[right], this.heap[priorityIdx]) < 0) {
                priorityIdx = right;
            }
            
            if (priorityIdx === i) break;
            
            [this.heap[priorityIdx], this.heap[i]] = [this.heap[i], this.heap[priorityIdx]];
            i = priorityIdx;
        }
    }
}
```

---

## 6. Applications of Heaps

Now that we have a Heap class, we can solve classic problems.

#### 1. Kth Largest Element in an Array (LeetCode 215)

Using a MinHeap of size K.
```javascript
function findKthLargest(nums, k) {
    const heap = new Heap((a, b) => a - b); // MinHeap
    
    for (const num of nums) {
        heap.push(num);
        // Maintain heap size k. The smallest elements are popped.
        if (heap.size() > k) {
            heap.pop();
        }
    }
    
    // The top of the heap is the kth largest element.
    return heap.peek();
}
```
*Time Complexity: O(N log K)*

#### 2. Merge K Sorted Lists (LeetCode 23)

```javascript
// Assume ListNode class exists
function mergeKLists(lists) {
    // Custom comparator to sort by node value
    const heap = new Heap((a, b) => a.val - b.val);
    
    // Initialize heap with the heads of all lists
    for (const list of lists) {
        if (list) heap.push(list);
    }
    
    const dummy = new ListNode(0);
    let curr = dummy;
    
    while (heap.size() > 0) {
        const node = heap.pop(); // Get smallest node
        curr.next = node;
        curr = curr.next;
        
        // If the node has a next element, push it into the heap
        if (node.next) {
            heap.push(node.next);
        }
    }
    
    return dummy.next;
}
```

#### 3. Top K Frequent Elements (LeetCode 347)

```javascript
function topKFrequent(nums, k) {
    // 1. Count frequencies using a Map
    const freqMap = new Map();
    for (const num of nums) {
        freqMap.set(num, (freqMap.get(num) || 0) + 1);
    }
    
    // 2. Use a MinHeap based on frequency
    // Storing array [num, freq]
    const heap = new Heap((a, b) => a[1] - b[1]); 
    
    for (const [num, freq] of freqMap.entries()) {
        heap.push([num, freq]);
        if (heap.size() > k) heap.pop(); // Pop least frequent
    }
    
    // 3. Extract results
    const result = [];
    while (heap.size() > 0) {
        result.push(heap.pop()[0]); // push the 'num' part
    }
    
    return result;
}
```

#### 4. Find Median from Data Stream (LeetCode 295)

We maintain two heaps: a MaxHeap for the smaller half of numbers, and a MinHeap for the larger half.

```javascript
class MedianFinder {
    constructor() {
        this.small = new Heap((a, b) => b - a); // MaxHeap
        this.large = new Heap((a, b) => a - b); // MinHeap
    }

    addNum(num) {
        this.small.push(num);
        
        // Make sure every element in small <= every element in large
        if (this.small.size() > 0 && this.large.size() > 0 && 
            this.small.peek() > this.large.peek()) {
            this.large.push(this.small.pop());
        }
        
        // Handle uneven sizes
        if (this.small.size() > this.large.size() + 1) {
            this.large.push(this.small.pop());
        } else if (this.large.size() > this.small.size() + 1) {
            this.small.push(this.large.pop());
        }
    }

    findMedian() {
        if (this.small.size() > this.large.size()) {
            return this.small.peek();
        } else if (this.large.size() > this.small.size()) {
            return this.large.peek();
        } else {
            return (this.small.peek() + this.large.peek()) / 2;
        }
    }
}
```

#### 5. Heap Sort Implementation

Heap sort in-place (O(1) auxiliary space). We build a Max Heap to sort in ascending order.

```javascript
function heapSort(arr) {
    const n = arr.length;
    
    // 1. Build max heap (rearrange array)
    // Start from the last non-leaf node
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
    
    // 2. One by one extract an element from heap
    for (let i = n - 1; i > 0; i--) {
        // Move current root to end
        [arr[0], arr[i]] = [arr[i], arr[0]];
        
        // call max heapify on the reduced heap
        heapify(arr, i, 0);
    }
    return arr;
}

// To heapify a subtree rooted with node i which is an index in arr[]
function heapify(arr, n, i) {
    let largest = i; // Initialize largest as root
    const l = 2 * i + 1; // left child
    const r = 2 * i + 2; // right child
    
    // If left child is larger than root
    if (l < n && arr[l] > arr[largest]) largest = l;
    
    // If right child is larger than largest so far
    if (r < n && arr[r] > arr[largest]) largest = r;
    
    // If largest is not root
    if (largest !== i) {
        // Swap
        [arr[i], arr[largest]] = [arr[largest], arr[i]];
        // Recursively heapify the affected sub-tree
        heapify(arr, n, largest);
    }
}
```

---

## 7. Practice Problems

Reinforce your tree and heap knowledge with these problems:

**Trees & BST:**
1.  **Symmetric Tree** (LeetCode 101) - Checking mirror conditions recursively.
2.  **Path Sum II** (LeetCode 113) - DFS Backtracking on a tree.
3.  **Construct Binary Tree from Preorder and Inorder Traversal** (LeetCode 105) - Array splitting and recursion.
4.  **Flatten Binary Tree to Linked List** (LeetCode 114) - Manipulating pointers in place.
5.  **Lowest Common Ancestor of a Binary Search Tree** (LeetCode 235) - Utilizing BST properties for O(h) time.
6.  **Convert Sorted Array to Binary Search Tree** (LeetCode 108) - Building balanced tree by taking mid points.
7.  **Invert Binary Tree** (LeetCode 226) - Simple but classic.
8.  **Count Complete Tree Nodes** (LeetCode 222) - Utilizing properties of complete trees to achieve better than O(N).
9.  **Binary Tree Maximum Path Sum** (LeetCode 124) - Hard. Similar to diameter, but tracking max sums.
10. **Binary Search Tree Iterator** (LeetCode 173) - Simulating iterative inorder traversal incrementally.

**Heaps:**
11. **Sort Characters By Frequency** (LeetCode 451) - Map to Heap or Bucket Sort.
12. **K Closest Points to Origin** (LeetCode 973) - MaxHeap of size K using distance formula as comparator.
13. **Task Scheduler** (LeetCode 621) - MaxHeap to track tasks with highest frequencies + Queue for cooldown.
14. **Design Twitter** (LeetCode 355) - Merge K sorted lists variant.
15. **Reorganize String** (LeetCode 767) - MaxHeap to greedily place characters.
