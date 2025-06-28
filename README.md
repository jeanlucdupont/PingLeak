# PingLeak
PoC that shows how easy it is to exfiltrate data over ICMP.

PingLeak Client. Usually, a Windows machine. Must have python.
PingLeak Server. A Linux machine. Must run as root. Must be internet facing and accepting ICMP requests.

This PoC has so much room for improvement but it works.
Run the pingleaksrv.py on the Linux server. 
Run pingleakclt.py on the Windows machines. Specify a directory to exfiltrate, a file pattern (It can be *.* but that could be a looong process), and the public IP of the Linux server.

PingLeak Client will send the files. PingLeak Server will receive the file and will recreate locally the directory structure of the client. Each directory structure is identified by a client machine name.
Process can be long. 

This tool is a good test to check if your Firewall detect/block this activity. I would also use it to test the DLP.

What's missing:
- Multiple session management.
- Packet sequencing.
- Having a true ICMP server allowing ICMP reply. RN, we're just sniffing the network on the server side.
- Checksum computation.
- Retry on checksum failure.
- The client should be written in C to generate a standalone executable.
