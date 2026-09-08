# Greedy Algorithms and Dynamic Programming in JavaScript

Welcome! Transitioning from Java to JavaScript for DP and Greedy problems is typically smooth. The logic is identical, but JavaScript's dynamic typing and array initialization syntax will save you a significant amount of boilerplate code. 

Let's break down these two critical paradigms.

---

## PART 1: GREEDY ALGORITHMS

Greedy algorithms make the locally optimal choice at each stage with the hope of finding a global optimum. They don't look back or reconsider past decisions.

**How to identify Greedy problems:**
- Problem asks for an extreme (min/max).
- A local optimal choice naturally leads to a global optimal solution.
- Choices cannot be 'undone'.
- Many involve sorting a list and iterating once.

### 1. Activity Selection / Non-overlapping Intervals

**Problem:** Given start and end times of activities, find the maximum number of non-overlapping activities.

```javascript
/**
 * Activity Selection
 * Time Complexity: O(N log N) for sorting
 */
function activitySelection(start, end) {
    const n = start.length;
    // Combine into a single structure for sorting
    const activities = Array.from({length: n}, (_, i) => [start[i], end[i]]);
    
    // Sort by END time
    activities.sort((a, b) => a[1] - b[1]);
    
    let count = 1;
    let lastEnd = activities[0][1];
    
    for (let i = 1; i < n; i++) {
        // If start time is >= last end time, it doesn't overlap
        if (activities[i][0] >= lastEnd) {
            count++;
            lastEnd = activities[i][1];
        }
    }
    return count;
}
```

### 2. Merge Intervals

**Problem:** Merge all overlapping intervals.

```javascript
/**
 * LeetCode 56: Merge Intervals
 */
function merge(intervals) {
    if (intervals.length <= 1) return intervals;
    
    // Sort by START time
    intervals.sort((a, b) => a[0] - b[0]);
    
    const result = [intervals[0]];
    
    for (let i = 1; i < intervals.length; i++) {
        const current = intervals[i];
        const lastMerged = result[result.length - 1];
        
        if (current[0] <= lastMerged[1]) {
            // Overlapping, merge them by updating the end time
            lastMerged[1] = Math.max(lastMerged[1], current[1]);
        } else {
            // Not overlapping, push to result
            result.push(current);
        }
    }
    
    return result;
}
```

### 3. Jump Game I & II

**Jump Game I (Can Reach End?)**
```javascript
function canJump(nums) {
    let maxReach = 0;
    for (let i = 0; i < nums.length; i++) {
        if (i > maxReach) return false; // Stuck
        maxReach = Math.max(maxReach, i + nums[i]);
        if (maxReach >= nums.length - 1) return true;
    }
    return true;
}
```

**Jump Game II (Min Jumps to End)**
```javascript
function jump(nums) {
    let jumps = 0;
    let currentEnd = 0;
    let farthest = 0;
    
    for (let i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        
        if (i === currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }
    
    return jumps;
}
```

### 4. Gas Station (Circular Tour)

```javascript
/**
 * LeetCode 134: Gas Station
 */
function canCompleteCircuit(gas, cost) {
    let totalTank = 0;
    let currTank = 0;
    let startStation = 0;
    
    for (let i = 0; i < gas.length; i++) {
        const net = gas[i] - cost[i];
        totalTank += net;
        currTank += net;
        
        if (currTank < 0) {
            startStation = i + 1;
            currTank = 0;
        }
    }
    
    return totalTank >= 0 ? startStation : -1;
}
```

### 5. Minimum Platforms

```javascript
/**
 * Railway Platforms
 */
function findPlatform(arr, dep, n) {
    arr.sort((a, b) => a - b);
    dep.sort((a, b) => a - b);
    
    let platforms = 1;
    let maxPlatforms = 1;
    
    let i = 1, j = 0;
    
    while (i < n && j < n) {
        if (arr[i] <= dep[j]) {
            platforms++;
            i++;
        } else {
            platforms--;
            j++;
        }
        maxPlatforms = Math.max(maxPlatforms, platforms);
    }
    
    return maxPlatforms;
}
```

---

## PART 2: DYNAMIC PROGRAMMING

