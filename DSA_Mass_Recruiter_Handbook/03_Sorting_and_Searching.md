# Sorting & Searching — Q56 to Q65

> **Target companies:** TCS, Wipro, Cognizant, Infosys  
> **Difficulty:** Easy to Medium  
> **Coverage:** ~10% of mass-recruiter questions — knowing HOW to implement these from scratch is expected

---

## Q56. Bubble Sort

**Problem:** Sort an array using the Bubble Sort algorithm.  
**Companies:** TCS, Wipro, HCL, Tech Mahindra  
**Approach:** Repeatedly swap adjacent elements if out of order. Each pass "bubbles" the largest element to the end.

```java
public class BubbleSort {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false; // Optimization: stop early if already sorted
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (!swapped) break; // Array is already sorted
        }
    }

    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        bubbleSort(arr);
        for (int x : arr) System.out.print(x + " "); // 11 12 22 25 34 64 90
    }
}
```
**Time:** O(n²) worst/avg, O(n) best | **Space:** O(1)

---

## Q57. Selection Sort

**Problem:** Sort an array using the Selection Sort algorithm.  
**Companies:** TCS, Wipro  
**Approach:** Find the minimum in unsorted part and swap it to the front.

```java
public class SelectionSort {
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++)
                if (arr[j] < arr[minIdx]) minIdx = j;
            // Swap minimum with arr[i]
            int temp = arr[minIdx];
            arr[minIdx] = arr[i];
            arr[i] = temp;
        }
    }

    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11};
        selectionSort(arr);
        for (int x : arr) System.out.print(x + " "); // 11 12 22 25 64
    }
}
```
**Time:** O(n²) | **Space:** O(1)

---

## Q58. Insertion Sort

**Problem:** Sort an array using the Insertion Sort algorithm.  
**Companies:** TCS, Wipro  
**Approach:** Build the sorted array one element at a time — pick the next unsorted element and insert it at the correct position in the sorted part.

```java
public class InsertionSort {
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    public static void main(String[] args) {
        int[] arr = {5, 4, 3, 2, 1};
        insertionSort(arr);
        for (int x : arr) System.out.print(x + " "); // 1 2 3 4 5
    }
}
```
**Time:** O(n²) worst/avg, O(n) best | **Space:** O(1)

---

## Q59. Merge Sort

**Problem:** Sort an array using Merge Sort (Divide and Conquer).  
**Companies:** TCS Digital, Infosys SP, Cognizant GenC Next  
**Approach:** Divide array into halves, sort each, merge back.

```java
public class MergeSort {
    public static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int mid = l + (r - l) / 2;
            mergeSort(arr, l, mid);
            mergeSort(arr, mid + 1, r);
            merge(arr, l, mid, r);
        }
    }

    static void merge(int[] arr, int l, int mid, int r) {
        int n1 = mid - l + 1, n2 = r - mid;
        int[] left = new int[n1], right = new int[n2];
        System.arraycopy(arr, l, left, 0, n1);
        System.arraycopy(arr, mid + 1, right, 0, n2);
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2)
            arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
        while (i < n1) arr[k++] = left[i++];
        while (j < n2) arr[k++] = right[j++];
    }

    public static void main(String[] args) {
        int[] arr = {38, 27, 43, 3, 9, 82, 10};
        mergeSort(arr, 0, arr.length - 1);
        for (int x : arr) System.out.print(x + " "); // 3 9 10 27 38 43 82
    }
}
```
**Time:** O(n log n) | **Space:** O(n)

---

## Q60. Quick Sort

**Problem:** Sort an array using Quick Sort (partition-based Divide and Conquer).  
**Companies:** TCS Digital, Infosys SP, Wipro Elite  
**Approach:** Pick a pivot, place all smaller elements before it and larger after it (partition). Recursively sort both halves.

```java
public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    static int partition(int[] arr, int low, int high) {
        int pivot = arr[high]; // Last element as pivot
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
            }
        }
        int temp = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = temp;
        return i + 1;
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        quickSort(arr, 0, arr.length - 1);
        for (int x : arr) System.out.print(x + " "); // 1 5 7 8 9 10
    }
}
```
**Time:** O(n log n) avg, O(n²) worst | **Space:** O(log n) stack space

