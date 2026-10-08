from src.tp1.utils.report import generer_pdf


def test_generer_pdf(tmp_path):
    chemin = tmp_path / "rapport.pdf"

    generer_pdf({"TCP": 10, "UDP": 5}, str(chemin))

    assert chemin.exists()
    assert chemin.read_bytes().startswith(b"%PDF")