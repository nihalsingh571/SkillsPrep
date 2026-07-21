# MongoDB Complete Guide — CRUD, Aggregation, Indexes, Schema Design

> **80 queries covering all MongoDB interview topics from basics to FAANG-level**

---

## 1. BASICS & CRUD — Q1 to Q25

### Q1. Insert a single document
```javascript
db.employees.insertOne({
    name: "Alice",
    dept: "Engineering",
    salary: 90000,
    skills: ["Java", "MongoDB", "React"],
    address: { city: "Mumbai", pincode: "400001" },
    joined: new Date("2022-06-15"),
    isActive: true
});
```

---

### Q2. Insert multiple documents
```javascript
db.employees.insertMany([
    { name: "Bob", dept: "Marketing", salary: 65000, city: "Delhi" },
    { name: "Carol", dept: "Engineering", salary: 95000, city: "Bangalore" },
    { name: "David", dept: "HR", salary: 55000, city: "Mumbai" }
]);
```

---

### Q3. Find all documents in a collection
```javascript
db.employees.find({});
// With formatting:
db.employees.find({}).pretty();
```

---

### Q4. Find with conditions (WHERE equivalent)
```javascript
// WHERE salary > 70000 AND dept = 'Engineering'
db.employees.find({ salary: { $gt: 70000 }, dept: "Engineering" });

// WHERE salary BETWEEN 60000 AND 90000
db.employees.find({ salary: { $gte: 60000, $lte: 90000 } });
```

---

### Q5. Projection — Select specific fields (SELECT a, b FROM table)
```javascript
// Include only name and salary; exclude _id
db.employees.find({}, { name: 1, salary: 1, _id: 0 });

// Mix: Cannot combine inclusion and exclusion (except _id)
// This is INVALID: { name: 1, dept: 0 }
```
**Trap ⚠️:** Cannot mix inclusion (1) and exclusion (0) in projection, EXCEPT for `_id`.

---

### Q6. Comparison Operators
```javascript
db.employees.find({ salary: { $gt: 80000 } });   // >
db.employees.find({ salary: { $gte: 80000 } });  // >=
db.employees.find({ salary: { $lt: 50000 } });   // <
db.employees.find({ salary: { $lte: 50000 } });  // <=
db.employees.find({ salary: { $ne: 90000 } });   // != (includes documents with no salary field!)
db.employees.find({ dept: { $in: ["Engineering", "Marketing"] } });  // IN
db.employees.find({ dept: { $nin: ["HR"] } });  // NOT IN
```

---

### Q7. Logical Operators
```javascript
// AND (implicit — multiple conditions in same object):
db.employees.find({ dept: "Engineering", salary: { $gt: 80000 } });

// Explicit AND:
db.employees.find({ $and: [{ dept: "Engineering" }, { salary: { $gt: 80000 } }] });

// OR:
db.employees.find({ $or: [{ dept: "Engineering" }, { dept: "Marketing" }] });

// NOT:
db.employees.find({ salary: { $not: { $gt: 80000 } } });

// NOR (neither condition):
db.employees.find({ $nor: [{ dept: "HR" }, { salary: { $lt: 50000 } }] });
```

---

### Q8. Update a single document
```javascript
// Update Alice's salary
db.employees.updateOne(
    { name: "Alice" },           // Filter
    { $set: { salary: 95000 } }  // Update
);

// Increment salary by 5000
db.employees.updateOne(
    { name: "Alice" },
    { $inc: { salary: 5000 } }
);
```

---

### Q9. Update operators
```javascript
db.employees.updateOne(
    { _id: ObjectId("...") },
    {
        $set: { salary: 100000, city: "Pune" },  // Set field
        $unset: { temp_field: "" },               // Remove field
        $inc: { login_count: 1 },                 // Increment
        $push: { skills: "Kubernetes" },          // Add to array
        $pull: { skills: "Java" },               // Remove from array
        $addToSet: { skills: "Python" },          // Add to array only if not exists
        $rename: { "old_field": "new_field" }     // Rename field
    }
);
```

---

### Q10. Update multiple documents
```javascript
// Give 10% raise to all Engineering employees
db.employees.updateMany(
    { dept: "Engineering" },
    { $mul: { salary: 1.10 } }  // Multiply salary by 1.1
);
```

