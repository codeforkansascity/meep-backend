FROM python:3.7.3-alpine

WORKDIR /meep/api/src

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    && pip install --upgrade pip \
    # CLI alias for developer convenience for those more used to ll instead of ls.
    # The normal way of shelling in doesn't load the profile though so you have to use
    # the -l option: `docker container exec -it meep-backend_api_1 /bin/ash -l`
    && echo 'alias ll="'ls -lah'"' >> /etc/profile

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /meep/api/src

COPY . ..

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "wsgi"]
