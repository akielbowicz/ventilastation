import esp
from utime import ticks_us, ticks_add, ticks_diff, sleep, sleep_us
from machine import Pin
import micropython

clock = Pin(13, Pin.OUT)
data = Pin(14, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)

buf = bytearray(52*4)

vuelta = 1

def change():
    global vuelta
    vuelta = vuelta + 1
    for n in range(0, 52*4, 4):
        buf[n + 0] = 0 if (vuelta%2) else 255
        buf[n + 1] = 0 if (vuelta%3) else 127
        buf[n + 2] = 0 if (vuelta%5) else 255
        buf[n + 3] = 31


def recalc(this_turn):
    esp.apa102_write(clock, data, buf)
    change()

def vsync(_):
    micropython.schedule(recalc, ticks_us())

hall.irq(vsync, trigger=Pin.IRQ_FALLING)

esp.apa102_write(clock, data, buf)

micropython.schedule(recalc, ticks_us())

while True:
    pass

print("chau pycamp")
