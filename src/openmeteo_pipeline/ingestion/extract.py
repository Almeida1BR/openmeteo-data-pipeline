from typing import Any
import httpx

URL_API = "https://api.open-meteo.com/v1/forecast"

def extract_weather(latitude: float, longitude: float) -> dict[str, Any]:

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
        "temperature_2m,relative_humidity_2m,"
        "precipitation_probability,precipitation,"
        "weather_code,wind_speed_10m"
    ),
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1,
    }
    response = httpx.get(URL_API, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


