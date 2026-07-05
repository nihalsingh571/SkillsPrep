# Java DSA Master Guide: HashMap, HashSet, and Sliding Window

This guide provides an end-to-end, deep-dive explanation of **HashMap**, **HashSet**, and the **Sliding Window Technique** in Java. It covers internal architectures, mathematical complexities, code templates, and walkthroughs of basic to advanced algorithmic problems.

---

## 1. Hashing Fundamentals in Java

Before understanding collections, you must understand **Hashing**. Hashing is the process of mapping arbitrary-sized data to fixed-size values (usually integers) using a mathematical formula called a **Hash Function**.

### The `hashCode()` and `equals()` Contract
In Java, every class inherits two crucial methods from the parent `Object` class:
1. `public int hashCode()`: Returns an integer representation of the object's memory address or content value.
2. `public boolean equals(Object obj)`: Compares two objects for equality.

#### The Contract Rules:
* If two objects are equal according to the `equals(Object)` method, calling `hashCode()` on each must produce the **same integer result**.
* If two objects produce the same hash code, they are **not necessarily equal**. This scenario is called a **Hash Collision**.
* If you override `equals()`, you **must** override `hashCode()` to maintain this contract. Otherwise, hashing-based collections like `HashMap` and `HashSet` will fail to retrieve elements correctly.

---

## 2. HashMap: Under the Hood

A `HashMap<K, V>` is a hashing-based collection that stores data in **Key-Value pairs**. It provides $O(1)$ average time complexity for basic search, insertion, and deletion operations.

```
 [Key] ──> [hash()] ──> [Index Calculation] ──> [Bucket Array (Table)]
                                                      │
                                                      ├──> Bucket [0] ──> null
                                                      ├──> Bucket [1] ──> [Node K1:V1] ──> null
                                                      └──> Bucket [2] ──> [Node K2:V2] ──> [Node K3:V3] (Chaining)
```

### Internal Architecture
Internally, a `HashMap` maintains an array of buckets (often referred to as the node table):
* **Node Struct:** Each entry in the array is a Node containing four fields:
  1. `int hash` (cached hash code)
  2. `K key`
  3. `V value`
  4. `Node<K,V> next` (pointer to the next node in case of collisions)

### How Hashing and Indexing Works
When you call `map.put(key, value)`:
1. **Hash Code Calculation:** The map calculates the key's hash code and runs a secondary utility function to distribute the bits evenly:
   $$\text{hash} = \text{key.hashCode()} \oplus (\text{key.hashCode()} \gg 16)$$
2. **Index Mapping:** The hash is mapped to a valid index in the bucket array using bitwise AND (which acts as a modulo operation when capacity $N$ is a power of 2):
   $$\text{index} = (\text{capacity} - 1) \ \& \ \text{hash}$$

### Collision Resolution
If two different keys map to the same index, a **collision** occurs. Java resolves this using **Chaining**:
* **Linked List Chaining:** Colliding nodes are appended to a linked list starting at that bucket index.
* **Red-Black Tree Conversion (Java 8+ Optimization):**
  * If a linked list chain exceeds a threshold of **8 elements** (`TREEIFY_THRESHOLD`) and the total map capacity is at least **64** (`MIN_TREEIFY_CAPACITY`), the bucket's linked list is converted into a self-balancing **Red-Black Tree**.
  * This changes the worst-case lookup time from $O(N)$ (linked list traversal) to $O(\log N)$ (binary tree search), protecting against Denial of Service (DoS) attacks that attempt to exploit hash collisions.
  * If the number of nodes in a bucket drops below **6** (`UNTREEIFY_THRESHOLD`) during removal or resizing, the tree is converted back to a flat linked list.

### Capacity, Load Factor, and Rehashing
* **Default Initial Capacity:** $16$ buckets (always a power of 2).
* **Load Factor:** Defaults to $0.75$. It is the ratio of elements stored to total bucket capacity before the map resizes:
  $$\text{Resize Threshold} = \text{Capacity} \times \text{Load Factor}$$
* **Rehashing:** When the element count exceeds the threshold, the bucket array size is **doubled**. All existing keys are re-evaluated, their index positions recalculate, and nodes migrate to the new array. This is an $O(N)$ operation.

