# CampusFlow — Comprehensive Project Report

**Course Code:** CSE1021 — Introduction to Problem Solving and Programming  
**Course Title:** Problem Solving and Programming in Python  
**Project Title:** CampusFlow — Smart College Resource Allocation and Utilization System  
**Academic Term:** First-Year Engineering  

---

## 1. Cover Page Details
- **Project Title:** CampusFlow: Smart College Resource Allocation and Utilization System
- **Course Name & Code:** CSE1021 — Introduction to Problem Solving and Programming
- **Department:** Department of Computer Science and Engineering
- **Target Audience:** First-Year Undergraduate Evaluation & Viva Voce
- **Implementation Language:** Python 3.8+ (Pure Standard Library)

---

## 2. Introduction
Physical infrastructure on university campuses represents a valuable and finite resource. Modern academic curricula require regular access to specialized facilities such as software computing laboratories, seminar auditoriums, group discussion spaces, and quiet study halls. In the absence of an automated system, resource allocation is typically handled through manual registers, spreadsheets, or ad-hoc verbal agreements. This approach leads to scheduling disputes, room double-bookings, underutilization of large facilities, and an inability to audit campus spatial efficiency.

**CampusFlow** was developed as a clean, algorithmic solution to this problem. Designed within the curriculum guidelines of **CSE1021**, the system demonstrates computational problem decomposition, modular software engineering, foundational data structures (dictionaries, lists, tuples, sets), rule-based algorithms, input validation, and file persistence.

---

## 3. Problem Statement
Campus facility coordinators and student representatives face four recurring operational challenges:
1. **Double-Booking & Time Clashes:** Concurrent reservations of the same venue during overlapping time intervals.
2. **Capacity Mismatch & Spatial Waste:** Booking 80-seat auditoriums for 4-student discussions when suitable smaller rooms exist.
3. **Opaque Request Rejection:** Lack of descriptive feedback when a reservation fails, leaving students without actionable alternative slots.
4. **Data Blindness:** Absence of descriptive metrics detailing which facilities experience peak demand and which remain idle.

CampusFlow automates this lifecycle using transparent, rule-based algorithms that enforce multi-attribute constraints and compute actionable analytics.

---

## 4. Objectives
1. **Deconstruct the Allocation Lifecycle:** Decompose space booking into modular stages: input validation, eligibility filtering, conflict detection, candidate optimization, and alternative search.
2. **Apply Foundational Data Structures:** Employ dictionaries for fast associative lookups, lists for ordered records, tuples for immutable time intervals, and sets for unique facilities and set operations.
3. **Implement Rule-Based Algorithmic Decision Making:** Develop a multi-stage filtering pipeline and a Best-Fit optimization algorithm to minimize wasted seating capacity.
4. **Provide Defensible Error Handling:** Defend against invalid inputs, negative numbers, malformed time ranges, and duplicate student schedules without system crashes.
5. **Generate Algorithmic Analytics:** Calculate utilization rates, peak operating windows, and resource frequency distributions using explicit Python loops and accumulators.

---

## 5. Functional Requirements
- **FR-1 (Resource Management):** Add, search, view, update, and remove physical resources with defined seating capacity, equipment amenities, and operating hours.
- **FR-2 (Request Intake):** Accept student space requests capturing Student ID, Name, Resource Type, Group Size, Weekday, Start/End Time, and Required Amenities.
- **FR-3 (Input Validation):** Validate all user inputs, rejecting empty strings, non-numeric inputs, negative numbers, invalid weekdays, and backward time intervals ($start \ge end$).
- **FR-4 (Multi-Constraint Filtering):** Evaluate candidate spaces against five sequential criteria: category match, capacity sufficiency, equipment availability, operational hours, and booking overlaps.
- **FR-5 (Best-Fit Room Optimization):** Among all fully qualified rooms, select the candidate room that minimizes wasted seating capacity ($\min(\text{capacity} - \text{students})$).
- **FR-6 (Decision Trace Logging):** Generate a clear explanation for every candidate room, detailing why it was accepted or rejected.
- **FR-7 (Alternative Slot Discovery):** In the event of a failed allocation, automatically scan and recommend available alternative slots on the same day or across other operational days.
- **FR-8 (Schedule Conflict Audit):** Perform pairwise checks across the booking registry to verify that no overlapping room reservations or concurrent student bookings exist.
- **FR-9 (Utilization Analytics):** Generate a metrics dashboard showing allocation success rates, busiest weekdays, peak time slots, most/least utilized spaces, and seat packing efficiency.
- **FR-10 (Persistent Storage):** Store and retrieve resources, requests, and bookings using structured JSON files.

