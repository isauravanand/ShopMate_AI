# ShopMate AI — Codebase Discovery and Technical Analysis Report

**Author:** Senior Forward Deployed Engineer (FDE)  
**Project:** ShopMate AI Modernization & Enterprise AI Integration  
**Date:** November 2026  
**Status:** Discovery Complete — Non-Destructive Codebase Audit  

---

## 1. Project Architecture and Technology Stack

ShopMate AI is a container-ready, multi-tier e-commerce web application designed with a decoupled frontend-backend architecture.

```
┌──────────────────────────────────────────────────────────────┐
│                    Client Tier (Browser)                     │
│  React 18 (TypeScript) + MUI 5 + Tailwind CSS + Context API │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTP / JSON
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                 Reverse Proxy Tier (Nginx)                   │
│   Routing: /api -> Backend (8000), / -> Frontend (3000)     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  Application Tier (FastAPI)                  │
│       Python 3.10 + Uvicorn + Pydantic v2 + SQLAlchemy       │
└──────────────────────────────┬───────────────────────────────┘
                               │ PostgreSQL Dialect / Psycopg2
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Persistence Tier                          │
│               PostgreSQL 16/18 Relational DB                 │
└──────────────────────────────────────────────────────────────┘
```

### Technology Breakdown

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React | `18.2.0` | Component-based single-page user interface |
| **Language (Frontend)** | TypeScript | `4.9.5` | Type-safe frontend client implementation |
| **UI Component Library** | Material UI (`@mui/material`) | `5.15.15` | Prebuilt UI components (cards, drawers, icons) |
| **CSS Framework** | Tailwind CSS | `3.4.3` | Utility-first styling framework |
| **Client Routing** | React Router DOM | `6.22.3` | Browser-based client-side routing |
| **Backend Framework** | FastAPI | `0.162.5` | High-performance ASGI REST API framework |
| **ASGI Server** | Uvicorn | `0.49.0` | Asynchronous production server |
| **ORM** | SQLAlchemy | `2.0.55` | Relational database mapping and queries |
| **Database Driver** | Psycopg2-binary | `2.9.13` | PostgreSQL database connection adapter |
| **Database Migrations** | Alembic | `1.20.1` | Database schema versioning and migrations |
| **Data Validation** | Pydantic | `2.13.5` | Request and response schema validation |
| **Database** | PostgreSQL | `16-alpine` (Docker) / `18.x` (Local) | ACID-compliant relational data store |
| **Reverse Proxy** | Nginx (Alpine) | `latest` | Reverse proxy and static file server |
| **Containerization** | Docker & Docker Compose | `3.9` spec | Multi-service orchestration and packaging |

---

## 2. Complete Folder and File Structure

