RUN apt-get -q update && apt-get -qy install netcat

FROM python:3.8-alpine

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    # CLI alias for developer convenience for those more used to ll instead of ls.
    # The normal way of shelling in doesn't load the profile though so you have to use
    # the -l option: `docker container exec -it meep-backend_api_1 /bin/ash -l`
    && echo 'alias ll="'ls -lah'"' >> /etc/profile

RUN pip install pipenv

WORKDIR /meep/api/src
COPY . .
RUN pipenv install
ENV APP_SETTINGS env.test.cfg 
ENV FLASK_ENV test

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()" ]

CMD ["pipenv", "run", "db_operations.py", "reset", "test"]