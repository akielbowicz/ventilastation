from esp import apa102_write
from utime import sleep
from machine import Pin, SPI

hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

#hspi = SPI(1, baudrate=20000000, polarity=0, phase=0)

clock = Pin(14, Pin.OUT)     # set GPIO14 to output to drive the clock
data = Pin(13, Pin.OUT)      # set GPIO13 to output to drive the data


def vsync(_):
    led.value(not led.value())

hall.irq(vsync, trigger=Pin.IRQ_FALLING)

buffer = bytearray(4*52 + 4)

def loop():
    index = 0
    colores = [
        bytearray((255, 0, 0, 0xFF)),
        bytearray((0, 0, 0, 0xFF)),
        bytearray((0, 255, 0, 0xFF)),
        bytearray((0, 0, 255, 0xFF)),
    ]
    colores2 = [
        bytearray((0xFF, 255, 0, 0)),
        bytearray((0xFF, 0, 255, 0)),
        bytearray((0xFF, 0, 0, 255)),
    ]

    for n in range(10):
        c = index % len(colores)
        for n in range(0, len(buffer) -4 -16, 4):
            buffer[n+4:n+8] = colores[c]

            
        #hspi.write(buffer)
        print(buffer)
        sleep(0.3)
        apa102_write(clock, data, buffer)
        led.value(not led.value())
        index += 1

apa102_write(clock, data, buffer)
led.value(1)
loop()
