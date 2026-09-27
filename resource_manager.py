"""
resource_manager.py
-------------------
Resource inventory management for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- Dictionaries as associative key-value stores for resources
- List filtering and iterative searching (linear search)
- Set accumulation for unique attributes
- String formatting for clear console presentation
- Input validation prior to database modification
"""

from models import create_resource
from validation import validate_resource_data


def add_resource(resources_dict, resource_id, name, res_type, capacity, facilities, available_slots):
    """
    Validates and inserts a new resource into the resources dictionary.
    
    Demonstrates:
    - Input validation
    - Dictionary insertion: resources_dict[key] = value
    
    Returns:
        (bool, str): (True, "Success message") or (False, "Error message")
    """
    existing_ids = list(resources_dict.keys())
    is_valid, error_msg = validate_resource_data(
        resource_id, name, res_type, capacity, facilities, existing_ids=existing_ids
    )
    if not is_valid:
        return False, error_msg

    res_obj = create_resource(resource_id, name, res_type, capacity, facilities, available_slots)
    clean_id = res_obj["resource_id"]
    resources_dict[clean_id] = res_obj
    return True, f"Resource '{clean_id} - {name}' added successfully."


def get_resource_by_id(resources_dict, resource_id):
    """
    Retrieves a single resource dictionary by its unique ID.
    Performs case-insensitive lookup.
    
    Time Complexity: O(1) average lookup or O(N) case-insensitive search.
    """
    if not resource_id:
        return None
    target_id = resource_id.strip().upper()
    return resources_dict.get(target_id, None)


def search_resources(resources_dict, res_type=None, min_capacity=None, required_facility=None):
    """
    Filters resources based on optional search criteria.
    
    Demonstrates:
    - Linear search through list of dictionary values
    - Filtering using multiple logical conditions (AND logic)
    - Set containment check for facilities
    
    Returns:
        list: Matching resource dictionaries
    """
    results = []
    
    for res_id, res in resources_dict.items():
        # Condition 1: Check resource type
        if res_type and res_type.strip() != "":
            if res.get("resource_type", "").lower() != res_type.strip().lower():
                continue

        # Condition 2: Check minimum capacity
        if min_capacity is not None and min_capacity > 0:
            if res.get("capacity", 0) < min_capacity:
                continue

        # Condition 3: Check required facility
        if required_facility and required_facility.strip() != "":
            fac_set = {f.lower() for f in res.get("facilities", [])}
            if required_facility.strip().lower() not in fac_set:
                continue

        # All specified filters passed
        results.append(res)

    return results


def update_resource(resources_dict, resource_id, name=None, res_type=None,
                    capacity=None, facilities=None, available_slots=None):
    """
    Updates attributes of an existing resource.
    
    Returns:
        (bool, str): Status and message.
    """
    res = get_resource_by_id(resources_dict, resource_id)
    if not res:
        return False, f"Resource '{resource_id}' does not exist."

    if name is not None and str(name).strip() != "":
        res["name"] = str(name).strip()

    if res_type is not None and str(res_type).strip() != "":
        res["resource_type"] = str(res_type).strip()

    if capacity is not None and int(capacity) > 0:
        res["capacity"] = int(capacity)

    if facilities is not None and isinstance(facilities, (list, set)):
        res["facilities"] = sorted(list(set(facilities)))

    if available_slots is not None and isinstance(available_slots, list):
        res["available_slots"] = available_slots

    return True, f"Resource '{resource_id.upper()}' updated successfully."


def remove_resource(resources_dict, resource_id, existing_bookings=None):
    """
    Removes a resource from the dictionary if safe.
    Checks if active bookings exist for this resource to prevent orphaned bookings.
    
    Demonstrates:
    - Referential integrity check using a loop
    - Dictionary item removal with del
    
    Returns:
        (bool, str): Status and message.
    """
    clean_id = resource_id.strip().upper()
    if clean_id not in resources_dict:
        return False, f"Resource '{clean_id}' not found."

    if existing_bookings:
        for b in existing_bookings:
            if b.get("resource_id", "").strip().upper() == clean_id:
                return False, (f"Cannot delete resource '{clean_id}' because it has active booking "
                              f"'{b.get('booking_id')}'. Cancel bookings first.")

    del resources_dict[clean_id]
    return True, f"Resource '{clean_id}' removed successfully."


def get_all_unique_facilities(resources_dict):
    """
    Accumulates all unique facilities available across all resources using a set.
    
    Demonstrates:
    - Set union / set accumulation
    
    Returns:
        list: Sorted list of unique facility strings
    """
    facilities_set = set()
    for res in resources_dict.values():
        for fac in res.get("facilities", []):
            facilities_set.add(fac)
    return sorted(list(facilities_set))


def format_resource_table(resources_list):
    """
    Formats a list of resources into an aligned text table for terminal output.
    """
    if not resources_list:
        return "No resources found."

    lines = []
    header = f"{'ID':<8} | {'Name':<20} | {'Type':<16} | {'Cap':<5} | {'Facilities':<30}"
    divider = "-" * len(header)
    lines.append(divider)
    lines.append(header)
    lines.append(divider)

    for r in resources_list:
        facs = ", ".join(r.get("facilities", []))
        if len(facs) > 28:
            facs = facs[:25] + "..."
        line = (f"{r.get('resource_id', ''):<8} | "
                f"{r.get('name', ''):<20} | "
                f"{r.get('resource_type', ''):<16} | "
                f"{r.get('capacity', 0):<5} | "
                f"{facs:<30}")
        lines.append(line)

    lines.append(divider)
    return "\n".join(lines)
