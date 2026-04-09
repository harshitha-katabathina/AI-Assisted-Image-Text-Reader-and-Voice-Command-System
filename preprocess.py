import cv2
from PIL import Image
import numpy as np

def clean_image(frame):

    # convert BGR → RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # noise removal
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # adaptive threshold
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return Image.fromarray(thresh)