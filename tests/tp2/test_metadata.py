import pytest

from src.tp2.utils.metadata import entropy, get_file_metadata


def test_sha256():
    resultat = get_file_metadata(b"abc")

    assert resultat["sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert resultat["md5"] == "900150983cd24fb0d6963f7d28e17f72"
    assert resultat["size"] == 3

def test_entropy():
    assert entropy(b"") == 0.0
    assert entropy(b"aaaa") == 0.0
    assert entropy(b"ab") == pytest.approx(1.0)
    assert entropy(bytes(range(256))) == pytest.approx(8.0)