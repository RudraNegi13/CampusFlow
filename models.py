"""
models.py
---------
Core data models and helper constructors for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Dictionaries and Lists for entity representation
- Tuples for fixed time slot structures: (day, start_time, end_time)
- Sets for unique facilities and types
- Data constructors with clear parameter lists
"""

# Tuple of valid standard resource types
RESOURCE_TYPES = (
    "Computer Lab",
    "Study Room",
    "Discussion Room",
    "Project Room",
    "Seminar Room"
)

# Tuple of standard operating days
VALID_DAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
)

# Set of standard campus facilities
STANDARD_FACILITIES = {
    "Computers",
    "Projector",
    "Whiteboard",
    "AC",
    "Internet",
    "Audio System"
}


def create_resource(resource_id, name, resource_type, capacity, facilities, available_slots):
    """
    Constructs and returns a resource dictionary.
    
    Parameters:
        resource_id (str): Unique identifier e.g., 'LAB01'
        name (str): Display name e.g., 'Computer Lab 1'
        resource_type (str): Type of resource from RESOURCE_TYPES
        capacity (int): Maximum student capacity (positive integer)
        facilities (list): List of facility strings e.g., ['Computers', 'Projector']
        available_slots (list of tuples): List of (day, start_time, end_time)
        
    Returns:
        dict: Standardized resource dictionary
    """
    # Convert facilities to a sorted list of unique entries using set
    unique_facilities = sorted(list(set(facilities)))
    
    # Standardize available slots as a list of tuples
    formatted_slots = []
    for slot in available_slots:
        if isinstance(slot, (list, tuple)) and len(slot) == 3:
            formatted_slots.append((str(slot[0]), str(slot[1]), str(slot[2])))

    return {
        "resource_id": str(resource_id).strip().upper(),
        "name": str(name).strip(),
        "resource_type": str(resource_type).strip(),
        "capacity": int(capacity),
        "facilities": unique_facilities,
        "available_slots": formatted_slots
    }


def create_request(request_id, student_id, student_name, resource_type,
                   student_count, day, start_time, end_time, facilities, status="PENDING"):
    """
    Constructs and returns a student space request dictionary.
    
    Parameters:
        request_id (str): Unique request identifier e.g., 'REQ101'
        student_id (str): Student ID e.g., 'STU2026'
        student_name (str): Full name of student
        resource_type (str): Requested resource type
        student_count (int): Number of students
        day (str): Preferred day e.g., 'Monday'
        start_time (str): Start time in 'HH:MM' 24-hr format
        end_time (str): End time in 'HH:MM' 24-hr format
        facilities (list): List of required facility strings
        status (str): Current status ('PENDING', 'ALLOCATED', 'FAILED')
        
    Returns:
        dict: Standardized request dictionary
    """
    unique_facilities = sorted(list(set(facilities))) if facilities else []
    
    return {
        "request_id": str(request_id).strip().upper(),
        "student_id": str(student_id).strip().upper(),
        "student_name": str(student_name).strip(),
        "resource_type": str(resource_type).strip(),
        "student_count": int(student_count),
        "day": str(day).strip().capitalize(),
        "start_time": str(start_time).strip(),
        "end_time": str(end_time).strip(),
        "facilities": unique_facilities,
        "status": status,
        "allocated_resource_id": None
    }


def create_booking(booking_id, request_data, resource_data):
    """
    Constructs a confirmed booking dictionary by binding a request to an allocated resource.
    
    Parameters:
        booking_id (str): Unique booking identifier e.g., 'BK201'
        request_data (dict): The student request being fulfilled
        resource_data (dict): The resource allocated
        
    Returns:
        dict: Confirmed booking dictionary
    """
    return {
        "booking_id": str(booking_id).strip().upper(),
        "request_id": request_data["request_id"],
        "student_id": request_data["student_id"],
        "student_name": request_data["student_name"],
        "resource_id": resource_data["resource_id"],
        "resource_name": resource_data["name"],
        "resource_type": resource_data["resource_type"],
        "day": request_data["day"],
        "start_time": request_data["start_time"],
        "end_time": request_data["end_time"],
        "student_count": request_data["student_count"],
        "facilities_used": list(request_data["facilities"])
    }
