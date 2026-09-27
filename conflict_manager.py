"""
conflict_manager.py
-------------------
Conflict detection and validation algorithms for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Time arithmetic conversion (HH:MM to integer minutes)
- Interval overlap checking algorithm
- Set difference operations for missing facilities
- Loop-based searching for duplicate and overlapping bookings
- Clear and explanatory conflict diagnostics
"""


def time_to_minutes(time_str):
    """
    Converts a 24-hour time string 'HH:MM' into total minutes since midnight.
    Example: '14:30' -> 14 * 60 + 30 = 870 minutes.
    
    Time Complexity: O(1)
    """
    parts = str(time_str).strip().split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    return hours * 60 + minutes


def minutes_to_time(minutes):
    """
    Converts total minutes from midnight back to 'HH:MM' 24-hour format string.
    Example: 870 -> '14:30'.
    
    Time Complexity: O(1)
    """
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def is_time_overlap(start1, end1, start2, end2):
    """
    Determines whether two time intervals [start1, end1) and [start2, end2) overlap.
    
    Mathematical Condition:
    Two intervals overlap if and only if:
        start1 < end2 AND start2 < end1
        
    Time Complexity: O(1)
    """
    s1 = time_to_minutes(start1)
    e1 = time_to_minutes(end1)
    s2 = time_to_minutes(start2)
    e2 = time_to_minutes(end2)

    return (s1 < e2) and (s2 < e1)


def is_slot_within_window(req_start, req_end, window_start, window_end):
    """
    Checks if a requested slot [req_start, req_end] is completely contained
    within an operating availability window [window_start, window_end].
    
    Condition:
        window_start <= req_start AND req_end <= window_end
    """
    r_s = time_to_minutes(req_start)
    r_e = time_to_minutes(req_end)
    w_s = time_to_minutes(window_start)
    w_e = time_to_minutes(window_end)

    return (w_s <= r_s) and (r_e <= w_e)


def check_resource_operating_availability(resource, day, start_time, end_time):
    """
    Checks if the resource is scheduled to be open during the requested day and time.
    
    Parameters:
        resource (dict): The resource dictionary
        day (str): Requested day (e.g. 'Monday')
        start_time (str): Requested start ('HH:MM')
        end_time (str): Requested end ('HH:MM')
        
    Returns:
        (bool, str): (True, "") if resource is open, (False, reason) otherwise.
    """
    available_slots = resource.get("available_slots", [])
    if not available_slots:
        return False, f"Resource '{resource['name']}' has no defined operational hours."

    day_matched = False
    for slot in available_slots:
        slot_day, slot_start, slot_end = slot
        if slot_day.strip().lower() == day.strip().lower():
            day_matched = True
            if is_slot_within_window(start_time, end_time, slot_start, slot_end):
                return True, ""

    if not day_matched:
        return False, f"Resource '{resource['name']}' is not open on {day}."
    else:
        return False, (f"Resource '{resource['name']}' is open on {day}, but the requested time "
                      f"{start_time}-{end_time} falls outside its operating hours.")


def check_booking_conflict(resource_id, day, start_time, end_time, existing_bookings):
    """
    Searches existing bookings for any scheduling collision on the same resource and day.
    
    Demonstrates:
    - Linear search through bookings list
    - Conditional filtering by resource_id and day
    - Time overlap comparison
    
    Returns:
        (bool, dict or None): (True, conflicting_booking) or (False, None)
    """
    res_id_clean = resource_id.strip().upper()
    day_clean = day.strip().lower()

    for booking in existing_bookings:
        if booking.get("resource_id", "").strip().upper() == res_id_clean:
            if booking.get("day", "").strip().lower() == day_clean:
                b_start = booking.get("start_time")
                b_end = booking.get("end_time")
                if is_time_overlap(start_time, end_time, b_start, b_end):
                    return True, booking

    return False, None


def detect_duplicate_student_booking(student_id, day, start_time, end_time, existing_bookings):
    """
    Detects if the same student has already booked another resource at an overlapping time.
    Prevents a student from holding concurrent bookings.
    
    Returns:
        (bool, dict or None): (True, conflicting_booking) or (False, None)
    """
    stu_id_clean = student_id.strip().upper()
    day_clean = day.strip().lower()

    for booking in existing_bookings:
        if booking.get("student_id", "").strip().upper() == stu_id_clean:
            if booking.get("day", "").strip().lower() == day_clean:
                b_start = booking.get("start_time")
                b_end = booking.get("end_time")
                if is_time_overlap(start_time, end_time, b_start, b_end):
                    return True, booking

    return False, None


def check_capacity_conflict(resource_capacity, student_count):
    """
    Checks if a resource has sufficient seats for the requested student group.
    
    Returns:
        (bool, str): (True, "") if sufficient, (False, reason) if insufficient.
    """
    if resource_capacity < student_count:
        deficit = student_count - resource_capacity
        return False, (f"Insufficient capacity: Resource has {resource_capacity} seats, "
                      f"which is {deficit} seat(s) short of the required {student_count}.")
    return True, ""


def check_facility_conflict(resource_facilities, required_facilities):
    """
    Compares required facilities against resource facilities using set operations.
    
    Demonstrates:
    - Set difference to identify missing elements
    
    Returns:
        (bool, list): (True, []) if all required facilities exist, (False, missing_list) otherwise.
    """
    res_set = set(resource_facilities)
    req_set = set(required_facilities)
    missing = req_set - res_set

    if len(missing) > 0:
        return False, sorted(list(missing))
    return True, []


def audit_all_bookings(bookings):
    """
    Audits a list of bookings to detect any overlapping conflicts between bookings.
    Demonstrates nested loop pairwise comparison with duplicate prevention.
    
    Returns:
        list of tuples: [(booking_A, booking_B, reason), ...]
    """
    conflicts = []
    n = len(bookings)

    for i in range(n):
        for j in range(i + 1, n):
            b1 = bookings[i]
            b2 = bookings[j]

            # Case 1: Same resource booked at overlapping time on same day
            if (b1.get("resource_id") == b2.get("resource_id") and
                b1.get("day", "").lower() == b2.get("day", "").lower()):
                if is_time_overlap(b1["start_time"], b1["end_time"], b2["start_time"], b2["end_time"]):
                    conflicts.append((
                        b1, b2,
                        f"Resource Double-Booking: Resource {b1['resource_id']} is overlapping "
                        f"between {b1['booking_id']} ({b1['start_time']}-{b1['end_time']}) "
                        f"and {b2['booking_id']} ({b2['start_time']}-{b2['end_time']}) on {b1['day']}."
                    ))

            # Case 2: Same student booked at overlapping time in different rooms
            if (b1.get("student_id") == b2.get("student_id") and
                b1.get("day", "").lower() == b2.get("day", "").lower()):
                if is_time_overlap(b1["start_time"], b1["end_time"], b2["start_time"], b2["end_time"]):
                    conflicts.append((
                        b1, b2,
                        f"Student Schedule Collision: Student {b1['student_id']} ({b1['student_name']}) "
                        f"has concurrent bookings {b1['booking_id']} in {b1['resource_id']} and "
                        f"{b2['booking_id']} in {b2['resource_id']} on {b1['day']}."
                    ))

    return conflicts
