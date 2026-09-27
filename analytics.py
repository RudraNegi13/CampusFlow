"""
analytics.py
------------
Resource utilization and allocation analytics for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Foundational counting algorithms using loops
- Summation algorithms (accumulators)
- Maximum and Minimum finding algorithms with explicit tracking variables
- Frequency distribution using dictionaries
- Mathematical percentage and ratio calculations
- Terminal dashboard report formatting
"""

from conflict_manager import time_to_minutes


def count_summary_totals(resources_dict, requests_list, bookings_list):
    """
    Computes summary counts of resources, requests, and bookings.
    
    Demonstrates:
    - Counting algorithm with conditional accumulator variables
    """
    total_resources = len(resources_dict)
    total_requests = len(requests_list)
    total_bookings = len(bookings_list)

    successful_allocations = 0
    failed_allocations = 0
    pending_allocations = 0

    for req in requests_list:
        status = req.get("status", "").upper()
        if status == "ALLOCATED":
            successful_allocations += 1
        elif status == "FAILED":
            failed_allocations += 1
        else:
            pending_allocations += 1

    return {
        "total_resources": total_resources,
        "total_requests": total_requests,
        "total_bookings": total_bookings,
        "successful_allocations": successful_allocations,
        "failed_allocations": failed_allocations,
        "pending_allocations": pending_allocations
    }


def calculate_allocation_success_rate(requests_list):
    """
    Calculates the percentage of requests successfully satisfied.
    Formula: (successful / total_requests) * 100
    """
    if not requests_list:
        return 0.0

    successful = 0
    for req in requests_list:
        if req.get("status") == "ALLOCATED":
            successful += 1

    rate = (successful / len(requests_list)) * 100.0
    return round(rate, 2)


def find_most_and_least_used_resources(resources_dict, bookings_list):
    """
    Identifies the most frequently booked and least frequently booked resources.
    
    Demonstrates:
    - Frequency counting using a dictionary
    - Explicit Maximum and Minimum tracking algorithms
    
    Returns:
        tuple: (most_used_tuple, least_used_tuple)
        where each tuple is (resource_id, resource_name, booking_count)
    """
    if not resources_dict:
        return None, None

    # Step 1: Initialize usage count dictionary for all registered resources to 0
    usage_counts = {}
    for res_id in resources_dict.keys():
        usage_counts[res_id] = 0

    # Step 2: Accumulate counts from confirmed bookings
    for booking in bookings_list:
        res_id = booking.get("resource_id")
        if res_id in usage_counts:
            usage_counts[res_id] += 1
        else:
            usage_counts[res_id] = 1

    # Step 3: Find Maximum and Minimum using classic comparison algorithm
    max_count = -1
    most_used_id = None

    min_count = 99999999
    least_used_id = None

    for res_id, count in usage_counts.items():
        # Check for maximum
        if count > max_count:
            max_count = count
            most_used_id = res_id

        # Check for minimum
        if count < min_count:
            min_count = count
            least_used_id = res_id

    most_res_name = resources_dict.get(most_used_id, {}).get("name", most_used_id) if most_used_id else "N/A"
    least_res_name = resources_dict.get(least_used_id, {}).get("name", least_used_id) if least_used_id else "N/A"

    most_tuple = (most_used_id, most_res_name, max_count)
    least_tuple = (least_used_id, least_res_name, min_count)

    return most_tuple, least_tuple


def find_busiest_day(bookings_list):
    """
    Finds the day of the week with the highest booking count.
    
    Demonstrates:
    - Frequency mapping
    - Max finding
    """
    if not bookings_list:
        return "N/A", 0

    day_counts = {}
    for b in bookings_list:
        d = b.get("day", "Unknown")
        day_counts[d] = day_counts.get(d, 0) + 1

    busiest_day = None
    max_count = -1

    for day, count in day_counts.items():
        if count > max_count:
            max_count = count
            busiest_day = day

    return busiest_day, max_count


def find_busiest_time_slot(bookings_list):
    """
    Finds the most popular time window requested across bookings.
    """
    if not bookings_list:
        return "N/A", 0

    slot_counts = {}
    for b in bookings_list:
        slot_label = f"{b.get('start_time')} - {b.get('end_time')}"
        slot_counts[slot_label] = slot_counts.get(slot_label, 0) + 1

    busiest_slot = None
    max_count = -1

    for slot, count in slot_counts.items():
        if count > max_count:
            max_count = count
            busiest_slot = slot

    return busiest_slot, max_count


