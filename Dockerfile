FROM python:3.9-slim-bullseye as builder

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

COPY requirements.txt .

FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]