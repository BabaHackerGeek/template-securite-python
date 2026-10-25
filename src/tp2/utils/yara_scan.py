import os

import yara


def yara_scan(data: bytes, rules_dir: str) -> list:
    """Ca permet de compiler les règles du dossier et ca renvoie les noms des règles qui correspondent"""
    fichiers = {
        os.path.splitext(nom)[0]: os.path.join(rules_dir, nom)
        for nom in sorted(os.listdir(rules_dir))
        if nom.endswith((".yar", ".yara"))
    }
    if not fichiers:
        return []
    regles = yara.compile(filepaths=fichiers)
    return sorted({match.rule for match in regles.match(data=data)})