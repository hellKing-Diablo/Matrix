#!/usr/bin/env python3

import signal
import time

running = True


def shutdown(signum, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print("MATRIX orchestrator starting", flush=True)

while running:
    print("MATRIX orchestrator heartbeat", flush=True)
    time.sleep(15)

print("MATRIX orchestrator stopped cleanly", flush=True)
