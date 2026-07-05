# Java Interview Mastery Handbook: Section 3 & 4

## Section 3: Strings in Java

### 3.1 String Class: Definition, Internals, and Immutability
**Definition & Why it exists:** `String` is a class in Java that represents a sequence of characters. It is fundamental to almost every Java application.
**Internal Working:** 
- **Pre-Java 9:** Backed by a `char[]` array (UTF-16, 2 bytes per char).
- **Java 9+ (Compact Strings):** Backed by a `byte[]` array + a `coder` flag (`LATIN1` = 1 byte, `UTF16` = 2 bytes) to optimize memory.

**Immutability:** Strings cannot be modified once created.
*Why?*
1. **Security:** Used for sensitive data (DB passwords, URLs). Immutability prevents tampering after validation.
2. **String Pool (Memory):** Multiple references can safely point to the same literal because it won't change.
3. **Thread Safety:** Inherently thread-safe; requires no synchronization.
4. **Performance (Hash Caching):** Since the string won't change, its `hashCode` is calculated once and cached, making it extremely fast as a `HashMap` key.

### 3.2 The String Pool and Memory Mechanics
**String Pool:** A special storage area within the Java Heap memory. It stores unique String literals.
- `String s = "Hello"` creates/reuses an object in the Pool.
- `String s = new String("Hello")` forces the creation of a *new* object in the Heap memory (outside the pool), and places "Hello" in the pool if not already there.

**Memory Diagram (ASCII):**
```text
      Stack                    Heap Memory
    ---------              -----------------------
   | s1 = 0x1| ------     |    String Pool        |
   | s2 = 0x1| ------|--> |  0x1: "Java"          |
   | s3 = 0x2| --    |    |                       |
    ---------    |   |     -----------------------
                 |   |
                 |    ---> [Heap Object] 0x2: "Java"
```
*`s1 = "Java"` and `s2 = "Java"` point to 0x1. `s3 = new String("Java")` points to 0x2.*

### 3.3 == vs equals() vs compareTo()
- `==`: Compares **reference/memory address**.
- `equals()`: Compares **actual content/value**.
- `compareTo()`: Compares lexicographically (returns integer). Used for sorting.

### 3.4 StringBuilder vs StringBuffer
When you need to mutate text frequently, use these instead of `String` to avoid creating many garbage objects.

| Feature | String | StringBuilder | StringBuffer |
|---------|--------|---------------|--------------|
| **Mutability** | Immutable | Mutable | Mutable |
| **Thread Safety**| Thread-safe | **Not** thread-safe | Thread-safe (Synchronized) |
| **Performance** | Fast (if not modifying) | **Fastest** | Slow (due to locks) |

**Internal Expansion:** Both are backed by `char[]`/`byte[]`. Default capacity is 16. If exceeded, capacity grows by `(current_capacity * 2) + 2`.

### 3.5 String Concatenation Internals
**Code:** `String s = "a" + "b" + "c";`
**Pre-Java 9:** Compiler translates this to `new StringBuilder().append("a").append("b").append("c").toString()`.
**Java 9+:** Uses `invokedynamic` with `StringConcatFactory` for better performance and reduced byte code.

### 3.6 Creating Immutable Objects
**Benefits:** Thread-safe, cacheable, great for Map keys.
**How to create:**
1. Make class `final` so it cannot be extended.
2. Make fields `private` and `final`.
3. Do not provide setters.
4. Deep copy mutable objects in constructors and getters.

```java
public final class ImmutableStudent {
    private final int id;
    private final List<String> courses;
    
    public ImmutableStudent(int id, List<String> courses) {
        this.id = id;
        this.courses = new ArrayList<>(courses); // Deep Copy
    }
    
    public List<String> getCourses() {
        return new ArrayList<>(courses); // Deep Copy
    }
}
```

