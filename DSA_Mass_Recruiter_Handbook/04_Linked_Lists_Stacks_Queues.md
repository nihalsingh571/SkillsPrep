# Linked Lists, Stacks & Queues — Q66 to Q80

> **Target companies:** TCS, Infosys, Cognizant, Wipro, HCL  
> **Difficulty:** Easy to Medium  
> **Coverage:** ~15% of mass-recruiter questions

---

## Node Class (Reused Across All Linked List Questions)

```java
class Node {
    int data;
    Node next;
    Node(int data) { this.data = data; this.next = null; }
}
```

---

## Q66. Reverse a Singly Linked List

**Problem:** Reverse a singly linked list iteratively.  
**Companies:** TCS, Infosys, Cognizant, Wipro (all companies!)  
**Approach:** Keep track of previous, current, and next pointers.

```java
public class ReverseLinkedList {
    public static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node next = curr.next; // Save next
            curr.next = prev;      // Reverse the link
            prev = curr;           // Move prev forward
            curr = next;           // Move curr forward
        }
        return prev; // New head
    }

    // Utility: print list
    static void print(Node head) {
        while (head != null) { System.out.print(head.data + " "); head = head.next; }
        System.out.println();
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        head = reverse(head);
        print(head); // 4 3 2 1
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q67. Detect a Cycle in a Linked List (Floyd's Algorithm)

**Problem:** Determine if a linked list contains a cycle.  
**Companies:** TCS, Infosys, Cognizant  
**Approach:** Floyd's Tortoise and Hare — slow pointer moves 1 step, fast moves 2. If they meet, there's a cycle.

```java
public class DetectCycle {
    public static boolean hasCycle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true; // Cycle detected
        }
        return false;
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = head.next; // Creates a cycle
        System.out.println(hasCycle(head)); // true
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q68. Find the Middle Element of a Linked List

**Problem:** Find the middle node. If there are two middle nodes (even length), return the second one.  
**Companies:** TCS, Wipro, Cognizant  
**Approach:** Slow and fast pointers — fast moves 2 steps, slow moves 1. When fast reaches end, slow is at middle.

```java
public class MiddleOfLinkedList {
    public static Node findMiddle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow; // Middle node
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        head.next.next.next.next = new Node(5);
        System.out.println("Middle: " + findMiddle(head).data); // 3
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q69. Merge Two Sorted Linked Lists

**Problem:** Merge two sorted linked lists into one sorted list.  
**Companies:** TCS, Infosys, Cognizant  
**Approach:** Compare heads of both lists and link the smaller one, recursively.

```java
public class MergeSortedLists {
    public static Node merge(Node l1, Node l2) {
        if (l1 == null) return l2;
        if (l2 == null) return l1;
        if (l1.data <= l2.data) {
            l1.next = merge(l1.next, l2);
            return l1;
        } else {
            l2.next = merge(l1, l2.next);
            return l2;
        }
    }

    static void print(Node head) {
        while (head != null) { System.out.print(head.data + " "); head = head.next; }
        System.out.println();
    }

    public static void main(String[] args) {
        Node l1 = new Node(1); l1.next = new Node(3); l1.next.next = new Node(5);
        Node l2 = new Node(2); l2.next = new Node(4); l2.next.next = new Node(6);
        print(merge(l1, l2)); // 1 2 3 4 5 6
    }
}
```
**Time:** O(m+n) | **Space:** O(m+n) recursive stack

---

## Q70. Remove Duplicates from a Sorted Linked List

**Problem:** Remove duplicate nodes from a sorted linked list.  
**Companies:** TCS, Wipro, HCL  

```java
public class RemoveDuplicatesLinkedList {
    public static Node removeDuplicates(Node head) {
        Node curr = head;
        while (curr != null && curr.next != null) {
            if (curr.data == curr.next.data)
                curr.next = curr.next.next; // Skip duplicate
            else
                curr = curr.next;
        }
        return head;
    }

