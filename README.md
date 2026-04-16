# 🌱 Smart Irrigation System

This project is an IoT-based Smart Irrigation System that automates plant watering using soil moisture sensors, ESP8266 (NodeMCU), and a backend API.

## 🚀 Features
- Soil moisture monitoring via sensor
- Automatic watering control
- Microcontroller-based automation (ESP8266)
- REST API communication with backend
- Authentication using token-based requests
- Optional LLM integration for smart watering decisions

## 🛠️ Tech Stack
- MicroPython (ESP8266 / NodeMCU)
- Node.js (Backend API)
- Python (LLM service / optional logic layer)
- HTTP REST API
- JSON communication

## 🧠 System Architecture
Sensor → ESP8266 → Node.js API → (Optional Python LLM Service) → Decision → Actuator (Pump)

## ⚙️ How It Works
1. Sensor reads soil moisture
2. ESP8266 sends data to backend via HTTP
3. Backend processes data
4. System decides whether to activate irrigation
5. Water pump is triggered if needed

## 📌 Future Improvements
- Mobile app integration
- Real-time dashboard
- Advanced AI-based watering prediction

## 👨‍💻 Author
Fatima Aliyeva
