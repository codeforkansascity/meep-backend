FROM python:3.7.3-alpine

WORKDIR /meep/api/src

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==19.9.0

COPY . .
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "wsgi"]
