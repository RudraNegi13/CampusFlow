"""
request_manager.py
------------------
Student request handling and tracking for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- List operations (append, iteration, filtering)
- Sequential ID generation using counting
- Searching requests by ID or student ID
- State tracking and status mutation
"""

from models import create_request
from validation import validate_request_data


def generate_next_request_id(requests_list):
    """
    Generates a new sequential request ID (e.g. REQ101, REQ102, ...).
    
    Demonstrates:
    - Counting and maximum ID extraction
    - String manipulation and integer parsing
    """
    if not requests_list:
        return "REQ101"

    max_num = 100
    for req in requests_list:
        req_id = req.get("request_id", "")
        if req_id.startswith("REQ") and req_id[3:].isdigit():
            num = int(req_id[3:])
            if num > max_num:
                max_num = num

    return f"REQ{max_num + 1}"


def submit_request(requests_list, student_id, student_name, resource_type,
                   student_count, day, start_time, end_time, facilities=None):
    """
    Validates and appends a new student request to requests_list.
    
    Returns:
        (bool, dict or str): (True, request_dict) or (False, error_message)
    """
    is_valid, error_msg = validate_request_data(
        student_id, student_name, resource_type, student_count, day, start_time, end_time
    )
    if not is_valid:
        return False, error_msg

    req_id = generate_next_request_id(requests_list)
    new_request = create_request(
        request_id=req_id,
        student_id=student_id,
        student_name=student_name,
        resource_type=resource_type,
        student_count=student_count,
        day=day,
        start_time=start_time,
        end_time=end_time,
        facilities=facilities if facilities else []
    )

    requests_list.append(new_request)
    return True, new_request


def get_request_by_id(requests_list, request_id):
    """
    Finds a request by ID using linear search.
    
    Time Complexity: O(N)
    """
    clean_id = str(request_id).strip().upper()
    for req in requests_list:
        if req.get("request_id", "").strip().upper() == clean_id:
            return req
    return None


def get_pending_requests(requests_list):
    """
    Filters and returns all requests with status 'PENDING'.
    
    Demonstrates:
    - Filtering a list using a for loop and conditional
    """
    pending = []
    for req in requests_list:
        if req.get("status") == "PENDING":
            pending.append(req)
    return pending


def get_requests_by_student(requests_list, student_id):
    """
    Finds all requests made by a specific student ID.
    """
    clean_sid = str(student_id).strip().upper()
    student_requests = []
    for req in requests_list:
        if req.get("student_id", "").strip().upper() == clean_sid:
            student_requests.append(req)
    return student_requests


def update_request_status(requests_list, request_id, new_status, allocated_resource_id=None):
    """
    Updates the status of a request (PENDING -> ALLOCATED or FAILED).
    """
    req = get_request_by_id(requests_list, request_id)
    if not req:
        return False, f"Request {request_id} not found."

    req["status"] = new_status
    if allocated_resource_id:
        req["allocated_resource_id"] = allocated_resource_id
    return True, "Status updated."


def format_request_summary(req):
    """
    Formats a single request into a clean human-readable summary string.
    """
    facs = ", ".join(req.get("facilities", [])) if req.get("facilities") else "None"
    return (
        f"Request [{req.get('request_id')}] - Status: {req.get('status')}\n"
        f"  Student: {req.get('student_name')} ({req.get('student_id')})\n"
        f"  Requirement: {req.get('resource_type')} for {req.get('student_count')} students\n"
        f"  Time: {req.get('day')} from {req.get('start_time')} to {req.get('end_time')}\n"
        f"  Facilities: {facs}"
    )
