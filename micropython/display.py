import esp
from utime import ticks_us, ticks_add, ticks_diff, sleep, sleep_us
from machine import Pin
import micropython
micropython.alloc_emergency_exception_buf(100)

COLUMNS = const(32)

clock = Pin(14, Pin.OUT)
data = Pin(13, Pin.OUT)
hall = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

last_turn = ticks_us()
segment_duration = 1000

def recalc(this_turn):
    global last_turn
    global segment_duration
    last_turn_duration = ticks_diff(this_turn, last_turn)
    last_turn = this_turn
    segment_duration = last_turn_duration // COLUMNS

def vsync(_):
    led.value(not led.value())
    micropython.schedule(recalc, ticks_us())

hall.irq(vsync, trigger=Pin.IRQ_FALLING) #, wake=IDLE | SLEEP | DEEPSLEEP)

buf = bytearray(50*4)
buf2 = bytearray(288*4)
raw = open("pictures/mario32.bytes", "rb")


def nextframe(*args):
    raw.readinto(buf)
    esp.apa102_write(clock, data, buf)

def loop():
    next_column_time = 0
    for j in range(100):
        for i in range(COLUMNS):
            raw.readinto(buf)
            esp.apa102_write(clock, data, buf)
            now = ticks_us()
            sleep_us(ticks_diff(next_column_time, now))
            next_column_time = ticks_add(now, segment_duration)
        raw.seek(0)

led.value(1)
sleep(5)
loop()
esp.apa102_write(clock, data, buf2)
led.value(0)
print("chau pycamp")
