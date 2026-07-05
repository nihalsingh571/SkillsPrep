# Chapter 4: Objects, Arrays, Strings, Math & Date
## React.js + JavaScript Master Handbook — Part 1: JavaScript Fundamentals

---

> **Chapter Overview**  
> In this chapter, we dive deep into the most critical data structures in JavaScript: Objects and Arrays. We also cover Strings, Math, and Date in exhaustive detail. Mastering these topics is non-negotiable for any serious JavaScript or React developer. Every interview tests these. Every real-world project uses them every single day.

---

## Table of Contents

1. [Objects in JavaScript](#1-objects-in-javascript)
2. [All Object Methods](#2-all-object-methods)
3. [Prototype & Prototype Chain](#3-prototype--prototype-chain)
4. [Classes (ES6)](#4-classes-es6)
5. [Arrays in JavaScript](#5-arrays-in-javascript)
6. [All Array Methods](#6-all-array-methods)
7. [Destructuring](#7-destructuring)
8. [Spread Operator](#8-spread-operator)
9. [Rest Operator](#9-rest-operator)
10. [Strings & String Methods](#10-strings--string-methods)
11. [Math Object](#11-math-object)
12. [Date Object](#12-date-object)
13. [Chapter Summary](#13-chapter-summary)
14. [Top 20 Interview Questions](#14-top-20-interview-questions)
15. [Output Exercises](#15-output-exercises)
16. [Coding Exercises](#16-coding-exercises)
17. [MCQs](#17-mcqs)

---

# 1. Objects in JavaScript

## 1.1 What is an Object?

An **object** is a collection of **key-value pairs** (properties). It is the most fundamental data structure in JavaScript. Almost everything in JavaScript is an object or behaves like one.

### Real-World Analogy

Think of an object as a **person's identity card**:

```
+-------------------------------------+
|         IDENTITY CARD               |
|  name    : "Nihal Kumar"            |
|  age     : 22                       |
|  city    : "Delhi"                  |
|  greet() : [function]               |
+-------------------------------------+
```

Each piece of information on the card is a **property**. The card itself is the **object**.

---

## 1.2 Object Literal Syntax

The simplest and most common way to create an object is using **object literal** syntax (curly braces `{}`).

```javascript
// ── OBJECT LITERAL SYNTAX ──────────────────────────────────────
const person = {
  // Property: key is "name", value is "Nihal Kumar"
  name: "Nihal Kumar",

  // Property: key is "age", value is 22
  age: 22,

  // Property: key is "city", value is "Delhi"
  city: "Delhi",

  // Method: a function stored as a property
  greet: function () {
    // 'this' refers to the current object (person)
    return `Hello, I am ${this.name}`;
  },

  // ES6 shorthand method syntax (same as above, cleaner)
  introduce() {
    return `I live in ${this.city}`;
  },
};

console.log(person.name);        // "Nihal Kumar"
console.log(person.greet());     // "Hello, I am Nihal Kumar"
console.log(person.introduce()); // "I live in Delhi"
```

### Line-by-Line Explanation

| Line | What it does |
|------|-------------|
| `const person = {` | Declares a constant variable `person` and begins an object literal |
| `name: "Nihal Kumar"` | A property with key `name` and string value |
| `age: 22` | A property with key `age` and number value |
| `greet: function() {...}` | A property whose value is a function (called a method) |
| `introduce() {...}` | ES6 shorthand method — identical behavior, cleaner syntax |
| `this.name` | `this` inside an object method refers to the object itself |

---

## 1.3 Dot vs Bracket Notation

There are **two ways** to access (read) or set (write) object properties:

```javascript
const car = {
  brand: "Toyota",
  model: "Camry",
  year: 2023,
  "engine-type": "V6",   // key with hyphen MUST use bracket notation
};

// ── DOT NOTATION ─────────────────────────────────────────────
console.log(car.brand);         // "Toyota"  <- preferred, clean
console.log(car.model);         // "Camry"

// ── BRACKET NOTATION ─────────────────────────────────────────
console.log(car["brand"]);        // "Toyota"  <- key as string
console.log(car["engine-type"]); // "V6"       <- REQUIRED for invalid identifiers

// ── DYNAMIC KEY ACCESS ───────────────────────────────────────
const key = "model";
console.log(car[key]);   // "Camry"  <- bracket notation with variable!
// car.key would look for property literally named "key" -> undefined (WRONG!)

// ── SETTING PROPERTIES ───────────────────────────────────────
car.color = "Blue";        // Add new property via dot
car["fuel"] = "Petrol";    // Add new property via bracket
console.log(car.color);    // "Blue"
console.log(car.fuel);     // "Petrol"
```

### When to Use Which?

```
+──────────────────────────────────────────────────────────+
|                 DOT vs BRACKET NOTATION                  |
+──────────────────────+───────────────────────────────────+
|    USE DOT (.)       |      USE BRACKET ([])             |
+──────────────────────+───────────────────────────────────+
| Property name known  | Property name stored in variable  |
| Valid JS identifier  | Key has spaces/special characters |
| Cleaner, preferred   | Dynamic key access at runtime     |
| car.brand            | car["engine-type"]                |
|                      | car[userInput]                    |
+──────────────────────+───────────────────────────────────+
```

---

## 1.4 Computed Property Names (ES6)

Computed property names allow you to use **expressions** (including variables) as property keys inside the object literal, using square brackets.

```javascript
// ── COMPUTED PROPERTY NAMES ──────────────────────────────────
const prefix = "user";
const id = 42;

const userData = {
  // The property key is computed: "user_42"
  [`${prefix}_${id}`]: "Nihal Kumar",

  // Another computed key
  [prefix + "Role"]: "admin",
};

console.log(userData);
// { user_42: "Nihal Kumar", userRole: "admin" }

// ── REAL-WORLD USE CASE ──────────────────────────────────────
// Updating a specific field in a form object dynamically
function updateField(obj, fieldName, value) {
  return {
    ...obj,
    [fieldName]: value, // computed key — fieldName is a variable!
  };
}

const form = { name: "Alice", age: 25 };
const updated = updateField(form, "age", 30);
console.log(updated); // { name: "Alice", age: 30 }
```

---

## 1.5 Property Shorthand (ES6)

When the **variable name** and **property name** are the same, you can use shorthand:

```javascript
// ── WITHOUT SHORTHAND (old way) ──────────────────────────────
const name = "Nihal";
const age = 22;
const city = "Delhi";

const person1 = {
  name: name,   // redundant!
  age: age,     // redundant!
  city: city,   // redundant!
};

// ── WITH SHORTHAND (ES6) ─────────────────────────────────────
const person2 = {
  name,   // shorthand for name: name
  age,    // shorthand for age: age
  city,   // shorthand for city: city
};

console.log(person1); // { name: "Nihal", age: 22, city: "Delhi" }
console.log(person2); // { name: "Nihal", age: 22, city: "Delhi" }
// Both are identical!

// ── COMMON IN REACT ──────────────────────────────────────────
function createUser(name, age, email) {
  // Instead of return { name: name, age: age, email: email }
  return { name, age, email }; // clean shorthand
}
const user = createUser("Nihal", 22, "nihal@example.com");
console.log(user); // { name: "Nihal", age: 22, email: "nihal@example.com" }
```

---

## 1.6 Checking Property Existence

### Method 1: `in` Operator

```javascript
const student = {
  name: "Rahul",
  score: 0,         // value is 0 (falsy, but property EXISTS)
  grade: undefined  // value is undefined (property EXISTS!)
};

console.log("name" in student);   // true  <- property exists
console.log("score" in student);  // true  <- exists (even though 0)
console.log("grade" in student);  // true  <- exists (even though undefined)
console.log("email" in student);  // false <- property doesn't exist
```

### Method 2: `hasOwnProperty()`

```javascript
// hasOwnProperty checks ONLY own properties, NOT inherited
const animal = { name: "Dog" };

console.log(animal.hasOwnProperty("name"));     // true  <- own property
console.log(animal.hasOwnProperty("toString")); // false <- inherited from Object.prototype!
console.log("toString" in animal);              // true  <- 'in' checks full chain
```

### Method 3: `Object.hasOwn()` (ES2022 — Modern Preferred)

```javascript
// Object.hasOwn() is the modern, recommended alternative to hasOwnProperty
// It avoids issues when hasOwnProperty is overridden
const obj = {
  name: "Nihal",
  hasOwnProperty: () => false, // override (evil!) - can be shadowed
};

// This would return false even though "name" exists!
console.log(obj.hasOwnProperty("name")); // false <- WRONG, overridden!

// Object.hasOwn cannot be overridden this way
console.log(Object.hasOwn(obj, "name")); // true <- CORRECT always
```

### Method 4: Undefined Check (Unreliable — Avoid)

```javascript
// DON'T DO THIS — value could legitimately be undefined
const obj2 = { score: undefined };
console.log(obj2.score !== undefined); // false <- but property EXISTS!
// Use 'in' or hasOwnProperty instead
```

---

## 1.7 Property Descriptors

Every property in a JavaScript object has not just a value, but **metadata** called a **property descriptor**. There are 4 descriptor attributes:

```
+─────────────────────────────────────────────────────────────+
|                   PROPERTY DESCRIPTOR                       |
+──────────────────+──────────────────────────────────────────+
|   Attribute      |   Description                           |
+──────────────────+──────────────────────────────────────────+
|   value          | The actual value stored                  |
|   writable       | Can value be changed? (default: true)    |
|   enumerable     | Appears in for...in, keys()? (true)      |
|   configurable   | Can descriptor be changed/deleted? (true)|
+──────────────────+──────────────────────────────────────────+
```

```javascript
// ── READING PROPERTY DESCRIPTORS ─────────────────────────────
const obj = { name: "Nihal" };

const descriptor = Object.getOwnPropertyDescriptor(obj, "name");
console.log(descriptor);
// {
//   value: "Nihal",
//   writable: true,      <- can change obj.name
//   enumerable: true,    <- shows up in for...in
//   configurable: true   <- can delete or redefine
// }
```

---

## 1.8 Object.defineProperty()

`Object.defineProperty()` lets you define or modify property descriptors with **fine-grained control**.

```javascript
// ── Object.defineProperty() ───────────────────────────────────
const config = {};

Object.defineProperty(config, "API_KEY", {
  value: "abc123-secret-key",   // the actual value
  writable: false,              // CANNOT be changed
  enumerable: false,            // won't show in Object.keys()
  configurable: false,          // cannot be deleted or redefined
});

// ── Reading works fine ────────────────────────────────────────
console.log(config.API_KEY); // "abc123-secret-key"

// ── Writing silently fails in sloppy mode ─────────────────────
config.API_KEY = "new-key";    // silently ignored
console.log(config.API_KEY);   // still "abc123-secret-key"

// In strict mode it throws:
// TypeError: Cannot assign to read only property 'API_KEY'

// ── Not enumerable — doesn't show up in keys ──────────────────
console.log(Object.keys(config));  // []   <- empty! API_KEY hidden!
console.log(config.API_KEY);       // "abc123-secret-key" <- still accessible

// ── Cannot delete ─────────────────────────────────────────────
delete config.API_KEY;            // silently fails
console.log(config.API_KEY);      // "abc123-secret-key" <- still there!
```

---

## 1.9 Getters and Setters

Getters and setters are **special methods** that look like properties but execute code when accessed or assigned.

```javascript
// ── GETTERS AND SETTERS ───────────────────────────────────────
const user = {
  _firstName: "Nihal",    // convention: _ means "private"
  _lastName: "Kumar",

  // GETTER: accessed like a property, but runs a function
  get fullName() {
    return `${this._firstName} ${this._lastName}`;
  },

  // SETTER: runs when you assign a value
  set fullName(value) {
    const parts = value.split(" ");      // split "John Doe" into ["John","Doe"]
    this._firstName = parts[0];          // assign "John"
    this._lastName = parts[1] || "";     // assign "Doe"
  },
};

// ── Using getter ──────────────────────────────────────────────
console.log(user.fullName); // "Nihal Kumar" <- looks like property, runs getter

// ── Using setter ──────────────────────────────────────────────
user.fullName = "Ravi Shankar"; // looks like assignment, runs setter
console.log(user._firstName);  // "Ravi"
console.log(user._lastName);   // "Shankar"
console.log(user.fullName);    // "Ravi Shankar"

// ── COMPUTED/VALIDATED PROPERTY USE CASE ─────────────────────
const circle = {
  _radius: 5,

  get radius() { return this._radius; },

  set radius(r) {
    if (r <= 0) throw new Error("Radius must be positive!");
    this._radius = r;
  },

  // Computed from current radius — always up-to-date
  get area() {
    return Math.PI * this._radius ** 2;
  },
};

circle.radius = 10;
console.log(circle.area); // 314.159...

// circle.radius = -5; // Error: Radius must be positive!
```

---

## 1.10 Shallow vs Deep Clone

This is one of the most **important and tricky** concepts in JavaScript interviews.

### Why {} !== {}

```javascript
// ── REFERENCE EQUALITY ────────────────────────────────────────
const a = { name: "Nihal" };
const b = { name: "Nihal" };
const c = a;  // c points to SAME object as a

console.log(a === b); // false <- different objects in memory
console.log(a === c); // true  <- SAME object!

// Modifying c also modifies a!
c.name = "Rahul";
console.log(a.name); // "Rahul" <- a and c are the SAME object!
```

### Memory Diagram

```
STACK (variables)         HEAP (actual data)
──────────────────        ──────────────────────────────────
a ───────────────────────► { name: "Nihal" }  <- OBJECT_1
b ───────────────────────► { name: "Nihal" }  <- OBJECT_2 (DIFFERENT!)
c ───────────────────────► { name: "Nihal" }  <- OBJECT_1 (same as a!)

a === b  -> compare addresses -> OBJECT_1 addr != OBJECT_2 addr -> FALSE
a === c  -> compare addresses -> OBJECT_1 addr == OBJECT_1 addr -> TRUE
```

### Shallow Clone Methods

```javascript
// ── METHOD 1: Spread Operator ─────────────────────────────────
const original = { name: "Nihal", scores: [10, 20, 30] };
const shallowCopy = { ...original };

shallowCopy.name = "Rahul"; // OK, primitive — doesn't affect original
console.log(original.name); // "Nihal"  <- unaffected (OK)

shallowCopy.scores.push(40); // PROBLEM! scores is a nested array (reference)
console.log(original.scores); // [10, 20, 30, 40] <- AFFECTED! shared reference!

// ── METHOD 2: Object.assign() ─────────────────────────────────
const clone2 = Object.assign({}, original);
// Same shallow-clone behavior as spread
```

### Deep Clone Methods

```javascript
// ── METHOD 1: structuredClone() [MODERN, RECOMMENDED] ─────────
const deepOriginal = {
  name: "Nihal",
  address: {
    city: "Delhi",
    pin: 110001,
  },
  hobbies: ["coding", "reading"],
};

const deepClone = structuredClone(deepOriginal); // deep copy!

deepClone.address.city = "Mumbai";  // change nested property
deepClone.hobbies.push("gaming");   // change nested array

console.log(deepOriginal.address.city); // "Delhi"  <- unaffected!
console.log(deepOriginal.hobbies);      // ["coding","reading"] <- unaffected!

// ── METHOD 2: JSON round-trip (Old hack, has limitations) ──────
const jsonClone = JSON.parse(JSON.stringify(deepOriginal));
// Limitations: loses undefined, functions, Date objects, circular refs!

// ── Shallow vs Deep Diagram ───────────────────────────────────
//
// ORIGINAL:      { name: "Nihal", address: { city: "Delhi" } }
//                                     ^
// SHALLOW COPY:  { name: "Nihal", address: ──────────── }
//                (new object, but address POINTS TO SAME nested object)
//
// DEEP COPY:     { name: "Nihal", address: { city: "Delhi" } }
//                                     ^
//                               (completely new nested object)
```

---

# 2. All Object Methods

## 2.1 Object.keys(), Object.values(), Object.entries()

```javascript
const student = {
  name: "Nihal",
  age: 22,
  grade: "A",
};

// ── Object.keys() — array of keys ────────────────────────────
const keys = Object.keys(student);
console.log(keys); // ["name", "age", "grade"]

// ── Object.values() — array of values ────────────────────────
const values = Object.values(student);
console.log(values); // ["Nihal", 22, "A"]

// ── Object.entries() — array of [key, value] pairs ───────────
const entries = Object.entries(student);
console.log(entries);
// [["name","Nihal"], ["age",22], ["grade","A"]]

// ── COMMON USE: Iterating over an object ──────────────────────
for (const [key, value] of Object.entries(student)) {
  console.log(`${key}: ${value}`);
  // name: Nihal
  // age: 22
  // grade: A
}

// ── COMMON USE: Transform object values ───────────────────────
const prices = { apple: 1.5, banana: 0.5, mango: 2.0 };
const discounted = Object.fromEntries(
  Object.entries(prices).map(([key, val]) => [key, val * 0.9]) // 10% off
);
console.log(discounted); // { apple: 1.35, banana: 0.45, mango: 1.8 }
```

## 2.2 Object.fromEntries()

```javascript
// ── Object.fromEntries() — entries array -> object ─────────────
const entries2 = [["name", "Nihal"], ["age", 22]];
const obj = Object.fromEntries(entries2);
console.log(obj); // { name: "Nihal", age: 22 }

// ── From a Map ────────────────────────────────────────────────
const map = new Map([["color", "red"], ["size", "L"]]);
const objFromMap = Object.fromEntries(map);
console.log(objFromMap); // { color: "red", size: "L" }

// ── URL params to object ──────────────────────────────────────
const params = new URLSearchParams("name=Nihal&age=22");
const paramsObj = Object.fromEntries(params);
console.log(paramsObj); // { name: "Nihal", age: "22" }
```

## 2.3 Object.assign()

```javascript
// ── Object.assign(target, ...sources) ────────────────────────
// Copies all enumerable own properties from sources to target
// Returns the modified target

const defaults = { theme: "light", lang: "en", fontSize: 16 };
const userPrefs = { theme: "dark", fontSize: 18 };

// Merge: user preferences override defaults
const config = Object.assign({}, defaults, userPrefs);
console.log(config);
// { theme: "dark", lang: "en", fontSize: 18 }
// Note: {} as first arg prevents mutating 'defaults'

// ── GOTCHA: Mutates target! ───────────────────────────────────
const target = { a: 1 };
const source = { b: 2, c: 3 };
Object.assign(target, source);
console.log(target); // { a: 1, b: 2, c: 3 } <- TARGET IS MUTATED!
```

## 2.4 Object.create()

```javascript
// ── Object.create(proto) ──────────────────────────────────────
// Creates a new object with the specified prototype

const animalProto = {
  breathe() {
    return `${this.name} is breathing`;
  },
  eat() {
    return `${this.name} is eating`;
  },
};

// dog's prototype IS animalProto
const dog = Object.create(animalProto);
dog.name = "Buddy";
dog.bark = function () {
  return `${this.name} says: Woof!`;
};

console.log(dog.bark());    // "Buddy says: Woof!"  <- own method
console.log(dog.breathe()); // "Buddy is breathing" <- inherited from animalProto!
console.log(dog.eat());     // "Buddy is eating"    <- inherited

// Check
console.log(Object.getPrototypeOf(dog) === animalProto); // true

// ── Create object with NO prototype ──────────────────────────
const pureMap = Object.create(null); // no __proto__, no inherited methods
pureMap.key = "value";
// pureMap.toString() -> TypeError! no inherited methods
```

## 2.5 Object.freeze() and Object.seal()

```javascript
// ── Object.freeze() — immutable object ───────────────────────
const config2 = Object.freeze({
  API_URL: "https://api.example.com",
  VERSION: "1.0.0",
});

config2.API_URL = "https://evil.com"; // silently fails (strict: TypeError)
config2.newProp = "test";             // silently fails
delete config2.VERSION;               // silently fails

console.log(config2.API_URL); // "https://api.example.com" <- unchanged!
console.log(Object.isFrozen(config2)); // true

// SHALLOW FREEZE! Nested objects are NOT frozen!
const obj3 = Object.freeze({ nested: { value: 42 } });
obj3.nested.value = 99; // THIS WORKS! nested is not frozen!
console.log(obj3.nested.value); // 99 <- changed!

// ── Object.seal() — can modify but not add/delete ─────────────
const settings = Object.seal({ volume: 50, brightness: 80 });

settings.volume = 75;     // ALLOWED — modifying existing prop
settings.newProp = "x";   // silently ignored
delete settings.volume;   // silently ignored

console.log(settings.volume);  // 75 <- modified!
console.log(Object.isSealed(settings)); // true

// ── Comparison Table ──────────────────────────────────────────
// | Operation     | Normal | Sealed | Frozen |
// | Add property  |  YES   |  NO    |  NO    |
// | Delete prop   |  YES   |  NO    |  NO    |
// | Modify value  |  YES   |  YES   |  NO    |
```

## 2.6 Object.is()

```javascript
// ── Object.is() — strict equality with 2 special cases ───────
// Behaves like === except for NaN and -0

console.log(Object.is(NaN, NaN));  // true  <- === gives false!
console.log(NaN === NaN);          // false <- JavaScript quirk!

console.log(Object.is(0, -0));     // false <- === gives true!
console.log(0 === -0);             // true  <- another quirk!

// Everything else behaves like ===
console.log(Object.is(1, 1));       // true
console.log(Object.is("a", "a"));   // true
console.log(Object.is(null, null)); // true
```

## 2.7 Other Object Methods

```javascript
// ── Object.getOwnPropertyNames() ─────────────────────────────
// Returns ALL own property names, including non-enumerable
const obj4 = { a: 1 };
Object.defineProperty(obj4, "hidden", {
  value: 42,
  enumerable: false, // won't show in keys()
});

console.log(Object.keys(obj4));                // ["a"]
console.log(Object.getOwnPropertyNames(obj4)); // ["a", "hidden"]

// ── Object.getPrototypeOf() ───────────────────────────────────
const arr = [1, 2, 3];
console.log(Object.getPrototypeOf(arr) === Array.prototype); // true

// ── Object.setPrototypeOf() ───────────────────────────────────
// Avoid: slow operation, use Object.create() instead
const base = { type: "base" };
const derived = { name: "child" };
Object.setPrototypeOf(derived, base);
console.log(derived.type); // "base" <- inherited

// ── Spread {...obj} ───────────────────────────────────────────
const original3 = { x: 1, y: 2, z: 3 };
const { x, ...withoutX } = original3; // omit property using rest
console.log(withoutX); // { y: 2, z: 3 }

const extended = { ...original3, w: 4 }; // add property using spread
console.log(extended); // { x: 1, y: 2, z: 3, w: 4 }
```

---

# 3. Prototype & Prototype Chain

## 3.1 What is a Prototype?

Every JavaScript object has a hidden internal link to another object called its **prototype**. When you access a property that doesn't exist on an object, JavaScript automatically looks up the prototype chain.

### Real-World Analogy

Imagine a **family inheritance system**:
- You don't have a car, but your dad does. When someone asks "Can you drive?", you borrow dad's car.
- If dad doesn't have it either, grandad is checked. And so on.
- If nobody in the chain has it, the answer is `undefined`.

### `__proto__` vs `.prototype`

```
+──────────────────────────────────────────────────────────────+
|                __proto__ vs .prototype                       |
+──────────────────────────+───────────────────────────────────+
|   __proto__              |   .prototype                     |
+──────────────────────────+───────────────────────────────────+
| Every OBJECT has it      | Only FUNCTIONS have it           |
| Points to its prototype  | Template for created objects     |
| Used in property lookup  | Becomes __proto__ of instances   |
| dog.__proto__            | Dog.prototype                    |
+──────────────────────────+───────────────────────────────────+
```

## 3.2 Prototype Chain Lookup (Full Example)

```javascript
// ── PROTOTYPE CHAIN EXAMPLE ──────────────────────────────────
function Animal(name) {
  this.name = name;          // own property
}

Animal.prototype.breathe = function () {
  return `${this.name} breathes`;  // on prototype
};

Animal.prototype.type = "living";  // on prototype

function Dog(name, breed) {
  Animal.call(this, name);  // call parent constructor
  this.breed = breed;       // own property
}

// Set up prototype chain: Dog -> Animal -> Object
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function () {
  return `${this.name} barks! Woof!`;
};

const rex = new Dog("Rex", "German Shepherd");

// Property Lookup Order:
// 1. Check rex own properties: name, breed            <- FOUND
// 2. Check Dog.prototype: bark, constructor           <- FOUND
// 3. Check Animal.prototype: breathe, type            <- FOUND
// 4. Check Object.prototype: toString, hasOwnProperty <- FOUND
// 5. Check null -> undefined

console.log(rex.name);       // "Rex"               <- own property
console.log(rex.breed);      // "German Shepherd"   <- own property
console.log(rex.bark());     // "Rex barks! Woof!"  <- Dog.prototype
console.log(rex.breathe());  // "Rex breathes"      <- Animal.prototype
console.log(rex.type);       // "living"            <- Animal.prototype
console.log(rex.toString()); // "[object Object]"   <- Object.prototype
```

### ASCII Prototype Chain Diagram

```
rex (instance)
|  name: "Rex"
|  breed: "German Shepherd"
|  [[Prototype]]: ───────────────────────────────────────────────+
                                                                 |
                                                                 v
                                                        Dog.prototype
                                                        |  bark: [fn]
                                                        |  constructor: Dog
                                                        |  [[Prototype]]: ──────+
                                                                                |
                                                                                v
                                                                     Animal.prototype
                                                                     |  breathe: [fn]
                                                                     |  type: "living"
                                                                     |  [[Prototype]]: ──+
                                                                                        |
                                                                                        v
                                                                              Object.prototype
                                                                              |  toString: [fn]
                                                                              |  hasOwnProperty: [fn]
                                                                              |  [[Prototype]]: null
```

## 3.3 hasOwnProperty vs Inherited

```javascript
console.log(rex.hasOwnProperty("name"));     // true  <- own
console.log(rex.hasOwnProperty("breed"));    // true  <- own
console.log(rex.hasOwnProperty("bark"));     // false <- Dog.prototype
console.log(rex.hasOwnProperty("breathe"));  // false <- Animal.prototype
console.log(rex.hasOwnProperty("toString")); // false <- Object.prototype

// Object.keys — only OWN enumerable properties
console.log(Object.keys(rex)); // ["name", "breed"]

// for...in — own AND inherited enumerable
for (const key in rex) {
  if (rex.hasOwnProperty(key)) {
    console.log(`own: ${key} = ${rex[key]}`);
    // own: name = Rex
    // own: breed = German Shepherd
  }
}
```

## 3.4 Object.create() for Prototype-Based OOP

```javascript
// ── PROTOTYPE-BASED OOP PATTERN ───────────────────────────────
const Vehicle = {
  init(make, model, year) {
    this.make = make;
    this.model = model;
    this.year = year;
    return this;
  },
  describe() {
    return `${this.year} ${this.make} ${this.model}`;
  },
  start() {
    return `${this.model} engine starting...`;
  },
};

// Car inherits from Vehicle
const Car = Object.create(Vehicle);
Car.init = function (make, model, year, doors) {
  Vehicle.init.call(this, make, model, year);
  this.doors = doors;
  return this;
};
Car.honk = function () {
  return `${this.model} goes Beep Beep!`;
};

const myCar = Object.create(Car).init("Toyota", "Camry", 2023, 4);
console.log(myCar.describe()); // "2023 Toyota Camry"
console.log(myCar.honk());     // "Camry goes Beep Beep!"
console.log(myCar.start());    // "Camry engine starting..."
```

---

# 4. Classes (ES6)

## 4.1 What are Classes?

ES6 classes are **syntactic sugar** over JavaScript's prototype-based inheritance. Under the hood, they still use prototypes — classes just provide a cleaner, more familiar syntax.

> **Key Insight:** `class` is just a function! `typeof MyClass === "function"` is `true`.

```javascript
// ── CLASS SYNTAX ──────────────────────────────────────────────
class Person {
  // Constructor: runs when 'new Person()' is called
  constructor(name, age) {
    this.name = name;  // instance property
    this.age = age;    // instance property
  }

  // Instance method (stored on Person.prototype, NOT each instance)
  greet() {
    return `Hi, I'm ${this.name}, age ${this.age}`;
  }

  // Another instance method
  isAdult() {
    return this.age >= 18;
  }

  // Static method: called on the CLASS, not on instances
  static create(name, age) {
    return new Person(name, age);
  }

  // Static property
  static species = "Homo sapiens";

  // Getter
  get info() {
    return `${this.name} (${this.age})`;
  }

  // Setter
  set info(str) {
    const [name, age] = str.split(",");
    this.name = name.trim();
    this.age = parseInt(age);
  }
}

// ── USING THE CLASS ───────────────────────────────────────────
const p1 = new Person("Nihal", 22);
console.log(p1.greet());          // "Hi, I'm Nihal, age 22"
console.log(p1.isAdult());        // true
console.log(p1.info);             // "Nihal (22)"  <- getter
p1.info = "Rahul, 25";            // setter
console.log(p1.name);             // "Rahul"
console.log(p1.age);              // 25

// Static usage
const p2 = Person.create("Priya", 20); // static factory method
console.log(Person.species);           // "Homo sapiens"

// ── WHERE METHODS ARE STORED ──────────────────────────────────
console.log(p1.hasOwnProperty("greet")); // false <- on Person.prototype!
console.log(typeof Person.prototype.greet); // "function"
console.log(typeof Person);                 // "function" <- class IS a function!
```

## 4.2 Inheritance with extends and super

```javascript
// ── PARENT CLASS ──────────────────────────────────────────────
class Animal {
  constructor(name, sound) {
    this.name = name;
    this.sound = sound;
  }

  speak() {
    return `${this.name} says ${this.sound}`;
  }

  toString() {
    return `Animal: ${this.name}`;
  }
}

// ── CHILD CLASS ───────────────────────────────────────────────
class Dog extends Animal {
  constructor(name, breed) {
    // super() MUST be called before using 'this' in constructor!
    super(name, "Woof");  // calls Animal's constructor
    this.breed = breed;   // own property
  }

  // Override parent method
  speak() {
    // super.speak() calls Animal's speak method
    const parentSpeech = super.speak();
    return `${parentSpeech} (${this.breed})`;
  }

  fetch(item) {
    return `${this.name} fetches the ${item}!`;
  }
}

const buddy = new Dog("Buddy", "Labrador");
console.log(buddy.speak());       // "Buddy says Woof (Labrador)"
console.log(buddy.fetch("ball")); // "Buddy fetches the ball!"

// instanceof checks
console.log(buddy instanceof Dog);    // true
console.log(buddy instanceof Animal); // true (prototype chain!)

// ── MULTI-LEVEL INHERITANCE ───────────────────────────────────
class GuideDog extends Dog {
  constructor(name, breed, owner) {
    super(name, breed); // calls Dog constructor
    this.owner = owner;
  }

  guide() {
    return `${this.name} guides ${this.owner}`;
  }
}

const rex2 = new GuideDog("Rex", "German Shepherd", "Alice");
console.log(rex2.speak());  // inherited from Dog
console.log(rex2.guide());  // own method
```

## 4.3 Private Fields (#)

```javascript
// ── PRIVATE FIELDS (ES2022) ───────────────────────────────────
class BankAccount {
  // Private fields declared with # prefix
  #balance = 0;         // private — NOT accessible outside class!
  #owner;               // private field

  static #bankName = "NihalBank"; // private static field

  constructor(owner, initialBalance) {
    this.#owner = owner;
    this.#balance = initialBalance;
  }

  // Public method to interact with private field
  deposit(amount) {
    if (amount <= 0) throw new Error("Deposit must be positive");
    this.#balance += amount;
    return this;  // for chaining
  }

  withdraw(amount) {
    if (amount > this.#balance) throw new Error("Insufficient funds");
    this.#balance -= amount;
    return this;
  }

  get balance() {
    return this.#balance;  // controlled access via getter
  }

  static getBankName() {
    return BankAccount.#bankName;
  }

  // Private method
  #formatBalance() {
    return `Rs. ${this.#balance.toFixed(2)}`;
  }

  getStatement() {
    return `${this.#owner}: ${this.#formatBalance()}`;
  }
}

const account = new BankAccount("Nihal", 1000);
account.deposit(500).withdraw(200); // chaining!
console.log(account.balance);         // 1300
console.log(BankAccount.getBankName()); // "NihalBank"
console.log(account.getStatement());    // "Nihal: Rs. 1300.00"

// account.#balance  // SyntaxError: Private field not accessible!
// account.#owner    // SyntaxError!
```

## 4.4 Class Expressions

```javascript
// ── NAMED CLASS EXPRESSION ────────────────────────────────────
const MyClass = class NamedClass {
  greet() {
    return "Hello from NamedClass";
  }
};

const instance = new MyClass();
console.log(instance.greet()); // "Hello from NamedClass"
// new NamedClass() // ReferenceError: NamedClass is not accessible outside

// ── ANONYMOUS CLASS EXPRESSION ────────────────────────────────
const Greeter = class {
  greet() { return "Hello!"; }
};
```

## 4.5 Class vs Constructor Function Comparison

```
+──────────────────────────────────────────────────────────────────────+
|            Class vs Constructor Function                             |
+────────────────────────────┬─────────────────────────────────────────+
|   CONSTRUCTOR FUNCTION     |   CLASS (ES6)                           |
+────────────────────────────+─────────────────────────────────────────+
| function Person() {}       | class Person {}                         |
| Person.prototype.method    | method() {} inside class body           |
| Hoisted (but not init)     | NOT hoisted (temporal dead zone)        |
| Can call without new       | MUST use new (TypeError otherwise)      |
| No private fields          | Private fields with #                   |
| No extends keyword         | extends, super keywords                 |
| Messy inheritance setup    | Clean extends syntax                    |
| Same under the hood (proto)| Same under the hood (proto)             |
+────────────────────────────+─────────────────────────────────────────+

KEY DIFFERENCE: class body is always in strict mode!
```

---

# 5. Arrays in JavaScript

## 5.1 What is an Array?

An array is an **ordered list** of values. But in JavaScript, an array is actually a special kind of **object** where keys are numeric indices.

```javascript
// ── PROOF THAT ARRAY IS AN OBJECT ────────────────────────────
const arr = [10, 20, 30];
console.log(typeof arr);          // "object" <- NOT "array"!
console.log(Array.isArray(arr));  // true  <- use this to check!

// Under the hood, JavaScript treats this as:
// { 0: 10, 1: 20, 2: 30, length: 3 }

// ── ARRAY LITERAL ─────────────────────────────────────────────
const fruits = ["apple", "banana", "mango"];

// ── INDEX ACCESS (0-indexed) ──────────────────────────────────
console.log(fruits[0]);  // "apple"    <- first element
console.log(fruits[2]);  // "mango"    <- last element
console.log(fruits[10]); // undefined  <- out of bounds

// ── LENGTH PROPERTY ───────────────────────────────────────────
console.log(fruits.length); // 3
fruits[5] = "grape"; // setting index 5 on a length-3 array
console.log(fruits.length); // 6 <- length is max_index + 1
console.log(fruits[3]);     // undefined <- sparse slot!
console.log(fruits[4]);     // undefined <- sparse slot!
```

### Memory Layout

```
fruits array (special object):
+──────────────────────────────────────────────────────────────+
|  index:  0          1          2          length             |
|  value: "apple"  "banana"   "mango"        3                |
|         ─────────────────────────────────────────           |
|  memory: [ptr_A]  [ptr_B]   [ptr_C]                         |
|            |        |          |                             |
|          "apple" "banana"   "mango"   (strings on heap)     |
+──────────────────────────────────────────────────────────────+
```

## 5.2 Sparse Arrays

```javascript
// ── SPARSE ARRAYS ─────────────────────────────────────────────
// Arrays with "holes" — missing indices
const sparse = [1, , , 4]; // indices 1 and 2 are holes
console.log(sparse.length); // 4
console.log(sparse[1]);     // undefined
console.log(1 in sparse);   // false <- index 1 truly doesn't exist!

// Sparse arrays behave oddly with forEach — holes are SKIPPED!
sparse.forEach(v => console.log(v)); // 1   4 (skipped holes!)
console.log([...sparse]); // [1, undefined, undefined, 4] (spread fills holes)
```

---

# 6. All Array Methods

## 6.1 Mutating Methods (Modify Original Array)

### push() — Add to End

```javascript
const arr = [1, 2, 3];
const newLength = arr.push(4, 5);  // can push multiple elements
console.log(arr);       // [1, 2, 3, 4, 5]
console.log(newLength); // 5 <- returns NEW LENGTH
// Time complexity: O(1) amortized
```

### pop() — Remove from End

```javascript
const arr2 = [1, 2, 3];
const removed = arr2.pop(); // removes last element
console.log(removed); // 3 <- returns REMOVED ELEMENT
console.log(arr2);    // [1, 2]
// Time complexity: O(1)
```

### shift() — Remove from Front

```javascript
const arr3 = [1, 2, 3];
const first = arr3.shift(); // removes first element
console.log(first); // 1 <- returns REMOVED ELEMENT
console.log(arr3);  // [2, 3]
// Time complexity: O(n) <- must reindex all remaining elements!
```

### unshift() — Add to Front

```javascript
const arr4 = [3, 4, 5];
const newLen = arr4.unshift(1, 2); // add to beginning
console.log(arr4);   // [1, 2, 3, 4, 5]
console.log(newLen); // 5 <- returns new length
// Time complexity: O(n) <- must shift all existing elements!
```

### splice() — Add/Remove/Replace (Most Versatile Mutating Method)

```javascript
// splice(startIndex, deleteCount, ...itemsToInsert)
// Returns array of deleted elements
const fruits2 = ["apple", "banana", "mango", "grape"];

// ── Delete 2 elements starting at index 1 ────────────────────
const deleted = fruits2.splice(1, 2);
console.log(deleted); // ["banana", "mango"] <- returns deleted elements
console.log(fruits2); // ["apple", "grape"]  <- original modified!

// ── Insert without deleting ───────────────────────────────────
const nums = [1, 2, 5, 6];
nums.splice(2, 0, 3, 4); // at index 2, delete 0, insert 3 and 4
console.log(nums); // [1, 2, 3, 4, 5, 6]

// ── Replace elements ──────────────────────────────────────────
const colors = ["red", "blue", "green"];
colors.splice(1, 1, "yellow", "purple"); // replace 1 element at index 1
console.log(colors); // ["red", "yellow", "purple", "green"]

// ── Negative index (from end) ─────────────────────────────────
const letters = ["a", "b", "c", "d"];
letters.splice(-1, 1); // remove last element
console.log(letters); // ["a", "b", "c"]
```

### reverse() — Reverses Array In Place

```javascript
const arr5 = [1, 2, 3, 4, 5];
arr5.reverse();
console.log(arr5); // [5, 4, 3, 2, 1] <- ORIGINAL MUTATED!
// Non-mutating alternative (ES2023): toReversed()
```

### sort() — Sorts In Place (CRITICAL DEEP DIVE!)

```javascript
// ── DEFAULT SORT: CONVERTS TO STRINGS! ───────────────────────
const nums2 = [10, 9, 2, 21, 100];
nums2.sort();
console.log(nums2); // [10, 100, 2, 21, 9] <- WRONG! Sorted as strings!
// "10" < "100" < "2" < "21" < "9" (lexicographic comparison!)

// ── NUMERIC SORT with comparator ─────────────────────────────
const nums3 = [10, 9, 2, 21, 100];
nums3.sort((a, b) => a - b); // ascending
console.log(nums3); // [2, 9, 10, 21, 100] <- CORRECT!

// ── How the comparator works ──────────────────────────────────
// If (a - b) < 0  -> a comes BEFORE b  (a is smaller)
// If (a - b) > 0  -> a comes AFTER b   (b is smaller)
// If (a - b) === 0 -> order unchanged

// ── Descending sort ───────────────────────────────────────────
nums3.sort((a, b) => b - a); // descending: just swap a and b
console.log(nums3); // [100, 21, 10, 9, 2]

// ── Sort strings (works correctly with default sort) ──────────
const words = ["banana", "apple", "mango", "cherry"];
words.sort();
console.log(words); // ["apple", "banana", "cherry", "mango"]

// ── Sort objects by property ──────────────────────────────────
const people = [
  { name: "Charlie", age: 30 },
  { name: "Alice", age: 25 },
  { name: "Bob", age: 35 },
];
people.sort((a, b) => a.age - b.age); // sort by age ascending
console.log(people[0].name); // "Alice" (youngest)
console.log(people[2].name); // "Bob"   (oldest)

// ── STABILITY NOTE ────────────────────────────────────────────
// Modern JS engines (V8 v7.0+, SpiderMonkey) use STABLE sort (TimSort)
// Equal elements maintain their original relative order
// Old browsers used unstable sort — be aware for legacy code!
// Time complexity: O(n log n) — TimSort in modern V8

// ── Sort strings with locale support ─────────────────────────
const names = ["Ångström", "Banana", "apple", "cherry"];
names.sort((a, b) => a.localeCompare(b)); // locale-aware!
console.log(names); // handles accents, case correctly
```

### fill() — Fill Array with Value

```javascript
// fill(value, start, end) — end is exclusive
const arr6 = [1, 2, 3, 4, 5];
arr6.fill(0, 2, 4); // fill with 0, from index 2 to 4 (exclusive)
console.log(arr6); // [1, 2, 0, 0, 5]

// ── Create array of zeros ─────────────────────────────────────
const zeros = new Array(5).fill(0);
console.log(zeros); // [0, 0, 0, 0, 0]

// ── GOTCHA with objects: all elements share same reference! ───
const matrix = new Array(3).fill([]); // ALL rows share SAME array!
matrix[0].push(1); // modifies all rows!
console.log(matrix); // [[1],[1],[1]] <- BUG!

// FIX: use Array.from() with mapping function
const matrix2 = Array.from({ length: 3 }, () => []); // independent rows
matrix2[0].push(1);
console.log(matrix2); // [[1],[],[]] <- correct!
```

### copyWithin() — Copy Part of Array Within Itself

```javascript
// copyWithin(target, start, end) — copies elements within the array
const arr7 = [1, 2, 3, 4, 5];
arr7.copyWithin(0, 3); // copy from index 3 to end, paste at index 0
console.log(arr7); // [4, 5, 3, 4, 5]
// Rarely used but appears in typed array performance code
```

---

## 6.2 Non-Mutating Methods

### slice() — Extract Portion (Does NOT Mutate)

```javascript
// slice(start, end) — end is exclusive
const fruits3 = ["apple", "banana", "mango", "grape", "kiwi"];

const chunk = fruits3.slice(1, 4); // indices 1, 2, 3
console.log(chunk);    // ["banana", "mango", "grape"]
console.log(fruits3);  // unchanged! <- NON-MUTATING

const fromEnd = fruits3.slice(-2); // last 2 elements
console.log(fromEnd);  // ["grape", "kiwi"]

const copy = fruits3.slice(); // entire array shallow copy
console.log(copy === fruits3); // false <- new array!
```

### concat() — Merge Arrays (Does NOT Mutate)

```javascript
const a = [1, 2, 3];
const b = [4, 5, 6];
const c = a.concat(b);
console.log(c); // [1, 2, 3, 4, 5, 6]
console.log(a); // [1, 2, 3] <- unchanged!

// Concat multiple arrays and individual values
const merged = [1].concat([2, 3], [4, 5], 6);
console.log(merged); // [1, 2, 3, 4, 5, 6]
```

### join() — Array to String

```javascript
const words2 = ["Hello", "World", "JavaScript"];
console.log(words2.join(" "));   // "Hello World JavaScript"
console.log(words2.join("-"));   // "Hello-World-JavaScript"
console.log(words2.join(""));    // "HelloWorldJavaScript"
console.log(words2.join());      // "Hello,World,JavaScript" <- default: comma

// Practical use: build CSV row
const row = ["Nihal", "22", "Delhi"];
console.log(row.join(",")); // "Nihal,22,Delhi"
```

### indexOf() / lastIndexOf() / includes()

```javascript
const arr8 = [1, 2, 3, 2, 4, 2];

console.log(arr8.indexOf(2));     // 1  <- FIRST occurrence index
console.log(arr8.lastIndexOf(2)); // 5  <- LAST occurrence index
console.log(arr8.indexOf(99));    // -1 <- not found returns -1

console.log(arr8.includes(3));    // true  <- boolean check
console.log(arr8.includes(99));   // false

// includes can handle NaN (indexOf cannot!)
const special = [1, NaN, 3];
console.log(special.indexOf(NaN));  // -1   <- can't find NaN! (uses ===)
console.log(special.includes(NaN)); // true <- works correctly!
```

---

## 6.3 Functional Methods (Critical for React!)

### filter() — Create New Array of Matching Elements

```javascript
// filter(callback) — callback should return true/false
// Non-mutating. Returns NEW array. Keeps elements where callback is truthy.
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evens = numbers.filter(num => num % 2 === 0);
console.log(evens);   // [2, 4, 6, 8, 10]
console.log(numbers); // [1..10] <- unchanged!

// ── Filter objects ────────────────────────────────────────────
const users = [
  { name: "Alice", active: true },
  { name: "Bob", active: false },
  { name: "Charlie", active: true },
];
const activeUsers = users.filter(user => user.active);
console.log(activeUsers); // [{Alice,true},{Charlie,true}]

// ── Remove element by index (common React pattern!) ───────────
const items = ["a", "b", "c", "d"];
const removeIndex = 2;
const result = items.filter((_, index) => index !== removeIndex);
console.log(result); // ["a", "b", "d"]

// ── Remove falsy values ───────────────────────────────────────
const mixed = [0, 1, "", "hello", null, undefined, false, true, NaN];
const truthy = mixed.filter(Boolean);
console.log(truthy); // [1, "hello", true]
// Time complexity: O(n)
```

### map() — Transform Each Element

```javascript
// map(callback) — returns NEW array of same length
// Non-mutating. FUNDAMENTAL in React for rendering lists!
const nums4 = [1, 2, 3, 4, 5];

const doubled = nums4.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]
console.log(nums4);   // [1, 2, 3, 4, 5] <- unchanged!

// ── Map with objects (React-style) ────────────────────────────
const products = [
  { id: 1, name: "Laptop", price: 50000 },
  { id: 2, name: "Phone", price: 20000 },
];

const productCards = products.map(product => ({
  // NOTE: Wrapping in () because {} would be treated as function body!
  ...product,                             // spread all properties
  discountedPrice: product.price * 0.9,   // add new property
  label: `${product.name} - Rs.${product.price}`,
}));

console.log(productCards[0]);
// { id: 1, name: "Laptop", price: 50000, discountedPrice: 45000, label: "..." }

// ── Common map patterns ───────────────────────────────────────
const names = ["alice", "bob", "charlie"];
const capitalized = names.map(n => n[0].toUpperCase() + n.slice(1));
console.log(capitalized); // ["Alice", "Bob", "Charlie"]

// map callback receives: (currentValue, index, array)
const withIndex = names.map((name, i) => `${i + 1}. ${name}`);
console.log(withIndex); // ["1. alice", "2. bob", "3. charlie"]
// Time complexity: O(n)
```

### reduce() — Accumulate to Single Value

```javascript
// reduce(callback, initialValue)
// callback receives (accumulator, currentValue, currentIndex, array)
const nums5 = [1, 2, 3, 4, 5];

// Sum all numbers
const sum = nums5.reduce((acc, curr) => acc + curr, 0);
console.log(sum); // 15

// ── Step-by-step trace ────────────────────────────────────────
// Initial: acc = 0
// Step 1:  acc = 0 + 1  = 1   (curr = 1)
// Step 2:  acc = 1 + 2  = 3   (curr = 2)
// Step 3:  acc = 3 + 3  = 6   (curr = 3)
// Step 4:  acc = 6 + 4  = 10  (curr = 4)
// Step 5:  acc = 10 + 5 = 15  (curr = 5) <- final result

// ── Max value ─────────────────────────────────────────────────
const max = nums5.reduce((acc, curr) => Math.max(acc, curr), -Infinity);
console.log(max); // 5

// ── Flatten array ─────────────────────────────────────────────
const nested = [[1, 2], [3, 4], [5]];
const flat = nested.reduce((acc, curr) => acc.concat(curr), []);
console.log(flat); // [1, 2, 3, 4, 5]

// ── Count occurrences (frequency map) ────────────────────────
const fruits4 = ["apple","banana","apple","mango","banana","apple"];
const count = fruits4.reduce((acc, fruit) => {
  acc[fruit] = (acc[fruit] || 0) + 1; // increment or initialize to 1
  return acc;
}, {}); // initial value is empty object
console.log(count); // { apple: 3, banana: 2, mango: 1 }

// ── Group objects by property ─────────────────────────────────
const people2 = [
  { name: "Alice", dept: "Engineering" },
  { name: "Bob", dept: "Marketing" },
  { name: "Charlie", dept: "Engineering" },
];
const byDept = people2.reduce((acc, person) => {
  const dept = person.dept;
  if (!acc[dept]) acc[dept] = [];   // initialize group if not exists
  acc[dept].push(person.name);       // add to group
  return acc;
}, {});
console.log(byDept);
// { Engineering: ["Alice", "Charlie"], Marketing: ["Bob"] }

// ── reduceRight: same as reduce, but from RIGHT to LEFT ───────
const result2 = [1, 2, 3, 4].reduceRight((acc, n) => acc - n, 0);
// 0 - 4 - 3 - 2 - 1 = -10
console.log(result2); // -10
// Time complexity: O(n)
```

### forEach() — Iterate (No Return Value)

```javascript
const nums6 = [1, 2, 3];

// forEach — purely for side effects, returns undefined
nums6.forEach((num, index) => {
  console.log(`Index ${index}: ${num}`);
  // Index 0: 1
  // Index 1: 2
  // Index 2: 3
});

// CANNOT break out of forEach!
// Use for...of or for loop if you need to break early

// forEach returns undefined — CANNOT chain!
const wrongResult = nums6.forEach(n => n * 2);
console.log(wrongResult); // undefined <- NOT [2,4,6]! Use map() for that.
```

### flat() and flatMap()

```javascript
// flat(depth) — flattens nested arrays
const nested2 = [1, [2, 3], [4, [5, 6]]];
console.log(nested2.flat());         // [1, 2, 3, 4, [5, 6]] <- 1 level
console.log(nested2.flat(2));        // [1, 2, 3, 4, 5, 6]   <- 2 levels
console.log(nested2.flat(Infinity)); // [1, 2, 3, 4, 5, 6]   <- fully flat

// ── flatMap() = map() + flat(1) combined ──────────────────────
// More efficient than calling them separately!
const sentences = ["Hello World", "foo bar"];
const words3 = sentences.flatMap(sentence => sentence.split(" "));
console.log(words3); // ["Hello", "World", "foo", "bar"]

// Real use: remove elements while transforming
const data = [1, -2, 3, -4, 5];
const positiveDoubled = data.flatMap(n => n > 0 ? [n * 2] : []);
console.log(positiveDoubled); // [2, 6, 10] <- negatives removed!
```

---

## 6.4 Search Methods

```javascript
const users2 = [
  { id: 1, name: "Alice", age: 25 },
  { id: 2, name: "Bob", age: 30 },
  { id: 3, name: "Charlie", age: 25 },
];

// find() — returns FIRST matching element (or undefined)
const found = users2.find(u => u.age === 25);
console.log(found); // { id: 1, name: "Alice", age: 25 } <- FIRST match

// findIndex() — returns INDEX of first match (or -1)
const foundIdx = users2.findIndex(u => u.name === "Bob");
console.log(foundIdx); // 1

// findLast() — returns LAST matching element (ES2023)
const last = users2.findLast(u => u.age === 25);
console.log(last); // { id: 3, name: "Charlie", age: 25 } <- LAST match

// findLastIndex() — returns INDEX of last match (ES2023)
const lastIdx = users2.findLastIndex(u => u.age === 25);
console.log(lastIdx); // 2

// every() — ALL elements match? (short-circuits on false!)
const allAdults = users2.every(u => u.age >= 18);
console.log(allAdults); // true

const allOver30 = users2.every(u => u.age > 30);
console.log(allOver30); // false <- stops checking at first failure

// some() — AT LEAST ONE matches? (short-circuits on true!)
const hasSecretary = users2.some(u => u.name === "Bob");
console.log(hasSecretary); // true
```

---

## 6.5 Static Methods

```javascript
// ── Array.from() — create array from iterable/array-like ──────
const str = "hello";
const chars = Array.from(str); // string -> array
console.log(chars); // ["h", "e", "l", "l", "o"]

// Array.from with NodeList (DOM)
// const nodeList = document.querySelectorAll("div"); // array-like
// const divArray = Array.from(nodeList); // now it's a real array!

// Array.from with mapping function (2nd argument!)
const squares = Array.from({ length: 5 }, (_, i) => i ** 2);
console.log(squares); // [0, 1, 4, 9, 16]

const range = Array.from({ length: 10 }, (_, i) => i + 1);
console.log(range); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

// ── Array.of() — create array from arguments ──────────────────
console.log(Array.of(1, 2, 3));   // [1, 2, 3]
console.log(new Array(3));         // [,,] <- 3 empty slots (confusing!)
console.log(Array.of(3));          // [3]  <- just the value 3, not 3 slots!

// ── Array.isArray() ───────────────────────────────────────────
console.log(Array.isArray([1, 2, 3]));   // true
console.log(Array.isArray("hello"));     // false
console.log(Array.isArray({ length: 3 })); // false <- NOT an array!
```

---

## 6.6 Modern Methods

```javascript
// ── at() — index with negative support ───────────────────────
const arr9 = [10, 20, 30, 40, 50];
console.log(arr9.at(0));   // 10  <- first element
console.log(arr9.at(-1));  // 50  <- last element (no arr[-1] in JS!)
console.log(arr9.at(-2));  // 40  <- second to last

// ── entries() — [index, value] pairs iterator ─────────────────
for (const [index, value] of arr9.entries()) {
  console.log(`${index}: ${value}`);
  // 0: 10, 1: 20, 2: 30, 3: 40, 4: 50
}

// ── keys() — indices iterator ─────────────────────────────────
console.log([...arr9.keys()]);   // [0, 1, 2, 3, 4]

// ── values() — values iterator ────────────────────────────────
console.log([...arr9.values()]); // [10, 20, 30, 40, 50]
```

---

## 6.7 ES2023 Non-Mutating Counterparts

These are critical for React development where state must not be mutated!

```javascript
const original = [3, 1, 4, 1, 5, 9, 2, 6];

// ── toSorted() — sort without mutating ───────────────────────
const sorted = original.toSorted((a, b) => a - b);
console.log(sorted);    // [1, 1, 2, 3, 4, 5, 6, 9]
console.log(original);  // [3, 1, 4, 1, 5, 9, 2, 6] <- unchanged!

// ── toReversed() — reverse without mutating ───────────────────
const reversed = original.toReversed();
console.log(reversed);  // [6, 2, 9, 5, 1, 4, 1, 3]
console.log(original);  // unchanged!

// ── toSpliced() — splice without mutating ─────────────────────
// toSpliced(start, deleteCount, ...items)
const spliced = original.toSpliced(2, 1, 99, 100);
console.log(spliced);   // [3, 1, 99, 100, 1, 5, 9, 2, 6]
console.log(original);  // unchanged!

// ── with() — update specific index without mutating ───────────
const withNew = original.with(0, 999); // set index 0 to 999
console.log(withNew);   // [999, 1, 4, 1, 5, 9, 2, 6]
console.log(original);  // unchanged!

// ── WHY THESE MATTER IN REACT: ────────────────────────────────
// In React, NEVER mutate state directly!
// setItems(items.toSorted(...)) creates new array -> triggers re-render
// setItems([...items].sort(...)) also works but less clean
```

---

# 7. Destructuring

## 7.1 Array Destructuring

```javascript
// ── BASIC ARRAY DESTRUCTURING ─────────────────────────────────
const rgb = [255, 128, 0];

// Old way:
const red = rgb[0];
const green = rgb[1];
const blue = rgb[2];

// Destructuring (elegant!):
const [r, g, b] = rgb;
console.log(r, g, b); // 255 128 0

// ── SKIP ELEMENTS with commas ─────────────────────────────────
const [first, , third] = [10, 20, 30]; // skip index 1
console.log(first, third); // 10 30

// ── DEFAULT VALUES ────────────────────────────────────────────
const [x = 0, y = 0, z = 0] = [5, 10]; // z is undefined, uses default
console.log(x, y, z); // 5 10 0

// ── REST in array destructuring ───────────────────────────────
const [head, ...tail] = [1, 2, 3, 4, 5];
console.log(head); // 1
console.log(tail); // [2, 3, 4, 5] <- REST must be last!

// ── SWAP VARIABLES (elegant trick!) ───────────────────────────
let a = 1, bVar = 2;
[a, bVar] = [bVar, a]; // swap without temp variable!
console.log(a, bVar); // 2 1

// ── NESTED ARRAY DESTRUCTURING ────────────────────────────────
const matrix3 = [[1, 2], [3, 4]];
const [[a1, a2], [b1, b2]] = matrix3;
console.log(a1, a2, b1, b2); // 1 2 3 4

// ── FROM FUNCTION RETURN ──────────────────────────────────────
function getMinMax(arr) {
  return [Math.min(...arr), Math.max(...arr)];
}
const [min, max] = getMinMax([3, 1, 4, 1, 5, 9, 2, 6]);
console.log(min, max); // 1 9

// ── useState style (React!) ───────────────────────────────────
// const [count, setCount] = useState(0);
// count is the value, setCount is the setter function
```

## 7.2 Object Destructuring

```javascript
// ── BASIC OBJECT DESTRUCTURING ────────────────────────────────
const person3 = {
  name: "Nihal Kumar",
  age: 22,
  city: "Delhi",
  role: "Developer",
};

// Old way:
const name1 = person3.name;
const age1 = person3.age;

// Destructuring:
const { name, age } = person3;
console.log(name, age); // "Nihal Kumar" 22

// ── RENAMING (aliasing) ───────────────────────────────────────
// Extract 'name' but store in variable named 'fullName'
const { name: fullName, age: years } = person3;
console.log(fullName); // "Nihal Kumar"
console.log(years);    // 22

// ── DEFAULT VALUES ────────────────────────────────────────────
const { city, country = "India" } = person3; // country not in object
console.log(city);    // "Delhi"
console.log(country); // "India" <- default used!

// ── RENAME + DEFAULT combined ─────────────────────────────────
const { role: userRole = "Guest" } = person3;
console.log(userRole); // "Developer" (exists, so no default)

// ── REST in object destructuring ──────────────────────────────
const { name: n, ...rest } = person3;
console.log(n);    // "Nihal Kumar"
console.log(rest); // { age: 22, city: "Delhi", role: "Developer" }

// ── NESTED OBJECT DESTRUCTURING ───────────────────────────────
const user3 = {
  name: "Alice",
  address: {
    city: "Mumbai",
    pin: { code: 400001 },
  },
};

const { address: { city: userCity, pin: { code } } } = user3;
console.log(userCity); // "Mumbai"
console.log(code);     // 400001

// ── IN FUNCTION PARAMETERS (extremely common in React!) ────────
function greetUser({ name, age, role = "Member" }) {
  return `Hello ${name}! Age: ${age}. Role: ${role}`;
}

console.log(greetUser(person3));
// "Hello Nihal Kumar! Age: 22. Role: Developer"

// ── React component example ───────────────────────────────────
// function UserCard({ name, age, city, onClick }) {
//   return (
//     <div onClick={onClick}>
//       {name} - {age} - {city}
//     </div>
//   );
// }
```

---

# 8. Spread Operator (...)

```javascript
// ── SPREAD IN ARRAYS ──────────────────────────────────────────
const arr10 = [1, 2, 3];
const arr11 = [4, 5, 6];

// Merge arrays (creates NEW array)
const merged2 = [...arr10, ...arr11];
console.log(merged2); // [1, 2, 3, 4, 5, 6]

// Clone array (shallow)
const clone = [...arr10];
clone.push(99);
console.log(arr10);  // [1, 2, 3] <- unchanged!
console.log(clone);  // [1, 2, 3, 99]

// Insert in middle
const withMiddle = [...arr10, 99, ...arr11];
console.log(withMiddle); // [1, 2, 3, 99, 4, 5, 6]

// ── SPREAD IN FUNCTION CALLS ──────────────────────────────────
const nums7 = [3, 1, 4, 1, 5, 9];
console.log(Math.max(...nums7)); // 9
// Equivalent to: Math.max(3, 1, 4, 1, 5, 9)

function add(a, b, c) { return a + b + c; }
const args = [1, 2, 3];
console.log(add(...args)); // 6

// ── SPREAD IN OBJECTS ─────────────────────────────────────────
const defaults2 = { color: "blue", size: "M", font: "Arial" };
const custom = { size: "L", weight: "bold" };

// Merge objects (RIGHTMOST wins on conflict)
const merged3 = { ...defaults2, ...custom };
console.log(merged3);
// { color: "blue", size: "L", font: "Arial", weight: "bold" }
// size: "L" <- custom overrides default!

// ── CLONE OBJECT (shallow) ────────────────────────────────────
const original4 = { a: 1, b: { c: 2 } };
const cloned = { ...original4 };
cloned.a = 99;        // OK, primitive — independent
cloned.b.c = 99;      // SHARED REFERENCE! modifies original!
console.log(original4.a);   // 1  <- unaffected
console.log(original4.b.c); // 99 <- AFFECTED! (shallow clone limitation)

// ── SPREAD FROM STRING ────────────────────────────────────────
const chars2 = [..."hello"];
console.log(chars2); // ["h", "e", "l", "l", "o"]

// ── SPREAD FROM SET (for unique values) ───────────────────────
const unique = [...new Set([1, 1, 2, 2, 3])];
console.log(unique); // [1, 2, 3]

// ── REACT PATTERNS ────────────────────────────────────────────
// Update object in state without mutation:
// setState(prev => ({ ...prev, name: "NewName" }))

// Add item to array state:
// setItems(prev => [...prev, newItem])

// Remove item from array state:
// setItems(prev => prev.filter(item => item.id !== removeId))
```

---

# 9. Rest Operator (...)

```javascript
// ── REST IN FUNCTION PARAMETERS ───────────────────────────────
// Rest collects REMAINING arguments into a REAL array
function sum(...numbers) {
  // 'numbers' is a real array with all array methods!
  return numbers.reduce((acc, n) => acc + n, 0);
}
console.log(sum(1, 2, 3));        // 6
console.log(sum(1, 2, 3, 4, 5));  // 15
console.log(sum());               // 0 (empty array, reduce returns initial)

// ── Mixing normal params with rest ────────────────────────────
function logAll(first, second, ...rest) {
  console.log("First:", first);
  console.log("Second:", second);
  console.log("Rest:", rest);
}
logAll("a", "b", "c", "d", "e");
// First: a
// Second: b
// Rest: ["c", "d", "e"]

// Rest must be LAST parameter!
// function bad(a, ...rest, b) <- SyntaxError!

// ── REST vs 'arguments' object ────────────────────────────────
function oldWay() {
  // 'arguments' is array-LIKE, NOT a real array
  // No: arguments.filter(), arguments.map(), etc.
  const arr = Array.from(arguments); // must convert
  return arr.filter(n => n > 2);
}

function newWay(...args) {
  // 'args' is a REAL array — all array methods available!
  return args.filter(n => n > 2);
}
console.log(newWay(1, 2, 3, 4, 5)); // [3, 4, 5]

// NOTE: Arrow functions don't have 'arguments' — use rest instead!

// ── REST in Array Destructuring ───────────────────────────────
const [first2, second2, ...remaining] = [10, 20, 30, 40, 50];
console.log(first2);     // 10
console.log(second2);    // 20
console.log(remaining);  // [30, 40, 50]

// ── REST in Object Destructuring ─────────────────────────────
const { x: x2, y: y2, ...others } = { x: 1, y: 2, z: 3, w: 4 };
console.log(x2);      // 1
console.log(y2);      // 2
console.log(others);  // { z: 3, w: 4 } <- remaining properties
```

### Spread vs Rest — Clear Distinction

```
+──────────────────────────────────────────────────────────────────────+
|                     SPREAD vs REST                                   |
+──────────────────────────────┬───────────────────────────────────────+
|         SPREAD               |           REST                        |
+──────────────────────────────+───────────────────────────────────────+
| EXPANDS array/object         | COLLECTS values into array            |
| Used in: function CALLS      | Used in: function PARAMETERS          |
|          array literals      |          destructuring                |
|          object literals     |                                       |
| Math.max(...[1,2,3])         | function f(...args) {}               |
| [...arr1, ...arr2]           | const [a, ...rest] = arr              |
| {...obj1, ...obj2}           | const {a, ...rest} = obj              |
| "Spreads out" ---->          | "Gathers in" <----                    |
| Context: VALUE position      | Context: VARIABLE position            |
+──────────────────────────────+───────────────────────────────────────+
```

---

# 10. Strings & String Methods

## 10.1 String Fundamentals

```javascript
// ── STRING PRIMITIVE vs STRING OBJECT ─────────────────────────
const str1 = "hello";           // primitive <- prefer this!
const str2 = new String("hello"); // object   <- avoid!

console.log(typeof str1); // "string"
console.log(typeof str2); // "object"

// When you call methods on a primitive string, JS temporarily
// wraps it in a String object (AUTOBOXING), then discards the wrapper:
str1.toUpperCase(); // internally: new String("hello").toUpperCase()

// ── IMMUTABILITY ──────────────────────────────────────────────
let s = "hello";
s[0] = "H"; // silently fails! Strings are immutable!
console.log(s); // "hello" <- unchanged!
// String methods ALWAYS return NEW strings, never modify in place.

// ── LENGTH ────────────────────────────────────────────────────
console.log("hello".length);    // 5
console.log("".length);         // 0
console.log("hi there".length); // 8 <- space counts!
console.log("".length === 0);   // true <- use for empty string check

// ── TEMPLATE LITERALS ─────────────────────────────────────────
const name3 = "Nihal";
const age3 = 22;
const greeting = `Hello, ${name3}! You are ${age3} years old.`;
console.log(greeting); // "Hello, Nihal! You are 22 years old."

// Multi-line string (backtick magic!)
const multiLine = `Line 1
Line 2
Line 3`;

// Expressions in template literals
console.log(`2 + 2 = ${2 + 2}`);                          // "2 + 2 = 4"
console.log(`${age3 >= 18 ? "adult" : "minor"}`);          // "adult"
console.log(`List: ${[1,2,3].map(n => n*2).join(", ")}`);  // "List: 2, 4, 6"
```

## 10.2 Character Access

```javascript
const str3 = "JavaScript";
//            0123456789

// charAt(index) — character at given index
console.log(str3.charAt(0));    // "J"
console.log(str3.charAt(100));  // "" <- empty string for out-of-range

// Bracket notation
console.log(str3[0]);    // "J"
console.log(str3[100]);  // undefined <- different from charAt!

// at() — supports negative indices! (modern)
console.log(str3.at(0));   // "J"  <- first
console.log(str3.at(-1));  // "t"  <- last
console.log(str3.at(-2));  // "p"  <- second to last

// charCodeAt(index) — UTF-16 code of character
console.log("A".charCodeAt(0)); // 65
console.log("a".charCodeAt(0)); // 97
console.log("0".charCodeAt(0)); // 48

// String.fromCharCode(code) — code -> character
console.log(String.fromCharCode(65));      // "A"
console.log(String.fromCharCode(74, 83));  // "JS"
```

## 10.3 Searching in Strings

```javascript
const text = "Hello World, Hello JavaScript!";
//            0123456789012345678901234567890

// indexOf(searchStr, fromIndex) — first occurrence, returns index or -1
console.log(text.indexOf("Hello"));     // 0   <- found at index 0
console.log(text.indexOf("Hello", 5));  // 13  <- search from index 5
console.log(text.indexOf("Python"));    // -1  <- not found

// lastIndexOf(searchStr) — last occurrence
console.log(text.lastIndexOf("Hello")); // 13 <- last "Hello"

// includes(searchStr, position) — boolean check (ES6)
console.log(text.includes("World"));    // true
console.log(text.includes("React"));    // false

// startsWith(str, position) — does it begin with?
console.log(text.startsWith("Hello"));     // true
console.log(text.startsWith("World"));     // false
console.log(text.startsWith("World", 6));  // true <- from position 6

// endsWith(str, length) — does it end with?
console.log(text.endsWith("!"));           // true
console.log(text.endsWith("World"));       // false
console.log(text.endsWith("World", 11));   // true <- check first 11 chars

// search(regex) — like indexOf but for regex, returns index
console.log("hello world".search(/world/)); // 6
console.log("hello world".search(/xyz/));   // -1
```

## 10.4 Extracting Substrings — slice vs substring

```javascript
const str4 = "Hello, World!";
//            0123456789012

// ── slice(start, end) — end is EXCLUSIVE ──────────────────────
console.log(str4.slice(0, 5));    // "Hello"
console.log(str4.slice(7));       // "World!" <- from 7 to end
console.log(str4.slice(-6));      // "World!" <- last 6 chars (negative!)
console.log(str4.slice(-6, -1)); // "World"  <- negative end too!
console.log(str4.slice(5, 2));    // ""       <- start > end -> empty!

// ── substring(start, end) — KEY DIFFERENCES from slice ────────
console.log(str4.substring(0, 5)); // "Hello"   <- same
console.log(str4.substring(7));    // "World!"  <- same

// DIFFERENCE 1: Negative values treated as 0 (slice uses from-end)
console.log(str4.substring(-6));   // "Hello, World!" <- -6 treated as 0!
console.log(str4.slice(-6));       // "World!"        <- last 6 chars!

// DIFFERENCE 2: If start > end, substring SWAPS them (slice returns "")
console.log(str4.substring(5, 2)); // "llo" <- swapped to substring(2,5)!
console.log(str4.slice(5, 2));     // ""    <- returns empty string

// ── RECOMMENDATION: Use slice() — more predictable behavior! ──
```

## 10.5 Case Conversion

```javascript
const mixed = "Hello World";
console.log(mixed.toLowerCase()); // "hello world"
console.log(mixed.toUpperCase()); // "HELLO WORLD"
console.log(mixed);               // "Hello World" <- unchanged! immutable

// Capitalize first letter
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
console.log(capitalize("hELLO")); // "Hello"

// Normalize user input
const userInput = "  NIHAL@EXAMPLE.COM  ";
const email = userInput.trim().toLowerCase();
console.log(email); // "nihal@example.com"
```

## 10.6 Trimming & Padding

```javascript
// ── TRIM ──────────────────────────────────────────────────────
const messy = "   hello world   ";
console.log(messy.trim());       // "hello world"         <- both sides
console.log(messy.trimStart());  // "hello world   "      <- only left
console.log(messy.trimEnd());    // "   hello world"      <- only right

// ── PADSTART / PADEND ─────────────────────────────────────────
// padStart(targetLength, padString)
console.log("5".padStart(3, "0"));     // "005" <- common for number formatting
console.log("5".padStart(3));          // "  5" <- default pad: space
console.log("hello".padStart(3));      // "hello" <- already >= length, no padding
console.log("hi".padEnd(5, "*"));      // "hi***"

// Use case: format time display
function formatTime(h, m, s) {
  return [h, m, s].map(n => String(n).padStart(2, "0")).join(":");
}
console.log(formatTime(9, 5, 3));   // "09:05:03"
console.log(formatTime(14, 30, 0)); // "14:30:00"
```

## 10.7 Split, Replace, Repeat

```javascript
// ── SPLIT ─────────────────────────────────────────────────────
const csv = "apple,banana,mango,grape";
console.log(csv.split(","));      // ["apple","banana","mango","grape"]
console.log(csv.split(",", 2));   // ["apple","banana"] <- limit to 2!
console.log("hello".split(""));   // ["h","e","l","l","o"] <- each char
console.log("hello".split());     // ["hello"] <- no separator: full string in array!

// ── REPLACE ───────────────────────────────────────────────────
const sentence = "The cat sat on the cat mat";
console.log(sentence.replace("cat", "dog")); 
// "The dog sat on the cat mat" <- only FIRST occurrence!

// Use regex with /g for global replace:
console.log(sentence.replace(/cat/g, "dog"));
// "The dog sat on the dog mat" <- ALL occurrences

// ── REPLACEALL (ES2021) ───────────────────────────────────────
console.log(sentence.replaceAll("cat", "dog"));
// "The dog sat on the dog mat" <- all occurrences, no regex needed!

// Replace with function (dynamic replacement!)
const result3 = "hello world".replace(/(\w+)/g, word => word.toUpperCase());
console.log(result3); // "HELLO WORLD"

// ── REPEAT ────────────────────────────────────────────────────
console.log("ha".repeat(3));   // "hahaha"
console.log("-".repeat(20));   // "────────────────────"
console.log("abc".repeat(0));  // "" <- 0 times = empty string
```

## 10.8 Pattern Matching

```javascript
// ── MATCH ─────────────────────────────────────────────────────
const text2 = "I have 3 cats and 5 dogs";

// Without /g flag — returns first match with full details
const firstMatch = text2.match(/\d+/);
console.log(firstMatch[0]);    // "3"
console.log(firstMatch.index); // 7 <- position of match

// With /g flag — returns all matches as plain array (no details)
const allNumbers = text2.match(/\d+/g);
console.log(allNumbers); // ["3", "5"]

// ── MATCHALL ──────────────────────────────────────────────────
// Returns iterator of ALL matches WITH details (requires /g flag!)
const text3 = "foo123bar456baz789";
const matches = [...text3.matchAll(/([a-z]+)(\d+)/g)];
for (const match of matches) {
  console.log(`Full: ${match[0]}, Letters: ${match[1]}, Digits: ${match[2]}`);
}
// Full: foo123, Letters: foo, Digits: 123
// Full: bar456, Letters: bar, Digits: 456
// Full: baz789, Letters: baz, Digits: 789
```

## 10.9 Tagged Template Literals

```javascript
// ── TAGGED TEMPLATES ──────────────────────────────────────────
// A tag is a function that processes a template literal
// The tag function receives: (strings, ...values)

function highlight(strings, ...values) {
  // strings: array of static string parts
  // values: the interpolated expressions
  
  let result = "";
  strings.forEach((str, i) => {
    result += str;
    if (values[i] !== undefined) {
      result += `<strong>${values[i]}</strong>`;
    }
  });
  return result;
}

const name4 = "Nihal";
const score = 95;
const html = highlight`Hello ${name4}! Your score is ${score}%!`;
console.log(html);
// "Hello <strong>Nihal</strong>! Your score is <strong>95</strong>%!"

// ── Real-world: SQL sanitization ──────────────────────────────
function safeSQL(strings, ...values) {
  const sanitized = values.map(v => String(v).replace(/'/g, "''"));
  return strings.reduce((acc, str, i) => acc + str + (sanitized[i] || ""), "");
}

const username = "O'Brien"; // dangerous SQL injection attempt!
const query = safeSQL`SELECT * FROM users WHERE name = '${username}'`;
console.log(query); // SELECT * FROM users WHERE name = 'O''Brien' <- safe!

// ── String.raw — raw string (no escape processing) ────────────
const path = String.raw`C:\Users\Nihal\Documents`;
console.log(path); // "C:\Users\Nihal\Documents" <- backslashes not escaped
```

---

# 11. Math Object

```javascript
// ── MATH CONSTANTS ────────────────────────────────────────────
console.log(Math.PI);      // 3.141592653589793
console.log(Math.E);       // 2.718281828459045
console.log(Math.SQRT2);   // 1.4142135623730951
console.log(Math.LN2);     // 0.6931471805599453
console.log(Math.LN10);    // 2.302585092994046

// ── ROUNDING ──────────────────────────────────────────────────
console.log(Math.round(4.5));   // 5   <- rounds to nearest (0.5 goes up)
console.log(Math.round(4.4));   // 4
console.log(Math.round(-4.5));  // -4  <- rounds toward +infinity

console.log(Math.floor(4.9));   // 4   <- always rounds DOWN
console.log(Math.floor(-4.1));  // -5  <- negative: more negative!

console.log(Math.ceil(4.1));    // 5   <- always rounds UP
console.log(Math.ceil(-4.9));   // -4  <- negative: less negative!

console.log(Math.trunc(4.9));   // 4   <- removes decimal part
console.log(Math.trunc(-4.9));  // -4  <- toward zero (unlike floor!)

// ── Difference: floor vs trunc for negatives ──────────────────
// Math.floor(-4.1) = -5  (goes down to more negative)
// Math.trunc(-4.1) = -4  (removes decimal, toward zero)

// ── ABSOLUTE VALUE, SIGN ──────────────────────────────────────
console.log(Math.abs(-5));   // 5
console.log(Math.abs(5));    // 5
console.log(Math.sign(-5));  // -1  <- negative
console.log(Math.sign(0));   // 0   <- zero
console.log(Math.sign(5));   // 1   <- positive

// ── MIN, MAX ──────────────────────────────────────────────────
console.log(Math.max(3, 1, 4, 1, 5, 9)); // 9
console.log(Math.min(3, 1, 4, 1, 5, 9)); // 1
console.log(Math.max());                  // -Infinity (no args)
console.log(Math.min());                  // +Infinity (no args)

// With array (must spread!):
const nums8 = [3, 1, 4, 1, 5, 9];
console.log(Math.max(...nums8)); // 9

// ── POWER, SQRT ───────────────────────────────────────────────
console.log(Math.pow(2, 10));   // 1024
console.log(2 ** 10);           // 1024 (same, ES7 exponentiation operator)
console.log(Math.sqrt(144));    // 12
console.log(Math.cbrt(27));     // 3 <- cube root
console.log(Math.hypot(3, 4));  // 5 <- sqrt(3^2 + 4^2) = sqrt(25) = 5

// ── LOGARITHMS ────────────────────────────────────────────────
console.log(Math.log(Math.E)); // 1  <- natural log (ln) of e = 1
console.log(Math.log2(8));     // 3  <- log base 2: 2^3 = 8
console.log(Math.log10(1000)); // 3  <- log base 10: 10^3 = 1000

// ── RANDOM ────────────────────────────────────────────────────
// Returns a number: 0 <= x < 1 (never exactly 1)
console.log(Math.random()); // e.g., 0.7392...

// Random integer between min and max (inclusive)
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
console.log(randomInt(1, 6));  // dice roll! (1-6)
console.log(randomInt(0, 1));  // coin flip! (0 or 1)

// Random element from array
function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}
console.log(randomFrom(["rock", "paper", "scissors"]));

// Shuffle array (Fisher-Yates algorithm)
function shuffle(arr) {
  const result = [...arr]; // don't mutate original
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]]; // swap
  }
  return result;
}
console.log(shuffle([1, 2, 3, 4, 5])); // e.g., [3, 5, 1, 4, 2]

// ── TRIG FUNCTIONS ────────────────────────────────────────────
// NOTE: Angles are in RADIANS, not degrees!
console.log(Math.sin(Math.PI / 2)); // 1   (sin 90°)
console.log(Math.cos(0));           // 1   (cos 0°)
console.log(Math.tan(Math.PI / 4)); // 1   (tan 45°)

// Convert degrees to radians:
const toRadians = degrees => degrees * (Math.PI / 180);
console.log(Math.sin(toRadians(90)));  // 1
console.log(Math.cos(toRadians(180))); // -1

// ── OTHER USEFUL METHODS ──────────────────────────────────────
console.log(Math.fround(1.337));  // 1.3370000123977661 (32-bit float)
console.log(Math.clz32(1));       // 31 (count leading zeros in 32-bit)
console.log(Math.imul(3, 4));     // 12 (32-bit integer multiply)
```

---

# 12. Date Object

## 12.1 Creating Dates

```javascript
// ── CREATING DATES ────────────────────────────────────────────

// Current date and time
const now = new Date();
console.log(now); // current datetime

// From timestamp (milliseconds since Jan 1, 1970 00:00:00 UTC = UNIX epoch)
const epoch = new Date(0);
console.log(epoch); // 1970-01-01T00:00:00.000Z

// From date string
const fromString = new Date("2024-01-15");         // ISO format (recommended)
const fromString2 = new Date("January 15, 2024"); // human-readable
const fromString3 = new Date("2024-01-15T10:30:00"); // with time

// From components: new Date(year, month, day, hours, minutes, seconds, ms)
// MONTHS ARE 0-INDEXED! January = 0, February = 1, ... December = 11!
const fromParts = new Date(2024, 0, 15, 10, 30, 0, 0);
//                               ^— month 0 = JANUARY!

// COMMON MISTAKE:
const mistakeJan = new Date(2024, 1, 15); // month 1 = FEBRUARY, NOT January!
console.log(mistakeJan.toLocaleDateString()); // 2/15/2024 <- Feb 15!

// Correct January:
const correctJan = new Date(2024, 0, 15); // month 0 = January
console.log(correctJan.toLocaleDateString()); // 1/15/2024 <- Jan 15!

// ── Date.now() ────────────────────────────────────────────────
console.log(Date.now()); // current timestamp in milliseconds (no new needed)
```

## 12.2 Getting Date Components

```javascript
const d = new Date(2024, 0, 15, 10, 30, 45, 123);
// Mon Jan 15 2024 10:30:45.123

console.log(d.getFullYear());     // 2024
console.log(d.getMonth());        // 0   <- January (0-indexed!)
console.log(d.getDate());         // 15  <- day of month (1-31)
console.log(d.getDay());          // 1   <- Monday (0=Sunday, 6=Saturday)
console.log(d.getHours());        // 10
console.log(d.getMinutes());      // 30
console.log(d.getSeconds());      // 45
console.log(d.getMilliseconds()); // 123
console.log(d.getTime());         // ms since Unix epoch

// UTC variants (useful for timezone-independent code)
console.log(d.getUTCHours());     // may differ from local hours
console.log(d.getUTCMonth());     // same 0-indexed!
```

## 12.3 Setting Date Components

```javascript
const d2 = new Date(2024, 0, 15);

d2.setFullYear(2025);  // change year
d2.setMonth(5);        // change to June (0-indexed! 5 = June)
d2.setDate(20);        // change to 20th
d2.setHours(14);       // 2 PM

console.log(d2.toDateString()); // Fri Jun 20 2025
```

## 12.4 Date Formatting

```javascript
const d3 = new Date(2024, 0, 15, 10, 30, 0);

// ── Basic output methods ──────────────────────────────────────
console.log(d3.toString());           // Full string with timezone
console.log(d3.toDateString());       // "Mon Jan 15 2024"
console.log(d3.toTimeString());       // "10:30:00 GMT+0530 (IST)"
console.log(d3.toISOString());        // "2024-01-15T05:00:00.000Z" (UTC!)
console.log(d3.toLocaleDateString()); // "1/15/2024" (locale-dependent)
console.log(d3.toLocaleTimeString()); // "10:30:00 AM"
console.log(d3.toLocaleString());     // "1/15/2024, 10:30:00 AM"
console.log(d3.toUTCString());        // "Mon, 15 Jan 2024 05:00:00 GMT"

// ── Intl.DateTimeFormat (most powerful!) ──────────────────────
const formatter = new Intl.DateTimeFormat("en-IN", {
  year: "numeric",
  month: "long",
  day: "numeric",
  weekday: "long",
  hour: "2-digit",
  minute: "2-digit",
});
console.log(formatter.format(d3)); // "Monday, 15 January 2024 at 10:30 AM"

// Different locales
const de = new Intl.DateTimeFormat("de-DE").format(d3); // "15.1.2024"
const ja = new Intl.DateTimeFormat("ja-JP").format(d3); // "2024/1/15"
```

## 12.5 Date Arithmetic

```javascript
// ── COMPARING DATES ───────────────────────────────────────────
const date1 = new Date("2024-01-15");
const date2 = new Date("2024-03-20");

// Comparison works because Date has valueOf() returning timestamp
console.log(date1 < date2);  // true
console.log(date1 > date2);  // false
// Use getTime() for === comparison!
console.log(date1.getTime() === date2.getTime()); // false

// ── DATE DIFFERENCE ───────────────────────────────────────────
const diffMs = date2 - date1;  // subtraction triggers valueOf()
const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
console.log(diffDays); // 65 days

// ── ADD DAYS TO DATE ──────────────────────────────────────────
function addDays(date, days) {
  const result = new Date(date); // clone to avoid mutation!
  result.setDate(result.getDate() + days);
  return result;
}
console.log(addDays(date1, 30).toDateString()); // "Fri Feb 14 2024"

// ── ADD MONTHS ────────────────────────────────────────────────
function addMonths(date, months) {
  const result = new Date(date);
  result.setMonth(result.getMonth() + months);
  return result;
}

// ── PERFORMANCE TIMING ────────────────────────────────────────
const start = Date.now(); // current timestamp in ms
// ... do some work ...
const end = Date.now();
console.log(`Took ${end - start}ms`);

// Even better: performance.now() (sub-millisecond precision, relative time)
const t1 = performance.now();
for (let i = 0; i < 1000000; i++) {} // heavy loop
const t2 = performance.now();
console.log(`Took ${(t2 - t1).toFixed(3)}ms`);
```

---

# 13. Chapter Summary

```
+─────────────────────────────────────────────────────────────────────+
|                     CHAPTER 4 SUMMARY                              |
+─────────────────────────────────────────────────────────────────────+
|  OBJECTS                                                            |
|  • Object literal: { key: value }                                   |
|  • Dot notation (obj.key) vs Bracket (obj["key"] or obj[var])       |
|  • {} !== {} -> reference equality, objects live on heap            |
|  • Object.keys/values/entries/fromEntries/assign/create             |
|  • Object.freeze() -> no changes; Object.seal() -> only modify      |
|  • Property descriptors: writable, enumerable, configurable         |
|  • Getters/Setters: computed & validated properties                 |
|  • structuredClone() for deep copy                                  |
+─────────────────────────────────────────────────────────────────────+
|  PROTOTYPE CHAIN                                                    |
|  • Every object has [[Prototype]] link                              |
|  • Lookup: own -> proto -> proto's proto -> ... -> null             |
|  • __proto__ (each object) vs .prototype (constructor functions)    |
|  • hasOwnProperty checks own only; 'in' checks full chain           |
|  • Object.hasOwn() is modern preferred method                       |
+─────────────────────────────────────────────────────────────────────+
|  CLASSES                                                            |
|  • Syntactic sugar over prototypes                                  |
|  • constructor, instance methods, static methods                    |
|  • extends, super — call parent constructor first!                  |
|  • Private fields: #field (cannot be accessed outside class)        |
|  • Class body is always strict mode                                 |
+─────────────────────────────────────────────────────────────────────+
|  ARRAYS                                                             |
|  • typeof [] === "object" -> use Array.isArray()                    |
|  • Mutating: push/pop/shift/unshift/splice/sort/reverse/fill        |
|  • Non-mutating: slice/concat/map/filter/reduce/find/every/some     |
|  • sort() converts to string by default! Always use comparator!     |
|  • ES2023: toSorted/toReversed/toSpliced/with (non-mutating!)       |
|  • at(-1) -> last element                                           |
+─────────────────────────────────────────────────────────────────────+
|  DESTRUCTURING / SPREAD / REST                                      |
|  • [a, b, ...rest] = arr  /  const {x, ...rest} = obj              |
|  • Spread expands; Rest collects                                    |
|  • Swap variables: [a, b] = [b, a]                                 |
|  • Default values: const { name = "Anonymous" } = obj              |
|  • Rename: const { name: fullName } = obj                          |
+─────────────────────────────────────────────────────────────────────+
|  STRINGS                                                            |
|  • Immutable — methods return new strings                           |
|  • slice vs substring: use slice (supports negatives correctly)     |
|  • Template literals: `${expr}` and tagged templates               |
|  • at(-1) -> last character                                         |
|  • includes, startsWith, endsWith for boolean checks               |
+─────────────────────────────────────────────────────────────────────+
|  MATH & DATE                                                        |
|  • Math.random() -> 0 <= x < 1                                     |
|  • Math.floor/ceil/round/trunc differences                         |
|  • getMonth() -> 0-indexed! (Jan=0, Dec=11) <- most common bug!    |
|  • getDay() -> 0=Sunday, 1=Monday ... 6=Saturday                   |
|  • Date subtraction returns milliseconds                            |
|  • Use Intl.DateTimeFormat for locale-aware formatting              |
+─────────────────────────────────────────────────────────────────────+
```

---

# 14. Top 20 Interview Questions

### Basic Level

**Q1: What is the difference between dot notation and bracket notation?**

**Answer:** Dot notation (`obj.key`) requires the key to be a valid JavaScript identifier (no spaces, hyphens, must not start with numbers). Bracket notation (`obj["key"]`) accepts any string as a key and supports dynamic (variable) keys. Example:
```javascript
const key = "name";
obj.key     // looks for property named literally "key"
obj[key]    // looks for property named value of key = "name"
obj["my-property"]  // works, hyphen requires bracket notation
```

---

**Q2: What does `typeof []` return and why?**

**Answer:** `"object"`. Arrays are a special kind of object in JavaScript — their keys are numeric indices and they have a special `length` property. To check for arrays, use `Array.isArray()` which returns `true` only for real arrays.

---

**Q3: Explain the difference between `==` and `===` for objects.**

**Answer:** For objects (including arrays and functions), both `==` and `===` check **reference equality** — whether the two operands point to the exact same object in memory. Two objects with identical content are NOT equal unless they are the same reference.
```javascript
const a = { x: 1 };
const b = { x: 1 };
a == b;  // false — different objects
a === b; // false — different objects
const c = a;
a === c; // true  — same reference
```

---

**Q4: What is a shallow copy vs deep copy?**

**Answer:** A shallow copy creates a new object but nested properties still reference the same objects. A deep copy creates completely independent copies at all levels. Use `structuredClone()` for deep copy. The spread operator `{...obj}` and `Object.assign({}, obj)` are shallow copies.

---

**Q5: What is property shorthand in ES6?**

**Answer:** When a variable name matches the property key, you can write just the name once: `const { name, age } = person` instead of `{ name: name, age: age }`. Used heavily in function returns: `return { name, age, email }`.

---

### Intermediate Level

**Q6: What is the prototype chain and how does property lookup work?**

**Answer:** Every JavaScript object has a hidden `[[Prototype]]` link to another object. When you access a property:
1. Check the object itself
2. Check its `[[Prototype]]`
3. Check `[[Prototype]]`'s `[[Prototype]]`
4. Continue until `null` is reached
5. Return `undefined` if not found

This chain enables inheritance — child objects can access parent properties.

---

**Q7: What is the difference between `Object.freeze()` and `Object.seal()`?**

**Answer:**
- `Object.freeze()`: Cannot add, delete, OR modify properties
- `Object.seal()`: Cannot add or delete, but CAN modify existing properties
- Both are **shallow** — nested objects are NOT affected

---

**Q8: Why does `sort()` give wrong results with numbers?**

**Answer:** `sort()` converts elements to strings before comparing. So `[10, 9, 2]` sorts as `["10", "2", "9"]` → `[10, 2, 9]` (lexicographic order). Always use a comparator: `arr.sort((a, b) => a - b)`.

---

**Q9: What is the difference between `find()` and `filter()`?**

**Answer:**
- `find()` returns the **first** matching element (or `undefined`)
- `filter()` returns **all** matching elements as a new array (or `[]` if none match)
- `findIndex()` returns the index of the first match (or `-1`)

---

**Q10: Explain `reduce()` with a non-trivial example.**

**Answer:** `reduce()` accumulates all array elements into a single value. The callback receives `(accumulator, currentValue, index, array)`. Example — grouping by property:
```javascript
const grouped = people.reduce((acc, person) => {
  const dept = person.dept;
  acc[dept] = acc[dept] || [];
  acc[dept].push(person);
  return acc;
}, {});
```

---

### Advanced Level

**Q11: What is the difference between `__proto__` and `.prototype`?**

**Answer:** `__proto__` is a property on every **object instance** that points to its prototype (used internally for property lookup). `.prototype` is a property on **constructor functions** — it becomes the `__proto__` of objects created using `new`. When you do `new Dog()`, the new object's `__proto__` is set to `Dog.prototype`.

---

**Q12: How does `structuredClone()` differ from `JSON.parse(JSON.stringify())`?**

**Answer:**

| Feature | structuredClone | JSON round-trip |
|---------|----------------|-----------------|
| `undefined` values | Preserved | Lost |
| `Date` objects | Preserved as Date | Converted to string |
| `Map`, `Set` | Preserved | Converted to `{}` or `[]` |
| Functions | Cannot clone | Dropped |
| Circular references | Handled | Throws TypeError |
| `RegExp` | Preserved | Converted to `{}` |

---

**Q13: What are private fields (#) and why use them?**

**Answer:** Private fields (prefixed with `#`) are truly inaccessible outside the class body — not just by convention. They prevent external code from accidentally or maliciously modifying internal state. They don't appear in `Object.keys()` or through normal property access. They enforce encapsulation at the language level.

---

**Q14: What is the difference between `for...in` and `for...of`?**

**Answer:**
- `for...in` iterates over **enumerable property KEYS** (strings), including inherited ones. Use with `hasOwnProperty()` guard. Do NOT use on arrays (order not guaranteed, may iterate prototype properties).
- `for...of` iterates over **iterable VALUES** (arrays, strings, Maps, Sets, generators). Clean, no inherited property issues.

---

**Q15: When would you use `Object.create(null)`?**

**Answer:** When you need a truly pure hashmap with no prototype. `{}` inherits from `Object.prototype` (giving `toString`, `hasOwnProperty`, etc.), which can cause subtle bugs if someone stores keys like `"toString"` or `"constructor"`. `Object.create(null)` creates an object with no prototype — a clean dictionary.

---

### Tricky/Scenario-Based

**Q16: What is the output?**
```javascript
const a = [1, 2, 3];
const b = a;
b.push(4);
console.log(a.length);
```
**Answer:** `4`. `b` is not a copy — it's another reference to the same array.

---

**Q17: What is the output?**
```javascript
const obj = Object.freeze({ x: 1, nested: { y: 2 } });
obj.x = 10;
obj.nested.y = 20;
console.log(obj.x, obj.nested.y);
```
**Answer:** `1 20`. `freeze` is shallow. `obj.x` cannot change, but `obj.nested.y` can because the nested object itself is not frozen.

---

**Q18: What is the output?**
```javascript
console.log([10, 9, 2, 1, 100].sort());
```
**Answer:** `[1, 10, 100, 2, 9]`. Default sort converts to strings and sorts lexicographically!

---

**Q19: What is the output?**
```javascript
const arr = [1, 2, 3];
arr[10] = 99;
console.log(arr.length);
console.log(arr[5]);
```
**Answer:** `11` (length = highest index + 1) and `undefined` (sparse array — index 5 is a hole).

---

**Q20: Why is this approach dangerous and what's the fix?**
```javascript
const obj = { hasOwnProperty: () => false };
console.log(obj.hasOwnProperty("anyKey")); // ?
```
**Answer:** Returns `false` for everything because the local `hasOwnProperty` overrides `Object.prototype.hasOwnProperty`. Fix: Use `Object.hasOwn(obj, "anyKey")` which cannot be shadowed.

---

# 15. Output Exercises

**Exercise 1:**
```javascript
const nums = [1, 2, 3];
const doubled = nums.map(n => n * 2);
console.log(nums);     // ?
console.log(doubled);  // ?
```
**Answer:** `[1, 2, 3]` and `[2, 4, 6]`. `map` is non-mutating.

---

**Exercise 2:**
```javascript
const obj1 = { a: 1, b: { c: 2 } };
const obj2 = Object.assign({}, obj1);
obj2.a = 99;
obj2.b.c = 99;
console.log(obj1.a);   // ?
console.log(obj1.b.c); // ?
```
**Answer:** `1` and `99`. `a` is a primitive (independent copy), but `b` is a shared reference (shallow copy).

---

**Exercise 3:**
```javascript
const arr = [1, [2, [3, [4]]]];
console.log(arr.flat());         // ?
console.log(arr.flat(Infinity)); // ?
```
**Answer:** `[1, 2, [3, [4]]]` (1 level) and `[1, 2, 3, 4]` (fully flat).

---

**Exercise 4:**
```javascript
const str = "Hello World";
console.log(str.slice(-5));        // ?
console.log(str.substring(-5));    // ?
```
**Answer:** `"World"` (last 5 chars) and `"Hello World"` (negative treated as 0).

---

**Exercise 5:**
```javascript
const d = new Date(2024, 0, 1);   // Careful!
console.log(d.getMonth());  // ?
console.log(d.getDate());   // ?
console.log(d.getDay());    // ?
```
**Answer:** `0` (January = month 0), `1` (first day), `1` (Monday — Jan 1, 2024 was a Monday).

---

# 16. Coding Exercises

**Exercise 1:** Write `deepEqual(a, b)` that returns `true` if two objects are deeply equal.

```javascript
function deepEqual(a, b) {
  // Same primitive or same reference
  if (a === b) return true;
  
  // One or both are null, or not objects
  if (typeof a !== "object" || typeof b !== "object") return false;
  if (a === null || b === null) return false;
  
  // Check if both are arrays or both are plain objects
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  
  // Must have same number of keys
  if (keysA.length !== keysB.length) return false;
  
  // Recursively compare each key's value
  return keysA.every(key => 
    Object.hasOwn(b, key) && deepEqual(a[key], b[key])
  );
}

// Tests
console.log(deepEqual({ a: 1, b: { c: 2 } }, { a: 1, b: { c: 2 } })); // true
console.log(deepEqual({ a: 1 }, { a: 2 }));    // false
console.log(deepEqual([1, 2, 3], [1, 2, 3]));  // true
console.log(deepEqual([1, 2], [1, 2, 3]));      // false
console.log(deepEqual(null, null));             // true
```

---

**Exercise 2:** Implement `groupBy(array, key)`.

```javascript
function groupBy(array, key) {
  return array.reduce((groups, item) => {
    const groupKey = item[key];           // get the grouping value
    groups[groupKey] = groups[groupKey] || [];  // initialize if needed
    groups[groupKey].push(item);           // add item to group
    return groups;
  }, {});
}

const employees = [
  { name: "Alice", dept: "Engineering" },
  { name: "Bob", dept: "HR" },
  { name: "Charlie", dept: "Engineering" },
  { name: "Dave", dept: "HR" },
];

console.log(groupBy(employees, "dept"));
// { Engineering: [{Alice}, {Charlie}], HR: [{Bob}, {Dave}] }
```

---

**Exercise 3:** Flatten a deeply nested array without `flat()`.

```javascript
function flattenDeep(arr) {
  return arr.reduce((acc, item) => {
    if (Array.isArray(item)) {
      // Recursively flatten and concatenate
      return acc.concat(flattenDeep(item));
    }
    return acc.concat(item);
  }, []);
}

// Alternative: iterative approach
function flattenIterative(arr) {
  const result = [];
  const stack = [...arr]; // copy to avoid mutating input
  
  while (stack.length) {
    const item = stack.pop(); // take from end
    if (Array.isArray(item)) {
      stack.push(...item);    // expand nested array back onto stack
    } else {
      result.unshift(item);   // add to front (maintaining order)
    }
  }
  return result;
}

console.log(flattenDeep([1, [2, [3, [4, [5]]]]])); // [1, 2, 3, 4, 5]
```

---

**Exercise 4:** Implement `pick(obj, keys)` and `omit(obj, keys)`.

```javascript
// pick: return object with only specified keys
function pick(obj, keys) {
  return keys.reduce((result, key) => {
    if (Object.hasOwn(obj, key)) {
      result[key] = obj[key];
    }
    return result;
  }, {});
}

// omit: return object without specified keys
function omit(obj, keys) {
  const keysToOmit = new Set(keys); // O(1) lookup
  return Object.fromEntries(
    Object.entries(obj).filter(([key]) => !keysToOmit.has(key))
  );
}

const user4 = { name: "Nihal", age: 22, email: "n@n.com", password: "secret" };
console.log(pick(user4, ["name", "email"]));
// { name: "Nihal", email: "n@n.com" }

console.log(omit(user4, ["password"]));
// { name: "Nihal", age: 22, email: "n@n.com" }
```

---

**Exercise 5:** Implement a memoize function using WeakMap (for object keys) or Map.

```javascript
function memoize(fn) {
  const cache = new Map();
  
  return function (...args) {
    // Create a cache key from arguments
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      console.log("Cache hit!"); // for demonstration
      return cache.get(key);
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Expensive Fibonacci function
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const memoFib = memoize(fibonacci);
console.log(memoFib(40)); // slow first time
console.log(memoFib(40)); // "Cache hit!" — instant!
```

---

# 17. MCQs

**Q1:** What does `typeof []` return?
- A) `"array"`
- B) **`"object"` ✓**
- C) `"undefined"`
- D) `"function"`

---

**Q2:** Which method creates a DEEP clone?
- A) `Object.assign()`
- B) `{...obj}`
- C) **`structuredClone()` ✓**
- D) `JSON.stringify()` alone

---

**Q3:** What does `[3, 1, 10, 2].sort()` return?
- A) `[1, 2, 3, 10]`
- B) **`[1, 10, 2, 3]` ✓**
- C) `[10, 3, 2, 1]`
- D) `[3, 1, 10, 2]`

