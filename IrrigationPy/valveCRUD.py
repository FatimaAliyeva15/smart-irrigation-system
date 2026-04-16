import network
import time
import urequests
import ujson
import machine

# --- Konfiqurasiya ---
SSID = "ALHN-C947"
PASSWORD = "YfbZQUCXy2"
BASE_URL = "http://192.168.1.67:5000"
VALVE_URL = f"{BASE_URL}/valve"


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
    print(f"Qoşuldu: IP: {ip}")
    return ip

# --- Header-lar ---
def get_headers():
    return {'Content-Type': 'application/json'}

# --- POST: Yeni valve əlavə et ---
def create_valve(valve_data):
    try:
        response = urequests.post(VALVE_URL, data=ujson.dumps(valve_data), headers=get_headers())
        print("Valve yaradıldı:", response.status_code, response.text)
    except Exception as e:
        print("POST xətası:", e)

# --- GET: Bütün valve-lar ---
def get_all_valves():
    try:
        response = urequests.get(VALVE_URL, headers=get_headers())
        print("Bütün valve-lar:", response.status_code, response.text)
    except Exception as e:
        print("GET xətası:", e)

# --- GET: Valve ID ilə ---
def get_valve_by_id(valve_id):
    url = f"{VALVE_URL}/{valve_id}"
    try:
        response = urequests.get(url, headers=get_headers())
        print("Valve by ID:", response.status_code, response.text)
    except Exception as e:
        print("GET by ID xətası:", e)
        
# --- PATCH: Valve ID ilə yenilə ---
def update_valve(valve_id, update_data):
    url = f"{VALVE_URL}/{valve_id}"
    try:
        response = urequests.patch(url, data=ujson.dumps(update_data), headers=get_headers())
        print("Valve yeniləndi:", response.status_code, response.text)
    except Exception as e:
        print("PATCH xətası:", e)


# --- DELETE: Valve ID ilə ---
def delete_valve(valve_id):
    url = f"{VALVE_URL}/{valve_id}"
    try:
        response = urequests.delete(url, headers=get_headers())
        print("Valve silindi:", response.status_code, response.text)
    except Exception as e:
        print("DELETE xətası:", e)

def generate_schedule(start_date, start_hour, start_minute, interval_minute, duration):
    schedule = {}
    hour = start_hour
    minute = start_minute

    for i in range(1, 6):
        valve_key = f"valve_{i}"
        time_str = f"{hour:02d}:{minute:02d}"
        schedule[valve_key] = {
            "date": start_date,
            "time": time_str,
            "duration_minut": duration
        }
        # Vaxt intervalını artır
        minute += interval_minute
        if minute >= 60:
            hour += minute // 60
            minute = minute % 60

    return schedule


# --- Əsas funksiyanın işə düşməsi ---
def main():
    connect_wifi(SSID, PASSWORD)
    
    mode = {
        "rejim": "Manual",
        "manual_mode": "aktiv"
    }

    schedule = generate_schedule("2025-06-01", 8, 0, 30, 10)
    print("Yaradılmış cədvəl:")
    print(schedule)
    
    new_valve = {"mode": mode}
    new_valve.update(schedule)

#     new_valve = {
#         "mode": {
#             "rejim": "Manual",
#             "manual_mode": "aktiv"
#         },
#         "valve_1": {
#             "date": "2025-06-01",
#             "time": "11:00",
#             "duration_minut": 10
#         },
#         "valve_2": {
#             "date": "2025-06-01",
#             "time": "11:30",
#             "duration_minut": 10
#         },
#         "valve_3": {
#             "date": "2025-06-01",
#             "time": "12:00",
#             "duration_minut": 10
#         },
#         "valve_4": {
#             "date": "2025-06-01",
#             "time": "12:30",
#             "duration_minut": 10
#         },
#         "valve_5": {
#             "date": "2025-06-01",
#             "time": "13:00",
#             "duration_minut": 10
#         }
#     }


#     create_valve(new_valve)     
#     get_all_valves()            

    valve_id = "683991fe2db71d305e992dbd"
#     update_data = {
#         "mode": {
#             "rejim": "Auto",
#             "manual_mode": "passive"
#         }
#     }
#     update_valve(valve_id, update_data)
    # get_valve_by_id(valve_id)  
    # delete_valve(valve_id)     

main()
