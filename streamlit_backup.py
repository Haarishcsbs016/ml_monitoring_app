import streamlit as st
import time
import joblib

# Load the trained model
model = joblib.load("fault_detection_model.pkl")

from src.data_acquisition import update_live_feed
from src.rule_engine import load_rules, evaluate_rules, combine_with_ai
from src.ai_model import load_model, predict_fault
from src.db import SimpleDB


st.set_page_config(page_title="Machine Health Dashboard")

st.title("Machine Health Dashboard — Prototype")

db = SimpleDB()

placeholder = st.empty()

@st.cache_data
def get_rules(path="rules.json"):
    try:
        return load_rules(path)
    except Exception:
        # default example
        return [
            {"id": "r1", "fault_type": "Overheating", "severity": 5, "conditions": [{"field": "temperature", "op": ">", "value": 80}, {"field": "vibration", "op": ">", "value": 5}]},
            {"id": "r2", "fault_type": "Leakage", "severity": 4, "conditions": [{"field": "pressure", "op": "<", "value": 30}, {"field": "current", "op": ">", "value": 10}]},
        ]


rules = get_rules()

st.sidebar.header("Demo Controls")
interval = st.sidebar.slider("Update interval (s)", 0.1, 5.0, 1.0)
equipment = st.sidebar.text_input("Equipment ID", "EQ-1")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Live Sensor Reading")
    live_box = st.empty()

with col2:
    st.subheader("Fault Status")
    status_box = st.empty()

model = None
try:
    model = load_model("model.joblib")
except Exception:
    model = None

feed = update_live_feed(interval=interval, equipment_id=equipment)
for reading in feed:
    live_box.json(reading)
    db.save_sensor_data(reading)
    rule_eval = evaluate_rules(reading, rules)
    ai_out = {"class": "Normal", "confidence": 0.0}
    if model is not None:
        import pandas as pd

        df = pd.DataFrame([{
            k: v for k, v in reading.items() if k in ("temperature", "pressure", "vibration", "current")
        }])
        pred = predict_fault(model, df)[0]
        ai_out = pred

    final = combine_with_ai(ai_out, rule_eval)
    status_box.write(final)
    time.sleep(0.01)


import streamlit as st

st.write("✅ Streamlit is working — file loaded successfully")
