from typing import Dict, Any
import time


def combine_decisions(ai_result: Dict, rule_result: Dict) -> Dict:
    """Combine AI and rule outputs. Prefer rule if matched; otherwise use AI confidence thresholds."""
    if rule_result.get("matched"):
        return {"label": rule_result.get("fault_type"), "confidence": 1.0, "source": "rule"}
    # ai_result expected to be {'class': '...', 'confidence': 0.92}
    conf = ai_result.get("confidence", 0.0)
    label = ai_result.get("class", "Normal")
    return {"label": label, "confidence": conf, "source": "ai"}


def classify_fault_level(confidence: float, label: str) -> str:
    if label == "Normal":
        return "Normal"
    if confidence >= 0.8:
        return "Critical"
    if confidence >= 0.5:
        return "Warning"
    return "Informational"


def log_decision(db_conn, entry: Dict[str, Any]):
    # db_conn expected to implement save_fault_log
    try:
        db_conn.save_fault_log(entry)
    except Exception:
        # In prototypes we silently ignore DB failures
        pass


def trigger_alert(alert_fn, entry: Dict[str, Any]):
    # alert_fn is a callable that sends notifications; we call it for Critical/Warning
    level = entry.get("level", "Informational")
    if level in ("Critical", "Warning"):
        # include a small debounce or immediate trigger depending on infra
        alert_fn(entry)
