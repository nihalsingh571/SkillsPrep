# 🚀 COMPLETE OOP IN JAVA MASTERCLASS
### From Beginner → Interview-Ready | By a Senior Java Architect & FAANG Interviewer

---

> **How to use this guide:** Read sequentially. Every section builds on the previous one. Don't skip. Run every code example. Return to this as a reference before interviews.

---

## 📚 TABLE OF CONTENTS

| # | Section | Level |
|---|---------|-------|
| 1 | Objects and Classes | Beginner |
| 2 | Encapsulation | Beginner |
| 3 | Inheritance | Beginner-Intermediate |
| 4 | Polymorphism | Intermediate |
| 5 | Overriding vs Overloading | Intermediate |
| 6 | The Object Class | Intermediate |
| 7 | Mastering equals() | Intermediate-Advanced |
| 8 | Mastering hashCode() | Advanced |
| 9 | equals() and hashCode() Contract | Advanced |
| 10 | HashMap Internals | Advanced |
| 11 | HashSet Internals | Advanced |
| 12 | Abstraction | Intermediate |
| 13 | Interface Masterclass | Advanced |
| 14 | Advanced OOP Relationships | Advanced |
| 15 | JVM Internals Related to OOP | Advanced |
| 16 | Top 100 Interview Questions | All Levels |
| 17 | Practice Section | All Levels |
| 18 | Cheat Sheet | Reference |

---

# ═══════════════════════════════════════════
# SECTION 1: OBJECTS AND CLASSES
# ═══════════════════════════════════════════

## 🧠 The Mental Model First

Before we write a single line of code, let's understand the **philosophy**.

> **Real World Analogy:**
> A **Class** is like a **blueprint/architectural plan** for a house.
> An **Object** is the **actual house** built from that blueprint.
>
> The blueprint doesn't have rooms — it *describes* rooms.
> The actual house HAS rooms you can walk into.

You can build **many houses** (objects) from **one blueprint** (class). Each house is independent — painting one red doesn't paint them all red.

---

## 1.1 What is a Class?

### Definition
A **class** is a user-defined data type that acts as a template/blueprint for creating objects. It defines:
- **State** → fields/variables (what an object *has*)
- **Behavior** → methods (what an object *does*)

### Why it exists
Without classes, you'd write separate variables for every student:
```java
// Without classes — CHAOS
String student1Name = "Alice";
int student1Age = 20;
String student2Name = "Bob";
int student2Age = 22;
```
With classes, you group related data and behavior into one unit:
```java
// With classes — ORGANIZED
class Student {
    String name;
    int age;
    
    void study() {
        System.out.println(name + " is studying.");
    }
}
```

### Syntax
```java
[access_modifier] class ClassName {
    // fields (state)
    // constructors
    // methods (behavior)
}
```

### Full Example
```java
public class Student {
    // Fields (state)
    String name;
    int age;
    double gpa;
    
    // Method (behavior)
    void introduce() {
        System.out.println("Hi, I'm " + name + ", age " + age);
    }
    
    void study(String subject) {
        System.out.println(name + " is studying " + subject);
    }
}
```

---

## 1.2 What is an Object?

### Definition
An **object** is a concrete **instance** of a class — it occupies actual **memory** and has actual **values** for its fields.

### Why it exists
Classes are just templates. Objects are the **living, breathing** entities that actually do work in your program.

### Object Creation Syntax
```java
Student s = new Student();
//  ^         ^    ^
//  |         |    |-- calls constructor
//  |         |-- allocates memory on heap
//  |-- reference variable on stack
```

Let's break this down:
- `Student` — the **type** (tells compiler what `s` can do)
- `s` — the **reference variable** (lives on Stack)
- `new` — **operator** that allocates memory on Heap
- `Student()` — **constructor call**

---

## 1.3 Memory Representation — THE MOST IMPORTANT DIAGRAM

This is the diagram most books skip. **Understand this deeply.**

```
STACK MEMORY                    HEAP MEMORY
┌─────────────────┐             ┌──────────────────────────────┐
│                 │             │                              │
│  main() frame   │             │   Student Object             │
│ ┌─────────────┐ │    points   │  ┌────────────────────────┐ │
│ │  s = 0x1A4F │─┼────────────▶│  │ name = null            │ │
│ └─────────────┘ │             │  │ age  = 0               │ │
│                 │             │  │ gpa  = 0.0             │ │
│                 │             │  └────────────────────────┘ │
│                 │             │   Address: 0x1A4F           │
└─────────────────┘             └──────────────────────────────┘
```

### Key Insight: `s` does NOT contain the object. It contains the **address** of the object.

```java
Student s1 = new Student();
Student s2 = s1;  // s2 points to SAME object!

s2.name = "Alice";
System.out.println(s1.name); // "Alice" — same object!
```

```
STACK                           HEAP
┌──────────┐                   ┌──────────────────┐
│ s1=0x1A4F│──────────────────▶│ Student Object   │
│ s2=0x1A4F│──────────────────▶│ name = "Alice"   │
└──────────┘                   │ age  = 0         │
                               └──────────────────┘
```

### Null Reference
```java
Student s = null;  // s holds no address, points to nothing
s.name = "Alice";  // NullPointerException! No object exists!
```

```
STACK                           HEAP
┌──────────┐                   
│ s = null │──────▶ (nothing)  
└──────────┘                   
```

---

## 1.4 Heap vs Stack — Deep Comparison

| Feature | Stack | Heap |
|---------|-------|------|
| Stores | Primitive values, references | Objects |
| Size | Small (few MB) | Large (configurable, GBs) |
| Lifetime | Until method returns | Until GC collects |
| Speed | Very fast (LIFO) | Slower (dynamic allocation) |
| Thread safety | Each thread has own stack | Shared across threads |
| Error | StackOverflowError | OutOfMemoryError |

```
JVM Memory Layout
┌─────────────────────────────────────────────────────────┐
│                        JVM                              │
│  ┌───────────────┐  ┌───────────────────────────────┐  │
│  │  Stack        │  │           Heap                │  │
│  │ (per thread)  │  │  ┌────────┐  ┌────────────┐  │  │
│  │ ┌───────────┐ │  │  │ Young  │  │    Old     │  │  │
│  │ │main frame │ │  │  │  Gen   │  │    Gen     │  │  │
│  │ │ s=0x1A4F  │ │  │  └────────┘  └────────────┘  │  │
│  │ └───────────┘ │  └───────────────────────────────┘  │
│  └───────────────┘                                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │                Method Area (Metaspace)            │  │
│  │  Class definitions, static variables, bytecode   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 1.5 Constructors

### Definition
A **constructor** is a special method that is called automatically when an object is created with `new`. It **initializes** the object's state.

### Why it exists
Imagine building a house but forgetting to install doors. Constructors ensure objects are **properly initialized** before use.

### Rules
1. Same name as the class
2. No return type (not even `void`)
3. Called once per object creation
4. Can be overloaded

### 1.5.1 Default Constructor

```java
class Student {
    String name;
    int age;
    // Java automatically provides:
    // Student() { }  ← default constructor
}

Student s = new Student(); // calls default constructor
// name = null, age = 0 (Java default values)
```

**Java's default values:**

| Type | Default |
|------|---------|
| int, long, short, byte | 0 |
| float, double | 0.0 |
| boolean | false |
| char | '\u0000' |
| Object/reference | null |

> ⚠️ **Important:** If you define ANY constructor, Java **stops** providing the default constructor!

```java
class Student {
    String name;
    Student(String name) { this.name = name; }
}

Student s = new Student();  // COMPILE ERROR! No default constructor!
Student s = new Student("Alice"); // OK
```

### 1.5.2 Parameterized Constructor

```java
class Student {
    String name;
    int age;
    
    Student(String name, int age) {
        this.name = name;  // 'this' refers to current object
        this.age = age;
    }
}

Student s = new Student("Alice", 20);
```

### 1.5.3 Constructor Overloading

Having multiple constructors with different parameter lists:

```java
class Student {
    String name;
    int age;
    double gpa;
    
    // Constructor 1: No args
    Student() {
        this.name = "Unknown";
        this.age = 0;
        this.gpa = 0.0;
    }
    
    // Constructor 2: Name only
    Student(String name) {
        this.name = name;
        this.age = 0;
        this.gpa = 0.0;
    }
    
    // Constructor 3: All fields
    Student(String name, int age, double gpa) {
        this.name = name;
        this.age = age;
        this.gpa = gpa;
    }
}
```

### 1.5.4 Constructor Chaining with `this()`

Instead of repeating initialization code, chain constructors:

```java
class Student {
    String name;
    int age;
    double gpa;
    
    Student() {
        this("Unknown", 0, 0.0);  // calls 3-arg constructor
    }
    
    Student(String name) {
        this(name, 0, 0.0);  // calls 3-arg constructor
    }
    
    Student(String name, int age, double gpa) {
        this.name = name;
        this.age = age;
        this.gpa = gpa;
        System.out.println("Student created: " + name);
    }
}
```

> ⚠️ `this()` must be the **first statement** in a constructor.

---

## 1.6 The `this` Keyword

`this` is a reference to the **current object** — the object whose method/constructor is being called.

### Use Case 1: Disambiguating field and parameter names
```java
class Student {
    String name;
    
    Student(String name) {
        // Without this: name = name; // WRONG! assigns param to itself
        this.name = name;  // field = parameter
    }
}
```

### Use Case 2: Calling another constructor
```java
Student() {
    this("Default", 0);  // Constructor chaining
}
```

### Use Case 3: Passing current object as argument
```java
class Printer {
    void print(Student s) { /* ... */ }
}

class Student {
    void printSelf(Printer p) {
        p.print(this);  // pass current object
    }
}
```

### Use Case 4: Returning current object (Builder pattern)
```java
class StudentBuilder {
    String name;
    
    StudentBuilder setName(String name) {
        this.name = name;
        return this;  // enables chaining: builder.setName("X").setAge(20)
    }
}
```

---

## 1.7 The `super` Keyword

`super` refers to the **parent class** object.

```java
class Animal {
    String name = "Animal";
    
    Animal() {
        System.out.println("Animal constructor");
    }
    
    void sound() {
        System.out.println("Some sound");
    }
}

class Dog extends Animal {
    String name = "Dog";
    
    Dog() {
        super();  // calls Animal() constructor — IMPLICIT if not written
        System.out.println("Dog constructor");
    }
    
    void display() {
        System.out.println(name);         // Dog (own field)
        System.out.println(super.name);   // Animal (parent field)
    }
    
    void sound() {
        super.sound();    // calls Animal's sound()
        System.out.println("Woof!");
    }
}
```

> ⚠️ `super()` must be the **first statement** in a constructor. Java automatically inserts `super()` if not present.

### Interview Question: What's the output?
```java
class A {
    A() { System.out.println("A"); }
}
class B extends A {
    B() { System.out.println("B"); }
}
class C extends B {
    C() { System.out.println("C"); }
}

new C();
```
**Output:** `A` → `B` → `C` (constructors always chain up to Object first)

---

## 1.8 Common Mistakes

```java
// MISTAKE 1: Forgetting 'this' disambiguation
class Box {
    int width;
    Box(int width) {
        width = width;  // BUG! self-assignment, field stays 0
    }
}

// MISTAKE 2: Two this() calls
Box() {
    this(10);
    this(20);  // COMPILE ERROR — only one this() allowed
}

// MISTAKE 3: Circular constructor chaining
Box() { this(10); }
Box(int w) { this(); }  // COMPILE ERROR — recursive chaining
```

---

# ═══════════════════════════════════════════
# SECTION 2: ENCAPSULATION
# ═══════════════════════════════════════════

## 🧠 The Mental Model

> **Real World Analogy:**
> Think of an **ATM machine**. You don't have access to its internal cash vault or circuitry. You only interact through a controlled interface (buttons, card slot). This is encapsulation.
>
> The internal state (cash amount, transaction logs) is **hidden**. You access it only through **controlled methods**.

---

## 2.1 Definition

**Encapsulation** = Bundling data (fields) + behavior (methods) into one unit, AND **restricting direct access** to the internal data.

It's often called **"data hiding"** — but more accurately it's **"controlled access"**.

---

## 2.2 Why Encapsulation Exists

### Problem Without Encapsulation:
```java
class BankAccount {
    double balance;  // public by default
}

BankAccount acc = new BankAccount();
acc.balance = -999999;  // DISASTER! No validation!
```

### Solution With Encapsulation:
```java
class BankAccount {
    private double balance;  // hidden
    
    public void deposit(double amount) {
        if (amount > 0) {         // validation!
            balance += amount;
        }
    }
    
    public double getBalance() {
        return balance;           // controlled read
    }
}

BankAccount acc = new BankAccount();
acc.balance = -999999;  // COMPILE ERROR! Field is private.
acc.deposit(-999999);   // No effect — validation rejects it.
```

---

## 2.3 Private Fields + Getters/Setters

```java
public class Person {
    private String name;
    private int age;
    private String email;
    
    // Getter — read access
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getEmail() { return email; }
    
    // Setter — write access with validation
    public void setName(String name) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        this.name = name;
    }
    
    public void setAge(int age) {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Invalid age: " + age);
        }
        this.age = age;
    }
    
    public void setEmail(String email) {
        if (!email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
        this.email = email;
    }
}
```

---

## 2.4 Access Modifiers — The Four Levels

```
More Restrictive ◄──────────────────────────────► More Open

  private     default      protected      public
    │            │             │             │
    │         (package)        │             │
    │            │             │             │
 Same class  Same package  Same package   Everywhere
 only        only          + subclasses
