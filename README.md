# MQTT Mosquitto-Paho Project

A Python-based MQTT communication system using the Paho MQTT client library and Mosquitto broker for IoT sensor data transmission.

## Overview

This project demonstrates MQTT publish-subscribe messaging patterns for IoT applications. It includes a subscriber client that listens to sensor topics and logs incoming data with timestamps.

## Features

- **MQTT Subscriber**: Listens to sensor data on `sensors/#` topic pattern
- **JSON Message Handling**: Parses JSON payloads with fallback for raw data
- **Logging System**: Records messages with ISO timestamps
- **Topic-based File Logging**: Creates separate log files per topic
- **Graceful Shutdown**: Clean exit on keyboard interrupt

## Prerequisites

- Python 3.7+
- Mosquitto MQTT Broker
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://chatgpt.com/c/6929a155-0ae8-832f-b77c-444cc1751afe
cd Mosqitto-Paho
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create logs directory:
```bash
mkdir logs
```

## Configuration

Edit the configuration variables in `subscriber.py`:

```python
BROKER = "localhost"     # MQTT broker address
PORT = 1883             # MQTT broker port
STUDENT_ID = <Your student ID> # Your student ID
LOGFILE = "logs/subscriber_log.txt"  # Main log file
```

## Usage

### Starting the Mosquitto Broker

```bash
# Windows (if installed via installer)
net start mosquitto

# Or run directly
mosquitto -v
```

### Running the Subscriber

```bash
python subscriber.py
```

The subscriber will:
- Connect to the MQTT broker
- Subscribe to all topics under `sensors/`
- Display received messages in console
- Log messages to files in the `logs/` directory

### Testing with Mosquitto Client

Publish test messages:
```bash
# JSON message
mosquitto_pub -h localhost -t sensors/temperature -m '{"value": 23.5, "unit": "C"}'

# Raw message
mosquitto_pub -h localhost -t sensors/humidity -m "65%"
```

## Log Format

### Console Output
```
Connected with result code 0
Received message on topic sensors/temperature: {'value': 23.5, 'unit': 'C'}
Logged entry: {'received_at': '2025-11-28T10:30:00.123456Z', 'topic': 'sensors/temperature', 'payload': {'value': 23.5, 'unit': 'C'}}
```

## License

This project is for educational purposes.
