# Section 14: Coding Interview Preparation - DSA Patterns

Welcome to the ultimate DSA Patterns guide. Mastering Data Structures and Algorithms (DSA) is about recognizing *patterns* rather than memorizing solutions. This section covers 16 critical patterns, complete with templates, recognition triggers, complexities, and real-world analogies.

---

## 1. Arrays

### Concept Explanation + Why it exists
Arrays are contiguous blocks of memory. They allow O(1) random access but O(n) insertion/deletion. Array problems often involve subarrays, prefix sums, or in-place transformations.

### When to Recognize
- Problem asks for contiguous subarrays.
- Need to compute cumulative sums.
- "In-place" modification required.
- O(n) time and O(1) space constraints.

### Java Template Code (Prefix Sum & Kadane's)
```java
// Prefix Sum Template
int[] prefix = new int[n + 1];
for (int i = 0; i < n; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}

// Kadane's Algorithm Template
int maxSoFar = nums[0], currentMax = nums[0];
for (int i = 1; i < nums.length; i++) {
    currentMax = Math.max(nums[i], currentMax + nums[i]);
    maxSoFar = Math.max(maxSoFar, currentMax);
}
```

### Time & Space Complexity
- **Time:** O(N) for single pass algorithms.
- **Space:** O(1) for Kadane's, O(N) for Prefix Sum array.

### Common Problems & Java Solutions

