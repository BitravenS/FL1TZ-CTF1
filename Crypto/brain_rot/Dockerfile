FROM python:3.9-slim

WORKDIR /app

COPY brain_rot.py .
COPY requirements.txt .
COPY ascii-art.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

EXPOSE 1001

ENV FLAG="FL1TZ{look_again;)}"

CMD ["socat","-v","-T", "90", "TCP-LISTEN:1001,fork,reuseaddr,bind=0.0.0.0", "EXEC:'python3 brain_rot.py'"]

