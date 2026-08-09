# 🌐 API & REST API — Complete Notes
*From zero to interview-ready. Simple language, real code, no fluff.*

---

## PART 1: WHAT IS AN API?

### The Simple Explanation

Imagine you're at a restaurant. You (the customer) don't go into the kitchen to cook your food. Instead, you tell the **waiter** what you want. The waiter goes to the kitchen, gets your food, and brings it back.

**API = The Waiter.**

An **API (Application Programming Interface)** is a messenger that takes your request to a system, gets what you need, and brings it back.

```
Your App  ──── API Request ────▶  Server/Database
Your App  ◀─── API Response ────  Server/Database
```

### Real-World Examples

| You use... | It calls API of... |
|---|---|
| Google Maps in Swiggy | Google Maps API |
| "Login with Google" | Google OAuth API |
| Weather widget on your phone | OpenWeatherMap API |
| UPI payment in any app | Payment gateway API |
| Instagram in a 3rd party app | Instagram API |

---

## PART 2: TYPES OF APIs

### 1. REST API (Most Common)
Uses HTTP. Data in JSON format. What you'll use 90% of the time.

### 2. SOAP API (Old, Enterprise)
Uses XML. Very strict rules. Used in banking and government systems. You won't build one but may hear about it.

### 3. GraphQL API
You ask for exactly what you want — no more, no less. Created by Facebook. Used when REST sends too much data.

### 4. WebSocket API
Two-way, real-time connection. Used in chat apps, live dashboards. (Socket.IO uses this.)

### 5. Webhook
Not a request you make — the server **calls you** when something happens.
Example: Stripe calls your URL when a payment is successful.

---

## PART 3: REST API — THE MAIN THING TO LEARN

### What is REST?

**REST = Representational State Transfer**

It's not a library or a framework. It's a **set of rules** for designing APIs.

Think of REST like the rules of cricket. Cricket defines how to play the game — REST defines how to design an API.

### The 6 Rules of REST (Constraints)

| Rule | What it means | Simple example |
|---|---|---|
| **Client-Server** | Frontend and backend are separate | React app calls Node.js API |
| **Stateless** | Each request is independent. Server remembers nothing between requests | Send JWT token every time |
| **Cacheable** | Responses can be stored/reused | Browser caches GET /products |
| **Uniform Interface** | Consistent URL and data format | Always use JSON, standard URLs |
| **Layered System** | Client doesn't know if it's talking to server or a proxy | Load balancer in between |
| **Code on Demand** (optional) | Server can send executable code | Sending JS to browser |

---

## PART 4: HTTP METHODS — THE VERBS

Every REST API request uses an HTTP **method** (also called a verb) to say what action you want.

```
CRUD Operation    HTTP Method    Meaning
─────────────────────────────────────────
Create         →  POST          Add something new
Read           →  GET           Fetch something
Update         →  PUT / PATCH   Change something
Delete         →  DELETE        Remove something
```

### Difference Between PUT and PATCH

```
PUT   = Replace the ENTIRE resource
PATCH = Update ONLY specific fields

Example — User object: { name: "Nihal", email: "x@y.com", age: 21 }

PUT /users/1    → you must send ALL fields: { name, email, age }
                  Missing fields get deleted or set to null

PATCH /users/1  → you only send what changed: { age: 22 }
                  Everything else stays the same
```

---

## PART 5: HTTP STATUS CODES — WHAT THE SERVER TELLS YOU BACK

Always memorize these. Interviewers love asking.

### 2xx — Success ✅
| Code | Meaning | When to use |
|---|---|---|
| **200** | OK | GET request succeeded |
| **201** | Created | POST succeeded, new resource created |
| **204** | No Content | DELETE succeeded, nothing to return |

### 3xx — Redirection 🔀
| Code | Meaning | When to use |
|---|---|---|
| **301** | Moved Permanently | URL has changed forever |
| **302** | Found (Temporary Redirect) | URL temporarily different |

### 4xx — Client Error (YOU messed up) ❌
| Code | Meaning | When to use |
|---|---|---|
| **400** | Bad Request | Invalid data sent (missing required field) |
| **401** | Unauthorized | Not logged in / no token |
| **403** | Forbidden | Logged in but no permission |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate (user with email already exists) |
| **422** | Unprocessable Entity | Data format wrong (string where number expected) |
| **429** | Too Many Requests | Rate limit exceeded |

### 5xx — Server Error (SERVER messed up) 🔥
| Code | Meaning | When to use |
|---|---|---|
| **500** | Internal Server Error | Unhandled exception in server code |
| **502** | Bad Gateway | Upstream server failed (nginx → app server) |
| **503** | Service Unavailable | Server overloaded or down for maintenance |
| **504** | Gateway Timeout | Upstream server too slow |

### 401 vs 403 — The Most Confused Pair

```
401 Unauthorized = "Who are you? Show me your ID."
    → No token, expired token, invalid token
    → Fix: Log in again

403 Forbidden = "I know who you are, but you can't come in."
    → Token is valid, but role doesn't have permission
    → Fix: Ask admin for access
```

---

