import re

URL = re.compile(r"https?://[^\s\"']+")


def extract_urls(text: str) -> list:
    """Ca renvoie les URLs trouvées dans un texte en enlevantt la ponctuation finale."""
    urls = URL.findall(text)
    return sorted({url.rstrip(".,;:!?)") for url in urls})