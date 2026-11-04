import re

from config.settings import (
    ASSISTANT_NAME,
    VERSION,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE,
)
from wolf.brain import WolfBrain
from wolf.voice import WolfVoice
from wolf.wake_word import WolfWakeWord
from wolf.desktop import WolfDesktop
from wolf.system_control import WolfSystem
from wolf.commands import normalize_command, parse_command


def print_and_speak(voice, message):
    print(f"\n[WOLF] {message}")
    voice.speak(message)


def main():
    print("\n============================================")
    print(f"       {ASSISTANT_NAME} AI ASSISTANT")
    print(f"              VERSION {VERSION}")
    print("============================================\n")
    print(WELCOME_MESSAGE)

    brain = voice = wake_word = desktop = system = None

    try:
        brain = WolfBrain()
        print("[SYSTEM] Gemini connected!")

        voice = WolfVoice()
        print("[SYSTEM] Voice system ready!")

        wake_word = WolfWakeWord()
        print("[SYSTEM] Wake word ready!")

        desktop = WolfDesktop()
        print("[SYSTEM] Desktop control ready!")

        system = WolfSystem()

    except Exception as error:
        print("[SYSTEM ERROR]", error)
        if voice:
            voice.close()
        return

    print("\n[WOLF] All systems operational!")
    voice.speak("Hello. WOLF is online.")

    voice_mode = True
    active_session = False
    pending_google_search = False

    try:
        while True:
            if voice_mode:
                if not active_session:
                    print("\n[WOLF] Waiting for wake word...")
                    wake_word.wait_for_wake_word()
                    active_session = True
                    voice.speak("I'm listening.")

                user_input = voice.listen(timeout=10, phrase_time_limit=7)

                if not user_input:
                    print("\n[WOLF] Returning to standby...")
                    active_session = False
                    pending_google_search = False
                    continue
            else:
                user_input = input("\nYOU: ").strip()
                if not user_input:
                    continue

            command = normalize_command(user_input)

            if command in {"exit", "quit", "stop wolf", "shut down wolf", "goodbye"}:
                print_and_speak(voice, GOODBYE_MESSAGE)
                break

            if command == "keyboard mode":
                voice_mode = False
                active_session = False
                pending_google_search = False
                print_and_speak(voice, "Keyboard mode activated.")
                continue

            if command == "voice mode":
                voice_mode = True
                active_session = False
                pending_google_search = False
                print_and_speak(voice, "Voice mode activated.")
                continue

            # If WOLF just opened Google and asked what to search, treat the
            # next ordinary sentence as the search query. Explicit commands
            # still take priority.
            action, argument = parse_command(command)

            if pending_google_search and action == "unknown":
                result = desktop.search_google(user_input)
                pending_google_search = False
                print_and_speak(voice, result)
                continue

            if action == "set_volume":
                result = system.set_volume(argument)
            elif action == "volume_up":
                result = system.volume_up(argument)
            elif action == "volume_down":
                result = system.volume_down(argument)
            elif action == "mute":
                result = system.mute()
            elif action == "unmute":
                result = system.unmute()
            elif action == "get_volume":
                current = system.get_volume()
                result = (
                    f"Current volume is {current} percent."
                    if current is not None
                    else "Audio control is unavailable."
                )
            elif action == "search_google":
                pending_google_search = False
                result = desktop.search_google(argument)
            elif action == "open_google_search":
                pending_google_search = True
                result = desktop.open_website("google")
                result = "Google opened. What would you like to search?"
            elif action == "open":
                pending_google_search = False
                result = desktop.open_target(argument)
            elif action == "close":
                pending_google_search = False
                result = desktop.close_app(argument)
            elif action == "time":
                from datetime import datetime
                result = "The time is " + datetime.now().strftime("%I:%M %p")
            elif action == "date":
                from datetime import datetime
                result = "Today's date is " + datetime.now().strftime("%d %B %Y")
            elif action == "help":
                result = (
                    "You can open Notepad, Calculator, VS Code, Google, "
                    "YouTube, GitHub or Instagram. You can search Google, "
                    "control volume, ask me questions, or say keyboard mode."
                )
            elif action == "clear_memory":
                result = brain.clear_memory()
            else:
                print("\n[WOLF] Thinking...")
                result = brain.think(user_input)

            print_and_speak(voice, result)

    except KeyboardInterrupt:
        print("\n[WOLF] Shutting down...")
        if voice:
            voice.speak(GOODBYE_MESSAGE)
    except Exception as error:
        print("\n[WOLF ERROR]", error)
    finally:
        if voice:
            voice.close()


if __name__ == "__main__":
    main()
