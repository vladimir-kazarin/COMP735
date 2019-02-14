import socket, struct
from datetime import datetime

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(1024)
        print('Connected by', addr)
        timestamp = datetime.now().timestamp()
        if timestamp:
            s.sendto(struct.pack('f',timestamp), addr)
