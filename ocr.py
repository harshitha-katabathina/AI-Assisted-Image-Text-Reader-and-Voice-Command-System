# ocr.py — Tesseract OCR (NO CRASH VERSION)

import pytesseract
from PIL import Image
import numpy as np

class DeepOCR:
    def __init__(self):
        print("OCR: Using TESSERACT (offline, stable, no-crash)")

    def read_text(self, pil_img):
        # Convert PIL → RGB
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")

        # OCR
        text = pytesseract.image_to_string(pil_img)
        return text.strip()
