from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy.dialects.postgresql import insert

from openmeteo_pipeline.storage.database import SessionLocal
from openmeteo_pipeline.storage.models import WeatherForecast

FORECAST_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def save_weather_record(record: dict[str, Any]) -> None:
    forecast_time = datetime.fromisoformat(record["time"]).replace(
        tzinfo=FORECAST_TIMEZONE
    )
    collected_at = datetime.fromisoformat(record["collected_at"])

    values = {
        "latitude": record["latitude"],
        "longitude": record["longitude"],
        "forecast_time": forecast_time,
        "collected_at": collected_at,
        "temperature_2m": record.get("temperature_2m"),
        "relative_humidity_2m": record.get("relative_humidity_2m"),
        "precipitation_probability": record.get("precipitation_probability"),
        "precipitation": record.get("precipitation"),
        "weather_code": record.get("weather_code"),
        "wind_speed_10m": record.get("wind_speed_10m"),
    }

    statement = insert(WeatherForecast).values(**values)
    statement = statement.on_conflict_do_nothing(
        constraint="uq_weather_forecast_snapshot"
    )

    with SessionLocal.begin() as session:
        session.execute(statement)
