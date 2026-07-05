# Java Interview Mastery Handbook - Sections 12 & 13

---

# Section 12 - Spring Boot Interview Preparation

## 1. Spring Core & IOC Container

**Definition + Why it exists**
Inversion of Control (IoC) is a principle where the framework takes control of object creation and lifecycle, decoupling components. The Spring IoC container creates, wires, and manages "Beans" (objects). 
*BeanFactory* is the basic container (lazy loading). *ApplicationContext* extends BeanFactory (eager loading, i18n, event publishing).
Bean scopes define the lifespan of a bean: `singleton` (one per context), `prototype` (new instance per request), `request`, `session`, `application`.

**Internal Working**
Spring parses configurations (Annotations, XML, Java Config), creates bean definitions, and stores them in a registry. During context startup, singletons are eagerly instantiated using Reflection, properties are injected, and lifecycle callbacks are invoked.

**Real-world Analogy**
Think of an IoC container as a Restaurant Manager. Instead of the chef (your class) worrying about buying ingredients and hiring waiters (instantiating dependencies), the Manager (IoC) provides everything the chef needs so they can just cook.

**ASCII Diagram: Bean Lifecycle**
```text
[Instantiation]
      │
[Populate Properties]
      │
[BeanNameAware] ───────► setBeanName()
      │
[BeanFactoryAware] ────► setBeanFactory()
      │
[ApplicationContextAware]► setApplicationContext()
      │
[BeanPostProcessor] ───► postProcessBeforeInitialization()
      │
[@PostConstruct] / [InitializingBean] ──► afterPropertiesSet()
      │
[BeanPostProcessor] ───► postProcessAfterInitialization()
      │
[READY FOR USE]
      │
[@PreDestroy] / [DisposableBean] ──► destroy()
```

**Syntax + Code Examples**
```java
@Component
@Scope("singleton")
public class PaymentService {
    @PostConstruct
    public void init() { System.out.println("Init"); }
    @PreDestroy
    public void destroy() { System.out.println("Destroy"); }
}
```

**Time & Space Complexity**
*Time*: O(1) to retrieve a singleton bean from the context. O(N) context startup time relative to beans.
*Space*: O(N) where N is the number of singleton beans stored in the container's ConcurrentHashMap.

**Common Mistakes + Best Practices**
- *Mistake*: Injecting a prototype bean into a singleton bean expecting a new prototype instance every time (Lookup method injection is the fix).
- *Best Practice*: Prefer ApplicationContext over BeanFactory. Stick to singleton scope unless absolutely necessary.

**Interview Explanation**
Start by explaining *why* IoC is needed (loose coupling). Explain how ApplicationContext builds upon BeanFactory. Outline the bean lifecycle emphasizing `@PostConstruct` and `@PreDestroy`. 

**Tricky Interview Questions**
- *Q: What happens if a prototype bean is injected into a singleton bean?*
  A: The prototype bean is created only once when the singleton is instantiated. Subsequent calls use the same prototype instance. Use `@Lookup` to fix.
- *Q: Can we change the scope of a bean at runtime?*
  A: No, scopes are bound at context startup. You would need custom scopes and a custom registry.

**Follow-up Questions**
- What is a BeanPostProcessor? (Allows custom modification of new bean instances before and after initialization).

**Memory Tricks / Mnemonics**
*Lifecycle*: **I P**roposed **B**ecause **A**nnie **P**romised **I**nstant **R**omantic **D**inners.
(Instantiate, Populate, BeanName/Factory, ApplicationContext, PostProcessBefore, Init, Ready, Destroy).

**Revision Notes**
- BeanFactory = Lazy, lightweight.
- ApplicationContext = Eager, heavy, enterprise ready.
- Scopes: singleton (default), prototype, request, session.

**Cheat Sheet Snippets**
```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
MyBean bean = ctx.getBean(MyBean.class);
```

**Practice Problems**
1. Create a singleton bean holding a prototype bean and prove the prototype is not refreshed. Fix it using `@Lookup`.

---

## 2. Dependency Injection

