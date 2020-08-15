FROM python:3.7.3-alpine

ARG db_username=meep_user@ocs-db-pg
ARG db_name=meep
ARG db_host=ocs-db-pg.postgres.database.azure.com:5432
ARG db_password

WORKDIR /meep/api/src

COPY src/requirements.txt .

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==19.9.0 \
    # CLI alias for developer convenience for those more used to ll instead of ls.
    # The normal way of shelling in doesn't load the profile though so you have to use
    # the -l option: `docker container exec -it meep-backend_api_1 /bin/ash -l`
    && echo 'alias ll="'ls -lah'"' >> /etc/profile

ENV PYTHONPATH /meep/api/src
ENV DEV_DATABASE_URL postgresql+psycopg2://$db_username:$db_password@$db_host/$db_name


COPY . ..

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "wsgi"]
