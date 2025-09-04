import json
from collections import defaultdict
from datetime import datetime, timedelta


# Severity weights
def severity_weight(severity):
    return {"critical": 10, "warning": 5, "info": 1}.get(severity, 0)


def parse_alerts(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    assert "alerts" in data and isinstance(
        data["alerts"], list
    ), "Invalid alert data structure."
    return data["alerts"]


def filter_alerts(alerts, severity=None, service=None, minutes=None):
    now = datetime.utcnow()
    filtered = []
    for alert in alerts:
        if severity and alert["severity"] != severity:
            continue
        if service and alert["service"] != service:
            continue
        if minutes:
            alert_time = datetime.strptime(alert["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            if now - alert_time > timedelta(minutes=minutes):
                continue
        filtered.append(alert)
    return filtered


def group_alerts(alerts):
    groups = defaultdict(list)
    for alert in alerts:
        key = (alert["service"], alert["component"])
        groups[key].append(alert)
    return groups


def calculate_priority(alert_group):
    sev = max(severity_weight(a["severity"]) for a in alert_group)
    deviation = max(
        (a["value"] - a["threshold"]) / a["threshold"] * 100 for a in alert_group
    )
    num_components = len(set(a["component"] for a in alert_group))
    return sev + deviation + num_components


def main():
    alerts = parse_alerts("sample_alerts.json")
    # You can adjust or remove filters as needed
    filtered = filter_alerts(
        alerts, severity="critical", service="payment-processor", minutes=60
    )
    if not filtered:
        print("No alerts found matching the filter criteria.")
        # Optionally, show all groups for reference
        print("\nAll alert groups:")
        all_groups = group_alerts(alerts)
        for key, group in all_groups.items():
            print(f"Group: {key}, Alerts: {len(group)}")
        return
    groups = group_alerts(filtered)
    for key, group in groups.items():
        priority = calculate_priority(group)
        print(f"Group: {key}, Alerts: {len(group)}, Priority: {priority:.2f}")


if __name__ == "__main__":
    main()
