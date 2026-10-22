from tp2.utils.iocs import extract_iocs
from tp2.utils.metadata import get_file_metadata


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
    rapport["flag"] = None
    return rapport