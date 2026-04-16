import network
import urequests
import time
import json

# Wi-Fi bağlantısı
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('enteskedu', 'ABC100200')  # Wi-Fi şəbəkənizin adı və şifrəsi

while not wlan.isconnected():
    time.sleep(1)
    
print('Connected to Wi-Fi')

# Sensor məlumatı (sadəcə nümunə)
sensor_data = {
    'humidity': 40,
    'temperature': 25
}

# Server URL və Header-lar
url = "http://192.168.0.144:5000/irrigation"  # Flask serverinizin IP ünvanı və portu
headers = {'Authorization': 'Bearer your-token'}  # Əgər autentifikasiya tələb olunursa

# POST sorğusu göndəririk
response = urequests.post(url, json=sensor_data, headers=headers)

# Server cavabını ekrana çap edirik
print(response.text)
