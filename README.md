# 🌱 Smart Irrigation System (IoT + AI)

## 📌 Overview

This project is an IoT-based smart irrigation system that collects soil moisture data and uses AI to determine whether watering is required.

The system integrates embedded devices, backend services, and an AI decision layer.

---

## 🧠 Architecture

ESP8266 (MicroPython) → Node.js Backend → Flask AI Service (Ollama)

---

## ⚙️ Technologies

* MicroPython (ESP8266 NodeMCU)
* Node.js (REST API)
* Python Flask
* Ollama (LLM)
* HTTP & Token-based Authentication

---

## 🚀 Features

* 📡 Real-time soil moisture data collection
* 🔗 REST API communication between device and backend
* 🤖 AI-based irrigation decision system
* 🔐 Secure communication using authentication tokens
* 🧩 Multi-layer architecture (Device → Backend → AI)

---

## 📂 Project Structure

* `/device` – MicroPython code for ESP8266
* `/backend` – Node.js REST API
* `/ai-service` – Flask + Ollama integration

---

## ▶️ How It Works

1. ESP8266 collects soil moisture data
2. Data is sent to Node.js backend via HTTP
3. Backend forwards data to Flask AI service
4. LLM analyzes the data and decides whether watering is needed
5. Response is returned to the device

---

## 🎯 Future Improvements

* Mobile application integration
* Real-time dashboard
* Weather API integration

---

## 📬 Contact

Fatima – Backend Developer
