from typing import Any
from openmeteo_pipeline.transformations.clean import flatten_hourly
from openmeteo_pipeline.ingestion.extract import extract_weather

def ingest_weather(latitude: float, longitude: float) -> list[dict[str, Any]]:
    payload = extract_weather(latitude, longitude)
    records = flatten_hourly(payload)
    return records
