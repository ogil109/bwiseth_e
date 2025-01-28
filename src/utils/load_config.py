import json


class Config:
    def __init__(self, config_file) -> None:
        with open(config_file) as file:
            config_data = json.load(file)

        self.market_data = config_data["market_data"]
        self.kafka = config_data["kafka"]

    def get_kafka_config(self):
        return {
            "bootstrap.servers": self.kafka["bootstrap_servers"],
            "client.id": self.kafka["client_id"],
            "acks": self.kafka["acks"],
            "retries": self.kafka["retries"],
            "linger.ms": self.kafka["linger_ms"],
            "batch.size": self.kafka["batch_size"],
            "buffer.memory": self.kafka["buffer_memory"],
            "compression.type": self.kafka["compression_type"],
            "security.protocol": self.kafka["security_protocol"],
        }
