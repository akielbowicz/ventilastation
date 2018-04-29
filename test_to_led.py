import sys
from to_led import to_led


sys.stdout.buffer.write(to_led(path='./files/mario.png',n_ang=128))