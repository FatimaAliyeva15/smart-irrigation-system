import network
import usocket
import time

ssid = "enteskedu"
password = "ABC100200"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    print("Qoşulur...")
    time.sleep(1)

print("Qoşuldu:", station.ifconfig())

host = "irregationsystem.onrender.com"
port = 80 

sock = usocket.socket()
addr = usocket.getaddrinfo(host, port)[0][-1]
sock.connect(addr)


request = b"GET / HTTP/1.1\r\nHost: irregationsystem.onrender.com\r\nConnection: close\r\n\r\n"
sock.send(request)

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(data)

sock.close()
