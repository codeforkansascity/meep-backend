FROM python:3.6
ENV FLASK_APP=main.py
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
