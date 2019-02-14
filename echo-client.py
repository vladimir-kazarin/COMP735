import socket, struct
from datetime import datetime

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

print('UDP connection...')
before_call  = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b'', (HOST, PORT))
    data, addr = s.recvfrom(1024)
    received_time = struct.unpack('f', data)[0]
    received_datetime = datetime.fromtimestamp(received_time)
    print('Received datetime: ', received_datetime)
after_call = datetime.now()
milsec = after_call - before_call
print(f'it took {milsec} to fetch {data}')
