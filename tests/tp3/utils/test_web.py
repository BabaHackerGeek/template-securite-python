import requests

from src.tp3.utils import web


class FauxReponse:
    def __init__(self, content=b"", json_data=None):
        self.content = content
        self._json = json_data or {}

    def json(self):
        return self._json


def test_breach_web_enchaine_les_etapes(monkeypatch):
    # Given
    monkeypatch.setattr(web, "find_hidden_endpoint", lambda target: f"{target}/internal-panel")
    monkeypatch.setattr(web, "solve_captcha", lambda image_bytes: "WA24A")
    monkeypatch.setattr(requests.Session, "get", lambda self, url, timeout=5: FauxReponse(content=b"image"))
    monkeypatch.setattr(
        requests.Session,
        "post",
        lambda self, url, data=None, timeout=5: FauxReponse(
            json_data={"host": "1.2.3.4", "port": 9090, "key": "deadbeef", "flag1": "ESGI{web_test}"}
        ),
    )

    # When
    host, port, key, flag1 = web.breach_web("http://cible")

    # Then
    assert (host, port, key, flag1) == ("1.2.3.4", 9090, "deadbeef", "ESGI{web_test}")
