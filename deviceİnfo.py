# import network
# 
# wlan = network.WLAN(network.STA_IF)  # WiFi interfeysini açırıq
# wlan.active(True)  # WiFi-ni aktiv edirik
# 
# mac_address = wlan.config('mac')  # MAC ünvanını əldə edirik
# mac_address_str = ':'.join(f'{b:02X}' for b in mac_address)  # Oxunaqlı formata salırıq
# 
# print("NodeMCU V3 cihazının MAC ünvanı:", mac_address_str)
# 

# import machine
# 
# def check_deep_sleep():
#     reset_reason = machine.reset_cause()
#     if reset_reason == machine.DEEPSLEEP_RESET:
#         print("Cihaz Deep Sleep-dən oyandı!")
#         return True
#     else:
#         print("Cihaz normal qaydada başladı.")
#         return False
# wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Entesk_EDU", "ABC100200")

import time
while not wlan.isconnected():
    print("Qoşulmağa çalışır...")
    time.sleep(1)

print("Qoşuldu:", wlan.ifconfig())
