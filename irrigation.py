import network
import time
import urequests
import ujson

SSID = "enteskedu"        
PASSWORD = "ABC100200"  
API_URL = "http://192.168.1.68:5000/engine"
SERVER_IP_URL = "http://192.168.1.68:5000/device-ip"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("WiFi-yə qoşulur...")
        time.sleep(1)
    
    ip_address = wlan.ifconfig()[0] 
    print("WiFi bağlantısı uğurludur:")
    print(f"Cihazın IP ünvanı: {ip_address}")  
    
    return ip_address


def ensure_connection():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Şəbəkə bağlantısı itdi, yenidən qoşulmağa çalışılır...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            print("Yenidən qoşulmağa çalışılır...")
            time.sleep(5)
        print("WiFi bağlantısı yenidən uğurlu oldu:", wlan.ifconfig())

def send_ip_to_server(ip_address):
    try:
        data = {"ip_address": ip_address}
        headers = {'Content-Type': 'application/json'}
        
        print(f"IP ünvanı serverə göndərilir: {data}")
        time.sleep(2)
        
        response = urequests.post(SERVER_IP_URL, data=ujson.dumps(data), headers=headers)
        
        print("Serverdən cavab:", response.status_code, response.text)
        response.close()
        
    except OSError as e:
        print(f"Şəbəkə xətası baş verdi: {e}")
    except Exception as e:
        print(f"Naməlum xəta baş verdi: {e}")


def getdata():
    try:
        print(f"API-yə sorğu göndərilir: {API_URL}")
        response = urequests.get(API_URL)
        if response.status_code == 200:
            print("Cavab:", response.text)
        else:
            print(f"Serverdən uğursuz cavab alındı: {response.status_code}")
        response.close()
    except OSError as e:
        print(f"Şəbəkə xətası baş verdi: {e}")
    except Exception as e:
        print(f"Naməlum xəta baş verdi: {e}")

def send_post():
    data = {
        "Motor_OK": 1,
        "Motor_ON": 0,
        "time": 8200
    }
    headers = {'Content-Type': 'application/json'}

    response = urequests.post(API_URL, data=ujson.dumps(data), headers=headers)

    print("Response Status:", response.status_code)
    print("Response Text:", response.text)
    
    response.close()
    

def update_data(id, updated_data):
    try:
        url = f"{API_URL}/{id}"
        
        headers = {'Content-Type': 'application/json'}
        
        response = urequests.patch(url, data=ujson.dumps(updated_data), headers=headers)

        
        
        print("Məlumat uğurla yeniləndi!")
        print("Cavab Məzmunu:", response.text)          
        response.close()
        
    except OSError as e:
        print(f"Şəbəkə xətası baş verdi: {e}")
    except ValueError as e:
        print(f"JSON formatı xətası: {e}")
    except Exception as e:
        print(f"Naməlum xəta baş verdi: {e}")
        
def delete_data(id):
    try:
        url = f"{API_URL}/{id}"
        
        response = urequests.delete(url)
        
        if response.status_code == 200:
            print(f"Məlumat uğurla silindi: {id}")
        else:
            print(f"Silinmə uğursuz oldu. Status kodu: {response.status_code}")
            print("Serverin cavabı:", response.text)
        
        response.close()
        
    except OSError as e:
        print(f"Şəbəkə xətası baş verdi: {e}")
    except Exception as e:
        print(f"Naməlum xəta baş verdi: {e}")

def main():
    device_ip = connect()  
    print(f"Cihazın IP ünvanı (əsas proqramda): {device_ip}")
    send_ip_to_server(device_ip)
    getdata()

    send_post()
    
    object_id = "5c6766be-44ab-4d76-9d66-a54dd329f2c7"  
    updated_data = {
        "Motor_OK": 1,
        "Motor_ON": 1,
        "time": 32000
    }
    
    update_data(object_id, updated_data)
    
    delobject_id = "d6265196-bb85-4a1b-a7c8-027861667a7b"
    
    delete_data(delobject_id)

main()
