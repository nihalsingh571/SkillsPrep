# Java Interview Mastery Handbook

## Section 1: Java Fundamentals

### 1.1 Java Introduction & Platform Independence

**1. Definition + Why it exists**
Java is a high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible. Created by James Gosling at Sun Microsystems in 1995, it was built to overcome the portability issues of C and C++. It exists to allow developers to "Write Once, Run Anywhere" (WORA), meaning compiled Java code can run on all platforms that support Java without the need for recompilation.

**2. Internal Working**
Java achieves platform independence through a two-step execution process. First, the source code (`.java`) is compiled by the Java Compiler (`javac`) into an intermediate representation called Bytecode (`.class`). This bytecode is platform-independent. Second, the Java Virtual Machine (JVM), which is platform-specific, interprets and compiles this bytecode into machine code specific to the underlying operating system and hardware at runtime.

**3. Real-world Analogy**
Imagine a speech given at the United Nations. The speaker speaks in English (Source Code). An intermediate translator converts this speech into a universal shorthand language (Bytecode). Then, multiple local interpreters (JVMs) simultaneously read this shorthand and translate it into French, Spanish, Japanese, etc. (Machine Code) for the specific audience (Operating System).

**4. ASCII Diagram**
```text
[ Developer ] -> (Writes) -> HelloWorld.java (Source Code)
                               |
                               v
                         [ Java Compiler (javac) ]
                               |
                               v
                     HelloWorld.class (Bytecode)
                               |
          -------------------------------------------
          |                    |                    |
[ Windows JVM ]         [ Linux JVM ]          [ Mac JVM ]
          |                    |                    |
          v                    v                    v
[ Windows Machine Code ] [ Linux Machine Code ] [ Mac Machine Code ]
```

**5. Syntax + Full Code Examples**
```java
public class HelloWorld {
    // Entry point of the program
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**6. Dry Runs**
- Step 1: Program starts at `main` method.
- Step 2: Executes `System.out.println("Hello, World!");`.
- Step 3: `System` is a built-in class, `out` is a static PrintStream instance, `println` prints the string and adds a newline.
- Step 4: Program terminates successfully.

**7. Common Mistakes**
- Forgetting that Java is case-sensitive (`Main` vs `main`).
- Not matching the file name with the public class name.
- Misunderstanding that JVM is platform-independent (JVM is platform-dependent; bytecode is independent).

**8. Best Practices**
- Always name the file exactly as the public class.
- Keep the `main` method clean; delegate logic to other methods/classes.

**9. Interview Explanation**
"Java is a platform-independent language because it compiles down to bytecode rather than machine code. This bytecode acts as a universal intermediate language. The JVM, which is installed on the host operating system, takes this bytecode and executes it. Therefore, as long as a machine has a JVM, it can run any Java program."

**10. Tricky Interview Questions**
*Q: Is Java 100% Object-Oriented?*
A: No, Java is not 100% object-oriented because it supports primitive data types (like `int`, `char`, `boolean`) which are not objects. This was done for performance reasons.

*Q: Can we write a program without a main method?*
A: Prior to Java 7, we could use static blocks to execute code without a main method, but from Java 7 onwards, the JVM explicitly looks for the `main` method before initializing the class, throwing an error if it's missing. (Note: Java 21 introduced unnamed classes which allow simpler main methods).

**11. Follow-up Questions**
- How does the JVM handle garbage collection?
- What are the differences between Java and C++?

**12. Memory Tricks / Mnemonics**
*WORA* - Write Once, Run Anywhere.

**13. Revision Notes**
> [!NOTE]
> - Source -> Compiler -> Bytecode -> JVM -> OS.
> - Bytecode is the secret to platform independence.
> - JVM is platform-specific.


---

### 1.2 Features of Java

**1. Definition + Why it exists**
Java features (buzzwords) were defined by Sun Microsystems to describe the language's core design philosophy. They exist to assure developers that Java is robust, secure, and versatile for enterprise environments. Key features: Simple, Object-Oriented, Portable, Platform-Independent, Secured, Robust, Architecture-Neutral, Interpreted, High Performance, Multithreaded, Distributed, and Dynamic.

**2. Internal Working**
- **Robust**: Strong memory management, lack of pointers (avoids security issues), automatic Garbage Collection, and strict Exception Handling.
- **Secure**: No explicit pointers, programs run inside a virtual machine sandbox, ClassLoader separates local vs network classes.
- **Multithreaded**: Native support via the `Thread` class and `Runnable` interface, sharing memory efficiently.

**3. Real-world Analogy**
Think of Java as a modern, fortified bank. It is **Secure** (vaults, guards, no direct access to money/memory), **Robust** (backup generators, error handling if alarms trip), and **Multithreaded** (multiple tellers serving customers simultaneously).

**4. ASCII Diagram**
```text
+-------------------+--------------------+-------------------+
|      Secure       |       Robust       |   Multithreaded   |
| No Pointers,      | Strong Type Check, | Thread Scheduler, |
| ClassLoader,      | Garbage Collection,| Concurrency API   |
| Security Manager  | Exception Handling |                   |
+-------------------+--------------------+-------------------+
```

**5. Syntax + Full Code Examples**
```java
// Multithreading feature example
public class FeatureDemo extends Thread {
    public void run() {
        System.out.println("Thread is running securely and robustly!");
    }
    
    public static void main(String[] args) {
        FeatureDemo t1 = new FeatureDemo();
        t1.start(); // Invokes run() in a new thread
        
        // Robustness: Exception Handling
        try {
            int data = 50 / 0; // Throws ArithmeticException
        } catch (ArithmeticException e) {
            System.out.println("Handled robustly: " + e);
        }
    }
}
```

**6. Dry Runs**
- `main` starts.
- Thread `t1` is created and started. JVM schedules it.
- Concurrently, `main` thread attempts `50/0`.
- Exception is thrown and caught immediately, proving robustness.

**7. Common Mistakes**
- Assuming Java is completely secure without proper coding practices (e.g., SQL injection is still possible if developers write bad code).
- Creating too many threads, leading to memory exhaustion instead of high performance.

**8. Best Practices**
- Utilize Java's robust exception handling to build fault-tolerant applications.
- Use `ExecutorService` instead of manual `Thread` creation for better multithreading.

**9. Interview Explanation**
"Java's main features revolve around its safety and portability. It's 'Robust' because it forces strict compile-time checking and runtime exception handling, while managing memory automatically. It's 'Secure' because it runs in a JVM sandbox and lacks explicit pointers. It's 'Multithreaded' built-in, making it ideal for scalable enterprise applications."

**10. Tricky Interview Questions**
*Q: How does Java achieve high performance if it is interpreted?*
A: Java uses a Just-In-Time (JIT) compiler inside the JVM. The JIT compiles frequently executed bytecode (hotspots) into native machine code at runtime, bridging the gap between interpretation and compilation.

**11. Follow-up Questions**
- Explain how the ClassLoader contributes to security.

**12. Memory Tricks / Mnemonics**
*SPPOR* - Secure, Portable, Platform-Independent, Object-Oriented, Robust.

**13. Revision Notes**
> [!NOTE]
> No pointers = Security.
> Garbage Collection + Exception Handling = Robustness.
> Threading API = Multithreading.


---

### 1.3 JDK vs JRE vs JVM

**1. Definition + Why it exists**
- **JVM (Java Virtual Machine)**: An abstract machine that executes Java bytecode.
- **JRE (Java Runtime Environment)**: Provides the libraries, JVM, and other components to *run* applications written in Java.
- **JDK (Java Development Kit)**: A full-featured software development kit. It contains JRE + development tools (compiler `javac`, archiver `jar`, documentation generator `javadoc`).

**2. Internal Working**
The JDK compiles source code. If you only want to run a program, you only need the JRE. The JRE contains the JVM, which is the actual engine that translates bytecode to machine-level instructions. The JVM consists of Class Loaders, Memory Areas (Method Area, Heap, Stack, PC Register, Native Method Stack), and an Execution Engine.

**3. Real-world Analogy**
- **JVM**: The oven that actually bakes the cake (executes).
- **JRE**: The kitchen. It has the oven (JVM) and ingredients/utensils (Libraries) needed to bake the cake, but you can't invent a new recipe here.
- **JDK**: The master chef's studio. It has the kitchen (JRE), but also recipe books, pens, testing equipment (tools like `javac`) to invent and test new recipes.

**4. ASCII Diagram**
```text
+-----------------------------------------------------------+
|                           JDK                             |
|  +-----------------------------------------------------+  |
|  |                        JRE                          |  |
|  |  +-----------------------------------------------+  |  |
|  |  |                     JVM                       |  |  |
|  |  |                                               |  |  |
|  |  |  Class Loader -> Memory Area -> Execution     |  |  |
|  |  |                                 Engine        |  |  |
|  |  +-----------------------------------------------+  |  |
|  |                                                     |  |
|  |  + Core Libraries (rt.jar, etc.)                    |  |
|  |  + Other Integration Libraries                      |  |
|  +-----------------------------------------------------+  |
|                                                           |
|  + Development Tools (javac, java, javadoc, jdb)          |
+-----------------------------------------------------------+
```

**5. Syntax + Full Code Examples**
This is conceptual, but the usage is via CLI:
```bash
# JDK Tool: Compiler
javac MyProgram.java