Dynamic Programming solves problems by breaking them down into overlapping subproblems and storing the results.

### DP Framework

1.  **State Definition:** What does `dp[i]` or `dp[i][j]` represent?
2.  **State Transition:** How does state `i` relate to `i-1`? `dp[i] = f(dp[i-1], dp[i-2], ...)`
3.  **Base Cases:** Initialize `dp[0]`, `dp[1]`, etc.
4.  **Final Answer:** Usually `dp[n]` or the max/min of the DP array.
5.  **Space Optimization:** Can we reduce 2D space to 1D, or 1D to just variables?

### Array Initialization in JS

```javascript
// 1D DP Array of size N, filled with 0
const dp1 = new Array(n + 1).fill(0);

// 2D DP Array of size (M x N), filled with 0
const dp2 = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));
```

---

### 1D DP Problems

#### 1. Fibonacci / Climbing Stairs

**Problem:** Number of ways to climb `n` stairs taking 1 or 2 steps.
**State:** `dp[i]` = ways to reach step `i`.
**Transition:** `dp[i] = dp[i-1] + dp[i-2]`

```javascript
// O(N) Space
function climbStairs(n) {
    if (n <= 2) return n;
    const dp = new Array(n + 1).fill(0);
    dp[1] = 1;
    dp[2] = 2;
    for (let i = 3; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    return dp[n];
}

// O(1) Space Optimization
function climbStairsOpt(n) {
    if (n <= 2) return n;
    let prev2 = 1, prev1 = 2;
    for (let i = 3; i <= n; i++) {
        [prev2, prev1] = [prev1, prev1 + prev2];
    }
    return prev1;
}
```

#### 2. House Robber

**Problem:** Max money you can rob without triggering adjacent alarms.
**State:** `dp[i]` = max money robbing up to house `i`.

```javascript
function rob(nums) {
    if (nums.length === 0) return 0;
    if (nums.length === 1) return nums[0];
    
    let prev2 = 0; // dp[i-2]
    let prev1 = 0; // dp[i-1]
    
    for (const num of nums) {
        // max(rob current + prev2, skip current and keep prev1)
        [prev2, prev1] = [prev1, Math.max(prev1, prev2 + num)];
    }
    return prev1;
}
```

#### 3. Kadane's Algorithm (Max Subarray Sum)

```javascript
function maxSubArray(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}
```

---

### 2D DP Problems

#### 4. Unique Paths

**Problem:** Ways to reach bottom-right from top-left in a grid.

```javascript
function uniquePaths(m, n) {
    const dp = Array.from({length: m}, () => new Array(n).fill(1));
    
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            dp[i][j] = dp[i-1][j] + dp[i][j-1];
        }
    }
    return dp[m-1][n-1];
}
```

---

### The Knapsack Family

The 0/1 Knapsack problem forms the basis for many DP problems (Subset Sum, Partition Equal Subset, Target Sum).

#### 5. 0/1 Knapsack

**Problem:** Given weights and values, find max value for a given capacity.

```javascript
// 2D Approach: Time O(N * W), Space O(N * W)
function knapsack01(weights, values, capacity) {
    const n = weights.length;
    const dp = Array.from({length: n + 1}, () => new Array(capacity + 1).fill(0));
    
    for (let i = 1; i <= n; i++) {
        for (let w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i-1][w]; // Exclude
            if (weights[i-1] <= w) {
                // Include vs Exclude
                dp[i][w] = Math.max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1]);
            }
        }
    }
    return dp[n][capacity];
}

// 1D Optimized Approach: Space O(W)
function knapsack01Opt(weights, values, capacity) {
    const dp = new Array(capacity + 1).fill(0);
    
    for (let i = 0; i < weights.length; i++) {
        // Crucial: Iterate backwards to prevent reusing the same item in the same step
        for (let w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}
```

#### 6. Unbounded Knapsack (Coin Change)

In unbounded knapsack, we iterate forwards so items can be reused.

```javascript
function coinChange(coins, amount) {
    const dp = new Array(amount + 1).fill(Infinity);
    dp[0] = 0;
    
    for (const coin of coins) {
        for (let w = coin; w <= amount; w++) { // Forwards!
            dp[w] = Math.min(dp[w], dp[w - coin] + 1);
        }
    }
    return dp[amount] === Infinity ? -1 : dp[amount];
}
```

