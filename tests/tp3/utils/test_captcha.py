import io

from PIL import Image

from src.tp3.utils.captcha import solve_captcha


def _image_vide() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), "white").save(buf, "PNG")
    return buf.getvalue()


def test_solve_captcha_nettoie_le_texte(monkeypatch):
    # Given
    monkeypatch.setattr(
        "src.tp3.utils.captcha.pytesseract.image_to_string",
        lambda img, config="": "  WA24A  \n",
    )

    # When
    result = solve_captcha(_image_vide())

    # Then
    assert result == "WA24A"
