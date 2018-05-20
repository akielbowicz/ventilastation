import usocket
from utime import ticks_us, sleep

PIXELS = const(52)
buffer = bytearray(PIXELS * 4)

vsync_handler = None

socksend_addr = usocket.getaddrinfo('127.0.0.1', 5005)[0][-1]
sockrecv_addr = usocket.getaddrinfo('127.0.0.1', 5225)[0][-1]

socksend = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
socksend.setblocking(False)

sockrecv = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
sockrecv.setblocking(False)
sockrecv.bind(sockrecv_addr)


def write():
    socksend.sendto(buffer, socksend_addr)

def clear():
    for n in range(0, len(buffer), 4):
        buffer[n+1] = 0
        buffer[n+2] = 0
        buffer[n+3] = 0
    write()

def loop():
    try:
        buf = sockrecv.recv(1)
        if buf:
            for b in buf:
                b = chr(b)
                if b == 'V':
                    if vsync_handler:
                        vsync_handler(ticks_us())
                elif b == 'l':
                    pass
                elif b == 'L':
                    pass
                elif b == 'r':
                    pass
                elif b == 'R':
                    pass
    except OSError:
        pass
