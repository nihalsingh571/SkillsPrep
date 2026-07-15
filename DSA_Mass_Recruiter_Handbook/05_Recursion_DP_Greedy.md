# Recursion, DP & Greedy — Q81 to Q90

> **Target companies:** TCS Digital/Prime, Infosys SP/DSE, Wipro Elite, Cognizant GenC Next  
> **Difficulty:** Medium to Hard  
> **Coverage:** ~15–20% of premium track questions

---

## Q81. Fibonacci Sequence (Three Approaches)

**Problem:** Find the nth Fibonacci number (F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)).  
**Companies:** TCS, Wipro, Accenture, HCL  
**Note:** Show all three approaches in the interview to demonstrate depth.

```java
public class Fibonacci {
    // 1. Naive Recursion — O(2^n) time, O(n) space
    public static int fibRecursive(int n) {
        if (n <= 1) return n;
        return fibRecursive(n - 1) + fibRecursive(n - 2);
    }

    // 2. Memoization (Top-Down DP) — O(n) time, O(n) space
    static int[] memo = new int[100];
    public static int fibMemo(int n) {
        if (n <= 1) return n;
        if (memo[n] != 0) return memo[n];
        return memo[n] = fibMemo(n - 1) + fibMemo(n - 2);
    }

    // 3. Iterative (Bottom-Up DP) — O(n) time, O(1) space (BEST!)
    public static int fibIterative(int n) {
        if (n <= 1) return n;
        int prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    public static void main(String[] args) {
        System.out.println(fibRecursive(10));  // 55
        System.out.println(fibMemo(10));       // 55
        System.out.println(fibIterative(10));  // 55
    }
}
```

---

## Q82. Factorial of a Number (Recursive & Iterative)

**Problem:** Compute n! (factorial of n).  
**Companies:** TCS, Wipro, HCL, Tech Mahindra  

```java
public class Factorial {
    // Recursive
    public static long factRecursive(int n) {
        if (n == 0 || n == 1) return 1;
        return n * factRecursive(n - 1);
    }

    // Iterative
    public static long factIterative(int n) {
        long result = 1;
        for (int i = 2; i <= n; i++) result *= i;
        return result;
    }

    public static void main(String[] args) {
        System.out.println(factRecursive(10)); // 3628800
        System.out.println(factIterative(10)); // 3628800
    }
}
```

---

## Q83. 0/1 Knapsack Problem

**Problem:** Given weights and values of n items and a bag of capacity W, maximize the total value without exceeding weight limit.  
**Companies:** TCS Digital, Infosys SP, Wipro Elite  
**Approach:** Bottom-up DP table where `dp[i][w]` = max value using first i items with capacity w.

```java
public class Knapsack {
    public static int knapsack(int[] weights, int[] values, int capacity, int n) {
        int[][] dp = new int[n + 1][capacity + 1];
        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= capacity; w++) {
                // Don't include item i
                dp[i][w] = dp[i - 1][w];
                // Include item i (if it fits)
                if (weights[i - 1] <= w)
                    dp[i][w] = Math.max(dp[i][w],
                        dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
        return dp[n][capacity];
    }

    public static void main(String[] args) {
        int[] values  = {60, 100, 120};
        int[] weights = {10, 20, 30};
        int capacity = 50, n = 3;
        System.out.println(knapsack(weights, values, capacity, n)); // 220
    }
}
```
**Time:** O(n * W) | **Space:** O(n * W)

---

## Q84. Longest Common Subsequence (LCS)

**Problem:** Find the length of the longest subsequence present in both strings.  
**Companies:** TCS Digital, Infosys SP/DSE  
**Note:** A subsequence maintains order but not contiguity.

```java
public class LCS {
    public static int lcs(String s1, String s2) {
        int m = s1.length(), n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1))
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                else
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }

    public static void main(String[] args) {
        System.out.println(lcs("AGGTAB", "GXTXAYB")); // 4 (GTAB)
        System.out.println(lcs("ABCBDAB", "BDCABA")); // 4 (BCBA)
    }
}
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Q85. Subset Sum Problem

**Problem:** Given a set of non-negative integers and a target sum, determine if any subset adds up to the target.  
**Companies:** Infosys SP, TCS Digital  

```java
public class SubsetSum {
    public static boolean canAchieve(int[] arr, int target) {
        int n = arr.length;
        boolean[][] dp = new boolean[n + 1][target + 1];
        // Sum = 0 is always achievable (empty subset)
        for (int i = 0; i <= n; i++) dp[i][0] = true;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s <= target; s++) {
                dp[i][s] = dp[i - 1][s]; // Don't include arr[i-1]
                if (arr[i - 1] <= s)
                    dp[i][s] = dp[i][s] || dp[i - 1][s - arr[i - 1]];
            }
        }
        return dp[n][target];
    }

    public static void main(String[] args) {
        System.out.println(canAchieve(new int[]{3, 34, 4, 12, 5, 2}, 9)); // true (4+5)
        System.out.println(canAchieve(new int[]{3, 34, 4, 12, 5, 2}, 30)); // false
    }
}
```
**Time:** O(n * target) | **Space:** O(n * target)

---

## Q86. Coin Change — Minimum Coins

**Problem:** Given coin denominations and a target amount, find the minimum number of coins needed.  
**Companies:** Accenture, Infosys SP, TCS Digital  

```java
import java.util.Arrays;

