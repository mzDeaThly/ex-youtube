FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-noto \
    fonts-thai-tlwg \
    fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
