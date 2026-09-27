"""
main.py
-------
Interactive terminal user interface for CampusFlow.
Course: CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Top-down modular architecture integrating all modules
- Menu-driven user loop with while and conditional branches
- Input sanitization and error prevention
- Formatting and terminal presentation
"""

import sys
from models import RESOURCE_TYPES, VALID_DAYS, STANDARD_FACILITIES
import storage
import validation
import resource_manager
import request_manager
import conflict_manager
import allocation_engine
import analytics


def print_header(title):
    """Prints a styled section header."""
    print("\n" + "=" * 50)
    print(f"  {title.upper()}")
    print("=" * 50)


def print_menu():
    """Prints the main interactive console menu."""
    print("\n" + "=" * 50)
    print("                 CAMPUSFLOW")
    print("  Smart College Resource Allocation System")
    print("  CSE1021: Problem Solving & Programming")
    print("=" * 50)
    print("  1. Submit Space Request")
    print("  2. View Available Resources")
    print("  3. Allocate Resource (Process Request)")
    print("  4. View Bookings")
    print("  5. Detect Conflicts & Audit")
    print("  6. View Utilization Analytics")
    print("  7. Manage Resources")
    print("  8. Exit")
    print("=" * 50)


# =========================================================
# SUB-WORKFLOWS
# =========================================================

def handle_submit_request(requests_list, resources_dict, bookings_list):
    """Handles student space request intake and immediate allocation offer."""
    print_header("Submit Space Request")

    # 1. Student ID
    while True:
        student_id = input("Enter Student ID (e.g. STU1005): ").strip()
        v, msg = validation.validate_non_empty(student_id, "Student ID")
        if v:
            break
        print(f"  [Error] {msg}")

    # 2. Student Name
    while True:
        student_name = input("Enter Student Name: ").strip()
        v, msg = validation.validate_non_empty(student_name, "Student Name")
        if v:
            break
        print(f"  [Error] {msg}")

    # 3. Resource Type
    print("\nSelect Required Resource Type:")
    for idx, r_type in enumerate(RESOURCE_TYPES, 1):
        print(f"  {idx}. {r_type}")
    while True:
        choice = input(f"Enter choice (1-{len(RESOURCE_TYPES)}): ").strip()
        v, msg = validation.validate_menu_choice(choice, 1, len(RESOURCE_TYPES))
        if v:
            selected_type = RESOURCE_TYPES[int(choice) - 1]
            break
        print(f"  [Error] {msg}")

    # 4. Student Count
    while True:
        count_str = input("Enter Number of Students: ").strip()
        v, msg = validation.validate_positive_integer(count_str, "Student Count")
        if v:
            student_count = int(count_str)
            break
        print(f"  [Error] {msg}")

    # 5. Preferred Day
    print(f"\nOperational Days: {', '.join(VALID_DAYS)}")
    while True:
        day_input = input("Enter Preferred Day (e.g. Monday): ").strip()
        v, msg = validation.validate_day(day_input)
        if v:
            selected_day = day_input.capitalize()
            break
        print(f"  [Error] {msg}")

    # 6. Time Range
    while True:
        start_time = input("Enter Start Time (HH:MM in 24-hr format, e.g. 10:00): ").strip()
        end_time = input("Enter End Time (HH:MM in 24-hr format, e.g. 12:00): ").strip()
        v, msg = validation.validate_time_range(start_time, end_time)
        if v:
            break
        print(f"  [Error] {msg}")

    # 7. Facilities
    print(f"\nStandard Facilities: {', '.join(sorted(list(STANDARD_FACILITIES)))}")
    fac_input = input("Enter Required Facilities (comma-separated, or press Enter for none): ").strip()
    facilities = []
    if fac_input:
        raw_items = [f.strip() for f in fac_input.split(",")]
        facilities = [f for f in raw_items if f]

    # Submit
    ok, res = request_manager.submit_request(
        requests_list, student_id, student_name, selected_type,
        student_count, selected_day, start_time, end_time, facilities
    )

    if ok:
        storage.save_requests(requests_list)
        print(f"\n[Success] Request '{res['request_id']}' submitted successfully!")
        print(request_manager.format_request_summary(res))

        # Ask if user wants immediate allocation
        alloc_now = input("\nWould you like to process allocation for this request immediately? (y/n): ").strip().lower()
        if alloc_now == 'y':
            run_single_allocation(res, resources_dict, bookings_list, requests_list)
    else:
        print(f"\n[Error] Request submission failed: {res}")


