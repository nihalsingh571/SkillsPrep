# Graphs and Graph Algorithms in JavaScript

Welcome to the comprehensive guide on Graphs and Graph algorithms in JavaScript! If you're coming from a Java background, you'll find that JavaScript offers a lot of flexibility when it comes to representing and manipulating graphs.

In Java, you might be used to explicitly declaring `List<List<Integer>>` or defining custom `Node` classes. In JavaScript, we often rely on arrays, the `Map` object, and the `Set` object to achieve similar, if not more concise, results.

This guide will walk you through the various ways to represent graphs, fundamental traversal algorithms, and advanced algorithms for shortest paths, minimum spanning trees, and more. Let's dive in!

---

## 1. Graph Representation in JavaScript

Before we can traverse or analyze a graph, we need a way to store it in memory. There are three main ways to represent a graph:

1.  **Adjacency List**
2.  **Adjacency Matrix**
3.  **Edge List**

### Adjacency List (The most common for DSA)

An adjacency list is often the preferred choice because it is memory efficient for sparse graphs (graphs where the number of edges is much less than the square of the number of vertices).

#### Using `Map` of Arrays

This approach is highly flexible and works exceptionally well when vertex IDs are not sequential integers (e.g., strings or objects).

```javascript
// Initialization
const graph = new Map();
const n = 5; // number of vertices

// Initialize empty arrays for all vertices
for (let i = 0; i < n; i++) {
    graph.set(i, []);
}

// Adding an undirected edge between u and v
const u = 0, v = 1;
graph.get(u).push(v);
graph.get(v).push(u); // Omit this line for a directed graph

console.log(graph);
```

#### Using Array of Arrays

If your vertices are sequential integers from `0` to `n-1`, an array of arrays is faster and simpler to write. This closely mirrors the `ArrayList<ArrayList<Integer>>` approach in Java.

```javascript
const n = 5;

// Create an array of n empty arrays
// The Array.from() method is very handy here.
const graph = Array.from({ length: n }, () => []);

// Add an edge
const u = 0, v = 1;
graph[u].push(v);
graph[v].push(u); // undirected
```

**Java Comparison:**
```java
// Java Equivalent
int n = 5;
List<List<Integer>> graph = new ArrayList<>();
for(int i = 0; i < n; i++) {
    graph.add(new ArrayList<>());
}
graph.get(0).add(1);
graph.get(1).add(0);
```

#### Weighted Adjacency List

For algorithms like Dijkstra's or Prim's, edges have weights. In JavaScript, we can simply push an array `[neighbor, weight]` or an object `{node: neighbor, weight: w}`.

```javascript
const graph = Array.from({ length: n }, () => []);
const u = 0, v = 1, weight = 10;

// Storing as an array pair
graph[u].push([v, weight]);

// Or storing as an object
graph[u].push({ node: v, cost: weight });
```

### Adjacency Matrix

An adjacency matrix is a 2D array of size `V x V`. It is useful for dense graphs and when you need to quickly check if an edge exists between two specific vertices. However, it takes `O(V^2)` space.

```javascript
const n = 5;

// Initialize an n x n matrix with 0s
const matrix = Array.from({ length: n }, () => new Array(n).fill(0));

// Add an edge (weight = 1 for unweighted, or actual weight)
const u = 0, v = 1;
matrix[u][v] = 1;
matrix[v][u] = 1; // undirected
```

### Edge List

An edge list is simply a list of all edges in the graph. It is heavily used in algorithms like Kruskal's for Minimum Spanning Tree or Bellman-Ford.

```javascript
// Array of [u, v, weight]
const edges = [
    [0, 1, 10],
    [1, 2, 5],
    [2, 0, 15]
];
```

---

## 2. Breadth-First Search (BFS)

BFS explores the graph level by level. It uses a Queue. Since JavaScript's native `Array.shift()` operation is `O(N)`, using a simple pointer (`front`) for our queue array is a common optimization in competitive programming and interviews to simulate `O(1)` dequeue.

### Implementation

```javascript
/**
 * BFS Traversal
 * Time Complexity: O(V + E)
 * Space Complexity: O(V) for the queue and visited array
 */
function bfs(graph, start, n) {
    const visited = new Array(n).fill(false);
    const queue = [start];
    let front = 0; // Optimization: index instead of shift()
    
    visited[start] = true;
    const result = [];
    
    while (front < queue.length) {
        const node = queue[front++]; // Dequeue
        result.push(node);
        
        for (const neighbor of graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.push(neighbor); // Enqueue
            }
        }
    }
    
    return result;
}

// Example usage:
const n = 5;
const graph = Array.from({length: n}, () => []);
// Edges: 0-1, 0-2, 1-3, 2-4
graph[0].push(1, 2);
graph[1].push(0, 3);
graph[2].push(0, 4);
graph[3].push(1);
graph[4].push(2);

console.log("BFS:", bfs(graph, 0, n));
```

