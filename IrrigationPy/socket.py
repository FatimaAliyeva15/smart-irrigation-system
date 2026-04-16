import network
import socket
import time

SSID = "enteskedu"
PASSWORD = "ABC100200"

# WiFi bağlantısı
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("WiFi-yə qoşulmağa çalışılır...")
        time.sleep(1)
    
    print("WiFi-yə qoşuldu! IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Sadə HTML cavabı
html = """<!DOCTYPE html>
<html>
<head><title>ESP8266 Data</title></head>
<body>
<h1>NodeMCU Üzərində Data</h1>
<p>Burada cihazın dataları olacaq!</p>
</body>
</html>
"""

# Server qurmaq
def start_server():
    ip = connect_wifi(SSID, PASSWORD)
    
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print('Server başladı, IP üzərindən bax: http://{}'.format(ip))
    
    while True:
        cl, addr = s.accept()
        print('Yeni bağlantı:', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()

# Əsas
start_server()
