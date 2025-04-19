FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все нужные файлы
COPY Activation/ ./Activation/
COPY bestyolo.pt .
COPY .env .

# Установка рабочей директории
WORKDIR /Activation

# Устанавливаем переменные окружения из .env
ENV PYTHONUNBUFFERED=1

# По умолчанию запускаем WEBCAM.py
CMD ["python", "WEBCAM.py"]
