from datetime import timedelta

import pendulum
from airflow.sdk import DAG

from airflow.providers.standard.operators.python import PythonOperator

from openmeteo_pipeline.ingestion.pipeline import ingest_weather
from openmeteo_pipeline.streaming.producer import (create_producer, publish_weather_records)


def collected_and_publish_weather() -> None:
    latitude = -19.4658
    longitude = -44.2467

    records = ingest_weather(latitude, longitude)
    producer = create_producer()

    publish_weather_records(
    producer,
    records,
    latitude,
    longitude
    )

with DAG(
    dag_id= "openmeteo_weather_hourly",
    schedule = "0 * * * *",
    start_date = pendulum.datetime(2026,10,3, tz="America/Sao_Paulo"),
    catchup = False,
    max_active_runs = 1,
    default_args = {
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
    },
    tags = ["openmeteo", "clima"],
) as dag:
    publish_weather_task = PythonOperator(
        task_id = "collect_and_publish_weather",
        python_callable = collected_and_publish_weather,
    )
