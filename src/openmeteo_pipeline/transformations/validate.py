from typing import Any

REQUIRED_HOURLY_FIELDS = [
    "time",
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation_probability",
    "precipitation",
    "weather_code",
    "wind_speed_10m",
]


def validate_hourly_payload(payload: dict[str, Any]) -> None:
    hourly = payload.get("hourly")
    if not isinstance(hourly, dict):
        raise ValueError("A resposta da API não contém um objeto 'hourly' válido.")

    missing_fields = [
        field for field in REQUIRED_HOURLY_FIELDS if field not in hourly
    ]
    if missing_fields:
        raise ValueError(
            f"Campos obrigatórios ausentes em 'hourly': {', '.join(missing_fields)}"
        )

    times = hourly["time"]
    if not isinstance(times, list) or not times:
        raise ValueError("O campo 'time' em 'hourly' deve ser uma lista não vazia.")

    for field in REQUIRED_HOURLY_FIELDS[1:]:
        values = hourly[field]
        if not isinstance(values, list):
            raise ValueError(f"O campo '{field}' não está em uma lista válida.")

        if len(values) != len(times):
            raise ValueError(
                f"O campo '{field}' tem {len(values)} valores, "
                f"mas 'time' tem {len(times)}."
            )
