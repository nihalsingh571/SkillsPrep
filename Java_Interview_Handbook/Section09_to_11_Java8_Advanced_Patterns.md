# Java Interview Mastery Handbook: Sections 9, 10, and 11

## Section 9 - Modern Java (Java 8+ Features)

### 9.1 Lambda Expressions
**Definition & Why it exists:** A lambda expression is an anonymous (unnamed) block of code that takes parameters and returns a value. It exists to enable functional programming in Java, drastically reducing boilerplate code (replacing anonymous inner classes) and facilitating the use of the Streams API.

**Internal Working:** At compile time, the Java compiler uses *invokedynamic* to defer the creation of the lambda to runtime. A `CallSite` is linked to a factory method (`LambdaMetafactory`) that dynamically generates a class implementing the functional interface.

**Real-world Analogy:** Hiring a freelancer. Instead of building a whole company department (creating a class) to do a one-off task, you just pass the instructions (lambda) directly to the worker.

**ASCII Diagram:**
```text
[ Anonymous Inner Class ]       [ Lambda Expression ]
  new Runnable() {                () -> {
    public void run() {             System.out.println("Run");
      print("Run");               }
    }
  }
```

**Syntax + Code Examples:**
```java
// Syntax: (parameters) -> expression OR (parameters) -> { statements; }
Runnable r = () -> System.out.println("Running");
Comparator<Integer> comp = (a, b) -> a.compareTo(b);
```

