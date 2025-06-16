import json
from kafka import KafkaConsumer
import pandas as pd
from utils import load_and_prepare_data
from model import train_model

# train offline
model = train_model(load_and_prepare_data())

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='fraud-detector'
)

for msg in consumer:
    record = msg.value
    df = pd.DataFrame([record]).drop('Class', axis=1)
    pred = model.predict(df)[0]
    print(f"Fraudulent: {'YES' if pred == -1 else 'NO'} | Amount: ${record['Amount']:.2f}")