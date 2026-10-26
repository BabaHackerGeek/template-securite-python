import os

import yara

REGLES_PERSO = r"""
rule Persistence_Run_Key {
    strings:
        $run = "CurrentVersion\\Run" ascii nocase
    condition:
        $run
}

rule Keylogger_Hooks {
    strings:
        $hook = "SetWindowsHookEx" ascii
        $keys = "GetAsyncKeyState" ascii
    condition:
        any of them
}
"""


def yara_scan(data: bytes, rules_dir: str) -> list:
    """ca permet de compiler mes règles et celles du dossier et renvoie ensuite les noms des règles qui correspondent"""
    sources = {"_perso": REGLES_PERSO}
    if os.path.isdir(rules_dir):
        for nom in sorted(os.listdir(rules_dir)):
            if nom.endswith((".yar", ".yara")):
                with open(os.path.join(rules_dir, nom), encoding="utf-8") as f:
                    sources[os.path.splitext(nom)[0]] = f.read()
    regles = yara.compile(sources=sources)
    return sorted({match.rule for match in regles.match(data=data)})