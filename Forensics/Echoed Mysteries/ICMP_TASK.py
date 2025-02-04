from scapy.all import *
import time
target_ip = "192.168.1.18"
flag = "FL1TZ{H1DD3N_1N_1CMP_P4CK37S!!!}"
fake_flag = ""
def packet_reply(letter, target_ip):
    packet = IP(dst=target_ip) / ICMP(type="echo-reply", id=1234, seq=1) / letter
    send(packet)

def packet_request(target_ip):
    packet = IP(dst=target_ip) / ICMP(type="echo-request", id=1234, seq=1)
    send(packet)

def send_packets(target_ip) :
    for letter in flag:
            packet_request(target_ip)
            print(f"SENT ICMP REQUEST PACKET")
            time.sleep(1)
            packet_reply(letter, target_ip)
            print(f"SENT ICMP REPLY PACKET WITH LETTER: {letter}")
            time.sleep(2)

send_packets(target_ip)