# JRE/JDK Tool: Runner (invokes JVM)
java MyProgram
```

**6. Dry Runs**
Not applicable for code, but for tool flow:
- Write code.
- Run `javac` (Requires JDK).
- Code becomes `.class`.
- Run `java` (Requires JRE/JDK).
- JVM loads class, allocates memory, executes.

**7. Common Mistakes**
- Installing only JRE when trying to compile code.
- Confusing JVM and JRE (JVM is a specification and instance; JRE is the physical installation).

**8. Best Practices**
- Keep your production environments lightweight by only installing the JRE (though modern containerized setups sometimes just bundle the necessary modules via `jlink`).

**9. Interview Explanation**
"JDK is for developers; it includes the compiler and JRE. JRE is for end-users; it includes the JVM and core libraries needed to run a program. JVM is the core engine that actually interprets the bytecode into machine language and manages memory."

**10. Tricky Interview Questions**
*Q: Is JVM platform-independent?*
A: No! The JVM is highly platform-dependent. There are different JVMs for Windows, Mac, and Linux. It is the *bytecode* that is platform-independent.

**11. Follow-up Questions**
- What memory areas exist inside the JVM?
- What is `rt.jar`?

**12. Memory Tricks / Mnemonics**
*JDK = JRE + Tools. JRE = JVM + Libraries. JVM = Execution Engine.*

**13. Revision Notes**
> [!NOTE]
> JDK > JRE > JVM. 
> JVM executes. JRE provides environment. JDK provides tools to build.

---

### 1.4 Bytecode

**1. Definition + Why it exists**
Bytecode is the intermediate, machine-independent code generated by the Java compiler (`javac`) from Java source code. It is stored in `.class` files. It exists to serve as the universal language for the JVM, enabling Java's "Write Once, Run Anywhere" capability.

**2. Internal Working**
Java bytecode consists of an instruction set (opcodes). Each opcode is 1 byte in size (hence "bytecode"). The JVM acts as a stack-based machine, reading these opcodes sequentially, pushing and popping values from the operand stack, and translating them into native OS instructions.

**3. Real-world Analogy**
Imagine a movie script written in English (Source Code). It's translated into Esperanto (Bytecode), a universal language. No one speaks Esperanto natively, but every theater in the world has an Esperanto-to-Local-Language translator (JVM).

**4. ASCII Diagram**
```text
Source Code (Java)
      |
   [javac]
      |
Bytecode (Hexadecimal opcodes: aload_0, getfield, iadd)
      |
    [JVM]
      |
Machine Code (01010100...)
```

**5. Syntax + Full Code Examples**
```java
public class Addition {
    public int add(int a, int b) {
        return a + b;
    }
}
```
*Disassembled Bytecode (using `javap -c Addition.class`):*
```text
  public int add(int, int);
    Code:
       0: iload_1        // Load variable 'a' onto stack
       1: iload_2        // Load variable 'b' onto stack
       2: iadd           // Add the top two integers on the stack
       3: ireturn        // Return the integer result
```

**6. Dry Runs**
- `iload_1`: Pushes integer at local variable index 1 (a) onto operand stack.
- `iload_2`: Pushes integer at index 2 (b) onto stack.
- `iadd`: Pops the two integers, adds them, and pushes the result back.
- `ireturn`: Pops the result and returns it to the caller.

**7. Common Mistakes**
- Thinking bytecode is machine code. It is not; the OS cannot understand it directly.
- Believing bytecode can only be generated by Java. Languages like Kotlin, Scala, and Groovy also compile down to Java bytecode.

**8. Best Practices**
- Understand bytecode basics to optimize code and understand performance bottlenecks. Tools like ASM or ByteBuddy manipulate bytecode directly.

**9. Interview Explanation**
"Bytecode is a highly optimized set of instructions designed to be executed by the JVM. It abstracts away hardware details. When code is compiled, we get `.class` files containing this bytecode. The JVM then reads it and either interprets it or uses JIT compilation to turn it into machine code."

**10. Tricky Interview Questions**
*Q: Why is it called 'bytecode'?*
A: Because each instruction opcode in the Java bytecode instruction set is exactly one byte (8 bits) long. 

**11. Follow-up Questions**
- Can bytecode be decompiled back to Java? (Yes, easily, using tools like CFR or JD-GUI).
- How do you protect bytecode from decompilation? (Obfuscation).

**12. Memory Tricks / Mnemonics**
Bytecode is the JVM's native language.

**13. Revision Notes**
> [!NOTE]
> Bytecode = Intermediate, platform-independent, stored in `.class`, executed by JVM.

---

### 1.5 Java Program Execution Flow

**1. Definition + Why it exists**
The execution flow describes the journey of a Java program from raw source text to executing hardware instructions. It exists to formalize the stages of parsing, compiling, loading, linking, initializing, and executing, ensuring security and dynamic flexibility.

**2. Internal Working**
1. **Compilation**: `javac` compiles `.java` to `.class` (bytecode).
2. **Class Loading**: JVM's ClassLoader subsystem loads the `.class` file into memory.
3. **Linking**: Verifies bytecode (Security), Prepares memory for static fields, and Resolves symbolic references.
4. **Initialization**: Executes static blocks and assigns initial values to static variables.
5. **Execution**: The Execution Engine (Interpreter + JIT) executes the bytecode.

**3. Real-world Analogy**
Running a restaurant:
1. **Compile**: Chef writes down the recipe (Source -> Bytecode).
2. **Load**: Manager brings the recipe into the kitchen (ClassLoader).
3. **Link**: Health inspector checks the recipe, ingredients are prepared (Verification/Preparation).
4. **Initialize**: Ovens are pre-heated (Static Initialization).
5. **Execute**: Cooks follow the recipe to make the food (Execution Engine).

**4. ASCII Diagram**
```text
Source Code (.java) -> [ javac ] -> Bytecode (.class)
                                         |
+-----------------------------------------------------------+
|                            JVM                            |
|  [ ClassLoader Subsystem ]                                |
|    |-> Loading -> Linking (Verify, Prepare, Resolve)      |
|    |-> Initialization                                     |
|                                                           |
|  [ Runtime Data Areas (Method Area, Heap, Stack...) ]     |
|                                                           |
|  [ Execution Engine ]                                     |
|    |-> Interpreter                                        |
|    |-> JIT Compiler                                       |
|    |-> Garbage Collector                                  |
+-----------------------------------------------------------+
```

**5. Syntax + Full Code Examples**
```java
public class ExecutionFlow {
    static {
        System.out.println("1. Static block executed during Initialization.");
    }
    
