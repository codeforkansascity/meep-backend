FROM kartoza/postgis

COPY xlsx /xlsx

COPY scripts /scripts

RUN rm /etc/postgresql/11/main/pg_hba.conf

COPY pg_hba.conf /etc/postgresql/11/main/pg_hba.conf

RUN apt-get -y update \
  && apt-get -y install postgis \
  && ls -la /usr/bin/ | grep shp \
