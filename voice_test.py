
import speech_recognition as sr
import pyttsx3


def main():
    print("\n================================")
    print("       WOLF VOICE TEST")
    print("================================\n")

    # Test speaker
    print("[1] Initializing speaker...")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)

        engine.say("Hello! I am Wolf. My speaker is working.")
        engine.runAndWait()

        print("[SUCCESS] Speaker is working!\n")

    except Exception as error:
        print("[ERROR] Speaker problem:", error)
        return

    # Test microphone
    print("[2] Checking microphone...")

    recognizer = sr.Recognizer()

    try:
        microphones = sr.Microphone.list_microphone_names()

        if not microphones:
            print("[ERROR] No microphone detected.")
            return

        print("Available microphones:")

        for index, name in enumerate(microphones):
            print(f"{index}: {name}")

        print("\nPlease speak after the listening message.")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(
                source, duration=1
            )

            print("\n[WOLF] Listening...")
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=8
            )

        print("[WOLF] Processing your voice...")

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("\n[SUCCESS] Your voice was recognized!")
        print("YOU SAID:", text)

        engine.say("I heard you say " + text)
        engine.runAndWait()

    except sr.WaitTimeoutError:
        print("[ERROR] No speech detected within 8 seconds.")

    except sr.UnknownValueError:
        print("[ERROR] I could not understand your voice.")

    except sr.RequestError as error:
        print("[ERROR] Speech recognition internet problem:", error)

    except Exception as error:
        print("[ERROR] Microphone problem:", error)

    print("\n================================")
    print("         TEST FINISHED")
    print("================================")


if __name__ == "__main__":
    main()
