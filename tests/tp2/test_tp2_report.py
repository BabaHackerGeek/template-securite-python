import json
from pathlib import Path

from fpdf import FPDF

from src.tp2.utils.report import (
    _section,
    _texte,
    generate_pdf,
    write_report,
    write_triage,
)


def test_write_report(tmp_path):
    rapport = {"sha256": "abc123", "score": 0}

    chemin = write_report(rapport, str(tmp_path / "out"))

    assert chemin.endswith("abc123.json")
    assert json.loads(Path(chemin).read_text()) == rapport


def test_write_triage(tmp_path):
    chemin = write_triage({"sha256": "abc"}, str(tmp_path), "sample1_dropper.bin")

    assert Path(chemin).name == "sample1_dropper.bin.triage.json"
    assert json.loads(Path(chemin).read_text()) == {"sha256": "abc"}


def test_generate_pdf(tmp_path):
    rapport = {
        "sha256": "abc123",
        "md5": "def456",
        "size": 3,
        "entropy": 1.58,
        "file_type": "ASCII text",
        "family_guess": "keylogger",
        "score": 8,
        "mitre_attack": ["T1056"],
        "yara_matches": ["Keylogger_Hooks"],
        "iocs": {"urls": ["http://c2.example.test/gate.php"], "ips": []},
        "flag": "ESGI{test}",
    }
    chemin = tmp_path / "rapport.pdf"

    generate_pdf(rapport, str(chemin))

    assert chemin.read_bytes().startswith(b"%PDF")


def test_texte_remplace_les_caracteres_hors_latin1():
    assert _texte("café €") == "café ?"


def test_section_avance_dans_la_page():
    pdf = FPDF()
    pdf.add_page()
    position_avant = pdf.get_y()

    _section(pdf, "Titre", ["une ligne"])

    assert pdf.get_y() > position_avant