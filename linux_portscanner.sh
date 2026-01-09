#!/bin/bash

# Validate Input
if [[ -z "$1" ]]; then
    echo "Usage: $0 <target-ip> [ports]"
    exit 1
fi

TARGET=$1
# Default to 1-65535 if no ports are provided
if [[ -z "$2" ]]; then
    PORTS=$(seq 1 65535)
else
    PORTS=$(echo "$2" | tr ',' ' ')
fi

echo "Scanning $TARGET..."

COUNTER=0
for PORT in $PORTS; do
    ((COUNTER++))
    
    # Print a progress log after every 5000 ports scanned
    if (( COUNTER % 5000 == 0 )); then
        echo "[LOG] Scanned $COUNTER ports so far..."
    fi

    # Attempt connection using native bash pseudo-device
    timeout 1 bash -c "echo > /dev/tcp/$TARGET/$PORT" 2>/dev/null && \
    echo "Port $PORT is OPEN"
done

echo "Scan complete. Total ports checked: $COUNTER"
