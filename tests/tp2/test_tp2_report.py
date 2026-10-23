import json
from pathlib import Path

from src.tp2.utils.report import write_report


def test_write_report(tmp_path):
    rapport = {"sha256": "abc123", "score": 0}

    chemin = write_report(rapport, str(tmp_path / "out"))

    assert chemin.endswith("abc123.json")
    assert json.loads(Path(chemin).read_text()) == rapport