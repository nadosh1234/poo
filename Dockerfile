FROM python:3.10-slim

# تثبيت tesseract والاعتمادات اللي بيحتاجها OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# إعداد مكان المشروع
WORKDIR /app

# نسخ كل الملفات للمسار /app
COPY . .

# تثبيت الباكدجات
RUN pip install --no-cache-dir -r requirements.txt

# فتح البورت وتشغيل التطبيق بـ gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
