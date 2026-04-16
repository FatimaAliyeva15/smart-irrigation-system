
import network
import urequests
import time
import json
import machine

# Wi-Fi Məlumatları
WIFI_SSID = 'enteskedu'
WIFI_PASSWORD = 'ABC100200'
API_URL = "http://192.168.0.140:5000/llm"  

# Wi-Fi bağlantısı
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print('Wi-Fi bağlıdır:', wlan.ifconfig())
        return

    print('Wi-Fi-ya qoşulmağa çalışılır...')
    wlan.connect(ssid, password)

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print('Wi-Fi qoşuldu:', wlan.ifconfig())
    else:
        print('Wi-Fi bağlantısı alınmadı!')

# Torpaq nəmliyi oxu
def read_moisture():
    adc = machine.ADC(0)  # A0 pin
    value = adc.read()
    percent = int((1024 - value) / 1024 * 100)
    print(f"Nəmlik: {percent}%")
    return percent

# Backend-ə göndər
def send_to_backend(moisture):
    try:
        payload = {"moisture": moisture}
        res = urequests.post(API_URL, json=payload)
        data = res.json()
        res.close()

        if data.get("should_water"):
            print("💧 Suvarma LAZIMDIR — Pompanı işə sal!")
        else:
            print("🚫 Suvarma lazım deyil.")
    except Exception as e:
        print("Backend xətası:", e)

def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    while True:
        moisture = read_moisture()
        send_to_backend(moisture)
        time.sleep(60)

main()