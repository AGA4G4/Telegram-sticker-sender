FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    libssl-dev \
    libopenjp2-7 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