---

## 3. Depth-First Search (DFS)

DFS explores as far as possible along each branch before backtracking. It can be implemented recursively (using the call stack) or iteratively (using an explicit stack).

### Recursive DFS

The recursive approach is elegant and widely used.

```javascript
/**
 * Recursive DFS
 * Time Complexity: O(V + E)
 * Space Complexity: O(V) due to recursion stack
 */
function dfsRecursive(graph, start, n) {
    const visited = new Array(n).fill(false);
    const result = [];
    
    function dfs(node) {
        visited[node] = true;
        result.push(node);
        
        for (const neighbor of graph[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
    }
    
    dfs(start);
    return result;
}
```

### Iterative DFS

The iterative approach uses an explicit stack array. Note that to match the exact traversal order of recursive DFS, you would need to push neighbors onto the stack in reverse order. However, generally, any valid DFS order is acceptable.

```javascript
/**
 * Iterative DFS
 * Time Complexity: O(V + E)
 * Space Complexity: O(V)
 */
function dfsIterative(graph, start, n) {
    const visited = new Array(n).fill(false);
    const stack = [start];
    const result = [];
    
    while (stack.length > 0) {
        const node = stack.pop();
        
        if (visited[node]) continue;
        
        visited[node] = true;
        result.push(node);
        
        // Push to stack. (Pushing in reverse order mimics recursive DFS)
        for (let i = graph[node].length - 1; i >= 0; i--) {
            const neighbor = graph[node][i];
            if (!visited[neighbor]) {
                stack.push(neighbor);
            }
        }
    }
    
    return result;
}
```

---

## 4. Connected Components

Finding connected components involves iterating through all vertices and initiating a traversal (BFS or DFS) from every unvisited vertex.

### Counting Components

```javascript
/**
 * Counts the number of connected components in an undirected graph.
 */
function countComponents(n, edges) {
    // 1. Build the graph
    const graph = Array.from({length: n}, () => []);
    for (const [u, v] of edges) { 
        graph[u].push(v); 
        graph[v].push(u); 
    }
    
    // 2. Traversal setup
    const visited = new Array(n).fill(false);
    let count = 0;
    
    function dfs(node) {
        visited[node] = true;
        for (const neighbor of graph[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
    }
    
    // 3. Count
    for (let i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i);
            count++;
        }
    }
    
    return count;
}
```

### Number of Islands (Grid DFS)

A classic problem where the graph is implicitly represented as a 2D grid. We can perform DFS directly on the grid, mutating it to mark cells as visited.

```javascript
/**
 * LeetCode 200: Number of Islands
 * Time Complexity: O(M * N)
 * Space Complexity: O(M * N) for worst-case recursion stack
 */
function numIslands(grid) {
    if (!grid || grid.length === 0) return 0;
    
    const rows = grid.length;
    const cols = grid[0].length;
    let islands = 0;
    
    function dfs(r, c) {
        // Bounds check and visited/water check
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] === '0') {
            return;
        }
        
        // Mark as visited by sinking the island
        grid[r][c] = '0';
        
        // Explore all 4 directions
        dfs(r + 1, c); // Down
        dfs(r - 1, c); // Up
        dfs(r, c + 1); // Right
        dfs(r, c - 1); // Left
    }
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (grid[r][c] === '1') {
                dfs(r, c);
                islands++;
            }
        }
    }
    
    return islands;
}
```

---

## 5. Cycle Detection

Cycle detection logic differs based on whether the graph is directed or undirected.

### Undirected Graph (DFS with Parent)

In an undirected graph, an edge goes both ways. We must keep track of the `parent` node we came from to avoid falsely identifying the trivial back-edge as a cycle.

```javascript
function hasCycleUndirected(n, edges) {
    // Build graph
    const graph = Array.from({length: n}, () => []);
    for (const [u, v] of edges) {
        graph[u].push(v);
        graph[v].push(u);
    }
    
    const visited = new Array(n).fill(false);
    
    function dfs(node, parent) {
        visited[node] = true;
        
        for (const neighbor of graph[node]) {
            if (!visited[neighbor]) {
                if (dfs(neighbor, node)) return true;
            } else if (neighbor !== parent) {
                // We reached an already visited node that is NOT our parent
                return true;
            }
        }
        return false;
    }
    
    // Graph might be disconnected
    for (let i = 0; i < n; i++) {
        if (!visited[i]) {
            if (dfs(i, -1)) return true;
        }
    }
    
    return false;
}
```

