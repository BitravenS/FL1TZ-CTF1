FROM python:3.9-slim

WORKDIR /app

COPY maze2-remote.py .
COPY flag.txt .

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

EXPOSE 1037

ENV FLAG="FL1TZ{look_again;)}"

CMD ["socat","-v","-T", "90", "TCP-LISTEN:1037,fork,reuseaddr,bind=0.0.0.0", "EXEC:'python3 maze2-remote.py'"]
