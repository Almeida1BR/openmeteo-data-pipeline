import json
import os
from typing import Any

from confluent_kafka import Consumer, Message

from openmeteo_pipeline.storage.repository import save_weather_record
from openmeteo_pipeline.streaming.producer import TOPIC_NAME
from openmeteo_pipeline.storage.database import create_tables

BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092",
)
CONSUMER_GROUP_ID = os.getenv(
    "KAFKA_CONSUMER_GROUP_ID",
    "openmeteo-postgres-sink",
)


def create_consumer() -> Consumer:
    consumer = Consumer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "group.id": CONSUMER_GROUP_ID,
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([TOPIC_NAME])
    return consumer


def decode_weather_message(message: Message) -> dict[str, Any]:
    raw_value = message.value()
    if raw_value is None:
        raise ValueError("Mensagem Kafka vazia.")

    try:
        record = json.loads(raw_value.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Falha ao decodificar a mensagem Kafka: {error}"
        ) from error

    if not isinstance(record, dict):
        raise ValueError("Mensagem Kafka não é um objeto JSON válido.")

    return record


def poll_weather_record(
    consumer: Consumer,
    timeout: float = 1.0,
) -> tuple[Message, dict[str, Any]] | None:
    message = consumer.poll(timeout)
    if message is None:
        return None

    if message.error() is not None:
        raise RuntimeError(
            f"Erro ao consumir mensagem Kafka: {message.error()}"
        )

    return message, decode_weather_message(message)


def consume_weather_records(consumer: Consumer) -> None:
    try:
        while True:
            result = poll_weather_record(consumer)
            if result is None:
                continue

            message, record = result
            save_weather_record(record)

            committed_offsets = consumer.commit(
                message=message,
                asynchronous=False,
            )
            if committed_offsets is not None:
                commit_errors = [
                    str(partition.error)
                    for partition in committed_offsets
                    if partition.error is not None
                ]
                if commit_errors:
                    raise RuntimeError(
                        "Erro ao confirmar offset Kafka: "
                        + "; ".join(commit_errors)
                    )
    finally:
        consumer.close()


def main() -> None:
    create_tables()
    consumer = create_consumer()
    consume_weather_records(consumer)


if __name__ == "__main__":
    main()