    public static void main(String[] args) {
        System.out.println("2. Main method executed by Execution Engine.");
    }
}
```

**6. Dry Runs**
- Command: `java ExecutionFlow`
- JVM starts, ClassLoader loads `ExecutionFlow.class`.
- Linking happens (no static vars to allocate, but verifies).
- Initialization happens: the static block runs first. Output: `1. Static block...`
- Execution Engine finds `main` and invokes it. Output: `2. Main method...`

**7. Common Mistakes**
- Assuming the `main` method runs before static blocks. (Static blocks run during class initialization, *before* main).
- Forgetting the verification step, which prevents malformed bytecode from crashing the JVM.

**8. Best Practices**
- Keep static blocks minimal; heavy operations can slow down class loading and program startup.

**9. Interview Explanation**
"Execution involves compiling source to bytecode, then at runtime, the ClassLoader loads it into the JVM. The linking phase verifies the bytecode for security. Then, static variables and blocks are initialized. Finally, the Execution Engine interprets the code or JIT-compiles it to machine code for execution."

**10. Tricky Interview Questions**
*Q: What happens if the bytecode verification fails?*
A: The JVM throws a `java.lang.VerifyError` and halts the execution, ensuring that tampered or corrupted `.class` files cannot execute malicious operations.

**11. Follow-up Questions**
- What are the three steps in the Linking phase? (Verify, Prepare, Resolve).

**12. Memory Tricks / Mnemonics**
*C L L I E* : Compile, Load, Link, Initialize, Execute.

**13. Revision Notes**
> [!NOTE]
> Static blocks execute during the Initialization phase of Class Loading, strictly before main() is called.

---

### 1.6 Compiler vs Interpreter

**1. Definition + Why it exists**
Compilers and Interpreters are translators that convert high-level code into machine code. 
- A **Compiler** translates the entire code at once before execution. 
- An **Interpreter** translates code line-by-line during execution.
Java uses *both* to balance platform independence and execution speed.

**2. Internal Working**
- `javac` (Compiler): Takes `.java` and generates `.class` (bytecode). It checks syntax and type safety.
- JVM Interpreter: Reads bytecode one instruction at a time and executes it. This allows platform independence but is slower.
- JIT (Just-In-Time Compiler): Runs inside the JVM alongside the interpreter. It compiles frequently used bytecode directly to machine code to speed up execution.

**3. Real-world Analogy**
- **Compiler**: Translating an entire book from English to French and publishing the French book. Fast to read, but you have to wait for the whole translation to finish first.
- **Interpreter**: A live translator at a conference. They translate sentence by sentence as you speak. Instant start, but overall slower to consume.
- **Java**: Translates book to a shorthand code (Compiler). At the destination, someone reads the shorthand aloud, translating line-by-line (Interpreter), but memorizes the repeated choruses and just speaks them natively (JIT).

**4. ASCII Diagram**
```text
C/C++ Approach (Pure Compiler):
Source -> [Compiler] -> OS-Specific Machine Code -> Run

Python/Ruby Approach (Pure Interpreter):
Source -> [Interpreter (Line by Line)] -> Run

Java Approach (Hybrid):
Source -> [Compiler] -> Bytecode -> [Interpreter + JIT] -> Run
```

**5. Syntax + Full Code Examples**
Not applicable for code, but conceptually understood via JVM flags:
```bash
# Run entirely interpreted (disables JIT - very slow)
java -Xint MyProgram

# Run with compiler only (forces JIT compilation for everything)
java -Xcomp MyProgram
```

**6. Time & Space Complexity**
- Compiler: High upfront time, low execution time. High disk space (stored binary).
- Interpreter: Zero upfront time, high execution time. Low disk space.

**7. Common Mistakes**
- Stating that Java is an interpreted language. It is a *hybrid* language (compiled to bytecode, then interpreted/JIT compiled).

**8. Best Practices**
- Let the JVM optimize itself. Don't mess with `-Xint` or `-Xcomp` unless profiling specific edge cases.

**9. Interview Explanation**
"Java uses a hybrid approach. It compiles source code to bytecode using `javac`. At runtime, the JVM uses an interpreter to execute the bytecode line-by-line, ensuring platform independence. To overcome the slowness of interpretation, the JVM includes a JIT compiler that compiles 'hot' methods directly into native machine code at runtime."

**10. Tricky Interview Questions**
*Q: Why doesn't Java just compile directly to machine code like C++?*
A: If it did, it would lose its "Write Once, Run Anywhere" capability. You would have to compile separate versions for Windows, Mac, and Linux.

**11. Follow-up Questions**
- What is JIT? How does it decide what to compile?

**12. Memory Tricks / Mnemonics**
Java is a Hybrid: `javac` prepares it, Interpreter reads it, JIT speeds it up.

**13. Revision Notes**
> [!NOTE]
> Java = Compiled + Interpreted + JIT Compiled.

---

### 1.7 Class Loader Subsystem

**1. Definition + Why it exists**
The ClassLoader is a part of the JRE that dynamically loads Java classes into the JVM memory only when they are required (Dynamic Loading). It exists because Java applications don't load all files into memory at startup; they load them on-demand, saving memory and allowing dynamic extensions.

**2. Internal Working**
Java uses a **Delegation Hierarchy Model**.
1. **Bootstrap ClassLoader**: Loads core Java API classes (`rt.jar`, `java.lang.*`). Written in native code (C/C++).
2. **Extension ClassLoader**: Loads classes from the JDK extension directories (`jre/lib/ext`).
3. **Application/System ClassLoader**: Loads classes from the system classpath (environment variable, `-cp`, your own code).
When a class needs loading, the App loader asks the Ext loader, which asks the Bootstrap loader. If Bootstrap can't find it, it drops back down the chain.

**3. Real-world Analogy**
Finding a specific book in a library system:
- You ask the Local Branch (App Loader).
- Instead of checking shelves, they ask the Regional Hub (Ext Loader).
- Regional Hub asks the National Archives (Bootstrap).
- If National Archive has it, they return it. If not, Regional checks. If not, Local checks. If nobody has it, you get a `ClassNotFoundException`.

**4. ASCII Diagram**
```text
          [ Bootstrap ClassLoader ]  (Loads Core APIs)
                     ^
                     | (Delegates to parent)
                     |
          [ Extension ClassLoader ]  (Loads Extensions)
                     ^
                     | (Delegates to parent)
                     |
         [ Application ClassLoader ] (Loads your .class files)
```

**5. Syntax + Full Code Examples**
```java
public class ClassLoaderDemo {
    public static void main(String[] args) {
        // App ClassLoader (Loads our class)
        System.out.println(ClassLoaderDemo.class.getClassLoader()); 
        
        // Bootstrap ClassLoader (Loads String class)
        // Returns null because Bootstrap is written in native code!
        System.out.println(String.class.getClassLoader()); 
    }
}
```

**6. Dry Runs**
- `ClassLoaderDemo.class.getClassLoader()` runs. It was loaded from our classpath, so it prints `sun.misc.Launcher$AppClassLoader@...`
- `String.class.getClassLoader()` runs. String is a core class loaded by Bootstrap. Since Bootstrap isn't a Java object, it prints `null`.

**7. Common Mistakes**
- Thinking `ClassNotFoundException` and `NoClassDefFoundError` are the same. (The former is when `Class.forName()` fails to find a class at runtime; the latter is when a class was present during compilation but missing at runtime).
- Assuming `null` classloader means an error (it just means Bootstrap loader).

**8. Best Practices**
- Avoid writing custom class loaders unless you are building complex frameworks (like Tomcat or OSGi), as violating the delegation model causes severe security/stability issues.

**9. Interview Explanation**
"The ClassLoader subsystem loads `.class` files into JVM memory. It follows the delegation hierarchy: Application delegates to Extension, which delegates to Bootstrap. The highest parent tries to load it first. This ensures core Java classes are loaded securely and cannot be hijacked by user-defined classes."

**10. Tricky Interview Questions**
*Q: Can we write our own `java.lang.String` class?*
A: You can write it and compile it, but the JVM will never use it. Because of the delegation model, the request to load `String` goes to the Bootstrap loader, which will load the actual, secure `java.lang.String` from `rt.jar`. Your custom class will be ignored, protecting the system.

**11. Follow-up Questions**
- What are custom class loaders used for? (e.g., loading classes over a network, encrypted classes).

**12. Memory Tricks / Mnemonics**
*BEA* -> Bootstrap, Extension, Application (Top to bottom).

**13. Revision Notes**
> [!NOTE]
> Delegation goes UP, searching goes DOWN. If all fail: `ClassNotFoundException`.

---

### 1.8 JIT (Just-In-Time) Compiler

**1. Definition + Why it exists**
The JIT compiler is a component of the Execution Engine inside the JVM. It improves the performance of Java applications by compiling bytecodes to native machine code at runtime. It exists to solve the performance issue of pure line-by-line interpretation.

**2. Internal Working**
The JVM interpreter tracks how often each method or block of code is executed. 
- Code executed frequently is identified as a **"Hot Spot"**.
- The JIT compiler takes these hot spots and compiles the bytecode into highly optimized native machine code.
- The next time the code runs, the JVM directly executes the machine code, vastly improving speed.
- JIT has multiple levels (C1 compiler for fast, low-optimization; C2 compiler for slower, high-level optimization).

**3. Real-world Analogy**
Imagine taking a taxi route every day.
- **Interpreter**: The driver asks you for directions at every single intersection, every single day.
- **JIT**: After 5 days, the driver realizes this is a "hot spot" route. They memorize the best, fastest path. The next day, they drive it perfectly without asking, getting you there instantly.

**4. ASCII Diagram**
```text
Bytecode Executed -> [ JVM Interpreter ] -> Native Code
                          |
                      (Count Invocations)
                          |
                    Threshold Reached?
                     /          \
                   YES           NO -> Continue Interpreting
                   /
          [ JIT Compiler ]
                 |
      Optimized Machine Code (Cached)
