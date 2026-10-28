"""
Test suite for SmartPark Core DSA and Backend Functionality
Run with: python tests/test_dsa_and_slots.py
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.dsa.parking_lot import ParkingLotDSA, SlotNode
from app.dsa.queue_manager import WaitingQueueDSA
from app.main import init_db_and_dsa, app
from app.db.session import SessionLocal, engine, Base
from app.models.models import ParkingSlot, SlotStatus

def test_parking_lot_dsa():
    print("Testing ParkingLotDSA...")
    dsa = ParkingLotDSA()

    # Create test slots (Array)
    dsa.slots = [
        SlotNode(id=1, slot_number="A-101", slot_type="standard", status="available", floor=1),
        SlotNode(id=2, slot_number="A-102", slot_type="compact", status="available", floor=1),
        SlotNode(id=3, slot_number="A-103", slot_type="ev", status="available", floor=1),
    ]

    # Test 1: First-Fit slot search
    slot = dsa.find_available_slot()
    assert slot is not None and slot.id == 1, "First-Fit should find slot A-101"

    # Test 2: Specific type First-Fit
    ev_slot = dsa.find_available_slot(slot_type="ev")
    assert ev_slot is not None and ev_slot.slot_number == "A-103", "Should find EV slot"

    # Test 3: Allocate slot and verify Hash Map O(1) lookup
    success = dsa.allocate_slot(1, "KA-01-MJ-9999")
    assert success is True, "Allocation should succeed"
    assert dsa.slots[0].status == "occupied"

    lookup = dsa.find_vehicle_slot("KA-01-MJ-9999")
    assert lookup is not None and lookup.id == 1, "Hash Map lookup should return slot 1 in O(1)"

    # Test 4: Release slot and verify Hash Map deletion
    released = dsa.release_slot(1)
    assert released is not None and released.status == "available"
    assert dsa.find_vehicle_slot("KA-01-MJ-9999") is None, "Plate should be removed from Hash Map"

    print("[OK] ParkingLotDSA tests passed successfully!")

def test_waiting_queue_dsa():
    print("Testing WaitingQueueDSA...")
    queue = WaitingQueueDSA()

    assert queue.is_empty() is True
    assert queue.size() == 0

    # Test FIFO behavior
    v1 = queue.enqueue_fifo(101, "MH-12-AB-1111", "car")
    v2 = queue.enqueue_fifo(102, "DL-01-XY-2222", "suv")
    v3 = queue.enqueue_fifo(103, "KA-05-ZZ-3333", "bike")

    assert queue.size() == 3
    assert queue.peek().license_plate == "MH-12-AB-1111", "FIFO front should be first car"

    # Dequeue in arrival order
    d1 = queue.dequeue()
    assert d1.license_plate == "MH-12-AB-1111", "First dequeued must be v1"
    d2 = queue.dequeue()
    assert d2.license_plate == "DL-01-XY-2222", "Second dequeued must be v2"
    d3 = queue.dequeue()
    assert d3.license_plate == "KA-05-ZZ-3333", "Third dequeued must be v3"
    assert queue.is_empty() is True

    print("[OK] WaitingQueueDSA tests passed successfully!")

def test_database_and_seeding():
    print("Testing Database Initialization & Seeding...")
    with SessionLocal() as db:
        from app.services.parking_service import seed_10_initial_slots
        seed_10_initial_slots(db, force=True)
        count = db.query(ParkingSlot).count()
        assert count == 10, f"Expected 10 seeded slots, found {count}"

        avail = db.query(ParkingSlot).filter(ParkingSlot.status == SlotStatus.AVAILABLE.value).count()
        assert avail == 10, f"Expected all 10 seeded slots to start available, found {avail}"

    print(f"[OK] SQLite database successfully initialized with {count} slots!")

def test_api_endpoints():
    print("Testing FastAPI Endpoints via TestClient...")
    from fastapi.testclient import TestClient
    from app.core.security import create_access_token
    from app.models.models import User
    from app.core.security import hash_password
    
    with SessionLocal() as db:
        if not db.query(User).filter(User.email == "tester@testpark.com").first():
            user = User(full_name="Tester", email="tester@testpark.com", hashed_password=hash_password("pw123456"))
            db.add(user)
            db.commit()
    
    token = create_access_token({"sub": "tester@testpark.com"})

    with TestClient(app) as client:
        # Test 1: Health check (Public)
        res = client.get("/api/health")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        health_data = res.json()
        assert health_data["status"] == "healthy"
        assert health_data["database"]["status"] == "connected"
        assert health_data["dsa_engine"]["status"] == "ready"
        print("[OK] /api/health returned healthy status and SQLite connection!")

        # Set Bearer token for protected routes
        client.headers["Authorization"] = f"Bearer {token}"

        # Test 2: Slots list (Protected)
        res = client.get("/api/slots")
        assert res.status_code == 200
        slots = res.json()
        assert len(slots) == 10
        assert slots[0]["slot_number"] == "S-101"
        print(f"[OK] /api/slots returned {len(slots)} active slots!")

        # Test 3: Dashboard summary (Protected)
        res = client.get("/api/dashboard/summary")
        assert res.status_code == 200
        dash = res.json()
        assert dash["total_slots"] == 10
        assert dash["available_slots"] == 10
        assert "dsa_metrics" in dash
        print(f"[OK] /api/dashboard/summary verified (Total: {dash['total_slots']}, Avail: {dash['available_slots']})!")

if __name__ == "__main__":
    test_parking_lot_dsa()
    test_waiting_queue_dsa()
    test_database_and_seeding()
    test_api_endpoints()
    print("\nAll Stage 1 DSA, Database, and API endpoint tests passed perfectly!")