## PART 6: URL DESIGN — HOW TO NAME YOUR ROUTES

### Rules for Clean REST URLs

```
✅ GOOD                      ❌ BAD
─────────────────────────────────────────────────────
GET    /users                GET /getUsers
GET    /users/42             GET /getUserById?id=42
POST   /users                POST /createUser
PUT    /users/42             POST /updateUser
DELETE /users/42             GET  /deleteUser?id=42
GET    /users/42/posts       GET  /getPostsOfUser?userId=42
```

### Rules to Remember

1. **Use nouns, not verbs** in URLs (the HTTP method IS the verb)
2. **Use plural** resource names: `/users`, `/products`, `/orders`
3. **Use lowercase and hyphens**: `/maintenance-requests` not `/maintenanceRequests`
4. **Nest for relationships**: `/users/42/orders` (orders belonging to user 42)
5. **Version your API**: `/api/v1/users` (so you can change v2 without breaking old clients)

### Query Parameters vs Path Parameters

```
Path Parameter   → Part of the URL, identifies a specific resource
/users/42        → Get user with ID 42

Query Parameter  → After ?, filters or options
/users?role=admin&page=2   → Get users with role=admin, page 2

RULE: Use path params for IDs, query params for filters/sorting/pagination
```

---

## PART 7: REQUEST AND RESPONSE STRUCTURE

### Anatomy of an HTTP Request

```
POST /api/v1/users HTTP/1.1
Host: api.propsync.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

{
  "name": "Nihal Singh",
  "email": "nihal@example.com",
  "password": "securePass123",
  "role": "tenant"
}

│                   │
│    HEADERS        │  ← Metadata (who you are, what format you're sending)
│                   │
│    BODY           │  ← The actual data (only in POST, PUT, PATCH)
```

### Anatomy of an HTTP Response

```
HTTP/1.1 201 Created
Content-Type: application/json
X-Request-Id: abc-123

{
  "success": true,
  "data": {
    "id": "64f3b...",
    "name": "Nihal Singh",
    "email": "nihal@example.com",
    "role": "tenant",
    "createdAt": "2024-01-15T10:30:00Z"
  },
  "message": "User created successfully"
}
```

### Standard API Response Format (Use This Always)

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "error": null
}

// On error:
{
  "success": false,
  "data": null,
  "message": "Email already exists",
  "error": {
    "code": "DUPLICATE_EMAIL",
    "field": "email"
  }
}
```

---

## PART 8: HEADERS — THE IMPORTANT ONES

```
Request Headers (you send these):
──────────────────────────────────────────────────────
Content-Type: application/json      ← "I'm sending JSON data"
Authorization: Bearer <token>       ← "Here is my JWT token"
Accept: application/json            ← "I want JSON back"
X-API-Key: abc123                   ← "Here's my API key"

Response Headers (server sends these):
──────────────────────────────────────────────────────
Content-Type: application/json      ← "I'm sending you JSON"
X-RateLimit-Remaining: 99           ← "You have 99 requests left"
Cache-Control: max-age=3600         ← "Cache this for 1 hour"
Set-Cookie: session=xyz; HttpOnly   ← "Store this cookie"
```

---

## PART 9: AUTHENTICATION vs AUTHORIZATION

People confuse these constantly. Remember:

```
Authentication = WHO are you?   (Login, verify identity)
Authorization  = WHAT can you do? (Permissions, roles)

Flow:
1. User logs in → Server verifies credentials → Authentication ✓
2. User requests /admin/delete-user → Server checks role → Authorization
```

### How JWT Works End-to-End

```
1. User sends: POST /login { email, password }

2. Server:
   - Finds user in DB ✓
   - Verifies password with bcrypt ✓
   - Creates JWT token and sends back

3. JWT Token Structure (3 parts, dot-separated):
   header.payload.signature

   Header:  { "alg": "HS256", "typ": "JWT" }    → base64 encoded
   Payload: { "userId": "42", "role": "admin",
              "exp": 1700000000 }                → base64 encoded
   Signature: HMACSHA256(header + "." + payload,
                          SECRET_KEY)            → verifies it wasn't tampered

4. Client stores JWT (localStorage or httpOnly cookie)

5. Every future request:
   Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

6. Server middleware decodes token, checks signature,
   checks expiry, extracts userId and role → continues
```

> ⚠️ **JWT is NOT encrypted** — payload is only base64 encoded (anyone can decode it). Never put passwords in JWT payload. It's just signed — tampering is detectable, but contents are readable.

---

## PART 10: COMPLETE NODE.JS + EXPRESS REST API

### Project Setup

```bash
mkdir my-api && cd my-api
npm init -y
npm install express mongoose bcryptjs jsonwebtoken dotenv cors
npm install --save-dev nodemon
```

### Full API — `server.js`

```javascript
// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const userRoutes = require('./routes/users');

const app = express();

// ── Middleware ────────────────────────────────────────
app.use(cors());                        // Allow cross-origin requests
app.use(express.json());                // Parse JSON request body
app.use(express.urlencoded({ extended: true })); // Parse form data

