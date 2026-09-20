# COURSE END PROJECT 14 – AMBULANCE RESPONSE-TIME ANALYSIS

## 1. Abstract
Ambulance response time is an important operational measure in emergency healthcare. Delays can occur during call handling, dispatch, travel, traffic conditions, ambulance availability, or other operational stages. This project develops a Python + DBMS based system to record emergency incidents, calculate dispatch delay and total response time, classify incidents, search incidents by location, and generate an analytical report.

The system uses Python for input handling, validation, calculations and reporting, and a relational DBMS (SQLite) for persistent storage. The project also analyzes locations and emergency-call periods to identify patterns that may require operational review.

## 2. Problem Statement
Analyze emergency calls, dispatch times and arrival times to identify response delays.

## 3. Objectives
1. Store emergency call records.
2. Accept call, dispatch and arrival times.
3. Validate invalid or logically inconsistent time entries.
4. Calculate dispatch delay.
5. Calculate total response time.
6. Categorize response performance.
7. Search incidents by location.
8. Store records in a DBMS.
9. Generate response-time reports.
10. Identify locations with longer average response times.
11. Identify peak emergency periods.
12. Provide data-driven resource allocation observations.

## 4. Scope
### Included
- Emergency incident registration
- Time validation
- Response-time calculation
- Dispatch-delay calculation
- Categorization
- Location search
- Database storage
- Aggregated analysis
- Report generation

### Not included
- Real-time GPS tracking
- Live ambulance dispatch
- Patient diagnosis
- Hospital bed management
- Automatic emergency decisions

## 5. Technologies
| Component | Technology |
|---|---|
| Programming | Python 3 |
| Database | SQLite |
| Query language | SQL |
| Python DB interface | sqlite3 |
| Time processing | datetime |
| Statistical calculation | statistics.mean |

## 6. System Modules
### Module 1 – Data Input
Collects incident ID, location, call time, dispatch time and arrival time.

### Module 2 – Validation
Checks:
- ID and location are not empty.
- Time follows HH:MM format.
- Dispatch is not before the call.
- Arrival is not before dispatch.

### Module 3 – Response Calculation
Dispatch Delay = Dispatch Time − Call Time

Response Time = Arrival Time − Call Time

### Module 4 – Categorization
Project thresholds:
- 0–10 minutes: Low Response Time
- 11–15 minutes: Moderate Response Time
- >15 minutes: High Response Time

### Module 5 – DBMS
Each valid incident is stored in the `incidents` table. Incident ID is the primary key.

### Module 6 – Search
Users can retrieve incidents for a particular zone/location.

### Module 7 – Reporting
The system calculates:
- Total incidents
- Average response time
- Minimum response time
- Maximum response time
- Average dispatch delay
- Category counts
- Location-wise averages
- Peak emergency hour
- High-response incidents

## 7. Database Design
Table: `incidents`

| Field | Type | Constraint | Purpose |
|---|---|---|---|
| incident_id | VARCHAR/TEXT | PRIMARY KEY | Unique incident |
| location | VARCHAR/TEXT | NOT NULL | Emergency zone |
| call_time | TIME/TEXT | NOT NULL | Time emergency call received |
| dispatch_time | TIME/TEXT | NOT NULL | Time ambulance dispatched |
| arrival_time | TIME/TEXT | NOT NULL | Arrival time |
| response_time | INTEGER | NOT NULL | Arrival − call |
| dispatch_delay | INTEGER | NOT NULL | Dispatch − call |
| category | VARCHAR/TEXT | NOT NULL | Response category |
| created_at | TIMESTAMP | DEFAULT | Record creation time |

### Primary Key
`incident_id` uniquely identifies each emergency incident.

### Indexes
Indexes are created on `location` and `call_time` to improve common searches and analysis.

## 8. Algorithm
1. Start.
2. Initialize database and table.
3. Display menu.
4. Accept incident details.
5. Validate the incident ID and location.
6. Parse all times in HH:MM format.
7. Convert times into minutes.
8. Check dispatch >= call.
9. Check arrival >= dispatch.
10. Calculate dispatch delay.
11. Calculate response time.
12. Assign category.
13. Insert valid record into database.
14. Allow search/report operations.
15. Display analysis.
16. Exit.

## 9. Pseudocode
```
START
CREATE incidents table if it does not exist

REPEAT
    DISPLAY menu
    READ choice

    IF choice = ADD
        READ incident ID, location, call, dispatch, arrival
        VALIDATE all fields
        CONVERT times to minutes

        IF dispatch < call
            DISPLAY invalid time
        ELSE IF arrival < dispatch
            DISPLAY invalid time
        ELSE
            dispatch_delay = dispatch - call
            response_time = arrival - call

            IF response_time <= 10
                category = LOW
            ELSE IF response_time <= 15
                category = MODERATE
            ELSE
                category = HIGH

            STORE record in DBMS
            DISPLAY result
        END IF

    ELSE IF choice = SEARCH
        READ location
        QUERY database
        DISPLAY matching incidents

    ELSE IF choice = REPORT
        QUERY aggregate data
        DISPLAY statistics and interpretation

    ELSE IF choice = EXIT
        STOP
END REPEAT
```

