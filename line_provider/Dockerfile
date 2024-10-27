FROM python:3.10-slim-buster

WORKDIR /code
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# CMD ["gunicorn", "run:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "127.0.0.1:8500"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7777"]