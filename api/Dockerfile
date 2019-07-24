FROM python:3.7.3-alpine

WORKDIR /meep/api/src

COPY src/requirements.txt .

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==19.9.0
# proj = Project(name='tasty cake')
# db.session.add(proj)
# db.session.commit()
ENV PYTHONPATH /meep/api/src
ENV TEST_DATABASE_URL postgresql://meep:supersafe@db:5432/meep_api

COPY . ..

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "wsgi"]
