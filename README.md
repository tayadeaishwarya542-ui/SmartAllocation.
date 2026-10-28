# SmartPark: Smart Parking Queue and Slot Allocation System

An engineering capstone project implementing a real-time, high-efficiency parking management system powered by **deterministic Data Structures and Algorithms (DSA)**, **FastAPI (Python)**, **SQLite**, and **React (TypeScript)**.

---

## 🎯 1. Project Objective

The objective of **SmartPark** is to eliminate parking congestion and slot allocation inefficiencies in commercial complexes, campuses, and multi-level parking facilities. The system deterministically manages slot assignments, prevents concurrent allocation conflicts, manages waiting lines with fair queueing, enables pre-booked reservations, and automates exit tariff computations without relying on black-box or non-deterministic AI models.

---

## ⚠️ 2. Problem Statement

Conventional parking management suffers from multiple critical bottlenecks:
1. **Uncoordinated Slot Allocation**: Drivers circle lots searching for parking, causing fuel waste, aisle congestion, and accidents.
2. **Double Allocation Conflicts**: Race conditions occur when two drivers or operators target the same vacant slot simultaneously.
3. **Unfair Queuing**: When a facility reaches maximum capacity, arriving vehicles queue up arbitrarily rather than in arrival order, causing disputes.
4. **Manual Tariff Calculation Inaccuracies**: Human operators frequently miscalculate dwell duration or apply arbitrary fees upon vehicle departure.
5. **Slow Lookup Speeds**: In facilities with hundreds of parked vehicles, linear database lookups during exit create exit gate bottlenecks.

**SmartPark solves these challenges** through an integrated in-memory DSA engine synchronized with an ACID-compliant SQLite transactional database.

---

## 🛠️ 3. Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Vanilla CSS Design System (Custom Dark Slate Theme, CSS Grid/Flexbox), Lucide React Icons.
- **Backend**: Python 3.10+, FastAPI (high-performance asynchronous ASGI web framework), Pydantic v2 (data validation and schemas), Uvicorn (ASGI web server).
- **Authentication & Security**: `bcrypt` (password hashing with automatic salt generation), `python-jose` (cryptographic HMAC-SHA256 JWT tokens), HTTP Bearer token dependency injection.
- **Database**: SQLite 3 with SQLAlchemy 2.0 ORM (persisted to disk at `backend/data/smartpark.db`).
- **Data Structures Engine**: Pure Python standard library (`collections.deque`, `heapq`, native dynamic arrays, and hash tables/dictionaries).
- **Architectural Paradigm**: Clean layered architecture separating Presentation (React Views), API Transport (FastAPI routers), Security & Auth Guards, Business Logic (`ParkingService`), In-Memory DSA Engine (`ParkingLotDSA`, `WaitingQueueDSA`), and Persistence (`SQLAlchemy Models`).

---

## 🧠 4. Data Structures & Algorithms (DSA) Implementation

| Component | Primary Data Structure | Algorithm / Mechanism | Time Complexity | Space Complexity | Engineering & Academic Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Slot Allocation** | Contiguous Dynamic Array (`List[SlotNode]`) | **First-Fit Allocation** | Best: $\mathcal{O}(1)$<br>Worst: $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Represents physical parking slots ordered sequentially by floor and slot identifier. Allocates the first available compatible slot. |
| **Vehicle Lookup** | Hash Map / Hash Table (`Dict[str, SlotNode]`) | **Direct Hash Indexing** | Average: $\mathcal{O}(1)$<br>Worst: $\mathcal{O}(N)$ | $\mathcal{O}(V)$ where $V \le N$ | Provides instant $\mathcal{O}(1)$ lookup of active parking slot, floor, and session by license plate string during checkout. |
| **Waiting Line** | FIFO Queue (`collections.deque`) | **First-In First-Out Queueing** | Enqueue: $\mathcal{O}(1)$<br>Dequeue: $\mathcal{O}(1)$<br>Peek: $\mathcal{O}(1)$ | $\mathcal{O}(K)$ where $K$ = queued vehicles | Implemented as a doubly-linked list ring buffer. Guarantees fair arrival-order dispatching when parking is at 100% capacity. |
| **Emergency Priority** | Priority Queue (`heapq` Min-Heap) | **Binary Min-Heap Scheduling** | Push: $\mathcal{O}(\log K)$<br>Pop: $\mathcal{O}(\log K)$ | $\mathcal{O}(K)$ | Prioritizes emergency vehicles (ambulances, security) and VIP permits ahead of standard FIFO traffic. |
| **Reservation Hold** | Hash Map + Array Status Guard | **Exclusive Status Locking** | Search: $\mathcal{O}(N)$<br>Lock: $\mathcal{O}(1)$ | $\mathcal{O}(R)$ where $R$ = reservations | Transitions target slot status to `reserved`, completely masking it from First-Fit searches to prevent double allocation. |
| **Tariff Computation** | Mathematical Step Function | **Ceiling Duration Multiplier** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Computes billable hours with a grace period threshold ($\le 15$ mins free; thereafter $\lceil \Delta t / 60 \rceil \times \text{Rate}$). |

