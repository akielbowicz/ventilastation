import socket
import sys
from itertools import cycle
from struct import unpack
from pygletengine import PygletEngine

LED_COUNT = 50
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def line_data_to_rgba(data):
    line_bytes = bytearray(data)
    bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
    rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
    return rgba_list

def file_iterator(filename):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4*LED_COUNT)
            while data != b"":
                yield line_data_to_rgba(data)
                data = f.read(4*LED_COUNT)
            f.seek(0)

def sock_iterator():
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, _ = sock.recvfrom(1024)
        yield line_data_to_rgba(data)


filename = '-'
if len(sys.argv) >= 2:
    filename = sys.argv[1]

if filename == '-':
    iterator = sock_iterator()
else:
    iterator = file_iterator(filename)

led_count = 50
if len(sys.argv) >= 3:
    led_count = int(sys.argv[2])

steps = 128
if len(sys.argv) >= 4:
    steps = int(sys.argv[3])


PygletEngine(led_count, steps, iterator)
