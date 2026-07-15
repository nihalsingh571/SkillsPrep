# Arrays & Strings — Q1 to Q40

> **Target companies:** TCS, Infosys, Wipro, Cognizant, Accenture, Capgemini, HCL, Tech Mahindra  
> **Difficulty:** Easy to Medium  
> **Coverage:** ~40% of all mass-recruiter coding questions

---

## Q1. Reverse an Array In-Place

**Problem:** Given an integer array, reverse it without using extra space.  
**Companies:** TCS, Wipro, Cognizant, Accenture  
**Approach:** Two-pointer — swap elements from both ends moving inward.

```java
public class ReverseArray {
    public static void reverse(int[] arr) {
        int left = 0, right = arr.length - 1;
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        reverse(arr);
        // Output: 5 4 3 2 1
        for (int x : arr) System.out.print(x + " ");
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q2. Find Second Largest Element

**Problem:** Find the second largest element without sorting the full array.  
**Companies:** TCS, Cognizant, Wipro  
**Approach:** Single pass tracking largest and second largest.

```java
public class SecondLargest {
    public static int find(int[] arr) {
        int first = Integer.MIN_VALUE, second = Integer.MIN_VALUE;
        for (int x : arr) {
            if (x > first) {
                second = first;
                first = x;
            } else if (x > second && x != first) {
                second = x;
            }
        }
        return second;
    }