**1. Maximum Subarray (Kadane's)**
```java
public int maxSubArray(int[] nums) {
    int max = nums[0], sum = nums[0];
    for(int i = 1; i < nums.length; i++) {
        sum = Math.max(nums[i], sum + nums[i]);
        max = Math.max(max, sum);
    }
    return max;
}
```

**2. Rotate Array**
```java
public void rotate(int[] nums, int k) {
    k %= nums.length;
    reverse(nums, 0, nums.length - 1);
    reverse(nums, 0, k - 1);
    reverse(nums, k, nums.length - 1);
}
private void reverse(int[] nums, int start, int end) {
    while(start < end) { int temp = nums[start]; nums[start++] = nums[end]; nums[end--] = temp; }
}
```

**3. Merge Intervals**
```java
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> res = new ArrayList<>();
    int[] current = intervals[0];
    res.add(current);
    for(int[] interval : intervals) {
        if(current[1] >= interval[0]) current[1] = Math.max(current[1], interval[1]);
        else { current = interval; res.add(current); }
    }
    return res.toArray(new int[res.size()][]);
}
```

**4. Find the Duplicate Number**
```java
public int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[nums[0]];
    while (slow != fast) { slow = nums[slow]; fast = nums[nums[fast]]; }
    slow = 0;
    while (slow != fast) { slow = nums[slow]; fast = nums[fast]; }
    return slow;
}
```

**5. Product of Array Except Self**
```java
public int[] productExceptSelf(int[] nums) {
    int[] res = new int[nums.length];
    int left = 1; for(int i=0; i<nums.length; i++) { res[i] = left; left *= nums[i]; }
    int right = 1; for(int i=nums.length-1; i>=0; i--) { res[i] *= right; right *= nums[i]; }
    return res;
}
```

### Key Tips & Tricks
- Always clarify if the array is sorted.
- Beware of integer overflow (use `long` when summing).
- For O(1) space optimizations, consider using the input array to store state (e.g., making numbers negative).

---

## 2. Strings

### Concept Explanation
Strings in Java are immutable. Frequent modifications require `StringBuilder`. String problems often involve substring searches, palindromes, or frequency counting using arrays/maps.

### When to Recognize
- "Anagram", "Palindrome", "Substring" keywords.
- Character frequencies.
- Lexicographical order.

### Java Template Code (Frequency Map)
```java
int[] freq = new int[26]; // For lowercase English letters
for (char c : s.toCharArray()) {
    freq[c - 'a']++;
}
```

### Time & Space Complexity
- **Time:** O(N) to traverse.
- **Space:** O(1) if using fixed size array (e.g., `int[26]` or `int[256]`), O(N) if generating `StringBuilder`.

### Common Problems & Java Solutions

**1. Valid Anagram**
```java
public boolean isAnagram(String s, String t) {
    if(s.length() != t.length()) return false;
    int[] counts = new int[26];
    for(int i = 0; i < s.length(); i++) { counts[s.charAt(i) - 'a']++; counts[t.charAt(i) - 'a']--; }
    for(int c : counts) if(c != 0) return false;
    return true;
}
```

**2. Valid Palindrome**
```java
public boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while(l < r) {
        while(l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
        while(l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
        if(Character.toLowerCase(s.charAt(l++)) != Character.toLowerCase(s.charAt(r--))) return false;
    }
    return true;
}
```

**3. Longest Substring Without Repeating Characters**
```java
public int lengthOfLongestSubstring(String s) {
    int[] map = new int[128];
    int left = 0, max = 0;
    for(int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        left = Math.max(left, map[c]);
        max = Math.max(max, right - left + 1);
        map[c] = right + 1;
    }
    return max;
}
```

**4. Group Anagrams**
```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for(String s : strs) {
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        String key = new String(arr);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}
```

**5. Longest Palindromic Substring**
```java
public String longestPalindrome(String s) {
    if(s == null || s.length() < 1) return "";
    int start = 0, end = 0;
    for(int i = 0; i < s.length(); i++) {
        int len1 = expand(s, i, i), len2 = expand(s, i, i+1);
        int len = Math.max(len1, len2);
        if(len > end - start) { start = i - (len - 1) / 2; end = i + len / 2; }
    }
    return s.substring(start, end + 1);
}
private int expand(String s, int L, int R) {
    while(L >= 0 && R < s.length() && s.charAt(L) == s.charAt(R)) { L--; R++; }
    return R - L - 1;
}
```

### Key Tips & Tricks
- Never use `==` for String comparison in Java; use `.equals()`.
- Use `s.toCharArray()` for faster iteration than `s.charAt(i)` inside tight loops.

---

## 3. Hashing

### Concept Explanation
Hashing uses functions to map keys to values, giving O(1) average time complexity for lookups, insertions, and deletions.

### When to Recognize
- Need to lookup elements instantly.
- Counting frequencies of non-character items.
- Finding pairs or subsets that satisfy a condition (e.g., sum).

### Java Template Code
```java
Map<Integer, Integer> map = new HashMap<>();
for (int n : nums) {
    map.put(n, map.getOrDefault(n, 0) + 1);
}
```

### Time & Space Complexity
- **Time:** O(1) average for add/remove/contains.
- **Space:** O(N) to store N elements.

### Common Problems & Java Solutions

**1. Two Sum**
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for(int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if(map.containsKey(complement)) return new int[] {map.get(complement), i};
        map.put(nums[i], i);
    }
    return new int[0];
}
```

**2. Subarray Sum Equals K**
```java
public int subarraySum(int[] nums, int k) {
    int count = 0, sum = 0;
    Map<Integer, Integer> map = new HashMap<>();
    map.put(0, 1);
    for(int n : nums) {
        sum += n;
        if(map.containsKey(sum - k)) count += map.get(sum - k);
        map.put(sum, map.getOrDefault(sum, 0) + 1);
    }
    return count;
}
```

**3. Valid Sudoku**
```java
public boolean isValidSudoku(char[][] board) {
    Set<String> seen = new HashSet<>();
    for (int i=0; i<9; ++i) {
        for (int j=0; j<9; ++j) {
            char number = board[i][j];
            if (number != '.')
                if (!seen.add(number + " in row " + i) ||
                    !seen.add(number + " in col " + j) ||
                    !seen.add(number + " in block " + i/3 + "-" + j/3))
                    return false;
        }
    }
    return true;
}
```

**4. Contains Duplicate**
```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for(int n : nums) if(!set.add(n)) return true;
    return false;
}
```

**5. Longest Consecutive Sequence**
```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for(int n : nums) set.add(n);
    int max = 0;
    for(int n : set) {
        if(!set.contains(n - 1)) {
            int curr = n, count = 1;
            while(set.contains(curr + 1)) { curr++; count++; }
            max = Math.max(max, count);
        }
    }
    return max;
}
```

### Key Tips & Tricks
- If elements have a small range, use an array instead of HashMap for better performance.
- `map.getOrDefault(key, defaultVal)` and `map.computeIfAbsent()` save a lot of boilerplate.

---

## 4. Linked List

### Concept Explanation
Nodes connected by pointers. Memory is not contiguous. Strengths: O(1) insertions/deletions if pointer is known. Weakness: O(N) search/access.

### When to Recognize
- Problem explicitly involves `ListNode`.
- Need to reverse, find middle, or detect cycles.

### Java Template Code (Fast & Slow Pointers)
```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}
```

### Time & Space Complexity
- **Time:** O(N)
- **Space:** O(1) mostly, unless recursive O(N).

### Common Problems & Java Solutions

**1. Reverse Linked List**
```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while(curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

**2. Detect Cycle (Floyd's)**
```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while(fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if(slow == fast) return true;
    }
    return false;
}
```

**3. Merge Two Sorted Lists**
```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), curr = dummy;
    while(l1 != null && l2 != null) {
        if(l1.val < l2.val) { curr.next = l1; l1 = l1.next; }
        else { curr.next = l2; l2 = l2.next; }
        curr = curr.next;
    }
    curr.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

**4. Remove Nth Node From End of List**
```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode fast = dummy, slow = dummy;
    for(int i=0; i<=n; i++) fast = fast.next;
    while(fast != null) { slow = slow.next; fast = fast.next; }
    slow.next = slow.next.next;
    return dummy.next;
}
```

**5. Find Middle of Linked List**
```java
public ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while(fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    return slow;
}
```

### Key Tips & Tricks
- Always use a `dummy` node when the head might change or be deleted.
- Handle `NullPointerException` by checking `curr != null && curr.next != null`.

---

## 5. Stack

### Concept Explanation
LIFO (Last In First Out) structure. Great for nested structures, history tracing, and monotonic constraints (finding the next greater/smaller element).

### When to Recognize
- "Next Greater Element", "Next Smaller Element".
- Parsing parentheses or expressions.
- Maintaining a history where only the most recent state matters.

### Java Template Code (Monotonic Increasing Stack)
```java
Deque<Integer> stack = new ArrayDeque<>();
for (int i = 0; i < nums.length; i++) {
    while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) {
        stack.pop(); // Resolve top element
    }
    stack.push(i);
}
```

### Time & Space Complexity
- **Time:** O(N) because each element is pushed/popped at most once.
- **Space:** O(N) worst case.

### Common Problems & Java Solutions

**1. Valid Parentheses**
```java
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for(char c : s.toCharArray()) {
        if(c == '(') stack.push(')');
        else if(c == '{') stack.push('}');
        else if(c == '[') stack.push(']');
        else if(stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}
```

**2. Min Stack**
```java
class MinStack {
    private Deque<int[]> st = new ArrayDeque<>();
    public void push(int val) {
        if(st.isEmpty()) st.push(new int[]{val, val});
        else st.push(new int[]{val, Math.min(val, st.peek()[1])});
    }
    public void pop() { st.pop(); }
    public int top() { return st.peek()[0]; }
    public int getMin() { return st.peek()[1]; }
}
```

**3. Next Greater Element I**
```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> map = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();
    for(int num : nums2) {
        while(!stack.isEmpty() && stack.peek() < num) map.put(stack.pop(), num);
        stack.push(num);
    }
    int[] res = new int[nums1.length];
    for(int i=0; i<nums1.length; i++) res[i] = map.getOrDefault(nums1[i], -1);
    return res;
}
```

**4. Daily Temperatures**
```java
public int[] dailyTemperatures(int[] temps) {
    int[] res = new int[temps.length];
    Deque<Integer> stack = new ArrayDeque<>();
    for(int i = 0; i < temps.length; i++) {
        while(!stack.isEmpty() && temps[i] > temps[stack.peek()]) {
            int idx = stack.pop();
            res[idx] = i - idx;
        }
        stack.push(i);
    }
    return res;
}
```

**5. Largest Rectangle in Histogram**
```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int maxArea = 0;
    for(int i = 0; i <= heights.length; i++) {
        int h = (i == heights.length ? 0 : heights[i]);
        while(!stack.isEmpty() && h < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
}
```

### Key Tips & Tricks
- Use `Deque<Type> stack = new ArrayDeque<>()` over `Stack<Type>` as it's faster and not synchronized.
- Storing indices instead of values in the stack often provides more context (e.g., width calculation).

---

## 6. Queue / BFS

### Concept Explanation
FIFO (First In First Out) structure. Perfect for Level Order Traversal in trees and finding the shortest path in unweighted graphs.

### When to Recognize
- "Shortest path", "Minimum steps".
- "Level by level" processing.
- Graph/Grid traversal spreading outwards uniformly.

### Java Template Code (BFS)
```java
Queue<Node> q = new LinkedList<>();
q.offer(startNode);
int steps = 0;
while (!q.isEmpty()) {
    int size = q.size(); // process level by level
    for (int i = 0; i < size; i++) {
        Node curr = q.poll();
        if (curr == target) return steps;
        for (Node neighbor : curr.neighbors) {
            q.offer(neighbor);
        }
    }
    steps++;
}
```

### Complexity
- **Time:** O(V + E)
- **Space:** O(W) where W is max width of the tree/graph.

### Common Problems & Java Solutions

**1. Binary Tree Level Order Traversal**
```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if(root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while(!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>();
        for(int i=0; i<size; i++) {
            TreeNode node = q.poll();
            level.add(node.val);
            if(node.left != null) q.offer(node.left);
            if(node.right != null) q.offer(node.right);
        }
        res.add(level);
    }
    return res;
}
```

**2. Rotting Oranges**
```java
public int orangesRotting(int[][] grid) {
    Queue<int[]> q = new LinkedList<>();
    int fresh = 0;
    for(int i=0; i<grid.length; i++) {
        for(int j=0; j<grid[0].length; j++) {
            if(grid[i][j] == 2) q.offer(new int[]{i, j});
            else if(grid[i][j] == 1) fresh++;
        }
    }
    if(fresh == 0) return 0;
    int mins = 0;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    while(!q.isEmpty() && fresh > 0) {
        int size = q.size();
        for(int i=0; i<size; i++) {
            int[] curr = q.poll();
            for(int[] d : dirs) {
                int r = curr[0]+d[0], c = curr[1]+d[1];
                if(r>=0 && r<grid.length && c>=0 && c<grid[0].length && grid[r][c] == 1) {
                    grid[r][c] = 2; fresh--; q.offer(new int[]{r, c});
                }
            }
        }
        mins++;
    }
    return fresh == 0 ? mins : -1;
}
```

**3. Number of Islands (BFS Approach)**
```java
public int numIslands(char[][] grid) {
    int count = 0;
    for(int i=0; i<grid.length; i++) {
        for(int j=0; j<grid[0].length; j++) {
            if(grid[i][j] == '1') {
                count++;
                Queue<int[]> q = new LinkedList<>();
                q.offer(new int[]{i, j});
                grid[i][j] = '0'; // mark visited
                while(!q.isEmpty()) {
                    int[] curr = q.poll();
                    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
                    for(int[] d : dirs) {
                        int r = curr[0]+d[0], c = curr[1]+d[1];
                        if(r>=0 && r<grid.length && c>=0 && c<grid[0].length && grid[r][c]=='1') {
                            q.offer(new int[]{r, c}); grid[r][c] = '0';
                        }
                    }
                }
            }
        }
    }
    return count;
}
```

---

## 7. Trees

### Concept Explanation
Hierarchical data structures. Traversals (Pre/In/Post) define the order of processing. Most tree problems are elegantly solved using Recursion (DFS).

### When to Recognize
- "Binary Tree", "Binary Search Tree".
- Finding ancestors, depths, paths.
- Tree construction or serialization.

### Java Template Code (DFS / Recursion)
```java
public int dfs(TreeNode root) {
    if (root == null) return 0; // Base case
    int left = dfs(root.left);
    int right = dfs(root.right);
    return process(root, left, right);
}
```

### Complexity
- **Time:** O(N) visiting each node.
- **Space:** O(H) where H is tree height (Call stack).

### Common Problems & Java Solutions

**1. Maximum Depth of Binary Tree**
```java
public int maxDepth(TreeNode root) {
    if(root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

**2. Validate Binary Search Tree**
```java
public boolean isValidBST(TreeNode root) {
    return isValidBST(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
private boolean isValidBST(TreeNode root, long min, long max) {
    if(root == null) return true;
    if(root.val <= min || root.val >= max) return false;
    return isValidBST(root.left, min, root.val) && isValidBST(root.right, root.val, max);
}
```

**3. Lowest Common Ancestor of a Binary Tree**
```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if(root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if(left != null && right != null) return root;
    return left != null ? left : right;
}
```

**4. Binary Tree Right Side View**
```java
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    dfs(root, res, 0);
    return res;
}
private void dfs(TreeNode root, List<Integer> res, int depth) {
    if(root == null) return;
    if(depth == res.size()) res.add(root.val);
    dfs(root.right, res, depth + 1);
    dfs(root.left, res, depth + 1);
}
```

**5. Diameter of Binary Tree**
```java
int maxDiameter = 0;
public int diameterOfBinaryTree(TreeNode root) {
    depth(root);
    return maxDiameter;
}
private int depth(TreeNode root) {
    if(root == null) return 0;
    int left = depth(root.left);
    int right = depth(root.right);
    maxDiameter = Math.max(maxDiameter, left + right);
    return 1 + Math.max(left, right);
}
```

---

## 8. Graphs

### Concept Explanation
Nodes (vertices) connected by edges. Cycles can occur, so a `visited` set is mandatory. Representations: Adjacency List (most common) or Adjacency Matrix.

### When to Recognize
- "Dependencies", "Connected Components", "Network".
- Topological Sort (DAGs, ordering dependencies like course schedule).
- Union-Find (Dynamic connectivity).

### Java Template Code (DFS Graph)
```java
Set<Integer> visited = new HashSet<>();
public void dfs(int node, Map<Integer, List<Integer>> adj) {
    if (visited.contains(node)) return;
    visited.add(node);
    for (int neighbor : adj.getOrDefault(node, new ArrayList<>())) {
        dfs(neighbor, adj);
    }
}
```

### Complexity
- **Time:** O(V + E)
- **Space:** O(V + E) for adj list, O(V) for visited set.

### Common Problems & Java Solutions

**1. Clone Graph**
```java
Map<Node, Node> map = new HashMap<>();
public Node cloneGraph(Node node) {
    if(node == null) return null;
    if(map.containsKey(node)) return map.get(node);
    Node clone = new Node(node.val);
    map.put(node, clone);
    for(Node neighbor : node.neighbors) clone.neighbors.add(cloneGraph(neighbor));
    return clone;
}
```

**2. Course Schedule (Topological Sort using Kahn's BFS)**
```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    int[] indegree = new int[numCourses];
    List<List<Integer>> adj = new ArrayList<>();
    for(int i=0; i<numCourses; i++) adj.add(new ArrayList<>());
    for(int[] pre : prerequisites) { adj.get(pre[1]).add(pre[0]); indegree[pre[0]]++; }
    
    Queue<Integer> q = new LinkedList<>();
    for(int i=0; i<numCourses; i++) if(indegree[i] == 0) q.offer(i);
    int count = 0;
    while(!q.isEmpty()) {
        int curr = q.poll(); count++;
        for(int next : adj.get(curr)) {
            if(--indegree[next] == 0) q.offer(next);
        }
    }
    return count == numCourses;
}
```

**3. Number of Provinces (Union Find)**
```java
public int findCircleNum(int[][] isConnected) {
    int n = isConnected.length;
    int[] parent = new int[n];
    for(int i=0; i<n; i++) parent[i] = i;
    int count = n;
    for(int i=0; i<n; i++) {
        for(int j=i+1; j<n; j++) {
            if(isConnected[i][j] == 1) {
                int p1 = find(parent, i), p2 = find(parent, j);
                if(p1 != p2) { parent[p1] = p2; count--; }
            }
        }
    }
    return count;
}
private int find(int[] parent, int i) {
    if(parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]); // Path compression
}
```

**4. Pacific Atlantic Water Flow**
```java
// Omitted due to size, but standard multi-source DFS from edges.
```

---

## 9. Heap / Priority Queue

### Concept Explanation
Complete binary tree where parent is always smaller (Min-Heap) or larger (Max-Heap) than children. Used for dynamic minimum/maximum tracking.

### When to Recognize
- "Top K", "Kth Largest/Smallest", "Median".
- Merging K sorted structures.

### Java Template Code
```java
// Min-Heap
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
// Max-Heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);

minHeap.offer(val);
if (minHeap.size() > k) minHeap.poll(); // Keep size K
```

### Complexity
- **Time:** O(log K) for insertion/deletion. O(N log K) overall.
- **Space:** O(K)

### Common Problems & Java Solutions

**1. Kth Largest Element in an Array**
```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for(int n : nums) {
        minHeap.offer(n);
        if(minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek();
}
```

**2. Top K Frequent Elements**
```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> map = new HashMap<>();
    for(int n : nums) map.put(n, map.getOrDefault(n, 0) + 1);
    PriorityQueue<Integer> pq = new PriorityQueue<>((a, b) -> map.get(a) - map.get(b));
    for(int n : map.keySet()) {
        pq.offer(n);
        if(pq.size() > k) pq.poll();
    }
    return pq.stream().mapToInt(i->i).toArray();
}
```

**3. Find Median from Data Stream**
```java
class MedianFinder {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    
    public void addNum(int num) {
        maxHeap.offer(num);
        minHeap.offer(maxHeap.poll());
        if(maxHeap.size() < minHeap.size()) maxHeap.offer(minHeap.poll());
    }
    
    public double findMedian() {
        if(maxHeap.size() == minHeap.size()) return (maxHeap.peek() + minHeap.peek()) / 2.0;
        return maxHeap.peek();
    }
}
```

---

## 10. Recursion & Backtracking

### Concept Explanation
Building incrementally, dropping (backtracking) solutions that fail constraints. Essentially a Depth First Search (DFS) on the state space tree.

### When to Recognize
- "Generate all permutations / combinations / subsets".
- Finding a valid path in a maze (Sudoku, N-Queens).
- Constraints must be tested incrementally.

### Java Template Code
```java
public void backtrack(List<List<Integer>> res, List<Integer> tempList, int[] nums, int start) {
    if (goalReached) {
        res.add(new ArrayList<>(tempList));
        return;
    }
    for (int i = start; i < nums.length; i++) {
        // Option selection
        tempList.add(nums[i]);
        backtrack(res, tempList, nums, i + 1);
        // Backtrack (undo selection)
        tempList.remove(tempList.size() - 1);
    }
}
```

### Complexity
- **Time:** O(N!), O(2^N) or O(K^N) - usually exponential.
- **Space:** O(N) stack space + storage for answers.

### Common Problems & Java Solutions

**1. Subsets**
```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    backtrack(res, new ArrayList<>(), nums, 0);
    return res;
}
private void backtrack(List<List<Integer>> res, List<Integer> temp, int[] nums, int start) {
    res.add(new ArrayList<>(temp));
    for(int i = start; i < nums.length; i++) {
        temp.add(nums[i]);
        backtrack(res, temp, nums, i + 1);
        temp.remove(temp.size() - 1);
    }
}
```

**2. Permutations**
```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    backtrack(res, new ArrayList<>(), nums);
    return res;
}
private void backtrack(List<List<Integer>> res, List<Integer> temp, int[] nums) {
    if(temp.size() == nums.length) { res.add(new ArrayList<>(temp)); return; }
    for(int i = 0; i < nums.length; i++) {
        if(temp.contains(nums[i])) continue;
        temp.add(nums[i]);
        backtrack(res, temp, nums);
        temp.remove(temp.size() - 1);
    }
}
```

**3. Word Search**
```java
public boolean exist(char[][] board, String word) {
    for(int i=0; i<board.length; i++)
        for(int j=0; j<board[0].length; j++)
            if(dfs(board, i, j, word, 0)) return true;
    return false;
}
private boolean dfs(char[][] b, int r, int c, String w, int idx) {
    if(idx == w.length()) return true;
    if(r<0 || r>=b.length || c<0 || c>=b[0].length || b[r][c] != w.charAt(idx)) return false;
    char temp = b[r][c];
    b[r][c] = '#'; // visited
    boolean found = dfs(b, r+1, c, w, idx+1) || dfs(b, r-1, c, w, idx+1) ||
                    dfs(b, r, c+1, w, idx+1) || dfs(b, r, c-1, w, idx+1);
    b[r][c] = temp; // backtrack
    return found;
}
```

---

## 11. Dynamic Programming

### Concept Explanation
Breaking a problem into overlapping subproblems. Compute once, store (memoize/tabulate), and reuse. DP = Recursion + Memoization.

### When to Recognize
- "Maximum", "Minimum", "Longest", "Shortest", "Number of ways".
- Current state depends on previous state(s).
- Combinatorics with overlapping conditions.

### Java Template Code (1D Tabulation)
```java
int[] dp = new int[n + 1];
dp[0] = baseCase0;
dp[1] = baseCase1;
for (int i = 2; i <= n; i++) {
    dp[i] = dp[i-1] + dp[i-2]; // Transition
}
return dp[n];
```

### Complexity
- **Time:** O(States) × O(Transitions per state)
- **Space:** O(States) - can often be optimized to O(1) if looking at previous 2 elements.

### Common Problems & Java Solutions

**1. Climbing Stairs**
```java
public int climbStairs(int n) {
    if(n <= 2) return n;
    int a = 1, b = 2;
    for(int i = 3; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}
```

**2. House Robber**
```java
public int rob(int[] nums) {
    int prev1 = 0, prev2 = 0;
    for(int n : nums) {
        int temp = prev1;
        prev1 = Math.max(prev2 + n, prev1);
        prev2 = temp;
    }
    return prev1;
}
```

**3. Coin Change**
```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for(int i=1; i<=amount; i++) {
        for(int coin : coins) {
            if(coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

**4. Longest Increasing Subsequence**
```java
public int lengthOfLIS(int[] nums) {
    int[] dp = new int[nums.length];
    Arrays.fill(dp, 1);
    int max = 1;
    for(int i=1; i<nums.length; i++) {
        for(int j=0; j<i; j++) {
            if(nums[i] > nums[j]) dp[i] = Math.max(dp[i], dp[j] + 1);
        }
        max = Math.max(max, dp[i]);
    }
    return max;
}
```

---

## 12. Sliding Window

### Concept Explanation
Maintains a "window" of items (substring, subarray). Expand the right edge, and shrink the left edge when constraints are violated.

### When to Recognize
- "Contiguous subarray/substring".
- Max/Min size that satisfies a condition.

### Java Template Code
```java
int left = 0, res = 0;
for (int right = 0; right < nums.length; right++) {
    // add nums[right] to window state
    while (conditionViolated) {
        // remove nums[left] from window state
        left++;
    }
    res = Math.max(res, right - left + 1);
}
```

### Complexity
- **Time:** O(N) - left and right pointers only move forward.
- **Space:** O(1) or O(N) if using HashMap.

### Common Problems & Java Solutions

**1. Maximum Average Subarray I (Fixed Window)**
```java
public double findMaxAverage(int[] nums, int k) {
    long sum = 0;
    for(int i=0; i<k; i++) sum += nums[i];
    long max = sum;
    for(int i=k; i<nums.length; i++) {
        sum += nums[i] - nums[i-k];
        max = Math.max(max, sum);
    }
    return max / (double) k;
}
```

**2. Minimum Size Subarray Sum (Variable Window)**
```java
public int minSubArrayLen(int target, int[] nums) {
    int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
    for(int right=0; right<nums.length; right++) {
        sum += nums[right];
        while(sum >= target) {
            minLen = Math.min(minLen, right - left + 1);
            sum -= nums[left++];
        }
    }
    return minLen == Integer.MAX_VALUE ? 0 : minLen;
}
```

---

## 13. Two Pointers

### Concept Explanation
Two variables pointing at indices. Usually move towards each other (sorted arrays) or in the same direction (fast/slow pointers).

### When to Recognize
- Searching in a sorted array (Two Sum II).
- Comparing left/right elements (Palindromes, Trapping Rain Water).

### Java Template Code
```java
int left = 0, right = nums.length - 1;
while (left < right) {
    int sum = nums[left] + nums[right];
    if (sum == target) return new int[]{left, right};
    else if (sum < target) left++;
    else right--;
}
```

### Complexity
- **Time:** O(N) usually. Sorting first takes O(N log N).
- **Space:** O(1)

### Common Problems & Java Solutions

**1. Container With Most Water**
```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, max = 0;
    while(left < right) {
        int w = right - left;
        int h = Math.min(height[left], height[right]);
        max = Math.max(max, w * h);
        if(height[left] < height[right]) left++;
        else right--;
    }
    return max;
}
```

**2. 3Sum**
```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> res = new ArrayList<>();
    for(int i=0; i<nums.length-2; i++) {
        if(i > 0 && nums[i] == nums[i-1]) continue;
        int l = i+1, r = nums.length-1;
        while(l < r) {
            int sum = nums[i] + nums[l] + nums[r];
            if(sum == 0) {
                res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                while(l<r && nums[l] == nums[l+1]) l++;
                while(l<r && nums[r] == nums[r-1]) r--;
                l++; r--;
            } else if(sum < 0) l++;
            else r--;
        }
    }
    return res;
}
```

---

## 14. Binary Search

### Concept Explanation
Halving the search space recursively or iteratively. Requires a monotonic function (usually sorted array). Can also search "on the answer".

### When to Recognize
- "Sorted array".
- "O(log N)" time constraint.
- Find minimum capacity / maximum distance (Binary Search on Answer).

### Java Template Code
```java
int left = 0, right = nums.length - 1;
while (left <= right) {
    int mid = left + (right - left) / 2; // Prevents overflow
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
}
return -1;
```

### Complexity
- **Time:** O(log N)
- **Space:** O(1)

### Common Problems & Java Solutions

**1. Binary Search**
```java
// See template above
```

**2. Search in Rotated Sorted Array**
```java
public int search(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while(l <= r) {
        int mid = l + (r - l) / 2;
        if(nums[mid] == target) return mid;
        // Left half is sorted
        if(nums[l] <= nums[mid]) {
            if(target >= nums[l] && target < nums[mid]) r = mid - 1;
            else l = mid + 1;
        } 
        // Right half is sorted
        else {
            if(target > nums[mid] && target <= nums[r]) l = mid + 1;
            else r = mid - 1;
        }
    }
    return -1;
}
```

---

## 15. Greedy

### Concept Explanation
Making the locally optimal choice at each step hoping it leads to the globally optimal solution. Often involves sorting first.

### When to Recognize
- "Minimum jumps", "Maximum intervals", "Optimal assignments".
- No overlapping subproblems that need future look-back (otherwise use DP).

### Java Template
- Typically involves custom sorting arrays or using PriorityQueues. No standard loop template.

### Complexity
- **Time:** O(N log N) due to sorting, or O(N).
- **Space:** O(1) mostly.

### Common Problems & Java Solutions

**1. Jump Game**
```java
public boolean canJump(int[] nums) {
    int maxReach = 0;
    for(int i=0; i<nums.length; i++) {
        if(i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
    }
    return true;
}
```

**2. Gas Station**
```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, current = 0, start = 0;
    for(int i=0; i<gas.length; i++) {
        int diff = gas[i] - cost[i];
        total += diff;
        current += diff;
        if(current < 0) { start = i + 1; current = 0; }
    }
    return total >= 0 ? start : -1;
}
```

---

## 16. Divide and Conquer

### Concept Explanation
Divide problem into independent subproblems, solve them, and combine. Merge Sort and Quick Sort are primary examples.

### When to Recognize
- Tree recursion where branches don't overlap.
- O(N log N) sorting natively.

### Complexity
- **Time:** O(N log N) usually.
- **Space:** O(log N) to O(N).

### Common Problems & Java Solutions

**1. Sort an Array (Merge Sort Core)**
```java
public void merge(int[] arr, int l, int m, int r) {
    int[] left = Arrays.copyOfRange(arr, l, m + 1);
    int[] right = Arrays.copyOfRange(arr, m + 1, r + 1);
    int i = 0, j = 0, k = l;
    while(i < left.length && j < right.length) {
        if(left[i] <= right[j]) arr[k++] = left[i++];
        else arr[k++] = right[j++];
    }
    while(i < left.length) arr[k++] = left[i++];
    while(j < right.length) arr[k++] = right[j++];
}
```

---

# Appendices & Cheat Sheets

## DSA Patterns Recognition Guide

| If you see this keyword / constraint | Think about this pattern |
| ------------------------------------ | ------------------------ |
| "Top K", "Kth largest/smallest" | Heap / Priority Queue |
| "Contiguous subarray/substring" | Sliding Window |
| "Sorted array" + O(N) | Two Pointers |
| "Sorted array" + O(log N) | Binary Search |
| "Tree" + "Level by level" | BFS (Queue) |
| "Tree" + "Path / Depth / Ancestor" | DFS (Recursion) |
| "Shortest path in unweighted graph"| BFS |
| "Graph dependencies", "Prerequisites"| Topological Sort (Kahn's) |
| "All combinations/permutations" | Backtracking |
| "Optimization", "Overlapping Subproblems"| Dynamic Programming |
| "Next greater/smaller element" | Monotonic Stack |

---

## Java Collections for DSA Cheat Sheet

- **List:** Use `ArrayList<>` for O(1) random access. Use `LinkedList<>` only if treating as a standard Queue.
- **Set:** `HashSet<>` (O(1) lookups). `TreeSet<>` (O(log N) lookups, sorted data). `LinkedHashSet<>` (O(1) lookups + insertion order).
- **Map:** `HashMap<>` (O(1) get/put). `TreeMap<>` (O(log N) get/put, sorted keys).
- **Queue/Deque:** `ArrayDeque<>` is faster than `LinkedList` for stacks and queues.
- **PriorityQueue:** Defaults to Min-Heap. Pass `Collections.reverseOrder()` for Max-Heap.
- **Strings:** `StringBuilder` for concatenation inside loops. `s.toCharArray()` for faster iteration.

---

## Big O Complexity Cheat Sheet

| Data Structure / Alg | Access | Search | Insertion | Deletion |
| -------------------- | ------ | ------ | --------- | -------- |
| Array | O(1) | O(N) | O(N) | O(N) |
| HashMap / HashSet | N/A | O(1) | O(1) | O(1) |
| LinkedList | O(N) | O(N) | O(1)* | O(1)* |
| Binary Search Tree | O(log N)| O(log N)| O(log N)| O(log N) |
| Binary Heap | N/A | O(N) | O(log N) | O(log N) |
| Quick/Merge Sort | O(N log N)| | | |
*\*If pointer to node is already known.*

---

## Top 50 Coding Interview Questions Categorized
*(Cross-reference the above sections for full logic!)*

### Arrays & Hashing
1. Two Sum (Hashing)
2. Valid Anagram (Hashing/Arrays)
3. Contains Duplicate (Hashing)
4. Group Anagrams (Hashing)
5. Top K Frequent Elements (Heap/Hashing)
6. Product of Array Except Self (Prefix Arrays)
7. Valid Sudoku (Hashing)
8. Longest Consecutive Sequence (Hashing)

### Two Pointers
9. Valid Palindrome (Two Pointers)
10. Two Sum II (Two Pointers)
11. 3Sum (Two Pointers)
12. Container With Most Water (Two Pointers)
13. Trapping Rain Water (Two Pointers)

### Sliding Window
14. Best Time to Buy and Sell Stock (Sliding Window)
15. Longest Substring Without Repeating Characters (Sliding Window)
16. Longest Repeating Character Replacement (Sliding Window)
17. Minimum Window Substring (Sliding Window)

### Stack
18. Valid Parentheses (Stack)
19. Min Stack (Stack)
20. Evaluate Reverse Polish Notation (Stack)
21. Generate Parentheses (Backtracking/Stack)
22. Daily Temperatures (Monotonic Stack)

### Binary Search
23. Binary Search
24. Search a 2D Matrix (Binary Search)
25. Koko Eating Bananas (Binary Search on Answer)
26. Find Minimum in Rotated Sorted Array
27. Search in Rotated Sorted Array

### Linked List
28. Reverse Linked List (Pointers)
29. Merge Two Sorted Lists (Pointers)
30. Reorder List (Fast/Slow, Reverse)
31. Remove Nth Node From End of List (Two Pointers)
32. Linked List Cycle (Floyd's Fast/Slow)

### Trees
33. Invert Binary Tree (DFS)
34. Maximum Depth of Binary Tree (DFS)
35. Diameter of Binary Tree (DFS)
36. Balanced Binary Tree (DFS)
37. Same Tree (DFS)
38. Subtree of Another Tree (DFS)
39. Lowest Common Ancestor of a BST (DFS)
40. Binary Tree Level Order Traversal (BFS)

### Tries & Heap
41. Implement Trie (Prefix Tree)
42. Kth Largest Element in a Stream (Min-Heap)
43. Last Stone Weight (Max-Heap)

### Backtracking & Graphs
44. Subsets (Backtracking)
45. Combination Sum (Backtracking)
46. Permutations (Backtracking)
47. Number of Islands (BFS/DFS Graph)
48. Max Area of Island (DFS Graph)
49. Clone Graph (DFS/BFS Graph)

### Dynamic Programming
50. Climbing Stairs (1D DP)
51. Coin Change (1D DP)
52. Longest Common Subsequence (2D DP)