---

### Q11. Upsert — Insert if not exists
```javascript
db.employees.updateOne(
    { email: "new@example.com" },
    { $set: { name: "New Employee", salary: 70000 } },
    { upsert: true }  // Creates document if no match found
);
```

---

### Q12. Delete operations
```javascript
db.employees.deleteOne({ name: "Alice" });    // Delete first match
db.employees.deleteMany({ isActive: false }); // Delete all matches
db.employees.deleteMany({});                  // Delete ALL documents (table truncate equivalent)
```

---

### Q13. Sort, Limit, Skip (ORDER BY, LIMIT, OFFSET)
```javascript
db.employees.find({})
    .sort({ salary: -1 })  // -1 = DESC, 1 = ASC
    .limit(5)
    .skip(10);              // Skip first 10 (page 2)
```

---

### Q14. Query embedded/nested documents
```javascript
// WHERE address.city = 'Mumbai'
db.employees.find({ "address.city": "Mumbai" });

// Find employees in Engineering department with Mumbai address
db.employees.find({ dept: "Engineering", "address.city": "Mumbai" });
```

---

### Q15. Query arrays
```javascript
// Find employees who have 'Java' skill
db.employees.find({ skills: "Java" });  // Checks if array contains element

// Find employees with EXACTLY these skills:
db.employees.find({ skills: ["Java", "Python"] });  // Exact match

// $all — must contain all listed elements (in any order):
db.employees.find({ skills: { $all: ["Java", "Python"] } });

// $size — array has exactly N elements:
db.employees.find({ skills: { $size: 3 } });

// $elemMatch — element in array matches multiple conditions:
db.orders.find({ items: { $elemMatch: { qty: { $gt: 5 }, price: { $lt: 100 } } } });
```

---

### Q16. Existence and type checks
```javascript
// Documents where salary field EXISTS:
db.employees.find({ salary: { $exists: true } });

// Documents where salary field does NOT EXIST:
db.employees.find({ salary: { $exists: false } });

// Type check — only documents where salary is a number:
db.employees.find({ salary: { $type: "number" } });  // or $type: 1

// NULL check:
db.employees.find({ manager: null });  // Matches null OR missing field
db.employees.find({ manager: { $exists: true, $eq: null } });  // Only null, not missing
```

---

### Q17. Regular expressions
```javascript
// Names starting with 'A'
db.employees.find({ name: /^A/ });

// Case-insensitive search
db.employees.find({ name: { $regex: "alice", $options: "i" } });

// Contains 'eng' anywhere
db.employees.find({ dept: /eng/i });
```

---

### Q18. Counting documents
```javascript
db.employees.countDocuments({});                          // Total count
db.employees.countDocuments({ dept: "Engineering" });     // With filter
db.employees.estimatedDocumentCount();                    // Fast approximate count
```

---

### Q19. Distinct values (SELECT DISTINCT equivalent)
```javascript
db.employees.distinct("dept");            // All unique departments
db.employees.distinct("city", { salary: { $gt: 80000 } });  // With filter
```

---

### Q20. Replace a document entirely (vs update which patches)
```javascript
db.employees.replaceOne(
    { name: "Bob" },
    { name: "Bob", salary: 70000, dept: "Sales" }  // Completely replaces (loses old fields!)
);
```
**Trap ⚠️:** `replaceOne` replaces the ENTIRE document. `updateOne` with `$set` only modifies specified fields.

---

### Q21. Find documents with array containing specific value at specific position
```javascript
// Skills[0] must be "Java" (first skill = Java):
db.employees.find({ "skills.0": "Java" });
```

---

### Q22. Update a specific element in an array (positional operator $)
```javascript
// Update first element of scores array that equals 80 to 85
db.students.updateOne(
    { scores: 80 },
    { $set: { "scores.$": 85 } }
);
```

---

### Q23. Bulk operations
```javascript
db.employees.bulkWrite([
    { insertOne: { document: { name: "New1", salary: 60000 } } },
    { updateOne: { filter: { name: "Alice" }, update: { $inc: { salary: 5000 } } } },
    { deleteOne: { filter: { name: "Bob" } } }
]);
```

---