### HashMap Complexity & Operations Table

| Operation | Average Case | Worst Case (Fully Collided) | Space Complexity |
| :--- | :--- | :--- | :--- |
| **`put(K, V)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |
| **`get(K)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |
| **`remove(K)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |
| **`containsKey(K)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |

---

## 3. HashSet: Under the Hood

A `HashSet<E>` is a collection that stores **unique elements** only. It does not allow duplicate entries.

### The Internals: Reusing HashMap
A `HashSet` is not a standalone structure. It is simply a wrapper around a `HashMap` instance:
```java
// Inside the source code of java.util.HashSet:
public class HashSet<E> implements Set<E> {
    private transient HashMap<E, Object> map;

    // Dummy value to associate with an Object in the backing Map
    private static final Object PRESENT = new Object();

    public HashSet() {
        map = new HashMap<>();
    }

    public boolean add(E e) {
        return map.put(e, PRESENT) == null;
    }

    public boolean contains(Object o) {
        return map.containsKey(o);
    }
}
```

* When you call `add(element)`, the `HashSet` inserts the element as a **Key** into the backing `HashMap`, mapping it to a dummy static object instance named `PRESENT`.
* Since `HashMap` keys must be unique, duplicate inserts are automatically overwritten, maintaining `HashSet` uniqueness.
* All lookups (`contains(element)`) call `map.containsKey(element)`.

### HashSet Complexity & Operations Table

| Operation | Average Case | Worst Case | Space Complexity |
| :--- | :--- | :--- | :--- |
| **`add(E)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |
| **`contains(Object)`**| $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |
| **`remove(Object)`** | $O(1)$ | $O(\log N)$ | $O(1)$ auxiliary |

---

## 4. The Sliding Window Technique

The **Sliding Window** is an algorithmic optimization technique used to reduce nested loop solutions from $O(N^2)$ or $O(N^3)$ to linear $O(N)$ time complexity.

```
Initial Array:  [ 1,  3, -1, -3,  5,  3,  6,  7 ]  (K=3)

Window 1:       [ 1,  3, -1]                         Sum = 3
Window 2:          [ 3, -1, -3]                      Sum = -1
Window 3:              [-1, -3,  5]                  Sum = 1
Window 4:                  [-3,  5,  3]              Sum = 5
```

### When to Use Sliding Window:
1. The problem involves a **contiguous sequence** (subarrays, substrings, sublists).
2. The problem asks for a minimum, maximum, longest, shortest, or target value matching criteria.
3. Brute force solutions require analyzing overlapping segments repeatedly.

### Core Window Types

#### Type A: Fixed Size Window
The size of the window $K$ is constant. 
* **Mechanism:** 
  1. Calculate the initial value (e.g. sum, character count) of the first window of size $K$.
  2. Slide the window one element forward at a time.
  3. Update the state by **adding** the new element entering the window from the right and **subtracting** the old element exiting the window from the left.

#### Type B: Variable Size (Dynamic) Window
The window size expands or contracts dynamically based on constraints.
* **Mechanism:**
  1. Maintain two pointers: `left` (window start) and `right` (window end).
  2. Expand the window by incrementing `right` and incorporating elements.
  3. If a constraint is violated, contract the window from the left by incrementing `left` until the constraint is satisfied again.

---

## 5. Algorithmic Problems: Basic to Advanced

Here are 5 classic problems showing how to implement HashMaps, HashSets, and Sliding Windows in Java.

---

### Example 1 (Basic HashMap): Two Sum
* **LeetCode Number:** 1
* **Difficulty:** Easy
* **Problem Statement:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.
* **Analogy/Logic:** As you walk through the array, calculate the "complement" needed to reach the target ($C = \text{target} - \text{current}$). Check if the complement is already in your HashMap. If yes, you found the pair. If not, add the current number and its index to the map.

#### Java Solution:
```java
import java.util.HashMap;

