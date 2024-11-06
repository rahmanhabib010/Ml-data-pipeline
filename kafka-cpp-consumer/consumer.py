import sys
import json
from confluent_kafka import Consumer, KafkaError
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# InfluxDB 2.x configuration
bucket = "logdb"
org = "vt-gmu-log"
token = "vt-gmu-token"
url = "http://10.0.0.117:8086"

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Kafka Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

# Initialize Kafka Consumer
consumer = Consumer(consumer_conf)

# Subscribe to the 'sinusoidal_values' topic
consumer.subscribe(['sinusoidal_values'])

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

        # Convert the message value to a float
        value = float(message_value)

        # Create a point in InfluxDB format
        point = (
            Point("sinusoidal_data")  # Measurement name in InfluxDB
            .field("value", value)  # Use the float value from the message
            .time(datetime.utcnow(), WritePrecision.NS)  # Add timestamp from now
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