---

## Q61. Binary Search (Iterative)

**Problem:** Search for a target element in a sorted array and return its index.  
**Companies:** TCS, Wipro, Cognizant, Accenture (all companies!)  
**Approach:** Halve the search space at each step — compare target with middle element.

```java
public class BinarySearchIterative {
    public static int binarySearch(int[] arr, int target) {
        int low = 0, high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2; // Avoid overflow
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1; // Not found
    }

    public static void main(String[] args) {
        int[] arr = {2, 4, 6, 8, 10, 12};
        System.out.println(binarySearch(arr, 8));  // 3
        System.out.println(binarySearch(arr, 7));  // -1
    }
}
```
**Time:** O(log n) | **Space:** O(1)

---

## Q62. Binary Search (Recursive)

**Problem:** Same as Q61 but implemented recursively.  
**Companies:** TCS, Cognizant  

```java
public class BinarySearchRecursive {
    public static int binarySearch(int[] arr, int low, int high, int target) {
        if (low > high) return -1;
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) return binarySearch(arr, mid + 1, high, target);
        return binarySearch(arr, low, mid - 1, target);
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11};
        System.out.println(binarySearch(arr, 0, arr.length - 1, 7)); // 3
    }
}
```
**Time:** O(log n) | **Space:** O(log n) — recursive stack

---

## Q63. Search in a Rotated Sorted Array

**Problem:** A sorted array has been rotated at some unknown pivot. Search for a target.  
**Companies:** TCS Digital, Infosys SP, Cognizant GenC Next  
**Approach:** Modified binary search — determine which half is sorted at each step.

```java
public class SearchRotatedArray {
    public static int search(int[] arr, int target) {
        int low = 0, high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            // Left half is sorted
            if (arr[low] <= arr[mid]) {
                if (target >= arr[low] && target < arr[mid]) high = mid - 1;
                else low = mid + 1;
            } else { // Right half is sorted
                if (target > arr[mid] && target <= arr[high]) low = mid + 1;
                else high = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] arr = {4, 5, 6, 7, 0, 1, 2};
        System.out.println(search(arr, 0)); // 4
        System.out.println(search(arr, 3)); // -1
    }
}
```
**Time:** O(log n) | **Space:** O(1)

---

## Q64. Find the Peak Element in an Array

**Problem:** A peak element is greater than its neighbors. Find any one peak element's index.  
**Companies:** Infosys, Accenture  
**Approach:** Binary search — move toward the side with a larger neighbor.

```java
public class PeakElement {
    public static int findPeak(int[] arr) {
        int low = 0, high = arr.length - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > arr[mid + 1]) high = mid;
            else low = mid + 1;
        }
        return low; // Index of peak
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 1};
        System.out.println("Peak index: " + findPeak(arr)); // 2 (value: 3)
    }
}
```
**Time:** O(log n) | **Space:** O(1)

---

## Q65. Find the Floor and Ceiling of a Value in a Sorted Array

**Problem:** Find the floor (largest element ≤ target) and ceiling (smallest element ≥ target) in a sorted array.  
**Companies:** TCS, Infosys  

```java
public class FloorCeiling {
    public static int floor(int[] arr, int target) {
        int low = 0, high = arr.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] <= target) { result = arr[mid]; low = mid + 1; }
            else high = mid - 1;
        }
        return result;
    }

    public static int ceiling(int[] arr, int target) {
        int low = 0, high = arr.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) { result = arr[mid]; high = mid - 1; }
            else low = mid + 1;
        }
        return result;
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 8, 10, 10, 12, 19};
        System.out.println("Floor of 5: " + floor(arr, 5));   // 2
        System.out.println("Ceiling of 5: " + ceiling(arr, 5)); // 8
    }
}
```
**Time:** O(log n) | **Space:** O(1)

---

*Next: [04_Linked_Lists_Stacks_Queues.md](./04_Linked_Lists_Stacks_Queues.md)*
