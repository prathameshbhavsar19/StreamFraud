import time, json
from kafka import KafkaProducer
from utils import load_and_prepare_data

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = load_and_prepare_data()
for _, row in df.iterrows():
    producer.send('transactions', value=row.to_dict())
    print("Produced:", row.to_dict())
    time.sleep(0.5)