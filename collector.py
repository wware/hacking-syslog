# collector.py
import socket, datetime, json, time
import urllib.request
from prometheus_client import Counter, start_http_server

messages_total = Counter('syslog_messages_total', 'Total syslog messages received')
bytes_total = Counter('syslog_bytes_total', 'Total bytes received')

LOKI_URL = 'http://loki:3100/loki/api/v1/push'

def push_to_loki(msg):
    payload = json.dumps({
        "streams": [{"stream": {"job": "syslog"}, "values": [[str(time.time_ns()), msg]]}]
    }).encode()
    req = urllib.request.Request(LOKI_URL, data=payload, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

start_http_server(8000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5514))
print('collector listening on :5514, metrics on :8000', flush=True)
while True:
    data, addr = s.recvfrom(4096)
    messages_total.inc()
    bytes_total.inc(len(data))
    msg = data.decode(errors="replace")
    print(f'[{datetime.datetime.now().isoformat()}] {addr[0]}: {msg}', flush=True)
    push_to_loki(msg)
