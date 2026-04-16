import network
import time
import urequests
import ujson
import ubinascii
import machine

SSID = "enteskedu"         
PASSWORD = "ABC100200"   
API_URL = "http://192.168.0.144:5000/engine"
SERVER_IP_URL = "http://192.168.0.144:5000/device-ip"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    retry_count = 0
    while not wlan.isconnected():
        if retry_count > 10:
            print("WiFi bağlantısı alınmadı, yenidən başladılır...")
            machine.reset()
        print("WiFi-yə qoşulur...")
        time.sleep(1)
        retry_count += 1
    
    ip_address = wlan.ifconfig()[0] 
    mac_address = ubinascii.hexlify(wlan.config('mac'), ':').decode()
    print("WiFi bağlantısı uğurludur:")
    print(f"Cihazın IP ünvanı: {ip_address}")  
    print(f"MAC ünvanı: {mac_address}")
    
    return ip_address, mac_address

def send_device_info(ip_address, mac_address):
    try:
        
        wifi = network.WLAN(network.STA_IF)
        wifi_signal_strength = wifi.status('rssi')  

        data = {
            "ip_address": ip_address,
            "mac_address": mac_address,
            "status": 1,  
            "firmware_version": "1.0",
            "isConnected": True,
            "wifi_ssid": SSID,
            "wifi_signal_strength": wifi_signal_strength, 
            "deep_sleep_enabled": False
        }
        headers = {'Content-Type': 'application/json'}
        
        print(f"Cihaz məlumatları serverə göndərilir: {data}")
        response = urequests.post(API_URL, data=ujson.dumps(data), headers=headers)
        response_json = response.json()
        device_id = response_json.get("_id", None)
        print("Serverdən cavab:", response.status_code, response.text)
        response.close()
        return device_id
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

def get_ip_from_server(device_id):
    try:
        url = f"{SERVER_IP_URL}/{device_id}"
        response = urequests.get(url)
        if response.status_code == 200:
            print("Serverdən IP ünvanı alındı:", response.text)
        else:
            print(f"Serverdən uğursuz cavab alındı: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

def update_device_info(device_id, updated_data):
    try:
        if not device_id:
            print("Device ID tapılmadı!")
            return
        
        url = f"{API_URL}/{device_id}"
        headers = {'Content-Type': 'application/json'}
        response = urequests.patch(url, data=ujson.dumps(updated_data), headers=headers)
        print("Məlumat uğurla yeniləndi!")
        print("Cavab Məzmunu:", response.text)          
        response.close()
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

def delete_device(device_id):
    try:
        if not device_id:
            print("Device ID tapılmadı!")
            return
        
        url = f"{API_URL}/{device_id}"
        response = urequests.delete(url)
        if response.status_code == 200:
            print(f"Məlumat uğurla silindi: {device_id}")
        else:
            print(f"Silinmə uğursuz oldu. Status kodu: {response.status_code}")
            print("Serverin cavabı:", response.text)
        response.close()
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

def main():
    ip_address, mac_address = connect()
    device_id = send_device_info(ip_address, mac_address)
    
    if device_id:
        get_ip_from_server(device_id)
        
        updated_data = {
            "status": 2,  
            "wifi_signal_strength": -40
        }
        update_device_info(device_id, updated_data)
        
        delete_device(device_id)  

main()