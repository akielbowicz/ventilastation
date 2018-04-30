import socket
import time


sock_listener = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock_listener.setblocking(False)
sock_listener.bind((UDP_IP, UDP_PORT))

while True:
    try:
        data, _ = sock_listener.recvfrom(1024)

    except BlockingIOError:
        pass


def send_data(file_name=None,ip='192.168.4.2',port=9999):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
    
    raw = open(file_name,"rb")
    buf0 = bytearray(50*4)
    buf = memoryview(buf0)
    
    while True:
        time.sleep(0.5)
        r =  raw.readinto(buf)
        if r == 0:
            raw.seek(0)
        else:
            s.sendto(buf,(ip,port))

send_data('colorPye.bytes')
