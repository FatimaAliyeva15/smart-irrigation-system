import network
import urequests
import time

# Wi-Fi bağlantısı
wifi_ssid = 'enteskedu'
wifi_password = 'ABC100200'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)

    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi")

# LLM serverinə məlumat göndərmək
def send_llm_request(temperature, humidity, weather):
    url = 'http://192.168.0.144:5000/ask-llm'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'temperature': temperature,
        'humidity': humidity,
        'weather': weather
    }

    response = urequests.post(url, json=payload, headers=headers)
    print(response.json())  # Cavabı ekrana yazdır

# Wi-Fi əlaqəsini qurun
connect_wifi()

# Torpaq rütubəti, temperatur və hava haqqında məlumatları göndərin
send_llm_request(temperature=25, humidity=40, weather="Sunny")
