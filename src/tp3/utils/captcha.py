import platform
from io import BytesIO

import pytesseract
from PIL import Image

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TESSERACT_CONFIG = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def solve_captcha(image_bytes: bytes) -> str:
    """Agrandit l'image, la seuille en noir/blanc pour virer le bruit, puis la lit avec Tesseract."""
    img = Image.open(BytesIO(image_bytes)).convert("L")
    img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
    img = img.point(lambda p: 0 if p < 140 else 255)
    text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
    return text.strip()