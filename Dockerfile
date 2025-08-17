FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port
ENV PORT=8080

# Start Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
