from PIL import Image
from pdf2image import convert_from_path

def read_image_file(path):
    img = Image.open(path)
    img = img.convert("RGB")
    return img

def read_pdf_first_page(path):
    pages = convert_from_path(path, first_page=1, last_page=1)
    if pages:
        return pages[0]
    return None

def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()