def run_single_allocation(request_data, resources_dict, bookings_list, requests_list):
    """Executes the allocation engine on a single request and displays the decision trace."""
    print_header(f"Allocating Request {request_data['request_id']}")
    print(f"Target: {request_data['resource_type']} on {request_data['day']} "
          f"from {request_data['start_time']} to {request_data['end_time']} "
          f"for {request_data['student_count']} student(s).")
    print("\n--- DECISION LOG TRACE ---")

    success, booking, rejection_log, alternatives = allocation_engine.process_allocation_request(
        request_data, resources_dict, bookings_list
    )

    for item in rejection_log:
        r_id, r_name, r_msg = item
        print(f"  * {r_name} ({r_id}): {r_msg}")

    print("--------------------------")

    if success:
        print(f"\n[SUCCESS] Resource '{booking['resource_name']}' ({booking['resource_id']}) allocated!")
        print(f"Booking ID      : {booking['booking_id']}")
        print(f"Allocated Slot  : {booking['day']} {booking['start_time']} - {booking['end_time']}")
        print(f"Booked For      : {booking['student_name']} ({booking['student_id']})")
        # Save updates
        storage.save_bookings(bookings_list)
        storage.save_requests(requests_list)
    else:
        print(f"\n[FAILED] Could not allocate exact requested slot for Request {request_data['request_id']}.")
        storage.save_requests(requests_list)

        if alternatives:
            print("\nRecommended Alternative Available Slots:")
            for idx, alt in enumerate(alternatives, 1):
                print(f"  {idx}. {alt['resource_name']} ({alt['resource_id']}) | "
                      f"{alt['day']} {alt['start_time']}-{alt['end_time']} ({alt['reason']})")
        else:
            print("No matching alternative slots could be found.")


def handle_view_resources(resources_dict):
    """Displays resource inventory with optional filtering."""
    print_header("Campus Resources Inventory")
    print(resource_manager.format_resource_table(list(resources_dict.values())))

    print("\nResource Options:")
    print("  1. Filter by Resource Type")
    print("  2. Filter by Minimum Capacity")
    print("  3. Filter by Facility")
    print("  4. View Resource Operational Schedule")
    print("  5. Return to Main Menu")

    choice = input("Enter choice (1-5): ").strip()
    if choice == "1":
        print(f"Types: {', '.join(RESOURCE_TYPES)}")
        t = input("Enter resource type to filter: ").strip()
        results = resource_manager.search_resources(resources_dict, res_type=t)
        print(f"\nFilter: Type = '{t}' ({len(results)} found)")
        print(resource_manager.format_resource_table(results))
    elif choice == "2":
        cap_str = input("Enter minimum capacity: ").strip()
        v, _ = validation.validate_positive_integer(cap_str, "Capacity")
        if v:
            results = resource_manager.search_resources(resources_dict, min_capacity=int(cap_str))
            print(f"\nFilter: Capacity >= {cap_str} ({len(results)} found)")
            print(resource_manager.format_resource_table(results))
        else:
            print("Invalid capacity value.")
    elif choice == "3":
        fac = input("Enter facility name (e.g. Projector, Computers): ").strip()
        results = resource_manager.search_resources(resources_dict, required_facility=fac)
        print(f"\nFilter: Has Facility '{fac}' ({len(results)} found)")
        print(resource_manager.format_resource_table(results))
    elif choice == "4":
        res_id = input("Enter Resource ID (e.g. LAB01): ").strip().upper()
        res = resource_manager.get_resource_by_id(resources_dict, res_id)
        if res:
            print(f"\nOperational Hours for {res['name']} ({res['resource_id']}):")
            for slot in res.get("available_slots", []):
                print(f"  - {slot[0]}: {slot[1]} to {slot[2]}")
        else:
            print(f"Resource '{res_id}' not found.")


