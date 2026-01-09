#!/bin/bash

# Validate Input
if [[ -z "$1" ]]; then
    echo "Usage: $0 <target-ip> [ports]"
    echo "Example: $0 192.168.1.1 22,80,443"
    exit 1
fi

TARGET=$1
# Default to full range (1-65535) if no second argument is provided
if [[ -z "$2" ]]; then
    PORTS=$(seq 1 65535)
else
    # Replace commas with spaces to iterate easily
    PORTS=$(echo "$2" | tr ',' ' ')
fi

echo "Scanning $TARGET..."

for PORT in $PORTS; do
    # Using timeout to prevent the script from hanging on closed/filtered ports
    # 2>/dev/null hides 'Connection Refused' errors
    timeout 1 bash -c "echo > /dev/tcp/$TARGET/$PORT" 2>/dev/null && \
    echo "Port $PORT is OPEN"
done

echo "Scan complete."