---

### String DP Problems

#### 7. Longest Common Subsequence (LCS)

```javascript
function lcs(s1, s2) {
    const m = s1.length;
    const n = s2.length;
    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));
    
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i-1] === s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    return dp[m][n];
}
```

#### 8. Edit Distance

```javascript
function minDistance(word1, word2) {
    const m = word1.length;
    const n = word2.length;
    
    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));
    
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (word1[i-1] === word2[j-1]) {
                dp[i][j] = dp[i-1][j-1]; // characters match
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i-1][j],    // Delete
                    dp[i][j-1],    // Insert
                    dp[i-1][j-1]   // Replace
                );
            }
        }
    }
    return dp[m][n];
}
```

---

### Advanced DP Concepts

#### 9. Longest Increasing Subsequence (LIS)

**O(N²) DP Approach:**
```javascript
function lengthOfLIS_DP(nums) {
    const dp = new Array(nums.length).fill(1);
    let max = 1;
    
    for(let i=1; i<nums.length; i++){
        for(let j=0; j<i; j++){
            if(nums[i] > nums[j]){
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        max = Math.max(max, dp[i]);
    }
    return max;
}
```

**O(N log N) Binary Search (Patience Sorting):**
```javascript
function lengthOfLIS(nums) {
    const tails = [];
    
    for (const num of nums) {
        let lo = 0, hi = tails.length;
        while (lo < hi) {
            const mid = (lo + hi) >> 1;
            if (tails[mid] < num) lo = mid + 1;
            else hi = mid;
        }
        
        tails[lo] = num; // Replace or extend
    }
    return tails.length;
}
```

#### 10. Bitmask DP (Traveling Salesperson Problem - TSP)

Used when `N` is very small (e.g., `N <= 20`). We use an integer to represent a set of visited nodes (e.g., `5` is binary `101`, meaning nodes 0 and 2 are visited).

```javascript
/**
 * TSP / Shortest Path Visiting All Nodes
 * Time Complexity: O(N^2 * 2^N)
 */
function shortestPathAllNodes(graph) {
    const n = graph.length;
    // dp[mask][i] = min cost to visit nodes in mask, ending at i
    const dp = Array.from({length: 1 << n}, () => new Array(n).fill(Infinity));
    
    // Example: Start from node 0
    dp[1][0] = 0; // mask 1 (binary 0..01), ending at 0
    
    for (let mask = 1; mask < (1 << n); mask++) {
        for (let u = 0; u < n; u++) {
            if (!(mask & (1 << u))) continue; // If u is not in mask, skip
            
            for (let v = 0; v < n; v++) {
                if (mask & (1 << v)) continue; // If v is already in mask, skip
                
                const newMask = mask | (1 << v);
                // dist[u][v] represents distance from u to v
                // dp[newMask][v] = Math.min(dp[newMask][v], dp[mask][u] + dist[u][v]);
            }
        }
    }
    // Answer is min over all dp[(1<<n)-1][i]
}
```

---

## Practice Problems

**Greedy:**
1.  **Assign Cookies** (Easy)
2.  **Lemonade Change** (Easy)
3.  **Jump Game I & II** (Medium)
4.  **Gas Station** (Medium)
5.  **Task Scheduler** (Medium)
6.  **Minimum Number of Arrows to Burst Balloons** (Medium)

**Dynamic Programming:**
7.  **Climbing Stairs** (Easy)
8.  **Min Cost Climbing Stairs** (Easy)
9.  **House Robber I & II** (Medium)
10. **Coin Change** (Medium)
11. **Partition Equal Subset Sum** (Medium)
12. **Target Sum** (Medium)
13. **Longest Common Subsequence** (Medium)
14. **Edit Distance** (Hard)
15. **Word Break** (Medium)
16. **Longest Increasing Subsequence** (Medium)
17. **Maximum Product Subarray** (Medium)
18. **Burst Balloons** (Hard) - Interval DP
19. **Regular Expression Matching** (Hard)
20. **Distinct Subsequences** (Hard)

Enjoy mastering DP and Greedy patterns!
