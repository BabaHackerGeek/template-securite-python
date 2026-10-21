import ipaddress
import re

URL = re.compile(r"https?://[^\s\"']+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def extract_urls(text: str) -> list:
    """Ca renvoie les URLs trouvées dans un texte en enlevantt la ponctuation finale."""
    urls = URL.findall(text)
    return sorted({url.rstrip(".,;:!?)") for url in urls})


def extract_ips(text: str) -> list:
    """Nous renvoie les adresses IPv4 valides trouvées dans un texte."""
    candidats = set(IPV4.findall(text))
    return sorted(ip for ip in candidats if est_ipv4_valide(ip))


def est_ipv4_valide(adresse: str) -> bool:
    """la fonction nous dit si une chaîne est une adresse IPv4 valide (chaque nombre de 0 à 255)."""
    try:
        ipaddress.IPv4Address(adresse)
    except ValueError:
        return False
    return True