### Directed Graph (DFS with Recursion Stack)

In a directed graph, we track the current path (recursion stack). A cycle exists if we encounter a node that is currently in our recursion stack. We use a 3-state visited array:
- `0` = Unvisited
- `1` = Visiting (in current path/stack)
- `2` = Visited (fully processed)

```javascript
function hasCycleDirected(n, edges) {
    const graph = Array.from({length: n}, () => []);
    for (const [u, v] of edges) {
        graph[u].push(v); // Directed edge
    }
    
    const state = new Array(n).fill(0);
    
    function dfs(node) {
        state[node] = 1; // Mark as currently visiting
        
        for (const neighbor of graph[node]) {
            if (state[neighbor] === 1) {
                // Found a back-edge to a node currently in the stack
                return true;
            }
            if (state[neighbor] === 0) {
                if (dfs(neighbor)) return true;
            }
        }
        
        state[node] = 2; // Mark as fully processed
        return false;
    }
    
    for (let i = 0; i < n; i++) {
        if (state[i] === 0) {
            if (dfs(i)) return true;
        }
    }
    
    return false;
}
```

---

## 6. Bipartite Graph Check

A Bipartite Graph is a graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex in one set to a vertex in the other. We can solve this using Graph Coloring (2 colors) via BFS or DFS.

```javascript
/**
 * Checks if a graph is bipartite using BFS coloring.
 * LeetCode 785: Is Graph Bipartite?
 */
function isBipartite(graph) {
    const n = graph.length;
    const color = new Array(n).fill(-1); // -1: uncolored, 0: color A, 1: color B
    
    for (let i = 0; i < n; i++) {
        // If already colored, skip
        if (color[i] !== -1) continue;
        
        // Start BFS
        const queue = [i];
        let front = 0;
        color[i] = 0;
        
        while (front < queue.length) {
            const node = queue[front++];
            
            for (const neighbor of graph[node]) {
                if (color[neighbor] === -1) {
                    // Color with opposite color
                    color[neighbor] = 1 - color[node];
                    queue.push(neighbor);
                } else if (color[neighbor] === color[node]) {
                    // Conflict found
                    return false;
                }
            }
        }
    }
    
    return true;
}
```

---

## 7. Topological Sort

Topological sort is applicable only for Directed Acyclic Graphs (DAGs). It linearly orders vertices such that for every directed edge `u -> v`, vertex `u` comes before `v`.

### Kahn's Algorithm (BFS based)

This algorithm uses the concept of "in-degree" (number of incoming edges).

```javascript
/**
 * Kahn's Algorithm for Topological Sort
 * Time Complexity: O(V + E)
 * Returns the sorted array, or empty array if a cycle exists.
 */
function topoSortKahn(n, graph) {
    const inDegree = new Array(n).fill(0);
    
    // 1. Calculate in-degrees
    for (let u = 0; u < n; u++) {
        for (const v of graph[u]) {
            inDegree[v]++;
        }
    }
    
    // 2. Initialize queue with vertices having 0 in-degree
    const queue = [];
    let front = 0;
    for (let i = 0; i < n; i++) {
        if (inDegree[i] === 0) queue.push(i);
    }
    
    // 3. Process
    const result = [];
    while (front < queue.length) {
        const node = queue[front++];
        result.push(node);
        
        // Decrease in-degree of neighbors
        for (const neighbor of graph[node]) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] === 0) {
                queue.push(neighbor);
            }
        }
    }
    
    // If result length !== n, there was a cycle
    return result.length === n ? result : [];
}
```

### DFS-based Topological Sort

```javascript
/**
 * DFS Topological Sort
 * Reverses post-order traversal.
 */
function topoSortDFS(n, graph) {
    const visited = new Array(n).fill(false);
    const result = [];
    let hasCycle = false;
    
    // We also need cycle detection to ensure it's a DAG
    const visiting = new Array(n).fill(false);
    
    function dfs(node) {
        if (hasCycle) return;
        visiting[node] = true;
        visited[node] = true;
        
        for (const neighbor of graph[node]) {
            if (visiting[neighbor]) {
                hasCycle = true;
                return;
            }
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
        
        visiting[node] = false;
        result.push(node); // Post-order push
    }
    
    for (let i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i);
        }
    }
    
    if (hasCycle) return [];
    
    // The top-sort is the reverse of post-order
    return result.reverse();
}
```

