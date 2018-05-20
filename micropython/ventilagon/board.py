from ventilagon.pattern import Pattern
import machine

NUM_COLUMNS = const(6)
BASE = const(5)
NUM_ROWS = const(52 - BASE)
ROW_SHIP = const(3)
ROW_COLISION = const(7)
SUBDEGREES = const(8192)
SUBDEGREES_MASK = const(8191)

circular_buffer = bytearray(NUM_ROWS)
cb_first_row = 0

def cb_reset():
    global cb_first_row
    cb_first_row = 0
    for n in range(NUM_ROWS):
        circular_buffer[n] = 0

def cb_push_front(row):
    global cb_first_row
    try:
        state = machine.disable_irq()
        circular_buffer[cb_first_row] = row
        cb_first_row = (cb_first_row - 1) % NUM_ROWS
    finally:
        machine.enable_irq(state)

def cb_push_back(row):
    global cb_first_row
    try:
        state = machine.disable_irq()
        circular_buffer[cb_first_row] = row
        cb_first_row = (cb_first_row + 1) % NUM_ROWS
    finally:
        machine.enable_irq(state)

@micropython.viper
def cb_get_row(row_num: int) -> int:
    cb8 = ptr8(circular_buffer)
    pos = (row_num + int(cb_first_row)) % NUM_ROWS
    return cb8[pos]

pat = Pattern()

def board_reset():
    pat.randomize()
    cb_reset()

def fill_patterns():
    row_num = 20
    while row_num != NUM_ROWS:
        pat.randomize()

        while not pat.finished():
            cb_push_back(pat.next_row())
            row_num += 1
            if row_num == NUM_ROWS:
                break

def collision(pos, num_row):
    # la nave esta en la misma fila
    #real_pos = (pos + nave_calibrate + SUBDEGREES / 2) & SUBDEGREES_MASK
    ship_column = int((pos * NUM_COLUMNS) / SUBDEGREES)
    row_ship = cb_get_row(num_row)
    mask = 1 << ship_column
    return row_ship & mask

def step():
    cb_push_back(pat.next_row())
    if pat.finished():
        pat.randomize()

def step_back():
    cb_push_front(0)

def win_reset():
    pat.randomize()

def win_step_back():
    cb_push_front(self.pat.next_row())
    if pat.finished():
        pat.randomize()

def draw_column(column):
    mask = 1 << column
    ledbar.clear()

    # always paint the innermost circle
    ledbar.draw(0, True, True)

    for n in range(1, NUM_ROWS):
        row = cb_get_row(n)
        value = row & mask
        ledbar.draw(n, value, column & 1)

    ledbar.update()

colores = [
    0x00ff00ff,
    0xff0000ff,
    0x0000ffff,
    0xffff00ff,
    0x00ffffff,
    0xff00ffff,
    0xffffffff
]
RED = 0xff0000ff

@micropython.viper
def render(buffer: ptr32, index: int, first_row: int, show_ship: int):
    mask = 1 << index
    fg0 = int(current_level.color)
    #fg0 = int(colores[index])
    bg1 = int(current_level.bg1)
    bg2 = int(current_level.bg2)
    b32 = ptr32(buffer)
    cb8 = ptr8(circular_buffer)
    multicolored = False
    alt_column = index & 1

    # always paint the innermost circle
    b32[BASE] = fg0
    #print(first_row)

    for n in range(1, NUM_ROWS):
        if show_ship and n == ROW_SHIP: # == :#num_row == int(ROW_SHIP) show_ship:
            b32[BASE+n] = int(RED)
            continue
        row = cb8[(n + first_row) % NUM_ROWS]
        #row = int(cb_get_row(n))
        value = row & mask
        if value:
            #if num_row == ROW_SHIP:
            #    c = RED
            #if multicolored:
            #    c = colors[((num_row>>2)+(alt_column<<1))%6]
            #else:
            color = fg0
        else:
            color = bg1 if alt_column else bg2

        b32[BASE+n] = color

if __name__ == "__main__":
    import utime
    def timed_function(f, *args, **kwargs):
        myname = str(f).split(' ')[1]
        def new_func(*args, **kwargs):
            t = utime.ticks_us()
            result = f(*args, **kwargs)
            delta = utime.ticks_diff(utime.ticks_us(), t)
            print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
            return result
        return new_func

    @micropython.viper
    def draw_rows():
        for n in range(NUM_ROWS):
            b = cb_get_row(n)
        print("{0:06b}".format(b))

    @timed_function
    def loop():
        for n in range(1000):
            step()
            draw_rows()

    loop()

    import micropython
    micropython.mem_info()
