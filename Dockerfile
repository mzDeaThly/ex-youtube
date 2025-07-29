FROM python:3.10-slim

# ติดตั้ง ffmpeg และไลบรารีที่จำเป็น
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# สร้าง user ชื่อ appuser และสร้าง home directory
RUN useradd -m appuser

WORKDIR /app

# คัดลอกไฟล์ requirements.txt เข้า container
COPY requirements.txt .

# ติดตั้ง Python dependencies ด้วยสิทธิ์ root (จำเป็นตอนติดตั้ง)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# คัดลอกโค้ดโปรเจกต์ทั้งหมดเข้า container
COPY . .

# เปลี่ยน user เป็น appuser เพื่อความปลอดภัย
USER appuser

# รันไฟล์หลัก
CMD ["python", "main.py"]
