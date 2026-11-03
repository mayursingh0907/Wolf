
<<<<<<< HEAD
import speech_recognition as sr
import pyttsx3
=======
import subprocess
import speech_recognition as sr
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)


class WolfVoice:

    def __init__(self):
<<<<<<< HEAD
        # Initialize microphone recognition
        self.recognizer = sr.Recognizer()

        # Initialize Windows speech engine
        self.engine = pyttsx3.init()

        # Configure speaking speed
        self.engine.setProperty("rate", 165)

        # Configure speaking volume
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        """Convert text into spoken audio."""
=======
        self.recognizer = sr.Recognizer()

        print("[VOICE] Windows speech system initialized.")

    def speak(self, text):
        """Use Windows built-in speech engine."""
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)

        if not text:
            return

<<<<<<< HEAD
        try:
            print("\n[WOLF VOICE] Speaking...")
            self.engine.say(text)
            self.engine.runAndWait()
=======
        # Safely pass text as an environment variable
        # instead of inserting it into a PowerShell command.
        env = None

        import os
        env = os.environ.copy()
        env["WOLF_SPEECH_TEXT"] = str(text)

        script = """
Add-Type -AssemblyName System.Speech

$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Volume = 100
$speaker.Rate = 0
$speaker.Speak($env:WOLF_SPEECH_TEXT)
$speaker.Dispose()
"""

        try:
            print("[WOLF VOICE] Speaking...")

            subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    script
                ],
                env=env,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )

            print("[VOICE] Speech completed.")
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)

        except Exception as error:
            print("[VOICE ERROR]", error)

    def listen(self):
<<<<<<< HEAD
        """Listen to the microphone and convert speech into text."""
=======
        """Listen to microphone and convert speech into text."""
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)

        try:
            with sr.Microphone() as source:

                print("\n[WOLF] Adjusting microphone...")
<<<<<<< HEAD
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
=======

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)
                )

                print("[WOLF] Listening... Speak now!")

                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=12
                )

            print("[WOLF] Understanding your voice...")

            text = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("[YOU SAID]", text)

            return text

        except sr.WaitTimeoutError:
            print("[WOLF] I didn't hear anything.")
            return None

        except sr.UnknownValueError:
            print("[WOLF] Sorry, I couldn't understand.")
            return None

        except sr.RequestError as error:
<<<<<<< HEAD
            print("[WOLF] Speech recognition connection error:", error)
=======
            print("[WOLF] Recognition connection error:", error)
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)
            return None

        except Exception as error:
            print("[WOLF] Microphone error:", error)
            return None
