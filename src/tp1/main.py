from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.report import Report

import argparse
import json
from collections import Counter
from scapy.all import PcapReader, ARP, TCP, UDP, ICMP

def main():
    total = 0
    compteur = Counter ()

    for pkt in PcapReader("capture.pcap"):
        total += 1
        if pkt.haslayer(ARP):
            compteur["ARP"] += 1
        elif pkt.haslayer(TCP):
            compteur["TCP"] += 1
        elif pkt.haslayer(UDP):
            compteur["UDP"] += 1
        elif pkt.haslayer(ICMP):
            compteur["ICMP"] += 1

    logger.info("Nombre de paquets : %d", total)
    logger.info("Protocoles : %s", dict(compteur))

if __name__ == "__main__":
    main()
