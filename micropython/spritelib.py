PIXELS = const(52)
NUM_SPRITES = const(3)

hspi_buffer = bytearray(4 + PIXELS * 4 + 7)
buffer = memoryview(hspi_buffer)[4:PIXELS * 4 + 4]
#buffer = bytearray(PIXELS * 4)

COLOR_TRANSPARENT = const(0xFF)
palette = bytearray(256*4)
with open("raw/palette.pal") as f:
    f.readinto(palette)

background = bytearray(PIXELS*8)
with open("raw/fondo.raw") as f:
    f.readinto(background)

sprite_sizes = bytearray(2 * NUM_SPRITES)
sprite_sizes[0:6] = bytearray((16, 16, 14, 20, 16, 16))
xpos = bytearray(NUM_SPRITES)
ypos = bytearray(NUM_SPRITES)

xpos[0] = 16
ypos[0] = 12

xpos[1] = 48
ypos[1] = 12

xpos[2] = 64
ypos[2] = 16

images = bytearray(14 * 20 * NUM_SPRITES)
with open("raw/images.raw") as f:
    f.readinto(images)
sprite_bases = bytearray(NUM_SPRITES * 2)

@micropython.viper
def render(x: int):
    b32 = ptr32(buffer)
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

    base = (x % 8) * PIXELS
    for y in range(PIXELS):
        color = back8[base + y]
        b32[PIXELS-1-y] = p32[color]

    for n in range(NUM_SPRITES):
        sw = sizes8[n*2]
        sh = sizes8[n*2 + 1]
        sx = xpos8[n]
        sy = ypos8[n]
        if sx <= x < (sx + sw):
            base = bases16[n] + (x - sx) * sh
            for y in range(sh):
                color = image8[base + y]
                if color != COLOR_TRANSPARENT:
                    b32[PIXELS - 1 - (sy + y)] = p32[color]


if __name__ == "__main__":
    import utime
    from machine import SPI
    hspi = SPI(1, baudrate=20000000, polarity=0, phase=0)

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
    def loop():
        for n in range(1000):
            x = n % 128
            render(x)
            hspi.write(buffer)

    @timed_function
    def scanline_simulator():
        loop()

    scanline_simulator()