```
ShopMate-AI/
├── .github/
│   └── workflows/
│       └── build-and-push.yml      # CI/CD: Automated Docker build & Docker Hub push
├── backend/
│   ├── alembic/
│   │   ├── versions/               # Generated migration scripts
│   │   ├── env.py                  # Alembic runtime configuration
│   │   ├── README                  # Alembic boilerplate readme
│   │   └── script.py.mako          # Alembic migration template
│   ├── app/
│   │   ├── db/
│   │   │   └── __init__.py         # DB engine, session maker, URL encoding, table initialization
│   │   ├── models/
│   │   │   └── sqlalchemy/
│   │   │       ├── __init__.py     # Model exports and models_arr registry
│   │   │       ├── cart.py         # Cart and Cart_Item ORM models
│   │   │       ├── category.py     # Category ORM model
│   │   │       ├── join_tables.py  # product_categories many-to-many join table
│   │   │       ├── order.py        # Order and OrderItem ORM models
│   │   │       ├── product.py      # Product and ProductSize ORM models
│   │   │       ├── review.py       # Review ORM model
│   │   │       └── user.py         # User ORM model
│   │   ├── routers/
│   │   │   ├── auth_router.py      # Auth routes: /register, /token, /protected (unmounted)
│   │   │   ├── cart_router.py      # Cart routes: /cart/{user_id} (stubbed)
│   │   │   ├── product_router.py   # Product routes: /products, /products/{slug} (active)
│   │   │   └── support_router.py   # Ticket support routes (stubbed)
│   │   ├── schemas/
│   │   │   ├── cart_schemas.py     # CartBase, CartItemBase schemas
│   │   │   ├── product_schemas.py  # ProductBase, ProductResponse, ProductSize schemas
│   │   │   └── user_schemas.py     # UserBase, UserCreate, UserResponse, LoginRequest
│   │   ├── services/
│   │   │   ├── product_service.py  # Product CRUD operations and querying
│   │   │   ├── review_service.py   # Empty placeholder file
│   │   │   └── user_service.py     # User registration, JWT creation, authentication
│   │   ├── app.py                  # FastAPI application entrypoint, CORS, router mounting
│   │   ├── config.py               # Environment configuration & DATABASE dictionary
│   │   └── __init__.py
│   ├── tests/
│   │   ├── __init__.py             # Empty test suite marker
│   │   └── test_product_service.py # 0-byte empty test file
│   ├── .env                        # Local database credentials
│   ├── .env.docker                 # Docker container environment variables
│   ├── alembic.ini                 # Alembic database URL configuration
│   ├── Dockerfile                  # Backend container build specification
│   ├── main.py                     # Local development Uvicorn entrypoint
│   ├── requirements.txt            # Python pip dependencies
│   └── seed.py                     # Database initialization and sample catalog seeder
├── frontend/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html              # HTML shell
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── components/
│   │   │   ├── shared/
│   │   │   │   ├── cart/
│   │   │   │   │   ├── Cart.tsx         # Slide-out shopping cart drawer component
│   │   │   │   │   └── CartItem.tsx     # Cart item component stub
│   │   │   │   ├── modal/
│   │   │   │   │   └── SideDrawer/
│   │   │   │   │       └── SideDrawer.tsx # Reusable MUI Drawer wrapper
│   │   │   │   └── navigation/
│   │   │   │       ├── MainNav.tsx      # Category navigation bar
│   │   │   │       ├── SubNav.tsx       # Auth links, free shipping banner, cart icon
│   │   │   │       ├── navigation.css   # Navigation bar styling
│   │   │   │       └── Navigation.tsx   # Parent navigation container
│   │   │   └── ui/
│   │   │       ├── buttons/
│   │   │       │   ├── AddToCart/
│   │   │       │   │   ├── AddToCart.css
│   │   │       │   │   └── AddToCart.tsx # Client-side cart item insertion button
│   │   │       │   ├── CartButton/
│   │   │       │   │   └── CartButton.tsx
│   │   │       │   └── RadioProduct/
│   │   │       │       └── RadioProduct.tsx # Color/size radio selector button group
│   │   │       └── cards/
│   │   │           └── ProductCard/
│   │   │               └── ProductCard.tsx # Catalog grid product card
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── AuthPage.tsx    # Auth container wrapper
│   │   │   │   ├── Login.tsx       # Login form component
│   │   │   │   └── Register.tsx    # User registration form component
│   │   │   └── product/
│   │   │       ├── ProductPage.tsx # Individual product detail page
│   │   │       └── Products.tsx    # Product catalog listing page
│   │   ├── services/
│   │   │   └── Product.ts          # REST client for /products endpoints
│   │   ├── types/
│   │   │   ├── CartTypes.ts        # TypeScript interfaces for Cart and CartContext
│   │   │   └── types.ts            # TypeScript product and catalog classes
│   │   ├── App.css
│   │   ├── App.test.tsx            # Default Create-React-App test
│   │   ├── App.tsx                 # Root component, routing, CartContext provider
│   │   ├── constants.ts            # BACKEND_URL and AWS_S3_BASE_URL env references
│   │   ├── index.css               # Global Tailwind CSS directives
│   │   ├── index.tsx               # React DOM root render
│   │   ├── reportWebVitals.ts
│   │   └── setupTests.ts
│   ├── .env                        # Local frontend environment variables
│   ├── .env.docker                 # Docker frontend environment variables
│   ├── Dockerfile                  # Frontend multi-stage container build
│   ├── nginx.conf                  # Nginx configuration for static frontend serving
│   ├── package.json                # NPM dependencies and scripts
│   ├── tailwind.config.js          # Tailwind styling configuration
│   └── tsconfig.json               # TypeScript compiler options
├── nginx/
│   ├── default.conf                # Global reverse proxy configuration
│   └── Dockerfile                  # Nginx container specification
├── .env                            # Root Docker Compose environment variables
├── .env.docker                     # Docker Compose container defaults
├── docker-compose.yml              # Multi-container orchestration definition
└── README.md                       # High-level project summary
```

