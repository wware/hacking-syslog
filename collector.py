# collector.py
import socket, datetime

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5514))
print('collector listening on :5514', flush=True)
while True:
    data, addr = s.recvfrom(4096)
    print(f'[{datetime.datetime.now().isoformat()}] {addr[0]}: {data.decode(errors="replace")}', flush=True)