public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        // Key: Element Value, Value: Element Index
        HashMap<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            // Check if complement has been seen
            if (map.containsKey(complement)) {
                return new int[] { map.get(complement), i };
            }
            
            // Store the current number with its index
            map.put(nums[i], i);
        }
        
        // Return empty array if no match is found
        return new int[] {};
    }
}
```
* **Time Complexity:** $O(N)$ — We traverse the array of length $N$ exactly once. Each map lookup takes $O(1)$ average time.
* **Space Complexity:** $O(N)$ — In the worst case, we store $N$ elements in the HashMap.

---

### Example 2 (Basic HashSet): Contains Duplicate
* **LeetCode Number:** 217
* **Difficulty:** Easy
* **Problem Statement:** Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.
* **Logic:** Use a HashSet to track numbers you have seen. For each number, attempt to add it to the set. If `add()` returns `false` (or `contains()` is true), a duplicate exists.

#### Java Solution:
```java
import java.util.HashSet;

public class ContainsDuplicate {
    public boolean containsDuplicate(int[] nums) {
        HashSet<Integer> seen = new HashSet<>();
        
        for (int num : nums) {
            // add() returns false if the element was already present in the set
            if (!seen.add(num)) {
                return true;
            }
        }
        
        return false;
    }
}
```
* **Time Complexity:** $O(N)$ — Traversal of $N$ elements. HashSet insertion takes $O(1)$ average time.
* **Space Complexity:** $O(N)$ — In the worst case, we store $N$ unique elements in the set.

---

### Example 3 (Fixed Sliding Window): Max Sum Subarray of Size K
* **Difficulty:** Easy/Medium
* **Problem Statement:** Given an array of integers and a number $K$, find the maximum sum of any contiguous subarray of size $K$.
* **Logic:** Compute the sum of the first $K$ elements. Then, slide the window across the array. For each step, add the element at `i` and subtract the element at `i - K` to compute the new window sum in $O(1)$ time.

#### Java Solution:
```java
public class MaxSumSubarray {
    public int findMaxSumSubarray(int[] nums, int k) {
        if (nums == null || nums.length < k || k <= 0) {
            return 0;
        }

        int windowSum = 0;
        
        // Calculate the sum of the first window
        for (int i = 0; i < k; i++) {
            windowSum += nums[i];
        }

        int maxSum = windowSum;

        // Slide the window from index k to the end of the array
        for (int i = k; i < nums.length; i++) {
            // Slide: Add the entering element, subtract the exiting element
            windowSum += nums[i] - nums[i - k];
            maxSum = Math.max(maxSum, windowSum);
        }

        return maxSum;
    }
}
```
* **Time Complexity:** $O(N)$ — The loop runs from $K$ to $N$, performing constant time operations at each step.
* **Space Complexity:** $O(1)$ — Only a few integer variables are used for tracking.

---

### Example 4 (Variable Sliding Window + HashSet): Longest Substring Without Repeating Characters
* **LeetCode Number:** 3
* **Difficulty:** Medium
* **Problem Statement:** Given a string `s`, find the length of the longest substring without repeating characters.
* **Logic:** Maintain a variable window `[left, right]`. Expand the window by adding characters at `right` to a HashSet. If the character at `right` is already in the set, contract the window by removing characters from the `left` and incrementing `left` until the duplicate character is removed.

#### Java Solution:
```java
import java.util.HashSet;

public class LongestSubstring {
    public int lengthOfLongestSubstring(String s) {
        if (s == null || s.length() == 0) {
            return 0;
        }

        HashSet<Character> set = new HashSet<>();
        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char currChar = s.charAt(right);

            // If a duplicate is found, shrink the window from the left
            while (set.contains(currChar)) {
                set.remove(s.charAt(left));
                left++;
            }

            // Add the current character to the window
            set.add(currChar);
            
            // Calculate and track the maximum length
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }
}
```
* **Time Complexity:** $O(N)$ — Although there is a nested `while` loop, each character is added to the set once and removed at most once. The pointers `left` and `right` traverse the string length $N$ at most once, resulting in $O(2N) = O(N)$ time.
* **Space Complexity:** $O(\min(N, M))$ — Space matches window size, bounded by string length $N$ and the character set size $M$ (e.g. 26 for lowercase English, or 128 for ASCII).

---

### Example 5 (Sliding Window + HashMap): Minimum Window Substring
* **LeetCode Number:** 76
* **Difficulty:** Hard
* **Problem Statement:** Given two strings `s` and `t` of lengths $m$ and $n$, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return the empty string `""`.
* **Logic:**
  1. Count character frequencies in `t` using a HashMap (`mapT`).
  2. Use a sliding window `[left, right]` to scan `s`. Track character frequencies in the current window using another HashMap (`windowMap`).
  3. Maintain a `have` counter tracking how many unique characters match the required frequency in `t` (`need`).
  4. Expand `right`. If the character's count matches the required frequency in `mapT`, increment `have`.
  5. While `have == need`, record the minimum window length, then shrink the window by removing the character at `left` and incrementing `left` to find a smaller valid window.

#### Java Solution:
```java
import java.util.HashMap;

