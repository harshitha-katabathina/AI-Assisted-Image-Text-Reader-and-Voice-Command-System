# tts_engine.py
import os, tempfile
from gtts import gTTS
import pyttsx3
from translator import is_online

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 150)

    def set_voice(self, index=0):
        if index < len(self.voices):
            self.engine.setProperty('voice', self.voices[index].id)

    def speak_offline(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak_online(self, text, lang_code):
        tts = gTTS(text=text, lang=lang_code)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        os.system(f"afplay '{tmp.name}'")
        os.remove(tmp.name)

    def speak(self, text, lang_code='en'):
        if is_online():
            self.speak_online(text, lang_code)
        else:
            self.speak_offline(text)