## 10. Sample Calculation
Given:
- Incident ID: E205
- Location: Zone 4
- Call Time: 14:10
- Dispatch Time: 14:14
- Arrival Time: 14:28

Dispatch Delay:
14:14 − 14:10 = 4 minutes

Response Time:
14:28 − 14:10 = 18 minutes

Since 18 > 15:
Category = High Response Time

This exactly demonstrates the calculation requested in the project statement.

## 11. Sample Dataset
| ID | Zone | Call | Dispatch | Arrival | Dispatch Delay | Response | Category |
|---|---|---|---|---|---:|---:|---|
| E201 | Zone 1 | 08:05 | 08:07 | 08:15 | 2 | 10 | Low |
| E202 | Zone 2 | 09:20 | 09:24 | 09:35 | 4 | 15 | Moderate |
| E203 | Zone 3 | 10:10 | 10:12 | 10:22 | 2 | 12 | Moderate |
| E204 | Zone 4 | 12:40 | 12:45 | 12:55 | 5 | 15 | Moderate |
| E205 | Zone 4 | 14:10 | 14:14 | 14:28 | 4 | 18 | High |
| E206 | Zone 2 | 15:30 | 15:32 | 15:43 | 2 | 13 | Moderate |
| E207 | Zone 1 | 17:15 | 17:18 | 17:27 | 3 | 12 | Moderate |
| E208 | Zone 3 | 18:05 | 18:11 | 18:28 | 6 | 23 | High |
| E209 | Zone 4 | 19:20 | 19:22 | 19:42 | 2 | 22 | High |
| E210 | Zone 2 | 20:10 | 20:16 | 20:25 | 6 | 15 | Moderate |

For this sample:
- Total incidents = 10
- Average response time = 15.5 minutes
- Minimum response time = 10 minutes
- Maximum response time = 23 minutes
- Average dispatch delay = 3.6 minutes
- Low = 1
- Moderate = 6
- High = 3

Location averages:
- Zone 1 = 11.00 minutes
- Zone 2 = 14.33 minutes
- Zone 3 = 17.50 minutes
- Zone 4 = 18.33 minutes

The sample therefore shows Zone 4 with the highest average response time, followed by Zone 3. This is a result for the demonstration dataset only, not a real-world conclusion.

Peak emergency hour in the sample is the hour with the largest number of recorded calls. The program calculates it automatically rather than hard-coding it.

## 12. SQL Queries for Demonstration
### Create table
```
CREATE TABLE incidents (...);
```

### Display all records
```
SELECT * FROM incidents ORDER BY call_time;
```

### Search a location
```
SELECT * FROM incidents
WHERE LOWER(location) = LOWER('Zone 4');
```

### Average response
```
SELECT ROUND(AVG(response_time), 2)
FROM incidents;
```

### Location-wise analysis
```
SELECT location,
       ROUND(AVG(response_time), 2) AS average_response_time,
       COUNT(*) AS incident_count
FROM incidents
GROUP BY location
ORDER BY average_response_time DESC;
```

### High response incidents
```
SELECT incident_id, location, response_time
FROM incidents
WHERE category = 'High Response Time'
ORDER BY response_time DESC;
```

### Peak hour
```
SELECT substr(call_time, 1, 2) AS hour,
       COUNT(*) AS emergency_calls
FROM incidents
GROUP BY substr(call_time, 1, 2)
ORDER BY emergency_calls DESC;
```

## 13. Invalid Input Handling
Examples:
- `14:7` is rejected because the required format is HH:MM.
- Dispatch `14:05` with call `14:10` is rejected.
- Arrival `14:00` with dispatch `14:05` is rejected.
- Empty location is rejected.
- Duplicate incident ID is rejected.

This prevents inconsistent records from entering the database.

## 14. Analysis & Interpretation
### Longer response areas
Calculate average response time for every location. Locations with higher averages can be reviewed for distance, traffic, road conditions, ambulance availability and dispatch patterns.

### Peak emergency periods
Group call records by hour. The hour with the highest number of calls is reported as the peak recorded period in the dataset.

### Response performance
The report compares minimum, maximum and average response time and counts each category.

### Resource allocation observations
Possible operational areas for review include:
- Positioning ambulances closer to repeatedly high-response zones.
- Reviewing dispatch delays separately from travel delays.
- Studying traffic and road-access conditions.
- Checking ambulance availability during peak periods.
- Reviewing whether demand peaks are recurring across larger datasets.

These are analytical suggestions; actual emergency resource decisions require operational and clinical validation.

