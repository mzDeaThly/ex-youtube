FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ตรวจสอบ moviepy ติดตั้งสำเร็จไหม
RUN python -c "import moviepy.editor"

COPY . .

USER appuser

CMD ["python", "main.py"]
