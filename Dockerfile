FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg fonts-noto
    ffmpeg \
    fonts-thai-tlwg \
    fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
    
# ติดตั้ง Python dependencies ตาม requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . .

CMD ["python", "main.py"]