### Q24. findOneAndUpdate — Atomic find + update (returns old or new document)
```javascript
// Return the document AFTER update:
db.employees.findOneAndUpdate(
    { name: "Alice" },
    { $inc: { salary: 10000 } },
    { returnDocument: "after" }
);
```

---

### Q25. Transactions in MongoDB
```javascript
const session = db.getMongo().startSession();
session.startTransaction();
try {
    db.accounts.updateOne({ _id: 1 }, { $inc: { balance: -500 } }, { session });
    db.accounts.updateOne({ _id: 2 }, { $inc: { balance: +500 } }, { session });
    session.commitTransaction();
} catch (e) {
    session.abortTransaction();
} finally {
    session.endSession();
}
// Transactions require replica set (even single-node in MongoDB 4.0+)
```

---

## 2. AGGREGATION PIPELINE — Q26 to Q60

### Q26. Basic Aggregation — Average salary by department
```javascript
db.employees.aggregate([
    { $group: {
        _id: "$dept",
        avg_salary: { $avg: "$salary" },
        count: { $sum: 1 },
        max_salary: { $max: "$salary" },
        min_salary: { $min: "$salary" },
        total: { $sum: "$salary" }
    }}
]);
```

---

### Q27. $match — Filter before grouping (use EARLY to reduce pipeline size)
```javascript
db.employees.aggregate([
    { $match: { dept: "Engineering", salary: { $gt: 70000 } } },  // Filter first!
    { $group: { _id: "$city", count: { $sum: 1 } } }
]);
```
**Tip ⚠️:** Always put `$match` as early as possible in the pipeline to reduce documents processed.

---

### Q28. $project — Include, exclude, compute new fields
```javascript
db.employees.aggregate([
    { $project: {
        name: 1,
        salary: 1,
        _id: 0,
        annual_salary: { $multiply: ["$salary", 12] },  // New computed field
        name_upper: { $toUpper: "$name" }
    }}
]);
```

---

### Q29. $sort — Sort the output
```javascript
db.employees.aggregate([
    { $group: { _id: "$dept", avg_sal: { $avg: "$salary" } } },
    { $sort: { avg_sal: -1 } }  // Sort by avg salary descending
]);
```

---

### Q30. $limit and $skip
```javascript
db.employees.aggregate([
    { $sort: { salary: -1 } },
    { $skip: 10 },
    { $limit: 5 }
]);
```

---

### Q31. $lookup — JOIN two collections
```javascript
// Equivalent to LEFT JOIN employees ON departments
db.employees.aggregate([
    { $lookup: {
        from: "departments",        // Collection to join
        localField: "dept_id",      // Field in employees
        foreignField: "_id",        // Field in departments
        as: "department_info"       // Output array field name
    }},
    { $unwind: "$department_info" },  // Flatten the array (makes it INNER JOIN if no match = excluded)
    { $project: { name: 1, salary: 1, "department_info.dept_name": 1 } }
]);
```

---

### Q32. $lookup with pipeline (JOIN with conditions)
```javascript
db.orders.aggregate([
    { $lookup: {
        from: "products",
        let: { prod_id: "$product_id", min_amount: "$amount" },
        pipeline: [
            { $match: { $expr: { $eq: ["$$prod_id", "$_id"] } } },
            { $project: { name: 1, category: 1 } }
        ],
        as: "product_details"
    }}
]);
```

---

### Q33. $unwind — Deconstruct array fields
```javascript
// Document: { name: "Alice", skills: ["Java", "Python", "MongoDB"] }
db.employees.aggregate([
    { $unwind: "$skills" }
]);
// Produces 3 documents (one per skill):
// { name: "Alice", skills: "Java" }
// { name: "Alice", skills: "Python" }
// { name: "Alice", skills: "MongoDB" }
```
**Trap ⚠️:** `$unwind` on empty array removes the document. Use `preserveNullAndEmptyArrays: true` to keep it.

---

### Q34. Count skills frequency across all employees
```javascript
db.employees.aggregate([
    { $unwind: "$skills" },
    { $group: { _id: "$skills", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
]);
```

---

### Q35. $addFields — Add computed fields without hiding existing ones
```javascript
db.employees.aggregate([
    { $addFields: {
        monthly_salary: { $divide: ["$salary", 12] },
        seniority: {
            $cond: {
                if: { $gte: ["$years_exp", 5] },
                then: "Senior",
                else: "Junior"
            }
        }
    }}
]);
```

