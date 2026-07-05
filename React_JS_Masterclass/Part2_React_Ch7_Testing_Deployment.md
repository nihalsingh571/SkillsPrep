# Chapter 7: Testing & Deployment

> **"Code without tests is broken by design. A deployment without automation is a nightmare waiting to happen."**

---

## Table of Contents

1. [Types of Testing](#types-of-testing)
2. [Jest Fundamentals](#jest)
3. [React Testing Library (RTL)](#rtl)
4. [Testing Asynchronous Code & API Mocks (MSW)](#msw)
5. [End-to-End Testing (Cypress / Playwright)](#e2e)
6. [Error Boundaries in React](#error-boundaries)
7. [Accessibility (a11y) & SEO](#a11y-seo)
8. [The Build Process (Vite / Webpack)](#build-process)
9. [CI/CD Pipelines (GitHub Actions)](#ci-cd)
10. [Deployment Strategies (Vercel, Netlify, AWS)](#deployment)
11. [Chapter Summary & Interview Prep](#summary)

---

## 1. Types of Testing {#types-of-testing}

Before writing a single test, you must understand the Testing Pyramid:

1. **Unit Tests:** Testing an individual function, hook, or isolated component. (High speed, low cost, tests logic). *Tool: Jest/Vitest.*
2. **Integration Tests:** Testing how multiple components or hooks work together. (Medium speed, tests how parts interact). *Tool: React Testing Library.*
3. **End-to-End (E2E) Tests:** Simulating a real user clicking through the actual browser against a real or staging backend. (Slow, high cost, tests the entire system). *Tool: Cypress, Playwright.*

**The modern React consensus:** Focus heavily on **Integration Tests**. Testing that a user can type in a form and see a success message provides far more confidence than testing if a specific `div` has a specific class name.

---

## 2. Jest Fundamentals {#jest}

Jest (or Vitest, its modern, faster equivalent) is a test runner. It provides the functions `describe`, `it` (or `test`), and `expect`.

### Basic Test Syntax
```javascript
// math.test.js
import { add } from './math';

describe('Math utilities', () => { // Group tests
  
  beforeEach(() => {
    // Runs before every test in this block
  });

  it('should add two numbers correctly', () => { // The actual test
    const result = add(2, 3);
    
    // Assertion (Matcher)
    expect(result).toBe(5); 
  });
});
```

### Common Matchers
```javascript
expect(value).toBe(5);          // Exact equality (===)
expect(object).toEqual({a: 1}); // Deep equality (for objects/arrays)
expect(value).toBeTruthy();     // Truthy check
expect(array).toContain('item');// Array check
expect(func).toThrow();         // Checks if function throws an error
```

---

## 3. React Testing Library (RTL) {#rtl}

> *"The more your tests resemble the way your software is used, the more confidence they can give you." - Kent C. Dodds (Creator of RTL)*

RTL doesn't care about your React state, hooks, or components. It renders the DOM and forces you to query it exactly how a user would (by text, by label, by role).

### Basic Component Test

```javascript
// Counter.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Counter from './Counter';

describe('Counter Component', () => {
  
  it('renders initial count and increments on click', async () => {
    // 1. Render the component to a virtual DOM
    render(<Counter />);
    
    // 2. Query the DOM like a user would
    // "Find the text 'Count: 0'"
    const countText = screen.getByText(/Count: 0/i);
    expect(countText).toBeInTheDocument();
    
    // "Find the button that says 'Increment'"
    const button = screen.getByRole('button', { name: /increment/i });
    
    // 3. Fire an event (use userEvent instead of fireEvent for better realism)
    const user = userEvent.setup();
    await user.click(button);
    
    // 4. Assert the result
    expect(screen.getByText(/Count: 1/i)).toBeInTheDocument();
  });
});
```

### Query Priority
Always query the DOM in this order of preference:
1. `getByRole` (Most accessible)
2. `getByLabelText` (For forms)
3. `getByPlaceholderText`
4. `getByText`
5. `getByTestId` (Last resort, uses `data-testid="foo"`)

### Query Types
- `getBy...`: Returns the element, **throws an error** if not found. (Good for assertions).
- `queryBy...`: Returns the element, **returns null** if not found. (Good for asserting an element is *not* on the screen).
- `findBy...`: Returns a **Promise**. (Good for async elements that appear after loading).

---

## 4. Testing Asynchronous Code & API Mocks (MSW) {#msw}

Never hit a real API during integration tests! It makes tests slow, flaky, and expensive. 
The modern standard for mocking APIs is **Mock Service Worker (MSW)**.

Instead of mocking `fetch` or `axios`, MSW intercepts actual network requests at the network level and returns fake responses.

### Setting up MSW
```javascript
// handlers.js
import { rest } from 'msw';

export const handlers = [
  rest.get('https://api.example.com/user', (req, res, ctx) => {
    // Return a mocked 200 OK response with JSON data
    return res(
      ctx.status(200),
      ctx.json({ name: 'John Doe' })
    );
  }),
];
```

### Async Test with RTL
```javascript
import { render, screen } from '@testing-library/react';
import UserProfile from './UserProfile';

it('fetches and displays user data', async () => {
  render(<UserProfile />);
  
  // Initially shows loading
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  // Wait for the data to appear (using findBy!)
  const userName = await screen.findByText('John Doe');
  
  expect(userName).toBeInTheDocument();
  // Loading should be gone now
  expect(screen.queryByText(/loading/i)).toBeNull(); 
});
```

---

## 5. End-to-End Testing (Cypress / Playwright) {#e2e}

E2E testing spins up a real Chrome/Firefox browser and actually clicks around your deployed (or staging) site. 

Playwright Example:
```javascript
// login.spec.js
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  
  await page.fill('input[name="email"]', 'test@user.com');
  await page.fill('input[name="password"]', 'password123');
  
  await page.click('button[type="submit"]');
  
  // Expect URL to change to dashboard
  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  
  // Expect welcome message
  await expect(page.locator('h1')).toHaveText('Welcome back, test!');
});
```

---

## 6. Error Boundaries in React {#error-boundaries}

If a JavaScript error occurs inside a component during rendering, React will completely unmount the whole app (White Screen of Death). 
**Error Boundaries** catch these errors and display a fallback UI instead.

Currently, Error Boundaries **must be written as Class Components** (there is no hook for it yet).

```javascript
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  // 1. Update state so the next render shows the fallback UI
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  // 2. Log error to reporting service (Sentry, LogRocket)
  componentDidCatch(error, errorInfo) {
    logErrorToMyService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong. Please refresh.</h1>;
    }
    return this.props.children;
  }
}

// Usage in App.jsx:
<ErrorBoundary>
  <MyWidget />
</ErrorBoundary>
```

*(Note: Error boundaries do NOT catch errors in event handlers like `onClick` or `setTimeout`. You must use standard `try/catch` for those).*

---

## 7. Accessibility (a11y) & SEO {#a11y-seo}

### Accessibility (a11y) Rules:
1. **Semantic HTML:** Use `<button>` not `<div onClick="...">`. Use `<nav>`, `<main>`, `<article>`.
2. **Alt text:** Every `<img>` needs an `alt` attribute. If it's purely decorative, use `alt=""` so screen readers skip it.
3. **Keyboard Navigation:** Users should be able to tab through your app. Never use `outline: none` without providing a custom `:focus-visible` style.
4. **ARIA:** (Accessible Rich Internet Applications). Use `aria-hidden`, `aria-label`, and `aria-expanded` only when semantic HTML isn't enough.
5. **Color Contrast:** Ensure text is readable against its background (WCAG AA standard requires 4.5:1 contrast).

### SEO (Search Engine Optimization) in React
Single Page Applications (SPAs) are traditionally terrible for SEO because the server sends a blank HTML file, and crawlers (often) don't run JavaScript.

**Solutions:**
1. Use React Helmet to dynamically update `<title>` and `<meta>` tags.
2. Use **Next.js** for Server-Side Rendering (SSR) or Static Site Generation (SSG). This sends fully populated HTML to the client, making SEO perfect.

---

## 8. The Build Process (Vite / Webpack) {#build-process}

You cannot deploy raw JSX or modern JS to a browser. It must be built.

1. **Babel:** Transpiles JSX into `React.createElement` and modern ES6 into older ES5 for browser compatibility.
2. **Webpack/Vite (Bundlers):** Crawls your imports, tree-shakes dead code, minifies variables, removes comments, and bundles 1000 files into a few optimized `.js` and `.css` files (chunking).
3. **Minification:** Tools like Terser compress the code (`function doSomething()` becomes `function a()`).

**Vite vs Webpack:** Webpack bundles the entire app during development (slow). Vite serves files natively via ES modules in the browser during dev (instant reload) and uses Rollup for the production build.

---

## 9. CI/CD Pipelines (GitHub Actions) {#ci-cd}

**Continuous Integration (CI):** Every time you push code, an automated server runs your linter (ESLint) and your tests (Jest). If tests fail, the code cannot be merged.
**Continuous Deployment (CD):** If CI passes, the server automatically builds the project and deploys it to production.

```yaml
# .github/workflows/deploy.yml
name: Build and Test

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node
      uses: actions/setup-node@v3
      with:
        node-version: 18
    - run: npm install
    - run: npm run lint
    - run: npm test
    - run: npm run build
```

---

## 10. Deployment Strategies {#deployment}

### Static Hosting (Vercel, Netlify, AWS S3)
Because standard React apps (Vite/CRA) are just static HTML/JS/CSS files after the build process, they do NOT require a Node.js server to run!
You can host them entirely on a CDN (Content Delivery Network).

1. Run `npm run build`.
2. Take the `/dist` or `/build` folder.
3. Upload it to Vercel/Netlify/S3.

*Important config:* Because it's a SPA, the server must be configured to route ALL requests (e.g., `example.com/about`) to `index.html`. If not, users get a 404 when directly visiting a URL, because the file `about.html` doesn't actually exist on the server.

### Server-Side Rendering (Next.js)
If using Next.js with SSR, you DO need a running Node.js server. Vercel handles this automatically using Serverless Functions.

---

## 11. Chapter Summary & Interview Prep {#summary}

### Top 25 Interview Questions

**Q1. What is the difference between Jest and React Testing Library?**
*Answer:* Jest is a test runner and assertion library (it runs the test and checks if `expect(a).toBe(b)`). React Testing Library is a set of utilities specifically designed for rendering React components into a virtual DOM and querying them in a way that mimics user behavior.

**Q2. Why is it recommended to query by Role in RTL?**
*Answer:* Querying by Role (`getByRole('button')`) ensures that the element is actually accessible to screen readers. If you query by a `data-testid`, you might accidentally pass a test for a `div` disguised as a button that a keyboard user cannot actually click.

**Q3. How do you test a component that fetches data?**
*Answer:* You should not hit the real API in tests. You should use Mock Service Worker (MSW) to intercept the network request and return a mocked response. Then, use an asynchronous query (`findBy`) in RTL to wait for the mocked data to render on the screen.

**Q4. What is an Error Boundary in React?**
*Answer:* A class component that implements `static getDerivedStateFromError` or `componentDidCatch`. It acts like a global `try/catch` block for React rendering, preventing the entire app from crashing if one component throws an error, and allowing you to show a fallback UI.

**Q5. Can an Error Boundary catch errors in `setTimeout` or `onClick` handlers?**
*Answer:* No. Error boundaries only catch errors during the React Render phase, in lifecycle methods, and in constructors. Errors inside event handlers must be caught using standard `try/catch` blocks.

**Q6. What happens during the `npm run build` process?**
*Answer:* The bundler (Vite/Webpack) crawls the dependency tree. Babel transpiles JSX and modern JS into browser-compatible code. Dead code is removed (tree shaking). The code is minified and obfuscated (Terser). Finally, it outputs static HTML, JS, and CSS files into a `dist` directory.

**Q7. How do you handle 404 errors when a React SPA is deployed to a static server?**
*Answer:* Static servers look for actual files. If a user visits `/about`, the server looks for `about.html` and returns a 404. You must configure the server (e.g., using a `_redirects` file in Netlify, or `vercel.json`) to rewrite all missing routes to `index.html`. React Router then takes over and renders the correct component.

**Q8. What does CI/CD stand for and why do we use it?**
*Answer:* Continuous Integration / Continuous Deployment. It automates testing, linting, and deployment every time code is pushed. It ensures that broken code never reaches production and removes the human error of manual deployments.

**Q9. How do you improve the SEO of a React application?**
*Answer:* SPAs are bad for SEO because the initial HTML is empty. You can use React Helmet to manage meta tags per page. For true SEO, migrate to a meta-framework like Next.js that supports Server-Side Rendering (SSR) or Static Site Generation (SSG), which delivers fully populated HTML to the search engine crawler.

**Q10. What is semantic HTML and why is it important in React?**
*Answer:* Using HTML tags for their intended purpose (e.g., `<button>` for actions, `<a>` for navigation, `<nav>`, `<article>`). It is critical for accessibility (screen readers rely on semantics to navigate the page) and SEO.

---

## 5 Output Prediction Exercises

**Exercise 1**
```javascript
// Test code:
render(<MyComponent />);
const el = screen.getByText('Hello');
expect(el).not.toBeInTheDocument();
// If 'Hello' is NOT on the screen, does this test pass or fail?
```
*Answer:* Fails. `getByText` throws an error immediately if it cannot find the text, terminating the test before the assertion is reached. You must use `queryByText` instead, which returns `null`.

**Exercise 2**
```javascript
// A user clicks a button that triggers a Promise rejection inside an onClick handler.
// Does the ErrorBoundary component catch this?
```
*Answer:* No. Error boundaries do not catch errors inside event handlers.

**Exercise 3**
```javascript
// You deploy a standard Create React App to AWS S3. 
// A user clicks a React Router Link from '/' to '/users'. It works.
// The user hits the refresh button in their browser while on '/users'. What happens?
```
*Answer:* They get an Access Denied / 404 error from AWS S3, unless S3 and CloudFront are explicitly configured to route fallback errors to `index.html`.

**Exercise 4**
```javascript
// Test code:
render(<FetchDataComponent />);
const data = screen.getByText('API Data');
```
*Answer:* Fails. Assuming the fetch takes time, the data isn't there on the initial render. You must use `await screen.findByText('API Data')`.

**Exercise 5**
```javascript
import { omit } from 'lodash';
// vs
import omit from 'lodash/omit';
// Which is better for the build process?
```
*Answer:* The second one. While modern bundlers *can* sometimes tree-shake the first one, importing directly from the specific file guarantees that you aren't bundling the entire Lodash library into your app.

---
*End of Chapter 7 — Testing & Deployment. You've completed Part 2!*
