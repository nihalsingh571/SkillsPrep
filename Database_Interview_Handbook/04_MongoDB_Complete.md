# MongoDB Complete Guide — CRUD, Aggregation, Indexes, Schema Design
## 80 Queries with Sample Data + Expected Output for Every Query

> **Sample documents for all queries are in [README.md](./README.md). Refer there for the full dataset.**

---

## Sample Data Reminder

```javascript
// employees collection (5 docs used throughout)
{ _id:1, name:"Alice",  dept:"Engineering", salary:90000, city:"Mumbai",    skills:["Java","React","MongoDB"], isActive:true }
{ _id:2, name:"Bob",    dept:"Engineering", salary:75000, city:"Mumbai",    skills:["Java","Spring"],          isActive:true }
{ _id:3, name:"Carol",  dept:"Marketing",   salary:85000, city:"Delhi",     skills:["SEO","Analytics"],        isActive:true }
{ _id:4, name:"David",  dept:"Marketing",   salary:60000, city:"Delhi",     skills:["Content","SEO"],          isActive:false }
{ _id:5, name:"Eve",    dept:"Sales",       salary:95000, city:"Bangalore", skills:["CRM","Negotiation","Java"],isActive:true }

// orders collection (5 docs)
{ _id:101, customer_id:1, product_id:1, amount:75000, status:"DELIVERED", order_date:ISODate("2024-01-10") }
{ _id:102, customer_id:1, product_id:2, amount:1500,  status:"DELIVERED", order_date:ISODate("2024-02-14") }
{ _id:103, customer_id:2, product_id:3, amount:12000, status:"SHIPPED",   order_date:ISODate("2024-01-20") }
{ _id:104, customer_id:3, product_id:4, amount:800,   status:"DELIVERED", order_date:ISODate("2024-03-05") }
{ _id:105, customer_id:4, product_id:1, amount:75000, status:"PENDING",   order_date:ISODate("2024-03-18") }

// products collection (5 docs)
{ _id:1, name:"Laptop Pro",     category:"Electronics", price:75000, stock:50  }
{ _id:2, name:"Wireless Mouse", category:"Electronics", price:1500,  stock:200 }
{ _id:3, name:"Office Chair",   category:"Furniture",   price:12000, stock:30  }
{ _id:4, name:"Java Book",      category:"Books",       price:800,   stock:100 }
{ _id:5, name:"Standing Desk",  category:"Furniture",   price:25000, stock:15  }
```

---

## SECTION 1 — CRUD (Q1–Q25)

---

### Q1. Insert a single document

📌 **New Concept — insertOne:** Inserts exactly one document into a collection. Returns an `insertedId` acknowledgement. If `_id` is omitted, MongoDB auto-generates an `ObjectId`.

```javascript
db.employees.insertOne({
    name: "Frank", dept: "Sales", salary: 70000,
    city: "Bangalore", skills: ["Negotiation"], isActive: true
});
```

**Output:**
```json
{ "acknowledged": true, "insertedId": ObjectId("...auto-generated...") }
```

---

### Q2. Insert multiple documents

📌 **New Concept — insertMany:** Inserts an array of documents in a single call. More efficient than multiple `insertOne` calls. `ordered: false` continues inserting even if one document fails.

```javascript
db.employees.insertMany([
    { name: "Grace", dept: "Engineering", salary: 80000, city: "Mumbai" },
    { name: "Hank",  dept: "Marketing",   salary: 65000, city: "Delhi" }
]);
```

**Output:**
```json
{ "acknowledged": true, "insertedIds": { "0": ObjectId("..."), "1": ObjectId("...") } }
```

---

### Q3. Find all documents

📌 **New Concept — find({}):** An empty filter `{}` matches ALL documents, like `SELECT *`. Returns a cursor object. Use `.pretty()` to format output in the shell.

```javascript
db.employees.find({}).pretty();
```

**Output (5 documents):**
```json
{ "_id": 1, "name": "Alice", "dept": "Engineering", "salary": 90000, ... }
{ "_id": 2, "name": "Bob",   "dept": "Engineering", "salary": 75000, ... }
{ "_id": 3, "name": "Carol", "dept": "Marketing",   "salary": 85000, ... }
{ "_id": 4, "name": "David", "dept": "Marketing",   "salary": 60000, ... }
{ "_id": 5, "name": "Eve",   "dept": "Sales",       "salary": 95000, ... }
```

---

### Q4. Find with conditions

📌 **New Concept — Comparison Operators:** `$gt` (>), `$gte` (>=), `$lt` (<), `$lte` (<=), `$ne` (!=), `$in` (IN), `$nin` (NOT IN). Always wrapped in `{}` as value of the field.

```javascript
// salary > 80000 AND dept = "Engineering"
db.employees.find({ salary: { $gt: 80000 }, dept: "Engineering" });

// salary BETWEEN 70000 AND 90000
db.employees.find({ salary: { $gte: 70000, $lte: 90000 } });
```

**Output (first query — salary > 80000 AND Engineering):**
```json
{ "_id": 1, "name": "Alice", "dept": "Engineering", "salary": 90000 }
```

