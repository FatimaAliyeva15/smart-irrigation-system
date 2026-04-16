import network
import urequests as requests
import time
import machine
import ubinascii
import json

# ====================
# WiFi Konfiqurasiyası
# ====================
WIFI_SSID = "enteskedu"
WIFI_PASSWORD = "ABC100200"


SERVER_URL = "http://192.168.0.168:5000/engine"  # Məsələn: http://192.168.1.100:3000/engine
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2N2ZkZmZmYmYwOTZiMzY1N2VlNzZlNzAiLCJ1c2VybmFtZSI6ImZhdGltYTEyMyIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc0NjY5MTMwNSwiZXhwIjoxNzQ2Njk0OTA1fQ.wbgGh2qY3h_RODlo4cu7X5lctMm4MsRk0x22if2D9p4"

# ====================
# Qurğunun Məlumatı
# ====================
STATUS = "active"
FIRMWARE_VERSION = "1.0"
IS_CONNECTED = True
DEEP_SLEEP_ENABLED = False

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('WiFi-yə qoşulur...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('WiFi qoşuldu:', wlan.ifconfig())
    return wlan

def get_device_info(wlan):
    mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
    ip = wlan.ifconfig()[0]
    return mac, ip

def register_engine(mac, ip):
    payload = {
        "mac_address": mac,
        "ip_address": ip,
        "status": STATUS,
        "firmware_version": FIRMWARE_VERSION,
        "isConnected": IS_CONNECTED,
        "wifi_ssid": WIFI_SSID,
        "wifi_signal_strength": -50,  # Bu sadəcə nümunədir
        "deep_sleep_enabled": DEEP_SLEEP_ENABLED
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": TOKEN
    }

    try:
        response = requests.post(SERVER_URL, headers=headers, data=json.dumps(payload))
        print("Cavab kodu:", response.status_code)
        print("Cavab:", response.text)
    except Exception as e:
        print("Xəta baş verdi:", e)

def main():
    wlan = connect_wifi()
    mac, ip = get_device_info(wlan)
    print("MAC:", mac)
    print("IP:", ip)

    register_engine(mac, ip)

    if DEEP_SLEEP_ENABLED:
        print("Deep sleep aktivdir. 10 saniyə gözləyib yatacaq.")
        time.sleep(10)
        machine.deepsleep()

main()