def handle_allocation_menu(requests_list, resources_dict, bookings_list):
    """Processes pending requests interactively."""
    print_header("Resource Allocation Engine")
    pending = request_manager.get_pending_requests(requests_list)

    if not pending:
        print("No pending requests to allocate.")
        return

    print(f"Found {len(pending)} pending request(s):")
    for idx, req in enumerate(pending, 1):
        print(f"  {idx}. [{req['request_id']}] {req['student_name']} - "
              f"{req['resource_type']} ({req['student_count']} students) on "
              f"{req['day']} {req['start_time']}-{req['end_time']}")

    print("\nOptions:")
    print("  1. Allocate a specific pending request")
    print("  2. Allocate all pending requests in batch")
    print("  3. Cancel and return")

    choice = input("Enter choice (1-3): ").strip()
    if choice == "1":
        req_id_input = input("Enter Request ID to allocate (e.g. REQ104): ").strip().upper()
        target_req = request_manager.get_request_by_id(requests_list, req_id_input)
        if target_req:
            if target_req["status"] == "ALLOCATED":
                print(f"Request {req_id_input} has already been allocated.")
            else:
                run_single_allocation(target_req, resources_dict, bookings_list, requests_list)
        else:
            print(f"Request {req_id_input} not found.")
    elif choice == "2":
        print("\nProcessing all pending requests...")
        for req in pending:
            run_single_allocation(req, resources_dict, bookings_list, requests_list)


def handle_view_bookings(bookings_list, requests_list):
    """Displays existing confirmed bookings with filtering and cancellation."""
    print_header("Confirmed Bookings")
    if not bookings_list:
        print("No bookings registered currently.")
        return

    header = f"{'Booking ID':<11} | {'Resource':<18} | {'Student':<16} | {'Day':<10} | {'Time':<13} | {'Seats':<5}"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)

    for b in bookings_list:
        time_str = f"{b['start_time']}-{b['end_time']}"
        res_info = f"{b['resource_name'][:17]}"
        stu_info = f"{b['student_name'][:15]}"
        print(f"{b['booking_id']:<11} | {res_info:<18} | {stu_info:<16} | "
              f"{b['day']:<10} | {time_str:<13} | {b['student_count']:<5}")
    print(divider)

    print("\nOptions:")
    print("  1. Cancel a booking")
    print("  2. Filter bookings by Resource ID")
    print("  3. Filter bookings by Day")
    print("  4. Return to Main Menu")

    choice = input("Enter choice (1-4): ").strip()
    if choice == "1":
        bk_id = input("Enter Booking ID to cancel (e.g. BK201): ").strip().upper()
        found_idx = -1
        for idx, b in enumerate(bookings_list):
            if b.get("booking_id") == bk_id:
                found_idx = idx
                break

        if found_idx != -1:
            cancelled_booking = bookings_list.pop(found_idx)
            # Revert corresponding request status if found
            for req in requests_list:
                if req.get("request_id") == cancelled_booking.get("request_id"):
                    req["status"] = "PENDING"
                    req["allocated_resource_id"] = None
                    break

            storage.save_bookings(bookings_list)
            storage.save_requests(requests_list)
            print(f"[Success] Booking '{bk_id}' has been cancelled.")
        else:
            print(f"Booking ID '{bk_id}' not found.")
    elif choice == "2":
        r_id = input("Enter Resource ID (e.g. LAB01): ").strip().upper()
        filtered = [b for b in bookings_list if b.get("resource_id") == r_id]
        print(f"\nBookings for {r_id}: ({len(filtered)} found)")
        for b in filtered:
            print(f"  - {b['booking_id']}: {b['day']} {b['start_time']}-{b['end_time']} ({b['student_name']})")
    elif choice == "3":
        day_q = input("Enter Day (e.g. Monday): ").strip().capitalize()
        filtered = [b for b in bookings_list if b.get("day") == day_q]
        print(f"\nBookings on {day_q}: ({len(filtered)} found)")
        for b in filtered:
            print(f"  - {b['booking_id']}: {b['resource_name']} from {b['start_time']} to {b['end_time']} ({b['student_name']})")


def handle_conflict_audit(bookings_list):
    """Executes conflict detection algorithms across all bookings."""
    print_header("Conflict Detection & Schedule Audit")
    print("Scanning all bookings for potential scheduling collisions...")

    conflicts = conflict_manager.audit_all_bookings(bookings_list)

    if not conflicts:
        print("\n[OK] Audit Complete: 0 conflicts detected. All bookings are valid and conflict-free.")
    else:
        print(f"\n[ALERT] Found {len(conflicts)} conflict(s) in active schedule:")
        for idx, c in enumerate(conflicts, 1):
            _, _, reason = c
            print(f"  {idx}. {reason}")


