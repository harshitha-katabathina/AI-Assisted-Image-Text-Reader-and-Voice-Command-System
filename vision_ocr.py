# vision_ocr.py
from google.cloud import vision
import io
from PIL import Image

class GoogleVisionOCR:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def extract_text(self, pil_image: Image.Image) -> str:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format="PNG")
        content = img_byte_arr.getvalue()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(response.error.message)

        texts = response.text_annotations
        if texts:
            return texts[0].description.strip()

        return ""
