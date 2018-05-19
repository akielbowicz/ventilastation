import esp
from utime import ticks_us, ticks_add, ticks_diff, sleep, sleep_us
from machine import Pin, SPI
import micropython

COLUMNS = const(32)

clock = Pin(13, Pin.OUT)
data = Pin(14, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

#hspi = SPI(1, baudrate=80000000, polarity=0, phase=0)
#hspi.write(buffer)

clock = Pin(14, Pin.OUT)     # set GPIO14 to output to drive the clock
data = Pin(13, Pin.OUT)      # set GPIO13 to output to drive the data

last_turn = ticks_us()
segment_duration = 1000

index = 0

def recalc(this_turn):
    global last_turn
    global segment_duration
    global index
    last_turn_duration = ticks_diff(this_turn, last_turn)
    last_turn = this_turn
    segment_duration = min(last_turn_duration // COLUMNS, 100000)
    index = 0
    led.value(not led.value())

def vsync(_):
    micropython.schedule(recalc, ticks_us())

hall.irq(vsync, trigger=Pin.IRQ_FALLING)

buf = bytearray(6400)
raw = open("pictures/mario32.bytes", "rb")
raw.readinto(buf)
raw.close()
mv = memoryview(buf)
buf2 = bytearray(52*4)

def loop():
    global index
    next_column_time = 0
    while True:
        esp.apa102_write(clock, data, mv[index:index+200])
        sleep_us(ticks_diff(next_column_time, ticks_us()))
        next_column_time = ticks_add(ticks_us(), segment_duration)
        index += 200

esp.apa102_write(clock, data, buf2)
led.value(1)
loop()
esp.apa102_write(clock, data, buf2)
led.value(0)
print("chau pycamp")
