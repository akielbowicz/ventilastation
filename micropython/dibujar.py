import esp
import time
from machine import Pin #, IDLE, SLEEP, DEEPSLEEP
import micropython
micropython.alloc_emergency_exception_buf(100)

clock = Pin(14, Pin.OUT)
data = Pin(13, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)

buf0 = bytearray(288*4)
buf = memoryview(buf0)[0:200]
buf2 = bytearray(288*4)
raw = open("pictures/mario128.bytes", "rb")

def nextframe():
    raw.readinto(buf)
    esp.apa102_write(clock, data, buf)

def vsync():
    micropython.schedule(nextframe)

hall.irq(vsync) #, trigger=Pin.IRQ_FALLING) #, wake=IDLE | SLEEP | DEEPSLEEP)

while True:
    pass

#@micropython.viper
def change():
    for j in range(100):
        for i in range(32):
            raw.readinto(buf)
            esp.apa102_write(clock, data, buf)
            #time.sleep_us(500000)
            while hall.value():
                True
        raw.seek(0)
    esp.apa102_write(clock, data, buf2)

change()
    
print("hola pycamp")
