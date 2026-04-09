# voice_commands.py
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json

class VoiceControl:
    def __init__(self, model_path="vosk-model", samplerate=16000):
        self.model = Model(model_path)
        self.samplerate = samplerate
        self.rec = KaldiRecognizer(self.model, self.samplerate)

    def listen_once(self, duration=4):
        print("Listening...")
        audio = sd.rec(
            int(duration * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        data = audio.tobytes()

        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            return result.get("text", "")
        else:
            partial = json.loads(self.rec.PartialResult())
            return partial.get("partial", "")
