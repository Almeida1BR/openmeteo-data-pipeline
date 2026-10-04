from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from openmeteo_pipeline.storage.database import Base

class WeatherForecast(Base):

    __tablename__ = "weather_forecast"

    __table_args__ = (UniqueConstraint(
        "latitude",
        "longitude",
        "forecast_time",
        "collected_at",
        name="uq_weather_forecast_snapshot"
    ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    forecast_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    temperature_2m: Mapped[float | None] = mapped_column(Float)
    relative_humidity_2m: Mapped[float | None] = mapped_column(Float)
    precipitation_probability: Mapped[float | None] = mapped_column(Float)
    precipitation: Mapped[float | None] = mapped_column(Float)
    weather_code: Mapped[int | None] = mapped_column(Integer)
    wind_speed_10m: Mapped[float | None] = mapped_column(Float)


