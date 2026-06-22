# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A minimal two-container Docker Compose demo showing how to configure Docker's syslog logging driver to forward container output to a custom UDP log collector instead of Docker's default logging buffer.

## Running

```bash
docker compose up
```

Watch only the collector's output:
```bash
docker compose logs -f collector
```

## Architecture

Two services defined in `docker-compose.yml`:

- **collector** — Python 3.12-Alpine container running `collector.py`, a ~10-line UDP socket server listening on port 5514. Prints timestamped syslog messages (sender IP + payload) to stdout.
- **app** — Alpine container running a shell loop that emits "hello from app" every 2 seconds. Configured with Docker's `syslog` logging driver pointing to `udp://127.0.0.1:5514` with tag `demo-app`. Depends on collector.

The key mechanism: Docker's `logging.driver: syslog` intercepts the app container's stdout/stderr and forwards it as syslog UDP datagrams to the collector, bypassing Docker's default log buffer entirely.

No external Python dependencies — `collector.py` uses only `socket` and `datetime` from the standard library.
