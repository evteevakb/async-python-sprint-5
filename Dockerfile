FROM python:3.10.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src
COPY .env .env.app requirements.txt src ./

RUN pip3 install --upgrade pip && pip3 install -U -r requirements.txt