---

## 3. Backend Architecture and API Endpoints

### 3.1 Application Bootstrap (`backend/app/app.py`)
* The application initializes a `FastAPI` instance with title `"E-Commerce API"` and `root_path="/api"`.
* Configures permissive CORS:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
* Database tables are initialized eagerly on startup via `create_tables()`.

### 3.2 Routers Inventory & Status

| Router | File Path | Mount Status in `app.py` | Implementation State |
| :--- | :--- | :--- | :--- |
| `product_router` | `backend/app/routers/product_router.py` | **Mounted** (`app.include_router(product_router)`) | **Active & Functional** |
| `cart_router` | `backend/app/routers/cart_router.py` | **Mounted** (`app.include_router(cart_router)`) | **Stubbed (`pass`)** |
| `support_router` | `backend/app/routers/support_router.py` | **Mounted** (`app.include_router(support_router)`) | **Stubbed (`pass`)** |
| `auth_router` | `backend/app/routers/auth_router.py` | **NOT Mounted** (Omitted from `app.py`) | **Broken (MongoDB calls)** |

### 3.3 Endpoint Catalog

#### Product Endpoints (`backend/app/routers/product_router.py`)
* `GET /products?page=0&limit=10`
  * **Handler:** `read_products(page: int = 0, limit: int = 0)`
  * **Service:** `Product_Service.get_products(page, limit)`
  * **Returns:** List of product records.
* `GET /products/{product_slug}`
  * **Handler:** `read_product(product_slug: str)`
  * **Service:** `Product_Service.get_product(product_slug)`
  * **Response Model:** `ProductBase`
  * **Returns:** Single matching product.
* `POST /product/{product_slug}/cart`
  * **Handler:** `add_product_to_cart(product_slug: str)`
  * **Status:** Incomplete; references undefined variable `product_id`.
* `POST /product/{product_slug}/review`
  * **Handler:** `post_review_product(product_slug: str)`
  * **Status:** Incomplete; references undefined variable `product_id`.

#### Cart Endpoints (`backend/app/routers/cart_router.py` — All Stubbed)
* `GET /cart/{user_id}` — Intended to return `CartBase`.
* `POST /cart/{user_id}` — Intended to add item by `user_id`, `product_id`, `product_size`, `product_color`.
* `DELETE /cart/{user_id}/{cart_item_id}` — Intended to remove item from user cart.
* `PUT /cart/{user_id}/{cart_item_id}` — Intended to modify quantity.
* `GET /cart/{user_id}/price` — Intended to calculate and return total cart price.

#### Support Endpoints (`backend/app/routers/support_router.py` — All Stubbed)
* `GET /ticket` — Read all tickets.
* `GET /ticket/${ticket_id}` — Read ticket by ID.
* `POST /ticket` — Submit ticket.
* `PUT /ticket` — Update ticket status.

#### Authentication Endpoints (`backend/app/routers/auth_router.py` — Unmounted)
* `POST /register` — User signup with `UserCreate`.
* `POST /token` — OAuth2 Password Request Form login returning JWT bearer token.
* `GET /protected` — Guarded route referencing `UserServices.get_current_user`.

---

## 4. Database Schema, Models and Relationships

