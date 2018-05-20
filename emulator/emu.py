import socket
import sys
from itertools import cycle
from pygletengine import PygletEngine

LED_COUNT = 50
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
UDP_PORT_COMMANDS = 5225

def file_iterator(f):
    while True:
        data = f.read(4*LED_COUNT)
        while data != b"":
            yield data
            data = f.read(4*LED_COUNT)
        f.seek(0)

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((UDP_IP, UDP_PORT))

def sock_iterator():
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            yield data
        except BlockingIOError:
            yield None


def sock_send(what):
    sock.sendto(what, (UDP_IP, UDP_PORT_COMMANDS))

def sock_vsync():
    sock_send(b"V")


filename = '-'
if len(sys.argv) >= 2:
    filename = sys.argv[1]

if filename == '-':
    iterator = sock_iterator()
    vsync = sock_vsync
else:
    f = open(filename, 'rb')
    iterator = file_iterator(f)
    vsync = lambda: f.seek(0)

led_count = 50
if len(sys.argv) >= 3:
    led_count = int(sys.argv[2])

revs_per_second = 5
if len(sys.argv) >= 4:
    revs_per_second = float(sys.argv[3])

PygletEngine(led_count, iterator, vsync, revs_per_second)