**Target Typing & Effectively Final (Closure):**
- **Target Typing:** The compiler infers the type of the lambda from the context (the functional interface it's assigned to).
- **Effectively Final:** Lambdas can capture local variables from their enclosing scope. However, these variables must be `final` or "effectively final" (never modified after initialization). *Why?* Because local variables are stored on the stack, but the lambda might execute in another thread later. Java makes a copy of the variable for the lambda; if the original changed, they'd be out of sync.

**Common Mistakes:** Trying to modify a captured local variable inside the lambda. Use an array `int[] count = {0}` or `AtomicInteger` as a workaround.

### 9.2 Functional Interfaces
**Definition:** An interface with exactly ONE abstract method (SAM - Single Abstract Method). The `@FunctionalInterface` annotation is optional but recommended as it tells the compiler to enforce the SAM rule.

**Core Functional Interfaces (java.util.function):**
1. **`Predicate<T>`**: `boolean test(T t)` - Filters data.
   *Example:* `Predicate<String> isLong = s -> s.length() > 5;`
2. **`Function<T, R>`**: `R apply(T t)` - Transforms data.
   *Example:* `Function<String, Integer> getLength = s -> s.length();`
3. **`Consumer<T>`**: `void accept(T t)` - Consumes data (side-effects).
   *Example:* `Consumer<String> print = s -> System.out.println(s);`
4. **`Supplier<T>`**: `T get()` - Supplies data (lazy evaluation).
   *Example:* `Supplier<Double> random = () -> Math.random();`
5. **`BiFunction<T, U, R>`**: `R apply(T t, U u)` - 2 inputs, 1 output.
   *Example:* `BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;`
6. **`UnaryOperator<T>`**: `T apply(T t)` - Function where input/output types match.
7. **`BinaryOperator<T>`**: `T apply(T t1, T t2)` - BiFunction where all 3 types match.

### 9.3 Streams API: DEEP DIVE
**Definition:** A sequence of elements supporting sequential and parallel aggregate operations. Streams do NOT store data; they process data from a source (collections, arrays, I/O).

**Internal Working:** A stream pipeline consists of a source, 0 or more *intermediate* operations, and a *terminal* operation. It utilizes **Lazy Evaluation**: intermediate operations don't execute until the terminal operation is invoked.

**Real-world Analogy:** An assembly line in a factory. The raw materials (Collection) go on the conveyor belt (Stream). Various machines filter/modify them (Intermediate Ops). At the end, they are packaged into boxes (Terminal Op). Nothing moves on the belt until the packaging station is turned on (Lazy evaluation).

**Code + Intermediate & Terminal Ops:**
```java
List<String> names = Arrays.asList("John", "Jane", "Adam", "Eve");
List<String> result = names.stream()               // Source
    .filter(name -> name.startsWith("J"))          // Intermediate (Predicate)
    .map(String::toUpperCase)                      // Intermediate (Function)
    .sorted()                                      // Intermediate
    .peek(n -> System.out.println("Peek: " + n))   // Intermediate (Consumer - for debug)
    .limit(2)                                      // Intermediate (short-circuiting)
    .collect(Collectors.toList());                 // Terminal
```
*Other Terminal Ops:* `forEach`, `reduce`, `count`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`, `min`, `max`.

**Collectors (java.util.stream.Collectors):**
- `toList()`, `toSet()`
- `toMap(keyMapper, valueMapper)`
- `groupingBy(classifier)`: Groups elements into a `Map<K, List<V>>`.
- `partitioningBy(predicate)`: Groups into a `Map<Boolean, List<V>>` (True/False buckets).
- `joining(", ")`: Concatenates strings.
- `summarizingInt()`: Returns an IntSummaryStatistics (count, min, max, sum, avg).

**Parallel Streams:**
- **When to use:** Massive datasets (>10k elements), CPU-intensive tasks, independent elements.
- **Thread Pool:** Uses the common `ForkJoinPool` (`ForkJoinPool.commonPool()`).
- **Pitfalls:** Thread-safety issues (modifying shared state), overhead of splitting/merging data (can be slower for small datasets), order isn't guaranteed.

**Stream vs Collection differences:**
- Collections hold data; Streams process data.
- Collections can be iterated multiple times; Streams are consumed once (throw `IllegalStateException` if reused).
- Collections are eager; Streams are lazy.

**20 Output-based Stream Questions:**
1. `Stream.of(1,2).map(i->{System.out.print(i); return i;}).count();` -> Nothing is printed in Java 9+ (API optimization). In Java 8, prints `12` returns `2`.
2. `Stream.generate(() -> 1).limit(3).forEach(System.out::print);` -> `111`
3. `Stream.of("a", "b").map(String::toUpperCase).findFirst().get();` -> `"A"`
4. `IntStream.range(1, 5).sum();` -> `10` (1+2+3+4)
5. `Stream.of(1, 2, 3).filter(i -> i > 3).findAny().orElse(0);` -> `0`
6. `Stream.of(1, 2).peek(System.out::print).count();` -> `12` (Java 8)
7. `Stream.of("a").flatMap(s -> Stream.of(s, s)).count();` -> `2`
8. `IntStream.iterate(0, i -> i + 2).limit(3).sum();` -> `6` (0+2+4)
9. `Stream.of(1,2,3).reduce(0, Integer::sum);` -> `6`
10. `Stream.of("a","b").anyMatch(s -> s.equals("a"));` -> `true`
11. `Stream.of("a","b").allMatch(s -> s.equals("a"));` -> `false`
12. `Stream.empty().allMatch(e -> false);` -> `true` (Vacuous truth)
13. `Stream.of(1,2,3).skip(2).limit(1).count();` -> `1`
14. `Stream.of(3,1,2).sorted().findFirst().get();` -> `1`
15. `IntStream.rangeClosed(1, 3).reduce(1, (a,b)->a*b);` -> `6`
16. `Stream.of("A", "B").collect(Collectors.joining("-"));` -> `"A-B"`
17. `Stream.of(1,2,3).parallel().forEachOrdered(System.out::print);` -> `123` (forEachOrdered forces order even in parallel)
18. `Stream.of(1,1,2).distinct().count();` -> `2`
19. `Stream.of(1,2,3).max(Integer::compareTo).get();` -> `3`
20. `Arrays.asList("a").stream().close(); Arrays.asList("a").stream().count();` -> `1` (New stream created).

### 9.4 Optional
**Definition:** A container object which may or may not contain a non-null value. Prevents `NullPointerException` and expresses API intent explicitly.
**Creation:** `Optional.empty()`, `Optional.of(value)` (throws NPE if null), `Optional.ofNullable(value)`.
**Methods:** `map`, `flatMap`, `filter`, `ifPresent(Consumer)`.
**orElse vs orElseGet vs orElseThrow:**
- `orElse(T)`: Evaluates the fallback value *eagerly* (always executed, even if Optional is present).
- `orElseGet(Supplier)`: Evaluates the fallback value *lazily* (executed ONLY if Optional is empty).
- `orElseThrow(Supplier)`: Throws a specified exception if empty.

### 9.5 Method References
**Syntax:** `ClassName::methodName`
1. **Static Method:** `Math::max` (equivalent to `(a, b) -> Math.max(a, b)`)
2. **Instance Method of specific object:** `System.out::println` (`(s) -> System.out.println(s)`)
3. **Instance Method of arbitrary object of specific type:** `String::length` (`(s) -> s.length()`)
4. **Constructor:** `ArrayList::new` (`() -> new ArrayList<>()`)

### 9.6 Default & Static Methods in Interfaces
**Why?** To add new methods to existing interfaces (like `Collection`) without breaking existing implementations (Backward Compatibility).
**Diamond Problem Solution:** If a class implements two interfaces with the same default method, it *must* override the method. To call a specific interface's default method: `InterfaceA.super.methodName();`
**Static Methods:** Utility methods tied to the interface namespace. Not inherited by implementing classes.

### 9.7 Date-Time API (java.time)
Replaces old `java.util.Date` (which was mutable and not thread-safe). Modern API is **immutable and thread-safe**.
- `LocalDate`: Date without time (2023-10-01).
- `LocalTime`: Time without date (14:30:00).
- `LocalDateTime`: Date + Time.
- `ZonedDateTime`: Date + Time + TimeZone.
- `Instant`: Machine time (seconds/nanos from Epoch).
- `Duration`: Time-based amount (seconds/nanos).
- `Period`: Date-based amount (years/months/days).

### 9.8 CompletableFuture (Advanced)
**Definition:** Advanced implementation of `Future` that allows building asynchronous, non-blocking pipelines.
**Key Methods:**
- `supplyAsync(Supplier)`: Starts async task returning value.
- `runAsync(Runnable)`: Starts async task returning void.
- `thenApply(Function)`: Maps result to a new value.
- `thenAccept(Consumer)`: Consumes result.
- `thenCombine(CompletableFuture, BiFunction)`: Combines two independent futures.
- `exceptionally(Function)`: Error handling.

### 9.9 Modern Java Features (Java 10-17)
- **`var` (Java 10):** Local Variable Type Inference. `var list = new ArrayList<String>();` Compiler infers type. Only for local variables!
- **Records (Java 16):** Immutable data carriers. `public record Point(int x, int y) {}`. Auto-generates constructor, getters, `equals`, `hashCode`, `toString`.
- **Sealed Classes (Java 17):** Restricts which classes can extend it. `public sealed class Shape permits Circle, Square {}`
- **Pattern Matching for instanceof (Java 16):** Avoids casting. `if (obj instanceof String s) { System.out.println(s.length()); }`

### 9.10 50 Java 8+ Interview Questions
1. **What is the main benefit of Java 8?** Functional programming, Streams, Lambdas, APIs.
2. **Difference between Collections and Streams?** Storage vs computation.
3. **What is a Functional Interface?** Interface with 1 abstract method.
4. **What is `@FunctionalInterface` used for?** Compiler validation.
5. **Can a Functional Interface have default methods?** Yes, any number.
6. **What is target typing in Lambdas?** Compiler infers type based on context.
7. **What is a closure in Java?** Lambdas capturing enclosing variables.
8. **Why must variables in lambdas be effectively final?** Stack vs Heap memory management across threads.
9. **Difference between `map` and `flatMap`?** `map` transforms 1:1. `flatMap` transforms 1:N and flattens nested streams.
10. **What is intermediate vs terminal operation?** Intermediate returns Stream (lazy), Terminal triggers execution.
...*(Skipping repetitive basics, focusing on trick questions)*...
21. **Can we reuse a stream?** No, throws `IllegalStateException`.
22. **What does `findAny` do in parallel stream?** Returns whichever element finishes first.
23. **How does `Optional` avoid NPE?** By forcing the developer to handle the "empty" case via API design.
24. **Difference between `orElse` and `orElseGet`?** Eager vs Lazy evaluation of the fallback parameter.
25. **How to sort a map by values using streams?** `map.entrySet().stream().sorted(Map.Entry.comparingByValue()).collect(...)`
26. **What is the diamond problem in Java 8?** Multiple inheritance of default methods.
27. **How to resolve it?** Override the method and use `Interface.super.method()`.
28. **What is a Method Reference?** Shorthand for a lambda calling an existing method.
29. **Difference between `Predicate` and `Function`?** Returns boolean vs returns any type R.
30. **What is `Supplier` used for?** Lazy generation of values.
31. **What is the common thread pool used by parallel streams?** `ForkJoinPool.commonPool()`.
32. **When should you NOT use parallel streams?** I/O tasks, small datasets, non-thread-safe state.
33. **Difference between `Date` and `LocalDate`?** Mutable vs Immutable. Thread-safe vs not.
34. **What is `Instant`?** A point in time from Unix Epoch.
35. **What is `CompletableFuture`?** A callback-driven async promise in Java.
36. **Difference between `Future` and `CompletableFuture`?** `Future` blocks on `get()`. `CF` can be chained non-blockingly.
37. **What is `var` keyword?** Type inference for local variables.
38. **Is `var` dynamically typed like JavaScript?** No, it is statically typed at compile time.
39. **What are Records?** Transparent carriers for immutable data.
40. **Can Records extend other classes?** No, they implicitly extend `java.lang.Record`.
41. **What are Sealed classes?** Classes that explicitly declare permitted subclasses.
42. **What is pattern matching for `instanceof`?** Combines type checking and casting into one variable declaration.
43. **How to convert Stream to List in Java 16+?** `stream.toList()` (returns unmodifiable list).
44. **What is `IntStream`?** Primitive specialization of Stream to avoid boxing/unboxing overhead.
45. **What does `peek()` do?** Intermediate consumer operation, mostly for debugging.
46. **How to handle checked exceptions in Lambdas?** Try/catch block inside the lambda, or use a custom wrapper function.
47. **What is the output of `Stream.empty().findFirst()`?** `Optional.empty`.
48. **How does `groupingBy` work?** Acts like a SQL GROUP BY, returning a Map.
49. **Can interfaces have `private` methods?** Yes, since Java 9, to share code between default methods.
50. **What is `ZonedDateTime`?** A date-time with a time-zone in the ISO-8601 calendar system.

### Java 8+ Cheat Sheet
- **Filter/Transform:** `stream().filter(cond).map(func)`
- **List to Map:** `list.stream().collect(Collectors.toMap(Item::getId, Item::getName))`
- **Group by:** `list.stream().collect(Collectors.groupingBy(Item::getCategory))`
- **Count elements:** `list.stream().count()`
- **Sum ints:** `list.stream().mapToInt(Item::getPrice).sum()`
- **Optional safe unwrap:** `opt.orElse("default")`

---

## Section 10 - Advanced Java Concepts

### 10.1 Generics
**Why Generics?** Introduced in Java 5 to provide **Compile-Time Type Safety** and eliminate the need for manual casting (`ClassCastException` at runtime).
**Generic Classes/Methods:** `public class Box<T> { private T item; }`
**Wildcards:**
- `? extends T` (Upper Bounded): Accepts T or its subclasses. (Read-only structure).
- `? super T` (Lower Bounded): Accepts T or its superclasses. (Write-only structure).
- `?` (Unbounded): Any type.

**PECS Rule (Producer Extends, Consumer Super):**
- Use `? extends T` if you only need to READ from a collection (it *produces* T objects for you). You cannot safely add elements to it.
- Use `? super T` if you need to WRITE to a collection (it *consumes* T objects).

**Type Erasure:**
At compile time, Java removes all generic type information to ensure backward compatibility with pre-Java 5 bytecode. `<T>` becomes `Object` (or the bound, e.g., `Comparable` if `<T extends Comparable>`).
*Limitations:* Cannot do `new T()`, `new T[]`, or `instanceof T` due to type erasure.
*Bridge Methods:* Generated by the compiler to maintain polymorphism when a subclass overrides a generic method from a superclass.

### 10.2 Reflection API (`java.lang.reflect`)
**Definition:** Ability of a program to inspect and manipulate its own internal properties (classes, methods, fields) at runtime.
**Core Operations:**
- Get Class: `Class.forName("com.A")`, `obj.getClass()`, `A.class`
- Instantiation: `clazz.getDeclaredConstructor().newInstance()`
- Inspect: `getFields()`, `getMethods()`, `getConstructors()`
- **Invoking Private Methods:**
  ```java
  Method m = clazz.getDeclaredMethod("secretMethod");
  m.setAccessible(true); // Bypasses access checks!
  m.invoke(obj);
  ```
**Use Cases:** Frameworks like Spring (Dependency Injection), Hibernate (ORM), JUnit (test execution).
**Cost:** High performance overhead (bypasses JVM optimizations, access checks). Breaks encapsulation.

### 10.3 Annotations
**Definition:** Metadata added to Java source code that can be read at compile time or runtime.
**Built-in:** `@Override`, `@Deprecated`, `@SuppressWarnings`, `@FunctionalInterface`.
**Meta-annotations (Annotations applied to custom annotations):**
- `@Retention`: When is it available? `SOURCE` (compile-time only), `CLASS` (bytecode, discarded at runtime), `RUNTIME` (available via reflection).
- `@Target`: Where can it be applied? `METHOD`, `FIELD`, `TYPE` (Class).
- `@Documented`: Include in Javadoc.
- `@Inherited`: Subclasses inherit this annotation.
**Custom Annotation Example:**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Retry {
    int times() default 3;
}
```

### 10.4 Serialization
**Definition:** Converting an object's state into a byte stream so it can be saved to a file, database, or sent over a network. Deserialization is the reverse.
**Mechanics:**
- Implement the marker interface `java.io.Serializable`.
- `serialVersionUID`: A unique version identifier for the class. If omitted, JVM generates one based on class structure. If class changes, ID changes, causing `InvalidClassException` on deserialization. Always explicitly define it!
- `transient` Keyword: Prevents a field from being serialized. (e.g., passwords, temporary cache, open sockets).
- **Object Graph:** If Object A holds a reference to Object B, Object B must also be Serializable, or a `NotSerializableException` is thrown.
- `Externalizable`: A child interface of `Serializable` offering `writeExternal()` and `readExternal()` for custom, high-performance serialization control.
- **Security:** Deserialization vulnerabilities allow Remote Code Execution (RCE). Never deserialize untrusted data!

### 10.5 Comparable vs Comparator
**Comparable (`java.lang.Comparable`)**:
- Defines the **natural ordering** of a class.
- Modifies the class itself: `public class Employee implements Comparable<Employee>`.
- Method: `public int compareTo(T o)`. Return negative, zero, positive.
- Used implicitly by `Collections.sort(list)`.

**Comparator (`java.util.Comparator`)**:
- Defines a **custom ordering**.
- Extraneous to the class being sorted.
- Method: `public int compare(T o1, T o2)`.
- Used via: `Collections.sort(list, comparator)`.
- Java 8 features: `Comparator.comparing(Employee::getSalary).thenComparing(Employee::getName).reversed()`.

### 10.6 Cloneable
**Definition:** Marker interface allowing `Object.clone()` to perform a field-by-field copy.
- **Shallow Clone:** Primitives are copied. Object references are copied (original and clone point to the *same* inner objects).
- **Deep Clone:** Primitives and fully independent copies of inner objects are made.
- **Issues:** `clone()` is broken by design (doesn't call constructor, tricky with `final` fields). **Best Practice:** Use a Copy Constructor (`public Employee(Employee other)`) or factory method instead of `Cloneable`.

### 10.7 30 Advanced Java Interview Questions
1. **What is Type Erasure?** JVM removes generic type info at compile-time to maintain backward compatibility.
2. **Explain PECS.** Producer Extends (read-only collections), Consumer Super (write-only collections).
3. **Can we have generic arrays? `new T[]`?** No, arrays enforce types at runtime, generic types are erased at runtime.
4. **What is a Bridge Method?** Synthetic method created by compiler to allow covariant return types/generics with inheritance.
5. **How does Reflection break encapsulation?** `setAccessible(true)` allows calling private methods.
6. **What is the default `RetentionPolicy` for annotations?** `CLASS`.
7. **What is a Marker Interface?** Interface with no methods (e.g., `Serializable`, `Cloneable`).
8. **Why do we need `serialVersionUID`?** To verify that the serialized byte stream matches the loaded class structure.
9. **What happens if a field is `transient`?** It is ignored during serialization (becomes null/0 upon deserialization).
10. **Difference between `Serializable` and `Externalizable`?** Externalizable gives custom control over serialization logic.
11. **Are static variables serialized?** No, they belong to the class, not the object state.
12. **Difference between Comparable and Comparator?** Natural ordering vs Custom ordering. 1 sorting logic vs multiple sorting logics.
13. **Contract of `compareTo`?** x.compareTo(y) > 0 implies x > y. Must be consistent with `equals()`.
14. **What is a shallow copy?** Copies references, not the actual contained objects.
15. **How to achieve deep copy?** Manually clone nested objects, use Copy Constructor, or use JSON/Serialization cloning.
16. **Why is `Object.clone()` protected?** To force you to override it and explicitly implement `Cloneable`.
17. **Can we serialize a Singleton?** Yes, but deserialization creates a new instance. Must implement `readResolve()` to return the existing instance.
18. **What is Annotation Processing?** Pluggable logic executed at compile-time to generate code (e.g., Lombok).
19. **What is the `Class.forName()` method used for?** Dynamically loads a class into memory and initializes it (runs static blocks).
20. **Can we change a `final` field using reflection?** Yes, by modifying field modifiers, though highly discouraged.
21. **Why does Java use type erasure instead of reification (like C#)?** Strictly for backward compatibility with Java 1.4 code.
22. **What is `super T` used for?** Allowing a method to accept a collection of T or any of its superclasses, so we can insert T into it safely.
23. **What happens if an object is not Serializable but its superclass is?** The subclass is automatically Serializable.
24. **What if the subclass is Serializable but superclass is not?** The superclass must have a no-arg constructor to initialize its state during deserialization.
25. **How does `Collections.sort()` work internally?** Uses TimSort (MergeSort + InsertionSort).
26. **What's the output of `compareTo` if objects are equal?** `0`.
27. **How to sort a list of nulls?** Use `Comparator.nullsFirst(Comparator.naturalOrder())`.
28. **What is the reflection performance hit?** Reflection is ~10-50x slower due to dynamic resolution and access checks.
29. **What are the meta-annotations in Java?** Annotations that apply to other annotations (`@Target`, `@Retention`, etc.).
30. **Can we instantiate an interface using reflection?** No, you can only instantiate concrete classes or generate dynamic proxies.

---

## Section 11 - Design Patterns

### Creational Patterns
Deal with object creation mechanisms, optimizing and controlling the instantiation process.

#### 1. Singleton Pattern
**Intent:** Ensure a class has only one instance and provide a global point of access to it.
**Problem:** Multiple instances of a resource-heavy class (like DB Connection or Logger) consume memory and cause state inconsistencies.
**Real-World Example:** Task Manager in Windows. Configuration Manager in an app.
**Implementations:**
1. **Eager:** `private static final Singleton instance = new Singleton();` (Thread-safe but wastes memory if unused).
2. **Lazy Double-Checked Locking:**
   ```java
   public class Singleton {
       private static volatile Singleton instance; // volatile is crucial!
       private Singleton() {}
       public static Singleton getInstance() {
           if (instance == null) {
               synchronized (Singleton.class) {
                   if (instance == null) instance = new Singleton();
               }
           }
           return instance;
       }
   }
   ```
3. **Bill Pugh Inner Class:** Best non-enum method. Relies on ClassLoader synchronization.
4. **Enum (Best Practice):** `public enum Singleton { INSTANCE; }`. Defends against Reflection and Serialization attacks.
**Interview Q:** How do Reflection and Serialization break Singleton?
*Ans:* Reflection can invoke the private constructor. Serialization creates a new object on deserialization (unless `readResolve` is implemented). Enum prevents both natively.

#### 2. Factory Method
**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate.
**Real-World Example:** `LoggerFactory.getLogger()`. `Calendar.getInstance()`.
**Code Structure:** A `Creator` interface with `createProduct()` method. Implementations like `PdfCreator` return `PdfDocument`.

#### 3. Abstract Factory
**Intent:** Provide an interface for creating *families* of related or dependent objects without specifying their concrete classes.
**Real-World Example:** UI Toolkits (WindowsButton + WindowsCheckbox vs MacButton + MacCheckbox). It is a "Factory of Factories".

#### 4. Builder
**Intent:** Separate the construction of a complex object from its representation.
**Problem:** Telescoping Constructor anti-pattern (constructors with 10 parameters, 8 of which are optional).
**Real-World Example:** `StringBuilder`, Lombok `@Builder`, `HttpRequest.newBuilder()`.
**Code Structure:**
```java
User user = new User.Builder("John")
    .age(30)
    .email("john@doe.com")
    .build();
```

### Behavioral Patterns
Concerned with algorithms and the assignment of responsibilities between objects.

#### 5. Strategy
**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable. Complies with Open/Closed Principle.
**Real-World Example:** Payment gateways (CreditCard vs PayPal). `Collections.sort()` passing different `Comparator`s.
**Structure:** Context holds a reference to a Strategy interface. Context delegates execution to the Strategy object.

#### 6. Observer
**Intent:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.
**Real-World Example:** GUI Event Listeners (`onClick`), Message Queues (Pub/Sub).
**Implementation:** Subject maintains a list of Observers. When state changes, calls `observer.update()`.

#### 7. Template Method
**Intent:** Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.
**Real-World Example:** `HttpServlet.doGet()`, `AbstractList`.
**Implementation:** Abstract class with a `final` base method executing the steps, and abstract "hook" methods that subclasses implement.

### Structural Patterns
Deal with object composition to form larger structures.

#### 8. Adapter
**Intent:** Convert the interface of a class into another interface clients expect. Wraps an incompatible object.
**Real-World Example:** `Arrays.asList()`, `InputStreamReader(System.in)` (Adapts byte stream to char stream). Power plug adapters!
**Types:** Class Adapter (Inheritance - not possible in Java for multiple base classes), Object Adapter (Composition - widely used).

#### 9. Decorator
**Intent:** Attach additional responsibilities to an object dynamically. A flexible alternative to subclassing.
**Real-World Example:** Java I/O Streams (`new BufferedReader(new FileReader(new File()))`).
**Structure:** Decorator implements the same Interface as the target object, holds a reference to it, and delegates calls to it while adding pre/post behavior.

#### 10. Facade
**Intent:** Provide a unified interface to a set of interfaces in a subsystem. Hides complexity.
**Real-World Example:** `SLF4J` (Facade over Log4j/Logback), Car Starter (turn key, which handles battery, ignition, fuel systems behind the scenes).

### Design Patterns Cheat Sheet & Decision Table

| Scenario | Use Pattern | Why? |
|----------|-------------|------|
| Complex object, many optional fields | **Builder** | Prevents constructor explosion. |
| Swappable algorithms at runtime | **Strategy** | Open/Closed principle, easy to add new algos. |
| Publish/Subscribe event system | **Observer** | Loose coupling between sender and receivers. |
| Incompatible interfaces | **Adapter** | Acts as a bridge without altering source code. |
| Add features at runtime without sub-classing | **Decorator** | Combines features flexibly (Java I/O). |
| Hide complex subsystem | **Facade** | Provides a simple API entry point. |
| Enforce exact algorithm sequence | **Template Method** | Reuses code via inverted control (Hollywood Principle). |
| Exactly ONE instance globally | **Singleton** | Centralized state/resource management. |

### 30 Design Patterns Interview Questions
1. **Difference between Factory and Abstract Factory?** Factory creates one product; Abstract Factory creates a family of related products.
2. **Why is Double-Checked Locking needed in Singleton?** First check avoids synchronization overhead; second check ensures thread-safety during creation.
3. **Why use `volatile` in Double-Checked Locking?** Prevents the JVM from reordering instructions (publishing a partially initialized object).
4. **How does Builder pattern differ from Factory?** Factory is for single-step creation; Builder is for step-by-step configuration of a complex object.
5. **Difference between Strategy and State pattern?** Strategy is client-driven (client chooses algorithm). State is internal (object changes behavior based on internal state).
6. **Difference between Adapter and Decorator?** Adapter changes the *interface*. Decorator changes the *behavior/responsibilities* while keeping the same interface.
7. **What is the Hollywood Principle?** "Don't call us, we'll call you." Used in Template Method pattern.
8. **How does Enum prevent reflection attacks for Singleton?** Java specification explicitly forbids instantiating Enums via reflection (`IllegalArgumentException` is thrown).
9. **Give an example of Decorator in Java API.** `java.io.BufferedInputStream(new FileInputStream(...))`
10. **Give an example of Strategy in Java API.** `java.util.Comparator`.
11. **Give an example of Observer in Java API.** `java.util.EventListener`.
12. **What pattern does Spring DI (Dependency Injection) represent?** Inversion of Control / Factory / Builder depending on context, but fundamentally a sophisticated Factory.
13. **Difference between Facade and Adapter?** Facade simplifies a complex API. Adapter makes two incompatible APIs work together.
14. **What is a "Hook" in Template Method?** A method with an empty or default implementation that subclasses *can* (but don't have to) override.
15. **What pattern does `Runtime.getRuntime()` use?** Singleton.
16. **Why is the classical Observer pattern (Java's `Observable`) deprecated?** It was a class, not an interface, forcing inheritance and breaking composition. Modern Java uses property listeners or Reactive streams.
17. **How does the Proxy pattern differ from Decorator?** Proxy controls access to an object (lazy loading, security). Decorator adds behavior.
18. **What is the Bill Pugh Singleton implementation?** Uses a `private static class` inside the singleton to hold the instance. Relies on classloader lazy loading for thread-safety without locks.
19. **What design pattern is MVC based on?** Composite (View), Strategy (Controller), Observer (Model).
20. **Can you clone a Singleton object?** By default yes if it implements `Cloneable`. You must override `clone()` to throw `CloneNotSupportedException` to prevent it.
21. **What is the main drawback of Singleton?** It introduces global state, making unit testing difficult (hidden dependencies).
22. **When to use an Interface vs Abstract class in Template Method?** Template Method strictly requires an Abstract Class because it needs a concrete `final` method to enforce the algorithm steps.
23. **How does Strategy promote the Open-Closed Principle?** You can add a new strategy class without modifying the existing Context class.
24. **Difference between Factory Method and Simple Factory?** Simple factory is just a static method with a huge switch statement. Factory Method relies on polymorphism and subclasses.
25. **What pattern does `Arrays.asList()` use?** Adapter (Adapts an Array to a List interface).
26. **What is the Chain of Responsibility pattern?** Passing a request down a chain of handlers until one handles it (e.g., Servlet Filters, Exception handling).
27. **What is the Flyweight pattern?** Caching and sharing memory for high-volume objects (e.g., String Pool, `Integer.valueOf()`).
28. **How do you implement thread-safe lazy init without sync block?** Bill Pugh Singleton (Inner Static Helper Class).
29. **What is the Iterator pattern?** Sequentially access elements of a collection without exposing its underlying representation.
30. **What is the fundamental design principle behind Design Patterns?** Favor Composition over Inheritance. Program to an Interface, not an implementation.
