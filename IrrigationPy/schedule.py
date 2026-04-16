import network
import urequests
import time
import json

# Wi-Fi və server parametrləri
SSID = "enteskedu"
PASSWORD = "ABC100200"
API_BASE_URL = "http://192.168.0.144:5000/valve"  # Backend server ünvanı

# Wi-Fi bağlantısı
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

# CRUD funksiyaları
def create_valve(name, status, schedule):
    data = {"name": name, "status": status, "schedule": schedule}
    headers = {'Content-Type': 'application/json'}
    try:
        resp = urequests.post(API_BASE_URL, data=json.dumps(data), headers=headers)
        print("Create:", resp.status_code, resp.text)
        resp.close()
    except Exception as e:
        print("Create xətası:", e)

def get_all_valves():
    try:
        resp = urequests.get(API_BASE_URL)
        print("Valves:", resp.status_code, resp.text)
        resp.close()
    except Exception as e:
        print("Get all valves xətası:", e)

def get_valve_by_id(valve_id):
    try:
        url = f"{API_BASE_URL}/{valve_id}"
        resp = urequests.get(url)
        print("Valve by ID:", resp.status_code, resp.text)
        resp.close()
    except Exception as e:
        print("Get by ID xətası:", e)

def delete_valve(valve_id):
    try:
        url = f"{API_BASE_URL}/{valve_id}"
        resp = urequests.delete(url)
        print("Delete:", resp.status_code, resp.text)
        resp.close()
    except Exception as e:
        print("Delete xətası:", e)



# Əsas funksiya
def main():
    connect_wifi(SSID, PASSWORD)
    time.sleep(2)

    # Test əməliyyatları
    create_valve("TestValve", "off", "12:00")
    time.sleep(2)

    get_all_valves()
    time.sleep(2)

    # Buraya mövcud valve ID-ni qoy
    valve_id = "PUT_REAL_VALVE_ID_HERE"
    get_valve_by_id(valve_id)
    time.sleep(2)

    delete_valve(valve_id)

if __name__ == "__main__":
    main()