**Definition + Why it exists**
Dependency Injection (DI) is a design pattern used to implement IoC. Instead of an object creating its dependencies via the `new` keyword, dependencies are passed to it (via constructor, setter, or field). This makes code testable, maintainable, and loosely coupled.

**Internal Working**
Spring uses Reflection to inject dependencies. If using `@Autowired`, Spring searches the context by type. If multiple beans exist, `@Qualifier` or `@Primary` resolves the conflict.

**Real-world Analogy**
A surgeon (Class) needs a scalpel (Dependency). Instead of the surgeon forging a scalpel in the OR (using `new`), a nurse (Spring Container) hands the surgeon a sterilized scalpel (Injection).

**Syntax + Code Examples**
```java
@Service
public class OrderService {
    private final PaymentProcessor processor;

    // Constructor Injection (Preferred)
    @Autowired // Optional if only one constructor
    public OrderService(@Qualifier("stripeProcessor") PaymentProcessor processor) {
        this.processor = processor;
    }
}
```

**Common Mistakes + Best Practices**
- *Mistake*: Using Field Injection (`@Autowired` on a private field). It makes testing harder (need reflection) and hides circular dependencies.
- *Best Practice*: Always use Constructor Injection. It ensures dependencies are not null, enforces immutability (`final`), and reveals circular dependencies at startup.

**Interview Explanation**
Highlight the three types of injection. State definitively that Constructor injection is best. Explain that `@Primary` provides a default, while `@Qualifier` allows specific selection when multiple implementations of an interface exist.

**Tricky Interview Questions**
- *Q: How does Spring handle Circular Dependencies?*
  A: For constructor injection, it throws `BeanCurrentlyInCreationException`. For setter/field injection, Spring uses a 3-level cache (early singleton exposure) to resolve it. Fix: redesign, or use `@Lazy`.

**Revision Notes**
- `@Autowired` resolves by Type.
- `@Resource` resolves by Name.
- Use Constructor injection for mandatory dependencies, Setter for optional.

---

## 3. Spring Boot Specifics

**Definition + Why it exists**
Spring Boot is an extension of the Spring framework that eliminates boilerplate configuration required for setting up a Spring application. It provides Auto-configuration, embedded servers, and opinionated starter dependencies.

**Internal Working**
`@SpringBootApplication` comprises three annotations:
1. `@ComponentScan`: Scans for components in the current package and sub-packages.
2. `@SpringBootConfiguration`: Marks it as a configuration class.
3. `@EnableAutoConfiguration`: The magic. It looks into `META-INF/spring.factories` (or `AutoConfiguration.imports` in Boot 2.7+) and loads beans conditionally using `@ConditionalOnClass`, `@ConditionalOnMissingBean`.

**Real-world Analogy**
Spring is like building a custom car from individual parts. Spring Boot is buying a pre-assembled car with sensible defaults where you can swap out the radio or tires if you want.

**Syntax + Code Examples**
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**Common Mistakes + Best Practices**
- *Mistake*: Placing the main class in the root directory (default package). `@ComponentScan` will scan every single class in the classpath, slowing down startup.
- *Best Practice*: Use `application.yml` for hierarchical configuration. Use Actuator but secure its endpoints.

**Interview Explanation**
Walk through the `@SpringBootApplication` breakdown. Explain Auto-configuration by describing how Spring Boot checks the classpath (e.g., "Oh, I see Tomcat on the classpath, let me configure an embedded Tomcat"). 

**Tricky Interview Questions**
- *Q: How do you exclude a specific Auto-configuration class?*
  A: `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`
- *Q: application.properties vs bootstrap.properties?*
  A: bootstrap is loaded first by Spring Cloud Context for externalized configuration (e.g., Config Server) before the main application context loads application.properties.

**Memory Tricks / Mnemonics**
*Auto-configuration magic*: **C C E** (Component scan, Configuration, EnableAutoConfig).

---

## 4. Spring MVC & REST

**Definition + Why it exists**
Spring MVC is a web framework built on the Model-View-Controller pattern. REST in Spring is handled by the same infrastructure but returns data (JSON/XML) instead of views.

**Internal Working**
The `DispatcherServlet` is the Front Controller. It receives all requests, asks the `HandlerMapping` which controller to invoke, calls the controller, and uses a `ViewResolver` (for MVC) or `HttpMessageConverter` (for REST) to return the response.

