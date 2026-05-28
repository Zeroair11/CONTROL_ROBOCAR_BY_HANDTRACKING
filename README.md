# 🚗 CONTROL ROBOT CAR BY HAND TRACKING

Project điều khiển xe robot bằng **Hand Tracking + Machine Learning + ESP32 TCP Server**

---

## 📌 Mô tả

Hệ thống sử dụng camera + MediaPipe để nhận diện cử chỉ tay, sau đó:
- Python xử lý hand landmarks
- Model Machine Learning (RandomForest) dự đoán hành động
- Gửi lệnh qua TCP tới ESP32
- ESP32 điều khiển L298N để chạy xe

---

## 🧠 Công nghệ sử dụng

- Python
- OpenCV
- MediaPipe
- Scikit-learn (RandomForest)
- ESP32 (Arduino framework)
- TCP Socket
- L298N Motor Driver

---

## ⚙️ Chức năng

| Gesture | Command | Ý nghĩa |
|--------|--------|--------|
| F | Forward | Đi thẳng |
| B | Backward | Lùi |
| L | Left | Rẽ trái |
| R | Right | Rẽ phải |
| S | Stop | Dừng |


## 🚀 Cách chạy

### 1. ESP32
- Mở file `esp32.ino`
- Sửa WiFi:
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";

- Upload lên ESP32
- Mở Serial Monitor để lấy IP

---

### 2. Python AI

Cài thư viện:

```bash
pip install -r gesture_robot/requirements.txt
```

Chạy:

```bash
python gesture_robot/inference_classifier.py
```

---

## 🌐 Kết nối

Trong file Python:

```python
ESP32_IP = "192.168.x.x"
PORT = 1234
```

---

## 🔌 Phần cứng

- ESP32 DevKit
- L298N Motor Driver
- DC Motors
- Pin 6–12V
- Webcam (or PC CAM neu ban chay tren PC)

---

## ⚠️ Lưu ý

- ESP32 và PC phải chung WiFi
- Không dùng venv / dataset trong GitHub
- Nếu lag: giảm resolution camera

---

## 📷 Demo



---

## 👨‍💻 Tác giả

Project cá nhân phục vụ học tập và nghiên cứu IoT + AI + Robotics
```
Khoa va nhung nguoi ban
---