// ── Routes ────────────────────────────────────────────
app.use('/api/v1/users', userRoutes);

// ── 404 Handler ───────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route ${req.method} ${req.url} not found`
  });
});

// ── Global Error Handler ──────────────────────────────
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Internal Server Error'
  });
});

// ── Connect DB & Start ────────────────────────────────
mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    console.log('MongoDB connected');
    app.listen(process.env.PORT || 3000, () => {
      console.log(`Server running on port ${process.env.PORT || 3000}`);
    });
  })
  .catch(err => {
    console.error('DB connection failed:', err);
    process.exit(1);
  });
```

### User Model — `models/User.js`

```javascript
// models/User.js
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    minlength: [2, 'Name must be at least 2 characters']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,               // Creates a DB index, prevents duplicates
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Please provide a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters'],
    select: false               // Never returned in queries by default
  },
  role: {
    type: String,
    enum: ['admin', 'owner', 'tenant', 'maintenance'],
    default: 'tenant'
  }
}, {
  timestamps: true              // Adds createdAt and updatedAt automatically
});

// Hash password BEFORE saving (pre-save hook)
userSchema.pre('save', async function(next) {
  // Only hash if password was modified (not on every save)
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12); // 12 salt rounds
  next();
});

// Method to compare passwords during login
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

### Auth Middleware — `middleware/auth.js`

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Verify JWT token
const protect = async (req, res, next) => {
  try {
    // 1. Get token from header
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        message: 'No token provided. Please log in.'
      });
    }

    const token = authHeader.split(' ')[1];  // "Bearer TOKEN" → TOKEN

    // 2. Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    // If invalid or expired, jwt.verify throws an error → caught below

    // 3. Find user from token payload
    const user = await User.findById(decoded.userId);
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User no longer exists'
      });
    }

    // 4. Attach user to request for downstream use
    req.user = user;
    next();

  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ success: false, message: 'Invalid token' });
    }
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ success: false, message: 'Token expired. Please log in again.' });
    }
    next(error);
  }
};

// Role-based authorization
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: `Role '${req.user.role}' is not authorized for this action`
      });
    }
    next();
  };
};

module.exports = { protect, authorize };
```

### Routes — `routes/users.js`

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const {
  register,
  login,
  getMe,
  getAllUsers,
  updateUser,
  deleteUser
} = require('../controllers/userController');
const { protect, authorize } = require('../middleware/auth');

// Public routes (no token needed)
router.post('/register', register);   // POST /api/v1/users/register
router.post('/login', login);         // POST /api/v1/users/login

// Protected routes (token required)
router.get('/me', protect, getMe);    // GET  /api/v1/users/me

// Admin-only routes (token + admin role required)
router.get('/', protect, authorize('admin'), getAllUsers);
router.put('/:id', protect, authorize('admin', 'owner'), updateUser);
router.delete('/:id', protect, authorize('admin'), deleteUser);

module.exports = router;
```

### Controllers — `controllers/userController.js`

```javascript
// controllers/userController.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Helper to generate JWT
const generateToken = (userId) => {
  return jwt.sign(
    { userId },                           // Payload
    process.env.JWT_SECRET,               // Secret key
    { expiresIn: process.env.JWT_EXPIRE || '7d' }  // Expiry
  );
};

// ── POST /register ─────────────────────────────────────
exports.register = async (req, res, next) => {
  try {
    const { name, email, password, role } = req.body;

    // Check if email already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({
        success: false,
        message: 'Email already registered'
      });
    }

    // Create user (password is hashed by pre-save hook in model)
    const user = await User.create({ name, email, password, role });

    // Generate token
    const token = generateToken(user._id);

    res.status(201).json({
      success: true,
      token,
      data: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role
      },
      message: 'Registration successful'
    });

  } catch (error) {
    next(error);  // Pass to global error handler
  }
};

// ── POST /login ────────────────────────────────────────
exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Please provide email and password'
      });
    }

    // Find user (select: false on password, so we explicitly select it)
    const user = await User.findOne({ email }).select('+password');
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'  // Don't reveal which one is wrong!
      });
    }

    // Check password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'
      });
    }

    const token = generateToken(user._id);

    res.status(200).json({
      success: true,
      token,
      data: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role
      },
      message: 'Login successful'
    });

  } catch (error) {
    next(error);
  }
};

// ── GET /me ────────────────────────────────────────────
exports.getMe = async (req, res, next) => {
  try {
    // req.user is set by the protect middleware
    res.status(200).json({
      success: true,
      data: req.user,
      message: 'Profile fetched'
    });
  } catch (error) {
    next(error);
  }
};

// ── GET / (all users, admin only) ─────────────────────
exports.getAllUsers = async (req, res, next) => {
  try {
    // Pagination
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    // Filtering by role
    const filter = {};
    if (req.query.role) filter.role = req.query.role;

    const users = await User.find(filter)
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 });  // Newest first

    const total = await User.countDocuments(filter);

    res.status(200).json({
      success: true,
      data: users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    next(error);
  }
};

// ── PUT /:id ──────────────────────────────────────────
exports.updateUser = async (req, res, next) => {
  try {
    const { name, email } = req.body;

    // findByIdAndUpdate with { new: true } returns the UPDATED document
    const user = await User.findByIdAndUpdate(
      req.params.id,
      { name, email },
      { new: true, runValidators: true }  // runValidators: applies schema rules
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.status(200).json({
      success: true,
      data: user,
      message: 'User updated'
    });
  } catch (error) {
    next(error);
  }
};

// ── DELETE /:id ───────────────────────────────────────
exports.deleteUser = async (req, res, next) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.status(204).send();  // 204 = No Content (success, nothing to return)
  } catch (error) {
    next(error);
  }
};
```

