# Alert Processor Script

## Overview
This repository contains a Python script, `alert_processor.py`, designed to process, filter, group, and prioritize alert data from monitoring systems. The script is built to help SRE teams manage mission-critical infrastructure by quickly and accurately handling alerts.

## Scenario
Your team manages infrastructure where alerts must be processed efficiently. The script parses alert data, applies multiple filters, groups related alerts to reduce noise, and calculates incident priority using a weighted algorithm.

## Features
The script implements the following functionalities:

1. **Alert Data Processing**
    - Parses a sample alert data file (`sample_alerts.json`).
    - Filters alerts based on severity, service, and time window.
    - Groups related alerts (e.g., by service and component).
    - Calculates incident priority using a weighted algorithm.

2. **Sample Data Structure**
    - Alerts are stored in a JSON file with the following structure:
      ```json
      {
        "alerts": [
          {
            "id": "ALT-1023",
            "timestamp": "2024-04-28T09:15:22Z",
            "service": "payment-processor",
            "component": "api-gateway",
            "severity": "critical",
            "metric": "latency",
            "value": 3,
            "threshold": 2,
            "description": "API response time exceeded threshold"
          },
          // ... more alerts ...
        ]
      }
      ```

## Script Modules & Functions

### 1. `severity_weight(severity)`
Assigns a numeric weight to each severity level:
- `critical`: 10
- `warning`: 5
- `info`: 1

### 2. `parse_alerts(json_file)`
- Loads and validates the alert data from a JSON file.
- Ensures the structure contains an `alerts` list.

### 3. `filter_alerts(alerts, severity=None, service=None, minutes=None)`
- Filters alerts by severity, service, and time window (last X minutes).
- Returns only alerts matching all specified criteria.

### 4. `group_alerts(alerts)`
- Groups alerts by `(service, component)` to reduce noise.
- Returns a dictionary where each key is a tuple and the value is a list of alerts.

### 5. `calculate_priority(alert_group)`
Calculates a priority score for each group based on:
- **Severity**: Highest severity weight in the group.
- **Deviation from Threshold**: Maximum percentage deviation in the group.
- **Number of Components**: Count of unique components affected.

Formula:
```
priority = severity_weight + deviation_percentage + num_components
```

### 6. `main()`
- Loads alerts from `sample_alerts.json`.
- Applies filters (e.g., severity='critical', service='payment-processor', last 60 minutes).
- Groups filtered alerts and calculates priority for each group.
- Prints results to the console.

## Usage
1. Place your alert data in `sample_alerts.json`.
2. Run the script:
   ```bash
   python alert_processor.py
   ```
3. Adjust filter criteria in the `main()` function as needed.

## Customization
- Modify filter parameters in `main()` to suit your needs.
- Extend grouping or priority calculation logic as required.

## References
- See `Scenario.txt` for the full scenario and requirements.
- See `sample_alerts.json` for sample alert data.

---