## 15. Test Cases
| Test | Input/Condition | Expected |
|---|---|---|
| TC01 | Valid E205 data | Store successfully |
| TC02 | Response = 10 min | Low |
| TC03 | Response = 15 min | Moderate |
| TC04 | Response = 16 min | High |
| TC05 | Dispatch earlier than call | Reject |
| TC06 | Arrival earlier than dispatch | Reject |
| TC07 | Invalid time format | Reject |
| TC08 | Duplicate incident ID | Reject |
| TC09 | Search existing zone | Display records |
| TC10 | Search unknown zone | No records message |

## 16. Advantages
- Simple user interface.
- Automatic calculations reduce arithmetic mistakes.
- Database provides persistent storage.
- Search is fast and organized.
- Reports support trend analysis.
- Validation improves data quality.
- Easily extendable.

## 17. Limitations
- Times are entered manually.
- No GPS/traffic integration.
- Same-day HH:MM data is assumed.
- Dataset quality affects analysis.
- Thresholds are project-defined and not a medical standard.
- SQLite is suitable for a prototype but a large production system would require stronger infrastructure, access control, backups and concurrency management.

## 18. Future Scope
1. Add GPS-based ambulance tracking.
2. Integrate live traffic information.
3. Add ambulance availability status.
4. Add hospital destination and handover time.
5. Add dashboards and graphs.
6. Add user login and role-based access.
7. Add automated alerts for repeated high response times.
8. Add larger historical datasets.
9. Add predictive analysis after sufficient historical data is collected.
10. Deploy with a web/mobile interface.

## 19. Conclusion
The Ambulance Response-Time Analysis System demonstrates how Python and a relational DBMS can be combined to solve a practical healthcare operations problem. The system stores emergency incidents, validates time information, calculates dispatch delay and response time, categorizes records, searches by location and produces analytical reports. The project provides a foundation that can later be extended with real-time GPS, traffic and dashboard capabilities.

## 20. Viva Questions and Answers

Q1. What is the main objective?
A. To analyze emergency call, dispatch and arrival times and identify response delays.

Q2. What is response time?
A. The elapsed time from receiving the emergency call to ambulance arrival.

Q3. What is dispatch delay?
A. The elapsed time from receiving the call to dispatching the ambulance.

Q4. Why use a DBMS?
A. To store records persistently and support organized insertion, searching, filtering and aggregation.

Q5. Why is incident_id a primary key?
A. Each incident needs a unique identifier, so duplicate records can be prevented.

Q6. Why is validation necessary?
A. Incorrect time sequences can produce meaningless response-time values.

Q7. What Python module is used for the database?
A. `sqlite3`.

Q8. What does `datetime.strptime()` do?
A. It converts a string in a specified format into a datetime object and helps validate time input.

Q9. How is response time calculated?
A. Response time = arrival time − call time.

Q10. How is dispatch delay calculated?
A. Dispatch delay = dispatch time − call time.

Q11. What is SQL?
A. Structured Query Language, used to create, retrieve, update and analyze relational database data.

Q12. What is `GROUP BY` used for?
A. It groups rows with the same value so aggregate functions such as AVG and COUNT can be applied.

Q13. Why use `AVG()`?
A. To calculate the average response time.

Q14. What is an index?
A. A database structure that can speed up searches on selected columns.

Q15. What happens if a duplicate incident ID is entered?
A. The database primary-key constraint rejects it and the program displays an error.

Q16. What is the difference between dispatch delay and response time?
A. Dispatch delay ends when the ambulance is dispatched; response time ends when it arrives.

Q17. Why is location analysis useful?
A. It can reveal areas where response times are consistently higher and may require further operational investigation.

Q18. What is the role of Python?
A. Input handling, validation, calculations, database operations and report generation.

Q19. What is the role of SQL/DBMS?
A. Persistent storage, retrieval, filtering and aggregation of incident records.

Q20. Is this a real emergency dispatch system?
A. No. It is an academic analytical prototype and should not be used for real emergency decisions without extensive validation, security, reliability and clinical/operational safeguards.

## 21. Presentation Flow
1. Introduce the problem.
2. Explain why response time matters.
3. Show the input fields.
4. Demonstrate the E205 calculation.
5. Show the database table.
6. Demonstrate location search.
7. Generate the report.
8. Explain average and peak-period analysis.
9. Show invalid-input handling.
10. Explain future scope.
11. Conclude with the Python + DBMS integration.

## 22. One-Minute Project Explanation
"My project is Ambulance Response-Time Analysis. The objective is to analyze emergency calls, dispatch times and ambulance arrival times to identify response delays. I developed the system using Python and SQLite DBMS. The program accepts an incident ID, location, call time, dispatch time and arrival time. It validates the time sequence, calculates dispatch delay and total response time, and categorizes the response as low, moderate or high according to project-defined thresholds. The records are stored in a relational database. The system can search incidents by location and generate reports showing average response time, high-response incidents, location-wise performance and peak emergency periods. The project can be extended with GPS, live traffic, ambulance availability and dashboards."

## 23. Important Note for Evaluation
The response-time thresholds in this academic project are demonstration thresholds. They should not be presented as official medical or ambulance-service standards unless the college specifically provides a standard to use.
