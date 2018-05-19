from utime import ticks_us, ticks_add, ticks_diff, sleep, sleep_us
from micropython import mem_info
from spritelib.spritelib import *
#from ventilagon import ventilador
import ventilagon.emulador as ventilador

COLUMNS = const(128)

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
    #print(last_turn_duration)

ventilador.vsync_handler = recalc

def loop():
    global index
    next_column_time = ticks_us()
    while True:
        render(index, ventilador.buffer)
        ventilador.write()
        sleep_us(ticks_diff(next_column_time, ticks_us()))
        index = int(index) + 1
        next_column_time = ticks_add(last_turn, segment_duration * index)
        ventilador.loop()

ventilador.clear()
try:
    loop()
finally:
    mem_info()
    ventilador.clear()
