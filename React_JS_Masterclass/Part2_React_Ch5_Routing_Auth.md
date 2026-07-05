# Chapter 5: Routing, Authentication, and APIs

> **"A React app without routing and data is just a static widget. Routing dictates the structure, APIs bring the data, and Authentication protects it. This trinity forms the backbone of any real-world SPA."**

---

## Table of Contents

1. [Client-Side Routing Concepts](#routing-concepts)
2. [React Router v6 Fundamentals](#react-router)
3. [Nested Routes & Layouts](#nested-routes)
4. [Route Parameters & Query Strings](#url-state)
5. [Programmatic Navigation](#navigation)
6. [Authentication Architecture](#auth-architecture)
7. [Protected Routes (Private Routes)](#protected-routes)
8. [Token Storage (Security Debate)](#token-storage)
9. [Axios Interceptors & Refresh Tokens](#axios-interceptors)
10. [Handling CORS & CSRF](#security)
11. [Chapter Summary & Interview Prep](#summary)

---

## 1. Client-Side Routing Concepts {#routing-concepts}

### Traditional vs Client-Side Routing

**Traditional Routing (MPA):**
1. User clicks link `/about`.
2. Browser sends request to server.
3. Server generates HTML and sends it back.
4. Browser completely refreshes the page (white flash).

**Client-Side Routing (SPA):**
1. User clicks link `/about`.
2. JavaScript intercepts the click, prevents the default refresh.
3. JS changes the URL in the browser (using the HTML5 History API).
4. React unmounts the `Home` component and mounts the `About` component instantly.
5. (Optional) React fetches JSON data for the new view in the background.

**Result:** Extremely fast, app-like experience with zero page reloads.

---

## 2. React Router v6 Fundamentals {#react-router}

`react-router-dom` is the de facto standard routing library for React.

### Setup (BrowserRouter)

```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    // 1. Wrap the entire app in BrowserRouter
    <BrowserRouter>
      {/* Navbar stays outside Routes so it's always visible! */}
      <Navbar />
      
      {/* 2. Define Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} /> {/* Catch-all 404 */}
      </Routes>
    </BrowserRouter>
  );
}
```

### Links (Never use `<a href="">`!)
Using `<a href="/about">` causes a full page reload! Always use `<Link>` or `<NavLink>`.

```javascript
import { Link, NavLink } from 'react-router-dom';

// Basic link
<Link to="/about">About Us</Link>

// NavLink automatically knows if it's the active route!
<NavLink 
  to="/dashboard" 
  className={({ isActive }) => isActive ? "text-red-500 font-bold" : "text-gray-500"}
>
  Dashboard
</NavLink>
```

---

## 3. Nested Routes & Layouts {#nested-routes}

Nested routes allow you to render UI inside other UI, perfect for sidebars or tabbed layouts.

### The `<Outlet />` Component
The `Outlet` is a placeholder. It tells the parent route: "Render the matching child route right here."

```javascript
// App.jsx
<Routes>
  <Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<DashboardHome />} /> {/* Renders at /dashboard */}
    <Route path="stats" element={<Stats />} />  {/* Renders at /dashboard/stats */}
    <Route path="users" element={<Users />} />  {/* Renders at /dashboard/users */}
  </Route>
</Routes>

// DashboardLayout.jsx
import { Outlet } from 'react-router-dom';

function DashboardLayout() {
  return (
    <div className="flex">
      <Sidebar /> {/* Always present in the dashboard */}
      
      <main className="flex-1 p-4">
        {/* The child component (Stats, Users, etc.) renders here! */}
        <Outlet /> 
      </main>
    </div>
  );
}
```

---

## 4. Route Parameters & Query Strings {#url-state}

### URL Parameters (Path Variables)
Used for identifying a specific resource. e.g., `/users/123`.

```javascript
// 1. Define route with dynamic segment (:id)
<Route path="/users/:id" element={<UserProfile />} />

// 2. Extract parameter using useParams hook
import { useParams } from 'react-router-dom';

function UserProfile() {
  const { id } = useParams(); // Returns { id: "123" }
  
  useEffect(() => {
    fetchUser(id);
  }, [id]); // Always include URL params in dependency arrays!
  
  return <h1>User ID: {id}</h1>;
}
```

### Query Strings (Search Parameters)
Used for filtering, sorting, or pagination. e.g., `/products?sort=price&page=2`.
Query strings are **URL State**. They allow users to bookmark or share a specific filtered view.

```javascript
import { useSearchParams } from 'react-router-dom';

function Products() {
  // Works exactly like useState!
  const [searchParams, setSearchParams] = useSearchParams();
  
  const sort = searchParams.get('sort') || 'name'; // Default to 'name'
  
  const handleSortChange = (e) => {
    setSearchParams({ sort: e.target.value }); // Updates URL instantly!
  };
  
  return (
    <select value={sort} onChange={handleSortChange}>
      <option value="name">Sort by Name</option>
      <option value="price">Sort by Price</option>
    </select>
  );
}
```

---

## 5. Programmatic Navigation {#navigation}

Sometimes you need to navigate via code (e.g., after a successful form submission).

```javascript
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleLogin = async () => {
    await submitLogin();
    
    // Navigate to dashboard
    navigate('/dashboard');
    
    // OR: Navigate back one page (like browser back button)
    // navigate(-1);
    
    // OR: Replace current history entry (user can't click back to login page)
    // navigate('/dashboard', { replace: true });
  };
  
  return <button onClick={handleLogin}>Log In</button>;
}
```

---

## 6. Authentication Architecture {#auth-architecture}

The most common auth flow in SPAs is **JWT (JSON Web Token)**.

1. User submits email/password.
2. Server verifies and signs a JWT, returning it to the client.
3. Client stores the token.
4. Client attaches the token to the `Authorization: Bearer <token>` header for all subsequent API requests.
5. If token expires, API returns `401 Unauthorized`. Client handles logout or token refresh.

---

## 7. Protected Routes (Private Routes) {#protected-routes}

How do we prevent unauthenticated users from visiting `/dashboard`? We build a wrapper component.

```javascript
// ProtectedRoute.jsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  
  // If not logged in, redirect to login page (replace history)
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  // If logged in, render the child routes!
  return <Outlet />;
}

// App.jsx usage:
<Routes>
  {/* Public Route */}
  <Route path="/login" element={<Login />} />
  
  {/* Protected Routes Wrapper */}
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
  </Route>
</Routes>
```

---

## 8. Token Storage (Security Debate) {#token-storage}

Where do you store the JWT on the client? This is a massive interview question.

### Option 1: LocalStorage (Most Common, Least Secure)
- **Pros:** Easy to use, survives tab closures, available across tabs.
- **Cons:** Vulnerable to **XSS (Cross-Site Scripting)**. Any rogue JavaScript on your site (like a compromised third-party NPM package) can read `localStorage` and steal the token.

### Option 2: HttpOnly Cookie (Best Practice)
- **Pros:** The server sends the token in a cookie with the `HttpOnly` flag. JavaScript CANNOT read it. 100% immune to XSS token theft.
- **Cons:** Harder to implement. Requires backend cooperation. Vulnerable to **CSRF (Cross-Site Request Forgery)**, requiring Anti-CSRF tokens or `SameSite=Strict` flags.

### Option 3: In-Memory (Redux/State) + Silent Refresh
- Store short-lived Access Token in React state (wiped on refresh).
- Store long-lived Refresh Token in HttpOnly cookie.
- When app loads, silently ask server for a new Access Token using the cookie.

---

## 9. Axios Interceptors & Refresh Tokens {#axios-interceptors}

If using JWTs, you don't want to manually add the `Authorization` header to every single fetch request. Use an Axios Interceptor!

```javascript
import axios from 'axios';

// Create a custom instance
export const api = axios.create({
  baseURL: 'https://api.example.com',
});

// REQUEST INTERCEPTOR: Attach token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// RESPONSE INTERCEPTOR: Global Error Handling & Silent Refresh
api.interceptors.response.use(
  (response) => response, // Success, pass it through
  async (error) => {
    const originalRequest = error.config;
    
    // If API returns 401 Unauthorized, and we haven't retried yet...
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Attempt to get a new token
        const res = await axios.post('/api/refresh-token');
        const newToken = res.data.token;
        
        localStorage.setItem('token', newToken);
        
        // Retry the original failed request with the new token!
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
        
      } catch (refreshError) {
        // Refresh token expired. Force logout!
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);
```
*(This code snippet alone will impress senior interviewers.)*

---

## 10. Handling CORS & CSRF {#security}

### CORS (Cross-Origin Resource Sharing)
**Problem:** The browser blocks JS requests from `http://localhost:3000` (React) to `http://api.com:8000` (Server) for security.
**Solution:** The SERVER must return specific headers (`Access-Control-Allow-Origin: *` or specific domain). **You cannot fix CORS from the frontend code.** You can only proxy requests in development.

### CSRF (Cross-Site Request Forgery)
**Problem:** A malicious site tricks the user's browser into sending an authenticated request (via cookies) to your bank API to transfer money.
**Solution:** If using cookies for auth, ensure the server sets `SameSite=Lax` or `Strict` on the cookie. Alternatively, the server provides an Anti-CSRF token that the frontend must attach to POST requests.

---

## 11. Chapter Summary & Interview Prep {#summary}

### Top Interview Questions

**Q1. What is the difference between client-side routing and server-side routing?**
*Answer:* SSR fetches a completely new HTML page from the server on every click, causing a full page refresh. CSR intercepts the click, modifies the URL history, and uses JS to unmount/mount components, resulting in faster transitions and no white flash.

**Q2. Why do we use `<Link>` instead of `<a href>`?**
*Answer:* `<a href>` triggers a native browser request, causing a full page reload and resetting all React state (like Redux). `<Link>` prevents default behavior and utilizes the HTML5 History API (`pushState`) to update the UI instantly without losing state.

**Q3. How do you implement protected routes?**
*Answer:* By creating a wrapper component (like `<ProtectedRoute>`) that checks the authentication state. If authenticated, it renders the child route (`<Outlet />`). If not, it returns a `<Navigate to="/login" replace />` component to redirect the user.

**Q4. Where is the safest place to store a JWT in a React application?**
*Answer:* Storing it in `localStorage` is vulnerable to XSS attacks. The most secure approach is having the server set an `HttpOnly` cookie for a Refresh Token, and keeping a short-lived Access Token in JavaScript memory (React state). 

**Q5. What is an Axios Interceptor?**
*Answer:* A middleware function that intercepts HTTP requests or responses before they are handled by `then` or `catch`. Commonly used to attach Authorization headers to every outgoing request, or to globally handle 401 errors by silently refreshing tokens.

**Q6. What is CORS and how do you fix a CORS error?**
*Answer:* CORS is a browser security mechanism that restricts cross-origin HTTP requests. You cannot fix it purely on the frontend. The backend server must be configured to send the correct `Access-Control-Allow-Origin` headers. In development, you can use a proxy in `vite.config.js` or package.json to bypass it.

**Q7. Explain how URL parameters work vs Query Strings.**
*Answer:* URL parameters (`/users/:id`) define the exact resource being accessed and are required for the route to match. Query strings (`?sort=price`) are optional, key-value pairs used for filtering, sorting, or providing additional non-identifying data.

**Q8. What happens if a user enters a URL that doesn't match any route?**
*Answer:* You should define a Catch-All route at the bottom of your routing configuration: `<Route path="*" element={<NotFound404 />} />` which acts as a fallback.

**Q9. How do you handle navigation after a successful API mutation?**
*Answer:* Use the `useNavigate` hook to programmatically route the user (e.g., `navigate('/dashboard')`).

**Q10. Why might you use URL state instead of useState?**
*Answer:* If you have complex filters on a page (search query, sort order, pagination), putting them in URL Query Strings allows the user to copy-paste the URL and share it with someone else, who will see the exact same filtered view. `useState` is lost on refresh.

---

## 5 Output Prediction Exercises

**Exercise 1**
```javascript
// Route config: <Route path="/products/:id" element={<Product />} />
// User visits: /products/123?sort=asc
const { id } = useParams();
const [searchParams] = useSearchParams();
console.log(id, searchParams.get('sort'));
```
*Answer:* `"123", "asc"`.

**Exercise 2**
```javascript
// User is on /home. They click a button that runs:
navigate('/login', { replace: true });
// They login, which runs:
navigate('/dashboard');
// They click the browser's native Back button. Where do they go?
```
*Answer:* `/home`. Because `/login` used `replace: true`, it replaced `/home` in the stack. Then `/dashboard` was added. Clicking back skips login entirely.

**Exercise 3**
```javascript
// App.jsx
<Routes>
  <Route path="/" element={<A />} />
  <Route path="/about" element={<B />} />
  <Route path="*" element={<C />} />
</Routes>
// User visits /about/team
```
*Answer:* Renders `<C />`. The path does not exactly match `/about` unless a nested route or wildcard is defined.

**Exercise 4**
```javascript
function AuthWrapper({ children }) {
  const isAuth = false;
  return isAuth ? children : <Navigate to="/login" />;
}
// Rendered as: <AuthWrapper><Secret /></AuthWrapper>
// Does the <Secret /> component run its useEffect?
```
*Answer:* No. The ternary returns the Navigate component. The children (`<Secret />`) are never mounted into the DOM.

**Exercise 5**
```javascript
<NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>
  Dashboard
</NavLink>
// User is currently at URL: /dashboard/settings
// Will the NavLink have the 'active' class?
```
*Answer:* Yes. By default, `NavLink` matching is inclusive. To strictly match only the exact path, use the `end` prop: `<NavLink to="/dashboard" end>`.

---
*End of Chapter 5 — Routing and APIs.*
