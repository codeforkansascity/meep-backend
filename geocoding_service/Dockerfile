FROM python:3.7.5-buster

WORKDIR /geocoding_service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY config config

COPY src src

WORKDIR src

CMD ["python", "run.py", "/geocoding_service/config/config.json"]
