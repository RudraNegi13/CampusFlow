# CampusFlow: Project Statement

**Course Code:** CSE1021 — Introduction to Problem Solving and Programming  
**Project Title:** CampusFlow — Smart College Resource Allocation and Utilization System  
**Academic Level:** First-Year Undergraduate  

---

## 1. Problem Statement

Modern college campuses house a diverse set of specialized shared facilities, including computer laboratories, study rooms, project collaboration spaces, discussion suites, and seminar halls. As student enrollments and collaborative course projects increase, managing these physical spaces efficiently becomes challenging:

1. **Manual Scheduling Inefficiencies:** Traditional manual sign-up sheets or fragmented email requests result in double-booking, scheduling conflicts, and human errors.
2. **Suboptimal Capacity Utilization:** High-capacity venues (e.g., 80-seat seminar halls) are frequently reserved for small student groups (e.g., 5 students), leaving large classes without suitable venues.
3. **Lack of Transparent Conflict Feedback:** When a request is denied, students are rarely provided with specific explanations or actionable alternatives, leading to frustration and repeated failed submissions.
4. **Absence of Utilization Visibility:** College administrations often lack real-time visibility into which resources are bottlenecked and which remain underutilized throughout the academic week.

**CampusFlow** addresses these challenges by providing an algorithmic, rule-based resource allocation and audit system implemented in Python. It systematically matches student space requests with compatible campus facilities, enforces strict multi-attribute constraints, logs granular rejection feedback, recommends alternative available slots, and computes quantitative utilization metrics.

---

## 2. Project Scope

### In Scope
- **Inventory Management:** Centralized registry of physical college spaces (Computer Labs, Study Rooms, Discussion Rooms, Project Rooms, Seminar Halls) with defined seat capacities, specialized equipment/facilities, and weekly operating windows.
- **Request Processing & Input Validation:** Intake and defensive verification of student booking requests (verifying positive headcount, valid 24-hour time ranges, allowable weekdays, and recognized room categories).
- **Rule-Based Allocation Engine:** Multi-factor algorithmic filtering checking room type, group capacity, required facilities, operating hours, and active schedule conflicts.
- **Best-Fit Capacity Heuristic:** Algorithmic selection among eligible candidate rooms to minimize vacant seating waste.
- **Conflict Detection & Audit:** Pairwise schedule auditing to prevent overlapping reservations for the same room or concurrent bookings for the same student.
- **Intelligent Alternative Recommendations:** Automated discovery of alternative operating windows on the requested day or across other weekdays when an exact match cannot be satisfied.
- **Utilization & Efficiency Analytics:** Calculation of total bookings, allocation success rate, busiest days/time windows, most/least utilized spaces, and overall seating packing efficiency using standard counting, summation, and min/max algorithms.
- **Lightweight File Persistence:** Safe JSON serialization and deserialization ensuring state persistence between system sessions.

### Out of Scope (Educational Context)
- Multi-tier web frontends (e.g., React, Angular) and heavy web frameworks (Django, Flask).
- Distributed database systems or ORM frameworks (SQL/NoSQL).
- External AI/ML cloud APIs or language model wrappers.
- Cloud payment gateways or access-card physical hardware integrations.

The implementation is intentionally constrained to standard Python algorithms, modular functions, and native data structures to align with the pedagogical objectives of CSE1021.

---

## 3. Target Users

1. **College Students & Study Groups:**
   - Submit space reservation requests for academic projects, lab assignments, club meetings, and collaborative peer study.
   - Receive immediate verification, transparent allocation feedback, or alternative slot recommendations.
   - View confirmed reservations and cancel bookings when plans change.

2. **Faculty Members & Lab Instructors:**
   - Reserve specialized lecture halls, seminar rooms, and computer labs for workshops and review sessions.
   - Monitor facility availability across weekdays.

3. **Department Administrators & Facility Managers:**
   - Maintain the resource inventory (register new rooms, update seating capacities, adjust operating hours).
   - Audit the campus schedule to verify that zero double-bookings or concurrent student reservations exist.
   - Review utilization analytics to make data-driven decisions on room maintenance and lab provisioning.

---

## 4. High-Level Features

| Feature ID | Feature Name | Description |
| :--- | :--- | :--- |
| **F-01** | Space Request Submission | Interactive intake of student ID, name, room type, attendee count, weekday, start/end time, and required facilities with real-time input validation. |
| **F-02** | Resource Inventory Search | Multi-criteria querying of campus rooms by category, minimum capacity threshold, or specific equipment (e.g., Projector, Whiteboard). |
| **F-03** | Algorithmic Resource Allocation | Automated candidate matching evaluating room category, capacity compliance, facility presence, operational hours, and booking overlaps. |
| **F-04** | Best-Fit Room Selection | Objective minimization of idle seats: selects the candidate room with $\min(\text{capacity} - \text{student\_count})$. |
| **F-05** | Decision Trace & Rejection Log | Detailed terminal explanation indicating why each potential room was accepted or rejected during the evaluation loop. |
| **F-06** | Alternative Slot Discovery | Algorithmic scan proposing alternative unbooked operating windows on the same weekday or alternate days when an exact slot is unavailable. |
| **F-07** | Conflict Detection & Audit | Comprehensive pairwise audit scanning active bookings for overlapping time intervals or dual-booking anomalies. |
| **F-08** | Utilization Dashboard | Analytical reporting of allocation success percentage, busiest days, peak time windows, most/least booked rooms, and seat packing ratio. |
| **F-09** | Resource Inventory Management | Administrative functions to add, inspect, update, or remove physical resources with referential integrity protection. |
| **F-10** | Persistent JSON Storage | File-backed storage layer loading and saving inventory, requests, and bookings across program restarts. |
