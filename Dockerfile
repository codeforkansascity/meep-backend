FROM python:3.7.3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==19.9.0

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]
