from fpdf import FPDF
from tp1.utils.capture import Capture


class Report:
    def __init__(self, capture: Capture, filename: str, summary: str):
        self.capture = capture
        self.filename = filename
        self.title = "TITRE DU RAPPORT"
        self.summary = summary
        self.array = ""
        self.graph = ""

    def concat_report(self) -> str:

        content = ""
        content += self.title
        content += self.summary
        content += self.array
        content += self.graph

        return content

    def save(self, filename: str) -> None:

        final_content = self.concat_report()
        with open(self.filename, "w") as report:
            report.write(final_content)

    def generate(self, param: str) -> None:

        if param == "graph":
            graph = ""
            self.graph = graph
        elif param == "array":
            array = ""
            self.array = array

    def generer_pdf(protocoles: dict, chemin: str) -> None:
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", size=14)
        pdf.cell(
            0,
            10,
            "Rapport TP1 : paquets par protocole",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.output(chemin)