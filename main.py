import sqlite3
from datetime import datetime
from statistics import mean

DB_NAME = "ambulance_response.db"

# Response-time categories used by this project:
# <= 10 minutes  -> Low Response Time
# 11-15 minutes -> Moderate Response Time
# > 15 minutes  -> High Response Time

def connect_db():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id TEXT PRIMARY KEY,
            location TEXT NOT NULL,
            call_time TEXT NOT NULL,
            dispatch_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            response_time INTEGER NOT NULL,
            dispatch_delay INTEGER NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_incident_location ON incidents(location)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_incident_call_time ON incidents(call_time)")
    conn.commit()
    conn.close()

def parse_time(value):
    """Return a datetime for HH:MM input; raise ValueError for invalid input."""
    return datetime.strptime(value.strip(), "%H:%M")

def time_to_minutes(value):
    return parse_time(value).hour * 60 + parse_time(value).minute

def validate_times(call_time, dispatch_time, arrival_time):
    # HH:MM is assumed to be on the same operational day.
    call = time_to_minutes(call_time)
    dispatch = time_to_minutes(dispatch_time)
    arrival = time_to_minutes(arrival_time)

    if dispatch < call:
        raise ValueError("Dispatch time cannot be earlier than call time.")
    if arrival < dispatch:
        raise ValueError("Arrival time cannot be earlier than dispatch time.")
    return call, dispatch, arrival

def calculate_times(call_time, dispatch_time, arrival_time):
    call, dispatch, arrival = validate_times(
        call_time, dispatch_time, arrival_time
    )
    dispatch_delay = dispatch - call
    response_time = arrival - call
    return response_time, dispatch_delay

def categorize(response_time):
    if response_time <= 10:
        return "Low Response Time"
    elif response_time <= 15:
        return "Moderate Response Time"
    return "High Response Time"

