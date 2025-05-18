import requests
import time
import random

# Configuration
ORION_URL = "http://orion:1026/v2/op/update"
SENSORS = [
    {"id": "SmokeSensor1", "type": "SmokeSensor"},
    {"id": "SmokeSensor2", "type": "SmokeSensor"},
    {"id": "SmokeSensor3", "type": "SmokeSensor"}
]
SMOKE_LEVEL_THRESHOLD = 80  # Threshold for triggering alerts

def generate_smoke_level():
    """Generate a random smoke level between 0 and 100."""
    return random.uniform(0, 100)

def send_sensor_data(sensor_id, smoke_level):
    """Send sensor data to the Orion Context Broker."""
    payload = {
        "actionType": "append",
        "entities": [
            {
                "id": sensor_id,
                "type": "SmokeSensor",
                "smokeLevel": {
                    "value": smoke_level,
                    "type": "Number",
                    "metadata": {
                        "dateCreated": {
                            "type": "DateTime",
                            "value": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                        }
                    }
                }
            }
        ]
    }

    response = requests.post(ORION_URL, json=payload)
    if response.status_code == 204:
        print(f"Sent data for {sensor_id}: smokeLevel={smoke_level}")
    else:
        print(f"Failed to send data for {sensor_id}: {response.text}")

def trigger_alert(sensor_id, smoke_level):
    """Send an alert to the Flask application."""
    alert_url = "http://flask-app:5000/alert"
    payload = {
        "id": sensor_id,
        "smokeLevel": smoke_level
    }
    response = requests.post(alert_url, json=payload)
    if response.status_code == 200:
        print(f"Alert triggered for {sensor_id}: smokeLevel={smoke_level}")
    else:
        print(f"Failed to trigger alert for {sensor_id}: {response.text}")

def main():
    while True:
        for sensor in SENSORS:
            sensor_id = sensor["id"]
            smoke_level = generate_smoke_level()

            # Send sensor data to Orion
            send_sensor_data(sensor_id, smoke_level)

            # Trigger alert if smoke level exceeds threshold
            if smoke_level > SMOKE_LEVEL_THRESHOLD:
                trigger_alert(sensor_id, smoke_level)

        # Wait for a short interval before simulating new data
        time.sleep(5)

if __name__ == "__main__":
    main()