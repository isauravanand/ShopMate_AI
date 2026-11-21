# ShopMate AI — Phase 1: Backend Foundation Verification & Audit

**Document:** Comprehensive Backend Audit & Repair Roadmap  
**Role:** Senior Python Backend Engineer  
**Scope:** Phase 1 — Backend Foundation Modernization  
**Date:** November 2026  
**Status:** Complete — Non-Destructive Codebase Inspection  

---

## Executive Summary

This audit performs an empirical, line-by-line verification of the ShopMate AI backend against the architectural claims and integration prerequisites documented in `docs/codebase-analysis.md`, `docs/architecture.md`, and `docs/integration-plan.md`. 

Every finding below has been verified directly against the active Python backend code in `backend/app/`, `backend/alembic/`, `backend/tests/`, and container configuration files. No application code, database records, or environment configurations were modified during this inspection.

---

## 1. Verified Backend Issues

### 1.1 Database Session Management
* **Source File:** [backend/app/services/product_service.py](file:///c:/Users/saura/ShopMate-AI/backend/app/services/product_service.py#L11)
* **Component / Line:** Line 11: `db = get_db_session()`
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**  
  `get_db_session()` in [backend/app/db/\_\_init\_\_.py](file:///c:/Users/saura/ShopMate-AI/backend/app/db/__init__.py#L22-L25) constructs a new SQLAlchemy `Session` bound to `engine`. However, in `product_service.py`, `db` is instantiated once at the module level.
  1. **Thread & Async Concurrency Collisions:** In an ASGI application (Uvicorn), multiple concurrent requests access the identical `Session` instance. If one request issues a query that raises an exception, the session enters an aborted transaction state, breaking subsequent queries for all other concurrent requests until `rollback()` is triggered.
  2. **Connection Leakage:** The module-level session is never closed (`db.close()` is never called in request lifecycles), keeping connection handles open indefinitely.
* **Recommended Fix:**  
  Remove the global `db` assignment in `product_service.py`. Implement standard FastAPI dependency injection in [backend/app/db/\_\_init\_\_.py](file:///c:/Users/saura/ShopMate-AI/backend/app/db/__init__.py):
  ```python
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db_engine())

  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```
  Inject `db: Session = Depends(get_db)` into router handlers and pass `db` directly to service functions.

---

### 1.2 Authentication Implementation and Router Registration
* **Source Files:** 
  * [backend/app/app.py](file:///c:/Users/saura/ShopMate-AI/backend/app/app.py#L44-L46)
  * [backend/app/routers/auth_router.py](file:///c:/Users/saura/ShopMate-AI/backend/app/routers/auth_router.py#L13-L35)
  * [backend/app/services/user_service.py](file:///c:/Users/saura/ShopMate-AI/backend/app/services/user_service.py#L18-L58)
* **Component / Class:** `app.include_router(...)`, `router` in `auth_router.py`, `UserServices` class.
* **Verification Status:** **CONFIRMED (Critical Blocker)**
* **Technical Impact:**
  1. **Unmounted Router:** In `app.py`, only `product_router`, `cart_router`, and `support_router` are registered. `auth_router` is completely omitted, resulting in HTTP 404 on `/api/register`, `/api/token`, and `/api/protected`.
  2. **MongoDB ODM Calls on SQLAlchemy Model:** `UserServices` calls Motor/MongoDB asynchronous methods:
     * Line 21: `await User.find_one({"email": user_data.email})`
     * Line 27: `await user_obj.insert()`
     * Line 32: `await User.find_one({"email": login_request.email})`
     * Line 55: `await User.find_one({"_id": user_id})`  
     Because `User` is an SQLAlchemy declarative class ([backend/app/models/sqlalchemy/user.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/user.py)), invoking these methods triggers `AttributeError: type object 'User' has no attribute 'find_one'`, crashing every authentication call.
  3. **Method Signature Mismatch in Login:** `auth_router.py` (line 24) calls `UserServices.authenticate(form_data.username, form_data.password)` with two string arguments. However, `UserServices.authenticate` (line 31) expects a single argument `login_request: LoginRequest`. This triggers an immediate `TypeError`.
  4. **Primary Key Mismatch:** `auth_router.py` (line 28) generates a token with `str(user.id)`. The `User` model defines the primary key as `uuid = Column(UUID(as_uuid=True), primary_key=True)`, not `id`. This raises `AttributeError: 'User' object has no attribute 'id'`.
  5. **Hardcoded Secret Key:** `user_service.py` (line 13) specifies `SECRET_KEY = "your_secret_key"`.
* **Recommended Fix:**  
  * Rewrite `UserServices` to use SQLAlchemy queries: `db.query(User).filter(User.email == email).first()`.
  * Pass `user.uuid` into JWT payload.
  * Load `SECRET_KEY` from `os.getenv("JWT_SECRET_KEY")`.
  * Register `app.include_router(auth_router)` in `app.py`.

---

### 1.3 Product Service CRUD Operations & Schema Inconsistencies
* **Source Files:**
  * [backend/app/services/product_service.py](file:///c:/Users/saura/ShopMate-AI/backend/app/services/product_service.py#L30-L76)
  * [backend/app/schemas/product_schemas.py](file:///c:/Users/saura/ShopMate-AI/backend/app/schemas/product_schemas.py#L36-L42)
  * [backend/app/models/sqlalchemy/product.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/product.py#L8-L24)
* **Component / Class:** `Product_Service` (`update_product`, `delete_product`, `create_product`, `map_product_to_response`).
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**
  1. **Primary Key Mismatch in `.get()`:** In `product_service.py` lines 59 and 71:
     ```python
     db_product = db.query(Product).get(product_slug)
     ```
     `Product.id` is an `Integer` primary key. Passing `product_slug` (`str`) into `.get()` coerces or fails type checks and returns `None` or raises `DataError` in PostgreSQL. Product update and delete operations cannot function.
  2. **Schema Inconsistency (`created_at`):** `ProductResponse` in `product_schemas.py` line 38 defines:
     ```python
     created_at: datetime = Field(..., example=datetime.now())
     ```
     However, the `Product` SQLAlchemy model in `product.py` **does not have a `created_at` column**. Calling `map_product_to_response(db_product)` inside `create_product` fails Pydantic validation with `ValidationError: Field required: created_at`.
  3. **Deprecated Pydantic v1 Syntax:** `product.dict()` and `product.dict(exclude_unset=True)` in `create_product` and `update_product` use deprecated methods under Pydantic v2.
* **Recommended Fix:**  
  * Change lookup queries in `update_product` and `delete_product` to:
    ```python
    db_product = db.query(Product).filter(Product.slug == product_slug).first()
    ```
  * Add `created_at = Column(DateTime(timezone=True), server_default=func.now())` to `Product`, or make `created_at: Optional[datetime] = None` in `ProductResponse`.
  * Replace `.dict()` with `.model_dump()`.

---

### 1.4 Product Search and Filtering Capabilities
* **Source Files:**
  * [backend/app/routers/product_router.py](file:///c:/Users/saura/ShopMate-AI/backend/app/routers/product_router.py#L8-L11)
  * [backend/app/services/product_service.py](file:///c:/Users/saura/ShopMate-AI/backend/app/services/product_service.py#L39-L46)
* **Component / Class:** `read_products()`, `Product_Service.get_products()`.
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**
  1. **Hardcoded Limit:** `get_products` defines signature `(page: int = 0, limit: int = 10)`, but line 41 hardcodes `.limit(10).all()`. The `limit` parameter passed by the client is completely discarded.
  2. **Zero Default Limit in Router:** In `product_router.py` line 9:
     ```python
     def read_products(page: int = 0, limit: int = 0):
     ```
     Passing `limit: int = 0` by default causes `page * limit` to evaluate to `0`, making pagination calculations non-functional.
  3. **Zero Filtering / Search Logic:** No query parameters exist for keywords, categories, price range, or sizing. An AI agent cannot query the catalog effectively without pulling all products into LLM memory.
* **Recommended Fix:**  
  * Update `get_products` to respect `limit` (e.g. `query.offset(page * limit).limit(limit)`).
  * Add query filters to `read_products`: `q: Optional[str]`, `category: Optional[str]`, `min_price: Optional[float]`, `max_price: Optional[float]`, `size: Optional[str]`. Apply parameterized SQLAlchemy `.filter(...)` conditions.

---

### 1.5 Cart Router & Cart Service Implementation
* **Source Files:**
  * [backend/app/routers/cart_router.py](file:///c:/Users/saura/ShopMate-AI/backend/app/routers/cart_router.py#L6-L35)
  * [backend/app/routers/product_router.py](file:///c:/Users/saura/ShopMate-AI/backend/app/routers/product_router.py#L17-L21)
  * `backend/app/services/`
* **Component / Class:** `cart_router`, `add_product_to_cart()`.
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**
  1. **Missing Service:** There is no `cart_service.py` in `backend/app/services/`.
  2. **Empty Stub Endpoints:** Every endpoint in `cart_router.py` (`GET /cart/{user_id}`, `POST /cart/{user_id}`, `DELETE /cart/{user_id}/{cart_item_id}`, `PUT /cart/{user_id}/{cart_item_id}`, `GET /cart/{user_id}/price`) terminates with a bare `pass` statement, returning `null` with HTTP 200 without touching PostgreSQL.
  3. **Type Mismatch on `user_id`:** `cart_router.py` declares `user_id: int`, but `Cart.user_id` in [cart.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/cart.py#L15) is a `UUID(as_uuid=True)`. Valid UUID strings passed to the endpoint fail FastAPI validation (`value is not a valid integer`).
  4. **Undefined Variable Runtime Crash in `product_router.py`:**
     Line 20 of `product_router.py`:
     ```python
     @product_router.post("/product/{product_slug}/cart")
     def add_product_to_cart(product_slug: str):
         return {"message": "Product added to cart", "product_id": product_id}
     ```
     `product_id` is never declared or passed. Invoking this endpoint crashes with `NameError: name 'product_id' is not defined`.
* **Recommended Fix:**  
  * Create `backend/app/services/cart_service.py` with methods: `get_or_create_cart`, `add_item_to_cart`, `remove_item_from_cart`, `update_item_quantity`, `get_cart_summary`.
  * Change `user_id: int` to `user_id: uuid.UUID` in `cart_router.py`.
  * Fix or deprecate the redundant endpoint in `product_router.py`.

---

### 1.6 Order Service & Order Ownership Validation
* **Source Files:**
  * [backend/app/models/sqlalchemy/order.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/order.py#L11-L30)
  * `backend/app/routers/`
  * `backend/app/services/`
* **Component / Class:** `Order`, `OrderItem`.
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**
  1. **No Service or Router:** No `order_router.py` or `order_service.py` exists anywhere in the repository.
  2. **Incomplete Order Schema:**
     * `OrderItem` lacks a `price_at_purchase` column. If a product's price changes, historical order records cannot compute accurate totals.
     * `Order` lacks `status` (e.g. `PENDING`, `PAID`, `SHIPPED`), `total_amount`, and `shipping_address`.
  3. **Zero Ownership Verification:** Because no order retrieval endpoint exists, user authorization checks (`order.user_id == current_user.uuid`) do not exist.
* **Recommended Fix:**  
  * Enhance `Order` and `OrderItem` models with status, price, and address columns.
  * Create `backend/app/services/order_service.py` and `backend/app/routers/order_router.py` with user ownership validation via authenticated dependency.

---

### 1.7 Existing Database Models and Relationships
* **Source Files:** [backend/app/models/sqlalchemy/](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/)
* **Component / Class:** All ORM classes.
* **Verification Status:** **CONFIRMED with New Insights**
* **Findings:**
  1. `users`, `products`, `product_sizes`, `categories`, `product_categories`, `carts`, `cart_items`, `orders`, `order_items`, and `reviews` are properly registered in `models_arr` ([backend/app/models/sqlalchemy/\_\_init\_\_.py](file:///c:/Users/saura/ShopMate-AI/backend/app/models/sqlalchemy/__init__.py#L11)) and create cleanly via `Base.metadata.create_all()`.
  2. In `review.py` line 14: `user_id = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)`. But `review.py` imports `from .user import *` and `from .review import *` recursively, causing circular warnings.
  3. In `cart.py` line 28: `product_size_id = Column(Integer, ForeignKey('product_sizes.id'), nullable=False)` references `product_sizes.id`. However, in `product.py` line 30: `size_id = Column("id", Integer, primary_key=True)`. The DB column name is `"id"`, so the foreign key succeeds, but the Python attribute is `size_id`.

---

### 1.8 Existing Tests and Docker Configuration
* **Source Files:**
  * [backend/tests/test_product_service.py](file:///c:/Users/saura/ShopMate-AI/backend/tests/test_product_service.py)
  * [backend/Dockerfile](file:///c:/Users/saura/ShopMate-AI/backend/Dockerfile)
  * [docker-compose.yml](file:///c:/Users/saura/ShopMate-AI/docker-compose.yml)
* **Verification Status:** **CONFIRMED**
* **Technical Impact:**
  1. **Zero Test Coverage:** `test_product_service.py` and `backend/tests/__init__.py` are 0-byte empty files.
  2. **Dockerfile Syntax Error:** Line 13 of `backend/Dockerfile` contains `EXPOSE 8000:8000`. In Dockerfile grammar, `EXPOSE` only accepts a port or port/protocol (e.g. `EXPOSE 8000`). Port mapping syntax belongs exclusively in runtime flags or compose files.
  3. **Docker Compose Volume Paths:** `docker-compose.yml` mounts host paths using Linux home directory shorthand (`~/apps/postgres:/var/lib/postgresql/data`, `~/apps/backend:/var/lib/backend/data`), which fail to resolve on Windows hosts.
  4. **Frontend Context Error:** `docker-compose.yml` line 6 sets `context: julianlechner/ecommerce-frontend:latest` inside a `build:` block instead of pointing to a local directory path (`context: ./frontend`).

---

## 2. Incorrect or Outdated Documentation Findings

During this line-by-line audit, the following discrepancies were identified in earlier documentation (`docs/codebase-analysis.md` and `docs/architecture.md`):

| Documented Claim | Actual Codebase Reality | Severity |
| :--- | :--- | :--- |
| **`ProductResponse` Schema Compatibility** | Documented as functioning schema. In reality, `ProductResponse` defines `created_at: datetime` as mandatory, but the `Product` SQLAlchemy model has no `created_at` column, causing `create_product` serialization to fail. | **High** |
| **Pydantic Serialization Methods** | Documented using `.dict()`. The project runs on Pydantic v2.13.5 where `.dict()` is deprecated and generates runtime deprecation warnings or schema discrepancies. | **Low** |
| **`read_products` limit parameter** | Documented as offset-pagination. In reality, `read_products` in `product_router.py` defaults to `limit = 0`, and `Product_Service.get_products` completely ignores client limits with a hardcoded `.limit(10)`. | **Medium** |
| **`cart_router.py` User Identification** | Documented as requiring user ID. Missed that the router types it as `int` (`user_id: int = Path(...)`) whereas `User.uuid` is a 128-bit `UUID`. Passing standard UUIDs results in HTTP 422 Unprocessable Entity. | **Medium** |

---

## 3. Backend Components That Are Already Working

The following backend systems were tested and confirmed operational:

1. **Database Engine & URL Parser:**  
   [backend/app/db/\_\_init\_\_.py](file:///c:/Users/saura/ShopMate-AI/backend/app/db/__init__.py) correctly encodes passwords using `urllib.parse.quote_plus`, successfully authenticating against PostgreSQL 18 with special characters (`@`).
2. **Table Generation (`create_tables`):**  
   All 10 relational tables (`users`, `products`, `product_sizes`, `categories`, `product_categories`, `carts`, `cart_items`, `orders`, `order_items`, `reviews`) generate cleanly without schema migration errors.
3. **Product Catalog Retrieval:**  
   `GET /products` returns HTTP 200 with the active seeded catalog (16 products) correctly formatted.
4. **Single Product Retrieval by Slug:**  
   `GET /products/{product_slug}` correctly returns the requested product model with HTTP 200.
5. **CORS Middleware:**  
   CORS is actively configured on the FastAPI instance.
6. **Database Seeder (`backend/seed.py`):**  
   Populates real categories, products, sizing inventory, and images into PostgreSQL.

---

## 4. Recommended Repair Sequence (Phase 1 Execution)

To establish an enterprise-grade backend foundation for Pydantic AI without introducing regressions, repairs must proceed in this strict order:

```
Step 1: Session Dependency Injection
  └── Create get_db() generator in db/__init__.py
  └── Replace static module-level db in product_service.py

Step 2: Product Service & Schema Alignment
  └── Fix .get(product_slug) bug to .filter(Product.slug == slug).first()
  └── Fix hardcoded limit(10) in get_products()
  └── Align Product model and ProductResponse (created_at field)
  └── Remove broken stub routes in product_router.py

Step 3: Cart Service & Endpoint Implementation
  └── Create backend/app/services/cart_service.py
  └── Implement real DB CRUD on carts and cart_items
  └── Update cart_router.py parameters from int to UUID
  └── Test full cart lifecycle: add, view, update, delete

Step 4: Authentication & User Service Modernization
  └── Replace MongoDB calls with SQLAlchemy in user_service.py
  └── Wire JWT signing to use user.uuid and environment SECRET_KEY
  └── Fix authenticate() signature to accept username and password
  └── Mount auth_router in app.py

Step 5: Product Filtering & Search Capabilities
  └── Add q, category, price range, and size query parameters
  └── Implement parameterized SQLAlchemy filters in Product_Service
  └── Verify query performance and index utilization

Step 6: Dockerfile & Container Sanitization
  └── Fix EXPOSE 8000 in backend/Dockerfile
  └── Update docker-compose.yml context and portable volume paths
```

---

## 5. Tests Required for Each Repair

| Repair Step | Required Automated Tests (`backend/tests/`) |
| :--- | :--- |
| **Session Injection** | `test_session_lifecycle`: Verify session opens per request and closes upon response; verify concurrent requests do not share transaction state. |
| **Product CRUD** | `test_get_product_by_slug`: Verify 200 on valid slug, 404 on missing slug.  <br>`test_update_product_by_slug`: Verify update succeeds using slug.  <br>`test_create_product_schema`: Verify `ProductResponse` serializes without `created_at` validation failure. |
| **Cart Operations** | `test_cart_lifecycle`: Create cart for UUID user, add item with size, verify item in DB, modify quantity, calculate subtotal and tax, delete item. |
| **Auth Modernization** | `test_user_registration`: Verify password hashing with bcrypt, unique email constraint.  <br>`test_user_login_token`: Verify OAuth2 `/token` returns valid JWT containing `sub=str(user.uuid)`.  <br>`test_protected_route`: Verify valid bearer token allows access; invalid or expired token returns 401. |
| **Product Search** | `test_filter_by_category`: Verify filtering by "Shoes", "Tops", etc.  <br>`test_filter_by_price_range`: Verify `min_price` and `max_price` bounds.  <br>`test_search_keyword`: Verify partial keyword match against `product_name` and `blurb`. |

---

## 6. Single Highest-Priority Implementation Task

### **Task 1: Transition Database Session Management to FastAPI Dependency Injection (`get_db`)**

* **Why it is Highest Priority:**  
  Every subsequent repair—Cart CRUD, User Authentication, and Pydantic AI Tool Execution—relies directly on database transactions. If services continue sharing the single module-level `db = get_db_session()` instance, any failed query or concurrent tool call will lock or invalidate the database session across all API endpoints. 

Implementing `get_db` with `Depends(get_db)` is the prerequisite architectural foundation before writing any new services or AI agent tools.