---

**Q4:** Which method does NOT mutate the original array?
- A) `push()`
- B) `splice()`
- C) `sort()`
- D) **`filter()` ✓**

---

**Q5:** What does `"hello".slice(-3)` return?
- A) `"hel"`
- B) **`"llo"` ✓**
- C) `"he"`
- D) `"ello"`

---

**Q6:** What is `new Date(2024, 1, 15).getMonth()`?
- A) **`1` ✓** (February, because months are 0-indexed)
- B) `2`
- C) `0`
- D) `15`

---

**Q7:** `Object.freeze()` on `{ nested: { value: 42 } }` — can you change `nested.value`?
- A) No, freeze is deep
- B) **Yes, freeze is shallow ✓**
- C) Throws an error
- D) Depends on strict mode

---

**Q8:** What does `[1,2,3,4].reduce((a,b) => a * b, 1)` return?
- A) `1`
- B) **`24` ✓** (1*1*2*3*4 = 24)
- C) `10`
- D) `undefined`

---

**Q9:** How do you swap variables `a` and `b` WITHOUT a temp variable?
- A) `a = b; b = a;` (Wrong — a becomes b before b is saved!)
- B) **`[a, b] = [b, a];` ✓**
- C) `Object.assign(a, b);`
- D) `a ^= b ^= a ^= b;` (Works for integers but not recommended)

