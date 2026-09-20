-- Ambulance Response-Time Analysis
-- SQLite / standard SQL-compatible schema

CREATE TABLE IF NOT EXISTS incidents (
    incident_id VARCHAR(20) PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    call_time TIME NOT NULL,
    dispatch_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    response_time INTEGER NOT NULL,
    dispatch_delay INTEGER NOT NULL,
    category VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_incident_location
ON incidents(location);

CREATE INDEX IF NOT EXISTS idx_incident_call_time
ON incidents(call_time);

-- Useful DBMS queries for demonstration:

-- 1. View all incidents
SELECT * FROM incidents ORDER BY call_time;

-- 2. Search by location
SELECT * FROM incidents
WHERE LOWER(location) = LOWER('Zone 4');

-- 3. Find high response-time incidents
SELECT incident_id, location, response_time, category
FROM incidents
WHERE category = 'High Response Time'
ORDER BY response_time DESC;

-- 4. Average response time
SELECT ROUND(AVG(response_time), 2) AS average_response_time
FROM incidents;

-- 5. Average response time by location
SELECT location,
       ROUND(AVG(response_time), 2) AS average_response_time,
       COUNT(*) AS incident_count
FROM incidents
GROUP BY location
ORDER BY average_response_time DESC;

-- 6. Peak hour
SELECT substr(call_time, 1, 2) AS hour,
       COUNT(*) AS emergency_calls
FROM incidents
GROUP BY substr(call_time, 1, 2)
ORDER BY emergency_calls DESC;

-- 7. Highest response time
SELECT *
FROM incidents
ORDER BY response_time DESC
LIMIT 1;
