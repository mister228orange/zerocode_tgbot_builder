# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pyyaml aiosqlite telethon tonutils tonsdk

CMD ["python", "main.py"]