### `.env` file

```bash
PORT=3000
MONGO_URI=mongodb://localhost:27017/myapi
JWT_SECRET=your_super_secret_key_here_make_it_long_and_random
JWT_EXPIRE=7d
```

---

## PART 11: API BEST PRACTICES

### 1. Always Validate Input

```javascript
// Bad — trusting user input directly
const user = await User.create(req.body);

// Good — validate first
const { name, email, password } = req.body;
if (!name || !email || !password) {
  return res.status(400).json({ success: false, message: 'All fields required' });
}
```

### 2. Never Expose Sensitive Data

```javascript
// Bad — password returned in response
res.json({ user }); // includes password!

// Good — explicitly select what to return
res.json({
  data: { id: user._id, name: user.name, email: user.email }
});
```

### 3. Use Consistent Error Messages

```javascript
// Bad — different formats in different routes
res.send("error");
res.json({ err: "not found" });

// Good — same structure everywhere
res.status(404).json({
  success: false,
  message: 'User not found'
});
```

### 4. Implement Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                    // Max 100 requests per window
  message: {
    success: false,
    message: 'Too many requests. Please try again after 15 minutes.'
  }
});

app.use('/api', limiter);
```

### 5. Paginate Large Lists

```javascript
// Bad — return all 100,000 users at once
const users = await User.find();

// Good — paginate
const page = parseInt(req.query.page) || 1;
const limit = parseInt(req.query.limit) || 10;
const users = await User.find().skip((page - 1) * limit).limit(limit);
```

### 6. Version Your API

```javascript
// Good — version in URL
app.use('/api/v1/users', v1UserRoutes);
app.use('/api/v2/users', v2UserRoutes);  // New version, old still works
```

### 7. Log All Requests

```javascript
const morgan = require('morgan');
app.use(morgan('dev'));  // Logs: GET /api/v1/users 200 23ms
```

---

## PART 12: IDEMPOTENCY — ONE OF THE MOST ASKED INTERVIEW TOPICS

**Idempotent** = Making the same request multiple times gives the same result.

```
Method      Idempotent?   Safe (no side effects)?
──────────────────────────────────────────────────
GET         ✅ Yes         ✅ Yes
POST        ❌ No          ❌ No
PUT         ✅ Yes         ❌ No
PATCH       ❌ No*         ❌ No
DELETE      ✅ Yes         ❌ No

* PATCH CAN be idempotent (set name="Nihal" twice = same result)
  but it ISN'T always (increment counter by 1 = different result each time)
```

**Why it matters:**
- If a network error occurs and the client retries, a POST creates duplicate orders
- Solution: Use **idempotency keys** — unique IDs the client sends, server checks if already processed

---

## PART 13: CORS — WHY YOUR API BLOCKS BROWSER REQUESTS

```
CORS = Cross-Origin Resource Sharing

Origin = protocol + domain + port
http://localhost:3000  ≠  http://localhost:5173  (different port = different origin)

Browser Rule: Scripts can only fetch from the SAME origin.
CORS = A way for the SERVER to say "it's okay to let other origins access me"

Flow:
Browser: "I'm from localhost:5173, can I call localhost:3000/api/users?"
Server response header: "Access-Control-Allow-Origin: http://localhost:5173"
Browser: "OK, allowed!" → Makes the real request
```

```javascript
// Express CORS setup
const cors = require('cors');

