# StreamFraud

StreamFraud is a real-time credit card fraud detection system built using Apache Kafka, Streamlit, and an Isolation Forest anomaly detection model. It simulates transaction streaming from a static dataset and visualizes the results in a live dashboard.

---

## Architecture

![img.png](img.png)

1. **Producer**  
   Reads the static `creditcard.csv`, shuffles and scales features, then publishes each transaction as a JSON record to the Kafka topic `transactions`.

2. **Kafka Cluster**  
   - **Zookeeper** manages broker metadata.  
   - **Kafka Broker** stores and delivers the `transactions` topic to consumers.

3. **Consumer (fraud-detector)**  
   Subscribes to `transactions`, applies the trained Isolation Forest model, and logs fraud decisions.

4. **Streamlit Dashboard**  
   Subscribes to `transactions`, maintains a rolling window of records, and displays:
   - Total transactions
   - Fraud count & rate
   - Amount trend chart
   - Live, color-coded transaction table

---

## Performance Metrics

**Test set size**: 56,962 transactions (56,863 non-fraud, 99 fraud)  
**Overall accuracy**: **99.79%**

### Confusion Matrix

|                | Predicted 0 | Predicted 1 |
|----------------|-------------|-------------|
| **Actual 0**   | 56,825      | 38          |
| **Actual 1**   | 82          | 17          |

### Classification Report

| Class | Precision | Recall | F1-score | Support |
|------:|----------:|-------:|---------:|--------:|
|     0 |     0.9986 |  0.9993 |   0.9989 |   56,863 |
|     1 |     0.3091 |  0.1717 |   0.2208 |       99 |
| **Macro avg**    | 0.6538    | 0.5855   | 0.6099   |   56,962 |
| **Weighted avg** | 0.9974    | 0.9979   | 0.9976   |   56,962 |

---

## Features

- Real-time transaction simulation via Kafka  
- Anomaly detection with Isolation Forest  
- Live, interactive dashboard built with Streamlit  
- Fully containerized using Docker and Docker Compose  

---

## Project Structure

```
streamfraud/
├── app/
│   ├── producer.py          # Kafka producer
│   ├── consumer.py          # Kafka consumer + model inference
│   ├── streamlit_app.py     # Streamlit dashboard
│   ├── model.py             # Isolation Forest training
│   └── utils.py             # Data loading & preprocessing
├── data/
│   └── creditcard.csv       # Kaggle dataset
├── architecture.png         # System architecture diagram
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
└── docker-compose.yml       # Multi-container orchestration
```

---

## Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/streamfraud.git
   cd streamfraud
   ```

2. **Download the dataset**  
   From https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud  
   and place `creditcard.csv` into the `data/` directory.

3. **Build and launch**  
   ```bash
   docker-compose up --build
   ```

4. **View the dashboard**  
   Open <http://localhost:8501> in your browser.

---

## Tech Stack

- **Python**  
- **Apache Kafka** & **Zookeeper**  
- **Streamlit**  
- **scikit-learn**  
- **Docker** & **Docker Compose**

---

## Future Improvements

- Tune the Isolation Forest contamination for higher recall  
- Replace with autoencoders or supervised models  
- Add email/SMS alerts on anomaly detection  
- Persist results in a database (e.g. PostgreSQL, Elasticsearch)  
- User authentication and role-based access in the dashboard  

---

## License

This project is open-source under the MIT License.
