# استخدم Python رسمي من DockerHub
FROM python:3.10-slim

# تثبيت Tesseract و curl
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# ضبط مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY . .

# تثبيت مكتبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل التطبيق باستخدام gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
