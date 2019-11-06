FROM python:3.7.5-buster

WORKDIR /geocoding_service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src

COPY src .

# CMD ["python", "run.py"]

CMD ["bin", "bash"]
