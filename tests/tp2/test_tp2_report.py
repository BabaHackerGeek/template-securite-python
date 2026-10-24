import json
from pathlib import Path

from src.tp2.utils.report import write_report, write_triage


def test_write_report(tmp_path):
    rapport = {"sha256": "abc123", "score": 0}

    chemin = write_report(rapport, str(tmp_path / "out"))

    assert chemin.endswith("abc123.json")
    assert json.loads(Path(chemin).read_text()) == rapport

def test_write_triage(tmp_path):
    chemin = write_triage({"sha256": "abc"}, str(tmp_path), "sample1_dropper.bin")

    assert Path(chemin).name == "sample1_dropper.bin.triage.json"
    assert json.loads(Path(chemin).read_text()) == {"sha256": "abc"}