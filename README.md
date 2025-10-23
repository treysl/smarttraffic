# SmartTraffic - smartraffic.py

This repository contains a single script, `smartraffic.py`, which demonstrates simple traffic-management helper functions and a small hybrid (eager + lazy) traffic management system prototype.

## Purpose

`smartraffic.py` is an educational and prototyping script that:

- Calculates average vehicle waiting time at an intersection using simple queue-processing logic.
- Checks whether current traffic volume exceeds a configurable threshold.
- Evaluates whether a traffic signal should turn green based on average waiting time and vehicle count.
- Demonstrates eager vs. lazy evaluation patterns for handling sensor data.
- Provides a small generator-based hybrid traffic management system that uses eager storage for recent metrics and lazy/on-demand calculations for decisions.

## Main functions

- `calculate_average_waiting_time(sensor_data)`
  - Inputs: `sensor_data` - list of tuples `[(arrival_time, service_time), ...]` where `arrival_time` and `service_time` are numbers (seconds).
  - Output: `float` average waiting time in seconds.
  - Notes: Sorts by arrival time and simulates FIFO service; returns `0.0` for empty input.

- `check_traffic_threshold(traffic_volume, threshold=50)`
  - Inputs: `traffic_volume` - integer vehicles per minute, `threshold` - integer threshold (default 50).
  - Output: `bool` indicating if `traffic_volume > threshold`.

- `should_turn_green(avg_waiting_time, traffic_count)`
  - Inputs: `avg_waiting_time` (seconds), `traffic_count` (number of vehicles waiting).
  - Output: `bool` - returns `True` when `avg_waiting_time > 60` AND `traffic_count > 40`.

- `process_traffic_data_eager(sensor_readings)`
  - Demonstrates eager evaluation by processing a list comprehension and returning a sum of processed readings that exceed a threshold.

- `process_traffic_data_lazy(sensor_readings)`
  - Demonstrates lazy evaluation by yielding processed readings one at a time using a generator.

- `smart_traffic_management_system(sensor_stream, max_recent_readings=100)`
  - Inputs: `sensor_stream` - iterable of `(arrival_time, service_time)` tuples; `max_recent_readings` - window size for recent metrics.
  - Output: generator that yields boolean signal decisions for each reading.
  - Behavior: Keeps an eager list of recent readings (bounded by `max_recent_readings`), computes average waiting time on demand, and yields whether the light should turn green.

## Example usage

The script contains an `if __name__ == "__main__":` block that demonstrates:

- Calculating average wait for a small sample dataset.
- Checking a traffic volume threshold.
- Deciding whether to turn a light green for a sample wait time and vehicle count.
- Running the `smart_traffic_management_system` generator on a dummy sensor stream of 150 readings (with a sliding window).

When executed directly, the script prints example outputs and iterates through the generator.

## How to run

From the repository root (requires Python 3.x):

```bash
python smartraffic.py
```

The script includes a small sleep at the top to simulate startup delay; remove or adjust `time.sleep(0.1)` if needed.

## Assumptions and notes

- `arrival_time` and `service_time` are assumed to be numeric values in seconds. `calculate_average_waiting_time` sorts by arrival time before simulation.
- The signal decision logic in `should_turn_green` is intentionally simple for demonstration and can be replaced with more sophisticated policies (e.g., weighted scoring, time-of-day adjustments, dynamic thresholds).
- `smart_traffic_management_system` expects tuples from `sensor_stream`. If your sensors produce different formats (e.g., raw counts or timestamps), adapt the preprocessing step accordingly.
- This is a prototype/educational script; it doesn't include logging, error handling for malformed inputs, or external integrations.

## Possible next steps

- Add unit tests for core functions (average waiting time, threshold checks, and generator behavior).
- Add type hints and input validation for robustness.
- Replace prints with structured logging and provide a CLI for different modes (demo, simulation, live).
- Integrate with real sensor data sources (MQTT, REST API, files) and implement persistence/metrics.
