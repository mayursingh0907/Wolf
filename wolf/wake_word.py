
import json
import os
import re

import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel


class WolfWakeWord:

    def __init__(self):

        self.model_path = os.path.join(
            "models",
            "vosk-model-small-en-us-0.15"
        )

        if not os.path.isdir(self.model_path):
            raise FileNotFoundError(
                "Vosk model not found."
            )

        SetLogLevel(-1)

        print("[WAKE WORD] Loading offline model...")

        self.model = Model(self.model_path)

        self.wake_phrases = [
            "wake up wolf",
            "wake up wulf",
            "wake up woof",
            "wake up woolf",
            "wake up wall",
            "wake a wolf"
        ]

        # Help Vosk focus on likely wake-word phrases.
        grammar = self.wake_phrases + [
            "[unk]"
        ]

        self.grammar = json.dumps(grammar)

        print("[WAKE WORD] Model loaded successfully.")

    def normalize(self, text):

        text = text.lower()

        text = re.sub(
            r"[^a-z ]",
            "",
            text
        )

        return " ".join(text.split())

    def is_wake_word(self, text):

        text = self.normalize(text)

        return any(
            phrase in text
            for phrase in self.wake_phrases
        )

    def wait_for_wake_word(self):

        audio = pyaudio.PyAudio()
        stream = None

        try:

            device_info = audio.get_default_input_device_info()

            sample_rate = int(
                device_info["defaultSampleRate"]
            )

            recognizer = KaldiRecognizer(
                self.model,
                sample_rate,
                self.grammar
            )

            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=4000
            )

            stream.start_stream()

            print("\n================================")
            print("       WOLF STANDBY MODE")
            print("================================")
            print("Say: WAKE UP WOLF")
            print("Offline voice detection active.")
            print("Listening for your wake word...")
            print("================================\n")

            last_text = ""

            while True:

                data = stream.read(
                    4000,
                    exception_on_overflow=False
                )

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    detected_text = result.get(
                        "text", ""
                    )

                else:

                    result = json.loads(
                        recognizer.PartialResult()
                    )

                    detected_text = result.get(
                        "partial", ""
                    )

                detected_text = self.normalize(
                    detected_text
                )

                # Show what Vosk hears.
                if detected_text and detected_text != last_text:

                    print("[HEARD]", detected_text)

                    last_text = detected_text

                if self.is_wake_word(detected_text):

                    print("\n[WAKE WORD] WOLF ACTIVATED!")

                    return True

        except KeyboardInterrupt:
            raise

        except Exception as error:

            print("[WAKE WORD ERROR]", repr(error))
            raise

        finally:

            if stream is not None:

                if stream.is_active():
                    stream.stop_stream()

                stream.close()

            audio.terminate()
