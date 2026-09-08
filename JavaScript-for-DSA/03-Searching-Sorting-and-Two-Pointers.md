# Searching, Sorting, and Two Pointers in JavaScript

Welcome to the comprehensive guide on Searching, Sorting, and Two Pointers algorithms in JavaScript, designed specifically for developers transitioning from Java. As a Java developer, you already possess a strong foundation in Data Structures and Algorithms (DSA). This guide will bridge the gap by highlighting JavaScript-specific nuances, particularly when dealing with sorting, and providing robust templates for competitive programming and technical interviews.

---

## 1. JavaScript's Dangerous Default Sort

Before diving into complex algorithms, it is absolutely critical to understand how JavaScript handles sorting natively. If you carry over your Java intuition without adjusting for JavaScript's behavior, you will encounter silent bugs that are notoriously difficult to track down.

### The Pitfall: Sorting Numbers

In Java, calling `Arrays.sort(arr)` on an array of integers sorts them numerically in ascending order. 

```java
// Java
int[] arr = {10, 2, 5, 1};
Arrays.sort(arr);
// arr is now [1, 2, 5, 10]
```

In JavaScript, calling `sort()` on an array of numbers does **not** sort them numerically by default.

```javascript
// WRONG for numbers in JavaScript:
[10, 2, 5, 1].sort()  // → [1, 10, 2, 5] — sorts as STRINGS!
```

**Why does this happen?**
By default, the `Array.prototype.sort()` method in JavaScript converts all elements to strings and compares them lexicographically (alphabetically) based on their UTF-16 code unit values. 
Because the string `"10"` comes before the string `"2"`, `10` is placed before `2` in the sorted array.

### The Solution: Custom Comparators

To sort numbers correctly in JavaScript, you must provide a comparator function. The comparator takes two arguments, `a` and `b`, and should return:
- A negative number if `a` should come before `b`.
- A positive number if `a` should come after `b`.
- Zero if they are equal.

```javascript
// CORRECT for numbers:
[10, 2, 5, 1].sort((a, b) => a - b)  // → [1, 2, 5, 10] ascending
[10, 2, 5, 1].sort((a, b) => b - a)  // → [10, 5, 2, 1] descending
```

### Custom Comparators for DSA Problems

When dealing with complex data structures like arrays of pairs or objects, comparators become essential.

```javascript
// Sort by second element of pairs (e.g., Intervals)
pairs.sort((a, b) => a[1] - b[1]);

// Sort objects by property
people.sort((a, b) => a.age - b.age);

// Sort intervals by start time
intervals.sort((a, b) => a[0] - b[0]);

// Stable sort note: JavaScript sort is stable since ES2019
// Java: Arrays.sort is stable for objects, not guaranteed for primitives
```

---

## 2. Sorting Algorithms

While you will primarily use the built-in `sort()` method, implementing sorting algorithms from scratch is a common interview requirement and builds foundational DSA skills.

### Bubble Sort
Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.

**Java vs. JavaScript Note:** 
In Java, swapping requires a temporary variable. In JavaScript, you can use array destructuring for a concise one-liner swap: `[a, b] = [b, a]`.

```javascript
/**
 * Bubble Sort Implementation
 * Time Complexity: O(n^2) worst/average, O(n) best (if already sorted and optimized)
 * Space Complexity: O(1)
 */
function bubbleSort(arr) {
    const n = arr.length;
    for(let i = 0; i < n-1; i++) {
        for(let j = 0; j < n-i-1; j++) {
            if(arr[j] > arr[j+1]) {
                [arr[j], arr[j+1]] = [arr[j+1], arr[j]]; // JS swap
            }
        }
    }
}
```

### Selection Sort
Selection sort divides the input list into two parts: a sorted sublist and an unsorted sublist. It repeatedly selects the smallest element from the unsorted sublist and moves it to the end of the sorted sublist.

```javascript
/**
 * Selection Sort Implementation
 * Time Complexity: O(n^2) in all cases
 * Space Complexity: O(1)
 */
function selectionSort(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        let minIndex = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex !== i) {
            [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]]; // Swap
        }
    }
}
```

### Insertion Sort
Insertion sort builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms like quicksort or mergesort, but provides O(n) best-case performance for nearly sorted data.

```javascript
/**
 * Insertion Sort Implementation
 * Time Complexity: O(n^2) worst/average, O(n) best
 * Space Complexity: O(1)
 */
function insertionSort(arr) {
    const n = arr.length;
    for (let i = 1; i < n; i++) {
        let key = arr[i];
        let j = i - 1;
        // Move elements of arr[0..i-1], that are greater than key,
        // to one position ahead of their current position
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
```

### Merge Sort
Merge sort is a divide-and-conquer algorithm that divides the array into halves, recursively sorts them, and then merges the sorted halves.

```javascript
/**
 * Merge Sort Implementation
 * Time Complexity: O(n log n) in all cases
 * Space Complexity: O(n) due to auxiliary arrays in merge and call stack
 */
function mergeSort(arr) {
    if(arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    return merge(left, right);
}

function merge(left, right) {
    const result = [];
    let i = 0, j = 0;
    while(i < left.length && j < right.length) {
        if(left[i] <= right[j]) result.push(left[i++]);
        else result.push(right[j++]);
    }
    return [...result, ...left.slice(i), ...right.slice(j)];
}
```

### Quick Sort
Quick sort is another divide-and-conquer algorithm. It picks an element as a pivot and partitions the given array around the picked pivot.

