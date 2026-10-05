from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.report import Report

import argparse
import json
from collections import Counter
from scapy.all import PcapReader, ARP, TCP, UDP, ICMP

def main():
    total = 0

    for pkt in PcapReader("capture.pcap"):
        total += 1

    logger.info("Nombre de paquets : %d", total)

if __name__ == "__main__":
       main()
