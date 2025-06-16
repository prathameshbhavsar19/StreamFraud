FROM python:3.9-slim
WORKDIR /app
COPY app/ ./app/
COPY data/ ./data/
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["streamlit", "run", "app/streamlit_app.py"]