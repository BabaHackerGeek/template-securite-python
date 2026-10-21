from src.tp2.utils.iocs import extract_urls


def test_extract_urls_dedoublonne():
    # Given : un texte avec la même URL deux fois
    texte = "contact http://c2.example.test/gate.php et http://c2.example.test/gate.php ok"

    # When : on extrait les URLs
    resultat = extract_urls(texte)

    # Then : une seule URL est renvoyée
    assert resultat == ["http://c2.example.test/gate.php"]