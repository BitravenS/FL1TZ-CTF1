FROM python:3.9-slim

WORKDIR /app

COPY out_of_sight.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

EXPOSE 1234

ENV FLAG="FL1TZ{look_again;)}"

CMD ["socat","-v","-T", "90", "TCP-LISTEN:1234,fork,reuseaddr,bind=0.0.0.0", "EXEC:'python3 out_of_sight.py'"]
