def _texte(valeur) -> str:
    """Rend un texte compatible avec la police Helvetica (latin-1)."""
    return str(valeur).encode("latin-1", "replace").decode("latin-1")


def _section(pdf: FPDF, titre: str, lignes: list) -> None:
    """Écrit un titre de section puis ses lignes."""
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, _texte(titre), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=9)
    for ligne in lignes or ["(aucun)"]:
        pdf.multi_cell(0, 5, _texte(ligne), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def generate_pdf(report: dict, path: str) -> None:
    """Écrit le rapport de triage d'un échantillon dans un PDF lisible."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Rapport de triage", new_x="LMARGIN", new_y="NEXT")
    _section(pdf, "Fichier", [
        f"SHA-256 : {report['sha256']}",
        f"MD5 : {report['md5']}",
        f"Taille : {report['size']} octets",
        f"Entropie : {report['entropy']:.2f}",
        f"Type : {report['file_type']}",
    ])
    _section(pdf, "Verdict", [
        f"Famille : {report['family_guess']}",
        f"Score : {report['score']} / 10",
        f"MITRE ATT&CK : {', '.join(report['mitre_attack'])}",
    ])
    _section(pdf, "Règles YARA", report["yara_matches"])
    for categorie, valeurs in report["iocs"].items():
        _section(pdf, f"IOC : {categorie}", valeurs)
    _section(pdf, "Flag", [report["flag"]] if report["flag"] else [])
    pdf.output(path)