```

| Modifier | Same Class | Same Package | Subclass | Everywhere |
|----------|-----------|--------------|----------|------------|
| private | ✅ | ❌ | ❌ | ❌ |
| default | ✅ | ✅ | ❌ | ❌ |
| protected | ✅ | ✅ | ✅ | ❌ |
| public | ✅ | ✅ | ✅ | ✅ |

---

## 2.5 Immutable Classes

An **immutable** class is one whose state cannot change after construction. Think `String` in Java.

### How to create an immutable class:
```java
public final class ImmutablePerson {       // 1. final class
    private final String name;             // 2. final fields
    private final int age;
    private final List<String> hobbies;    // 3. mutable field — need deep copy
    
    public ImmutablePerson(String name, int age, List<String> hobbies) {
        this.name = name;
        this.age = age;
        // 4. Defensive copy of mutable objects
        this.hobbies = new ArrayList<>(hobbies);
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    
    // 5. Return defensive copy
    public List<String> getHobbies() {
        return new ArrayList<>(hobbies);  // not the internal list!
    }
    // NO setters!
}
```

### Rules for Immutability:
1. `final` class (prevent subclassing)
2. All fields `private final`
3. No setters
4. Deep copy mutable fields in constructor
5. Return defensive copies from getters

### Why Immutability Matters:
- Thread-safe by default (no synchronization needed)
- Safe to use as HashMap keys
- Easy to reason about
- `String`, `Integer`, `LocalDate` are all immutable

---

## 2.6 Interview Questions — Encapsulation

**Q: Why are fields made private and not protected?**
A: `protected` allows subclasses to access fields directly, breaking encapsulation. `private` enforces that even subclasses must use the controlled interface (getters/setters).

**Q: Can a class be encapsulated without getters/setters?**
A: Yes — if fields are `private` and no access is provided externally, that's still encapsulation (maximum restriction).

**Q: What's the difference between encapsulation and abstraction?**
A: Encapsulation is about **hiding data** (HOW). Abstraction is about **hiding complexity** and showing only essential features (WHAT).

---

# ═══════════════════════════════════════════
# SECTION 3: INHERITANCE
# ═══════════════════════════════════════════

## 🧠 The Mental Model

> **Real World Analogy:**
> A **Toyota Camry** IS-A **Car**. It inherits all properties of a car (wheels, engine, steering) and adds its own (Camry-specific features, Toyota logo).
>
> You don't redefine "what a wheel is" every time you create a car model. You **inherit** it.

---

## 3.1 Definition

**Inheritance** is a mechanism where a child class **acquires** the properties and behaviors of a parent class.

- Parent class = Superclass / Base class
- Child class = Subclass / Derived class
- Keyword: `extends`

```java
class Parent {
    int x = 10;
    void display() { System.out.println("Parent: " + x); }
}

class Child extends Parent {
    int y = 20;
    void show() { System.out.println("Child: " + y); }
}

Child c = new Child();
c.display();  // inherited from Parent
c.show();     // own method
System.out.println(c.x);  // inherited field
```

---

## 3.2 Why Inheritance Exists

### Without Inheritance:
```java
class Dog {
    String name;
    void eat() { System.out.println("eating"); }
    void bark() { System.out.println("woof"); }
}

class Cat {
    String name;
    void eat() { System.out.println("eating"); }  // DUPLICATE!
    void meow() { System.out.println("meow"); }
}
```

### With Inheritance:
```java
class Animal {
    String name;
    void eat() { System.out.println(name + " is eating"); }
}

class Dog extends Animal {
    void bark() { System.out.println("Woof!"); }
}

class Cat extends Animal {
    void meow() { System.out.println("Meow!"); }
}
```

**Benefits:** Code reuse, extensibility, polymorphism enablement.

---

## 3.3 Types of Inheritance in Java

### Single Inheritance
```
Animal
  │
  ▼
Dog
```
```java
class Animal { }
class Dog extends Animal { }
```

### Multilevel Inheritance
```
Animal
  │
  ▼
Dog
  │
  ▼
Labrador
```
```java
class Animal { }
class Dog extends Animal { }
class Labrador extends Dog { }

Labrador lab = new Labrador();
// lab inherits from both Dog AND Animal
```

### Hierarchical Inheritance
```
        Animal
       /      \
      /        \
    Dog        Cat
```
```java
class Animal { }
class Dog extends Animal { }
class Cat extends Animal { }
```

### ❌ Multiple Inheritance (NOT supported in Java for classes)
```
// Java does NOT allow:
class C extends A, B { }  // COMPILE ERROR!
```

**Why?** The **Diamond Problem**:
```
    A
   / \
  B   C
   \ /
    D
```
If both B and C override a method from A, D doesn't know which version to use. Java avoids this for classes. **Interfaces solve this differently** (covered in Section 13).

---

## 3.4 Memory Model for Inheritance

When you create a `Dog` object, memory contains **both** parts:

```
HEAP
┌────────────────────────────────────┐
│         Dog Object                 │
│  ┌─────────────────────────────┐   │
│  │     Animal Part             │   │
│  │  name = null                │   │
│  │  [Animal methods ref]       │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │     Dog Part                │   │
│  │  breed = null               │   │
│  │  [Dog methods ref]          │   │
│  └─────────────────────────────┘   │
└────────────────────────────────────┘
```

---

## 3.5 `super` in Inheritance — Deep Dive

```java
class Animal {
    String name;
    
    Animal(String name) {
        this.name = name;
        System.out.println("Animal constructor: " + name);
    }
    
    void eat() {
        System.out.println(name + " eats food.");
    }
}

class Dog extends Animal {
    String breed;
    
    Dog(String name, String breed) {
        super(name);   // MUST be first line — calls Animal(String)
        this.breed = breed;
        System.out.println("Dog constructor: " + breed);
    }
    
    void displayInfo() {
        System.out.println("Name: " + super.name);   // parent field
        System.out.println("Breed: " + this.breed);  // own field
    }
    
    void eat() {
        super.eat();   // call parent's eat()
        System.out.println(name + " also loves bones!");
    }
}

Dog d = new Dog("Rex", "Labrador");
// Output:
// Animal constructor: Rex
// Dog constructor: Labrador
```

---

## 3.6 What is NOT Inherited?

| Not Inherited | Reason |
|---------------|--------|
| `private` members | Access restriction |
| Constructors | Not members; but can be called via `super()` |
| `static` members | Belong to class, not object |

---

## 3.7 `final` and Inheritance

```java
final class String { }  // cannot be extended!

class MyString extends String { }  // COMPILE ERROR!
```

**Why is String final?** Security and consistency — if you could subclass String, you could override `equals()`, breaking HashMap and security checks.

---

# ═══════════════════════════════════════════
# SECTION 4: POLYMORPHISM
# ═══════════════════════════════════════════

## 🧠 The Mental Model

> **Real World Analogy:**
> The word **"draw"** means different things:
> - An artist draws a painting
> - A lawyer draws up a contract
> - A gun draws from a holster
>
> Same word, different behavior based on **context**. That's polymorphism.

**Polymorphism** = "Many forms" (Greek: *poly* = many, *morphe* = form)

In Java: One interface / method name → multiple implementations.

---

## 4.1 Types of Polymorphism

```
Polymorphism
     │
     ├── Compile-Time (Static)
     │        └── Method Overloading
     │
     └── Runtime (Dynamic)
              └── Method Overriding
```

---

## 4.2 Compile-Time Polymorphism: Method Overloading

### Definition
Multiple methods in the **same class** with the **same name** but **different parameter lists**.

Resolved at **compile time** by the compiler.

### Valid Ways to Overload

```java
class Calculator {
    // 1. Different number of parameters
    int add(int a, int b) {
        return a + b;
    }
    int add(int a, int b, int c) {
        return a + b + c;
    }
    
    // 2. Different parameter types
    double add(double a, double b) {
        return a + b;
    }
    
    // 3. Different parameter order
    void print(String s, int n) {
        System.out.println(s + " " + n);
    }
    void print(int n, String s) {
        System.out.println(n + " " + s);
    }
}
```

### ❌ Why Return Type Alone Cannot Overload

```java
int getValue() { return 1; }
double getValue() { return 1.0; }  // COMPILE ERROR!
```

**Why?** The compiler resolves overloading based on the **call site**:
```java
getValue();  // Compiler sees this — return type is DISCARDED
             // Both methods look identical to the compiler!
```

The compiler needs to know WHICH method to call before it knows the return type. So return type alone is insufficient for disambiguation.

### How JVM Resolves Overloading

```java
Calculator calc = new Calculator();
calc.add(1, 2);        // compiler sees: add(int, int) → links to method 1
calc.add(1.0, 2.0);    // compiler sees: add(double, double) → links to method 3
```

This linking happens during **compilation** → called **static binding** or **early binding**.

Bytecode will have direct references to the correct method.

### Widening in Overloading

```java
class Test {
    void method(int a) { System.out.println("int"); }
    void method(long a) { System.out.println("long"); }
}

Test t = new Test();
byte b = 5;
t.method(b);  // prints "int" — byte widens to int (closest match)
```

**Widening order:** `byte → short → int → long → float → double`

### Autoboxing in Overloading (Important!)

```java
class Test {
    void method(int a) { System.out.println("primitive int"); }
    void method(Integer a) { System.out.println("Integer"); }
}

Test t = new Test();
t.method(5);          // "primitive int" — exact match wins over autoboxing
t.method(new Integer(5));  // "Integer"
```

---

## 4.3 Runtime Polymorphism: Method Overriding

### Definition
A **child class** provides its own implementation of a method already defined in the **parent class**.

Resolved at **runtime** by JVM.

### Rules for Overriding
1. Same method name
2. Same parameter list
3. Same (or covariant) return type
4. Access modifier can be same or more permissive (not more restrictive)
5. Can throw same or fewer/narrower checked exceptions
6. Annotate with `@Override` (highly recommended)

```java
class Animal {
    void sound() {
        System.out.println("Some animal sound");
    }
    
    String describe() {
        return "I am an animal";
    }
}

class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Woof!");
    }
    
    @Override
    String describe() {  // Covariant return type also allowed
        return "I am a dog";
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Meow!");
    }
}
```

### Dynamic Method Dispatch — The Heart of Runtime Polymorphism

This is the **most important concept** in OOP:

```java
Animal a = new Dog();  // reference type = Animal, object type = Dog
a.sound();             // Which sound() runs?
```

**Answer: Dog's sound() runs!**

**Why?** JVM looks at the **actual object type** (Dog), not the reference type (Animal).

```
At Runtime:
                     
Animal a = new Dog();

STACK              HEAP
┌─────────┐       ┌───────────────────────────┐
│a = 0xABC│──────▶│    Dog Object at 0xABC    │
└─────────┘       │  [vtable pointer] ──────┐ │
                  │  Animal part:           │ │
                  │    [fields]             │ │
                  │  Dog part:              │ │
                  │    [fields]             │ │
                  └─────────────────────────┼─┘
                                            │
                                 ┌──────────▼──────────┐
                                 │  Dog's vtable        │
                                 │  sound() → Dog.sound │
                                 │  describe()→Dog.desc │
                                 └──────────────────────┘
```

### vtable (Virtual Method Table) — How JVM Does It

Every object has a hidden pointer to its class's **vtable** — a table of method addresses.

```
Animal vtable:
┌──────────────────────────────────┐
│ sound()    → Animal.sound()      │
│ describe() → Animal.describe()   │
│ toString() → Object.toString()   │
└──────────────────────────────────┘

Dog vtable:
┌──────────────────────────────────┐
│ sound()    → Dog.sound()  ◄ OVERRIDDEN
│ describe() → Dog.describe()  ◄ OVERRIDDEN
│ toString() → Object.toString()   │
└──────────────────────────────────┘
```

When `a.sound()` is called:
1. JVM follows pointer in `a` to the object on heap
2. Object has vtable pointer → Dog's vtable
3. Looks up `sound()` in Dog's vtable → finds `Dog.sound()`
4. Calls `Dog.sound()`

This is **late binding** — binding happens at runtime.

### The Power of Runtime Polymorphism

```java
Animal[] animals = {
    new Dog(),
    new Cat(),
    new Dog(),
    new Cat()
};

for (Animal a : animals) {
    a.sound();  // Automatically calls the right sound()!
}
// Output:
// Woof!
// Meow!
// Woof!
// Meow!
```

You wrote the loop **once** — it works for any Animal subclass, even ones added in the future!

```java
// This is the power of polymorphism in real systems:
List<Shape> shapes = getShapes();
for (Shape s : shapes) {
    s.draw();   // Circle draws circle, Rectangle draws rectangle, etc.
    s.resize(); // Each knows how to resize itself
}
```

---

## 4.4 What Can NOT Be Overridden?

| Cannot Override | Reason |
|-----------------|--------|
| `static` methods | Belong to class, not object — no vtable |
| `final` methods | Explicitly prevented |
| `private` methods | Not visible to child class |
| Constructors | Not methods |

### Static Method Hiding (NOT overriding!)

```java
class Parent {
    static void staticMethod() { System.out.println("Parent static"); }
}

class Child extends Parent {
    static void staticMethod() { System.out.println("Child static"); }
}

Parent p = new Child();
p.staticMethod();  // "Parent static" — resolved at COMPILE TIME!
                   // This is method HIDING, not overriding
```

---

# ═══════════════════════════════════════════
# SECTION 5: OVERRIDING VS OVERLOADING
# ═══════════════════════════════════════════

## Comprehensive Comparison Table

| Feature | Overloading | Overriding |
|---------|-------------|------------|
| Definition | Same name, different params in same class | Same name, same params in child class |
| Binding | Compile-time (Static) | Runtime (Dynamic) |
| Class | Same class | Parent-Child classes |
| Inheritance required? | No | Yes |
| Parameters | Must differ | Must be identical |
| Return type | Can differ (with caution) | Must be same or covariant |
| Access modifier | Any | Same or more permissive |
| `static` | Yes, static can be overloaded | No, static cannot be overridden |
| `private` | Yes, can be overloaded | No, private not inherited |
| `final` | Yes, final can be overloaded | No, final cannot be overridden |
| Polymorphism | Compile-time | Runtime |
| Performance | Faster (resolved at compile) | Slightly slower (vtable lookup) |
| @Override | Not applicable | Highly recommended |

---

## 20 Examples — Overloading vs Overriding

```java
// ========== OVERLOADING EXAMPLES ==========

