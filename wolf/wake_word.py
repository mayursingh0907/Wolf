import json
import re
from pathlib import Path

import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel


class WolfWakeWord:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        self.model_path = project_root / "models" / "vosk-model-small-en-us-0.15"

        if not self.model_path.is_dir():
            raise FileNotFoundError(
                f"Vosk model not found at: {self.model_path}"
            )

        SetLogLevel(-1)
        print("[WAKE WORD] Loading offline model...")
        self.model = Model(str(self.model_path))

        self.wake_phrases = [
            "wake up wolf",
            "wake up wulf",
            "wake up woof",
            "wake up woolf",
        ]
        self.grammar = json.dumps(self.wake_phrases + ["[unk]"])
        print("[WAKE WORD] Model loaded successfully.")

    @staticmethod
    def normalize(text):
        text = (text or "").lower()
        text = re.sub(r"[^a-z ]", " ", text)
        return " ".join(text.split())

    def is_wake_word(self, text):
        normalized = self.normalize(text)
        return any(phrase in normalized for phrase in self.wake_phrases)

    def wait_for_wake_word(self):
        audio = pyaudio.PyAudio()
        stream = None

        try:
            device_info = audio.get_default_input_device_info()
            sample_rate = int(device_info["defaultSampleRate"])
            recognizer = KaldiRecognizer(self.model, sample_rate, self.grammar)

            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=4000,
            )
            stream.start_stream()

            print("\n================================")
            print("       WOLF STANDBY MODE")
            print("================================")
            print("Say: WAKE UP WOLF")
            print("Offline wake-word detection active.")
            print("================================\n")

            last_displayed = ""

            while True:
                data = stream.read(4000, exception_on_overflow=False)

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    heard = result.get("text", "")
                else:
                    result = json.loads(recognizer.PartialResult())
                    heard = result.get("partial", "")

                heard = self.normalize(heard)

                # Suppress blank/unknown fragments to keep the console clean.
                if heard and heard != "[unk]" and heard != last_displayed:
                    if any(word in heard for word in ("wake", "wolf", "wulf", "woof")):
                        print("[HEARD]", heard)
                    last_displayed = heard

                if self.is_wake_word(heard):
                    print("\n[WAKE WORD] WOLF ACTIVATED!")
                    return True

        finally:
            if stream is not None:
                try:
                    if stream.is_active():
                        stream.stop_stream()
                finally:
                    stream.close()
            audio.terminate()
