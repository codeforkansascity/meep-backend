FROM postgres:11.3
ENV POSTGRES_USER=meep POSTGRES_PASSWORD=supersafe POSTGRES_DB=meep_api

COPY data_cleaning/processed /data

COPY scripts /scripts
