FROM python:3.9-slim

WORKDIR /app

COPY workers/requirements.txt .

COPY workers/.env .

RUN pip install --no-cache-dir -r requirements.txt

COPY workers/main.py .

CMD ["python", "main.py"]