The application uses SQLAlchemy declarative models located in `backend/app/models/sqlalchemy/`.

```
                    ┌──────────────┐
                    │     User     │
                    │ (UUID, PK)   │
                    └───┬──────┬───┘
                        │1     │1
                        │      │
                       1│      │*
                 ┌──────▼┐   ┌─▼────────┐
                 │  Cart │   │  Order   │
                 └──┬────┘   └──┬───────┘
                    │1          │1
                    │           │
                    │*          │*
             ┌──────▼────┐   ┌──▼────────┐
             │ Cart_Item │   │ OrderItem │
             └──────┬────┘   └──┬────────┘
                    │*          │*
                    │           │
                    │     1     │
                    └─────►┌────▼────┐1        *┌──────────┐
                           │ Product ├──────────┤ Category │
                           └───┬─────┘ (M-to-M) └──────────┘
                               │1
                               │*
                        ┌──────▼──────┐
                        │ ProductSize │
                        └─────────────┘
```

### 4.1 Schema Definitions

#### `users` (`backend/app/models/sqlalchemy/user.py`)
* `uuid`: `UUID(as_uuid=True)`, Primary Key, default `uuid.uuid4`.
* `first_name`: `String`, nullable.
* `last_name`: `String`, nullable.
* `email`: `String`, unique, indexed, non-nullable.
* `hashed_password`: `String`, non-nullable.
* `salt`: `String`, non-nullable.
* `is_active`: `Boolean`, default `True`.
* `email_verified`: `Boolean`, default `False`.
* `verification_token`: `String`, nullable.
* `created_at` / `updated_at`: `DateTime(timezone=True)`.
* **Relationships:** `cart` (1:1 with `Cart`), `orders` (1:N with `Order`), `reviews` (1:N with `Review`).

#### `products` (`backend/app/models/sqlalchemy/product.py`)
* `id`: `Integer`, Primary Key, autoincrement.
* `slug`: `String`, unique lookup handle.
* `product_type`: `String`, indexed (e.g., "Shoes", "Tops", "Bottoms").
* `product_name`: `String`, non-nullable.
* `price`: `Float`, non-nullable.
* `sale_price`: `Float`, nullable.
* `blurb`: `Text`, nullable.
* `description`: `Text`, nullable.
* `image_url`: `String`, nullable.
* **Relationships:** `reviews` (1:N with `Review`), `categories` (M:N via `product_categories`), `sizes` (1:N with `ProductSize`).

#### `product_sizes` (`backend/app/models/sqlalchemy/product.py`)
* `id` (`size_id`): `Integer`, Primary Key.
* `product_id`: `Integer`, ForeignKey(`products.id`), non-nullable.
* `size`: `String` (e.g., "S", "M", "L", "8", "9", "10").
* `stock_quantity`: `Integer`, default `0`, non-nullable.
* **Relationships:** `product` (N:1 with `Product`), `cart_items` (1:N with `Cart_Item`).

#### `categories` (`backend/app/models/sqlalchemy/category.py`)
* `id`: `Integer`, Primary Key.
* `name`: `String`, non-nullable.
* `description`: `Text`, nullable.
* **Relationships:** `products` (M:N via `product_categories`).

#### `product_categories` (`backend/app/models/sqlalchemy/join_tables.py`)
* `product_id`: `Integer`, ForeignKey(`products.id`), Composite PK.
* `category_id`: `Integer`, ForeignKey(`categories.id`), Composite PK.

#### `carts` & `cart_items` (`backend/app/models/sqlalchemy/cart.py`)
* **`carts`**:
  * `id`: `Integer`, Primary Key.
  * `user_id`: `UUID`, ForeignKey(`users.uuid`), non-nullable.
  * `created_at`: `DateTime`, default `datetime.utcnow`.
