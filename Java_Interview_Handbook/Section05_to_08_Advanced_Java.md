# Java Interview Mastery Handbook: Sections 5 to 8

## Section 5 - `equals()`, `hashCode()` and Hashing

### 1. Definition + Why It Exists
In Java, every class implicitly inherits from the `Object` class, which provides default implementations for `equals()` and `hashCode()`. 
- **`equals()`**: Used to compare two objects for logical equivalence.
- **`hashCode()`**: Returns an integer hash code value for the object, used to efficiently distribute objects across buckets in hash-based collections like `HashMap`, `HashSet`, and `Hashtable`.

**Why they exist**: Comparing objects using `==` only checks memory references (identity). To compare the actual *content* of objects (value equality), we must override `equals()`. Hashing collections require a fast mechanism to categorize objects, hence `hashCode()`.

### 2. Internal Working & The Contracts
**The `equals()` Contract:**
1. **Reflexive**: `x.equals(x)` must return `true`.
2. **Symmetric**: `x.equals(y)` must return `true` if and only if `y.equals(x)` returns `true`.
3. **Transitive**: If `x.equals(y)` and `y.equals(z)` are `true`, then `x.equals(z)` must be `true`.
4. **Consistent**: Multiple invocations of `x.equals(y)` consistently return `true` or `false`, provided no information used in equals comparisons is modified.
5. **Null**: `x.equals(null)` must return `false`.

**The `hashCode()` Contract:**
1. **Consistency**: Whenever invoked on the same object more than once during an execution, it must consistently return the same integer, provided no info used in equals is modified.
2. **Equal Objects**: If two objects are equal according to `equals(Object)`, then calling `hashCode()` on each must produce the same integer result.
3. **Unequal Objects**: If two objects are unequal, they are *not required* to have distinct hash codes (though distinct hash codes improve performance).

### 3. Real-World Analogy
**Analogy**: A Post Office Box System.
- **hashCode()** is the Zip Code (tells you which city/post office bucket to go to).
- **equals()** is checking the Exact Name and House Number on the letter once you are at the correct post office.
If you change your zip code (`hashCode`), the mailman drops your letter in the wrong city, and even if your name (`equals`) is right, nobody will find your mail!

### 4. Why You MUST Override Both Together
If you override `equals()` but NOT `hashCode()`, two logically equal objects might have different hash codes. In a `HashMap`, they will be placed in different buckets. When you try to retrieve the object using an equal object as a key, `HashMap` will look in the wrong bucket and return `null`.

### 5. How `HashMap` Uses `hashCode()` + `equals()`
**Time Complexity**: O(1) average for `get`/`put`. O(n) worst-case (or O(log n) with TreeBins in Java 8+).
**Space Complexity**: O(n).

**Internal Working (Dry Run)**:
1. `map.put(key, value)`
2. Calculate hash: `int hash = hash(key.hashCode())` (bit spread to avoid collisions).
3. Determine bucket index: `index = (n - 1) & hash`.
4. Go to bucket array at `index`.
5. If empty, place node there.
6. If occupied (Collision), traverse the Linked List (or Red-Black Tree):
   - For each node: check if `node.hash == hash && (node.key == key || key.equals(node.key))`.
   - If true, replace value.
   - If false, append to the end.

### 6. Broken Contract Scenarios (Interview Traps)
- **Trap 1: Overriding `equals` but not `hashCode`**. Result: Objects are equal, but go to different HashMap buckets. Memory leak in Maps.
- **Trap 2: Mutable Keys in HashMap**. If you change a key's fields after putting it in a Map, its `hashCode` changes. The Map will never find it again (Memory Leak).
- **Trap 3: Using `instanceof` vs `getClass()` in `equals`**. `instanceof` violates symmetry when dealing with subclasses that add state.

### 7. Implementing Correct `equals()` and `hashCode()`

```java
import java.util.Objects;

public class Employee {
    private int id;
    private String name;

    // IDE Generated + Manual best practices
    @Override
    public boolean equals(Object o) {
        // 1. Same instance check
        if (this == o) return true;
        // 2. Null and Class check
        if (o == null || getClass() != o.getClass()) return false;
        // 3. Cast and compare fields
        Employee employee = (Employee) o;
        return id == employee.id && Objects.equals(name, employee.name);
    }

    @Override
    public int hashCode() {
        // Uses Arrays.hashCode internally
        return Objects.hash(id, name);
    }
}
```

### 8. 20 Tricky Interview Questions
**Q1. What happens if you override `equals` but not `hashCode`?**
*Ans:* Objects that are logically equal will have different hash codes (inherited from `Object`). In a `HashMap` or `HashSet`, you won't be able to retrieve or find the object, leading to duplicates and memory leaks.

**Q2. Can two different objects have the same `hashCode`?**
*Ans:* Yes, this is called a hash collision. `HashMap` handles this by chaining nodes in a Linked List (or Tree) at the same bucket index.

