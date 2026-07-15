# Trees & Graphs — Q91 to Q100

> **Target companies:** TCS Digital/Prime, Infosys SP/HackWithInfy, Wipro Elite/Turbo, Cognizant GenC Next/Pro  
> **Difficulty:** Medium to Hard  
> **Coverage:** ~10% — reserved for premium tracks; will separate you from the crowd

---

## TreeNode Class (Reused Across All Tree Questions)

```java
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; left = right = null; }
}
```

---

## Q91. Inorder, Preorder, Postorder Traversal (Recursive)

**Problem:** Traverse a binary tree in all three orders.  
**Companies:** TCS, Infosys, Cognizant (all companies with trees!)  

```java
import java.util.*;

public class BinaryTreeTraversals {
    // Inorder: Left → Root → Right (gives sorted order for BST)
    public static List<Integer> inorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }
    static void inorderHelper(TreeNode node, List<Integer> list) {
        if (node == null) return;
        inorderHelper(node.left, list);
        list.add(node.val);
        inorderHelper(node.right, list);
    }

    // Preorder: Root → Left → Right
    public static List<Integer> preorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }
    static void preorderHelper(TreeNode node, List<Integer> list) {
        if (node == null) return;
        list.add(node.val);
        preorderHelper(node.left, list);
        preorderHelper(node.right, list);
    }

    // Postorder: Left → Right → Root
    public static List<Integer> postorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }
    static void postorderHelper(TreeNode node, List<Integer> list) {
        if (node == null) return;
        postorderHelper(node.left, list);
        postorderHelper(node.right, list);
        list.add(node.val);
    }

    public static void main(String[] args) {
        //        1
        //       / \
        //      2   3
        //     / \
        //    4   5
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2); root.right = new TreeNode(3);
        root.left.left = new TreeNode(4); root.left.right = new TreeNode(5);

        System.out.println("Inorder:   " + inorder(root));   // [4, 2, 5, 1, 3]
        System.out.println("Preorder:  " + preorder(root));  // [1, 2, 4, 5, 3]
        System.out.println("Postorder: " + postorder(root)); // [4, 5, 2, 3, 1]
    }
}
```
**Time:** O(n) | **Space:** O(h) — h = tree height

---

## Q92. Level Order Traversal (BFS on Tree)

**Problem:** Traverse the tree level by level (Breadth-First Search).  
**Companies:** TCS Digital, Infosys SP, Cognizant  
**Approach:** Use a Queue — process each node, enqueue its children.

```java
import java.util.*;

public class LevelOrderTraversal {
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size(); // Nodes at current level
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            result.add(level);
        }
        return result;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9); root.right = new TreeNode(20);
        root.right.left = new TreeNode(15); root.right.right = new TreeNode(7);
        System.out.println(levelOrder(root)); // [[3], [9, 20], [15, 7]]
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q93. Height / Maximum Depth of a Binary Tree

**Problem:** Find the height (maximum depth) of a binary tree.  
**Companies:** TCS, Cognizant, Infosys  

```java
public class TreeHeight {
    public static int maxDepth(TreeNode root) {
        if (root == null) return 0;
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        return 1 + Math.max(leftDepth, rightDepth);
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2); root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        System.out.println("Height: " + maxDepth(root)); // 3
    }
}
```
**Time:** O(n) | **Space:** O(h)

---

## Q94. Check if a Binary Tree is a BST

**Problem:** Verify that a binary tree satisfies BST properties (all left descendants < node < all right descendants).  
**Companies:** TCS Digital, Infosys SP, Cognizant GenC Next  
**Approach:** Pass valid range (min, max) to each node's subtree.

```java
public class ValidateBST {
    public static boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    static boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        if (node.val <= min || node.val >= max) return false;
        return validate(node.left, min, node.val) &&
               validate(node.right, node.val, max);
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(2);
        root.left = new TreeNode(1); root.right = new TreeNode(3);
        System.out.println(isValidBST(root)); // true
    }
}
```
**Time:** O(n) | **Space:** O(h)

---

## Q95. BST Insert and Search

**Problem:** Insert a value into a BST and search for a value.  
**Companies:** TCS, Cognizant, HCL  

```java
public class BSTInsertSearch {
    // Insert: smaller goes left, larger goes right
    public static TreeNode insert(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);
        if (val < root.val) root.left = insert(root.left, val);
        else if (val > root.val) root.right = insert(root.right, val);
        return root;
    }

    // Search: same comparison logic
    public static boolean search(TreeNode root, int target) {
        if (root == null) return false;
        if (root.val == target) return true;
        if (target < root.val) return search(root.left, target);
        return search(root.right, target);
    }

    public static void main(String[] args) {
        TreeNode root = null;
        root = insert(root, 5);
        root = insert(root, 3);
        root = insert(root, 7);
        root = insert(root, 1);
        System.out.println(search(root, 3)); // true
        System.out.println(search(root, 6)); // false
    }
}
```
**Time:** O(h) for both | **Space:** O(h)

---

## Q96. Lowest Common Ancestor (LCA) of a BST

**Problem:** Find the lowest common ancestor of two nodes in a BST.  
**Companies:** TCS Digital, Infosys SP  
**Approach:** Use BST property — LCA is the first node that splits the paths to p and q.

```java
public class LCAofBST {
    public static TreeNode lca(TreeNode root, int p, int q) {
        if (root == null) return null;
        // Both nodes are smaller — go left
        if (p < root.val && q < root.val) return lca(root.left, p, q);
        // Both nodes are larger — go right
        if (p > root.val && q > root.val) return lca(root.right, p, q);
        // Split point — this node is the LCA
        return root;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2); root.right = new TreeNode(8);
        root.left.left = new TreeNode(0); root.left.right = new TreeNode(4);
        System.out.println("LCA of 2 and 4: " + lca(root, 2, 4).val); // 2
        System.out.println("LCA of 2 and 8: " + lca(root, 2, 8).val); // 6
    }
}
```
**Time:** O(h) | **Space:** O(h)

---

## Q97. Graph Representation and BFS

**Problem:** Represent a graph as an adjacency list and perform Breadth-First Search.  
**Companies:** TCS Digital, Infosys SP, Wipro Elite  

```java
import java.util.*;