---

### Q36. $cond — Conditional logic (CASE WHEN equivalent)
```javascript
db.employees.aggregate([
    { $project: {
        name: 1,
        salary_band: {
            $switch: {
                branches: [
                    { case: { $lt: ["$salary", 50000] }, then: "Low" },
                    { case: { $lt: ["$salary", 80000] }, then: "Mid" },
                    { case: { $gte: ["$salary", 80000] }, then: "High" }
                ],
                default: "Unknown"
            }
        }
    }}
]);
```

---

### Q37. $facet — Multiple aggregations in one pass
```javascript
db.products.aggregate([
    { $facet: {
        by_category: [
            { $group: { _id: "$category", count: { $sum: 1 } } }
        ],
        price_stats: [
            { $group: { _id: null, avg: { $avg: "$price" }, max: { $max: "$price" } } }
        ],
        top_5_expensive: [
            { $sort: { price: -1 } },
            { $limit: 5 },
            { $project: { name: 1, price: 1 } }
        ]
    }}
]);
```

---

### Q38. $bucket — Price range grouping (histogram)
```javascript
db.products.aggregate([
    { $bucket: {
        groupBy: "$price",
        boundaries: [0, 1000, 5000, 20000, 100000],  // Range boundaries
        default: "Other",  // Bucket for values outside boundaries
        output: {
            count: { $sum: 1 },
            avg_price: { $avg: "$price" },
            products: { $push: "$name" }
        }
    }}
]);
```

---

### Q39. Top N per group — Top 3 earners per department
```javascript
db.employees.aggregate([
    { $sort: { salary: -1 } },
    { $group: {
        _id: "$dept",
        top_earners: { $push: { name: "$name", salary: "$salary" } }
    }},
    { $project: {
        dept: "$_id",
        top_3: { $slice: ["$top_earners", 3] }  // $slice to get first N elements
    }}
]);
```

---

### Q40. $out and $merge — Write aggregation result to a collection
```javascript
// Write to new collection (replaces if exists):
db.employees.aggregate([
    { $group: { _id: "$dept", avg_salary: { $avg: "$salary" } } },
    { $out: "dept_salary_summary" }
]);

// Merge into existing collection (upsert):
db.employees.aggregate([
    { $group: { _id: "$dept", avg_salary: { $avg: "$salary" } } },
    { $merge: {
        into: "dept_summary",
        on: "_id",
        whenMatched: "replace",
        whenNotMatched: "insert"
    }}
]);
```

---

### Q41. $count — Count pipeline results
```javascript
db.employees.aggregate([
    { $match: { salary: { $gt: 80000 } } },
    { $count: "high_earner_count" }
]);
```

---

### Q42. $group with $push — Collect all values (like GROUP_CONCAT)
```javascript
db.employees.aggregate([
    { $group: {
        _id: "$dept",
        employee_names: { $push: "$name" },
        unique_cities: { $addToSet: "$city" }  // addToSet = no duplicates
    }}
]);
```

---

### Q43. Date aggregation — Monthly order count
```javascript
db.orders.aggregate([
    { $group: {
        _id: {
            year: { $year: "$order_date" },
            month: { $month: "$order_date" }
        },
        count: { $sum: 1 },
        revenue: { $sum: "$amount" }
    }},
    { $sort: { "_id.year": 1, "_id.month": 1 } }
]);
```

---

### Q44. String operations in aggregation
```javascript
db.employees.aggregate([
    { $project: {
        full_name: { $concat: ["$first_name", " ", "$last_name"] },
        upper_dept: { $toUpper: "$dept" },
        name_length: { $strLenCP: "$name" },
        trimmed: { $trim: { input: "$name" } }
    }}
]);
```

---

### Q45. $lookup with $unwind and $match — Find employees with dept info
```javascript
db.employees.aggregate([
    { $lookup: {
        from: "departments",
        localField: "dept_id",
        foreignField: "_id",
        as: "dept"
    }},
    { $unwind: { path: "$dept", preserveNullAndEmptyArrays: true } },  // LEFT JOIN
    { $match: { "dept.location": "Mumbai" } },
    { $project: { name: 1, salary: 1, dept_name: "$dept.name" } }
]);
```

---

