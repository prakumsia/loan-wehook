FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Cloud Run requires the app to listen on $PORT
CMD exec gunicorn -b :$PORT app:app
