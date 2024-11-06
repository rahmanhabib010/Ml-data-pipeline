#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <rdkafka.h>
#include "SinusoidalGenerator.h"

const std::string BROKER = "localhost:29092";  // Ensure this matches your Kafka broker
const std::string TOPIC = "sinusoidal_values";  // Change to your actual topic name
const int INTERVAL_MS = 100;  // Interval in milliseconds

// Error callback function
static void error_callback(rd_kafka_t* rk, int err, const char* reason, void* opaque) {
    std::cerr << "Kafka error: " << rd_kafka_err2str(static_cast<rd_kafka_resp_err_t>(err))
              << " (" << reason << ")" << std::endl;
}

// Delivery report callback function
static void delivery_report_callback(rd_kafka_t* rk, const rd_kafka_message_t* rkmessage, void* opaque) {
    if (rkmessage->err) {
        std::cerr << "Message delivery failed: " << rd_kafka_message_errstr(rkmessage) << std::endl;
    } else {
        std::cout << "Message delivered to topic " << rd_kafka_topic_name(rkmessage->rkt)
                  << " [" << rkmessage->partition << "] at offset " << rkmessage->offset << std::endl;
    }
}

int main() {
    rd_kafka_t* producer;
    rd_kafka_conf_t* conf;
    char errstr[512];

    // Initialize Kafka configuration
    conf = rd_kafka_conf_new();
    rd_kafka_conf_set_error_cb(conf, error_callback);
    rd_kafka_conf_set_dr_msg_cb(conf, delivery_report_callback);

    // Set broker configuration
    if (rd_kafka_conf_set(conf, "bootstrap.servers", BROKER.c_str(), errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        std::cerr << "Failed to configure broker: " << errstr << std::endl;
        return 1;
    }

    // Create producer instance
    producer = rd_kafka_new(RD_KAFKA_PRODUCER, conf, errstr, sizeof(errstr));
    if (!producer) {
        std::cerr << "Failed to create producer: " << errstr << std::endl;
        return 1;
    }

    rd_kafka_topic_t* topic = rd_kafka_topic_new(producer, TOPIC.c_str(), nullptr);

    // Sinusoidal generator instance
    SinusoidalGenerator generator(1.0, 1.0);  // Amplitude = 1.0, Frequency = 1 Hz

    while (true) {
        double value = generator.generateValue(INTERVAL_MS); // Generate a sinusoidal value
        std::string message = std::to_string(value);

        // Produce the message to the Kafka topic
        int err = rd_kafka_produce(
            topic,
            RD_KAFKA_PARTITION_UA,
            RD_KAFKA_MSG_F_COPY,
            const_cast<char*>(message.c_str()), message.size(),
            nullptr, 0,
            nullptr
        );

        // Check for errors in producing the message
        if (err) {
            std::cerr << "Failed to send message: " << rd_kafka_err2str(static_cast<rd_kafka_resp_err_t>(err)) << std::endl;
        } else {
            std::cout << "Sent: " << message << std::endl;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(INTERVAL_MS));  // Wait for the specified interval
    }

    // Clean up
    rd_kafka_topic_destroy(topic);
    rd_kafka_flush(producer, 1000);  // Wait for max 1000ms for messages to be delivered
    rd_kafka_destroy(producer);

    return 0;
}

