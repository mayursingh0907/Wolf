
from config.settings import (
    ASSISTANT_NAME,
    VERSION,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE
)

from wolf.brain import WolfBrain


def main():

    print("\n=============================================")
    print(f"       {ASSISTANT_NAME} AI ASSISTANT")
    print(f"             Version {VERSION}")
    print("=============================================\n")

    print(WELCOME_MESSAGE)
    print("Type 'exit' to close WOLF.\n")

    try:
        brain = WolfBrain()
        print("WOLF AI Brain: Connected successfully!\n")

    except Exception as error:
        print(f"Could not initialize AI: {error}")
        return

    while True:

        try:
            user_input = input("YOU: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "stop wolf"]:
                print(f"\nWOLF: {GOODBYE_MESSAGE}")
                break

            print("\nWOLF: Thinking...\n")

            answer = brain.think(user_input)

            print(f"WOLF: {answer}\n")

        except KeyboardInterrupt:
            print(f"\n\nWOLF: {GOODBYE_MESSAGE}")
            break


if __name__ == "__main__":
    main()