```javascript
/**
 * Quick Sort Implementation
 * Time Complexity: O(n log n) average, O(n^2) worst case
 * Space Complexity: O(log n) average for recursion stack
 */
function quickSort(arr, low = 0, high = arr.length - 1) {
    if(low < high) {
        const pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

function partition(arr, low, high) {
    const pivot = arr[high];
    let i = low - 1;
    for(let j = low; j < high; j++) {
        if(arr[j] <= pivot) {
            i++;
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    [arr[i+1], arr[high]] = [arr[high], arr[i+1]];
    return i + 1;
}
```

### Counting Sort
Time Complexity: O(n+k)
Space Complexity: O(k)
Non-comparison-based sorting algorithm that sorts integers by counting the number of objects having distinct key values.

### Radix Sort
Time Complexity: O(d*(n+k))
Space Complexity: O(n+k)
Processes digits individually, from least significant to most significant.

### When to use built-in `sort()`: 
For most interview problems, sorting is a sub-step. Just use `arr.sort((a,b) => a - b)` for O(n log n) performance.

---

## 3. Searching Algorithms

### Linear Search
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)

```javascript
function linearSearch(arr, target) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === target) return i;
    }
    return -1;
}
```

### Binary Search

Binary search works on **sorted** arrays.

**Important Note on Overflow:**
`Math.floor((left + right) / 2)` can overflow in Java. While this isn't practically an issue in JavaScript due to double-precision floats, using the safe form `left + Math.floor((right - left) / 2)` is excellent practice.

```javascript
function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while(left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        if(arr[mid] === target) return mid;
        else if(arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

**Recursive Binary Search:**
```javascript
function binarySearchRecursive(arr, target, left = 0, right = arr.length - 1) {
    if (left > right) return -1;
    const mid = left + Math.floor((right - left) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) return binarySearchRecursive(arr, target, mid + 1, right);
    return binarySearchRecursive(arr, target, left, mid - 1);
}
```

**Binary search on answer template:**
```javascript
// Binary search on answer template
function binarySearchOnAnswer(lo, hi, check) {
    while(lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if(check(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

Templates for:
- First occurrence (lower bound)
- Last occurrence (upper bound)
- First true in boolean array
- Search in rotated sorted array

---

## 4. Two Pointers

### Opposite Direction

```javascript
// Two sum in sorted array
function twoSum(arr, target) {
    let left = 0, right = arr.length - 1;
    while(left < right) {
        const sum = arr[left] + arr[right];
        if(sum === target) return [left, right];
        else if(sum < target) left++;
        else right--;
    }
    return [-1, -1];
}
```

### Same Direction (Fast/Slow)

```javascript
// Remove duplicates from sorted array
function removeDuplicates(arr) {
    let slow = 0;
    for(let fast = 1; fast < arr.length; fast++) {
        if(arr[fast] !== arr[slow]) {
            arr[++slow] = arr[fast];
        }
    }
    return slow + 1;
}
```

Problems: palindrome check, container with most water, 3Sum, remove element, partition

---

## 5. Sliding Window

### Fixed Window

```javascript
function maxSumSubarrayK(arr, k) {
    let windowSum = arr.slice(0, k).reduce((a,b) => a+b, 0);
    let maxSum = windowSum;
    for(let i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i-k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

### Variable Window

```javascript
// Longest substring without repeating characters
function lengthOfLongestSubstring(s) {
    const seen = new Map();
    let left = 0, maxLen = 0;
    for(let right = 0; right < s.length; right++) {
        if(seen.has(s[right]) && seen.get(s[right]) >= left) {
            left = seen.get(s[right]) + 1;
        }
        seen.set(s[right], right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

Templates for: min window substring, fruits in basket, all anagrams in string

---

## 6. Prefix Sum

```javascript
// Build prefix sum
const prefix = new Array(n+1).fill(0);
for(let i = 0; i < n; i++) prefix[i+1] = prefix[i] + arr[i];

// Range sum query O(1)
function rangeSum(l, r) { return prefix[r+1] - prefix[l]; }

// Prefix sum + Map: subarray sum equals k
function subarraySum(nums, k) {
    const map = new Map([[0, 1]]);
    let count = 0, prefixSum = 0;
    for(const num of nums) {
        prefixSum += num;
        count += (map.get(prefixSum - k) || 0);
        map.set(prefixSum, (map.get(prefixSum) || 0) + 1);
    }
    return count;
}
```

2D prefix sum template.

---

## 7. Dutch National Flag / 0-1-2 sort

```javascript
function sort012(arr) {
    let low = 0, mid = 0, high = arr.length - 1;
    while(mid <= high) {
        if(arr[mid] === 0) [arr[low++], arr[mid++]] = [arr[mid], arr[low]];
        else if(arr[mid] === 1) mid++;
        else [arr[mid], arr[high--]] = [arr[high], arr[mid]];
    }
}
```

---

## 8. Practice Problems List (15 problems)

**Sorting & Searching:**
1. Sort Colors (LeetCode 75)
2. Search in Rotated Sorted Array (LeetCode 33)
3. Find First and Last Position of Element in Sorted Array (LeetCode 34)
4. Merge Intervals (LeetCode 56)
5. Koko Eating Bananas (LeetCode 875)

**Two Pointers:**
6. Two Sum II (LeetCode 167)
7. Container With Most Water (LeetCode 11)
8. 3Sum (LeetCode 15)
9. Valid Palindrome (LeetCode 125)
10. Remove Duplicates from Sorted Array (LeetCode 26)

**Sliding Window & Prefix Sum:**
11. Longest Substring Without Repeating Characters (LeetCode 3)
12. Minimum Size Subarray Sum (LeetCode 209)
13. Subarray Sum Equals K (LeetCode 560)
14. Permutation in String (LeetCode 567)
15. Range Sum Query 2D - Immutable (LeetCode 304)
