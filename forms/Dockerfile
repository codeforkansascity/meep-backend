ARG PORT=5000

FROM python:3.7.3-alpine

WORKDIR /meep/forms/src

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /meep/forms/src

COPY . ..

EXPOSE ${PORT}

CMD gunicorn --bind 0.0.0.0:${PORT} --reload wsgi