public class GraphBFS {
    int vertices;
    List<List<Integer>> adj;

    GraphBFS(int v) {
        vertices = v;
        adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
    }

    void addEdge(int u, int v) {
        adj.get(u).add(v);
        adj.get(v).add(u); // Undirected graph
    }

    void bfs(int start) {
        boolean[] visited = new boolean[vertices];
        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        queue.add(start);

        System.out.print("BFS: ");
        while (!queue.isEmpty()) {
            int node = queue.poll();
            System.out.print(node + " ");
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
    }

    public static void main(String[] args) {
        GraphBFS g = new GraphBFS(6);
        g.addEdge(0, 1); g.addEdge(0, 2);
        g.addEdge(1, 3); g.addEdge(2, 4);
        g.addEdge(3, 5);
        g.bfs(0); // BFS: 0 1 2 3 4 5
    }
}
```
**Time:** O(V+E) | **Space:** O(V)

---

## Q98. Graph DFS (Depth-First Search)

**Problem:** Perform Depth-First Search on a graph.  
**Companies:** TCS Digital, Infosys SP, Wipro Elite  

```java
import java.util.*;

public class GraphDFS {
    int vertices;
    List<List<Integer>> adj;

    GraphDFS(int v) {
        vertices = v;
        adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
    }

    void addEdge(int u, int v) { adj.get(u).add(v); adj.get(v).add(u); }

    void dfsHelper(int node, boolean[] visited) {
        visited[node] = true;
        System.out.print(node + " ");
        for (int neighbor : adj.get(node))
            if (!visited[neighbor]) dfsHelper(neighbor, visited);
    }

    void dfs(int start) {
        boolean[] visited = new boolean[vertices];
        System.out.print("DFS: ");
        dfsHelper(start, visited);
    }

    public static void main(String[] args) {
        GraphDFS g = new GraphDFS(6);
        g.addEdge(0, 1); g.addEdge(0, 2);
        g.addEdge(1, 3); g.addEdge(2, 4);
        g.addEdge(3, 5);
        g.dfs(0); // DFS: 0 1 3 5 2 4
    }
}
```
**Time:** O(V+E) | **Space:** O(V)

---

## Q99. Detect Cycle in a Directed Graph (DFS with Color Marking)

**Problem:** Check if a directed graph contains a cycle.  
**Companies:** Infosys SP/HackWithInfy, TCS Digital  
**Approach:** DFS with three states: WHITE (0=unvisited), GRAY (1=in progress), BLACK (2=done). Cycle = we reach a GRAY node.

```java
import java.util.*;

public class DetectCycleDirectedGraph {
    int vertices;
    List<List<Integer>> adj;
    int[] color; // 0=white, 1=gray, 2=black

    DetectCycleDirectedGraph(int v) {
        vertices = v;
        adj = new ArrayList<>();
        color = new int[v];
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
    }

    void addEdge(int u, int v) { adj.get(u).add(v); }

    boolean dfs(int node) {
        color[node] = 1; // Mark as in-progress (gray)
        for (int neighbor : adj.get(node)) {
            if (color[neighbor] == 1) return true; // Back edge = cycle!
            if (color[neighbor] == 0 && dfs(neighbor)) return true;
        }
        color[node] = 2; // Mark as done (black)
        return false;
    }

    boolean hasCycle() {
        for (int i = 0; i < vertices; i++)
            if (color[i] == 0 && dfs(i)) return true;
        return false;
    }