---

## 📂 5. Project Folder Structure

```
SmartPark/
├── README.md                          # Comprehensive project documentation
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application initialization & lifecycle
│   │   ├── api/
│   │   │   ├── __init__.py            # API router mounting & JWT auth route protection
│   │   │   ├── deps.py                # Database and get_current_user Bearer token dependencies
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── health.py          # /api/health endpoint (Public - DB & DSA engine telemetry)
│   │   │       ├── auth.py            # /api/auth (register, login, me endpoints)
│   │   │       ├── slots.py           # /api/slots (Protected - CRUD & slot status operations)
│   │   │       ├── vehicles.py        # /api/vehicles/entry & /api/vehicles/exit (Protected)
│   │   │       ├── queue.py           # /api/queue (Protected - FIFO waiting queue inspection)
│   │   │       ├── sessions.py        # /api/sessions/active & /api/sessions/history (Protected)
│   │   │       ├── reservations.py    # /api/reservations (Protected - Pre-booking & cancellation)
│   │   │       └── dashboard.py       # /api/dashboard/summary (Protected - Real SQLite metrics)
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Configuration settings, rates, JWT secret, DB path
│   │   │   └── security.py            # bcrypt password hashing & JWT encoding/decoding
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── session.py             # SQLite engine and session factory
│   │   ├── dsa/
│   │   │   ├── __init__.py
│   │   │   ├── parking_lot.py         # Dynamic Array & Hash Map DSA implementation
│   │   │   └── queue_manager.py       # FIFO Queue & Priority Heap DSA implementation
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py              # SQLAlchemy models (User, Slots, Vehicles, Sessions, Queue, Reservations)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py             # Pydantic schemas for request/response validation
│   │   └── services/
│   │       ├── __init__.py
│   │       └── parking_service.py     # Core business logic integrating DSA & Database
│   ├── data/
│   │   └── smartpark.db               # SQLite database file
│   ├── tests/
│   │   ├── test_auth.py               # Automated tests for register, login, security & protection
│   │   ├── test_dsa_and_slots.py      # Automated tests for DSA algorithms & seeding
│   │   └── test_parking_core.py       # End-to-end integration tests for all 6 scenarios
│   └── requirements.txt               # Backend dependencies
│
└── frontend/
    ├── index.html                     # HTML root template
    ├── package.json                   # Frontend scripts & dependencies
    ├── vite.config.ts                 # Vite bundler config with /api proxy
    └── src/
        ├── main.tsx                   # React root entry point
        ├── App.tsx                    # Top-level auth gatekeeper, tab router, toast notifications
        ├── index.css                  # Custom styling (design tokens, auth cards, responsive rules)
        ├── types/
        │   └── index.ts               # Shared TypeScript data models (AuthUser, AuthResponse, etc.)
        ├── api/
        │   └── client.ts              # Fetch API client with Bearer auth token injection
        ├── components/
        │   └── layout/
        │       ├── Sidebar.tsx        # Navigation sidebar, real-time queue badge, operator card & logout
        │       └── Header.tsx         # Header with tab title, clock, refresh control & sign out
        └── views/
            ├── LoginView.tsx          # Operator login with show/hide password toggle & validation
            ├── RegisterView.tsx       # Operator account registration with format verification
            ├── DashboardView.tsx      # System overview, slot capacity & live sessions
            ├── ParkingSlotsView.tsx   # Visual slot grid (Floor 1 & 2) & status filters
            ├── VehicleEntryView.tsx   # Vehicle entry registration & auto-allocation
            ├── VehicleExitView.tsx    # Vehicle exit billing & duration calculation
            ├── ReservationsView.tsx   # Slot pre-booking & cancellation manager
            ├── QueueManagementView.tsx# Live FIFO waiting queue visualization
            └── ParkingHistoryView.tsx # Historical parking session logs & revenue tally
```

---

## 🗄️ 6. Database Overview (SQLite Schema)

The SQLite database (`backend/data/smartpark.db`) consists of 6 normalized relational tables:

1. **`users`** (Authentication & Operators):
   - `id` (INTEGER, Primary Key)
   - `full_name` (VARCHAR) — Operator's display name
   - `email` (VARCHAR, Unique, indexed) — Lowercase login email
   - `hashed_password` (VARCHAR) — Secure salted bcrypt hash (rounds=12)
   - `is_active` (INTEGER, Default 1)
   - `created_at` (DATETIME)