// Allow specific origins (production)
app.use(cors({
  origin: ['https://myapp.com', 'https://www.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true  // Allow cookies to be sent cross-origin
}));

// Allow all origins (development only — never in production!)
app.use(cors());
```

---

## PART 14: QUICK REFERENCE CHEAT SHEET

```
HTTP Method  │  Action           │  URL Example           │  Response Code
─────────────┼───────────────────┼────────────────────────┼───────────────
GET          │  List all         │  /api/users            │  200
GET          │  Get one          │  /api/users/42         │  200 or 404
POST         │  Create           │  /api/users            │  201
PUT          │  Replace all      │  /api/users/42         │  200
PATCH        │  Update partial   │  /api/users/42         │  200
DELETE       │  Delete           │  /api/users/42         │  204 or 200

Status Code Quick Reference:
200 OK │ 201 Created │ 204 No Content
400 Bad Request │ 401 Unauthorized │ 403 Forbidden │ 404 Not Found │ 409 Conflict
500 Server Error │ 503 Service Unavailable
```

---

## PART 15: TOP 10 API INTERVIEW QUESTIONS (WORLD-CLASS)

---

### Q1: What is the difference between REST and SOAP?

**What they're testing:** Basic API knowledge and ability to compare technologies.

**Answer:**

REST (Representational State Transfer) and SOAP (Simple Object Access Protocol) are two different approaches to building APIs.

| Feature | REST | SOAP |
|---|---|---|
| Data format | JSON (usually), also XML | XML only |
| Protocol | HTTP | HTTP, SMTP, TCP |
| Performance | Fast, lightweight | Slower, heavy XML |
| Flexibility | Flexible | Strict standards |
| Caching | Supports caching | Doesn't support caching |
| Use case | Web/mobile apps | Enterprise, banking, government |
| Learning curve | Easy | Complex |

**REST Example:**
```
GET /users/42
Response: { "id": 42, "name": "Nihal" }
```

**SOAP Example:**
```xml
<soap:Envelope>
  <soap:Body>
    <GetUser><userId>42</userId></GetUser>
  </soap:Body>
</soap:Envelope>
```

**When to use SOAP:** When you need WS-Security standards (banking), formal contracts (WSDL), or ACID transactions.

**Common wrong answer:** Saying REST is always better. SOAP has strong security standards that some industries legally require.

---

### Q2: What is the difference between PUT and PATCH?

**What they're testing:** HTTP method understanding and idempotency.

**Answer:**

Both update a resource, but with different scope:

```javascript
// User in DB: { name: "Nihal", email: "a@b.com", age: 21, role: "tenant" }

// PUT /users/42 → REPLACE entirely
// You MUST send all fields. Missing fields get deleted/null.
PUT /users/42
Body: { "name": "Nihal Kumar", "email": "new@b.com", "age": 21, "role": "tenant" }
// Result: { name: "Nihal Kumar", email: "new@b.com", age: 21, role: "tenant" }

// PATCH /users/42 → UPDATE partially
// Only send what changed. Everything else stays.
PATCH /users/42
Body: { "age": 22 }
// Result: { name: "Nihal", email: "a@b.com", age: 22, role: "tenant" }
```

**Idempotency:**
- PUT is idempotent (same request = same result always)
- PATCH may or may not be (depends on implementation)

**Common wrong answer:** "PUT and PATCH do the same thing." They don't — PUT replaces, PATCH partially updates.

---

### Q3: What is idempotency and why does it matter?

**What they're testing:** Deep HTTP understanding, distributed systems awareness.

**Answer:**

An operation is **idempotent** if performing it multiple times has the same effect as performing it once.

```
GET /users/42   → Called 10 times → Always returns same user → IDEMPOTENT ✅
DELETE /users/42 → Called 3 times → User deleted on 1st call,
                                     2nd and 3rd return 404
                                     But the STATE is same → IDEMPOTENT ✅
POST /orders    → Called 3 times → Creates 3 separate orders → NOT IDEMPOTENT ❌
```

**Why it matters in production:**

Network requests can fail mid-transit. The client might retry. If POST isn't idempotent:

```
Client → POST /orders → Network drops → Client retries → 2 orders created!
Customer is charged twice. 😱
```

**Solution — Idempotency Key:**
```javascript
// Client generates unique ID and sends with request
POST /orders
Headers: { "Idempotency-Key": "uuid-abc-123" }

// Server checks: have we processed this key before?
const existing = await Order.findOne({ idempotencyKey: "uuid-abc-123" });
if (existing) return res.json({ data: existing }); // Return same result
```

**Common wrong answer:** Saying all methods are idempotent, or not knowing what idempotent means at all.

---

### Q4: What is the difference between 401 and 403?

**What they're testing:** HTTP status code precision, auth understanding.

**Answer:**

```
401 Unauthorized → Authentication problem
   "I don't know who you are. Please identify yourself."
   → No token
   → Expired token
   → Invalid/tampered token
   → Fix: Log in again to get a new token

403 Forbidden → Authorization problem
   "I know who you are, but you don't have permission."
   → Valid token ✓
   → But your role is 'tenant', this route requires 'admin'
   → Fix: Ask an admin to grant you access
```

Real-world example from PropSync:
```javascript
// Returns 401
GET /api/admin/users
Headers: {}   // No token at all

// Returns 403
GET /api/admin/users
Headers: { Authorization: "Bearer validTenantToken" }
// Token is valid, but user is 'tenant', route requires 'admin'
```

**Common wrong answer:** Saying 401 means "wrong password" (it means no valid authentication provided). Wrong password results in 401 but the reason is "authentication failed" not "wrong password" — the distinction matters.

---

### Q5: How does JWT authentication work? What are its security risks?

**What they're testing:** Auth architecture, security awareness.

**Answer:**

JWT has 3 base64-encoded parts: `header.payload.signature`

```javascript
// Decoded JWT payload (NOT secret, anyone can decode):
{
  "userId": "64f3b...",
  "role": "admin",
  "iat": 1700000000,  // issued at (Unix timestamp)
  "exp": 1700604800   // expires at (7 days later)
}

// Server verifies by re-computing signature:
HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY) === signature?
If yes → trusted.  If no → tampered, rejected.
```

**Security Risks & Mitigations:**

| Risk | Problem | Solution |
|---|---|---|
| Token theft | Attacker steals token, acts as user | Short expiry (15min), HTTPS only |
| No revocation | Can't invalidate a valid token until expiry | Maintain blacklist in Redis |
| Large payload | JWT sent on EVERY request, increases size | Keep payload minimal |
| Secret leak | If SECRET_KEY leaks, all tokens compromised | Rotate keys, use env vars |
| XSS | Script steals token from localStorage | Store in httpOnly cookie instead |

**Common wrong answer:** Saying JWT is encrypted (it's only signed, not encrypted). Payload is visible to anyone.

---

### Q6: What is CORS and how do you fix it?

**What they're testing:** Browser security model, practical debugging skill.

**Answer:**

CORS is a browser security mechanism. The browser refuses to let JavaScript make requests to a different origin (protocol + domain + port) unless the server explicitly allows it.

```
Your React app: http://localhost:5173
Your API:       http://localhost:3000

