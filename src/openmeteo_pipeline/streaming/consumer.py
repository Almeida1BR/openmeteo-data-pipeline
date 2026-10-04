import os
from confluent_kafka import Consumer
from openmeteo_pipeline.streaming.producer import TOPIC_NAME
import json
from typing import Any
from confluent_kafka import Message


BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092"
)
CONSUMER_GROUP_ID = os.getenv(
    "KAFKA_CONSUMER_GROUP_ID",
    "openmeteo-postgres-sink"
)

def create_consumer() -> Consumer:
    consumer = Consumer({
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": CONSUMER_GROUP_ID,
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    })

    consumer.subscribe([TOPIC_NAME])
    return consumer

def decode_weather_message(message: Message) -> dict[str, Any]:
    raw_value = message.value()

    if raw_value is None:
        raise ValueError("Mensagem Kafka vazia.")

    try:
        record = json.loads(raw_value.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Falha ao decodificar a mensagem Kafka: {error}") from error

        if not isinstance(record, dict):
            raise ValueError("Mensagem Kafka não é um objeto JSON válido.")

    return record

    def poll_weather_records(
        consumer: Consumer,
        timeout: float = 1.0
        ) -> tuple[Message, dict[str, Any]] | None:

        message = consumer.poll(timeout)

        if message is None:
            return None
        if message.error() is not None:
            raise RuntimeError(f"Erro ao consumir mensagem Kafka: {message.error()}")

        record = decode_weather_message(message)
        return message, record
