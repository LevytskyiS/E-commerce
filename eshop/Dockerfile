FROM python:3.10-slim-buster

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

