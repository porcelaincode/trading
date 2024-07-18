FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

# copy assets
COPY . .

ENV PYTHONPATH=/app/src

RUN pip install --no-cache-dir --no-deps -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]