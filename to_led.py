import matplotlib.image as mpimg
from numpy import sin, cos, pi
from struct import pack

def to_led(path=None):
    img = mpimg.imread(path)

    led = []

    for m in range(0,32):
        for n in range(1,51):
            x = 511 + int(511 * n/50 * cos(m * pi/16))
            y = 561 + int( 511 * n/50 * sin(m * pi/16))
            tupla = tuple(int(g) for g in img[x,y])
            led.append(pack('BBBB', *tupla))
    return led