### Q46. $replaceRoot — Promote embedded document to root
```javascript
db.employees.aggregate([
    { $replaceRoot: { newRoot: "$address" } }
]);
// Replaces the entire document with the 'address' subdocument
```

---

### Q47. Graph lookup — Find all ancestors in a hierarchy
```javascript
db.employees.aggregate([
    { $match: { emp_id: 15 } },  // Start from this employee
    { $graphLookup: {
        from: "employees",
        startWith: "$manager_id",
        connectFromField: "manager_id",
        connectToField: "emp_id",
        as: "management_chain",
        depthField: "depth"
    }}
]);
```

---

### Q48. $sample — Random sample of documents
```javascript
// Get 10 random employees
db.employees.aggregate([
    { $sample: { size: 10 } }
]);
```

---

### Q49. Using $expr — Compare fields within same document
```javascript
// Find orders where amount > budget (two fields in same document)
db.projects.find({ $expr: { $gt: ["$spent", "$budget"] } });

// In aggregation:
db.orders.aggregate([
    { $match: { $expr: { $gte: ["$actual_delivery", "$promised_delivery"] } } }
]);
```

---

### Q50. Aggregation performance best practices
```javascript
// ✅ GOOD: Match and project early, reduce pipeline data early
db.orders.aggregate([
    { $match: { status: "PENDING", order_date: { $gte: new Date("2024-01-01") } } },  // Filter first!
    { $project: { customer_id: 1, amount: 1 } },  // Project early!
    { $group: { _id: "$customer_id", total: { $sum: "$amount" } } }
]);

// ❌ BAD: Group first (processes all documents), then match
db.orders.aggregate([
    { $group: { _id: "$customer_id", orders: { $push: "$$ROOT" } } },  // All docs grouped
    { $match: { "orders.status": "PENDING" } }  // Then filtered
]);
```

---

## 3. INDEXES — Q51 to Q65

### Q51. Create a single field index
```javascript
db.employees.createIndex({ salary: 1 });           // ASC index
db.employees.createIndex({ dept: -1 });            // DESC index
db.employees.createIndex({ email: 1 }, { unique: true }); // Unique index
```

---

### Q52. Compound index
```javascript
db.employees.createIndex({ dept: 1, salary: -1 });
// Helps queries filtering by: dept only, or dept + salary
// Does NOT help queries filtering by: salary only (leftmost prefix rule!)
```

---

### Q53. Text index (full-text search)
```javascript
db.products.createIndex({ name: "text", description: "text" });
db.products.find({ $text: { $search: "wireless bluetooth" } });
// Score relevance:
db.products.find(
    { $text: { $search: "wireless" } },
    { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```

---

### Q54. Geospatial index
```javascript
db.restaurants.createIndex({ location: "2dsphere" });
// Find restaurants within 5km:
db.restaurants.find({
    location: {
        $near: {
            $geometry: { type: "Point", coordinates: [72.8, 19.0] },
            $maxDistance: 5000  // meters
        }
    }
});
```

---

### Q55. Partial index — Index only active users
```javascript
db.users.createIndex(
    { email: 1 },
    { partialFilterExpression: { isActive: true } }
);
// Smaller index — only indexes active users
```

---

### Q56. TTL index — Auto-expire documents
```javascript
// Automatically delete documents 1 hour after 'created_at'
db.sessions.createIndex(
    { created_at: 1 },
    { expireAfterSeconds: 3600 }
);
```
**Interview Tip:** TTL indexes are perfect for session data, OTP tokens, cache collections.

---

### Q57. Use EXPLAIN to analyze query performance
```javascript
db.employees.find({ dept: "Engineering" }).explain("executionStats");
// Look for:
// - COLLSCAN = bad (no index used)
// - IXSCAN = good (index used)
// - totalDocsExamined vs nReturned (should be close for good queries)
```

---

### Q58. List and manage indexes
```javascript
db.employees.getIndexes();            // List all indexes
db.employees.dropIndex("salary_1");   // Drop by name
db.employees.dropIndexes();           // Drop ALL indexes (except _id)
```

---

## 4. SCHEMA DESIGN — Q59 to Q70

