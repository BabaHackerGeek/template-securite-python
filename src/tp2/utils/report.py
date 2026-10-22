import json
import os


def write_report(report: dict, out_dir: str) -> str:
    """ecrit le rapport dans out_dir sous le nom <sha256>.json et renvoie le chemin"""
    os.makedirs(out_dir, exist_ok=True)
    chemin = os.path.join(out_dir, f"{report['sha256']}.json")
    with open(chemin, "w") as f:
        json.dump(report, f, indent=2)
    return chemin