import utime
from esp import apa102_write
from machine import Pin

clock = Pin(14, Pin.OUT)     # set GPIO14 to output to drive the clock
data = Pin(13, Pin.OUT)      # set GPIO13 to output to drive the data

PIXELS = const(52)
COLOR_TRANSPARENT = const(0xFF)


def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

b = bytearray(PIXELS * 4)


@timed_function
def apa102write():
    @micropython.viper
    def inner():
        for n in range(1000):
            apa102_write(clock, data, b)
    inner()

colores = bytearray(256*4)

background = bytearray(PIXELS*8)


class Sprite:
    def __init__(self):
        self.image = bytearray(16*16)
        self.sx, self.sy = (0, 0)
        self.sw, self.sh = (16, 16)

    @micropython.viper
    def blit(self, x: int):
        b32 = ptr32(b)
        c32 = ptr32(colores)
        image8 = ptr8(self.image)
        sx = int(self.sx)
        sy = int(self.sy)
        sw = int(self.sw)
        sh = int(self.sh)

        if sx <= x < sx + sw:
            base = (x - sx) * sh + sy
            for y in range(sh):
                color = image8[base + y]
                if color != COLOR_TRANSPARENT:
                    b32[sy + y] = c32[color]


sprites = [Sprite() for _ in range(8)]

def init_pixels():
    for n in range(256):
        v = (n & 0x3f) + 0x20
        colores[n*4:n*4+4] = bytearray((v,v,v,ord('.')))

    for n in range(len(background)):
        background[n] = 0x0 % 0x7f

    for s in sprites:
        for n in range(len(s.image)):
            s.image[n] = (n + 0x10) % 0x7f

@micropython.viper
def write_background(x: int):
    b32 = ptr32(b)
    c32 = ptr32(colores)
    back8 = ptr8(background)

    base = x * PIXELS
    for y in range(PIXELS):
        color = back8[base + y]
        b32[y] = c32[color]

@timed_function
def scanline_simulator():
    for n in range(1000):
        x = n % 8
        write_background(x)
        for s in sprites:
            s.blit(x)

init_pixels()
apa102write()
scanline_simulator()
print(b)
