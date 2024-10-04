FROM python:3.10-slim

WORKDIR /app

COPY ./user-agents.txt /app

COPY ./results.txt /app

COPY ./app.py /app

CMD ["python", "app.py"]
