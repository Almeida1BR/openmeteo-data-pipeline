from typing import Any
from datetime import UTC, datetime
from openmeteo_pipeline.transformations.validate import validate_hourly_payload



def flatten_hourly(payload: dict[str, Any]) -> list[dict[str, Any]]:
    validate_hourly_payload(payload)
    hourly = payload["hourly"]
    times = hourly["time"]
    records = []
    collected_at = datetime.now(tz=UTC).isoformat()
    for index, timestamp in enumerate(times):
        record = {"time": timestamp,
        "collected_at": collected_at}
        for key, values in hourly.items():
            if key != "time":
                record[key] = values[index]
        records.append(record)
    return records
