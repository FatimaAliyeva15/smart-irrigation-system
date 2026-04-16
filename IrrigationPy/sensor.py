from machine import ADC
import time

adc = ADC(0)  # A0 pin

while True:
    value = adc.read()  # 0 - 1023 arasında dəyişir
    print("Torpaq nəmlik dəyəri:", value)
    time.sleep(1)
