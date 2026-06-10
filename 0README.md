# Docker Syslog Demo

A minimal two-container Docker Compose setup that demonstrates how to ship container logs over syslog to a custom log collector.

## What it does

- **`collector` container** — runs a small Python script (`collector.py`) that listens on UDP port 5514 and prints every syslog message it receives, timestamped, to stdout.
- **`app` container** — an Alpine shell loop that emits `hello from app` every 2 seconds. Its Docker logging driver is configured to send output via syslog (UDP) to the collector instead of the normal Docker log buffer.

The result: `app`'s stdout ends up in `collector`'s stdout, routed through the syslog protocol, rather than being captured by Docker directly.

## How to run

```bash
# Start collector first (app depends on it), then app
docker compose up

# Watch logs from the collector
docker compose logs -f collector
```

## Key concepts

| Thing | Role |
|-------|------|
| `syslog` logging driver | Tells Docker to forward a container's output to a syslog endpoint instead of keeping it locally |
| `udp://127.0.0.1:5514` | The syslog address the `app` container sends to |
| `collector.py` | A plain UDP socket server — no syslog library needed; the payload is just a syslog-formatted string |
| `depends_on` | Ensures the collector is up before the app starts sending logs |
