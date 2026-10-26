def heuristic_triage(report: dict) -> dict:
    """deduit famille score et techniques MITRE à partir des règles YARA et des IOC"""
    matches = report["yara_matches"]
    famille = "unknown"
    mitre = []
    score = 0
    if "Keylogger_Hooks" in matches:
        famille = "keylogger"
        mitre.append("T1056")
        score += 4
    if "Persistence_Run_Key" in matches or report["iocs"]["registry"]:
        mitre.append("T1547")
        score += 2
    if report["iocs"]["urls"]:
        mitre.append("T1071")
        score += 2
    if report["entropy"] > 7.0:
        score += 2
    return {
        "family_guess": famille,
        "mitre_attack": sorted(set(mitre)),
        "score": min(score, 10),
    }