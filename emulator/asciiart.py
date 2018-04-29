import sys
from time import sleep

_w = sys.stdout.write


def apply_alpha(rgba):
    r, g, b, a = rgba
    a_abs = a / 255.
    new_r = int(a_abs * r)
    new_g = int(a_abs * g)
    new_b = int(a_abs * b)
    return new_r, new_g, new_b

def draw_color(rgba):
    rgb = apply_alpha(rgba)
    _w("\033[38;2;{0};{1};{2};48;2;{0};{1};{2}m \033[0m".format(*rgb))

def cursor_up(lines=1):
    _w("\033[{0}A".format(lines))

def cursor_down(lines=1):
    _w("\033[{0}B".format(lines))

def cursor_forward(columns=1):
    _w("\033[{0}C".format(columns))

def cursor_backward(columns=1):
    _w("\033[{0}D".format(columns))

def clean():
    _w("\033[2J")

def set_cursor(line, column):
    _w("\033[{0};{1}f".format(line, column))


class AsciiArt():
    def __init__(self, width=None, height=None):
        self.screen_w = width or 80
        self.screen_h = height or 6
        self._cur_line = 0
        clean()
        cursor_up()

    def draw(self, line):
        if self._cur_line >= self.screen_w:
            set_cursor(0, 0)
            self._cur_line = -1

        for dot in line:
            draw_color(dot)
            cursor_down()
            cursor_backward()

        sys.stdout.flush()
        sleep(0.01)

        cursor_up(self.screen_h)
        cursor_forward()
        self._cur_line += 1
