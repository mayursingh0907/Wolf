
from config.settings import (
    ASSISTANT_NAME,
    VERSION,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE
)

from wolf.brain import WolfBrain
from wolf.voice import WolfVoice


def main():

    print("\n============================================")
    print(f"       {ASSISTANT_NAME} AI ASSISTANT")
    print(f"              VERSION {VERSION}")
    print("============================================\n")

    print(WELCOME_MESSAGE)

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

    except Exception as error:
        print("[SYSTEM ERROR] Gemini initialization failed:", error)
        return

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

            # Ask Gemini
            print("\n[WOLF] Thinking...\n")

            answer = brain.think(user_input)

            print(f"WOLF: {answer}")

            # Speak Gemini response
            voice.speak(answer)

        except KeyboardInterrupt:
            print(f"\n\nWOLF: {GOODBYE_MESSAGE}")
            voice.speak(GOODBYE_MESSAGE)
            break

        except Exception as error:
            print("\n[WOLF ERROR]", error)


if __name__ == "__main__":
    main()
