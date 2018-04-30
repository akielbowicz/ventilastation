import socket
from itertools import cycle
from struct import unpack
from pygletengine import PygletEngine

LED_COUNT = 50
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def file_iterator(filename):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4*LED_COUNT)
            while data != b"":
                line_bytes = bytearray(data)
                bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
                rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
                yield rgba_list
                data = f.read(4*LED_COUNT)

            f.seek(0)

def sock_iterator():
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, _ = sock.recvfrom(1024)
        line_bytes = bytearray(data)
        bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
        rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
        yield rgba_list


PygletEngine(50, 128, file_iterator('../files/corgibus128.bytes'))
#PygletEngine(50, 128, sock_iterator())
