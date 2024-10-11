import sys
import json
from confluent_kafka import Consumer, KafkaError
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime

# InfluxDB 2.x configuration
bucket = "logdb"
org = "vt-log"
token = "vt-token"
url = "http://172.23.0.6:8086"

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Kafka Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:29094',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

# Initialize Kafka Consumer
consumer = Consumer(consumer_conf)

# Subscribe to the 'log-input' topic
consumer.subscribe(['log-input'])

try:
    while True:
        print('Waiting for message...')
        msg = consumer.poll(1.0)  # Poll Kafka for new messages (1-second timeout)

        if msg is None:
            continue  # No new messages
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
            else:
                print(f"Error: {msg.error()}")
                break

        # Decode and print message value
        message_value = msg.value().decode('utf-8')
        print(f"Received message: {message_value}")

        # Parse the JSON message
        message_data = json.loads(message_value)

        # Create a point in InfluxDB format
        point = (
            Point("device_count")  # Measurement name in InfluxDB
            .tag("label", message_data.get("label"))  # Add tags like 'label' from the message
            .field("value", message_data.get("value"))  # Use 'value' from the message as a field
            .time(datetime.utcnow())  # Add timestamp from now
        )
        
        # Write the point to InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)
        print('Data written to InfluxDB:', point)

except KeyboardInterrupt:
    print('%% Aborted by user')

finally:
    # Close the Kafka consumer and InfluxDB client
    consumer.close()
    client.close()

