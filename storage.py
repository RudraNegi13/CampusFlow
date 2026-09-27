"""
storage.py
----------
JSON storage module for CampusFlow.
CSE1021 - Introduction to Problem Solving and Programming.

Demonstrates:
- File input/output handling
- JSON parsing and serialization
- Safe error handling (try/except for FileNotFoundError, JSONDecodeError, IOError)
- Separation of storage concerns from business logic
"""

import json
import os

# Default storage directories relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESOURCES_FILE = os.path.join(DATA_DIR, "resources.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.json")


def ensure_data_directory():
    """Ensures that the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def load_json_file(filepath, default_value):
    """
    Safely loads data from a JSON file.
    
    Parameters:
        filepath (str): Absolute or relative path to file.
        default_value (any): Value to return if file is missing or invalid.
        
    Returns:
        any: Parsed JSON data or default_value.
    """
    if not os.path.exists(filepath):
        return default_value
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError) as error:
        print(f"[Warning] Could not read {filepath}: {error}. Returning default values.")
        return default_value


def save_json_file(filepath, data):
    """
    Safely writes data to a JSON file with human-readable indentation.
    
    Parameters:
        filepath (str): Path to destination file.
        data (any): Data structure to serialize.
        
    Returns:
        bool: True if write succeeded, False otherwise.
    """
    ensure_data_directory()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except (IOError, TypeError) as error:
        print(f"[Error] Failed to save data to {filepath}: {error}")
        return False


# Specific Entity Storage Helpers

def load_resources(filepath=RESOURCES_FILE):
    """Loads resources dictionary from file. Default is empty dict."""
    raw_data = load_json_file(filepath, {})
    # Return as dict {resource_id: resource_data}
    return raw_data


def save_resources(resources_dict, filepath=RESOURCES_FILE):
    """Saves resources dictionary to file."""
    return save_json_file(filepath, resources_dict)


def load_bookings(filepath=BOOKINGS_FILE):
    """Loads confirmed bookings list from file. Default is empty list."""
    return load_json_file(filepath, [])


def save_bookings(bookings_list, filepath=BOOKINGS_FILE):
    """Saves confirmed bookings list to file."""
    return save_json_file(filepath, bookings_list)


def load_requests(filepath=REQUESTS_FILE):
    """Loads space requests list from file. Default is empty list."""
    return load_json_file(filepath, [])


def save_requests(requests_list, filepath=REQUESTS_FILE):
    """Saves space requests list to file."""
    return save_json_file(filepath, requests_list)
