from src.tp2.utils.analyzer import analyze_sample, process_samples


def test_analyze_sample(tmp_path):
    # Given : un fichier qui contient une URL
    fichier = tmp_path / "sample.bin"
    fichier.write_bytes(b"http://c2.example.test/gate.php")
    regles = tmp_path / "rules"
    regles.mkdir()

    # When : on analyse ce fichier
    rapport = analyze_sample(str(fichier), str(regles))

    # Then : les infos de base et les IOC sont là
    assert rapport["size"] == 31
    assert rapport["iocs"]["urls"] == ["http://c2.example.test/gate.php"]
    assert rapport["yara_matches"] == []


def test_process_samples(tmp_path):
    # Given : un dossier avec deux fichiers et un sous-dossier
    samples = tmp_path / "samples"
    samples.mkdir()
    (samples / "a.bin").write_bytes(b"aaa")
    (samples / "b.bin").write_bytes(b"bbb")
    (samples / "dossier").mkdir()
    regles = tmp_path / "rules"
    regles.mkdir()

    # When : on traite le dossier
    chemins = process_samples(str(samples), str(regles), str(tmp_path / "out"))

    # Then : un rapport par fichier, le sous-dossier est ignoré
    assert len(chemins) == 2