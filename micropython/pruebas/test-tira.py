import esp
from utime import sleep
from machine import Pin

clock = Pin(13, Pin.OUT)
data = Pin(14, Pin.OUT)
led = Pin(2, Pin.OUT)

buf2 = bytearray(52*4)

def nextframe(d):
    led.value(not led.value())
    buf = bytearray(52*4)
    for n in range(0, 52*4, 4):
        buf[n + 0] = 0
        buf[n + 1] = 0
        buf[n + 2] = 0
        buf[n + d] = 255
        buf[n + 3] = 31
    esp.apa102_write(clock, data, buf)
    sleep(1)

esp.apa102_write(clock, data, buf2)
for n in range(600):
    nextframe(0)
    nextframe(1)
    nextframe(2)
esp.apa102_write(clock, data, buf2)
print("chau pycamp")