**Output (second query — salary 70k–90k):**
```json
{ "_id": 1, "name": "Alice", "salary": 90000 }
{ "_id": 2, "name": "Bob",   "salary": 75000 }
{ "_id": 3, "name": "Carol", "salary": 85000 }
```

---

### Q5. Projection — Select specific fields

📌 **New Concept — Projection:** The second argument to `find()`. `1` = include field, `0` = exclude. Cannot mix inclusion and exclusion except for `_id` (you can always exclude `_id` with `_id: 0`).

```javascript
db.employees.find({}, { name: 1, salary: 1, _id: 0 });
```

**Output:**
```json
{ "name": "Alice", "salary": 90000 }
{ "name": "Bob",   "salary": 75000 }
{ "name": "Carol", "salary": 85000 }
{ "name": "David", "salary": 60000 }
{ "name": "Eve",   "salary": 95000 }
```

---

### Q6. Logical operators — $or, $and, $not

📌 **New Concept — $or:** Returns documents matching ANY of the conditions. Takes an array of condition objects.

📌 **New Concept — $and (explicit):** Explicit AND — useful when the same field appears in multiple conditions (implicit AND can't repeat field names in one object).

```javascript
// dept = "Engineering" OR salary > 90000
db.employees.find({ $or: [{ dept: "Engineering" }, { salary: { $gt: 90000 } }] });
```

**Output:**
```json
{ "_id": 1, "name": "Alice", "dept": "Engineering", "salary": 90000 }
{ "_id": 2, "name": "Bob",   "dept": "Engineering", "salary": 75000 }
{ "_id": 5, "name": "Eve",   "dept": "Sales",       "salary": 95000 }
```

---

### Q7. Array query — Find employees with 'Java' skill

📌 **New Concept — Array field query:** When you query a field that contains an array, MongoDB checks if the array **contains** the queried value. `{ skills: "Java" }` matches any document where the `skills` array includes "Java".

```javascript
db.employees.find({ skills: "Java" });
```

**Output:**
```json
{ "_id": 1, "name": "Alice", "skills": ["Java","React","MongoDB"] }
{ "_id": 2, "name": "Bob",   "skills": ["Java","Spring"] }
{ "_id": 5, "name": "Eve",   "skills": ["CRM","Negotiation","Java"] }
```

---

### Q8. $all — Employee must have ALL listed skills

📌 **New Concept — $all:** The array field must contain **all** specified elements (in any order). Unlike the direct array match which requires EXACT array equality.

```javascript
db.employees.find({ skills: { $all: ["Java", "React"] } });
```

**Output:**
```json
{ "_id": 1, "name": "Alice", "skills": ["Java","React","MongoDB"] }
```

> Only Alice has both "Java" AND "React".

---

### Q9. Update a field with $set

📌 **New Concept — updateOne + $set:** `updateOne` modifies the **first** matching document. `$set` changes only the specified fields, leaving all other fields untouched. Without `$set`, MongoDB would REPLACE the entire document!

```javascript
db.employees.updateOne(
    { name: "Alice" },
    { $set: { salary: 95000, city: "Pune" } }
);
```

**Output:**
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

**Document after update:**
```json
{ "_id": 1, "name": "Alice", "dept": "Engineering", "salary": 95000, "city": "Pune", "skills": [...] }
```

---

### Q10. $inc — Increment a numeric field

📌 **New Concept — $inc:** Atomically increments (or decrements with negative value) a numeric field. Safer than read-then-write for counters.

```javascript
db.employees.updateOne({ name: "Bob" }, { $inc: { salary: 5000 } });
```

**Bob's salary before:** 75000 → **After:** 80000

---

### Q11. $push — Add element to array

📌 **New Concept — $push:** Adds a value to an array field. If the field doesn't exist, creates it.

📌 **New Concept — $addToSet:** Like `$push`, but only adds if the value doesn't already exist in the array (prevents duplicates).

```javascript
db.employees.updateOne({ name: "Alice" }, { $push: { skills: "Kubernetes" } });
db.employees.updateOne({ name: "Alice" }, { $addToSet: { skills: "Java" } }); // No-op — Java exists
```

**Alice's skills before:** `["Java","React","MongoDB"]`
**After $push Kubernetes:** `["Java","React","MongoDB","Kubernetes"]`
**After $addToSet Java:** No change — Java already in array.

---

### Q12. $pull — Remove element from array

📌 **New Concept — $pull:** Removes all array elements that match the given condition/value.

```javascript
db.employees.updateOne({ name: "Carol" }, { $pull: { skills: "SEO" } });
```

**Carol's skills before:** `["SEO","Analytics"]`
**After:** `["Analytics"]`

---

### Q13. updateMany — Update all matching documents

```javascript
db.employees.updateMany(
    { dept: "Engineering" },
    { $inc: { salary: 5000 } }
);
```

**Output:**
```json
{ "acknowledged": true, "matchedCount": 2, "modifiedCount": 2 }
```

Engineering employees (Alice, Bob) get 5000 raise.

---

### Q14. Sort, Limit, Skip

📌 **New Concept — sort():** `-1` = descending, `1` = ascending.
📌 **New Concept — skip():** Skips the first N documents (used for pagination with limit).

```javascript
db.employees.find({}).sort({ salary: -1 }).limit(3).skip(0);
```

**Output (top 3 earners):**
```json
{ "_id": 5, "name": "Eve",   "salary": 95000 }
{ "_id": 1, "name": "Alice", "salary": 90000 }
{ "_id": 3, "name": "Carol", "salary": 85000 }
```

---

### Q15. Query nested/embedded document

📌 **New Concept — Dot notation for nested fields:** Use `"parent.child"` (quoted) to access nested fields in queries and projections.

```javascript
// Find employees in Mumbai using nested address:
// Assuming: { address: { city: "Mumbai", pincode: "400001" } }
db.employees.find({ "address.city": "Mumbai" });
```

**Output:** Alice (Mumbai) and Bob (Mumbai) — using city field as top-level in our dataset:
```javascript
db.employees.find({ city: "Mumbai" });
```

```json
{ "_id": 1, "name": "Alice", "city": "Mumbai" }
{ "_id": 2, "name": "Bob",   "city": "Mumbai" }
```

---

### Q16. deleteOne and deleteMany

```javascript
db.employees.deleteOne({ _id: 4 });     // Delete David
db.employees.deleteMany({ isActive: false }); // Delete all inactive
```

**deleteOne output:**
```json
{ "acknowledged": true, "deletedCount": 1 }
```

---

### Q17. $exists — Check if field exists

📌 **New Concept — $exists:** Returns documents where the specified field exists (`true`) or does not exist (`false`). A `null` value field DOES exist — `$exists: true` matches it.

```javascript
db.employees.find({ manager_id: { $exists: true } });  // Has manager_id field
db.employees.find({ manager_id: { $exists: false } }); // No manager_id field at all
```

---

### Q18. Count documents

📌 **New Concept — countDocuments:** Counts documents matching the filter. More accurate than `estimatedDocumentCount()` which uses collection metadata.

```javascript
db.employees.countDocuments({});                         // All: 5
db.employees.countDocuments({ dept: "Engineering" });    // 2
db.employees.countDocuments({ salary: { $gt: 80000 } }); // 3
```

**Output:** `5`, `2`, `3`

---

### Q19. distinct — Unique values

📌 **New Concept — distinct:** Returns an array of unique values for a specified field across all matching documents.

```javascript
db.employees.distinct("dept");
db.employees.distinct("city", { salary: { $gt: 70000 } });
```

**Output (first):** `["Engineering", "Marketing", "Sales"]`
**Output (second — cities of high earners):** `["Mumbai", "Delhi", "Bangalore"]`

---

### Q20. Upsert — Insert if not exists, update if exists

📌 **New Concept — upsert:** When `upsert: true`, if no document matches the filter, a new document is created using the filter + update data.

```javascript
db.employees.updateOne(
    { name: "NewEmp" },
    { $set: { salary: 70000, dept: "HR" } },
    { upsert: true }
);
```

**Output (no match → inserts):**
```json
{ "acknowledged": true, "matchedCount": 0, "upsertedId": ObjectId("...") }
```

---

### Q21. Regular expressions — Pattern matching

📌 **New Concept — $regex:** Applies a regular expression pattern to string fields. `$options: "i"` makes it case-insensitive.

```javascript
db.employees.find({ name: { $regex: "^A", $options: "i" } }); // Names starting with A
db.employees.find({ city: /mumbai/i });                        // City contains "mumbai" (case-insensitive)
```

**Output (names starting with A):**
```json
{ "_id": 1, "name": "Alice" }
```

---

### Q22. $size — Find documents where array has N elements

📌 **New Concept — $size:** Matches documents where the array field has exactly N elements.

```javascript
db.employees.find({ skills: { $size: 2 } });
```

**Output:**
```json
{ "_id": 2, "name": "Bob",   "skills": ["Java","Spring"] }
{ "_id": 3, name:"Carol", skills:["SEO","Analytics"] }
{ "_id": 4, "name": "David", "skills": ["Content","SEO"] }
```

---

### Q23. $elemMatch — Array element matching multiple conditions

📌 **New Concept — $elemMatch:** Used when a single array element must satisfy MULTIPLE conditions simultaneously. Without it, MongoDB matches documents where different elements satisfy different conditions.

```javascript
// Find orders where at least one item has qty > 2 AND price < 1000
// (Assuming: items: [{ product: "A", qty: 3, price: 500 }, ...])
db.orders.find({ items: { $elemMatch: { qty: { $gt: 2 }, price: { $lt: 1000 } } } });
```

---

### Q24. findOneAndUpdate — Atomic find + update

📌 **New Concept — findOneAndUpdate:** Atomically finds a document, updates it, and returns it. `returnDocument: "after"` returns the updated version (default is before).

```javascript
db.employees.findOneAndUpdate(
    { name: "Bob" },
    { $inc: { salary: 10000 } },
    { returnDocument: "after" }
);
```

**Output (Bob's document after salary increase):**
```json
{ "_id": 2, "name": "Bob", "dept": "Engineering", "salary": 85000, ... }
```

---

### Q25. Transaction — Transfer salary budget between departments

📌 **New Concept — MongoDB Transactions:** Multi-document atomic operations (since MongoDB 4.0, requires replica set). Uses session-based API. Either all operations commit or all roll back.

```javascript
const session = db.getMongo().startSession();
session.startTransaction();
try {
    db.employees.updateOne({ _id: 1 }, { $inc: { salary: -5000 } }, { session });
    db.employees.updateOne({ _id: 2 }, { $inc: { salary: 5000  } }, { session });
    session.commitTransaction();
    print("Transfer committed");
} catch (e) {
    session.abortTransaction();
    print("Transfer rolled back: " + e.message);
} finally { session.endSession(); }
```

**Output (on success):** `Transfer committed`
**After commit:** Alice: 90000→85000, Bob: 75000→80000

---

## SECTION 2 — AGGREGATION PIPELINE (Q26–Q60)

---

### Q26. Basic aggregation — Avg and max salary by department

📌 **New Concept — Aggregation Pipeline:** A sequence of stages where each stage transforms the documents. Output of one stage flows as input to the next. Key stages: `$match` (filter), `$group` (aggregate), `$project` (reshape), `$sort`, `$lookup` (join).

📌 **New Concept — $group:** Groups documents by `_id` field. Accumulator operators: `$sum`, `$avg`, `$max`, `$min`, `$push`, `$addToSet`.

```javascript
db.employees.aggregate([
    { $group: {
        _id: "$dept",
        avg_salary: { $avg: "$salary" },
        max_salary: { $max: "$salary" },
        count:      { $sum: 1 }
    }}
]);
```

**Output:**
```json
{ "_id": "Engineering", "avg_salary": 82500, "max_salary": 90000, "count": 2 }
{ "_id": "Marketing",   "avg_salary": 72500, "max_salary": 85000, "count": 2 }
{ "_id": "Sales",       "avg_salary": 95000, "max_salary": 95000, "count": 1 }
```

---

### Q27. $match — Filter before grouping

📌 **New Concept — $match:** Filters documents — equivalent to SQL `WHERE`. Always place `$match` as **early as possible** to reduce documents in subsequent stages.

```javascript
db.employees.aggregate([
    { $match: { isActive: true, salary: { $gte: 80000 } } },
    { $group: { _id: "$dept", count: { $sum: 1 }, total_salary: { $sum: "$salary" } } }
]);
```

**Output (active employees with salary ≥ 80000):**
```json
{ "_id": "Engineering", "count": 1, "total_salary": 90000 }
{ "_id": "Marketing",   "count": 1, "total_salary": 85000 }
{ "_id": "Sales",       "count": 1, "total_salary": 95000 }
```

---

### Q28. $project — Include, exclude, compute new fields

📌 **New Concept — $project:** Reshapes documents — include/exclude fields and compute new ones using expressions. Similar to SQL `SELECT`.

```javascript
db.employees.aggregate([
    { $project: {
        name: 1,
        salary: 1,
        _id: 0,
        annual_salary: { $multiply: ["$salary", 12] },
        name_upper:    { $toUpper: "$name" }
    }}
]);
```

**Output:**
```json
{ "name": "Alice", "salary": 90000, "annual_salary": 1080000, "name_upper": "ALICE" }
{ "name": "Bob",   "salary": 75000, "annual_salary": 900000,  "name_upper": "BOB"   }
{ "name": "Carol", "salary": 85000, "annual_salary": 1020000, "name_upper": "CAROL" }
{ "name": "David", "salary": 60000, "annual_salary": 720000,  "name_upper": "DAVID" }
{ "name": "Eve",   "salary": 95000, "annual_salary": 1140000, "name_upper": "EVE"   }
```

---

### Q29. $sort, $limit, $skip

```javascript
db.employees.aggregate([
    { $sort: { salary: -1 } },
    { $limit: 3 }
]);
```

**Output (top 3 earners):**
```json
{ "_id": 5, "name": "Eve",   "salary": 95000 }
{ "_id": 1, "name": "Alice", "salary": 90000 }
{ "_id": 3, "name": "Carol", "salary": 85000 }
```

---

### Q30. $lookup — JOIN employees with a departments collection

📌 **New Concept — $lookup:** The MongoDB equivalent of SQL JOIN. Performs a left outer join with another collection. Returns an array field with matching documents.

📌 **New Concept — $unwind:** Deconstructs an array field, creating one document per array element. After `$lookup`, the joined result is an array — `$unwind` flattens it to behave like INNER JOIN (documents with empty arrays are dropped).

```javascript
db.employees.aggregate([
    { $lookup: {
        from: "departments",          // Collection to join
        localField: "dept_id",        // Field in employees
        foreignField: "_id",          // Field in departments
        as: "dept_info"               // Output array field name
    }},
    { $unwind: "$dept_info" },        // Flatten array → one doc per employee
    { $project: { name: 1, salary: 1, "dept_info.name": 1, _id: 0 } }
]);
```

> *(Our employees collection uses `dept` as string not `dept_id` FK — the pattern is the same)*

**Conceptual Output:**
```json
{ "name": "Alice", "salary": 90000, "dept_info": { "name": "Engineering" } }
{ "name": "Bob",   "salary": 75000, "dept_info": { "name": "Engineering" } }
```

---

### Q31. $unwind with array data — Skills frequency

```javascript
db.employees.aggregate([
    { $unwind: "$skills" },
    { $group: { _id: "$skills", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
]);
```

**Input:** 5 employees with various skills.
**After $unwind:** Each skill becomes a separate document: Alice×3 = 3 docs, Bob×2, Carol×2, David×2, Eve×3 = 12 total docs.

**Output:**
```json
{ "_id": "Java",        "count": 3 }
{ "_id": "SEO",         "count": 2 }
{ "_id": "React",       "count": 1 }
{ "_id": "MongoDB",     "count": 1 }
{ "_id": "Spring",      "count": 1 }
{ "_id": "Analytics",   "count": 1 }
{ "_id": "Content",     "count": 1 }
{ "_id": "CRM",         "count": 1 }
{ "_id": "Negotiation", "count": 1 }
```

---

### Q32. $addFields — Add computed fields without replacing others

📌 **New Concept — $addFields:** Adds new fields to documents while keeping ALL existing fields. Unlike `$project` (which requires explicitly listing fields to keep), `$addFields` is additive-only.

```javascript
db.employees.aggregate([
    { $addFields: {
        monthly_salary: { $divide:   ["$salary", 12] },
        seniority:      { $cond: { if: { $gte: ["$salary", 85000] }, then: "Senior", else: "Junior" } }
    }}
]);
```

**Output (first 2 docs):**
```json
{ "_id":1, "name":"Alice", "dept":"Engineering", "salary":90000, "monthly_salary":7500,  "seniority":"Senior" }
{ "_id":2, "name":"Bob",   "dept":"Engineering", "salary":75000, "monthly_salary":6250,  "seniority":"Junior" }
```

---

### Q33. $cond and $switch — Conditional logic

📌 **New Concept — $cond:** Inline if-else expression: `{ $cond: { if: condition, then: value, else: value } }`.

📌 **New Concept — $switch:** Multi-branch conditional (equivalent to SQL `CASE WHEN`). Evaluates branches in order, uses the first matching `then` value.

```javascript
db.employees.aggregate([
    { $project: {
        name: 1,
        salary_band: {
            $switch: {
                branches: [
                    { case: { $lt:  ["$salary", 70000] }, then: "Low" },
                    { case: { $lt:  ["$salary", 90000] }, then: "Mid" },
                    { case: { $gte: ["$salary", 90000] }, then: "High" }
                ],
                default: "Unknown"
            }
        }
    }}
]);
```

**Output:**
```json
{ "name": "Alice", "salary_band": "High" }
{ "name": "Bob",   "salary_band": "Mid"  }
{ "name": "Carol", "salary_band": "Mid"  }
{ "name": "David", "salary_band": "Low"  }
{ "name": "Eve",   "salary_band": "High" }
```

---

### Q34. $facet — Multiple aggregations in one pass

📌 **New Concept — $facet:** Runs multiple aggregation pipelines simultaneously on the SAME input documents. Returns a single document with one field per sub-pipeline — perfect for search result facets (counts by category + top items + stats).

```javascript
db.products.aggregate([
    { $facet: {
        by_category: [
            { $group: { _id: "$category", count: { $sum: 1 } } }
        ],
        price_stats: [
            { $group: { _id: null, avg_price: { $avg: "$price" }, max_price: { $max: "$price" } } }
        ],
        top_2_expensive: [
            { $sort: { price: -1 } }, { $limit: 2 }, { $project: { name: 1, price: 1 } }
        ]
    }}
]);
```

**Output:**
```json
{
  "by_category": [
    { "_id": "Electronics", "count": 2 },
    { "_id": "Furniture",   "count": 2 },
    { "_id": "Books",       "count": 1 }
  ],
  "price_stats": [
    { "_id": null, "avg_price": 22860, "max_price": 75000 }
  ],
  "top_2_expensive": [
    { "_id": 1, "name": "Laptop Pro",     "price": 75000 },
    { "_id": 5, "name": "Standing Desk",  "price": 25000 }
  ]
}
```

---

### Q35. $bucket — Group products by price range

📌 **New Concept — $bucket:** Groups documents into predefined price ranges. `boundaries` defines the bucket edges (must be sorted ascending). Values outside all boundaries go to `default`.

```javascript
db.products.aggregate([
    { $bucket: {
        groupBy:    "$price",
        boundaries: [0, 2000, 20000, 100000],
        default:    "Other",
        output: {
            count:     { $sum: 1 },
            avg_price: { $avg: "$price" },
            items:     { $push: "$name" }
        }
    }}
]);
```

**Output:**
```json
{ "_id": 0,      "count": 2, "avg_price": 1150,  "items": ["Wireless Mouse","Java Book"] }
{ "_id": 2000,   "count": 1, "avg_price": 12000, "items": ["Office Chair"] }
{ "_id": 20000,  "count": 2, "avg_price": 50000, "items": ["Laptop Pro","Standing Desk"] }
```

> *(Python Course 1200 also goes to first bucket, Java Book 800 too — adjust per actual data)*

---

### Q36. Top N per group — Top 2 earners per department

```javascript
db.employees.aggregate([
    { $sort: { salary: -1 } },
    { $group: {
        _id: "$dept",
        top_earners: { $push: { name: "$name", salary: "$salary" } }
    }},
    { $project: {
        dept: "$_id",
        top_2: { $slice: ["$top_earners", 2] }
    }}
]);
```

📌 **New Concept — $slice:** Extracts a subset of an array. `{ $slice: [array, n] }` returns first N elements.

**Output:**
```json
{ "dept": "Engineering", "top_2": [{ "name": "Alice", "salary": 90000 }, { "name": "Bob", "salary": 75000 }] }
{ "dept": "Marketing",   "top_2": [{ "name": "Carol", "salary": 85000 }, { "name": "David","salary": 60000 }] }
{ "dept": "Sales",       "top_2": [{ "name": "Eve",   "salary": 95000 }] }
```

---

### Q37. Date aggregation — Order count by month

```javascript
db.orders.aggregate([
    { $group: {
        _id: {
            year:  { $year:  "$order_date" },
            month: { $month: "$order_date" }
        },
        count:   { $sum: 1 },
        revenue: { $sum: "$amount" }
    }},
    { $sort: { "_id.year": 1, "_id.month": 1 } }
]);
```

**Output:**
```json
{ "_id": { "year": 2024, "month": 1 }, "count": 2, "revenue": 87000 }
{ "_id": { "year": 2024, "month": 2 }, "count": 1, "revenue": 1500  }
{ "_id": { "year": 2024, "month": 3 }, "count": 2, "revenue": 75800 }
```

---

### Q38. $lookup with unwind — Orders with product names

```javascript
db.orders.aggregate([
    { $lookup: {
        from:         "products",
        localField:   "product_id",
        foreignField: "_id",
        as:           "product"
    }},
    { $unwind: "$product" },
    { $project: {
        order_id: "$_id",
        customer_id: 1, amount: 1, status: 1,
        product_name: "$product.name",
        product_category: "$product.category"
    }}
]);
```

**Output:**
```json
{ "order_id": 101, "customer_id": 1, "amount": 75000, "status": "DELIVERED", "product_name": "Laptop Pro",     "product_category": "Electronics" }
{ "order_id": 102, "customer_id": 1, "amount": 1500,  "status": "DELIVERED", "product_name": "Wireless Mouse", "product_category": "Electronics" }
{ "order_id": 103, "customer_id": 2, "amount": 12000, "status": "SHIPPED",   "product_name": "Office Chair",   "product_category": "Furniture"   }
{ "order_id": 104, "customer_id": 3, "amount": 800,   "status": "DELIVERED", "product_name": "Java Book",      "product_category": "Books"        }
{ "order_id": 105, "customer_id": 4, "amount": 75000, "status": "PENDING",   "product_name": "Laptop Pro",     "product_category": "Electronics"  }
```

---

### Q39. Revenue by product category via $lookup + $group

```javascript
db.orders.aggregate([
    { $lookup: { from: "products", localField: "product_id", foreignField: "_id", as: "prod" } },
    { $unwind: "$prod" },
    { $group: { _id: "$prod.category", total_revenue: { $sum: "$amount" } } },
    { $sort: { total_revenue: -1 } }
]);
```

**Output:**
```json
{ "_id": "Electronics", "total_revenue": 152500 }
{ "_id": "Furniture",   "total_revenue": 12000  }
{ "_id": "Books",       "total_revenue": 800    }
```

---

### Q40. $count — Count high earners

```javascript
db.employees.aggregate([
    { $match: { salary: { $gte: 85000 } } },
    { $count: "high_earner_count" }
]);
```

**Output:**
```json
{ "high_earner_count": 3 }
```

> Alice (90k), Carol (85k), Eve (95k).

---

### Q41. $group with $addToSet — Unique cities per department

```javascript
db.employees.aggregate([
    { $group: {
        _id: "$dept",
        employee_names: { $push: "$name" },
        cities:         { $addToSet: "$city" }
    }}
]);
```

📌 **New Concept — $addToSet (accumulator):** Adds to an array but skips duplicates — produces unique values. Different from `$push` which allows duplicates.

**Output:**
```json
{ "_id": "Engineering", "employee_names": ["Alice","Bob"], "cities": ["Mumbai"] }
{ "_id": "Marketing",   "employee_names": ["Carol","David"], "cities": ["Delhi"] }
{ "_id": "Sales",       "employee_names": ["Eve"],          "cities": ["Bangalore"] }
```

---

### Q42. $out — Write aggregation result to a collection

📌 **New Concept — $out:** Writes the aggregation pipeline output to a specified collection. If the collection exists, it is **replaced entirely**.

```javascript
db.employees.aggregate([
    { $group: { _id: "$dept", avg_salary: { $avg: "$salary" } } },
    { $out: "dept_salary_summary" }
]);

// Verify:
db.dept_salary_summary.find({});
```

**Output of find() after $out:**
```json
{ "_id": "Engineering", "avg_salary": 82500 }
{ "_id": "Marketing",   "avg_salary": 72500 }
{ "_id": "Sales",       "avg_salary": 95000 }
```

---

### Q43. $sample — Random documents

📌 **New Concept — $sample:** Returns N randomly selected documents from the collection.

```javascript
db.employees.aggregate([{ $sample: { size: 2 } }]);
```

**Output (random — results vary per run):**
```json
{ "_id": 3, "name": "Carol", ... }
{ "_id": 1, "name": "Alice", ... }
```

---

### Q44. $expr — Compare two fields in same document

📌 **New Concept — $expr:** Allows using aggregation expressions inside `$match`. Enables comparing two fields within the same document (not possible with regular query operators).

```javascript
// Find orders where amount > product price (over-charged)
db.orders.find({ $expr: { $gt: ["$amount", 70000] } });
```

**Output:**
```json
{ "_id": 101, "customer_id": 1, "amount": 75000, "status": "DELIVERED" }
{ "_id": 105, "customer_id": 4, "amount": 75000, "status": "PENDING"   }
```

---

### Q45. $filter — Filter array elements within a document

📌 **New Concept — $filter:** Filters elements of an array within a document. `input` is the array, `as` is the local variable name, `cond` is the filter condition. Use `$$variableName` to reference the local variable.

```javascript
db.employees.aggregate([
    { $project: {
        name: 1,
        java_skills: {
            $filter: {
                input: "$skills",
                as:    "skill",
                cond:  { $eq: ["$$skill", "Java"] }
            }
        }
    }}
]);
```

**Output (only shows docs/skills matching 'Java'):**
```json
{ "_id": 1, "name": "Alice", "java_skills": ["Java"] }
{ "_id": 2, "name": "Bob",   "java_skills": ["Java"] }
{ "_id": 3, "name": "Carol", "java_skills": [] }
{ "_id": 4, "name": "David", "java_skills": [] }
{ "_id": 5, "name": "Eve",   "java_skills": ["Java"] }
```

---

## SECTION 3 — INDEXES (Q46–Q60)

---

### Q46. Create and verify a single field index

📌 **New Concept — createIndex:** Creates an index on a collection. `1` = ascending, `-1` = descending. The `unique: true` option prevents duplicate values.

```javascript
db.employees.createIndex({ salary: 1 });
db.employees.createIndex({ email: 1 }, { unique: true });

// Verify:
db.employees.getIndexes();
```

**Output of getIndexes():**
```json
[
  { "key": { "_id": 1 }, "name": "_id_" },
  { "key": { "salary": 1 }, "name": "salary_1" },
  { "key": { "email": 1 }, "name": "email_1", "unique": true }
]
```

---

### Q47. Compound index — Leftmost prefix rule

📌 **New Concept — Compound Index:** Index on multiple fields. MongoDB uses it for queries that filter on the **leftmost prefix** of the indexed fields. Queries on non-leftmost fields alone cannot use this index.

```javascript
db.employees.createIndex({ dept: 1, salary: -1 });
```

| Query | Uses Index? |
|---|---|
| `find({ dept: "Engineering" })` | ✅ Yes |
| `find({ dept: "Engineering", salary: { $gt: 70000 } })` | ✅ Yes |
| `find({ salary: { $gt: 70000 } })` | ❌ No — `salary` is not leftmost |

---

### Q48. Text index — Full-text search

📌 **New Concept — Text Index:** A special index for text search. Only one text index per collection. Supports `$text` operator with relevance scoring.

```javascript
db.products.createIndex({ name: "text", category: "text" });

db.products.find(
    { $text: { $search: "laptop wireless" } },
    { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```

**Output:**
```json
{ "_id": 2, "name": "Wireless Mouse", "score": 0.75 }
{ "_id": 1, "name": "Laptop Pro",     "score": 0.75 }
```

---

### Q49. TTL index — Auto-expire documents

📌 **New Concept — TTL Index:** A special index that automatically deletes documents after a specified number of seconds. Only works on `Date` fields. Used for sessions, OTP tokens, temp data.

```javascript
db.sessions.createIndex(
    { created_at: 1 },
    { expireAfterSeconds: 3600 }  // Delete 1 hour after created_at
);

// Insert a session:
db.sessions.insertOne({ user_id: 1, token: "abc123", created_at: new Date() });
// This document will be automatically deleted after 1 hour.
```

---

### Q50. EXPLAIN — Analyze query performance

📌 **New Concept — explain("executionStats"):** Shows the query execution plan. Look for `COLLSCAN` (collection scan = bad, no index) vs `IXSCAN` (index scan = good). Also check `totalDocsExamined` vs `nReturned` — they should be close.

```javascript
db.employees.find({ dept: "Engineering" }).explain("executionStats");
```

**Output (without index on dept — COLLSCAN):**
```json
{
  "queryPlanner": { "winningPlan": { "stage": "COLLSCAN" } },
  "executionStats": {
    "totalDocsExamined": 5,
    "nReturned": 2
  }
}
```

```javascript
db.employees.createIndex({ dept: 1 });
db.employees.find({ dept: "Engineering" }).explain("executionStats");
```

**Output (with index — IXSCAN):**
```json
{
  "queryPlanner": { "winningPlan": { "stage": "FETCH", "inputStage": { "stage": "IXSCAN" } } },
  "executionStats": {
    "totalDocsExamined": 2,
    "nReturned": 2
  }
}
```

---

## SECTION 4 — SCHEMA DESIGN & QUICK-FIRE Q&A (Q51–Q80)

---

### Q51. Embed vs Reference — When to use each

```javascript
// EMBED: User with addresses (1-to-few, always accessed together)
{
    _id: 1, name: "Alice",
    addresses: [
        { type: "home", city: "Mumbai", street: "MG Road" },
        { type: "work", city: "Pune",   street: "FC Road" }
    ]
}

// REFERENCE: Blog post with thousands of comments (1-to-many, unbounded growth)
// posts:    { _id: 1, title: "MongoDB Guide", author: "Alice" }
// comments: { _id: 101, post_id: 1, user: "Bob", text: "Great post!" }
```

---

### Q52. Product catalog with variable attributes (MongoDB advantage over SQL)

```javascript
// All in one collection — no need for ALTER TABLE when new attribute is added:
{ _id: 1, type: "Laptop",  name: "Pro 15", specs: { ram: "16GB", storage: "512GB", display: "15.6in" } }
{ _id: 2, type: "T-Shirt", name: "Basic",  specs: { sizes: ["S","M","L"], color: "Blue", material: "Cotton" } }
{ _id: 3, type: "Book",    name: "MongoDB Guide", specs: { pages: 420, isbn: "978-..." } }
```

---

### Q53–Q80: Quick-Fire Interview Q&A with Outputs

**Q53. What is the difference between `find()` and `aggregate()`?**
```javascript
// find() — Simple query, projection, sort, limit:
db.employees.find({ salary: { $gt: 80000 } }, { name: 1 }).sort({ salary: -1 });
// Output: [{ name: "Eve" }, { name: "Alice" }, { name: "Carol" }]

// aggregate() — Multi-stage transformation, grouping, joins:
db.employees.aggregate([
    { $match:  { salary: { $gt: 80000 } } },
    { $project: { name: 1 } },
    { $sort:   { salary: -1 } }
]);
// Same output — but aggregate allows $group, $lookup, etc.
```

**Q54. What happens to `$unwind` on empty array?**
```javascript
// Document: { _id: 1, name: "Test", skills: [] }
db.test.aggregate([{ $unwind: "$skills" }]);
// Output: [] — Empty array → document is REMOVED

// Fix with preserveNullAndEmptyArrays:
db.test.aggregate([{ $unwind: { path: "$skills", preserveNullAndEmptyArrays: true } }]);
// Output: { _id: 1, name: "Test", skills: null }
```

**Q55. Capped Collection — Fixed-size circular buffer**

📌 **New Concept — Capped Collection:** A fixed-size collection that overwrites the oldest documents when full. Insertion order preserved. Cannot delete individual documents.

```javascript
db.createCollection("audit_log", { capped: true, size: 1048576, max: 1000 });
// Stores max 1000 documents or 1MB (whichever comes first)
```

**Q56. Read preference options**
```javascript
db.getMongo().setReadPref("secondaryPreferred"); // Read from replica if available
// Options: primary, primaryPreferred, secondary, secondaryPreferred, nearest
```

**Q57. Write concern — Ensure data durability**
```javascript
db.orders.insertOne(
    { order_id: 999 },
    { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
);
// w:"majority" — wait for majority of replica set to acknowledge
// j:true — wait for journal write (disk durability)
```

**Q58. MongoDB ObjectId structure**
```javascript
ObjectId("507f1f77bcf86cd799439011")
//        |--4B--|--5B--|--3B--|
//        timestamp|random|counter
// 4 bytes = Unix timestamp (seconds since epoch)
// 5 bytes = random value
// 3 bytes = incrementing counter
// Result: auto-sorted by insertion time!
```

**Q59. Index covering query — No document fetch needed**
```javascript
db.employees.createIndex({ dept: 1, salary: 1, name: 1 });
// This query is fully COVERED — all needed fields are in the index:
db.employees.find({ dept: "Engineering" }, { salary: 1, name: 1, _id: 0 })
            .explain("executionStats");
// executionStats.totalDocsExamined = 0 (no document fetch!)
```

**Q60. MongoDB vs SQL — When to choose each**

| Scenario | MongoDB | SQL |
|---|---|---|
| Financial transactions | ❌ | ✅ (ACID critical) |
| Flexible/evolving schema | ✅ | ❌ |
| Complex multi-table reports | ❌ | ✅ |
| High write throughput (logs) | ✅ | ❌ |
| Embedded one-to-few data | ✅ | ❌ |
| Horizontal scale / sharding | ✅ (native) | ❌ (complex) |

**Q61–Q80 topics covered in [05_Rapid_Revision_Guide.md](./05_Rapid_Revision_Guide.md):** Replication, Sharding, CAP theorem application to MongoDB, Aggregation performance tips, Schema patterns (Bucket, Outlier, Polymorphic), and BSON data types.