```

**5. Syntax + Full Code Examples**
No direct syntax, but you can see JIT in action by running a loop and seeing execution time drop.
```java
public class JITDemo {
    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        for (int i = 0; i < 100000; i++) {
            mathOperation(); // Becomes a hot spot
        }
        System.out.println("Time: " + (System.currentTimeMillis() - start) + "ms");
    }
    
    public static void mathOperation() {
        Math.sin(1.0);
    }
}
```

**6. Time & Space Complexity**
- Time: Fast execution, but JIT compiling itself takes CPU time.
- Space: Compiled native code uses memory (Code Cache).

**7. Common Mistakes**
- Believing JIT compiles the *entire* program at startup. (It only compiles *hot spots* to save memory and startup time).

**8. Best Practices**
- Write small, modular methods. JIT compilers optimize small methods much better than massive, monolithic blocks of code (method inlining).

**9. Interview Explanation**
"JIT runs inside the JVM to boost performance. While the interpreter reads code line-by-line, it monitors method invocation counts. When a method hits a threshold, it's flagged as a hot spot. The JIT compiles this method into native machine code and caches it, so subsequent calls execute at raw hardware speed."

**10. Tricky Interview Questions**
*Q: What is Method Inlining?*
A: It's an optimization by the JIT compiler where the body of a called method is copied directly into the caller's body, eliminating the overhead of the method call itself.

**11. Follow-up Questions**
- What is the JVM Code Cache?
- What is Ahead-Of-Time (AOT) compilation?

**12. Memory Tricks / Mnemonics**
JIT spots Hot Spots.

**13. Revision Notes**
> [!NOTE]
> JIT only compiles frequently used code. It stores the result in the Code Cache.


---
---

## Section 2: Object-Oriented Programming (OOP)

### 2.1 Class and Object

**1. Definition + Why it exists**
- **Class**: A blueprint or template that defines the properties (variables) and behaviors (methods) of a certain entity. It is a logical entity.
- **Object**: A physical/real-world instance of a class. It occupies memory.
They exist to allow programmers to model real-world entities in code, making software easier to design, maintain, and scale.

**2. Internal Working**
When a class is loaded, its structural information is stored in the **Method Area** of the JVM. When you use the `new` keyword, JVM allocates memory for the object in the **Heap**, and returns a reference to that memory, which is stored in the **Stack** (if it's a local variable).

**3. Real-world Analogy**
- **Class**: The architectural blueprint of a house. You cannot live in a blueprint.
- **Object**: The actual house built from the blueprint. You can build multiple houses (objects) from the same blueprint (class).

**4. ASCII Diagram**
```text
      [ Stack ]                  [ Heap ]
  Car myCarRef;   ------>  { Object: Car
                             color: "Red",
                             speed: 100 }
```

**5. Syntax + Full Code Examples**
```java
// 1. Define the Class
class Car {
    // Properties / Fields
    String color;
    int speed;

    // Behavior / Method
    void drive() {
        System.out.println("Driving a " + color + " car at " + speed + " mph.");
    }
}

public class Main {
    public static void main(String[] args) {
        // 2. Create the Object
        Car myCar = new Car(); 
        
        // 3. Access fields and methods
        myCar.color = "Red";
        myCar.speed = 60;
        myCar.drive();
    }
}
```

**6. Dry Runs**
- `Car myCar`: Creates a reference variable in the Stack.
- `new Car()`: Allocates memory in the Heap for a Car object, initializing fields to default values (`null`, `0`).
- `=`: Assigns the memory address of the Heap object to `myCar`.
- `myCar.color = "Red"`: Updates the heap object.
- `myCar.drive()`: Invokes the method based on the object's state.

**7. Common Mistakes**
- Using an object reference without initializing it with `new`, leading to `NullPointerException`.
- Confusing the reference variable with the object itself.

**8. Best Practices**
- Keep classes highly cohesive (one class = one specific job / Single Responsibility Principle).
- Use proper naming conventions: PascalCase for Classes, camelCase for objects/references.

**9. Interview Explanation**
"A class is a logical blueprint containing state and behavior. An object is an instance of that blueprint created in the Heap memory using the `new` keyword. A reference variable points to that object's memory location."

**10. Tricky Interview Questions**
*Q: Can we create an object without the `new` keyword?*
A: Yes! Using `Class.forName().newInstance()`, using `clone()`, using Object Deserialization, or using String literals (for Strings).

**11. Follow-up Questions**
- What happens to an object when its reference is set to null? (It becomes eligible for Garbage Collection).

**12. Memory Tricks / Mnemonics**
Class = Blueprint. Object = Building.

**13. Revision Notes**
> [!NOTE]
> Objects live in Heap memory. References live in Stack memory.


---

### 2.2 Constructor

**1. Definition + Why it exists**
A constructor is a special method block that is invoked automatically when an object is instantiated. It has the *same name* as the class and *no return type*. It exists to initialize the state (variables) of an object at the time of creation.

**2. Internal Working**
When `new MyClass()` is called, the JVM allocates memory, initializes variables to default values, and then invokes the constructor. If no constructor is defined, the Java Compiler automatically injects a **Default Constructor** (no-argument constructor).

**3. Real-world Analogy**
When you buy a brand new smartphone (Object Creation), the factory settings are automatically applied, the OS is installed, and the battery is at 50% (Constructor Initialization). The phone is ready to use the moment it turns on.

**4. ASCII Diagram**
```text
new Employee(101, "John") 
        |
        v
[ Allocate Heap Mem ] -> [ Defaults: id=0, name=null ] -> [ Run Constructor ] -> [ id=101, name="John" ]
```

**5. Syntax + Full Code Examples**
```java
class Employee {
    int id;
    String name;

    // 1. No-Argument Constructor
    Employee() {
        System.out.println("No-arg constructor called");
    }

    // 2. Parameterized Constructor
    Employee(int id, String name) {
        this.id = id;
        this.name = name;
        System.out.println("Parameterized constructor called");
    }
}

public class Main {
    public static void main(String[] args) {
        Employee e1 = new Employee(); // Calls no-arg
        Employee e2 = new Employee(1, "Alice"); // Calls parameterized
    }
}
```

**6. Dry Runs**
- `new Employee()` invokes `Employee()`. Output: "No-arg...". Object fields remain `0` and `null`.
- `new Employee(1, "Alice")` invokes the parameterized constructor. `id` becomes 1, `name` becomes "Alice". Output: "Parameterized...".

**7. Common Mistakes**
- Putting a return type like `void Employee()`. It becomes a normal method, NOT a constructor, and the compiler won't warn you!
- Assuming the default constructor is still provided by the compiler if you write a parameterized constructor. (It is NOT).

**8. Best Practices**
- Always define a no-arg constructor if you define a parameterized one, especially if using frameworks like Spring or Hibernate, which require no-arg constructors for reflection.

**9. Interview Explanation**
"Constructors initialize objects. They share the class name and have no return type. There are three types conceptually: Default (provided by compiler), No-Arg (written by developer), and Parameterized. If you write any constructor, the compiler stops providing the default one."

**10. Tricky Interview Questions**
*Q: Can constructors be private?*
A: Yes. Private constructors prevent instantiation from outside the class. This is the core mechanic used in the Singleton Design Pattern.

**11. Follow-up Questions**
- Can a constructor be final, static, or abstract? (No, compilation error).

**12. Memory Tricks / Mnemonics**
Constructors *Construct* the initial state.

**13. Revision Notes**
> [!NOTE]
> No return type. Same name as class. Called exactly once per object creation.


---

### 2.3 Constructor Chaining

**1. Definition + Why it exists**
Constructor chaining is the process of calling one constructor from another constructor within the same class (using `this()`) or from the parent class (using `super()`). It exists to avoid duplicate initialization code and maintain clean, modular constructor logic.

**2. Internal Working**
When a constructor calls `this(...)` or `super(...)`, that call MUST be the absolute first statement in the constructor. The JVM stacks the constructor calls, resolving the top-most constructor first, then flowing back down.

**3. Real-world Analogy**
Ordering a custom pizza. 
- You want a "Deluxe Pizza".
- Deluxe Pizza constructor says: "First, call the 'Cheese Pizza' constructor."
- Cheese Pizza constructor says: "First, call the 'Basic Crust' constructor."
- Crust is made -> Cheese is added -> Deluxe toppings added.

**4. ASCII Diagram**
```text
new Demo(10, 20) -> calls this(10) -> calls this() 
                                           |
                                      Executes this()
                                           |
                                   Executes this(10)
                                           |
                                 Executes this(10, 20)
