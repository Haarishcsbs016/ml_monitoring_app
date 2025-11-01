import pandas as pd
import time
import streamlit as st

# Load dataset once
df = pd.read_csv("sensor_data.csv")

st.title("AI-Based Fault Detection System")

# Simulate streaming row-by-row
placeholder = st.empty()

for i, row in df.iterrows():
    data = {
        "timestamp": row["timestamp"],
        "temperature": row["temperature"],
        "pressure": row["pressure"],
        "vibration": row["vibration"],
        "current": row["current"],
        "fault_status": row["fault_status"]
    }

    with placeholder.container():
        st.write("### Current Sensor Readings:")
        st.json(data)
    
    # Wait for 1 second between updates
    time.sleep(1)