### 3.7 Important String Methods
```java
String s = " Hello Java ";
s.length();           // 12
s.trim();             // "Hello Java"
s.substring(1, 5);    // "Hell"
s.charAt(1);          // 'H'
s.indexOf('J');       // 7
s.replace("Java", "World"); // " Hello World "
s.split(" ");         // ["", "Hello", "Java", ""]
```

---

### 3.8 50 Tricky Output-Based Questions

1. `String s1 = "A"; String s2 = "A"; System.out.print(s1==s2);` -> **true** (Same pool reference).
2. `String s1 = new String("A"); String s2 = new String("A"); System.out.print(s1==s2);` -> **false** (Different heap objects).
3. `System.out.print(s1.equals(s2));` -> **true** (Content is the same).
4. `String s3 = "A"; System.out.print(s1.intern() == s3);` -> **true** (intern returns pool object).
5. `System.out.print("A" == "A");` -> **true**.
6. `String s = "a" + "b"; System.out.print(s == "ab");` -> **true** (Constants concatenated at compile time).
7. `String s1 = "a"; String s2 = s1 + "b"; System.out.print(s2 == "ab");` -> **false** (Variables concatenated at runtime create new heap object).
8. `final String s1 = "a"; String s2 = s1 + "b"; System.out.print(s2 == "ab");` -> **true** (final variable treated as compile-time constant).
9. `String s = " Java "; s.trim(); System.out.print(s);` -> **" Java "** (Strings are immutable, return value of trim ignored).
10. `String s = "A"; s = s.concat("B"); System.out.print(s);` -> **"AB"** (Reassigned to new object).
11. `System.out.print("a".compareTo("b"));` -> **-1**.
12. `System.out.print("b".compareTo("a"));` -> **1**.
13. `System.out.print("a".compareTo("A"));` -> **32** (ASCII diff).
14. `System.out.print(new StringBuilder("A").equals(new StringBuilder("A")));` -> **false** (StringBuilder doesn't override equals()).
15. `String s = null; System.out.print(s + "A");` -> **"nullA"**.
16. `System.out.print(null + null);` -> **Compiler Error**.
17. `System.out.print("A" + null);` -> **"Anull"**.
18. `String s1 = new String("X"); s1.intern(); String s2 = "X"; System.out.print(s1 == s2);` -> **false** (s1 is still heap ref).
19. `String s = new String("A") + new String("B"); s.intern(); String s2 = "AB"; System.out.print(s == s2);` -> **true** (In Java 7+, intern moves heap ref to pool if not present).
20. `System.out.print("abc".substring(1, 1));` -> **""** (Empty string).
21. `System.out.print("abc".substring(1, 4));` -> **StringIndexOutOfBoundsException**.
22. `System.out.print("abc".charAt(3));` -> **StringIndexOutOfBoundsException**.
23. `System.out.print(10 + 20 + "A");` -> **"30A"**.
24. `System.out.print("A" + 10 + 20);` -> **"A1020"**.
25. `System.out.print("A" + (10 + 20));` -> **"A30"**.
26. `System.out.print('A' + 'B');` -> **131** (Addition of chars yields int).
27. `System.out.print("A" + 'B');` -> **"AB"**.
28. `System.out.print(String.join("-", "A", "B", "C"));` -> **"A-B-C"**.
29. `String s = "Hello"; s = null; System.out.print(s instanceof String);` -> **false**.
30. `System.out.print("Hello".replace('l', 'w'));` -> **"Hewwo"**.
31. `System.out.print("Hello".replaceAll("l", "w"));` -> **"Hewwo"**.
32. `System.out.print("Hello".replaceFirst("l", "w"));` -> **"Hewlo"**.
33. `System.out.print("Hello".indexOf("l", 3));` -> **3**.
34. `System.out.print("Hello".lastIndexOf("l"));` -> **3**.
35. `System.out.print("".isEmpty());` -> **true**.
36. `System.out.print(" ".isEmpty());` -> **false**.
37. `System.out.print(" ".isBlank());` -> **true** (Java 11+).
38. `System.out.print("A".equalsIgnoreCase("a"));` -> **true**.
39. `System.out.print("A\nB".lines().count());` -> **2** (Java 11+).
40. `System.out.print("A".repeat(3));` -> **"AAA"** (Java 11+).
41. `System.out.print(new String(new char[]{'A', 'B'}));` -> **"AB"**.
42. `System.out.print(String.valueOf(null));` -> **NullPointerException** (if char[]) or **"null"** (if Object). Resolves to char[] causing NPE.
43. `System.out.print(String.valueOf((Object)null));` -> **"null"**.
44. `System.out.print("   ".strip());` -> **""** (Java 11+).
45. `System.out.print("ABC".toCharArray().length);` -> **3**.
46. `System.out.print("AB\\nC".length());` -> **5**.
47. `String s1 = "a"; String s2 = s1.intern(); System.out.print(s1==s2);` -> **true**.
48. `System.out.print("a" == new String("a").intern());` -> **true**.
49. `StringBuilder sb = new StringBuilder("A"); sb.append("B").reverse(); System.out.print(sb);` -> **"BA"**.
50. `System.out.print("Aa".hashCode() == "BB".hashCode());` -> **true** (Famous hash collision: 65*31 + 97 == 66*31 + 66).

### 3.9 Most Asked String Interview Questions
**Q1. How many objects are created in `String s = new String("Java");`?**
A: Two (if "Java" is not in the pool). One in the heap via `new`, and one in the String Pool for the literal "Java". The reference `s` points to the heap object.

**Q2. Why is char[] preferred over String for storing passwords?**
A: Strings are immutable and go to the String Pool, staying in memory until GC clears the pool (rare). A `char[]` can be explicitly wiped (`arr[i] = '*'`) immediately after use, reducing security risks from heap dumps.

**Q3. How does `intern()` method work?**
A: `intern()` checks if the exact string exists in the String Pool. If yes, it returns the pool reference. If no, it adds the string to the pool and returns the reference.

**Q4. What is the difference between `isEmpty()` and `isBlank()`?**
A: `isEmpty()` checks if length is 0. `isBlank()` (Java 11+) checks if string is empty OR contains only white spaces.

---

## Section 4: Collections Framework

### 4.1 Complete Hierarchy (ASCII Diagram)
```text
                  Iterable
                     |
                 Collection
         /           |           \
      List          Set         Queue
       |             |             |
   ArrayList     HashSet      PriorityQueue
  LinkedList   LinkedHashSet  Deque
    Vector       TreeSet       |-- ArrayDeque
       |                       |-- LinkedList
    Stack
```

### 4.2 Map Hierarchy
```text
                    Map
           /         |         \
      HashMap    Hashtable   SortedMap
         |                      |
  LinkedHashMap              TreeMap
```

---
### 4.3 List Implementations (Ordered, allows duplicates)

#### 1. ArrayList
- **Internal Data Structure:** Resizable Object Array (`Object[]`).
- **Mechanics:** Initial capacity is 10. When full, grows by 1.5x (`newCapacity = oldCapacity + (oldCapacity >> 1)`).
- **Time Complexity:** `add(E)`: Amortized O(1). `insert(index, E)`: O(n). `get(index)`: O(1). `remove(index)`: O(n).
- **Space Complexity:** O(n).
- **When to Use:** Frequent read operations.
- **When NOT to Use:** Frequent insertions/deletions in the middle (requires array shifting).
- **Tricky:** Fail-fast iterator. Throws `ConcurrentModificationException` if modified outside iterator.

#### 2. LinkedList
- **Internal Data Structure:** Doubly Linked List (Node contains `item`, `next`, `prev`).
- **Mechanics:** No initial capacity. Implements both `List` and `Deque`.
- **Time Complexity:** `addFirst/Last`: O(1). `insert/remove(middle)`: O(n). `get(index)`: O(n).
- **Space Complexity:** O(n) + overhead for Node pointers.
- **When to Use:** Frequent insertions/deletions at ends.
- **When NOT to Use:** Frequent random access `get(index)`.

#### 3. Vector & Stack (Legacy)
- **Vector:** Like `ArrayList` but synchronized (thread-safe). Grows by 2x. Slow. Avoid using; use `Collections.synchronizedList()` or `CopyOnWriteArrayList` instead.
- **Stack:** Extends Vector. LIFO structure (`push`, `pop`, `peek`). Modern alternative: `ArrayDeque`.

---
### 4.4 Set Implementations (No duplicates)

#### 1. HashSet
- **Internal Data Structure:** Backed by a `HashMap`. Elements are stored as Map keys, Map values are a dummy `Object`.
- **Mechanics:** Uses `equals()` and `hashCode()` to detect duplicates. Unordered.
- **Time Complexity:** O(1) for add, remove, contains.
- **Space Complexity:** O(n).
- **When to Use:** Fast uniqueness checks.

#### 2. LinkedHashSet
- **Internal Data Structure:** `LinkedHashMap` (Hash table + Doubly linked list).
- **Mechanics:** Maintains insertion order.
- **Time Complexity:** O(1).
- **When to Use:** Uniqueness + Insertion order required.

#### 3. TreeSet
- **Internal Data Structure:** Backed by `TreeMap` (Red-Black Tree).
- **Mechanics:** Sorted order (natural or custom `Comparator`). Implements `NavigableSet`.
- **Time Complexity:** O(log n) for add, remove, contains.
- **When to Use:** Ordered unique elements (e.g., getting ranges, smallest/largest).

---
### 4.5 Queue Implementations (FIFO / Priority)

#### 1. PriorityQueue
- **Internal Data Structure:** Min-Heap (Array-based binary tree).
- **Mechanics:** Elements sorted by priority. Root is always the smallest (or largest with custom Comparator).
- **Time Complexity:** `offer()`/`poll()`: O(log n). `peek()`: O(1).
- **When to Use:** Scheduling tasks, finding Top K elements.

#### 2. ArrayDeque
- **Internal Data Structure:** Resizable circular array.
- **Mechanics:** Double-ended queue. No nulls allowed.
- **Time Complexity:** O(1) add/remove at both ends.
- **When to Use:** Faster than `Stack` for LIFO, faster than `LinkedList` for FIFO.

---
### 4.6 Map Implementations (Key-Value pairs)

#### DEEP DIVE: HashMap
**Internal Data Structure:** Array of "Buckets". Each bucket is a Linked List (or a Red-Black Tree in Java 8+).

**Hashing Process Step-by-Step:**
1. `put(Key K, Value V)`
2. Calculate Hash: `int hash = (h = key.hashCode()) ^ (h >>> 16);` (XORs top 16 bits with bottom 16 to reduce collisions).
3. Calculate Index: `index = hash & (n - 1)` where `n` is array capacity (always power of 2).
4. **Collision Handling:** If bucket is empty, store node. If occupied:
   - Check if exact key exists (`hash` matches AND `equals()` is true). If yes, overwrite value.
   - If no, append to Linked List (Chaining).

**Treeification (Java 8+):**
- If a linked list chain exceeds **8 elements** (and total capacity >= 64), it converts into a **Red-Black Tree** to improve search from O(n) to O(log n).
- Untreeifies back to linked list if elements drop to **6**.

**Rehashing:**
- **Initial Capacity:** 16. **Load Factor:** 0.75.
- **Threshold:** 16 * 0.75 = 12.
- When elements exceed 12, capacity doubles (to 32). All existing elements are rehashed into the new array.

**Memory Diagram (HashMap Array):**
```text
Index:  0       1        2        3 ... 15
      [Node]  [null]   [Node]   [null]
        |                |
      null            [Node]  <- Linked List (Collision)
                         |
                      [Node]
```

**20 Tricky HashMap Questions:**
1. **Can HashMap have null keys?** Yes, exactly one null key (stored at index 0).
2. **Can it have null values?** Yes, multiple.
3. **What is time complexity of get()?** O(1) average, O(n) worst case (Java 7), O(log n) worst case (Java 8).
4. **Why is capacity always a power of 2?** So `hash % n` can be optimized to bitwise `hash & (n-1)`.
5. **Is HashMap thread-safe?** No. Use `ConcurrentHashMap`.
6. **What happens if two keys have same hashcode?** Collision. Stored in same bucket via Linked List / Tree.
7. **What if two keys have same hashcode but different equals()?** Stored as different nodes in the same bucket chain.
8. **What if two keys have same hashcode and same equals()?** Overwrites the existing value.
9. **Why use load factor 0.75?** Sweet spot between time and space overhead.
10. **What is the worst-case time complexity of put()?** O(N) during rehashing.
11. **Why does treeification threshold happen at 8?** Based on Poisson distribution, chance of 8 collisions is < 0.00000006.
12. **What if a class overrides hashCode() to return 1 always?** HashMap degrades to a Linked List (or Tree). O(n) or O(log n) performance.
13. **Can we use a mutable object as a HashMap key?** Bad practice. If modified, hashcode changes, and you can never retrieve the value.
14. **How does ConcurrentHashMap differ?** Java 8 uses Node-level locking (CAS + synchronized) instead of locking the whole map.
15. **Does ConcurrentHashMap allow null keys/values?** No. Avoids ambiguity in concurrent environments.
16. **How to sort a HashMap?** Use a `TreeMap` or sort the `entrySet()` using Streams.
17. **What is the default capacity?** 16.
18. **What happens in Java 7 during concurrent rehashing?** Infinite loop due to cycle in linked list. (Fixed in Java 8 by maintaining insertion order).
19. **What is IdentityHashMap?** Uses `==` instead of `equals()` for comparing keys.
20. **What is WeakHashMap?** Keys are stored via WeakReferences. If key has no other strong reference, entry is garbage collected.

#### LinkedHashMap
- Extends `HashMap`. Adds a doubly linked list through all entries.
- Maintains insertion order or access order (useful for LRU caches).
- Time Complexity: O(1).

#### TreeMap
- Implements `NavigableMap`. Red-Black Tree.
- Sorted by natural order or custom Comparator.
- Time Complexity: O(log n).

---

### 4.7 Collections Cheat Sheet & Decision Table

| Requirement | Use This Collection |
|-------------|---------------------|
| Ordered list, fast iteration | `ArrayList` |
| Fast add/remove at ends | `ArrayDeque` / `LinkedList` |
| Unique elements, no order | `HashSet` |
| Unique elements, insertion order | `LinkedHashSet` |
| Unique elements, sorted order | `TreeSet` |
| Key-Value, fast access | `HashMap` |
| Key-Value, insertion order | `LinkedHashMap` |
| Key-Value, sorted by keys | `TreeMap` |
| Thread-safe Map | `ConcurrentHashMap` |
| Top/Min/Max elements | `PriorityQueue` |

---
### 4.8 Top 100 Collections Interview Questions (Concise Rapid-Fire)

1. **Root of Collections?** `Iterable`.
2. **Difference between Collection and Collections?** `Collection` is an interface. `Collections` is a utility class.
3. **Does Map extend Collection?** No.
4. **List vs Set?** List allows duplicates/ordered. Set prohibits duplicates/unordered.
5. **ArrayList vs LinkedList?** Array vs Doubly Linked List.
6. **Default ArrayList capacity?** 10.
7. **ArrayList growth rate?** 1.5x.
8. **Vector growth rate?** 2x.
9. **Fail-fast vs Fail-safe?** Fail-fast throws CME immediately. Fail-safe works on clone.
10. **Example of Fail-safe?** `ConcurrentHashMap`, `CopyOnWriteArrayList`.
11. **Iterator vs ListIterator?** ListIterator is bidirectional and allows modification.
12. **Can ListIterator be used for Set?** No, only Lists.
13. **How does HashSet work?** Uses HashMap internally.
14. **What is the value in HashSet's HashMap?** A dummy static `Object`.
15. **TreeSet internal structure?** `TreeMap` (Red-Black tree).
16. **Comparable vs Comparator?** Comparable modifies the class (`compareTo()`). Comparator is external (`compare()`).
17. **Default sorting of Strings?** Lexicographical.
18. **PriorityQueue null values?** Not allowed (throws NPE).
19. **ArrayDeque vs Stack?** ArrayDeque is faster, no synchronization overhead.
20. **HashMap vs Hashtable?** Hashtable is synchronized, no nulls allowed.
21. **HashMap initial capacity?** 16.
22. **HashMap load factor?** 0.75.
23. **Why String is popular Map key?** Immutable, cached hashcode.
24. **ConcurrentModificationException?** Modifying a collection directly while iterating over it.
25. **How to avoid CME?** Use `Iterator.remove()` or concurrent collections.
26. **BlockingQueue use case?** Producer-Consumer patterns.
27. **CopyOnWriteArrayList use case?** Reads vastly outnumber writes.
28. **Collections.sort() algorithm?** TimSort (Merge + Insertion sort).
29. **Time complexity of TimSort?** O(n log n).
30. **TreeSet null elements?** Throws NPE (cannot compare null).
31. **LinkedHashSet performance vs HashSet?** Slightly slower due to linked list maintenance, but faster iteration.
32. **HashMap get() O(1) guaranteed?** No, O(n) or O(log n) if severe collisions.
33. **Convert Array to List?** `Arrays.asList()`.
34. **Is Arrays.asList() modifiable?** Cannot add/remove elements (throws exception), but can modify existing elements.
35. **Convert List to Array?** `list.toArray(new String[0])`.
36. **Difference between peek() and poll()?** peek() views, poll() removes and returns.
37. **What if Queue is empty in poll()?** Returns null.
38. **What if Queue is empty in remove()?** Throws NoSuchElementException.
39. **Collections.unmodifiableList()?** Returns read-only view.
40. **Are unmodifiable collections immutable?** No, if the original list changes, the view changes.
41. **List.of() vs Arrays.asList()?** `List.of()` is truly immutable and prohibits nulls (Java 9).
42. **Thread-safe HashMap alternatives?** `Hashtable`, `Collections.synchronizedMap()`, `ConcurrentHashMap`.
43. **Why is ConcurrentHashMap best?** Uses lock striping / node locks. High concurrency.
44. **ConcurrentHashMap size() accurate?** Can be approximate due to concurrent updates.
45. **NavigableMap methods?** `lowerKey()`, `floorKey()`, `ceilingKey()`, `higherKey()`.
46. **Set with LRU capabilities?** No native Set, but can build via LinkedHashMap.
47. **Implement LRU Cache?** Extend `LinkedHashMap`, override `removeEldestEntry()`.
48. **EnumSet?** High-performance Set for Enums (uses bit vectors).
49. **EnumMap?** Map with Enum keys (uses array internally).
50. **IdentityHashMap use case?** Topology traversal, graph algorithms where exact instances matter.
51. **WeakHashMap use case?** Caching, preventing memory leaks.
52. **Properties class?** Extends Hashtable, string-based keys/values.
53. **How to synchronize a list?** `Collections.synchronizedList(list)`.
54. **Should you manually synchronize Iterator on synchronized collections?** Yes.
55. **List vs array?** Arrays are fixed size and hold primitives. Lists are dynamic and hold Objects.
56. **Autoboxing in Collections?** Primitives are automatically converted to Wrapper classes.
57. **Memory impact of Wrapper classes?** Significant overhead compared to primitive arrays.
58. **Trove / FastUtil libraries?** Third-party libraries for primitive collections.
59. **Which Set allows null?** HashSet allows one null. TreeSet does not.
60. **Does PriorityQueue guarantee sorting when iterating?** No, only `poll()` guarantees order.
61. **Initial capacity of Vector?** 10.
62. **Can you set load factor for HashSet?** Yes, via constructor.
63. **Default load factor for ArrayList?** N/A, no load factor concept, it grows when full.
64. **Can we cast List<String> to List<Object>?** No, generics are invariant.
65. **Type Erasure?** Generics are removed at compile time for backward compatibility.
66. **List<?> vs List<Object>?** `?` is wildcard (read-only), `Object` means accepts specifically Object type.
67. **PECS principle?** Producer Extends, Consumer Super.
68. **Why no generic arrays?** Arrays know type at runtime, Generics erase type at runtime. Incompatible.
69. **Dictionary class?** Obsolete abstract parent of Hashtable.
70. **Difference between clear() and re-initializing?** `clear()` keeps capacity, `new` allocates new memory.
71. **remove() by object vs index in ArrayList?** `remove(int)` uses index. `remove(Object)` loops and removes first occurrence.
72. **ArrayList with capacity 0?** Yes, valid. Grows on first add.
73. **Java 8 Streams and Collections?** Collections provide data, Streams process it functional-style.
74. **stream() vs parallelStream()?** parallelStream divides work across CPU cores (ForkJoinPool).
75. **When to NOT use parallelStream?** Small datasets, stateful operations, IO bound tasks.
76. **Spliterator?** Iterator designed for parallel traversal.
77. **Characteristics of Spliterator?** SIZED, ORDERED, DISTINCT, etc.
78. **RandomAccess interface?** Marker interface indicating fast O(1) element access (ArrayList has it, LinkedList doesn't).
79. **Cloneable interface in Collections?** Most implement it, but perform Shallow Copy.
80. **Deep Copy of List?** Must iterate and clone/copy each object manually.
81. **java.util.concurrent collections?** `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`.
82. **SkipListMap?** `ConcurrentSkipListMap` is the concurrent equivalent of `TreeMap`.
83. **How SkipList works?** Linked list with multi-level express lanes for O(log n) search.
84. **DelayQueue?** Elements can only be taken when their delay expires.
85. **SynchronousQueue?** Capacity 0. Put blocks until take.
86. **ArrayBlockingQueue vs LinkedBlockingQueue?** Fixed size (Array) vs Optionally bounded (Linked).
87. **Deque implementations?** `ArrayDeque`, `LinkedList`.
88. **Stack methods on Deque?** `push()`, `pop()`.
89. **Why Deque over Stack?** Stack extends Vector (locks). Deque is lock-free.
90. **Queue offer vs add?** `offer` returns false if full. `add` throws exception.
91. **Difference between set() and add() in List?** `set` replaces. `add` shifts and inserts.
92. **Best collection for Dictionary/Spell checker?** `HashSet` or Trie (custom).
93. **What happens if hashcode returns random number?** You can't find the object again.
94. **Null key in TreeMap?** Throws NPE (uses compareTo).
95. **Does List support null?** Yes, ArrayList/LinkedList support multiple nulls.
96. **Does Deque support null?** `LinkedList` does, `ArrayDeque` does NOT.
97. **Can Iterator move backwards?** No, use `ListIterator`.
98. **Does Iterator.remove() modify size?** Yes.
99. **How to sort list in reverse?** `Collections.sort(list, Collections.reverseOrder())`.
100. **Guava / Apache Commons?** Popular external libraries offering `Multimap`, `BiMap`, etc.