**Q3. Can we make `hashCode` return a constant value, like `1`?**
*Ans:* Yes, it doesn't violate the contract. However, it destroys performance. All objects will fall into a single bucket, reducing the `HashMap` to a LinkedList with O(n) lookup time.

**Q4. What is the difference between `==` and `equals()`?**
*Ans:* `==` checks reference/memory address identity. `equals()` checks logical value equality.

**Q5. Can `HashMap` have a `null` key?**
*Ans:* Yes, exactly one `null` key is allowed. It is always stored in bucket index `0`.

**Q6. Can `ConcurrentHashMap` have a `null` key?**
*Ans:* No. Both keys and values cannot be `null` to avoid ambiguity in concurrent environments.

**Q7. Explain the Java 8 `HashMap` improvement for collisions.**
*Ans:* Once a bucket's linked list reaches a threshold (8 nodes) and array size is >= 64, it transforms into a Red-Black Tree, improving worst-case search time from O(n) to O(log n).

**Q8. Why is `String` a popular `HashMap` key?**
*Ans:* It is immutable, caches its hash code, and correctly implements equals/hashCode. Immutable keys guarantee the hash code won't change after insertion.

**Q9. What happens if a `HashMap` key's state changes after insertion?**
*Ans:* Its calculated `hashCode` will change. `HashMap` will look in the wrong bucket, making the entry lost/unretrievable, leading to a memory leak.

**Q10. How does `IdentityHashMap` differ from `HashMap`?**
*Ans:* It uses reference equality (`==`) instead of `equals()` for comparing keys, and uses `System.identityHashCode()` instead of `hashCode()`.

**Q11. How does `Objects.hash()` work?**
*Ans:* It accepts varargs (`Object...`), wraps them in an array, and calls `Arrays.hashCode()`, combining the hash codes of all passed fields with a prime multiplier (usually 31).

**Q12. Why is the prime number 31 used in `hashCode` calculations?**
*Ans:* 31 is prime and odd. It has a nice property: `31 * i == (i << 5) - i`. Modern VMs optimize this multiplication into bit shifts.

**Q13. What is `Load Factor` in `HashMap`?**
*Ans:* It determines when the hash table should resize. Default is 0.75. When `(entries > capacity * load_factor)`, the capacity is doubled.

**Q14. How does resizing (`rehashing`) work in `HashMap`?**
*Ans:* A new array of double the size is created. All existing entries are re-hashed and moved to the new array. In Java 8, bitwise operations efficiently move nodes without fully recalculating hash codes.

**Q15. Is `hashCode` generated based on the memory address?**
*Ans:* In HotSpot JVM, the default `hashCode` (identity hashcode) is *not* the memory address. It is generated using thread-local random states or other algorithms, stored in the object header.

**Q16. If `x.equals(y)` is false, can `x.hashCode() == y.hashCode()` be true?**
*Ans:* Yes, this is a valid collision.

**Q17. Should we use `instanceof` or `getClass()` in `equals()`?**
*Ans:* `getClass()` is strictly exact and better if subclasses can add state. `instanceof` allows subclass comparison but can easily break the symmetry contract.

**Q18. How to compare two objects ignoring case without Strings?**
*Ans:* You must implement custom logic in `equals()` converting fields to lowercase, and similarly use lowercase strings in `hashCode()`.

**Q19. What is `System.identityHashCode(obj)`?**
*Ans:* Returns the hash code as if it was not overridden (the default `Object.hashCode()` behavior).

**Q20. What is a Memory Leak in Java regarding `HashMap`?**
*Ans:* Keeping strong references to objects in a Map without removing them, or using mutable keys that get lost. `WeakHashMap` can be a solution.

---

## Section 6 - Exception Handling

### 1. Definition + Why It Exists
Exception handling is a mechanism to handle runtime errors, ensuring the normal flow of the application is maintained. 
**Why it exists:** To separate error-handling code from regular business logic, preventing application crashes.

### 2. Throwable Hierarchy (ASCII Diagram)
```text
                  Object
                    |
                Throwable
                /       \
            Error      Exception
           /    \        /      \
        OOM  Stack  Checked   Unchecked (RuntimeException)
                         |             |
               IOException   NullPointerException
               SQLException  IllegalArgumentException
```
- **Error**: Irrecoverable issues (JVM crash, Out of Memory). Do not catch.
- **Checked Exception**: Checked at compile time. Must be caught or declared (`throws`).
- **Unchecked Exception**: Extends `RuntimeException`. Occurs at runtime (e.g., programming bugs).

### 3. Rules & Mechanisms
**`try-catch-finally`**
- Execution order: `try` -> if exception -> `catch` -> ALWAYS `finally`.
- **`finally` always executes**, EXCEPT when:
  1. `System.exit()` is called.
  2. The JVM crashes.
  3. Infinite loop / deadlock in the `try` block.
  4. Power failure.

**`try-with-resources` (Java 7)**
Automatically closes resources that implement `AutoCloseable` or `Closeable`. No `finally` block needed.