public class MinimumWindowSubstring {
    public String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) {
            return "";
        }

        // Map containing target character frequencies
        HashMap<Character, Integer> mapT = new HashMap<>();
        for (char c : t.toCharArray()) {
            mapT.put(c, mapT.getOrDefault(c, 0) + 1);
        }

        int need = mapT.size();
        int have = 0;

        // Map tracking active characters in the sliding window
        HashMap<Character, Integer> windowMap = new HashMap<>();
        
        // Tracking window metrics: [minLength, startIdx, endIdx]
        int minLen = Integer.MAX_VALUE;
        int minStart = 0;
        int minEnd = 0;

        int left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            
            // If the character is part of target string, update window counts
            if (mapT.containsKey(c)) {
                windowMap.put(c, windowMap.getOrDefault(c, 0) + 1);
                
                // If count matches target frequency, increment our matching counter
                if (windowMap.get(c).equals(mapT.get(c))) {
                    have++;
                }
            }

            // While we have all required characters, shrink the window from the left
            while (have == need) {
                // Record current minimum window indices
                int currentWindowLen = right - left + 1;
                if (currentWindowLen < minLen) {
                    minLen = currentWindowLen;
                    minStart = left;
                    minEnd = right;
                }

                char leftChar = s.charAt(left);
                if (mapT.containsKey(leftChar)) {
                    // Decrease count in window map
                    windowMap.put(leftChar, windowMap.get(leftChar) - 1);
                    
                    // If count falls below target frequency, decrement have counter
                    if (windowMap.get(leftChar) < mapT.get(leftChar)) {
                        have--;
                    }
                }
                
                // Move the left pointer forward
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minEnd + 1);
    }
}
```
* **Time Complexity:** $O(N + M)$ — Where $N$ is the length of string `s` and $M$ is the length of string `t`. We scan `t` once to build the frequency map, and then slide our pointers across `s` at most twice.
* **Space Complexity:** $O(N + M)$ — In the worst case, both maps store all distinct characters present in `s` and `t`.

---

## 6. Applications & Use Cases in Production Systems

Hashing-based structures and sliding window logic are used extensively in modern backend engines:

1. **Caching (LRU Cache):**
   * An **LRU (Least Recently Used) Cache** combines a `HashMap` (for $O(1)$ lookups) and a custom Doubly Linked List (for $O(1)$ updates to access order).
2. **Rate Limiting (Sliding Window Log / Sliding Window Counter):**
   * API Gateways (like Kong, Envoy, or custom spring-boot filters) use sliding windows to track client requests over time.
   * *Example:* If client requests must not exceed 100 requests per minute, a sliding window tracks timestamps of requests made in the last 60 seconds, rejecting new requests if the limit is exceeded.
3. **Database Indexing:**
   * Hashing indexes are used in databases (like PostgreSQL hash indexes) for equality comparisons (`=`), providing fast lookups compared to B-Trees.
4. **Data Stream Processing:**
   * Analytics platforms (like Apache Flink or Spark Streaming) process data in sliding windows (e.g. calculating average server response times over the last 10 minutes, updated every 30 seconds).
5. **JSON/YAML Mapping Engines:**
   * Parser engines like Jackson or Gson deserialize incoming JSON documents directly into HashMaps before mapping them to Java objects.