def calculate_resource_utilization_percentage(resources_dict, bookings_list):
    """
    Calculates total hours booked vs total operational hours offered by all resources.
    
    Demonstrates:
    - Summation accumulator for duration in hours
    - Ratio calculation
    """
    if not resources_dict:
        return 0.0

    # Sum total weekly available hours from available_slots across all resources
    total_available_minutes = 0
    for res in resources_dict.values():
        for slot in res.get("available_slots", []):
            _, start, end = slot
            duration = time_to_minutes(end) - time_to_minutes(start)
            if duration > 0:
                total_available_minutes += duration

    if total_available_minutes == 0:
        return 0.0

    # Sum total booked minutes
    total_booked_minutes = 0
    for b in bookings_list:
        duration = time_to_minutes(b["end_time"]) - time_to_minutes(b["start_time"])
        if duration > 0:
            total_booked_minutes += duration

    utilization_rate = (total_booked_minutes / total_available_minutes) * 100.0
    return round(utilization_rate, 2)


def calculate_capacity_efficiency(bookings_list, resources_dict):
    """
    Calculates capacity efficiency:
    Formula: (Sum of seated students / Sum of maximum capacity of booked rooms) * 100
    
    Demonstrates:
    - Dual summation accumulators
    - Average resource packing efficiency
    """
    if not bookings_list:
        return 0.0

    total_students_seated = 0
    total_capacity_allocated = 0

    for b in bookings_list:
        total_students_seated += b.get("student_count", 0)
        res = resources_dict.get(b.get("resource_id"))
        if res:
            total_capacity_allocated += res.get("capacity", 0)
        else:
            total_capacity_allocated += b.get("student_count", 0)

    if total_capacity_allocated == 0:
        return 0.0

    efficiency = (total_students_seated / total_capacity_allocated) * 100.0
    return round(efficiency, 2)


def generate_analytics_report_text(resources_dict, requests_list, bookings_list):
    """
    Formats the complete analytics report into a readable dashboard string.
    """
    counts = count_summary_totals(resources_dict, requests_list, bookings_list)
    success_rate = calculate_allocation_success_rate(requests_list)
    most_used, least_used = find_most_and_least_used_resources(resources_dict, bookings_list)
    busiest_day, day_bookings = find_busiest_day(bookings_list)
    busiest_slot, slot_bookings = find_busiest_time_slot(bookings_list)
    utilization = calculate_resource_utilization_percentage(resources_dict, bookings_list)
    efficiency = calculate_capacity_efficiency(bookings_list, resources_dict)

    lines = [
        "==================================================",
        "          CAMPUSFLOW UTILIZATION ANALYTICS        ",
        "==================================================",
        f"  Total Resources Registered : {counts['total_resources']}",
        f"  Total Requests Submitted  : {counts['total_requests']}",
        f"  Successful Allocations    : {counts['successful_allocations']}",
        f"  Failed Allocations        : {counts['failed_allocations']}",
        f"  Pending Requests          : {counts['pending_allocations']}",
        f"  Allocation Success Rate   : {success_rate}%",
        "--------------------------------------------------",
        "  RESOURCE USAGE METRICS:",
        f"  Most-Used Resource        : {most_used[1]} ({most_used[0]}) - {most_used[2]} booking(s)" if most_used else "  Most-Used Resource: N/A",
        f"  Least-Used Resource       : {least_used[1]} ({least_used[0]}) - {least_used[2]} booking(s)" if least_used else "  Least-Used Resource: N/A",
        f"  Busiest Day of the Week   : {busiest_day} ({day_bookings} booking(s))",
        f"  Busiest Time Window       : {busiest_slot} ({slot_bookings} booking(s))",
        "--------------------------------------------------",
        "  EFFICIENCY & UTILIZATION:",
        f"  Resource Time Utilization : {utilization}% of operational hours booked",
        f"  Seat Packing Efficiency   : {efficiency}% seats filled during bookings",
        "=================================================="
    ]
    return "\n".join(lines)
