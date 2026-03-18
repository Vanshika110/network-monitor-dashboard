from scapy.all import IP, TCP, UDP, ICMP
from datetime import datetime

def parse_packet(packet):
    """Parse raw packet into structured dict"""
    try:
        ip_layer = packet[IP]
        proto = "OTHER"
        src_port = None
        dst_port = None

        if TCP in packet:
            proto = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            proto = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif ICMP in packet:
            proto = "ICMP"

        return {
            "timestamp": datetime.now().isoformat(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "protocol": proto,
            "src_port": src_port,
            "dst_port": dst_port,
            "size": len(packet)
        }
    except Exception as e:
        print(f"[!] Parse error: {e}")
        return None