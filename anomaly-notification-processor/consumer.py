import os
import time
from kafka import KafkaConsumer, errors
from kafka import KafkaConsumer


def main():
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("TOPIC", "postgres.public.hfj_res_ver")
    consumer = None
    while consumer is None:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers.split(","),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="anomaly-notification-consumer",
            )
        except errors.NoBrokersAvailable:
            print(
                f"Kafka brokers at {bootstrap_servers} not available, retrying..."
            )
            time.sleep(5)

    print(f"Consuming topic '{topic}' from {bootstrap_servers}")
    try:
        for msg in consumer:
            value = msg.value
            if isinstance(value, bytes):
                value = value.decode("utf-8", "ignore")
            print(f"{msg.topic}:{msg.partition}:{msg.offset}: {value}")
    except KeyboardInterrupt:
        print("Stopping consumer")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
