import socket

def send_data(file_name=None,ip='192.168.4.2',port=9999):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
    
    raw = open(file_name,"rb")
    buf0 = bytearray(288*4)
    buf = memoryview(buf0)
    raw.readinto(buf)
    
    s.sendto(buf,(ip,port))