    public static void main(String[] args) {
        DetectCycleDirectedGraph g = new DetectCycleDirectedGraph(4);
        g.addEdge(0, 1); g.addEdge(1, 2); g.addEdge(2, 3); g.addEdge(3, 1);
        System.out.println("Has cycle: " + g.hasCycle()); // true

        DetectCycleDirectedGraph g2 = new DetectCycleDirectedGraph(4);
        g2.addEdge(0, 1); g2.addEdge(1, 2); g2.addEdge(2, 3);
        System.out.println("Has cycle: " + g2.hasCycle()); // false
    }
}
```
**Time:** O(V+E) | **Space:** O(V)

---

## Q100. Dijkstra's Shortest Path Algorithm

**Problem:** Find the shortest path from a source vertex to all other vertices in a weighted directed graph (no negative weights).  
**Companies:** TCS Prime, Infosys HackWithInfy, Wipro Turbo  
**Approach:** Greedy with a Min-Heap (Priority Queue). Always expand the node with the smallest current distance.

```java
import java.util.*;

public class DijkstraShortestPath {
    static final int INF = Integer.MAX_VALUE;

    public static int[] dijkstra(int[][] graph, int src) {
        int n = graph.length;
        int[] dist = new int[n];
        Arrays.fill(dist, INF);
        dist[src] = 0;

        // Min-Heap: (distance, node)
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        pq.offer(new int[]{0, src});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int d = curr[0], u = curr[1];

            if (d > dist[u]) continue; // Outdated entry

            for (int v = 0; v < n; v++) {
                if (graph[u][v] != 0) { // Edge exists
                    int newDist = dist[u] + graph[u][v];
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        pq.offer(new int[]{dist[v], v});
                    }
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        // Graph as adjacency matrix (0 = no edge)
        int[][] graph = {
            {0, 4, 0, 0, 0, 0, 0, 8, 0},
            {4, 0, 8, 0, 0, 0, 0, 11,0},
            {0, 8, 0, 7, 0, 4, 0, 0, 2},
            {0, 0, 7, 0, 9, 14,0, 0, 0},
            {0, 0, 0, 9, 0, 10,0, 0, 0},
            {0, 0, 4, 14,10,0, 2, 0, 0},
            {0, 0, 0, 0, 0, 2, 0, 1, 6},
            {8, 11,0, 0, 0, 0, 1, 0, 7},
            {0, 0, 2, 0, 0, 0, 6, 7, 0}
        };
        int[] distances = dijkstra(graph, 0);
        System.out.println("Shortest distances from vertex 0:");
        for (int i = 0; i < distances.length; i++)
            System.out.println("  to " + i + ": " + distances[i]);
        // 0:0, 1:4, 2:12, 3:19, 4:21, 5:11, 6:9, 7:8, 8:14
    }
}
```
**Time:** O((V + E) log V) | **Space:** O(V)

---

## 🎯 Final Revision Cheat Sheet

| # | Question | Key Concept | Time |
|---|---|---|---|
| 1-3 | Reverse, Move Zeros, Second Largest | Two Pointer | O(n) |
| 4,29 | Duplicates, Unique Elements | HashSet | O(n) |
| 6 | Max Subarray Sum | Kadane's | O(n) |
| 9 | Two Sum | HashMap | O(n) |
| 13 | Palindrome String | Two Pointer | O(n) |
| 17 | Anagram Check | Frequency Array | O(n) |
| 18 | Longest Palindromic Substring | Expand Around Center | O(n²) |
| 19 | Run-Length Encoding | String Traversal | O(n) |
| 34 | Longest Substring No Repeat | Sliding Window | O(n) |
| 41-43 | Number Base Conversion | Divide & Remainder | O(log n) |
| 44 | Prime Check | √n Divisors | O(√n) |
| 45 | All Primes in Range | Sieve | O(n log log n) |
| 49,50 | GCD / LCM | Euclidean | O(log n) |
| 61 | Binary Search | Halving | O(log n) |
| 59,60 | Merge/Quick Sort | Divide & Conquer | O(n log n) |
| 66 | Reverse Linked List | Three Pointers | O(n) |
| 67 | Cycle Detection | Floyd's | O(n) |
| 73 | Balanced Brackets | Stack | O(n) |
| 77 | Next Greater Element | Monotonic Stack | O(n) |
| 81 | Fibonacci | Memoization/DP | O(n) |
| 83 | Knapsack | 2D DP | O(n*W) |
| 84 | LCS | 2D DP | O(m*n) |
| 88 | Activity Selection | Greedy | O(n log n) |
| 91 | Tree Traversals | DFS | O(n) |
| 92 | Level Order | BFS | O(n) |
| 97,98 | Graph BFS/DFS | Queue/Recursion | O(V+E) |
| 100 | Dijkstra | Greedy + MinHeap | O((V+E)log V) |

---

*You have now covered all 100 essential questions for Indian mass-recruiter company interviews. Good luck!* 🚀