def handle_analytics(resources_dict, requests_list, bookings_list):
    """Displays utilization statistics and metrics."""
    print(analytics.generate_analytics_report_text(resources_dict, requests_list, bookings_list))


def handle_manage_resources(resources_dict, bookings_list):
    """CRUD operations for resource inventory."""
    print_header("Resource Management")
    print("  1. Add New Resource")
    print("  2. Remove Resource")
    print("  3. View All Resources")
    print("  4. Return to Main Menu")

    choice = input("Enter choice (1-4): ").strip()
    if choice == "1":
        r_id = input("Enter Resource ID (e.g. LAB03): ").strip().upper()
        name = input("Enter Resource Name (e.g. Electronics Lab): ").strip()

        print(f"Select Type: {', '.join(RESOURCE_TYPES)}")
        r_type = input("Enter Resource Type: ").strip()

        cap_str = input("Enter Seating Capacity: ").strip()
        fac_str = input("Enter Facilities (comma-separated): ").strip()
        facilities = [f.strip() for f in fac_str.split(",") if f.strip()]

        # Collect at least one operating slot
        print("\nAdd Operating Slot for this resource:")
        day = input(f"Day ({', '.join(VALID_DAYS)}): ").strip()
        s_time = input("Start Time (HH:MM): ").strip()
        e_time = input("End Time (HH:MM): ").strip()

        slots = [(day.capitalize(), s_time, e_time)]

        ok, msg = resource_manager.add_resource(
            resources_dict, r_id, name, r_type, cap_str, facilities, slots
        )
        if ok:
            storage.save_resources(resources_dict)
            print(f"[Success] {msg}")
        else:
            print(f"[Error] {msg}")

    elif choice == "2":
        r_id = input("Enter Resource ID to remove: ").strip().upper()
        ok, msg = resource_manager.remove_resource(resources_dict, r_id, bookings_list)
        if ok:
            storage.save_resources(resources_dict)
            print(f"[Success] {msg}")
        else:
            print(f"[Error] {msg}")
    elif choice == "3":
        print(resource_manager.format_resource_table(list(resources_dict.values())))


# =========================================================
# MAIN DRIVER
# =========================================================

def main():
    """Application main entry point and event loop."""
    print("\nStarting CampusFlow...")

    # Load persistent datasets
    resources_dict = storage.load_resources()
    bookings_list = storage.load_bookings()
    requests_list = storage.load_requests()

    print(f"Loaded {len(resources_dict)} resources, {len(bookings_list)} bookings, and {len(requests_list)} requests.")

    while True:
        try:
            print_menu()
            choice = input("Enter your choice (1-8): ").strip()

            v, msg = validation.validate_menu_choice(choice, 1, 8)
            if not v:
                print(f"[Invalid Input] {msg}")
                continue

            choice_num = int(choice)

            if choice_num == 1:
                handle_submit_request(requests_list, resources_dict, bookings_list)
            elif choice_num == 2:
                handle_view_resources(resources_dict)
            elif choice_num == 3:
                handle_allocation_menu(requests_list, resources_dict, bookings_list)
            elif choice_num == 4:
                handle_view_bookings(bookings_list, requests_list)
            elif choice_num == 5:
                handle_conflict_audit(bookings_list)
            elif choice_num == 6:
                handle_analytics(resources_dict, requests_list, bookings_list)
            elif choice_num == 7:
                handle_manage_resources(resources_dict, bookings_list)
            elif choice_num == 8:
                print("\nSaving data and shutting down CampusFlow...")
                storage.save_resources(resources_dict)
                storage.save_bookings(bookings_list)
                storage.save_requests(requests_list)
                print("All records safely persisted. Goodbye!\n")
                sys.exit(0)

        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation interrupted by user. Exiting cleanly...")
            storage.save_resources(resources_dict)
            storage.save_bookings(bookings_list)
            storage.save_requests(requests_list)
            sys.exit(0)


if __name__ == "__main__":
    main()
