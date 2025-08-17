FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run will inject $PORT, so gunicorn must bind to it
CMD ["gunicorn", "-b", ":$PORT", "app:app"]