These are DIFFERENT origins → Browser blocks the request!
```

**The server must send a header to allow it:**
```
Access-Control-Allow-Origin: http://localhost:5173
```

**The Preflight Request (often confusing):**

For non-simple requests (POST with JSON, DELETE, custom headers), the browser first sends an OPTIONS request:

```
Browser: OPTIONS /api/users
Headers: Origin: http://localhost:5173
         Access-Control-Request-Method: POST

Server: 200 OK
Headers: Access-Control-Allow-Origin: http://localhost:5173
         Access-Control-Allow-Methods: GET, POST, PUT, DELETE
         Access-Control-Allow-Headers: Content-Type, Authorization

Browser: "OK, allowed!" → Sends actual POST request
```

**Fix in Express:**
```javascript
const cors = require('cors');
app.use(cors({
  origin: process.env.CLIENT_URL,  // 'http://localhost:5173' in dev
  credentials: true
}));
```

**Common wrong answer:** Fixing CORS on the frontend. CORS is enforced by the browser, fixed on the SERVER.

---

### Q7: What is API Rate Limiting and why is it important?

**What they're testing:** Production API design, security knowledge.

**Answer:**

Rate limiting restricts how many requests a client can make in a time window. Without it:

```
Attacker sends 1,000,000 login attempts per hour → brute-force attack
Bot scrapes your entire product database → competitive theft
DDoS attack → server goes down for everyone
```

**Implementation in Express:**
```javascript
const rateLimit = require('express-rate-limit');

// General limit: 100 requests per 15 minutes
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,   // Send X-RateLimit headers
  legacyHeaders: false,
  message: { success: false, message: 'Too many requests' }
});

// Stricter limit for auth routes
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // Only 5 login attempts per 15 minutes
  message: { success: false, message: 'Too many login attempts' }
});

app.use('/api', generalLimiter);
app.use('/api/v1/users/login', authLimiter);  // Extra strict on login
```

**At scale:** Use Redis-based rate limiting so limits are shared across multiple server instances (express-rate-limit + redis store).

**Common wrong answer:** "It's just to prevent server overload." It's also critical for security (brute force prevention).

---

### Q8: What is the difference between authentication and authorization?

**What they're testing:** Security fundamentals, clear communication.

**Answer:**

```
Authentication = Proving WHO you are
   → "Here's my email and password / JWT token"
   → Server verifies: "Yes, this is Nihal"

Authorization = Determining WHAT you can do
   → "I'm Nihal, I want to delete user 99"
   → Server checks: "Nihal is a 'tenant', tenants can't delete users" → 403
```

**In code:**
```javascript
// Authentication middleware — answers "Who are you?"
const protect = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'Please log in' });
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  req.user = await User.findById(decoded.userId);
  next();
};

// Authorization middleware — answers "Are you allowed?"
const authorize = (...roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res.status(403).json({ message: 'Access denied' });
  }
  next();
};

// Usage: protect runs first (authn), then authorize (authz)
router.delete('/users/:id', protect, authorize('admin'), deleteUser);
```

**Common wrong answer:** Using them interchangeably. They are distinct steps that can fail independently.

---

### Q9: How do you design pagination for a REST API?

**What they're testing:** API design skills, scalability thinking.

**Answer:**

**Two main approaches:**

**1. Offset-based pagination (most common)**
```javascript
// Request: GET /api/products?page=2&limit=10
const page = parseInt(req.query.page) || 1;
const limit = parseInt(req.query.limit) || 10;
const skip = (page - 1) * limit;  // page=2 → skip 10

const products = await Product.find().skip(skip).limit(limit);
const total = await Product.countDocuments();

res.json({
  data: products,
  pagination: {
    currentPage: page,
    totalPages: Math.ceil(total / limit),
    totalItems: total,
    hasNextPage: page < Math.ceil(total / limit),
    hasPrevPage: page > 1
  }
});
```

**2. Cursor-based pagination (for real-time data / large datasets)**
```javascript
// Request: GET /api/posts?cursor=lastPostId&limit=10
// Use the last item's ID as cursor → no skip needed
// Better performance on large tables (no OFFSET scan)
const posts = await Post.find({
  _id: { $gt: req.query.cursor }  // Items after cursor
}).limit(limit);

