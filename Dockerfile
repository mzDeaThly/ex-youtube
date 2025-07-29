# ใช้ base image แบบ full เพื่อลดปัญหา dependency
FROM python:3.10

# ติดตั้ง ffmpeg และ dependencies สำหรับ moviepy, pillow, และ fonts
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    libfontconfig1 \
    libfreetype6 \
    ttf-dejavu \
    fonts-thai-tlwg \
    && rm -rf /var/lib/apt/lists/*

# สร้าง user ปลอดภัย ไม่ใช้ root
RUN useradd -m appuser

# กำหนด directory สำหรับโปรเจกต์
WORKDIR /app

# คัดลอกไฟล์ dependencies และติดตั้ง Python package
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้า container
COPY . .

# ใช้ user ที่ไม่ใช่ root
USER appuser

# สั่งให้ container เริ่มรันด้วยคำสั่งนี้
CMD ["python", "main.py"]
