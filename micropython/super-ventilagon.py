from utime import ticks_us, ticks_add, ticks_diff, sleep_us
from micropython import mem_info
from ventilagon import board
from ventilagon.board import *
#from ventilagon import ventilador
import ventilagon.emulador as ventilador
from ventilagon import io
from ventilagon.levels import current_level

COLUMNS = const(6)

HALF_SHIP_WIDTH = const(50)

last_step = 0
last_keycheck = 0
ship_showing = False
last_column_drawn = 0

last_turn = ticks_us()
last_turn_duration = 10


ship_position = 1024

def recalc(this_turn):
    global last_turn
    global last_turn_duration
    last_turn_duration = ticks_diff(this_turn, last_turn)
    last_turn = this_turn

io.vsync_handler = recalc

def playstate_loop():
    global last_step, last_keycheck, ship_position
    now = ticks_us()

    if ticks_diff(ticks_add(last_keycheck, 100), now) < 0:
        last_keycheck = now
        if io.left_pressed != io.right_pressed:
            if io.left_pressed:
                new_pos = ship_position - 1
            if io.right_pressed:
                new_pos = ship_position + 1

            new_pos = (new_pos + SUBDEGREES) & SUBDEGREES_MASK

            future_collision = board.collision(new_pos, ROW_SHIP)
            if not future_collision:
                ship_position = new_pos

    if ticks_diff(ticks_add(last_step, current_level.step_delay), now) < 0:
        if not board.collision(ship_position, ROW_SHIP+1):
            board.step()
            last_step = now
        else:
            # crash boom bang
            pass

def ship_on(current_pos):
    #if calibrating:
        # return board.collision(current_pos, ROW_SHIP)

    if abs(ship_position - current_pos) < HALF_SHIP_WIDTH:
        return True

    if abs( (int(ship_position + SUBDEGREES / 2) & SUBDEGREES_MASK) -
            (int(current_pos + SUBDEGREES / 2) & SUBDEGREES_MASK)
        ) < HALF_SHIP_WIDTH:
        return True

    return False

def display_tick(now):
    global ship_showing, last_column_drawn
    drift = 0
    now_drift = ticks_diff(ticks_add(drift, now), last_turn)
    current_pos = int(now_drift * SUBDEGREES / last_turn_duration) & SUBDEGREES_MASK
    current_column = int(now_drift * NUM_COLUMNS / last_turn_duration) % NUM_COLUMNS
    show_ship = ship_on(current_pos)
    if show_ship != ship_showing or current_column != last_column_drawn:
        board.render(ventilador.buffer, current_column, board.cb_first_row, show_ship)
        ventilador.write()
        ship_showing = show_ship
        last_column_drawn = current_column

def loop():
    next_column_time = ticks_us()
    while True:
        now = ticks_us()
        display_tick(now)
        io.loop()
        playstate_loop()
        #if ventilador.down_pressed:
            #step()

ventilador.clear()
try:
    loop()
finally:
    ventilador.clear()
    mem_info()