### Q59. Embedding vs Referencing — When to embed
```javascript
// EMBED when:
// - Data is frequently accessed together
// - One-to-few relationship (not one-to-many with thousands)
// - Child data doesn't need independent access

// Example: User with addresses (1:few — embed)
{
    _id: ObjectId("..."),
    name: "Alice",
    addresses: [
        { type: "home", city: "Mumbai", street: "MG Road" },
        { type: "work", city: "Pune", street: "FC Road" }
    ]
}

// REFERENCE when:
// - Data grows unboundedly (comments on a viral post)
// - Data needs independent access/queries
// - Many-to-many relationships
// - Data is shared across multiple parent documents
```

---

### Q60. Product catalog schema — Handling variable attributes
```javascript
// Flexible approach using attributes array:
{
    _id: ObjectId("..."),
    name: "Laptop Pro 15",
    category: "Electronics",
    price: 75000,
    attributes: [
        { name: "RAM", value: "16GB" },
        { name: "Storage", value: "512GB SSD" },
        { name: "Display", value: "15.6 inch" }
    ],
    // Or using Map/object for direct access:
    specs: {
        ram: "16GB",
        storage: "512GB",
        display: "15.6 inch"
    }
}
```

---

### Q61. One-to-Many — Blog posts and comments
```javascript
// Option 1: Embed comments (good for < 100 comments per post)
{
    post_id: 1,
    title: "MongoDB Tutorial",
    comments: [
        { user: "Alice", text: "Great post!", date: ISODate("...") },
        { user: "Bob", text: "Very helpful.", date: ISODate("...") }
    ]
}

// Option 2: Reference (for viral posts with thousands of comments)
// posts collection: { _id, title, author, content }
// comments collection: { _id, post_id, user, text, date }
// INDEX: db.comments.createIndex({ post_id: 1, date: -1 })
```

---

### Q62. Many-to-Many — Students and Courses
```javascript
// Option 1: Two-way embedding (avoid — data duplication)
// Option 2: Reference with junction
// students: { _id, name, course_ids: [1, 2, 3] }
// courses: { _id, name, student_count }
// enrollments collection: { student_id, course_id, enrolled_date, grade }
```

---

### Q63. Bucket pattern — Time-series data
```javascript
// Instead of one document per sensor reading (millions of docs):
// Store 1 hour of readings per document:
{
    sensor_id: "temp_01",
    date: ISODate("2024-01-15T10:00:00Z"),
    count: 60,  // Readings in this hour
    readings: [
        { ts: ISODate("2024-01-15T10:01:00Z"), value: 22.5 },
        { ts: ISODate("2024-01-15T10:02:00Z"), value: 22.6 },
        // ... 60 readings
    ],
    min: 22.1, max: 23.0, avg: 22.5  // Pre-computed summary
}
```

---

### Q64. Polymorphic pattern — Different product types in one collection
```javascript
// All products in one collection, with type-specific fields:
{ type: "Book", title: "MongoDB Guide", author: "Joe", isbn: "..." }
{ type: "Movie", title: "Inception", director: "Nolan", duration: 148 }
{ type: "Album", title: "Thriller", artist: "MJ", tracks: 9 }
// Index on 'type' for filtering
```

---

### Q65. Outlier pattern — Handling viral posts
```javascript
// Normal post: { _id, content, likes_count: 245, likes: [user1, user2, ...] }
// Viral post: { _id, content, likes_count: 2500000, has_extras: true }
// extras collection: { post_id, page: 1, users: [user1...user1000] }
```

---

## 5. REPLICATION, SHARDING & TRANSACTIONS — Q66 to Q80

### Q66. Replica set write concerns
```javascript
// Write acknowledged by majority of replica set members:
db.orders.insertOne(
    { order_id: 123, amount: 5000 },
    { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
);
// w: "majority" — wait for majority acknowledgment (strong consistency)
// j: true — wait for journal write (durability)
// wtimeout: 5000 — timeout in ms
```

---

### Q67. Read preference — Reading from replicas
```javascript
// Read from nearest replica (may be slightly stale — eventual consistency):
db.getMongo().setReadPref("nearest");

// Read preferences:
// primary — Always read from primary (default, strong consistency)
// primaryPreferred — Primary if available, else secondary
// secondary — Always from secondary (may be stale!)
// secondaryPreferred — Secondary if available, else primary
// nearest — Least network latency
```

---

