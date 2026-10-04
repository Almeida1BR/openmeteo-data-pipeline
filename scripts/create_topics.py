import os

from confluent_kafka.admin import AdminClient, NewTopic

TOPIC_NAME = "weather.forecast.hourly"
BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092",
)

def create_admin_client() -> AdminClient:
    return AdminClient({
        "bootstrap.servers": BOOTSTRAP_SERVERS,
    })

def create_topic(admin_client: AdminClient) -> None:
    topic = NewTopic(
        TOPIC_NAME,
        num_partitions=1,
        replication_factor=1,
    )

    futures = admin_client.create_topics([topic])

    for topic_name, future in futures.items():
        try:
            future.result()
            print(f"Tópico criado: {topic_name}")

        except Exception as error:
            print(f"Não foi possível criar o tópico {topic_name}: {error}")

if __name__ == "__main__":
    admin_client = create_admin_client()
    create_topic(admin_client)