---

## 8. Shortest Paths Algorithms

Depending on graph characteristics, different algorithms apply.

### BFS Shortest Path (Unweighted Graph)

If all edge weights are equal (or unweighted), BFS finds the shortest path optimally.

```javascript
function shortestPathUnweighted(graph, start, end) {
    const n = graph.length;
    const dist = new Array(n).fill(Infinity);
    dist[start] = 0;
    
    const queue = [start];
    let front = 0;
    
    while (front < queue.length) {
        const node = queue[front++];
        
        if (node === end) return dist[end];
        
        for (const neighbor of graph[node]) {
            if (dist[neighbor] === Infinity) {
                dist[neighbor] = dist[node] + 1;
                queue.push(neighbor);
            }
        }
    }
    
    return dist[end]; // Returns Infinity if unreachable
}
```

### Dijkstra's Algorithm (Non-negative Weights)

Dijkstra's finds the shortest path from a single source to all other nodes. It requires a Priority Queue (Min Heap). JavaScript doesn't have a built-in MinHeap, so we often have to implement a simple one, or in interviews, you can sometimes get away with an array and sorting, though it degrades time complexity.

Below is Dijkstra's using a conceptual `MinHeap` implementation.

```javascript
// Minimal MinHeap Implementation for Dijkstra
class MinHeap {
    constructor() { this.heap = []; }
    size() { return this.heap.length; }
    push(val) { 
        this.heap.push(val); 
        this._bubbleUp(this.heap.length - 1); 
    }
    pop() {
        if (this.heap.length === 1) return this.heap.pop();
        const top = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._sinkDown(0);
        return top;
    }
    _bubbleUp(idx) {
        while (idx > 0) {
            let pIdx = Math.floor((idx - 1) / 2);
            if (this.heap[pIdx][0] <= this.heap[idx][0]) break;
            [this.heap[pIdx], this.heap[idx]] = [this.heap[idx], this.heap[pIdx]];
            idx = pIdx;
        }
    }
    _sinkDown(idx) {
        const length = this.heap.length;
        while (true) {
            let left = 2 * idx + 1, right = 2 * idx + 2, swap = null;
            if (left < length && this.heap[left][0] < this.heap[idx][0]) swap = left;
            if (right < length && this.heap[right][0] < (swap === null ? this.heap[idx][0] : this.heap[left][0])) swap = right;
            if (swap === null) break;
            [this.heap[idx], this.heap[swap]] = [this.heap[swap], this.heap[idx]];
            idx = swap;
        }
    }
}

function dijkstra(graph, start) {
    const n = graph.length;
    const dist = new Array(n).fill(Infinity);
    dist[start] = 0;
    
    const heap = new MinHeap(); // Holds [distance, node]
    heap.push([0, start]);
    
    while (heap.size() > 0) {
        const [d, u] = heap.pop();
        
        // If we pop a stale entry, skip it
        if (d > dist[u]) continue;
        
        for (const [v, weight] of graph[u]) {
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                heap.push([dist[v], v]);
            }
        }
    }
    
    return dist;
}
```

### Bellman-Ford (Handles Negative Weights)

Used when graphs contain negative edge weights. Can also detect negative weight cycles.
Time Complexity: `O(V * E)`

```javascript
function bellmanFord(n, edges, start) {
    const dist = new Array(n).fill(Infinity);
    dist[start] = 0;
    
    // Relax edges V - 1 times
    for (let i = 0; i < n - 1; i++) {
        let updated = false;
        for (const [u, v, w] of edges) {
            if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        // Optimization: if no relaxation occurred, we can stop early
        if (!updated) break;
    }
    
    // Check for negative weight cycle
    for (const [u, v, w] of edges) {
        if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
            console.log("Negative weight cycle detected!");
            return null;
        }
    }
    
    return dist;
}
```

### Floyd-Warshall (All-Pairs Shortest Path)

Time Complexity: `O(V^3)`
Space Complexity: `O(V^2)`

```javascript
function floydWarshall(n, edges) {
    // 1. Initialize distance matrix
    const dist = Array.from({length: n}, () => new Array(n).fill(Infinity));
    for (let i = 0; i < n; i++) dist[i][i] = 0;
    for (const [u, v, w] of edges) dist[u][v] = w; // Add graph edges
    
    // 2. The core algorithm
    for (let k = 0; k < n; k++) {
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (dist[i][k] !== Infinity && dist[k][j] !== Infinity) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }
    }
    
    // 3. Negative cycle check
    for (let i = 0; i < n; i++) {
        if (dist[i][i] < 0) return null; // Negative cycle
    }
    
    return dist;
}
```

