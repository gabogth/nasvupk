import os
from kafka import KafkaConsumer


def main():
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("TOPIC", "postgres.public.hfj_res_ver")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers.split(","),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="anomaly-notification-consumer",
    )
    print(f"Consuming topic '{topic}' from {bootstrap_servers}")
    for msg in consumer:
        value = msg.value
        if isinstance(value, bytes):
            value = value.decode("utf-8", "ignore")
        print(f"{msg.topic}:{msg.partition}:{msg.offset}: {value}")


if __name__ == "__main__":
    main()
