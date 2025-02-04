from scapy.all import *
import random
import time

flag = "FL1TZ{1CMP_15_601N6_CR4ZY_15N7_17?}"

flag_binary = ''.join(format(ord(char), '08b') for char in flag)
flag_chunks = [flag_binary[i:i+2] for i in range(0, len(flag_binary), 2)]

base_ttl = 64

src_ip = "192.168.1.19"  
dst_ip = "192.168.1.18"  

for chunk in flag_chunks:
    modified_ttl = (base_ttl & 0b11111100) | int(chunk, 2)
    icmp_request = IP(src=src_ip, dst=dst_ip, ttl=modified_ttl)/ICMP()
    send(icmp_request, verbose=False)
    time.sleep(0.5)