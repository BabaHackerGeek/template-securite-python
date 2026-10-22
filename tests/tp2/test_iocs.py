from src.tp2.utils.iocs import (
    est_ipv4_valide,
    extract_domains,
    extract_ips,
    extract_mutex,
    extract_registry,
    extract_urls,
)


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


def test_extract_ips_dedoublonne():
    texte = "serveur 185.10.20.30 puis 185.10.20.30 et 10.0.0.1"

    assert extract_ips(texte) == ["10.0.0.1", "185.10.20.30"]


def test_extract_ips_ignore_les_adresses_invalides():
    texte = "adresse 999.1.1.1 puis 10.0.0.1"

    assert extract_ips(texte) == ["10.0.0.1"]


def test_est_ipv4_valide():
    assert est_ipv4_valide("185.10.20.30")
    assert not est_ipv4_valide("999.1.1.1")


def test_extract_domains_dedoublonne():
    texte = "c2.example.test puis C2.Example.test et evil.example.org"

    assert extract_domains(texte) == ["c2.example.test", "evil.example.org"]


def test_extract_domains_ignore_les_noms_de_fichiers():
    texte = "http://c2.example.test/gate.php puis config.ini et setup.exe"

    assert extract_domains(texte) == ["c2.example.test"]


def test_extract_mutex_dedoublonne():
    texte = r"CreateMutexA Global\abc123 puis Global\abc123 et Local\xyz"

    assert extract_mutex(texte) == ["Global\\abc123", "Local\\xyz"]


def test_extract_registry_dedoublonne():
    texte = r"RegSetValueEx HKCU\Software\Run\svc puis HKCU\Software\Run\svc et HKLM\System\Foo"

    assert extract_registry(texte) == [r"HKCU\Software\Run\svc", r"HKLM\System\Foo"]