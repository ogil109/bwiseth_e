import asyncio

from confluent_kafka import Producer

from src.ingestion.extract_kline import listen
from src.utils.load_config import Config

# Entry point for running the script
if __name__ == "__main__":
    # Load configuration from Docker root directory
    config = Config("/app/config.json")

    # Get Kafka configuration
    producer = Producer(config.get_kafka_config())

    # Start listening to the WebSocket
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen())
