from machine import Pin, SPI
from micropython import schedule

PIXELS = const(52)

#clock = Pin(14, Pin.OUT)
#data = Pin(13, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

hspi_buffer = bytearray(4 + PIXELS * 4 + 7)
buffer = memoryview(hspi_buffer)[4:PIXELS * 4 + 4]

hspi = SPI(1, baudrate=20000000, polarity=0, phase=0)

vsync_handler = None

def irq_handler(_):
    if vsync_handler:
        schedule(vsync_handler, ticks_us())
    led.value(not led.value())

hall.irq(irq_handler, trigger=Pin.IRQ_FALLING)

def write():
    hspi.write(hspi_buffer)

def clear():
    led.value(0)
    for n in range(0, len(buffer), 4):
        buffer[n+0] = 0
        buffer[n+1] = 0
        buffer[n+2] = 0
    write()

def loop():
    pass