```java
try (BufferedReader br = new BufferedReader(new FileReader("test.txt"))) {
    System.out.println(br.readLine());
} catch (IOException e) {
    e.printStackTrace();
} // br is closed automatically here!
```

**`throw` vs `throws`**
- `throw`: Used explicitly inside a method to throw an exception object.
- `throws`: Used in a method signature to declare that the method might throw exceptions.

### 4. Custom Exceptions & Best Practices
```java
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
    public UserNotFoundException(String message, Throwable cause) {
        super(message, cause); // Exception Chaining
    }
}
```
**Best Practices:**
- Never swallow exceptions (empty catch block).
- Catch specific exceptions first, generic `Exception` last.
- Do not use exceptions for flow control (expensive stack trace generation).
- Always use Exception Chaining (`initCause` or constructor) when wrapping exceptions to preserve the original stack trace.

### 5. 30 Interview Questions
**Q1. Difference between Error and Exception?**
*Ans:* Errors indicate serious problems (JVM-level) that apps shouldn't try to catch. Exceptions indicate conditions a reasonable app might want to catch and recover from.

**Q2. Checked vs Unchecked Exception?**
*Ans:* Checked exceptions are validated at compile-time (e.g., `IOException`). Unchecked extend `RuntimeException` and are not validated at compile-time (e.g., `NullPointerException`).

**Q3. Does `finally` block always execute?**
*Ans:* Yes, almost always. Exceptions: `System.exit(0)`, JVM crash, or thread death.

**Q4. What happens if `return` is in both `try` and `finally`?**
*Ans:* The `return` in `finally` overrides the `return` in `try`! (Interview trap).

**Q5. Can we have `try` without `catch`?**
*Ans:* Yes, but it must have a `finally` block, or be a `try-with-resources`.

**Q6. What is Exception Chaining?**
*Ans:* Wrapping one exception inside another to provide higher-level abstraction while maintaining the original cause/stack trace (`new CustomException("msg", originalException)`).

**Q7. Explain try-with-resources.**
*Ans:* Introduced in Java 7, it guarantees that resources implementing `AutoCloseable` are closed at the end of the statement, avoiding manual `finally` block resource leaks.

**Q8. What is Multi-catch block?**
*Ans:* Java 7 feature to catch multiple exceptions in one block: `catch (IOException | SQLException e)`.

**Q9. Why shouldn't you catch `Throwable` or `Error`?**
*Ans:* Errors like `OutOfMemoryError` leave the JVM in an unstable state. Recovering from them is dangerous and often impossible.

**Q10. Difference between `throw` and `throws`?**
*Ans:* `throw` actually throws the exception instance. `throws` is part of method signature indicating potential exceptions.

**Q11. Can we throw an Unchecked Exception in a method without declaring it in `throws`?**
*Ans:* Yes, the compiler does not force `throws` declarations for `RuntimeException`.

**Q12. What happens if a catch block throws an exception?**
*Ans:* The remaining catch blocks are skipped, the `finally` block executes, and the new exception propagates up the call stack.

**Q13. How to create a Custom Checked Exception?**
*Ans:* Create a class extending `Exception` (not `RuntimeException`).

**Q14. What is `ClassNotFoundException` vs `NoClassDefFoundError`?**
*Ans:* `ClassNotFoundException` is thrown when explicitly loading a class via reflection (`Class.forName`) and it's missing. `NoClassDefFoundError` is an Error thrown when a class was present at compile time but is missing at runtime during implicit linking.

**Q15. Can you override a method to throw a broader exception?**
*Ans:* No. An overridden method in a subclass cannot throw new checked exceptions or broader checked exceptions than the superclass method. It can throw narrower ones or unchecked exceptions.

**Q16. Is it good practice to use Exceptions for control flow?**
*Ans:* No. Creating exceptions is extremely slow because the JVM has to capture the entire stack trace.

**Q17. What causes `StackOverflowError`?**
*Ans:* Infinite or excessively deep method recursion causing the thread's call stack memory to be exhausted.

**Q18. What causes `OutOfMemoryError`?**
*Ans:* Heap space exhaustion, where the Garbage Collector cannot free enough memory for new object allocation.

**Q19. What is Suppressed Exception?**
*Ans:* When a try-with-resources block throws an exception, and the `close()` method also throws an exception, the `close()` exception is added as a "suppressed" exception to the primary exception.

**Q20. What is `NullPointerException`?**
*Ans:* Thrown when attempting to call an instance method or access a field on a `null` object reference.

**Q21. How to avoid `NullPointerException`?**
*Ans:* Use `java.util.Optional`, add null checks, use `@NonNull` annotations, and call `equals()` on known constants (e.g., `"CONSTANT".equals(variable)`).

**Q22. Can an interface method declare `throws Exception`?**
*Ans:* Yes, but it forces all implementations to handle or declare it, which is poor design.

**Q23. What happens to the thread if an exception is completely unhandled?**
*Ans:* The thread terminates. If it's the main thread, the application exits.

**Q24. How to set a global exception handler?**
*Ans:* Use `Thread.setDefaultUncaughtExceptionHandler()`.

