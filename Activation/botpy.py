import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import torch
import cv2
import telegram
import asyncio
import logging
import os
from dotenv import load_dotenv
import time
import requests
from io import BytesIO
import numpy as np
'''
Code was written by Eraly Gainulla 15.01.2025 
Updated for ESP32-CAM integration 20.04.2025 with Khassanov Arkat
'''

# Загрузка переменных c окружения
load_dotenv(dotenv_path=".env)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="smoke_detection.log"
)
logger = logging.getLogger(__name__)

# Параметры конфигурации
MODEL_PATH = os.getenv("MODEL_PATH", "bestyolo.pt")
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', ))
CONSECUTIVE_FRAMES_THRESHOLD = int(os.getenv('CONSECUTIVE_FRAMES_THRESHOLD', ))
USE_GPU = os.getenv("USE_GPU", "True").lower() in ["true", "1", "yes"]
ESP32CAM_IP = os.getenv("ESP32CAM_IP", "192.168.100.25")
ESP32CAM_STREAM_URL = f"http://{ESP32CAM_IP}/capture"  # URL для получения кадров с ESP32-CAM

# Функция для отправки уведомлений в Telegram 
async def send_telegram_notification(bot, chat_id, frame_path):
    try:
        await bot.send_message(chat_id=chat_id, text="Обнаружен дым!")
        with open(frame_path, "rb") as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo)
        logger.info("Уведомление отправлено в Telegram.")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")

# Функция для загрузки модели
def load_model():
    try:
        model = torch.hub.load("ultralytics/yolov5", "custom", path='bestyolo.pt', force_reload=True)
        device = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"
        model.to(device)
        logger.info(f"Модель успешно загружена на устройство: {device}")
        return model, device
    except Exception as e:
        logger.error(f"Ошибка при загрузке модели: {e}")
        raise

# Функция для получения кадра с ESP32-CAM
def get_esp32cam_frame():
    try:
        response = requests.get(ESP32CAM_STREAM_URL, timeout=5)
        if response.status_code == 200:
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return True, frame
        else:
            logger.error(f"Ошибка при получении кадра: HTTP {response.status_code}")
            return False, None
    except Exception as e:
        logger.error(f"Ошибка при подключении к ESP32-CAM: {e}")
        return False, None

# Основная функция
async def main():
    # Инициализация Telegram-бота
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("Токен бота и/или chat_id не указаны. Проверьте настройки.")
        return
    bot = telegram.Bot(token=BOT_TOKEN)

    # Загрузка модели
    model, device = load_model()

    # Переменные для контроля уведомлений
    smoke_detected = False
    frames_without_smoke = 0
    last_detection_time = 0  # Время последнего обнаружения дыма

    try:
        while True:
            # Получаем кадр с ESP32-CAM
            ret, frame = get_esp32cam_frame()
            if not ret:
                logger.error("Не удалось получить кадр с ESP32-CAM. Повторная попытка через 5 секунд...")
                await asyncio.sleep(5)
                continue

            # Выполнение инференса
            results = model(frame)
            detections = results.xyxy[0].cpu().numpy()

            smoke_present = False
            for det in detections:
                class_id = int(det[5])
                confidence = det[4]
                if class_id == 0 and confidence > CONFIDENCE_THRESHOLD:
                    smoke_present = True
                    x1, y1, x2, y2 = map(int, det[:4])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"Smoke: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Обработка уведомлений
            if smoke_present and not smoke_detected:
                current_time = time.time()
                if current_time - last_detection_time >= 10:  # Тайм-аут 10 секунд
                    frame_path = "smoke_detected.jpg"
                    cv2.imwrite(frame_path, frame)
                    await send_telegram_notification(bot, CHAT_ID, frame_path)
                    smoke_detected = True
                    frames_without_smoke = 0
                    last_detection_time = current_time

            if not smoke_present:
                frames_without_smoke += 1
                if smoke_detected and frames_without_smoke >= CONSECUTIVE_FRAMES_THRESHOLD:
                    smoke_detected = False

            # Изменение размера кадра для отображения
            resized_frame = cv2.resize(frame, (1280, 720))

            # Отображение кадра с измененным размером
            cv2.imshow("Smoke Detection - ESP32-CAM", resized_frame)
            if cv2.waitKey(1) == ord("q"):
                break

            await asyncio.sleep(0.1)  # Небольшая задержка для снижения нагрузки

    except Exception as e:
        logger.error(f"Ошибка во время выполнения: {e}")
    finally:
        cv2.destroyAllWindows()
        logger.info("Программа завершена.")

await main()
