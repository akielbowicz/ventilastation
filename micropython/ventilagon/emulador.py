from ventilagon import io

PIXELS = const(52)
buffer = bytearray(PIXELS * 4)

def write():
    io.send(buffer)

def clear():
    for n in range(0, len(buffer), 4):
        buffer[n+1] = 0
        buffer[n+2] = 0
        buffer[n+3] = 0
    write()
