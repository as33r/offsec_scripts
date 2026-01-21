import sys
import struct

"""
This script will convert mssql sid to a domain sid
"""

def sid_to_str(hex_sid):
    # Remove 0x prefix and spaces if present
    hex_sid = hex_sid.replace('0x', '').replace(' ', '').strip()
    sid_bytes = bytes.fromhex(hex_sid)

    revision = sid_bytes[0]
    sub_authority_count = sid_bytes[1]
    identifier_authority = int.from_bytes(sid_bytes[2:8], byteorder='big')

    sub_authorities = [
        struct.unpack('<I', sid_bytes[8 + i*4 : 12 + i*4])[0]
        for i in range(sub_authority_count)
    ]

    sid_string = f"S-{revision}-{identifier_authority}"
    for sub in sub_authorities:
        sid_string += f"-{sub}"

    return sid_string

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sid2str.py <hex_sid>")
        sys.exit(1)

    print(sid_to_str(sys.argv[1]))