---

## 9. Disjoint Set Union (DSU)

Also known as Union-Find, DSU is vital for grouping elements and cycle detection in undirected graphs (used in Kruskal's). 
Java has no built-in DSU; JavaScript doesn't either. The implementation is identical in structure.

```javascript
class DSU {
    constructor(n) {
        this.parent = Array.from({length: n}, (_, i) => i);
        this.rank = new Array(n).fill(0);
        this.size = new Array(n).fill(1); // Optional: tracks size of components
    }
    
    // Find with path compression
    find(x) {
        if (this.parent[x] === x) return x;
        return this.parent[x] = this.find(this.parent[x]);
    }
    
    // Union by rank
    union(x, y) {
        const px = this.find(x);
        const py = this.find(y);
        
        if (px === py) return false; // Already in same component
        
        if (this.rank[px] < this.rank[py]) {
            this.parent[px] = py;
            this.size[py] += this.size[px];
        } else if (this.rank[px] > this.rank[py]) {
            this.parent[py] = px;
            this.size[px] += this.size[py];
        } else {
            this.parent[py] = px;
            this.rank[px]++;
            this.size[px] += this.size[py];
        }
        return true;
    }
    
    connected(x, y) {
        return this.find(x) === this.find(y);
    }
    
    getSize(x) {
        return this.size[this.find(x)];
    }
}
```

---

## 10. Minimum Spanning Tree (MST)

### Kruskal's Algorithm

Kruskal's uses DSU and greedily picks the edges with the minimum weight, avoiding cycles.

```javascript
function kruskal(n, edges) {
    // 1. Sort edges by weight
    edges.sort((a, b) => a[2] - b[2]);
    
    const dsu = new DSU(n);
    let cost = 0;
    let edgeCount = 0;
    
    // 2. Iterate and build MST
    for (const [u, v, w] of edges) {
        if (dsu.union(u, v)) {
            cost += w;
            edgeCount++;
            if (edgeCount === n - 1) break; // MST complete
        }
    }
    
    // Check if graph is disconnected
    return edgeCount === n - 1 ? cost : -1;
}
```

### Prim's Algorithm

Prim's builds the tree from a starting vertex, growing it greedily. (Requires a MinHeap for optimal `O(E log V)` time).

```javascript
function prim(n, graph) {
    const heap = new MinHeap(); // Holds [weight, node]
    const visited = new Array(n).fill(false);
    
    heap.push([0, 0]); // Start at node 0
    let cost = 0;
    let edgesUsed = 0;
    
    while(heap.size() > 0 && edgesUsed < n) {
        const [w, u] = heap.pop();
        
        if (visited[u]) continue;
        
        visited[u] = true;
        cost += w;
        edgesUsed++;
        
        for (const [v, edgeWeight] of graph[u]) {
            if (!visited[v]) {
                heap.push([edgeWeight, v]);
            }
        }
    }
    
    return edgesUsed === n ? cost : -1;
}
```

---

## 11. Practice Problems Reference

1.  **Number of Islands** (LeetCode 200) - BFS/DFS on Grid
2.  **Max Area of Island** (LeetCode 695) - DFS size counting
3.  **Clone Graph** (LeetCode 133) - Graph Traversal & Hash Map
4.  **Word Ladder** (LeetCode 127) - Shortest Path BFS
5.  **Course Schedule** (LeetCode 207) - Cycle Detection / Topo Sort
6.  **Course Schedule II** (LeetCode 210) - Topological Sort Array
7.  **Network Delay Time** (LeetCode 743) - Dijkstra
8.  **Cheapest Flights Within K Stops** (LeetCode 787) - Bellman-Ford / BFS
9.  **Redundant Connection** (LeetCode 684) - DSU
10. **Number of Provinces** (LeetCode 547) - DSU / Connected Components
11. **Is Graph Bipartite?** (LeetCode 785) - BFS/DFS Graph Coloring
12. **Evaluate Division** (LeetCode 399) - Graph DFS
13. **Min Cost to Connect All Points** (LeetCode 1584) - Kruskal / Prim
14. **Find Eventual Safe States** (LeetCode 802) - Directed Graph Cycle Detection
15. **Critical Connections in a Network** (LeetCode 1192) - Tarjan's Bridge Finding

This covers a solid foundation for mastering Graph algorithms in JavaScript, drawing strong parallels to what you know in Java, while leveraging JS-specific syntax and idioms.
