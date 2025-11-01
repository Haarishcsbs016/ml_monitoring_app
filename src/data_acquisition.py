import time
import json
import random
from datetime import datetime
from typing import Dict, Generator, Optional

import pandas as pd


def simulate_sensor_data(equipment_id: str = "EQ-1") -> Dict:
    """Generate a single simulated sensor reading.

    Returns JSON-like dict with timestamp and sensor fields.
    """
    ts = datetime.utcnow().isoformat() + "Z"
    data = {
        "timestamp": ts,
        "equipment_id": equipment_id,
        "temperature": round(random.normalvariate(60, 5), 2),
        "pressure": round(random.normalvariate(50, 8), 2),
        "vibration": round(abs(random.normalvariate(1.0, 0.8)), 3),
        "current": round(abs(random.normalvariate(5.0, 1.5)), 3),
    }
    # Occasionally inject an anomaly
    if random.random() < 0.02:
        data["temperature"] += random.uniform(20, 40)
        data["vibration"] += random.uniform(4, 8)
    return data


def read_sensor_data(source: Optional[str] = None) -> Dict:
    """Placeholder for reading from real sensors.

    If `source` is None, fall back to simulated data.
    """
    if source is None:
        return simulate_sensor_data()
    # TODO: implement actual sensor reading (MQTT/HTTP/Modbus) based on source
    return simulate_sensor_data()


def fetch_from_dataset(path: str) -> pd.DataFrame:
    """Read CSV dataset into a DataFrame.

    Expects columns similar to the simulated data.
    """
    return pd.read_csv(path)


def store_raw_data(data: Dict, path: str = "raw_sensor_data.jsonl") -> None:
    """Append a JSON-line entry to a local file for raw data archival."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")


def update_live_feed(interval: float = 1.0, equipment_id: str = "EQ-1") -> Generator[Dict, None, None]:
    """Generator that yields simulated sensor readings at specified interval (seconds).

    Use in demos or to feed downstream processors.
    """
    try:
        while True:
            reading = simulate_sensor_data(equipment_id=equipment_id)
            yield reading
            time.sleep(interval)
    except GeneratorExit:
        return
