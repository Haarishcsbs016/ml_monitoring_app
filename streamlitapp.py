import pandas as pd
import streamlit as st
import time
import joblib

# --- Load the trained model ---
model = joblib.load("fault_detection_model.pkl")

# --- Load the dataset ---
df = pd.read_csv("sensor_data.csv")

st.set_page_config(page_title="AI-Based Fault Detection System")
st.title("⚙️ AI-Based Fault Detection Dashboard")

# --- Placeholder for live updates ---
placeholder = st.empty()
chart_placeholder = st.empty()

chart_data = pd.DataFrame(columns=["temperature", "pressure", "vibration", "current"])

# --- Stream data row by row ---
for i, row in df.iterrows():
    data = {
        "timestamp": row["timestamp"],
        "temperature": row["temperature"],
        "pressure": row["pressure"],
        "vibration": row["vibration"],
        "current": row["current"],
    }

    # --- Predict Fault using the model ---
    X_input = [[row["temperature"], row["pressure"], row["vibration"], row["current"]]]
    prediction = model.predict(X_input)[0]

    # --- Display readings and prediction ---
    with placeholder.container():
        st.subheader("📡 Current Sensor Readings")
        st.json(data)

        if prediction == 1:
            st.error("🚨 Fault Detected in Machine!")
        else:
            st.success("✅ Machine Operating Normally")

    # --- Update live chart ---
    chart_data.loc[len(chart_data)] = [row["temperature"], row["pressure"], row["vibration"], row["current"]]
    with chart_placeholder.container():
        st.line_chart(chart_data)

    time.sleep(1)  # wait for 1 second between updates
