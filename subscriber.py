import json
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
STUDENT_ID = "12217558"


def on_connect(client, userdata, flags, rc):
    """
    Callback when the client connects to the broker.
    :param client: The MQTT client instance.
    :param userdata: The private user data.
    :param flags: Response flags sent by the broker.
    :param rc: The connection result.
    """
    print(f"Connected with result code {rc}")
    client.subscribe(f"sensors/#")


def on_message(client, userdata, msg):
    """
    Callback when a message is received from the broker.
    :param client: The MQTT client instance.
    :param userdata: The private user data.
    :param msg: The received MQTT message.
    """
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"Received message on topic {msg.topic}: {data}")
    except Exception:
        data = {"raw": payload}
        print(f"Received invalid JSON on topic {msg.topic}: {data}")

    entry = {
        "received_at": datetime.utcnow().isoformat() + "Z",
        "topic": msg.topic,
        "payload": data,
    }

    print(f"Logged entry: {entry}")
    print(f"{entry['received_at']} {entry['payload']}")


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "subscriber_client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped by user")