**Q25. Can `try-with-resources` have `catch` and `finally`?**
*Ans:* Yes. The resource is closed *before* the `catch` or `finally` blocks execute.

**Q26. What happens if both `try` and `catch` return a value?**
*Ans:* Depends on execution. If `try` completes, it returns. If exception occurs, `catch` returns.

**Q27. Can we have multiple `catch` blocks for the same exception?**
*Ans:* No, compile-time error.

**Q28. Order of catch blocks matters?**
*Ans:* Yes. Subclasses (specific exceptions) must come before superclasses (generic exceptions), else compile-time error.

**Q29. What is `ClassCastException`?**
*Ans:* Thrown when attempting to downcast an object reference to a type that it is not an instance of.

**Q30. Does garbage collection happen for exception objects?**
*Ans:* Yes, exception objects are regular objects allocated on the heap. They are garbage collected when unreachable.

---

## Section 7 - Multithreading & Concurrency (VERY DETAILED)

### 1. Process vs Thread
- **Process**: An executing instance of a program. Has its own separate memory space (Process Control Block - PCB). Heavyweight.
- **Thread**: A path of execution within a process. Threads within the same process share the same memory (Heap and Method Area) but have their own Stack and Program Counter (Thread Control Block - TCB). Lightweight.

### 2. Thread Lifecycle (ASCII Diagram)
```text
  [ NEW ] --(start())--> [ RUNNABLE ] <----------------+
                             |                         |
               (wait, sleep, join, lock)     (notify, timeout, unlocked)
                             V                         |
                   [ BLOCKED / WAITING / TIMED_WAITING ]
                             |
                   (run method completes)
                             V
                       [ TERMINATED ]
```

### 3. Creating Threads
1. **Extends `Thread`**: Cannot extend other classes.
2. **Implements `Runnable`**: Better design. Can extend another class. Used with Thread pools. No return value.
3. **Implements `Callable<T>`**: Returns a `Future<T>`, can throw checked exceptions. Used with `ExecutorService`.
4. **Lambdas**: Concise way to pass tasks. `new Thread(() -> System.out.println("Running")).start();`

### 4. Synchronization, Locks, and Race Conditions
**Race Condition**: When two or more threads access shared data concurrently and try to change it at the same time, leading to unpredictable results.
**Monitor/Lock**: Every object in Java has an intrinsic lock (monitor). Using `synchronized` requires threads to acquire this lock.

```java
// Synchronized method (locks 'this')
public synchronized void increment() { count++; }

// Synchronized block (locks specific object)
public void incrementBlock() {
    synchronized(this) { count++; }
}
```

### 5. `volatile` Keyword
Guarantees **Visibility** and provides **Happens-Before** relationship.
- Prevents CPU from caching the variable; forces reads/writes directly to main memory.
- Does **NOT** guarantee atomicity (e.g., `count++` is still not thread-safe with just volatile).

### 6. Atomic Classes & CAS
`AtomicInteger`, `AtomicReference`, etc., use **CAS (Compare-And-Swap)** CPU instructions to perform lock-free thread-safe operations.
- CAS works by: "If the current value in memory is X, update it to Y. Otherwise, fail and retry."

### 7. Executors Framework & Thread Pools
Separates task creation from execution. `ThreadPoolExecutor` handles thread lifecycle, queueing, and rejection policies.
- **FixedThreadPool**: Fixed number of threads.
- **CachedThreadPool**: Creates new threads as needed, reuses idle ones. Good for many short-lived tasks.
- **SingleThreadExecutor**: One thread, executes sequentially.
- **ScheduledThreadPool**: For delayed or periodic execution.

### 8. Advanced Concurrency Utilities (`java.util.concurrent`)
- **ReentrantLock**: Advanced alternative to `synchronized`. Supports `tryLock()`, fairness policies, and multiple `Condition` variables.
- **CountDownLatch**: Causes one or more threads to wait until a set of operations in other threads completes. *Cannot be reset*.
- **CyclicBarrier**: Allows a set of threads to all wait for each other to reach a common barrier point. *Can be reset*.
- **Semaphore**: Maintains a set of permits. Used to control access to a restricted resource (e.g., max 5 database connections).
- **CompletableFuture**: Modern async programming tool. Chaining (`thenApply`, `thenCompose`), combining (`thenCombine`), and handling errors (`exceptionally`).
- **ThreadLocal**: Provides thread-local variables. Each thread accessing it gets its own independent copy. *Warning: Can cause memory leaks in app servers if `remove()` is not called.*

### 9. Deadlock
**Definition**: Two or more threads are blocked forever, waiting for each other to release locks.
**Example**: Thread 1 locks A, waits for B. Thread 2 locks B, waits for A.
**Prevention**: Always acquire locks in the exact same order.

---
### 10. 50 Multithreading Interview Questions

**Q1. Thread vs Process?**
*Ans:* Processes have isolated memory, are heavy to create. Threads share memory within a process, are lightweight.

