# CampusFlow — Smart College Resource Allocation and Utilization System

> **Course Code:** CSE1021 — Introduction to Problem Solving and Programming  
> **Target Platform:** Python 3.8+ (Cross-Platform: Windows, macOS, Linux)  
> **Dependencies:** None (Pure Python Standard Library)

---

## 1. Project Overview

**CampusFlow** is a modular, terminal-based resource allocation and audit system developed for academic institutions. It matches student space requests (for computer labs, study rooms, discussion suites, project rooms, and seminar halls) with available college resources using rule-based decision logic, multi-constraint satisfaction, and a **Best-Fit** capacity heuristic.

The project is designed specifically to demonstrate core foundational concepts from **CSE1021 — Introduction to Problem Solving and Programming**, emphasizing algorithmic clarity, problem decomposition, structured data modeling, defensive input validation, automated testing, and persistent file storage.

---

## 2. Problem Being Solved

University campuses face persistent challenges in coordinating shared physical spaces:
- **Scheduling Conflicts:** Simultaneous booking of the same room during overlapping times.
- **Student Dual-Booking:** A student inadvertently reserving multiple rooms at the same time.
- **Capacity Mismatch:** Small groups booking large lecture halls, resulting in wasted seating capacity.
- **Opaque Denials:** Students receive rejections without explanations or alternative recommendations.
- **Lack of Utilization Visibility:** Administration lacks clear data on peak days, hours, and underutilized rooms.

CampusFlow solves these issues by automating the intake, validation, evaluation, allocation, alternative discovery, and analytics reporting.

---

## 3. Key Objectives

1. Implement **Top-Down Problem Decomposition** across distinct modules.
2. Utilize native Python data structures:
   - **Dictionaries:** Associative lookup for resources, requests, and bookings.
   - **Lists:** Ordered sequences of records, candidates, and operational slots.
   - **Tuples:** Immutable time intervals: `("Monday", "14:00", "16:00")`.
   - **Sets:** Unordered unique collections for facility matching and duplicate detection.
3. Demonstrate foundational programming algorithms:
   - **Searching:** Linear search for matching resources and pending requests.
   - **Filtering:** Multi-criteria querying (type, capacity, equipment).
   - **Counting & Summation:** Loop accumulators for total hours, bookings, and attendees.
   - **Maximum & Minimum:** Explicit loop tracking for most/least used spaces and best-fit capacity selection.
   - **Interval Overlap Arithmetic:** Converting `HH:MM` times to integer minutes and checking $(s_1 < e_2) \land (s_2 < e_1)$.
4. Build a robust test suite using Python's built-in `unittest` module.

---

## 4. System Features

- **Space Request Submission:** Interactive intake with real-time validation (positive attendee count, valid 24-hr time ranges, allowed weekdays).
- **Resource Inventory & Search:** View and filter campus resources by category, capacity, or available equipment (Computers, Projectors, Whiteboards, Audio Systems, AC, Internet).
- **Algorithmic Allocation Engine:**
  - Evaluates candidate rooms against category, capacity, equipment, operating hours, and active bookings.
  - Generates a **Decision Trace Log** explaining why each room was accepted or rejected.
  - Applies **Best-Fit Optimization** to select the room with minimal seat wastage.
- **Alternative Slot Recommendation:** Proposes open operating windows on the same weekday or other days when the exact requested slot is unavailable.
- **Conflict Detection & Schedule Audit:** Pairwise inspection of the schedule to verify zero overlapping reservations or concurrent student bookings.
- **Utilization Analytics Dashboard:** Computes allocation success rate, busiest day, peak time slot, most/least utilized spaces, and seat packing efficiency.
- **Resource Inventory Management:** Add, update, or remove physical resources with active booking dependency protection.
- **Persistent JSON Storage:** Automatic file persistence across sessions.

---

## 5. Technologies Used

- **Language:** Python 3.8+
- **Standard Library Modules:**
  - `json`: Data serialization and deserialization
  - `os`: Cross-platform path handling
  - `sys`: Clean application exit
  - `unittest`: Automated unit and integration testing
  - `copy`: Deep-copying state for isolated test cases