class MathUtil {
    // Example 1: Different parameter count
    int sum(int a, int b) { return a + b; }
    int sum(int a, int b, int c) { return a + b + c; }
    
    // Example 2: Different types
    double sum(double a, double b) { return a + b; }
    
    // Example 3: Different order
    void show(String s, int n) { }
    void show(int n, String s) { }
    
    // Example 4: Widening
    void test(long l) { }
    void test(int i) { }
    
    // Example 5: Autoboxing
    void box(int i) { System.out.println("primitive"); }
    void box(Integer i) { System.out.println("Integer"); }
    
    // Example 6: Varargs (lowest priority)
    void vararg(int... a) { System.out.println("varargs"); }
    
    // Example 7: String and Object
    void process(String s) { }
    void process(Object o) { }
}

// ========== OVERRIDING EXAMPLES ==========

class Vehicle {
    // Example 8: Basic override
    void start() { System.out.println("Vehicle starts"); }
    
    // Example 9: Covariant return type
    Vehicle getType() { return new Vehicle(); }
    
    // Example 10: Throwing exceptions
    void load() throws Exception { }
}

class Car extends Vehicle {
    // Example 11: Override with same signature
    @Override
    void start() { System.out.println("Car starts"); }
    
    // Example 12: Covariant return — Car IS-A Vehicle, so this is valid
    @Override
    Car getType() { return new Car(); }  // return type narrowed
    
    // Example 13: Override — can throw fewer exceptions
    @Override
    void load() { }  // no exception declared — valid!
    
    // Example 14: Calling super in override
    @Override
    void start() {
        super.start();
        System.out.println("Car start sequence complete");
    }
}

// Example 15: Widened access modifier (valid)
class A { protected void method() { } }
class B extends A {
    @Override
    public void method() { }  // protected → public: MORE permissive — valid
}

// Example 16: INVALID — narrowing access
class C extends A {
    // @Override
    // private void method() { }  // COMPILE ERROR! public → private
}

// Example 17: Final preventing override
class D {
    final void cannotOverride() { }
}
class E extends D {
    // void cannotOverride() { }  // COMPILE ERROR!
}

// Example 18: Static hiding (not overriding)
class F { static void staticM() { System.out.println("F"); } }
class G extends F { static void staticM() { System.out.println("G"); } }
// F ref = new G(); ref.staticM(); → "F" (compile-time resolution)

// Example 19: Constructor "overloading" (constructors CAN be overloaded)
class H {
    H() { }
    H(int x) { }
    H(String s) { }
}

// Example 20: Overloading with null
class I {
    void method(String s) { System.out.println("String"); }
    void method(Object o) { System.out.println("Object"); }
}
// I i = new I(); i.method(null);  → "String" (most specific type wins)
```

---

# ═══════════════════════════════════════════
# SECTION 6: THE OBJECT CLASS
# ═══════════════════════════════════════════

## 6.1 java.lang.Object — The Root of All

**Every class in Java implicitly extends `Object`.**

```java
class Student { }
// is EXACTLY the same as:
class Student extends Object { }
```

**Inheritance Hierarchy:**
```
java.lang.Object
     │
     ├── String
     ├── Integer
     ├── ArrayList
     ├── HashMap
     ├── YourStudent class
     └── Every other class...
```

This is why you can write:
```java
Object o = new Student();   // Student IS-A Object
Object o2 = new String("hi");
Object o3 = new ArrayList<>();
```

---

## 6.2 Key Methods of Object Class

### 6.2.1 `toString()`

```java
// Default implementation in Object:
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

```java
Student s = new Student("Alice", 20);
System.out.println(s);  // Student@1b6d3586  ← ugly default!
```

**Override it:**
```java
class Student {
    String name; int age;
    
    @Override
    public String toString() {
        return "Student{name='" + name + "', age=" + age + "}";
    }
}
// Now: System.out.println(s);  → "Student{name='Alice', age=20}"
```

`println()` automatically calls `toString()` — so override it for debugging!

### 6.2.2 `equals(Object obj)`

Default behavior: `==` comparison (reference equality).

```java
// Default in Object:
public boolean equals(Object obj) {
    return (this == obj);  // just reference comparison
}
```

Covered in full depth in **Section 7**.

### 6.2.3 `hashCode()`

Returns an integer "hash" representing the object.

Covered in full depth in **Section 8**.

### 6.2.4 `getClass()`

```java
Student s = new Student("Alice", 20);
Class<?> c = s.getClass();
System.out.println(c.getName());        // "Student"
System.out.println(c.getSimpleName()); // "Student"

// Checking type at runtime:
if (s.getClass() == Student.class) {
    System.out.println("It's a Student!");
}
```

### 6.2.5 `clone()`

Creates a copy of the object. Must implement `Cloneable` interface.

```java
class Student implements Cloneable {
    String name;
    int age;
    
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();  // shallow copy
    }
}

Student s1 = new Student();
s1.name = "Alice";
Student s2 = (Student) s1.clone();
s2.name = "Bob";
System.out.println(s1.name);  // "Alice" — unaffected (primitive-like String)
```

⚠️ `clone()` does **shallow copy** — mutable objects inside are still shared.

### 6.2.6 `finalize()` (Deprecated)

Called by GC before object is collected. Don't rely on it — use try-with-resources instead. **Deprecated since Java 9.**

---

# ═══════════════════════════════════════════
# SECTION 7: MASTERING equals()
# ═══════════════════════════════════════════

## 7.1 What is equals()?

`equals()` is a method defined in `Object` class to check **logical equality** between two objects.

```java
// Signature in java.lang.Object:
public boolean equals(Object obj) {
    return (this == obj);
}
```

---

## 7.2 == vs equals() — The Fundamental Distinction

### `==` → **Reference Equality** (Are they the SAME object in memory?)
### `equals()` → **Content Equality** (Do they have the SAME values?)

```java
String s1 = new String("Java");
String s2 = new String("Java");

System.out.println(s1 == s2);       // false — different objects in heap!
System.out.println(s1.equals(s2));  // true  — same content!
```

**Memory diagram:**
```
STACK              HEAP
┌──────────┐      ┌──────────────┐   ┌──────────────┐
│ s1=0xAAA │─────▶│ "Java" @0xAAA│   │ "Java" @0xBBB│
│ s2=0xBBB │─────▶│              │   │              │
└──────────┘      └──────────────┘   └──────────────┘

s1 == s2    → compares 0xAAA == 0xBBB → FALSE
s1.equals(s2) → compares "Java" content == "Java" content → TRUE
```

### String Pool Twist (Important for Interviews!)

```java
String s1 = "Java";        // goes to String Pool
String s2 = "Java";        // reuses same Pool entry

System.out.println(s1 == s2);      // TRUE! Same object in pool!
System.out.println(s1.equals(s2)); // TRUE!
```

```
STACK              String Pool (Heap)
┌──────────┐      ┌──────────────┐
│ s1=0xAAA │─────▶│ "Java" @0xAAA│◄── both point here!
│ s2=0xAAA │─────▶│              │
└──────────┘      └──────────────┘
```

`intern()` forces a string into the pool: `s1.intern() == s2.intern()` → true.

---

## 7.3 Why Java Created equals()

Default `==` only checks **identity** (same memory address). For objects, we often care about **logical equality**:

- Two `Person` objects with same name and ID should be "equal" logically
- Two `String` objects with same characters should be "equal"
- Without `equals()`, you couldn't put objects in Sets or use them as Map keys correctly

---

## 7.4 Breaking Down the Method Signature

```java
public boolean equals(Object obj)
//^      ^       ^       ^    ^
//│      │       │       │    └── parameter name
//│      │       │       └─────── parameter TYPE (very important!)
//│      │       └─────────────── method name
//│      └─────────────────────── return type
//└────────────────────────────── access modifier
```

### Why `Object obj` and NOT `Person obj`?

This is **the most important question in Java OOP.**

Let's say you have:
```java
class Person {
    boolean equals(Person obj) { ... }  // WRONG! Not an override!
}
```

This does NOT override `Object.equals()` — it **overloads** it!

Now:
```java
Person p1 = new Person("Alice");
Object o = new Person("Alice");
p1.equals(o);  // calls Object.equals() — reference comparison! BUG!
```

**The parameter must be `Object` to truly override:**
```java
class Person {
    String name;
    
    @Override  // This annotation would FAIL if parameter was Person
    public boolean equals(Object obj) {  // matches Object's signature exactly
        // ...
    }
}
```

### The Polymorphism Involved

When you write:
```java
p1.equals(o);
```

`o` is of type `Object` reference. Since `equals(Object obj)` takes `Object`, **any** object can be passed — `String`, `Integer`, `Person`, anything. This is **upcasting in action**:

```java
Person p1 = new Person("Alice");
Person p2 = new Person("Alice");

p1.equals(p2);
// p2 (Person) is automatically upcast to Object when passed
// Inside equals(), obj holds the upcast reference
```

---

## 7.5 Type Casting — The Full Story

### What is Type Casting?

**Type casting** = Telling the compiler "treat this reference as a different type."

```java
Object obj = new Person("Alice");
//     ^          ^
//     |          |-- actual object is Person
//     |-- reference type is Object
```

### Upcasting (Widening) — Always Safe, Automatic

**Going UP the hierarchy: Child → Parent**

```java
Person p = new Person("Alice");
Object o = p;             // UPCASTING — automatic, no cast operator needed
Object o2 = (Object) p;  // explicit cast — works but unnecessary
```

```
Hierarchy:    Object
                │
              Person  ← p points here
              
After upcasting:
  o also points to same Person object, but sees it as Object
```

✅ Always safe — a Person IS always an Object.

### Downcasting (Narrowing) — Requires Explicit Cast + Runtime Check

**Going DOWN the hierarchy: Parent → Child**

```java
Object obj = new Person("Alice");  // upcast (Person stored as Object)
Person p = (Person) obj;           // DOWNCAST — explicit cast required
```

```
Before cast:  obj ──────▶ Person Object in heap
After cast:   p ──────────▶ Person Object in heap (same object!)
              
              We're just changing how we VIEW the object, not the object itself.
```

### Why is `(Person) obj` needed inside equals()?

```java
@Override
public boolean equals(Object obj) {
    // obj parameter is of type Object
    // We need to access Person-specific fields (name, age)
    // Object class doesn't have name or age!
    // So we must downcast:
    
    Person other = (Person) obj;  // tell compiler: "trust me, it's a Person"
    return this.name.equals(other.name);  // now we can access .name
}
```

**Without the cast:**
```java
obj.name  // COMPILE ERROR! Object doesn't have 'name' field
```

### The Danger of Downcasting — ClassCastException

```java
Object obj = new String("hello");  // obj is actually a String
Person p = (Person) obj;  // RUNTIME ERROR! ClassCastException!
// A String is NOT a Person!
```

### `instanceof` — The Safe Way

```java
@Override
public boolean equals(Object obj) {
    if (obj == null) return false;
    if (this == obj) return true;
    
    if (!(obj instanceof Person)) {  // safety check BEFORE casting
        return false;
    }
    
    Person other = (Person) obj;  // now safe to cast
    return this.name.equals(other.name) && this.age == other.age;
}
```

### `instanceof` with Pattern Matching (Java 16+)

```java
// Traditional
if (obj instanceof Person) {
    Person p = (Person) obj;  // redundant cast
    System.out.println(p.name);
}

// Modern — pattern matching
if (obj instanceof Person p) {  // cast + bind in one step!
    System.out.println(p.name);
}
```

---

## 7.6 Complete equals() Implementation

```java
public class Person {
    private String name;
    private int age;
    private String email;
    
    // Constructor, getters...
    
    @Override
    public boolean equals(Object obj) {
        // Rule 1: Reflexive — x.equals(x) must be true
        if (this == obj) return true;
        
        // Rule 2: Handle null — x.equals(null) must be false
        if (obj == null) return false;
        
        // Rule 3: Type check — must be same type
        if (!(obj instanceof Person)) return false;
        
        // Rule 4: Downcast safely
        Person other = (Person) obj;
        
        // Rule 5: Compare all relevant fields
        return Objects.equals(this.name, other.name)  // null-safe!
            && this.age == other.age
            && Objects.equals(this.email, other.email);
    }
}
```

---

## 7.7 The 5 Contracts of equals()

| Contract | Meaning | Example |
|----------|---------|---------|
| **Reflexive** | x.equals(x) = true | A person equals themselves |
| **Symmetric** | x.equals(y) = y.equals(x) | If Alice = Bob, then Bob = Alice |
| **Transitive** | x=y and y=z → x=z | If Alice=Bob and Bob=Charlie, then Alice=Charlie |
| **Consistent** | Same result on repeated calls | Unless state changes |
| **Null-safe** | x.equals(null) = false | Never equal to null |

---

# ═══════════════════════════════════════════
# SECTION 8: MASTERING hashCode()
# ═══════════════════════════════════════════

## 8.1 What is hashCode()?

`hashCode()` returns an **integer** that represents the object. Think of it as a fast-lookup fingerprint.

```java
// In Object:
public native int hashCode();  // native = implemented in C, uses memory address
```

```java
Person p = new Person("Alice", 25);
System.out.println(p.hashCode());  // some integer, e.g., 366712642
```

---

## 8.2 Why hashCode() Exists — The Performance Story

### Problem: Finding items in a collection