**Q2. Runnable vs Callable?**
*Ans:* `Runnable.run()` returns `void` and cannot throw checked exceptions. `Callable.call()` returns a generic value (`Future`) and can throw exceptions.

**Q3. What is a Future?**
*Ans:* A placeholder object representing the result of an asynchronous computation. Provides `get()`, `cancel()`, `isDone()`.

**Q4. Difference between `wait()` and `sleep()`?**
*Ans:* `wait()` belongs to `Object`, releases the lock, and must be called in a synchronized block. `sleep()` belongs to `Thread`, keeps the lock, and pauses execution.

**Q5. Can you call `run()` directly instead of `start()`?**
*Ans:* Yes, but it will execute synchronously in the current thread, completely defeating the purpose of multithreading.

**Q6. What is `volatile`?**
*Ans:* Ensures visibility of variables across threads by bypassing CPU cache and writing directly to main memory. Does not ensure atomicity.

**Q7. What is a Race Condition?**
*Ans:* Unpredictable behavior when multiple threads concurrently read and write shared data without synchronization.

**Q8. What is Deadlock?**
*Ans:* A circular waiting condition where two or more threads are permanently blocked waiting for locks held by each other.

**Q9. How to detect Deadlock?**
*Ans:* Take a thread dump using tools like `jstack`, VisualVM, or JConsole. It explicitly reports "Found one Java-level deadlock".

**Q10. How to prevent Deadlock?**
*Ans:* 1. Lock ordering (acquire locks in same order). 2. Lock timeout (`tryLock`). 3. Avoid nested locks.

**Q11. What is Starvation?**
*Ans:* A thread is perpetually denied access to a shared resource because other threads keep acquiring it (e.g., low priority thread).

**Q12. What is Livelock?**
*Ans:* Threads are actively changing states in response to each other, but making no actual progress (e.g., two people stepping aside in a hallway repeatedly).

**Q13. Difference between `synchronized` block and method?**
*Ans:* Method locks the entire object (`this` or `Class`). Block allows locking specific objects and reducing the locked scope for better performance.

**Q14. What lock is acquired for a `static synchronized` method?**
*Ans:* The `Class` object lock (e.g., `MyClass.class`), not the instance lock.

**Q15. Can two threads call a static synchronized and a non-static synchronized method concurrently?**
*Ans:* Yes. They acquire different locks (Class lock vs Instance lock).

**Q16. What is ThreadPoolExecutor?**
*Ans:* Core class for executing tasks. Configured with core pool size, max pool size, keep-alive time, and a blocking queue.

**Q17. ExecutorService vs `Executors`?**
*Ans:* `ExecutorService` is the interface. `Executors` is a factory class providing utility methods to create pre-configured thread pools.

**Q18. Why use Thread Pools instead of `new Thread()`?**
*Ans:* Thread creation is expensive. Pools reuse threads, control resource usage, prevent memory exhaustion, and manage task queuing.

**Q19. What is `ReentrantLock`?**
*Ans:* A lock that allows a thread to re-acquire a lock it already holds without deadlocking. It provides `tryLock()`, interruptible locks, and fairness.

**Q20. What is Fairness in ReentrantLock?**
*Ans:* If true, the lock is granted to the longest-waiting thread. If false (default), barging is allowed for better throughput.

**Q21. `ReadWriteLock` use case?**
*Ans:* Allows multiple concurrent readers, but only one writer. Good for read-heavy caches.

**Q22. What is `CountDownLatch`?**
*Ans:* Synchronization aid allowing threads to wait until a counter reaches zero (`await()`). Other threads decrement it (`countDown()`). Cannot be reused.

**Q23. What is `CyclicBarrier`?**
*Ans:* Allows a set of threads to wait for each other at a common barrier. Once all arrive, they proceed. Can be reset and reused.

**Q24. `Semaphore` use case?**
*Ans:* Limits the number of concurrent threads accessing a specific resource using a set of permits (`acquire()`, `release()`).

**Q25. What is `ConcurrentHashMap`?**
*Ans:* Thread-safe map. In Java 8, it uses CAS and synchronizes only on the specific node/bucket, not the whole map (lock striping), providing high concurrency.

**Q26. `CopyOnWriteArrayList`?**
*Ans:* Thread-safe list. Mutative operations (`add`, `set`) create a fresh copy of the underlying array. Fast for iteration/reads, slow for writes.

**Q27. What is `ThreadLocal`?**
*Ans:* Provides thread-local variables. Each thread has its own isolated instance. Useful for passing context (like user ID or Transaction ID) without method arguments.

**Q28. Why does `ThreadLocal` cause Memory Leaks?**
*Ans:* In app servers, threads are pooled. If `ThreadLocal.remove()` is not called, the pooled thread keeps the reference to the object forever, preventing GC of the webapp classloader.

**Q29. What is CAS (Compare and Swap)?**
*Ans:* Hardware-level atomic instruction used by Atomic classes. It updates a value only if the current value matches the expected value.

