from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.report import Report

import argparse
import json
from collections import Counter, defaultdict
from scapy.all import PcapReader, ARP, TCP, UDP, ICMP, Raw, IP
import re

def main():
    total = 0
    flag = None
    compteur = Counter()
    ports_par_ip = defaultdict(set)
    attaques = []

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
        if pkt.haslayer(Raw):
            trouve = re.search(rb"ESGI\{[^}]+\}", pkt[Raw].load)
            if trouve:
                flag = trouve.group().decode()
        if pkt.haslayer(IP) and pkt.haslayer(TCP):
            if pkt[TCP].flags == "S":
                ports_par_ip[pkt[IP].src].add(pkt[TCP].dport)

    logger.info("Nombre de paquets : %d", total)
     logger.info("Protocoles : %s", dict(compteur))

    for ip, ports in ports_par_ip.items():
        if len(ports) >= 15:
            attaques.append({"type": "port_scan", "attacker": ip})
             logger.warning("Scan de ports détecté depuis %s (%d ports)", ip, len(ports))

    rapport = {
        "protocols": dict(compteur),
          "attacks":  attaques,
        "flag": flag,
    }

    with open("report.json", "w") as f:
        json.dump(rapport, f, indent=2)


if __name__ == "__main__":
    main()