**ASCII Diagram: DispatcherServlet Flow**
```text
      (1) HTTP Request
Client ─────────────────► DispatcherServlet
                               │  ▲
                     (2) Ask   │  │ (3) Handler Execution Chain
                         HandlerMapping
                               │
                     (4) Call  ▼  (5) Return Model & View / Data
                           Controller
                               │
                     (6) ViewResolver (If MVC) / MessageConverter (If REST)
                               ▼
Client ◄───────────────── HTTP Response
```

**Syntax + Code Examples**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id, @RequestParam boolean detail) {
        return ResponseEntity.ok(new User(id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User createUser(@RequestBody User user) {
        return user;
    }
}
```

**Common Mistakes + Best Practices**
- *Mistake*: Confusing `@PathVariable` (URI path: `/users/1`) with `@RequestParam` (Query string: `/users?id=1`).
- *Best Practice*: Use `@RestControllerAdvice` and `@ExceptionHandler` for centralized, clean global exception handling instead of try-catch in every controller.

**Interview Explanation**
Differentiate `@Controller` (returns Views) from `@RestController` (`@Controller` + `@ResponseBody`, returns data). Explain how `HttpMessageConverters` serialize Java objects to JSON using Jackson.

**Tricky Interview Questions**
- *Q: How does Content Negotiation work?*
  A: Spring looks at the HTTP `Accept` header (e.g., `application/json` vs `application/xml`) or a file extension in the URL to determine which HttpMessageConverter to use.

---

## 5. Spring Data JPA & Hibernate

**Definition + Why it exists**
- **Hibernate**: An ORM (Object-Relational Mapping) framework that maps Java objects to DB tables.
- **JPA**: The Java specification (interfaces) for ORM.
- **Spring Data JPA**: Abstraction layer over JPA that auto-generates data access code (Repositories) using method naming conventions.

**Internal Working**
Spring Data creates proxy implementations of repository interfaces at runtime. When a method like `findByLastName` is called, it translates the method name into a JPQL query, executes it via Hibernate's Session, and returns the entity.

**ASCII Diagram: Architecture**
```text
[Spring Data JPA (CrudRepository)]
             │ (Auto-generates proxies)
             ▼
[JPA (EntityManager)]
             │ (Standard API)
             ▼
[Hibernate (Session / ORM Engine)]
             │ (Translates to SQL)
             ▼
[JDBC] ──► [Database]
```

**Syntax + Code Examples**
```java
@Entity
@Table(name = "employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "dept_id")
    private Department department;
}

public interface EmployeeRepo extends JpaRepository<Employee, Long> {
    List<Employee> findByDepartmentId(Long deptId);
    
    @Query("SELECT e FROM Employee e JOIN FETCH e.department")
    List<Employee> findAllWithDepartment();
}
```

**Common Mistakes + Best Practices**
- *Mistake*: Defaulting to `FetchType.EAGER` for `@ManyToOne` relationships. This causes massive performance issues (N+1 problem).
- *Best Practice*: Always use `FetchType.LAZY`. Use `JOIN FETCH` or `@EntityGraph` when you explicitly need the associated entities in a single query.

**Interview Explanation**
Explain the N+1 problem: You execute 1 query to get N parents, then Hibernate executes N extra queries to get the children. Solution: `JOIN FETCH`.
Explain transactions: `@Transactional` uses AOP proxies to begin, commit, or rollback transactions. Default propagation is `REQUIRED`.

**Tricky Interview Questions**
- *Q: Difference between save() and saveAndFlush()?*
  A: `save()` keeps the entity in the Persistence Context (L1 cache) and flushes to DB at transaction commit. `saveAndFlush()` forces an immediate SQL insert/update.
- *Q: What are L1 and L2 caches?*
  A: L1 is the Session cache (enabled by default, scoped to transaction). L2 is the SessionFactory cache (shared across sessions, requires configuration like EhCache).

---

## 6. Spring Security

**Definition + Why it exists**
A framework focusing on Authentication (Who are you?) and Authorization (What can you do?). It protects Spring apps against common vulnerabilities (CSRF, session fixation).

**Internal Working**
Built around a chain of Servlet `Filter`s (Security Filter Chain). `UsernamePasswordAuthenticationFilter` extracts credentials, passes them to `AuthenticationManager`, which delegates to `AuthenticationProvider`, which uses `UserDetailsService` to fetch user details from the DB and compare the password using `PasswordEncoder`.

**Syntax + Code Examples**
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf().disable() // Disable for stateless APIs
        .authorizeHttpRequests()
        .requestMatchers("/api/public/**").permitAll()
        .anyRequest().authenticated()
        .and()
        .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    return http.build();
}
```

**Tricky Interview Questions**
- *Q: What is the difference between @PreAuthorize and @Secured?*
  A: `@PreAuthorize` uses SpEL (Spring Expression Language) enabling complex rules (e.g., `#user.name == principal.username`). `@Secured` is older and only supports roles.
- *Q: What is a JWT and how is it used in Spring Security?*
  A: JSON Web Token is a stateless token. In Spring, you create a custom OncePerRequestFilter to extract the JWT from the Authorization header, validate the signature, and set the `SecurityContextHolder`.

---

## 7. Microservices with Spring

**Definition + Why it exists**
Microservices divide a monolith into small, independently deployable services organized around business capabilities. Spring Cloud provides tools to build distributed systems.

**Key Components**
- **Service Discovery (Eureka)**: A phonebook for services. Services register themselves; clients query Eureka to find IP addresses.
- **API Gateway (Spring Cloud Gateway)**: Single entry point routing requests to appropriate microservices. Handles cross-cutting concerns (auth, rate limiting).
- **Load Balancing (Spring Cloud LoadBalancer)**: Client-side routing to distribute traffic among multiple instances of a service.
- **Circuit Breaker (Resilience4j)**: Stops cascading failures. If Service B is down, Service A stops calling it and executes a fallback method.
- **Config Server**: Externalized, centralized configuration management.

**Interview Explanation**
Focus on the resilience and discovery aspects. "Without Eureka, we'd hardcode IPs. Without an API Gateway, frontend clients would need to know 50 different microservice URLs. Without Circuit Breakers, one slow database could bring down the entire ecosystem."

---

## Top 50 Spring Boot Interview Questions

1. **What is Spring Boot?** An extension of Spring that auto-configures applications and provides embedded servers.
2. **What is IoC?** Inversion of Control, letting the container manage object lifecycles.
3. **What is DI?** Dependency Injection, providing objects with their instance variables rather than them creating it.
4. **ApplicationContext vs BeanFactory?** BeanFactory is lazy; ApplicationContext is eager and adds enterprise features.
5. **Default Bean Scope?** Singleton.
6. **How to create a prototype bean?** `@Scope("prototype")`.
7. **What is @Autowired?** Marks a constructor, field, or setter for automatic injection by Spring.
8. **What does @SpringBootApplication do?** Combines `@Configuration`, `@EnableAutoConfiguration`, and `@ComponentScan`.
9. **How does Auto-configuration work?** Inspects classpath and defines beans automatically if specific classes/beans are missing.
10. **Difference between @Component, @Service, @Repository?** `@Component` is generic; `@Service` denotes business logic; `@Repository` translates SQL exceptions into Spring DataAccessException.
11. **What is @RestController?** `@Controller` + `@ResponseBody`.
12. **@RequestMapping vs @GetMapping?** `@GetMapping` is a shortcut for `@RequestMapping(method = RequestMethod.GET)`.
13. **@PathVariable vs @RequestParam?** PathVariable extracts data from URI path; RequestParam from query params.
14. **What is Actuator?** Provides production-ready endpoints (health, metrics, env).
15. **How to change default Tomcat port?** `server.port=8080` in properties file.
16. **How to handle exceptions globally?** `@ControllerAdvice` + `@ExceptionHandler`.
17. **What is Spring Data JPA?** Repository abstraction over JPA.
18. **Difference between CrudRepository and JpaRepository?** JpaRepository extends PagingAndSortingRepository and provides JPA-specific methods like `flush()`.
19. **What is the N+1 problem?** One query fetches N parents, N queries fetch their children. Fix with `JOIN FETCH`.
20. **@Transactional propagation default?** `REQUIRED` (join existing, or create new).
21. **What is Spring Security?** Authentication and authorization framework.
22. **What is a Security Filter Chain?** A chain of filters checking headers, sessions, and credentials.
23. **What is UserDetailsService?** Interface to load user-specific data from DB.
24. **Difference between Authentication and Authorization?** Identity verification vs. access control.
25. **What is JWT?** Stateless token containing JSON payload, signed to prevent tampering.
26. **What is Eureka?** Service registry and discovery server.
27. **What is an API Gateway?** Reverse proxy, single entry point for microservices.
28. **What is a Circuit Breaker?** Pattern to prevent cascading failures in distributed systems.
29. **What does @Qualifier do?** Disambiguates injection when multiple beans of the same type exist.
30. **What is @Primary?** Marks a bean as the default candidate for autowiring.
31. **What are Spring Profiles?** Way to segregate parts of application config (e.g., dev, prod) and make it available only in certain environments.
32. **Constructor vs Setter injection?** Constructor enforces mandatory dependencies and immutability; Setter is for optional.
33. **Can you inject a prototype bean into a singleton?** Yes, but it only injects once. Use `@Lookup` for dynamic fetching.
34. **What is Spring Cloud Config?** Centralized external configuration management.
35. **Difference between application.yml and bootstrap.yml?** Bootstrap is loaded earlier by the parent context (used for config server config).
36. **How to test a Spring Boot application?** `@SpringBootTest`. Use `@WebMvcTest` for controller slicing.
37. **What is @MockBean?** Adds a mock to the Spring ApplicationContext, replacing any existing bean of the same type.
38. **What is the Front Controller pattern in Spring?** `DispatcherServlet`.
39. **How to secure an endpoint in Spring Security?** `.requestMatchers("/api/**").authenticated()`.
40. **How does @Transactional work internally?** Generates a proxy around the target object that intercepts calls to begin/commit/rollback the transaction.
41. **What are JPA cascade types?** Define how entity state transitions cascade to child entities (e.g., ALL, PERSIST, REMOVE).
42. **L1 vs L2 Cache in Hibernate?** L1 is Session-scoped, L2 is SessionFactory-scoped.
43. **What is @EntityGraph?** Defines a template to specify fetch plans, avoiding N+1.
44. **What is CORS?** Cross-Origin Resource Sharing. Configured via `@CrossOrigin`.
45. **What is CSRF?** Cross-Site Request Forgery. Often disabled for stateless REST APIs.
46. **What is a Feign Client?** Declarative REST client used to call other microservices.
47. **How to start a background task?** `@EnableAsync` and `@Async`.
48. **How to run code on startup?** Implement `CommandLineRunner` or `ApplicationRunner`.
49. **How to exclude a dependency from auto-configuration?** In application.properties: `spring.autoconfigure.exclude`.
50. **Why is field injection bad?** Hides dependencies, difficult to mock without reflection, masks circular dependencies.

---

# Section 13 - Database Concepts for Java Interviews

## 1. JDBC Architecture

**Definition + Why it exists**
Java Database Connectivity (JDBC) is the Java API that connects and executes queries with the database. It exists to provide a uniform, DB-agnostic interface.
*DriverManager*: Manages a list of DB drivers. Matches connection requests to the right driver.
*Connection*: Session with the DB.
*Statement*: Executes static SQL.
*PreparedStatement*: Executes pre-compiled SQL (prevents SQL injection).
*CallableStatement*: Executes DB stored procedures.
*ResultSet*: Stores data retrieved from DB.

**Syntax + Code Example**
```java
String url = "jdbc:mysql://localhost:3306/db";
try (Connection conn = DriverManager.getConnection(url, "user", "pass");
     PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE age > ?")) {
    
    pstmt.setInt(1, 18);
    ResultSet rs = pstmt.executeQuery();
    while (rs.next()) {
        System.out.println(rs.getString("username"));
    }
}
```

**Common Mistakes & Interview Qs**
- *Mistake*: Using `Statement` instead of `PreparedStatement` using string concatenation. This invites SQL Injection.
- *Q: Why use Connection Pooling (HikariCP)?*
  A: Creating DB connections via TCP is extremely slow and resource-heavy. Connection pools keep a set of active connections ready to be borrowed, drastically improving latency.

---

## 2. ACID Properties

**Definition**
- **Atomicity**: "All or Nothing." If a transaction has 5 steps, and step 4 fails, the DB rolls back steps 1-3. (e.g., Bank transfer: deduct from A, add to B. Must do both or neither).
- **Consistency**: Database state must remain valid before and after a transaction according to defined rules/constraints.
- **Isolation**: Concurrent transactions do not interfere with each other. (Implemented via locking/MVCC).
- **Durability**: Once a transaction commits, it remains committed even if the server crashes (Saved to persistent storage/Write-Ahead Logging).

---

## 3. Transaction Isolation Levels

**Definition**
Control the degree to which transactions are isolated from data modifications made by other transactions.

**Concurrency Anomalies**
- *Dirty Read*: Reading uncommitted data from another transaction.
- *Non-repeatable Read*: Reading the same row twice, but getting different data because another transaction updated it in between.
- *Phantom Read*: Running a range query twice, but getting a different number of rows because another transaction inserted/deleted rows.

**Isolation Levels Table**
| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Lock Strategy |
| :--- | :---: | :---: | :---: | :--- |
| **Read Uncommitted** | Yes | Yes | Yes | No locks |
| **Read Committed** (Default PG/Oracle) | No | Yes | Yes | Locks updated rows |
| **Repeatable Read** (Default MySQL) | No | No | Yes | Locks read/updated rows |
| **Serializable** | No | No | No | Locks tables / Range locks |

---

## 4. Indexing

**Definition + Why it exists**
An index is a data structure (usually B-Tree or Hash) that improves the speed of data retrieval operations on a database table at the cost of slower writes and more storage space. Analogy: Index at the back of a book.

**Types**
- **Clustered Index**: Determines the physical order of data in the table. Only ONE per table (usually Primary Key). Leaves of the B-Tree contain the actual row data.
- **Non-clustered Index**: Secondary index. Leaves contain pointers to the clustered index.
- **Composite Index**: Index on multiple columns. Must follow *Leftmost Prefix Rule*.
- **Covering Index**: An index that contains all the columns needed for a query, avoiding the need to look up the actual table row.

**Tricky Interview Questions**
- *Q: Why do indexes hurt performance?*
  A: Every INSERT, UPDATE, or DELETE requires updating the B-Tree index structures, slowing down write operations.
- *Q: What does the EXPLAIN keyword do?*
  A: It shows the execution plan of a query (whether it uses a full table scan or an index scan).

---

## 5. SQL Joins

**Definition**
Combine rows from two or more tables based on a related column.

**ASCII Venn Diagrams & Types**
```text
INNER JOIN: (A ∩ B) - Returns records with matching values in both tables.
LEFT JOIN:  (A) + (A ∩ B) - Returns all records from left table, and matched from right.
RIGHT JOIN: (B) + (A ∩ B) - Returns all records from right table, and matched from left.
FULL OUTER: (A U B) - Returns all records when there is a match in either left or right.
CROSS JOIN: Cartesian product (Row count = A * B).
SELF JOIN: Table joined with itself.
```

**Common Mistake**
- Filtering LEFT JOIN conditions in the `WHERE` clause instead of the `ON` clause turns it into an INNER JOIN.

---

## 6. Normalization

**Definition**
Organizing data to reduce redundancy and improve data integrity.
- **1NF**: Atomic values. No repeating groups/arrays in a column.
- **2NF**: 1NF + All non-key attributes are fully dependent on the whole Primary Key (no partial dependency).
- **3NF**: 2NF + No transitive dependencies (Non-key columns shouldn't depend on other non-key columns).
- **BCNF**: Stricter 3NF where every determinant must be a candidate key.

*Denormalization* is intentionally adding redundancy to speed up read performance (avoiding complex joins), common in Data Warehousing.

---

## 7. Common SQL Interview Questions & Window Functions

- **Nth Highest Salary**: 
  ```sql
  -- Using Window Function
  SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
  ) WHERE rank = N;
  ```
- **Duplicate Removal**:
  ```sql
  DELETE FROM employees WHERE id NOT IN (
    SELECT MIN(id) FROM employees GROUP BY email
  );
  ```
- **GROUP BY vs HAVING**: `WHERE` filters rows *before* aggregation. `HAVING` filters groups *after* aggregation.
- **EXISTS vs IN**: `EXISTS` evaluates true/false iteratively and stops at the first match (better for large subqueries). `IN` compares against a generated list of all values in the subquery.

---

## Top 30 Database Interview Questions

1. **What is a Primary Key?** Unique identifier for a record; cannot be null.
2. **What is a Foreign Key?** Field that refers to the Primary Key of another table, ensuring referential integrity.
3. **TRUNCATE vs DELETE?** TRUNCATE is DDL (fast, resets identity, cannot rollback). DELETE is DML (logs each row, can be rolled back).
4. **DROP vs TRUNCATE?** DROP removes the table structure and data entirely.
5. **What is a View?** A virtual table based on the result-set of an SQL statement.
6. **What is a Materialized View?** A view that physically stores data for faster reads, periodically refreshed.
7. **What is a Trigger?** SQL code automatically executed in response to certain events on a table.
8. **What is a Stored Procedure?** Precompiled block of SQL code stored in the DB.
9. **Difference between Function and Procedure?** Function must return a value and can be used in a SELECT statement. Procedure might not return and cannot be used in SELECT.
10. **What is a B-Tree?** Balanced tree data structure keeping data sorted, used heavily in databases for indexes.
11. **What is the N+1 query problem?** Fetching N records, then running N queries to get related entities.
12. **UNION vs UNION ALL?** UNION removes duplicates and sorts. UNION ALL includes duplicates and is faster.
13. **What is DDL vs DML?** DDL (Data Definition Language: CREATE, ALTER). DML (Data Manipulation Language: SELECT, INSERT, UPDATE).
14. **What is DCL and TCL?** DCL (Data Control Language: GRANT, REVOKE). TCL (Transaction Control Language: COMMIT, ROLLBACK).
15. **What is a Sequence?** Database object generating unique numeric values.
16. **How do you optimize a slow query?** Use EXPLAIN to check execution plan, add missing indexes, avoid SELECT *, rewrite subqueries to joins.
17. **What is a Deadlock?** Two transactions wait for locks held by each other, blocking forever. DB kills one transaction to resolve it.
18. **What is MVCC?** Multi-Version Concurrency Control. Allows readers to not block writers, and writers not to block readers by keeping snapshots of data.
19. **What is a cursor?** A DB object to retrieve data row by row (usually slow, should be avoided).
20. **Leftmost Prefix Rule in indexing?** If index is on (A, B, C), query must use A, or A,B, or A,B,C to utilize the index. Query on B,C ignores index.
21. **What is sharding?** Horizontal partitioning of a DB across multiple servers.
22. **What is replication?** Copying data from a Master node to Replica nodes for high availability and read scaling.
23. **What is SQL Injection?** Malicious SQL statements inserted into entry fields. Prevented by PreparedStatements.
24. **Difference between clustered and non-clustered index?** Clustered dictates physical order; non-clustered is a separate lookup table.
25. **What is an anti-join?** Finding rows in one table that do not have a match in another (using LEFT JOIN where right side IS NULL).
26. **Row_Number vs Rank vs Dense_Rank?** `Row_Number`: 1,2,3,4. `Rank`: 1,2,2,4. `Dense_Rank`: 1,2,2,3.
27. **What is OLTP vs OLAP?** OLTP: Online Transaction Processing (fast writes, normal DB). OLAP: Online Analytical Processing (heavy reads, Data Warehouse).
28. **What is a Self Join?** A table joined to itself, useful for hierarchical data (e.g., Employees and their Managers in the same table).
29. **Difference between COUNT(*) and COUNT(column)?** `COUNT(*)` counts all rows. `COUNT(column)` ignores NULLs in that column.
30. **Why avoid SELECT *?** Wastes I/O, memory, and network bandwidth. Breaks Covering Indexes.