**Q30. `AtomicInteger` vs `volatile`?**
*Ans:* `volatile` only ensures visibility. `AtomicInteger` provides thread-safe, lock-free atomic operations like `incrementAndGet()` using CAS.

**Q31. Difference between `notify()` and `notifyAll()`?**
*Ans:* `notify()` wakes up one random waiting thread. `notifyAll()` wakes up all waiting threads (they then compete for the lock).

**Q32. Why must `wait()` be inside a `while` loop?**
*Ans:* To prevent "Spurious Wakeups". The thread must re-check the condition after waking up to ensure it's truly safe to proceed.

**Q33. Explain `CompletableFuture`.**
*Ans:* Enhances `Future` by allowing non-blocking callbacks, combining multiple futures, and async pipelines.

**Q34. `thenApply()` vs `thenAccept()` in `CompletableFuture`?**
*Ans:* `thenApply()` transforms the result and returns a new value. `thenAccept()` consumes the result and returns `void`.

**Q35. What is `ForkJoinPool`?**
*Ans:* Specialized thread pool using Work-Stealing algorithm. Used by Parallel Streams and `CompletableFuture` by default. Designed for recursive task splitting.

**Q36. What is Work-Stealing?**
*Ans:* Idle threads in a pool steal tasks from the end of busy threads' queues to maximize CPU utilization.

**Q37. Can we catch exceptions thrown by another thread?**
*Ans:* Not with standard try-catch. You must use `Thread.setDefaultUncaughtExceptionHandler()`.

**Q38. What is a Daemon Thread?**
*Ans:* A low-priority background thread (like GC). The JVM shuts down when only daemon threads remain. Set via `setDaemon(true)` before starting.

**Q39. `yield()` vs `sleep()`?**
*Ans:* `sleep()` pauses for a specific time. `yield()` is a hint to the scheduler that the current thread is willing to yield its current use of a processor.

**Q40. `join()` method?**
*Ans:* `threadA.join()` makes the current thread wait until `threadA` terminates.

**Q41. Thread Interruption?**
*Ans:* `thread.interrupt()` sets the interrupt flag. If the thread is blocked in `wait/sleep/join`, it throws `InterruptedException` and clears the flag.

**Q42. Is `i++` thread-safe?**
*Ans:* No. It is 3 operations: Read, Modify, Write. Requires synchronization or `AtomicInteger`.

**Q43. What is `LockSupport`?**
*Ans:* Low-level threading utility providing `park()` and `unpark()` to block and unblock threads. Used to build high-level locks.

**Q44. What is a Monitor in Java?**
*Ans:* An synchronization construct tied to every object. Comprises a mutex (lock) and wait sets (for `wait/notify`).

**Q45. `submit()` vs `execute()` in ExecutorService?**
*Ans:* `execute()` takes a `Runnable` and returns nothing. `submit()` takes `Runnable` or `Callable` and returns a `Future`.

**Q46. How to shut down an `ExecutorService`?**
*Ans:* `shutdown()` initiates orderly shutdown (no new tasks). `shutdownNow()` tries to cancel running tasks immediately.

**Q47. What happens if queue is full in `ThreadPoolExecutor`?**
*Ans:* It creates new threads up to `maximumPoolSize`. If max threads are reached, it uses the `RejectedExecutionHandler` (e.g., throws `RejectedExecutionException`).

**Q48. `Phaser` vs `CyclicBarrier`?**
*Ans:* `Phaser` is more flexible; the number of registered parties can change dynamically over time.

**Q49. Double-Checked Locking in Singleton?**
*Ans:* Used to initialize a singleton safely and lazily. Requires the instance variable to be `volatile` to prevent partially constructed objects due to instruction reordering.

**Q50. `Exchanger` utility?**
*Ans:* A synchronization point where two threads can exchange objects data bidirectionally.

---

## Section 8 - Memory Management & JVM Internals

### 1. JVM Architecture (ASCII Diagram)
```text
 +---------------------------------------------------+
 |                   Class Loader                    |
 +---------------------------------------------------+
                          |
 +---------------------------------------------------+
 |                Runtime Data Areas                 |
 |                                                   |
 |  +-------+ +-------+ +-----+ +----+ +-----------+ |
 |  |Method | | Heap  | |Stack| | PC | |Native Mthd| |
 |  | Area  | |       | |     | | Reg| |   Stack   | |
 |  +-------+ +-------+ +-----+ +----+ +-----------+ |
 +---------------------------------------------------+
                          |
 +---------------------------------------------------+
 |               Execution Engine                    |
 |  [Interpreter]  [JIT Compiler]  [Garbage Coll]    |
 +---------------------------------------------------+
```

### 2. Runtime Data Areas
1. **Method Area (Metaspace since Java 8)**: Stores class-level data, metadata, static variables, and constant pool. Shared by all threads. Native memory.
2. **Heap**: Stores all instantiated objects and arrays. Shared by all threads. Garbage collected.
3. **Stack**: Stores local variables, method call frames, and partial results. **One per thread**.
4. **PC Register**: Program Counter. Holds the address of the currently executing JVM instruction. **One per thread**.
5. **Native Method Stack**: Stores state of native (C/C++) method calls. **One per thread**.