Without hashing — searching 1 million items:
```
[Alice, Bob, Charlie, Dave, ... 1,000,000 items]
                    
Looking for "Zara":
Check Alice → Not Zara
Check Bob → Not Zara
...
Check 1,000,000th item → Found!

Time: O(n) — LINEAR — too slow!
```

With hashing — searching 1 million items:
```
hashCode("Zara") = 3457
Bucket[3457] → [Zara]  
FOUND! O(1) — CONSTANT — instant!
```

---

## 8.3 hashCode in Action — The Bucket Concept

```
Hash table with 16 buckets:

Bucket 0:  [ ]
Bucket 1:  [Alice → obj1]
Bucket 2:  [ ]
Bucket 3:  [Bob → obj2] → [Charlie → obj3]  (collision!)
Bucket 4:  [Dave → obj4]
...
Bucket 15: [ ]

When looking up "Alice":
1. hashCode("Alice") % 16 = 1  (calculate bucket)
2. Go to Bucket 1               (O(1) lookup)
3. Check Alice → found!         (O(1) in best case)
```

---

## 8.4 Object Identity vs Content Hashing

```java
// Default hashCode (in Object) — based on IDENTITY (memory address)
Person p1 = new Person("Alice", 25);
Person p2 = new Person("Alice", 25);

System.out.println(p1.hashCode());  // e.g., 1829164700
System.out.println(p2.hashCode());  // e.g., 2018699554 — DIFFERENT!
```

Same content → Different hashCodes. **This is a problem** (shown in Section 9).

**Override hashCode** to base it on content:
```java
@Override
public int hashCode() {
    return Objects.hash(name, age, email);  // content-based hash
}
```

Now: same content → same hashCode.

---

## 8.5 Collisions — When Two Objects Share a hashCode

```java
Person pA = new Person("Alice", 25);  // hashCode = 100
Person pB = new Person("Bob", 30);    // hashCode = 100  (collision!)

// Both go to bucket 100
// Java handles this with a LINKED LIST in the bucket:
//
// Bucket 100: [pA] → [pB]
//
// When searching for pB:
// 1. Go to bucket 100
// 2. Check pA → not equal (equals() called!)
// 3. Check pB → equal! Found.
```

This is why **both** hashCode AND equals must be correct — hashCode finds the bucket, equals finds the exact object.

---

## 8.6 Writing a Good hashCode

```java
// Using Java's Objects.hash() utility (recommended):
@Override
public int hashCode() {
    return Objects.hash(name, age, email);
}

// Manual implementation (if needed):
@Override
public int hashCode() {
    int result = 17;           // prime number start
    result = 31 * result + (name != null ? name.hashCode() : 0);
    result = 31 * result + age;
    result = 31 * result + (email != null ? email.hashCode() : 0);
    return result;
}
// 31 is chosen because 31 * x = 32x - x = (x << 5) - x
// Modern CPUs optimize this to a shift operation
```

---

# ═══════════════════════════════════════════
# SECTION 9: equals() AND hashCode() CONTRACT
# ═══════════════════════════════════════════

## 9.1 The Golden Contract

```
┌─────────────────────────────────────────────────────────────┐
│                  THE CONTRACT                               │
│                                                             │
│  Rule 1: If a.equals(b) == true                             │
│          then a.hashCode() == b.hashCode() MUST be true     │
│                                                             │
│  Rule 2: If a.hashCode() == b.hashCode()                    │
│          then a.equals(b) MAY be true or false              │
│          (collision is allowed)                             │
│                                                             │
│  Contrapositive of Rule 1:                                  │
│  If a.hashCode() != b.hashCode()                            │
│  then a.equals(b) MUST be false                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9.2 What Breaks When You Violate the Contract

### Scenario 1: Override equals() but NOT hashCode()

```java
class Person {
    String name;
    
    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Person)) return false;
        return this.name.equals(((Person)obj).name);
    }
    // hashCode() NOT overridden — uses Object's identity-based hash!
}

Person p1 = new Person("Alice");
Person p2 = new Person("Alice");

System.out.println(p1.equals(p2));  // true (we said they're equal)
System.out.println(p1.hashCode());  // e.g., 1000
System.out.println(p2.hashCode());  // e.g., 2000  ← DIFFERENT! CONTRACT VIOLATED!
```

**HashMap goes WRONG:**
```java
HashMap<Person, String> map = new HashMap<>();
map.put(p1, "Engineer");

System.out.println(map.get(p2));  // null — SHOULD be "Engineer" but it's null!

// Why?
// put(p1):  hashCode(p1) = 1000 → Bucket 1000
// get(p2):  hashCode(p2) = 2000 → Bucket 2000 (WRONG BUCKET!)
//           Bucket 2000 is empty → returns null!
```

### Scenario 2: Override hashCode() but NOT equals()

```java
class Person {
    String name;
    
    @Override
    public int hashCode() { return name.hashCode(); }
    // equals() not overridden — uses == (reference comparison)
}

Person p1 = new Person("Alice");
Person p2 = new Person("Alice");

// Same bucket, but equals() uses ==
// p1 == p2 → false (different objects)
// So HashMap treats them as different keys!
map.put(p1, "Engineer");
map.put(p2, "Manager");  // Creates SECOND entry! Should have updated p1!
map.size() == 2  // Should be 1!
```

---

## 9.3 Correct Implementation — Together Always

```java
public class Person {
    private final String name;
    private final int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Person)) return false;
        Person other = (Person) obj;
        return Objects.equals(name, other.name) && age == other.age;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age);  // SAME FIELDS as equals!
    }
}
```

**Rule of thumb: If you override one, always override both. Always use the same fields in both.**

---

## 9.4 Using IDE/Lombok for Correctness

```java
// Lombok annotation (recommended for production):
@EqualsAndHashCode
public class Person {
    private String name;
    private int age;
}

// Java 16+ records automatically get correct equals/hashCode:
record Person(String name, int age) { }
// Correct equals() and hashCode() are auto-generated!
```

---

# ═══════════════════════════════════════════
# SECTION 10: HASHMAP INTERNALS
# ═══════════════════════════════════════════

## 10.1 What is a HashMap?

`HashMap<K, V>` is a data structure that stores **key-value pairs** with O(1) average-case lookup.

```java
HashMap<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
System.out.println(scores.get("Alice"));  // 95
```

---

## 10.2 Internal Structure

```java
// Simplified internal structure of HashMap:
class HashMap<K, V> {
    Node<K,V>[] table;  // array of buckets
    int size;           // number of entries
    int threshold;      // resize when size > threshold
    float loadFactor;   // default 0.75
    
    static class Node<K,V> {
        final int hash;     // cached hash of key
        final K key;
        V value;
        Node<K,V> next;     // linked list for chaining
    }
}
```

**Visual:**
```
HashMap internal array (capacity = 16 by default):

Index:    0    1    2    3    4    5    6    7    8...15
        ┌────┬────┬────┬────┬────┬────┬────┬────┬─────┐
table:  │null│null│Node│null│Node│null│null│Node│ ... │
        └────┴────┴────┴────┴────┴────┴────┴────┴─────┘
                   │          │          │
                  [k1,v1]    [k2,v2]   [k3,v3]─▶[k4,v4]
                                       (chained — collision)
```

---

## 10.3 put() — Step by Step

```java
map.put("Alice", 95);
```

**Step 1: Calculate hashCode**
```java
int hash = "Alice".hashCode();  // e.g., 63354551
```

**Step 2: Apply bit manipulation (spread hash bits)**
```java
// Internal HashMap does: hash = hash ^ (hash >>> 16)
// This reduces collisions by mixing high bits into low bits
int h = hash ^ (hash >>> 16);
```

**Step 3: Find bucket index**
```java
int index = h & (capacity - 1);  // e.g., h & 15 (for capacity 16)
// Equivalent to h % capacity, but faster using bitwise AND
// Works only when capacity is power of 2!
```

**Step 4: Insert into bucket**
```
If bucket[index] is empty:
    Create new Node(hash, "Alice", 95, null)
    bucket[index] = node
    
If bucket[index] has entries (collision):
    Walk linked list:
        If key already exists (equals() check): update value
        If key not found: add to end (or beginning in Java 7-)
```

```java
// Pseudocode for put():
void put(K key, V value) {
    int hash = hash(key.hashCode());
    int i = hash & (capacity - 1);
    
    Node<K,V> node = table[i];
    while (node != null) {
        if (node.hash == hash && node.key.equals(key)) {
            node.value = value;  // update existing
            return;
        }
        node = node.next;
    }
    
    // Key not found — add new node
    addNode(hash, key, value, i);
    
    if (++size > threshold) resize();  // rehash if needed
}
```

---

## 10.4 get() — Step by Step

```java
map.get("Alice");
```

1. `hash("Alice")` → same hash as during put()
2. `index = hash & (capacity-1)` → same bucket
3. Walk linked list in bucket
4. For each node: check `hash == node.hash && key.equals(node.key)`
5. Return `node.value` if found, `null` if not

**Why check hash FIRST before equals()?**
Hash comparison is O(1) integer comparison. `equals()` could be expensive (comparing long strings, complex objects). Checking hash first eliminates false candidates cheaply.

---

## 10.5 Capacity, Load Factor, Rehashing

```
Default capacity: 16
Default load factor: 0.75

Threshold = capacity * load factor = 16 * 0.75 = 12

When size > 12:
    New capacity = 32 (doubled, always power of 2)
    All existing entries rehashed and repositioned
    New threshold = 32 * 0.75 = 24
```

**Rehashing is expensive** — O(n). Choose initial capacity wisely:
```java
// If you know you'll store ~100 entries:
HashMap<K,V> map = new HashMap<>(128, 0.75f);
// 128 > 100/0.75 = 134... actually use 256 to avoid rehashing
HashMap<K,V> map = new HashMap<>(256);
```

---

## 10.6 Treeification (Java 8+)

When a bucket's linked list grows too long (8+ entries), Java converts it to a **Red-Black Tree** for better performance:

```
Bucket (linked list — O(n) search):
[k1] → [k2] → [k3] → ... → [k8]  ← at 8 entries, TREEIFY!

Bucket (Red-Black Tree — O(log n) search):
           [k4]
          /    \
        [k2]  [k6]
        /  \  /  \
       [k1][k3][k5][k7]
```

```java
// From HashMap source:
static final int TREEIFY_THRESHOLD = 8;  // convert list to tree
static final int UNTREEIFY_THRESHOLD = 6;  // revert tree to list
static final int MIN_TREEIFY_CAPACITY = 64;  // min table size for tree
```

---

## 10.7 containsKey() and containsValue()

```java
// containsKey: O(1) average — uses hash
boolean containsKey(Object key) {
    return getNode(hash(key), key) != null;
}

// containsValue: O(n) — must scan ALL buckets!
boolean containsValue(Object value) {
    for (Node<K,V>[] tab = table; tab != null; ) {
        for (Node<K,V> e : tab) {
            while (e != null) {
                if (e.value.equals(value)) return true;
                e = e.next;
            }
        }
    }
    return false;
}
```

**Interview Takeaway:** `containsKey()` is O(1), `containsValue()` is O(n).

---

## 10.8 Key Requirements for HashMap Keys

1. Must implement `hashCode()` correctly
2. Must implement `equals()` correctly
3. The key **must not change** after insertion (immutable keys ideal)

```java
// DANGER: Mutable key
Person p = new Person("Alice", 25);
map.put(p, "Engineer");

p.name = "Bob";  // Key changed!
map.get(p);      // null — hash changed, wrong bucket!
```

**Always use immutable objects as HashMap keys: `String`, `Integer`, `LocalDate`, etc.**

---

# ═══════════════════════════════════════════
# SECTION 11: HASHSET INTERNALS
# ═══════════════════════════════════════════

## 11.1 HashSet is a HashMap in Disguise

```java
// From JDK source:
public class HashSet<E> implements Set<E> {
    private transient HashMap<E, Object> map;  // THE BACKING MAP
    
    private static final Object PRESENT = new Object();  // DUMMY VALUE
    
    public HashSet() {
        map = new HashMap<>();
    }
    
    public boolean add(E e) {
        return map.put(e, PRESENT) == null;
    }
    
    public boolean contains(Object o) {
        return map.containsKey(o);
    }
    
    public boolean remove(Object o) {
        return map.remove(o) == PRESENT;
    }
    
    public int size() {
        return map.size();
    }
}
```

**HashSet just wraps HashMap, using `PRESENT` as a dummy value for all entries.**

---

## 11.2 Why PRESENT Object?

`HashMap` requires a value. `HashSet` only cares about keys (uniqueness). So it uses a singleton `PRESENT` object as a placeholder value — same for every entry, wastes minimal memory.

```
HashSet: {Alice, Bob, Charlie}

Internally:
HashMap:
  "Alice" → PRESENT
  "Bob"   → PRESENT
  "Charlie" → PRESENT
```

---

## 11.3 Why HashSet Needs equals() and hashCode()

```java
Set<Person> people = new HashSet<>();
people.add(new Person("Alice", 25));
people.add(new Person("Alice", 25));  // Duplicate! Should not be added.

System.out.println(people.size());  // Should be 1, but...
```

**Without overriding equals/hashCode:** `size() == 2` — duplicates allowed! Both are different objects.
**With correct equals/hashCode:** `size() == 1` — correctly detected as duplicate.

---

## 11.4 add() Step by Step

```java
hashSet.add(new Person("Alice", 25));
```

1. Calls `map.put(person, PRESENT)`
2. HashMap computes `person.hashCode()` → bucket index
3. Checks if bucket has existing entry with same hash + equals()
4. If found: return `PRESENT` (old value) — `put()` returns old value, not null → `add()` returns false (duplicate)
5. If not found: insert new node → `put()` returns null → `add()` returns true

---

# ═══════════════════════════════════════════
# SECTION 12: ABSTRACTION
# ═══════════════════════════════════════════

## 🧠 The Mental Model

> **Real World Analogy:**
> When you drive a car, you use the **steering wheel, accelerator, and brakes** — the abstract interface.
> You don't think about fuel injection, transmission gears, or combustion cycles.
>
> Abstraction = **hiding complexity, showing essential interface.**

---

## 12.1 Abstract Classes

### Definition
An **abstract class** is a class that:
- Cannot be instantiated directly
- May have abstract methods (methods without body)
- May have concrete methods (with body)

```java
abstract class Shape {
    String color;
    