res.json({
  data: posts,
  nextCursor: posts[posts.length - 1]?._id
});
```

**Why cursor > offset for real-time:**
If 5 new items are added between page 1 and page 2, offset-based pagination shows duplicates. Cursor-based doesn't.

**Common wrong answer:** Returning all records and letting the client paginate. Never do this — it kills your server.

---

### Q10: What is the difference between REST and GraphQL?

**What they're testing:** Modern API knowledge, trade-off analysis.

**Answer:**

```
Problem REST has:
───────────────────────────────────────────────────────
Over-fetching: GET /users/42 returns 20 fields,
               but you only need name and email

Under-fetching: Need user + their posts + post comments?
               GET /users/42, then GET /users/42/posts,
               then GET /posts/1/comments → 3 requests!
```

**GraphQL Solution:**
```graphql
# One request, get exactly what you need
query {
  user(id: "42") {
    name
    email
    posts {
      title
      comments {
        text
        author { name }
      }
    }
  }
}
```

| Feature | REST | GraphQL |
|---|---|---|
| Multiple resources | Multiple requests | Single request |
| Data shaping | Fixed response | Client decides fields |
| Learning curve | Low | Higher |
| Caching | HTTP cache built-in | Complex (no URL per query) |
| Tooling | Universal | Needs GraphQL client |
| File upload | Easy | Complex |
| Best for | Simple CRUD, public APIs | Complex data, mobile (save bandwidth) |

**When to use GraphQL:** Mobile apps (save bandwidth), complex nested data, multiple clients needing different data shapes.

**Common wrong answer:** "GraphQL is always better." It has real downsides: no HTTP caching out of the box, complex rate limiting, harder debugging.

---

## PART 16: TOP 5 NODE.JS API INTERVIEW QUESTIONS

---

### N1: What is the Node.js Event Loop and why does it matter for APIs?

**Answer:**

Node.js is **single-threaded** — it runs one piece of code at a time. But it handles thousands of simultaneous requests because of the **event loop**.

```
Node.js process:
─────────────────────────────────────────────────────

Call Stack                  │  Web APIs / I/O
──────────────              │  ─────────────────
executeRequest()            │
  → check DB (async) ───────┼──→ MongoDB query (running in background)
  ← return to event loop    │
  → handle next request     │
  → handle next request     │  ← DB returns result
  ← callback queued         │
  → DB callback executed    │
```

**Why this matters for APIs:**

```javascript
// BAD — This BLOCKS the event loop for ALL users
app.get('/compute', (req, res) => {
  let sum = 0;
  for (let i = 0; i < 10_000_000_000; i++) { sum += i; } // CPU-intensive!
  res.json({ sum }); // Server is frozen for ~5 seconds for EVERYONE
});

// GOOD — Offload CPU work to worker threads or external service
const { Worker } = require('worker_threads');
app.get('/compute', (req, res) => {
  const worker = new Worker('./compute-worker.js');
  worker.on('message', result => res.json({ result }));
});

// GOOD — I/O is always non-blocking in Node
app.get('/users', async (req, res) => {
  const users = await User.find(); // Non-blocking: event loop is free while DB queries
  res.json({ data: users });
});
```

**Common wrong answer:** Thinking Node.js is multi-threaded like Java. It's single-threaded for JS execution, but uses libuv's thread pool for I/O.

---

### N2: What is middleware in Express and how does it work?

**Answer:**

Middleware is a function that runs between the incoming request and the final route handler. Every middleware gets `(req, res, next)` and must either send a response or call `next()`.

```javascript
// Middleware anatomy:
function myMiddleware(req, res, next) {
  // Do something with req or res
  console.log(`${req.method} ${req.url}`);

  // MUST call next() or send a response — otherwise request hangs!
  next();  // Pass to next middleware
  // OR: res.status(401).json({ message: 'Unauthorized' }); // End here
}

// Middleware stack executes in ORDER:
app.use(cors());              // 1st: Handle CORS headers
app.use(express.json());      // 2nd: Parse JSON body
app.use(morgan('dev'));        // 3rd: Log request
app.use(rateLimiter);         // 4th: Check rate limit
app.use('/api', router);      // 5th: Route to handlers

// Route-level middleware:
router.get('/profile', protect, authorize('admin'), getProfile);
//                     ↑         ↑                  ↑
//                 authN     authZ          actual handler
// protect runs → if ok → authorize runs → if ok → getProfile runs
```

**Error middleware (4 arguments):**
```javascript
// Express identifies error middleware by the 4th argument (err)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ success: false, message: err.message });
});

// Call it by passing error to next():
app.get('/route', (req, res, next) => {
  try {
    // ...
  } catch (err) {
    next(err); // Skips all regular middleware, goes straight to error handler
  }
});
```

**Common wrong answer:** Forgetting to call `next()` in middleware (request hangs forever with no response).

---

### N3: How do you handle async errors in Express?

**Answer:**

The biggest mistake beginners make in Express is not catching async errors:

```javascript
// BAD — Uncaught promise rejection, Express doesn't handle this
app.get('/users', async (req, res) => {
  const users = await User.find(); // If this throws, app CRASHES
  res.json({ data: users });
});