    public static void main(String[] args) {
        int[] arr = {12, 35, 1, 10, 34, 1};
        System.out.println("Second Largest: " + find(arr)); // 34
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q3. Move All Zeros to End (Preserve Order)

**Problem:** Move all 0s to the end of the array while preserving the order of non-zero elements.  
**Companies:** TCS (most frequent), Wipro  
**Approach:** Two-pointer — write position tracks next non-zero slot.

```java
public class MoveZeros {
    public static void moveZeros(int[] arr) {
        int writePos = 0;
        for (int x : arr) {
            if (x != 0) arr[writePos++] = x;
        }
        while (writePos < arr.length) arr[writePos++] = 0;
    }

    public static void main(String[] args) {
        int[] arr = {1, 0, 3, 0, 5, 2};
        moveZeros(arr);
        // Output: 1 3 5 2 0 0
        for (int x : arr) System.out.print(x + " ");
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q4. Find Duplicate Elements in an Array

**Problem:** Print all duplicate values in an array.  
**Companies:** TCS, Wipro, HCL  
**Approach:** Use a HashSet — add each element; if already present, it's a duplicate.

```java
import java.util.*;

public class FindDuplicates {
    public static void findDuplicates(int[] arr) {
        Set<Integer> seen = new HashSet<>();
        Set<Integer> duplicates = new HashSet<>();
        for (int x : arr) {
            if (!seen.add(x)) duplicates.add(x);
        }
        System.out.println("Duplicates: " + duplicates);
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 4, 2, 2, 3, 5};
        findDuplicates(arr); // Duplicates: [2, 3]
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q5. Count Even and Odd Numbers

**Problem:** Count the number of even and odd numbers in an array.  
**Companies:** TCS, HCL, Tech Mahindra  
**Approach:** Simple modulo check per element.

```java
public class EvenOddCount {
    public static void count(int[] arr) {
        int even = 0, odd = 0;
        for (int x : arr) {
            if (x % 2 == 0) even++;
            else odd++;
        }
        System.out.println("Even: " + even + ", Odd: " + odd);
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5, 6};
        count(arr); // Even: 3, Odd: 3
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q6. Maximum Subarray Sum (Kadane's Algorithm)

**Problem:** Find the contiguous subarray with the maximum sum.  
**Companies:** Accenture, Infosys, Cognizant  
**Approach:** Kadane's algorithm — extend or restart the subarray at each element.

```java
public class MaxSubarraySum {
    public static int maxSum(int[] arr) {
        int maxSoFar = arr[0], currentMax = arr[0];
        for (int i = 1; i < arr.length; i++) {
            currentMax = Math.max(arr[i], currentMax + arr[i]);
            maxSoFar = Math.max(maxSoFar, currentMax);
        }
        return maxSoFar;
    }

    public static void main(String[] args) {
        int[] arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Max Subarray Sum: " + maxSum(arr)); // 6
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q7. Rotate Array by K Positions

**Problem:** Rotate an array to the right by k positions.  
**Companies:** TCS, Cognizant  
**Approach:** Reverse the whole array, then reverse the first k and the remaining n-k elements.

```java
public class RotateArray {
    static void reverse(int[] arr, int l, int r) {
        while (l < r) {
            int t = arr[l]; arr[l++] = arr[r]; arr[r--] = t;
        }
    }

    public static void rotate(int[] arr, int k) {
        int n = arr.length;
        k %= n;
        reverse(arr, 0, n - 1);
        reverse(arr, 0, k - 1);
        reverse(arr, k, n - 1);
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        rotate(arr, 2);
        // Output: 4 5 1 2 3
        for (int x : arr) System.out.print(x + " ");
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q8. Find Missing Number in Range 1 to N

**Problem:** An array of size n-1 contains distinct numbers from 1 to n. Find the missing number.  
**Companies:** TCS, Wipro, Accenture  
**Approach:** Expected sum = n*(n+1)/2. Missing = Expected - Actual sum.

```java
public class MissingNumber {
    public static int find(int[] arr, int n) {
        int expected = n * (n + 1) / 2;
        int actual = 0;
        for (int x : arr) actual += x;
        return expected - actual;
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 4, 5, 6};
        System.out.println("Missing: " + find(arr, 6)); // 3
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q9. Two Sum — Find Pair with Given Sum

**Problem:** Find two elements in an array that add up to a target sum.  
**Companies:** Accenture, Infosys, Cognizant  
**Approach:** HashMap to store complements.

```java
import java.util.*;

public class TwoSum {
    public static int[] twoSum(int[] arr, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < arr.length; i++) {
            int complement = target - arr[i];
            if (map.containsKey(complement))
                return new int[]{map.get(complement), i};
            map.put(arr[i], i);
        }
        return new int[]{-1, -1};
    }

    public static void main(String[] args) {
        int[] arr = {2, 7, 11, 15};
        int[] result = twoSum(arr, 9);
        System.out.println("Indices: " + result[0] + ", " + result[1]); // 0, 1
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q10. Matrix Row-Sum — Find Row with Maximum Sum

**Problem:** Given a 2D matrix, print the sum of each row and identify the row with the maximum sum.  
**Companies:** TCS, Wipro  
**Approach:** Iterate over each row and compute sum.

```java
public class MatrixRowSum {
    public static void findMaxRow(int[][] matrix) {
        int maxSum = Integer.MIN_VALUE, maxRow = 0;
        for (int i = 0; i < matrix.length; i++) {
            int sum = 0;
            for (int val : matrix[i]) sum += val;
            System.out.println("Row " + i + " sum: " + sum);
            if (sum > maxSum) { maxSum = sum; maxRow = i; }
        }
        System.out.println("Max row: " + maxRow + " with sum: " + maxSum);
    }

    public static void main(String[] args) {
        int[][] matrix = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        findMaxRow(matrix);
    }
}
```
**Time:** O(m*n) | **Space:** O(1)

---

## Q11. Merge Two Sorted Arrays

**Problem:** Merge two sorted arrays into a single sorted array.  
**Companies:** Infosys, Cognizant, TCS  
**Approach:** Two-pointer merge (merge step of merge sort).

```java
public class MergeSortedArrays {
    public static int[] merge(int[] a, int[] b) {
        int[] result = new int[a.length + b.length];
        int i = 0, j = 0, k = 0;
        while (i < a.length && j < b.length)
            result[k++] = (a[i] <= b[j]) ? a[i++] : b[j++];
        while (i < a.length) result[k++] = a[i++];
        while (j < b.length) result[k++] = b[j++];
        return result;
    }

    public static void main(String[] args) {
        int[] a = {1, 3, 5}, b = {2, 4, 6};
        int[] merged = merge(a, b);
        for (int x : merged) System.out.print(x + " "); // 1 2 3 4 5 6
    }
}
```
**Time:** O(m+n) | **Space:** O(m+n)

---

## Q12. Find Median of Two Sorted Arrays (Easy Approach)

**Problem:** Find the median of two sorted arrays combined.  
**Companies:** Infosys (SP), Cognizant  
**Approach:** Merge both arrays (like Q11), then find middle element(s).

```java
public class MedianTwoArrays {
    public static double findMedian(int[] a, int[] b) {
        int[] merged = new int[a.length + b.length];
        int i = 0, j = 0, k = 0;
        while (i < a.length && j < b.length)
            merged[k++] = (a[i] <= b[j]) ? a[i++] : b[j++];
        while (i < a.length) merged[k++] = a[i++];
        while (j < b.length) merged[k++] = b[j++];
        int n = merged.length;
        return (n % 2 == 0)
            ? (merged[n/2 - 1] + merged[n/2]) / 2.0
            : merged[n/2];
    }

    public static void main(String[] args) {
        int[] a = {1, 3}, b = {2, 4};
        System.out.println("Median: " + findMedian(a, b)); // 2.5
    }
}
```
**Time:** O(m+n) | **Space:** O(m+n)

---

## Q13. Palindrome Check — String

**Problem:** Check whether a given string is a palindrome (ignoring spaces and case).  
**Companies:** TCS, Wipro, Cognizant, HCL  
**Approach:** Two-pointer from both ends.

```java
public class PalindromeCheck {
    public static boolean isPalindrome(String s) {
        s = s.toLowerCase().replaceAll("[^a-z0-9]", "");
        int l = 0, r = s.length() - 1;
        while (l < r) {
            if (s.charAt(l) != s.charAt(r)) return false;
            l++; r--;
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("A man a plan a canal Panama")); // true
        System.out.println(isPalindrome("Hello")); // false
    }
}
```
**Time:** O(n) | **Space:** O(n) for cleaned string

---

## Q14. Reverse a String

**Problem:** Reverse a string without using any built-in reverse function.  
**Companies:** TCS, Wipro, HCL, Tech Mahindra  
**Approach:** Convert to char array, swap from both ends.

```java
public class ReverseString {
    public static String reverse(String s) {
        char[] chars = s.toCharArray();
        int l = 0, r = chars.length - 1;
        while (l < r) {
            char t = chars[l]; chars[l++] = chars[r]; chars[r--] = t;
        }
        return new String(chars);
    }

    public static void main(String[] args) {
        System.out.println(reverse("Hello World")); // dlroW olleH
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q15. Reverse Words in a Sentence

**Problem:** Given a sentence, reverse the order of words (not characters).  
**Companies:** TCS, Wipro  
**Approach:** Split by space, iterate from last to first.

```java
public class ReverseWords {
    public static String reverseWords(String sentence) {
        String[] words = sentence.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i = words.length - 1; i >= 0; i--) {
            sb.append(words[i]);
            if (i > 0) sb.append(" ");
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(reverseWords("Hello World Java")); // Java World Hello
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q16. Count Occurrences of a Character/Word in a String

**Problem:** Count how many times a specific character or word appears in a string.  
**Companies:** TCS, Wipro, HCL  

```java
public class CountOccurrences {
    // Count character occurrences
    public static int countChar(String s, char target) {
        int count = 0;
        for (char c : s.toCharArray()) if (c == target) count++;
        return count;
    }

    // Count word occurrences
    public static int countWord(String s, String word) {
        int count = 0;
        String[] words = s.split("\\s+");
        for (String w : words) if (w.equalsIgnoreCase(word)) count++;
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countChar("hello world", 'l')); // 3
        System.out.println(countWord("to be or not to be", "to")); // 2
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q17. Check if Two Strings are Anagrams

**Problem:** Determine if two strings are anagrams (same characters, different order).  
**Companies:** TCS, Accenture, Infosys  
**Approach:** Sort both strings and compare, OR use a frequency count array.

```java
import java.util.Arrays;

public class AnagramCheck {
    public static boolean isAnagram(String s1, String s2) {
        if (s1.length() != s2.length()) return false;
        int[] freq = new int[26];
        for (char c : s1.toCharArray()) freq[c - 'a']++;
        for (char c : s2.toCharArray()) freq[c - 'a']--;
        for (int f : freq) if (f != 0) return false;
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isAnagram("listen", "silent")); // true
        System.out.println(isAnagram("hello", "world"));   // false
    }
}
```
**Time:** O(n) | **Space:** O(1) (fixed 26-size array)

---

## Q18. Longest Palindromic Substring

**Problem:** Find the longest substring that is a palindrome.  
**Companies:** Infosys, TCS Digital  
**Approach:** Expand Around Center — for each index, expand outward as long as characters match.

```java
public class LongestPalindromicSubstring {
    static int start, maxLen;

    static void expand(String s, int l, int r) {
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
            if (r - l + 1 > maxLen) {
                start = l;
                maxLen = r - l + 1;
            }
            l--; r++;
        }
    }

    public static String longestPalindrome(String s) {
        start = 0; maxLen = 1;
        for (int i = 0; i < s.length(); i++) {
            expand(s, i, i);     // Odd length palindromes
            expand(s, i, i + 1); // Even length palindromes
        }
        return s.substring(start, start + maxLen);
    }

    public static void main(String[] args) {
        System.out.println(longestPalindrome("babad"));  // bab
        System.out.println(longestPalindrome("cbbd"));   // bb
    }
}
```
**Time:** O(n²) | **Space:** O(1)

---

## Q19. Run-Length Encoding (String Compression)

**Problem:** Compress a string so consecutive repeated characters are encoded with their count. e.g., "aaabb" → "a3b2".  
**Companies:** Capgemini (very frequent!)  

```java
public class RunLengthEncoding {
    public static String encode(String s) {
        if (s.isEmpty()) return "";
        StringBuilder sb = new StringBuilder();
        int count = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                count++;
            } else {
                sb.append(s.charAt(i - 1)).append(count);
                count = 1;
            }
        }
        sb.append(s.charAt(s.length() - 1)).append(count);
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(encode("aaabb"));   // a3b2
        System.out.println(encode("abcdddd")); // a1b1c1d4
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q20. Move Special Characters to Front of String

**Problem:** Rearrange a string so all special characters (non-alphabetic) come first, preserving relative order of both groups.  
**Companies:** Capgemini  

```java
public class MoveSpecialChars {
    public static String moveSpecial(String s) {
        StringBuilder special = new StringBuilder();
        StringBuilder letters = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (!Character.isLetterOrDigit(c)) special.append(c);
            else letters.append(c);
        }
        return special.append(letters).toString();
    }

    public static void main(String[] args) {
        System.out.println(moveSpecial("a#b!c@d")); // #!@abcd
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q21. First Non-Repeating Character in a String

**Problem:** Find the first character in a string that does not repeat.  
**Companies:** TCS, Infosys, Accenture  
**Approach:** LinkedHashMap preserves insertion order while tracking frequency.

```java
import java.util.*;

public class FirstNonRepeating {
    public static char firstUnique(String s) {
        Map<Character, Integer> freq = new LinkedHashMap<>();
        for (char c : s.toCharArray())
            freq.put(c, freq.getOrDefault(c, 0) + 1);
        for (Map.Entry<Character, Integer> e : freq.entrySet())
            if (e.getValue() == 1) return e.getKey();
        return '\0'; // No unique character
    }

    public static void main(String[] args) {
        System.out.println(firstUnique("leetcode")); // l
        System.out.println(firstUnique("aabb"));     // no unique char
    }
}
```
**Time:** O(n) | **Space:** O(1) (at most 26 chars)

---

## Q22. Find All Substrings of a String

**Problem:** Generate and print all substrings of a given string.  
**Companies:** TCS, Wipro  

```java
public class AllSubstrings {
    public static void printAll(String s) {
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j <= s.length(); j++)
                System.out.println(s.substring(i, j));
    }

    public static void main(String[] args) {
        printAll("abc"); // a, ab, abc, b, bc, c
    }
}
```
**Time:** O(n³) | **Space:** O(1)

---

## Q23. Remove Duplicates from a Sorted Array

**Problem:** Remove duplicates from a sorted array in-place and return the new length.  
**Companies:** Wipro, Cognizant  

```java
public class RemoveDuplicatesSortedArray {
    public static int removeDuplicates(int[] arr) {
        if (arr.length == 0) return 0;
        int writePos = 1;
        for (int i = 1; i < arr.length; i++)
            if (arr[i] != arr[i - 1]) arr[writePos++] = arr[i];
        return writePos;
    }

    public static void main(String[] args) {
        int[] arr = {1, 1, 2, 3, 3, 4};
        int len = removeDuplicates(arr);
        for (int i = 0; i < len; i++) System.out.print(arr[i] + " "); // 1 2 3 4
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q24. Maximum Occurring Character in a String

**Problem:** Find the character that occurs the most in a string.  
**Companies:** TCS, HCL  

```java
public class MaxOccurringChar {
    public static char maxChar(String s) {
        int[] freq = new int[256];
        int max = 0;
        char result = '\0';
        for (char c : s.toCharArray()) {
            freq[c]++;
            if (freq[c] > max) { max = freq[c]; result = c; }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(maxChar("teststring")); // t
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q25. Check if a String Contains Only Digits

**Problem:** Check if all characters in a string are digits.  
**Companies:** TCS, HCL  

```java
public class OnlyDigits {
    public static boolean isNumeric(String s) {
        if (s == null || s.isEmpty()) return false;
        for (char c : s.toCharArray())
            if (!Character.isDigit(c)) return false;
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isNumeric("12345")); // true
        System.out.println(isNumeric("123a5")); // false
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q26. Find the Majority Element (Appears > n/2 times)

**Problem:** Find the element that appears more than n/2 times in an array.  
**Companies:** Infosys, Accenture  
**Approach:** Boyer-Moore Voting Algorithm

```java
public class MajorityElement {
    public static int findMajority(int[] arr) {
        int candidate = arr[0], count = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == candidate) count++;
            else if (--count == 0) { candidate = arr[i]; count = 1; }
        }
        return candidate;
    }

    public static void main(String[] args) {
        int[] arr = {3, 3, 4, 2, 4, 4, 2, 4, 4};
        System.out.println("Majority: " + findMajority(arr)); // 4
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q27. Longest Common Prefix Among Array of Strings

**Problem:** Find the longest common prefix string amongst an array of strings.  
**Companies:** TCS, Infosys  

```java
public class LongestCommonPrefix {
    public static String lcp(String[] strs) {
        String prefix = strs[0];
        for (int i = 1; i < strs.length; i++)
            while (!strs[i].startsWith(prefix))
                prefix = prefix.substring(0, prefix.length() - 1);
        return prefix;
    }

    public static void main(String[] args) {
        String[] arr = {"flower", "flow", "flight"};
        System.out.println(lcp(arr)); // fl
    }
}
```
**Time:** O(S) where S is total chars | **Space:** O(1)

---

## Q28. Count Vowels and Consonants

**Problem:** Count vowels and consonants in a string.  
**Companies:** TCS, HCL, Tech Mahindra  

```java
public class VowelConsonantCount {
    public static void count(String s) {
        s = s.toLowerCase();
        int vowels = 0, consonants = 0;
        String vowelSet = "aeiou";
        for (char c : s.toCharArray()) {
            if (Character.isLetter(c)) {
                if (vowelSet.indexOf(c) >= 0) vowels++;
                else consonants++;
            }
        }
        System.out.println("Vowels: " + vowels + ", Consonants: " + consonants);
    }

    public static void main(String[] args) {
        count("Hello World"); // Vowels: 3, Consonants: 7
    }
}
```

---

## Q29. Print All Unique Elements in an Array

**Problem:** Print all elements that appear exactly once in an array.  
**Companies:** TCS, Wipro  

```java
import java.util.*;

public class UniqueElements {
    public static void printUnique(int[] arr) {
        Map<Integer, Integer> freq = new LinkedHashMap<>();
        for (int x : arr) freq.put(x, freq.getOrDefault(x, 0) + 1);
        for (Map.Entry<Integer, Integer> e : freq.entrySet())
            if (e.getValue() == 1) System.out.print(e.getKey() + " ");
    }

    public static void main(String[] args) {
        printUnique(new int[]{1, 2, 3, 2, 4, 1}); // 3 4
    }
}
```

---

## Q30. Left Rotate an Array by One Position

**Problem:** Rotate an array one position to the left.  
**Companies:** TCS, Wipro  

```java
public class LeftRotateOne {
    public static void leftRotate(int[] arr) {
        int first = arr[0];
        for (int i = 1; i < arr.length; i++) arr[i - 1] = arr[i];
        arr[arr.length - 1] = first;
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        leftRotate(arr);
        for (int x : arr) System.out.print(x + " "); // 2 3 4 5 1
    }
}
```

---

## Q31. Maximum Difference Between Two Elements (max - min, later - earlier)

**Problem:** Find the maximum difference arr[j] - arr[i] such that j > i.  
**Companies:** Wipro, Accenture  

```java
public class MaxDifference {
    public static int maxDiff(int[] arr) {
        int minSoFar = arr[0], maxDiff = 0;
        for (int i = 1; i < arr.length; i++) {
            maxDiff = Math.max(maxDiff, arr[i] - minSoFar);
            minSoFar = Math.min(minSoFar, arr[i]);
        }
        return maxDiff;
    }

    public static void main(String[] args) {
        int[] arr = {2, 3, 10, 6, 4, 8, 1};
        System.out.println("Max Diff: " + maxDiff(arr)); // 8 (10 - 2)
    }
}
```

---

## Q32. Intersection of Two Arrays

**Problem:** Find common elements in two arrays.  
**Companies:** Infosys, Cognizant  

```java
import java.util.*;

public class ArrayIntersection {
    public static List<Integer> intersect(int[] a, int[] b) {
        Set<Integer> setA = new HashSet<>();
        List<Integer> result = new ArrayList<>();
        for (int x : a) setA.add(x);
        for (int x : b) if (setA.contains(x)) { result.add(x); setA.remove(x); }
        return result;
    }

    public static void main(String[] args) {
        int[] a = {1, 2, 4, 5, 6}, b = {2, 3, 5, 7};
        System.out.println(intersect(a, b)); // [2, 5]
    }
}
```

---

## Q33. String to Integer (atoi)

**Problem:** Convert a string to an integer without using parseInt.  
**Companies:** TCS, Wipro  

```java
public class StringToInt {
    public static int myAtoi(String s) {
        s = s.trim();
        if (s.isEmpty()) return 0;
        int sign = 1, i = 0;
        long result = 0;
        if (s.charAt(0) == '-') { sign = -1; i = 1; }
        else if (s.charAt(0) == '+') { i = 1; }
        while (i < s.length() && Character.isDigit(s.charAt(i))) {
            result = result * 10 + (s.charAt(i++) - '0');
            if (result * sign > Integer.MAX_VALUE) return Integer.MAX_VALUE;
            if (result * sign < Integer.MIN_VALUE) return Integer.MIN_VALUE;
        }
        return (int)(result * sign);
    }

    public static void main(String[] args) {
        System.out.println(myAtoi("   -42")); // -42
        System.out.println(myAtoi("4193 with words")); // 4193
    }
}
```

---

## Q34. Find Length of Longest Substring Without Repeating Characters

**Problem:** Given a string, find the length of the longest substring with all unique characters.  
**Companies:** Infosys SP, TCS Digital, Accenture  
**Approach:** Sliding window with a HashSet.

```java
import java.util.*;

public class LongestUniqueSubstring {
    public static int lengthOfLongestSubstring(String s) {
        Set<Character> window = new HashSet<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            while (window.contains(s.charAt(right)))
                window.remove(s.charAt(left++));
            window.add(s.charAt(right));
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }

    public static void main(String[] args) {
        System.out.println(lengthOfLongestSubstring("abcabcbb")); // 3
        System.out.println(lengthOfLongestSubstring("pwwkew"));   // 3
    }
}
```
**Time:** O(n) | **Space:** O(min(m, n))

---

## Q35. Check Balanced String (Equal Chars)

**Problem:** Given a string with only two distinct characters, check if they appear equal number of times.  
**Companies:** TCS, Wipro  

```java
public class BalancedString {
    public static boolean isBalanced(String s, char a, char b) {
        int countA = 0, countB = 0;
        for (char c : s.toCharArray()) {
            if (c == a) countA++;
            else if (c == b) countB++;
        }
        return countA == countB;
    }

    public static void main(String[] args) {
        System.out.println(isBalanced("aabb", 'a', 'b')); // true
        System.out.println(isBalanced("aaabb", 'a', 'b')); // false
    }
}
```

---

## Q36. Find All Pairs with a Given Difference

**Problem:** Find all pairs in the array whose difference equals a given value k.  
**Companies:** Wipro, Accenture  

```java
import java.util.*;

public class PairsWithDifference {
    public static void findPairs(int[] arr, int k) {
        Set<Integer> set = new HashSet<>();
        for (int x : arr) set.add(x);
        for (int x : arr)
            if (set.contains(x + k)) System.out.println(x + ", " + (x + k));
    }

    public static void main(String[] args) {
        findPairs(new int[]{1, 5, 3, 4, 2}, 3); // 1,4 and 2,5
    }
}
```

---

## Q37. Count Occurrences of an Element in a Sorted Array

**Problem:** Count the frequency of a target element in a sorted array using binary search.  
**Companies:** TCS, Cognizant  

```java
public class CountInSortedArray {
    static int firstOccurrence(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1, result = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) { result = mid; hi = mid - 1; }
            else if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return result;
    }

    static int lastOccurrence(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1, result = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) { result = mid; lo = mid + 1; }
            else if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return result;
    }

    public static int count(int[] arr, int target) {
        int first = firstOccurrence(arr, target);
        if (first == -1) return 0;
        return lastOccurrence(arr, target) - first + 1;
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 2, 2, 3, 4};
        System.out.println("Count of 2: " + count(arr, 2)); // 3
    }
}
```

---

## Q38. Product of Array Except Self

**Problem:** Return an array where each element is the product of all other elements except itself (no division).  
**Companies:** Infosys SP, TCS Digital  

```java
public class ProductExceptSelf {
    public static int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        result[0] = 1;
        for (int i = 1; i < n; i++) result[i] = result[i - 1] * nums[i - 1];
        int rightProduct = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        return result;
    }

    public static void main(String[] args) {
        int[] result = productExceptSelf(new int[]{1, 2, 3, 4});
        for (int x : result) System.out.print(x + " "); // 24 12 8 6
    }
}
```
**Time:** O(n) | **Space:** O(1) (excluding output array)

---

## Q39. Find the Element that Appears Once (Others Appear Twice)

**Problem:** Every element in the array appears twice except one. Find that element.  
**Companies:** TCS, Accenture  
**Approach:** XOR — same elements cancel out (a XOR a = 0, a XOR 0 = a).

```java
public class SingleElement {
    public static int findSingle(int[] arr) {
        int result = 0;
        for (int x : arr) result ^= x;
        return result;
    }

    public static void main(String[] args) {
        System.out.println(findSingle(new int[]{2, 3, 5, 4, 5, 3, 4})); // 2
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q40. Minimum Size Subarray with Sum ≥ Target

**Problem:** Find the minimum length subarray whose sum is at least the target.  
**Companies:** Infosys SP, TCS Digital  
**Approach:** Sliding window.

```java
public class MinSubarrayLength {
    public static int minLength(int[] arr, int target) {
        int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
        for (int right = 0; right < arr.length; right++) {
            sum += arr[right];
            while (sum >= target) {
                minLen = Math.min(minLen, right - left + 1);
                sum -= arr[left++];
            }
        }
        return (minLen == Integer.MAX_VALUE) ? 0 : minLen;
    }

    public static void main(String[] args) {
        System.out.println(minLength(new int[]{2, 3, 1, 2, 4, 3}, 7)); // 2
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

*Next: [02_Math_and_Number_Systems.md](./02_Math_and_Number_Systems.md)*
