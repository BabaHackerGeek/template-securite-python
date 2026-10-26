import sys

from src.tp2.utils.binary import parse_binary


def test_parse_binary_executable():
    resultat = parse_binary(sys.executable)

    assert len(resultat["sections"]) > 0
    assert isinstance(resultat["imports"], list)


def test_parse_binary_fichier_texte(tmp_path):
    fichier = tmp_path / "note.txt"
    fichier.write_text("pas un binaire")

    assert parse_binary(str(fichier)) == {"imports": [], "exports": [], "sections": []}