---

**Q10:** What does `"abc".padStart(5, "0")` return?
- A) `"abc00"`
- B) **`"00abc"` ✓**
- C) `"0abc0"`
- D) `"abc  "`

---

> **Revision Cheat Sheet**
>
> | Concept | Key Point |
> |---------|-----------|
> | `{} !== {}` | Reference equality — objects compared by memory address |
> | `typeof []` | `"object"` — use `Array.isArray()` to detect arrays |
> | `sort()` default | Converts to string! Always use `(a,b) => a-b` for numbers |
> | `slice` vs `substring` | slice supports negatives correctly; substring treats -ve as 0 |
> | `getMonth()` | 0-indexed! January=0, December=11 — classic interview trap |
> | `structuredClone()` | Modern deep copy — handles Date, Map, Set, circular refs |
> | `Object.freeze()` | Shallow freeze only! |
> | `in` operator | Checks own AND prototype chain |
> | `Object.hasOwn()` | Preferred over `hasOwnProperty` (can't be shadowed) |
> | `flat(Infinity)` | Completely flattens any nesting depth |
> | Rest `...` | **Collects** into array (params/destructuring) |
> | Spread `...` | **Expands** out (calls/literals) |
> | `at(-1)` | Last element of array or string |
> | `toSorted/toReversed` | ES2023 — non-mutating counterparts, perfect for React |

---

*End of Chapter 4 — Objects, Arrays, Strings, Math & Date*

---
*React.js + JavaScript Master Handbook | Part 1: JavaScript Fundamentals*