```

**5. Syntax + Full Code Examples**
```java
class Person {
    String name;
    int age;

    // Constructor 1
    Person() {
        this("Unknown"); // Calls Constructor 2
        System.out.println("No-arg constructor");
    }

    // Constructor 2
    Person(String name) {
        this(name, 18); // Calls Constructor 3
        System.out.println("One-arg constructor");
    }

    // Constructor 3 (Main Initialization logic)
    Person(String name, int age) {
        this.name = name;
        this.age = age;
        System.out.println("Two-arg constructor");
    }
}

public class Main {
    public static void main(String[] args) {
        Person p = new Person(); 
    }
}
```

**6. Dry Runs**
- `new Person()` executes.
- `Person()` calls `this("Unknown")`.
- `Person(String)` calls `this("Unknown", 18)`.
- `Person(String, int)` sets `name="Unknown"`, `age=18`, prints "Two-arg constructor".
- Control returns to `Person(String)`, prints "One-arg constructor".
- Control returns to `Person()`, prints "No-arg constructor".

**7. Common Mistakes**
- Putting `this()` on the second line of the constructor. (Compilation error).
- Creating recursive constructor chains (e.g., A calls B, B calls A). This causes a compile-time error: "recursive constructor invocation".

**8. Best Practices**
- Channel all constructors to a single "Master Constructor" that does all the heavy lifting and validation.

**9. Interview Explanation**
"Constructor chaining is calling a constructor from another using `this()` or `super()`. It promotes code reuse. The strict rule is that `this()` or `super()` must be the very first statement. They cannot both be used in the same constructor block."

**10. Tricky Interview Questions**
*Q: Can we use both `this()` and `super()` in the same constructor?*
A: No. Both must be the first statement in the constructor. You cannot have two first statements.

**11. Follow-up Questions**
- What happens if you don't write `super()`? (Compiler injects a no-arg `super()` automatically).

**12. Memory Tricks / Mnemonics**
Chain from smallest to biggest: `this()` -> `this(x)` -> `this(x,y)`.

**13. Revision Notes**
> [!NOTE]
> `this()` and `super()` MUST be the first statement. Cannot use both together.


---

### 2.4 this and super keywords

**1. Definition + Why it exists**
- `this`: A reference variable that refers to the **current object** of the class.
- `super`: A reference variable that refers to the **immediate parent class object**.
They exist to resolve namespace collisions (shadowing) between instance variables/methods and local variables/parameters, and to allow inheritance to function properly.

**2. Internal Working**
Both are implicitly passed by the JVM to non-static methods. 
- `this.x` looks in the current heap object.
- `super.x` bypasses the current class's scope and looks specifically at the parent class's definition in the heap object.

**3. Real-world Analogy**
- `this`: When I say "my house", I mean the one I am currently living in.
- `super`: When I say "my father's house", I am specifically referring to the properties of my parent.

**4. ASCII Diagram**
```text
Parent Class { int x = 10; }
       ^
       |
Child Class { int x = 20; 
    void print() {
        int x = 30;
        print(x);       // 30 (Local)
        print(this.x);  // 20 (Current Object)
        print(super.x); // 10 (Parent Object)
    }
}
```

**5. Syntax + Full Code Examples**
```java
class Animal {
    String sound = "Generic Animal Sound";
    
    void makeSound() {
        System.out.println("Animal makes sound");
    }
}

class Dog extends Animal {
    String sound = "Bark";
    
    void display() {
        String sound = "Local Sound";
        
        System.out.println(sound);       // Local Sound
        System.out.println(this.sound);  // Bark
        System.out.println(super.sound); // Generic Animal Sound
        
        this.makeSound();  // Calls Dog's (if overridden) or Animal's
        super.makeSound(); // Strictly calls Animal's
    }
}
```

**6. Dry Runs**
- `Dog d = new Dog(); d.display();`
- `sound` refers to the local variable -> prints "Local Sound".
- `this.sound` points to instance variable of Dog -> prints "Bark".
- `super.sound` accesses parent variable -> prints "Generic Animal Sound".

**7. Common Mistakes**
- Using `this` or `super` inside a `static` method. Static methods belong to the class, not an object, so there is no "current object" to refer to. (Compilation Error).

**8. Best Practices**
- Always use `this.` when assigning constructor parameters to instance variables to avoid ambiguity.

**9. Interview Explanation**
"`this` points to the current instance, used for accessing shadowed instance variables, invoking other constructors via `this()`, or returning the current instance. `super` points to the parent instance, used to access hidden parent variables, overridden parent methods, or parent constructors via `super()`."

**10. Tricky Interview Questions**
*Q: Can we return `this` from a method?*
A: Yes! This is heavily used in the Builder Design Pattern to allow method chaining (e.g., `return this;`).

**11. Follow-up Questions**
- Does `super()` create a parent object in the heap? (No, only one object is created, but it contains parent characteristics).

**12. Memory Tricks / Mnemonics**
`this` = me. `super` = dad.

**13. Revision Notes**
> [!NOTE]
> Neither can be used in static contexts.


---

### 2.5 Encapsulation

**1. Definition + Why it exists**
Encapsulation is the wrapping of data (variables) and code acting on the data (methods) together as a single unit. It involves **data hiding** by making variables `private` and providing access via `public` getter and setter methods. It exists to protect an object's internal state from unwanted or direct modification.

**2. Internal Working**
By declaring variables as `private`, the compiler prevents any external class from accessing the variable's memory address directly. The only way to read/write is to invoke a method stack frame (the getter/setter), inside which the developer can place validation logic.

**3. Real-world Analogy**
A capsule of medicine. The chemicals (data) are hidden inside the capsule shell. You don't interact with the chemicals directly; you consume the capsule (methods).
Alternatively, a Bank ATM. You cannot directly reach into the cash box (variables). You must use the keypad and screen (getters/setters), which validate your PIN before giving cash.

**4. ASCII Diagram**
```text
+---------------------------------------+
|  Class: BankAccount                   |
|                                       |
|  [ Private Data: balance ]  <----     |
|                                 |     |
|  [ Public Methods:        ]     |     |
|    deposit()    ---------/------/     |
|    withdraw()   --------/             |
+---------------------------------------+
      ^
      | (External access MUST go through methods)
[ Main Program ]
```

**5. Syntax + Full Code Examples**
```java
class BankAccount {
    // Hidden data
    private double balance;

    // Public setter with validation
    public void setBalance(double amount) {
        if (amount >= 0) {
            this.balance = amount;
        } else {
            System.out.println("Invalid amount!");
        }
    }

    // Public getter
    public double getBalance() {
        return this.balance;
    }
}

public class Main {
    public static void main(String[] args) {
        BankAccount acc = new BankAccount();
        // acc.balance = -100; // ERROR: balance has private access
        
        acc.setBalance(500); // Valid
        acc.setBalance(-100); // Intercepted by validation
        System.out.println(acc.getBalance()); // 500.0
    }
}
```

**6. Dry Runs**
- `acc.setBalance(500)` -> `500 >= 0` is true -> `balance = 500`.
- `acc.setBalance(-100)` -> `-100 >= 0` is false -> prints "Invalid amount". State remains protected.

**7. Common Mistakes**
- Creating getters and setters but leaving the variables `public`. This defeats the entire purpose of encapsulation.
- Blindly generating getters/setters for every variable. If a variable shouldn't change after creation, omit the setter!

**8. Best Practices**
- By default, make all instance variables `private`.
- Favor immutability (set values in constructor, only provide getters).

**9. Interview Explanation**
"Encapsulation is data hiding. We make variables private and expose public getters/setters. This gives us control over the data. We can add validation in setters, or make a class read-only by omitting setters. It protects the integrity of the object's state."

**10. Tricky Interview Questions**
*Q: What is the difference between Encapsulation and Abstraction?*
A: Encapsulation is about **hiding the state** (data protection). Abstraction is about **hiding the implementation** (reducing complexity). Encapsulation is achieved via access modifiers; Abstraction via interfaces and abstract classes.

**11. Follow-up Questions**
- What are tightly encapsulated classes? (Every single variable is private).

**12. Memory Tricks / Mnemonics**
Encapsulation = Private Data + Public Methods.

**13. Revision Notes**
> [!NOTE]
> Used to achieve data security and create read-only/write-only classes.


---

### 2.6 Abstraction

**1. Definition + Why it exists**
Abstraction is the process of hiding internal implementation details and showing only functionality to the user. It exists to reduce complexity and allow programmers to focus on *what* an object does rather than *how* it does it. In Java, it is achieved using Abstract Classes (0-100% abstraction) and Interfaces (100% abstraction).

**2. Internal Working**
- **Abstract Class**: Marked with `abstract` keyword. Cannot be instantiated using `new`. Can have both abstract methods (no body) and concrete methods.
- **Interface**: A contract. Methods are implicitly `public abstract` (prior to Java 8). Classes `implements` interfaces and must provide the method bodies.

**3. Real-world Analogy**
Driving a car. You press the accelerator pedal to increase speed. You know *what* the pedal does (Abstraction). You don't need to know the internal engine combustion mechanics (Implementation details).

**4. Abstract Class vs Interface Comparison Table**

| Feature | Abstract Class | Interface |
| :--- | :--- | :--- |
| **Methods** | Can have abstract and concrete methods. | Abstract methods (Java 7), Default/Static (Java 8), Private (Java 9). |
| **Variables** | Can have final, non-final, static, non-static. | Implicitly `public static final`. |
| **Multiple Inheritance**| Doesn't support. | Supported (class can implement multiple). |
| **Constructors** | Can have constructors. | Cannot have constructors. |
| **Keyword** | `abstract` | `interface` |

**5. Syntax + Full Code Examples**
```java
// Interface
interface Vehicle {
    void start(); // implicit public abstract
}

