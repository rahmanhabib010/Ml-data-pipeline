
# Dive into Real-Time Data: An End-to-End Streaming Pipeline Solution with Kafka, InfluxDB, and Grafana!

This project demonstrates development of  a portable, end-to-end streaming data pipeline using Docker Compose and create dashboards for real-time data visualization. The pipeline is containerized for easy deployment and management, making it highly portable and scalable.
 
## Tools Used:

- **Docker**: For containerizing all the services.
- **Docker Compose Plugin**: To orchestrate multi-container Docker applications.
- **Kafka**: For building a distributed streaming platform.
- **Zookeeper**: Used to coordinate distributed systems like Kafka.
- **KSQL**: For real-time stream processing with SQL on Kafka.
- **InfluxDB**: A time series database to store and query the streaming data.
- **Grafana**: To visualize and create dashboards from the data stored in InfluxDB.

## Deployment Steps:

### Prerequisites
- Ubuntu 20.04 VM.
- [Docker](https://docs.docker.com/desktop/install/linux/) installed on your system.
- [Docker Compose plugin](https://docs.docker.com/compose/install/linux/) installed.
- Python.
- influxdb-client.
- confluent-kafka.

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Generate KSQL Commands File**
- Navigate to the ksql/device_count directory and run the Python script to generate the necessary KSQL commands file:

```bash
cd ksql/device_count
python gen_sql.py
```

3. **Build and Start Services**
- Navigate to the docker directory and use Docker Compose to build and start all services:

```bash
cd docker
sudo docker compose -f docker-compose.yaml up -d
```
This will start all the required services:

- Kafka
- Zookeeper
- KSQL
- InfluxDB v2
- Grafana

4. **Check Running Containers**
- Ensure all services are up and running:

```bash
sudo docker ps -a
```
5. **Run producer and consumer script**
- Navigate to the producer directory and run *producer.py* file to read data from json file as well as publish it to an input Kafka topic:

```bash
cd producer
python producer.py -i time_series_data.json -t time
```
- Navigate to the consumer directory and run *consumer.py* file to consume data from Kafka output topic when available and writes it to InfluxDB:

```bash
cd consumer
python consumer.py 
```

6. **Access influxDB v2**
- To check ip of the influxdB container:

```bash
sudo docker inspect <container_name> | grep "IPAddress"
```
- To access influxdB container:
 ```bash
sudo docker exec -it <influxDB_container_name> /bin/bash
or
sudo docker exec -it <influxDB_container_id> /bin/bash
```
- Before running "influx" CLI command from the containier:
 ```bash
export INFLUX_TOKEN=<admin-token>
```
- To check list of token, bucket:
```bash
influx auth list
influx bucket list
```
- To create new bucket and delete a bucket:
```bash
influx bucket create --name <bucket_name> --org <organization_name> --retention <retention_period>
influx delete --bucket <bucket_name> --start '1970-01-01T00:00:00Z' --stop '2026-10-10T00:00:00Z' --org <organization_name>
```
- To run continous query from influxdB for displaying received data:
```bash
cd influxDB
python run_query.py
```
7. **Access KSQL**

- To access KSQL container:
 ```bash
sudo docker exec -it <KSQL_container_name> /bin/bash
or
sudo docker exec -it <KSQL_container_id> /bin/bash
```
- To start KSQL CLI:
 ```bash
ksql http://ksql-server:8090
```
- To create a new stream associated with *'kafka-topic'*:
```bash
CREATE STREAM <stream_name> (
    time VARCHAR,
    value DOUBLE,
    label VARCHAR
) WITH (
    KAFKA_TOPIC=<'kafka-topic'>,
    VALUE_FORMAT='JSON'
);
```
- To check Existing Streams:
```bash
LIST STREAMS;
```
- To Query the Stream:
```bash
SELECT * FROM <stream_name>;
SELECT * FROM <stream_name> LIMIT 10;
```
- To exit KSQL CLI:
```bash
EXIT;
```
8. **Access Grafana**

- Open a browser and go to http://localhost:3000 to access Grafana.
- Log in using the default credentials:
  - **Username**: `admin`
  - **Password**: `admin`
- Set up a data source for InfluxDB and start building dashboards.

9. **Stop Services**
- To stop and remove all running containers:
```bash
cd docker
sudo docker compose -f docker-compose.yaml down
```

## Acknowledgments

This project was inspired by the article "[Streaming Data Pipeline using Kafka, KSQL, InfluxDB, and Grafana](https://medium.com/@ketulsheth2/streaming-data-pipeline-using-kafka-ksql-influxdb-and-grafana-8a934569fcb9)" by Ketul Sheth. I appreciate the valuable insights and guidance provided in the article, which helped shape this project.