* **`cart_items`**:
  * `id`: `Integer`, Primary Key.
  * `cart_id`: `Integer`, ForeignKey(`carts.id`), non-nullable.
  * `product_id`: `Integer`, ForeignKey(`products.id`), non-nullable.
  * `product_size_id`: `Integer`, ForeignKey(`product_sizes.id`), non-nullable.
  * `quantity`: `Integer`, default 1.
  * `price`: `Float`, default 0.0.

#### `orders` & `order_items` (`backend/app/models/sqlalchemy/order.py`)
* **`orders`**:
  * `id`: `Integer`, Primary Key, indexed.
  * `user_id`: `UUID`, ForeignKey(`users.uuid`), non-nullable.
  * `created_at`: `DateTime`, default `datetime.utcnow`.
* **`order_items`**:
  * `id`: `Integer`, Primary Key, indexed.
  * `order_id`: `Integer`, ForeignKey(`orders.id`).
  * `product_id`: `Integer`, ForeignKey(`products.id`).
  * `quantity`: `Integer`, non-nullable.

#### `reviews` (`backend/app/models/sqlalchemy/review.py`)
* `id`: `Integer`, Primary Key.
* `product_id`: `Integer`, ForeignKey(`products.id`).
* `user_id`: `UUID`, ForeignKey(`users.uuid`), non-nullable.
* `content`: `Text`, non-nullable.
* `rating`: `Integer`, non-nullable.

---

## 5. Authentication and Authorization Flow

### 5.1 Architecture & Current Status
* **Configuration:** Intended to use JWT (JSON Web Tokens) with symmetric signing (`HS256`), 30-minute expiration, and `passlib` bcrypt hashing.
* **Current State:** **Non-functional / Disabled**.
  1. `auth_router.py` is not mounted in `backend/app/app.py`.
  2. `backend/app/services/user_service.py` is coded against an asynchronous document database interface (e.g. `await User.find_one(...)`, `await user_obj.insert()`), which throws runtime exceptions against SQLAlchemy ORM models.
  3. The `SECRET_KEY` is hardcoded as `"your_secret_key"`.
* **Frontend State:**
  * [Register.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/pages/auth/Register.tsx) sends a `POST` request to `${BACKEND_URL}/register`.
  * [Login.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/pages/auth/Login.tsx) attempts a `POST` request to `/token` with form urlencoded body, storing `data.access_token` in `localStorage.setItem("accessToken", ...)`.
  * Because the backend endpoints are unmounted and misconfigured, user authentication cannot succeed in the current deployment.

---

## 6. Product Management and Search Implementation

