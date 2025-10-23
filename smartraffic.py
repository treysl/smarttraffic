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
    
    for arrival_time, service_time in sensor_data:
        # Vehicle starts moving when either it arrives or intersection is free
        current_time = max(current_time, arrival_time) + service_time
        
        # Waiting time = completion time - arrival time
        waiting_time = current_time - arrival_time
        total_waiting_time += waiting_time
    
    return total_waiting_time / len(sensor_data)

# Example usage
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
def smart_traffic_management_system(sensor_stream):
    """
    Hybrid approach: Lazy evaluation for data processing,
    eager evaluation for critical decisions.
    """
    # LAZY: Process continuous sensor stream
    for sensor_reading in process_traffic_data_lazy(sensor_stream):
        
        # EAGER: Store recent critical metrics in memory
        recent_metrics = []
        recent_metrics.append(sensor_reading)
        
        # Keep only last 100 readings for immediate analysis
        if len(recent_metrics) > 100:
            recent_metrics.pop(0)
        
        # LAZY: Calculate metrics on-the-fly
        avg_wait = calculate_average_waiting_time(recent_metrics)
        
        # EAGER: Make immediate signal control decision
        signal_decision = should_turn_green(avg_wait, len(recent_metrics))
        
        yield signal_decision