    // Abstract method — no body, MUST be overridden by subclass
    abstract double area();
    abstract double perimeter();
    
    // Concrete method — has body, inherited as-is
    void display() {
        System.out.println("Shape: " + color + ", Area: " + area());
    }
}

class Circle extends Shape {
    double radius;
    
    Circle(double radius, String color) {
        this.radius = radius;
        this.color = color;
    }
    
    @Override
    double area() { return Math.PI * radius * radius; }
    
    @Override
    double perimeter() { return 2 * Math.PI * radius; }
}

class Rectangle extends Shape {
    double width, height;
    
    Rectangle(double w, double h, String c) {
        width = w; height = h; color = c;
    }
    
    @Override
    double area() { return width * height; }
    
    @Override
    double perimeter() { return 2 * (width + height); }
}

// Shape s = new Shape();  // COMPILE ERROR! Cannot instantiate abstract class
Shape s = new Circle(5, "Red");  // OK — Circle is concrete
s.display();
```

### When to Use Abstract Classes

- You want to share **code** (concrete methods) among related classes
- You want to enforce that subclasses implement certain methods
- When classes share a common **IS-A** relationship
- When you need **constructors** or non-static/non-final fields in the base

---

## 12.2 Interfaces (Basic — Full in Section 13)

### Definition
An interface is a **pure contract** — it defines WHAT, not HOW.

```java
interface Drawable {
    void draw();           // abstract by default
    void resize(double factor);
}

interface Printable {
    void print();
}

class Circle implements Drawable, Printable {
    @Override
    public void draw() { System.out.println("Drawing circle"); }
    
    @Override
    public void resize(double factor) { /* ... */ }
    
    @Override
    public void print() { System.out.println("Printing circle"); }
}
```

---

## 12.3 Abstract Class vs Interface

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Instantiation | No | No |
| Methods | Abstract + Concrete | Abstract + default + static (Java 8+) |
| Fields | Any (instance + static) | Only `public static final` constants |
| Constructors | Yes | No |
| Multiple inheritance | No (single extends) | Yes (multiple implements) |
| Access modifiers | Any | public by default |
| Use when | IS-A with shared code | CAN-DO contract |
| Speed | Slightly faster | Slightly slower (interface dispatch) |

---

## 12.4 When to Choose What

```
USE ABSTRACT CLASS when:
  ✅ You want to share code among closely related classes
  ✅ You need instance variables (not constants)
  ✅ You need constructors
  ✅ Classes share IS-A relationship

USE INTERFACE when:
  ✅ Unrelated classes need the same behavior
     (e.g., Dog and Car both can be Serializable)
  ✅ You want multiple inheritance of type
  ✅ You're defining a CONTRACT (API)
  ✅ You want to enable duck typing

REAL EXAMPLE:
  AbstractList (abstract class) — shared list code
  List (interface) — the contract
  ArrayList, LinkedList — concrete implementations
```

---

# ═══════════════════════════════════════════
# SECTION 13: INTERFACE MASTERCLASS
# ═══════════════════════════════════════════

## 13.1 Interface Deep Dive

```java
interface Vehicle {
    // Constant (implicitly public static final)
    int MAX_SPEED = 200;
    
    // Abstract method (implicitly public abstract)
    void start();
    void stop();
    
    // Default method (Java 8+) — provides implementation
    default void honk() {
        System.out.println("Beep! Beep!");
    }
    
    // Static method (Java 8+) — called on interface, not instance
    static Vehicle create() {
        return new Car();
    }
    
    // Private method (Java 9+) — helper for default methods
    private void internalCheck() {
        System.out.println("Internal check");
    }
}
```

---

## 13.2 Default Methods — Why They Were Added

**Problem:** Java had millions of classes implementing `Collection` interface. Adding a new abstract method to `Collection` would break ALL of them!

**Solution:** `default` methods — new methods with implementations that don't force existing classes to override them.

```java
// Java 8 added:
interface Iterable<T> {
    default void forEach(Consumer<? super T> action) {
        for (T t : this) {
            action.accept(t);
        }
    }
}
// All existing List/Set implementations got forEach() for free!
```

**Custom example:**
```java
interface Greeting {
    String getName();
    
    default void greet() {  // default — optional to override
        System.out.println("Hello, " + getName() + "!");
    }
    
    default void greetFormal() {
        System.out.println("Good day, " + getName() + ".");
    }
}

class Person implements Greeting {
    private String name;
    
    @Override
    public String getName() { return name; }
    
    // greet() and greetFormal() are inherited — no need to implement!
    
    // Optionally override:
    @Override
    public void greet() {
        System.out.println("Hey " + getName() + "!");
    }
}
```

---

## 13.3 Diamond Problem with Default Methods

```java
interface A {
    default void hello() { System.out.println("A"); }
}

interface B extends A {
    default void hello() { System.out.println("B"); }
}

interface C extends A {
    default void hello() { System.out.println("C"); }
}

class D implements B, C {
    // COMPILE ERROR! Ambiguous default method!
    // Must resolve explicitly:
    
    @Override
    public void hello() {
        B.super.hello();  // explicitly choose B's version
    }
}
```

**Rules for resolving default method conflicts:**
1. **Classes win over interfaces** — class method always takes priority
2. **More specific interface wins** — subinterface wins over superinterface
3. **Explicit override required** if still ambiguous

---

## 13.4 Functional Interfaces

A **functional interface** has exactly ONE abstract method (can have multiple default/static methods).

```java
@FunctionalInterface  // optional annotation — compiler enforces 1 abstract method
interface Transformer<T, R> {
    R transform(T input);  // single abstract method
    
    default Transformer<T, R> andThen(/* ... */) { /* ... */ }
}
```

**Built-in functional interfaces (java.util.function):**

| Interface | Method | Example |
|-----------|--------|---------|
| `Predicate<T>` | `boolean test(T t)` | `n -> n > 0` |
| `Function<T,R>` | `R apply(T t)` | `s -> s.length()` |
| `Consumer<T>` | `void accept(T t)` | `s -> print(s)` |
| `Supplier<T>` | `T get()` | `() -> new Person()` |
| `BiFunction<T,U,R>` | `R apply(T t, U u)` | `(a,b) -> a+b` |
| `UnaryOperator<T>` | `T apply(T t)` | `n -> n * 2` |
| `Comparator<T>` | `int compare(T o1, T o2)` | Lambda comparator |

---

## 13.5 Lambda Expressions — Implementing Functional Interfaces

**Lambda = anonymous implementation of a functional interface**

```java
// Traditional anonymous class:
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running!");
    }
};

// Lambda equivalent (much shorter):
Runnable r = () -> System.out.println("Running!");
```

**Lambda syntax:**
```java
// No params:
() -> System.out.println("Hello")

// One param (parentheses optional):
name -> System.out.println("Hello " + name)

// Multiple params:
(a, b) -> a + b

// Block body:
(a, b) -> {
    int sum = a + b;
    return sum;
}
```

**Real example:**
```java
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");

// Sort with lambda:
names.sort((a, b) -> a.compareTo(b));

// Method reference (even shorter):
names.sort(String::compareTo);

// forEach with lambda:
names.forEach(name -> System.out.println(name));
names.forEach(System.out::println);  // method reference
```

---

## 13.6 Interface vs Abstract Class — Full Decision Tree

```
Do you need to share implementation code?
    │
    ├── YES: Does the class need constructors or instance state?
    │           ├── YES → Abstract Class
    │           └── NO  → Interface with default methods (Java 8+)
    │
    └── NO: Is this a pure contract/capability?
                └── YES → Interface
```

---

# ═══════════════════════════════════════════
# SECTION 14: ADVANCED OOP RELATIONSHIPS
# ═══════════════════════════════════════════

## 14.1 The Three Relationships: Association, Aggregation, Composition

### Quick Summary:

```
IS-A  → Inheritance  (Dog IS-A Animal)
HAS-A → Association relationships (Car HAS-A Engine)
        ├── Aggregation (loose HAS-A)
        └── Composition (strong HAS-A)
```

---

## 14.2 Association

**Definition:** A general relationship where objects **know about** each other, but neither owns the other.

```
Teacher ──────── Student
(teaches)        (learns from)
Both exist independently.
```

```java
class Teacher {
    String name;
    List<Student> students;  // Teacher knows about students
    
    void teach(Student s) {
        System.out.println(name + " teaches " + s.name);
    }
}

class Student {
    String name;
    Teacher teacher;  // Student knows about teacher
}
```

**Key:** Teacher and Student can exist without each other. If teacher is deleted, students still exist.

**Multiplicity:**
- One-to-One (one teacher per student)
- One-to-Many (one teacher, many students)
- Many-to-Many (multiple teachers, multiple students)

---

## 14.3 Aggregation — Weak HAS-A

**Definition:** A HAS-A relationship where the **part can exist without the whole**.

```
Department ◇───── Professor
(contains)
If Department is disbanded, Professors still exist elsewhere.
```

```java
class Professor {
    String name;
    String specialization;
    // Professor exists independently
}

class Department {
    String deptName;
    List<Professor> professors;  // aggregation — professors pre-exist
    
    Department(String name) {
        this.deptName = name;
        this.professors = new ArrayList<>();
    }
    
    void addProfessor(Professor p) {
        professors.add(p);  // department doesn't CREATE professors
    }
}

Professor prof1 = new Professor("Dr. Smith");  // created outside
Department cs = new Department("CS");
cs.addProfessor(prof1);  // just associated
// If cs is destroyed, prof1 still exists!
```

**Real-world:** A library HAS books. If the library burns down, the knowledge (books) might still exist elsewhere.

---

## 14.4 Composition — Strong HAS-A

**Definition:** A HAS-A relationship where the **part cannot exist without the whole**. The whole **creates and owns** the parts.

```
House ◆───── Room
(composed of)
If House is demolished, Rooms cease to exist.
```

```java
class Room {
    String type;
    double area;
    
    Room(String type, double area) {
        this.type = type;
        this.area = area;
    }
}

class House {
    String address;
    List<Room> rooms;  // composition — House CREATES rooms
    
    House(String address, int numRooms) {
        this.address = address;
        this.rooms = new ArrayList<>();
        
        // House creates its own rooms
        for (int i = 0; i < numRooms; i++) {
            rooms.add(new Room("Room " + (i+1), 150.0));
        }
    }
    
    // When House is garbage collected, rooms are also unreachable → GC'd
}
```

**Composition in Java:**
```java
class Engine {
    int horsepower;
    void start() { System.out.println("Engine started"); }
}

class Car {
    private final Engine engine;  // private + final = strong ownership
    String brand;
    
    Car(String brand, int hp) {
        this.brand = brand;
        this.engine = new Engine();  // Car CREATES its engine
        this.engine.horsepower = hp;
    }
    
    void drive() {
        engine.start();  // Car uses its engine
        System.out.println(brand + " is driving!");
    }
}
```

---

## 14.5 Aggregation vs Composition — Key Test

**Question: "Can the part exist without the whole?"**

```
YES → Aggregation (weak HAS-A)
NO  → Composition (strong HAS-A)

Examples:
  University HAS Departments:
    Department can't exist without University → COMPOSITION
    
  Playlist HAS Songs:
    Song can exist without Playlist → AGGREGATION
    
  Car HAS Engine:
    Car's engine is built for that car, meaningless alone → COMPOSITION
    
  Library HAS Books:
    Book exists outside library → AGGREGATION
```

---

## 14.6 UML Notation Reference

```
Inheritance (IS-A):       A ──▷ B  (A extends B)

Association:              A ────── B

Aggregation (weak HAS-A): A ◇──── B  (hollow diamond at whole)

Composition (strong HAS-A): A ◆──── B  (filled diamond at whole)

Interface implementation: A ──▷ «interface» I
```

---

# ═══════════════════════════════════════════
# SECTION 15: JVM INTERNALS RELATED TO OOP
# ═══════════════════════════════════════════

## 15.1 JVM Memory Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                              JVM                                  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                         HEAP                             │    │
│  │                                                          │    │
│  │  ┌─────────────────────┐  ┌───────────────────────────┐ │    │
│  │  │    Young Generation  │  │      Old Generation       │ │    │
│  │  │  ┌──────┬─────┬────┐│  │  (long-lived objects)     │ │    │
│  │  │  │ Eden │  S0 │ S1 ││  │                           │ │    │
│  │  │  └──────┴─────┴────┘│  └───────────────────────────┘ │    │
│  │  └─────────────────────┘                                  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────┐  ┌─────────────────────────────────────────┐   │
│  │    STACK     │  │            METHOD AREA (Metaspace)      │   │
│  │  (per thread)│  │  Class bytecode                        │   │
│  │ ┌──────────┐ │  │  Static variables                      │   │
│  │ │main frame│ │  │  String pool                           │   │
│  │ │ local    │ │  │  vtables                               │   │
│  │ │ variables│ │  │  Constant pool                         │   │
│  │ └──────────┘ │  └─────────────────────────────────────────┘   │
│  └──────────────┘                                                 │
│                                                                   │
│  ┌──────────────────┐  ┌────────────────────────┐               │
│  │  PC Registers    │  │  Native Method Stack   │               │
│  └──────────────────┘  └────────────────────────┘               │
└───────────────────────────────────────────────────────────────────┘
```

---

## 15.2 Class Loading