2. **`parking_slots`**:
   - `id` (INTEGER, Primary Key)
   - `slot_number` (VARCHAR, Unique, indexed) — e.g., `S-101`
   - `slot_type` (VARCHAR) — `standard`, `compact`, `ev`, `accessible`
   - `status` (VARCHAR) — `available`, `occupied`, `reserved`
   - `floor` (INTEGER) — Floor level (1 or 2)
   - `created_at` (DATETIME)

3. **`vehicles`**:
   - `id` (INTEGER, Primary Key)
   - `license_plate` (VARCHAR, Unique, indexed) — Normalized uppercase plate
   - `vehicle_type` (VARCHAR) — `car`, `bike`, `ev`, `truck`
   - `owner_name`, `contact_number` (VARCHAR, Optional)
   - `created_at` (DATETIME)

4. **`parking_sessions`**:
   - `id` (INTEGER, Primary Key)
   - `vehicle_id` (INTEGER, Foreign Key $\rightarrow$ `vehicles.id`)
   - `slot_id` (INTEGER, Foreign Key $\rightarrow$ `parking_slots.id`)
   - `entry_time` (DATETIME, Indexed)
   - `exit_time` (DATETIME, Nullable)
   - `duration_minutes` (INTEGER, Nullable)
   - `total_fee` (FLOAT, Default 0.0)
   - `status` (VARCHAR) — `active`, `completed`

5. **`waiting_queue`**:
   - `id` (INTEGER, Primary Key)
   - `vehicle_id` (INTEGER, Foreign Key $\rightarrow$ `vehicles.id`)
   - `priority` (INTEGER, Default 0) — 0 = Standard FIFO, 1 = Priority/Emergency
   - `entry_time` (DATETIME, Indexed)
   - `status` (VARCHAR) — `waiting`, `allocated`, `cancelled`

6. **`reservations`**:
   - `id` (INTEGER, Primary Key)
   - `vehicle_id` (INTEGER, Foreign Key $\rightarrow$ `vehicles.id`)
   - `slot_id` (INTEGER, Foreign Key $\rightarrow$ `parking_slots.id`)
   - `reservation_time` (DATETIME)
   - `expires_at` (DATETIME)
   - `status` (VARCHAR) — `active`, `fulfilled`, `cancelled`

---

## ⚡ 7. Installation and Setup Instructions

### Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, or 3.13 installed (`python --version`).
- **Node.js**: Version 18.x or 20.x+ installed (`node --version`, `npm --version`).

### Step 1: Clone or Navigate to the Workspace
```powershell
cd c:\Users\hp\OneDrive\Desktop\SmartPark
```

### Step 2: Install Backend Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
cd ..\frontend
npm install
```

---

## 🖥️ 8. Exact Commands to Run the Application

Open two separate terminal windows (PowerShell or Command Prompt):

### Terminal 1: Backend Server (FastAPI)
```powershell
cd backend
python -m uvicorn app.main:app --port 8000 --reload
```
- **Backend API URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/api/health`

### Terminal 2: Frontend Client (React + Vite)
```powershell
cd frontend
npm run dev
```
- **Web Application URL**: `http://localhost:5173`

---

## 🧪 9. Automated Testing & Verification

SmartPark includes 3 automated test suites covering all core DSA algorithms, authentication guards, database constraints, and REST API flows:

### Run Authentication & Security Test Suite
```powershell
cd backend
python tests/test_auth.py
```
*Verifies: User registration, duplicate email rejection (400), valid login (200), invalid password rejection (401), unauthenticated route rejection (401), and access with Bearer tokens.*

### Run DSA & Seeding Test Suite
```powershell
cd backend
python tests/test_dsa_and_slots.py
```
*Verifies: `ParkingLotDSA`, `WaitingQueueDSA`, database seeding of 10 slots, and `/api/health`.*

### Run Core Parking Scenarios Test Suite
```powershell
cd backend
python tests/test_parking_core.py
```
*Executes all 6 validation scenarios:*
1. **Scenario 1**: Vehicle entry when slot is available (allocated to first available slot `S-101`).
2. **Scenario 2**: Vehicle entry when all 10 slots are occupied (correctly placed into FIFO waiting queue).
3. **Scenario 3**: Waiting vehicle auto-allocated on vehicle exit (head of FIFO queue dispatched instantly to newly freed slot).
4. **Scenario 4**: Duplicate active vehicle entry rejected (prevents double check-in of same plate).
5. **Scenario 5**: Database consistency & persistence check (verifies SQLite state is identical after server restart).
6. **Scenario 6**: Slot reservations and double-allocation prevention (ensures reserved slots cannot be allocated to regular walk-in traffic).

