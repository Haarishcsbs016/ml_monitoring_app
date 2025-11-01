import sqlite3
import json
from typing import Dict, Any, Optional, List


class SimpleDB:
    """Tiny SQLite wrapper for prototype data storage.

    Tables: sensor_data (json), fault_log (json), rules (json)
    """

    def __init__(self, path: str = "prototype.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY, ts TEXT, equipment_id TEXT, payload TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS fault_log (id INTEGER PRIMARY KEY, ts TEXT, equipment_id TEXT, payload TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS rules (id TEXT PRIMARY KEY, payload TEXT)")
        self.conn.commit()

    def save_sensor_data(self, data: Dict[str, Any]):
        c = self.conn.cursor()
        ts = data.get("timestamp")
        eq = data.get("equipment_id")
        payload = json.dumps(data)
        c.execute("INSERT INTO sensor_data (ts,equipment_id,payload) VALUES (?,?,?)", (ts, eq, payload))
        self.conn.commit()

    def save_fault_log(self, entry: Dict[str, Any]):
        c = self.conn.cursor()
        ts = entry.get("timestamp") or entry.get("ts") or ""
        eq = entry.get("equipment_id") or ""
        payload = json.dumps(entry)
        c.execute("INSERT INTO fault_log (ts,equipment_id,payload) VALUES (?,?,?)", (ts, eq, payload))
        self.conn.commit()

    def get_historical_data(self, date_range: Optional[Dict] = None) -> List[Dict]:
        # date_range ignored for prototype; return last 100 entries
        c = self.conn.cursor()
        rows = c.execute("SELECT payload FROM sensor_data ORDER BY id DESC LIMIT 100").fetchall()
        return [json.loads(r[0]) for r in rows]

    def save_ruleset(self, rules: List[Dict]):
        c = self.conn.cursor()
        for r in rules:
            c.execute("REPLACE INTO rules (id,payload) VALUES (?,?)", (r.get("id"), json.dumps(r)))
        self.conn.commit()

    def fetch_rules(self) -> List[Dict]:
        c = self.conn.cursor()
        rows = c.execute("SELECT payload FROM rules").fetchall()
        return [json.loads(r[0]) for r in rows]

    def fetch_model_results(self) -> List[Dict]:
        # placeholder: return last 50 fault_log entries
        c = self.conn.cursor()
        rows = c.execute("SELECT payload FROM fault_log ORDER BY id DESC LIMIT 50").fetchall()
        return [json.loads(r[0]) for r in rows]
