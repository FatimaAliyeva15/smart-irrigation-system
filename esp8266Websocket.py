import network
import time
import ujson
import ubinascii
import machine
import usocket as socket
import ustruct as struct
import uasyncio as asyncio

SSID = "ALHN-C947"  
PASSWORD = "YfbZQUCXy2"   
WS_URL = "ws://192.168.1.68:5000/ws/engine"
SERVER_WS_URL = "ws://192.168.1.68:5000/ws/device-ip"

async def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("WiFi-yə qoşulur...")
        await asyncio.sleep(1)
    
    ip_address = wlan.ifconfig()[0] 
    mac_address = ubinascii.hexlify(wlan.config('mac'), ':').decode()
    print("WiFi bağlantısı uğurludur:")
    print(f"Cihazın IP ünvanı: {ip_address}")  
    print(f"MAC ünvanı: {mac_address}")
    
    return ip_address, mac_address

async def create_websocket_connection():
    ws = socket.socket()
    host, port = WS_URL.split("://")[1].split(":")
    port = int(port)  # WebSocket portunu doğru şəkildə təyin et
    ws.connect((host, port))
    
    request = (
        "GET /ws HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    )
    
    ws.send(request.encode())
    response = ws.recv(1024)
    print("Handshake cavabı:", response.decode())
    
    return ws

async def send_device_info(ws, ip_address, mac_address):
    try:
        wifi = network.WLAN(network.STA_IF)
        wifi_signal_strength = wifi.status('rssi')
        
        if wifi_signal_strength is not None:
            wifi_signal_strength = int(wifi_signal_strength)  # Ensure it's an integer
        else:
            wifi_signal_strength = -100  # Default if signal strength is not available
        
        data = {
            "type": "register",
            "ip_address": ip_address,
            "mac_address": mac_address,
            "status": 1,
            "firmware_version": "1.0",
            "isConnected": True,
            "wifi_ssid": SSID,
            "wifi_signal_strength": wifi_signal_strength,
            "deep_sleep_enabled": False
        }
        
        print(f"Cihaz məlumatları serverə göndərilir: {data}")
        message = ujson.dumps(data)
        ws.send(message.encode())
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

async def get_device_info(ws, device_id):
    try:
        request = {
            "type": "get",
            "device_id": device_id
        }
        message = ujson.dumps(request)
        print(f"GET sorğusu göndərilir: {message}")
        ws.send(message.encode())
        
        response = ws.recv(1024)
        print("Serverdən cavab alındı:", response.decode())
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

async def delete_device(ws, device_id):
    try:
        request = {
            "type": "delete",
            "device_id": device_id
        }
        message = ujson.dumps(request)
        print(f"DELETE sorğusu göndərilir: {message}")
        ws.send(message.encode())
        
        response = ws.recv(1024)
        print("Serverdən cavab alındı:", response.decode())
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

async def main():
    ip_address, mac_address = await connect()
    
    try:
        ws = await create_websocket_connection()
        print("WebSocket bağlantısı quruldu.")
        await send_device_info(ws, ip_address, mac_address)
        
        device_id = "67f6a2023dffabff27340b46"
        await get_device_info(ws, device_id)
        await delete_device(ws, device_id)
        
        while True:
            response = ws.recv(1024)
            print("Serverdən mesaj alındı:", response.decode())
            await asyncio.sleep(5)
    
    except Exception as e:
        print("WebSocket xətası:", e)
    
    finally:
        ws.close()
        print("Bağlantı bağlandı.")

# Asinxron olaraq çalışdır
asyncio.run(main())
