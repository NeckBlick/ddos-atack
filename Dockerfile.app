FROM python:3.10-slim

WORKDIR /app

COPY ./app.py /app

CMD ["python", "main.py"]
