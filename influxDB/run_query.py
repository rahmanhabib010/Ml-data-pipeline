import json
from influxdb_client import InfluxDBClient, Point, WriteOptions
from datetime import datetime
import time

# InfluxDB credentials and configurations
INFLUXDB_URL = "http://172.23.0.6:8086"  # Replace with your InfluxDB URL
TOKEN = "vt-token"                       # Your token
ORG = "vt-log"                             # Your organization name
BUCKET = "logdb"                         # Your bucket name

# Create InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN)

# Function to query data continuously
def query_data_continuously():
    while True:
        # Define your query
        query = f'from(bucket: "{BUCKET}") |> range(start: -1m)'  # Adjust the range as needed
        
        # Execute the query
        result = client.query_api().query(query, org=ORG)
        
        # Process and print results
        print("Current Data in the Bucket:")
        for table in result:
            for record in table.records:
                print(f'Time: {record.get_time()}, Value: {record.get_value()}, Label: {record.values.get("label")}')
        
        # Wait for 5 seconds before the next query
        time.sleep(5)

# Call the function to start querying data
if __name__ == "__main__":
    query_data_continuously()