**No external third-party libraries or frameworks are required.**

---

## 6. Project Directory Structure

```text
CampusFlow/
├── main.py                 # Interactive terminal UI and main event loop
├── models.py               # Entity constructors and system constants
├── storage.py              # JSON storage load/save functions
├── validation.py           # Input sanitization and format validators
├── conflict_manager.py     # Time arithmetic, overlap checks, and audit algorithms
├── resource_manager.py     # Resource inventory CRUD and linear search
├── request_manager.py      # Student request intake and queue tracking
├── allocation_engine.py    # Rule-based allocation, Best-Fit selection, and alternatives
├── analytics.py            # Utilization metrics, max/min, counting, and summation
├── test_campusflow.py      # 12 automated unit and integration tests
│
├── data/                   # Persistent JSON storage files
│   ├── resources.json      # Pre-loaded campus resource records
│   ├── bookings.json       # Confirmed reservations
│   └── requests.json       # Space requests log
│
├── diagrams/               # System architecture and design diagrams
│   ├── architecture.mmd    # 4-layer system architecture diagram
│   ├── workflow.mmd        # Allocation decision tree flowchart
│   ├── use_case.mmd        # Student and Admin use case diagram
│   ├── class_diagram.mmd   # Component and function structure
│   ├── sequence_diagram.mmd# Request-to-booking sequence diagram
│   └── data_schema.mmd     # Entity-Relationship diagram for JSON data
│
├── statement.md            # Academic project statement and scope
├── REPORT_OUTLINE.md       # Comprehensive 16-section project report outline
├── requirements.txt        # Python dependency documentation (Zero external dependencies)
└── .gitignore              # Standard git ignore file
```

---

## 7. How to Install and Set Up

1. Open your terminal or command prompt (PowerShell / Command Prompt on Windows, Terminal on macOS/Linux).
2. Navigate to the project directory:
   ```bash
   cd CampusFlow
   ```
3. Verify that Python 3 is installed:
   ```bash
   python --version
   ```
   *(Ensure Python version is 3.8 or higher)*

---

## 8. How to Run the Program

Launch the interactive console application:
```bash
python main.py
```

You will see the main menu:
```text
==================================================
                 CAMPUSFLOW
  Smart College Resource Allocation System
  CSE1021: Problem Solving & Programming
==================================================
  1. Submit Space Request
  2. View Available Resources
  3. Allocate Resource (Process Request)
  4. View Bookings
  5. Detect Conflicts & Audit
  6. View Utilization Analytics
  7. Manage Resources
  8. Exit
==================================================
Enter your choice (1-8):
```

---

## 9. Example Usage Walkthrough

### Example 1: View Resource Inventory
1. Choose option `2`.
2. Inspect the pre-configured rooms:
   - `LAB01`: Computer Lab 1 (Capacity: 30)
   - `LAB02`: Computer Lab 2 (Capacity: 50)
   - `ROOM01`: Study Room A (Capacity: 8)
   - `ROOM02`: Project Room (Capacity: 12)
   - `SEM01`: Seminar Room (Capacity: 80)
3. Filter by capacity or facilities as desired.

### Example 2: Submit a Space Request & Immediate Allocation
1. Choose option `1`.
2. Enter student details:
   - Student ID: `STU1005`
   - Student Name: `Rohan Gupta`
   - Resource Type: `1` (Computer Lab)
   - Number of Students: `22`
   - Preferred Day: `Monday`
   - Start Time: `09:00`
   - End Time: `11:00`
   - Required Facilities: `Computers, Projector`
3. The system validates all inputs.
4. When prompted: `Would you like to process allocation for this request immediately? (y/n):`, enter `y`.
5. Observe the **Decision Log Trace**:
   ```text
   --- DECISION LOG TRACE ---
     * Computer Lab 1 (LAB01): Accepted -- all requirements satisfied.
     * Computer Lab 2 (LAB02): Accepted -- all requirements satisfied.
   --------------------------
   [SUCCESS] Resource 'Computer Lab 1' (LAB01) allocated!
   Booking ID      : BK204
   Allocated Slot  : Monday 09:00 - 11:00
   Booked For      : Rohan Gupta (STU1005)
   ```
   *Note: LAB01 was selected because its capacity (30) is closer to 22 than LAB02 (50), minimizing seat wastage.*