### 3. Heap Generation Architecture (ASCII Diagram)
```text
 +-----------------------------------------+
 |                  Heap                   |
 | +----------------+ +------------------+ |
 | |   Young Gen    | |     Old Gen      | |
 | | +----+ +--+ +--+ | +--------------+ | |
 | | |Eden| |S0| |S1| | |   Tenured    | | |
 | | +----+ +--+ +--+ | +--------------+ | |
 | +----------------+ +------------------+ |
 +-----------------------------------------+
```
- **Eden**: All new objects are allocated here.
- **Survivor Spaces (S0 & S1)**: Objects that survive a Minor GC are moved here.
- **Old Gen (Tenured)**: Long-lived objects promoted from Survivor space after surviving multiple GC cycles.

### 4. Garbage Collection Mechanisms
- **GC Roots**: Starting points for tracing object reachability. Includes Active Threads, Local Variables in Stack, Static Variables.
- **Mark-and-Sweep**: Traverses from GC roots, marks reachable objects, sweeps (deletes) unmarked objects. Leaves memory fragmented.
- **Mark-Compact**: Same as above, but compacts live objects to the start of memory to prevent fragmentation.
- **Minor GC**: Cleans Young Gen. Fast. Causes "Stop-The-World" (STW) pause.
- **Major / Full GC**: Cleans Old Gen (and often entire Heap). Slower, longer STW pauses.

### 5. GC Algorithms
- **Serial GC**: Single-threaded. For small client apps.
- **Parallel GC**: (Default till Java 8). Multiple threads for Minor GC. Maximizes throughput.
- **G1GC (Garbage First)**: (Default since Java 9). Divides heap into equal regions. Does concurrent marking. Prioritizes regions with the most garbage. Good for predictable pause times.
- **ZGC (Z Garbage Collector)**: Low latency, scalable. Pause times under 1 millisecond. Works on multi-terabyte heaps using colored pointers and load barriers.

### 6. Reference Types
- **Strong**: `String s = new String("A")`. Never collected if reachable.
- **Soft**: Collected *only* if JVM is absolutely running out of memory (useful for Caches).
- **Weak**: Collected during the *very next* GC cycle if no strong references exist (`WeakHashMap`).
- **Phantom**: Cannot be accessed directly. Used to schedule post-mortem cleanup actions (alternative to `finalize()`).

### 7. Class Loading
Parent Delegation Model prevents security breaches (like injecting a fake `java.lang.String`).
1. **Bootstrap ClassLoader**: Loads core java classes (`rt.jar`, `java.lang.*`). Written in native code.
2. **Extension ClassLoader**: Loads classes from `jre/lib/ext`.
3. **Application ClassLoader**: Loads classes from application Classpath.

### 8. JIT Compiler
Just-In-Time compiler translates Java bytecode to native machine code at runtime for performance.
- **C1 (Client)**: Fast compilation, less optimization.
- **C2 (Server)**: Slower compilation, aggressive optimizations (Inlining, Loop Unrolling, Escape Analysis).
- **Tiered Compilation**: Java 8+. Starts with interpreted/C1 for fast startup, then hot spots are re-compiled with C2 for peak performance.

### 9. Memory Leaks & OOM
- **Java Heap Space OOM**: Heap is full. Solution: Find leak or increase `-Xmx`.
- **Metaspace OOM**: Too many classes loaded. Often happens in app servers during hot-redeploy. Increase `-XX:MaxMetaspaceSize`.
- **GC Overhead Limit Exceeded**: 98% of time spent in GC, recovering less than 2% of heap.
- **Tools**: `jmap` (heap dump), `jstack` (thread dump), VisualVM, Eclipse MAT.

### 10. JVM Flags Cheat Sheet
- `-Xms`: Initial heap size (e.g., `-Xms2g`)
- `-Xmx`: Max heap size (e.g., `-Xmx2g`) (Best practice: set Xms = Xmx to avoid resizing pauses)
- `-Xss`: Thread stack size (e.g., `-Xss1m`)
- `-XX:MaxMetaspaceSize=256m`: Max Metaspace.
- `-XX:+UseG1GC`: Use G1 Garbage Collector.
- `-XX:+HeapDumpOnOutOfMemoryError`: Auto-generate heap dump on crash.

---
### 11. 30 JVM Interview Questions

**Q1. What is JVM, JRE, and JDK?**
*Ans:* JVM executes bytecode. JRE = JVM + Core Libraries. JDK = JRE + Development Tools (compiler `javac`, debugger).

**Q2. Stack vs Heap memory?**
*Ans:* Stack stores local variables, method calls, thread-specific. Heap stores objects, shared globally. Stack is fast, Heap requires GC.

**Q3. Does Java have pointers?**
*Ans:* Java has references, not pointers. You cannot do pointer arithmetic or directly access memory addresses.

