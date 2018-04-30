import socket
import sys
import time
from itertools import cycle
from struct import unpack
from pygletengine import PygletEngine


class BaseColorSource(object):
    def line_data_to_rgba(self, data):
        line_bytes = bytearray(data)
        bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
        rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
        return rgba_list

    def send_tick(self):
        pass

    def create_color_iterator(self):
        raise NotImplementedError


class FileColorSource(BaseColorSource):
    def __init__(self, filename):
        self.filename = filename
        self.sleep_time = 0.05
        self.last_iteration_time = time.time()
        self.last_tick_time = time.time()
        self.file = open(self.filename, 'rb')

    def send_tick(self):
        print('tick')
        tick_time = time.time()
        self.file.seek(0)
        self.sleep_time = (tick_time - self.last_tick_time) / 32
        self.last_tick_time = tick_time

    def create_color_iterator(self):
        global led_count

        while True:
            iteration_time = time.time()
            if iteration_time - self.last_iteration_time > self.sleep_time:
                self.last_iteration_time = iteration_time
                data = self.file.read(4*led_count)
                if data == b'':
                    self.file.seek(0)
                    data = self.file.read(4*led_count)
                yield self.line_data_to_rgba(data)
            else:
                yield None


class SocketColorSource(BaseColorSource):
    SERVER_UDP_IP = "0.0.0.0"
    SERVER_UDP_PORT = 9999
    CLIENT_UDP_IP = '192.168.4.1'
    CLIENT_UDP_PORT = 5005

    def __init__(self):
        self.tick_socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_DGRAM)
        self.tick_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_tick(self):
        print('tick')
        self.tick_socket.sendto(b'tick', (self.CLIENT_UDP_IP, self.CLIENT_UDP_PORT))

    def create_color_iterator(self):
        global led_count
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.setblocking(False)
        sock.bind((self.SERVER_UDP_IP, self.SERVER_UDP_PORT))
        while True:
            try:
                data, _ = sock.recvfrom(led_count * 4)
                yield self.line_data_to_rgba(data)
            except BlockingIOError:
                yield None

filename = '-'
if len(sys.argv) >= 2:
    filename = sys.argv[1]

if filename == '-':
    color_source = SocketColorSource()
else:
    color_source = FileColorSource(filename)

led_count = 50
if len(sys.argv) >= 3:
    led_count = int(sys.argv[2])

steps = 32
if len(sys.argv) >= 4:
    steps = int(sys.argv[3])

PygletEngine(color_source, led_count)
