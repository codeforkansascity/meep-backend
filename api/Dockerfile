FROM python:3.7.3-alpine

WORKDIR /meep/api

COPY requirements.txt .

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src /meep/api/src

WORKDIR src

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "wsgi"]