public class CoinChangeMin {
    public static int minCoins(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1); // Initialize to "infinity"
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i)
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        System.out.println(minCoins(new int[]{1, 5, 6, 9}, 11)); // 2 (5+6)
        System.out.println(minCoins(new int[]{2}, 3));           // -1
    }
}
```
**Time:** O(amount * coins) | **Space:** O(amount)

---

## Q87. Coin Change — Number of Ways

**Problem:** Find the total number of ways to make the target amount using given coin denominations.  
**Companies:** TCS Digital, Infosys  

```java
public class CoinChangeWays {
    public static int countWays(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        dp[0] = 1; // One way to make 0 — use no coins
        for (int coin : coins)
            for (int i = coin; i <= amount; i++)
                dp[i] += dp[i - coin];
        return dp[amount];
    }

    public static void main(String[] args) {
        System.out.println(countWays(new int[]{1, 2, 3}, 4)); // 4 ways
        // Ways: {1,1,1,1}, {1,1,2}, {2,2}, {1,3}
    }
}
```
**Time:** O(amount * coins) | **Space:** O(amount)

---

## Q88. Activity Selection Problem (Greedy)

**Problem:** Given n activities with start and end times, select the maximum number of activities that don't overlap.  
**Companies:** Infosys SP/DSE, Wipro Elite  
**Approach:** Greedy — always pick the activity that finishes earliest.

```java
import java.util.*;

public class ActivitySelection {
    public static int maxActivities(int[] start, int[] end, int n) {
        // Sort by end time
        Integer[] indices = new Integer[n];
        for (int i = 0; i < n; i++) indices[i] = i;
        Arrays.sort(indices, (a, b) -> end[a] - end[b]);

        int count = 1;
        int lastEnd = end[indices[0]]; // First activity always selected

        for (int i = 1; i < n; i++) {
            int idx = indices[i];
            if (start[idx] >= lastEnd) { // Activity doesn't overlap
                count++;
                lastEnd = end[idx];
            }
        }
        return count;
    }

    public static void main(String[] args) {
        int[] start = {1, 3, 0, 5, 8, 5};
        int[] end   = {2, 4, 6, 7, 9, 9};
        System.out.println("Max activities: " + maxActivities(start, end, 6)); // 4
    }
}
```
**Time:** O(n log n) | **Space:** O(n)

---

## Q89. Longest Increasing Subsequence (LIS)

**Problem:** Find the length of the longest strictly increasing subsequence in an array.  
**Companies:** TCS Digital, Infosys SP  

```java
public class LongestIncreasingSubsequence {
    public static int lis(int[] arr) {
        int n = arr.length;
        int[] dp = new int[n];
        java.util.Arrays.fill(dp, 1); // Every element is a subsequence of length 1
        int maxLen = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[j] < arr[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            maxLen = Math.max(maxLen, dp[i]);
        }
        return maxLen;
    }

    public static void main(String[] args) {
        System.out.println(lis(new int[]{10, 9, 2, 5, 3, 7, 101, 18})); // 4 (2,3,7,101)
    }
}
```
**Time:** O(n²) | **Space:** O(n)

---

## Q90. Jump Game (Can You Reach the Last Index?)

**Problem:** Given an array where each element represents max jump length from that position, determine if you can reach the last index.  
**Companies:** Accenture, Infosys  
**Approach:** Greedy — track the farthest reachable index.

```java
public class JumpGame {
    public static boolean canJump(int[] nums) {
        int maxReach = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > maxReach) return false; // Current index unreachable
            maxReach = Math.max(maxReach, i + nums[i]);
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(canJump(new int[]{2, 3, 1, 1, 4})); // true
        System.out.println(canJump(new int[]{3, 2, 1, 0, 4})); // false
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

*Next: [06_Trees_and_Graphs.md](./06_Trees_and_Graphs.md)*
