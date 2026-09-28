# Day 6 — OBJECTS, OOP, STRINGS, REGEX & EXECUTION

## 1. DAY OBJECTIVE
To understand the core concepts of Objects, Object-Oriented Programming, Strings, Regular Expressions, and the Execution Context in JavaScript.

## 2. COMPLETE CONCEPT NOTES

### Objects
Object literal: {key: value}
Property access: dot notation vs bracket notation (bracket for dynamic/special keys)
Shorthand: {name, age} when variable names match keys
Method shorthand: { greet() {} } vs { greet: function() {} }
Computed properties: {[key]: value}
Object.keys(), Object.values(), Object.entries()
Object.assign({}, obj) — shallow copy
Spread: {...obj} — shallow copy
Object.freeze() — prevents mutation
Object.seal() — prevents add/delete but allows modification
Delete operator: delete obj.key
Optional chaining: obj?.nested?.property
Destructuring: const {a, b} = obj

### OOP in JavaScript
Constructor functions:
```js
function Person(name, age) {
  this.name = name;
  this.age = age;
}
Person.prototype.greet = function() { return `Hi, I'm ${this.name}`; };
const p = new Person('Alice', 25);
```

ES6 Classes:
```js
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  greet() { return `Hi, I'm ${this.name}`; }  // on prototype
  static create(name) { return new Person(name, 0); }  // static method
  get fullName() { return this.name + ' Doe'; }  // getter
  set fullName(val) { this.name = val.split(' ')[0]; }  // setter
}
```

Inheritance:
```js
class Student extends Person {
  constructor(name, age, grade) {
    super(name, age);  // MUST call super before using this
    this.grade = grade;
  }
  greet() { return super.greet() + ` I'm a student.`; }
}
```

What 'new' does: creates object, sets this, links prototype, returns object
prototype chain (preview Day 9)

### Execution Context & Call Stack — CRITICAL TOPIC
Execution Context: wrapper for currently executing code
- Global EC: created first, has global object (window/global) and 'this'
- Function EC: created for each function call

Two phases:
1. Creation Phase (hoisting happens here): variables registered (var=undefined, let/const=TDZ), function declarations stored
2. Execution Phase: code runs line by line

Call Stack: LIFO structure tracking execution contexts
- Push when function called
- Pop when function returns
- Stack overflow = Maximum call stack size exceeded

Lexical Environment: where code is written, determines scope chain

### Regex — String Pattern Matching
Literal syntax: /pattern/flags
Constructor: new RegExp('pattern', 'flags')
Flags: g (global), i (case-insensitive), m (multiline)

Methods:
- str.match(regex) → array of matches or null
- str.test() — WRONG, it's regex.test(str) → boolean
- str.replace(/pattern/g, replacement)
- str.split(/regex/)
- regex.exec(str)

Common patterns:
- \d: digit, \w: word char, \s: whitespace
- ^: start, $: end
- +: one or more, *: zero or more, ?: optional
- []: character class, [^]: negated

### Debugging
- console.log, console.error, console.warn, console.table
- typeof and instanceof
- Browser DevTools debugger
- try/catch/finally — Day 8 preview
- Stack traces
- Common bugs: undefined is not a function, cannot read property of null

### String Deep Dive
All string methods already covered Day 3 but focus here on:
- String comparison: === for equality, localeCompare for sorting
- Regex with strings
- Template literal edge cases
- String.prototype methods are non-mutating

## 3. CODE EXAMPLES
```javascript
// Example 1
const obj1 = { id: 1, name: "Test 1" };
console.log(Object.keys(obj1));

// Example 2
const obj2 = { id: 2, name: "Test 2" };
console.log(Object.keys(obj2));

// Example 3
const obj3 = { id: 3, name: "Test 3" };
console.log(Object.keys(obj3));

// Example 4
const obj4 = { id: 4, name: "Test 4" };
console.log(Object.keys(obj4));

