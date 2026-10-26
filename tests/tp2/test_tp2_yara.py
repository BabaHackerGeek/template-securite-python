from src.tp2.utils.yara_scan import yara_scan


def test_yara_scan(tmp_path):
    # Given : un dossier avec une règle qui cherche "gate.php"
    regles = tmp_path / "rules"
    regles.mkdir()
    (regles / "downloader.yar").write_text(
        'rule Suspicious_Downloader { strings: $a = "gate.php" condition: $a }'
    )

    # When : on scanne un contenu qui contient "gate.php"
    resultat = yara_scan(b"GET /gate.php HTTP/1.1", str(regles))

    # Then : la règle est signalée
    assert resultat == ["Suspicious_Downloader"]


def test_yara_scan_sans_regle(tmp_path):
    regles = tmp_path / "rules"
    regles.mkdir()

    assert yara_scan(b"rien", str(regles)) == []