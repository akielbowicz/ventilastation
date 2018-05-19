from machine import Pin
from utime import sleep

led = Pin(2, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)

def vsync(p):
    led.value(not led.value())
    #print("vsync")
    #    micropython.schedule(nextframe)

hall.irq(vsync, trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING) #, wake=IDLE | SLEEP | DEEPSLEEP)

led.value(not led.value())
sleep(10)
