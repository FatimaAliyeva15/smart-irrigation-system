import network
import time
import urequests
import ujson
import ubinascii
import machine
import json

# --- Konfiqurasiya ---
SSID = "ALHN-C947"
PASSWORD = "YfbZQUCXy2"
BASE_URL = "http://192.168.1.67:5000"
ENGINE_URL = f"{BASE_URL}/engine"
NODE_JS_SERVER_URL = f"{BASE_URL}/engine/assignEngineToUser"  # Əlavə etdim

TOKEN_ADMIN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2N2ZkZmZmYmYwOTZiMzY1N2VlNzZlNzAiLCJ1c2VybmFtZSI6ImZhdGltYTEyMyIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc0ODYwMTEwNCwiZXhwIjoxNzQ4NjA0NzA0fQ.VJU2o0jaK2hLDDmfWAzZ3n4XK0qb2PuJnJWrRFKCnVI"
TOKEN_USER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2N2ZlMDAxMmZmNWI1MmIwZjA1OWU2MzQiLCJ1c2VybmFtZSI6InppdmVyMTIzIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NDU4MjQ5OTksImV4cCI6MTc0NTgyNTg5OX0.xcJsEzU3OBMrY9ApLJOLhEGuCHwux7DKSBdMU-QrOPE"

# --- WiFi bağlantısı ---
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    retry = 0
    while not wlan.isconnected():
        if retry > 10:
            print("WiFi bağlantısı alınmadı. Yenidən başladılır...")
            machine.reset()
        print("WiFi-yə qoşulmağa çalışılır...")
        time.sleep(1)
        retry += 1

    ip = wlan.ifconfig()[0]
    mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
    print(f"Qoşuldu: IP: {ip}, MAC: {mac}")
    return ip, mac

# --- Header-lar ---
def get_headers(token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

# --- POST: Yeni cihaz əlavə et (yalnız admin) ---
def create_engine(ip, mac, token):
    if token != TOKEN_ADMIN:
        print("Yalnız admin cihaz əlavə edə bilər.")
        return
    data = {
        "ip_address": ip,
        "mac_address": mac,
        "status": 1,
        "firmware_version": "1.0",
        "wifi_ssid": SSID,
        "wifi_signal_strength": network.WLAN(network.STA_IF).status('rssi'),
        "isConnected": True,
        "deep_sleep_enabled": False
    }
    try:
        response = urequests.post(ENGINE_URL, data=ujson.dumps(data), headers=get_headers(token))
        print("POST cavabı:", response.status_code, response.text)
    except Exception as e:
        print("POST xətası:", e)

# --- GET: Bütün cihazlar (yalnız admin) ---
def get_all_engines(token):
    if token != TOKEN_ADMIN:
        print("Yalnız admin bütün cihazlara baxa bilər.")
        return
    try:
        response = urequests.get(ENGINE_URL, headers=get_headers(token))
        print("GET cavabı:", response.status_code, response.text)
    except Exception as e:
        print("GET xətası:", e)

# --- GET: İstifadəçinin öz cihazları (istifadəçi) ---
def get_user_engines(token):
    try:
        response = urequests.get(ENGINE_URL, headers=get_headers(token))
        print("İstifadəçi GET:", response.status_code, response.text)
    except Exception as e:
        print("GET xətası:", e)

# --- GET: ID ilə cihaz gətir (admin və ya istifadəçi) ---
def get_engine_by_id(engine_id, token):
    url = f"{ENGINE_URL}/{engine_id}"
    try:
        response = urequests.get(url, headers=get_headers(token))
        print("GET by ID:", response.status_code, response.text)
    except Exception as e:
        print("GET by ID xətası:", e)

# --- PATCH: Cihaz yenilə (yalnız admin) ---
def update_engine(engine_id, update_data, token):
    if token != TOKEN_ADMIN:
        print("Yalnız admin cihaz yeniləyə bilər.")
        return
    url = f"{ENGINE_URL}/{engine_id}"
    try:
        response = urequests.patch(url, data=ujson.dumps(update_data), headers=get_headers(token))
        print("PATCH:", response.status_code, response.text)
    except Exception as e:
        print("PATCH xətası:", e)

# --- DELETE: Cihaz sil (yalnız admin) ---
def delete_engine(engine_id, token):
    if token != TOKEN_ADMIN:
        print("Yalnız admin cihaz silə bilər.")
        return
    url = f"{ENGINE_URL}/{engine_id}"
    try:
        response = urequests.delete(url, headers=get_headers(token))
        print("DELETE:", response.status_code, response.text)
    except Exception as e:
        print("DELETE xətası:", e)

# --- POST: Engine-i istifadəçiyə təyin et (yalnız admin) ---
def assign_engine_to_user(engine_id, user_id, token):
    if token != TOKEN_ADMIN:
        print("Yalnız admin təyin edə bilər.")
        return
    data = {"engineId": engine_id, "userId": user_id}
    try:
        response = urequests.post(NODE_JS_SERVER_URL, data=ujson.dumps(data), headers=get_headers(token))
        print("Təyin et:", response.status_code, response.text)
    except Exception as e:
        print("POST təyin xətası:", e)

# --- Əsas ---
def main():
    ip, mac = connect_wifi(SSID, PASSWORD)

    # 1. Admin yeni cihaz yaradır
    create_engine(ip, mac, TOKEN_ADMIN)

    # 2. Admin bütün cihazlara baxır
    get_all_engines(TOKEN_ADMIN)

    # 3. İstifadəçi öz cihazlarını görür
    # get_user_engines(TOKEN_USER)

    # 4. Admin bir cihazı ID ilə tapır
    # get_engine_by_id("ENGINE_ID", TOKEN_ADMIN)

    # 5. Admin cihazı yeniləyir
    # update_engine("ENGINE_ID", {"status": 0}, TOKEN_ADMIN)

    # 6. Admin cihazı silir
    # delete_engine("ENGINE_ID", TOKEN_ADMIN)

    # 7. Admin engine-i istifadəçiyə təyin edir
    # assign_engine_to_user("ENGINE_ID", "USER_ID", TOKEN_ADMIN)

main()