### Example 3: View Utilization Analytics
1. Choose option `6`.
2. View the dynamically generated analytics dashboard:
   - Total resources, requests, bookings, and pending queue
   - Allocation success rate percentage
   - Most-used and least-used resources
   - Busiest weekday and time window
   - Operational hour utilization and seat packing efficiency

---

## 10. How to Run the Automated Test Suite

To run all automated test cases:
```bash
python test_campusflow.py
```
Or using the standard unittest discovery:
```bash
python -m unittest test_campusflow.py
```

### Test Coverage Summary:
- `test_01_valid_resource_creation`: Checks proper resource insertion.
- `test_02_invalid_resource_capacity`: Confirms zero, negative, and string rejection.
- `test_03_valid_booking`: Validates non-conflicting allocation.
- `test_04_duplicate_booking`: Confirms prevention of concurrent student bookings.
- `test_05_capacity_conflict`: Tests rejection when student count exceeds room capacity.
- `test_06_time_conflict`: Tests rejection when resource is already occupied.
- `test_07_invalid_request`: Validates inverted time ranges and invalid room types.
- `test_08_alternative_slot_search`: Tests alternative slot discovery when requested slot is blocked.
- `test_09_utilization_calculation`: Tests counting, summation, max/min, and ratio math.
- `test_10_search_and_filter`: Tests linear search across type, capacity, and equipment.
- `test_11_audit_conflicts`: Tests schedule audit on corrupted booking records.
- `test_12_best_fit_selection`: Verifies selection of room with minimum capacity surplus.

---

## 11. Viva Voce Preparation Guide (CSE1021 Concepts)

If asked by your examiner to explain key algorithms in the code:

1. **How does Time Interval Overlap Detection work? (`conflict_manager.py`)**
   - *"We convert the 24-hour time strings `HH:MM` into integer minutes from midnight using `hours * 60 + minutes`. Two intervals $[s_1, e_1)$ and $[s_2, e_2)$ overlap if and only if $s_1 < e_2$ AND $s_2 < e_1$. This avoids string comparison errors and works in $O(1)$ time."*

2. **How does the Allocation Engine choose between multiple eligible rooms? (`allocation_engine.py`)**
   - *"We use a Best-Fit heuristic. For all candidate rooms that meet the type, capacity, facility, and time requirements, we calculate seat wastage as `room_capacity - student_count`. We iterate through the candidates using a linear minimum-finding algorithm to select the room with the smallest non-negative waste."*

3. **How are Missing Facilities detected? (`conflict_manager.py`)**
   - *"We convert the required facilities and room facilities into Python sets. Using the set difference operator `set(required) - set(resource_facilities)`, we instantly obtain any missing amenities in $O(|required|)$ time."*

4. **How are Most-Used and Least-Used Resources calculated? (`analytics.py`)**
   - *"We initialize a dictionary mapping each resource ID to 0. We iterate through confirmed bookings with a `for` loop, incrementing counts. Then, we use explicit `max_count` and `min_count` tracking variables in a loop to identify the extremes without relying on complex black-box functions."*

---

## 12. Non-Functional Requirements Addressed

- **Usability:** Menu-driven terminal interface with input prompts and aligned tables.
- **Reliability:** Deterministic allocation behavior and referential checks preventing deletion of booked rooms.
- **Maintainability:** 8 modular Python files, each containing focused functions with clear docstrings.
- **Robust Error Handling:** Validations return `(is_valid, error_message)` tuples to prevent unhandled crashes.
- **Performance:** Instantaneous algorithmic execution ($< 5\text{ ms}$) on campus datasets.

---

## 13. Future Enhancements

- Semester-long recurring weekly booking reservations.
- Priority queue based on academic deadlines or class seniority.
- Exporting analytics reports to CSV / PDF.
- Visual ASCII weekly timetable grid.
