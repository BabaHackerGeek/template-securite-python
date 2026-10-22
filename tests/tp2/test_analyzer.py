from src.tp2.utils.analyzer import analyze_sample


def test_analyze_sample(tmp_path):
    # Given : un fichier qui contient une URL
    fichier = tmp_path / "sample.bin"
    fichier.write_bytes(b"http://c2.example.test/gate.php")

    # When : on analyse ce fichier
    rapport = analyze_sample(str(fichier))

    # Then : les infos de base et les IOC sont là
    assert rapport["size"] == 31
    assert rapport["iocs"]["urls"] == ["http://c2.example.test/gate.php"]
    assert rapport["yara_matches"] == []