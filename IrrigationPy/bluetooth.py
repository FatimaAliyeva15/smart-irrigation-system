from machine import UART
import time

# UART portunu təyin edirik (TX=GPIO1, RX=GPIO3)
uart = UART(1, baudrate=9600, tx=1, rx=3)

print("Bluetooth bağlantısı gözlənilir...")

while True:
    if uart.any():
        data = uart.read().decode('utf-8')  # Bluetooth-dan gələn mesajı oxuyuruq
        print("Received:", data)  # Terminalda mesajı göstər
        uart.write("ESP8266: " + data)  # Eyni mesajı geri göndər
    time.sleep(1)
