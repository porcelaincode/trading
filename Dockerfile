FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/

ENV PYTHONPATH=/app/src

RUN pip install --no-deps -r requirements.txt

COPY ./src /app/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]