### Q68. Explain sharding
```javascript
// Shard a collection on customer_id (range sharding):
sh.enableSharding("ecommerce");
sh.shardCollection("ecommerce.orders", { customer_id: 1 });

// Hash sharding (even distribution):
sh.shardCollection("ecommerce.orders", { customer_id: "hashed" });

// Check which shard a document goes to:
db.orders.explain().find({ customer_id: 5 });
```

---

### Q69. MongoDB ACID multi-document transaction
```javascript
// Full bank transfer:
const session = client.startSession();
session.startTransaction({
    readConcern: { level: "snapshot" },
    writeConcern: { w: "majority" }
});
try {
    await db.accounts.updateOne(
        { _id: fromAccount },
        { $inc: { balance: -amount } },
        { session }
    );
    await db.accounts.updateOne(
        { _id: toAccount },
        { $inc: { balance: +amount } },
        { session }
    );
    await db.transactions.insertOne(
        { from: fromAccount, to: toAccount, amount, ts: new Date() },
        { session }
    );
    await session.commitTransaction();
} catch (error) {
    await session.abortTransaction();
    throw error;
} finally {
    await session.endSession();
}
```

---

### Q70-Q80: Quick-Fire MongoDB Interview Questions

**Q70. What is the _id field?**
Every MongoDB document has a unique `_id`. Defaults to `ObjectId` (12-byte BSON type: 4-byte timestamp + 5-byte random + 3-byte counter). Can be any unique value.

**Q71. What is the difference between find() and aggregate()?**
`find()`: Simple queries, projection, sort, skip, limit. Returns cursor.
`aggregate()`: Complex transformations, joins ($lookup), grouping, computed fields, multiple stages. More powerful.

**Q72. What is the MongoDB aggregation pipeline?**
A sequence of stages where each stage transforms documents. Output of one stage is input to next. Like Unix pipes for data.

**Q73. What are the stages of the aggregation pipeline?**
`$match` → `$project` → `$group` → `$sort` → `$limit` → `$skip` → `$lookup` → `$unwind` → `$addFields` → `$replaceRoot` → `$facet` → `$out`

**Q74. What is $unwind and what happens to empty arrays?**
`$unwind` deconstructs an array field — creates one document per array element. Empty array or null field = document is removed. Fix: `{ $unwind: { path: "$field", preserveNullAndEmptyArrays: true } }`

**Q75. What is a capped collection?**
Fixed-size collection that automatically overwrites oldest documents when size limit is reached. Like a circular buffer. Used for logs, audit trails.
```javascript
db.createCollection("audit_log", { capped: true, size: 10485760, max: 1000 });
```

**Q76. What is MongoDB's BSON?**
Binary JSON. MongoDB's internal data format. Supports additional types not in JSON: `Date`, `ObjectId`, `Binary`, `Decimal128`, `Int32/Int64`. More efficient to encode/decode than JSON.

**Q77. How does MongoDB ensure consistency?**
Single document operations are atomic. Multi-document requires explicit transactions (supported since MongoDB 4.0 with replica sets). By default, MongoDB prioritizes availability over consistency (AP in CAP theorem), but can be tuned.

**Q78. When would you use MongoDB over MySQL?**
- Flexible/evolving schema (no ALTER TABLE pain)
- Document-oriented data (JSON API responses cached as-is)
- Horizontal scaling required (native sharding)
- High write throughput
- Embedded documents are natural (avoid joins)
- Real-time analytics with aggregation pipeline

**Q79. What is indexCovering in MongoDB?**
When all fields needed by a query are in the index — MongoDB can answer the query without reading actual documents (like a covering index in SQL). 
```javascript
db.employees.createIndex({ dept: 1, salary: 1, name: 1 });
db.employees.find({ dept: "Engineering" }, { salary: 1, name: 1, _id: 0 });
// All fields in index → covered query!
```

**Q80. What is the difference between $match and $filter?**
`$match`: Pipeline stage — filters DOCUMENTS in the collection.
`$filter`: Expression operator — filters ELEMENTS within an array field inside a document.
```javascript
// $filter example — show only high-value items in an order:
db.orders.aggregate([
    { $project: {
        order_id: 1,
        expensive_items: {
            $filter: {
                input: "$items",
                as: "item",
                cond: { $gte: ["$$item.price", 1000] }
            }
        }
    }}
]);
```
