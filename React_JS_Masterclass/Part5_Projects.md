# Part 5: Complete Projects Guide

> **"Theory gets you the interview. Projects get you the job. To truly understand React, you must build real-world applications, run into architecture problems, and solve them."**

This chapter provides a complete guide for 16 projects, ranging from absolute beginner to FAANG-level system design. 

---

## Table of Contents

1. [Beginner Projects (Core React)](#beginner)
   - Project 1: Todo App (CRUD)
   - Project 2: Calculator
   - Project 3: Notes App (Local Storage)
   - Project 4: Weather App (API Integration)
2. [Intermediate Projects (Routing & State)](#intermediate)
   - Project 5: Movie Search (Debouncing)
   - Project 6: Expense Tracker (Reducers)
   - Project 7: Shopping Cart (Global State)
   - Project 8: Blog App (Routing & Markdown)
3. [Advanced Projects (Full Stack Architecture)](#advanced)
   - Project 9: Chat Application (WebSockets)
   - Project 10: Authentication System (JWT)
   - Project 11: Admin Dashboard (Data Vis)
   - Project 12: E-commerce Platform (Redux/RTK)
4. [Master Projects (FAANG Portfolio)](#master)
   - Project 13: Kanban Board (Drag & Drop)
   - Project 14: Social Media Feed (Infinite Scroll)
   - Project 15: Netflix Clone (Video & Carousels)
   - Project 16: Airbnb Clone (Maps & Complex State)

---

## 1. Beginner Projects (Core React) {#beginner}

### Project 1: Todo App
**Learning Goals:** State management (`useState`), CRUD operations, rendering lists with keys, controlled components.

**Key Architecture:**
- Use a single array of objects for state: `[{ id: 1, text: "Learn React", completed: false }]`.
- Never mutate the array directly; use `.map()` for toggling completion and `.filter()` for deleting.

**Interview Talking Point:** "I implemented a functional update pattern for state changes to prevent stale closures, and ensured list keys were stable unique IDs rather than array indexes to optimize React's reconciliation."

### Project 2: Calculator
**Learning Goals:** Complex state interactions, event handling, math logic.

**Key Architecture:**
- State needs to track: `previousOperand`, `currentOperand`, and `operation`.
- Use `useReducer` instead of multiple `useStates`. A calculator is a perfect state machine.

**Implementation Highlight (Reducer):**
```javascript
function reducer(state, { type, payload }) {
  switch (type) {
    case 'ADD_DIGIT':
      if (payload.digit === '0' && state.currentOperand === '0') return state;
      return { ...state, currentOperand: `${state.currentOperand || ''}${payload.digit}` };
    case 'CHOOSE_OPERATION':
      if (state.currentOperand == null) return state;
      if (state.previousOperand == null) {
        return { ...state, operation: payload.operation, previousOperand: state.currentOperand, currentOperand: null };
      }
      return { ...state, previousOperand: evaluate(state), operation: payload.operation, currentOperand: null };
    // ... clear, delete, evaluate
  }
}
```

### Project 3: Notes App
**Learning Goals:** Persistent state (`localStorage`), Custom Hooks, Search/Filtering.

**Key Architecture:**
- Build a `useLocalStorage` custom hook to abstract away the `JSON.stringify/parse` logic and `useEffect` syncing.
- Use `useMemo` for the search filter so the heavy array filtering doesn't run unnecessarily.

### Project 4: Weather App
**Learning Goals:** Fetch API, `useEffect`, Error Handling, Geolocation API, Async/Await.

**Key Architecture:**
- Fetch data from OpenWeatherMap API.
- Must handle 3 states: Loading, Error, and Data.
- Use `navigator.geolocation.getCurrentPosition` in a `useEffect` on mount.

---

## 2. Intermediate Projects (Routing & State) {#intermediate}

### Project 5: Movie Search App
**Learning Goals:** Debouncing API calls, React Router (Details page), OMDb API.

**Key Architecture:**
- When the user types, do not hit the API on every keystroke. Implement a `useDebounce` hook.
- Use React Router to navigate from `/` to `/movie/:id`.
- Use the `useParams` hook on the Details page to fetch the specific movie.

**Implementation Highlight (useDebounce):**
```javascript
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}
```

### Project 6: Expense Tracker
**Learning Goals:** `useContext` for global state, Data visualization (Chart.js or Recharts).

**Key Architecture:**
- The total balance, income, and expenses need to be calculated derived state.
- Wrap the app in a `<GlobalProvider>` using Context to avoid passing transactions down through props.

### Project 7: Shopping Cart
**Learning Goals:** Complex global state (Zustand or Redux Toolkit), derived state (totals).

**Key Architecture:**
- The state should be an array of cart items: `[{ productId: 1, quantity: 2 }]`.
- The total price should NOT be in state. It should be derived on the fly using `.reduce()`.

**Interview Talking Point:** "I avoided duplicating data by only storing the Product ID and Quantity in the cart state. The actual product details (name, price) were mapped at render time, ensuring a single source of truth."

### Project 8: Blog App
**Learning Goals:** React Router v6 (Nested Routes), Markdown rendering.

**Key Architecture:**
- Structure: `/` (Home), `/posts` (List), `/posts/:slug` (Detail).
- Use `react-markdown` to render the content.
- (Bonus) Implement a protected route `/admin` for creating posts.

---

## 3. Advanced Projects (Full Stack Architecture) {#advanced}

### Project 9: Chat Application
**Learning Goals:** WebSockets (Socket.io), Real-time state updates, Presence (Online/Offline).

**Key Architecture:**
- Connect to the WebSocket inside a `useEffect` at the top level.
- Handle race conditions and duplicate messages by storing messages in a `Map` or Set based on unique message IDs.
- Use `useRef` to auto-scroll to the bottom of the chat window when a new message arrives.

### Project 10: Authentication System
**Learning Goals:** JWT handling, HttpOnly Cookies, Axios Interceptors, React Router Protected Routes.

**Key Architecture:**
- Create an `AuthContext` to store the logged-in user.
- Create an Axios Interceptor that catches `401 Unauthorized` errors and automatically attempts to hit the `/refresh` endpoint to get a new token, then retries the original request.

**Interview Talking Point:** "I designed the auth flow securely by storing the refresh token in an HttpOnly cookie to prevent XSS attacks, while keeping the short-lived access token in React state."

### Project 11: Admin Dashboard
**Learning Goals:** Data Tables (TanStack Table), Pagination, Sorting, Permissions/Roles.

**Key Architecture:**
- Do not render 10,000 users at once. Implement server-side pagination.
- Use TanStack Query (React Query) to fetch, cache, and synchronize the table data.

### Project 12: E-commerce Platform
**Learning Goals:** Redux Toolkit, Stripe Integration (Payment Gateway), Search/Filters.

**Key Architecture:**
- Slice up the Redux store: `cartSlice`, `userSlice`, `productSlice`.
- Implement optimistic updates when adding items to the cart.
- Secure the Stripe payment flow by processing the actual charge on the backend, only handling the token generation on the frontend.

---

## 4. Master Projects (FAANG Portfolio) {#master}

### Project 13: Kanban Board (Trello Clone)
**Learning Goals:** Drag and Drop (`@dnd-kit` or `react-beautiful-dnd`), Complex nested state normalization.

**Key Architecture:**
- **State Normalization is critical.** Do not nest tasks inside columns.
- Store columns and tasks separately as dictionaries (objects keyed by ID), and keep an array of Task IDs inside the Column object to maintain order.

```javascript
// Normalized State:
const state = {
  tasks: {
    'task-1': { id: 'task-1', content: 'Take out trash' },
    'task-2': { id: 'task-2', content: 'Cook dinner' }
  },
  columns: {
    'col-1': { id: 'col-1', title: 'To Do', taskIds: ['task-1', 'task-2'] }
  },
  columnOrder: ['col-1']
};
```

### Project 14: Social Media Feed (Twitter Clone)
**Learning Goals:** Infinite Scrolling, Optimistic Updates, Media Uploads.

**Key Architecture:**
- Use `IntersectionObserver` at the bottom of the list to trigger the next page fetch.
- Use `useInfiniteQuery` from TanStack Query.
- **Optimistic Updates:** When a user likes a post, instantly turn the heart red in the UI before the server responds. Roll back if the API fails.

### Project 15: Netflix Clone
**Learning Goals:** Video APIs (TMDB), Horizontal Carousels, Skeleton Loaders, CSS Grid/Flexbox mastery.

**Key Architecture:**
- Highly visual. Focus on Core Web Vitals (LCP, CLS).
- Lazy load images using the native `loading="lazy"` attribute.
- Preload the trailer video on hover.

### Project 16: Airbnb Clone
**Learning Goals:** Mapbox/Google Maps integration, Complex Date Pickers, Multi-parameter URL State.

**Key Architecture:**
- The filters (Location, Dates, Guests) must be synchronized with the URL Query Strings (`?location=Paris&guests=2`) so users can share links.
- The Map and the List View must share the same hovered state (hovering a card highlights the map pin). Use a shared Context or Zustand store for `hoveredListingId`.

---

## How to Present Projects in an Interview

When asked "Walk me through a project you built," do NOT just list features. Use this framework:

1. **The Problem:** "I wanted to build X because..."
2. **The Architecture:** "I chose React with Zustand for state, and TanStack Query for data fetching because..."
3. **The Hardest Technical Challenge:** "The hardest part was implementing the drag-and-drop state. Initially, I used deeply nested arrays, but updates were O(N). I solved it by normalizing the state into Hash Maps, reducing update time to O(1)."
4. **The Result:** "The app is deployed on Vercel, scores 98 on Lighthouse, and handles X concurrent users."

---
*End of Part 5 — Projects Guide. You now have the blueprint to become a Senior React Developer.*
