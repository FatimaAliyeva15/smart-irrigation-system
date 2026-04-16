import urequests
import network
import time

import network
import time

# Wi-Fi parametrləri
ssid = 'enteskedu'  # Wi-Fi şəbəkəsinin adı
password = 'ABC100200'  # Wi-Fi şifrəniz

# Wi-Fi-yə qoşulmaq
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Wi-Fi üçün status interfeysi
    wlan.active(True)  # Wi-Fi-ni aktiv et
    wlan.connect(ssid, password)  # Şəbəkəyə qoşul
    print('Wi-Fi-yə qoşulmağa çalışır...')
    
    # Qoşulma uğurlu olana qədər gözləyirik
    timeout = 10  
    start_time = time.time()
    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print("Wi-Fi-yə qoşulmaqda problem yaranıb.")
            return False
        time.sleep(1)
    
    print("Wi-Fi-yə qoşulundu!")
    print("IP ünvanı:", wlan.ifconfig()[0])  # IP ünvanını çap et
    return True

# Wi-Fi-yə qoşulma funksiyasını çağır
connect_wifi()


url = "http://192.168.0.146:5000/ask-llm"  # Node.js server IP və portu

data = {
    "temperature": 25,
    "moisture": 40
}

headers = {"Content-Type": "application/json"}

res = urequests.post(url, json=data, headers=headers)
print("Ollamadan cavab:", res.text)
