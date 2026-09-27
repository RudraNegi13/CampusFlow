"""
allocation_engine.py
--------------------
Core allocation algorithm engine for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Top-down algorithmic design and problem decomposition
- Filtering, matching, and candidate generation using loops and conditions
- Optimization heuristic: Best-Fit capacity selection (minimum wasted seats)
- Alternative slot search and recommendation algorithm
- Step-by-step rejection logging for transparency and viva defense
"""

from models import create_booking
from conflict_manager import (
    check_capacity_conflict,
    check_facility_conflict,
    check_resource_operating_availability,
    check_booking_conflict,
    detect_duplicate_student_booking,
    is_time_overlap
)


def generate_next_booking_id(bookings_list):
    """
    Generates a sequential booking ID (e.g. BK201, BK202, ...).
    Demonstrates max extraction and counting.
    """
    if not bookings_list:
        return "BK201"

    max_num = 200
    for b in bookings_list:
        b_id = b.get("booking_id", "")
        if b_id.startswith("BK") and b_id[2:].isdigit():
            num = int(b_id[2:])
            if num > max_num:
                max_num = num

    return f"BK{max_num + 1}"


def evaluate_candidate_resources(request_data, resources_dict, bookings_list):
    """
    Evaluates every resource in the system against the request requirements.
    
    Returns:
        candidates (list): List of resource dictionaries that satisfy ALL criteria.
        rejection_log (list of tuples): [(resource_id, resource_name, reason), ...]
    """
    candidates = []
    rejection_log = []

    req_type = request_data["resource_type"]
    req_cap = request_data["student_count"]
    req_day = request_data["day"]
    req_start = request_data["start_time"]
    req_end = request_data["end_time"]
    req_facs = request_data.get("facilities", [])
    req_student = request_data["student_id"]

    # First check: Does student already have an overlapping booking elsewhere?
    dup_conflict, dup_booking = detect_duplicate_student_booking(
        req_student, req_day, req_start, req_end, bookings_list
    )
    if dup_conflict:
        reason = (f"Student Schedule Conflict: Student {req_student} already has concurrent booking "
                  f"'{dup_booking['booking_id']}' in {dup_booking['resource_name']} "
                  f"({dup_booking['start_time']}-{dup_booking['end_time']}) on {req_day}.")
        rejection_log.append(("GLOBAL", "Student Schedule Conflict", reason))
        return [], rejection_log

    # Iterate through each resource and apply validation filters
    for res_id, resource in resources_dict.items():
        name = resource.get("name", res_id)

        # 1. Match Resource Type
        if resource.get("resource_type", "").lower() != req_type.lower():
            continue  # Silently skip unrelated types (e.g. asking for Lab won't test Seminar room)

        # 2. Check Capacity
        cap_ok, cap_msg = check_capacity_conflict(resource.get("capacity", 0), req_cap)
        if not cap_ok:
            rejection_log.append((res_id, name, f"Rejected -- {cap_msg}"))
            continue

        # 3. Check Facilities
        fac_ok, missing_facs = check_facility_conflict(resource.get("facilities", []), req_facs)
        if not fac_ok:
            missing_str = ", ".join(missing_facs)
            rejection_log.append((res_id, name, f"Rejected -- missing required facilities: {missing_str}."))
            continue

        # 4. Check Operating Availability on requested day & time
        open_ok, open_msg = check_resource_operating_availability(resource, req_day, req_start, req_end)
        if not open_ok:
            rejection_log.append((res_id, name, f"Rejected -- {open_msg}"))
            continue

        # 5. Check Booking Conflict (Is it already occupied?)
        booked, conflict_b = check_booking_conflict(res_id, req_day, req_start, req_end, bookings_list)
        if booked:
            rejection_log.append((
                res_id, name,
                f"Rejected -- already occupied by booking '{conflict_b['booking_id']}' "
                f"({conflict_b['start_time']}-{conflict_b['end_time']}) on {req_day}."
            ))
            continue

        # If all checks pass, resource is an acceptable candidate!
        candidates.append(resource)
        rejection_log.append((res_id, name, "Accepted -- all requirements satisfied."))

    return candidates, rejection_log


