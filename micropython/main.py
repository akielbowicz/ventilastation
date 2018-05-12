from utime import ticks_us, ticks_add, ticks_diff, sleep, sleep_us
from machine import Pin, SPI
from micropython import schedule, mem_info
from spritelib import *

COLUMNS = const(128)

#clock = Pin(14, Pin.OUT)
#data = Pin(13, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

hspi = SPI(1, baudrate=20000000, polarity=0, phase=0)

last_turn = ticks_us()
segment_duration = 1000

index = 0

def recalc(this_turn):
    global last_turn
    global segment_duration
    global index
    last_turn_duration = ticks_diff(this_turn, last_turn)
    last_turn = this_turn
    segment_duration = min(int(last_turn_duration) // COLUMNS, 100000)
    index = 0
    led.value(not led.value())

def vsync(_):
    schedule(recalc, ticks_us())

hall.irq(vsync, trigger=Pin.IRQ_FALLING)

def loop():
    global index
    next_column_time = ticks_us()
    while True:
        render(index)
        hspi.write(hspi_buffer)
        #sleep_us(ticks_diff(next_column_time, ticks_us()))
        index = int(index) + 1
        #next_column_time = ticks_add(last_turn, segment_duration * index)

hspi.write(hspi_buffer)
led.value(1)
try:
    loop()
finally:
    led.value(0)
    mem_info()
    for n in range(0, len(buffer), 4):
        buffer[n+0] = 0
        buffer[n+1] = 0
        buffer[n+2] = 0
    hspi.write(hspi_buffer)