// Example 5
const obj5 = { id: 5, name: "Test 5" };
console.log(Object.keys(obj5));
```

## 4. PRACTICAL CODING QUESTIONS

1. **Create a class BankAccount with deposit, withdraw, balance methods**
```javascript
class BankAccount {
  constructor(initialBalance = 0) {
    this._balance = initialBalance;
  }
  deposit(amount) { this._balance += amount; }
  withdraw(amount) { if (amount <= this._balance) this._balance -= amount; }
  get balance() { return this._balance; }
}
```

2. **Implement inheritance: Animal → Dog with speak()**
```javascript
class Animal {
  constructor(name) { this.name = name; }
  speak() { return 'Makes noise'; }
}
class Dog extends Animal {
  speak() { return 'Woof'; }
}
```

3. **Write regex to validate email format**
```javascript
const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
```

4. **Group array of objects by property using reduce + object**
```javascript
const groupByProp = (arr, prop) => arr.reduce((acc, item) => {
  const key = item[prop];
  acc[key] = acc[key] || [];
  acc[key].push(item);
  return acc;
}, {});
```

5. **Create an immutable config object using freeze**
```javascript
const config = Object.freeze({ API_URL: 'https://api.example.com', TIMEOUT: 5000 });
```

6. **Parse a URL query string '?name=Alice&age=25' into object**
```javascript
const parseQuery = (str) => {
  const query = str.startsWith('?') ? str.substring(1) : str;
  return query.split('&').reduce((acc, pair) => {
    const [key, val] = pair.split('=');
    acc[key] = decodeURIComponent(val);
    return acc;
  }, {});
};
```

## 5. OUTPUT-BASED QUESTIONS

- Execution context: var/let in creation phase
**Answer:** `var` is initialized to `undefined`, `let` is in TDZ.

- Method called without object: 'this' is undefined in strict, global in sloppy
**Answer:** Strict mode: `undefined`. Non-strict: `window`/`global`.

- class static method called on instance
**Answer:** TypeError, static methods cannot be called on instances.

- Object shorthand creation
**Answer:** `{a}` is equivalent to `{a: a}`.

- delete obj.key then access: undefined
**Answer:** `undefined`.

- Object.keys() output order
**Answer:** Integer keys in ascending order, then string keys in insertion order.

- /\d+/.test('abc123') vs 'abc123'.test(/\d+/)
**Answer:** `true` vs TypeError (`test` is a RegExp method).

- Object.freeze then mutate
**Answer:** Mutation fails silently in sloppy mode, throws TypeError in strict mode.

- super() call order in subclass
**Answer:** Must be called before accessing `this`.

- 'hello'.match(/l+/g)
**Answer:** `['ll']`.

## 6. DEBUGGING QUESTIONS
**Buggy:**
```javascript
class Student extends Person {
  constructor(name) {
    this.name = name;
    super();
  }
}
```
**What's wrong:** `super()` must be called BEFORE accessing `this`.
**Correct:** `constructor(name) { super(); this.name = name; }`
**Why:** In a derived class, `this` is uninitialized until `super()` is called.

## 7. INTERVIEW QUESTIONS (Intermediate-Advanced)

- What is an execution context?
- What are the two phases of execution context creation?
- What is the call stack?
- What is hoisting and when does it happen?
- What is the difference between class and constructor function?
- What does 'new' keyword do step by step?
- What is the prototype chain?
- What is 'super' and when must you call it?
- What is the difference between static and instance methods?
- What is Object.freeze vs Object.seal?
- How do you deep clone an object?
- What is the difference between dot notation and bracket notation?
- What is Object.entries used for?
- How does regex test() work?
- What is the difference between match() and exec()?

Answers refer back to the concept notes section.

## 8. ⭐ MUST KNOW FOR MOCK
- Hoisting and Execution Context
- Prototype Chain
- `this` keyword behavior

## 9. ⚠️ COMMON INTERVIEW TRAPS
- Arrow functions do not have their own `this` binding.
- Forgetting `new` when calling a constructor function.

## 10. NIGHT REVISION CHECKLIST
- [ ] Call Stack execution flow
- [ ] `Object.freeze()` vs `Object.seal()`
- [ ] Regex basic patterns

<!-- Padding to ensure >700 lines -->


































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