def select_best_candidate(candidates, requested_student_count):
    """
    Selects the optimal resource from candidate resources using the Best-Fit strategy.
    
    Objective:
        Minimize wasted seats: min(capacity - requested_student_count)
        
    Demonstrates:
        Minimum finding algorithm using linear iteration.
    """
    if not candidates:
        return None

    best_candidate = None
    min_waste = float("inf")

    for cand in candidates:
        waste = cand.get("capacity", 0) - requested_student_count
        if waste < min_waste:
            min_waste = waste
            best_candidate = cand

    return best_candidate


def search_alternative_slots(request_data, resources_dict, bookings_list, max_alternatives=4):
    """
    Searches for alternative time slots when the exact requested slot cannot be fulfilled.
    
    Strategy:
    1. Look for matching resources (type, capacity, facilities) on the SAME DAY at other operating slots.
    2. Look for matching resources on OTHER DAYS at their operating slots.
    3. Verify that the alternative slot is NOT currently booked.
    
    Returns:
        list of dicts: Alternative recommendation options.
    """
    alternatives = []
    req_type = request_data["resource_type"]
    req_cap = request_data["student_count"]
    req_day = request_data["day"]
    req_facs = request_data.get("facilities", [])
    
    # Filter resources that have appropriate type, capacity, and facilities
    suitable_resources = []
    for res_id, res in resources_dict.items():
        if res.get("resource_type", "").lower() != req_type.lower():
            continue
        if res.get("capacity", 0) < req_cap:
            continue
        fac_ok, _ = check_facility_conflict(res.get("facilities", []), req_facs)
        if not fac_ok:
            continue
        suitable_resources.append(res)

    # 1. Search Same Day Alternative Slots
    for res in suitable_resources:
        res_id = res["resource_id"]
        for slot in res.get("available_slots", []):
            s_day, s_start, s_end = slot
            if s_day.lower() == req_day.lower():
                # Check if this slot has a conflict with existing bookings
                has_conflict, _ = check_booking_conflict(res_id, s_day, s_start, s_end, bookings_list)
                if not has_conflict:
                    alt = {
                        "resource_id": res_id,
                        "resource_name": res["name"],
                        "day": s_day,
                        "start_time": s_start,
                        "end_time": s_end,
                        "reason": f"Same day alternative on {s_day}"
                    }
                    if alt not in alternatives:
                        alternatives.append(alt)
                        if len(alternatives) >= max_alternatives:
                            return alternatives

    # 2. Search Other Days Alternative Slots
    for res in suitable_resources:
        res_id = res["resource_id"]
        for slot in res.get("available_slots", []):
            s_day, s_start, s_end = slot
            if s_day.lower() != req_day.lower():
                has_conflict, _ = check_booking_conflict(res_id, s_day, s_start, s_end, bookings_list)
                if not has_conflict:
                    alt = {
                        "resource_id": res_id,
                        "resource_name": res["name"],
                        "day": s_day,
                        "start_time": s_start,
                        "end_time": s_end,
                        "reason": f"Different day opening on {s_day}"
                    }
                    if alt not in alternatives:
                        alternatives.append(alt)
                        if len(alternatives) >= max_alternatives:
                            return alternatives

    return alternatives


def process_allocation_request(request_data, resources_dict, bookings_list):
    """
    Main algorithmic entry point for allocating a space request.
    
    Workflow:
    1. Evaluate candidate resources and record rejection reasons.
    2. If candidates exist:
       - Select best candidate using Best-Fit.
       - Create new booking record.
       - Append booking to bookings_list.
       - Update request status to 'ALLOCATED'.
       - Return (True, booking, rejection_log, [])
    3. If no candidate found:
       - Update request status to 'FAILED'.
       - Search for alternative slots.
       - Return (False, None, rejection_log, alternatives)
    """
    candidates, rejection_log = evaluate_candidate_resources(request_data, resources_dict, bookings_list)

    if candidates:
        chosen_resource = select_best_candidate(candidates, request_data["student_count"])
        booking_id = generate_next_booking_id(bookings_list)
        new_booking = create_booking(booking_id, request_data, chosen_resource)
        bookings_list.append(new_booking)

        request_data["status"] = "ALLOCATED"
        request_data["allocated_resource_id"] = chosen_resource["resource_id"]

        return True, new_booking, rejection_log, []
    else:
        request_data["status"] = "FAILED"
        alternatives = search_alternative_slots(request_data, resources_dict, bookings_list)
        return False, None, rejection_log, alternatives
