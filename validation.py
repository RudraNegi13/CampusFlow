"""
validation.py
-------------
Input validation module for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- String operations and checks (strip, split, isdigit)
- Conditional statements and range checking
- Meaningful error reporting via (is_valid, error_message) tuples
- Defending against invalid inputs before processing
"""

from models import RESOURCE_TYPES, VALID_DAYS


def validate_non_empty(value, field_name="Field"):
    """
    Validates that a string value is not empty or composed solely of whitespace.
    """
    if value is None or str(value).strip() == "":
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_positive_integer(value, field_name="Value"):
    """
    Validates that a value can be converted to an integer strictly greater than zero.
    Detects zero and negative numbers.
    """
    # Check if empty
    is_valid, msg = validate_non_empty(value, field_name)
    if not is_valid:
        return False, msg

    try:
        val_int = int(value)
        if val_int <= 0:
            return False, f"{field_name} must be a positive integer greater than zero (received {val_int})."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid integer number."


def validate_menu_choice(choice_str, min_choice, max_choice):
    """
    Validates an interactive menu selection against a range [min_choice, max_choice].
    """
    is_valid, msg = validate_non_empty(choice_str, "Menu choice")
    if not is_valid:
        return False, msg

    try:
        choice_int = int(choice_str)
        if choice_int < min_choice or choice_int > max_choice:
            return False, f"Choice must be between {min_choice} and {max_choice}."
        return True, ""
    except ValueError:
        return False, "Invalid input. Please enter a valid number."


def validate_time_format(time_str, field_name="Time"):
    """
    Validates that a time string follows 24-hour 'HH:MM' format.
    Checks:
    - 2 parts separated by ':'
    - Hours between 00 and 23
    - Minutes between 00 and 59
    """
    is_valid, msg = validate_non_empty(time_str, field_name)
    if not is_valid:
        return False, msg

    parts = str(time_str).strip().split(":")
    if len(parts) != 2:
        return False, f"{field_name} must be formatted as HH:MM (e.g., 09:00 or 14:30)."

    h_str, m_str = parts[0], parts[1]
    if not (h_str.isdigit() and m_str.isdigit() and len(h_str) in (1, 2) and len(m_str) == 2):
        return False, f"{field_name} components must be numeric (HH:MM)."

    hours = int(h_str)
    minutes = int(m_str)

    if hours < 0 or hours > 23:
        return False, f"{field_name} hour must be between 0 and 23."
    if minutes < 0 or minutes > 59:
        return False, f"{field_name} minute must be between 0 and 59."

    return True, ""


def validate_time_range(start_time, end_time):
    """
    Validates that both start_time and end_time are valid format,
    and start_time is strictly earlier than end_time.
    """
    valid_start, msg_start = validate_time_format(start_time, "Start time")
    if not valid_start:
        return False, msg_start

    valid_end, msg_end = validate_time_format(end_time, "End time")
    if not valid_end:
        return False, msg_end

    s_hours, s_mins = map(int, start_time.split(":"))
    e_hours, e_mins = map(int, end_time.split(":"))

    start_total_mins = s_hours * 60 + s_mins
    end_total_mins = e_hours * 60 + e_mins

    if start_total_mins >= end_total_mins:
        return False, f"Start time ({start_time}) must be earlier than end time ({end_time})."

    return True, ""


def validate_day(day_str):
    """
    Validates that day matches one of the operational days (case-insensitive).
    """
    is_valid, msg = validate_non_empty(day_str, "Day")
    if not is_valid:
        return False, msg

    cleaned_day = str(day_str).strip().capitalize()
    if cleaned_day not in VALID_DAYS:
        valid_days_str = ", ".join(VALID_DAYS)
        return False, f"Invalid day '{day_str}'. Valid days are: {valid_days_str}."

    return True, ""


def validate_resource_type(resource_type):
    """
    Validates that resource_type is one of the valid RESOURCE_TYPES.
    """
    is_valid, msg = validate_non_empty(resource_type, "Resource type")
    if not is_valid:
        return False, msg

    cleaned_type = str(resource_type).strip()
    # Case-insensitive comparison against valid options
    matched = False
    for valid_type in RESOURCE_TYPES:
        if valid_type.lower() == cleaned_type.lower():
            matched = True
            break

    if not matched:
        types_str = ", ".join(RESOURCE_TYPES)
        return False, f"Invalid resource type '{resource_type}'. Valid types are: {types_str}."

    return True, ""


def validate_resource_data(resource_id, name, res_type, capacity, facilities, existing_ids=None):
    """
    Comprehensive validation for resource creation/updating.
    """
    # 1. ID check
    valid_id, msg_id = validate_non_empty(resource_id, "Resource ID")
    if not valid_id:
        return False, msg_id

    if existing_ids and resource_id.strip().upper() in [x.upper() for x in existing_ids]:
        return False, f"Resource ID '{resource_id.strip().upper()}' already exists."

    # 2. Name check
    valid_name, msg_name = validate_non_empty(name, "Resource name")
    if not valid_name:
        return False, msg_name

    # 3. Type check
    valid_type, msg_type = validate_resource_type(res_type)
    if not valid_type:
        return False, msg_type

    # 4. Capacity check
    valid_cap, msg_cap = validate_positive_integer(capacity, "Capacity")
    if not valid_cap:
        return False, msg_cap

    # 5. Facilities check
    if not isinstance(facilities, (list, set, tuple)):
        return False, "Facilities must be a list of facility names."

    return True, ""


def validate_request_data(student_id, student_name, res_type, student_count,
                          day, start_time, end_time):
    """
    Comprehensive validation for student space requests.
    """
    # Student ID & Name
    v, msg = validate_non_empty(student_id, "Student ID")
    if not v:
        return False, msg

    v, msg = validate_non_empty(student_name, "Student Name")
    if not v:
        return False, msg

    # Resource type
    v, msg = validate_resource_type(res_type)
    if not v:
        return False, msg

    # Student count
    v, msg = validate_positive_integer(student_count, "Student Count")
    if not v:
        return False, msg

    # Day
    v, msg = validate_day(day)
    if not v:
        return False, msg

    # Time range
    v, msg = validate_time_range(start_time, end_time)
    if not v:
        return False, msg

    return True, ""
