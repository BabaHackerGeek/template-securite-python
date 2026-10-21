import ipaddress
import re

URL = re.compile(r"https?://[^\s\"']+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)

def extract_urls(text: str) -> list:
    """Ca renvoie les URLs trouvées dans un texte en enlevantt la ponctuation finale."""
    urls = URL.findall(text)
    return sorted({url.rstrip(".,;:!?)") for url in urls})


def extract_ips(text: str) -> list:
    """Nous renvoie les adresses IPv4 valides trouvées dans un texte."""
    candidats = set(IPV4.findall(text))
    return sorted(ip for ip in candidats if est_ipv4_valide(ip))


def extract_domains(text: str) -> list:
    """fonction qui renvoie les noms de domaine trouvés dans un texte en minuscules"""
    return sorted({domaine.lower() for domaine in DOMAIN.findall(text)})


def est_ipv4_valide(adresse: str) -> bool:
    """la fonction nous dit si une chaîne est une adresse IPv4 valide (chaque nombre de 0 à 255)."""
    try:
        ipaddress.IPv4Address(adresse)
    except ValueError:
        return False
    return True