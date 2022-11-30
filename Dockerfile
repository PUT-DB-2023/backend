# syntax=docker/dockerfile:1
FROM python:3.11.0-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

COPY . .