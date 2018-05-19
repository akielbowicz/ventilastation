from ventilagon.pattern import Pattern
import machine

NUM_COLUMNS = const(6)
NUM_ROWS = const(32)
ROW_SHIP = const(3)
ROW_COLISION = const(7)

circular_buffer = bytearray(NUM_ROWS)
cb_first_row = 0

def cb_reset():
    global cb_first_row
    cb_first_row = 0
    for n in range(NUM_ROWS):
        circular_buffer[n] = 0

def cb_push_front(row):
    try:
        global cb_first_row
        state = machine.disable_irq()
        circular_buffer[cb_first_row] = row
        cb_first_row = (cb_first_row - 1) % NUM_ROWS
    finally:
        machine.enable_irq(state)

def cb_push_back(row):
    try:
        global cb_first_row
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

def colision(pos, num_row):
    # la nave esta en la misma fila
    real_pos = (pos + nave_calibrate + SUBDEGREES / 2) & SUBDEGREES_MASK
    ship_column = (real_pos * NUM_COLUMNS) / SUBDEGREES
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

    ledbar.update();

@micropython.viper
def render(buffer, index):
    mask = int(1 << int(index))
    fg0 = int(current_level.color)
    bg1 = int(current_level.bg1)
    bg2 = int(current_level.bg2)
    b32 = ptr32(buffer)
    multicolored = False
    alt_column = int(index) & 1

    # always paint the innermost circle
    b32[0] = fg0

    for n in range(1, NUM_ROWS):
        row = cb_get_row(n)
        value = 1 & mask
        if value:
            #if num_row == ROW_SHIP:
            #    c = RED
            #if multicolored:
            #    c = colors[((num_row>>2)+(alt_column<<1))%6]
            #else:
            color = fg0
        else:
            color = bg1 if alt_column else bg2

        b32[n] = color

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