// Abstract Class
abstract class Engine {
    // Concrete method
    void displayEngineType() {
        System.out.println("Combustion Engine");
    }
    // Abstract method
    abstract void fuelType();
}

// Concrete Class
class Car extends Engine implements Vehicle {
    @Override
    public void start() {
        System.out.println("Car starts with key");
    }

    @Override
    void fuelType() {
        System.out.println("Uses Petrol");
    }
}

public class Main {
    public static void main(String[] args) {
        Car myCar = new Car();
        myCar.start();
        myCar.displayEngineType();
        myCar.fuelType();
        
        // Vehicle v = new Vehicle(); // ERROR: Cannot instantiate interface
    }
}
```

**6. Dry Runs**
- `Car` inherits `displayEngineType()` from `Engine`.
- `Car` must override `start()` and `fuelType()`.
- Method calls execute the concrete implementations provided in `Car`.

**7. Common Mistakes**
- Trying to instantiate an abstract class or interface directly.
- Forgetting that interface variables are `static final` (constants) by default. You cannot reassign them.

**8. Best Practices**
- Use interfaces to define contracts and capabilities (e.g., `Runnable`, `Serializable`).
- Use abstract classes for sharing core code and state among closely related classes (e.g., `AbstractList`).

**9. Interview Explanation**
"Abstraction hides complexity. We use Interfaces for defining contracts that multiple unrelated classes can implement, allowing multiple inheritance of type. We use Abstract classes when we have closely related classes that share common state or concrete methods alongside abstract ones."

**10. Tricky Interview Questions**
*Q: Can an abstract class have no abstract methods?*
A: Yes! You can mark a class as `abstract` without any abstract methods. This simply prevents anyone from instantiating the class directly.

**11. Follow-up Questions**
- Why were default methods added to interfaces in Java 8? (To add backward compatibility, allowing new methods in interfaces without breaking existing implementations).

**12. Memory Tricks / Mnemonics**
Interface = What to do. Abstract/Concrete Class = How to do it.

**13. Revision Notes**
> [!NOTE]
> Interface supports Multiple Inheritance. Abstract Class does not. Both cannot be instantiated.


---

### 2.7 Inheritance

**1. Definition + Why it exists**
Inheritance is a mechanism where a new class (child/subclass) acquires all the properties and behaviors of an existing class (parent/superclass). It establishes an **IS-A relationship**. It exists to promote code reusability and method overriding (runtime polymorphism).

**2. Internal Working**
Java uses the `extends` keyword. When a child object is created, the JVM allocates memory for both the parent's variables and the child's variables within the single child object. 
*Types:* Single, Multilevel, Hierarchical. (Multiple and Hybrid inheritance via classes are NOT supported to avoid the Diamond Problem).

**3. Real-world Analogy**
A `Dog` IS-A `Animal`. 
The `Animal` class has methods like `eat()` and `sleep()`. The `Dog` inherits these, so you don't have to rewrite `eat()` for the dog. `Dog` just adds its own specific method, `bark()`.

**4. ASCII Diagram (Diamond Problem)**
```text
      [ Class A (show()) ]
        /            \
  [ Class B ]     [ Class C ]  (Both inherit show())
        \            /
     [ Class D (extends B, C) ]
     
If D calls show(), which one should it run? B's or C's? 
Ambiguity! Thus, Java prevents Multiple Class Inheritance.
```

**5. Syntax + Full Code Examples**
```java
// Parent
class Animal {
    void eat() { System.out.println("Eating..."); }
}

// Child (Single Inheritance)
class Dog extends Animal {
    void bark() { System.out.println("Barking..."); }
}

// Grandchild (Multilevel Inheritance)
class Puppy extends Dog {
    void weep() { System.out.println("Weeping..."); }
}

public class Main {
    public static void main(String[] args) {
        Puppy p = new Puppy();
        p.eat();  // Inherited from Animal
        p.bark(); // Inherited from Dog
        p.weep(); // Own method
    }
}
```

**6. Dry Runs**
- `Puppy p = new Puppy();`
- `p.eat()`: JVM looks in `Puppy`, not found -> looks in `Dog`, not found -> looks in `Animal`, found and executed.

**7. Common Mistakes**
- Using inheritance for code reuse without an IS-A relationship (this violates OOP). If A just needs B's code, use Composition (HAS-A) instead.
- Assuming private members of a parent class are inherited. (They are not directly accessible by the child, though they exist in memory).

**8. Best Practices**
- Favor Composition over Inheritance. Only use inheritance when a strict "IS-A" relation exists to prevent fragile base class issues.

**9. Interview Explanation**
"Inheritance creates parent-child relationships using `extends`. It allows code reuse. Java doesn't support multiple inheritance with classes due to the Diamond Problem, but achieves it via interfaces. Inheritance is the prerequisite for runtime polymorphism."

**10. Tricky Interview Questions**
*Q: What is the difference between IS-A and HAS-A?*
A: IS-A is inheritance (e.g., Car `extends` Vehicle). HAS-A is composition/aggregation, meaning one class has a reference to another (e.g., Car `has-a` Engine as an instance variable).

**11. Follow-up Questions**
- Every class in Java extends which class? (`java.lang.Object`).

**12. Memory Tricks / Mnemonics**
Inheritance = IS-A. Composition = HAS-A.

**13. Revision Notes**
> [!NOTE]
> No multiple class inheritance in Java. Private members are not inherited.


---

### 2.8 Polymorphism

**1. Definition + Why it exists**
Polymorphism means "many forms". It allows an object to take on many forms, meaning a single action can perform in different ways. It exists to decouple the system, allowing the developer to write generalized code that can handle multiple specific object types dynamically.

**2. Internal Working**
- **Compile-Time Polymorphism (Static Binding)**: Achieved via Method Overloading. The compiler determines which method to call based on the method signature (arguments) during compilation.
- **Runtime Polymorphism (Dynamic Binding)**: Achieved via Method Overriding. A parent reference points to a child object. The JVM determines which overridden method to call at runtime based on the actual object in the heap, not the reference type.

**3. Real-world Analogy**
- **Overloading (Compile-time)**: The word "Draw". If I give you a pen, you "Draw" a picture. If I give you a sword, you "Draw" the sword. The action depends on the parameter provided.
- **Overriding (Runtime)**: The instruction "Speak". If I tell a Dog object to speak, it barks. If I tell a Cat object to speak, it meows. Same instruction, different runtime behaviors based on the animal.

**4. ASCII Diagram**
```text
           [ Shape (draw()) ]
             /            \
[ Circle (draw()) ]   [ Square (draw()) ]

Shape s = new Circle();
s.draw(); // At runtime, JVM looks at heap -> calls Circle's draw()
```

**5. Syntax + Full Code Examples**
```java
class Shape {
    void draw() {
        System.out.println("Drawing a generic shape");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Circle");
    }
}

class Triangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Triangle");
    }
}

