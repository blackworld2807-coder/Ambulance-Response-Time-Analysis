# Ambulance Response-Time Analysis

## Technology
- Python 3
- SQLite relational DBMS
- SQL
- Python standard library: sqlite3, datetime, statistics

## Problem
Analyze emergency calls, dispatch times and arrival times to identify response delays.

## Main features
1. Store emergency call records.
2. Validate HH:MM time entries.
3. Calculate dispatch delay.
4. Calculate total response time.
5. Categorize response time.
6. Search incidents by location.
7. Store records in a relational DBMS.
8. Generate response reports.
9. Identify longer-response locations.
10. Identify the peak emergency hour.
11. Suggest data-driven resource-allocation improvements.

## Formulae
Dispatch Delay = Dispatch Time - Call Time
Response Time = Arrival Time - Call Time

The sample in the question:
Call 14:10, Dispatch 14:14, Arrival 14:28
Dispatch Delay = 4 minutes
Response Time = 18 minutes
Category = High Response Time

## Category rule
- 0-10 minutes: Low Response Time
- 11-15 minutes: Moderate Response Time
- More than 15 minutes: High Response Time

These thresholds are project-defined demonstration thresholds. In a real ambulance service, thresholds should be based on the service's clinical/operational standards and geography.

## How to run
1. Install Python 3.
2. Put `main.py` and `schema.sql` in one folder.
3. Open terminal in that folder.
4. Run:
   python main.py
5. Select option 5 to insert sample records.
6. Select option 2 to view records.
7. Select option 4 to generate the analysis report.

The database file `ambulance_response.db` is created automatically.

## Important validation
The program rejects:
- Empty incident IDs
- Empty locations
- Incorrect time format
- Dispatch time earlier than call time
- Arrival time earlier than dispatch time
- Duplicate incident IDs

## Academic note
This project demonstrates data collection, validation, computation, storage, retrieval, SQL aggregation and interpretation. It is an analytical prototype, not a live emergency-dispatch system.

## 📁 Repository Structure

```text
Ambulance-Response-Time-Analysis/
├── data/       # Sample/input data
├── docs/       # Project report and documentation
├── outputs/    # Generated reports/analysis outputs
├── src/        # Python source code and SQL schema
├── .gitignore
├── LICENSE
├── README.md
└── run.bat
```