---

## 6. Non-Functional Requirements
1. **Usability:** 
   - A clean, intuitive terminal menu with clear numbered options and formatted tabular presentations.
   - Comprehensive prompts guiding the user through every input field.
2. **Reliability:**
   - Deterministic allocation outcomes: identical requests against the same state always yield identical results.
   - Referential integrity: resources with active bookings cannot be accidentally deleted.
3. **Maintainability:**
   - Modular decomposition across 8 distinct Python modules, each with a single responsibility.
   - Zero external third-party dependencies, ensuring immediate execution across any standard Python 3.8+ environment.
4. **Robust Error Handling:**
   - Graceful input rejection with clear error messages rather than unhandled exception crashes.
   - Use of `(is_valid, message)` return patterns and localized `try/except` blocks for file I/O.
5. **Efficiency & Performance:**
   - Lightweight linear search algorithms and direct dictionary lookups ($O(1)$) ensuring instantaneous response times ($< 5\text{ ms}$) for campus-scale datasets.

---

## 7. System Architecture
CampusFlow follows a modular four-tier architecture:
- **Presentation Layer (`main.py`):** Drives interactive terminal navigation, input capture, and console formatting.
- **Management & Controller Layer (`resource_manager.py`, `request_manager.py`, `analytics.py`):** Orchestrates entity operations, inventory filtering, request tracking, and statistical reporting.
- **Algorithmic & Validation Layer (`allocation_engine.py`, `conflict_manager.py`, `validation.py`):** Houses the core problem-solving logic: time interval arithmetic, set difference checking, constraint satisfaction, candidate optimization, and alternative slot discovery.
- **Data & Persistence Layer (`models.py`, `storage.py`, `data/*.json`):** Defines domain constructors, enforces data structures, and handles JSON serialization.

---

## 8. Design Diagrams
The project includes formal Mermaid design diagrams located in the `diagrams/` directory:
1. **System Architecture Diagram (`diagrams/architecture.mmd`):** Illustrates the structural dependency graph across the four layers.
2. **Workflow Diagram (`diagrams/workflow.mmd`):** Flowchart tracing the step-by-step decision tree from request intake to booking confirmation or alternative suggestion.
3. **Use Case Diagram (`diagrams/use_case.mmd`):** Captures interactions between primary actors (Student, Faculty/Admin) and system use cases.
4. **Class & Module Diagram (`diagrams/class_diagram.mmd`):** Documents the component interfaces, functions, parameters, and relationships.
5. **Sequence Diagram (`diagrams/sequence_diagram.mmd`):** Illustrates the chronological message exchanges during an allocation request.
6. **Data & Storage Schema (`diagrams/data_schema.mmd`):** Entity-relationship diagram representing the JSON schemas for Resources, Requests, and Bookings.

---

## 9. Design Decisions and Rationale
1. **Why Pure Python Standard Library?**
   - In alignment with CSE1021 coursework, using external libraries (e.g., Pandas, NumPy, or web frameworks) masks foundational algorithmic thinking. Writing accumulators, search loops, and min/max routines manually demonstrates genuine mastery of programming principles.
2. **Why Tuples for Operating Slots?**
   - Time slots represent immutable records composed of `(day, start_time, end_time)`. Tuples ensure that slot boundaries cannot be inadvertently mutated in-memory.
3. **Why Sets for Facilities?**
   - Equipment requirements are order-independent. Using Python sets allows set difference (`req_set - res_set`) to instantly detect missing amenities in $O(|req|)$ time.