    static void print(Node head) {
        while (head != null) { System.out.print(head.data + " "); head = head.next; }
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(1);
        head.next.next = new Node(2);
        head.next.next.next = new Node(3);
        head.next.next.next.next = new Node(3);
        print(removeDuplicates(head)); // 1 2 3
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q71. Check if a Linked List is a Palindrome

**Problem:** Check if a singly linked list reads the same forwards and backwards.  
**Companies:** TCS, Infosys  
**Approach:** Find middle, reverse the second half, compare with first half.

```java
public class PalindromeLinkedList {
    static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node next = curr.next; curr.next = prev; prev = curr; curr = next;
        }
        return prev;
    }

    public static boolean isPalindrome(Node head) {
        if (head == null || head.next == null) return true;
        // Find middle
        Node slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next; fast = fast.next.next;
        }
        // Reverse second half
        Node secondHalf = reverse(slow.next);
        // Compare
        Node p1 = head, p2 = secondHalf;
        while (p2 != null) {
            if (p1.data != p2.data) return false;
            p1 = p1.next; p2 = p2.next;
        }
        return true;
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2); head.next.next = new Node(2); head.next.next.next = new Node(1);
        System.out.println(isPalindrome(head)); // true
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q72. Delete a Node at a Given Position

**Problem:** Delete the node at position k (1-indexed) in a linked list.  
**Companies:** TCS, HCL  

```java
public class DeleteAtPosition {
    public static Node delete(Node head, int pos) {
        if (head == null) return null;
        if (pos == 1) return head.next;
        Node curr = head;
        for (int i = 1; i < pos - 1 && curr.next != null; i++)
            curr = curr.next;
        if (curr.next != null) curr.next = curr.next.next;
        return head;
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q73. Balanced Parentheses Check Using Stack

**Problem:** Given a string of brackets `()[]{}`, check if they are balanced.  
**Companies:** TCS, Wipro, Cognizant, Accenture  
**Approach:** Push opening brackets, pop on closing — check if matched.

```java
import java.util.*;

public class BalancedParentheses {
    public static boolean isBalanced(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if (c == ')' && top != '(') return false;
                if (c == ']' && top != '[') return false;
                if (c == '}' && top != '{') return false;
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(isBalanced("()[]{}"));   // true
        System.out.println(isBalanced("([)]"));     // false
        System.out.println(isBalanced("{[]}"));     // true
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q74. Implement a Stack Using an Array

**Problem:** Implement push, pop, peek, and isEmpty operations for a stack.  
**Companies:** TCS, HCL, Cognizant  

```java
public class StackUsingArray {
    int[] arr;
    int top = -1;
    int capacity;

    StackUsingArray(int size) {
        capacity = size;
        arr = new int[capacity];
    }

    void push(int val) {
        if (top == capacity - 1) { System.out.println("Stack Overflow!"); return; }
        arr[++top] = val;
    }

    int pop() {
        if (top == -1) { System.out.println("Stack Underflow!"); return -1; }
        return arr[top--];
    }

    int peek() {
        if (top == -1) return -1;
        return arr[top];
    }

    boolean isEmpty() { return top == -1; }

    public static void main(String[] args) {
        StackUsingArray stack = new StackUsingArray(5);
        stack.push(10); stack.push(20); stack.push(30);
        System.out.println(stack.peek()); // 30
        System.out.println(stack.pop());  // 30
        System.out.println(stack.pop());  // 20
    }
}
```

---

## Q75. Implement a Queue Using an Array

**Problem:** Implement enqueue, dequeue, front operations for a queue (FIFO).  
**Companies:** TCS, HCL  

```java
public class QueueUsingArray {
    int[] arr;
    int front = 0, rear = -1, size = 0, capacity;

    QueueUsingArray(int cap) { capacity = cap; arr = new int[cap]; }

    void enqueue(int val) {
        if (size == capacity) { System.out.println("Queue is Full!"); return; }
        rear = (rear + 1) % capacity;
        arr[rear] = val;
        size++;
    }

    int dequeue() {
        if (size == 0) { System.out.println("Queue is Empty!"); return -1; }
        int val = arr[front];
        front = (front + 1) % capacity;
        size--;
        return val;
    }

    int front() { return size == 0 ? -1 : arr[front]; }

    public static void main(String[] args) {
        QueueUsingArray q = new QueueUsingArray(5);
        q.enqueue(10); q.enqueue(20); q.enqueue(30);
        System.out.println(q.dequeue()); // 10
        System.out.println(q.front());   // 20
    }
}
```

---

## Q76. Implement Stack Using Two Queues

**Problem:** Simulate a stack (LIFO) using only queue (FIFO) operations.  
**Companies:** Cognizant, TCS Digital  
**Approach:** On each push, enqueue the new element then rotate all previous elements behind it.

```java
import java.util.*;

public class StackUsingQueues {
    Queue<Integer> q1 = new LinkedList<>();

    void push(int val) {
        q1.add(val);
        // Rotate queue so new element is at front
        for (int i = 0; i < q1.size() - 1; i++)
            q1.add(q1.poll());
    }

    int pop() { return q1.isEmpty() ? -1 : q1.poll(); }
    int peek() { return q1.isEmpty() ? -1 : q1.peek(); }
    boolean isEmpty() { return q1.isEmpty(); }

    public static void main(String[] args) {
        StackUsingQueues s = new StackUsingQueues();
        s.push(1); s.push(2); s.push(3);
        System.out.println(s.pop()); // 3
        System.out.println(s.pop()); // 2
    }
}
```
**Time:** O(n) per push, O(1) per pop

---

## Q77. Next Greater Element

**Problem:** For each element in an array, find the next element to its right that is greater than it. Return -1 if none exists.  
**Companies:** Infosys, Accenture, TCS Digital  
**Approach:** Monotonic Stack — process right to left, maintaining a decreasing stack.

```java
import java.util.*;

public class NextGreaterElement {
    public static int[] nextGreater(int[] arr) {
        int n = arr.length;
        int[] result = new int[n];
        Stack<Integer> stack = new Stack<>(); // Stores indices
        for (int i = n - 1; i >= 0; i--) {
            while (!stack.isEmpty() && stack.peek() <= arr[i])
                stack.pop();
            result[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(arr[i]);
        }
        return result;
    }

    public static void main(String[] args) {
        int[] arr = {4, 5, 2, 10, 8};
        int[] result = nextGreater(arr);
        for (int x : result) System.out.print(x + " "); // 5 10 10 -1 -1
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

## Q78. Sort a Stack Using Recursion

**Problem:** Sort the elements of a stack in ascending order (smallest on top) using only recursion (no extra data structure).  
**Companies:** Infosys, TCS Digital  

```java
import java.util.*;

public class SortStack {
    static void sortedInsert(Stack<Integer> stack, int val) {
        if (stack.isEmpty() || stack.peek() <= val) { stack.push(val); return; }
        int top = stack.pop();
        sortedInsert(stack, val);
        stack.push(top);
    }

    public static void sortStack(Stack<Integer> stack) {
        if (!stack.isEmpty()) {
            int top = stack.pop();
            sortStack(stack);
            sortedInsert(stack, top);
        }
    }

    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        stack.push(3); stack.push(1); stack.push(4); stack.push(2);
        sortStack(stack);
        System.out.println(stack); // [1, 2, 3, 4] (1 on top after pops)
    }
}
```

---

## Q79. Find the Kth Node from the End of a Linked List

**Problem:** Find the kth node from the end of a singly linked list (k=1 means last node).  
**Companies:** TCS, Wipro, Infosys  
**Approach:** Two-pointer — advance fast pointer k steps first, then move both until fast reaches the end.

```java
public class KthFromEnd {
    public static Node findKthFromEnd(Node head, int k) {
        Node fast = head, slow = head;
        // Move fast k steps ahead
        for (int i = 0; i < k; i++) {
            if (fast == null) return null; // k > length
            fast = fast.next;
        }
        while (fast != null) { slow = slow.next; fast = fast.next; }
        return slow;
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2); head.next.next = new Node(3);
        head.next.next.next = new Node(4); head.next.next.next.next = new Node(5);
        System.out.println("2nd from end: " + findKthFromEnd(head, 2).data); // 4
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q80. Evaluate a Postfix Expression Using Stack

**Problem:** Given a postfix (Reverse Polish Notation) expression, evaluate it.  
**Companies:** TCS, Cognizant, Infosys  
**Approach:** Push operands, pop two when operator is encountered, compute, push result.

```java
import java.util.*;

public class PostfixEvaluation {
    public static int evaluate(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String token : tokens) {
            if (token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/")) {
                int b = stack.pop(), a = stack.pop();
                switch (token) {
                    case "+": stack.push(a + b); break;
                    case "-": stack.push(a - b); break;
                    case "*": stack.push(a * b); break;
                    case "/": stack.push(a / b); break;
                }
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        // Expression: 2 3 4 * + = 2 + (3 * 4) = 14
        String[] tokens = {"2", "3", "4", "*", "+"};
        System.out.println(evaluate(tokens)); // 14
    }
}
```
**Time:** O(n) | **Space:** O(n)

---

*Next: [05_Recursion_DP_Greedy.md](./05_Recursion_DP_Greedy.md)*
