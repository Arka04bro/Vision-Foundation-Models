# 🔥 Real-Time Smoke Detection with YOLOv5 & Telegram Alerts

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker Build](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/r/yourdockerusername/smoke-detector)
[![Deployment Ready](https://img.shields.io/badge/deployment-ready-success)](#)

---

This project is a real-time smoke detection system using a custom-trained YOLOv5 model. Upon detecting smoke, it automatically sends alerts — including annotated frames — to a specified Telegram chat. Designed to run in a Docker container for easy deployment.

---

## 📁 Project Structure

```
project-root/
├── Activation/
│   ├── WEBCAM.py         # Real-time smoke detection using a webcam
│   └── ESP32-CAM.py      # Optional script for ESP32-CAM
├── Images
├── bestyolo.pt           # Custom-trained YOLOv5 model for smoke detection
├── Dockerfile            # Docker container definition
├── requirements.txt      # Python dependencies
├──esp32cam_code.ino      # Esp32 settings 
├── .env                  # Environment variables for model and Telegram
└── README.md             # Project documentation
```

---

## ⚙️ Features

- ✅ Real-time object detection (smoke)
- ✅ Works with USB webcam or ESP32-CAM
- ✅ Telegram alert system with annotated frame delivery
- ✅ GPU/CPU support with auto-detection
- ✅ Configurable via `.env` file
- ✅ Dockerized for cross-platform deployment

---

## 🔐 .env Configuration

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=-46705****
CONFIDENCE_THRESHOLD=0.4
CONSECUTIVE_FRAMES_THRESHOLD=15
USE_GPU=True
MODEL_PATH=bestyolo.pt
```

---

## 🐳 Docker Build Instructions

1. Build the Docker image:

```bash
docker build -t smoke-detector .
```

2. Run the container (default runs `WEBCAM.py`):

```bash
docker run --rm --env-file .env smoke-detector
```

3. (Optional) Run with GPU support:

```bash
docker run --rm --env-file .env --gpus all smoke-detector
```

---

## 🖥️ Camera Source

By default, the system uses:

```python
cv2.VideoCapture("/dev/video1")
```

Update this line in `WEBCAM.py` if using a different device.

---

## ✅ Use Case

- Smoke early warning system
- Industrial monitoring
- Smart home safety integration
- Research in edge AI and object detection

---

## 📌 Future Enhancements

- Web interface for real-time monitoring
- MQTT/IoT integration
- Video recording of incidents
- Multi-camera support
- ESP32-CAM full integration

---

## 📜 License

This project is licensed under the MIT License — use it freely, improve it, and share it.

---

## 🤝 Acknowledgements

- [Ultralytics](https://github.com/ultralytics/yolov5) for YOLOv5
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- OpenCV and PyTorch communities

---

### Maintained by 
- **[Eraly Gainulla](https://eraly-ml.github.io/)** _SmartBilim School, Aktobe, Kazakhstan_
- **[Khassanov Arkat](https://github.com/Arka04bro)** _9th gymnasium Aktobe, Kazakhstan_