def add_incident(incident_id, location, call_time, dispatch_time, arrival_time):
    incident_id = incident_id.strip()
    location = location.strip()

    if not incident_id:
        raise ValueError("Incident ID cannot be empty.")
    if not location:
        raise ValueError("Location cannot be empty.")

    response_time, dispatch_delay = calculate_times(
        call_time, dispatch_time, arrival_time
    )
    category = categorize(response_time)

    conn = connect_db()
    try:
        conn.execute("""
            INSERT INTO incidents
            (incident_id, location, call_time, dispatch_time, arrival_time,
             response_time, dispatch_delay, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            incident_id, location, call_time.strip(), dispatch_time.strip(),
            arrival_time.strip(), response_time, dispatch_delay, category
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Incident ID already exists.")
    finally:
        conn.close()

    return response_time, dispatch_delay, category

def print_incident(row):
    print("-" * 70)
    print(f"Incident ID     : {row[0]}")
    print(f"Location        : {row[1]}")
    print(f"Call Time       : {row[2]}")
    print(f"Dispatch Time   : {row[3]}")
    print(f"Arrival Time    : {row[4]}")
    print(f"Response Time   : {row[5]} minutes")
    print(f"Dispatch Delay  : {row[6]} minutes")
    print(f"Category        : {row[7]}")

def list_incidents():
    conn = connect_db()
    rows = conn.execute("""
        SELECT incident_id, location, call_time, dispatch_time, arrival_time,
               response_time, dispatch_delay, category
        FROM incidents
        ORDER BY call_time, incident_id
    """).fetchall()
    conn.close()

    if not rows:
        print("\nNo incident records found.")
        return

    print("\nALL INCIDENT RECORDS")
    for row in rows:
        print_incident(row)
    print("-" * 70)

def search_by_location(location):
    conn = connect_db()
    rows = conn.execute("""
        SELECT incident_id, location, call_time, dispatch_time, arrival_time,
               response_time, dispatch_delay, category
        FROM incidents
        WHERE LOWER(location) = LOWER(?)
        ORDER BY response_time DESC
    """, (location.strip(),)).fetchall()
    conn.close()

    if not rows:
        print(f"\nNo incidents found for location: {location}")
        return

    print(f"\nINCIDENTS IN {location.strip()}")
    for row in rows:
        print_incident(row)
    print("-" * 70)

def generate_report():
    conn = connect_db()
    rows = conn.execute("""
        SELECT incident_id, location, call_time, dispatch_time, arrival_time,
               response_time, dispatch_delay, category
        FROM incidents
        ORDER BY response_time DESC
    """).fetchall()
    conn.close()

    if not rows:
        print("\nNo data available for report.")
        return

    response_values = [r[5] for r in rows]
    dispatch_values = [r[6] for r in rows]

    high = [r for r in rows if r[7] == "High Response Time"]
    moderate = [r for r in rows if r[7] == "Moderate Response Time"]
    low = [r for r in rows if r[7] == "Low Response Time"]

    print("\n" + "=" * 70)
    print("AMBULANCE RESPONSE-TIME REPORT")
    print("=" * 70)
    print(f"Total incidents          : {len(rows)}")
    print(f"Average response time    : {mean(response_values):.2f} minutes")
    print(f"Minimum response time    : {min(response_values)} minutes")
    print(f"Maximum response time    : {max(response_values)} minutes")
    print(f"Average dispatch delay   : {mean(dispatch_values):.2f} minutes")
    print(f"Low response incidents   : {len(low)}")
    print(f"Moderate incidents       : {len(moderate)}")
    print(f"High response incidents  : {len(high)}")

    if high:
        print("\nIncidents requiring attention (High Response Time):")
        for r in high:
            print(f"  {r[0]} | {r[1]} | {r[5]} min")

    # Location analysis
    by_location = {}
    for r in rows:
        by_location.setdefault(r[1], []).append(r[5])

    print("\nLOCATION ANALYSIS")
    location_stats = []
    for loc, values in by_location.items():
        location_stats.append((loc, mean(values), len(values), max(values)))
    for loc, avg, count, max_value in sorted(location_stats, key=lambda x: x[1], reverse=True):
        print(f"  {loc:<15} Avg: {avg:6.2f} min | Calls: {count:2d} | Max: {max_value:2d} min")

    # Peak emergency period by hour
    hour_counts = {}
    for r in rows:
        hour = int(r[2].split(":")[0])
        hour_counts[hour] = hour_counts.get(hour, 0) + 1

    peak_hour, peak_count = max(hour_counts.items(), key=lambda x: x[1])
    print(f"\nPeak emergency hour      : {peak_hour:02d}:00-{peak_hour:02d}:59 ({peak_count} incidents)")

    # Recommendations are data-driven, not automatic operational decisions.
    print("\nINTERPRETATION")
    worst_location = max(location_stats, key=lambda x: x[1])[0]
    print(f"- {worst_location} has the highest average response time in this dataset.")
    print("- High-response incidents should be reviewed for dispatch, traffic, distance, and availability factors.")
    print("- If dispatch delay is large, review call handling and ambulance allocation.")
    print("- If dispatch delay is small but response time is large, review travel distance, traffic, and route planning.")
    print("=" * 70)

def seed_sample_data():
    sample = [
        ("E201", "Zone 1", "08:05", "08:07", "08:15"),
        ("E202", "Zone 2", "09:20", "09:24", "09:35"),
        ("E203", "Zone 3", "10:10", "10:12", "10:22"),
        ("E204", "Zone 4", "12:40", "12:45", "12:55"),
        ("E205", "Zone 4", "14:10", "14:14", "14:28"),
        ("E206", "Zone 2", "15:30", "15:32", "15:43"),
        ("E207", "Zone 1", "17:15", "17:18", "17:27"),
        ("E208", "Zone 3", "18:05", "18:11", "18:28"),
        ("E209", "Zone 4", "19:20", "19:22", "19:42"),
        ("E210", "Zone 2", "20:10", "20:16", "20:25"),
    ]
    inserted = 0
    for record in sample:
        try:
            add_incident(*record)
            inserted += 1
        except ValueError:
            pass
    print(f"\nInserted {inserted} sample records.")

def add_incident_menu():
    print("\nENTER INCIDENT DETAILS")
    incident_id = input("Incident ID: ")
    location = input("Location/Zone: ")
    call_time = input("Call Time (HH:MM): ")
    dispatch_time = input("Dispatch Time (HH:MM): ")
    arrival_time = input("Arrival Time (HH:MM): ")

    try:
        response, delay, category = add_incident(
            incident_id, location, call_time, dispatch_time, arrival_time
        )
        print("\nRecord stored successfully.")
        print(f"Response Time : {response} minutes")
        print(f"Dispatch Delay: {delay} minutes")
        print(f"Category      : {category}")
    except ValueError as e:
        print(f"\nInvalid input: {e}")

def main():
    initialize_db()

    while True:
        print("\n" + "=" * 55)
        print("AMBULANCE RESPONSE-TIME ANALYSIS SYSTEM")
        print("=" * 55)
        print("1. Add emergency incident")
        print("2. View all incidents")
        print("3. Search incidents by location")
        print("4. Generate response report")
        print("5. Insert sample dataset")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_incident_menu()
        elif choice == "2":
            list_incidents()
        elif choice == "3":
            search_by_location(input("Enter location/zone: "))
        elif choice == "4":
            generate_report()
        elif choice == "5":
            seed_sample_data()
        elif choice == "6":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
