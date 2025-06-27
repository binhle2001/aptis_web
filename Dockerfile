# Stage 1: Builder/Compile stage
FROM --platform=linux/amd64 python:3.9-slim-bullseye AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt
COPY ./db /app/db

# Stage 2: Runtime/Final stage
FROM --platform=linux/amd64 python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-cache search espeak
RUN apt-get install -y espeak
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:${PATH}"

COPY ./app /app/app 
COPY .env /app/.env 


EXPOSE 5055 
# Lệnh chạy uvicorn, trỏ đến instance FastAPI trong app/main.py
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 5055 --reload"]

