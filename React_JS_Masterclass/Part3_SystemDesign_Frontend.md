# Part 3: Advanced Frontend System Design
## React.js + JavaScript Master Handbook — Senior/Staff Engineer Level

> **Target Audience:** Senior engineers (5+ years) preparing for FAANG / Staff-level frontend interviews.  
> **Goal:** Learn to think, design, and communicate like a Staff Frontend Engineer.

---

## Table of Contents

1. [Frontend System Design Introduction](#1-frontend-system-design-introduction)
2. [Component Design Principles](#2-component-design-principles)
3. [Folder Structure & Architecture](#3-folder-structure--architecture)
4. [Atomic Design](#4-atomic-design)
5. [State Management Architecture](#5-state-management-architecture)
6. [API Layer Design](#6-api-layer-design)
7. [Authentication Architecture](#7-authentication-architecture)
8. [Caching Architecture](#8-caching-architecture)
9. [Error Handling Architecture](#9-error-handling-architecture)
10. [Performance Architecture](#10-performance-architecture)
11. [Micro-Frontend Architecture](#11-micro-frontend-architecture)
12. [Design Patterns in React](#12-design-patterns-in-react)
13. [Component-Level System Design Questions](#13-component-level-system-design-questions)
14. [Application-Level System Design](#14-application-level-system-design)
15. [System Design Interview Checklist](#15-system-design-interview-checklist)
16. [Top 25 Frontend System Design Questions](#16-top-25-frontend-system-design-questions)
17. [5 Full Design Exercises](#17-5-full-design-exercises)
18. [Interview Answer Framework](#18-interview-answer-framework)

---

# 1. Frontend System Design Introduction

## 1.1 What Is Frontend System Design?

Frontend System Design is the practice of **designing the architecture, structure, and technical decisions** of a frontend application before writing code. It goes beyond coding questions — it tests your ability to think at scale.

In a frontend system design interview, you are expected to:
- Break down ambiguous requirements into concrete decisions
- Justify architectural trade-offs
- Think about scalability, maintainability, and performance simultaneously
- Communicate design clearly using diagrams, pseudo-interfaces, and structured thinking

**Analogy:** Think of it like designing a skyscraper. Before laying a single brick, you need a blueprint — the foundation type, floor plan, load-bearing structure, and fire escape plan. A system design interview is your chance to show you have that blueprint in your head.

---

## 1.2 LLD vs HLD

| Dimension             | High-Level Design (HLD)                                | Low-Level Design (LLD)                                      |
|-----------------------|--------------------------------------------------------|-------------------------------------------------------------|
| Scope                 | Entire application / system                            | Individual module, component, or feature                    |
| Audience              | Product managers, architects, stakeholders             | Engineers implementing the feature                          |
| Detail Level          | What systems exist and how they connect                | How each piece of code should be structured                 |
| Frontend Examples     | Micro-frontend layout, CDN strategy, auth flow         | Autocomplete component API, pagination hook, error boundary |
| Tools                 | Architecture diagrams, data flow charts                | Props interfaces, state diagrams, hooks design              |

In frontend interviews, you will be asked **both**:
- HLD: "Design a Facebook News Feed" → Think macro: component hierarchy, API design, state management strategy, performance plan
- LLD: "Design an Autocomplete component" → Think micro: props interface, internal state, accessibility, edge cases

---

## 1.3 How to Approach the Frontend System Design Interview

### The 4-Step Mental Model

```
STEP 1: CLARIFY (2-3 minutes)
   ↓
STEP 2: OUTLINE (1-2 minutes — say what you'll cover)
   ↓
STEP 3: DEEP DIVE (30-40 minutes — the actual design)
   ↓
STEP 4: TRADE-OFFS (5 minutes — alternatives, limitations)
```

### Clarification Questions to Always Ask:

**Scale:**
- How many users? (thousands vs millions)
- How many engineers will maintain this?
- Is this a greenfield or adding to existing system?

**Product:**
- What devices? (mobile-first, desktop-only, both?)
- What browsers/OS to support?
- Offline support needed?

**Technical:**
- Existing tech stack constraints?
- Performance SLAs? (LCP < 2.5s? FID < 100ms?)
- Real-time requirements (WebSockets)?
- Authentication needed?

---

## 1.4 The RADIO Framework

RADIO is the industry-standard framework for structuring a frontend system design interview answer. Used by Facebook/Meta engineering interviews.

```
┌─────────────────────────────────────────────────────────────────┐
│                      RADIO Framework                             │
├──────────────────────────────────────────────────────────────────┤
│  R  →  Requirements         (What are we building?)              │
│  A  →  Architecture         (What are the major components?)     │
│  D  →  Data Model           (What data do we store/fetch?)       │
│  I  →  Interface Design     (API contracts, component APIs)      │
│  O  →  Optimizations        (Performance, scale, edge cases)     │
└──────────────────────────────────────────────────────────────────┘
```

### RADIO in Detail

#### R — Requirements
Split into two parts:
- **Functional:** What the user can do (e.g., "user can search for products, filter by category")
- **Non-Functional:** Performance, accessibility, offline support, i18n

#### A — Architecture
Draw the major building blocks and how they interact:
- Page/Route structure
- Core components
- State management layer
- API layer
- Real-time layer (if needed)

#### D — Data Model
Define the shape of data:
- What does the API return?
- How is it stored in the client?
- Normalized vs denormalized?
- Optimistic update shape?

#### I — Interface Design
Define contracts:
- Component props interface (TypeScript interface)
- API endpoints (REST/GraphQL schemas)
- Custom hook signatures
- Event payload shapes

#### O — Optimizations
Consider:
- Code splitting
- Lazy loading of images
- Caching strategy
- Virtualization for long lists
- Accessibility (WCAG)
- Error handling
- Offline/PWA

---

## 1.5 Common Mistakes in System Design Interviews

| Mistake                                   | How to Avoid                                     |
|-------------------------------------------|--------------------------------------------------|
| Starting to code immediately              | Always clarify requirements first                |
| Designing in a vacuum (no trade-offs)     | Always mention what you chose and why            |
| Ignoring accessibility                    | Mention ARIA, keyboard navigation proactively    |
| Forgetting error states                   | Loading/error/empty state for every data fetch   |
| No mention of performance                 | Always tie performance decisions to user metrics |
| Over-engineering for the problem          | Start simple, mention where to scale             |

---

# 2. Component Design Principles

## 2.1 Single Responsibility Principle (SRP) for Components

**What:** Every component should do ONE thing and do it well.

**Analogy:** A Swiss Army knife is useful but terrible at each individual task. A chef's knife does one thing — cuts — and does it perfectly.

**Bad — Button does too much:**
```jsx
// ❌ BAD: One component handles rendering, analytics, auth check, navigation
function SubmitButton({ user, product, navigate }) {
  const handleClick = () => {
    if (!user.isLoggedIn) {
      navigate('/login');
      return;
    }
    analytics.track('purchase_clicked', { productId: product.id });
    api.purchase(product.id);
  };
  return <button onClick={handleClick}>Buy Now</button>;
}
```

**Good — SRP applied:**
```jsx
// ✅ GOOD: Each piece has one responsibility
// Button.jsx — only renders a button
function Button({ children, onClick, variant = 'primary', disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn--${variant}`}
    >
      {children}
    </button>
  );
}

// PurchaseButton.jsx — only handles purchase logic
function PurchaseButton({ product }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { trackEvent } = useAnalytics();

  const handlePurchase = () => {
    if (!user.isLoggedIn) return navigate('/login');
    trackEvent('purchase_clicked', { productId: product.id });
    purchaseProduct(product.id);
  };

  return <Button onClick={handlePurchase}>Buy Now</Button>;
}
```

---

## 2.2 Props Interface Design

A well-designed component API is like a well-designed function API — easy to use correctly, hard to use incorrectly.

**Principles:**
1. **Explicitness over magic** — prefer explicit props over inference
2. **Sane defaults** — always have defaults for optional props
3. **Escape hatches** — provide `className`, `style`, `ref` overrides
4. **Composition over configuration** — accept children/slots instead of 100 props

**Example: Designing a Button component API**

```typescript
// ✅ Production-quality Button props interface
interface ButtonProps {
  // Core content
  children: React.ReactNode;
  
  // Variants (prefer union types over booleans for exclusivity)
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'link';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  
  // States
  isLoading?: boolean;
  isDisabled?: boolean;
  
  // Behavior
  type?: 'button' | 'submit' | 'reset';
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  
  // Icons — using React.ReactNode for flexibility
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  
  // Accessibility
  ariaLabel?: string;
  ariaDescribedBy?: string;
  
  // Escape hatch for styling customization
  className?: string;
  style?: React.CSSProperties;
  
  // Ref forwarding for external control
  ref?: React.Ref<HTMLButtonElement>;
}
```

**Anti-patterns in Props Design:**

```typescript
// ❌ BAD — boolean explosion (can't be combined sensibly)
interface BadButton {
  isPrimary?: boolean;
  isSecondary?: boolean;  // What if both are true?
  isDanger?: boolean;
  isGhost?: boolean;
}

// ❌ BAD — too generic (loses type safety)
interface GenericButton {
  config: Record<string, any>; // Anyone knows what to pass here?
}

// ❌ BAD — god props (component does too much based on one prop)
interface GodButton {
  mode: 'submit-with-auth' | 'delete-with-confirm' | 'external-link';
}
```

---

## 2.3 Composability

**What:** Components that can be assembled into more complex UIs by combining simple pieces.

**The Composability Spectrum:**

```
Less Composable ←————————————→ More Composable
    "Config"                       "Composition"
    
<Select 
  options={[...]} 
  renderOption={fn}       vs       <Select>
  renderValue={fn}                   <Select.Option value="a">
  header={fn}                          <Icon /> Apple
/>                                   </Select.Option>
                                   </Select>
```

---

## 2.4 Compound Components Pattern

**What:** A pattern where a parent component shares state implicitly with a group of child components, using React Context internally.

**Real-world analogy:** Think of `<select>` and `<option>` in HTML — they work together, the parent manages the state, and children just describe what they contain.

**Implementation Example: Tabs Component**

```jsx
// Step 1: Create the context
const TabsContext = React.createContext(null);

// Step 2: Parent component — owns the state
function Tabs({ children, defaultValue }) {
  const [activeTab, setActiveTab] = React.useState(defaultValue);
  
  const contextValue = React.useMemo(() => ({
    activeTab,
    setActiveTab,
  }), [activeTab]);
  
  return (
    <TabsContext.Provider value={contextValue}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Step 3: Child components — read from context
Tabs.List = function TabsList({ children }) {
  return <div className="tabs__list" role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ value, children }) {
  const { activeTab, setActiveTab } = React.useContext(TabsContext);
  const isActive = activeTab === value;
  
  return (
    <button
      role="tab"
      aria-selected={isActive}
      className={`tabs__tab ${isActive ? 'tabs__tab--active' : ''}`}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ value, children }) {
  const { activeTab } = React.useContext(TabsContext);
  if (activeTab !== value) return null;
  
  return (
    <div role="tabpanel" className="tabs__panel">
      {children}
    </div>
  );
};

// Step 4: Usage — clean and readable
function App() {
  return (
    <Tabs defaultValue="profile">
      <Tabs.List>
        <Tabs.Tab value="profile">Profile</Tabs.Tab>
        <Tabs.Tab value="settings">Settings</Tabs.Tab>
        <Tabs.Tab value="billing">Billing</Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel value="profile"><ProfileContent /></Tabs.Panel>
      <Tabs.Panel value="settings"><SettingsContent /></Tabs.Panel>
      <Tabs.Panel value="billing"><BillingContent /></Tabs.Panel>
    </Tabs>
  );
}
```

**Why compound components are powerful:**
- Parent manages state — children are dumb/presentational
- Users control the rendering order
- Easy to add new child types without changing the API
- Composable and flexible — you can put anything between tabs

---

## 2.5 Render Props Pattern

**What:** A component receives a function as a prop, calls it with data, and the caller decides what to render.

```jsx
// MouseTracker using Render Props
function MouseTracker({ render }) {
  const [position, setPosition] = React.useState({ x: 0, y: 0 });
  
  const handleMouseMove = (e) => {
    setPosition({ x: e.clientX, y: e.clientY });
  };
  
  return (
    <div onMouseMove={handleMouseMove} style={{ height: '100vh' }}>
      {render(position)} {/* Call the render prop with data */}
    </div>
  );
}

// Usage — caller decides what to render with the data
function App() {
  return (
    <MouseTracker
      render={({ x, y }) => (
        <p>Mouse is at ({x}, {y})</p>
      )}
    />
  );
}
```

> **Note:** Today, custom hooks largely replace Render Props and HOCs. But the pattern is still seen in libraries like React Router (`<Route render={...}>`) and Formik.

---

## 2.6 Higher-Order Components (HOC)

**What:** A function that takes a component and returns a new, enhanced component.

```jsx
// withAuth HOC — adds authentication check
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    const { user, isLoading } = useAuth();
    
    if (isLoading) return <LoadingSpinner />;
    if (!user) return <Navigate to="/login" />;
    
    return <WrappedComponent {...props} user={user} />;
  };
}

// withLogger HOC — adds lifecycle logging
function withLogger(WrappedComponent) {
  return function LoggedComponent(props) {
    React.useEffect(() => {
      console.log(`[${WrappedComponent.displayName}] mounted`);
      return () => console.log(`[${WrappedComponent.displayName}] unmounted`);
    }, []);
    
    return <WrappedComponent {...props} />;
  };
}

// Usage — compose HOCs
const ProtectedDashboard = withLogger(withAuth(Dashboard));
```

**HOC vs Custom Hook — When to use which:**

| Situation                               | Use HOC           | Use Custom Hook      |
|-----------------------------------------|-------------------|----------------------|
| Wrapping with JSX (loading states, etc) | ✅                | ❌ (can't return JSX) |
| Pure logic sharing (no extra DOM)       | ❌ (adds layers)  | ✅                   |
| Need to work with class components      | ✅                | ❌                   |
| Composing multiple behaviors            | Gets messy        | ✅ (easily combined) |

---

## 2.7 Headless Components

**What:** Components that provide behavior and state management with ZERO opinions about UI/styling. The consumer 100% controls rendering.

**Analogy:** React Select vs a raw `useSelect()` hook. The hook gives you the logic (open/close, keyboard navigation, filtering), you provide the HTML.

```jsx
// Headless Dropdown
function useDropdown(options) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [selectedIndex, setSelectedIndex] = React.useState(-1);
  const [query, setQuery] = React.useState('');

  const filteredOptions = options.filter(opt =>
    opt.label.toLowerCase().includes(query.toLowerCase())
  );

  const handleKeyDown = (e) => {
    switch(e.key) {
      case 'ArrowDown':
        setSelectedIndex(i => Math.min(i + 1, filteredOptions.length - 1));
        break;
      case 'ArrowUp':
        setSelectedIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
        if (selectedIndex >= 0) selectOption(filteredOptions[selectedIndex]);
        break;
      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  const selectOption = (option) => {
    setIsOpen(false);
    return option;
  };

  return {
    isOpen, setIsOpen,
    selectedIndex, query, setQuery,
    filteredOptions, handleKeyDown, selectOption,
  };
}

// Consumer — 100% controls rendering
function CustomDropdown({ options }) {
  const dropdown = useDropdown(options);
  
  return (
    <div className="my-custom-dropdown">
      <button onClick={() => dropdown.setIsOpen(o => !o)}>
        Open
      </button>
      {dropdown.isOpen && (
        <ul onKeyDown={dropdown.handleKeyDown}>
          {dropdown.filteredOptions.map((opt, i) => (
            <li
              key={opt.value}
              className={i === dropdown.selectedIndex ? 'highlighted' : ''}
              onClick={() => dropdown.selectOption(opt)}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**Libraries using Headless pattern:** Headless UI (Tailwind Labs), Radix UI, Reach UI, Downshift

---

## 2.8 Component Design Case Studies

### Case Study 1: Button Component
```typescript
// Complete props interface
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'solid' | 'outline' | 'ghost' | 'link';
  colorScheme?: 'blue' | 'red' | 'green' | 'gray';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isFullWidth?: boolean;
  leftIcon?: React.ReactElement;
  rightIcon?: React.ReactElement;
  loadingText?: string;
  spinnerPlacement?: 'start' | 'end';
}
```

### Case Study 2: Modal Component
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  isCentered?: boolean;
  closeOnOverlayClick?: boolean;
  closeOnEsc?: boolean;
  initialFocusRef?: React.RefObject<HTMLElement>;
  finalFocusRef?: React.RefObject<HTMLElement>;
  children: React.ReactNode;
}

interface ModalHeaderProps { children: React.ReactNode; }
interface ModalBodyProps { children: React.ReactNode; }
interface ModalFooterProps { children: React.ReactNode; }
```

### Case Study 3: Select Component
```typescript
interface SelectOption<T = string> {
  value: T;
  label: string;
  isDisabled?: boolean;
  group?: string;
}

interface SelectProps<T = string> {
  options: SelectOption<T>[];
  value?: T;
  defaultValue?: T;
  onChange?: (value: T, option: SelectOption<T>) => void;
  isMulti?: boolean;
  isSearchable?: boolean;
  isClearable?: boolean;
  isDisabled?: boolean;
  isLoading?: boolean;
  placeholder?: string;
  noOptionsMessage?: string | ((query: string) => string);
  filterOption?: (option: SelectOption<T>, query: string) => boolean;
  renderOption?: (option: SelectOption<T>) => React.ReactNode;
  renderValue?: (value: T, option: SelectOption<T>) => React.ReactNode;
}
```

### Case Study 4: Autocomplete Component
```typescript
interface AutocompleteProps<T> {
  // Data
  options: T[];
  value?: T | null;
  defaultValue?: T;
  
  // Data access
  getOptionLabel: (option: T) => string;
  getOptionValue: (option: T) => string | number;
  isOptionEqual?: (option: T, value: T) => boolean;
  
  // Callbacks
  onChange?: (value: T | null) => void;
  onInputChange?: (value: string, reason: 'input' | 'reset' | 'clear') => void;
  
  // Async options
  loadOptions?: (query: string) => Promise<T[]>;
  
  // Display
  renderOption?: (option: T, state: { isSelected: boolean; isFocused: boolean }) => React.ReactNode;
  renderInput?: (params: InputParams) => React.ReactNode;
  noOptionsText?: string;
  loadingText?: string;
  
  // Behavior
  freeSolo?: boolean;
  clearOnBlur?: boolean;
  filterOptions?: (options: T[], query: string) => T[];
}
```

### Case Study 5: DatePicker Props Interface
```typescript
interface DatePickerProps {
  value?: Date | null;
  defaultValue?: Date;
  onChange?: (date: Date | null) => void;
  
  // Range support
  isRange?: boolean;
  startDate?: Date;
  endDate?: Date;
  onRangeChange?: (range: [Date | null, Date | null]) => void;
  
  // Constraints
  minDate?: Date;
  maxDate?: Date;
  disabledDates?: Date[] | ((date: Date) => boolean);
  
  // Display
  format?: string;                       // 'MM/DD/YYYY'
  locale?: string;                       // 'en-US'
  firstDayOfWeek?: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  showTimeSelect?: boolean;
  timeIntervals?: number;                // 15, 30, 60
  
  // Behavior
  closeOnSelect?: boolean;
  isClearable?: boolean;
  isReadOnly?: boolean;
  isDisabled?: boolean;
  portal?: boolean;                      // Render in a portal
  
  // Custom rendering
  renderDayContent?: (date: Date) => React.ReactNode;
  renderHeader?: (date: Date, navigation: NavigationProps) => React.ReactNode;
}
```

---

# 3. Folder Structure & Architecture

## 3.1 Feature-Based vs Technical-Based Structure

### Technical-Based (Type-Based) — Organize by WHAT the file is

```
src/
├── components/           ← ALL components
│   ├── Button.jsx
│   ├── Modal.jsx
│   ├── UserCard.jsx
│   ├── ProductCard.jsx
│   └── Header.jsx
├── hooks/                ← ALL hooks
│   ├── useAuth.js
│   ├── useFetch.js
│   └── useCart.js
├── pages/                ← ALL pages
│   ├── Home.jsx
│   ├── Product.jsx
│   └── Profile.jsx
├── services/             ← ALL API services
│   ├── authService.js
│   └── productService.js
└── utils/                ← ALL utilities
    ├── formatDate.js
    └── validators.js
```

**Problems:** As the app grows, `components/` becomes a jungle. You touch 6 different folders for one feature change.

---

### Feature-Based — Organize by WHAT the code belongs to

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   └── SignupForm.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── services/
│   │   │   └── authService.js
│   │   ├── store/
│   │   │   └── authSlice.js
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.js          ← Public API for this feature
│   │
│   ├── products/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductGrid.jsx
│   │   │   └── ProductFilter.jsx
│   │   ├── hooks/
│   │   │   ├── useProducts.js
│   │   │   └── useProductFilter.js
│   │   ├── services/
│   │   │   └── productService.js
│   │   └── index.js
│   │
│   └── cart/
│       ├── components/
│       │   ├── CartItem.jsx
│       │   └── CartSummary.jsx
│       ├── hooks/
│       │   └── useCart.js
│       └── index.js
│
├── shared/                   ← Truly shared, cross-feature code
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   ├── Button.test.jsx
│   │   │   └── Button.stories.jsx
│   │   ├── Modal/
│   │   └── Input/
│   ├── hooks/
│   │   ├── useFetch.js
│   │   ├── useDebounce.js
│   │   └── useLocalStorage.js
│   ├── utils/
│   │   ├── formatDate.js
│   │   ├── validators.js
│   │   └── helpers.js
│   └── types/
│       └── common.types.ts
│
├── pages/                    ← Route-level components only
│   ├── HomePage.jsx
│   ├── ProductPage.jsx
│   └── ProfilePage.jsx
│
├── app/                      ← App-level config
│   ├── App.jsx
│   ├── routes.jsx
│   ├── store.js              ← Redux store config
│   └── queryClient.js        ← React Query config
│
├── config/                   ← Environment config
│   ├── api.config.js
│   └── constants.js
│
└── assets/                   ← Static assets
    ├── images/
    ├── fonts/
    └── icons/
```

**Comparison Table:**

| Aspect                   | Technical-Based        | Feature-Based              |
|--------------------------|------------------------|----------------------------|
| Initial Setup            | Simple                 | More upfront planning      |
| Scalability              | Poor                   | Excellent                  |
| Finding related files    | Hard (scattered)       | Easy (co-located)          |
| Team ownership           | Hard to assign         | Easy (team owns feature/)  |
| Code deletion            | Risky (shared?)        | Safe (feature is self-contained) |
| Onboarding               | Confusing              | Intuitive                  |
| Suitable for             | Small apps, prototypes | Medium to large apps        |

---

## 3.2 Explanation of Every Folder

### `features/`
The core of feature-based architecture. Each subfolder represents a **domain** or **business capability**.

**Rules:**
- Features should NOT import from each other directly (use shared/)
- Each feature exports a public API via `index.js`
- Feature folders are self-sufficient (components + hooks + services + types)

### `shared/`
Code that is genuinely shared across 2+ features.

**Common Mistake:** Putting everything in `shared/` defeats the purpose. Be strict — only truly reusable code belongs here.

### `pages/`
Pages are thin orchestration layers. They import from features and connect them together. Pages should have minimal logic.

```jsx
// pages/ProductPage.jsx — thin orchestration
function ProductPage() {
  const { id } = useParams();
  
  return (
    <Layout>
      <ProductDetails productId={id} />  {/* from features/products */}
      <RelatedProducts productId={id} /> {/* from features/products */}
      <CartSidebar />                    {/* from features/cart */}
    </Layout>
  );
}
```

### `app/`
Application bootstrap and configuration — store, router, query client, global providers.

### `config/`
Environment-specific configuration, API base URLs, feature flags, constants.

---

## 3.3 Domain-Driven Design (DDD) Concepts for Frontend

DDD is a philosophy originating in backend/system design that translates well to frontend:

| DDD Concept     | Frontend Equivalent                              |
|-----------------|--------------------------------------------------|
| Domain          | Business area (auth, products, orders)           |
| Entity          | Data with an identity (User, Product, Order)     |
| Value Object    | Data without identity (Address, Price)           |
| Aggregate       | Cluster of entities (Order + OrderItems)         |
| Repository      | Service layer that fetches domain data           |
| Domain Event    | User action or system event (OrderPlaced)        |
| Bounded Context | Feature module with its own models               |

**Why DDD matters for frontend interviews:** When asked "How would you structure a large e-commerce app?", mentioning DDD concepts signals senior thinking.

---

## 3.4 Monorepo Concepts

A monorepo stores multiple packages/apps in a single repository.

```
monorepo/
├── apps/
│   ├── web/              ← Main React app
│   ├── mobile/           ← React Native app
│   └── admin/            ← Admin React app
├── packages/
│   ├── ui/               ← Shared design system components
│   ├── utils/            ← Shared utility functions
│   ├── api-client/       ← Shared API client
│   └── types/            ← Shared TypeScript types
├── package.json
└── turbo.json            ← Turborepo configuration
```

**Tools:** Turborepo, Nx, Yarn Workspaces, pnpm Workspaces

**Benefits:**
- Shared code without npm package overhead
- Atomic commits across packages
- Single CI/CD pipeline

**Trade-offs:**
- Longer build times (mitigated by caching in Turborepo/Nx)
- Complex tooling setup

---

# 4. Atomic Design

## 4.1 Overview

Atomic Design, introduced by Brad Frost, provides a systematic methodology for building design systems.

```
┌─────────────────────────────────────────────────────────────────┐
│                       Atomic Design                             │
│                                                                  │
│  ATOMS        →  Basic building blocks (Button, Input, Icon)    │
│    ↓                                                            │
│  MOLECULES    →  Simple groups of atoms (SearchBar, FormField)  │
│    ↓                                                            │
│  ORGANISMS    →  Complex UI sections (Header, ProductCard)      │
│    ↓                                                            │
│  TEMPLATES    →  Page-level structure (no real data)            │
│    ↓                                                            │
│  PAGES        →  Real data poured into templates                │
└─────────────────────────────────────────────────────────────────┘
```

## 4.2 Each Level in Detail

### Atoms
The smallest indivisible UI elements.

```jsx
// atoms/Button.jsx
// atoms/Input.jsx
// atoms/Label.jsx
// atoms/Icon.jsx
// atoms/Badge.jsx
// atoms/Avatar.jsx
// atoms/Spinner.jsx
// atoms/Divider.jsx
```

### Molecules
Combinations of atoms that form a simple, functional unit.

```jsx
// molecules/SearchBar.jsx — Input atom + Icon atom + Button atom
function SearchBar({ onSearch, placeholder }) {
  const [query, setQuery] = useState('');
  
  return (
    <div className="search-bar">
      <Icon name="search" />              {/* Atom */}
      <Input                              {/* Atom */}
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder={placeholder}
      />
      <Button onClick={() => onSearch(query)}> {/* Atom */}
        Search
      </Button>
    </div>
  );
}

// molecules/FormField.jsx — Label + Input + ErrorMessage
function FormField({ label, error, ...inputProps }) {
  return (
    <div className="form-field">
      <Label>{label}</Label>
      <Input {...inputProps} hasError={!!error} />
      {error && <span className="form-field__error">{error}</span>}
    </div>
  );
}
```

### Organisms
Complex UI sections that are a distinct section of the interface.

```jsx
// organisms/ProductCard.jsx — uses multiple molecules + atoms
function ProductCard({ product, onAddToCart }) {
  return (
    <article className="product-card">
      <img src={product.image} alt={product.name} />
      <Badge variant="sale">{product.discount}% OFF</Badge>
      <h3>{product.name}</h3>
      <StarRating value={product.rating} count={product.reviewCount} />
      <PriceDisplay price={product.price} originalPrice={product.originalPrice} />
      <Button onClick={() => onAddToCart(product)} leftIcon={<CartIcon />}>
        Add to Cart
      </Button>
    </article>
  );
}

// organisms/Header.jsx
function Header() {
  return (
    <header className="header">
      <Logo />
      <NavigationMenu />
      <SearchBar />
      <UserMenu />
      <CartIcon />
    </header>
  );
}
```

### Templates
Page-level layout without real data — defines structure.

```jsx
// templates/ProductListTemplate.jsx
function ProductListTemplate({ 
  header, 
  sidebar, 
  productGrid, 
  pagination 
}) {
  return (
    <div className="product-list-template">
      {header}
      <div className="product-list-template__body">
        <aside className="product-list-template__sidebar">
          {sidebar}
        </aside>
        <main className="product-list-template__main">
          {productGrid}
          {pagination}
        </main>
      </div>
    </div>
  );
}
```

### Pages
Real data fed into templates.

```jsx
// pages/ProductListPage.jsx
function ProductListPage() {
  const { products, isLoading, pagination } = useProducts();
  const { filters, handleFilterChange } = useProductFilters();
  
  return (
    <ProductListTemplate
      header={<Header />}
      sidebar={<FilterPanel filters={filters} onChange={handleFilterChange} />}
      productGrid={
        isLoading 
          ? <ProductGridSkeleton count={12} />
          : <ProductGrid products={products} />
      }
      pagination={<Pagination {...pagination} />}
    />
  );
}
```

---

## 4.3 Storybook

**What:** An isolated component development environment. Build and test components independently without needing to run the full app.

**Why it matters for system design:**
- Forces SRP — components must work in isolation
- Auto-documents the component library
- Visual regression testing (with Chromatic)
- Enables collaboration between design and engineering

```jsx
// Button.stories.jsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'ghost'] },
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
  },
};
export default meta;

type Story = StoryObj<typeof Button>;

// Each export is a story (a state of the component)
export const Primary: Story = {
  args: { variant: 'primary', children: 'Click Me' },
};

export const Loading: Story = {
  args: { isLoading: true, children: 'Saving...' },
};

export const WithIcon: Story = {
  args: { leftIcon: <SaveIcon />, children: 'Save' },
};
```

---

# 5. State Management Architecture

## 5.1 State Categorization

Not all state is equal. Categorizing state is the first step to managing it well.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     State Categories                                │
├──────────────┬──────────────────────────────────────────────────────┤
│ Category     │ Description + Examples                               │
├──────────────┼──────────────────────────────────────────────────────┤
│ Local UI     │ State local to a component                           │
│              │ → Modal open/close, form input value, hover state    │
│              │ → Tool: useState / useReducer                        │
├──────────────┼──────────────────────────────────────────────────────┤
│ Shared UI    │ State shared between nearby components               │
│              │ → Tab selection in a parent, filter state            │
│              │ → Tool: Lift state up / Context                      │
├──────────────┼──────────────────────────────────────────────────────┤
│ Server/Cache │ Data fetched from server                             │
│              │ → User profile, product list, search results         │
│              │ → Tool: React Query / SWR / RTK Query                │
├──────────────┼──────────────────────────────────────────────────────┤
│ Global App   │ App-wide state not tied to server                    │
│              │ → Current user/auth state, theme, locale             │
│              │ → Tool: Context API / Zustand / Redux                │
├──────────────┼──────────────────────────────────────────────────────┤
│ URL State    │ State that should be shareable via URL               │
│              │ → Search query, page number, selected filters        │
│              │ → Tool: React Router search params                   │
├──────────────┼──────────────────────────────────────────────────────┤
│ Persistent   │ State that survives page refresh                     │
│              │ → Cart items, user preferences, draft text           │
│              │ → Tool: localStorage / IndexedDB / Cookies           │
└──────────────┴──────────────────────────────────────────────────────┘
```

---

## 5.2 The Colocation Principle

**Rule:** Keep state as close to where it's used as possible. Only lift state when necessary.

```
Wrong approach — everything in global store:
  Redux Store
    ├── ui.modalOpen = false    ← WRONG — only used in Modal
    ├── ui.hoverCardId = null   ← WRONG — only used in HoverCard
    ├── form.email = ''         ← WRONG — only used in LoginForm
    └── ...

Right approach — colocate:
  <Modal>         ← owns its own open/close state
  <HoverCard>     ← owns its own hover state
  <LoginForm>     ← owns its own field values
  
  Global Store:   ← only genuinely global state
    ├── auth.user
    ├── theme.mode
    └── cart.items
```

---

## 5.3 State Decision Tree

```
Is this state used by only ONE component?
    │
    YES ──→ Use useState / useReducer (local state)
    │
    NO
    │
    ↓
Is it server data (from an API)?
    │
    YES ──→ Use React Query / SWR / RTK Query
    │
    NO
    │
    ↓
Does it need to be in the URL (shareable)?
    │
    YES ──→ Use URL search params (useSearchParams)
    │
    NO
    │
    ↓
Is it shared across distant components?
    │
    YES ──→ Few context consumers? → Context API
    │         Many consumers / complex? → Zustand / Redux
    NO
    │
    ↓
Is it shared between a few siblings?
    │
    YES ──→ Lift state up to common parent
    │
    ↓
Does it need to persist across sessions?
    │
    YES ──→ localStorage / IndexedDB + sync with state
```

---

## 5.4 State Normalization

**What:** Storing data in a flat, database-like structure instead of deeply nested objects.

**Problem with nested state:**
```javascript
// ❌ NESTED — hard to update
const state = {
  posts: [
    {
      id: 1,
      title: 'Hello',
      author: { id: 42, name: 'Alice' },
      comments: [
        { id: 101, text: 'Great!', author: { id: 43, name: 'Bob' } }
      ]
    }
  ]
};

// To update Bob's name everywhere → have to find all instances
```

**Normalized state:**
```javascript
// ✅ NORMALIZED — easy to update
const state = {
  entities: {
    posts: {
      1: { id: 1, title: 'Hello', authorId: 42, commentIds: [101] }
    },
    users: {
      42: { id: 42, name: 'Alice' },
      43: { id: 43, name: 'Bob' }     // Update once, reflects everywhere
    },
    comments: {
      101: { id: 101, text: 'Great!', authorId: 43 }
    }
  },
  result: [1]  // Ordered list of post IDs
};
```

**Using `createEntityAdapter` in Redux Toolkit:**
```javascript
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit';

const postsAdapter = createEntityAdapter({
  sortComparer: (a, b) => b.createdAt.localeCompare(a.createdAt),
});

const postsSlice = createSlice({
  name: 'posts',
  initialState: postsAdapter.getInitialState(),
  reducers: {
    postAdded: postsAdapter.addOne,
    postUpdated: postsAdapter.updateOne,
    postRemoved: postsAdapter.removeOne,
    postsReceived: postsAdapter.setAll,
  },
});

// Selectors automatically generated
export const { selectAll: selectAllPosts, selectById: selectPostById } = 
  postsAdapter.getSelectors(state => state.posts);
```

---

## 5.5 Optimistic Updates Architecture

**What:** Update the UI instantly, as if the server request already succeeded, then reconcile with the actual server response.

**Why:** Makes the app feel instant. Used by Facebook, Twitter for likes/reactions.

```
User Clicks "Like"
       │
       ↓
1. Immediately update UI (add like, increment count) ←─── Optimistic Update
       │
       ↓
2. Send API request to server
       │
       ├── SUCCESS → Server confirms → keep optimistic update ✅
       │
       └── FAILURE → Roll back the optimistic update ❌ + show error toast
```

**React Query implementation:**
```javascript
function useLikePost() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (postId) => api.likePost(postId),
    
    // Called before the mutation fires — snapshot current data
    onMutate: async (postId) => {
      // Cancel any in-flight refetches
      await queryClient.cancelQueries({ queryKey: ['posts'] });
      
      // Snapshot previous value
      const previousPosts = queryClient.getQueryData(['posts']);
      
      // Optimistically update the cache
      queryClient.setQueryData(['posts'], (old) => 
        old.map(post => 
          post.id === postId 
            ? { ...post, likeCount: post.likeCount + 1, isLiked: true }
            : post
        )
      );
      
      // Return snapshot for rollback
      return { previousPosts };
    },
    
    // Rollback on error using the snapshot
    onError: (err, postId, context) => {
      queryClient.setQueryData(['posts'], context.previousPosts);
      toast.error('Failed to like post');
    },
    
    // Refetch to get the true server state after success
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}
```

---

# 6. API Layer Design

## 6.1 Separating API from Components

**Bad — API calls directly in components:**
```jsx
// ❌ API call directly in component — untestable, not reusable
function ProductList() {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    fetch(`https://api.example.com/v2/products?page=1&limit=20`)
      .then(res => res.json())
      .then(data => setProducts(data.items));
  }, []);
  
  return <div>{products.map(p => <ProductCard key={p.id} product={p} />)}</div>;
}
```

**Good — Layered API architecture:**
```
Component → Custom Hook → Service Layer → Axios Instance → Server
```

---

## 6.2 Axios Instance Configuration

```javascript
// services/api.js — The Axios instance (single source of truth)
import axios from 'axios';
import { tokenManager } from './tokenManager';
import { handleApiError } from './errorHandler';

// Create a custom Axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,                              // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-App-Version': process.env.REACT_APP_VERSION,
  },
});

// REQUEST INTERCEPTOR — runs before every request
api.interceptors.request.use(
  (config) => {
    // Attach auth token to every request automatically
    const token = tokenManager.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add request ID for tracing/debugging
    config.headers['X-Request-ID'] = generateRequestId();
    
    return config;
  },
  (error) => Promise.reject(error)
);

// RESPONSE INTERCEPTOR — runs after every response
api.interceptors.response.use(
  (response) => {
    // Unwrap data (our API wraps in { data: ..., meta: ... })
    return response.data;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401 — token expired → try refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const newToken = await tokenManager.refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);      // Retry with new token
      } catch (refreshError) {
        tokenManager.logout();            // Refresh failed → logout
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(handleApiError(error));
  }
);

export default api;
```

---

## 6.3 Service Layer / Repository Pattern

```javascript
// services/productService.js — Repository for Product domain
import api from './api';

const PRODUCTS_BASE = '/products';

export const productService = {
  // Get all products with filtering/pagination
  getAll: async ({ page = 1, limit = 20, filters = {}, sort } = {}) => {
    const params = {
      page, limit, sort,
      ...filters,                           // Spread filter object as query params
    };
    return api.get(PRODUCTS_BASE, { params });
  },

  // Get a single product by ID
  getById: async (id) => {
    return api.get(`${PRODUCTS_BASE}/${id}`);
  },

  // Search products
  search: async (query, options = {}) => {
    return api.get(`${PRODUCTS_BASE}/search`, {
      params: { q: query, ...options }
    });
  },

  // Create a new product (admin)
  create: async (productData) => {
    return api.post(PRODUCTS_BASE, productData);
  },

  // Update a product (admin)
  update: async (id, updates) => {
    return api.patch(`${PRODUCTS_BASE}/${id}`, updates);
  },

  // Delete a product (admin)
  delete: async (id) => {
    return api.delete(`${PRODUCTS_BASE}/${id}`);
  },

  // Upload product image
  uploadImage: async (id, imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    return api.post(`${PRODUCTS_BASE}/${id}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        console.log(`Upload progress: ${percent}%`);
      },
    });
  },
};
```

---

## 6.4 Error Handling

```javascript
// services/errorHandler.js
export class AppError extends Error {
  constructor(message, code, statusCode, details = {}) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
    this.isAppError = true;
  }
}

export function handleApiError(axiosError) {
  // Network error (no response from server)
  if (!axiosError.response) {
    return new AppError(
      'Network error. Please check your connection.',
      'NETWORK_ERROR',
      0
    );
  }
  
  const { status, data } = axiosError.response;
  
  const errorMap = {
    400: () => new AppError(data?.message || 'Invalid request', 'BAD_REQUEST', 400, data?.errors),
    401: () => new AppError('Authentication required', 'UNAUTHORIZED', 401),
    403: () => new AppError('You don\'t have permission', 'FORBIDDEN', 403),
    404: () => new AppError('Resource not found', 'NOT_FOUND', 404),
    422: () => new AppError('Validation failed', 'VALIDATION_ERROR', 422, data?.errors),
    429: () => new AppError('Too many requests. Please slow down.', 'RATE_LIMIT', 429),
    500: () => new AppError('Server error. We\'re working on it.', 'SERVER_ERROR', 500),
  };
  
  return (errorMap[status] || (() => new AppError('An unexpected error occurred', 'UNKNOWN', status)))();
}
```

---

## 6.5 Retry Logic

```javascript
// utils/retry.js
export async function retryWithBackoff(fn, options = {}) {
  const {
    maxRetries = 3,
    initialDelay = 300,       // 300ms
    maxDelay = 5000,          // 5 seconds
    backoffFactor = 2,        // Exponential: 300 → 600 → 1200 → ...
    shouldRetry = (error) => error.statusCode >= 500, // Only retry server errors
  } = options;
  
  let lastError;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Don't retry on client errors (400, 401, 403, 404)
      if (!shouldRetry(error)) throw error;
      
      if (attempt === maxRetries) break;
      
      // Exponential backoff with jitter
      const delay = Math.min(
        initialDelay * Math.pow(backoffFactor, attempt) + Math.random() * 100,
        maxDelay
      );
      
      console.log(`Retry ${attempt + 1}/${maxRetries} in ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}
```

---

## 6.6 Request Deduplication

**Problem:** If 3 components mount simultaneously and all need `GET /user/profile`, you don't want 3 API calls.

**Solution:** React Query handles this automatically. Under the hood, it uses a query key cache.

```javascript
// All three of these components making the same request at the same time
// → React Query makes only ONE network call, shares the result with all

function Header() {
  const { data: user } = useQuery({ queryKey: ['user'], queryFn: getUser });
  return <Avatar src={user?.avatar} />;
}

function Sidebar() {
  const { data: user } = useQuery({ queryKey: ['user'], queryFn: getUser });
  return <p>Welcome, {user?.name}</p>;
}

function ProfileMenu() {
  const { data: user } = useQuery({ queryKey: ['user'], queryFn: getUser });
  return <span>{user?.email}</span>;
}
```

**Manual deduplication if not using React Query:**
```javascript
// Pending requests cache
const pendingRequests = new Map();

export function deduplicatedFetch(key, fetchFn) {
  if (pendingRequests.has(key)) {
    return pendingRequests.get(key); // Return same promise
  }
  
  const promise = fetchFn().finally(() => {
    pendingRequests.delete(key); // Clean up when done
  });
  
  pendingRequests.set(key, promise);
  return promise;
}
```

---

# 7. Authentication Architecture

## 7.1 Auth Flow Design

```
┌───────────────────────────────────────────────────────────────┐
│                 JWT Authentication Flow                        │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  User submits Login Form                                      │
│         │                                                     │
│         ↓                                                     │
│  POST /auth/login → { accessToken, refreshToken }            │
│         │                                                     │
│         ↓                                                     │
│  Store tokens:                                                │
│    accessToken  → Memory (JS variable) OR sessionStorage     │
│    refreshToken → httpOnly cookie (secure, samesite=strict)  │
│         │                                                     │
│         ↓                                                     │
│  Set Authorization header for all subsequent requests        │
│         │                                                     │
│         ↓                                                     │
│  accessToken expires (15 min)                                │
│         │                                                     │
│         ↓                                                     │
│  401 Response → Interceptor catches it                       │
│         │                                                     │
│         ↓                                                     │
│  POST /auth/refresh (refresh token sent via httpOnly cookie) │
│         │                                                     │
│         ├── Success → New accessToken → Retry original req   │
│         │                                                     │
│         └── Failure → Logout → Redirect to /login           │
└───────────────────────────────────────────────────────────────┘
```

---

## 7.2 Token Storage: The Debate

| Storage           | XSS Attack | CSRF Attack | Accessible to JS | Recommendation         |
|-------------------|------------|-------------|------------------|------------------------|
| localStorage      | ❌ Exposed  | ✅ Safe      | ✅ Yes            | Avoid for tokens       |
| sessionStorage    | ❌ Exposed  | ✅ Safe      | ✅ Yes            | Avoid for tokens       |
| In-memory (var)   | ✅ Safe     | ✅ Safe      | ✅ Yes            | Use for accessToken    |
| httpOnly Cookie   | ✅ Safe     | ❌ Vulnerable| ❌ No             | Use for refreshToken   |
| Cookie + SameSite | ✅ Safe     | ✅ Mitigated | ❌ No             | **Best option**        |

**Recommended Strategy:**
- `accessToken`: Store in memory (JavaScript variable). Short-lived (15 min). Lost on page refresh (intentional — silent refresh handles it).
- `refreshToken`: Store in `httpOnly; Secure; SameSite=Strict` cookie. Server-controlled.

---

## 7.3 Token Manager

```javascript
// services/tokenManager.js
let accessToken = null; // In-memory storage — not accessible to XSS

export const tokenManager = {
  getAccessToken: () => accessToken,
  
  setAccessToken: (token) => {
    accessToken = token;
  },
  
  clearAccessToken: () => {
    accessToken = null;
  },
  
  // Refresh token is sent via httpOnly cookie — we just call the endpoint
  refreshToken: async () => {
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include', // Send cookies
    });
    
    if (!response.ok) throw new Error('Token refresh failed');
    
    const { accessToken: newToken } = await response.json();
    tokenManager.setAccessToken(newToken);
    return newToken;
  },
  
  // Silent refresh — called on app startup (user already logged in from cookie)
  silentRefresh: async () => {
    try {
      return await tokenManager.refreshToken();
    } catch {
      return null; // User not logged in
    }
  },
  
  logout: async () => {
    tokenManager.clearAccessToken();
    await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
  },
};
```

---

## 7.4 Auth Context

```jsx
// context/AuthContext.jsx
const AuthContext = React.createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Start true — checking auth
  
  // On mount, do a silent refresh to restore session
  useEffect(() => {
    const initAuth = async () => {
      const token = await tokenManager.silentRefresh();
      
      if (token) {
        // Fetch user profile with the new token
        const userProfile = await authService.getProfile();
        setUser(userProfile);
      }
      
      setIsLoading(false);
    };
    
    initAuth();
  }, []);
  
  // Proactive token refresh — refresh 1 minute before expiry
  useEffect(() => {
    if (!user) return;
    
    const refreshInterval = setInterval(async () => {
      await tokenManager.refreshToken();
    }, 14 * 60 * 1000); // Every 14 minutes (token expires at 15)
    
    return () => clearInterval(refreshInterval);
  }, [user]);
  
  const login = async (credentials) => {
    const { accessToken, user: userData } = await authService.login(credentials);
    tokenManager.setAccessToken(accessToken);
    setUser(userData);
  };
  
  const logout = async () => {
    await tokenManager.logout();
    setUser(null);
  };
  
  if (isLoading) return <FullPageSpinner />;
  
  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = React.useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
```

---

## 7.5 Route Protection Patterns

```jsx
// components/ProtectedRoute.jsx
function ProtectedRoute({ 
  children, 
  requiredRole,
  fallback = <Navigate to="/login" replace /> 
}) {
  const { user, isAuthenticated } = useAuth();
  const location = useLocation();
  
  if (!isAuthenticated) {
    // Remember where user was trying to go
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  if (requiredRole && !user.roles.includes(requiredRole)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return children;
}

// Usage in routes
function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      
      {/* Authenticated routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardPage />
        </ProtectedRoute>
      } />
      
      {/* Role-based routes */}
      <Route path="/admin" element={
        <ProtectedRoute requiredRole="admin">
          <AdminPage />
        </ProtectedRoute>
      } />
    </Routes>
  );
}
```

---

# 8. Caching Architecture

## 8.1 Cache Hierarchy

```
Browser Request
       │
       ↓
  ┌────────────────────┐
  │  Service Worker     │ ← Intercepts all requests
  │  Cache (offline)    │
  └────────┬───────────┘
           │ Cache miss
           ↓
  ┌────────────────────┐
  │  HTTP Cache         │ ← Browser cache (ETags, Cache-Control)
  │  (disk/memory)      │
  └────────┬───────────┘
           │ Cache miss
           ↓
  ┌────────────────────┐
  │  Application Cache  │ ← React Query / SWR in-memory cache
  │  (React Query)      │
  └────────┬───────────┘
           │ Cache miss or stale
           ↓
  ┌────────────────────┐
  │  API Server         │ ← Actual network request
  │  (CDN / Origin)     │
  └────────────────────┘
```

---

## 8.2 HTTP Cache Headers

```
Cache-Control: max-age=3600         # Cache for 1 hour
Cache-Control: no-store             # Never cache
Cache-Control: no-cache             # Cache but always validate with server
Cache-Control: stale-while-revalidate=60  # Serve stale while fetching fresh
ETag: "abc123"                      # Fingerprint — server responds 304 if unchanged
Last-Modified: Fri, 05 Jul 2024     # Timestamp-based validation
```

---

## 8.3 React Query Cache Architecture

```javascript
// Configuring React Query globally
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // How long data stays in cache after component unmounts
      gcTime: 5 * 60 * 1000,          // 5 minutes (formerly cacheTime)
      
      // How long fetched data is considered "fresh" (no refetch)
      staleTime: 60 * 1000,            // 1 minute
      
      // Refetch on window focus (detect stale data)
      refetchOnWindowFocus: true,
      
      // Retry config
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});

// Per-query configuration
function useProducts(filters) {
  return useQuery({
    queryKey: ['products', filters],   // Cache key — changes → new fetch
    queryFn: () => productService.getAll(filters),
    
    staleTime: 2 * 60 * 1000,         // Products stale after 2 min
    gcTime: 10 * 60 * 1000,           // Keep in cache for 10 min after unmount
    
    // Serve stale data while fetching fresh
    placeholderData: keepPreviousData,
    
    // Only fetch when filter is ready
    enabled: !!filters,
  });
}
```

---

## 8.4 Cache Key Design

**Principle:** Cache keys should encode everything that makes one request different from another.

```javascript
// ✅ GOOD cache key design
['products']                          // All products (no filters)
['products', { category: 'shoes' }]  // Filtered products
['products', { page: 2, limit: 20 }] // Paginated products
['product', 42]                       // Single product by ID
['product', 42, 'reviews']           // Reviews for product 42
['user']                              // Current user
['user', 42, 'followers']            // User 42's followers

// ❌ BAD — same data, different key format (cache miss!)
['products', 'category=shoes']
['products', { category: 'shoes' }]
// These are different keys! Use consistent format.
```

---

## 8.5 Stale-While-Revalidate Strategy

**What:** Serve cached (possibly stale) data immediately, then update in the background.

```
User visits page
      │
      ↓
  Cache has data?
      │
     YES ──→ Render immediately (even if stale) ←──────────────┐
      │                                                          │
      ↓                                                          │
  Is data stale?                                                 │
      │                                                          │
     YES ──→ Fetch fresh data in background ──── Update cache ──┘
              (user doesn't see a loading state)
     NO  ──→ Do nothing
```

**Result:** Users never see loading spinners for previously visited data. Background updates keep data fresh.

---

# 9. Error Handling Architecture

## 9.1 Layered Error Handling

```
┌───────────────────────────────────────────────────────────────┐
│                  Error Handling Layers                         │
│                                                               │
│  Layer 1: Global Error Boundary                               │
│           → Catches catastrophic JS errors                    │
│           → Shows full-page fallback                          │
│                                                               │
│  Layer 2: Feature-Level Error Boundary                        │
│           → Catches errors in a feature section               │
│           → Shows feature-specific fallback                   │
│                                                               │
│  Layer 3: API Error Handling (Axios interceptors)             │
│           → Handles HTTP errors globally                      │
│           → Translates to user-friendly messages              │
│                                                               │
│  Layer 4: Component-Level try/catch                           │
│           → Handles specific async operations                 │
│           → Shows inline error states                         │
└───────────────────────────────────────────────────────────────┘
```

---

## 9.2 Global Error Boundary

```jsx
// components/ErrorBoundary.jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  
  static getDerivedStateFromError(error) {
    // Update state to show fallback UI
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log to error reporting service
    errorReportingService.captureError(error, {
      componentStack: errorInfo.componentStack,
      extra: {
        userId: this.props.userId,
        route: window.location.pathname,
      }
    });
  }
  
  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };
  
  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided, otherwise use default
      if (this.props.FallbackComponent) {
        return (
          <this.props.FallbackComponent
            error={this.state.error}
            onReset={this.handleReset}
          />
        );
      }
      
      return (
        <div className="error-boundary-fallback">
          <h2>Something went wrong</h2>
          <p>We've been notified and are looking into it.</p>
          <button onClick={this.handleReset}>Try Again</button>
          <button onClick={() => window.location.href = '/'}>Go Home</button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Usage — layered boundaries
function App() {
  return (
    <ErrorBoundary FallbackComponent={GlobalErrorPage}>  {/* Layer 1 */}
      <Router>
        <ErrorBoundary FallbackComponent={FeatureErrorFallback}>  {/* Layer 2 */}
          <ProductFeature />
        </ErrorBoundary>
      </Router>
    </ErrorBoundary>
  );
}
```

---

## 9.3 Circuit Breaker Pattern

**What:** If an API is repeatedly failing, stop calling it for a period to avoid cascading failures.

```javascript
// utils/circuitBreaker.js
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.recoveryTimeout = options.recoveryTimeout || 30000; // 30 seconds
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED = normal, OPEN = blocking, HALF_OPEN = testing
  }
  
  async execute(fn) {
    if (this.state === 'OPEN') {
      // Check if recovery timeout has passed
      if (Date.now() - this.lastFailureTime > this.recoveryTimeout) {
        this.state = 'HALF_OPEN'; // Try one request
      } else {
        throw new Error('Circuit breaker is OPEN — service unavailable');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      console.warn(`Circuit breaker tripped after ${this.failureCount} failures`);
    }
  }
}

// Usage
const apiCircuitBreaker = new CircuitBreaker({ failureThreshold: 5 });

async function fetchProducts() {
  return apiCircuitBreaker.execute(() => productService.getAll());
}
```

---

# 10. Performance Architecture

## 10.1 Critical Rendering Path

```
HTML  → DOM
               ↘
CSS   → CSSOM  → Render Tree → Layout → Paint → Composite
               ↗
JS    → (can block both DOM and CSSOM construction)
```

**Optimization strategies:**
- Place CSS in `<head>` (render-blocking but necessary)
- Place scripts at end of `<body>` or use `defer`/`async`
- Minimize render-blocking resources
- Inline critical CSS
- Use `<link rel="preload">` for critical resources

---

## 10.2 Code Splitting Strategy

```jsx
// Route-level splitting (most impactful)
import { lazy, Suspense } from 'react';

const ProductPage = lazy(() => import('./pages/ProductPage'));
const CheckoutPage = lazy(() => import('./pages/CheckoutPage'));
const AdminPage = lazy(() => import('./pages/AdminPage'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/products" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </Suspense>
  );
}

// Component-level splitting (for heavy components)
const HeavyChart = lazy(() => import('./components/HeavyChart'));
const RichTextEditor = lazy(() => import('./components/RichTextEditor'));

// Feature flag splitting
const loadFeature = (featureName) => {
  return lazy(() => import(`./features/${featureName}`));
};
```

---

## 10.3 Performance Budget

| Metric                    | Good       | Needs Improvement | Poor     |
|---------------------------|------------|-------------------|----------|
| LCP (Largest Contentful Paint) | < 2.5s  | 2.5s - 4.0s      | > 4.0s   |
| FID (First Input Delay)   | < 100ms    | 100ms - 300ms     | > 300ms  |
| CLS (Cumulative Layout Shift) | < 0.1  | 0.1 - 0.25        | > 0.25   |
| TTI (Time to Interactive) | < 3.8s     | 3.9s - 7.3s       | > 7.3s   |
| Bundle Size (initial JS)  | < 200KB    | 200-350KB         | > 350KB  |

**Monitoring tools:** Lighthouse, WebPageTest, Chrome User Experience Report (CrUX), Sentry Performance, Datadog RUM

---

## 10.4 Virtualization for Long Lists

```jsx
// Without virtualization: 10,000 DOM nodes
function NaiveList({ items }) {
  return (
    <ul>
      {items.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}

// With virtualization: only ~20 DOM nodes at any time
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}> {/* style has position/top/height from library */}
      <ListItem item={items[index]} />
    </div>
  );
  
  return (
    <FixedSizeList
      height={600}          // Viewport height
      width="100%"
      itemCount={items.length}
      itemSize={72}         // Each row is 72px tall
    >
      {Row}
    </FixedSizeList>
  );
}
```

---

# 11. Micro-Frontend Architecture

## 11.1 What and Why

**What:** Micro-frontends extend the microservices philosophy to frontend development. Instead of one large React app, you have multiple independently deployable frontend apps that compose together.

```
                     ┌──────────────────────────┐
                     │      Shell App            │
                     │  (app-container.js)       │
                     └──────────┬───────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────┴──────┐ ┌──────┴──────┐ ┌─────┴───────┐
        │  Auth MFE    │ │ Products MFE│ │  Cart MFE   │
        │  (Team A)    │ │  (Team B)   │ │  (Team C)   │
        └──────────────┘ └─────────────┘ └─────────────┘
          React 18          Vue 3          React 18
          Deploys           Deploys        Deploys
          independently     independently  independently
```

---

## 11.2 Module Federation (Webpack 5)

```javascript
// products-app/webpack.config.js (the remote)
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'productsApp',
      filename: 'remoteEntry.js',      // Entry point that shell loads
      exposes: {
        './ProductCard': './src/components/ProductCard',
        './ProductSearch': './src/components/ProductSearch',
      },
      shared: {
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
      },
    }),
  ],
};

// shell-app/webpack.config.js (the host)
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: {
        productsApp: 'productsApp@https://products.example.com/remoteEntry.js',
        cartApp: 'cartApp@https://cart.example.com/remoteEntry.js',
      },
      shared: {
        react: { singleton: true },
        'react-dom': { singleton: true },
      },
    }),
  ],
};

// shell-app/src/App.jsx
const ProductCard = lazy(() => import('productsApp/ProductCard'));

function App() {
  return (
    <div>
      <Suspense fallback={<Spinner />}>
        <ProductCard productId={42} />
      </Suspense>
    </div>
  );
}
```

---

## 11.3 Communication Between Micro-Frontends

```javascript
// Method 1: Custom Events (decoupled)
// Cart MFE publishes event
window.dispatchEvent(new CustomEvent('cart:item:added', {
  detail: { productId: 42, quantity: 1 }
}));

// Shell or another MFE subscribes
window.addEventListener('cart:item:added', (event) => {
  updateCartBadge(event.detail.quantity);
});

// Method 2: Shared State (via shared library)
// packages/shared-store/src/store.js
import { createStore } from 'zustand/vanilla';

export const appStore = createStore((set) => ({
  user: null,
  cartCount: 0,
  setUser: (user) => set({ user }),
  incrementCart: () => set(state => ({ cartCount: state.cartCount + 1 })),
}));

// Method 3: Props passing via Shell (tight coupling — avoid)
function Shell() {
  const [user, setUser] = useState(null);
  
  return (
    <>
      <AuthApp onLogin={setUser} />
      <ProductsApp user={user} />  {/* Shell passes user to each MFE */}
    </>
  );
}
```

---

## 11.4 When to Use Micro-Frontends

| Use Case                          | Recommendation              |
|-----------------------------------|-----------------------------|
| Single team, single codebase      | ❌ Don't use MFE             |
| Multiple teams, shared codebase   | Maybe — try monorepo first  |
| Multiple teams, need independence | ✅ Good candidate for MFE    |
| Different tech stacks needed      | ✅ Strong case for MFE       |
| Independent deployment needed     | ✅ Strong case for MFE       |
| Startup / small app               | ❌ Huge overhead             |

---

# 12. Design Patterns in React

## 12.1 Provider Pattern

```jsx
// Provide theme, auth, locale — everything the app needs at root level
function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <ThemeProvider>
            <LocaleProvider>
              <Router>
                <AppRoutes />
              </Router>
            </LocaleProvider>
          </ThemeProvider>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
```

**Context Splitting:** Don't put unrelated state in the same context — it causes unnecessary re-renders.

```jsx
// ❌ BAD — user change re-renders ALL theme consumers and vice versa
const AppContext = createContext({ user, theme, cart, locale });

// ✅ GOOD — each context is independent
const AuthContext = createContext(null);
const ThemeContext = createContext(null);
const CartContext = createContext(null);
```

---

## 12.2 Container/Presenter Pattern

```jsx
// Container — handles data and logic
function ProductListContainer() {
  const { filters } = useProductFilters();
  const { data: products, isLoading, error } = useProducts(filters);
  
  if (isLoading) return <ProductListSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  
  return <ProductListPresenter products={products} />;
}

// Presenter — handles rendering only
function ProductListPresenter({ products }) {
  return (
    <div className="product-list">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

---

# 13. Component-Level System Design Questions

## 13.1 Autocomplete Search Component

### Requirements
- **Functional:** Show suggestions as user types, keyboard navigation, mouse selection, clear button, debouncing, loading state, empty state
- **Non-Functional:** Accessible (ARIA combobox), < 100ms perceived response, handles 10k option list

### Props Interface
```typescript
interface AutocompleteProps {
  placeholder?: string;
  onSearch: (query: string) => Promise<SearchResult[]>;
  onSelect: (result: SearchResult) => void;
  debounceMs?: number;                 // default: 300
  minChars?: number;                   // default: 2 (don't search for 1 char)
  maxResults?: number;                 // default: 10
  renderResult?: (result: SearchResult) => React.ReactNode;
  emptyMessage?: string;
}
```

### State Design
```javascript
const state = {
  query: '',            // Current input value
  results: [],          // Search results
  isOpen: false,        // Dropdown visibility
  isLoading: false,     // Loading state
  selectedIndex: -1,    // Keyboard navigation cursor
  error: null,          // Error state
};
```

### Complete Implementation
```jsx
function Autocomplete({ onSearch, onSelect, debounceMs = 300, minChars = 2 }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [error, setError] = useState(null);
  
  const inputRef = useRef(null);
  const listRef = useRef(null);
  const abortControllerRef = useRef(null);
  
  // Debounced search function
  const debouncedSearch = useCallback(
    debounce(async (searchQuery) => {
      if (searchQuery.length < minChars) {
        setResults([]);
        setIsOpen(false);
        return;
      }
      
      // Cancel previous request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      abortControllerRef.current = new AbortController();
      
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await onSearch(searchQuery);
        setResults(data);
        setIsOpen(true);
        setSelectedIndex(-1);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError('Failed to load results');
        }
      } finally {
        setIsLoading(false);
      }
    }, debounceMs),
    [onSearch, minChars, debounceMs]
  );
  
  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };
  
  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(i => Math.min(i + 1, results.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(i => Math.max(i - 1, -1));
        break;
      case 'Enter':
        if (selectedIndex >= 0) {
          handleSelect(results[selectedIndex]);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        inputRef.current.blur();
        break;
    }
  };
  
  const handleSelect = (result) => {
    setQuery(result.label);
    setIsOpen(false);
    onSelect(result);
  };
  
  return (
    <div className="autocomplete" role="combobox" aria-expanded={isOpen}>
      <input
        ref={inputRef}
        value={query}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        aria-autocomplete="list"
        aria-controls="autocomplete-listbox"
        aria-activedescendant={selectedIndex >= 0 ? `option-${selectedIndex}` : undefined}
      />
      
      {isLoading && <Spinner />}
      
      {isOpen && (
        <ul id="autocomplete-listbox" ref={listRef} role="listbox">
          {results.length === 0 ? (
            <li className="autocomplete__empty">No results found</li>
          ) : (
            results.map((result, index) => (
              <li
                key={result.id}
                id={`option-${index}`}
                role="option"
                aria-selected={index === selectedIndex}
                className={`autocomplete__option ${index === selectedIndex ? 'autocomplete__option--focused' : ''}`}
                onMouseDown={(e) => e.preventDefault()} // Prevent input blur
                onClick={() => handleSelect(result)}
              >
                {result.label}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
```

### Performance Considerations
- Debounce prevents API call on every keystroke
- AbortController cancels stale requests
- `onMouseDown` with `e.preventDefault()` prevents input blur before click
- Keyboard navigation without re-rendering the list

---

## 13.2 Data Grid / Table with Pagination

### Architecture
```
┌─────────────────────────────────────────────────────────┐
│  DataGrid                                               │
│  ├── Toolbar (search, filter, bulk actions, export)     │
│  ├── TableHeader (sortable columns, select all)         │
│  ├── TableBody                                          │
│  │   └── TableRow[] (with cells, checkbox, actions)    │
│  ├── Pagination (page controls, page size, item count) │
│  └── Loading Overlay / Empty State                      │
└─────────────────────────────────────────────────────────┘
```

### Column Definition Interface
```typescript
interface Column<T> {
  key: keyof T;
  header: string;
  width?: number;
  minWidth?: number;
  sortable?: boolean;
  filterable?: boolean;
  render?: (value: T[keyof T], row: T, rowIndex: number) => React.ReactNode;
  headerRender?: () => React.ReactNode;
}

interface DataGridProps<T> {
  data: T[];
  columns: Column<T>[];
  rowKey: keyof T | ((row: T) => string);
  
  // Pagination
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
    onChange: (page: number, pageSize: number) => void;
    pageSizeOptions?: number[];
  };
  
  // Sorting
  sortConfig?: { key: string; direction: 'asc' | 'desc' };
  onSort?: (key: string, direction: 'asc' | 'desc') => void;
  
  // Selection
  selectable?: boolean;
  selectedKeys?: Set<string>;
  onSelectionChange?: (keys: Set<string>) => void;
  
  // States
  isLoading?: boolean;
  emptyMessage?: string;
  error?: string;
}
```

---

## 13.3 Infinite Scroll Feed

### Architecture Decision: Scroll-based vs Intersection Observer

```
Scroll Event (BAD)              Intersection Observer (GOOD)
─────────────────               ─────────────────────────────
Fires 60+/second                Fires only when sentinel
Causes layout thrash             crosses viewport
Needs throttle/debounce         Native browser API
Higher CPU usage                Efficient, off main thread
```

```jsx
function InfiniteScrollFeed({ queryKey, fetchFn, renderItem }) {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey,
    queryFn: ({ pageParam = 1 }) => fetchFn(pageParam),
    getNextPageParam: (lastPage) => 
      lastPage.hasMore ? lastPage.nextPage : undefined,
  });
  
  // Sentinel element at the bottom of the list
  const sentinelRef = useRef(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 0.1 }
    );
    
    if (sentinelRef.current) observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);
  
  const allItems = data?.pages.flatMap(page => page.items) ?? [];
  
  return (
    <div className="feed">
      {allItems.map(item => renderItem(item))}
      
      {/* Sentinel — when this enters viewport, load more */}
      <div ref={sentinelRef} className="feed__sentinel" />
      
      {isFetchingNextPage && <FeedSkeleton count={3} />}
      {!hasNextPage && <p className="feed__end">You're all caught up!</p>}
    </div>
  );
}
```

---

## 13.4 Virtual Scroll List

```jsx
import { FixedSizeList, VariableSizeList } from 'react-window';

// For items with variable heights (e.g., chat messages, feed posts)
function VirtualFeed({ items }) {
  const listRef = useRef(null);
  const rowHeights = useRef({});
  
  const getItemSize = (index) => rowHeights.current[index] || 100; // default 100px
  
  const setRowHeight = (index, size) => {
    if (rowHeights.current[index] !== size) {
      rowHeights.current[index] = size;
      listRef.current?.resetAfterIndex(index); // Tell react-window to recalculate
    }
  };
  
  const Row = ({ index, style }) => {
    const rowRef = useRef(null);
    
    useEffect(() => {
      if (rowRef.current) {
        setRowHeight(index, rowRef.current.getBoundingClientRect().height);
      }
    }, [index]);
    
    return (
      <div style={style}>
        <div ref={rowRef}>
          <FeedPost post={items[index]} />
        </div>
      </div>
    );
  };
  
  return (
    <VariableSizeList
      ref={listRef}
      height={window.innerHeight}
      width="100%"
      itemCount={items.length}
      itemSize={getItemSize}
    >
      {Row}
    </VariableSizeList>
  );
}
```

---

## 13.5 Chat Interface

### Architecture
```
┌──────────────────────────────────────────────────────────┐
│  ChatRoom                                                │
│  ├── MessageList (virtualized)                           │
│  │   └── Message (text/image/file, read receipts)       │
│  ├── TypingIndicator                                     │
│  └── MessageInput                                        │
│      ├── TextArea (auto-resize)                          │
│      ├── EmojiPicker                                     │
│      └── AttachmentButton                               │
└──────────────────────────────────────────────────────────┘
```

### Key Design Decisions

```javascript
// 1. WebSocket connection management
const socketRef = useRef(null);

useEffect(() => {
  socketRef.current = io(SOCKET_URL, {
    auth: { token: tokenManager.getAccessToken() },
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
  });
  
  return () => socketRef.current?.disconnect();
}, []);

// 2. Optimistic message sending
const sendMessage = (text) => {
  const tempMessage = {
    id: `temp-${Date.now()}`,
    text,
    sender: currentUser,
    timestamp: new Date(),
    status: 'sending',   // Not confirmed yet
  };
  
  // Add optimistically
  addMessageToList(tempMessage);
  
  // Send via WebSocket
  socketRef.current.emit('message:send', { text, roomId }, (ack) => {
    if (ack.success) {
      // Replace temp message with confirmed one
      replaceMessage(tempMessage.id, ack.message);
    } else {
      // Mark as failed
      updateMessage(tempMessage.id, { status: 'failed' });
    }
  });
};
```

---

## 13.6 Notification System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  Notification Architecture                    │
│                                                              │
│  Sources:                                                    │
│    WebSocket (real-time) ──┐                                 │
│    Polling (fallback)  ────┼──→  NotificationStore          │
│    User action (local) ────┘         │                      │
│                                      ↓                      │
│                             NotificationProvider            │
│                                 (Context)                   │
│                                      │                      │
│                    ┌─────────────────┼─────────────────┐   │
│                    ↓                 ↓                  ↓   │
│               Bell Icon       Toast System          Center  │
│             (count badge)    (top-right corner) (full list) │
└──────────────────────────────────────────────────────────────┘
```

---

# 14. Application-Level System Design

## 14.1 Facebook News Feed

### Requirements
- Display personalized posts from friends/pages
- Like, comment, share
- Real-time updates (new posts appear at top)
- Infinite scroll
- Multiple content types (text, image, video, link preview)

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                    News Feed Architecture                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    App Shell                              │   │
│  │  ┌─────────┐  ┌──────────────────────┐  ┌───────────┐   │   │
│  │  │ Navbar  │  │    Feed Container    │  │ Sidebar   │   │   │
│  │  │ (fixed) │  │                      │  │ (friends/ │   │   │
│  │  └─────────┘  │  ┌────────────────┐ │  │ groups)   │   │   │
│  │               │  │ StoryBar       │ │  └───────────┘   │   │
│  │               │  └────────────────┘ │                   │   │
│  │               │  ┌────────────────┐ │                   │   │
│  │               │  │ CreatePost     │ │                   │   │
│  │               │  └────────────────┘ │                   │   │
│  │               │  ┌────────────────┐ │                   │   │
│  │               │  │ FeedList       │ │                   │   │
│  │               │  │ (virtualized)  │ │                   │   │
│  │               │  │ ├─ PostCard    │ │                   │   │
│  │               │  │ ├─ PostCard    │ │                   │   │
│  │               │  │ └─ Loading...  │ │                   │   │
│  │               │  └────────────────┘ │                   │   │
│  │               └──────────────────────┘                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### State Design
```javascript
// Server State (React Query)
const feedQuery = useInfiniteQuery({
  queryKey: ['feed', userId],
  queryFn: ({ pageParam }) => feedService.getFeed({ cursor: pageParam }),
  getNextPageParam: (lastPage) => lastPage.nextCursor,
  staleTime: 30 * 1000,              // Feed stales after 30 seconds
  refetchInterval: 60 * 1000,        // Poll for new posts every minute
});

// Local State (per post — for optimistic updates)
const likePost = useLikePost(); // Optimistic mutation hook
```

### API Design
```
GET  /api/feed?cursor={cursor}&limit=20
     → { posts: Post[], nextCursor: string | null, newPostCount: number }

POST /api/posts
     → { post: Post }

POST /api/posts/{id}/reactions
     → { reactionCount: number, userReaction: string }

GET  /api/feed/poll?since={lastCursor}
     → { newCount: number }   (lightweight poll to show "3 new posts" banner)
```

### Performance Strategy
- Virtualized feed list (react-window)
- Images: lazy loading with blur placeholder (`loading="lazy"`, blurhash)
- Videos: autoplay only in viewport (Intersection Observer)
- New posts: show "N new posts" banner instead of auto-inserting at top (prevents scroll jump)
- Infinite scroll with cursor-based pagination

---

## 14.2 Twitter/X Design

```
┌────────────────────────────────────────────────────────────────┐
│                      Twitter Architecture                       │
│                                                                 │
│  ┌────────┐   ┌──────────────────────┐   ┌─────────────────┐  │
│  │  Left  │   │    Tweet Feed        │   │  Right Sidebar  │  │
│  │  Nav   │   │                      │   │  (Trending/Who  │  │
│  │        │   │  ┌────────────────┐  │   │   to Follow)    │  │
│  │ Home   │   │  │ ComposeBox     │  │   │                 │  │
│  │ Explore│   │  └────────────────┘  │   │                 │  │
│  │ Notif  │   │  ┌────────────────┐  │   │                 │  │
│  │ Messages│  │  │ TabBar         │  │   │                 │  │
│  │ Profile│   │  │(For You/Follow)│  │   │                 │  │
│  │        │   │  └────────────────┘  │   │                 │  │
│  │        │   │  ┌────────────────┐  │   │                 │  │
│  │        │   │  │  Tweet[]       │  │   │                 │  │
│  │        │   │  │  (virtual list)│  │   │                 │  │
│  └────────┘   └──────────────────────┘   └─────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Optimistic like/retweet** — instant UI update, rollback on failure
2. **Thread rendering** — recursive `TweetThread` component
3. **Media handling** — lazy load images, twitter card for links
4. **Real-time** — WebSocket for new tweets, notifications
5. **Cursor-based pagination** — not offset (Twitter's feed changes too fast)

---

## 14.3 Amazon Product Listing

```
┌────────────────────────────────────────────────────────────────┐
│                   Amazon Product Page Architecture             │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  Header (Search Bar + Cart + Account + Departments)   │    │
│  └───────────────────────────────────────────────────────┘    │
│  ┌──────────────┐  ┌────────────────────────────────────┐     │
│  │ FilterPanel  │  │         ProductGrid                │     │
│  │              │  │                                    │     │
│  │ Department   │  │  ┌──────┐  ┌──────┐  ┌──────┐    │     │
│  │ Price Range  │  │  │Card  │  │Card  │  │Card  │    │     │
│  │ Brand        │  │  └──────┘  └──────┘  └──────┘    │     │
│  │ Rating ≥ 4   │  │                                    │     │
│  │ Prime Only   │  │  ┌──────┐  ┌──────┐  ┌──────┐    │     │
│  │ Delivery     │  │  │Card  │  │Card  │  │Card  │    │     │
│  │              │  │  └──────┘  └──────┘  └──────┘    │     │
│  └──────────────┘  │  ┌──────────────────────────────┐ │     │
│                    │  │       Pagination              │ │     │
│                    │  └──────────────────────────────┘ │     │
│                    └────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────┘
```

### URL-Based Filter State
```javascript
// Filters live in URL — shareable and bookmarkable
function useProductFilters() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const filters = {
    category: searchParams.get('category'),
    minPrice: Number(searchParams.get('minPrice')) || 0,
    maxPrice: Number(searchParams.get('maxPrice')) || Infinity,
    brand: searchParams.getAll('brand'),        // Multi-value
    rating: Number(searchParams.get('rating')) || 0,
    prime: searchParams.get('prime') === 'true',
    sort: searchParams.get('sort') || 'relevance',
    page: Number(searchParams.get('page')) || 1,
  };
  
  const setFilter = (key, value) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (value === null || value === undefined || value === '') {
        next.delete(key);
      } else {
        next.set(key, String(value));
      }
      next.set('page', '1');  // Reset to page 1 when filter changes
      return next;
    });
  };
  
  return { filters, setFilter };
}
```

---

## 14.4 Netflix Home Page

```
┌────────────────────────────────────────────────────────────────┐
│                    Netflix Architecture                        │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  Hero Section (Featured Movie - autoplay trailer)      │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  ContentRow: "Trending Now"                            │    │
│  │  ← [Card][Card][Card][Card][Card][Card][Card] →        │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  ContentRow: "Continue Watching"                       │    │
│  │  ← [Card+Progress][Card][Card][Card] →                 │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                │
│  (More rows loaded as user scrolls — lazy loaded rows)        │
└────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Row-level lazy loading:** Each content row fetches its own data when it's near the viewport (Intersection Observer per row)
2. **Card hover preview:** Debounced hover (500ms) before showing trailer preview, to avoid triggering on mouse-over
3. **Video quality:** Adaptive bitrate (HLS/DASH), quality based on network speed
4. **Continue Watching:** Sync watch progress via periodic API calls + local storage backup

---

## 14.5 Jira Kanban Board

```
┌────────────────────────────────────────────────────────────────┐
│                      Kanban Architecture                       │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  TODO    │  │  IN PROG │  │  REVIEW  │  │   DONE   │     │
│  │          │  │          │  │          │  │          │     │
│  │ [Task 1] │  │ [Task 3] │  │ [Task 5] │  │ [Task 7] │     │
│  │ [Task 2] │  │ [Task 4] │  │          │  │ [Task 8] │     │
│  │          │  │          │  │          │  │          │     │
│  │  + Add   │  │  + Add   │  │  + Add   │  │  + Add   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                                │
│  DnD Library: @dnd-kit/core (accessible, performant)          │
└────────────────────────────────────────────────────────────────┘
```

### State Design
```javascript
const boardState = {
  columns: {
    'todo': { id: 'todo', title: 'TODO', taskIds: ['task-1', 'task-2'] },
    'in-progress': { id: 'in-progress', title: 'In Progress', taskIds: ['task-3'] },
    'review': { id: 'review', title: 'Review', taskIds: ['task-5'] },
    'done': { id: 'done', title: 'Done', taskIds: ['task-7', 'task-8'] },
  },
  tasks: {
    'task-1': { id: 'task-1', title: 'Build login page', assignee: {...}, priority: 'high' },
    // ...
  },
  columnOrder: ['todo', 'in-progress', 'review', 'done'],
};

// On drag end — optimistic update
function handleDragEnd(event) {
  const { active, over } = event;
  if (!over) return;
  
  const sourceColumn = findColumnByTaskId(active.id);
  const destColumn = findColumnById(over.id); // Over a column or a task
  
  if (sourceColumn === destColumn) {
    // Reorder within same column
    reorderTask(sourceColumn.id, active.id, over.id);
  } else {
    // Move to different column
    moveTask(active.id, sourceColumn.id, destColumn.id, over.id);
  }
  
  // Optimistic update + API call
  api.updateTaskStatus(active.id, destColumn.id);
}
```

---

# 15. System Design Interview Checklist

## Before You Start Designing

```
☐ Clarified functional requirements
☐ Clarified non-functional requirements (scale, performance, accessibility)
☐ Asked about existing constraints (tech stack, team size, timeline)
☐ Stated assumptions clearly
☐ Announced which RADIO sections you'll cover
```

## During Design

```
☐ Drew component hierarchy / architecture diagram
☐ Defined data model (API response shape, client state shape)
☐ Designed component props interfaces
☐ Addressed all CRUD operations or user flows
☐ Mentioned loading, error, and empty states
☐ Addressed accessibility (ARIA roles, keyboard navigation)
☐ Mentioned performance strategy (code splitting, virtualization, caching)
☐ Mentioned error handling strategy
☐ Considered mobile/responsive behavior
```

## After Design

```
☐ Discussed trade-offs of your choices
☐ Mentioned what you'd do differently at larger scale
☐ Identified open questions / things requiring more research
☐ Asked interviewer if there are specific areas to deep dive
```

---

# 16. Top 25 Frontend System Design Questions

| # | Question | Key Topics |
|---|----------|-----------|
| 1 | Design a News Feed (Facebook) | Infinite scroll, real-time, virtualization, optimistic updates |
| 2 | Design an Autocomplete Search | Debouncing, cancellation, keyboard nav, ARIA |
| 3 | Design a Chat Application | WebSockets, optimistic messages, presence, rooms |
| 4 | Design a Kanban Board (Jira) | DnD, complex state, real-time sync |
| 5 | Design Google Docs (collaborative) | OT/CRDT, WebSockets, conflict resolution |
| 6 | Design a Video Streaming Platform | HLS/DASH, adaptive bitrate, player, recommendations |
| 7 | Design a Photo Sharing App (Instagram) | Upload, CDN, lazy loading, stories |
| 8 | Design an E-commerce Product Page | Cart, variants, reviews, real-time inventory |
| 9 | Design a Dashboard with Charts | Data visualization, real-time updates, filtering |
| 10 | Design a Form Builder | Dynamic forms, validation, drag-to-reorder |
| 11 | Design a Notification System | Real-time, channels, preferences, badge |
| 12 | Design Google Maps-like App | Map tiles, overlays, geolocation, clustering |
| 13 | Design a File Upload Component | Chunked upload, progress, retry, drag-drop |
| 14 | Design a Rich Text Editor | ContentEditable, keyboard shortcuts, formatting |
| 15 | Design a Date Range Picker | Calendar UI, keyboard nav, constraints, localization |
| 16 | Design a Virtual Scroll List | Windowing, variable heights, dynamic loading |
| 17 | Design a Multi-Step Form / Wizard | Step state, validation per step, back/forward |
| 18 | Design Twitter/X | Feed, tweet thread, real-time, optimistic like |
| 19 | Design Airbnb Search | Map + list sync, filters, URL state |
| 20 | Design a Design System | Tokens, Storybook, a11y, versioning |
| 21 | Design Netflix | Rows, hover preview, adaptive video, continue watching |
| 22 | Design a Polling/Survey App | Real-time results, animations, form logic |
| 23 | Design a Code Editor (VS Code-like) | Monaco Editor, file tree, tabs, syntax highlighting |
| 24 | Design an Admin Data Table | Sort, filter, pagination, bulk actions, export |
| 25 | Design Slack | Channels, DMs, threads, search, file sharing |

---

# 17. Five Full Design Exercises

## Exercise 1: Design a YouTube-Like Video Feed

**Prompt:** Design the frontend for a YouTube-like homepage video feed. Users can browse recommendations, search for videos, and interact with video cards.

**Your Answer Should Cover:**

### Requirements (R)
- Functional: Browse feed, search, hover preview, click to watch, like/save
- Non-functional: LCP < 2.5s, handle 10k+ videos in feed

### Architecture (A)
```
App
├── Header (Logo, Search, User)
├── Sidebar (Navigation)
└── MainContent
    ├── VideoGrid (CSS Grid, responsive)
    │   └── VideoCard[]
    │       ├── Thumbnail (lazy image)
    │       ├── HoverPreview (lazy loaded gif/video on hover)
    │       ├── ChannelAvatar
    │       └── MetaInfo (title, views, time)
    └── LoadMoreSentinel (IntersectionObserver)
```

### Data Model (D)
```typescript
interface Video {
  id: string;
  title: string;
  thumbnailUrl: string;
  previewUrl?: string;        // Hover preview
  duration: number;           // seconds
  viewCount: number;
  publishedAt: string;
  channel: {
    id: string;
    name: string;
    avatarUrl: string;
    verified: boolean;
  };
}
```

### Interface (I)
```typescript
interface VideoCardProps {
  video: Video;
  layout?: 'grid' | 'list';   // Grid for homepage, list for search results
}
```

### Optimizations (O)
- Thumbnail: `loading="lazy"`, `width` and `height` attributes set (prevent CLS)
- Hover preview: debounce 500ms, cancel on mouse leave
- Channel avatar: tiny (32x32), aggressive caching
- Infinite scroll via IntersectionObserver
- Responsive grid: CSS Grid `auto-fill, minmax(200px, 1fr)` — no JS needed

---

## Exercise 2: Design a Google Docs-Like Collaborative Editor

**The Core Challenge:** Multiple users editing the same document simultaneously, seeing each other's changes in real time.

### Architecture
```
┌──────────────────────────────────────────────────────────────┐
│                  Collaborative Editor                         │
│                                                              │
│  Client A          WebSocket Server         Client B        │
│                                                              │
│  Type "hello"  →   Broadcast operation  →  Receive "hello"  │
│  (position 0)                              (inserted at 0)   │
│                                                              │
│  Operational Transformation (OT) or CRDT resolves conflicts  │
└──────────────────────────────────────────────────────────────┘
```

### Awareness Features (Who's editing what)
```javascript
// Show cursor positions of other users
const userCursors = {
  'user-alice': { position: 42, color: '#FF6B6B', name: 'Alice' },
  'user-bob': { position: 108, color: '#4ECDC4', name: 'Bob' },
};

// Render colored cursors inline in document
function CollaborativeCursor({ cursor }) {
  return (
    <span
      className="collab-cursor"
      style={{ borderColor: cursor.color }}
      data-user={cursor.name}
    />
  );
}
```

---

## Exercise 3: Design a Real-Time Dashboard

### Requirements
- Show live metrics (sales, users, revenue)
- Multiple chart types (line, bar, pie)
- Date range filtering
- Auto-refresh or WebSocket updates

### Performance Strategy
- WebSocket for live data (not polling every second)
- Canvas-based charts (not SVG) for performance with high data volumes
- Memoize chart data transformations (useMemo)
- Virtualize table rows if showing 1000+ data points

---

## Exercise 4: Design a File Upload Component

### Requirements
- Drag-and-drop + click-to-browse
- Multiple file upload
- Progress per file
- Retry failed uploads
- Preview uploaded images
- File size and type validation

### Architecture
```javascript
interface UploadState {
  files: {
    id: string;
    file: File;
    status: 'pending' | 'uploading' | 'success' | 'error';
    progress: number;    // 0-100
    error?: string;
    url?: string;        // After successful upload
  }[];
}

// Chunked upload for large files
async function uploadChunked(file, options) {
  const chunkSize = 5 * 1024 * 1024; // 5MB chunks
  const totalChunks = Math.ceil(file.size / chunkSize);
  
  for (let i = 0; i < totalChunks; i++) {
    const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize);
    const formData = new FormData();
    formData.append('chunk', chunk);
    formData.append('chunkIndex', i);
    formData.append('totalChunks', totalChunks);
    formData.append('uploadId', options.uploadId);
    
    await api.post('/upload/chunk', formData, {
      onUploadProgress: (e) => {
        const chunkProgress = (e.loaded / e.total) * (100 / totalChunks);
        const totalProgress = (i / totalChunks) * 100 + chunkProgress;
        options.onProgress(totalProgress);
      },
    });
  }
  
  return api.post('/upload/complete', { uploadId: options.uploadId });
}
```

---

## Exercise 5: Design a Design Token System

### What Are Design Tokens?
Design tokens are named variables that store design decisions (colors, spacing, typography). They form the single source of truth between design and code.

### Token Structure
```javascript
// tokens/base.js — Platform-agnostic raw values
const base = {
  colors: {
    blue: { 50: '#EFF6FF', 100: '#DBEAFE', /* ... */ 900: '#1E3A5F' },
    red:  { 50: '#FFF5F5', /* ... */ 900: '#7B0000' },
    // ...
  },
  space: { 0: '0', 1: '4px', 2: '8px', 3: '12px', 4: '16px', /* ... */ },
  fontSize: { sm: '12px', md: '14px', lg: '16px', xl: '20px', '2xl': '24px' },
  fontWeight: { normal: 400, medium: 500, semibold: 600, bold: 700 },
  borderRadius: { sm: '4px', md: '8px', lg: '12px', full: '9999px' },
  shadow: {
    sm: '0 1px 2px rgba(0,0,0,0.05)',
    md: '0 4px 6px rgba(0,0,0,0.07)',
    lg: '0 10px 15px rgba(0,0,0,0.1)',
  },
};

// tokens/semantic.js — Semantic aliases
const semantic = {
  color: {
    background: { primary: base.colors.white, secondary: base.colors.gray[50] },
    text: { primary: base.colors.gray[900], secondary: base.colors.gray[600] },
    brand: { primary: base.colors.blue[600], hover: base.colors.blue[700] },
    danger: { default: base.colors.red[600], light: base.colors.red[50] },
  },
};
```

---

# 18. Interview Answer Framework

## The STAR-RADIO Hybrid Framework for Frontend Design Interviews

```
Opening (30 seconds):
"Let me start by clarifying requirements, then I'll walk through the 
architecture, data model, component interfaces, and optimizations."

Requirements (3-5 minutes):
  Functional: "The core user flows are..."
  Non-functional: "For performance, I'm targeting LCP < 2.5s. 
                   This needs to be accessible (WCAG AA)."

Architecture (10-15 minutes):
  "Here's the high-level component hierarchy..."
  [Draw ASCII diagram or describe structure]
  "The key design decisions are..."

Data Model (5-8 minutes):
  "The API returns data in this shape..."
  "On the client, I'll store it like this..."
  "For normalization / caching..."

Interfaces (5-8 minutes):
  "The main component's props interface looks like..."
  "The custom hook signature is..."

Optimizations (5-8 minutes):
  "For performance: code splitting at routes, virtualize the list..."
  "For reliability: error boundaries at feature level, retry logic..."
  "For scale: CDN for static assets, service worker cache..."

Trade-offs (3-5 minutes):
  "The trade-off I made here is... The alternative would be..."
  "Given more time, I'd also consider..."
```

---

## Quick Reference: Common Interview Signals

| Signal | Junior | Mid | Senior | Staff |
|--------|--------|-----|--------|-------|
| Requirements | Jumps to code | Asks a few | Thorough clarification | Identifies unstated requirements |
| Architecture | Component-centric | Adds routing/state | Layers API, error, perf | Addresses org/team structure |
| Performance | Mentions memoization | Code splitting | Budget + monitoring | Capacity planning |
| Accessibility | Mentions it | Adds ARIA | Full keyboard flow | Enforces via ESLint/CI |
| Trade-offs | One option | A few options | Trade-offs with context | Business trade-offs too |
| Edge cases | Happy path | Some edge cases | Thorough | Adversarial thinking |

---

## Revision Notes — System Design

```
┌────────────────────────────────────────────────────────────────┐
│                    Quick Revision                              │
│                                                                │
│  RADIO = Requirements, Architecture, Data Model,               │
│          Interface, Optimizations                              │
│                                                                │
│  State types: Local, Shared, Server, URL, Global, Persistent   │
│                                                                │
│  Patterns: Compound Component, Render Props, HOC, Headless,    │
│            Provider, Container/Presenter                        │
│                                                                │
│  Performance: Code Split, Virtualize, Debounce, Cache,         │
│               Lazy Load, Service Worker                         │
│                                                                │
│  Auth: Access Token in memory, Refresh Token in httpOnly cookie │
│                                                                │
│  API Layer: Axios instance → Interceptors → Service Layer       │
│             → Custom Hook → Component                           │
│                                                                │
│  Error: Global Boundary → Feature Boundary → Inline            │
│                                                                │
│  Cache: HTTP Headers → React Query → Service Worker            │
└────────────────────────────────────────────────────────────────┘
```

---

*End of Part 3 — Advanced Frontend System Design*
*Next: Part 4 — Complete Interview Preparation Guide*