When JVM encounters `new Student()` for the first time:

**Step 1: Loading**
```
ClassLoader finds Student.class file
Reads bytecode into memory
Creates Class object in Method Area
```

**Step 2: Linking**
```
Verification: Is bytecode valid? Safe?
Preparation: Allocate static fields, set default values
Resolution: Resolve symbolic references (method names → memory addresses)
```

**Step 3: Initialization**
```
Execute static initializers in order
Execute static blocks
```

**Step 4: Object Creation (when `new` is called)**
```
Allocate memory on Heap for object
Initialize fields to default values (0, null, false)
Call constructor
Return reference
```

---

## 15.3 Object Creation — Detailed Process

```java
Student s = new Student("Alice", 20);
```

**Step-by-step:**

```
1. JVM checks if Student class is loaded → load if not

2. JVM allocates memory on Heap:
   Size = sum of all instance fields (+ object header)
   
   Object Header (hidden):
   ┌─────────────────────────────────────────┐
   │ Mark Word (8 bytes):                    │
   │   - hashCode (after first call)         │
   │   - GC age                              │
   │   - lock state                          │
   │ Class Pointer (4-8 bytes):              │
   │   - points to Class metadata in         │
   │     Metaspace (vtable lives here!)      │
   └─────────────────────────────────────────┘
   
3. Initialize all fields to default values:
   name = null, age = 0
   
4. Execute constructor: name = "Alice", age = 20

5. Reference to new object stored in s (on stack)
```

---

## 15.4 Method Area — Where Class Definitions Live

```
Method Area (Metaspace):
┌──────────────────────────────────────────────┐
│ Student class:                               │
│   ┌────────────────────────────────────┐    │
│   │ Bytecode for each method           │    │
│   │ Field metadata                     │    │
│   │ vtable:                            │    │
│   │   [0] Object.toString  → &toString │    │
│   │   [1] Object.equals    → &equals   │    │
│   │   [2] Object.hashCode  → &hashCode │    │
│   │   [3] Student.study    → &study    │    │
│   └────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

When `Dog extends Animal` and overrides `sound()`:
```
Dog's vtable:
  [0] Object.toString   → Object's toString (not overridden)
  [1] Animal.eat        → Animal's eat (inherited)
  [2] Animal.sound      → Dog.sound  ← OVERRIDDEN! Points to Dog's version
  [3] Dog.fetch         → Dog.fetch
```

---

## 15.5 Stack Frame — What Happens per Method Call

```java
public void study(String subject) {
    int hours = 5;
    System.out.println(name + " studies " + subject + " for " + hours + " hours");
}
```

```
Stack frame for study():
┌──────────────────────────────┐
│ Return address               │
│ subject = "Math" (reference) │
│ hours   = 5 (primitive)      │
│ this    = 0x1A4F (reference) │  ← points to object on Heap
└──────────────────────────────┘
```

**Key insight:** `this` in every instance method is an invisible first parameter pointing to the current object on the Heap.

---

## 15.6 Garbage Collection and Objects

```java
Student s1 = new Student("Alice", 20);  // Object A on Heap
Student s2 = new Student("Bob", 25);    // Object B on Heap
s1 = s2;  // s1 now points to Object B

// Object A (Alice) has no references — eligible for GC!
// GC will eventually reclaim Object A's memory
```

```
After s1 = s2:

STACK              HEAP
┌──────────┐      ┌───────────────┐   ┌───────────────┐
│ s1=0xBBB │─────▶│ "Bob" Object  │   │ "Alice" Object│◄─ no references!
│ s2=0xBBB │─────▶│               │   │               │   GC eligible
└──────────┘      └───────────────┘   └───────────────┘
```

---

# ═══════════════════════════════════════════
# SECTION 16: TOP 100 OOP INTERVIEW QUESTIONS
# ═══════════════════════════════════════════

## 🟢 BEGINNER LEVEL (Q1-Q30)

**Q1: What are the four pillars of OOP?**
> **Encapsulation, Inheritance, Polymorphism, Abstraction.**
> - Encapsulation: Bundling data + behavior, hiding internals.
> - Inheritance: Child class acquires parent's properties.
> - Polymorphism: One interface, multiple forms.
> - Abstraction: Hiding implementation, showing interface.

**Q2: What is the difference between a class and an object?**
> A class is a **blueprint** (template/type definition). An object is an **instance** — a concrete entity in memory with actual values.

**Q3: Where are objects stored in Java?**
> **Heap memory.** Reference variables (pointing to objects) are stored on the Stack.

**Q4: What is a constructor? How is it different from a method?**
> Constructor: same name as class, no return type, called automatically with `new`. A method: has return type, called explicitly, any name.

**Q5: What is constructor overloading?**
> Having multiple constructors with different parameter lists in the same class.

**Q6: What is `this` keyword?**
> Reference to the **current object**. Used to disambiguate fields from parameters, call other constructors (`this()`), or pass the current object.

**Q7: What is `super` keyword?**
> Reference to the **parent class**. Used to call parent constructor (`super()`), access parent fields (`super.field`), call parent methods (`super.method()`).

**Q8: What are access modifiers in Java?**
> `private` (class only), `default` (package), `protected` (package + subclasses), `public` (everywhere).

**Q9: What is encapsulation?**
> Bundling data and methods, restricting direct field access via `private`, controlling access through getters/setters.

**Q10: What is the difference between `==` and `equals()`?**
> `==` compares **references** (memory addresses). `equals()` compares **content** (logical equality, as defined by override).

**Q11: What is method overloading?**
> Multiple methods in same class with same name but different parameter lists. Resolved at compile time.

**Q12: What is method overriding?**
> Child class provides its own implementation of a parent class method with the same signature. Resolved at runtime.

**Q13: What is the default value of a reference variable?**
> `null` — it points to nothing.

**Q14: Can we override a `static` method?**
> No. Static methods belong to the class, not objects. Defining same static method in child class is **method hiding**, not overriding. No dynamic dispatch.

**Q15: Can we override a `private` method?**
> No. Private methods are not inherited, so cannot be overridden. Defining same method in subclass creates a new, unrelated method.

**Q16: What is inheritance?**
> Mechanism where a child class acquires properties/behaviors of parent class via `extends`. Enables code reuse.

**Q17: What is the `final` keyword?**
> - `final` variable: constant, cannot be reassigned.
> - `final` method: cannot be overridden.
> - `final` class: cannot be subclassed.

**Q18: Why is multiple inheritance not supported in Java (for classes)?**
> The **Diamond Problem** — ambiguity when multiple parents define the same method. Java avoids this via single class inheritance; interfaces solve it differently.

**Q19: What is `java.lang.Object`?**
> The root of the class hierarchy. Every Java class implicitly extends `Object`. It provides `toString()`, `equals()`, `hashCode()`, `clone()`, `getClass()`.

**Q20: What is an abstract class?**
> A class that cannot be instantiated, may have abstract methods (no body). Subclasses must implement all abstract methods.

**Q21: What is an interface?**
> A contract defining what methods a class must implement. Supports multiple implementation. Methods are `public abstract` by default.

**Q22: What happens if you don't override `toString()`?**
> `Object.toString()` returns `ClassName@hexHashCode`, which is not meaningful.

**Q23: What is `NullPointerException`?**
> Thrown when you try to call a method or access a field on a null reference (no object).

**Q24: Can constructors be inherited?**
> No. But child constructors implicitly call `super()` to invoke parent constructors.

**Q25: What is an immutable class?**
> A class whose state cannot change after construction. Make it `final`, fields `private final`, no setters, defensive copies for mutable fields.

**Q26: What is the difference between shallow copy and deep copy?**
> Shallow copy: copies references (shared mutable objects). Deep copy: copies the objects themselves (fully independent).

**Q27: What does `@Override` do?**
> Annotation telling compiler "this method overrides a parent method." Compiler gives an error if it doesn't actually override (prevents bugs from typos).

**Q28: Can an abstract class have a constructor?**
> Yes! Abstract class constructors are called by subclass constructors via `super()`.

**Q29: Can an interface have a constructor?**
> No. Interfaces cannot be instantiated, so constructors make no sense.

**Q30: What is the IS-A relationship?**
> Inheritance relationship. `Dog IS-A Animal`. Used to model things that are a specialized version of something else.

---

## 🟡 INTERMEDIATE LEVEL (Q31-Q65)

**Q31: Explain dynamic method dispatch.**
> The mechanism by which Java determines which overridden method to call at runtime based on the **actual object type**, not the reference type. Done via vtable lookup.

**Q32: What is covariant return type?**
> An overriding method can return a **subtype** of the parent method's return type.
> ```java
> class Animal { Animal get() { return new Animal(); } }
> class Dog extends Animal { Dog get() { return new Dog(); } }  // valid!
> ```

**Q33: Can we reduce the access modifier while overriding?**
> No. You can **widen** (protected → public) but not **narrow** (public → protected). This preserves the contract.

**Q34: What is the hashCode-equals contract?**
> If `a.equals(b) == true`, then `a.hashCode() == b.hashCode()` must also be true. The reverse is not required (collisions allowed).

**Q35: Why should you override hashCode when you override equals?**
> HashMap/HashSet use hashCode to find the bucket. If equal objects have different hashCodes, they'll be placed in different buckets → lookups fail → broken behavior.

**Q36: What is the internal structure of HashMap?**
> Array of `Node` (linked list nodes). Each entry has `hash`, `key`, `value`, `next`. Java 8+: linked list becomes Red-Black Tree when bucket has 8+ entries.

**Q37: What is the default capacity and load factor of HashMap?**
> Capacity: **16** (always power of 2). Load factor: **0.75**. Threshold = 16 × 0.75 = 12. When size > 12, resize to 32.

**Q38: How does HashMap handle collisions?**
> **Separate chaining** — multiple entries in same bucket form a linked list. Java 8+ converts long chains (≥8) to Red-Black trees.

**Q39: What is the difference between HashMap and HashSet?**
> HashSet is a HashMap where all values are the same dummy object (`PRESENT`). HashSet stores only keys; HashMap stores key-value pairs.

**Q40: Why should HashMap keys be immutable?**
> If a key's hashCode changes after insertion, get() searches the wrong bucket → key not found. Immutable keys guarantee consistent hash.

**Q41: What is the difference between abstract class and interface?**
> Abstract class: single inheritance, can have constructors, instance fields, any access modifier. Interface: multiple implementation, no constructors, only constants + abstract/default/static methods.

**Q42: When to use abstract class vs interface?**
> Abstract class: closely related classes sharing code (IS-A with implementation). Interface: unrelated classes sharing capability/contract (CAN-DO).

**Q43: What are default methods in interfaces?**
> Methods with implementation added in Java 8. Allow adding new methods to interfaces without breaking existing implementations.

**Q44: What is a functional interface?**
> An interface with exactly ONE abstract method. Enables lambda expressions. Examples: `Runnable`, `Comparator`, `Predicate`, `Function`.

**Q45: What is a lambda expression?**
> A concise way to implement a functional interface. Syntax: `(params) -> expression`. Example: `() -> System.out.println("hi")`.

**Q46: What is the difference between Aggregation and Composition?**
> Aggregation: part can exist without whole (weak HAS-A). Composition: part cannot exist without whole (strong HAS-A, whole creates parts).

**Q47: What is method hiding (static methods)?**
> When a subclass defines a static method with same signature as parent's static method. NOT overriding — resolved at compile time based on reference type.

**Q48: What is a vtable?**
> Virtual Method Table — a per-class table mapping method signatures to their implementations. Used by JVM for dynamic dispatch at runtime.

**Q49: What does `instanceof` do?**
> Checks if an object is an instance of a class or implements an interface. Returns boolean. Returns `false` for `null`. Safe before downcasting.

**Q50: What is upcasting and downcasting?**
> Upcasting: child → parent reference (automatic, safe). Downcasting: parent → child reference (explicit, needs cast operator, may throw ClassCastException).

**Q51: Why does `equals(Object obj)` use `Object` parameter instead of the specific type?**
> To truly **override** `Object.equals()`. If you use specific type (e.g., `Person`), you're overloading, not overriding. The `Object` parameter ensures the override.

**Q52: What is the String Pool?**
> A special area in heap (Method Area) where String literals are stored. Same literal reuses one object. `new String()` bypasses the pool.

**Q53: Can we call an overridden method from a constructor?**
> Yes, but it's dangerous. If a subclass overrides the method and the superclass constructor calls it, the overriding version runs before the subclass constructor completes — fields may be uninitialized.

**Q54: What is the order of initialization in Java?**
> 1. Static blocks (top to bottom, once per class load)
> 2. Instance initializer blocks (top to bottom, per object)
> 3. Constructor

**Q55: What is `Objects.equals(a, b)`?**
> Null-safe equality check. Returns `false` if either is null without NullPointerException. Equivalent to `(a == b) || (a != null && a.equals(b))`.

**Q56: What is `Objects.hash(fields...)`?**
> Convenience method to compute hashCode from multiple fields. Handles nulls safely.

**Q57: What happens when put() is called with a duplicate key in HashMap?**
> Old value is replaced with new value. `put()` returns the old value.

**Q58: What is `containsKey()` vs `containsValue()` in HashMap?**
> `containsKey()`: O(1) — uses hash. `containsValue()`: O(n) — scans all buckets.

**Q59: What is rehashing in HashMap?**
> When size exceeds threshold (capacity × loadFactor), the table is resized (doubled). All existing entries are recalculated and repositioned. O(n) operation.

**Q60: What is treeification in HashMap?**
> When a bucket's chain length ≥ 8 AND table capacity ≥ 64, the chain converts to a Red-Black Tree. Improves worst-case from O(n) to O(log n).

**Q61: What is the `Cloneable` interface?**
> Marker interface enabling `Object.clone()`. Without implementing it, clone() throws `CloneNotSupportedException`. Even then, clone() does shallow copy.

**Q62: What is the `Serializable` interface?**
> Marker interface enabling object serialization (converting to byte stream for storage/network transmission).

**Q63: What are marker interfaces?**
> Interfaces with no methods — just used to "mark" a class for special JVM or framework behavior. Examples: `Cloneable`, `Serializable`, `RandomAccess`.

**Q64: What is association in OOP?**
> A general "uses-a" or "knows-a" relationship between objects. Neither creates nor manages the lifetime of the other.

**Q65: What is the difference between method overriding and method hiding?**
> Overriding: instance methods, resolved at runtime based on object type. Hiding: static methods, resolved at compile time based on reference type.

---

## 🔴 ADVANCED LEVEL (Q66-Q100)

**Q66: How does JVM implement polymorphism at the bytecode level?**
> Through `invokevirtual` bytecode instruction — looks up method in object's vtable at runtime. Static calls use `invokestatic` (no vtable). Interface calls use `invokeinterface`.

**Q67: What is `invokespecial` in JVM?**
> Used for constructor calls, private methods, and `super` method calls. These never need vtable lookup — always directly bound.

**Q68: Can HashMap have a null key?**
> Yes, exactly **one null key** is allowed. Null key is placed in bucket 0 (hash = 0). `Hashtable` does not allow null keys.

**Q69: What is the difference between HashMap, LinkedHashMap, and TreeMap?**
> - HashMap: No ordering, O(1) ops.
> - LinkedHashMap: Maintains insertion order (doubly linked list + HashMap).
> - TreeMap: Natural ordering or custom Comparator, O(log n) ops (Red-Black Tree).

**Q70: How does Java handle the equals/hashCode contract for records?**
> Java records (Java 14+) auto-generate `equals()` and `hashCode()` based on all record components. Correct implementation guaranteed.

**Q71: What is the double-checked locking pattern in Singleton?**
```java
public class Singleton {
    private static volatile Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized(Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```
> `volatile` prevents CPU caching; double-check avoids synchronization overhead after initialization.

**Q72: Why is String immutable in Java?**
> 1. String Pool safety (shared references).
> 2. HashMap key safety (hashCode can't change).
> 3. Thread safety (no synchronization needed).
> 4. Security (file paths, class names can't be tampered).

**Q73: What is the Builder pattern and how does it relate to OOP?**
> Creational pattern for constructing complex objects step by step. Uses method chaining (`builder.setA().setB().build()`). Encapsulates construction logic. Good when many optional parameters.

**Q74: How does Java's garbage collector know when to collect an object?**
> When there are no more **reachable references** to the object. GC traces from GC roots (stack, static fields, JNI references) and marks reachable objects. Unreachable objects are collected.

**Q75: What is the `transient` keyword?**
> Marks a field as non-serializable. When object is serialized, transient fields are ignored (not written to byte stream).

**Q76: What is the difference between early binding and late binding?**
> Early binding (static): method resolved at compile time. Faster. Used for overloading, static methods, final methods, private methods. Late binding (dynamic): resolved at runtime via vtable. Used for overriding.

**Q77: Can an interface extend multiple interfaces?**
> Yes! Interfaces support multiple inheritance.
> ```java
> interface C extends A, B { }  // valid
> ```

**Q78: What is the `sealed` class in Java (Java 17+)?**
> A class that restricts which classes can extend it.
> ```java
> sealed class Shape permits Circle, Rectangle, Triangle { }
> ```
> Useful for exhaustive pattern matching.

**Q79: What is pattern matching in Java?**
> Java 16+: `instanceof` with binding variable. Java 17+: switch expressions with pattern matching. Reduces explicit casting.

**Q80: What is the cost of polymorphism in Java?**
> Virtual dispatch adds one indirection (vtable lookup). JIT compiler typically eliminates this overhead via **devirtualization** and **inlining** for frequently called methods.

**Q81: What is JIT compilation in relation to OOP?**
> JIT (Just-In-Time) compiler analyzes runtime behavior and can inline virtual method calls, eliminating polymorphism overhead for hotspot code.

**Q82: What are phantom, weak, and soft references?**
> Different reference strengths for GC behavior:
> - Strong: normal reference, prevents GC.
> - Soft: GC'd when low memory.
> - Weak: GC'd on next GC cycle.
> - Phantom: GC'd, get() always null, used for cleanup.

**Q83: What is the Liskov Substitution Principle (LSP)?**
> Objects of a superclass must be replaceable with objects of its subclasses without breaking correctness. A subclass should extend, not restrict, the parent's behavior.

**Q84: What is the Open/Closed Principle?**
> Classes should be open for extension, closed for modification. Add new behavior through inheritance/composition, not by editing existing code.

**Q85: What is SOLID?**
> - **S**: Single Responsibility Principle
> - **O**: Open/Closed Principle
> - **L**: Liskov Substitution Principle
> - **I**: Interface Segregation Principle
> - **D**: Dependency Inversion Principle

**Q86: What is the Dependency Inversion Principle?**
> High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces). Don't depend on concrete implementations.

**Q87: How does Java handle circular references in GC?**
> Java GC uses **reachability analysis** from GC roots, not reference counting. Circular references (A→B, B→A) with no external reference are both unreachable → both collected.

**Q88: What is the difference between `instanceof` and `getClass() ==`?**
> `instanceof` returns true for subclasses. `getClass() ==` is exact type match.
> ```java
> Dog d = new Dog();
> d instanceof Animal  // true
> d.getClass() == Animal.class  // false
> ```

**Q89: What are the implications of violating the equals/hashCode contract in a ConcurrentHashMap?**
> Same as HashMap — keys may not be found. Additionally, in concurrent scenarios, it can cause deadlocks or data corruption if hash changes mid-operation.

**Q90: What is the `finalize()` method and why is it deprecated?**
> Called by GC before collecting. Deprecated because: unpredictable timing, performance impact, can resurrect objects. Use `try-with-resources` and `Cleaner` (Java 9+) instead.

**Q91: What is object interning?**
> Storing only one copy of distinct values. `String.intern()` ensures only one String object per content in pool. `Integer.valueOf()` interns -128 to 127.

**Q92: What is the difference between `HashMap.putIfAbsent()` and `getOrDefault()`?**
> `putIfAbsent(key, val)`: inserts only if key not present; returns old value.
> `getOrDefault(key, def)`: returns value if present, else default (no insertion).

**Q93: Why does `HashMap` use power-of-2 capacity?**
> Index calculation: `hash & (capacity-1)`. For power-of-2, this equals `hash % capacity` but uses fast bitwise AND instead of expensive modulo.

**Q94: What is the load factor tradeoff in HashMap?**
> Lower load factor: fewer collisions, faster lookups, more memory waste.
> Higher load factor: more collisions, slower lookups, less memory waste.
> 0.75 is a balance (empirically good).

**Q95: How does `ConcurrentHashMap` differ from `HashMap`?**
> `ConcurrentHashMap` is thread-safe. Uses **segment locking** (Java 7) or **CAS + synchronized per bucket** (Java 8+). Allows concurrent reads. `HashMap` is not thread-safe.

**Q96: What is the `EnumMap` and when to use it?**
> A Map with enum keys. Uses array internally (enum ordinal as index). Very fast (O(1)) and compact. Use when all keys are from an enum.

**Q97: What is `IdentityHashMap`?**
> A HashMap that uses `==` (reference equality) for key comparison instead of `equals()`. Uses `System.identityHashCode()` instead of `hashCode()`. Used in graph traversal (cycle detection).

**Q98: How can you make a thread-safe Map in Java?**
> - `Collections.synchronizedMap(new HashMap<>())` — synchronizes every method
> - `ConcurrentHashMap` — better performance with fine-grained locking
> - `Hashtable` — legacy, avoid

**Q99: What is the `@FunctionalInterface` annotation?**
> Optional annotation that instructs the compiler to verify the interface has exactly one abstract method. Causes a compile error if violated.

**Q100: What is the difference between Comparable and Comparator?**
> `Comparable` (single method `compareTo()`): natural ordering defined in the class itself. `Comparator` (functional interface): external ordering defined separately, can have multiple. `Comparator` preferred for custom/multiple orderings.

---

# ═══════════════════════════════════════════
# SECTION 17: PRACTICE SECTION
# ═══════════════════════════════════════════

## Exercise 1: Overloading — Calculator

```java
// Problem: Create a Calculator class with overloaded add() methods

class Calculator {
    // TODO: Implement add() for:
    // 1. Two integers
    // 2. Three integers
    // 3. Two doubles
    // 4. An int and a double
    // 5. Varargs integers
}

// Solution:
class Calculator {
    int add(int a, int b) { return a + b; }
    int add(int a, int b, int c) { return a + b + c; }
    double add(double a, double b) { return a + b; }
    double add(int a, double b) { return a + b; }
    int add(int... nums) {
        int sum = 0;
        for (int n : nums) sum += n;
        return sum;
    }
    
    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println(c.add(1, 2));         // 3
        System.out.println(c.add(1, 2, 3));      // 6
        System.out.println(c.add(1.5, 2.5));     // 4.0
        System.out.println(c.add(1, 2, 3, 4, 5)); // 15 (varargs)
    }
}
```

## Exercise 2: Overriding — Shape Hierarchy

```java
// Problem: Create abstract Shape with area() and perimeter()
// Implement Circle, Rectangle, Triangle

// Solution:
abstract class Shape {
    abstract double area();
    abstract double perimeter();
    
