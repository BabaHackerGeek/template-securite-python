import os

from tp2.utils.binary import parse_binary
from tp2.utils.config import logger
from tp2.utils.iocs import extract_flag, extract_iocs
from tp2.utils.metadata import get_file_metadata
from tp2.utils.report import generate_pdf, write_report, write_triage
from tp2.utils.triage import heuristic_triage
from tp2.utils.yara_scan import yara_scan


def analyze_sample(path: str, rules_dir: str) -> dict:
    """permet d'analyser un fichier et renvoie le rapport au format attendu"""
    with open(path, "rb") as f:
        data = f.read()
    rapport = get_file_metadata(data)
    rapport["iocs"] = extract_iocs(data)
    rapport["imports"] = parse_binary(path)["imports"]
    rapport["yara_matches"] = yara_scan(data, rules_dir)
    rapport.update(heuristic_triage(rapport))
    rapport["llm_summary"] = ""
    rapport["flag"] = extract_flag(data.decode("latin-1"))
    return rapport


def process_samples(samples_dir: str, rules_dir: str, out_dir: str) -> list:
    """analyse chaque fichier du dossier et écrit un JSON par échantillon"""
    chemins = []
    for nom in sorted(os.listdir(samples_dir)):
        path = os.path.join(samples_dir, nom)
        if not os.path.isfile(path):
            continue
        rapport = analyze_sample(path, rules_dir)
        chemins.append(write_report(rapport, out_dir))
        write_triage(rapport, out_dir, nom)
        generate_pdf(rapport, os.path.join(out_dir, f"{nom}.pdf"))
        logger.info("Analysé : %s", nom)
    return chemins