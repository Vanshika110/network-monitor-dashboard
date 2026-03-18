from scapy.all import sniff, IP, TCP, UDP, ICMP
from parser import parse_packet
from db import save_packet
import threading

def start_capture(interface=None):
    """Start packet capture on given interface"""
    print(f"[*] Starting capture on interface: {interface or 'default'}")
    sniff(
        iface=interface,
        prn=handle_packet,
        store=False,
        filter="ip"
    )

def handle_packet(packet):
    """Process each captured packet"""
    if IP in packet:
        parsed = parse_packet(packet)
        if parsed:
            save_packet(parsed)

if __name__ == "__main__":
    start_capture()