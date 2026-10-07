import argparse
import json
import os
import re
from collections import Counter, defaultdict
from urllib.parse import unquote

from scapy.all import ARP, DNS, ICMP, IP, TCP, UDP, Ether, PcapReader, Raw

from tp1.utils.config import logger
from tp1.utils.report import generer_pdf

SQLI = re.compile(r"'\s*or\s+1=1|union\s+select|sleep\(", re.IGNORECASE)

def analyser(chemin):
    total = 0
    flag = None
    compteur = Counter()
    ports_par_ip = defaultdict(set)
    attaques = []
    sqli = set()
    arp_ips = defaultdict(set)
    arp_reponses = Counter()
    flags_par_ip = defaultdict(list)

    for pkt in PcapReader(chemin):
        total += 1
        if pkt.haslayer(Ether):
            compteur["Ethernet"] += 1
        if pkt.haslayer(ARP):
            compteur["ARP"] += 1
        if pkt.haslayer(IP):
            compteur["IP"] += 1
        if pkt.haslayer(TCP):
            compteur["TCP"] += 1
        if pkt.haslayer(UDP):
            compteur["UDP"] += 1
        if pkt.haslayer(ICMP):
            compteur["ICMP"] += 1
        if pkt.haslayer(DNS):
            compteur["DNS"] += 1
        if pkt.haslayer(Raw):
            for m in re.finditer(rb"ESGI\{[^}]+\}", pkt[Raw].load):
                if pkt.haslayer(IP):
                    flags_par_ip[pkt[IP].src].append(m.group().decode())
            texte = unquote(pkt[Raw].load.decode(errors="ignore"))
            if pkt[Raw].load.startswith((b"GET ", b"POST ", b"PUT ", b"HEAD ", b"HTTP/")):
                compteur["HTTP"] += 1
            if SQLI.search(texte) and pkt.haslayer(IP):
                sqli.add(pkt[IP].src)
        if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[TCP].flags == "S":
            ports_par_ip[pkt[IP].src].add(pkt[TCP].dport)
        if pkt.haslayer(ARP) and pkt[ARP].op == 2:
            arp_ips[pkt[ARP].psrc].add(pkt[ARP].hwsrc)
            arp_reponses[pkt[ARP].hwsrc] += 1

    logger.info("Nombre de paquets : %d", total)
    logger.info("Protocoles : %s", dict(compteur))

    for ip, ports in ports_par_ip.items():
        if len(ports) >= 15:
            attaques.append({"type": "port_scan", "attacker": ip})
            logger.warning("Scan de ports détecté depuis %s (%d ports)", ip, len(ports))

    for ip in sqli:
        attaques.append({"type": "sql_injection", "attacker": ip})
        logger.warning("Injection SQL détectée depuis %s", ip)
        if flags_par_ip[ip]:
            flag = flags_par_ip[ip][0]

    for ip, macs in arp_ips.items():
        if len(macs) > 1:
            attaquant = max(macs, key=lambda m: arp_reponses[m])
            attaques.append({"type": "arp_spoofing", "attacker": attaquant})
            logger.warning("ARP spoofing détecté depuis %s (IP contestée : %s)", attaquant, ip)

    rapport = {
        "protocols": dict(compteur),
        "attacks": attaques,
        "flag": flag,
    }

    return rapport


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap", required=True)
    parser.add_argument("--out", default="report.json")
    args = parser.parse_args()

    rapport = analyser(args.pcap)

    with open(args.out, "w") as f:
        json.dump(rapport, f, indent=2)

    generer_pdf(rapport["protocols"], os.path.splitext(args.out)[0] + ".pdf")

if __name__ == "__main__":
    main()
