from machine import Pin
import time

relay = Pin(5, Pin.OUT)  # GPIO5 = D1

while True:
    relay.value(0)  # LOW siqnal - relay aktiv olmalıdır
    print("Relay ON")
    time.sleep(2)
    relay.value(1)  # HIGH siqnal - relay deaktiv
    print("Relay OFF")
    time.sleep(2)