4. **Why Best-Fit Selection Over First-Available?**
   - First-available allocation frequently leads to spatial fragmentation (e.g., assigning a 50-seat room to 2 students when a 10-seat room is available). Best-Fit capacity optimization directly reduces campus resource waste.
5. **Why Time Conversion to Integer Minutes?**
   - String comparisons like `"9:00" < "10:00"` fail when strings are not zero-padded, and time interval comparisons are error-prone. Converting `HH:MM` into total minutes from midnight transforms overlap verification into clean integer arithmetic: $(s_1 < e_2) \land (s_2 < e_1)$.

---

## 10. Implementation Details
The codebase is structured into 8 modular Python source files:

| Module | File | Core Functions & Algorithmic Responsibility |
| :--- | :--- | :--- |
| **Models** | `models.py` | Constructors for Resources, Requests, and Bookings; defines valid room types, operational days, and standard facility constants. |
| **Validation** | `validation.py` | Input sanitization, non-empty checks, positive integer verification, 24-hr time validation, and day checks. |
| **Storage** | `storage.py` | JSON read/write persistence with safe exception handling (`FileNotFoundError`, `JSONDecodeError`). |
| **Conflict Manager** | `conflict_manager.py` | `time_to_minutes()`, `is_time_overlap()`, operating hour verification, duplicate student detection, and pairwise schedule auditing. |
| **Resource Manager** | `resource_manager.py` | CRUD operations for resources, multi-criteria linear search, facility accumulation using sets, and table formatting. |
| **Request Manager** | `request_manager.py` | Sequential ID generation (`REQ101`...), request queue tracking, pending request filtering, and status mutation. |
| **Allocation Engine** | `allocation_engine.py` | Multi-constraint candidate evaluation, Best-Fit selection algorithm, rejection trace logging, and alternative slot discovery. |
| **Analytics** | `analytics.py` | Counting accumulators, summation algorithms, explicit min/max tracking, frequency mapping, and percentage calculations. |

---

## 11. Screenshots & Sample Execution Results
*(During viva / report submission, capture the terminal output from the following tested workflows):*

### Workflow A: Utilization Analytics Dashboard
```
==================================================
          CAMPUSFLOW UTILIZATION ANALYTICS        
==================================================
  Total Resources Registered : 5
  Total Requests Submitted  : 4
  Successful Allocations    : 3
  Failed Allocations        : 0
  Pending Requests          : 1
  Allocation Success Rate   : 75.0%
--------------------------------------------------
  RESOURCE USAGE METRICS:
  Most-Used Resource        : Computer Lab 1 (LAB01) - 1 booking(s)
  Least-Used Resource       : Computer Lab 2 (LAB02) - 0 booking(s)
  Busiest Day of the Week   : Monday (1 booking(s))
  Busiest Time Window       : 14:00 - 16:00 (1 booking(s))
--------------------------------------------------
  EFFICIENCY & UTILIZATION:
  Resource Time Utilization : 3.24% of operational hours booked
  Seat Packing Efficiency   : 77.12% seats filled during bookings
==================================================
```

### Workflow B: Allocation Engine with Decision Trace
```
==================================================
  ALLOCATING REQUEST REQ104
==================================================
Target: Computer Lab on Monday from 09:00 to 11:00 for 20 student(s).

--- DECISION LOG TRACE ---
  * Computer Lab 1 (LAB01): Accepted -- all requirements satisfied.
  * Computer Lab 2 (LAB02): Accepted -- all requirements satisfied.
--------------------------

[SUCCESS] Resource 'Computer Lab 1' (LAB01) allocated!
Booking ID      : BK204
Allocated Slot  : Monday 09:00 - 11:00
Booked For      : Vikram Patel (STU1004)
```

### Workflow C: Conflict Audit Verification
```
==================================================
  CONFLICT DETECTION & SCHEDULE AUDIT
==================================================
Scanning all bookings for potential scheduling collisions...

[OK] Audit Complete: 0 conflicts detected. All bookings are valid and conflict-free.
```

