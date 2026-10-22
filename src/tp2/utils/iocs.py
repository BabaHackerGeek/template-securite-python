import ipaddress
import re

URL = re.compile(r"https?://[^\s\"']+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)
EXTENSIONS_FICHIERS = {"php", "ini", "exe", "dll", "bin", "txt", "html", "js", "py", "sh", "bat", "log"}
MUTEX = re.compile(r"\b(?:Global|Local)\\[\w-]+")
REGISTRY = re.compile(r"\b(?:HKEY_[A-Z_]+|HKCU|HKLM|HKCR|HKU|HKCC)(?:\\[\w.-]+)+")
PATH = re.compile(r"\b[A-Za-z]:\\(?:[\w.-]+\\)*[\w.-]+|(?<![\w:/.])/(?:[\w.-]+/)+[\w.-]+")

def extract_urls(text: str) -> list:
    """Ca renvoie les URLs trouvées dans un texte en enlevantt la ponctuation finale"""
    urls = URL.findall(text)
    return sorted({url.rstrip(".,;:!?)") for url in urls})


def extract_ips(text: str) -> list:
    """Nous renvoie les adresses IPv4 valides trouvées dans un texte"""
    candidats = set(IPV4.findall(text))
    return sorted(ip for ip in candidats if est_ipv4_valide(ip))


def extract_domains(text: str) -> list:
    """fonction qui renvoie les noms de domaine trouvés dans un texte sans les noms de fichiers"""
    domaines = {domaine.lower() for domaine in DOMAIN.findall(text)}
    return sorted(d for d in domaines if d.rsplit(".", 1)[-1] not in EXTENSIONS_FICHIERS)


def extract_mutex(text: str) -> list:
    """Renvoie les noms de mutex (Global\\nom ou Local\\nom) trouvés dans un texte"""
    return sorted(set(MUTEX.findall(text)))


def extract_registry(text: str) -> list:
    """Renvoie les clés de registre (HKCU, HKLM...) trouvées dans un texte"""
    return sorted(set(REGISTRY.findall(text)))


def extract_paths(text: str) -> list:
    """Renvoie les chemins de fichiers (Windows ou Linux) trouvés dans un texte"""
    chemins = PATH.findall(text)
    return sorted({chemin.rstrip(".,;:!?)") for chemin in chemins})


def est_ipv4_valide(adresse: str) -> bool:
    """la fonction nous dit si une chaîne est une adresse IPv4 valide (chaque nombre de 0 à 255)"""
    try:
        ipaddress.IPv4Address(adresse)
    except ValueError:
        return False
    return True


def extract_iocs(data: bytes) -> dict:
    """la fonction extrait tous les IOC d'un contenu binaire, rangés par catégorie."""
    texte = data.decode("latin-1")
    return {
        "domains": extract_domains(texte),
        "ips": extract_ips(texte),
        "urls": extract_urls(texte),
        "mutex": extract_mutex(texte),
        "registry": extract_registry(texte),
    }