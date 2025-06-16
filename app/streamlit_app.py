# app/streamlit_app.py

import streamlit as st
import pandas as pd
import json
from collections import deque
from kafka import KafkaConsumer
from streamlit_autorefresh import st_autorefresh

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page config
st.set_page_config(page_title="StreamFraud Dashboard", layout="wide")
st.title("StreamFraud: Real-Time Credit Card Fraud Monitoring")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Sidebar controls
st.sidebar.header("Controls")
show_only_frauds = st.sidebar.checkbox("Show only frauds", value=False)
max_rows = st.sidebar.slider("Max rows to keep", 10, 500, 100)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-refresh every 2 s
# This will rerun the script (and pull new Kafka records) at the specified interval.
st_autorefresh(interval=2000, key="auto_refresh")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Persistent buffer in session_state
if "buffer" not in st.session_state:
    st.session_state.buffer = deque(maxlen=max_rows)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Singleton KafkaConsumer
@st.cache_resource
def get_consumer():
    return KafkaConsumer(
        'transactions',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        consumer_timeout_ms=500,
        group_id='streamfraud-dashboard'
    )

consumer = get_consumer()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Poll new records and append to buffer
records = consumer.poll(timeout_ms=500, max_records=100)
for tp, msgs in records.items():
    for msg in msgs:
        st.session_state.buffer.append(msg.value)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Build DataFrame and render
df = pd.DataFrame(list(st.session_state.buffer))

if df.empty or "Class" not in df.columns:
    st.warning("Waiting for transactions…")
    st.stop()

if show_only_frauds:
    df = df[df["Class"] == 1]

total = len(df)
frauds = int(df["Class"].sum())
fraud_rate = round(frauds / total * 100, 2) if total else 0.0

c1, c2, c3 = st.columns(3)
c1.metric("Total Transactions", total)
c2.metric("Frauds Detected", frauds)
c3.metric("Fraud Rate (%)", f"{fraud_rate}")

st.subheader("Transaction Amount Trend")
st.line_chart(df["Amount"])

st.subheader("Live Transaction Feed")
styled = df.style.applymap(
    lambda v: "background-color: #ffcccc" if v == 1 else "",
    subset=["Class"]
)
st.dataframe(styled, use_container_width=True)