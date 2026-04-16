import network
import urequests
import time
import json

SSID = "ALHN-C947"         
PASSWORD = "YfbZQUCXy2" 


API_BASE_URL = "http://192.168.1.67:5000"


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print('Əvvəlki bağlantı tapıldı:', wlan.ifconfig())
        return

    print('Wi-Fi-ya qoşulmağa çalışılır...')
    wlan.connect(ssid, password)

    timeout = 10  
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print('Qoşuldu:', wlan.ifconfig())
    else:
        print('Wi-Fi bağlantısı alınmadı!')


def login(username, password):
    login_url = API_BASE_URL + "/user/login"
    credentials = {
        "username": username,
        "password": password
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = urequests.post(login_url, data=json.dumps(credentials), headers=headers)
        print("Status kod:", response.status_code)
        print("Server cavabı:", response.text)

        if response.status_code == 200:
            token = response.text.strip()  
            if token:
                print("Login uğurludur! Token:", token)
                return token
            else:
                print("Token boş gəldi!")
                return None
        else:
            print("Login alınmadı.")
            return None
    except Exception as e:
        print("Xəta baş verdi (login):", e)
        return None


connect_wifi(SSID, PASSWORD)

username = "fatima123"
password = "fatima123"
token = login(username, password)