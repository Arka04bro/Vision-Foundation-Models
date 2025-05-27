# Real-Time Smoke Detection with YOLOv5 & Telegram Alerts

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker Build](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/r/yourdockerusername/smoke-detector)
[![Last commit](https://img.shields.io/github/last-commit/yourusername/yourrepo?color=red)](https://github.com/Arka04bro/Smoke_Detection-/commits/main)


<div align="center">
  <img src="Images/photo_5195330829839102595_y%20(1).jpg" alt="Smoke detected" width="600" style="border-radius:12px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);" />
  <p><i>Example of smoke detection with bounding boxes</i></p>
</div>

---

## Project Structure

```

project-root/
├── Activation/
│   ├── WEBCAM.py          # Real-time detection from webcam
│   └── ESP32-CAM.py       # Optional ESP32-CAM integration
├── Images/                # Sample images and screenshots
├── bestyolo.pt            # Custom YOLOv5 weights
├── Dockerfile             # Docker config
├── requirements.txt       # Dependencies
├── esp32cam\_code.ino      # ESP32 firmware
├── .env                   # Environment config
└── README.md              # This file

```

---

## Features

- Real-time smoke detection using **YOLOv5**
- Supports USB webcams and ESP32-CAM modules
- Telegram alerts with annotated images on detection
- Auto GPU/CPU detection for best performance
- Fully configurable via `.env`
- Docker-ready for easy deployment

---

## Configuration — `.env`

> [!TIP]
> Create a `.env` file in your project root with these variables:

```

BOT\_TOKEN=your\_telegram\_bot\_token
CHAT\_ID=-46705\*\*\*\*
CONFIDENCE\_THRESHOLD=0.4
CONSECUTIVE\_FRAMES\_THRESHOLD=15
USE\_GPU=True
MODEL\_PATH=bestyolo.pt

````

---

## Docker Usage

Build the image:

```bash
docker build -t smoke-detector .
````

Run (webcam default):

```bash
docker run --rm --env-file .env smoke-detector
```

Run with GPU support:

```bash
docker run --rm --env-file .env --gpus all smoke-detector
```

> \[!WARNING]
> When using GPU support, ensure your Docker and drivers support NVIDIA Container Toolkit.

---

## 🎥 Camera Source

By default:

```python
cv2.VideoCapture("/dev/video1")
```

Change device index in `Activation/WEBCAM.py` if needed.

---

## Use Cases

* Early smoke/fire warning systems
* Industrial safety monitoring
* Smart home security
* Edge AI prototyping

---

## Future Enhancements

* Web dashboard for live monitoring
* MQTT/IoT integration
* Video recording on detection
* Multi-camera support
* ESP32-CAM firmware integration

---

## License

Licensed under the MIT License — use and modify freely.

---

## Acknowledgements

* [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* OpenCV and PyTorch communities

---

## Maintainers

* **[Eraly Gainulla](https://eraly-ml.github.io/)** — SmartBilim School, Aktobe, Kazakhstan
* **[Khassanov Arkat](https://github.com/Arka04bro)** — 9th Gymnasium, Aktobe, Kazakhstan

---

If you want, I can help add testing instructions, CI/CD setup, or other sections.
