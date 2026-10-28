"""
Comprehensive Test Suite for SmartPark Core Parking Management Logic
=====================================================================
Covers the 5 mandatory testing scenarios:
1. Vehicle enters when a slot is available (First-Fit allocation).
2. Vehicle enters when all slots are occupied (FIFO waiting queue addition).
3. Waiting vehicle receives a slot automatically after another vehicle exits.
4. Duplicate active vehicle entry is rejected with HTTP 400.
5. Slot allocation consistency with SQLite database records and O(1) Hash Map.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app, init_db_and_dsa
from app.db.session import SessionLocal
from app.models.models import ParkingSlot, ParkingSession, WaitingQueue, Vehicle, SlotStatus, SessionStatus, QueueStatus
from app.dsa.parking_lot import parking_lot_dsa
from app.dsa.queue_manager import waiting_queue_dsa
from app.services.parking_service import seed_10_initial_slots

def setup_fresh_test_db():
    """Resets database and seeds exactly 10 initial parking slots."""
    with SessionLocal() as db:
        seed_10_initial_slots(db, force=True)

def get_auth_client():
    from app.core.security import create_access_token, hash_password
    from app.models.models import User
    with SessionLocal() as db:
        if not db.query(User).filter(User.email == "tester@testpark.com").first():
            db.add(User(full_name="Tester", email="tester@testpark.com", hashed_password=hash_password("pw123456")))
            db.commit()
    token = create_access_token({"sub": "tester@testpark.com"})
    client = TestClient(app)
    client.headers["Authorization"] = f"Bearer {token}"
    return client

def test_scenario_1_vehicle_entry_slot_available():
    """Scenario 1: Vehicle enters when a slot is available."""
    print("\n--- Running Scenario 1: Vehicle enters when slot is available ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # Check initial slot count
        res = client.get("/api/slots")
        assert res.status_code == 200
        slots = res.json()
        assert len(slots) == 10, f"Expected 10 slots, found {len(slots)}"
        assert slots[0]["status"] == "available"

        # Vehicle Entry
        entry_payload = {
            "license_plate": "KA-01-AB-1234",
            "vehicle_type": "car",
            "owner_name": "Rohan Sharma"
        }
        res = client.post("/api/vehicles/entry", json=entry_payload)
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
        data = res.json()

        assert data["status"] == "allocated"
        assert data["slot_number"] == "S-101", f"First available slot should be S-101, got {data['slot_number']}"
        assert data["license_plate"] == "KA-01-AB-1234"
        assert data["queue_position"] is None

        # Verify in-memory Hash Map O(1) lookup
        lookup = parking_lot_dsa.find_vehicle_slot("KA-01-AB-1234")
        assert lookup is not None and lookup.slot_number == "S-101", "Hash Map must hold slot S-101"

        # Verify SQLite record consistency
        with SessionLocal() as db:
            slot_s101 = db.query(ParkingSlot).filter(ParkingSlot.slot_number == "S-101").first()
            assert slot_s101.status == SlotStatus.OCCUPIED.value, "Database slot status must be occupied"

            active_session = db.query(ParkingSession).filter(
                ParkingSession.slot_id == slot_s101.id,
                ParkingSession.status == SessionStatus.ACTIVE.value
            ).first()
            assert active_session is not None, "Active parking session must exist in DB"
            assert active_session.vehicle.license_plate == "KA-01-AB-1234"

    print("[PASS] Scenario 1 passed: Vehicle successfully allocated to first available slot S-101.")

def test_scenario_2_all_slots_occupied_fifo_queue():
    """Scenario 2: Vehicle enters when all 10 slots are occupied."""
    print("\n--- Running Scenario 2: Vehicle enters when all slots are occupied ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # Fill all 10 slots with 10 distinct vehicles
        for i in range(1, 11):
            plate = f"KA-01-CAR-{i:02d}"
            res = client.post("/api/vehicles/entry", json={"license_plate": plate, "vehicle_type": "car"})
            assert res.status_code == 201
            assert res.json()["status"] == "allocated"

        # Verify all 10 slots are occupied
        res = client.get("/api/slots?status_filter=available")
        assert res.status_code == 200
        available_slots = res.json()
        assert len(available_slots) == 0, f"Expected 0 available slots, found {len(available_slots)}"

        # 11th vehicle arrives -> Must be queued into FIFO Waiting Queue at position 1
        queue_vehicle_plate = "DL-05-QUEUE-01"
        res = client.post("/api/vehicles/entry", json={"license_plate": queue_vehicle_plate, "vehicle_type": "suv"})
        assert res.status_code == 201
        data = res.json()

        assert data["status"] == "queued"
        assert data["queue_position"] == 1, f"Expected queue position 1, got {data['queue_position']}"
        assert data["slot_number"] is None
        assert "added to FIFO waiting queue at position 1" in data["message"]

        # 12th vehicle arrives -> Queue position 2
        queue_vehicle_plate_2 = "MH-12-QUEUE-02"
        res2 = client.post("/api/vehicles/entry", json={"license_plate": queue_vehicle_plate_2, "vehicle_type": "car"})
        assert res2.status_code == 201
        assert res2.json()["queue_position"] == 2

        # Verify waiting queue endpoint
        q_res = client.get("/api/queue")
        assert q_res.status_code == 200
        q_items = q_res.json()
        assert len(q_items) == 2
        assert q_items[0]["license_plate"] == "DL-05-QUEUE-01"
        assert q_items[0]["position"] == 1
        assert q_items[1]["license_plate"] == "MH-12-QUEUE-02"
        assert q_items[1]["position"] == 2

    print("[PASS] Scenario 2 passed: Arriving vehicles correctly placed into FIFO waiting queue.")

def test_scenario_3_waiting_vehicle_auto_allocated_on_exit():
    """Scenario 3: A waiting vehicle receives a slot after another vehicle exits."""
    print("\n--- Running Scenario 3: Waiting vehicle auto-allocated on vehicle exit ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # Fill all 10 slots
        for i in range(1, 11):
            client.post("/api/vehicles/entry", json={"license_plate": f"KA-01-PARK-{i:02d}", "vehicle_type": "car"})

        # Enqueue 1 waiting vehicle
        queued_plate = "KA-04-WAITING-CAR"
        client.post("/api/vehicles/entry", json={"license_plate": queued_plate, "vehicle_type": "car"})

        # Verify queue has 1 vehicle
        q_res = client.get("/api/queue")
        assert len(q_res.json()) == 1
        assert q_res.json()[0]["license_plate"] == queued_plate

        # Vehicle 1 (in slot S-101) exits
        exit_payload = {"license_plate": "KA-01-PARK-01"}
        exit_res = client.post("/api/vehicles/exit", json=exit_payload)
        assert exit_res.status_code == 200, f"Exit failed: {exit_res.text}"
        exit_data = exit_res.json()

        assert exit_data["status"] == "success"
        assert exit_data["license_plate"] == "KA-01-PARK-01"
        assert exit_data["slot_number"] == "S-101"
        assert "auto_allocated_to_queued_vehicle" in exit_data
        assert exit_data["auto_allocated_to_queued_vehicle"] is not None

        auto_alloc = exit_data["auto_allocated_to_queued_vehicle"]
        assert auto_alloc["license_plate"] == queued_plate
        assert auto_alloc["slot_number"] == "S-101"

        # Verify waiting queue is now empty
        q_res_after = client.get("/api/queue")
        assert len(q_res_after.json()) == 0, "Queue should now be empty"

        # Verify queued vehicle is now actively parked in slot S-101
        active_res = client.get("/api/sessions/active")
        assert active_res.status_code == 200
        active_plates = [s["license_plate"] for s in active_res.json()]
        assert queued_plate in active_plates, f"{queued_plate} must now be active"

        # Verify Hash Map O(1) lookup now resolves to S-101
        lookup = parking_lot_dsa.find_vehicle_slot(queued_plate)
        assert lookup is not None and lookup.slot_number == "S-101"

    print("[PASS] Scenario 3 passed: Waiting vehicle automatically dispatched to slot S-101.")

def test_scenario_4_duplicate_active_vehicle_rejected():
    """Scenario 4: A duplicate active vehicle entry is rejected."""
    print("\n--- Running Scenario 4: Duplicate active vehicle entry rejected ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # First entry succeeds
        res1 = client.post("/api/vehicles/entry", json={"license_plate": "MH-02-DUP-9999", "vehicle_type": "car"})
        assert res1.status_code == 201

        # Second entry with identical plate must be rejected with 400
        res2 = client.post("/api/vehicles/entry", json={"license_plate": "MH-02-DUP-9999", "vehicle_type": "car"})
        assert res2.status_code == 400, f"Expected 400, got {res2.status_code}"
        err = res2.json()
        assert "already has an active parking session" in err["detail"]

    print("[PASS] Scenario 4 passed: Duplicate active vehicle entry correctly rejected.")

def test_scenario_5_slot_allocation_consistency_with_db():
    """Scenario 5: Slot allocation remains consistent with database records across exit & restarts."""
    print("\n--- Running Scenario 5: Database consistency & persistence check ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # Park 3 vehicles
        client.post("/api/vehicles/entry", json={"license_plate": "KA-01-AA-1111", "vehicle_type": "car"})
        client.post("/api/vehicles/entry", json={"license_plate": "KA-01-BB-2222", "vehicle_type": "car"})
        client.post("/api/vehicles/entry", json={"license_plate": "KA-01-CC-3333", "vehicle_type": "car"})

        # Exit vehicle 2 (S-102)
        client.post("/api/vehicles/exit", json={"license_plate": "KA-01-BB-2222"})

        # Check DB records directly via SQLAlchemy Session
        with SessionLocal() as db:
            s1 = db.query(ParkingSlot).filter(ParkingSlot.slot_number == "S-101").first()
            s2 = db.query(ParkingSlot).filter(ParkingSlot.slot_number == "S-102").first()
            s3 = db.query(ParkingSlot).filter(ParkingSlot.slot_number == "S-103").first()

            assert s1.status == SlotStatus.OCCUPIED.value
            assert s2.status == SlotStatus.AVAILABLE.value
            assert s3.status == SlotStatus.OCCUPIED.value

        # Simulate backend restart by re-synchronizing in-memory DSA cache from DB
        with SessionLocal() as db:
            from app.services.parking_service import sync_dsa_from_db
            sync_dsa_from_db(db)

        # In-memory DSA state must match SQLite exactly
        assert parking_lot_dsa.find_vehicle_slot("KA-01-AA-1111").slot_number == "S-101"
        assert parking_lot_dsa.find_vehicle_slot("KA-01-BB-2222") is None
        assert parking_lot_dsa.find_vehicle_slot("KA-01-CC-3333").slot_number == "S-103"

        # First-fit search should now allocate freed slot S-102 to the next car
        res_next = client.post("/api/vehicles/entry", json={"license_plate": "KA-01-DD-4444", "vehicle_type": "car"})
        assert res_next.status_code == 201
        assert res_next.json()["slot_number"] == "S-102", "First-Fit should reuse freed slot S-102"

    print("[PASS] Scenario 5 passed: Slot allocation remains strictly consistent with database records.")

def test_parking_charges_calculation():
    """Verify tariff computation (grace period, hourly rounding, configurable rates)."""
    print("\n--- Running Test: Parking Charges & Grace Period Calculation ---")
    now = datetime.now(timezone.utc)

    # 10 minutes -> Within 15-min grace period -> Free
    entry_10m = now - timedelta(minutes=10)
    dur, fee, text = (10, 0.0, "Grace period applied")
    from app.services.parking_service import calculate_parking_charges
    dur, fee, text = calculate_parking_charges(entry_10m, now)
    assert fee == 0.0, f"Expected 0.0 fee within grace period, got {fee}"
    assert "Grace period applied" in text

    # 45 minutes -> 1 hour * ₹20 = ₹20.0
    entry_45m = now - timedelta(minutes=45)
    dur, fee, text = calculate_parking_charges(entry_45m, now)
    assert fee == 20.0, f"Expected ₹20.0 for 45 mins, got {fee}"

    # 75 minutes -> 2 hours * ₹20 = ₹40.0
    entry_75m = now - timedelta(minutes=75)
    dur, fee, text = calculate_parking_charges(entry_75m, now)
    assert fee == 40.0, f"Expected ₹40.0 for 75 mins, got {fee}"

    print("[PASS] Parking charges calculation passed: Grace period and hourly rates verified.")

def test_scenario_6_reservations_prevent_double_allocation():
    """Scenario 6: Reservations do not cause double allocation."""
    print("\n--- Running Scenario 6: Reservations and Double-Allocation Prevention ---")
    setup_fresh_test_db()

    with get_auth_client() as client:
        # Step 1: Vehicle A reserves slot S-101
        res_payload = {
            "license_plate": "KA-01-VIP-7777",
            "slot_number": "S-101",
            "vehicle_type": "car",
            "duration_hours": 2
        }
        res = client.post("/api/reservations", json=res_payload)
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
        data = res.json()
        assert data["slot_number"] == "S-101"
        assert data["status"] == "reserved"

        # Step 2: Verify S-101 is marked RESERVED in slots list
        slots_res = client.get("/api/slots")
        s101 = next(s for s in slots_res.json() if s["slot_number"] == "S-101")
        assert s101["status"] == "reserved"

        # Step 3: Vehicle B (regular traffic) enters -> First-Fit MUST NOT allocate S-101!
        # It must allocate the next available slot S-102
        b_entry = client.post("/api/vehicles/entry", json={"license_plate": "KA-05-REGULAR-1", "vehicle_type": "car"})
        assert b_entry.status_code == 201
        assert b_entry.json()["slot_number"] == "S-102", f"Expected S-102, but S-101 was double allocated to {b_entry.json()['slot_number']}!"

        # Step 4: Re-reserving S-101 by another vehicle must be rejected
        dup_res = client.post("/api/reservations", json={
            "license_plate": "MH-01-TRY-DUP",
            "slot_number": "S-101"
        })
        assert dup_res.status_code == 400, "Re-reserving S-101 must be rejected with 400"
        assert "cannot be reserved because it is currently 'reserved'" in dup_res.json()["detail"]

        # Step 5: Vehicle A arrives -> checks into reserved slot S-101
        a_entry = client.post("/api/vehicles/entry", json={"license_plate": "KA-01-VIP-7777", "vehicle_type": "car"})
        assert a_entry.status_code == 201
        assert a_entry.json()["slot_number"] == "S-101"
        assert "checked into its reserved slot" in a_entry.json()["message"]

        # Step 6: Verify S-101 is now OCCUPIED by Vehicle A
        slots_after = client.get("/api/slots")
        s101_after = next(s for s in slots_after.json() if s["slot_number"] == "S-101")
        assert s101_after["status"] == "occupied"
        assert s101_after["current_vehicle_plate"] == "KA-01-VIP-7777"

    print("[PASS] Scenario 6 passed: Reservations strictly prevent double allocation.")

if __name__ == "__main__":
    test_scenario_1_vehicle_entry_slot_available()
    test_scenario_2_all_slots_occupied_fifo_queue()
    test_scenario_3_waiting_vehicle_auto_allocated_on_exit()
    test_scenario_4_duplicate_active_vehicle_rejected()
    test_scenario_5_slot_allocation_consistency_with_db()
    test_parking_charges_calculation()
    test_scenario_6_reservations_prevent_double_allocation()
    print("\n========================================================")
    print("ALL CORE TESTING SCENARIOS PASSED WITH 100% SUCCESS!")
    print("========================================================")

