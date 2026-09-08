# Stacks, Queues, Deques, and Linked Lists in JavaScript

Welcome to the second module. In this guide, we dive into linear data structures: Stacks, Queues, and Linked Lists. 

---

## 1. Stack Implementation

```javascript
// JavaScript stack using array
const stack = [];
stack.push(10);           // push: O(1)
stack.push(20);
const top = stack[stack.length - 1]; // peek: O(1)
const x = stack.pop();    // pop: O(1)
const isEmpty = stack.length === 0;
```
Java comparison:
```java
Stack<Integer> stack = new Stack<>();
stack.push(10);
stack.peek();
stack.pop();
stack.isEmpty();
```

Stack class wrapper:
```javascript
class Stack {
    constructor() { this.data = []; }
    push(x) { this.data.push(x); }
    pop() { return this.data.pop(); }
    peek() { return this.data[this.data.length - 1]; }
    isEmpty() { return this.data.length === 0; }
    size() { return this.data.length; }
}
```

DSA Applications with COMPLETE JavaScript implementations:

**Balanced Parentheses**:
```javascript
function isValid(s) {
    const stack = [];
    const map = { ')': '(', '}': '{', ']': '[' };
    for(const c of s) {
        if('([{'.includes(c)) stack.push(c);
        else if(stack.pop() !== map[c]) return false;
    }
    return stack.length === 0;
}
```

**Next Greater Element** with Monotonic Stack:
```javascript
function nextGreaterElement(arr) {
    const n = arr.length;
    const result = new Array(n).fill(-1);
    const stack = [];
    for(let i = 0; i < n; i++) {
        while(stack.length && arr[stack[stack.length-1]] < arr[i]) {
            result[stack.pop()] = arr[i];
        }
        stack.push(i);
    }
    return result;
}
```

**Largest Rectangle in Histogram**:
Implement complete solution with monotonic stack.

**Valid expression evaluation**: postfix evaluation.

**DFS using iterative stack** template.

---

## 2. Queue Implementation

VERY IMPORTANT — explain the shift() problem first:
```
queue.shift() is O(n) because it moves all elements!
For small n (< 1000) it's fine.
For large n (10^5+) use index-based approach.
```

```javascript
// Efficient queue using index
const queue = [];
let front = 0;

queue.push(value);           // enqueue: O(1)
const item = queue[front++]; // dequeue: O(1)
const isEmpty = front >= queue.length;
const head = queue[front];   // peek: O(1)
```

Java comparison:
```java
Queue<Integer> q = new LinkedList<>();
q.offer(x);
q.poll();
q.peek();
q.isEmpty();
```

Queue class:
```javascript
class Queue {
    constructor() { this.data = []; this.front = 0; }
    enqueue(x) { this.data.push(x); }
    dequeue() { 
        if(this.isEmpty()) return undefined;
        return this.data[this.front++]; 
    }
    peek() { return this.data[this.front]; }
    isEmpty() { return this.front >= this.data.length; }
    size() { return this.data.length - this.front; }
}
```

BFS using Queue — complete template:
```javascript
function bfs(graph, start) {
    const visited = new Set([start]);
    const queue = [start];
    let front = 0;
    while(front < queue.length) {
        const node = queue[front++];
        for(const neighbor of graph[node]) {
            if(!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        }
    }
}
```

Level-order tree traversal with BFS.
Sliding window maximum using deque.

---

## 3. Deque

Deque implementation using doubly-linked list for O(1) both ends:
```javascript
class Deque {
    constructor() {
        this.data = [];
        this.front = 0;
    }
    pushBack(x) { this.data.push(x); }
    pushFront(x) { this.data.unshift(x); }  // O(n) — note for large n
    popBack() { return this.data.pop(); }
    popFront() { 
        if(this.isEmpty()) return undefined;
        return this.data[this.front++];
    }
    peekFront() { return this.data[this.front]; }
    peekBack() { return this.data[this.data.length-1]; }
    isEmpty() { return this.front >= this.data.length; }
    size() { return this.data.length - this.front; }
}
```

Note pushFront is O(n) — for competitive programming where both ends need O(1), explain linked list deque.

Sliding window maximum with monotonic deque:
```javascript
function maxSlidingWindow(nums, k) {
    const deque = [];  // stores indices
    const result = [];
    for(let i = 0; i < nums.length; i++) {
        // Remove indices outside window
        while(deque.length && deque[0] < i - k + 1) deque.shift();
        // Remove smaller elements from back
        while(deque.length && nums[deque[deque.length-1]] < nums[i]) deque.pop();
        deque.push(i);
        if(i >= k-1) result.push(nums[deque[0]]);
    }
    return result;
}
```

---

## 4. Linked List

Node class:
```javascript
class ListNode {
    constructor(val, next = null) {
        this.val = val;
        this.next = next;
    }
}
```
Java comparison:
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}
```

Differences explained: no int type, `null` default in constructor, `this` keyword

Doubly Linked List node:
```javascript
class DListNode {
    constructor(val, prev = null, next = null) {
        this.val = val; this.prev = prev; this.next = next;
    }
}
```

Complete implementations:

**Reverse Linked List** (iterative + recursive):
```javascript
function reverseList(head) {
    let prev = null, curr = head;
    while(curr) {
        const next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

**Detect Cycle** (Floyd's algorithm):
```javascript
function hasCycle(head) {
    let slow = head, fast = head;
    while(fast && fast.next) {
        slow = slow.next;
        fast = fast.next.next;
        if(slow === fast) return true;
    }
    return false;
}
```

**Find Middle**:
```javascript
function findMiddle(head) {
    let slow = head, fast = head;
    while(fast && fast.next) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```

**Merge Two Sorted Lists**:
```javascript
function mergeTwoLists(l1, l2) {
    const dummy = new ListNode(0);
    let curr = dummy;
    while(l1 && l2) {
        if(l1.val <= l2.val) { curr.next = l1; l1 = l1.next; }
        else { curr.next = l2; l2 = l2.next; }
        curr = curr.next;
    }
    curr.next = l1 || l2;
    return dummy.next;
}
```

**Remove Nth from End** (two-pointer)
**Find Intersection**
**Add Two Numbers**
**Palindrome Linked List**

---

## 5. Practice Problems List (15 problems)

**Stacks & Queues:**
1. Valid Parentheses (LeetCode 20)
2. Min Stack (LeetCode 155) - Design problem
3. Daily Temperatures (LeetCode 739) - Monotonic Stack
4. Largest Rectangle in Histogram (LeetCode 84)
5. Implement Queue using Stacks (LeetCode 232)
6. Sliding Window Maximum (LeetCode 239)
7. Rotting Oranges (LeetCode 994) - BFS with Queue

**Linked Lists:**
8. Reverse Linked List (LeetCode 206)
9. Linked List Cycle (LeetCode 141)
10. Merge Two Sorted Lists (LeetCode 21)
11. Middle of the Linked List (LeetCode 876)
12. Remove Nth Node From End of List (LeetCode 19)
13. Palindrome Linked List (LeetCode 234)
14. Intersection of Two Linked Lists (LeetCode 160)
15. LRU Cache (LeetCode 146)
