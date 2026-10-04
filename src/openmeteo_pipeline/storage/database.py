import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://airflow:airflow@localhost:5432/airflow",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,)

class Base(DeclarativeBase):
    pass

def create_tables() -> None:
    from openmeteo_pipeline.storage.models import WeatherForecast

    Base.metadata.create_all(bind=engine,
    tables=[WeatherForecast.__table__])

