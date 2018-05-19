import utime
from esp import apa102_write
from machine import Pin, SPI

hspi = SPI(1, baudrate=80000000, polarity=0, phase=0)

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

palette = bytearray(256*4)
with open("raw/palette.pal") as f:
    f.readinto(palette)

background = bytearray(PIXELS*8)
with open("raw/fondo.raw") as f:
    f.readinto(background)

NUM_SPRITES = const(8)
sprite_sizes = bytearray(2 * NUM_SPRITES)
sprite_sizes[0:6] = bytearray((16, 16, 14, 20, 16, 16))
xpos = bytearray(NUM_SPRITES)
ypos = bytearray(NUM_SPRITES)
images = bytearray(16 * 16 * NUM_SPRITES)
sprite_bases = bytearray(NUM_SPRITES * 2)

def dorandomcrap(x):
    xpos[0] = x
    ypos[1] = x

@micropython.viper
def blit():
    b32 = ptr32(b)
    p32 = ptr32(palette)
    image8 = ptr8(images)
    xpos8 = ptr8(xpos)
    ypos8 = ptr8(ypos)
    back8 = ptr8(background)
    sizes8 = ptr8(sprite_sizes)
    bases16 = ptr16(sprite_bases)
    bases16[0] = 0
    bases16[1] = 16 * 16
    bases16[2] = bases16[1] + 14 * 20

    for n in range(1000):
        #x = int(utime.ticks_us()) % 12
        x = n % 12

        #dorandomcrap(x)

        base = x * PIXELS
        for y in range(PIXELS):
            color = back8[base + y]
            b32[y] = p32[color]

        for n in range(NUM_SPRITES):
            sw = sizes8[n*2]
            sh = sizes8[n*2 + 1]
            sx = xpos8[n]
            sy = xpos8[n]
            if sx <= x < sx + sw:
                base = bases16[n] + (x - sx) * sh
                for y in range(sh):
                    color = image8[base + y]
                    if color != COLOR_TRANSPARENT:
                        b32[sy + y] = p32[color]

        hspi.write(b)
        #apa102_write(clock, data, b)


def init_pixels():
    for n in range(256):
        v = (n & 0x3f) + 0x20
        palette[n*4:n*4+4] = bytearray((v,v,v,ord('.')))

    for n in range(len(background)):
        background[n] = 0x0 % 0x7f

    for n in range(len(images)):
        images[n] = (n + 0x10) % 0x7f

@timed_function
def scanline_simulator():
    blit()

#init_pixels()
#apa102write()
scanline_simulator()
print(b)