// GOOD — Option 1: try/catch in every route
app.get('/users', async (req, res, next) => {
  try {
    const users = await User.find();
    res.json({ data: users });
  } catch (error) {
    next(error); // Pass to error handler middleware
  }
});

// GOOD — Option 2: asyncHandler wrapper (DRY approach)
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Now no try/catch needed in routes!
app.get('/users', asyncHandler(async (req, res) => {
  const users = await User.find();
  res.json({ data: users });
}));

// GOOD — Option 3: Express 5 (handles async errors natively)
// In Express 5+, async route errors are automatically passed to next()
```

**Global error handler (catch-all):**
```javascript
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Gracefully shutdown
  server.close(() => process.exit(1));
});
```

**Common wrong answer:** Just using `.catch()` without calling `next(error)` — the error is swallowed and the request hangs.

---

### N4: What is the difference between `require` and `import` in Node.js?

**Answer:**

```javascript
// CommonJS (require) — default in Node.js
const express = require('express');
const { Router } = require('express');
module.exports = router;         // Export
module.exports = { fn1, fn2 };  // Export multiple

// ES Modules (import) — modern standard, used in React etc.
import express from 'express';
import { Router } from 'express';
export default router;          // Default export
export { fn1, fn2 };           // Named exports
```

**Key differences:**

| Feature | CommonJS (require) | ES Modules (import) |
|---|---|---|
| Loading | Synchronous | Asynchronous |
| When loaded | Runtime | Parse time (static) |
| Default in Node | ✅ Yes | Needs `"type": "module"` in package.json |
| Tree shaking | ❌ No | ✅ Yes (bundlers can remove unused code) |
| Top-level await | ❌ No | ✅ Yes |

**In Node.js API projects:**
- Most use CommonJS (`require`) — simpler, no config needed
- TypeScript projects use ES module syntax (TypeScript transpiles it)

**Common wrong answer:** Thinking they're interchangeable. You can't use `import` in a CommonJS file without a bundler or TypeScript.

---

### N5: How do you structure a large Node.js API project?

**Answer:**

```
my-api/
├── src/
│   ├── config/
│   │   ├── database.js     ← DB connection logic
│   │   └── env.js          ← Validate env vars on startup
│   │
│   ├── models/
│   │   ├── User.js         ← Mongoose/Sequelize models
│   │   └── Post.js
│   │
│   ├── controllers/        ← Business logic (what to do)
│   │   ├── userController.js
│   │   └── postController.js
│   │
│   ├── routes/             ← URL definitions (where to go)
│   │   ├── users.js
│   │   └── posts.js
│   │
│   ├── middleware/         ← Reusable middleware
│   │   ├── auth.js         ← protect, authorize
│   │   ├── validate.js     ← Input validation
│   │   └── errorHandler.js
│   │
│   ├── services/           ← External API calls, complex logic
│   │   ├── emailService.js ← Send emails via SendGrid
│   │   └── s3Service.js    ← Upload to S3
│   │
│   ├── utils/              ← Helper functions
│   │   ├── asyncHandler.js
│   │   └── apiError.js     ← Custom error class
│   │
│   └── app.js              ← Express setup (middleware, routes)
│
├── .env
├── .env.example            ← Template (commit this, not .env)
├── .gitignore
├── package.json
└── server.js               ← Entry point (connects DB, starts server)
```

**Why separate controllers from routes?**
- Routes: Map URL + method → controller function
- Controllers: Contain the actual logic
- This makes routes thin and readable, controllers testable in isolation

**Why separate services?**
- Services handle complex external operations (email, payment, S3)
- Controllers call services — keeps controllers simple
- Services can be tested independently

**Common wrong answer:** Putting all code in one `index.js` file. This works for tutorials, kills you at production scale.

---

## PART 17: FINAL QUICK-REFERENCE SUMMARY

```
REST Principles → Stateless, Client-Server, Cacheable, Uniform Interface
HTTP Methods    → GET(read) POST(create) PUT(replace) PATCH(update) DELETE(remove)
Idempotent      → GET, PUT, DELETE | Not: POST, PATCH
Safe            → GET only

Status Codes to MEMORIZE:
  200 OK │ 201 Created │ 204 No Content
  400 Bad Request │ 401 Unauthorized │ 403 Forbidden │ 404 Not Found
  409 Conflict │ 429 Too Many Requests
  500 Server Error │ 503 Service Unavailable

Auth flow: Login → JWT → Send token in header → Middleware verifies → Authorized
401 = Not logged in | 403 = Logged in but no permission

CORS = Browser security. Fix it on the SERVER with Access-Control-Allow-Origin header.

URL design: nouns not verbs, plural, lowercase, hyphenated, versioned (/api/v1/)

Node.js event loop: Single-threaded, non-blocking I/O. Never block it with CPU work.
```

---

*Made for Nihal Kumar Singh — go ace that interview! 🚀*
