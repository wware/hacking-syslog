# collector.py
import socket, datetime
from prometheus_client import Counter, start_http_server

messages_total = Counter('syslog_messages_total', 'Total syslog messages received')
bytes_total = Counter('syslog_bytes_total', 'Total bytes received')

start_http_server(8000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5514))
print('collector listening on :5514, metrics on :8000', flush=True)
while True:
    data, addr = s.recvfrom(4096)
    messages_total.inc()
    bytes_total.inc(len(data))
    print(f'[{datetime.datetime.now().isoformat()}] {addr[0]}: {data.decode(errors="replace")}', flush=True)
