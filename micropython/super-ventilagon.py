from utime import ticks_us, ticks_add, ticks_diff, sleep_us
from micropython import mem_info
from ventilagon.board import render, cb_get_row, circular_buffer, cb_first_row
#import ventilagon.ventilador
import ventilagon.emulador as ventilador
from ventilagon.levels import current_level

COLUMNS = const(6)

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

ventilador.vsync_handler = recalc

def loop():
    global index
    next_column_time = ticks_us()
    while True:
        render(ventilador.buffer, index % 6)
        ventilador.write()
        #sleep_us(ticks_diff(next_column_time, ticks_us()))
        index = int(index) + 1
        #next_column_time = ticks_add(last_turn, segment_duration * index)
        ventilador.loop()

ventilador.clear()
try:
    loop()
finally:
    ventilador.clear()
    mem_info()
