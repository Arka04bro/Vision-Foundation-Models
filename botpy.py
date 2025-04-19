import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import torch
import cv2
import telegram
import asyncio
import logging
import os
from dotenv import load_dotenv
import time  # Для использования задержки
'''
Code was written by Eraly Gainulla 15.01.2025 
'''
# Загрузка переменных c окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="smoke_detection.log"
)
logger = logging.getLogger(__name__)

# Параметры конфигурации
MODEL_PATH = os.getenv("/home/eraly/smoke-d/bestyolo.pt")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD"))
CONSECUTIVE_FRAMES_THRESHOLD = int(os.getenv("CONSECUTIVE_FRAMES_THRESHOLD", 10))
USE_GPU = os.getenv("USE_GPU", "True").lower() in ["true", "1", "yes"]

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
        model = torch.hub.load("ultralytics/yolov5", "custom", path='/home/eraly/smoke-d/bestyolo.pt', force_reload=True)
        device = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"
        model.to(device)
        logger.info(f"Модель успешно загружена на устройство: {device}")
        return model, device
    except Exception as e:
        logger.error(f"Ошибка при загрузке модели: {e}")
        raise

# Основная функция
async def main():
    # Инициализация Telegram-бота
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("Токен бота и/или chat_id не указаны. Проверьте настройки.")
        return
    bot = telegram.Bot(token=BOT_TOKEN)

    # Загрузка модели
    model, device = load_model()

    # Инициализация видеозахвата через указанный путь
    cap = cv2.VideoCapture("0")  # Используем корректный индекс устройства
    if not cap.isOpened():
        logger.error("Не удалось открыть камеру. Проверьте подключение.")
        return

    # Переменные для контроля уведомлений
    smoke_detected = False
    frames_without_smoke = 0
    last_detection_time = 0  # Время последнего обнаружения дыма

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Не удалось захватить кадр. Проверьте камеру.")
                break

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
                    await send_telegram_notification(bot, CHAT_ID, frame_path)  # Гарантируем выполнение уведомления
                    smoke_detected = True
                    frames_without_smoke = 0
                    last_detection_time = current_time  # Обновляем время последнего обнаружения

            if not smoke_present:
                frames_without_smoke += 1
                if smoke_detected and frames_without_smoke >= CONSECUTIVE_FRAMES_THRESHOLD:
                    smoke_detected = False

            # Изменение размера кадра на 648x480
            resized_frame = cv2.resize(frame, (1280, 720))

            # Отображение кадра с измененным размером
            cv2.imshow("Smoke Detection", resized_frame)
            if cv2.waitKey(1) == ord("q"):
                break

            await asyncio.sleep(0.01)  # Небольшая задержка для выполнения других задач

    except Exception as e:
        logger.error(f"Ошибка во время выполнения: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Программа завершена.")

if __name__ == "__main__":
    asyncio.run(main())
