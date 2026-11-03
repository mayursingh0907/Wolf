
import speech_recognition as sr
import pyttsx3


class WolfVoice:

    def __init__(self):
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

        if not text:
            return

        try:
            print("\n[WOLF VOICE] Speaking...")
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as error:
            print("[VOICE ERROR]", error)

    def listen(self):
        """Listen to the microphone and convert speech into text."""

        try:
            with sr.Microphone() as source:

                print("\n[WOLF] Adjusting microphone...")
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
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
            print("[WOLF] Speech recognition connection error:", error)
            return None

        except Exception as error:
            print("[WOLF] Microphone error:", error)
            return None