---

## 🎓 10. Step-by-Step College Demonstration Walkthrough

Follow this scripted procedure during viva/demonstration:

1. **Authentication & Operator Login**:
   - Open `http://localhost:5173`.
   - Observe that unauthenticated visitors are automatically directed to the **SmartPark Sign In** page.
   - Click **Create Account** to navigate to registration.
   - Enter Full Name (e.g., `Rohan Sharma`), Email (`rohan@smartpark.com`), and Password (`Secure123!`).
   - Click **Register Account**: The system hashes the password with bcrypt, stores the account in SQLite, issues a signed JWT, and redirects to the live Dashboard!
   - Demonstrate the show/hide password toggle.

2. **System Health & Dashboard Overview**:
   - Observe the **Operator Profile** card in the sidebar showing the logged-in user name, email, and Sign Out button.
   - Point out the **System Status Pill** in the sidebar showing `FastAPI Connected` and `SQLite: smartpark.db`.
   - Show the 4 telemetry cards: Total Slots (10), Available Slots, Occupied Slots, and Waiting Queue.
   - Show the **DSA Architecture Overview** card explaining time complexities ($\mathcal{O}(1)$ Hash Map, $\mathcal{O}(N)$ Array, $\mathcal{O}(1)$ FIFO Queue).

3. **Visual Parking Slots Grid**:
   - Navigate to **Parking Slots**.
   - Show the 10 slots distributed across Floor 1 (`S-101` to `S-108`) and Floor 2 (`S-109`, `S-110`).
   - Note the slot types: Standard, Compact, EV Charging, and Accessible.

4. **Vehicle Entry & First-Fit Allocation**:
   - Navigate to **Vehicle Entry**.
   - Enter license plate `KA-01-AB-1234` (Vehicle Type: Car). Click **Register & Allocate Slot**.
   - Highlight the result card: Vehicle receives slot `S-101` via **First-Fit Allocation** in $\mathcal{O}(1)$ time.
   - Attempt to register the exact same plate `KA-01-AB-1234` again.
   - Show the error rejection banner: *"Vehicle already has an active parking session"*.

5. **Slot Reservation & Conflict Prevention**:
   - Navigate to **Reservations**.
   - Pre-book slot `S-103` for vehicle `DL-05-XY-9999`.
   - Switch to **Parking Slots**: Note slot `S-103` has changed status to orange **Reserved**.
   - Switch to **Vehicle Entry** and register a regular car `MH-12-CD-5555`.
   - Observe that First-Fit skips `S-103` and allocates the next vacant slot (e.g. `S-102`), proving double-allocation prevention.
   - Now register the reserving vehicle `DL-05-XY-9999`: It smoothly checks into its reserved slot `S-103`.

6. **Capacity Saturation & FIFO Waiting Queue**:
   - Fill the remaining available slots by registering cars until all 10 slots are occupied.
   - Register an 11th vehicle: `TN-07-ZZ-7777`.
   - Show that instead of failing, the system enters the vehicle into the **FIFO Waiting Queue** at position 1.
   - Navigate to **Queue Management**: Show `TN-07-ZZ-7777` waiting in position #1 with exact entry timestamp.

7. **Vehicle Exit, Tariff Billing & Automatic Dispatch**:
   - Navigate to **Vehicle Exit**.
   - Process departure for vehicle `KA-01-AB-1234` from slot `S-101`.
   - Point out the checkout bill: Duration calculation, grace period check, and computed parking fee (₹20/hr base tariff).
   - Point out the green banner at the bottom: **"Auto-Dispatched Queued Vehicle"** — Slot `S-101` was immediately reassigned to `TN-07-ZZ-7777` without any manual intervention!
   - Navigate back to **Queue Management**: The queue count decremented back to 0.

8. **Audit Trail & Operator Sign Out**:
   - Navigate to **Parking History** to inspect the audit log of completed sessions and collected fees.
   - Click the **Sign Out** button in the sidebar footer or top header.
   - Confirm immediate redirection back to the **Sign In** page, with the JWT session cleared and protected routes completely secured against unauthorized access.

---

## 📌 11. Known Limitations

1. **Single Node In-Memory Cache**: The in-memory DSA instances (`ParkingLotDSA` and `WaitingQueueDSA`) reside in the FastAPI process memory and synchronize with SQLite. In a multi-worker distributed environment, synchronization would require a shared distributed cache (e.g. Redis).
2. **Fixed 10-Slot Default Dimension**: Initial seed creates 10 slots for demonstration clarity; additional slots can be dynamically added via the backend API.
3. **No Hardware Sensor Integration**: Vehicle arrival is triggered via admin software entry rather than physical ultrasonic/RFID boom barrier hardware sensors.