### 6.1 Product Retrieval
* Implemented in [backend/app/services/product_service.py](file:///c:/Users/saura/ShopMate-AI/backend/app/services/product_service.py):
  ```python
  def get_products(page: int = 0, limit: int = 10) -> List[Dict]:
      try:
          products = db.query(Product).offset(page * limit).limit(10).all()
          return products
      except Exception as e:
          db.rollback()
          raise HTTPException(status_code=500, detail="Error fetching products")
  ```
* Supports offset-based pagination. Notice that `limit(10)` is hardcoded instead of using the `limit` parameter.
* Single product lookup queries `Product.slug == product_slug`.

### 6.2 Search Capabilities
* **Full-text search:** Does not exist.
* **Keyword search:** No SQL `ILIKE` or trigram search endpoints exist.
* **Category filtering:** Categories are modeled in the database, but `product_router.py` does not provide a category filter query parameter (e.g., `GET /products?category=Shoes`).
* **Price / Attribute filtering:** Frontend renders static filter buttons (`Fit`, `Color`, `Price`) in [Products.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/pages/product/Products.tsx), but no filtering logic or API parameters are hooked up.

---

## 7. Shopping Cart Business Logic

### 7.1 Separation of State: Client vs Server
* **Backend:** [backend/app/routers/cart_router.py](file:///c:/Users/saura/ShopMate-AI/backend/app/routers/cart_router.py) is purely a skeleton. No database cart records are created, queried, or updated.
* **Frontend:** The shopping cart is managed **entirely in client-side memory** via React Context API:
  * Managed in [frontend/src/App.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/App.tsx) via `CartContext` (`useState<ICartItem[]>([])`).
  * Items are added via [AddToCart.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/components/ui/buttons/AddToCart/AddToCart.tsx), which matches on `product_id`, `size`, and `color` to either increment quantity or append a new item.
  * Subtotal, tax (fixed at 7%), and total are calculated in real time inside [Cart.tsx](file:///c:/Users/saura/ShopMate-AI/frontend/src/components/shared/cart/Cart.tsx).
  * **Consequence:** Cart state is volatile and clears upon full page refresh.

---

## 8. Inventory Management

* **Model:** [ProductSize](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/product.py) holds `stock_quantity` per size.
* **Deduction Logic:** No inventory deduction, reservation, or concurrency locking logic exists. Adding items to the cart or creating an order does not modify `stock_quantity`.
* **Out of Stock Guard:** The frontend `AddToCart.tsx` component checks `if (product)` rather than `stock_quantity > 0`.

---

## 9. Order Creation and Order Tracking

* **Schema:** `orders` and `order_items` tables exist in PostgreSQL via SQLAlchemy definitions in [order.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/order.py).
* **Endpoints:** Zero endpoints exist for order creation (`POST /orders`), checkout, order listing (`GET /orders`), or order tracking (`GET /orders/{order_id}`).
* **Frontend:** No checkout or order confirmation pages exist in `frontend/src/pages/`.

---

## 10. Existing Service and Repository Layers

### 10.1 Service Inventory

| Service Class | File | Methods | Status |
| :--- | :--- | :--- | :--- |
| `Product_Service` | `backend/app/services/product_service.py` | `create_product`, `get_products`, `get_product`, `update_product`, `delete_product` | Partially functional; `.get(slug)` bug in update/delete |
| `UserServices` | `backend/app/services/user_service.py` | `register`, `authenticate`, `create_access_token`, `get_current_user` | Broken (MongoDB syntax) |
| `ReviewService` | `backend/app/services/review_service.py` | None | Empty file |

### 10.2 Architectural Observations
* **No Repository Pattern:** Database queries are executed directly inside service methods using a globally imported session `db = get_db_session()`.
* **No Dependency Injection:** Session lifecycle is not managed per-request via FastAPI's `Depends(get_db)`. If the database connection drops or experiences a transaction error, the global session can enter an invalid state across requests.

---

## 11. Error Handling and Testing Strategy

### 11.1 Error Handling
* Backend routes catch broad exceptions and raise `HTTPException(status_code=500, detail="...")`.
* Startup error handling in `backend/app/db/__init__.py` catches connection failures during table creation.
* Frontend services wrap API calls in `try...catch` blocks, logging to console and returning `null`.

### 11.2 Testing Strategy
* `backend/tests/test_product_service.py`: 0 bytes (no automated backend tests).
* `frontend/src/App.test.tsx`: Standard Create-React-App template test looking for "learn react" (failing).
* No unit, integration, or end-to-end testing pipeline is actively asserting application behavior.

---

## 12. How the Application Starts and Runs Locally

### Backend Execution
1. Environment variables loaded from `backend/.env` via `python-dotenv`.
2. Connection string constructed with URL-encoded password in `backend/app/db/__init__.py`.
3. Executed via:
   ```powershell
   cd backend
   python main.py
   # Or: uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Accessible at `http://localhost:8000`, with OpenAPI docs at `http://localhost:8000/docs`.

### Frontend Execution
1. Dependencies installed in `frontend/node_modules`.
2. Configured via `frontend/.env` (`REACT_APP_BACKEND_URL=http://localhost:8000`).
3. Executed via:
   ```powershell
   cd frontend
   npm start
   ```
4. Accessible at `http://localhost:3000`.

### Containerized Execution (Docker Compose)
* Orchestrates `frontend`, `backend`, `postgres:16-alpine`, `pgadmin4`, `nginx`, and `watchtower`.
* Reverse proxy terminates host traffic at port `80`, routing `/api` to the backend and `/` to the frontend.
