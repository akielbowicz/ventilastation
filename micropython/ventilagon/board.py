from pattern import Pattern
import machine

NUM_COLUMNS = 6
NUM_ROWS = 32
ROW_SHIP = 3
ROW_COLISION = 7

class CircularBuffer:
    def __init__(self):
        self.buffer = bytearray(NUM_ROWS)
        self.first_row = 0
        self.reset()

    def reset(self):
        self.first_row = 0
        for n in range(NUM_ROWS):
            self.buffer[n] = 0

    def push_front(self, row):
        try:
            state = machine.disable_irq()
            self.buffer[self.first_row] = row
            self.first_row = (self.first_row - 1) % NUM_ROWS
        finally:
            machine.enable_irq(state)

    def push_back(self, row):
        try:
            state = machine.disable_irq()
            self.buffer[self.first_row] = row
            self.first_row = (self.first_row + 1) % NUM_ROWS
        finally:
            machine.enable_irq(state)

    def get_row(self, row_num):
        pos = (row_num + self.first_row) % NUM_ROWS
        return self.buffer[pos]

class Board:
    def __init__(self):
        self.visible = CircularBuffer()
        self.pat = Pattern()
        self.reset()

    def reset(self):
        self.pat.randomize()
        self.visible.reset()

    def fill_patterns(self):
        row_num = 20
        while row_num != NUM_ROWS:
            self.pat.randomize()

            while not pat.finished():
                self.visible.push_back(self.pat.next_row())
                row_num += 1
                if row_num == NUM_ROWS:
                    break

    def colision(self, pos, num_row):
        # la nave esta en la misma fila
        real_pos = (pos + nave_calibrate + SUBDEGREES / 2) & SUBDEGREES_MASK
        ship_column = (real_pos * NUM_COLUMNS) / SUBDEGREES
        row_ship = self.visible.get_row(num_row)
        mask = 1 << ship_column
        return row_ship & mask

    def step(self):
        self.visible.push_back(self.pat.next_row())
        if self.pat.finished():
            #print("randomizando!")
            self.pat.randomize()

    def step_back(self):
        self.visible.push_front(0)

    def win_reset(self):
        self.pat.randomize()

    def win_step_back(self):
        self.visible.push_front(self.pat.next_row())
        if self.pat.finished():
            self.pat.randomize()

    def draw_column(self, column):
        mask = 1 << column
        ledbar.clear()

        # always paint the innermost circle
        ledbar.draw(0, True, True)

        for n in range(1, NUM_ROWS):
            row = self.visible.get_row(n)
            value = row & mask
            ledbar.draw(n, value, column & 1)

        ledbar.update();

board = Board()

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

    step = board.step
    get_row = board.visible.get_row
    @timed_function
    def loop():
        for n in range(1000):
            step()
            for n in range(NUM_ROWS):
                b = get_row(n)
            #print("{0:06b}".format(b))

    loop()

    import micropython
    micropython.mem_info()
