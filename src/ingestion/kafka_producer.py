import json

from src.main import producer


# Handle websocket data to Kafka
def delivery_report(err, msg) -> None:
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_to_kafka(topic, data) -> None:
    producer.produce(topic, key=None, value=json.dumps(data), callback=delivery_report)
    producer.flush()


def process_kline_data(kline_data) -> None:
    # Process and send kline data to Kafka
    send_to_kafka("kline_topic", kline_data)
