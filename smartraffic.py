# Task 1 Calculate Average Waiting Time
def calculate_average_waiting_time(sensor_data):
    """
    Calculate average waiting time based on traffic sensor data.
    
    Args:
        sensor_data: List of tuples [(arrival_time, service_time), ...]
        where arrival_time is when vehicle arrives and service_time is 
        time needed to pass through intersection
    
    Returns:
        float: Average waiting time in seconds
    """
    if not sensor_data:
        return 0.0
    
    total_waiting_time = 0
    current_time = 0
    
    # Sort data by arrival time to process in correct order
    sorted_data = sorted(sensor_data, key=lambda x: x[0])
    
    for arrival_time, service_time in sorted_data:
        # Vehicle starts moving when either it arrives or intersection is free
        # and then takes service_time to pass
        start_time = max(current_time, arrival_time)
        completion_time = start_time + service_time
        
        # Waiting time = time service starts - arrival time
        waiting_time = start_time - arrival_time
        total_waiting_time += waiting_time
        
        # Update the time the intersection becomes free
        current_time = completion_time
    
    return total_waiting_time / len(sensor_data)

# Example usage
# Note: The original calculation was slightly off. 
# A more standard queueing theory approach is:
# Vehicle 1: Arrives 0, Service 5. Starts 0. Waits 0. Finishes 5.
# Vehicle 2: Arrives 2, Service 4. Starts 5. Waits 3. Finishes 9.
# Vehicle 3: Arrives 5, Service 3. Starts 9. Waits 4. Finishes 12.
# Vehicle 4: Arrives 8, Service 6. Starts 12. Waits 4. Finishes 18.
# Vehicle 5: Arrives 10, Service 4. Starts 18. Waits 8. Finishes 22.
# Total Wait: 0 + 3 + 4 + 4 + 8 = 19. Average = 19 / 5 = 3.8
traffic_data = [(0, 5), (2, 4), (5, 3), (8, 6), (10, 4)]
avg_wait = calculate_average_waiting_time(traffic_data)
print(f"Average waiting time: {avg_wait:.2f} seconds")

#---------------------------------------------------
# Task 2 Relational Expression for Traffic Threshold
def check_traffic_threshold(traffic_volume, threshold=50):
    """
    Determine if current traffic volume exceeds safe threshold.
    
    Args:
        traffic_volume: int, vehicles per minute
        threshold: int, safe threshold (default 50 vehicles per minute)
    
    Returns:
        bool: True if traffic exceeds threshold, False otherwise
    """
    exceeds_threshold = traffic_volume > threshold
    return exceeds_threshold

# Example usage
current_volume = 55
is_congested = check_traffic_threshold(current_volume)
print(f"Traffic volume: {current_volume} vehicles/min")
print(f"Exceeds threshold (>50): {is_congested}")
#--------------------------------------------------------
#  Task 3 Boolean Expression for Traffic Signal Control
def should_turn_green(avg_waiting_time, traffic_count):
    """
    Determine if traffic light should turn green based on conditions.
    
    Conditions:
    - Average waiting time > 60 seconds AND
    - Traffic count > 40 vehicles
    
    Args:
        avg_waiting_time: float, average waiting time in seconds
        traffic_count: int, number of vehicles waiting
    
    Returns:
        bool: True if light should turn green, False otherwise
    """
    turn_green = (avg_waiting_time > 60) and (traffic_count > 40)
    return turn_green

# Example usage
wait_time = 65
vehicle_count = 45
signal_decision = should_turn_green(wait_time, vehicle_count)
print(f"Average wait: {wait_time}s, Vehicle count: {vehicle_count}")
print(f"Should turn green: {signal_decision}")
#-----------------------------------------------------
# Task 4 Eager vs. Lazy Evaluation Comparison
## Eager Evaluation
def process_traffic_data_eager(sensor_readings):
    """
    Eager evaluation: Process all traffic data immediately and store in list.
    """
    # All data is processed immediately and stored in memory
    processed_data = [reading * 2 for reading in sensor_readings if reading > 10]
    return sum(processed_data)

# Lazy Evaluation
def process_traffic_data_lazy(sensor_readings):
    """
    Lazy evaluation: Process traffic data on-demand using generator.
    """
    # Generator yields values one at a time without storing entire list
    for reading in sensor_readings:
        if reading > 10:
            yield reading * 2

#-------------------------------
# Hybrid implementation strategy
def smart_traffic_management_system(sensor_stream, max_recent_readings=100):
    """
    Hybrid approach: Lazy evaluation for data processing,
    eager evaluation for critical decisions.
    
    This function is now a generator that yields decisions.
    
    Args:
        sensor_stream: An iterable of sensor readings (e.g., a list or generator)
        max_recent_readings: The size of the "window" for recent metrics.
    """
    
    # *** FIX: Initialize list OUTSIDE the loop ***
    # This list will hold the *raw* readings for wait time calculation.
    # Assuming readings are (arrival_time, service_time) tuples.
    recent_metrics = []
    
    print("\n--- Starting Smart Traffic Management System ---")
    
    # LAZY: Process continuous sensor stream
    # Note: process_traffic_data_lazy processes *numbers*, 
    # but calculate_average_waiting_time needs *tuples*.
    # I will assume sensor_stream provides the (arrival, service) tuples directly.
    
    for sensor_reading in sensor_stream:
        
        # EAGER: Store recent critical metrics in memory
        recent_metrics.append(sensor_reading)
        
        # Keep only last N readings for immediate analysis
        if len(recent_metrics) > max_recent_readings:
            recent_metrics.pop(0) # Remove the oldest reading
        
        # LAZY (on-demand calculation): Calculate metrics on-the-fly from the eager list
        avg_wait = calculate_average_waiting_time(recent_metrics)
        current_vehicle_count = len(recent_metrics)
        
        # EAGER: Make immediate signal control decision
        signal_decision = should_turn_green(avg_wait, current_vehicle_count)

        print(f"Reading: {sensor_reading}, Avg Wait: {avg_wait:.2f}s, Count: {current_vehicle_count}, Turn Green: {signal_decision}")

        # Yield the decision for this time step
        yield signal_decision

if __name__ == "__main__":
    # This block only runs when the script is executed directly,
    # not when it's imported as a module.
    
    # Example usage for the corrected hybrid system
    dummy_stream = [(i*2, 5 + (i % 3)) for i in range(150)]

    # Run the management system
    # iterate over the generator to get the decisions
    # added try-except to catch any runtime issues
    try:
        for decision in smart_traffic_management_system(dummy_stream, max_recent_readings=50):
            pass
    except Exception as e:
        print(f"Critical runtime issue: {e}")
