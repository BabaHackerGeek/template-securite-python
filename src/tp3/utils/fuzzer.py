from pathlib import Path

import requests

from src.tp3.utils.config import logger

DEFAULT_WORDLIST = Path(__file__).parent / "wordlist.txt"


def find_hidden_endpoint(target: str, wordlist_path: Path = DEFAULT_WORDLIST) -> str | None:
    """Teste chaque mot de la wordlist comme chemin sur `target`, renvoie l'URL qui sort du lot."""
    session = requests.Session()

    with open(wordlist_path, encoding="utf-8") as f:
        for word in f:
            path = word.strip()
            if not path:
                continue
            url = f"{target}/{path}"
            r = session.get(url, timeout=5)
            if r.status_code != 404:
                logger.info(f"Endpoint trouvé : {url} (status {r.status_code})")
                return url

    logger.warning("Aucun endpoint trouvé dans la wordlist")
    return None