---

## 12. Testing Approach & Verification
Testing was conducted using Python's standard `unittest` framework in `test_campusflow.py`.

### Automated Test Matrix (12 Test Scenarios):
1. `test_01_valid_resource_creation`: Verifies successful resource addition with properly formatted fields.
2. `test_02_invalid_resource_capacity`: Confirms rejection of zero, negative, and non-numeric capacity inputs.
3. `test_03_valid_booking`: Asserts successful allocation and booking binding for a valid, non-conflicting request.
4. `test_04_duplicate_booking`: Asserts that a student cannot hold concurrent bookings across different rooms.
5. `test_05_capacity_conflict`: Confirms that rooms with capacity less than requested students are rejected.
6. `test_06_time_conflict`: Confirms that overlapping bookings for the same room are detected and rejected.
7. `test_07_invalid_request`: Validates rejection of inverted time ranges ($start \ge end$) and unregistered room types.
8. `test_08_alternative_slot_search`: Confirms that when an exact slot is occupied, viable alternative slots are discovered.
9. `test_09_utilization_calculation`: Validates counting, summation, max/min, and utilization math against known test values.
10. `test_10_search_and_filter`: Tests linear search across room types, capacity thresholds, and facility presence.
11. `test_11_audit_conflicts`: Confirms that corrupted overlapping bookings in storage are identified during schedule audits.
12. `test_12_best_fit_selection`: Verifies that between two candidate rooms, the room with the smallest capacity surplus is selected.

**Test Execution Command:**
```bash
python test_campusflow.py
```
**Outcome:** 12 tests passed in 0.001 seconds (`OK`).

---

## 13. Challenges Faced & Solutions
1. **Handling Time Overlaps Across Irregular Slot Boundaries:**
   - *Challenge:* Direct string comparisons fail when comparing times of varying lengths or when slots partially overlap.
   - *Solution:* Built `time_to_minutes(time_str)` converting any `HH:MM` into integer minutes. Two intervals overlap if and only if `start1 < end2 and start2 < end1`.
2. **Preventing Referential Orphan Records:**
   - *Challenge:* Deleting a resource that has confirmed future bookings leaves bookings referencing non-existent facilities.
   - *Solution:* Implemented an active booking dependency check in `resource_manager.remove_resource()` that forbids deletion until existing bookings are cancelled.
3. **Transparent Rejection Diagnostics:**
   - *Challenge:* Standard allocation systems return a binary "Success/Fail", leaving users in the dark.
   - *Solution:* Engineered a step-by-step rejection trace collecting human-readable reasons (e.g., "Insufficient capacity: has 8, requires 15", "Missing required facilities: Projector") for every evaluated room.

---

## 14. Learnings & Key Takeaways
1. **Power of Problem Decomposition:** Breaking a complex system into 8 focused modules makes development, debugging, and testing straightforward and manageable.
2. **Choosing the Right Data Structure:** Leveraging the distinct strengths of Python data structures (dictionaries for fast lookup, tuples for immutable intervals, sets for containment, lists for sequential storage) leads to clean and expressive code.
3. **Algorithmic Clarity over Complexity:** Writing explicit loops, counters, and comparison variables makes code readable, verifiable, and easy to explain during academic evaluation.

---

## 15. Future Enhancements
- **Recurring Booking Reservations:** Support for semester-long recurring weekly slots for academic lectures.
- **Priority-Based Request Queue:** Weighted priority queues for final-year capstone presentations or departmental exams.
- **CSV / PDF Export Facility:** Exporting utilization reports into tabular spreadsheets for administrative reviews.
- **Interactive Calendar View:** Terminal ASCII calendar grid visualizing weekly room occupancy schedules.

---

## 16. References
1. Python Software Foundation. *Python 3 Standard Library Documentation: `json`, `os`, `sys`, `unittest`*. Available at: https://docs.python.org/3/
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (3rd ed.). MIT Press (Interval Scheduling & Greedy Heuristics).
3. Course Notes & Lecture Materials for **CSE1021: Introduction to Problem Solving and Programming**.
