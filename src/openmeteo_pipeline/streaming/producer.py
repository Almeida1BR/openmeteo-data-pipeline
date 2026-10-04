import json
import os
from typing import Any

from confluent_kafka import Producer

TOPIC_NAME = "weather.forecast.hourly"
BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092",
)


def create_producer() -> Producer:
    producer_config = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "acks": "all",
        "enable.idempotence": True,
    }
    return Producer(producer_config)


def publish_weather_records(
    producer: Producer,
    records: list[dict[str, Any]],
    latitude: float,
    longitude: float,
) -> None:
    delivery_errors: list[str] = []

    def delivery_report(error: Any, message: Any) -> None:
        if error is not None:
            delivery_errors.append(str(error))

    for record in records:
        record_with_location = {
            "latitude": latitude,
            "longitude": longitude,
            **record,
        }

        producer.produce(
            TOPIC_NAME,
            key=f"{latitude:.4f},{longitude:.4f}|{record['time']}",
            value=json.dumps(record_with_location).encode("utf-8"),
            on_delivery=delivery_report,
        )
        producer.poll(0)

    remaining = producer.flush(timeout=10)
    if remaining > 0:
        raise TimeoutError(
            f"Falha ao enviar {remaining} mensagens para o Kafka."
        )

    if delivery_errors:
        raise RuntimeError(
            f"Falha na entrega de mensagens: {'; '.join(delivery_errors)}"
        )