    @Override
    public String toString() {
        return getClass().getSimpleName() + 
               "[area=" + String.format("%.2f", area()) + 
               ", perimeter=" + String.format("%.2f", perimeter()) + "]";
    }
}

class Circle extends Shape {
    double radius;
    Circle(double r) { this.radius = r; }
    
    @Override public double area() { return Math.PI * radius * radius; }
    @Override public double perimeter() { return 2 * Math.PI * radius; }
}

class Rectangle extends Shape {
    double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }
    
    @Override public double area() { return w * h; }
    @Override public double perimeter() { return 2 * (w + h); }
}

class Triangle extends Shape {
    double a, b, c;
    Triangle(double a, double b, double c) { this.a=a; this.b=b; this.c=c; }
    
    @Override
    public double area() {
        double s = (a+b+c)/2;
        return Math.sqrt(s*(s-a)*(s-b)*(s-c));
    }
    @Override public double perimeter() { return a + b + c; }
}
```

## Exercise 3: Polymorphism — Animal Sound System

```java
// Problem: Create Animal hierarchy. Use polymorphism to print all sounds.

class Animal {
    String name;
    Animal(String name) { this.name = name; }
    void makeSound() { System.out.println(name + " makes a sound"); }
}
class Dog extends Animal {
    Dog(String name) { super(name); }
    @Override void makeSound() { System.out.println(name + " says: Woof!"); }
}
class Cat extends Animal {
    Cat(String name) { super(name); }
    @Override void makeSound() { System.out.println(name + " says: Meow!"); }
}
class Duck extends Animal {
    Duck(String name) { super(name); }
    @Override void makeSound() { System.out.println(name + " says: Quack!"); }
}

public class Zoo {
    public static void main(String[] args) {
        Animal[] animals = { new Dog("Rex"), new Cat("Whiskers"), new Duck("Donald") };
        for (Animal a : animals) a.makeSound();
        // Rex says: Woof!
        // Whiskers says: Meow!
        // Donald says: Quack!
    }
}
```

## Exercise 4: Inheritance — Employee System

```java
// Problem: Create Employee hierarchy with salary calculation

class Employee {
    String name;
    double baseSalary;
    
    Employee(String name, double base) {
        this.name = name;
        this.baseSalary = base;
    }
    
    double calculateSalary() { return baseSalary; }
    
    @Override
    public String toString() {
        return name + ": $" + String.format("%.2f", calculateSalary());
    }
}

class Manager extends Employee {
    double bonus;
    Manager(String name, double base, double bonus) {
        super(name, base);
        this.bonus = bonus;
    }
    @Override
    double calculateSalary() { return super.calculateSalary() + bonus; }
}

class Contractor extends Employee {
    double hourlyRate;
    int hoursWorked;
    Contractor(String name, double rate, int hours) {
        super(name, 0);
        hourlyRate = rate; hoursWorked = hours;
    }
    @Override
    double calculateSalary() { return hourlyRate * hoursWorked; }
}

// Test:
Employee[] employees = {
    new Employee("Alice", 50000),
    new Manager("Bob", 80000, 20000),
    new Contractor("Charlie", 150, 160)
};
for (Employee e : employees) System.out.println(e);
```

## Exercise 5: equals() and hashCode() — Point Class

```java
// Problem: Implement a Point class with correct equals and hashCode

import java.util.Objects;

class Point {
    private final int x;
    private final int y;
    
    Point(int x, int y) { this.x = x; this.y = y; }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Point)) return false;
        Point other = (Point) obj;
        return this.x == other.x && this.y == other.y;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
    
    @Override
    public String toString() { return "Point(" + x + ", " + y + ")"; }
    
    public static void main(String[] args) {
        Point p1 = new Point(3, 4);
        Point p2 = new Point(3, 4);
        Point p3 = new Point(1, 2);
        
        System.out.println(p1.equals(p2));     // true
        System.out.println(p1.equals(p3));     // false
        System.out.println(p1.hashCode() == p2.hashCode());  // true
        
        // Use in HashSet:
        Set<Point> points = new HashSet<>();
        points.add(p1);
        points.add(p2);  // duplicate!
        System.out.println(points.size());  // 1
    }
}
```

## Exercise 6: HashMap Practice — Word Frequency Counter

```java
// Problem: Count word frequency in a text

import java.util.*;

