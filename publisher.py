import time
import json
import random
import threading
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
CLIENT_PREFIX = "pub_client_"
STUDENT_ID = "12217558"


def make_payload(sensor_type, value):
    """
    Create a JSON payload for the given sensor type and value.
    :param sensor_type: Type of the sensor (e.g., "temperature", "humidity").
    :param value: The sensor reading value.
    :return: A dictionary representing the JSON payload.
    """
    return {
        "student_id": STUDENT_ID,
        "sensor": sensor_type,
        "value": value,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def temperature_value():
    """
    Generate a random temperature value between 20 and 30 degrees Celsius.
    """
    return round(random.uniform(20.0, 30.0), 2)


def humidity_value():
    """
    Generate a random humidity value between 30% and 90%.
    """
    return round(random.uniform(30.0, 90.0), 2)


def people_counter_value():
    """
    Generate a random people count between 0 and 50.
    """
    return random.randint(0, 50)


class SensorPublisher(threading.Thread):
    """
    Threaded MQTT publisher for a specific sensor type.
    """

    def __init__(self, client_id, topic, interval, value_func):
        """
        Initialize the SensorPublisher thread.
        :param client_id: Unique client ID for the MQTT publisher.
        :param topic: MQTT topic to publish to.
        :param interval: Time interval (in seconds) between publications.
        :param value_func: Function to generate the sensor value.
        """
        super().__init__(daemon=True)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
        self.topic = topic
        self.interval = interval
        self.value_func = value_func

    def run(self):
        """
        Start the MQTT publisher thread.
        """
        try:
            self.client.connect(BROKER, PORT)
        except Exception as e:
            print(f"Error in publisher {self.client._client_id.decode()}: {e}")
            return

        while True:
            value = self.value_func()
            payload = make_payload(self.topic, value)
            payload_str = json.dumps(payload)
            rc = self.client.publish(self.topic, payload_str)
            print(f"Published to {self.topic}: {payload_str} (rc={rc[0]})")
            time.sleep(self.interval)


if __name__ == "__main__":
    publishers = [
        SensorPublisher(
            client_id=CLIENT_PREFIX + "temp",
            topic="sensors/temperature",
            interval=5,
            value_func=temperature_value,
        ),
        SensorPublisher(
            client_id=CLIENT_PREFIX + "hum",
            topic="sensors/humidity",
            interval=7,
            value_func=humidity_value,
        ),
        SensorPublisher(
            client_id=CLIENT_PREFIX + "people",
            topic="sensors/people_counter",
            interval=10,
            value_func=people_counter_value,
        ),
    ]

    for publisher in publishers:
        publisher.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping publishers...")
