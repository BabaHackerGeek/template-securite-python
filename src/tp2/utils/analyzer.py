import os

from tp2.utils.config import logger
from tp2.utils.iocs import extract_flag, extract_iocs
from tp2.utils.metadata import get_file_metadata
from tp2.utils.report import write_report


def analyze_sample(path: str) -> dict:
    """permet d'analysez un fichier et renvoie le rapport au format attendu"""
    with open(path, "rb") as f:
        data = f.read()
    rapport = get_file_metadata(data)
    rapport["iocs"] = extract_iocs(data)
    rapport["imports"] = []
    rapport["yara_matches"] = []
    rapport["family_guess"] = "unknown"
    rapport["mitre_attack"] = []
    rapport["llm_summary"] = ""
    rapport["score"] = 0
    rapport["flag"] = extract_flag(data.decode("latin-1"))
    return rapport


def process_samples(samples_dir: str, out_dir: str) -> list:
    """analyse chaque fichier du dossier et écrit un JSON par échantillon"""
    chemins = []
    for nom in sorted(os.listdir(samples_dir)):
        path = os.path.join(samples_dir, nom)
        if not os.path.isfile(path):
            continue
        chemins.append(write_report(analyze_sample(path), out_dir))
        logger.info("Analysé : %s", nom)
    return chemins