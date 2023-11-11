FROM python:3.10.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src
COPY migrations ./migrations
COPY alembic.ini .env .env.app requirements.txt src ./

RUN pip3 install --no-cache-dir -U -r requirements.txt