public class WordFrequency {
    public static Map<String, Integer> count(String text) {
        Map<String, Integer> freq = new HashMap<>();
        String[] words = text.toLowerCase().split("\\s+");
        
        for (String word : words) {
            freq.merge(word, 1, Integer::sum);
            // Equivalent to:
            // freq.put(word, freq.getOrDefault(word, 0) + 1);
        }
        return freq;
    }
    
    public static void main(String[] args) {
        String text = "the quick brown fox jumps over the lazy dog the fox";
        Map<String, Integer> freq = count(text);
        
        // Sort by frequency:
        freq.entrySet().stream()
            .sorted(Map.Entry.<String,Integer>comparingByValue().reversed())
            .forEach(e -> System.out.println(e.getKey() + ": " + e.getValue()));
        // the: 3
        // fox: 2
        // ... (others: 1)
    }
}
```

## Exercise 7: Interface — Pluggable Sorting System

```java
// Problem: Create a sorting system with pluggable strategies

@FunctionalInterface
interface SortStrategy<T> {
    void sort(T[] arr);
}

class Sorter<T extends Comparable<T>> {
    private SortStrategy<T> strategy;
    
    Sorter(SortStrategy<T> strategy) { this.strategy = strategy; }
    
    void setStrategy(SortStrategy<T> strategy) { this.strategy = strategy; }
    
    void sort(T[] arr) { strategy.sort(arr); }
}

public class SortingDemo {
    public static void main(String[] args) {
        Integer[] arr = {5, 2, 8, 1, 9, 3};
        
        // Bubble sort strategy (lambda)
        SortStrategy<Integer> bubbleSort = data -> {
            int n = data.length;
            for (int i = 0; i < n-1; i++)
                for (int j = 0; j < n-i-1; j++)
                    if (data[j] > data[j+1]) {
                        int temp = data[j]; data[j] = data[j+1]; data[j+1] = temp;
                    }
        };
        
        Sorter<Integer> sorter = new Sorter<>(bubbleSort);
        sorter.sort(arr);
        System.out.println(Arrays.toString(arr));  // [1, 2, 3, 5, 8, 9]
    }
}
```

## Exercise 8: Composition vs Inheritance — Library System

```java
// Problem: Design a Library system using composition

class Book {
    String title;
    String author;
    String isbn;
    boolean isAvailable = true;
    
    Book(String title, String author, String isbn) {
        this.title = title; this.author = author; this.isbn = isbn;
    }
    @Override
    public String toString() { return title + " by " + author; }
}

class Library {
    private String name;
    private List<Book> books = new ArrayList<>();  // COMPOSITION
    
    Library(String name) { this.name = name; }
    
    void addBook(Book book) { books.add(book); }
    
    Optional<Book> findByIsbn(String isbn) {
        return books.stream().filter(b -> b.isbn.equals(isbn)).findFirst();
    }
    
    boolean checkout(String isbn) {
        Optional<Book> book = findByIsbn(isbn);
        if (book.isPresent() && book.get().isAvailable) {
            book.get().isAvailable = false;
            System.out.println("Checked out: " + book.get());
            return true;
        }
        return false;
    }
    
    boolean returnBook(String isbn) {
        Optional<Book> book = findByIsbn(isbn);
        if (book.isPresent() && !book.get().isAvailable) {
            book.get().isAvailable = true;
            System.out.println("Returned: " + book.get());
            return true;
        }
        return false;
    }
}
```

## Exercises 9-20: Additional Challenges

```java
// Exercise 9: Builder Pattern
// Create a PersonBuilder that builds Person objects fluently

class Person {
    private final String name;
    private final int age;
    private final String email;
    private final String phone;
    
    private Person(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.email = builder.email;
        this.phone = builder.phone;
    }
    
    public static class Builder {
        private String name;          // required
        private int age;              // required
        private String email = "";    // optional
        private String phone = "";    // optional
        
        Builder(String name, int age) { this.name=name; this.age=age; }
        Builder email(String e) { this.email=e; return this; }
        Builder phone(String p) { this.phone=p; return this; }
        Person build() { return new Person(this); }
    }
}
// Usage:
// Person p = new Person.Builder("Alice", 25).email("a@b.com").build();


// Exercise 10: Singleton with thread safety
class Config {
    private static volatile Config instance;
    private final Map<String, String> settings = new HashMap<>();
    
    private Config() {
        settings.put("env", "production");
    }
    
    public static Config getInstance() {
        if (instance == null) {
            synchronized(Config.class) {
                if (instance == null) instance = new Config();
            }
        }
        return instance;
    }
    
    public String get(String key) { return settings.getOrDefault(key, ""); }
}


// Exercise 11: Demonstrate HashMap failure without hashCode override
// (Run this to see the bug in action)
class BuggyKey {
    String value;
    BuggyKey(String v) { this.value = v; }
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof BuggyKey)) return false;
        return value.equals(((BuggyKey)o).value);
    }
    // NO hashCode override!
}

HashMap<BuggyKey, String> map = new HashMap<>();
BuggyKey k1 = new BuggyKey("hello");
map.put(k1, "world");
BuggyKey k2 = new BuggyKey("hello");
System.out.println(map.get(k2));  // null! Bug demonstrated.


// Exercise 12: Demonstrate correct fix
class CorrectKey {
    String value;
    CorrectKey(String v) { this.value = v; }
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof CorrectKey)) return false;
        return value.equals(((CorrectKey)o).value);
    }
    @Override
    public int hashCode() { return Objects.hash(value); }  // FIXED!
}

HashMap<CorrectKey, String> map = new HashMap<>();
CorrectKey k1 = new CorrectKey("hello");
map.put(k1, "world");
CorrectKey k2 = new CorrectKey("hello");
System.out.println(map.get(k2));  // "world" — correct!


// Exercise 13: Polymorphism with interfaces
interface Drawable { void draw(); }
interface Resizable { void resize(double factor); }

class Canvas {
    List<Drawable> elements = new ArrayList<>();
    void add(Drawable d) { elements.add(d); }
    void drawAll() { elements.forEach(Drawable::draw); }
}
// Any Drawable object can be added — Circle, Rectangle, etc.


// Exercise 14: Abstract template method pattern
abstract class DataProcessor {
    // Template method — defines the algorithm skeleton
    final void process() {
        readData();
        processData();
        writeData();
    }
    
    abstract void readData();
    abstract void processData();
    
    void writeData() {
        System.out.println("Default: writing to stdout");
    }
}

class CsvProcessor extends DataProcessor {
    @Override void readData() { System.out.println("Reading CSV"); }
    @Override void processData() { System.out.println("Processing CSV data"); }
}


// Exercise 15: equals with inheritance challenge
// Research: symmetric contract violation with inheritance
class ColorPoint extends Point {
    String color;
    
    // If you override equals to include color,
    // then Point.equals(ColorPoint) != ColorPoint.equals(Point)
    // SYMMETRY VIOLATED!
    // Use composition instead of inheritance for this case.
}


// Exercises 16-20: Design challenges (try yourself)

// Exercise 16: Implement an immutable Money class with currency
// Exercise 17: Implement Observer pattern using interfaces
// Exercise 18: Implement a generic Stack<T> with push/pop/peek
// Exercise 19: Create a LRU Cache using LinkedHashMap
// Exercise 20: Implement a deep clone for a complex object graph
```

---

# ═══════════════════════════════════════════
# SECTION 18: CHEAT SHEET — FINAL REVISION
# ═══════════════════════════════════════════

## 🏛️ The 4 Pillars

| Pillar | What | How | Why |
|--------|------|-----|-----|
| **Encapsulation** | Bundle + hide data | `private` fields + getters/setters | Protect state, controlled access |
| **Inheritance** | Child acquires parent | `extends` | Code reuse, IS-A relationship |
| **Polymorphism** | One interface, many forms | Overloading + Overriding | Flexibility, extensibility |
| **Abstraction** | Hide complexity | Abstract classes + Interfaces | Show essential, hide implementation |

---

## ⚡ Overloading vs Overriding — Quick Reference

```
OVERLOADING                    OVERRIDING
────────────────               ────────────────────
Same class                     Parent-Child classes
Same name, diff params         Same name, same params
Compile-time (static)          Runtime (dynamic)
No inheritance needed          Inheritance required
Return type can differ         Return type same/covariant
@Override: NO                  @Override: YES
```

---

## 📋 equals() Checklist

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;          // 1. Same reference?
    if (obj == null) return false;         // 2. Null check
    if (!(obj instanceof MyClass)) return false;  // 3. Type check
    MyClass other = (MyClass) obj;         // 4. Safe downcast
    return Objects.equals(field1, other.field1)   // 5. Field comparison
        && field2 == other.field2;
}
```

---

## 📋 hashCode Checklist

```java
@Override
public int hashCode() {
    return Objects.hash(field1, field2, field3);  // same fields as equals!
}
```

---

## 🔗 equals-hashCode Contract

```
equals() → true  ===  hashCode() must match
hashCode() match =/=>  equals() must be true (collision OK)

USE SAME FIELDS IN BOTH!
```

---

## 🗺️ HashMap Internals at a Glance

```
put(key, val):
  1. hash = key.hashCode() ⊕ (hash >>> 16)
  2. index = hash & (capacity-1)
  3. If bucket empty → insert Node
  4. Else → walk list: if equals() → update, else → append
  5. size > threshold? → resize (double capacity, rehash all)

get(key):
  1. Same hash + index calculation
  2. Walk bucket: find node where hash matches AND key.equals()
  3. Return node.value or null

Key defaults: capacity=16, loadFactor=0.75, threshold=12
Java 8+: bucket chain ≥8 → Red-Black Tree
```

---

## 🎯 HashSet Internals

```
HashSet<E>  =  HashMap<E, PRESENT>

add(e)       →  map.put(e, PRESENT)   returns null if new
contains(o)  →  map.containsKey(o)
remove(o)    →  map.remove(o) == PRESENT

Uniqueness guaranteed by equals() + hashCode()
```

---

## 🔁 Polymorphism — Quick Reference

```
COMPILE-TIME (Overloading):
  Resolved by: parameter types
  Speed: faster (static binding)
  JVM instruction: invokevirtual (but resolved early)

RUNTIME (Overriding):
  Resolved by: actual object type via vtable
  Speed: one indirection (JIT often eliminates)
  JVM instruction: invokevirtual → vtable lookup
```

---

## 🏗️ Object Class Key Methods

| Method | Purpose | Override? |
|--------|---------|----------|
| `toString()` | String representation | Always for debuggability |
| `equals(Object)` | Logical equality | When logical equality ≠ reference |
| `hashCode()` | Hash-based lookup | Always with equals() |
| `getClass()` | Runtime type | Rarely |
| `clone()` | Object copy | When needed (implement Cloneable) |

---

## 🔐 Casting Reference

```
UPCASTING (Child → Parent):
  Safe, automatic
  Object o = new Person();

DOWNCASTING (Parent → Child):
  Explicit, may throw ClassCastException
  Person p = (Person) o;  // safe only if o is actually a Person
  
  ALWAYS check first:
  if (o instanceof Person) {
      Person p = (Person) o;  // or: Person p = (Person) o directly in Java 16+
  }
```

---

## 🔑 Interface vs Abstract Class — Quick Rules

```
Abstract Class:
  ✅ Shared implementation code
  ✅ Instance variables
  ✅ Constructors
  ✅ Any access modifier
  ❌ Multiple inheritance

Interface:
  ✅ Multiple implementation
  ✅ Pure contract
  ✅ default methods (Java 8+)
  ✅ static methods (Java 8+)
  ❌ Instance variables
  ❌ Constructors
```

---

## 🧩 OOP Relationships Summary

```
IS-A  → extends / implements
      Dog IS-A Animal

HAS-A → field reference
      ├── Association: A uses B (loose)
      ├── Aggregation: A has B (B exists independently)
      └── Composition: A owns B (B exists only within A)
```

---

## ⚠️ Top Common Mistakes

```
1. Not overriding hashCode when overriding equals → HashMap breaks
2. Using == for String/Object comparison instead of equals()
3. Making HashMap keys mutable → hash changes, key lost
4. Not calling super() in child constructor → parent not initialized
5. Overlooking @Override → silent overloading instead of overriding
6. Violating equals() contracts (symmetry, transitivity)
7. Returning internal mutable collections from getters → encapsulation broken
8. Using abstract class when interface suffices (over-constraining API)
9. Circular constructor chaining → StackOverflowError
10. Not handling null in equals() → NullPointerException
```

---

## 🧠 Mental Model Summary

```
Think of OOP as a CITY:

CLASS        = Building blueprint
OBJECT       = Actual building
ENCAPSULATION = Building security (only enter through doors/reception)
INHERITANCE  = District inherits city infrastructure
POLYMORPHISM = "Emergency" means different things to police/fire/medical
ABSTRACTION  = City residents use services without knowing plumbing

HASHMAP      = City directory (hash = address lookup, bucket = street, 
               equals = exact house match)
HASHSET      = Unique addresses list (backed by the same directory)
EQUALS       = "Is this the same building?"
HASHCODE     = "Which street/zip code?"

The contract:
  Same building → Same zip code (always)
  Same zip code → Not necessarily same building (collisions)
```

---

> ## 🎓 You're Interview-Ready!
>
> You now understand:
> - ✅ Why `equals(Object obj)` uses `Object` — to truly override and enable polymorphic comparison
> - ✅ Why `Person p = (Person) obj` is needed — Object reference can't access Person fields
> - ✅ How overriding works — vtable, dynamic dispatch, late binding
> - ✅ How HashMap uses hashCode (bucket) + equals (exact match)
> - ✅ How HashSet is a HashMap with dummy PRESENT values
> - ✅ How all Java OOP concepts connect as one coherent system
>
> **Next steps:** Implement every exercise. Build a mini project using all these concepts. You're ready to ace any OOP interview!

---
*End of Java OOP Masterclass — Senior Architect Edition*
