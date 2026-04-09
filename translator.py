import socket
from googletrans import Translator

def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except Exception:
        return False

class MyTranslator:
    def __init__(self):
        self.online = is_online()
        if self.online:
            self.trans = Translator()
        else:
            self.trans = None

    def translate(self, text, target_lang):
        if not self.online:
            return None

        mapping = {
            "telugu": "te",
            "hindi": "hi",
            "kannada": "kn",
            "tamil": "ta",
            "chinese": "zh-cn",
            "spanish": "es",
            "english": "en",
            "bengali": "bn",
            "japanese": "ja",
            "marathi": "mr",
            "german": "de",
            "french": "fr",
            "urdu": "ur"
        }

        code = mapping.get(target_lang.lower(), "en")
        result = self.trans.translate(text, dest=code)
        return result.text
