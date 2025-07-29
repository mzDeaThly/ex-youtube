FROM python:3.10-slim

# ติดตั้งระบบพื้นฐาน + ffmpeg + font ภาษาไทย
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    libfontconfig1 \
    libfreetype6 \
    fonts-thai-tlwg \
    ttf-dejavu \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# ทำงานในไดเรกทอรี /app
WORKDIR /app

# คัดลอก requirements.txt และติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์ทั้งหมด
COPY . .

# รันสคริปต์หลัก (เช่น ตั้ง cronjob ให้ Render เรียก main.py)
CMD ["python", "main.py"]
