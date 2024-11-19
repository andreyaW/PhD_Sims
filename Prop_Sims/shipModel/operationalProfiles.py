# Sample Corvette Mission Profile

# Define mission phases
mission_profile = [
    {"phase": "Departure and Transit", "speed_knots": 15, "duration_hours": 6},
    {"phase": "Patrol and Surveillance", "speed_knots": 12, "duration_hours": 12},
    {"phase": "Intercept Hostile Vessel", "speed_knots": 28, "duration_hours": 2},
    {"phase": "Engagement and Evasion", "speed_knots": 18, "duration_hours": 1},
    {"phase": "Return to Base", "speed_knots": 15, "duration_hours": 6},
]

# Function to calculate total distance covered
def calculate_total_distance(profile):
    total_distance = 0
    for phase in profile:
        distance = phase



# Sample Patrol Craft Mission Profile

# Define mission phases
mission_profile = [
    {"phase": "Departure and Transit", "speed_knots": 18, "duration_hours": 4},
    {"phase": "Routine Patrol", "speed_knots": 12, "duration_hours": 10},
    {"phase": "High-Speed Intercept", "speed_knots": 35, "duration_hours": 1},
    {"phase": "Close Surveillance", "speed_knots": 8, "duration_hours": 3},
    {"phase": "Return to Base", "speed_knots": 18, "duration_hours": 4},
]



# --------------------------------------------------------------------------------------------

# Function to calculate total distance covered
def calculate_total_distance(profile):
    total_distance = 0
    for phase in profile:
        distance = phase["speed_knots"] * phase["duration_hours"]
        total_distance += distance
    return total_distance

# Function to display mission details
def display_mission_profile(profile):
    print("Sample Patrol Craft Mission Profile")
    print("-" * 40)
    for phase in profile:
        print(
            f"Phase: {phase['phase']}\n"
            f"  Speed: {phase['speed_knots']} knots\n"
            f"  Duration: {phase['duration_hours']} hours\n"
            f"  Distance Covered: {phase['speed_knots'] * phase['duration_hours']} nautical miles\n"
        )
    print("-" * 40)
    print(f"Total Distance Covered: {calculate_total_distance(profile)} nautical miles")

# Execute functions
display_mission_profile(mission_profile)