public class Main {
    public static void main(String[] args) {
        // Upcasting: Parent reference, Child object
        Shape s1 = new Circle(); 
        Shape s2 = new Triangle();
        
        s1.draw(); // Output: Drawing a Circle
        s2.draw(); // Output: Drawing a Triangle
    }
}
```

**6. Dry Runs**
- `Shape s1 = new Circle()` creates a Circle object in heap.
- `s1.draw()` executes. Compiler checks if `draw()` exists in `Shape`. Yes. 
- At runtime, JVM checks the actual object type of `s1`. It's a `Circle`. It invokes `Circle`'s `draw()`.

**7. Common Mistakes**
- Believing variables are polymorphic. Variables DO NOT override, they hide (Variable Shadowing). Only methods are overridden and participate in runtime polymorphism.

**8. Best Practices**
- Code to an interface/superclass. e.g., use `List<String> list = new ArrayList<>();` instead of `ArrayList<String> list = new ArrayList<>();`. This is polymorphism in action.

**9. Interview Explanation**
"Polymorphism comes in two flavors. Compile-time is method overloading, resolved by the compiler. Runtime is method overriding, resolved by the JVM based on the actual object instance. Runtime polymorphism is the cornerstone of OOP, allowing us to build flexible and extensible systems."

**10. Tricky Interview Questions**
*Q: Can we override static methods?*
A: No! Static methods belong to the class, not the object. If a child class defines a static method with the same name as the parent, it is called **Method Hiding**, not overriding. Runtime polymorphism doesn't apply.

**11. Follow-up Questions**
- What is Dynamic Method Dispatch? (The process by which an overridden method call is resolved at runtime).

**12. Memory Tricks / Mnemonics**
Over**L**oading = Compi**L**e time. Over**R**iding = **R**untime.

**13. Revision Notes**
> [!NOTE]
> Variables and Static Methods CANNOT be overridden.


---

### 2.9 Method Overloading

**1. Definition + Why it exists**
Method Overloading occurs when a class has multiple methods with the *same name* but *different parameters* (type, number, or order). It exists to increase the readability of the program. Instead of `addInts()`, `addDoubles()`, we just use `add()`.

**2. Internal Working**
During compilation, the Java compiler analyzes the method call arguments. It binds the method call to the specific method signature that matches. This is early binding (static binding).

**3. Real-world Analogy**
Your smartphone's Camera button. 
- Tap it once -> Takes a photo.
- Hold it down -> Records a video.
Same button (method name), different input (parameters), different behavior.

**4. ASCII Diagram**
```text
Method Call: print(10) ---> Matches ---> print(int x)
Method Call: print("Hi") -> Matches ---> print(String s)
```

**5. Syntax + Full Code Examples**
```java
class Calculator {
    // 1. Two int parameters
    int add(int a, int b) {
        return a + b;
    }

    // 2. Three int parameters (Different number)
    int add(int a, int b, int c) {
        return a + b + c;
    }

    // 3. Two double parameters (Different type)
    double add(double a, double b) {
        return a + b;
    }
}

public class Main {
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        System.out.println(calc.add(5, 10));         // Calls #1
        System.out.println(calc.add(5, 10, 15));     // Calls #2
        System.out.println(calc.add(5.5, 2.0));      // Calls #3
    }
}
```

**6. Dry Runs**
- `calc.add(5, 10)`: Both args are `int`. Compiler links to `add(int, int)`. Result: 15.
- `calc.add(5.5, 2.0)`: Both args are `double`. Compiler links to `add(double, double)`. Result: 7.5.

**7. Common Mistakes**
- Trying to overload by changing *only* the return type. E.g., `int add(int a)` and `double add(int a)`. This results in a compile-time error because return type isn't part of the method signature.

**8. Best Practices**
- Keep overloaded methods functionally similar. Don't let `add(int, int)` do addition while `add(String, String)` deletes files.

**9. Interview Explanation**
"Method overloading is compile-time polymorphism. We create methods with the same name but different parameter lists. The compiler uses the number, type, and order of arguments to resolve which method to call. Changing only the return type is not allowed."

**10. Tricky Interview Questions**
*Q: What happens if you pass a `null` to overloaded methods `print(Object o)` and `print(String s)`?*
A: The compiler always resolves to the most specific type. Since `String` is a subclass of `Object`, `print(String s)` will be called. If there were `print(String s)` and `print(Integer i)`, passing `null` would cause an ambiguous compile-time error.

**11. Follow-up Questions**
- What is Type Promotion / Widening in overloading? (e.g., passing `int` to a method expecting `long` works automatically if no `int` method exists).

**12. Memory Tricks / Mnemonics**
Overloading: Same Name, Different Parameters.

**13. Revision Notes**
> [!NOTE]
> Return type does not matter for overloading. Most specific matching method wins.


---

### 2.10 Method Overriding

**1. Definition + Why it exists**
Method Overriding occurs when a child class provides a specific implementation for a method that is already defined in its parent class. The method must have the *same name*, *same parameters*, and *same return type* (or a subtype). It exists to provide child-specific behavior and achieve Runtime Polymorphism.

**2. Internal Working**
At runtime, the JVM uses the V-Table (Virtual Method Table). It inspects the actual object created in heap memory. If the object's class has an overridden version of the method, that version is invoked; otherwise, it walks up the inheritance tree.

**3. Real-world Analogy**
- Parent prescribes: "You must go to work." (Method)
- You inherit this rule. But you override it: "I go to work, but I work from home." You're doing the same action, but implementing it differently.

**4. ASCII Diagram**
```text
[ Parent: interestRate() returns 5% ]
               |
[ Child Bank: interestRate() returns 8% ] 
// Overrides the 5% with 8%
```

**5. Syntax + Full Code Examples**
```java
class Bank {
    int getRateOfInterest() {
        return 0;
    }
}

class SBI extends Bank {
    @Override // Annotation ensures compiler checks the signature
    int getRateOfInterest() {
        return 7;
    }
}

class HDFC extends Bank {
    @Override
    int getRateOfInterest() {
        return 9;
    }
}

