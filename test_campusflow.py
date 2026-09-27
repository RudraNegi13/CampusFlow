"""
test_campusflow.py
------------------
Automated test suite for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Tests Required by Course Guidelines:
1. Valid resource creation
2. Invalid resource capacity
3. Valid booking
4. Duplicate booking
5. Capacity conflict
6. Time conflict
7. Invalid request
8. Successful alternative-slot search
9. Utilization calculation
"""

import unittest
import copy

from models import create_resource, create_request, create_booking
import validation
import resource_manager
import request_manager
import conflict_manager
import allocation_engine
import analytics


class TestCampusFlow(unittest.TestCase):
    """Unit and integration test cases for CampusFlow core modules."""

    def setUp(self):
        """Set up fresh mock data before each test."""
        self.sample_resources = {
            "LAB01": {
                "resource_id": "LAB01",
                "name": "Computer Lab 1",
                "resource_type": "Computer Lab",
                "capacity": 30,
                "facilities": ["AC", "Computers", "Internet", "Projector"],
                "available_slots": [
                    ("Monday", "09:00", "12:00"),
                    ("Monday", "14:00", "17:00")
                ]
            },
            "LAB02": {
                "resource_id": "LAB02",
                "name": "Computer Lab 2",
                "resource_type": "Computer Lab",
                "capacity": 50,
                "facilities": ["AC", "Computers", "Internet", "Projector", "Whiteboard"],
                "available_slots": [
                    ("Monday", "14:00", "18:00")
                ]
            },
            "ROOM01": {
                "resource_id": "ROOM01",
                "name": "Study Room A",
                "resource_type": "Study Room",
                "capacity": 8,
                "facilities": ["AC", "Internet", "Whiteboard"],
                "available_slots": [
                    ("Monday", "08:00", "20:00"),
                    ("Tuesday", "08:00", "20:00")
                ]
            }
        }

        self.sample_bookings = [
            {
                "booking_id": "BK201",
                "request_id": "REQ101",
                "student_id": "STU1001",
                "student_name": "Rohan Gupta",
                "resource_id": "LAB01",
                "resource_name": "Computer Lab 1",
                "resource_type": "Computer Lab",
                "day": "Monday",
                "start_time": "14:00",
                "end_time": "16:00",
                "student_count": 25,
                "facilities_used": ["Computers", "Projector"]
            }
        ]

        self.sample_requests = [
            {
                "request_id": "REQ101",
                "student_id": "STU1001",
                "student_name": "Rohan Gupta",
                "resource_type": "Computer Lab",
                "student_count": 25,
                "day": "Monday",
                "start_time": "14:00",
                "end_time": "16:00",
                "facilities": ["Computers"],
                "status": "ALLOCATED",
                "allocated_resource_id": "LAB01"
            }
        ]

    # -----------------------------------------------------
    # Test 1: Valid Resource Creation
    # -----------------------------------------------------
    def test_01_valid_resource_creation(self):
        """Verifies that a well-formed resource is accepted and formatted correctly."""
        res_dict = copy.deepcopy(self.sample_resources)
        ok, msg = resource_manager.add_resource(
            res_dict,
            resource_id="SEM01",
            name="Seminar Hall 1",
            res_type="Seminar Room",
            capacity=100,
            facilities=["AC", "Projector", "Audio System"],
            available_slots=[("Monday", "10:00", "15:00")]
        )
        self.assertTrue(ok)
        self.assertIn("SEM01", res_dict)
        self.assertEqual(res_dict["SEM01"]["capacity"], 100)
        self.assertEqual(res_dict["SEM01"]["resource_type"], "Seminar Room")

    # -----------------------------------------------------
    # Test 2: Invalid Resource Capacity (Negative & Zero)
    # -----------------------------------------------------
    def test_02_invalid_resource_capacity(self):
        """Verifies that zero or negative capacities are rejected."""
        # Zero capacity
        valid_zero, _ = validation.validate_positive_integer(0, "Capacity")
        self.assertFalse(valid_zero)

        # Negative capacity
        valid_neg, _ = validation.validate_positive_integer(-15, "Capacity")
        self.assertFalse(valid_neg)

        # Non-numeric capacity
        valid_str, _ = validation.validate_positive_integer("ten", "Capacity")
        self.assertFalse(valid_str)

        # Rejection by resource_manager
        res_dict = copy.deepcopy(self.sample_resources)
        ok, msg = resource_manager.add_resource(
            res_dict, "LAB99", "Bad Lab", "Computer Lab", -5, [], []
        )
        self.assertFalse(ok)
        self.assertNotIn("LAB99", res_dict)

    # -----------------------------------------------------
    # Test 3: Valid Booking Creation
    # -----------------------------------------------------
    def test_03_valid_booking(self):
        """Verifies that a valid non-conflicting request is successfully allocated."""
        res_dict = copy.deepcopy(self.sample_resources)
        bk_list = copy.deepcopy(self.sample_bookings)
        
        # Valid request for Monday morning (09:00 - 11:00) in Computer Lab
        req = create_request(
            request_id="REQ102",
            student_id="STU1002",
            student_name="Priya Sharma",
            resource_type="Computer Lab",
            student_count=20,
            day="Monday",
            start_time="09:00",
            end_time="11:00",
            facilities=["Computers"]
        )

        success, booking, log, alts = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertTrue(success)
        self.assertIsNotNone(booking)
        self.assertEqual(booking["resource_id"], "LAB01")
        self.assertEqual(req["status"], "ALLOCATED")
        self.assertEqual(len(bk_list), 2)  # Added to bookings list

    # -----------------------------------------------------
    # Test 4: Duplicate Booking (Student Schedule Collision)
    # -----------------------------------------------------
    def test_04_duplicate_booking(self):
        """Verifies that a student cannot book two resources at the same time."""
        res_dict = copy.deepcopy(self.sample_resources)
        bk_list = copy.deepcopy(self.sample_bookings)

        # STU1001 is already booked in LAB01 on Monday 14:00 - 16:00
        # Try requesting Study Room during overlapping time: Monday 15:00 - 16:30
        req = create_request(
            request_id="REQ103",
            student_id="STU1001",
            student_name="Rohan Gupta",
            resource_type="Study Room",
            student_count=4,
            day="Monday",
            start_time="15:00",
            end_time="16:30",
            facilities=[]
        )

        success, booking, log, alts = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertFalse(success)
        self.assertIsNone(booking)
        self.assertEqual(req["status"], "FAILED")
        # Check rejection log contains student schedule conflict
        log_str = " ".join([item[2] for item in log])
        self.assertIn("Student Schedule Conflict", log_str)

    # -----------------------------------------------------
    # Test 5: Capacity Conflict
    # -----------------------------------------------------
    def test_05_capacity_conflict(self):
        """Verifies that a resource is rejected if student count exceeds capacity."""
        res_dict = copy.deepcopy(self.sample_resources)
        bk_list = []  # No bookings

        # Request 15 students for Study Room A (which only has capacity 8)
        req = create_request(
            request_id="REQ104",
            student_id="STU1004",
            student_name="Vikram",
            resource_type="Study Room",
            student_count=15,
            day="Monday",
            start_time="10:00",
            end_time="12:00",
            facilities=[]
        )

        success, booking, log, alts = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertFalse(success)
        self.assertIsNone(booking)
        log_str = " ".join([item[2] for item in log])
        self.assertIn("Insufficient capacity", log_str)

    # -----------------------------------------------------
    # Test 6: Time Conflict (Resource Occupied)
    # -----------------------------------------------------
    def test_06_time_conflict(self):
        """Verifies that overlapping booking for the same resource is rejected."""
        res_dict = copy.deepcopy(self.sample_resources)
        # LAB01 is already booked on Monday 14:00 - 16:00
        bk_list = copy.deepcopy(self.sample_bookings)

        # Another student requests LAB01 on Monday 15:00 - 17:00 (overlaps with 14:00-16:00)
        # Note: LAB02 is available from 14:00-18:00, so let's temporarily exclude LAB02
        del res_dict["LAB02"]

        req = create_request(
            request_id="REQ105",
            student_id="STU1005",
            student_name="Karan",
            resource_type="Computer Lab",
            student_count=20,
            day="Monday",
            start_time="15:00",
            end_time="17:00",
            facilities=["Computers"]
        )

        success, booking, log, alts = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertFalse(success)
        self.assertIsNone(booking)
        log_str = " ".join([item[2] for item in log])
        self.assertIn("already occupied", log_str)

    # -----------------------------------------------------
    # Test 7: Invalid Request (Time and Type Validation)
    # -----------------------------------------------------
    def test_07_invalid_request(self):
        """Verifies input validation on invalid time ranges and resource types."""
        # Invalid time: Start after end (16:00 to 14:00)
        v, msg = validation.validate_time_range("16:00", "14:00")
        self.assertFalse(v)
        self.assertIn("earlier than end time", msg)

        # Invalid time format ("9am")
        v, _ = validation.validate_time_format("9am", "Start Time")
        self.assertFalse(v)

        # Invalid day ("Funday")
        v, _ = validation.validate_day("Funday")
        self.assertFalse(v)

        # Invalid resource type ("Rocket Launchpad")
        v, _ = validation.validate_resource_type("Rocket Launchpad")
        self.assertFalse(v)

        # Comprehensive validation check
        is_ok, _ = validation.validate_request_data(
            "STU101", "Name", "Rocket Launchpad", 10, "Monday", "10:00", "12:00"
        )
        self.assertFalse(is_ok)

    # -----------------------------------------------------
    # Test 8: Successful Alternative-Slot Search
    # -----------------------------------------------------
    def test_08_alternative_slot_search(self):
        """Verifies that when exact slot is blocked, alternative available slots are returned."""
        res_dict = copy.deepcopy(self.sample_resources)
        # Block LAB01 on Monday 14:00-17:00 and remove LAB02
        del res_dict["LAB02"]
        bk_list = [
            {
                "booking_id": "BK201",
                "request_id": "REQ101",
                "student_id": "STU1001",
                "student_name": "Rohan Gupta",
                "resource_id": "LAB01",
                "resource_name": "Computer Lab 1",
                "resource_type": "Computer Lab",
                "day": "Monday",
                "start_time": "14:00",
                "end_time": "17:00",
                "student_count": 25,
                "facilities_used": ["Computers"]
            }
        ]

        # Request for Monday 14:00-16:00
        req = create_request(
            request_id="REQ106",
            student_id="STU1006",
            student_name="Deepa",
            resource_type="Computer Lab",
            student_count=20,
            day="Monday",
            start_time="14:00",
            end_time="16:00",
            facilities=["Computers"]
        )

        success, booking, log, alternatives = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertFalse(success)
        self.assertGreater(len(alternatives), 0)
        # Morning slot (09:00 - 12:00) should be suggested as alternative
        found_morning = any(alt["start_time"] == "09:00" and alt["end_time"] == "12:00" for alt in alternatives)
        self.assertTrue(found_morning)

    # -----------------------------------------------------
    # Test 9: Utilization & Analytics Calculation
    # -----------------------------------------------------
    def test_09_utilization_calculation(self):
        """Verifies counting, summation, max/min, and percentage calculations in analytics."""
        res_dict = copy.deepcopy(self.sample_resources)
        bk_list = copy.deepcopy(self.sample_bookings)
        req_list = copy.deepcopy(self.sample_requests)

        # 1. Total counts
        counts = analytics.count_summary_totals(res_dict, req_list, bk_list)
        self.assertEqual(counts["total_resources"], 3)
        self.assertEqual(counts["total_bookings"], 1)
        self.assertEqual(counts["successful_allocations"], 1)

        # 2. Allocation success rate
        rate = analytics.calculate_allocation_success_rate(req_list)
        self.assertEqual(rate, 100.0)

        # 3. Most-used resource
        most, least = analytics.find_most_and_least_used_resources(res_dict, bk_list)
        self.assertEqual(most[0], "LAB01")
        self.assertEqual(most[2], 1)

        # 4. Utilization percentage
        util_pct = analytics.calculate_resource_utilization_percentage(res_dict, bk_list)
        self.assertIsInstance(util_pct, float)
        self.assertGreater(util_pct, 0.0)

        # 5. Capacity efficiency
        eff_pct = analytics.calculate_capacity_efficiency(bk_list, res_dict)
        # LAB01 has capacity 30, booking had 25 students -> 25/30 = 83.33%
        self.assertEqual(eff_pct, 83.33)

    # -----------------------------------------------------
    # Test 10: Resource Search & Multi-criteria Filtering
    # -----------------------------------------------------
    def test_10_search_and_filter(self):
        """Verifies linear search and multi-attribute filtering algorithms."""
        res_dict = copy.deepcopy(self.sample_resources)

        # Filter by type 'Computer Lab'
        labs = resource_manager.search_resources(res_dict, res_type="Computer Lab")
        self.assertEqual(len(labs), 2)

        # Filter by capacity >= 40
        large_rooms = resource_manager.search_resources(res_dict, min_capacity=40)
        self.assertEqual(len(large_rooms), 1)
        self.assertEqual(large_rooms[0]["resource_id"], "LAB02")

        # Filter by facility 'Whiteboard'
        wb_rooms = resource_manager.search_resources(res_dict, required_facility="Whiteboard")
        self.assertEqual(len(wb_rooms), 2)  # LAB02 and ROOM01

    # -----------------------------------------------------
    # Test 11: Audit Conflict Detection
    # -----------------------------------------------------
    def test_11_audit_conflicts(self):
        """Verifies pairwise booking auditing to detect overlapping schedules."""
        corrupted_bookings = [
            {
                "booking_id": "BK301",
                "student_id": "STU101",
                "student_name": "Alice",
                "resource_id": "LAB01",
                "resource_name": "Computer Lab 1",
                "day": "Monday",
                "start_time": "10:00",
                "end_time": "12:00"
            },
            {
                "booking_id": "BK302",
                "student_id": "STU102",
                "student_name": "Bob",
                "resource_id": "LAB01",
                "resource_name": "Computer Lab 1",
                "day": "Monday",
                "start_time": "11:00",
                "end_time": "13:00"  # Overlaps with BK301 on LAB01!
            }
        ]

        conflicts = conflict_manager.audit_all_bookings(corrupted_bookings)
        self.assertEqual(len(conflicts), 1)
        self.assertIn("Resource Double-Booking", conflicts[0][2])

    # -----------------------------------------------------
    # Test 12: Best-Fit Capacity Optimization
    # -----------------------------------------------------
    def test_12_best_fit_selection(self):
        """Verifies that the allocation engine selects the room with minimal seat wastage."""
        res_dict = copy.deepcopy(self.sample_resources)
        # LAB01 (cap 30) and LAB02 (cap 50) both available on Monday 14:00-17:00
        # Clear bookings
        bk_list = []

        req = create_request(
            request_id="REQ200",
            student_id="STU200",
            student_name="Charlie",
            resource_type="Computer Lab",
            student_count=28,  # Closest to 30 (waste=2) rather than 50 (waste=22)
            day="Monday",
            start_time="14:00",
            end_time="16:00",
            facilities=["Computers"]
        )

        success, booking, log, alts = allocation_engine.process_allocation_request(
            req, res_dict, bk_list
        )

        self.assertTrue(success)
        self.assertEqual(booking["resource_id"], "LAB01")


if __name__ == "__main__":
    unittest.main()

