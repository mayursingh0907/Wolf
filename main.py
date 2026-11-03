
from config.settings import (
    ASSISTANT_NAME,
    VERSION,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE
)

from wolf.brain import WolfBrain
from wolf.voice import WolfVoice
<<<<<<< HEAD
=======
from wolf.wake_word import WolfWakeWord
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)


def main():

    print("\n============================================")
    print(f"       {ASSISTANT_NAME} AI ASSISTANT")
    print(f"              VERSION {VERSION}")
    print("============================================\n")

    print(WELCOME_MESSAGE)

<<<<<<< HEAD
    print("\nWOLF Voice + Gemini AI")
    print("--------------------------------------------")
    print("Press ENTER  : Speak to WOLF")
    print("Type message : Chat with WOLF")
    print("Type exit    : Close WOLF")
    print("--------------------------------------------")

    # Initialize Gemini AI
    try:
        brain = WolfBrain()
        print("\n[SYSTEM] Gemini AI connected successfully!")
=======
    # Initialize Gemini
    try:
        brain = WolfBrain()
        print("[SYSTEM] Gemini AI connected!")
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)

    except Exception as error:
        print("[SYSTEM ERROR] Gemini initialization failed:", error)
        return

<<<<<<< HEAD
    # Initialize voice system
    try:
        voice = WolfVoice()
        print("[SYSTEM] Microphone and speaker initialized!")

    except Exception as error:
        print("[SYSTEM ERROR] Voice initialization failed:", error)
        return

    print("\n[WOLF] All systems operational!")

    voice.speak("Hello! WOLF is online. How can I help you?")

    while True:

        try:
            user_input = input(
                "\nYOU (Enter to speak, or type): "
            ).strip()

            # Exit command
            if user_input.lower() in ["exit", "quit", "stop wolf"]:
                print(f"\nWOLF: {GOODBYE_MESSAGE}")
                voice.speak(GOODBYE_MESSAGE)
                break

            # Empty input activates microphone
            if not user_input:

                user_input = voice.listen()

                if not user_input:
                    continue

                if user_input.lower().strip(" .!?") in [
                    "exit", "quit", "stop wolf"
                ]:
                    print(f"\nWOLF: {GOODBYE_MESSAGE}")
                    voice.speak(GOODBYE_MESSAGE)
                    break

=======
    # Initialize voice
    try:
        voice = WolfVoice()
        print("[SYSTEM] Voice system initialized!")

    except Exception as error:
        print("[SYSTEM ERROR] Voice initialization failed:", error)
        return

    # Initialize wake word
    try:
        wake_word = WolfWakeWord()
        print("[SYSTEM] Wake word initialized!")

    except Exception as error:
        print("[SYSTEM ERROR] Wake word initialization failed:", error)
        return

    print("\n[WOLF] All systems operational!")

    voice.speak("Hello. WOLF is online.")

    try:

        while True:

            # Wait for Wake up WOLF
            wake_word.wait_for_wake_word()

            # Respond to wake word
            voice.speak("Yes, I'm listening.")

            # Listen to the user's question
            user_input = voice.listen()

            if not user_input:
                print("[WOLF] Returning to standby.")
                continue

            command = user_input.lower().strip(" .!?")

            # Exit commands
            if command in [
                "exit",
                "quit",
                "stop wolf",
                "shut down wolf"
            ]:

                voice.speak(GOODBYE_MESSAGE)
                print("[WOLF]", GOODBYE_MESSAGE)
                break

>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)
            # Ask Gemini
            print("\n[WOLF] Thinking...\n")

            answer = brain.think(user_input)

<<<<<<< HEAD
            print(f"WOLF: {answer}")

            # Speak Gemini response
            voice.speak(answer)

        except KeyboardInterrupt:
            print(f"\n\nWOLF: {GOODBYE_MESSAGE}")
            voice.speak(GOODBYE_MESSAGE)
            break
=======
            print("\nWOLF:", answer)

            # Speak Gemini response
            voice.speak(answer)

            print("\n[WOLF] Returning to standby...")

    except KeyboardInterrupt:

        print("\n[WOLF] Shutting down...")

        voice.speak(GOODBYE_MESSAGE)

    except Exception as error:

        print("[WOLF ERROR]", error)
>>>>>>> 418b280 (Complete WOLF Phase 4 voice assistant and wake word)

        except Exception as error:
            print("\n[WOLF ERROR]", error)


if __name__ == "__main__":
    main()
