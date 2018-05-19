from utime import sleep
from machine import Pin, SPI

hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

hspi = SPI(1, baudrate=20000000, polarity=0, phase=0)

#clock = Pin(14, Pin.OUT)     # set GPIO14 to output to drive the clock
#data = Pin(13, Pin.OUT)      # set GPIO13 to output to drive the data


def vsync(_):
    led.value(not led.value())

hall.irq(vsync, trigger=Pin.IRQ_FALLING)

PIXELS = 52
hspi_buffer = bytearray(4 + 4*PIXELS + 7)
buffer = memoryview(hspi_buffer)[4:4+4*PIXELS]
print(len(buffer))
print(len(hspi_buffer))

# 0xE0+Bright, Blue, Green, Red

colores = [
    b"\xff\x00\x00\x10",
    b"\xff\x00\x10\x00",
    b"\xff\x10\x00\x00",
    b"\xff\x00\x00\x00",
]

def drawcolor(c):
    for n in range(0, len(buffer), 4):
        buffer[n:n+4] = colores[c]
    hspi.write(hspi_buffer)

def loop():
    index = 0

    for n in range(10):
        sleep(0.3)
        c = index % len(colores)
        drawcolor(c)
        print(hspi_buffer)
        led.value(not led.value())
        index += 1

led.value(1)
try:
    loop()
finally:
    drawcolor(3)
