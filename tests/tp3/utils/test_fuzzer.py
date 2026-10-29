import requests

from src.tp3.utils.fuzzer import find_hidden_endpoint


class FauxReponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_find_hidden_endpoint_trouve_le_bon_mot(tmp_path, monkeypatch):
    # Given
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("admin\nsecret\ninternal-panel\n")

    def fake_get(self, url, timeout=5):
        if url.endswith("internal-panel"):
            return FauxReponse(200)
        return FauxReponse(404)

    monkeypatch.setattr(requests.Session, "get", fake_get)

    # When
    result = find_hidden_endpoint("http://cible", wordlist)

    # Then
    assert result == "http://cible/internal-panel"


def test_find_hidden_endpoint_renvoie_none_si_rien_trouve(tmp_path, monkeypatch):
    # Given
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("admin\nsecret\n")

    monkeypatch.setattr(requests.Session, "get", lambda self, url, timeout=5: FauxReponse(404))

    # When
    result = find_hidden_endpoint("http://cible", wordlist)

    # Then
    assert result is None
