import platform
from io import BytesIO

import pytesseract
from PIL import Image

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def solve_captcha(image_bytes: bytes) -> str:
    """Prétraite l'image (niveaux de gris + seuil pour virer le bruit gris) puis lit le texte avec Tesseract."""
    img = Image.open(BytesIO(image_bytes)).convert("L")
    img = img.point(lambda p: 0 if p < 128 else 255)
    text = pytesseract.image_to_string(img, config="--psm 7")
    return text.strip()
