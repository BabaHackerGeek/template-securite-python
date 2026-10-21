from src.tp2.utils.iocs import extract_urls


def test_extract_urls_dedoublonne():
    """Je me suis basé sur la slide en page 8 ici qui montre les 3 étapes"""
    # Given : un texte avec la même URL deux fois
    texte = "contact http://c2.example.test/gate.php et http://c2.example.test/gate.php ok"

    # When : on extrait les URLs
    resultat = extract_urls(texte)

    # Then : une seule URL est renvoyée
    assert resultat == ["http://c2.example.test/gate.php"]


def test_extract_urls_sans_url():
    assert extract_urls("rien d'intéressant ici") == []


def test_extract_urls_http_et_https():
    texte = "http://a.example.test et https://b.example.test/x"

    assert extract_urls(texte) == ["http://a.example.test", "https://b.example.test/x"]


def test_extract_urls_ponctuation_finale():
    texte = "voir http://c2.example.test/gate.php. puis (https://b.example.test/x), fin"

    assert extract_urls(texte) == [
        "http://c2.example.test/gate.php",
        "https://b.example.test/x",
    ]
