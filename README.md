# PingLeak

PoC demonstrating how easily data can be exfiltrated over ICMP.

PingLeak Client: Typically a Windows machine with Python installed.
PingLeak Server: A Linux machine, must run as root, internet-facing, and able to receive ICMP requests.

This PoC has plenty of room for improvement, but it functions as intended.
To use it:
- Run pingleaksrv.py on the Linux server.
- Run pingleakclt.py on the Windows machine. Specify a directory to exfiltrate, a file pattern (can be *.* but that may take a long time), and the public IP of the Linux server.

The PingLeak Client sends the files. The PingLeak Server receives them and recreates the directory structure locally, using the client machine name as an identifier. Note: the process can be lengthy.

This tool is useful for testing whether your firewall detects or blocks this kind of activity. It's also useful for testing your DLP.

What's missing:
- Multiple session management
- Packet sequencing
- A proper ICMP server that replies to ICMP requests (RN, the server only sniffs traffic)
- Checksum computation
- Retry mechanism for checksum failure
- Compression/encryption
- A C-based client to produce a standalone executable
  
_This project is intended for educational and research purposes only. Unauthorized use of this tool to access or exfiltrate data from systems you do not own or have explicit permission to test will probably get you into legal trouble. Use responsibly and stay on the right side of the law._

![image](https://github.com/user-attachments/assets/d1ece201-8faf-43a5-893b-4cc075624ea9)