**Q4. What is a GC Root?**
*Ans:* An object accessible from outside the heap. Static variables, local stack variables, active threads, JNI references.

**Q5. How does GC detect garbage?**
*Ans:* Reachability analysis. It traverses references from GC Roots. Unreachable objects are marked as garbage.

**Q6. What is Stop-The-World (STW)?**
*Ans:* A phase where all application threads are completely paused to allow the GC to safely work on memory.

**Q7. Explain G1GC.**
*Ans:* Garbage First GC. Splits heap into small regions. Concurrently marks live objects. Reclaims regions with mostly garbage first to meet user-defined pause time goals.

**Q8. What is Escape Analysis?**
*Ans:* JIT compiler optimization. If an object is created inside a method and never escapes it, the JIT might allocate it on the Stack instead of the Heap, eliminating GC overhead.

**Q9. What causes `OutOfMemoryError: Java heap space`?**
*Ans:* Application is generating new objects faster than GC can collect them, or a memory leak is holding strong references indefinitely.

**Q10. What is a Memory Leak in Java?**
*Ans:* Objects are no longer needed by the app logic but are still referenced by something (like an ever-growing static `HashMap`), preventing GC.

**Q11. How do you troubleshoot a Memory Leak?**
*Ans:* 1. Enable `-XX:+HeapDumpOnOutOfMemoryError`. 2. Reproduce OOM. 3. Open `.hprof` heap dump file in Eclipse MAT or VisualVM. 4. Look for the "Dominator Tree" or "Retained Size" to find the leak suspect.

**Q12. What is `Metaspace`?**
*Ans:* Replaced `PermGen` in Java 8. Stores class metadata. Lives in native memory, not the Java Heap. Auto-scales up to OS limits by default.

**Q13. Difference between Minor and Major GC?**
*Ans:* Minor cleans Young Gen (Eden/Survivor). Major/Full cleans Old Gen (and Young). Major is slower.

**Q14. What is the Parent Delegation Model?**
*Ans:* When a ClassLoader needs to load a class, it delegates the request to its parent ClassLoader first. If the parent fails, it tries to load it. Prevents core class overriding.

**Q15. Why was `finalize()` deprecated?**
*Ans:* Unpredictable execution time, performance penalties, can resurrect objects (security risk). Replaced by `Cleaner` and `PhantomReference`.

**Q16. WeakReference vs SoftReference?**
*Ans:* SoftReferences survive until the JVM is desperate for memory. WeakReferences are killed on the very next GC cycle, regardless of memory pressure.

**Q17. What is `System.gc()`?**
*Ans:* A request/suggestion to the JVM to run garbage collection. The JVM may ignore it. Bad practice to call it in production.

**Q18. What is String Pool? Where does it live?**
*Ans:* A cache of String literals. In Java 8+, it lives in the normal Heap memory, so it can be garbage collected if strings are no longer referenced.

**Q19. Explain ZGC (Z Garbage Collector).**
*Ans:* Ultra-low latency GC introduced in Java 11. Pauses are < 1ms. Uses colored pointers and load barriers to do almost all work concurrently with app threads.

**Q20. What is `OutOfMemoryError: GC Overhead limit exceeded`?**
*Ans:* JVM spends >98% of its time doing GC and frees <2% memory. It's the JVM throwing its hands up saying "I'm thrashing, help!".

**Q21. How does the JVM handle method overloading resolution?**
*Ans:* Compile-time static binding. The compiler looks at the reference type and arguments to determine the exact method.

**Q22. How does JVM handle method overriding?**
*Ans:* Runtime dynamic binding (Virtual Method Dispatch). The JVM looks at the actual object instance on the heap to call the correct method.

**Q23. What is Tiered Compilation?**
*Ans:* Using C1 compiler for fast startup, profiling the code, and then passing hot methods to C2 compiler for heavy optimizations.

**Q24. What is Method Inlining?**
*Ans:* JIT optimization replacing a method call with the actual body of the method to avoid call-stack overhead.

**Q25. What is `jstack` used for?**
*Ans:* Generates a thread dump. Shows exact stack traces of all threads. Used to find Deadlocks, blocked threads, and CPU spikes.

**Q26. What happens if an exception is thrown inside `finalize()`?**
*Ans:* The exception is completely ignored by the JVM and object destruction halts.

**Q27. Can you force an OutOfMemoryError?**
*Ans:* Yes. `List<byte[]> list = new ArrayList<>(); while(true) { list.add(new byte[10_000_000]); }`

**Q28. What is the TLAB (Thread Local Allocation Buffer)?**
*Ans:* A small private memory area in Eden space for each thread. Allows lock-free, highly efficient object allocation.

**Q29. What is a "Safe Point" in JVM?**
*Ans:* A specific state where all threads are paused and their memory maps are consistent, allowing the JVM to safely run a STW Garbage Collection.

**Q30. Why is setting `-Xms` and `-Xmx` to the same value recommended?**
*Ans:* Prevents the JVM from constantly requesting and releasing memory back to the OS, avoiding expensive heap resizing pauses during application runtime.
