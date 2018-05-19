import socket
import sys
from itertools import cycle
from struct import unpack
from pygletengine import PygletEngine

LED_COUNT = 50
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
UDP_PORT_COMMANDS = 5225

def line_data_to_rgba(data):
    line_bytes = bytearray(data)
    bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
    rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
    return rgba_list

def file_iterator(f):
    while True:
        data = f.read(4*LED_COUNT)
        while data != b"":
            yield line_data_to_rgba(data)
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
            yield line_data_to_rgba(data)
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

steps = 128
if len(sys.argv) >= 4:
    steps = int(sys.argv[3])


PygletEngine(led_count, steps, iterator, vsync)
