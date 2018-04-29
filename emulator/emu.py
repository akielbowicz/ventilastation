from itertools import cycle
from struct import unpack
from pygletengine import PygletEngine

LED_COUNT = 50

def line_iterator(filename):
    with open(filename, 'rb') as f:
        while True:
            byte = f.read(4)
            while byte != b"":
                rgba = unpack('BBBB', byte)
                #print(rgba)
                byte = f.read(4)
                yield rgba
            f.seek(0)

# 'corazon.bytes'
#PygletEngine(50, line_iterator('corazon.bytes'))
PygletEngine(50, 128, line_iterator('mario128.bytes'))
