import re

URL = re.compile(r"https?://[^\s\"']+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def extract_urls(text: str) -> list:
    """Ca renvoie les URLs trouvées dans un texte en enlevantt la ponctuation finale."""
    urls = URL.findall(text)
    return sorted({url.rstrip(".,;:!?)") for url in urls})


def extract_ips(text: str) -> list:
    """et la ca renvoie les adresses IPv4 trouvées dans un texte"""
    return sorted(set(IPV4.findall(text)))