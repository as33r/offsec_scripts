#!/usr/bin/env python3
import socket
import struct
import argparse

"""
tcp-decoder: A simple parser for /proc/net/tcp

This script reads Linux kernel TCP socket information from /proc/net/tcp
(or a supplied file) and converts it into a human-readable table.

Features:
- Decodes local/remote IP addresses and ports (from hex/little-endian).
- Translates TCP state codes (e.g., 01 → ESTABLISHED).
- Shows UID and inode for each socket.
- Can parse a live system (/proc/net/tcp) or an offline dump (via -f).

Useful for debugging, security research, or understanding raw socket
data without having to manually decode hex values.
"""

# TCP states mapping from hex to human readable
TCP_STATES = {
    "01": "ESTABLISHED",
    "02": "SYN_SENT",
    "03": "SYN_RECV",
    "04": "FIN_WAIT1",
    "05": "FIN_WAIT2",
    "06": "TIME_WAIT",
    "07": "CLOSE",
    "08": "CLOSE_WAIT",
    "09": "LAST_ACK",
    "0A": "LISTEN",
    "0B": "CLOSING",
}

def hex_to_ip(hex_ip):
    """Convert little-endian hex IP to dotted-decimal string."""
    raw = bytes.fromhex(hex_ip)
    return socket.inet_ntoa(raw[::-1])  # reverse bytes

def hex_to_port(hex_port):
    """Convert hex port to integer."""
    return int(hex_port, 16)

def parse_proc_net_tcp(filename):
    with open(filename, "r") as f:
        lines = f.readlines()[1:]  # skip header

    sockets = []
    for line in lines:
        parts = line.split()
        sl = parts[0].strip(":")
        local_ip, local_port = parts[1].split(":")
        rem_ip, rem_port = parts[2].split(":")
        state = parts[3]

        entry = {
            "sl": sl,
            "local_address": f"{hex_to_ip(local_ip)}:{hex_to_port(local_port)}",
            "remote_address": f"{hex_to_ip(rem_ip)}:{hex_to_port(rem_port)}",
            "state": TCP_STATES.get(state, "UNKNOWN"),
            "uid": parts[7],
            "inode": parts[9],
        }
        sockets.append(entry)
    return sockets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse /proc/net/tcp into human readable format")
    parser.add_argument(
        "-f", "--file",
        default="/proc/net/tcp",
        help="Path to the tcp file (default: /proc/net/tcp)"
    )
    args = parser.parse_args()

    sockets = parse_proc_net_tcp(args.file)
    print(f"{'SL':<4} {'Local Address':<22} {'Remote Address':<22} {'State':<13} {'UID':<6} {'Inode'}")
    for s in sockets:
        print(f"{s['sl']:<4} {s['local_address']:<22} {s['remote_address']:<22} {s['state']:<13} {s['uid']:<6} {s['inode']}")