public class Main {
    public static void main(String[] args) {
        Bank b1 = new SBI();
        Bank b2 = new HDFC();
        
        System.out.println("SBI Rate: " + b1.getRateOfInterest());   // 7
        System.out.println("HDFC Rate: " + b2.getRateOfInterest()); // 9
    }
}
```

**6. Dry Runs**
- `Bank b1 = new SBI()`
- `b1.getRateOfInterest()` -> Compiler confirms `Bank` has this method. At runtime, JVM sees the object is `SBI`. It runs `SBI`'s overridden method. Returns 7.

**7. Common Mistakes**
- Reducing the visibility of the overridden method. (e.g., Parent is `public`, Child makes it `protected` -> Compile Error).
- Not using the `@Override` annotation, leading to accidental method overloading instead of overriding if a typo occurs.

**8. Best Practices**
- ALWAYS use `@Override`. It forces the compiler to check if you are actually overriding a parent method.

**9. Interview Explanation**
"Overriding requires inheritance. The child class rewrites the parent's method with the exact same signature. The access modifier can be the same or wider, but never more restrictive. It enables runtime polymorphism, where the JVM decides which method to run based on the heap object."

**10. Tricky Interview Questions**
*Q: What is a Covariant Return Type?*
A: It means an overridden method can return a subclass of the type returned by the parent method. For example, if Parent returns `Number`, Child's overridden method can return `Integer`.

*Q: Can we override private or final methods?*
A: No. Private methods are invisible to the child. Final methods are explicitly locked from being overridden.

**11. Follow-up Questions**
- Can we override `main` method? (No, it is static).

**12. Memory Tricks / Mnemonics**
Overriding: Same everything, but in a Subclass.

**13. Revision Notes**
> [!NOTE]
> Cannot narrow visibility. Can use covariant return types. @Override is your best friend.


---
---

## Top 50 Interview Questions: Section 1 (Java Fundamentals)

1. **Why is Java Platform Independent?** Because it compiles to bytecode, which the JVM translates to OS-specific machine code.
2. **What is JVM?** An abstract machine that executes bytecode.
3. **What is the difference between JDK, JRE, and JVM?** JDK = tools + JRE; JRE = JVM + libs; JVM = execution engine.
4. **Is Java 100% Object-Oriented?** No, because of primitive data types.
5. **What are pointers and does Java support them?** Memory addresses; Java doesn't support explicit pointers for security.
6. **What is JIT?** Just-In-Time compiler, converts hot bytecode to machine code.
7. **Explain public static void main(String[] args).** public (accessible everywhere), static (called without object), void (returns nothing), main (JVM entry point), args (CLI arguments).
8. **What happens if you remove static from main?** Program compiles, but throws `NoSuchMethodError` at runtime.
9. **What is Bytecode?** Intermediate code generated by `javac`.
10. **Can you execute Java without main method?** Since Java 7, no.
11. **What is ClassLoader?** Subsystem that loads `.class` files dynamically.
12. **Name the types of ClassLoaders.** Bootstrap, Extension, Application.
13. **What is the default value of local variables?** No default value; must be initialized, else compile error.
14. **Difference between `==` and `.equals()`?** `==` compares references, `.equals()` compares content (if overridden).
15. **What are wrapper classes?** Classes that encapsulate primitives (e.g., Integer for int).
16. **Why do we need wrapper classes?** Collections only store objects, not primitives.
17. **What is Autoboxing/Unboxing?** Auto conversion between primitive and its wrapper class.
18. **Difference between Heap and Stack memory?** Heap stores objects; Stack stores local variables and method frames.
19. **What is Garbage Collection?** Automatic destruction of unreferenced objects to free heap memory.
20. **Can we force Garbage Collection?** No, we can only request it via `System.gc()`.
21. **What is a memory leak in Java?** When referenced objects are no longer needed but GC cannot remove them.
22. **Difference between path and classpath?** OS uses path to find executables; JVM uses classpath to find `.class` files.
23. **What is a package?** A namespace that organizes classes and interfaces.
24. **Difference between final, finally, finalize?** final (constant/un-overridable), finally (try-catch block always executed), finalize() (called by GC before destruction).
25. **Is String a primitive or a class?** A class.
26. **Why are Strings immutable in Java?** Security, synchronization, and caching (String Pool).
27. **What is the String Pool?** Special memory in heap that caches string literals.
28. **String vs StringBuffer vs StringBuilder?** String is immutable. StringBuffer is mutable and synchronized (thread-safe). StringBuilder is mutable but not synchronized (fast).
29. **What is an anonymous block?** Block of code without a name, runs during instance creation.
30. **When do static blocks execute?** During class loading, before `main()`.
31. **Can we overload the main method?** Yes, but JVM only calls the standard `String[]` one.
32. **Can we declare main as private?** Compiles fine, but runtime error because JVM can't access it.
33. **What is `System.out.println()`?** `System` is class, `out` is static PrintStream obj, `println` is method.
34. **Does Java support pass by value or pass by reference?** Java is strictly Pass by Value. (For objects, the reference value is passed).
35. **Difference between break and continue?** `break` exits loop; `continue` skips current iteration.
36. **What is a labeled loop?** Loop with a name, allows breaking/continuing specific outer loops.
37. **What are varargs?** Variable-length arguments (`int... a`), treated as an array.
38. **Can varargs be the first parameter?** No, must be the last.
39. **How many varargs can a method have?** Only one.
40. **Difference between Error and Exception?** Errors are unrecoverable system issues (OutOfMemory); Exceptions are application logic issues.
41. **Difference between print() and println()?** `println()` appends a newline.
42. **What is the size of boolean?** JVM dependent (usually 1 bit, but array of booleans uses 1 byte per element).
43. **Why does char take 2 bytes in Java?** Java uses Unicode to support international characters.
44. **What is Unicode?** Universal character encoding standard.
45. **What happens if a floating-point divides by zero?** Returns `Infinity` or `NaN`, no exception thrown.
46. **What is strictfp?** Keyword ensuring consistent floating-point results across platforms.
47. **What is an inner class?** Class declared inside another class.
48. **Difference between local and instance variables?** Local inside methods; instance inside class.
49. **What is a magic number in Java?** The first 4 bytes of a `.class` file (`0xCAFEBABE`).
50. **How do you compile and run via terminal?** `javac File.java` then `java File`.

---

## Top 50 Interview Questions: Section 2 (OOP)

1. **What are the four pillars of OOP?** Encapsulation, Abstraction, Inheritance, Polymorphism.
2. **What is an Object?** An instance of a class occupying heap memory.
3. **What is a Class?** A blueprint for objects.
4. **How do you create an object?** Using the `new` keyword.
5. **What is Encapsulation?** Hiding data behind private variables and public getters/setters.
6. **What is Abstraction?** Hiding implementation details and showing functionality.
7. **Abstract class vs Interface?** Interface is a contract (100% abstract usually), Abstract class shares code.
8. **Why no multiple class inheritance?** Diamond problem causing method ambiguity.
9. **How to achieve multiple inheritance?** By implementing multiple interfaces.
10. **What is Polymorphism?** One interface, multiple forms (Overloading / Overriding).
11. **Method Overloading?** Same method name, different parameters.
12. **Method Overriding?** Child class redefines parent method with exact signature.
13. **Compile-time vs Runtime polymorphism?** Overloading vs Overriding.
14. **What is a Constructor?** Special block to initialize objects.
15. **Does constructor have a return type?** No.
16. **Can constructor be inherited?** No.
17. **Can we make a constructor final?** No.
18. **What is constructor chaining?** Calling one constructor from another using `this()` or `super()`.
19. **What is the `this` keyword?** Refers to the current object.
20. **What is the `super` keyword?** Refers to the immediate parent object.
21. **Can we use `this` and `super` together?** Not in the same constructor as both must be the first line.
22. **What is variable shadowing?** Local variable has same name as instance variable.
23. **What is method hiding?** Child defines a static method with same name as parent's static method.
24. **Difference between IS-A and HAS-A?** IS-A = Inheritance. HAS-A = Composition.
25. **What is Composition?** Strong HAS-A relationship (House has Rooms; rooms die with house).
26. **What is Aggregation?** Weak HAS-A relationship (Department has Teachers; teachers exist without dept).
27. **Can we override private methods?** No, they are not visible to child.
28. **Can we override static methods?** No, resolved at compile-time.
29. **Can we override final methods?** No, final prevents overriding.
30. **What is Covariant Return Type?** Overriding method returns a subclass of parent's return type.
31. **Can we change access modifier while overriding?** Can only make it wider/more accessible, not restrictive.
32. **What happens if parent method throws Exception?** Child overridden method can throw same, subclass, or no exception. Cannot throw broader checked exceptions.
33. **Can abstract class have constructor?** Yes, called when child is instantiated.
34. **Can we declare abstract method private?** No, it must be overridden, private prevents that.
35. **Difference between `this()` and `super()`?** `this()` calls current class constructor; `super()` calls parent.
36. **What is Dynamic Method Dispatch?** Mechanism by which a call to overridden method is resolved at runtime.
37. **What is upcasting?** Parent reference pointing to Child object.
38. **What is downcasting?** Parent reference explicitly cast back to Child type.
39. **What is `instanceof`?** Operator to check if an object is of a specific type.
40. **What is an interface?** A blueprint of a class containing static constants and abstract methods.
41. **What are default methods in interfaces?** Introduced in Java 8 to allow method bodies in interfaces without breaking implementations.
42. **Can interface have static methods?** Yes (Java 8+).
43. **Can interface have private methods?** Yes (Java 9+).
44. **What is a marker interface?** Empty interface used to signal to JVM (e.g., Serializable, Cloneable).
45. **What is functional interface?** Interface with exactly one abstract method.
46. **How do you restrict a class from being inherited?** Make it `final`.
47. **What is a singleton class?** Class that allows only one instance to be created.
48. **How to make a class singleton?** Private constructor, static instance variable, public static getter.
49. **Can you overload main method?** Yes.
50. **Can we instantiate an abstract class?** No, but we can have an anonymous inner class implementation.

---

## Cheat Sheet: Section 1 & 2

### Java Fundamentals
- **Entry Point:** `public static void main(String[] args)`
- **Compilation:** `javac File.java` -> `File.class` (Bytecode)
- **Execution:** `java File` -> JVM reads bytecode.
- **Memory:** Stack = primitives + references. Heap = Objects.
- **Modifiers:**
  - `public`: Everywhere
  - `protected`: Same package + Subclasses
  - `default`: Same package only
  - `private`: Same class only
- **Keywords:**
  - `static`: Belongs to Class.
  - `final`: Constant (variable), un-overridable (method), un-inheritable (class).

### OOP Core
- **Class / Object:** `ClassName obj = new ClassName();`
- **Constructor:** `public ClassName() { ... }`
- **Encapsulation:** `private` data + `public` get/set.
- **Inheritance:** `class Child extends Parent`
- **Polymorphism:**
  - *Overloading*: Same name, different args.
  - *Overriding*: Same name, same args, child class, `@Override`.
- **Abstraction:**
  - `abstract class`: 0-100% abstract, allows state.
  - `interface`: 100% abstract, pure contract.
- **Pointers:**
  - `this`: Current object.
  - `super`: Parent object.
  - `this()` / `super()`: Constructor calls (Must be line 1).

> **Pro-Tip for Interviews**: Always relate OOP concepts back to the real world (e.g., Animal/Dog, BankAccount) and mention memory areas (Heap vs Stack, Compile-time vs Runtime) to show deep architectural understanding.
