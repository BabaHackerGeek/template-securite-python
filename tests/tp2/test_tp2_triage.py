from src.tp2.utils.triage import heuristic_triage


def test_heuristic_triage_keylogger():
    rapport = {
        "yara_matches": ["Keylogger_Hooks", "Persistence_Run_Key"],
        "iocs": {"urls": ["http://c2.example.test/gate.php"], "registry": ["HKCU\\x\\Run\\svc"]},
        "entropy": 5.0,
    }

    resultat = heuristic_triage(rapport)

    assert resultat["family_guess"] == "keylogger"
    assert "T1056" in resultat["mitre_attack"]
    assert 0 <= resultat["score"] <= 10


def test_heuristic_triage_fichier_propre():
    rapport = {"yara_matches": [], "iocs": {"urls": [], "registry": []}, "entropy": 1.0}

    resultat = heuristic_triage(rapport)

    assert resultat["family_guess"] == "unknown"
    assert resultat["score"] == 0